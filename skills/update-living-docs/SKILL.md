---
name: update-living-docs
description: Review memory needs at a completed work unit and, after user confirmation or an explicit maintenance request, update project memory as one coherent batch. Preserve detailed evidence and searchable history. Do not write memory after every small edit or use handoffs to bypass a user's deferral.
---

# Update Living Docs

Maintain verified project knowledge at work-unit boundaries. Keep default reading focused;
allow full-length explanations when they help future diagnosis, research or continuation.

## Establish the Update Scope First

- During implementation, collect evidence in the working context. Do not repeatedly update
  memory after each local fix, probe, attempt or commit.
- When the user's request or agreed work unit reaches its delivery point, ask whether the
  work is concluded and whether to update memory now. Discuss what should be retained,
  then write the confirmed batch. This point may be before commit, after commit or after
  deployment; neither commit nor deployment is a prerequisite.
- An explicit request to edit, initialize, migrate, maintain or produce a memory handoff
  already authorizes that scope. Complete it without asking again. Preserve prior choices
  to defer, skip or let the user write the record; do not bypass them through SHORT_MEMORY.
- If this work reveals stale memory before approval, report the discrepancy and propose
  a correction for closeout. Verify material facts instead of relying on stale wording.
- This gate concerns memory distillation, not documents or interface specifications already
  required by the user's task. Do that authorized work without adding a second approval.

## Read the Installed Contract

1. Resolve the memory directory and entry from repository instructions. Prefer the installed
   `memory-docs/INDEX.md`; respect an existing registered layout such as `docs/README.md`.
   Do not rename a project's memory to satisfy a template. Use `init-memory` for first setup.
2. Read the entry and relevant target files, including their `role`, `not_for`, `update_mode`
   and optional health metadata. Do not preload all history.
3. Ground claims in code, tests, executed commands, artifacts and explicit user decisions.
   Distinguish observation, interpretation, proposal, implementation and verification.
4. For an authorized update batch, run the installed validator before editing when available:

   ```bash
   python3 .memory-docs-tools/validate_memory_docs.py .
   ```

For a substantial archive / compression pass, health repair or triggered historical question,
read [health-and-maintenance.md](references/health-and-maintenance.md) completely.
Pre-existing warnings do not authorize unrelated rewrites.

## Historical Retrieval

Before asserting no prior work, reopening a route, reversing a stable choice, diagnosing
a regression or explaining history, search relevant topic terms and aliases across current
owners, full decision indexes, experiments, plans, archive routes and Git. Follow useful hits
through confirmation, closure or supersession; do not stop at a promising proposal or pilot.
The current view is intentionally incomplete as a historical catalog.

## Route Each Fact to One Detailed Owner

Paths below are relative to the project's actual memory root.

| Information | Primary owner |
|---|---|
| Project identity, structure and main workflow | `OVERVIEW.md` |
| Current project focus, recent meaningful milestones | `STATUS.md` |
| Module capabilities, blockers and local next steps | `detail_mem/PROGRESS.md` |
| Current rules and contracts | `CONVENTIONS.md` |
| Terms and definitions | `GLOSSARY.md` |
| Concept to 1–2 authoritative code entry points | `detail_mem/MAP.md` |
| Significant choice, applicability and rationale | `detail_mem/DECISIONS.md` current view + detail |
| Technical exploration outcomes and reopening conditions | Registered topic record |
| Research protocols, results and claim boundaries | Optional `research/EXPERIMENT_LEDGER.md` |
| Causal stage evolution | `HISTORY.md` or linked stage detail |
| Context required to continue unfinished work | `SHORT_MEMORY/` |
| Completed, rejected or superseded historical detail | `archive/` or a registered historical owner |
| Memory subdirectory routing | `DIRS.md` |

Do not turn each changed API, bug fix or probe into a MAP / STATUS / DECISIONS update.
Only update owners affected by the completed batch. Non-owners link to the explanation.
Test coverage maps belong with testing instructions; memory links to that maintained entry.

Successful and failed exploration records should retain the goal, conditions, observations,
interpretation, limits, failure / stopping cause, reopening conditions, repository and code
revision, data / configuration and artifact pointers. A feasible but unintegrated demo is a
valid outcome. Distinguish blocked or inconclusive from disproven. Mark uncommitted state
truthfully and preserve necessary differences; do not invent revisions or commit without scope.

Long troubleshooting narratives, failed approaches, handoffs and historical explanations are
welcome when useful. Control writing frequency and default retrieval, not evidence length.
SHORT_MEMORY owns continuation detail, not another copy of current status. The optional
research ledger owns evidence, not current TODOs or live infrastructure state.

## Update Modes and Decision Lifecycle

- `rewrite`: replace the current snapshot, preserving frontmatter and useful historical sources.
- `patch`: update structured entries only where the batch changes them.
- `append`: preserve historical reasoning; add records, dated corrections or closure notes.
- DECISIONS retains the compatible `append` frontmatter with a mixed internal contract:
  patch the current view, lifecycle and lookup routes; append rationale. Keep relevant active
  and governing choices visible by applicability and scope, not by age alone.

The full ID registry need not stay in the default-read table. As it grows, keep searchable
topic indexes or individual records, route to them from DECISIONS, and preserve each ID,
keywords, replacement relationships and valid detail links. Never reuse an ID; namespace
colliding legacy IDs. Preserve old references with redirects or repair known callers.
Move details only after the live conclusion and historical retrieval path are secure.

Plans and pilots are not evidence of implementation. At closure, link the outcome to its
confirmation or superseding evidence. A partially replaced choice must retain its scope.

## Complete the Confirmed Batch

1. Assemble the full work-unit outcome and separate stable facts, useful history, unfinished
   context and information with no lasting value.
2. Update the smallest sufficient set of canonical owners; keep the current answer visible.
3. Before compression, preserve stable conclusions and full useful evidence, add an archive
   manifest for multi-file bundles, and retain working retrieval links.
4. Register actual new memory directories in DIRS. Do not create ceremonial empty layers.
5. Validate once after the batch. Fix errors and relevant warnings introduced by the change;
   report unrelated pre-existing findings without expanding scope.

Never archive current blockers or active evidence to satisfy a length budget. HISTORY and
detail may be long; use topic / stage navigation when needed. Never invent completed work,
tests, rationale or priorities. Do not fill empty templates with the current maintenance task.

Report what changed, where detailed evidence lives, validation and remaining limitations.
If no write was approved or no durable content warrants it, make no memory diff. Do not ask
for another memory update just because this authorized maintenance operation finished.
