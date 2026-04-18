---
memory_layer: scaling
update_mode: patch
role: "Module-level implementation checklist"
read_when: "need module-level status, multi-module work"
not_for: "high-level summary (-> STATUS), dated changelogs (-> archive/)"
---

# Progress

## Mainline

- Clean template source: `docs_template/`
- Example template source: `docs_template_example/`
- Repository memory docs: `docs/`
- Agent skills: `.claude/skills/`
- Install helpers: `scripts/`

## Implemented

- `docs_template/` is the default docs tree for target projects.
- `docs_template_example/` remains available for explanation and comparison.
- `AGENTS.md` is a copyable Agent entry template for target repositories.
- All template files include identity-card frontmatter (update_mode, role, read_when, not_for).
- `init-memory` skill scans existing repos and populates empty docs templates with real content, while guarding against placeholder append artifacts, weak git-history inference, and unresolved uncertainty via optional focused sub-agent investigations.

## Gaps

- README and scripts must stay synchronized when install behavior changes.
- Future automated checks could validate that template manifests reference files
  that exist.
