# Docs Linking Reference

Use this reference when the repository contains living docs under `memory-docs/`.

## Purpose

Commit messages should summarize the change and point to the durable project context.
Do not duplicate long narratives that already belong in the living docs.

## Repository Mapping

- `memory-docs/detail_mem/DECISIONS.md`
  - Use for design rationale, tradeoffs, superseding prior choices, and architecture decisions.
  - Prefer referencing concrete IDs like `DEC-007`.
- `memory-docs/STATUS.md`
  - Use for current phase, completed milestones, in-progress work, and backlog.
  - Prefer this when the commit lands part of a broader phase.
- `memory-docs/CONVENTIONS.md`
  - Use for coding rules, workflow rules, and repository-wide constraints.

## Reference Style

Preferred:

```text
Live Docs:
- Status: memory-docs/STATUS.md
- Decisions: DEC-007, DEC-008 in memory-docs/detail_mem/DECISIONS.md
```

Optional when needed:

```text
Live Docs:
- Status: memory-docs/STATUS.md
- Decisions: DEC-007 in memory-docs/detail_mem/DECISIONS.md
- Conventions: memory-docs/CONVENTIONS.md
```

Avoid:

```text
Live Docs:
- see docs
```

## Selection Heuristics

- If the change introduces or refines a technical decision, include `detail_mem/DECISIONS.md`.
- If the change corresponds to a milestone or phase boundary, include `STATUS.md`.
- If the change enforces or updates a repository rule, include `CONVENTIONS.md`.
- If no living doc is relevant, omit `Live Docs` rather than inventing a weak reference.

## Claim Discipline

- A decision referenced from docs must match staged reality.
- If docs describe future work not present in the commit, do not summarize it as done.
- When a commit implements only part of a documented plan, say so in `Risk`.
