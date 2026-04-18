---
memory_layer: base
update_mode: patch
role: "Docs entry point — routing rules and reading order"
read_when: "entering project, deciding which docs to read"
not_for: "project content (-> OVERVIEW and other docs)"
---

# Project Memory Docs

This directory is the project's memory layer for Agents and humans.

Use these docs to preserve stable project facts, current status, decisions,
contracts, mappings, and session handoff notes.

## Read Order

For normal project context:

1. `docs/MEMORY_MANIFEST.yml`
2. `docs/OVERVIEW.md`
3. `docs/STATUS.md`
4. `docs/RUNBOOK.md`
5. `docs/CONVENTIONS.md`

Read on demand:

- `docs/DECISIONS.md` for rationale behind stable choices
- `docs/GLOSSARY.md` for terms, variables, labels, and display names
- `docs/PROGRESS.md` for module-level implementation checklist
- `docs/MAP.md` for feature, artifact, and file mappings
- `docs/SHORT_MEMORY/` for session handoff notes
- `docs/archive/` for historical records

## Update Rules

- Stable project truth goes in base memory.
- Detailed active implementation context goes in scaling memory.
- Useful but unstable session context goes in `SHORT_MEMORY/`.
- Completed historical records go in `archive/`.
- Do not write raw discussion into stable docs until it becomes a stable fact.
- If code and docs disagree, trust current code and update or flag the docs.

## Files

| File | Role | Update Mode |
|---|---|---|
| `MEMORY_MANIFEST.yml` | Machine-readable routing and progressive disclosure rules | patch |
| `OVERVIEW.md` | Project purpose, scope, architecture, and main directories | rewrite |
| `STATUS.md` | Current high-level state and priorities | rewrite |
| `DECISIONS.md` | Stable decisions and rationale | append |
| `GLOSSARY.md` | Terms, variables, labels, and naming meanings | patch |
| `RUNBOOK.md` | Commands, validation, debugging, and outputs | rewrite |
| `CONVENTIONS.md` | Hard rules, contracts, and safety constraints | patch |
| `PROGRESS.md` | Module-level implementation checklist | patch |
| `MAP.md` | Concept, artifact, feature, and file mappings | patch |
| `SHORT_MEMORY/` | Session-level handoff notes | append |
| `archive/` | Historical records and retrospectives | append |
