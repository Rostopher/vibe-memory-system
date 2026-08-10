---
name: update-living-docs
description: Maintain an initialized memory-docs system after meaningful implementation, research, operational, documentation, decision, milestone, or handoff work. Use when verified durable facts or continuation context should be distilled into canonical owners, or when a user asks to audit, compress, archive, or repair project memory. Do not use for first-time initialization, trivial edits, or unresolved discussion with no durable outcome.
---

# Update Living Docs

Keep project memory aligned with verified reality while minimizing active-document duplication and preserving useful historical detail.

## Establish the Memory Contract

1. Confirm `memory-docs/INDEX.md` exists. Use `init-memory` instead when the installed templates still need first-time initialization.
2. Read repository instructions, `memory-docs/INDEX.md`, and only the memory files relevant to the work. Do not preload all historical memory.
3. Read each target file's frontmatter:
   - `role`: what the file owns;
   - `not_for`: what belongs elsewhere;
   - `update_mode`: how the file may change;
   - optional `line_budget` and `stale_after_days`: advisory health thresholds.
4. Treat code, tests, generated results, executed commands, artifacts, and explicit user decisions as evidence. Never update memory from conversation recall alone.
5. Run the project-local validator as a preflight when it is installed:

   ```bash
   python3 .memory-docs-tools/validate_memory_docs.py .
   ```

Treat pre-existing findings as context, not permission for unrelated rewrites. Read `references/health-and-maintenance.md` completely before resolving health findings, performing a substantial archive or compression pass, or applying the historical retrieval gate below.

## Apply Historical Retrieval Only When Triggered

Before asserting that work was never done, avoiding a duplicate implementation, reopening an old route, reversing a stable decision, diagnosing a regression, or explaining why the project is in its current state, apply the bounded historical retrieval gate in `references/health-and-maintenance.md`.

For ordinary updates, do not load history by default. For triggered questions, search with 2–4 topic terms and aliases, read only useful hits, reconstruct the lifecycle beyond the first hit, prefer the current owner, and verify material conclusions against code or artifacts.

During an explicit protocol migration or a substantial maintenance pass, merge
a concise version of this gate into repository instructions and
`memory-docs/INDEX.md` when they lack it. Preserve project-specific rules; do
not replace either file with the template.

## Route Information to One Owner

Give every durable fact one canonical detailed owner. Other active documents may state the local consequence, but should link to the owner rather than repeat its explanation.

| Information | Primary target |
|---|---|
| Stable project identity, scope, top-level workflow | `memory-docs/OVERVIEW.md` |
| Project-wide current focus, recent 3–5 milestones, blockers, confirmed backlog | `memory-docs/STATUS.md` |
| Stage transitions and causal project evolution | `memory-docs/HISTORY.md` |
| Hard rules and stable contracts | `memory-docs/CONVENTIONS.md` |
| Domain terms, variables, display names | `memory-docs/GLOSSARY.md` |
| Detailed-memory directory registration | `memory-docs/DIRS.md` |
| Concept or artifact to 1–2 authoritative entry files | `memory-docs/detail_mem/MAP.md` |
| Module and capability implementation state | `memory-docs/detail_mem/PROGRESS.md` |
| Stable choices, current decision lifecycle, rationale, and impact | `memory-docs/detail_mem/DECISIONS.md` registry plus detail |
| Experimental protocol, artifacts, results, interpretation, uncertainty, claim limits | optional `memory-docs/research/EXPERIMENT_LEDGER.md` |
| Useful but not yet stable continuation context | `memory-docs/SHORT_MEMORY/` |
| Completed retrospectives, old snapshots, rejected or superseded detail | `memory-docs/archive/` |

Keep the ownership boundaries explicit:

- `STATUS.md` owns the concise project-level snapshot; `PROGRESS.md` owns module-level implementation detail.
- `SHORT_MEMORY/` owns only the delta required to resume active work, not stable project truth.
- `EXPERIMENT_LEDGER.md`, when present, owns durable research evidence and claim boundaries. It does not own current TODOs, the next experiment, live server state, raw logs, or session-resume instructions.
- The research ledger is optional. Do not create it merely because a repository contains research code, and do not treat its absence as a defect.

