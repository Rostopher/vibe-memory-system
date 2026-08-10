from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from install_to_project import install_project
from sync_skills import MANIFEST_FILENAME, SkillSyncConflict, check_skill_targets
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
        skill = self.source / "skills" / "sample-skill"
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

    def test_unrelated_root_index_does_not_shadow_memory_docs(self) -> None:
        root_index = self.target / "INDEX.md"
        root_index.write_text(
            "# Product index\n\nThis is application content, not project memory.\n",
            encoding="utf-8",
        )

        install_project(
            source_root=self.source,
            target=self.target,
            component="memory-docs",
            force=False,
            replace_agents=False,
        )

        errors, _ = validate_memory_docs(self.target)
        self.assertEqual([], errors)
        self.assertTrue((self.target / "memory-docs" / "STATUS.md").is_file())
        self.assertEqual(
            "# Product index\n\nThis is application content, not project memory.\n",
            root_index.read_text(encoding="utf-8"),
        )

    def test_install_refuses_symlinked_memory_root(self) -> None:
        external = self.root / "external-memory"
        memory_root = self.target / "memory-docs"
        memory_root.symlink_to(external, target_is_directory=True)

        with self.assertRaisesRegex(RuntimeError, "symbolic link"):
            install_project(
                source_root=self.source,
                target=self.target,
                component="memory-docs",
                force=False,
                replace_agents=False,
            )

        self.assertFalse(external.exists())

    def test_install_refuses_broken_nested_managed_symlinks(self) -> None:
        cases = (
            (
                "memory leaf",
                self.target / "memory-docs" / "OVERVIEW.md",
                self.root / "external-overview.md",
                "memory-docs",
            ),
            (
                "memory directory",
                self.target / "memory-docs" / "archive",
                self.root / "external-archive",
                "memory-docs",
            ),
            (
                "agents",
                self.target / "AGENTS.md",
                self.root / "external-agents.md",
                "memory-docs",
            ),
            (
                "validator",
                self.target / ".memory-docs-tools" / "validate_memory_docs.py",
                self.root / "external-validator.py",
                "tools",
            ),
        )
        for index, (label, link, external, component) in enumerate(cases):
            with self.subTest(path=label):
                target = self.root / f"symlink-target-{index}"
                target.mkdir()
                relative_link = link.relative_to(self.target)
                actual_link = target / relative_link
                actual_link.parent.mkdir(parents=True, exist_ok=True)
                actual_link.symlink_to(external, target_is_directory=label.endswith("directory"))

                with self.assertRaisesRegex(RuntimeError, "symbolic link"):
                    install_project(
                        source_root=self.source,
                        target=target,
                        component=component,
                        force=False,
                        replace_agents=False,
                    )

                self.assertFalse(external.exists())

    def test_existing_agents_is_preserved_without_explicit_replace(self) -> None:
        agents = self.target / "AGENTS.md"
        agents.write_text("project-specific guide\n", encoding="utf-8")

        install_project(
            source_root=self.source,
            target=self.target,
            component="all",
            force=False,
            replace_agents=False,
            skill_target="both",
        )

        self.assertEqual("project-specific guide\n", agents.read_text(encoding="utf-8"))
        self.assertTrue(
            (self.target / ".claude" / "skills" / "sample-skill" / "SKILL.md").is_file()
        )
        self.assertTrue(
            (self.target / ".agents" / "skills" / "sample-skill" / "SKILL.md").is_file()
        )
        self.assertTrue(
            (self.target / ".memory-docs-tools" / "validate_memory_docs.py").is_file()
        )

    def test_existing_agents_is_replaced_only_when_explicit(self) -> None:
        agents = self.target / "AGENTS.md"
        agents.write_text("project-specific guide\n", encoding="utf-8")

        install_project(
            source_root=self.source,
            target=self.target,
            component="memory-docs",
            force=False,
            replace_agents=True,
        )

        self.assertEqual("template agent guide\n", agents.read_text(encoding="utf-8"))

    def test_skills_can_install_for_claude_only(self) -> None:
        install_project(
            source_root=self.source,
            target=self.target,
            component="skills",
            force=False,
            replace_agents=False,
            skill_target="claude",
        )

        self.assertTrue(
            (self.target / ".claude" / "skills" / "sample-skill" / "SKILL.md").is_file()
        )
        self.assertFalse((self.target / ".agents").exists())

    def test_skills_can_install_for_codex_only(self) -> None:
        install_project(
            source_root=self.source,
            target=self.target,
            component="skills",
            force=False,
            replace_agents=False,
            skill_target="codex",
        )

        self.assertTrue(
            (self.target / ".agents" / "skills" / "sample-skill" / "SKILL.md").is_file()
        )
        self.assertFalse((self.target / ".claude").exists())

    def test_skills_install_for_both_targets_when_explicit(self) -> None:
        install_project(
            source_root=self.source,
            target=self.target,
            component="skills",
            force=False,
            replace_agents=False,
            skill_target="both",
        )

        for agent_dir in (".claude", ".agents"):
            self.assertTrue(
                (
                    self.target
                    / agent_dir
                    / "skills"
                    / "sample-skill"
                    / "SKILL.md"
                ).is_file()
            )

    def test_skills_require_an_explicit_target(self) -> None:
        with self.assertRaisesRegex(ValueError, "skill_target"):
            install_project(
                source_root=self.source,
                target=self.target,
                component="skills",
                force=False,
                replace_agents=False,
            )

        self.assertFalse((self.target / ".claude").exists())
        self.assertFalse((self.target / ".agents").exists())

    def test_project_skill_install_writes_receipts_and_detects_drift(self) -> None:
        install_project(
            source_root=self.source,
            target=self.target,
            component="skills",
            force=False,
            replace_agents=False,
            skill_target="both",
        )

        destinations = {
            "claude": self.target / ".claude" / "skills",
            "codex": self.target / ".agents" / "skills",
        }
        for destination in destinations.values():
            self.assertTrue((destination / MANIFEST_FILENAME).is_file())
        self.assertEqual(
            [],
            check_skill_targets(self.source / "skills", destinations),
        )

        modified = destinations["codex"] / "sample-skill" / "SKILL.md"
        modified.write_text("local project edit\n", encoding="utf-8")
        with self.assertRaises(SkillSyncConflict):
            install_project(
                source_root=self.source,
                target=self.target,
                component="skills",
                force=False,
                replace_agents=False,
                skill_target="both",
            )

    def test_force_refresh_preserves_active_and_historical_memory(self) -> None:
        install_project(
            source_root=self.source,
            target=self.target,
            component="all",
            force=False,
            replace_agents=False,
            skill_target="both",
        )
        status = self.target / "memory-docs" / "STATUS.md"
        status.write_text(
            status.read_text(encoding="utf-8") + "\nProject-owned status sentinel.\n",
            encoding="utf-8",
        )
        status_before = status.read_bytes()
        custom = self.target / "memory-docs" / "archive" / "note.md"
        custom.write_text("keep me\n", encoding="utf-8")

        install_project(
            source_root=self.source,
            target=self.target,
            component="all",
            force=True,
            replace_agents=False,
            skill_target="both",
        )

        self.assertEqual(status_before, status.read_bytes())
        self.assertEqual("keep me\n", custom.read_text(encoding="utf-8"))

    def test_replace_memory_docs_explicitly_overwrites_standard_files(self) -> None:
        install_project(
            source_root=self.source,
            target=self.target,
            component="memory-docs",
            force=False,
            replace_agents=False,
        )
        status = self.target / "memory-docs" / "STATUS.md"
        status.write_text(
            status.read_text(encoding="utf-8") + "\nProject-owned status sentinel.\n",
            encoding="utf-8",
        )
        archived = self.target / "memory-docs" / "archive" / "preserved-note.md"
        archived.write_text("preserve historical detail\n", encoding="utf-8")
        expected = (self.source / "STATUS.md").read_text(encoding="utf-8").replace(
            "<memory-docs>/", "memory-docs/"
        )

        install_project(
            source_root=self.source,
            target=self.target,
            component="memory-docs",
            force=False,
            replace_agents=False,
            replace_memory_docs=True,
        )

        self.assertEqual(expected, status.read_text(encoding="utf-8"))
        self.assertEqual(
            "preserve historical detail\n",
            archived.read_text(encoding="utf-8"),
        )

    def test_replace_memory_docs_refuses_custom_directories(self) -> None:
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
                force=False,
                replace_agents=False,
                replace_memory_docs=True,
            )

        self.assertEqual("keep me\n", custom.read_text(encoding="utf-8"))

    def test_force_refresh_mirrors_skills_and_removes_stale_files(self) -> None:
        install_project(
            source_root=self.source,
            target=self.target,
            component="skills",
            force=False,
            replace_agents=False,
            skill_target="both",
        )
        source_skill = self.source / "skills" / "sample-skill" / "SKILL.md"
        refreshed_skill = "---\nname: sample-skill\ndescription: refreshed\n---\n"
        source_skill.write_text(refreshed_skill, encoding="utf-8")

        for agent_dir in (".claude", ".agents"):
            destination = self.target / agent_dir / "skills" / "sample-skill"
            (destination / "stale.txt").write_text("remove me\n", encoding="utf-8")

        install_project(
            source_root=self.source,
            target=self.target,
            component="skills",
            force=True,
            replace_agents=False,
            skill_target="both",
        )

        for agent_dir in (".claude", ".agents"):
            destination = self.target / agent_dir / "skills" / "sample-skill"
            self.assertEqual(
                refreshed_skill,
                (destination / "SKILL.md").read_text(encoding="utf-8"),
            )
            self.assertFalse((destination / "stale.txt").exists())

    def test_force_refresh_updates_project_local_validator(self) -> None:
        install_project(
            source_root=self.source,
            target=self.target,
            component="tools",
            force=False,
            replace_agents=False,
        )
        source_validator = self.source / "scripts" / "validate_memory_docs.py"
        refreshed = "# refreshed project-local validator fixture\n"
        source_validator.write_text(refreshed, encoding="utf-8")

        install_project(
            source_root=self.source,
            target=self.target,
            component="tools",
            force=True,
            replace_agents=False,
        )

        installed_validator = (
            self.target / ".memory-docs-tools" / "validate_memory_docs.py"
        )
        self.assertEqual(refreshed, installed_validator.read_text(encoding="utf-8"))

    def test_global_sync_preflights_all_conflicts_before_copying(self) -> None:
        repository = Path(__file__).resolve().parent.parent
        skill_names = sorted(
            path.name for path in (repository / "skills").iterdir() if path.is_dir()
        )
        self.assertGreater(len(skill_names), 1)

        for script_name, relative_destination in (
            ("sync_to_claude.sh", Path(".claude/skills")),
            ("sync_to_codex.sh", Path(".agents/skills")),
        ):
            with self.subTest(script=script_name):
                home = self.root / script_name
                destination = home / relative_destination
                collision = destination / skill_names[-1]
                collision.mkdir(parents=True)
                sentinel = collision / "sentinel.txt"
                sentinel.write_text("preserve\n", encoding="utf-8")
                environment = os.environ.copy()
                environment["HOME"] = str(home)

                result = subprocess.run(
                    ["bash", str(repository / "scripts" / script_name)],
                    check=False,
                    capture_output=True,
                    text=True,
                    env=environment,
                )

                self.assertNotEqual(0, result.returncode)
                self.assertTrue(sentinel.is_file())
                self.assertFalse((destination / skill_names[0]).exists())

    def test_global_sync_wrappers_share_manifest_and_check_behavior(self) -> None:
        repository = Path(__file__).resolve().parent.parent
        for script_name, relative_destination in (
            ("sync_to_claude.sh", Path(".claude/skills")),
            ("sync_to_codex.sh", Path(".agents/skills")),
        ):
            with self.subTest(script=script_name):
                home = self.root / f"managed-{script_name}"
                environment = os.environ.copy()
                environment["HOME"] = str(home)
                script = repository / "scripts" / script_name

                installed = subprocess.run(
                    ["bash", str(script)],
                    check=False,
                    capture_output=True,
                    text=True,
                    env=environment,
                )
                self.assertEqual(0, installed.returncode, installed.stderr)
                destination = home / relative_destination
                self.assertTrue((destination / MANIFEST_FILENAME).is_file())

                clean = subprocess.run(
                    ["bash", str(script), "--check"],
                    check=False,
                    capture_output=True,
                    text=True,
                    env=environment,
                )
                self.assertEqual(0, clean.returncode, clean.stderr)

                first_skill = sorted(
                    path for path in destination.iterdir() if path.is_dir()
                )[0]
                entrypoint = first_skill / "SKILL.md"
                entrypoint.write_text("locally modified\n", encoding="utf-8")
                drifted = subprocess.run(
                    ["bash", str(script), "--check"],
                    check=False,
                    capture_output=True,
                    text=True,
                    env=environment,
                )
                self.assertEqual(1, drifted.returncode)
                self.assertEqual(
                    "locally modified\n",
                    entrypoint.read_text(encoding="utf-8"),
                )

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
        self.assertTrue(
            any("STATUS.md" in error and "update_mode" in error for error in errors)
        )

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
