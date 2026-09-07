# Living Docs Health and Maintenance

## Contents

1. Maintenance invariant
2. Conditional historical retrieval gate
3. Optional health metadata
4. Validation severity and workflow
5. Repair rules
6. Archive maintenance
7. Session handoffs
8. Research ledger boundary
9. Checker limitations and compatibility

## 1. Maintenance Invariant

Every durable fact has one detailed owner. Other active documents may show the consequence needed by their audience, but should link to the owner rather than reproduce its explanation.

The active memory surface should make these answers easy to find:

- what matters now;
- what happens next;
- what is blocked or uncertain;
- which decisions and constraints govern the work;
- where detailed evidence or historical context lives.

Health checks protect retrieval and provenance. They do not optimize documents for minimum size and do not authorize automatic deletion or rewriting.

Apply repairs within a user-confirmed memory batch or an explicit maintenance request. During
ordinary implementation, report discovered discrepancies for closeout instead of immediately
editing memory. Do not repeat a permission question for work already authorized.
Long histories, troubleshooting records and handoffs are valid; read them on demand.

## 2. Conditional Historical Retrieval Gate

Do not preload historical memory for an ordinary documentation update. Apply this gate before:

- claiming that prior work does not exist;
- implementing something that may duplicate an earlier attempt;
- reopening or extending a closed route;
- reversing a stable decision;
- diagnosing a regression against earlier behavior;
- explaining why the project reached its current state.

Use a bounded retrieval sequence:

1. Derive 2–4 natural topic terms, including old names, abbreviations, or aliases.
2. Search the decision registry and detail, `STATUS.md`, `HISTORY.md`, experiment ledgers, plans and research notes, archive filenames and manifests, and relevant Git history.
3. Open only high-signal hits. Do not read every archived source by default.
   When no manifest routes the topic, search matching flat archive notes as a
   bounded fallback.
4. Do not stop at the first match. Establish whether each hit is a proposal, pilot, confirmation, closure, superseded result, or merely historical context.
5. Prefer the current canonical owner when old plans or archived wording disagree.
6. Verify consequential conclusions against current code, tests, artifacts, or durable experiment evidence.

A plan authorizes exploration; it does not prove that the work ran or that its proposal became current truth. A positive pilot does not override a later failed confirmation. If the lifecycle remains ambiguous, report that uncertainty rather than inventing closure.

When this gate reveals a durable retrieval gap, propose it for work-unit closeout; if maintenance
is already authorized, repair the appropriate owner, index, lifecycle pointer or manifest.
Do not copy the whole historical chain into `STATUS.md`.

## 3. Optional Health Metadata

The standard `role`, `read_when`, `not_for`, and `update_mode` fields remain the document contract. A project may add either of these optional frontmatter fields to an individual document:

| Field | Value | Meaning |
|---|---|---|
| `line_budget` | positive integer | Advisory size threshold for an active document |
| `stale_after_days` | non-negative integer | Maximum age before a volatile document should be verified |

Keep these thresholds next to the document they govern. Do not add a second global ownership manifest merely to configure health checks.

Treat a line budget as a prompt to classify content, not as a deletion target:

- approaching the budget may produce an advisory warning;
- exceeding the budget may produce a warning;
- a detailed owner may legitimately be long when its information is active and non-duplicated.

Use `stale_after_days` only for volatile truth such as project status or verified remote state. A stale finding means “verify before trusting,” not “change the date.” Update the content and its explicit verification date together after checking code, artifacts, processes, or the responsible external system.

The validator also gives a conservative advisory for ordinary prose lines over
500 characters. It skips frontmatter, fenced code, headings, tables, lists, and
block quotes. Treat this as a readability and line-budget integrity signal, not
as a mandatory wrapping style.

## 4. Validation Severity and Workflow

Use the installed project validator:

```bash
python3 .memory-docs-tools/validate_memory_docs.py .
```

Use `--json` when machine-readable results are useful. Use `--strict` only when warnings should make the command fail.

Interpret findings as follows:

| Severity | Meaning | Required response |
|---|---|---|
| error | Deterministic memory contract is invalid | Repair errors introduced by the work before completion |
| warning | High-signal integrity or heuristic health problem | Resolve when related to the work; otherwise preserve and report |

Run validation before editing when the tool is available, then again afterward. This distinguishes pre-existing findings from regressions.

Do not broaden a focused task into a repository-wide documentation rewrite. Always resolve:

- errors introduced by the current change;
- broken links, missing owners, or invalid archive manifests caused by the current change;
- warnings that show the current update was routed to the wrong owner.

Preserve and report unrelated pre-existing findings unless they make the requested memory update unsafe or the user expands the scope.

## 5. Repair Rules

### Broken Local Links

Verify whether the target moved, was renamed, or was never created. Correct the link or restore the intended target. Do not simply remove a useful provenance link to make validation pass.

Ignore external URLs unless a separate task explicitly checks them. A local fragment or path should remain relative and portable.

### Oversized Active Documents

Classify the excess before moving it:

- current project-level answer → keep concise and visible in `STATUS.md`;
- active module detail → keep in `PROGRESS.md` or another registered detailed owner;
- active research evidence → keep in the optional research ledger;
- repeated explanation → retain it in one owner and link elsewhere;
- completed or superseded detail → distill and archive it;
- raw output already preserved as an artifact → link to the artifact instead of copying it.

Never hide current truth merely to satisfy `line_budget`.

### Stale Volatile Documents

Verify the state from implementation, artifacts, process state, commands, or the responsible system. Then update both the content and the verification date.

