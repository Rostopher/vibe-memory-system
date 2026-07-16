#!/usr/bin/env python3
"""Validate a memory-docs instance or the vibe-memory-system template root."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileSpec:
    layer: str
    update_mode: str


EXPECTED_FILES: dict[Path, FileSpec] = {
    Path("INDEX.md"): FileSpec("framework", "rewrite"),
    Path("OVERVIEW.md"): FileSpec("framework", "rewrite"),
    Path("STATUS.md"): FileSpec("framework", "rewrite"),
    Path("HISTORY.md"): FileSpec("framework", "append"),
    Path("CONVENTIONS.md"): FileSpec("framework", "patch"),
    Path("GLOSSARY.md"): FileSpec("framework", "patch"),
    Path("DIRS.md"): FileSpec("routing", "patch"),
    Path("detail_mem/MAP.md"): FileSpec("detail", "patch"),
    Path("detail_mem/PROGRESS.md"): FileSpec("detail", "patch"),
    Path("detail_mem/DECISIONS.md"): FileSpec("detail", "append"),
    Path("SHORT_MEMORY/README.md"): FileSpec("detail", "append"),
    Path("archive/README.md"): FileSpec("detail", "append"),
}

REQUIRED_FRONTMATTER_FIELDS = {
    "layer",
    "update_mode",
    "role",
    "read_when",
    "not_for",
}
PRESET_DIRECTORIES = {"detail_mem", "SHORT_MEMORY", "archive"}


def _memory_root(path: Path, template: bool) -> Path:
    resolved = path.expanduser().resolve()
    if template or (resolved / "INDEX.md").is_file():
        return resolved
    return resolved / "memory-docs"


def _frontmatter(text: str) -> dict[str, str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return None

    values: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def validate_memory_docs(
    path: Path,
    *,
    template: bool = False,
    allow_template_tokens: bool = False,
) -> tuple[list[str], list[str]]:
    root = _memory_root(path, template)
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        return [f"memory-docs root does not exist: {root}"], warnings

    for relative, expected in EXPECTED_FILES.items():
        file_path = root / relative
        if not file_path.is_file():
            errors.append(f"missing required file: {relative.as_posix()}")
            continue

        text = file_path.read_text(encoding="utf-8")
        frontmatter = _frontmatter(text)
        if frontmatter is None:
            errors.append(f"invalid or missing frontmatter: {relative.as_posix()}")
            continue

        missing_fields = REQUIRED_FRONTMATTER_FIELDS - frontmatter.keys()
        if missing_fields:
            errors.append(
                f"missing frontmatter fields in {relative.as_posix()}: "
                + ", ".join(sorted(missing_fields))
            )
        if frontmatter.get("layer") != expected.layer:
            errors.append(
                f"wrong layer in {relative.as_posix()}: "
                f"expected {expected.layer}, got {frontmatter.get('layer', '<missing>')}"
            )
        if frontmatter.get("update_mode") != expected.update_mode:
            errors.append(
                f"wrong update_mode in {relative.as_posix()}: "
                f"expected {expected.update_mode}, got "
                f"{frontmatter.get('update_mode', '<missing>')}"
            )
        if not template and not allow_template_tokens and "<memory-docs>/" in text:
            warnings.append(
                f"possible unresolved <memory-docs>/ token in {relative.as_posix()}"
            )

    dirs_file = root / "DIRS.md"
    if dirs_file.is_file() and not template:
        dirs_text = dirs_file.read_text(encoding="utf-8")
        actual_directories = {
            child.name for child in root.iterdir() if child.is_dir() and not child.name.startswith(".")
        }
        for dirname in sorted(actual_directories - PRESET_DIRECTORIES):
            if re.search(rf"`{re.escape(dirname)}/`", dirs_text) is None:
                errors.append(f"unregistered custom directory in DIRS.md: {dirname}/")

    if not template:
        legacy_files = ["MEMORY_MANIFEST.yml", "RUNBOOK.md", "README.md"]
        present_legacy = [name for name in legacy_files if (root / name).exists()]
        if present_legacy:
            warnings.append(
                "legacy files are not part of the current standard: "
                + ", ".join(present_legacy)
            )

    return errors, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a memory-docs project instance or template root."
    )
    parser.add_argument("path", type=Path, help="Project root, memory-docs directory, or template root")
    parser.add_argument(
        "--template",
        action="store_true",
        help="Treat PATH as the vibe-memory-system template root and allow template tokens",
    )
    parser.add_argument(
        "--allow-template-tokens",
        action="store_true",
        help="Allow project memory to discuss the literal <memory-docs>/ template token",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors, warnings = validate_memory_docs(
        args.path,
        template=args.template,
        allow_template_tokens=args.allow_template_tokens,
    )
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print("memory-docs validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
