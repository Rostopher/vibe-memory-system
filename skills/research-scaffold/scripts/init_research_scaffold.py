#!/usr/bin/env python3
"""Create selected research directories and optionally install current project memory."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence


DIRECTORY_PURPOSES = {
    "notes": "Digested paper reading, methods, data understanding, and research judgments.",
    "ideas": "Research questions, claims, proposals, and failed or parked directions.",
    "papers": "Source PDFs, metadata, OCR, extracted figures, and generated literature artifacts.",
    "repos": "External reference repositories, read-only unless changes are authorized.",
    "data": "Datasets, dictionaries, provenance, and versioned transformation inputs.",
    "modules": "Executable research workflows, local probes, maintained tests, and run artifacts.",
    "manuscripts": "Reader-facing drafts, appendices, and traceable paper assets.",
}

DIRECTORY_GUIDANCE = {
    "notes": """Organize by actual needs, such as paper-reading, methods, data, or pipelines.
Separate authors' claims, your inferences, and verified evidence. Detailed notes
can be long; source PDFs and OCR belong in papers/, formal prose in manuscripts/.
""",
    "ideas": """Capture the question or claim, evidence, assumptions, possible failure reasons,
and the next way to reduce uncertainty. Preserve failed or parked ideas with
stop reasons and reopening conditions. An exploratory experiment is not software
regression coverage. Link to one detailed owner instead of duplicating records.
""",
    "papers": """Treat OCR and parser outputs as generated artifacts. Human reading notes belong
in notes/. Explicit metadata or OCR corrections should remain traceable or
reproducible when artifacts are regenerated.
""",
    "repos": """Record the source and revision used for reference or reproduction. Keep project
implementation in its own modules. Authorized patches to reference code should
remain traceable; production workflows should not rely on an untracked patch.
""",
    "data": """Add raw/, interim/, processed/, external/, or dictionaries/ only when useful.
Record source, version, keys, sample definitions, units, missing-value semantics,
and transformations. External storage is valid: keep locators and reproducibility
metadata. Decide what to version or ignore dataset by dataset; do not blanket-ignore
all data. Small reproducible fixtures may belong with maintained tests.
""",
    "modules": """Use an isolated demo for an unknown technical direction, a probe_<purpose> script
for a local uncertainty, or implement directly when the path is clear. A working
demo can remain unintegrated. Integration needs module ownership, a complete
runtime path, and verification of affected behavior.

Add only the files a module needs: a reusable entry point, README, probe, tests,
outputs, or logs. Python tests normally use test_*.py; probes observe behavior
and do not establish regression coverage. Classify old _test_ files before any
separately arranged migration. Keep existing src/ and tests/ layouts where useful.

Protect data contracts, sample and variable definitions, key analytical results,
and important execution paths. Compare results using known data/config versions;
explain intentional baseline changes. Record coverage gaps rather than claiming
a probe proves everything works.

Resolve Python paths with pathlib from script resources, configuration, or explicit
inputs. Output storage is configurable and traceable. Preview unfamiliar large
inputs before choosing full, chunked, or streaming reads. Keep errors, skips, and
fallbacks visible. Retain run commands, code/data versions, configuration, and
artifacts as needed for reproducibility; include a patch or snapshot for dirty code.

Complete cleanup required for current integration. Propose broader consolidation
from structural evidence and let the user decide its scope and timing.
""",
    "manuscripts": """Add draft, section, appendix, or asset directories when useful. Keep figures and
