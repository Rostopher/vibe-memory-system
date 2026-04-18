---
memory_layer: base
update_mode: patch
role: "Docs entry point — routing rules and reading order"
read_when: "entering project, deciding which docs to read"
not_for: "project content (-> OVERVIEW and other docs)"
---

# Vibe Memory System Docs

These docs describe this repository itself, not the template copied into target
projects.

## Read Order

1. `docs/MEMORY_MANIFEST.yml`
2. `docs/OVERVIEW.md`
3. `docs/STATUS.md`
4. `docs/CONVENTIONS.md`
5. `docs/DECISIONS.md`
6. `docs/MAP.md`

## Repository vs Template

- `docs/` tracks this repository's own status and decisions.
- `docs_template/` is the clean installable template.
- `docs_template_example/` is the explanatory example template.
- `.claude/skills/` contains optional Agent workflows.
- `scripts/` installs or syncs templates and skills.

When changing template structure, update the relevant manifest and the install
script if default behavior changes.
