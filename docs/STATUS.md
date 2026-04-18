---
memory_layer: base
update_mode: rewrite
role: "High-level project snapshot"
read_when: "entering project, planning work"
not_for: "module-level detail (-> PROGRESS)"
---

# Project Status

Last updated: 2026-04-18

## Current Focus

- Improve clarity of each template file's identity: role, update mode, boundaries.
- Rename `REPO_STATUS.md` to `PROGRESS.md` to eliminate confusion with `STATUS.md`.
- Add identity-card frontmatter (`update_mode`, `role`, `read_when`, `not_for`) to all template files.

## Done

- [x] Added `AGENTS.md` as a reusable Agent entry template for target repositories.
- [x] Added `docs_template/` as the clean installable docs template.
- [x] Added `MEMORY_MANIFEST.yml` to the clean template.
- [x] Added lightweight `docs/` memory for this repository itself.
- [x] Aligned `README.md` and install script behavior with the new clean template default.
- [x] Removed local absolute-path assumptions from public-facing rules and skills.
- [x] Validated script syntax and smoke-tested default install output.
- [x] Renamed `REPO_STATUS.md` to `PROGRESS.md` across all template directories.
- [x] Added identity-card frontmatter to all `docs_template/` files.
- [x] Added `update_mode` field to `MEMORY_MANIFEST.yml` entries.
- [x] Updated all cross-references in AGENTS.md, README.md, skills, and example templates.

## In Progress

- [ ] Review whether future automated checks should validate manifest/file consistency.

## Backlog

- P0: Keep install behavior and README examples aligned.
- P1: Add more target-agent integration notes if new clients are supported.
- P2: Add automated checks for template completeness.

## Current Contracts

- `docs_template/` should remain clean and low-example.
- `docs_template_example/` may contain teaching prose and longer examples.
- `AGENTS.md` should remain copyable and avoid this repository's internal-only assumptions.
- Public docs and templates must not include personal machine paths.
- Every template file must include identity-card frontmatter: `update_mode`, `role`, `read_when`, `not_for`.
