---
memory_layer: base
update_mode: patch
role: "Project dictionary — what terms, variables, and labels mean in this project"
read_when: "encountering unfamiliar terms, naming questions, data schema questions"
not_for: "file/code location mapping (-> MAP), operational rules (-> CONVENTIONS)"
---

# Glossary

## `docs_template/`

Clean installable docs scaffold for target projects. It should avoid long
examples and project-specific facts.

## `docs_template_example/`

Teaching/reference version of the docs scaffold. It may include examples,
explanatory prose, and guidance for users evaluating the system.

## `MEMORY_MANIFEST.yml`

Structured routing file that tells Agents which docs to read, what each layer is
for, and when each file should be updated.

## Base Memory

Stable project facts that should be reused across sessions.

## Scaling Memory

Detailed active implementation context that is too granular for base memory.

## Session Memory

Temporary handoff context that is useful but not stable enough for base memory.

## Historical Memory

Retrospective or completed records kept for later reference.
