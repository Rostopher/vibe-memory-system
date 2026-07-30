#!/usr/bin/env python3
"""Validate the structure and lightweight health of a memory-docs instance."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlparse


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

# Optional extensions are validated when present but never required.
OPTIONAL_FILES: dict[Path, FileSpec] = {
    Path("research/EXPERIMENT_LEDGER.md"): FileSpec("detail", "append"),
}

REQUIRED_FRONTMATTER_FIELDS = {
    "layer",
    "update_mode",
    "role",
    "read_when",
    "not_for",
}
OPTIONAL_POSITIVE_INTEGER_FIELDS = {"line_budget", "stale_after_days"}
PRESET_DIRECTORIES = {"detail_mem", "SHORT_MEMORY", "archive"}
MEMORY_ROOT_MARKERS = (
    Path("INDEX.md"),
    Path("OVERVIEW.md"),
    Path("STATUS.md"),
    Path("DIRS.md"),
    Path("detail_mem/MAP.md"),
)

DATE_RE = re.compile(
    r"(?i)(?:last\s+(?:verified|updated)|verified|updated|"
    r"最后(?:验证|更新)|更新日期|验证日期|更新时间)"
    r"[^0-9]{0,24}(20\d{2}-\d{2}-\d{2})"
)
ARCHIVE_MANIFEST_FIELDS: dict[str, tuple[str, ...]] = {
    "Archived": (
        r"(?im)^\s*(?:[-*]\s+)?(?:\*\*)?"
        r"(?:archived|archive date|归档日期|归档时间)(?:\*\*)?\s*[:：]",
    ),
    "Reason": (
        r"(?im)^\s*(?:[-*]\s+)?(?:\*\*)?"
        r"(?:reason|archive reason|原因|归档原因)(?:\*\*)?\s*[:：]",
    ),
    "Preserves": (
        r"(?im)^\s*(?:[-*]\s+)?(?:\*\*)?"
        r"(?:preserves?|preserved sources?|保留(?:内容|来源|材料)?)"
        r"(?:\*\*)?\s*[:：]",
    ),
    "Distilled into": (
        r"(?im)^\s*(?:[-*]\s+)?(?:\*\*)?"
        r"(?:distilled into|distilled to|蒸馏(?:到|至|目标)|提炼(?:到|至))"
        r"(?:\*\*)?\s*[:：]",
    ),
    "Retrieval keywords": (
        r"(?im)^\s*(?:[-*]\s+)?(?:\*\*)?"
        r"(?:retrieval(?: keywords?)?|keywords?|检索(?:关键词|线索)?|"
        r"关键词|何时(?:重读|查阅|重新阅读))(?:\*\*)?\s*[:：]",
    ),
}

DUPLICATE_MIN_CHARS = 200
DUPLICATE_SIMILARITY = 0.94
DUPLICATE_MAX_PARAGRAPHS = 400
DUPLICATE_MAX_FINDINGS = 10
LONG_PROSE_MAX_CHARS = 500
LONG_PROSE_MAX_FINDINGS = 10


def _memory_root(path: Path, template: bool) -> Path:
    resolved = path.expanduser().resolve()
    if template or resolved.name == "memory-docs":
        return resolved
    installed = resolved / "memory-docs"
    if installed.is_dir():
        return installed
    if all((resolved / marker).is_file() for marker in MEMORY_ROOT_MARKERS):
        return resolved
    return installed


def _frontmatter(text: str) -> dict[str, str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == "---"
        )
    except StopIteration:
        return None

    values: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _validate_file_contract(
    root: Path,
    relative: Path,
    expected: FileSpec,
    *,
    required: bool,
    template: bool,
    allow_template_tokens: bool,
    errors: list[str],
    warnings: list[str],
) -> dict[str, str] | None:
    file_path = root / relative
    if not file_path.is_file():
        if required:
            errors.append(f"missing required file: {relative.as_posix()}")
        return None

    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read {relative.as_posix()}: {exc}")
        return None

    frontmatter = _frontmatter(text)
    if frontmatter is None:
        errors.append(f"invalid or missing frontmatter: {relative.as_posix()}")
        return None

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
    _validate_optional_integer_fields(relative, frontmatter, errors)

    if not template and not allow_template_tokens and "<memory-docs>/" in text:
        warnings.append(
            f"possible unresolved <memory-docs>/ token in {relative.as_posix()}"
        )
    return frontmatter


def _validate_optional_integer_fields(
    relative: Path,
    frontmatter: dict[str, str],
    errors: list[str],
) -> None:
    for field in sorted(OPTIONAL_POSITIVE_INTEGER_FIELDS):
        value = frontmatter.get(field)
        if value is None:
            continue
        try:
            parsed = int(value)
        except ValueError:
            parsed = -1
        minimum = 0 if field == "stale_after_days" else 1
        if parsed < minimum:
            qualifier = "non-negative" if minimum == 0 else "positive"
            errors.append(
                f"invalid {field} in {relative.as_posix()}: "
                f"expected a {qualifier} integer, got {value!r}"
            )


def _active_markdown_files(root: Path) -> list[Path]:
    """Return live Markdown files, excluding historical archive material."""
    sources: list[Path] = []
    for source in sorted(root.rglob("*.md")):
        try:
            relative = source.relative_to(root)
        except ValueError:
            continue
        if relative.parts and relative.parts[0] == "archive":
            continue
        sources.append(source)
    return sources


def _registered_directories(text: str) -> set[str]:
    """Read root directory registrations from structured DIRS entries."""
    registered: set[str] = set()

    def register(value: str) -> None:
        value = value.strip()
        if (
            not value.endswith("/")
            or any(marker in value for marker in ("<", ">", "{", "}"))
        ):
            return
        dirname = value[:-1].strip()
        if dirname and "/" not in dirname:
            registered.add(dirname)

    for line, _ in _visible_markdown_lines(text):
        stripped = line.strip()
        bullet = re.match(r"^\s*[-*+]\s+`([^`]+/)`(?:\s*[:：—-].*)?\s*$", line)
        if bullet is not None:
            register(bullet.group(1))
            continue

        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = stripped[1:-1].split("|")
        if not cells:
            continue
        first = cells[0].strip()
        if len(first) >= 2 and first.startswith("`") and first.endswith("`"):
            first = first[1:-1].strip()
        register(first)
    return registered


def _mask_inline_code(line: str) -> str:
    """Mask same-line backtick code spans while preserving character offsets."""
    masked = list(line)
    index = 0
    while index < len(line):
        if line[index] != "`":
            index += 1
            continue
        run_end = index
        while run_end < len(line) and line[run_end] == "`":
            run_end += 1
        delimiter = line[index:run_end]
        close = line.find(delimiter, run_end)
        if close < 0:
            index = run_end
            continue
        for position in range(index, close + len(delimiter)):
            masked[position] = " "
        index = close + len(delimiter)
    return "".join(masked)


def _visible_markdown_lines(text: str) -> Iterable[tuple[str, str]]:
    """Yield original and code-masked lines outside fenced code blocks."""
    fence_char: str | None = None
    fence_length = 0
    for line in text.splitlines():
        stripped = line.lstrip()
        if fence_char is not None:
            run_length = 0
            while (
                run_length < len(stripped)
                and stripped[run_length] == fence_char
            ):
                run_length += 1
            if (
                run_length >= fence_length
                and not stripped[run_length:].strip()
            ):
                fence_char = None
                fence_length = 0
            continue

        fence = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence is not None:
            delimiter = fence.group(1)
            fence_char = delimiter[0]
            fence_length = len(delimiter)
            continue
        yield line, _mask_inline_code(line)


def _is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return backslashes % 2 == 1


def _markdown_link_destinations(text: str) -> Iterable[str]:
    """Extract inline Markdown link targets with balanced parentheses."""
    for original, visible in _visible_markdown_lines(text):
        search_from = 0
        while True:
            close_label = visible.find("](", search_from)
            if close_label < 0:
                break
            if _is_escaped(visible, close_label):
                search_from = close_label + 2
                continue
            open_label = visible.rfind("[", 0, close_label)
            if open_label < 0 or _is_escaped(visible, open_label):
                search_from = close_label + 2
                continue

            target_start = close_label + 2
            depth = 1
            cursor = target_start
            while cursor < len(visible):
                character = visible[cursor]
                if character == "\\":
                    cursor += 2
                    continue
                if character == "(":
                    depth += 1
                elif character == ")":
                    depth -= 1
                    if depth == 0:
                        yield original[target_start:cursor]
                        cursor += 1
                        break
                cursor += 1
            search_from = max(cursor, close_label + 2)


def _link_destination(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        value = value[1 : value.index(">")]
    else:
        depth = 0
        escaped = False
        end = len(value)
        for index, character in enumerate(value):
            if escaped:
                escaped = False
                continue
            if character == "\\":
                escaped = True
            elif character == "(":
                depth += 1
            elif character == ")" and depth:
                depth -= 1
            elif character.isspace() and depth == 0:
                end = index
                break
        value = value[:end]
    value = re.sub(r"\\([\\() ])", r"\1", value)
    return unquote(value).strip()


def _extract_link_targets(
    source: Path,
    root: Path,
) -> Iterable[tuple[str, Path | None]]:
    try:
        text = source.read_text(encoding="utf-8")
    except OSError:
        return []

    targets: list[tuple[str, Path | None]] = []
    for raw_target in _markdown_link_destinations(text):
        display_raw = raw_target.strip()
        raw = _link_destination(raw_target)
        if not raw or raw.startswith("#") or raw.startswith("//"):
            continue
        try:
            parsed = urlparse(raw)
        except ValueError:
            targets.append((display_raw, None))
            continue
        if parsed.scheme:
            continue
        target = _resolve_local_link(raw_target, source, root)
        targets.append(target if target is not None else (display_raw, None))
    return targets


def _resolve_local_link(
    raw_target: str,
    source: Path,
    root: Path,
) -> tuple[str, Path] | None:
    raw = _link_destination(raw_target)
    if not raw or raw.startswith("#") or raw.startswith("//"):
        return None
    try:
        parsed = urlparse(raw)
    except ValueError:
        return None
    if parsed.scheme:
        return None
    path_text = raw.split("#", 1)[0].split("?", 1)[0]
    if not path_text:
        return None
    unresolved = (
        root / path_text.lstrip("/")
        if path_text.startswith("/")
        else source.parent / path_text
    )
    try:
        return raw, unresolved.resolve()
    except (OSError, RuntimeError, ValueError):
        return None


def _check_local_links(root: Path, sources: Iterable[Path], warnings: list[str]) -> None:
    reported: set[tuple[str, str]] = set()
    for source in sources:
        try:
            relative = source.relative_to(root).as_posix()
        except ValueError:
            relative = str(source)
        for raw, target in _extract_link_targets(source, root):
            if target is None:
                key = (relative, raw)
                if key not in reported:
                    reported.add(key)
                    warnings.append(
                        f"invalid Markdown link target in {relative}: {raw}"
                    )
                continue
            if target.exists():
                continue
            target_without_line = re.sub(r":\d+$", "", str(target))
            if Path(target_without_line).exists():
                continue
            key = (relative, raw)
            if key in reported:
                continue
            reported.add(key)
            warnings.append(f"broken local Markdown link in {relative}: {raw}")


def _configured_frontmatters(
    root: Path,
    sources: Iterable[Path],
) -> Iterable[tuple[Path, str, dict[str, str]]]:
    for source in sources:
        try:
            text = source.read_text(encoding="utf-8")
        except OSError:
            continue
        frontmatter = _frontmatter(text)
        if frontmatter is None:
            continue
        yield source, text, frontmatter


def _check_line_budgets(
    root: Path,
    configured: Iterable[tuple[Path, str, dict[str, str]]],
    warnings: list[str],
) -> None:
    for source, text, frontmatter in configured:
        value = frontmatter.get("line_budget")
        if value is None:
            continue
        try:
            budget = int(value)
        except ValueError:
            continue
        if budget < 1:
            continue
        line_count = len(text.splitlines())
        relative = source.relative_to(root).as_posix()
        if line_count > budget:
            warnings.append(
                f"active document exceeds line_budget in {relative}: "
                f"{line_count}/{budget} lines; distill before deleting detail"
            )
        elif line_count * 10 >= budget * 9:
            warnings.append(
                f"active document is near line_budget in {relative}: "
                f"{line_count}/{budget} lines"
            )


def _explicit_date(text: str) -> date | None:
    head = "\n".join(text.splitlines()[:80])
    match = DATE_RE.search(head)
    if not match:
        return None
    try:
        return date.fromisoformat(match.group(1))
    except ValueError:
        return None


def _git_file_date(root: Path, relative: str) -> date | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "log", "-1", "--format=%cs", "--", relative],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    value = result.stdout.strip()
    if result.returncode != 0 or not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _check_freshness(
    root: Path,
    configured: Iterable[tuple[Path, str, dict[str, str]]],
    warnings: list[str],
) -> None:
    today = date.today()
    for source, text, frontmatter in configured:
        value = frontmatter.get("stale_after_days")
        if value is None:
            continue
        try:
            threshold = int(value)
        except ValueError:
            continue
        if threshold < 0:
            continue

        relative = source.relative_to(root).as_posix()
        observed = _explicit_date(text)
        if observed is None:
            warnings.append(
                f"cannot determine freshness for {relative}: "
                "add an explicit ISO date near Last updated/verified or 更新时间"
            )
            continue

        age = (today - observed).days
        if age < 0:
            warnings.append(
                f"document date is in the future in {relative}: {observed.isoformat()}"
            )
        elif age > threshold:
            warnings.append(
                f"document is stale in {relative}: {age} days old, "
                f"stale_after_days is {threshold}; verify before trusting it"
            )

        committed = _git_file_date(root, relative)
        if committed is not None and observed < committed:
            warnings.append(
                f"explicit update date lags Git in {relative}: "
                f"{observed.isoformat()} < {committed.isoformat()}"
            )


def _body_lines(text: str) -> tuple[list[str], int]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return lines, 1
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return lines[index + 1 :], index + 2
    return lines, 1


def _normalize_paragraph(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"[`*_~]", "", value)
    return re.sub(r"\s+", " ", value).strip().casefold()


def _paragraphs(source: Path) -> list[tuple[str, int]]:
    try:
        text = source.read_text(encoding="utf-8")
    except OSError:
        return []
    lines, first_line = _body_lines(text)
    paragraphs: list[tuple[str, int]] = []
    buffer: list[str] = []
    start = first_line
    fenced = False

    def flush() -> None:
        nonlocal buffer
        if not buffer:
            return
        normalized = _normalize_paragraph(" ".join(part.strip() for part in buffer))
        if len(normalized) >= DUPLICATE_MIN_CHARS:
            paragraphs.append((normalized, start))
        buffer = []

    for offset, line in enumerate(lines):
        line_number = first_line + offset
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            flush()
            fenced = not fenced
            continue
        if fenced:
            continue
        skip = (
            not stripped
            or (bool(line) and line[0].isspace())
            or stripped.startswith("#")
            or stripped.startswith(">")
            or stripped.startswith("|")
            or re.match(r"^[-*+]\s+", stripped) is not None
            or re.match(r"^\d+[.)]\s+", stripped) is not None
            or re.match(r"^[-*_]{3,}$", stripped) is not None
        )
        if skip:
            flush()
            continue
        if not buffer:
            start = line_number
        buffer.append(stripped)
    flush()
    return paragraphs


def _check_duplicate_prose(
    root: Path,
    sources: Iterable[Path],
    warnings: list[str],
) -> None:
    paragraphs: list[tuple[str, int, str]] = []
    for source in sources:
        try:
            relative = source.relative_to(root)
        except ValueError:
            continue
        if relative.parts and relative.parts[0] in {"archive", "SHORT_MEMORY"}:
            continue
        for normalized, line_number in _paragraphs(source):
            paragraphs.append((relative.as_posix(), line_number, normalized))
            if len(paragraphs) >= DUPLICATE_MAX_PARAGRAPHS:
                break
        if len(paragraphs) >= DUPLICATE_MAX_PARAGRAPHS:
            break

    findings = 0
    for index, (path_a, line_a, text_a) in enumerate(paragraphs):
        for path_b, line_b, text_b in paragraphs[index + 1 :]:
            if path_a == path_b:
                continue
            length_ratio = min(len(text_a), len(text_b)) / max(
                len(text_a), len(text_b)
            )
            if length_ratio < 0.90:
                continue
            if text_a == text_b:
                similarity = 1.0
            else:
                matcher = difflib.SequenceMatcher(
                    None, text_a, text_b, autojunk=True
                )
                if matcher.quick_ratio() < DUPLICATE_SIMILARITY:
                    continue
                similarity = matcher.ratio()
            if similarity < DUPLICATE_SIMILARITY:
                continue
            warnings.append(
                f"long active prose is {similarity:.0%} similar across "
                f"{path_a}:{line_a} and {path_b}:{line_b}; keep detail in one owner"
            )
            findings += 1
            if findings >= DUPLICATE_MAX_FINDINGS:
                return


def _check_long_prose_lines(
    root: Path,
    sources: Iterable[Path],
    warnings: list[str],
) -> None:
    """Warn about unusually dense prose without flagging Markdown structures."""
    findings = 0
    for source in sources:
        try:
            text = source.read_text(encoding="utf-8")
            relative = source.relative_to(root).as_posix()
        except (OSError, ValueError):
            continue

        lines, first_line = _body_lines(text)
        fence_char: str | None = None
        fence_length = 0
        for offset, line in enumerate(lines):
            stripped = line.strip()
            if fence_char is not None:
                run_length = 0
                while (
                    run_length < len(stripped)
                    and stripped[run_length] == fence_char
                ):
                    run_length += 1
                if (
                    run_length >= fence_length
                    and not stripped[run_length:].strip()
                ):
                    fence_char = None
                    fence_length = 0
                continue

            fence = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
            if fence is not None:
                delimiter = fence.group(1)
                fence_char = delimiter[0]
                fence_length = len(delimiter)
                continue

            if len(stripped) <= LONG_PROSE_MAX_CHARS:
                continue
            next_line = lines[offset + 1].strip() if offset + 1 < len(lines) else ""
            structural = (
                not stripped
                or line.startswith("    ")
                or line.startswith("\t")
                or re.match(r"^\s{0,3}#{1,6}(?:\s|$)", line) is not None
                or re.match(r"^\s{0,3}(?:=+|-+)\s*$", next_line) is not None
                or "|" in stripped
                or stripped.startswith(">")
                or re.match(r"^[-*+]\s+", stripped) is not None
                or re.match(r"^\d+[.)]\s+", stripped) is not None
            )
            if structural:
                continue

            warnings.append(
                f"active prose line is unusually long in "
                f"{relative}:{first_line + offset}: {len(stripped)} characters; "
                f"keep ordinary prose lines at or below {LONG_PROSE_MAX_CHARS} "
                "characters when practical"
            )
            findings += 1
            if findings >= LONG_PROSE_MAX_FINDINGS:
                return


def _archive_manifest_values(text: str) -> dict[str, list[str]]:
    """Return inline values for every recognized archive manifest field."""
    values: dict[str, list[str]] = {}
    for original, visible in _visible_markdown_lines(text):
        if original.startswith("    ") or original.startswith("\t"):
            continue
        for label, patterns in ARCHIVE_MANIFEST_FIELDS.items():
            for pattern in patterns:
                match = re.search(pattern, visible)
                if match is not None:
                    values.setdefault(label, []).append(
                        original[match.end() :].strip()
                    )
    return values


def _has_valid_live_markdown_link(
    values: Iterable[str],
    source: Path,
    root: Path,
) -> bool:
    resolved_root = root.resolve()
    for value in values:
        for raw_target in _markdown_link_destinations(value):
            target = _resolve_local_link(raw_target, source, root)
            if target is None:
                continue
            _, resolved = target
            try:
                relative = resolved.relative_to(resolved_root)
            except ValueError:
                continue
            if (
                relative.parts
                and relative.parts[0] != "archive"
                and resolved.is_file()
                and resolved.suffix.casefold() == ".md"
            ):
                return True
    return False


def _check_archive_bundles(root: Path, warnings: list[str]) -> list[Path]:
    archive = root / "archive"
    if not archive.is_dir():
        return []
    manifests: list[Path] = []
    for topic in sorted(child for child in archive.iterdir() if child.is_dir()):
        if not any(child.is_file() for child in topic.rglob("*")):
            continue
        readme = topic / "README.md"
        manifest = topic / "MANIFEST.md"
        relative_topic = topic.relative_to(root).as_posix()
        candidates = [path for path in (readme, manifest) if path.is_file()]
        if not candidates:
            warnings.append(
                f"archive topic bundle has no README.md or MANIFEST.md: "
                f"{relative_topic}"
            )
            continue

        best: tuple[Path, dict[str, list[str]], tuple[int, int, int]] | None = None
        read_errors: list[tuple[Path, OSError]] = []
        for candidate in candidates:
            try:
                text = candidate.read_text(encoding="utf-8")
            except OSError as exc:
                read_errors.append((candidate, exc))
                continue
            values = _archive_manifest_values(text)
            nonempty_count = sum(
                any(value.strip() for value in field_values)
                for field_values in values.values()
            )
            score = (
                nonempty_count,
                int(
                    _has_valid_live_markdown_link(
                        values.get("Distilled into", []),
                        candidate,
                        root,
                    )
                ),
                int(candidate.name == "MANIFEST.md"),
            )
            if best is None or score > best[2]:
                best = (candidate, values, score)

        if best is None:
            candidate, exc = read_errors[0]
            warnings.append(
                f"cannot read archive manifest "
                f"{candidate.relative_to(root).as_posix()}: {exc}"
            )
            continue

        manifest_path, values, _ = best
        manifests.append(manifest_path)
        missing = [
            label for label in ARCHIVE_MANIFEST_FIELDS if label not in values
        ]
        empty = [
            label
            for label, field_values in values.items()
            if not any(value.strip() for value in field_values)
        ]
        if missing:
            warnings.append(
                f"archive manifest is missing fields in "
                f"{manifest_path.relative_to(root).as_posix()}: "
                + ", ".join(missing)
            )
        if empty:
            warnings.append(
                f"archive manifest has empty fields in "
                f"{manifest_path.relative_to(root).as_posix()}: "
                + ", ".join(empty)
            )

        distilled = values.get("Distilled into", [])
        if any(value.strip() for value in distilled) and not (
            _has_valid_live_markdown_link(distilled, manifest_path, root)
        ):
            warnings.append(
                f"archive manifest has invalid Distilled into in "
                f"{manifest_path.relative_to(root).as_posix()}: "
                "expected at least one existing live Markdown owner link"
            )
    return manifests


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
        _validate_file_contract(
            root,
            relative,
            expected,
            required=True,
            template=template,
            allow_template_tokens=allow_template_tokens,
            errors=errors,
            warnings=warnings,
        )
    for relative, expected in OPTIONAL_FILES.items():
        _validate_file_contract(
            root,
            relative,
            expected,
            required=False,
            template=template,
            allow_template_tokens=allow_template_tokens,
            errors=errors,
            warnings=warnings,
        )

    dirs_file = root / "DIRS.md"
    if dirs_file.is_file() and not template:
        try:
            dirs_text = dirs_file.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"cannot read DIRS.md: {exc}")
            dirs_text = ""
        actual_directories = {
            child.name
            for child in root.iterdir()
            if child.is_dir() and not child.name.startswith(".")
        }
        registered_directories = _registered_directories(dirs_text)
        for dirname in sorted(actual_directories - PRESET_DIRECTORIES):
            if dirname not in registered_directories:
                errors.append(f"unregistered custom directory in DIRS.md: {dirname}/")

    if template:
        return errors, warnings

    legacy_files = ["MEMORY_MANIFEST.yml", "RUNBOOK.md", "README.md"]
    present_legacy = [name for name in legacy_files if (root / name).exists()]
    if present_legacy:
        warnings.append(
            "legacy files are not part of the current standard: "
            + ", ".join(present_legacy)
        )

    active_sources = _active_markdown_files(root)
    configured = list(_configured_frontmatters(root, active_sources))
    manifests = _check_archive_bundles(root, warnings)
    _check_local_links(root, [*active_sources, *manifests], warnings)
    _check_line_budgets(root, configured, warnings)
    _check_freshness(root, configured, warnings)
    _check_duplicate_prose(root, active_sources, warnings)
    _check_long_prose_lines(root, active_sources, warnings)

    return errors, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a memory-docs project instance or template root."
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Project root, memory-docs directory, or template root",
    )
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
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero for warnings as well as errors",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = _memory_root(args.path, args.template)
    errors, warnings = validate_memory_docs(
        args.path,
        template=args.template,
        allow_template_tokens=args.allow_template_tokens,
    )

    if args.json:
        print(
            json.dumps(
                {
                    "path": str(args.path.expanduser().resolve()),
                    "memory_root": str(root),
                    "template": args.template,
                    "counts": {
                        "errors": len(errors),
                        "warnings": len(warnings),
                    },
                    "errors": errors,
                    "warnings": warnings,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        if errors:
            print(
                f"Validation failed with {len(errors)} error(s).",
                file=sys.stderr,
            )
        elif warnings:
            print(
                f"memory-docs validation passed with {len(warnings)} warning(s)."
            )
        else:
            print("memory-docs validation passed.")

    if errors:
        return 1
    if args.strict and warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