If a detailed topic needs more than a short entry, create a semantic subdirectory under `memory-docs/` and register it in `DIRS.md` in the same change.

## Obey Update Modes

### `rewrite`

Replace the current snapshot while preserving frontmatter. Standard files: `INDEX.md`, `OVERVIEW.md`, `STATUS.md`.

Move historically valuable removed content to `HISTORY.md` or `archive/`; do not retain stale text merely to avoid rewriting.

### `patch`

Modify structured entries in place. Standard files: `CONVENTIONS.md`, `GLOSSARY.md`, `DIRS.md`, `detail_mem/MAP.md`, `detail_mem/PROGRESS.md`.

Add, correct, or remove only the affected entries. `PROGRESS.md` is a checklist, not a dated changelog. `MAP.md` is navigation, not a full inventory.

### `append`

Add new records without silently rewriting history. Standard files: `HISTORY.md`, `detail_mem/DECISIONS.md`, `SHORT_MEMORY/`, `archive/`.

`DECISIONS.md` uses a compatible mixed contract: keep `update_mode: append`; patch its compact registry when status, current conclusion, keywords, or pointers change; append detailed records; and never reuse an ID. If a decision is superseded, append a new decision or dated closure note that references the old ID. When near budget, archive closed or superseded rationale only after retaining its registry row and a valid detail pointer. Namespace imported legacy IDs when collisions are possible.

For optional or project-specific documents, obey their own frontmatter.

## Workflow

1. Collect verified facts from the actual diff, tests, commands, artifacts, repository state, and explicit decisions.
2. Classify each fact as framework truth, detailed active state, session context, historical detail, or non-durable information.
3. Select one canonical owner for each durable fact and the smallest sufficient set of target files.
4. Put the current answer or decision first. Keep evidence, commands, and narrative in the detailed owner; use a short consequence and link elsewhere.
5. Apply each target's update mode and preserve its frontmatter.
6. Before shortening or replacing useful detail:
   - distill stable conclusions into their live owners;
   - preserve completed, superseded, rejected, or compressed source detail in `archive/`;
   - add a manifest for a multi-file archive bundle and keep relevant live-to-archive links;
   - only then remove the duplicated or stale live detail.
7. Close plan lifecycles explicitly. Treat plans as proposals, not current truth. When a plan completes, stops, or is replaced, add a closure or superseded pointer to the current owner, decision, evidence, or archive manifest.
8. Cross-check related layers without spraying the same update everywhere:
   - implementation entry changed → consider `MAP.md`;
   - module status changed → consider `PROGRESS.md` and a concise `STATUS.md` consequence;
   - stable choice emerged → append `DECISIONS.md`;
   - a stage settled → append `HISTORY.md` and trim stale `STATUS.md` milestones;
   - custom memory directory added → patch `DIRS.md`;
   - unresolved work needs continuation context → update the relevant handoff.
9. Run the validator again after editing. Resolve errors introduced by the change and high-signal warnings related to the current work. Preserve and report unrelated pre-existing warnings unless the user expands the scope.

Do not update files merely to make every layer change. If no durable or handoff-worthy information emerged, make no memory diff and report that no update was needed.

## Hard Rules

- Never invent completed work, tests, priorities, decisions, evidence, or historical rationale.
- Keep framework memory compact and prevent linear growth.
- Do not put raw discussion into stable memory.
- Do not treat a proposal, pilot, or stale plan as the current confirmed state.
- Do not put dated narratives in `PROGRESS.md` or full file lists in `MAP.md`.
- Do not archive unresolved blockers, current operating procedures, or active evidence merely to satisfy a budget.
- Do not delete useful content solely to make the validator green.
- Do not create legacy `docs/`, `MEMORY_MANIFEST.yml`, `RUNBOOK.md`, or `memory-docs/README.md` unless the project independently uses them for another purpose.
- Preserve user changes and project-specific custom memory directories.

## Completion Report

Report:

- files updated, the update mode used, and why each was the canonical owner;
- detail archived and where its stable conclusions now live;
- relevant files intentionally left untouched;
- preflight and postflight validation results;
- remaining warnings, distinguishing pre-existing findings from items requiring user judgment.
