---
memory_layer: base
update_mode: append
role: "Decision archive — why we chose A over B"
read_when: "design question, revisiting old choices"
not_for: "operational rules (-> CONVENTIONS), unresolved discussions (-> SHORT_MEMORY/)"
---

# Decisions

## Log

### DEC-001: Split clean template from teaching example (2026-04-17)

Context:

The repository originally used `docs_template_example/` as both the explanatory
example and the source users copied into target projects. That mixed teaching
content with installable project scaffolding.

Decision:

Use `docs_template/` as the clean installable template and keep
`docs_template_example/` as the teaching/reference version.

Rationale:

Target projects should not inherit example prose as if it were project fact.
The example version remains useful for explaining intent, while the clean
version gives Agents a lower-noise memory layer.

Impact:

Install scripts and README guidance should default to `docs_template/`.
Example-specific docs should stay under `docs_template_example/`.

### DEC-002: Use manifests for progressive disclosure (2026-04-17)

Context:

Agents need a compact way to decide which docs to read without always loading
the full docs tree.

Decision:

Add `MEMORY_MANIFEST.yml` to memory docs trees as the routing layer for read
order, layer purposes, and update triggers.

Rationale:

YAML is easier for Agents to scan and classify than long Markdown prose, while
Markdown remains better for human-readable project memory.

Impact:

When the docs structure changes, update the relevant manifest with the same
change.

### DEC-003: Treat AGENTS.md as a reusable template (2026-04-17)

Context:

The root `AGENTS.md` is not only an instruction file for this repository. It is
also intended to be copied into target repositories as a starting Agent entry
point.

Decision:

Keep root `AGENTS.md` generic and reusable. Put this repository's internal
maintenance details in `docs/` rather than hard-coding them into the root Agent
template.

Rationale:

Target projects need a strong baseline for docs reading, skill usage, data
handling, and documentation maintenance, but they should not inherit assumptions
that only apply to the template repository.

Impact:

`scripts/install_to_project.sh` should copy `AGENTS.md` into target projects.
Future repository-specific rules should be recorded in `docs/CONVENTIONS.md` or
other live docs unless they are also suitable as reusable template guidance.

### DEC-004: Rename REPO_STATUS.md to PROGRESS.md (2026-04-18)

Context:

`REPO_STATUS.md` and `STATUS.md` had names too similar to each other. In real
projects, REPO_STATUS tended to absorb dated changelog entries and grow into a
"catch-all" document, blurring the boundary with STATUS (high-level snapshot)
and archive (historical records).

Decision:

Rename `REPO_STATUS.md` to `PROGRESS.md`. Define it as a module/feature-level
implementation checklist, not a changelog. Dated update entries should move to
`archive/` once they accumulate.

Rationale:

The name "PROGRESS" immediately communicates "granular checklist" rather than
"another status file." It eliminates the STATUS vs REPO_STATUS naming
confusion and gives the file a clearer identity.

Impact:

All template files, manifests, skills, AGENTS.md, and README.md updated.
`docs-in-a-real-project/` retains historical references for reference purposes.

### DEC-005: Add identity-card frontmatter to all template files (2026-04-18)

Context:

Template files had minimal YAML frontmatter (`memory_layer`, `stability`,
`role`) that did not convey how a file should be updated or what should NOT be
put in it. Even the system author forgot the boundaries between similar files.

Decision:

Replace the old `stability` field with a structured identity card:
`update_mode` (rewrite / append / patch), `role` (one-line purpose),
`read_when`, and `not_for` (explicit exclusions with arrows to the correct
file). Add `update_mode` to MEMORY_MANIFEST.yml entries as well.

Rationale:

Agents need to know three things when opening a file: what it is for, how to
update it, and what should go elsewhere. The `not_for` field with explicit
arrows (e.g., "decision rationale (-> DECISIONS)") prevents role creep.

Impact:

All `docs_template/` files, `MEMORY_MANIFEST.yml`, and this repository's own
`docs/` files now carry the new frontmatter format.
