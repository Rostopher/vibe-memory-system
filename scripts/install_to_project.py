#!/usr/bin/env python3
"""Install the current memory-docs template and companion skills into a project."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from sync_skills import MANIFEST_FILENAME, SKILL_TARGETS, sync_skill_targets
from validate_memory_docs import EXPECTED_FILES, validate_memory_docs


def _copy_template_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8").replace("<memory-docs>/", "memory-docs/")
    destination.write_text(text, encoding="utf-8")


def _assert_no_symbolic_link_components(base: Path, destination: Path) -> None:
    try:
        relative = destination.relative_to(base)
    except ValueError as exc:
        raise RuntimeError(
            f"managed install path escapes target project: {destination}"
        ) from exc

    current = base
    for component in relative.parts:
        current = current / component
        if current.is_symlink():
            raise RuntimeError(
                f"refusing to write through symbolic link in managed path: {current}"
            )


def _preflight_managed_paths(
    source_root: Path,
    target: Path,
    component: str,
    skill_target: str | None,
) -> None:
    destinations: list[Path] = []
    if component in {"all", "memory-docs"}:
        destinations.extend(
            target / "memory-docs" / relative for relative in EXPECTED_FILES
        )
        destinations.append(target / "AGENTS.md")
    if component in {"all", "skills"}:
        if skill_target is None:
            raise ValueError(
                "skill_target is required when component includes skills"
            )
        target_names = (
            tuple(SKILL_TARGETS) if skill_target == "both" else (skill_target,)
        )
        skill_names = sorted(
            path.name
            for path in (source_root / "skills").iterdir()
            if path.is_dir() and not path.name.startswith(".")
        )
        for target_name in target_names:
            destination_root = target / SKILL_TARGETS[target_name]
            destinations.append(destination_root / MANIFEST_FILENAME)
            destinations.extend(
                destination_root / skill_name for skill_name in skill_names
            )
    if component in {"all", "tools"}:
        destinations.append(
            target / ".memory-docs-tools" / "validate_memory_docs.py"
        )

    for destination in destinations:
        _assert_no_symbolic_link_components(target, destination)


def _install_memory_docs(
    source_root: Path,
    target: Path,
    force: bool,
    replace_memory_docs: bool,
) -> list[str]:
    destination_root = target / "memory-docs"
    existing_standard = [
        relative for relative in EXPECTED_FILES if (destination_root / relative).exists()
    ]
    if existing_standard and not force and not replace_memory_docs:
        raise FileExistsError(
            f"memory-docs already contains standard files at {destination_root}; "
            "use --force to preserve existing memory while adding missing files, "
            "then run an explicit init-memory protocol migration; use "
            "--replace-memory-docs only to intentionally reset standard files"
        )
    if replace_memory_docs and destination_root.is_dir():
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
                "refusing to replace memory-docs with custom memory directories: "
                + ", ".join(custom_directories)
                + "; migrate standard files manually so DIRS.md registrations are preserved"
            )

    installed: list[str] = []
    for relative in EXPECTED_FILES:
        source = source_root / relative
        if not source.is_file():
            raise FileNotFoundError(f"template source is missing: {source}")
        destination = destination_root / relative
        if destination.exists() and not replace_memory_docs:
            installed.append(f"SKIPPED {destination}: preserve existing project memory")
            continue
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
            "merge the memory-docs section manually or with an init-memory "
            "protocol migration; use --replace-agents only for full replacement"
        ]
    shutil.copy2(source, destination)
    return [str(destination)]


def _install_skills(
    source_root: Path,
    target: Path,
    force: bool,
    skill_target: str | None,
) -> list[str]:
    if skill_target is None:
        raise ValueError(
            "skill_target is required when installing skills; "
            "choose claude, codex, or both"
        )
    source_skills = source_root / "skills"
    if not source_skills.is_dir():
        raise FileNotFoundError(f"skill source does not exist: {source_skills}")

    target_names = tuple(SKILL_TARGETS) if skill_target == "both" else (skill_target,)
    destinations = {
        target_name: target / SKILL_TARGETS[target_name]
        for target_name in target_names
    }
    return sync_skill_targets(source_skills, destinations, force=force)


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
    replace_memory_docs: bool = False,
    skill_target: str | None = None,
) -> list[str]:
    source_root = source_root.expanduser().resolve()
    target = target.expanduser().resolve()
    if not target.is_dir():
        raise NotADirectoryError(f"target project does not exist: {target}")
    if skill_target is not None and skill_target not in {*SKILL_TARGETS, "both"}:
        raise ValueError(f"unsupported skill target: {skill_target}")
    if component in {"all", "skills"} and skill_target is None:
        raise ValueError(
            "skill_target is required when component includes skills; "
            "choose claude, codex, or both"
        )

    template_errors, _ = validate_memory_docs(source_root, template=True)
    if template_errors:
        raise RuntimeError("invalid template source:\n- " + "\n- ".join(template_errors))
    _preflight_managed_paths(
        source_root,
        target,
        component,
        skill_target,
    )

    installed: list[str] = []
    if component in {"all", "memory-docs"}:
        installed.extend(
            _install_memory_docs(
                source_root,
                target,
                force,
                replace_memory_docs,
            )
        )
        installed.extend(_install_agents(source_root, target, replace_agents))
        errors, warnings = validate_memory_docs(target)
        installed.extend(f"WARNING {warning}" for warning in warnings)
        if errors:
            raise RuntimeError("installed memory-docs failed validation:\n- " + "\n- ".join(errors))

    if component in {"all", "skills"}:
        installed.extend(_install_skills(source_root, target, force, skill_target))
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
        help=(
            "Replace drifted/unmanaged skill copies, refresh tools, and add missing "
            "memory files without replacing existing memory"
        ),
    )
    parser.add_argument(
        "--replace-memory-docs",
        action="store_true",
        help="Explicitly replace standard memory files; project-specific extra files are preserved",
    )
    parser.add_argument(
        "--replace-agents",
        action="store_true",
        help="Explicitly replace an existing AGENTS.md instead of preserving it",
    )
    parser.add_argument(
        "--skill-target",
        choices=("claude", "codex", "both"),
        help=(
            "Required with --component all|skills: install local skills for "
            "Claude Code, Codex, or both"
        ),
    )
    args = parser.parse_args()
    if args.component in {"all", "skills"} and args.skill_target is None:
        parser.error(
            "--skill-target is required when --component is all or skills; "
            "choose claude, codex, or both"
        )
    return args


def main() -> int:
    args = parse_args()
    source_root = Path(__file__).resolve().parent.parent
    installed = install_project(
        source_root=source_root,
        target=args.target,
        component=args.component,
        force=args.force,
        replace_agents=args.replace_agents,
        replace_memory_docs=args.replace_memory_docs,
        skill_target=args.skill_target,
    )
    print(f"Installed from {source_root} to {args.target.expanduser().resolve()}:")
    for item in installed:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
