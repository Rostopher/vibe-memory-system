# Commit Batching Guide

Use this guide when a repository has a mixed working tree and Codex needs to decide how many commits to make.

## Primary Goal

Create commit batches that are:

- behaviorally coherent
- reviewable
- easy to describe
- easy to hand off to a commit-message generator

## Typical Batch Types

- feature implementation
- supporting tests
- live-doc sync
- config or ignore hygiene
- refactor-only cleanup
- generated-file cleanup

## Preferred Strategy

1. Isolate independent hygiene changes first.
2. Identify the largest coherent feature slice.
3. Attach matching tests unless they clearly need a separate follow-up.
4. Decide whether docs belong with the feature or as a follow-up docs batch.
5. Leave future-phase files out of the current batch.

## Docs Heuristics

- If `memory-docs/detail_mem/DECISIONS.md` records a decision implemented by the code, reference that decision in the feature batch.
- If `memory-docs/STATUS.md` marks the current feature as done or in-progress, use it to frame whether the batch is complete or partial.
- If `memory-docs/CONVENTIONS.md` changes because of the code, consider whether that should be in the same batch or a docs/rules batch.

## When to Split Docs

Split docs into their own batch when:

- the code is ready but docs are still being refined
- the docs update spans multiple already-landed commits
- the code batch is cleaner without the docs churn

Keep docs with code when:

- the docs define the new contract or workflow
- the repository treats living docs as part of the feature definition of done
- the docs are short and tightly coupled to the feature

## Warning Signs

- staged files mention a new feature, but the matching test is unstaged
- a new model file exists, but only the caller is staged
- docs describe multiple future tools, but code implements only one subset
- `.gitignore` or formatting noise is mixed into a feature batch

## Final Hand-off

After selecting a batch, pass only that batch to `$commit-messages`.
This keeps commit messages accurate and avoids accidental claims about unstaged work.