tables traceable to upstream code, data versions, and configuration. Raw reading
notes and OCR belong in their own layers, not in formal manuscript prose.
""",
}

GITIGNORE = """.DS_Store
__pycache__/
*.py[cod]
.venv/
venv/
.env
.env.*
!.env.example
.ipynb_checkpoints/
*.log
modules/**/logs/
modules/**/outputs/tmp/
tmp/
cache/
.cache/
"""

IGNORE = """modules/**/logs/
**/__pycache__/
.venv/
venv/
.cache/
cache/
tmp/
papers/**/images/
"""


def find_memory_root(target: Path, explicit_root: Path | None = None) -> Path | None:
    """Recognize common layouts; other existing roots must be named explicitly."""
    if explicit_root is not None:
        root = (target / explicit_root.expanduser()).resolve()
        if not root.is_relative_to(target) or not root.is_dir():
            raise ValueError("--memory-root must name an existing directory inside the project")
        return root

    candidates = []
    conventional = target / "memory-docs"
    if conventional.exists():
        if not conventional.is_dir():
            raise NotADirectoryError(f"memory-docs is not a directory: {conventional}")
        candidates.append(conventional)
    legacy = target / "docs"
    if (legacy / "STATUS.md").is_file() and any(
        (legacy / marker).exists()
        for marker in ("OVERVIEW.md", "CONVENTIONS.md", "detail_mem")
    ):
        candidates.append(legacy)
    if len(candidates) > 1:
        raise ValueError("Multiple memory roots found; select the active one with --memory-root")
    return candidates[0] if candidates else None


def preflight_paths(
    target: Path, directories: Sequence[str], memory_root: Path | None
) -> None:
    """Check all scaffold destinations before writing into an existing project."""
    file_paths = [target / name for name in ("README.md", ".gitignore", ".ignore")]
    file_paths.extend(target / name / "README.md" for name in directories)
    for destination in file_paths:
        if memory_root is not None and destination.is_relative_to(memory_root):
            raise ValueError(f"Scaffold destination overlaps project memory: {destination}")
        current = target
        parts = destination.relative_to(target).parts
        for index, part in enumerate(parts):
            current = current / part
            if current.is_symlink() or getattr(current, "is_junction", lambda: False)():
                raise ValueError(f"Refusing to write through a linked scaffold path: {current}")
            if not current.exists():
                continue
            if index < len(parts) - 1 and not current.is_dir():
                raise NotADirectoryError(f"Scaffold directory is occupied by a file: {current}")
            if index == len(parts) - 1 and not current.is_file():
                raise IsADirectoryError(f"Scaffold file is occupied by a directory: {current}")


def write_if_missing(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def project_readme(target: Path, memory_root: Path | None) -> str:
    lines = [
        "# Research Project", "", "## Directory Map", "",
        "| Path | Purpose |", "|---|---|",
    ]
    if memory_root is not None:
        entry = next(
            (
                memory_root / name for name in ("INDEX.md", "README.md")
                if (memory_root / name).is_file()
            ),
            memory_root,
        )
        lines.append(
            f"| `{entry.relative_to(target).as_posix()}` | Project memory; "
            "follow its existing entry and ownership contract. |"
        )
    for name, purpose in DIRECTORY_PURPOSES.items():
        if (target / name).is_dir():
            lines.append(f"| `{name}/` | {purpose} |")
    if memory_root is None:
        lines.extend([
            "", "Project memory is not installed. Install the current vibe-memory-system when needed.",
        ])
    lines.extend([
        "", "## Working Rhythm", "",
        "Use an isolated demo, a local probe, or direct implementation according to uncertainty.",
        "Verify affected behavior during integration; keep detailed evidence with one owner.",
        "Run artifacts and requested research notes are work products. Consolidate project memory",
        "at a completed work unit after confirming closeout and scope with the user; an explicit",
        "initialization, memory update, migration, or handoff request already authorizes that scope.",
        "Detailed evidence may be long. Avoid updating memory after every small edit or probe.",
        "", "Directory names are adaptable: keep established implementation, test, and data layouts.", "",
    ])
    return "\n".join(lines)


def init_scaffold(
    target: Path,
    force: bool = False,
    memory_system: Path | None = None,
    *,
    directories: Sequence[str] | None = None,
    memory_root: Path | None = None,
) -> list[Path]:
    target = target.expanduser().resolve()
    if target.exists() and not target.is_dir():
        raise NotADirectoryError(f"Target is not a directory: {target}")
    selected = list(dict.fromkeys(DIRECTORY_PURPOSES if directories is None else directories))
    if not selected or any(name not in DIRECTORY_PURPOSES for name in selected):
        raise ValueError("Select at least one supported research directory")
    active_memory = find_memory_root(target, memory_root)
    installer = None
    if active_memory is None and memory_system is not None:
        installer = memory_system.expanduser().resolve() / "scripts" / "install_to_project.py"
        if not installer.is_file():
            raise FileNotFoundError(f"vibe-memory-system installer not found: {installer}")
    preflight_paths(target, selected, active_memory)
    target.mkdir(parents=True, exist_ok=True)
    if active_memory is not None:
        print(f"Preserving existing project memory at {active_memory}")
    elif installer is not None:
        subprocess.run(
            [sys.executable, "-B", str(installer), str(target), "--component", "memory-docs"],
            check=True,
        )
        active_memory = target / "memory-docs"
        print("Memory template installed; use init-memory to populate evidence-backed project facts.")
    else:
        print("Project memory was not installed; supply --memory-system to install the current template.")

    written = []
    for name in selected:
        directory = target / name
        directory.mkdir(exist_ok=True)
        content = f"# {name.title()}\n\n{DIRECTORY_PURPOSES[name]}\n\n{DIRECTORY_GUIDANCE[name]}"
        if write_if_missing(directory / "README.md", content, force):
            written.append(directory / "README.md")
    for name, content in (
        ("README.md", project_readme(target, active_memory)),
        (".gitignore", GITIGNORE),
        (".ignore", IGNORE),
    ):
        if write_if_missing(target / name, content, force):
            written.append(target / name)
    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="Target research project directory.")
    parser.add_argument(
        "--force", action="store_true",
        help="Replace selected directory READMEs and root README/ignore files; preserve AGENTS and memory.",
    )
    parser.add_argument(
        "--memory-system", type=Path,
        help="Current vibe-memory-system source repository; used only if no existing memory root is found.",
    )
    parser.add_argument(
        "--memory-root", type=Path,
        help="Existing memory root inside the project; absolute or relative to target. Never creates or migrates it.",
    )
    parser.add_argument(
        "--directories", nargs="+", choices=tuple(DIRECTORY_PURPOSES),
        help="Research directories to create; default: all seven, without nested scaffolds.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        written = init_scaffold(
            args.target, args.force, args.memory_system,
            directories=args.directories, memory_root=args.memory_root,
        )
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"Scaffold initialization failed: {exc}") from exc
    print(f"Research scaffold ready at {args.target.expanduser().resolve()}")
    print(f"Wrote {len(written)} scaffold files; existing files were preserved unless --force was supplied.")


if __name__ == "__main__":
    main()
