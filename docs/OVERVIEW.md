---
memory_layer: base
update_mode: rewrite
role: "Project overview — what this project is, how it's organized, core workflows"
read_when: "entering project, architecture questions"
not_for: "current status (-> STATUS), how to run (-> RUNBOOK), decision rationale (-> DECISIONS)"
---

# Project Overview

## One-Sentence Description

`vibe-memory-system` is a reusable project-memory template and skill bundle for
AI-assisted software, research, and documentation workflows.

## Goals

- Provide a clean installable docs memory template.
- Keep a richer teaching example for users who need explanation.
- Provide optional Agent skills for docs maintenance and commit workflows.
- Make project memory progressive: read only the docs needed for the task.

## Main Workstreams

1. Template design: `docs_template/` and `docs_template_example/`
2. Agent workflow support: `.claude/skills/`
3. Installation and sync tooling: `scripts/`
4. Repository self-memory: `docs/`

## Architecture

```text
Template source
  -> install/sync scripts
  -> target project docs and Agent skills
  -> ongoing maintenance through skills and docs updates
```

## Important Directories

| Path | Role |
|---|---|
| `AGENTS.md` | Copyable Agent entry template for target repositories |
| `docs/` | Memory docs for this repository |
| `docs_template/` | Clean installable target-project docs template |
| `docs_template_example/` | Teaching/reference version with examples |
| `.claude/skills/` | Agent skills shipped with the repository |
| `scripts/` | Install and sync helpers |

## Related Docs

- Current status: `docs/STATUS.md`
- Decisions: `docs/DECISIONS.md`
- Conventions: `docs/CONVENTIONS.md`
- Map: `docs/MAP.md`
- Runbook: `docs/RUNBOOK.md`
