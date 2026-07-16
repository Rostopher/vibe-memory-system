#!/usr/bin/env python3
"""Install the current memory-docs template and companion skills into a project."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from validate_memory_docs import EXPECTED_FILES, validate_memory_docs


def _copy_template_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8").replace("<memory-docs>/", "memory-docs/")
    destination.write_text(text, encoding="utf-8")


def _install_memory_docs(source_root: Path, target: Path, force: bool) -> list[str]:
    destination_root = target / "memory-docs"
    existing_standard = [
        relative for relative in EXPECTED_FILES if (destination_root / relative).exists()
    ]
    if existing_standard and not force:
        raise FileExistsError(
            f"memory-docs already contains standard files at {destination_root}; "
            "use --force to refresh only the standard files"
        )
    if force and destination_root.is_dir():
        preset_directories = {"detail_mem", "SHORT_MEMORY", "archive"}
        custom_directories = sorted(
            child.name
            for child in destination_root.iterdir()
            if child.is_dir()
            and not child.name.startswith(".")
            and child.name not in preset_directories
        )
        if custom_directories:
            raise RuntimeError(
                "refusing to force-refresh memory-docs with custom memory directories: "
                + ", ".join(custom_directories)
                + "; migrate standard files manually so DIRS.md registrations are preserved"
            )

    installed: list[str] = []
    for relative in EXPECTED_FILES:
        source = source_root / relative
        if not source.is_file():
            raise FileNotFoundError(f"template source is missing: {source}")
        destination = destination_root / relative
        _copy_template_file(source, destination)
        installed.append(str(destination))
    return installed


def _install_agents(
    source_root: Path,
    target: Path,
    replace_agents: bool,
) -> list[str]:
    source = source_root / "AGENTS.md"
    destination = target / "AGENTS.md"
    if destination.exists() and not replace_agents:
        return [
            f"SKIPPED {destination}: preserve existing project rules; "
            "merge the memory-docs section manually or use --replace-agents"
        ]
    shutil.copy2(source, destination)
    return [str(destination)]


def _install_skills(source_root: Path, target: Path, force: bool) -> list[str]:
    source_skills = source_root / ".claude" / "skills"
    if not source_skills.is_dir():
        raise FileNotFoundError(f"skill source does not exist: {source_skills}")

    destination_root = target / ".claude" / "skills"
    installed: list[str] = []
    for source in sorted(path for path in source_skills.iterdir() if path.is_dir()):
        destination = destination_root / source.name
        if destination.exists() and not force:
            installed.append(f"SKIPPED {destination}: use --force to refresh")
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, destination, dirs_exist_ok=True)
        installed.append(str(destination))
    return installed


def _install_tools(source_root: Path, target: Path, force: bool) -> list[str]:
    source = source_root / "scripts" / "validate_memory_docs.py"
    destination = target / ".memory-docs-tools" / "validate_memory_docs.py"
    if destination.exists() and not force:
        return [f"SKIPPED {destination}: use --force to refresh"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return [str(destination)]


def install_project(
    *,
    source_root: Path,
    target: Path,
    component: str,
    force: bool,
    replace_agents: bool,
) -> list[str]:
    source_root = source_root.expanduser().resolve()
    target = target.expanduser().resolve()
    if not target.is_dir():
        raise NotADirectoryError(f"target project does not exist: {target}")

    template_errors, _ = validate_memory_docs(source_root, template=True)
    if template_errors:
        raise RuntimeError("invalid template source:\n- " + "\n- ".join(template_errors))

    installed: list[str] = []
    if component in {"all", "memory-docs"}:
        installed.extend(_install_memory_docs(source_root, target, force))
        installed.extend(_install_agents(source_root, target, replace_agents))
        errors, warnings = validate_memory_docs(target)
        installed.extend(f"WARNING {warning}" for warning in warnings)
        if errors:
            raise RuntimeError("installed memory-docs failed validation:\n- " + "\n- ".join(errors))

    if component in {"all", "skills"}:
        installed.extend(_install_skills(source_root, target, force))
    if component in {"all", "tools"}:
        installed.extend(_install_tools(source_root, target, force))
    return installed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install memory-docs and companion skills into a project."
    )
    parser.add_argument("target", type=Path, help="Existing target project directory")
    parser.add_argument(
        "--component",
        choices=("all", "memory-docs", "skills", "tools"),
        default="all",
        help="Install everything or only memory-docs, local skills, or validation tools",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Refresh standard memory files and existing local skill directories",
    )
    parser.add_argument(
        "--replace-agents",
        action="store_true",
        help="Explicitly replace an existing AGENTS.md instead of preserving it",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_root = Path(__file__).resolve().parent.parent
    installed = install_project(
        source_root=source_root,
        target=args.target,
        component=args.component,
        force=args.force,
        replace_agents=args.replace_agents,
    )
    print(f"Installed from {source_root} to {args.target.expanduser().resolve()}:")
    for item in installed:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
