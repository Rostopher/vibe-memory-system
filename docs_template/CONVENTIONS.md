---
memory_layer: base
update_mode: patch
role: "Hard rules and contracts — what must be followed, not why (why -> DECISIONS)"
read_when: "before editing code, style/contract questions, checking naming rules"
not_for: "decision rationale (-> DECISIONS), how to run (-> RUNBOOK), one-off preferences"
---

# Conventions

Record hard rules, stable contracts, naming rules, and safety constraints.

## Repository Rules

- Main development paths:
- Reference-only or legacy paths:
- Generated paths that should not be edited manually:
- Files that require explicit user approval before editing:

## Naming and Structure

- File naming:
- Function and variable naming:
- Module boundaries:
- Test placement:

## Safety and Error Handling

- Missing data policy:
- Whether silent skips are allowed:
- Required logging or error context:
- Operations that must fail loudly:

## Data / Interface Contracts

- Stable input layer:
- Stable output layer:
- Schema or primary key rules:
- Backward compatibility expectations:

## Artifact Rules

- Generated output directories:
- Final artifact directories:
- Large or binary file policy:

## Documentation Rules

- Docs entry point:
- When to update `STATUS.md`:
- When to update `DECISIONS.md`:
- When to update `MAP.md`:
- When to write `SHORT_MEMORY/`:

## Environment Rules

- Runtime version expectations:
- Dependency management:
- Environment variable policy:
- Local path and secret policy:
