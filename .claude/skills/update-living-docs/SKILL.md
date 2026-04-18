---
name: update-living-docs
description: Update the project's docs memory system after meaningful work. Use when code, decisions, conventions, mappings, session context, or historical records should be reflected in docs/ without asking the user to manually maintain them.
---

# Update Living Docs

Use this skill to keep the project's docs memory system aligned with reality.

The goal is not "update some docs."

The goal is:

- the user should not need to manually maintain project memory
- the Agent should proactively preserve stable facts, rules, mappings, and important context
- docs should stay consistent with implemented reality

## Core Rule

The Agent is responsible for maintaining docs when meaningful work has changed the project state.

Do not wait for perfect completeness.
Do not wait for the user to remember every doc that should change.
But also do not spray updates everywhere.

First decide which layer of the memory system should absorb the new information, then update only that layer.

## Understand The Memory System First

Before editing docs, identify the repository's memory layers:

- **Base Memory**
  - `docs/README.md`
  - `docs/OVERVIEW.md`
  - `docs/STATUS.md`
  - `docs/DECISIONS.md`
  - `docs/GLOSSARY.md`
  - `docs/RUNBOOK.md`
  - `docs/CONVENTIONS.md`
- **Scaling Memory**
  - `docs/PROGRESS.md`
  - `docs/MAP.md` or project-specific `*_MAP.md`
- **Session Memory**
  - `docs/SHORT_MEMORY/`
- **Historical Memory**
  - `docs/archive/`

Not every repository will use every layer. Detect what exists and work with the actual structure.

## Read Frontmatter Before Editing

Each docs file contains a YAML frontmatter with an `update_mode` field. **Always read this field before making changes.** It determines how the file should be modified:

### `update_mode: rewrite`

The file represents a **current snapshot** that can be completely replaced.

Files: `OVERVIEW.md`, `STATUS.md`, `RUNBOOK.md`

How to update:
- You may replace the entire content with a fresh version.
- Do not worry about preserving old text — the file is meant to reflect the current state.
- Historical content that is being removed should move to `archive/` if valuable.

### `update_mode: append`

The file is an **accumulating log** where old entries must never be modified.

Files: `DECISIONS.md`, `SHORT_MEMORY/`, `archive/`

How to update:
- Add new entries at the end (or in the appropriate section).
- Never rewrite, reorder, or delete existing entries.
- If an old entry is superseded, add a new entry that references the old one (e.g., `supersedes DEC-xxx`).

### `update_mode: patch`

The file contains **structured entries** that are individually updated in place.

Files: `CONVENTIONS.md`, `GLOSSARY.md`, `MAP.md`, `PROGRESS.md`, `README.md`

How to update:
- Add new entries in the appropriate section.
- Modify existing entries in place when their content changes.
- Remove entries only when they are clearly obsolete.
- Do not rewrite the entire file unless the structure itself needs reorganization.

## When To Use

Use this skill when:

- meaningful implementation work finished
- a milestone or current focus changed
- a new decision became stable
- a convention or contract changed
- a mapping between concept and implementation changed
- a long session produced context that should not be lost
- an exploration, pitfall, or failed direction should be preserved historically

## Update Strategy

Always classify the new information before editing.

### 1. Update Base Memory when the project's stable truth changed

Typical targets:

- `docs/STATUS.md` (**rewrite**)
  - current focus changed
  - something moved from in-progress to done
  - backlog priorities shifted
- `docs/DECISIONS.md` (**append**)
  - a design, method, naming, or workflow decision became stable
- `docs/CONVENTIONS.md` (**patch**)
  - a new hard rule, contract, naming rule, or output rule was established
- `docs/GLOSSARY.md` (**patch**)
  - a recurring term, variable, method label, or display name was standardized
- `docs/RUNBOOK.md` (**rewrite**)
  - the way to run, debug, export, or sync outputs changed
- `docs/OVERVIEW.md` (**rewrite**)
  - the project's high-level structure or main workstreams changed
- `docs/README.md` (**patch**)
  - the docs entry path or memory-system explanation changed

### 2. Update Scaling Memory when the detail is too fine for the base layer

Typical targets:

- `docs/PROGRESS.md` (**patch**)
  - module-level or workflow-level progress
  - feature completed or started
  - do NOT add dated changelog entries here — those belong in `archive/`
- `docs/MAP.md` or `docs/PAPER_MAP.md` (**patch**)
  - feature -> file mapping
  - artifact -> runner -> upstream inputs mapping
  - paper figure/table -> canonical outputs mapping

