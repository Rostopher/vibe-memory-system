---
name: update-living-docs
description: Keep a project's memory-docs system aligned with implemented reality after meaningful code, research, documentation, decision, mapping, milestone, handoff, or retrospective changes. Use when stable facts or active context should be preserved without asking the user to maintain project memory manually.
---

# Update Living Docs

Maintain project memory as part of completing meaningful work. Update only the layers affected by verified changes.

## Establish the Memory Contract

1. Confirm `memory-docs/INDEX.md` exists.
2. Read `AGENTS.md`, `memory-docs/INDEX.md`, and the target files before editing.
3. Read each target file's frontmatter:
   - `role`: what belongs there;
   - `not_for`: what must go elsewhere;
   - `update_mode`: how it may change.
4. Treat code, tests, generated results, executed commands, and explicit user decisions as evidence. When memory conflicts with implementation, trust implementation and repair or flag the memory.

## Route Information

| Information | Primary target |
|---|---|
| Stable project identity, scope, top-level workflow | `memory-docs/OVERVIEW.md` |
| Current focus, recent 3–5 milestones, blockers, confirmed backlog | `memory-docs/STATUS.md` |
| Stage transitions and causal project evolution | `memory-docs/HISTORY.md` |
| Hard rules and stable contracts | `memory-docs/CONVENTIONS.md` |
| Domain terms, variables, display names | `memory-docs/GLOSSARY.md` |
| Detailed-memory directory registration | `memory-docs/DIRS.md` |
| Concept or artifact to 1–2 authoritative entry files | `memory-docs/detail_mem/MAP.md` |
| Module and capability implementation checklist | `memory-docs/detail_mem/PROGRESS.md` |
| Stable choices with context, alternatives, reasons, and impact | `memory-docs/detail_mem/DECISIONS.md` |
| Useful but not yet stable handoff context | `memory-docs/SHORT_MEMORY/` |
| Completed retrospectives, old snapshots, failed explorations | `memory-docs/archive/` |

If a detailed topic needs more than a short entry, create a semantic subdirectory under `memory-docs/` and register it in `DIRS.md` in the same change.

## Obey Update Modes

### `rewrite`

Replace the current snapshot while preserving frontmatter. Standard files: `INDEX.md`, `OVERVIEW.md`, `STATUS.md`.

Move historically valuable removed content to `HISTORY.md` or `archive/`; do not retain stale text merely to avoid rewriting.

### `patch`

Modify structured entries in place. Standard files: `CONVENTIONS.md`, `GLOSSARY.md`, `DIRS.md`, `detail_mem/MAP.md`, `detail_mem/PROGRESS.md`.

Add, correct, or remove only the affected entries. `PROGRESS.md` is a checklist, not a dated changelog. `MAP.md` is navigation, not a full inventory.

### `append`

Add new records without rewriting historical entries. Standard files: `HISTORY.md`, `detail_mem/DECISIONS.md`, `SHORT_MEMORY/`, `archive/`.

If a decision is superseded, append a new decision that references the old ID. Do not silently rewrite history.

## Workflow

1. Collect verified facts from the conversation, actual diffs, tests, commands, and artifacts.
2. Classify each fact as stable framework truth, detailed active state, session context, or historical record.
3. Select the smallest set of target files.
4. Apply each target's update mode and preserve its frontmatter.
5. Cross-check related layers:
   - implementation entry changed → consider `MAP.md`;
   - module status changed → consider `PROGRESS.md` and concise `STATUS.md`;
   - stable choice emerged → append `DECISIONS.md`;
   - a stage settled → append `HISTORY.md` and trim stale `STATUS.md` milestones;
   - custom memory directory added → patch `DIRS.md`;
   - long session has unresolved context → add `SHORT_MEMORY/`.
6. Validate paths, claims, and memory structure.

Do not update files merely to make every layer change. If no durable or handoff-worthy information emerged, say that no memory update was needed.

## Hard Rules

- Never invent completed work, tests, priorities, decisions, or historical rationale.
- Keep framework memory compact and prevent linear growth.
- Do not put raw discussion into stable memory.
- Do not put dated narratives in `PROGRESS.md` or full file lists in `MAP.md`.
- Do not create legacy `docs/`, `MEMORY_MANIFEST.yml`, `RUNBOOK.md`, or `memory-docs/README.md` unless the project independently uses them for a different purpose.
- Preserve user changes and project-specific custom memory directories.

## Validate and Report

Prefer the project-local validator when installed:

```bash
python .memory-docs-tools/validate_memory_docs.py .
```

Otherwise run `scripts/validate_memory_docs.py` from the vibe-memory-system source against the project root.

Report the files changed, update mode used for each, why each layer was appropriate, validation results, and memory files intentionally left untouched.
