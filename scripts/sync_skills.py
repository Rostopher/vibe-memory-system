#!/usr/bin/env python3
"""Safely synchronize the repository's canonical skills into CLI skill roots."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping, Sequence


MANIFEST_FILENAME = ".vibe-memory-system-skills.json"
MANIFEST_SCHEMA_VERSION = 1
SOURCE_ID = "vibe-memory-system/skills"
SKILL_TARGETS = {
    "claude": Path(".claude/skills"),
    "codex": Path(".agents/skills"),
}


class SkillSyncConflict(RuntimeError):
    """Raised when synchronization would overwrite unowned or modified content."""


@dataclass(frozen=True)
class _TargetState:
    name: str
    root: Path
    managed: dict[str, str]
    observed_hashes: dict[str, str | None]
    manifest_snapshot: bytes | None


@dataclass
class _TargetPlan:
    state: _TargetState
    stage_root: Path
    backup_root: Path
    replacements: dict[str, Path]
    removals: set[str]
    desired_hashes: dict[str, str]
    desired_manifest: bytes
    staged_manifest: Path
    messages: list[str]
    preserve_backup: bool = False


@dataclass
class _Touch:
    destination: Path
    backup: Path
    expected_kind: str | None = None
    expected_value: str | bytes | None = None
    had_old: bool = False
    installed_new: bool = False


def _path_exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def _remove_path(path: Path) -> None:
    if not _path_exists(path):
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
    else:
        shutil.rmtree(path)


def _hash_skill_tree(root: Path) -> str:
    if not root.is_dir():
        raise NotADirectoryError(f"skill is not a directory: {root}")

    digest = hashlib.sha256()

    def add_field(value: bytes) -> None:
        digest.update(len(value).to_bytes(8, "big"))
        digest.update(value)

    def add_record(*fields: bytes) -> None:
        add_field(len(fields).to_bytes(2, "big"))
        for field_value in fields:
            add_field(field_value)

    add_record(
        b"tree-v2",
        f"{root.stat().st_mode & 0o111:03o}".encode("ascii"),
    )
    entries = sorted(root.rglob("*"), key=lambda path: path.relative_to(root).as_posix())
    for path in entries:
        if path.name == ".DS_Store":
            continue
        relative = path.relative_to(root).as_posix().encode("utf-8")
        if path.is_symlink():
            add_record(
                b"symlink",
                relative,
                os.readlink(path).encode("utf-8"),
            )
        elif path.is_dir():
            add_record(
                b"directory",
                relative,
                f"{path.stat().st_mode & 0o111:03o}".encode("ascii"),
            )
        elif path.is_file():
            content_digest = hashlib.sha256()
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    content_digest.update(chunk)
            add_record(
                b"file",
                relative,
                f"{path.stat().st_mode & 0o111:03o}".encode("ascii"),
                content_digest.digest(),
            )
    return digest.hexdigest()


def _source_snapshot(source_skills: Path) -> tuple[dict[str, Path], dict[str, str]]:
    source_skills = Path(
        os.path.abspath(os.fspath(Path(source_skills).expanduser()))
    )
    if source_skills.is_symlink():
        raise RuntimeError(
            f"skill source must not be a symbolic link: {source_skills}"
        )
    source_skills = source_skills.resolve()
    if not source_skills.is_dir():
        raise FileNotFoundError(f"skill source does not exist: {source_skills}")

    symlinked_skills = [
        path.name
        for path in sorted(source_skills.iterdir())
        if path.is_symlink() and not path.name.startswith(".")
    ]
    if symlinked_skills:
        raise RuntimeError(
            "top-level skill sources must not be symbolic links: "
            + ", ".join(symlinked_skills)
        )
    paths = {
        path.name: path
        for path in sorted(source_skills.iterdir())
        if path.is_dir() and not path.name.startswith(".")
    }
    if not paths:
        raise RuntimeError(f"refusing to sync an empty skill source: {source_skills}")

    missing_entrypoints = [
        name for name, path in paths.items() if not (path / "SKILL.md").is_file()
    ]
    if missing_entrypoints:
        raise RuntimeError(
            "skill source directories missing SKILL.md: "
            + ", ".join(sorted(missing_entrypoints))
        )
    return paths, {name: _hash_skill_tree(path) for name, path in paths.items()}


def _manifest_bytes(hashes: Mapping[str, str]) -> bytes:
    payload = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "source": SOURCE_ID,
        "skills": dict(sorted(hashes.items())),
    }
    return (
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def _load_manifest(root: Path) -> tuple[dict[str, str] | None, bytes | None]:
    path = root / MANIFEST_FILENAME
    if path.is_symlink():
        raise SkillSyncConflict(
            f"sync manifest must not be a symbolic link: {path}"
        )
    if _path_exists(path) and not path.is_file():
        raise SkillSyncConflict(
            f"sync manifest must be a regular file: {path}"
        )
    if not _path_exists(path):
        return None, None
    try:
        snapshot = path.read_bytes()
        payload = json.loads(snapshot.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SkillSyncConflict(f"invalid sync manifest {path}: {exc}") from exc

    if not isinstance(payload, dict):
        raise SkillSyncConflict(
            f"invalid sync manifest {path}: top-level value must be an object"
        )
    if payload.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        raise SkillSyncConflict(
            f"unsupported sync manifest schema in {path}: "
            f"{payload.get('schema_version')!r}"
        )
    if payload.get("source") != SOURCE_ID:
        raise SkillSyncConflict(
            f"sync manifest at {path} belongs to {payload.get('source')!r}, "
            f"not {SOURCE_ID!r}"
        )
    skills = payload.get("skills")
    if not isinstance(skills, dict):
        raise SkillSyncConflict(f"invalid skills map in sync manifest {path}")

    managed: dict[str, str] = {}
    for name, digest in skills.items():
        if (
            not isinstance(name, str)
            or not name
            or name in {".", ".."}
            or "/" in name
            or "\\" in name
            or not isinstance(digest, str)
            or len(digest) != 64
            or any(character not in "0123456789abcdef" for character in digest)
        ):
            raise SkillSyncConflict(f"invalid skill entry in sync manifest {path}")
        managed[name] = digest
    return managed, snapshot


def _destination_hash(path: Path) -> str | None:
    if not _path_exists(path):
        return None
    if not path.is_dir() or path.is_symlink():
        return "<non-directory>"
    return _hash_skill_tree(path)


def _normalize_destination_root(root_value: Path) -> Path:
    root = Path(os.path.abspath(os.fspath(Path(root_value).expanduser())))
    for candidate in (root.parent, root):
        if candidate.is_symlink():
            raise SkillSyncConflict(
                f"skill destination must not traverse a symbolic link: {candidate}"
            )
    return root.resolve()


def check_skill_targets(
    source_skills: Path,
    destinations: Mapping[str, Path],
) -> list[str]:
    """Return human-readable drift issues without changing any destination."""

    _, source_hashes = _source_snapshot(source_skills)
    issues: list[str] = []
    for target_name, root_value in sorted(destinations.items()):
        try:
            root = _normalize_destination_root(Path(root_value))
            managed, _ = _load_manifest(root)
        except SkillSyncConflict as exc:
            issues.append(f"{target_name}: {exc}")
            continue
        if managed is None:
            issues.append(f"{target_name}: sync manifest is missing")
            continue

        for skill_name, source_hash in sorted(source_hashes.items()):
            installed_hash = managed.get(skill_name)
            current_hash = _destination_hash(root / skill_name)
            if installed_hash is None:
                issues.append(
                    f"{target_name}/{skill_name}: unmanaged or manifest entry missing"
                )
                continue
            if current_hash is None:
                issues.append(f"{target_name}/{skill_name}: installed skill is missing")
                continue
            if current_hash == source_hash and installed_hash != source_hash:
                issues.append(
                    f"{target_name}/{skill_name}: manifest is outdated"
                )
                continue
            if current_hash != installed_hash:
                issues.append(
                    f"{target_name}/{skill_name}: installed skill was modified"
                )
            if source_hash != installed_hash:
                issues.append(
                    f"{target_name}/{skill_name}: installed skill is outdated "
                    "relative to source"
                )

        for skill_name, installed_hash in sorted(managed.items()):
            if skill_name in source_hashes:
                continue
            current_hash = _destination_hash(root / skill_name)
            if current_hash is None:
                issues.append(
                    f"{target_name}/{skill_name}: stale manifest entry for removed source"
                )
            elif current_hash == installed_hash:
                issues.append(
                    f"{target_name}/{skill_name}: source removed but installed copy remains"
                )
            else:
                issues.append(
                    f"{target_name}/{skill_name}: removed source has modified installed copy"
                )
    return issues


def _inspect_targets(
    source_hashes: Mapping[str, str],
    destinations: Mapping[str, Path],
    *,
    force: bool,
) -> list[_TargetState]:
    states: list[_TargetState] = []
    conflicts: list[str] = []
    for target_name, root_value in sorted(destinations.items()):
        root = _normalize_destination_root(Path(root_value))
        loaded_manifest, manifest_snapshot = _load_manifest(root)
        managed = loaded_manifest or {}
        observed_hashes = {
            skill_name: _destination_hash(root / skill_name)
            for skill_name in sorted(set(source_hashes) | set(managed))
        }
        for skill_name, source_hash in sorted(source_hashes.items()):
            current_hash = observed_hashes[skill_name]
            installed_hash = managed.get(skill_name)
            if current_hash is None:
                continue
            if installed_hash is None:
                conflicts.append(
                    f"{target_name}/{skill_name}: unmanaged destination exists"
                )
                continue
            if current_hash not in {installed_hash, source_hash}:
                conflicts.append(
                    f"{target_name}/{skill_name}: installed skill was modified"
                )

        for skill_name, installed_hash in sorted(managed.items()):
            if skill_name in source_hashes:
                continue
            current_hash = observed_hashes[skill_name]
            if current_hash is not None and current_hash != installed_hash:
                conflicts.append(
                    f"{target_name}/{skill_name}: removed source has modified "
                    "installed copy"
                )
        states.append(
            _TargetState(
                target_name,
                root,
                managed,
                observed_hashes,
                manifest_snapshot,
            )
        )

    if conflicts and not force:
        raise SkillSyncConflict(
            "skill synchronization conflicts; rerun with --force only if these "
            "generated copies may be replaced:\n- "
            + "\n- ".join(conflicts)
        )
    return states


def _copy_skill_tree(source: Path, destination: Path) -> None:
    shutil.copytree(
        source,
        destination,
        symlinks=True,
        ignore=shutil.ignore_patterns(".DS_Store"),
    )


def _current_manifest_snapshot(root: Path) -> bytes | None:
    _, snapshot = _load_manifest(root)
    return snapshot


def _verify_target_unchanged(state: _TargetState) -> None:
    try:
        current_manifest = _current_manifest_snapshot(state.root)
    except SkillSyncConflict as exc:
        raise SkillSyncConflict(
            f"{state.name}: destination changed during synchronization: {exc}"
        ) from exc
    if current_manifest != state.manifest_snapshot:
        raise SkillSyncConflict(
            f"{state.name}: sync manifest changed during synchronization"
        )
    for skill_name, expected_hash in state.observed_hashes.items():
        current_hash = _destination_hash(state.root / skill_name)
        if current_hash != expected_hash:
            raise SkillSyncConflict(
                f"{state.name}/{skill_name}: destination changed during "
                "synchronization"
            )


def _verify_skill_unchanged(state: _TargetState, skill_name: str) -> None:
    expected_hash = state.observed_hashes.get(skill_name)
    current_hash = _destination_hash(state.root / skill_name)
    if current_hash != expected_hash:
        raise SkillSyncConflict(
            f"{state.name}/{skill_name}: destination changed during synchronization"
        )


def _stage_target(
    state: _TargetState,
    source_paths: Mapping[str, Path],
    source_hashes: Mapping[str, str],
    manifest: bytes,
) -> _TargetPlan | None:
    replacements: dict[str, Path] = {}
    removals = {
        name
        for name in state.managed
        if name not in source_hashes and _path_exists(state.root / name)
    }
    changed_names = {
        name
        for name, digest in source_hashes.items()
        if _destination_hash(state.root / name) != digest
    }
    manifest_path = state.root / MANIFEST_FILENAME
    manifest_current = (
        manifest_path.read_bytes() if manifest_path.is_file() else None
    )
    if not changed_names and not removals and manifest_current == manifest:
        return None

    parent = state.root.parent
    parent.mkdir(parents=True, exist_ok=True)
    stage_root: Path | None = None
    backup_root: Path | None = None
    try:
        stage_root = Path(
            tempfile.mkdtemp(prefix=".vibe-memory-system-stage-", dir=parent)
        )
        backup_root = Path(
            tempfile.mkdtemp(prefix=".vibe-memory-system-backup-", dir=parent)
        )
        staged_skills = stage_root / "skills"
        for name in sorted(changed_names):
            destination = staged_skills / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            _copy_skill_tree(source_paths[name], destination)
            if _hash_skill_tree(destination) != source_hashes[name]:
                raise RuntimeError(f"staged skill verification failed: {name}")
            replacements[name] = destination

        staged_manifest = stage_root / MANIFEST_FILENAME
        staged_manifest.write_bytes(manifest)
        messages = [
            f"SYNCED {state.name}: {name}" for name in sorted(changed_names)
        ]
        messages.extend(
            f"REMOVED {state.name}: {name}" for name in sorted(removals)
        )
        return _TargetPlan(
            state=state,
            stage_root=stage_root,
            backup_root=backup_root,
            replacements=replacements,
            removals=removals,
            desired_hashes=dict(source_hashes),
            desired_manifest=manifest,
            staged_manifest=staged_manifest,
            messages=messages,
        )
    except BaseException:
        if stage_root is not None:
            shutil.rmtree(stage_root, ignore_errors=True)
        if backup_root is not None:
            shutil.rmtree(backup_root, ignore_errors=True)
        raise


def _touch_matches_expected_install(touch: _Touch) -> bool:
    if touch.expected_kind == "tree" and isinstance(touch.expected_value, str):
        return _destination_hash(touch.destination) == touch.expected_value
    if touch.expected_kind == "file" and isinstance(touch.expected_value, bytes):
        if touch.destination.is_symlink() or not touch.destination.is_file():
            return False
        return touch.destination.read_bytes() == touch.expected_value
    return False


def _commit_plans(plans: Sequence[_TargetPlan]) -> list[str]:
    touches: list[_Touch] = []
    messages: list[str] = []
    try:
        for plan in plans:
            _verify_target_unchanged(plan.state)
        for plan in plans:
            _verify_target_unchanged(plan.state)
            plan.state.root.mkdir(parents=True, exist_ok=True)
            names = sorted(set(plan.replacements) | plan.removals)
            for name in names:
                _verify_skill_unchanged(plan.state, name)
                destination = plan.state.root / name
                backup = plan.backup_root / "skills" / name
                staged = plan.replacements.get(name)
                touch = _Touch(
                    destination=destination,
                    backup=backup,
                    expected_kind="tree" if staged is not None else "absent",
                    expected_value=(
                        plan.desired_hashes[name] if staged is not None else None
                    ),
                )
                touches.append(touch)
                if _path_exists(destination):
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        os.replace(destination, backup)
                    finally:
                        touch.had_old = _path_exists(backup)
                if staged is not None:
                    try:
                        os.replace(staged, destination)
                    finally:
                        touch.installed_new = (
                            not _path_exists(staged) and _path_exists(destination)
                        )

            for skill_name in plan.replacements:
                expected_hash = plan.desired_hashes[skill_name]
                current_hash = _destination_hash(plan.state.root / skill_name)
                if current_hash != expected_hash:
                    raise SkillSyncConflict(
                        f"{plan.state.name}/{skill_name}: destination changed "
                        "during synchronization"
                    )
            for skill_name in plan.removals:
                if _destination_hash(plan.state.root / skill_name) is not None:
                    raise SkillSyncConflict(
                        f"{plan.state.name}/{skill_name}: removed skill reappeared "
                        "during synchronization"
                    )
            if _current_manifest_snapshot(plan.state.root) != plan.state.manifest_snapshot:
                raise SkillSyncConflict(
                    f"{plan.state.name}: sync manifest changed during synchronization"
                )
            manifest_destination = plan.state.root / MANIFEST_FILENAME
            manifest_backup = plan.backup_root / MANIFEST_FILENAME
            manifest_touch = _Touch(
                destination=manifest_destination,
                backup=manifest_backup,
                expected_kind="file",
                expected_value=plan.desired_manifest,
            )
            touches.append(manifest_touch)
            if _path_exists(manifest_destination):
                try:
                    os.replace(manifest_destination, manifest_backup)
                finally:
                    manifest_touch.had_old = _path_exists(manifest_backup)
            try:
                os.replace(plan.staged_manifest, manifest_destination)
            finally:
                manifest_touch.installed_new = (
                    not _path_exists(plan.staged_manifest)
                    and _path_exists(manifest_destination)
                )
            messages.extend(plan.messages)
            if not plan.messages:
                messages.append(f"UPDATED {plan.state.name}: sync manifest")
    except BaseException as commit_error:
        rollback_errors: list[str] = []
        for touch in reversed(touches):
            try:
                if touch.installed_new:
                    if not _touch_matches_expected_install(touch):
                        rollback_errors.append(
                            f"{touch.destination}: changed after commit; current "
                            f"content and recovery backup {touch.backup} were preserved"
                        )
                        continue
                    _remove_path(touch.destination)
                if touch.had_old and _path_exists(touch.backup):
                    if _path_exists(touch.destination):
                        rollback_errors.append(
                            f"{touch.destination}: destination is occupied during rollback; "
                            f"current content and recovery backup {touch.backup} "
                            "were preserved"
                        )
                        continue
                    touch.destination.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(touch.backup, touch.destination)
            except BaseException as rollback_error:
                rollback_errors.append(
                    f"{touch.destination}: {rollback_error}"
                )
        if rollback_errors:
            for plan in plans:
                plan.preserve_backup = True
            raise RuntimeError(
                "skill sync failed and rollback was incomplete:\n- "
                + "\n- ".join(rollback_errors)
                + "\nrecovery backups were preserved at:\n- "
                + "\n- ".join(str(plan.backup_root) for plan in plans)
            ) from commit_error
        raise
    return messages


def sync_skill_targets(
    source_skills: Path,
    destinations: Mapping[str, Path],
    *,
    force: bool = False,
) -> list[str]:
    """Synchronize skills transactionally across all requested destinations."""

    if not destinations:
        raise ValueError("at least one skill destination is required")
    source_paths, source_hashes = _source_snapshot(source_skills)
    states = _inspect_targets(source_hashes, destinations, force=force)
    manifest = _manifest_bytes(source_hashes)
    plans: list[_TargetPlan] = []
    try:
        for state in states:
            plan = _stage_target(state, source_paths, source_hashes, manifest)
            if plan is not None:
                plans.append(plan)
        return _commit_plans(plans)
    finally:
        for plan in plans:
            shutil.rmtree(plan.stage_root, ignore_errors=True)
            if not plan.preserve_backup:
                shutil.rmtree(plan.backup_root, ignore_errors=True)


def _destination_map(base: Path, target: str) -> dict[str, Path]:
    names = tuple(SKILL_TARGETS) if target == "both" else (target,)
    return {name: base / SKILL_TARGETS[name] for name in names}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synchronize canonical skills with drift detection and rollback."
    )
    parser.add_argument(
        "--target",
        choices=(*SKILL_TARGETS, "both"),
        required=True,
        help="CLI destination to synchronize",
    )
    parser.add_argument(
        "--base",
        type=Path,
        default=Path.home(),
        help="Base directory containing .claude/ or .agents/ (default: HOME)",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "skills",
        help="Canonical skills directory",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace unmanaged or locally modified destination skills",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report drift without changing destination files",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    destinations = _destination_map(args.base.expanduser().resolve(), args.target)
    if args.check:
        issues = check_skill_targets(args.source, destinations)
        if issues:
            for issue in issues:
                print(f"OUT-OF-SYNC {issue}")
            return 1
        print("Skill destinations are in sync.")
        return 0

    try:
        messages = sync_skill_targets(
            args.source,
            destinations,
            force=args.force,
        )
    except SkillSyncConflict as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if messages:
        for message in messages:
            print(message)
    else:
        print("Skill destinations are already in sync.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
