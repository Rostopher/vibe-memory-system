from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from install_to_project import install_project
from validate_memory_docs import EXPECTED_FILES, validate_memory_docs


class MemoryDocsToolsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.source = self.root / "source"
        self.target = self.root / "target"
        self.source.mkdir()
        self.target.mkdir()
        self._make_template_source()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _make_template_source(self) -> None:
        for relative, spec in EXPECTED_FILES.items():
            path = self.source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            body = (
                "---\n"
                f"layer: {spec.layer}\n"
                f"update_mode: {spec.update_mode}\n"
                'role: "test role"\n'
                'read_when: "test read condition"\n'
                'not_for: "test exclusion"\n'
                "---\n\n"
                f"# {path.stem}\n\nSee `<memory-docs>/STATUS.md`.\n"
            )
            if relative == Path("DIRS.md"):
                body += "\n`detail_mem/` `SHORT_MEMORY/` `archive/`\n"
            path.write_text(body, encoding="utf-8")

        (self.source / "AGENTS.md").write_text("template agent guide\n", encoding="utf-8")
        skill = self.source / ".claude" / "skills" / "sample-skill"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: sample-skill\ndescription: test\n---\n",
            encoding="utf-8",
        )
        tools = self.source / "scripts"
        tools.mkdir()
        (tools / "validate_memory_docs.py").write_text(
            "# project-local validator fixture\n",
            encoding="utf-8",
        )

    def test_install_rewrites_memory_docs_placeholder(self) -> None:
        install_project(
            source_root=self.source,
            target=self.target,
            component="memory-docs",
            force=False,
            replace_agents=False,
        )

        overview = (self.target / "memory-docs" / "OVERVIEW.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("memory-docs/STATUS.md", overview)
        self.assertNotIn("<memory-docs>/", overview)
        errors, _ = validate_memory_docs(self.target)
        self.assertEqual([], errors)

    def test_existing_agents_is_preserved_without_explicit_replace(self) -> None:
        agents = self.target / "AGENTS.md"
        agents.write_text("project-specific guide\n", encoding="utf-8")

        install_project(
            source_root=self.source,
            target=self.target,
            component="all",
            force=False,
            replace_agents=False,
        )

        self.assertEqual("project-specific guide\n", agents.read_text(encoding="utf-8"))
        self.assertTrue(
            (self.target / ".claude" / "skills" / "sample-skill" / "SKILL.md").is_file()
        )
        self.assertTrue(
            (self.target / ".memory-docs-tools" / "validate_memory_docs.py").is_file()
        )

    def test_force_refresh_preserves_historical_memory(self) -> None:
        install_project(
            source_root=self.source,
            target=self.target,
            component="memory-docs",
            force=False,
            replace_agents=False,
        )
        custom = self.target / "memory-docs" / "archive" / "note.md"
        custom.write_text("keep me\n", encoding="utf-8")

        install_project(
            source_root=self.source,
            target=self.target,
            component="memory-docs",
            force=True,
            replace_agents=False,
        )

        self.assertEqual("keep me\n", custom.read_text(encoding="utf-8"))

    def test_force_refresh_refuses_custom_directories(self) -> None:
        install_project(
            source_root=self.source,
            target=self.target,
            component="memory-docs",
            force=False,
            replace_agents=False,
        )
        custom = self.target / "memory-docs" / "design" / "note.md"
        custom.parent.mkdir()
        custom.write_text("keep me\n", encoding="utf-8")

        with self.assertRaisesRegex(RuntimeError, "custom memory directories"):
            install_project(
                source_root=self.source,
                target=self.target,
                component="memory-docs",
                force=True,
                replace_agents=False,
            )

        self.assertEqual("keep me\n", custom.read_text(encoding="utf-8"))

    def test_validator_rejects_wrong_update_mode(self) -> None:
        install_project(
            source_root=self.source,
            target=self.target,
            component="memory-docs",
            force=False,
            replace_agents=False,
        )
        status = self.target / "memory-docs" / "STATUS.md"
        status.write_text(
            status.read_text(encoding="utf-8").replace(
                "update_mode: rewrite", "update_mode: append"
            ),
            encoding="utf-8",
        )

        errors, _ = validate_memory_docs(self.target)
        self.assertTrue(any("STATUS.md" in error and "update_mode" in error for error in errors))

    def test_validator_can_explicitly_allow_literal_template_token(self) -> None:
        install_project(
            source_root=self.source,
            target=self.target,
            component="memory-docs",
            force=False,
            replace_agents=False,
        )
        status = self.target / "memory-docs" / "STATUS.md"
        status.write_text(
            status.read_text(encoding="utf-8") + "\nDiscuss `<memory-docs>/` literally.\n",
            encoding="utf-8",
        )

        _, warnings = validate_memory_docs(self.target)
        self.assertTrue(any("<memory-docs>/" in warning for warning in warnings))
        _, allowed_warnings = validate_memory_docs(
            self.target,
            allow_template_tokens=True,
        )
        self.assertFalse(any("<memory-docs>/" in warning for warning in allowed_warnings))


if __name__ == "__main__":
    unittest.main()
