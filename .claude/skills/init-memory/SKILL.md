---
name: init-memory
description: Scan an existing repository and initialize newly installed memory-docs templates with evidence-backed project facts. Use after memory-docs is first installed, when its files still contain placeholders, or when a user asks to initialize project memory from code, configuration, README files, and Git history.
---

# Init Memory

Turn a fresh `memory-docs/` template into truthful project memory. Do not invent goals, priorities, architecture, decisions, or completion states.

## Preflight

1. Confirm `memory-docs/INDEX.md` exists at the project root.
2. Read `AGENTS.md` and `memory-docs/INDEX.md` completely.
3. Inspect every standard memory file's frontmatter and classify it as:
   - template: mostly placeholders;
   - partial: real content mixed with placeholders;
   - initialized: substantial project-specific content.
4. If initialized content already exists, do not overwrite it wholesale; use `update-living-docs` unless the user explicitly requests reinitialization.

The current standard has no `MEMORY_MANIFEST.yml`, `RUNBOOK.md`, or `memory-docs/README.md`. Do not recreate legacy files merely to satisfy an older layout.

## Evidence Scan

Collect only what is needed:

- identity and purpose: root README, package manifest, license;
- structure and entry points: directory tree, main scripts, package entry files;
- conventions: lint, format, test, CI, build, container, and environment examples;
- current implementation: source modules, tests, artifacts, explicit TODOs;
- history: Git status and recent commits, only if Git is valid.

Exclude secrets, private environment files, generated/vendor directories, large data, and unrelated external repositories.

### Git confidence

- High: valid, recent history aligned with a mostly clean tree.
- Medium: valid but sparse, old, or moderately dirty.
- Low: no usable Git history or a broadly dirty tree.

Git supports observed history; it does not prove current priorities, blockers, roadmap, or intent. When confidence is low, mark those facts unknown unless the user confirms them.

An empty or scaffold-only project is valid. Initialize its observable structure and explicitly record that implementation, tech stack, and research/business goals are not yet defined.

## Confirmation Rule

Before writing, summarize the inferred project identity, main workflow, modules, conventions, Git confidence, and important unknowns.

Ask the user only when an unknown would materially change the project description or overwrite existing real content. If the user explicitly requested autonomous initialization, continue with `Unknown / needs confirmation` rather than guessing.

## Initialize Files

Process in this order so later files use established context:

1. `OVERVIEW.md` (`rewrite`): project identity, goals, top-level workflow, major areas, tech stack.
2. `detail_mem/MAP.md` (`patch`): concepts and artifacts to 1–2 authoritative entry files; never a full file inventory.
3. `CONVENTIONS.md` (`patch`): only observed or user-confirmed hard rules.
4. `GLOSSARY.md` (`patch`): domain-specific meanings, not generic programming terms.
5. `detail_mem/PROGRESS.md` (`patch`): module checklist; use `unknown` when evidence is insufficient.
6. `STATUS.md` (`rewrite`): current focus, 3–5 recent milestones, active work, confirmed backlog.
7. `HISTORY.md` (`append`): only evidence-backed stages or user-confirmed turning points.
8. `detail_mem/DECISIONS.md` (`append`): only decisions whose alternatives and reasons are known.
9. `DIRS.md` (`patch`): register actual detailed-memory subdirectories.

Leave `INDEX.md`, `SHORT_MEMORY/README.md`, and `archive/README.md` as protocol files unless the structure itself changed.

During first initialization, replace template placeholder entries even in `patch` and `append` files. After initialization, obey normal update modes.

## Writing Rules

- Preserve YAML frontmatter and each file's `role`, `read_when`, and `not_for` boundary.
- Keep framework files compact; route growing detail into `detail_mem/` or registered custom directories.
- Do not turn `MAP.md` into a full code catalog or `STATUS.md` into a changelog.
- Do not infer `done`, `active`, or `stale` from file existence alone.
- Do not manufacture historical decisions from visible architecture; rationale requires evidence.
- Use the project's primary language.

## Validate and Report

Prefer the project-local validator when installed:

```bash
python .memory-docs-tools/validate_memory_docs.py .
```

Otherwise run `scripts/validate_memory_docs.py` from the vibe-memory-system source against the project root.

Report which files were initialized, confidence and remaining unknowns, validation results, and any existing content intentionally preserved.
