---
name: commit-pipeline
description: "Orchestrate a complete commit flow: use commit-planner to define batches, stage the selected batch, generate the message with commit-messages, and execute git commit safely."
---

# Commit Pipeline

Run a full `plan -> stage -> message -> commit` flow.
Use this skill when the user wants to finish commits end-to-end instead of only planning or only writing messages.

## Skills Used

- `$commit-planner`: define coherent commit batches
- `$commit-messages`: draft a structured commit message for the staged batch

## Core Rule

Never commit files that are outside the selected batch.
If staging state does not match the selected batch, fix staging first before generating the message.

## Workflow

1. Capture working tree state.
   - `git status --short`
   - `git diff --name-only`
   - `git diff --staged --name-only`
2. Run `$commit-planner`.
   - Produce batch options with goal, file list, and type/scope.
   - Select one batch as the next commit.
3. Decide whether living docs belong in this batch.
   - Think in terms of the repository's memory system, not just a few default docs.
   - Framework memory may include `memory-docs/OVERVIEW.md`, `STATUS.md`, `HISTORY.md`, `CONVENTIONS.md`, and `GLOSSARY.md`.
   - Routing memory is `memory-docs/DIRS.md`; detailed memory includes `memory-docs/detail_mem/MAP.md`, `PROGRESS.md`, and `DECISIONS.md`.
   - Session and historical memory usually do not belong in the same commit by default, but include relevant `memory-docs/SHORT_MEMORY/...` or `memory-docs/archive/...` files when the batch intentionally captures handoff context or a retrospective.
   - Follow the repository's docs conventions and keep claims aligned with implemented reality.
   - Use `$update-living-docs` when it helps, but only for docs that are genuinely relevant to the selected batch.
   - If docs should be separate, make that an explicit follow-up batch instead of silently deferring them.
4. Stage only the selected batch.
   - If index is dirty with unrelated files, unstage first: `git restore --staged <path>`.
   - Stage selected files only, including any relevant living-doc updates: `git add <paths...>`.
   - Verify: `git diff --staged --name-only` must match the chosen batch.
5. Run `$commit-messages` on staged changes.
   - Generate title + `Why`/`What`/`Risk`/`Tests`/`Live Docs`.
   - Ensure claim discipline: staged facts only.
6. Commit with the generated message.
   - `git commit -m "<title>" -m "Why:\n- ...\n\nWhat:\n- ...\n\nRisk:\n- ...\n\nTests:\n- ...\n\nLive Docs:\n- ..."`
7. Verify commit result.
   - `git show --stat --name-only --oneline -1`
   - Confirm no accidental files were included.
8. Repeat from step 2 for the next batch until done.

## Output Format

Use this structure when reporting execution:

```text
Pipeline Run:
- Selected batch: ...
- Staged files: ...
- Commit title: ...
- Commit hash: ...
- Remaining changes: ...
```

## Safety Checks

- Stop if `git diff --staged --name-only` includes non-batch files.
- Stop if message claims behavior not present in staged diff.
- Do not auto-add untracked files unless they are explicitly part of the selected batch.

## Bad Patterns

- running `$commit-messages` before staging is finalized
- committing all changes with `git add .` in a mixed working tree
- combining unrelated hygiene and feature slices into one commit without rationale

## Output Checklist

Before finishing, verify:

- each commit corresponds to one batch from `$commit-planner`
- staged files exactly match the batch before message generation
- commit message comes from staged reality
- commit hash and remaining work are reported