If verification is impossible:

- mark the state as unknown or unverified;
- preserve the last verified observation and its date;
- state what must be checked next.

Do not refresh only the timestamp. If an explicit update or verification date is older than the document's latest Git change, inspect whether content changed without its freshness marker being maintained.

### Duplicate Active Content

1. Identify the canonical detailed owner.
2. Preserve the full explanation there.
3. Replace other copies with the local consequence and a link.
4. If neither document clearly owns the fact, repair the ownership boundary first.

Repeated licenses, safety rules, quotations, generated schemas, and deliberately mirrored public instructions can be legitimate. Use judgment before changing them.

### Missing Visibility

Route important owners from `memory-docs/INDEX.md` or `memory-docs/DIRS.md`. Put only the shortest current conclusion in `STATUS.md`; do not duplicate the detailed owner to make it visible.

### Decision Registry and Completed Plans

Keep the decision registry compact and searchable. Patch a row's status, one-line current conclusion, natural keywords, and detail pointer as the lifecycle changes; retain the stable ID. Append detailed rationale or a dated closure note instead of silently rewriting historical reasoning.

Never reuse a decision ID. Qualify colliding imported IDs with a stable source or date namespace.
The current view shows applicable decisions, not every historical ID. As it grows, keep complete
lookup rows in discoverable topic indexes with keywords, lifecycle, replacement and detail links.
Retain routes from DECISIONS and preserve old references with redirects or repaired callers.
Archive rationale only after its live conclusion and historical lookup path are secure.
An old but governing decision remains visible; a recent local detail need not become a global rule.

Treat plans as proposals. When a plan completes, stops, or is replaced, leave an explicit closure or superseded pointer from the plan or its registered entry to the current owner, decision, confirming evidence, or archive manifest. Do not let an old plan remain the easiest apparent statement of current state.

### Invalid or Unregistered Structure

Preserve required frontmatter and update modes. Register a new semantic subdirectory in `DIRS.md` in the same change. Do not create empty ceremonial directories.

## 6. Archive Maintenance

Archive-before-compression means:

1. distill stable conclusions into their active owners;
2. preserve the source detail at useful fidelity;
3. write and validate the archive manifest;
4. link the active summary to the archive when the detail remains relevant;
5. only then shorten or replace the live source.

A single self-contained retrospective or historical note may remain a flat file under `memory-docs/archive/`.

Use a dated topic bundle for multiple related source files:

```text
memory-docs/archive/YYYYMMDD_topic/
├── README.md
└── preserved-source.*
```

Its `README.md` or `MANIFEST.md` must state, with non-empty values:

- archive date and reason;
- preserved sources or artifacts;
- live documents and headings that own the distilled conclusions, using at least one valid local Markdown link;
- natural retrieval keywords, old names, and aliases;
- when a future reader should reopen the bundle.

An empty label is not a completed field. `Distilled into: detail_mem/DECISIONS.md` is also insufficient: use a link such as `[DEC-017](../../detail_mem/DECISIONS.md#dec-017)`. Keep manifest links valid. When the historical detail materially supports a live summary, preserve discoverability in both directions.

Do not continuously rewrite archived material to match current truth. Add a dated correction note or update the active owner. Never archive an unresolved blocker, a current operating procedure, active evidence, or the only copy of a current decision.

## 7. Session Handoffs

Write handoffs when explicitly requested or within the confirmed memory scope. Do not bypass
a user's choice to defer memory by automatically creating a session note. A detailed handoff
may be long when necessary; its ownership is temporary continuation context, not a word limit.

`SHORT_MEMORY/` is continuation context, not another project-status database.

Prefer one clearly current handoff per workstream, but allow multiple handoffs when parallel work genuinely requires them. Each active handoff should identify its workstream and avoid claiming to be the sole current state of unrelated work.

When a handoff is superseded:

1. distill stable facts into their owners;
2. update or replace the active handoff for that workstream;
3. archive the old handoff only when its detailed context remains useful.

Multiple well-scoped handoffs are not inherently unhealthy. Multiple files claiming the same workstream's current state are.

## 8. Research Ledger Boundary

`memory-docs/research/EXPERIMENT_LEDGER.md` is optional. Its absence is not a health finding.

When present, it owns durable experimental evidence:

- question or hypothesis;
- protocol and comparability boundary;
- artifact and result locations;
- observed results and interpretation;
- uncertainty, negative evidence, and claim limits;
- relationships to superseded or follow-up experiments.

It does not own current TODOs, the next experiment, live server state, raw command logs, or session-resume instructions. Route those to `STATUS.md`, `PROGRESS.md`, a registered operational owner, or `SHORT_MEMORY/`.

## 9. Checker Limitations and Compatibility

The validator is intentionally lightweight. It cannot prove:

- semantic consistency across paraphrased lists, tables, or prose;
- factual correctness of a documented claim;
- whether a historical command still runs;
- whether external state is current;
- whether every duplicate is harmful;
- whether an archive should be reopened for a new decision.

Duplicate detection may skip or conservatively sample structured content to avoid noise. Freshness is evidence to verify, not proof that content is wrong. Warning-free output therefore means “no configured high-signal problem was detected,” not “project memory is complete or perfectly consistent.”

Use `memory-docs/INDEX.md`, document frontmatter, and `DIRS.md` as the memory contract. Do not require `docs/.living-docs.json`, `MEMORY_MANIFEST.yml`, or a second checker. Respect project-specific detailed directories and thresholds instead of imposing one universal taxonomy.
