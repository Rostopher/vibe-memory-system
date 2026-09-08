# Memory Docs Initialization Architecture

## Contents

1. Design goals
2. Ownership and boundaries
3. Information flow
4. Bounded historical retrieval
5. Decision registry and plan lifecycle
6. Archive contract
7. Optional research ledger
8. Initialization decisions

## 1. Design goals

Initialize project memory that is:

- **visible**: current truth is reachable from the framework layer;
- **owned**: each recurring question has one detailed owner;
- **compressed**: framework files contain conclusions and navigation, not
  transcripts;
- **loss-aware**: source detail remains retrievable when it leaves the active
  surface;
- **adaptive**: optional owners appear only when the project needs them.

The installed `memory-docs/INDEX.md` and per-file frontmatter remain the
canonical contract. Do not add another global manifest.

## 2. Ownership and boundaries

Typical ownership:

| Question | Owner |
|---|---|
| What is this project? | `OVERVIEW.md` |
| What matters now at project level? | `STATUS.md` |
| How did the project reach this point? | `HISTORY.md` |
| What rules must work obey? | `CONVENTIONS.md` |
| What does a domain term mean? | `GLOSSARY.md` |
| Where is a concept implemented? | `detail_mem/MAP.md` |
| What is each module's implementation state? | `detail_mem/PROGRESS.md` |
| Why was a stable choice made? | `detail_mem/DECISIONS.md` |
| What must the next session resume? | `SHORT_MEMORY/` |
| What historical detail explains a summary? | the linked archive record |
| What evidence supports a research claim? | optional `research/EXPERIMENT_LEDGER.md` |

Boundary rules:

- `STATUS.md` owns the project-level current snapshot and shared next actions.
- `PROGRESS.md` owns module-level state, gaps, and local next steps.
- `SHORT_MEMORY/` contains only continuation detail not already obvious from
  stable owners.
- The research ledger owns evidence and claim limits, not current TODOs or live
  infrastructure state.
- Non-owner documents may state a short consequence, then link to the owner.

## 3. Information flow

After initialization, routine memory writes happen at a completed work unit, after the user
confirms closeout and memory scope. An explicit initialization, migration or maintenance request
already authorizes its scope. Do not write after every small edit, probe or commit.
Commit and deployment are not prerequisites. Respect deferral and user-authored summaries.
Complex history, troubleshooting and handoffs may be long; default reading and writing cadence
are the limits to control, not evidence length. HISTORY is read on demand.

Use one-way distillation:

```text
initial sources / raw artifacts
          ↓
active detailed owners or research evidence
          ↓
decisions, progress, and current status
          ↓
framework navigation and session continuation
```

When detail leaves the active path:

```text
distill stable facts → update owners → archive source detail → link for retrieval
```

Do not reverse-copy full explanations back into framework files.

## 4. Bounded historical retrieval

Do not preload all historical material during normal initialization. Apply a
historical retrieval gate when a source or proposed summary would claim that:

- work was never attempted or must be implemented again;
- an old route should be reopened or extended;
- a stable decision should be reversed;
- a regression needs historical diagnosis;
- the project needs an explanation of why the current state exists.

For each triggered question:

1. Derive 2–4 natural topic terms, including old names or aliases.
2. Search decision registry and detail, status and history, experiment ledgers,
   plans and research notes, archive filenames and manifests, and relevant Git
   history. If no manifest routes the topic, search matching flat archive notes
   as a bounded fallback.
3. Read only useful hits; do not scan every archived source by default.
4. Continue past the first hit until proposal, pilot, confirmation, closure,
   and superseded stages are distinguished.
5. Prefer the current canonical owner over stale plans or archived wording.
6. Verify consequential conclusions against current code, tests, artifacts, or
   durable experiment evidence.

This gate is a retrieval safeguard, not a second always-loaded memory layer.

## 5. Decision registry and plan lifecycle

Keep `detail_mem/DECISIONS.md` compatible with `update_mode: append`, but use a
mixed internal contract:

- maintain a compact `ID | Status | Topic | Current conclusion | Keywords |
  Detail` registry in place;
- append rationale and evidence records without silently rewriting them;
- never reuse a published ID;
- namespace imported legacy IDs when source histories collide;
- keep the default view focused on currently applicable decisions;
- as the registry grows, move complete historical lookup rows to topic indexes while retaining
  stable IDs, natural keywords, lifecycle relationships, detail links and discoverable routes;
- preserve old references by redirects or update known callers within the maintenance scope;
- archive rationale after preserving its live conclusion and valid historical lookup path.

Choose visibility by current applicability and scope, not age. Long active rationale may have
its own detailed page. No budget requires discarding useful history or hiding current constraints.

A plan is a proposal, not proof of execution or current status. For a completed,
abandoned, or replaced plan, preserve a closure or superseded pointer linking
the plan to the current owner, decision, confirming evidence, or archive
manifest. A promising pilot does not become a governing decision without its
confirmation and closure state.

## 6. Archive contract

Flat archive files remain valid for a single self-contained historical record.
Use a dated topic directory for a multi-file source bundle:

```text
memory-docs/archive/20260730_initial-design/
├── README.md
├── initial-brief.md
└── design-notes.md
```

The manifest should contain:

```markdown
# Archived: <topic>

- Archived: YYYY-MM-DD
- Reason: completed | superseded | compressed | rejected
- Preserves: <source files, artifacts, or discussion>
- Distilled into: [DEC-001](../../detail_mem/DECISIONS.md#dec-001)
- Retrieval keywords: <natural terms and aliases>; reopen when <condition>

## Context

Explain what this bundle contains and when to reopen it.
```

Rules:

- every required field must have a non-empty value;
- `Distilled into` must contain at least one valid local Markdown link to the
  live owner, not only a filename or plain-text path;
- retrieval keywords should use terms a future reader would naturally search
  and state when the bundle should be reopened;
- archive only after stable facts have owners;
- preserve source wording when provenance matters;
- do not rewrite old interpretation to match a later conclusion;
- add a correction note or a new live decision instead;
- keep current operations and unresolved blockers active.

## 7. Optional research ledger

Create the ledger only when experiments recur and future readers need stable
protocol, artifact, interpretation, or claim-boundary evidence.

The ledger owns:

- experiment question or hypothesis;
- protocol and comparability conditions;
- code revision, configuration, seed, data, and artifact pointers;
- result, interpretation, uncertainty, and claim boundary;
- validity, supersession, and links to related experiments.
- failure or stopping cause, reopening conditions and whether a feasible route was integrated.

Technical demos can use registered topic records instead of the optional research ledger.
Record repository-specific revisions and recoverable uncommitted differences where necessary;
code versions alone may not restore data, configuration or external model behavior.

It excludes:

- current project TODOs and next experiment direction;
- module implementation progress;
- live server/process state;
- raw logs that already have a durable artifact location.

Failed or invalid experiments remain evidence. Append a correction or
superseding entry instead of rewriting the historical record.

## 8. Initialization decisions

Create an optional owner when at least one condition holds:

- the question recurs across sessions;
- the information changes on a different cadence from existing owners;
- the content has a distinct verification method;
- combining it with an existing owner would hide current truth.

When initial sources disagree:

1. Prefer implemented and validated reality over aspirational text.
2. Prefer newer verified state over older state.
3. Preserve unresolved disagreement when evidence is insufficient.
4. Record provenance; never invent reconciliation.

An empty or scaffold-only repository is valid. Record observable structure and
unknowns without manufacturing goals or completed work.
