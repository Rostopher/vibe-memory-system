---
name: commit-planner
description: Analyze staged, unstaged, and untracked changes; group them into functionally coherent commit batches; and recommend staging order, commit boundaries, and related memory-docs references. Use when the working tree contains multiple kinds of changes and Codex needs to decide how many commits to make, which files belong together, and which project-memory files should be updated or referenced.
---

# Commit Planner

Plan commit batches before writing commit messages.
Use this skill to decide what should be staged together, what should be split into separate commits, and which living docs are relevant to each batch.

## Core Rule

Group changes by implemented behavior and commit intent, not by directory alone.

Use repository living docs as context amplifiers, not as the sole classifier.
Files should be grouped primarily by behavioral cohesion, then refined by `memory-docs/STATUS.md`, `memory-docs/detail_mem/DECISIONS.md`, `memory-docs/CONVENTIONS.md`, and recent commit context when helpful.

## Workflow

1. Inspect the full working tree.
   - Read `git status --short`.
   - Distinguish `staged`, `unstaged`, and `untracked` files.
2. Read the relevant diffs.
   - Read `git diff --staged` for the currently selected batch.
   - Read `git diff` for unstaged tracked files.
   - Inspect new files when they look like part of a feature slice.
3. Read living docs when present.
   - `memory-docs/STATUS.md` for current phase, done items, and backlog.
   - `memory-docs/detail_mem/DECISIONS.md` for relevant decisions or superseding entries.
   - `memory-docs/CONVENTIONS.md` for workflow and repository rules.
4. Classify changes into functional groups.
   - Feature code
   - Tests
   - Docs updates
   - Config or ignore hygiene
   - Refactor-only changes
   - Generated or unrelated noise
5. Propose commit batches.
   - Each batch should be coherent, reviewable, and independently understandable.
   - Prefer behavior-complete slices over partial implementation fragments.
6. For each batch, recommend:
   - goal
   - file list
   - why the files belong together
   - suggested staging order
   - suggested `type(scope)`
   - related living docs
   - exclusions or follow-up batches
7. Hand off the selected batch to `$commit-messages` for commit message generation.

## Working Tree Classification

Treat the working tree as three pools:

- **Staged**: candidate for the next commit right now
- **Unstaged**: tracked files with additional edits that may belong to the current or later commit
- **Untracked**: new files that may be feature code, tests, docs, assets, or noise

Key question:

> Is the current staged set already a self-contained commit, or is it only part of a larger functional change?

## Batching Rules

### 1. Prefer functional cohesion

Group files that together implement one behavior change.

Good grouping:

- `models/paper.py`
- `models/queue.py`
- `tools/pipeline.py`
- `tests/test_pipeline_status_persistence.py`

because they form one feature slice.

Bad grouping:

- all files under `models/`
- all docs in one commit
- all unstaged files in one commit

when those files represent different intents.

### 2. Detect partial feature slices

Warn when staged files look incomplete relative to unstaged or untracked companions.

Examples:

- implementation file staged, but matching test file is unstaged
- pipeline change staged, but new supporting model file is unstaged
- feature code staged, but the relevant living-doc update is missing

When this happens, recommend either:

- stage the related files together, or
- intentionally split the docs/config into a follow-up batch and say why

### 3. Keep hygiene changes separate when possible

Independent `.gitignore`, formatting-only, or repo-hygiene changes should usually be their own batch.

Example:

- `.gitignore`
- `.editorconfig`
- unrelated ignore patterns

should usually not be mixed into a feature commit unless they are strictly required for that feature.

### 4. Docs can be attached or split

Choose one of two strategies and explain the tradeoff:

- **Attached docs batch**: include docs with the feature when docs are part of the feature’s definition of done
- **Separate docs batch**: split docs into a follow-up commit when you want a cleaner code commit or docs are still being refined

### 5. Ignore backlog-only context

Do not group files together only because they appear in the same future phase or backlog item.
Backlog context helps interpret intent, but staged reality still wins.

## Living Docs Mapping

Use docs to sharpen commit boundaries.

- `memory-docs/STATUS.md`
  - Use to judge whether a change is one milestone, a partial phase, or a follow-up cleanup.
- `memory-docs/detail_mem/DECISIONS.md`
  - Use to connect code changes to decision IDs and see whether multiple files belong to one technical decision.
- `memory-docs/CONVENTIONS.md`
  - Use to identify rule-driven changes that may deserve their own docs or conventions batch.

If living docs and code reality disagree, prefer code reality and mention the mismatch.

## Output Format

Always produce a structured plan.

Use this template:

```text
Working Tree Summary:
- staged: ...
- unstaged: ...
- untracked: ...

Recommended Commit Batches:
1. <batch name>
   - Goal:
   - Files:
   - Why grouped together:
   - Suggested staging command:
   - Suggested type/scope:
   - Related live docs:
   - Exclusions / follow-up:
```

If the current staged set is already good to commit, say so explicitly.

If there is only one reasonable commit, say that too.

## Decision Heuristics

Use these heuristics in order:

1. **Behavioral cohesion**: do the files implement one observable change?
2. **Dependency completeness**: are required helpers/tests/docs included?
3. **Reviewability**: would a reviewer understand the purpose in one pass?
4. **Operational safety**: can this batch stand on its own without hidden coupling?
5. **Docs alignment**: do the living docs support this grouping?

## Hand-off to `$commit-messages`

Once a batch is chosen, recommend handing only that batch to `$commit-messages`.

Do not write the final commit message inside this skill unless the user explicitly asks.
This skill plans commits; `$commit-messages` writes the message.

## Good Output Example

```text
Working Tree Summary:
- staged: .gitignore
- unstaged: none
- untracked: memory-docs/STATUS.md, memory-docs/detail_mem/DECISIONS.md, src/academic_tools/models/queue.py

Recommended Commit Batches:
1. repo hygiene
   - Goal: commit ignore-rule cleanup independently
   - Files: .gitignore
   - Why grouped together: self-contained repository hygiene change
   - Suggested staging command: git add .gitignore
   - Suggested type/scope: chore(core)
   - Related live docs: none required
   - Exclusions / follow-up: do not mix with status-persistence feature files

2. status persistence feature
   - Goal: land paper-level and global processing status persistence
   - Files: src/academic_tools/models/paper.py, src/academic_tools/models/queue.py, src/academic_tools/tools/pipeline.py, tests/test_pipeline_status_persistence.py
   - Why grouped together: one functional feature slice with supporting test coverage
   - Suggested staging command: git add ...
   - Suggested type/scope: feat(status)
   - Related live docs: memory-docs/STATUS.md, DEC-007, DEC-008, DEC-009 in memory-docs/detail_mem/DECISIONS.md
   - Exclusions / follow-up: batch tools remain separate
```

## Bad Patterns

- grouping files only because they share a directory
- treating all docs as one mandatory batch
- ignoring unstaged companion files that clearly belong to the same feature
- forcing one large commit when the working tree obviously contains multiple intents
- writing commit messages instead of planning batches

## Output Checklist

Before finalizing, verify:

- each batch has one clear goal
- no batch hides an unrelated hygiene or docs-only change
- partial feature slices are called out explicitly
- living-doc references are relevant to the grouped files
- the plan makes it obvious what to stage next
