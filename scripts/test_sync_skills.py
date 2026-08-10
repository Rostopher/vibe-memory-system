from __future__ import annotations

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sync_skills as sync_module
from sync_skills import (
    MANIFEST_FILENAME,
    SkillSyncConflict,
    check_skill_targets,
    sync_skill_targets,
)


class SkillSyncTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.source = self.root / "source" / "skills"
        self.claude = self.root / "home" / ".claude" / "skills"
        self.codex = self.root / "home" / ".agents" / "skills"
        self.targets = {
            "claude": self.claude,
            "codex": self.codex,
        }
        self._write_skill("alpha", "alpha-v1\n")
        self._write_skill("beta", "beta-v1\n")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _write_skill(self, name: str, body: str) -> None:
        skill = self.source / name
        skill.mkdir(parents=True, exist_ok=True)
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: test\n---\n\n{body}",
            encoding="utf-8",
        )

    def _manifest(self, root: Path) -> dict[str, object]:
        return json.loads((root / MANIFEST_FILENAME).read_text(encoding="utf-8"))

    def _snapshot(self, root: Path) -> dict[str, bytes]:
        return {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    def test_initial_sync_writes_deterministic_manifest_and_checks_clean(self) -> None:
        sync_skill_targets(self.source, self.targets)

        self.assertEqual([], check_skill_targets(self.source, self.targets))
        for destination in self.targets.values():
            self.assertTrue((destination / "alpha" / "SKILL.md").is_file())
            self.assertTrue((destination / "beta" / "SKILL.md").is_file())

        claude_manifest = (self.claude / MANIFEST_FILENAME).read_bytes()
        codex_manifest = (self.codex / MANIFEST_FILENAME).read_bytes()
        self.assertEqual(claude_manifest, codex_manifest)
        self.assertNotIn(str(self.source).encode(), claude_manifest)

        manifest = self._manifest(self.claude)
        self.assertEqual(1, manifest["schema_version"])
        self.assertEqual("vibe-memory-system/skills", manifest["source"])
        self.assertEqual({"alpha", "beta"}, set(manifest["skills"]))
        for digest in manifest["skills"].values():
            self.assertRegex(str(digest), r"^[0-9a-f]{64}$")

    def test_executable_bit_changes_are_detected_and_synchronized(self) -> None:
        script = self.source / "alpha" / "scripts" / "run.sh"
        script.parent.mkdir()
        script.write_text("#!/usr/bin/env bash\n", encoding="utf-8")
        script.chmod(0o644)
        sync_skill_targets(self.source, self.targets)
        script.chmod(0o755)

        issues = check_skill_targets(self.source, self.targets)

        self.assertTrue(any("outdated" in issue.lower() for issue in issues))
        sync_skill_targets(self.source, self.targets)
        for destination in self.targets.values():
            installed = destination / "alpha" / "scripts" / "run.sh"
            self.assertEqual(0o111, installed.stat().st_mode & 0o111)
        self.assertEqual([], check_skill_targets(self.source, self.targets))

    def test_directory_executable_bit_changes_are_detected(self) -> None:
        scripts = self.source / "alpha" / "scripts"
        scripts.mkdir()
        (scripts / "run.sh").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
        scripts.chmod(0o700)
        sync_skill_targets(self.source, self.targets)
        scripts.chmod(0o755)

        issues = check_skill_targets(self.source, self.targets)

        self.assertTrue(any("outdated" in issue.lower() for issue in issues))
        sync_skill_targets(self.source, self.targets)
        for destination in self.targets.values():
            installed = destination / "alpha" / "scripts"
            self.assertEqual(0o111, installed.stat().st_mode & 0o111)

    def test_tree_hash_uses_unambiguous_record_framing(self) -> None:
        tree_a = self.root / "tree-a"
        tree_b = self.root / "tree-b"
        tree_a.mkdir()
        tree_b.mkdir()
        (tree_a / "a").write_bytes(
            b"X" + b"\0F\0" + b"b" + b"\0" + b"000" + b"\0Y"
        )
        (tree_b / "a").write_bytes(b"X")
        (tree_b / "b").write_bytes(b"Y")
        for path in (tree_a / "a", tree_b / "a", tree_b / "b"):
            path.chmod(0o644)

        self.assertNotEqual(
            sync_module._hash_skill_tree(tree_a),
            sync_module._hash_skill_tree(tree_b),
        )

    def test_check_detects_outdated_source_without_writing(self) -> None:
        sync_skill_targets(self.source, self.targets)
        before = {name: self._snapshot(root) for name, root in self.targets.items()}
        self._write_skill("alpha", "alpha-v2\n")

        issues = check_skill_targets(self.source, self.targets)

        self.assertTrue(any("outdated" in issue.lower() for issue in issues))
        self.assertEqual(
            before,
            {name: self._snapshot(root) for name, root in self.targets.items()},
        )

    def test_safe_refresh_updates_unchanged_managed_destinations_without_force(self) -> None:
        sync_skill_targets(self.source, self.targets)
        self._write_skill("alpha", "alpha-v2\n")

        sync_skill_targets(self.source, self.targets)

        for destination in self.targets.values():
            self.assertIn(
                "alpha-v2",
                (destination / "alpha" / "SKILL.md").read_text(encoding="utf-8"),
            )
        self.assertEqual([], check_skill_targets(self.source, self.targets))

    def test_modified_managed_destination_requires_force_before_any_write(self) -> None:
        sync_skill_targets(self.source, self.targets)
        modified = self.codex / "alpha" / "SKILL.md"
        modified.write_text("locally modified\n", encoding="utf-8")
        claude_before = self._snapshot(self.claude)

        with self.assertRaisesRegex(SkillSyncConflict, "modified"):
            sync_skill_targets(self.source, self.targets)

        self.assertEqual("locally modified\n", modified.read_text(encoding="utf-8"))
        self.assertEqual(claude_before, self._snapshot(self.claude))

    def test_force_refresh_overwrites_modified_managed_destination(self) -> None:
        sync_skill_targets(self.source, self.targets)
        modified = self.codex / "alpha" / "SKILL.md"
        modified.write_text("locally modified\n", encoding="utf-8")

        sync_skill_targets(self.source, self.targets, force=True)

        self.assertIn("alpha-v1", modified.read_text(encoding="utf-8"))
        self.assertEqual([], check_skill_targets(self.source, self.targets))

    def test_removed_owned_skill_is_deleted_but_foreign_skill_is_preserved(self) -> None:
        sync_skill_targets(self.source, self.targets)
        for destination in self.targets.values():
            foreign = destination / "foreign-skill"
            foreign.mkdir()
            (foreign / "SKILL.md").write_text("foreign\n", encoding="utf-8")
        shutil.rmtree(self.source / "beta")

        sync_skill_targets(self.source, self.targets)

        for destination in self.targets.values():
            self.assertFalse((destination / "beta").exists())
            self.assertEqual(
                "foreign\n",
                (destination / "foreign-skill" / "SKILL.md").read_text(
                    encoding="utf-8"
                ),
            )
        self.assertEqual([], check_skill_targets(self.source, self.targets))

    def test_unmanaged_collision_is_preflighted_across_all_targets(self) -> None:
        collision = self.codex / "beta"
        collision.mkdir(parents=True)
        sentinel = collision / "sentinel.txt"
        sentinel.write_text("preserve\n", encoding="utf-8")

        with self.assertRaisesRegex(SkillSyncConflict, "unmanaged"):
            sync_skill_targets(self.source, self.targets)

        self.assertTrue(sentinel.is_file())
        self.assertFalse(self.claude.exists())

    def test_symlinked_destination_root_is_refused_even_with_force(self) -> None:
        external = self.root / "external-skills"
        external.mkdir()
        self.codex.parent.mkdir(parents=True)
        self.codex.symlink_to(external, target_is_directory=True)

        with self.assertRaisesRegex(SkillSyncConflict, "symbolic link"):
            sync_skill_targets(
                self.source,
                {"codex": self.codex},
                force=True,
            )

        self.assertEqual([], list(external.iterdir()))

    def test_symlinked_top_level_source_skill_is_refused(self) -> None:
        external = self.root / "external-source-skill"
        external.mkdir()
        (external / "SKILL.md").write_text(
            "---\nname: external\ndescription: external\n---\n",
            encoding="utf-8",
        )
        (self.source / "external").symlink_to(
            external,
            target_is_directory=True,
        )

        with self.assertRaisesRegex(RuntimeError, "symbolic link"):
            sync_skill_targets(self.source, {"codex": self.codex})

        self.assertFalse(self.codex.exists())

    def test_symlinked_manifest_is_refused_even_with_force(self) -> None:
        sync_skill_targets(self.source, self.targets)
        manifest = self.codex / MANIFEST_FILENAME
        external_manifest = self.root / "external-manifest.json"
        manifest.replace(external_manifest)
        manifest.symlink_to(external_manifest)
        before = external_manifest.read_bytes()

        with self.assertRaisesRegex(SkillSyncConflict, "symbolic link"):
            sync_skill_targets(
                self.source,
                {"codex": self.codex},
                force=True,
            )

        self.assertTrue(manifest.is_symlink())
        self.assertEqual(before, external_manifest.read_bytes())

    def test_malformed_manifest_is_reported_without_writing(self) -> None:
        sync_skill_targets(self.source, self.targets)
        manifest = self.codex / MANIFEST_FILENAME
        manifest.write_text("[]\n", encoding="utf-8")
        before = {name: self._snapshot(root) for name, root in self.targets.items()}

        issues = check_skill_targets(self.source, self.targets)

        self.assertTrue(any("invalid sync manifest" in issue for issue in issues))
        with self.assertRaisesRegex(SkillSyncConflict, "invalid sync manifest"):
            sync_skill_targets(self.source, self.targets, force=True)
        self.assertEqual(
            before,
            {name: self._snapshot(root) for name, root in self.targets.items()},
        )

    def test_manifest_rejects_parent_and_current_directory_skill_names(self) -> None:
        for index, invalid_name in enumerate((".", "..")):
            with self.subTest(name=invalid_name):
                destination = self.root / f"invalid-name-{index}" / "skills"
                sync_skill_targets(self.source, {"codex": destination})
                manifest = destination / MANIFEST_FILENAME
                payload = json.loads(manifest.read_text(encoding="utf-8"))
                payload["skills"][invalid_name] = "0" * 64
                manifest.write_text(
                    json.dumps(payload, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                before = self._snapshot(destination)

                with self.assertRaisesRegex(
                    SkillSyncConflict,
                    "invalid skill entry",
                ):
                    sync_skill_targets(
                        self.source,
                        {"codex": destination},
                        force=True,
                    )

                self.assertEqual(before, self._snapshot(destination))

    def test_copy_failure_before_commit_preserves_all_destinations(self) -> None:
        sync_skill_targets(self.source, self.targets)
        before = {name: self._snapshot(root) for name, root in self.targets.items()}
        self._write_skill("alpha", "alpha-v2\n")
        real_copy = sync_module._copy_skill_tree
        calls = 0

        def fail_second_copy(source: Path, destination: Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                destination.mkdir(parents=True)
                (destination / "partial.txt").write_text("partial\n", encoding="utf-8")
                raise OSError("injected copy failure")
            real_copy(source, destination)

        with mock.patch.object(
            sync_module,
            "_copy_skill_tree",
            side_effect=fail_second_copy,
        ):
            with self.assertRaisesRegex(OSError, "injected copy failure"):
                sync_skill_targets(self.source, self.targets)

        self.assertEqual(
            before,
            {name: self._snapshot(root) for name, root in self.targets.items()},
        )
        self.assertFalse(
            any(
                path.name.startswith(".vibe-memory-system-stage-")
                for path in (self.claude.parent).iterdir()
            )
        )
        self.assertFalse(
            any(
                path.name.startswith(".vibe-memory-system-stage-")
                for path in (self.codex.parent).iterdir()
            )
        )

    def test_destination_change_during_staging_aborts_before_commit(self) -> None:
        sync_skill_targets(self.source, self.targets)
        claude_before = self._snapshot(self.claude)
        codex_manifest_before = (self.codex / MANIFEST_FILENAME).read_bytes()
        self._write_skill("alpha", "alpha-v2\n")
        real_copy = sync_module._copy_skill_tree
        changed = False

        def modify_codex_while_staging(source: Path, destination: Path) -> None:
            nonlocal changed
            real_copy(source, destination)
            if not changed:
                changed = True
                (self.codex / "alpha" / "SKILL.md").write_text(
                    "concurrent local edit\n",
                    encoding="utf-8",
                )

        with mock.patch.object(
            sync_module,
            "_copy_skill_tree",
            side_effect=modify_codex_while_staging,
        ):
            with self.assertRaisesRegex(
                SkillSyncConflict,
                "changed during synchronization",
            ):
                sync_skill_targets(self.source, self.targets)

        self.assertEqual(claude_before, self._snapshot(self.claude))
        self.assertEqual(
            "concurrent local edit\n",
            (self.codex / "alpha" / "SKILL.md").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            codex_manifest_before,
            (self.codex / MANIFEST_FILENAME).read_bytes(),
        )

    def test_manifest_ownership_and_snapshot_come_from_one_read(self) -> None:
        sync_skill_targets(self.source, {"codex": self.codex})
        old_alpha = (self.codex / "alpha" / "SKILL.md").read_bytes()
        self._write_skill("alpha", "alpha-v2\n")
        manifest = (self.codex / MANIFEST_FILENAME).resolve()
        real_read_bytes = Path.read_bytes
        changed = False

        def remove_alpha_ownership_during_read(path: Path) -> bytes:
            nonlocal changed
            if not changed and path.resolve() == manifest:
                changed = True
                payload = json.loads(real_read_bytes(path).decode("utf-8"))
                del payload["skills"]["alpha"]
                path.write_text(
                    json.dumps(payload, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
            return real_read_bytes(path)

        with mock.patch.object(
            Path,
            "read_bytes",
            new=remove_alpha_ownership_during_read,
        ):
            with self.assertRaises(SkillSyncConflict):
                sync_skill_targets(self.source, {"codex": self.codex})

        self.assertEqual(
            old_alpha,
            (self.codex / "alpha" / "SKILL.md").read_bytes(),
        )
        payload = json.loads(
            (self.codex / MANIFEST_FILENAME).read_text(encoding="utf-8")
        )
        self.assertNotIn("alpha", payload["skills"])

    def test_change_between_target_commits_rolls_back_prior_target(self) -> None:
        sync_skill_targets(self.source, self.targets)
        claude_before = self._snapshot(self.claude)
        codex_manifest_before = (self.codex / MANIFEST_FILENAME).read_bytes()
        self._write_skill("alpha", "alpha-v2\n")
        real_replace = os.replace
        changed = False
        claude_manifest = self.claude.resolve() / MANIFEST_FILENAME

        def modify_codex_after_claude_commit(
            source: str | Path,
            destination: str | Path,
        ) -> None:
            nonlocal changed
            real_replace(source, destination)
            if not changed and Path(destination) == claude_manifest:
                changed = True
                (self.codex / "alpha" / "SKILL.md").write_text(
                    "concurrent local edit\n",
                    encoding="utf-8",
                )

        with mock.patch.object(
            sync_module.os,
            "replace",
            side_effect=modify_codex_after_claude_commit,
        ):
            with self.assertRaisesRegex(
                SkillSyncConflict,
                "changed during synchronization",
            ):
                sync_skill_targets(self.source, self.targets)

        self.assertEqual(claude_before, self._snapshot(self.claude))
        self.assertEqual(
            "concurrent local edit\n",
            (self.codex / "alpha" / "SKILL.md").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            codex_manifest_before,
            (self.codex / MANIFEST_FILENAME).read_bytes(),
        )

    def test_backup_initialization_failure_cleans_staging_directory(self) -> None:
        real_mkdtemp = sync_module.tempfile.mkdtemp
        calls = 0

        def fail_second_mkdtemp(*args: object, **kwargs: object) -> str:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected backup initialization failure")
            return real_mkdtemp(*args, **kwargs)

        with mock.patch.object(
            sync_module.tempfile,
            "mkdtemp",
            side_effect=fail_second_mkdtemp,
        ):
            with self.assertRaisesRegex(
                OSError,
                "injected backup initialization failure",
            ):
                sync_skill_targets(self.source, {"codex": self.codex})

        self.assertFalse(
            any(
                path.name.startswith(".vibe-memory-system-stage-")
                for path in self.codex.parent.iterdir()
            )
        )

    def test_keyboard_interrupt_during_staging_cleans_temporary_directories(self) -> None:
        with mock.patch.object(
            sync_module,
            "_copy_skill_tree",
            side_effect=KeyboardInterrupt(),
        ):
            with self.assertRaises(KeyboardInterrupt):
                sync_skill_targets(self.source, {"codex": self.codex})

        self.assertFalse(self.codex.exists())
        self.assertFalse(
            any(
                path.name.startswith(
                    (".vibe-memory-system-stage-", ".vibe-memory-system-backup-")
                )
                for path in self.codex.parent.iterdir()
            )
        )

    def test_commit_failure_rolls_back_both_targets(self) -> None:
        sync_skill_targets(self.source, self.targets)
        before = {name: self._snapshot(root) for name, root in self.targets.items()}
        self._write_skill("alpha", "alpha-v2\n")
        real_replace = os.replace
        failed = False
        codex_alpha = self.codex.resolve() / "alpha"

        def fail_codex_install(source: str | Path, destination: str | Path) -> None:
            nonlocal failed
            if not failed and Path(destination) == codex_alpha:
                failed = True
                raise OSError("injected commit failure")
            real_replace(source, destination)

        with mock.patch.object(
            sync_module.os,
            "replace",
            side_effect=fail_codex_install,
        ):
            with self.assertRaisesRegex(OSError, "injected commit failure"):
                sync_skill_targets(self.source, self.targets)

        self.assertEqual(
            before,
            {name: self._snapshot(root) for name, root in self.targets.items()},
        )
        issues = check_skill_targets(self.source, self.targets)
        self.assertEqual(2, len(issues))
        self.assertTrue(all("outdated" in issue.lower() for issue in issues))

    def test_keyboard_interrupt_during_commit_rolls_back_both_targets(self) -> None:
        sync_skill_targets(self.source, self.targets)
        before = {name: self._snapshot(root) for name, root in self.targets.items()}
        self._write_skill("alpha", "alpha-v2\n")
        real_replace = os.replace
        interrupted = False
        codex_alpha = self.codex.resolve() / "alpha"

        def interrupt_codex_install(
            source: str | Path,
            destination: str | Path,
        ) -> None:
            nonlocal interrupted
            if not interrupted and Path(destination) == codex_alpha:
                interrupted = True
                raise KeyboardInterrupt()
            real_replace(source, destination)

        with mock.patch.object(
            sync_module.os,
            "replace",
            side_effect=interrupt_codex_install,
        ):
            with self.assertRaises(KeyboardInterrupt):
                sync_skill_targets(self.source, self.targets)

        self.assertEqual(
            before,
            {name: self._snapshot(root) for name, root in self.targets.items()},
        )

    def test_interrupt_after_successful_skill_move_still_rolls_back(self) -> None:
        sync_skill_targets(self.source, {"claude": self.claude})
        before = self._snapshot(self.claude)
        self._write_skill("alpha", "alpha-v2\n")
        real_replace = os.replace
        interrupted = False
        claude_alpha = self.claude.resolve() / "alpha"

        def interrupt_after_skill_backup(
            source: str | Path,
            destination: str | Path,
        ) -> None:
            nonlocal interrupted
            source_path = Path(source)
            destination_path = Path(destination)
            if (
                not interrupted
                and source_path == claude_alpha
                and ".vibe-memory-system-backup-" in destination_path.as_posix()
            ):
                real_replace(source, destination)
                interrupted = True
                raise KeyboardInterrupt()
            real_replace(source, destination)

        with mock.patch.object(
            sync_module.os,
            "replace",
            side_effect=interrupt_after_skill_backup,
        ):
            with self.assertRaises(KeyboardInterrupt):
                sync_skill_targets(self.source, {"claude": self.claude})

        self.assertEqual(before, self._snapshot(self.claude))

    def test_interrupt_after_successful_manifest_move_still_rolls_back(self) -> None:
        sync_skill_targets(self.source, {"claude": self.claude})
        before = self._snapshot(self.claude)
        self._write_skill("alpha", "alpha-v2\n")
        real_replace = os.replace
        interrupted = False
        claude_manifest = self.claude.resolve() / MANIFEST_FILENAME

        def interrupt_after_manifest_backup(
            source: str | Path,
            destination: str | Path,
        ) -> None:
            nonlocal interrupted
            source_path = Path(source)
            destination_path = Path(destination)
            if (
                not interrupted
                and source_path == claude_manifest
                and ".vibe-memory-system-backup-" in destination_path.as_posix()
            ):
                real_replace(source, destination)
                interrupted = True
                raise KeyboardInterrupt()
            real_replace(source, destination)

        with mock.patch.object(
            sync_module.os,
            "replace",
            side_effect=interrupt_after_manifest_backup,
        ):
            with self.assertRaises(KeyboardInterrupt):
                sync_skill_targets(self.source, {"claude": self.claude})

        self.assertEqual(before, self._snapshot(self.claude))

    def test_incomplete_rollback_preserves_backup_for_manual_recovery(self) -> None:
        sync_skill_targets(self.source, self.targets)
        self._write_skill("alpha", "alpha-v2\n")
        real_replace = os.replace
        commit_failed = False
        rollback_failed = False
        codex_alpha = self.codex.resolve() / "alpha"

        def fail_commit_and_restore(
            source: str | Path,
            destination: str | Path,
        ) -> None:
            nonlocal commit_failed, rollback_failed
            source_path = Path(source)
            destination_path = Path(destination)
            if (
                not commit_failed
                and destination_path == codex_alpha
                and ".vibe-memory-system-stage-" in source_path.as_posix()
            ):
                commit_failed = True
                raise OSError("injected commit failure")
            if (
                commit_failed
                and not rollback_failed
                and destination_path == codex_alpha
                and ".vibe-memory-system-backup-" in source_path.as_posix()
            ):
                rollback_failed = True
                raise OSError("injected rollback failure")
            real_replace(source, destination)

        with mock.patch.object(
            sync_module.os,
            "replace",
            side_effect=fail_commit_and_restore,
        ):
            with self.assertRaisesRegex(RuntimeError, "rollback was incomplete"):
                sync_skill_targets(self.source, self.targets)

        backups = [
            path
            for path in self.codex.parent.iterdir()
            if path.name.startswith(".vibe-memory-system-backup-")
        ]
        self.assertTrue(backups)
        self.assertTrue(
            any((backup / "skills" / "alpha" / "SKILL.md").is_file() for backup in backups)
        )

    def test_rollback_preserves_concurrent_edit_to_committed_target(self) -> None:
        sync_skill_targets(self.source, self.targets)
        old_claude_alpha = (
            self.claude / "alpha" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self._write_skill("alpha", "alpha-v2\n")
        real_replace = os.replace
        claude_edited = False
        codex_failed = False
        claude_manifest = self.claude.resolve() / MANIFEST_FILENAME
        codex_alpha = self.codex.resolve() / "alpha"

        def edit_claude_then_fail_codex(
            source: str | Path,
            destination: str | Path,
        ) -> None:
            nonlocal claude_edited, codex_failed
            source_path = Path(source)
            destination_path = Path(destination)
            if (
                not codex_failed
                and destination_path == codex_alpha
                and ".vibe-memory-system-stage-" in source_path.as_posix()
            ):
                codex_failed = True
                raise OSError("injected codex commit failure")
            real_replace(source, destination)
            if not claude_edited and destination_path == claude_manifest:
                claude_edited = True
                (self.claude / "alpha" / "SKILL.md").write_text(
                    "concurrent claude edit\n",
                    encoding="utf-8",
                )

        with mock.patch.object(
            sync_module.os,
            "replace",
            side_effect=edit_claude_then_fail_codex,
        ):
            with self.assertRaisesRegex(RuntimeError, "rollback was incomplete"):
                sync_skill_targets(self.source, self.targets)

        self.assertEqual(
            "concurrent claude edit\n",
            (self.claude / "alpha" / "SKILL.md").read_text(encoding="utf-8"),
        )
        backups = [
            path
            for path in self.claude.parent.iterdir()
            if path.name.startswith(".vibe-memory-system-backup-")
        ]
        self.assertTrue(
            any(
                (backup / "skills" / "alpha" / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                == old_claude_alpha
                for backup in backups
                if (backup / "skills" / "alpha" / "SKILL.md").is_file()
            )
        )

    def test_rollback_does_not_overwrite_reappeared_removed_skill(self) -> None:
        sync_skill_targets(self.source, {"claude": self.claude})
        shutil.rmtree(self.source / "beta")
        real_replace = os.replace
        recreated = False
        claude_beta = self.claude.resolve() / "beta"

        def recreate_beta_after_removal(
            source: str | Path,
            destination: str | Path,
        ) -> None:
            nonlocal recreated
            source_path = Path(source)
            destination_path = Path(destination)
            if (
                not recreated
                and source_path == claude_beta
                and ".vibe-memory-system-backup-" in destination_path.as_posix()
            ):
                real_replace(source, destination)
                claude_beta.mkdir()
                recreated = True
                return
            real_replace(source, destination)

        with mock.patch.object(
            sync_module.os,
            "replace",
            side_effect=recreate_beta_after_removal,
        ):
            with self.assertRaisesRegex(RuntimeError, "rollback was incomplete"):
                sync_skill_targets(self.source, {"claude": self.claude})

        self.assertTrue(claude_beta.is_dir())
        self.assertEqual([], list(claude_beta.iterdir()))
        backups = [
            path
            for path in self.claude.parent.iterdir()
            if path.name.startswith(".vibe-memory-system-backup-")
        ]
        self.assertTrue(
            any((backup / "skills" / "beta" / "SKILL.md").is_file() for backup in backups)
        )


if __name__ == "__main__":
    unittest.main()
