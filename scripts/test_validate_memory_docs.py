from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validate_memory_docs import EXPECTED_FILES, OPTIONAL_FILES, validate_memory_docs


class ValidateMemoryDocsHealthTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.project = self.root / "project"
        self.memory = self.project / "memory-docs"
        self.project.mkdir()
        self._write_standard_docs()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _write_standard_docs(self) -> None:
        for relative in EXPECTED_FILES:
            self._write_doc(relative)

    def _write_doc(
        self,
        relative: Path | str,
        *,
        extra_frontmatter: dict[str, str | int] | None = None,
        body: str | None = None,
    ) -> Path:
        relative = Path(relative)
        spec = EXPECTED_FILES.get(relative) or OPTIONAL_FILES[relative]
        lines = [
            "---",
            f"layer: {spec.layer}",
            f"update_mode: {spec.update_mode}",
            'role: "fixture role"',
            'read_when: "fixture read condition"',
            'not_for: "fixture exclusion"',
        ]
        for key, value in (extra_frontmatter or {}).items():
            lines.append(f"{key}: {value}")
        lines.extend(
            [
                "---",
                "",
                body
                if body is not None
                else f"# {relative.stem}\n\nUnique fixture content for {relative.as_posix()}.",
            ]
        )
        destination = self.memory / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return destination

    def _warnings(self) -> list[str]:
        errors, warnings = validate_memory_docs(self.project)
        self.assertEqual([], errors)
        return warnings

    def _register_directory(self, dirname: str) -> None:
        dirs = self.memory / "DIRS.md"
        dirs.write_text(
            dirs.read_text(encoding="utf-8")
            + f"\n| `{dirname}/` | optional fixture | when needed | 2026-07-30 |\n",
            encoding="utf-8",
        )

    def _run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        validator = Path(__file__).with_name("validate_memory_docs.py")
        return subprocess.run(
            [sys.executable, str(validator), str(self.project), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_template_mode_skips_health_warnings(self) -> None:
        self._write_doc(
            "STATUS.md",
            extra_frontmatter={"line_budget": 1, "stale_after_days": 0},
            body=(
                "Last updated: 2000-01-01\n\n"
                "[broken](missing.md)\n\n"
                "Template token: `<memory-docs>/STATUS.md`."
            ),
        )
        bundle = self.memory / "archive" / "topic"
        bundle.mkdir()
        (bundle / "evidence.md").write_text("archived evidence\n", encoding="utf-8")

        errors, warnings = validate_memory_docs(self.memory, template=True)

        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_broken_local_markdown_link_warns(self) -> None:
        overview = self.memory / "OVERVIEW.md"
        overview.write_text(
            overview.read_text(encoding="utf-8") + "\n[missing](missing/file.md)\n",
            encoding="utf-8",
        )

        warnings = self._warnings()

        self.assertTrue(
            any(
                "broken local Markdown link in OVERVIEW.md: missing/file.md" in warning
                for warning in warnings
            )
        )

    def test_malformed_markdown_links_warn_without_crashing(self) -> None:
        overview = self.memory / "OVERVIEW.md"
        overview.write_text(
            overview.read_text(encoding="utf-8")
            + "\n[bad IPv6](http://[::1)\n[bad path](%00)\n",
            encoding="utf-8",
        )

        warnings = self._warnings()

        self.assertIn(
            "invalid Markdown link target in OVERVIEW.md: http://[::1",
            warnings,
        )
        self.assertIn(
            "invalid Markdown link target in OVERVIEW.md: %00",
            warnings,
        )

    def test_code_links_are_ignored_and_parenthesized_paths_are_supported(self) -> None:
        guide = self.memory / "guides" / "path_(draft).md"
        guide.parent.mkdir()
        guide.write_text("valid guide\n", encoding="utf-8")
        self._register_directory("guides")
        overview = self.memory / "OVERVIEW.md"
        overview.write_text(
            overview.read_text(encoding="utf-8")
            + "\n"
            + "\n".join(
                [
                    "Inline example: `[ignored](missing-inline.md)`.",
                    "",
                    "```markdown",
                    "[ignored](missing-fenced.md)",
                    "```",
                    "",
                    "[Valid guide](guides/path_(draft).md)",
                    "",
                ]
            ),
            encoding="utf-8",
        )

        warnings = self._warnings()

        self.assertFalse(
            any("broken local Markdown link" in warning for warning in warnings)
        )

    def test_real_dirs_template_examples_do_not_register_custom_directories(self) -> None:
        template_dirs = Path(__file__).resolve().parent.parent / "DIRS.md"
        dirs_text = template_dirs.read_text(encoding="utf-8")
        self.assertIn("`design/`", dirs_text)
        (self.memory / "DIRS.md").write_text(dirs_text, encoding="utf-8")
        design = self.memory / "design"
        design.mkdir()
        (design / "note.md").write_text("unregistered design detail\n", encoding="utf-8")

        errors, _ = validate_memory_docs(self.project)

        self.assertIn("unregistered custom directory in DIRS.md: design/", errors)

    def test_line_budget_warns_at_ninety_percent_and_over_limit(self) -> None:
        near = self._write_doc(
            "OVERVIEW.md",
            extra_frontmatter={"line_budget": 11},
            body="Near-budget fixture.",
        )
        over = self._write_doc(
            "STATUS.md",
            extra_frontmatter={"line_budget": 9},
            body="Over-budget fixture.",
        )
        self.assertEqual(10, len(near.read_text(encoding="utf-8").splitlines()))
        self.assertEqual(10, len(over.read_text(encoding="utf-8").splitlines()))

        warnings = self._warnings()

        self.assertTrue(
            any(
                "active document is near line_budget in OVERVIEW.md: 10/11 lines"
                in warning
                for warning in warnings
            )
        )
        self.assertTrue(
            any(
                "active document exceeds line_budget in STATUS.md: 10/9 lines"
                in warning
                for warning in warnings
            )
        )

    def test_stale_explicit_date_warns(self) -> None:
        self._write_doc(
            "STATUS.md",
            extra_frontmatter={"stale_after_days": 1},
            body="Last updated: 2000-01-01",
        )

        warnings = self._warnings()

        self.assertTrue(
            any("document is stale in STATUS.md:" in warning for warning in warnings)
        )

    def test_explicit_date_behind_git_file_date_warns(self) -> None:
        if shutil.which("git") is None:
            self.skipTest("git is unavailable")
        self._write_doc(
            "STATUS.md",
            extra_frontmatter={"stale_after_days": 10000},
            body="Last updated: 2024-02-01",
        )
        subprocess.run(
            ["git", "init", "-q", str(self.project)],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "-C", str(self.project), "config", "user.name", "Fixture"],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(self.project),
                "config",
                "user.email",
                "fixture@example.invalid",
            ],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(self.project), "add", "memory-docs/STATUS.md"],
            check=True,
        )
        environment = os.environ.copy()
        environment.update(
            {
                "GIT_AUTHOR_DATE": "2024-02-02T12:00:00+00:00",
                "GIT_COMMITTER_DATE": "2024-02-02T12:00:00+00:00",
            }
        )
        subprocess.run(
            ["git", "-C", str(self.project), "commit", "-q", "-m", "fixture"],
            check=True,
            env=environment,
        )

        warnings = self._warnings()

        self.assertIn(
            "explicit update date lags Git in STATUS.md: 2024-02-01 < 2024-02-02",
            warnings,
        )

    def test_duplicate_long_prose_across_active_docs_warns(self) -> None:
        paragraph = (
            "This deliberately long ownership paragraph records one durable project "
            "fact with enough explanatory context to exceed the duplicate detector "
            "threshold, and it should remain in exactly one active owner document "
            "while every other active document links to that owner instead of "
            "copying the same detailed explanation. "
        )
        self._write_doc("OVERVIEW.md", body=paragraph)
        self._write_doc("STATUS.md", body=paragraph)

        warnings = self._warnings()

        self.assertTrue(
            any("long active prose is 100% similar across" in warning for warning in warnings)
        )

    def test_lists_tables_and_archive_prose_do_not_trigger_duplicates(self) -> None:
        paragraph = (
            "This deliberately long paragraph is repeated in non-prose structures "
            "and historical storage to verify that active ownership diagnostics do "
            "not treat list rows, table rows, or archived source material as live "
            "duplicate prose requiring consolidation by the documentation maintainer. "
        )
        self._write_doc("OVERVIEW.md", body=f"- {paragraph}")
        self._write_doc("STATUS.md", body=f"- {paragraph}")
        self._write_doc("HISTORY.md", body=f"| Record |\n| --- |\n| {paragraph} |")
        self._write_doc("CONVENTIONS.md", body=paragraph)
        (self.memory / "archive" / "flat-note.md").write_text(
            paragraph + "\n",
            encoding="utf-8",
        )

        warnings = self._warnings()

        self.assertFalse(any("long active prose is" in warning for warning in warnings))

    def test_flat_archive_files_are_valid_without_manifest(self) -> None:
        (self.memory / "archive" / "flat-note.md").write_text(
            "historical detail\n",
            encoding="utf-8",
        )

        warnings = self._warnings()

        self.assertFalse(any("archive topic bundle" in warning for warning in warnings))
        self.assertFalse(any("archive manifest" in warning for warning in warnings))

    def test_archive_bundle_without_manifest_warns(self) -> None:
        bundle = self.memory / "archive" / "topic"
        bundle.mkdir()
        (bundle / "evidence.txt").write_text("evidence\n", encoding="utf-8")

        warnings = self._warnings()

        self.assertIn(
            "archive topic bundle has no README.md or MANIFEST.md: archive/topic",
            warnings,
        )

    def test_archive_manifest_missing_fields_warns(self) -> None:
        bundle = self.memory / "archive" / "topic"
        bundle.mkdir()
        (bundle / "evidence.txt").write_text("evidence\n", encoding="utf-8")
        (bundle / "README.md").write_text(
            "# Topic\n\n- Archived: 2026-01-01\n",
            encoding="utf-8",
        )

        warnings = self._warnings()

        matches = [
            warning
            for warning in warnings
            if warning.startswith(
                "archive manifest is missing fields in archive/topic/README.md:"
            )
        ]
        self.assertEqual(1, len(matches))
        self.assertIn("Reason", matches[0])
        self.assertIn("Preserves", matches[0])
        self.assertIn("Distilled into", matches[0])
        self.assertIn("Retrieval keywords", matches[0])

    def test_archive_manifest_empty_fields_warn(self) -> None:
        bundle = self.memory / "archive" / "topic"
        bundle.mkdir()
        (bundle / "evidence.txt").write_text("evidence\n", encoding="utf-8")
        (bundle / "README.md").write_text(
            "\n".join(
                [
                    "# Topic",
                    "",
                    "- Archived: 2026-01-01",
                    "- Reason:",
                    "- Preserves: raw evidence",
                    "- Distilled into:",
                    "- Retrieval keywords: fixture, archive",
                    "",
                ]
            ),
            encoding="utf-8",
        )

        warnings = self._warnings()

        matches = [
            warning
            for warning in warnings
            if warning.startswith(
                "archive manifest has empty fields in archive/topic/README.md:"
            )
        ]
        self.assertEqual(1, len(matches))
        self.assertIn("Reason", matches[0])
        self.assertIn("Distilled into", matches[0])

    def test_archive_manifest_fields_inside_code_do_not_count(self) -> None:
        bundle = self.memory / "archive" / "topic"
        bundle.mkdir()
        (bundle / "evidence.txt").write_text("evidence\n", encoding="utf-8")
        (bundle / "README.md").write_text(
            "\n".join(
                [
                    "# Topic",
                    "",
                    "```markdown",
                    "- Archived: 2026-01-01",
                    "- Reason: completed investigation",
                    "- Preserves: raw evidence",
                    "- Distilled into: [STATUS](../../STATUS.md)",
                    "- Retrieval keywords: fixture, archive",
                    "```",
                    "",
                ]
            ),
            encoding="utf-8",
        )

        warnings = self._warnings()

        self.assertTrue(
            any(
                warning.startswith(
                    "archive manifest is missing fields in archive/topic/README.md:"
                )
                for warning in warnings
            )
        )

    def test_archive_manifest_bold_labels_are_valid(self) -> None:
        bundle = self.memory / "archive" / "topic"
        bundle.mkdir()
        (bundle / "evidence.txt").write_text("evidence\n", encoding="utf-8")
        (bundle / "README.md").write_text(
            "\n".join(
                [
                    "# Topic",
                    "",
                    "- **Archived**: 2026-01-01",
                    "- **Reason**: completed investigation",
                    "- **Preserves**: raw evidence",
                    "- **Distilled into**: [STATUS](../../STATUS.md)",
                    "- **Retrieval keywords**: fixture, archive",
                    "",
                ]
            ),
            encoding="utf-8",
        )

        warnings = self._warnings()

        self.assertFalse(any("archive manifest" in warning for warning in warnings))

    def test_archive_manifest_plain_or_external_distilled_target_warns(self) -> None:
        for target in (
            "STATUS.md",
            "[external](https://example.com/status)",
            "[archived evidence](evidence.md)",
            "[memory root](../..)",
            "[malformed](http://[::1)",
        ):
            with self.subTest(target=target):
                bundle = self.memory / "archive" / "topic"
                bundle.mkdir()
                (bundle / "evidence.md").write_text(
                    "evidence\n",
                    encoding="utf-8",
                )
                (bundle / "README.md").write_text(
                    "\n".join(
                        [
                            "# Topic",
                            "",
                            "- Archived: 2026-01-01",
                            "- Reason: completed investigation",
                            "- Preserves: raw evidence",
                            f"- Distilled into: {target}",
                            "- Retrieval keywords: fixture, archive",
                            "",
                        ]
                    ),
                    encoding="utf-8",
                )

                warnings = self._warnings()

                self.assertIn(
                    "archive manifest has invalid Distilled into in "
                    "archive/topic/README.md: expected at least one existing "
                    "live Markdown owner link",
                    warnings,
                )
                shutil.rmtree(bundle)

    def test_manifest_selection_prefers_more_nonempty_fields(self) -> None:
        bundle = self.memory / "archive" / "topic"
        bundle.mkdir()
        (bundle / "evidence.txt").write_text("evidence\n", encoding="utf-8")
        (bundle / "README.md").write_text(
            "\n".join(
                [
                    "# Topic",
                    "",
                    "- Archived:",
                    "- Reason:",
                    "- Preserves:",
                    "- Distilled into:",
                    "- Retrieval keywords:",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (bundle / "MANIFEST.md").write_text(
            "\n".join(
                [
                    "# Topic manifest",
                    "",
                    "- Archived: 2026-01-01",
                    "- Reason: completed investigation",
                    "- Preserves: raw evidence",
                    "- Distilled into: [STATUS](../../STATUS.md)",
                    "- Retrieval keywords: fixture, archive",
                    "",
                ]
            ),
            encoding="utf-8",
        )

        warnings = self._warnings()

        self.assertFalse(any("archive manifest" in warning for warning in warnings))

    def test_manifest_selection_prefers_valid_live_owner_link_on_tie(self) -> None:
        bundle = self.memory / "archive" / "topic"
        bundle.mkdir()
        (bundle / "evidence.md").write_text("evidence\n", encoding="utf-8")
        common = [
            "# Topic",
            "",
            "- Archived: 2026-01-01",
            "- Reason: completed investigation",
            "- Preserves: raw evidence",
        ]
        (bundle / "README.md").write_text(
            "\n".join(
                [
                    *common,
                    "- Distilled into: [STATUS](../../STATUS.md)",
                    "- Retrieval keywords: fixture, archive",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (bundle / "MANIFEST.md").write_text(
            "\n".join(
                [
                    *common,
                    "- Distilled into: [archived evidence](evidence.md)",
                    "- Retrieval keywords: fixture, archive",
                    "",
                ]
            ),
            encoding="utf-8",
        )

        warnings = self._warnings()

        self.assertFalse(any("archive manifest" in warning for warning in warnings))

    def test_complete_archive_manifest_is_valid(self) -> None:
        bundle = self.memory / "archive" / "topic"
        bundle.mkdir()
        (bundle / "evidence.txt").write_text("evidence\n", encoding="utf-8")
        (bundle / "MANIFEST.md").write_text(
            "\n".join(
                [
                    "# Topic",
                    "",
                    "- Archived: 2026-01-01",
                    "- Reason: completed investigation",
                    "- Preserves: raw evidence",
                    "- Distilled into: [STATUS](../../STATUS.md)",
                    "- Retrieval keywords: fixture, archive",
                    "",
                ]
            ),
            encoding="utf-8",
        )

        warnings = self._warnings()

        self.assertFalse(any("archive topic bundle" in warning for warning in warnings))
        self.assertFalse(any("archive manifest" in warning for warning in warnings))
        self.assertFalse(any("broken local Markdown link" in warning for warning in warnings))

    def test_archive_manifest_local_links_are_checked(self) -> None:
        bundle = self.memory / "archive" / "topic"
        bundle.mkdir()
        (bundle / "evidence.txt").write_text("evidence\n", encoding="utf-8")
        (bundle / "README.md").write_text(
            "\n".join(
                [
                    "# Topic",
                    "",
                    "- Archived: 2026-01-01",
                    "- Reason: completed investigation",
                    "- Preserves: raw evidence",
                    "- Distilled into: [missing owner](../../missing-owner.md)",
                    "- Retrieval: fixture, archive",
                    "",
                ]
            ),
            encoding="utf-8",
        )

        warnings = self._warnings()

        self.assertIn(
            "broken local Markdown link in archive/topic/README.md: "
            "../../missing-owner.md",
            warnings,
        )

    def test_archive_manifest_wins_over_short_readme_and_its_links_are_checked(
        self,
    ) -> None:
        bundle = self.memory / "archive" / "topic"
        bundle.mkdir()
        (bundle / "evidence.txt").write_text("evidence\n", encoding="utf-8")
        (bundle / "README.md").write_text(
            "# Topic\n\nDetailed provenance is recorded in [MANIFEST](MANIFEST.md).\n",
            encoding="utf-8",
        )
        (bundle / "MANIFEST.md").write_text(
            "\n".join(
                [
                    "# Topic manifest",
                    "",
                    "- Archived: 2026-01-01",
                    "- Reason: completed investigation",
                    "- Preserves: raw evidence",
                    "- Distilled into: [missing owner](../../missing-owner.md)",
                    "- Retrieval keywords: fixture, archive",
                    "",
                ]
            ),
            encoding="utf-8",
        )

        warnings = self._warnings()

        self.assertFalse(
            any("archive manifest is missing fields" in warning for warning in warnings)
        )
        self.assertIn(
            "broken local Markdown link in archive/topic/MANIFEST.md: "
            "../../missing-owner.md",
            warnings,
        )

    def test_long_plain_prose_line_warns(self) -> None:
        self._write_doc("STATUS.md", body="x" * 501)

        warnings = self._warnings()

        self.assertTrue(
            any(
                "active prose line is unusually long in STATUS.md:" in warning
                and "501 characters" in warning
                for warning in warnings
            )
        )

    def test_long_structural_markdown_lines_are_skipped(self) -> None:
        long_text = "x" * 501
        self._write_doc(
            "STATUS.md",
            body="\n".join(
                [
                    f"# {long_text}",
                    "",
                    f"| {long_text} |",
                    "",
                    "```text",
                    long_text,
                    "```",
                    "",
                    f"    {long_text}",
                ]
            ),
        )

        warnings = self._warnings()

        self.assertFalse(
            any("active prose line is unusually long" in warning for warning in warnings)
        )

    def test_optional_experiment_ledger_can_be_absent(self) -> None:
        errors, warnings = validate_memory_docs(self.project)

        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_optional_experiment_ledger_validates_frontmatter_when_present(self) -> None:
        self._register_directory("research")
        ledger = self._write_doc("research/EXPERIMENT_LEDGER.md")
        ledger.write_text(
            ledger.read_text(encoding="utf-8").replace(
                "update_mode: append", "update_mode: patch"
            ),
            encoding="utf-8",
        )

        errors, _ = validate_memory_docs(self.project)

        self.assertTrue(
            any(
                "wrong update_mode in research/EXPERIMENT_LEDGER.md" in error
                for error in errors
            )
        )

    def test_cli_warning_exit_codes_and_json_schema(self) -> None:
        overview = self.memory / "OVERVIEW.md"
        overview.write_text(
            overview.read_text(encoding="utf-8") + "\n[missing](missing.md)\n",
            encoding="utf-8",
        )

        default = self._run_cli()
        strict = self._run_cli("--strict")
        as_json = self._run_cli("--json")

        self.assertEqual(0, default.returncode, default.stderr)
        self.assertIn("WARNING: broken local Markdown link", default.stdout)
        self.assertEqual(1, strict.returncode)
        payload = json.loads(as_json.stdout)
        self.assertEqual(0, as_json.returncode, as_json.stderr)
        self.assertEqual(
            {
                "path",
                "memory_root",
                "template",
                "counts",
                "errors",
                "warnings",
            },
            set(payload),
        )
        self.assertEqual({"errors", "warnings"}, set(payload["counts"]))
        self.assertEqual(0, payload["counts"]["errors"])
        self.assertEqual(1, payload["counts"]["warnings"])
        self.assertEqual([], payload["errors"])
        self.assertEqual(1, len(payload["warnings"]))
        self.assertFalse(payload["template"])
        self.assertEqual(str(self.project.resolve()), payload["path"])
        self.assertEqual(str(self.memory.resolve()), payload["memory_root"])


if __name__ == "__main__":
    unittest.main()
