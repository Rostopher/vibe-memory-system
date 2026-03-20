---
name: update-living-docs
description: Update the project's docs memory system after meaningful work. Use when code, decisions, conventions, mappings, session context, or historical records should be reflected in docs/ without asking the user to manually maintain them.
---

# Update Living Docs

Use this skill to keep the project's docs memory system aligned with reality.

The goal is not “update some docs.”

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
  - `docs/REPO_STATUS.md`
  - `docs/MAP.md` or project-specific `*_MAP.md`
- **Session Memory**
  - `docs/SHORT_MEMORY/`
- **Historical Memory**
  - `docs/archive/`

Not every repository will use every layer. Detect what exists and work with the actual structure.

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

- `docs/STATUS.md`
  - current focus changed
  - something moved from in-progress to done
  - backlog priorities shifted
- `docs/DECISIONS.md`
  - a design, method, naming, or workflow decision became stable
- `docs/CONVENTIONS.md`
  - a new hard rule, contract, naming rule, or output rule was established
- `docs/GLOSSARY.md`
  - a recurring term, variable, method label, or display name was standardized
- `docs/RUNBOOK.md`
  - the way to run, debug, export, or sync outputs changed
- `docs/OVERVIEW.md`
  - the project's high-level structure or main workstreams changed
- `docs/README.md`
  - the docs entry path or memory-system explanation changed

### 2. Update Scaling Memory when the detail is too fine for the base layer

Typical targets:

- `docs/REPO_STATUS.md`
  - detailed implementation tracking
  - module-level or workflow-level progress
  - legacy vs mainline differences
- `docs/MAP.md` or `docs/PAPER_MAP.md`
  - feature -> file mapping
  - artifact -> runner -> upstream inputs mapping
  - paper figure/table -> canonical outputs mapping

### 3. Update Session Memory when context is useful but not yet stable

Typical target:

- `docs/SHORT_MEMORY/<date_or_session>_<topic>.md`

Use this when:

- the session is long and compact risk is high
- current understanding is useful but not yet stable enough for `STATUS`, `DECISIONS`, or `CONVENTIONS`
- the next Agent session should inherit this context

### 4. Update Historical Memory when the work should be preserved, not kept live

Typical target:

- `docs/archive/<date>_<topic>.md`

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
3. Classify each fact into one of four buckets:
   - stable project truth
   - detailed but active implementation context
   - session-only context
   - historical record
4. Update only the docs that match those buckets.
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

- Prefer append/update over large rewrites.
- Preserve each file's role; do not collapse multiple roles into one doc.
- Keep Base Memory concise.
- Let `REPO_STATUS` and `MAP` hold detail when needed.
- `DECISIONS.md` should record decisions, not raw discussion transcripts.
- `SHORT_MEMORY` should not become a second archive.
- `archive/` should not become a second `STATUS.md`.

## Examples

### Example: a new plotting rule stabilizes

Update:

- `docs/CONVENTIONS.md`

Maybe also:

- `docs/DECISIONS.md` if the rule came from a deliberate design choice

### Example: a paper figure now uses a new canonical output chain

Update:

- `docs/PAPER_MAP.md` or `docs/MAP.md`
- `docs/STATUS.md` if this changes current paper status materially

### Example: a long debugging session found a likely cause, but the fix is not final

Update:

- `docs/SHORT_MEMORY/...`

Do not prematurely write it as a stable decision.

### Example: an exploration ended and the rejected direction is worth remembering

Update:

- `docs/archive/...`
- `docs/DECISIONS.md` if there is now a stable “do not use this path” conclusion

## Output

When reporting back, summarize:

- which docs were updated
- why those docs were the right layer
- whether any docs were intentionally not updated
- whether no update was needed

## Hard Constraints

- Do not invent completed work, test results, or decisions.
- Do not let Base Memory bloat with session notes.
- Do not forget `MAP` when implementation-chain knowledge changed.
- Do not forget `SHORT_MEMORY` when session context would otherwise be lost.
- Do not rely on the user to remember to update docs manually.
