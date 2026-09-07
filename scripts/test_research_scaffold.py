"""Behavioral checks for scaffold creation, preservation, and skill distribution."""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from install_to_project import install_project


SOURCE_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = SOURCE_ROOT / "skills" / "research-scaffold"
SCRIPT = SKILL_ROOT / "scripts" / "init_research_scaffold.py"
SPEC = importlib.util.spec_from_file_location("research_scaffold", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
scaffold = importlib.util.module_from_spec(SPEC)
previous_bytecode_setting = sys.dont_write_bytecode
try:
    sys.dont_write_bytecode = True
    SPEC.loader.exec_module(scaffold)
finally:
    sys.dont_write_bytecode = previous_bytecode_setting


class ResearchScaffoldTest(unittest.TestCase):
    def setUp(self) -> None:
        self.sandbox = tempfile.TemporaryDirectory(prefix="research-scaffold-")
        self.addCleanup(self.sandbox.cleanup)
        self.root = Path(self.sandbox.name).resolve()
        self.target = self.root / "研究 project"

    def init(self, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            return scaffold.init_scaffold(self.target, **kwargs)

    def write(self, relative: str, content: str = "project-specific content\n") -> Path:
        path = self.target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_default_creation_is_shallow_and_idempotent(self) -> None:
        written = self.init()
        self.assertEqual(len(written), 10)
        for name in scaffold.DIRECTORY_PURPOSES:
            self.assertEqual(list((self.target / name).iterdir()), [self.target / name / "README.md"])
        self.assertFalse((self.target / "memory-docs").exists())
        self.assertFalse((self.target / "docs").exists())
        before = {path: path.read_bytes() for path in written}
        self.assertEqual(self.init(), [])
        self.assertEqual(before, {path: path.read_bytes() for path in written})

    def test_selected_directories_work_via_cli_from_another_directory(self) -> None:
        result = subprocess.run(
            [sys.executable, "-X", "utf8", "-B", str(SCRIPT), str(self.target), "--directories", "notes", "modules"],
            cwd=self.root, capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.target / "notes" / "README.md").is_file())
        self.assertTrue((self.target / "modules" / "README.md").is_file())
        self.assertFalse((self.target / "papers").exists())
        self.assertFalse((self.root / "modules").exists())

    def test_refresh_preserves_memory_rules_and_unselected_directories(self) -> None:
        protected = [self.write(name) for name in (
            "AGENTS.md", "memory-docs/INDEX.md", "memory-docs/STATUS.md", "notes/README.md",
        )]
        replaceable = [self.write(name) for name in ("README.md", ".gitignore", ".ignore", "modules/README.md")]
        before = {path: path.read_bytes() for path in protected + replaceable}
        self.assertEqual(self.init(directories=["modules"]), [])
        self.assertEqual(before, {path: path.read_bytes() for path in before})
        self.init(force=True, directories=["modules"])
        for path in protected:
            self.assertEqual(path.read_bytes(), before[path])
        for path in replaceable:
            self.assertNotEqual(path.read_bytes(), before[path])

    def test_legacy_memory_is_reused_without_installing_parallel_memory(self) -> None:
        existing = [self.write(name) for name in ("docs/README.md", "docs/STATUS.md", "docs/CONVENTIONS.md")]
        before = {path: path.read_bytes() for path in existing}
        self.init(memory_system=self.root / "unused-source", directories=["notes"])
        self.assertFalse((self.target / "memory-docs").exists())
        self.assertEqual(before, {path: path.read_bytes() for path in existing})
        self.assertEqual(scaffold.find_memory_root(self.target), self.target / "docs")
        self.assertIn("docs/README.md", (self.target / "README.md").read_text(encoding="utf-8"))

    def test_explicit_custom_memory_root_is_reused(self) -> None:
        entry = self.write("knowledge/INDEX.md")
        self.init(memory_root=Path("knowledge"), directories=["ideas"])
        self.assertFalse((self.target / "memory-docs").exists())
        self.assertEqual(entry.read_text(encoding="utf-8"), "project-specific content\n")
        self.assertIn("knowledge/INDEX.md", (self.target / "README.md").read_text(encoding="utf-8"))

    def test_unknown_custom_root_is_rejected_before_writing(self) -> None:
        with self.assertRaises(ValueError):
            self.init(memory_root=Path("missing-memory"))
        self.assertFalse(self.target.exists())

    def test_force_cannot_overwrite_memory_in_a_selected_scaffold_directory(self) -> None:
        entry = self.write("notes/README.md", "This is the custom memory entry.\n")
        with self.assertRaises(ValueError):
            self.init(force=True, memory_root=Path("notes"), directories=["notes", "modules"])
        self.assertEqual(entry.read_text(encoding="utf-8"), "This is the custom memory entry.\n")
        self.assertFalse((self.target / "modules").exists())

    def test_invalid_source_is_rejected_before_writing(self) -> None:
        with self.assertRaises(FileNotFoundError):
            self.init(memory_system=self.root / "missing-source")
        self.assertFalse(self.target.exists())

    def test_conflicting_destination_is_rejected_before_partial_scaffolding(self) -> None:
        occupied = self.write("modules")
        with self.assertRaises(NotADirectoryError):
            self.init(directories=["notes", "modules"])
        self.assertEqual(occupied.read_text(encoding="utf-8"), "project-specific content\n")
        self.assertFalse((self.target / "notes").exists())

    def test_multiple_memory_roots_require_selection(self) -> None:
        self.write("memory-docs/INDEX.md")
        self.write("docs/STATUS.md")
        self.write("docs/OVERVIEW.md")
        with self.assertRaises(ValueError):
            self.init()
        self.assertFalse((self.target / "notes").exists())
        self.init(memory_root=Path("docs"), directories=["notes"])
        self.assertTrue((self.target / "notes").is_dir())

    def test_real_memory_install_preserves_ordinary_docs_and_project_agents(self) -> None:
        docs = self.write("docs/README.md", "Public documentation, not project memory.\n")
        agents = self.write("AGENTS.md", "Existing project rules.\n")
        result = subprocess.run(
            [sys.executable, "-X", "utf8", "-B", str(SCRIPT), str(self.target), "--memory-system", str(SOURCE_ROOT), "--directories", "modules"],
            cwd=self.root, capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.target / "memory-docs" / "INDEX.md").is_file())
        self.assertTrue((self.target / "memory-docs" / "detail_mem" / "DECISIONS.md").is_file())
        self.assertEqual(docs.read_text(encoding="utf-8"), "Public documentation, not project memory.\n")
        self.assertEqual(agents.read_text(encoding="utf-8"), "Existing project rules.\n")
        self.assertFalse((self.target / ".agents").exists())

    def test_installer_distributes_identical_skill_to_both_targets(self) -> None:
        self.target.mkdir()
        install_project(source_root=SOURCE_ROOT, target=self.target, component="skills", force=False, replace_agents=False, skill_target="both")
        expected = {
            path.relative_to(SKILL_ROOT): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in SKILL_ROOT.rglob("*") if path.is_file()
        }
        for prefix in (".agents", ".claude"):
            installed = self.target / prefix / "skills" / "research-scaffold"
            actual = {
                path.relative_to(installed): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in installed.rglob("*") if path.is_file()
            }
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
