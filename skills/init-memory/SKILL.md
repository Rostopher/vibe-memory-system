---
name: init-memory
description: Initialize or migrate an installed memory-docs system from repository evidence. Use after memory-docs templates are installed but still contain placeholders, when existing briefs, plans, notes, and docs must be distilled into the standard layers, or when a user explicitly asks to initialize installed project memory. Do not use for routine incremental updates to already-initialized memory; use update-living-docs instead.
---

# Init Memory

Turn installed `memory-docs/` templates into truthful, concise project memory
without losing useful source detail.

## Required Reference

Before initializing or migrating memory, read
`references/memory-architecture.md` completely. It defines ownership,
distillation, archive bundles, conflict handling, and the optional research
ledger.

## Workflow

### 1. Confirm the installed contract

1. Confirm `memory-docs/INDEX.md` exists. If it does not, ask the user to install
   the template with this repository's installer; do not invent a parallel
   layout.
2. Read `AGENTS.md`, `memory-docs/INDEX.md`, and each standard file's
   frontmatter.
3. Classify the installed memory as:
   - **template**: mostly placeholders;
   - **partial**: real content mixed with placeholders;
   - **initialized**: substantial project-specific content.
4. If memory is already initialized, preserve it and use `update-living-docs`
   unless the user explicitly requests a migration.
5. For an explicit migration of initialized memory:
   - never use template replacement to perform the migration;
   - preserve current owners, frontmatter, custom directories, and project rules;
   - merge only missing protocol text into `AGENTS.md`, `INDEX.md`, and
     `archive/README.md`;
   - add the decision registry progressively from existing stable IDs and
     high-signal current decisions rather than rewriting all history at once;
   - archive detail only after its live conclusion and pointer are secure.

### 2. Establish repository truth

- Inspect repository instructions and the worktree before editing.
- Inventory initial briefs, plans, READMEs, notes, existing docs, code entry
  points, configuration, tests, artifacts, and relevant Git history.
- Separate verified facts from proposals, assumptions, stale statements, and
  unresolved conflicts.
- Treat plans as proposals unless code, artifacts, decisions, or later records
  confirm their execution and outcome.
- Record where important claims came from. Do not silently choose between
  conflicting sources.
- Exclude secrets, private environment files, generated/vendor trees, large
  datasets, and unrelated repositories.

Use Git confidence carefully:

- **high**: valid recent history aligned with a mostly clean tree;
- **medium**: valid but sparse, old, or moderately dirty history;
- **low**: no usable history or a broadly dirty tree.

Git supports observed history; it does not prove current intent, priorities, or
blockers.

When deciding whether work happened before, whether an old route should reopen,
why a decision exists, or which of several historical outcomes is final, use
the bounded historical retrieval gate in `references/memory-architecture.md`.
Do not preload the complete archive or stop at the first matching plan. Search
archive filenames and manifests first; use matching flat archive notes as a
bounded fallback when no manifest routes the topic.

### 3. Define ownership before writing

- Give every recurring question one detailed owner.
- Keep the standard framework files compact.
- Put module detail in `detail_mem/` and register semantic custom directories in
  `DIRS.md`.
- Do not add optional owners unless the information recurs, changes on a
  distinct cadence, or needs a distinct verification method.
- For research projects with repeated experiments, copy
  `assets/research/EXPERIMENT_LEDGER.md` to
  `memory-docs/research/EXPERIMENT_LEDGER.md` and register `research/` in
  `DIRS.md`.

### 4. Confirm material unknowns

Before writing, summarize the inferred project identity, main workflow,
modules, conventions, Git confidence, source conflicts, and important unknowns.

Ask only when an unknown would materially change the project description or
overwrite real content. If the user requested autonomous initialization, mark
the fact `Unknown / needs confirmation` instead of guessing.

### 5. Initialize the standard layers

Process files in this order:

1. `OVERVIEW.md` (`rewrite`): identity, goals, workflow, major areas, stack.
2. `detail_mem/MAP.md` (`patch`): concepts or artifacts to 1–2 authoritative
   entry files, never a full inventory.
3. `CONVENTIONS.md` (`patch`): observed or user-confirmed hard rules.
4. `GLOSSARY.md` (`patch`): domain-specific meanings only.
5. `detail_mem/PROGRESS.md` (`patch`): module-level implementation state.
6. `STATUS.md` (`rewrite`): project-level current focus, recent milestones,
   next actions, and blockers.
7. `HISTORY.md` (`append`): evidence-backed stages and turning points.
8. `detail_mem/DECISIONS.md` (`append`): build the compact decision registry,
   then append detail for choices whose alternatives and reasons are known.
9. `DIRS.md` (`patch`): actual detailed-memory directories.

Leave `INDEX.md`, `SHORT_MEMORY/README.md`, and `archive/README.md` as protocol
files unless the structure itself changed. During first initialization, replace
template entries even in patch/append files; afterwards obey update modes.

### 6. Preserve source detail

- Keep active detailed evidence in its working source or a registered detailed
  owner.
- When source material becomes completed, superseded, rejected, or too detailed
  for the live surface, first distill stable conclusions into owners.
- Then preserve multi-file source detail in
  `memory-docs/archive/YYYYMMDD_topic/` with a manifest.
- Give every manifest non-empty provenance fields, a valid local Markdown link
  back to the distilled owner, natural retrieval terms, and a reopen condition.
- Link a live summary to the archive when the detail remains useful.
- Never archive an unresolved blocker or operational fact still needed today.

### 7. Validate

Run the installed validator:

```bash
python3 .memory-docs-tools/validate_memory_docs.py .
```

Repair initialization-caused errors and high-signal warnings. Treat warnings as
prompts for judgment, not instructions to delete useful context.

## Safety Rules

- Merge with existing content; never overwrite it blindly.
- Preserve provenance, disagreement, and uncertainty.
- Never fabricate status, completion, validation, decisions, or rationale.
- Never infer current state from a proposal or pilot alone; preserve an explicit
  closure or superseded pointer for completed or abandoned plans.
- Do not move active evidence to archive merely to reduce line count.
- Use the project's primary language.

## Completion Report

Report initialized and preserved files, ownership decisions, optional owners
created or omitted, archived source detail, unresolved conflicts, Git
confidence, and validation results.
