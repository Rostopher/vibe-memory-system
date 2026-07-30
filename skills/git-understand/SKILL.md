---
name: git-understand
description: "Use at the start of a conversation to establish repository context, or when the user asks to review code changes, compare branches, or trace file and line history. Covers three directions: git-scan (repo overview), git-review (understand a concrete change), and git-trace (follow historical evolution)."
---

# Git Understand

Use this skill when the goal is to understand a repository, a change, or the history behind a piece of code.

This skill is not for committing changes. It is for building context before implementation, review, or debugging.

## When To Use

Use this skill when:

- a new conversation starts and you need repository context
- the user asks you to review a PR, MR, branch, or local change
- the user asks who changed a file, line, or behavior
- you need to compare branches or understand recent project direction

## Core Rule

Do not mechanically run every command in this skill.

First identify what question you need to answer, then use the smallest set of Git commands that gives a reliable answer.

## Common Context Scan

Before choosing a direction, run a lightweight context scan when it helps:

```bash
git status --short
git log --oneline -5
git diff --stat
```

Use this scan to answer three quick questions:

- Is the working tree clean or dirty?
- What happened recently?
- How large and how spread out are the current changes?

If there are no local changes, `git diff --stat` may be empty. That is fine.

## Direction A: git-scan

Use this when you need a high-level understanding of the repository.

### Questions To Answer

- What branch am I on, and is the working tree clean?
- What kinds of changes happened recently?
- What does the repository broadly contain?
- Are there project-specific docs that define current phase, decisions, or conventions?

### Suggested Workflow

1. Check current state.

```bash
git status
git branch -v
```

2. Look at recent history.

```bash
git log --oneline -20
```

3. Optionally inspect tracked structure.

```bash
git ls-tree -r --name-only HEAD | head -30
```

4. Optionally inspect project docs that explain the repository.
   - `memory-docs/STATUS.md` for current phase and progress
   - `memory-docs/detail_mem/DECISIONS.md` for major technical decisions
   - `memory-docs/CONVENTIONS.md` for workflow and coding rules

### Expected Output

Summarize:

- current branch and working tree state
- recent development themes
- broad repository structure
- any key living docs the user should know about

## Direction B: git-review

Use this when you need to understand a specific change or review someone else's work.

### Questions To Answer

- What is the review target?
- What is the correct comparison baseline?
- Which files and behaviors changed?
- Is this best described as a feature, bug fix, refactor, cleanup, or docs change?
- What nearby history helps explain the change?

### Choose The Right Review Target

Pick the review mode first:

- Working tree review:
  - `git diff`
  - `git diff --staged`
- Latest commit review:
  - `git show HEAD`
- Branch vs base review:
  - `git log --oneline main..HEAD`
  - `git diff --stat main...HEAD`
  - `git diff main...HEAD`
- Specific commit review:
  - `git show <commit>`

Use the repository's actual base branch if it is not `main`.

### Suggested Workflow

1. Identify the correct baseline.
2. Inspect change shape first.

```bash
git diff --stat
git diff --name-only
```

3. Inspect the detailed patch.

```bash
git diff
git show HEAD
```

4. Add local historical context when needed.

```bash
git log --oneline -5 -- <path>
git blame <path>
```

### Expected Output

Summarize:

- what changed
- which files matter most
- the likely intent of the change
- whether the change looks self-contained or part of a longer line of work

## Direction C: git-trace

Use this when you need to trace the origin or evolution of a file, function, or specific lines.

### Questions To Answer

- Who last changed this code?
- Which commit introduced or reshaped it?
- How did this file or behavior evolve over time?
- Does the visible line history reflect the real design history, or only the last touch?

### Suggested Workflow

1. Start with file history.

```bash
git log --oneline -- <path>
```

2. Inspect important commits directly.

```bash
git show <commit>
```

3. Use line-level attribution when needed.

```bash
git blame -L <start>,<end> <path>
```

4. Follow longer evolution when needed.

```bash
git log -p --follow <path>
```

### Trace Rule

`git blame` identifies the most recent commit that touched a line. It does not always explain the original design intent.

If you need to understand why the code looks the way it does, continue from `blame` into `git show` and broader file history.

### Expected Output

Summarize:

- who last changed the code
- which commit matters most
- what that commit says or shows
- whether further history changes the interpretation

## Branch Comparison

When the user asks about differences between branches, treat that as a review task with an explicit baseline.

Useful commands:

```bash
git log --oneline base..feature
git diff --stat base...feature
git diff base...feature
```

Use `...` when you want the diff from the merge base to the feature branch. Use `..` when you want commit range semantics.

## Living Docs Hint

If the repository uses living docs, mention them when they add context:

- `memory-docs/STATUS.md`
- `memory-docs/detail_mem/DECISIONS.md`
- `memory-docs/CONVENTIONS.md`

Use them to interpret project state and rules, not as a replacement for Git history.

## Notes

- Start broad, then narrow.
- Prefer summaries over raw command dumps.
- Answer the user's actual question before expanding scope.
- Use Git to establish evidence, then explain the conclusion in plain language.
