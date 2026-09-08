---
name: commit-messages
description: Generate structured git commit messages for staged changes using Conventional Commits plus `Why`/`What`/`Risk`/`Tests` sections. Use when preparing a commit after code changes, especially in repositories that keep living docs under `memory-docs/`. Prefer linking detailed rationale and progress to `memory-docs/detail_mem/DECISIONS.md`, `memory-docs/STATUS.md`, and `memory-docs/CONVENTIONS.md` instead of expanding the commit body with long design narratives.
---

# Commit Messages

Generate commit messages that are useful to both humans and future agents.
Keep the commit self-contained at summary level, then point to the living docs for the full context.

## Core Rule

Commit messages should be self-contained summaries with stable pointers into living docs, not full replacements for project context.

If the repository uses `memory-docs/`, prefer linking detailed context and decisions there instead of expanding commit bodies with long design narratives.

Reference records that already exist and match the staged facts. Message generation does not
authorize creating or updating memory; respect the user's work-unit closeout decision.
If memory is deferred or no relevant record exists, make the commit self-contained and omit
unsupported Live Docs links. Do not fabricate an ID or require memory before committing.

## Workflow

1. Read the staged facts first.
   - Inspect `git status --short`.
   - Inspect `git diff --staged --name-only`.
   - Inspect `git diff --staged`.
2. Read the repository living docs when present.
   - `memory-docs/detail_mem/DECISIONS.md` for design rationale and decisions.
   - `memory-docs/STATUS.md` for current phase, completed work, and backlog.
   - `memory-docs/CONVENTIONS.md` for coding and workflow rules.
3. Separate information into two buckets.
   - **Implemented now**: behavior and decisions reflected in staged changes.
   - **Not implemented now**: future phases, deferred tools, unmerged ideas.
4. Generate the commit message.
   - Title uses Conventional Commits.
   - Body uses `Why`, `What`, `Risk`, `Tests`, and `Live Docs`.
5. Run a claim check before finalizing.
   - Do not claim behavior not present in staged changes.
   - Do not promote design discussion into implementation facts.
   - If a decision doc exists but the code does not match it yet, say so in `Risk` or omit it.

## Title Format

Use:

```text
type(scope): subject
```

Rules:

- `type` must be one of: `feat|fix|refactor|perf|docs|test|build|ci|chore|revert`
- `scope` should be the dominant functional scope
- `subject` must start with an English verb
- keep the subject under 72 characters
- do not end the subject with a period
- summarize the most important behavior change, not implementation detail

## Scope Selection

Prefer repository-specific functional scopes over file-path scopes.

For this repository, prefer:

- `status`
- `pipeline`
- `queue`
- `models`
- `ocr`
- `metadata`
- `structure`
- `translate`
- `summary`
- `rename`
- `zotero`
- `arxiv`
- `config`
- `docs`
- `core`

If several areas changed, choose the dominant behavioral scope. Use `core` only when no better scope fits.

## Body Format

Default template:

```text
type(scope): subject

Why:
- ...

What:
- ...

Risk:
- ...

Tests:
- ...

Live Docs:
- ...
```

Section rules:

- `Why`: 1-2 bullets explaining the problem or motivation
- `What`: 2-4 bullets describing implemented behavior changes
- `Risk`: 1-2 bullets describing incomplete areas, compatibility notes, or operational cautions
- `Tests`: list actual commands, `manual validation`, `compile only`, or `not run`
- `Live Docs`: point to the relevant living docs with stable IDs or paths

## Live Docs Linking Rules

Prefer stable references over vague mentions like `see docs`.

For this repository:

- Use `memory-docs/detail_mem/DECISIONS.md` for design rationale and decision history.
- Reference decisions by ID when possible, for example `DEC-007`.
- Use `memory-docs/STATUS.md` for phase, done, in-progress, and backlog context.
- Use `memory-docs/CONVENTIONS.md` when the change is governed by or updates repository rules.

Preferred `Live Docs` formats:

```text
Live Docs:
- Status: memory-docs/STATUS.md
- Decisions: DEC-007, DEC-008 in memory-docs/detail_mem/DECISIONS.md
```

or, when needed:

```text
Live Docs:
- Status: memory-docs/STATUS.md
- Decisions: DEC-007 in memory-docs/detail_mem/DECISIONS.md
- Conventions: memory-docs/CONVENTIONS.md
```

Do not cite docs that are unrelated to the staged change.

## Claim Discipline

- Base the summary primarily on staged changes.
- Use docs as context and stable references, not as proof that code is already implemented.
- Future work must not be written as completed work.
- If Phase 2 or backlog items are discussed but not staged, mention them only as risk or omit them.
- Never invent test coverage.

## Good Patterns

Good title:

```text
feat(status): persist paper and global processing state
```

Good body:

```text
Why:
- Preserve processing state across restarts and agent handoffs
- Record stage completion at exact function completion points

What:
- Add paper-level status persistence in workspace metadata
- Add global queue persistence with lock-protected updates
- Sync pipeline and background job state to disk

Risk:
- Batch orchestration tools are not included in this commit
- Artifact-based compatibility checks remain in place

Tests:
- python -m compileall src/academic_tools/tools/pipeline.py
- manual validation of paper and queue status updates

Live Docs:
- Status: memory-docs/STATUS.md
- Decisions: DEC-007, DEC-008, DEC-009 in memory-docs/detail_mem/DECISIONS.md
```

Bad patterns:

- very long design essays inside the commit body
- listing raw file names as the subject
- claiming planned tools are implemented when only docs mention them
- writing `Tests: passed` without actual evidence

## Output Checklist

Before finalizing the message, verify:

- the title matches the dominant behavioral change
- the body only describes staged facts
- risks mention major exclusions or compatibility notes when relevant
- tests are real and accurately described
- the `Live Docs` section points to the right files and decision IDs