### 3. Update Session Memory when context is useful but not yet stable

Typical target:

- `docs/SHORT_MEMORY/<date_or_session>_<topic>.md` (**append**)

Use this when:

- the session is long and compact risk is high
- current understanding is useful but not yet stable enough for `STATUS`, `DECISIONS`, or `CONVENTIONS`
- the next Agent session should inherit this context

### 4. Update Historical Memory when the work should be preserved, not kept live

Typical target:

- `docs/archive/<date>_<topic>.md` (**append**)

Use this when:

- a troubleshooting cycle completed
- an exploration ended
- a failed direction or retrospective should be preserved
- the content is valuable historically, but not part of the active project surface

## Workflow

1. Collect facts from:
   - the current conversation
   - actual code changes
   - executed commands / validations
   - produced artifacts
2. Read the relevant docs before editing.
   - Never update a doc blindly from memory.
   - **Read the YAML frontmatter to check `update_mode` before writing.**
3. Classify each fact into one of four buckets:
   - stable project truth
   - detailed but active implementation context
   - session-only context
   - historical record
4. For each target file, apply the correct update mode:
   - `rewrite`: replace content with current-state snapshot
   - `append`: add new entry without touching old ones
   - `patch`: modify specific entries in place
5. Keep claims aligned with implemented reality.
   - no future work written as done
   - no invented validation
   - no fabricated decisions
6. If nothing should change, explicitly say so.

## Decision Rules

Use these rules when deciding where something belongs:

- If the fact is stable and should be repeatedly consulted, prefer Base Memory.
- If the fact is active but too detailed for the base layer, prefer Scaling Memory.
- If the fact is useful but not stable yet, prefer Session Memory.
- If the fact is complete and mainly useful for later retrospection, prefer Historical Memory.

## Writing Rules

- **Respect `update_mode`**: do not append to a `rewrite` file, do not rewrite an `append` file.
- Preserve each file's role; do not collapse multiple roles into one doc.
- Check the `not_for` field in frontmatter — it tells you what should go elsewhere.
- Keep Base Memory concise.
- Let `PROGRESS` and `MAP` hold detail when needed.
- `DECISIONS.md` should record decisions, not raw discussion transcripts.
- `SHORT_MEMORY` should not become a second archive.
- `archive/` should not become a second `STATUS.md`.
- `PROGRESS.md` is a checklist, not a changelog — dated narratives go to `archive/`.

## Examples

### Example: a new plotting rule stabilizes

Update:

- `docs/CONVENTIONS.md` (**patch**: add the new rule in the appropriate section)

Maybe also:

- `docs/DECISIONS.md` (**append**: add a new DEC entry if the rule came from a deliberate design choice)

### Example: a paper figure now uses a new canonical output chain

Update:

- `docs/PAPER_MAP.md` or `docs/MAP.md` (**patch**: update the mapping row)
- `docs/STATUS.md` (**rewrite**: refresh the current state if this changes the project status materially)

### Example: a long debugging session found a likely cause, but the fix is not final

Update:

- `docs/SHORT_MEMORY/...` (**append**: create a new session note)

Do not prematurely write it as a stable decision.

### Example: an exploration ended and the rejected direction is worth remembering

Update:

- `docs/archive/...` (**append**: create a dated record)
- `docs/DECISIONS.md` (**append**: add a DEC entry if there is now a stable "do not use this path" conclusion)

### Example: project finished a major milestone, many things changed

Update sequence:

1. `docs/STATUS.md` (**rewrite**: refresh the entire current-state snapshot)
2. `docs/PROGRESS.md` (**patch**: check off completed modules, add new in-progress items)
3. `docs/OVERVIEW.md` (**rewrite**: only if the project's scope or architecture actually changed)
4. `docs/DECISIONS.md` (**append**: only for decisions that became stable during this milestone)

## Output

When reporting back, summarize:

- which docs were updated
- what `update_mode` was applied to each
- why those docs were the right layer
- whether any docs were intentionally not updated
- whether no update was needed

## Hard Constraints

- Do not invent completed work, test results, or decisions.
- Do not let Base Memory bloat with session notes.
- Do not forget `MAP` when implementation-chain knowledge changed.
- Do not forget `SHORT_MEMORY` when session context would otherwise be lost.
- Do not rely on the user to remember to update docs manually.
- Do not add dated changelog entries to `PROGRESS.md` — use `archive/` instead.
- **Always read frontmatter before editing any doc file.**
