---
name: init-memory
description: Scan an existing repository and populate the docs/ memory templates with real project content. Use when vibe-memory-system docs have just been installed into a repository that already has code, history, and conventions.
---

# Init Memory — Repository Memory Initialization

Scan an existing repository and populate the `docs/` memory templates with real project content.

This skill is designed for the "day one" scenario: the user has just installed the vibe-memory-system docs templates into a repository that already has code, git history, and established conventions. The docs files contain only placeholders. This skill fills them with real content extracted from the repository.

## When To Use

Use this skill when:

- the user says "初始化文档" / "init memory" / "init docs" / "scan and fill docs"
- the user says "我刚装了 docs 模板，帮我填充"
- the user invokes `$init-memory`
- docs/ exists with template placeholders but no real content

Do not use this skill when:

- docs/ already contains substantial real content (use `$update-living-docs` instead)
- the user wants to create a new docs/ from scratch (use `install_to_project.sh` first)
- the user only wants to update one specific doc file

## Core Rules

1. **Evidence over invention.** Every claim written into docs must trace back to something observable in the repo: code, config, git history, README, or user confirmation. Never fabricate content.
2. **Ask when you cannot infer.** If important information cannot be extracted from code, ask the user directly. Do not guess project goals, team conventions, or historical decisions.
3. **Show before write.** Generate each doc file's draft and present it to the user for confirmation before writing. Never batch-write all docs silently.
4. **Token economy.** Do not read every source file. Use directory structure, config files, entry points, and git history to build understanding. Only deep-read files when necessary.
5. **Respect frontmatter.** Each template file has a YAML frontmatter with `update_mode`. Follow it: `rewrite` files get full content, `patch` files get structured entries, `append` files get new entries only.
6. **Initialization placeholder exception.** During first-time initialization only, placeholder content may be replaced even in `append` or `patch` files. Replace fake placeholder entries such as `DEC-001: <title>` instead of appending real content after them. After initialization, return to the normal `update_mode` semantics.
7. **Git is evidence, not truth.** Git history can describe observed activity, but it cannot prove current priorities, blockers, roadmap, branch strategy, or project intent unless those are explicit in README, issues, roadmap files, CI config, or user confirmation.

## Workflow

### Phase 0: Pre-flight Check

Before starting, verify the environment:

1. Confirm `docs/` directory exists at the repository root.
2. Confirm `docs/MEMORY_MANIFEST.yml` exists (this confirms vibe-memory-system templates are installed).
3. Scan each doc file to classify its state:
   - **Empty template**: contains only frontmatter and placeholder tokens like `<project-name>`, `<goal>`, `<path>`.
   - **Partially filled**: has some real content mixed with placeholders.
   - **Already filled**: has substantial real content with no placeholders.
4. Report the scan result to the user. For partially or fully filled files, ask whether to **skip**, **overwrite**, or **merge** (keep existing content and fill gaps).

If `docs/` does not exist, stop and tell the user to run `install_to_project.sh` first.

### Phase 1: Repository Scan (Read-Only)

Collect information systematically. Do not write any docs files in this phase.

#### 1.1 Project Identity

Read these files (if they exist):

- `README.md` or `README.rst` — project description, goals, getting started
- Package manifest: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`, `Gemfile`, `composer.json`
- `LICENSE` — license type
- `.env.example` or `.env.template` — environment variables

Extract: project name, language, framework, version, license, described purpose.

#### 1.2 Directory Structure

Generate a directory tree (depth 3-4 levels, excluding `node_modules/`, `.git/`, `__pycache__/`, `target/`, `build/`, `dist/`, `.venv/`, `venv/`).

Identify: source directories, test directories, config directories, documentation directories, script directories, output/artifact directories.

#### 1.3 Git Archaeology

Run these git commands if the repository is a git repo:

```bash
# Working tree state
git status --short

# Recent activity
git log --oneline -30

# Project origin
git log --reverse --oneline -5

# Branches
git branch -a

# Contributors
git shortlog -sn --all | head -20

# Recent hotspots (last 30 days)
git log --since="30 days ago" --name-only --format="commit %h %cs %s"

# Project age
git log --reverse --format="%ai" | head -1

# Latest commit date
git log -1 --format="%ai"
```

Assess git reliability before using git-derived claims:

- **High confidence**: git exists, recent commits match current files, and working tree is mostly clean.
- **Medium confidence**: git exists, but activity is old, sparse, or only loosely matches current files.
- **Low confidence**: no git repo, no commits, very old history, many uncommitted/untracked files, or a broad dirty working tree.

If git reliability is low, do not rely on git to populate `STATUS.md` or `PROGRESS.md` beyond "observed historical activity." Ask the user for current focus, project stage, and module status, or mark those fields as `Unknown / needs user confirmation`.

Extract only what git can support: project age, active contributors, observed recent activity, and path hotspots. Treat branch strategy and commit style as explicit only if they are documented or consistently obvious; otherwise mark them unknown.

#### 1.4 Configuration & Convention Scan

Search for these configuration files:

- **Linting**: `.eslintrc*`, `.prettierrc*`, `ruff.toml`, `pyproject.toml` `[tool.ruff]`/`[tool.black]`, `.golangci.yml`, `.rubocop.yml`, `biome.json`
- **Editor**: `.editorconfig`
- **CI/CD**: `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`
- **Container**: `Dockerfile`, `docker-compose.yml`
- **Build**: `Makefile`, `justfile`, `Taskfile.yml`, `nx.json`, `turbo.json`
- **Testing**: `jest.config.*`, `vitest.config.*`, `pytest.ini`, `conftest.py`, `.mocharc.*`

Extract: code style rules, formatting rules, testing framework, CI pipeline structure, build commands.

#### 1.5 Code Pattern Scan

Perform targeted scans:

```bash
# TODO/FIXME/HACK density
rg -n "TODO|FIXME|HACK|XXX" \
  -g '*.py' -g '*.ts' -g '*.js' -g '*.tsx' -g '*.jsx' \
  -g '*.rs' -g '*.go' -g '*.java' -g '*.rb' \
  -g '!node_modules/**' -g '!dist/**' -g '!build/**' -g '!target/**' \
  | wc -l

# Entry points (language-dependent)
# Python: main.py, __main__.py, app.py, manage.py, cli.py
# JS/TS: index.ts, main.ts, app.ts, server.ts
# Go: cmd/*/main.go, main.go
# Rust: src/main.rs, src/lib.rs

# Domain-specific types and interfaces (top-level class/interface/struct names)
```

Extract: entry points, key domain types, code health indicators.

### Phase 1.5: Scan Summary Confirmation — MANDATORY STOP

**You must stop here and present the scan summary to the user before proceeding.**

Present a structured summary:

```
## Scan Summary

**Project**: <name> (<language> / <framework>)
**Age**: <first commit date> → <latest commit date>
**Contributors**: <count> (<top contributors>)
**License**: <type>

### Understanding
<2-3 sentences describing what this project does, based on README and code structure>

### Tech Stack
- Language: ...
- Framework: ...
- Build: ...
- Test: ...
- CI: ...

### Key Modules
| Directory | Likely Role |
|-----------|-------------|
| ... | ... |

### Detected Conventions
- Commit style: ...
- Branch strategy: ...
- Code style: ...

### Git Reliability
- Confidence: high / medium / low
- Reason: <clean working tree, stale history, many uncommitted files, no git repo, etc.>
- Safe uses: <what git evidence can support>

### Information Gaps
- <things you could not determine from the scan>
```

Ask the user:

1. **Is the project understanding correct?** If not, what is wrong?
2. **Are there important aspects not captured?** (e.g., the project is a monorepo, has special deployment requirements, etc.)
3. For anything listed under "Information Gaps": ask specific questions.

If the user does not know an answer or does not want to decide immediately, offer three options:

- Mark the field as `Unknown / needs user confirmation`.
- Continue with a low-confidence draft and label the claim clearly.
- If the runtime supports sub-agents, delegate a focused read-only investigation for that specific file or question.

Wait for user confirmation before proceeding to Phase 2.

### Phase 2: Generate Docs (One File At A Time)

Process each doc file in the following order. This order is intentional — later files depend on context established by earlier ones.

For each file:

1. Read the template file's frontmatter to confirm `update_mode` and `role`.
2. Generate a complete draft based on scan data and user-confirmed understanding.
3. If you encounter information gaps, ask the user (max 3 questions per file), or offer to delegate one focused read-only sub-agent investigation if supported.
4. Present the draft to the user for review.
5. Wait for the user to say "ok" / "继续" / "写入" or provide corrections.
6. Write the confirmed content to the file.
7. Announce completion and move to the next file.

### Optional Sub-Agent Investigation

Use this only when the runtime supports sub-agents and the user agrees to delegate uncertainty instead of answering manually.

Rules:

- One sub-agent owns one doc file or one narrow uncertainty. Do not assign overlapping scopes.
- Sub-agents are read-only researchers. They must not edit docs or source files.
- Give each sub-agent a bounded prompt: target doc/question, files to inspect first, forbidden areas, and expected output.
- Expected output must include: findings, evidence paths, confidence, and remaining unknowns.
- The main Agent remains responsible for final synthesis and writing. Do not paste sub-agent output into docs without checking it against the memory layer's role.

Example prompt:

```text
Investigate RUNBOOK.md for this repository. Read README, package manifests,
Makefile/justfile/package scripts, CI config, and env examples. Do not edit files.
Return setup commands, dev/test/build commands, output locations, evidence paths,
confidence for each claim, and remaining unknowns.
```

#### File Order and Strategy

---

#### 2.1 OVERVIEW.md (`rewrite`)

**Priority: FIRST** — establishes project identity that all other docs reference.

**Auto-fill from scan:**
- Project name and one-liner (from README / package manifest)
- Goals (from README)
- Architecture / data flow (from directory structure and entry points)
- Important directories (from directory tree analysis)
- Tech stack (from package manifest and config files)

**Ask the user if not inferable:**
- "What is the one-sentence goal of this project?" (if README is absent or vague)
- "Who is the target audience?" (if not clear)
- "What stage is this project in?" (prototype / active development / maintenance / archived)

**Output format:** Follow the template's heading structure exactly:
`One-Sentence Description` → `Goals` → `Main Workstreams` → `Architecture` → `Important Directories` → `Tech Stack` → `Related Docs`

---

#### 2.2 MAP.md (`patch`)

**Priority: SECOND** — highest automation confidence, maps the entire codebase.

**Auto-fill from scan:**
- Every significant directory and file mapped to its role
- Entry points identified
- Module boundaries and relationships (if inferable from imports or config)
- Test file ↔ source file correspondence

**Ask the user if not inferable:**
- Rarely needed for this file. If some directories are ambiguous, ask.

**Output format:** Maintain the table structure:
`Concept / Artifact / Feature | File or Entry Point | Inputs / Outputs | Notes`

---

#### 2.3 CONVENTIONS.md (`patch`)

**Auto-fill from scan:**
- Code style rules (from linter configs)
- Formatting rules (from prettier/black/rustfmt config)
- Testing conventions (from test framework config and existing test patterns)
- File naming patterns (observed from the codebase)
- Import ordering (from linter config or observed patterns)

**Ask the user:**
- "What is your branch strategy?" (trunk-based / git-flow / other)
- "What is your commit style?" (conventional commits / free-form / other)
- "Are there unwritten rules the team follows that aren't in config files?"

---

#### 2.4 GLOSSARY.md (`patch`)

**Auto-fill from scan:**
- Domain-specific terms from README
- Key class/type/interface names that represent domain concepts
- Abbreviations used in the codebase
- Configuration key names that are non-obvious

**Filter out:** Generic programming terms (e.g., "controller", "service", "util") unless they have project-specific meanings.

**Ask the user:**
- "Are there domain terms that have specific meanings in this project?" (especially for domain-driven projects)

---

#### 2.5 PROGRESS.md (`patch`)

**Auto-fill from scan:**
- One row per significant module/feature (derived from MAP.md)
- Status estimation based on:
  - Git activity recency (last commit date per directory) only when git reliability is medium or high
  - Test coverage presence
  - TODO/FIXME density
  - File count and maturity signals

**Status categories:** `done` / `active` / `planned` / `stale` / `unknown`

If git reliability is low or the working tree is broadly dirty, avoid assigning `done`, `active`, or `stale` from git history alone. Use `unknown` and ask the user, or delegate a focused sub-agent investigation per module/file group.

**Ask the user:**
- "Are there modules listed here whose status is wrong?" (show the draft and ask for corrections)

---

#### 2.6 STATUS.md (`rewrite`)

**Auto-fill from scan:**
- Current focus only from README/roadmap/issue tracker/current branch name/user confirmation. If unavailable, write `Unknown / needs user confirmation`.
- Observed recent activity from recent commits, but label it as observation, not current priority.
- Recent completions only when commits, changelog, release notes, or README explicitly support them.
- Blockers or known issues only from explicit issue trackers, roadmap docs, TODO comments with clear context, or user confirmation.
- Next priorities only from roadmap docs, issue trackers, active planning docs, or user confirmation. Do not infer priorities from branch activity alone.

**Constraint:** Keep to 3-5 bullet points as per the template's design.

**Ask the user:**
- "What are you currently focused on?"
- "Are there any blockers or known issues I should capture?"

---

#### 2.7 RUNBOOK.md (`rewrite`)

**Auto-fill from scan:**
- Prerequisites (from package manifest dependencies, Dockerfile, CI config)
- Setup commands (from README's "Getting Started", Makefile targets)
- Dev commands (from Makefile, package.json scripts, justfile)
- Test commands (from test framework config, CI pipeline)
- Build/deploy commands (from CI/CD config, Dockerfile)
- Output locations (from build config, output directories)

**Ask the user:**
- "Are there any special local setup steps not captured in config files?"
- "What environment variables are required?" (if no `.env.example` exists)

---

#### 2.8 DECISIONS.md (`append`)

**Strategy:** This file records historical decisions that cannot be extracted from code. Do not fabricate decision history.

During initialization, apply the placeholder exception: if the template contains fake placeholder entries such as `DEC-001: <title>`, replace that placeholder block with real captured decisions or with a short comment saying no historical decisions were captured. Do not append real decisions after placeholder decisions.

**Auto-fill:** Very limited. Can only infer:
- Technology choices (why this language/framework — but the "why" requires human input)
- Architecture patterns visible in code (but the rationale requires human input)

**Ask the user:**
- "Do you remember key technical decisions made during this project? For example:"
  - "Why did you choose <framework> over alternatives?"
  - "Were there any architecture decisions you debated?"
  - "Were there approaches you tried and rejected?"
- If the user can recall decisions, record each as a `DEC-xxx` entry with date, context, decision, and rationale.
- If the user says they don't remember, write a minimal template with only the heading structure and a note: `<!-- No historical decisions captured during initialization. Add entries as new decisions are made. -->`

---

#### 2.9 docs/README.md (`patch`)

**Auto-fill:** Update the routing table to reflect which files have been populated and their current state.

**This file is generated last** because it summarizes the state of all other doc files.

---

### Phase 3: Wrap-Up

After all files are written:

1. Update `MEMORY_MANIFEST.yml` if any structural changes were made (e.g., custom MAP file names).

2. Present a completion report:

```
## Initialization Complete

| File | Status | Confidence | Needs Manual Review |
|------|--------|------------|---------------------|
| OVERVIEW.md | ✅ Filled | ⭐⭐⭐⭐ | — |
| MAP.md | ✅ Filled | ⭐⭐⭐⭐⭐ | — |
| CONVENTIONS.md | ✅ Filled | ⭐⭐⭐ | Unwritten team rules |
| GLOSSARY.md | ✅ Filled | ⭐⭐⭐ | Domain terms |
| PROGRESS.md | ✅ Filled | ⭐⭐⭐ | Status accuracy |
| STATUS.md | ✅ Filled | ⭐⭐⭐⭐ | — |
| RUNBOOK.md | ✅ Filled | ⭐⭐⭐⭐ | Local setup steps |
| DECISIONS.md | ⚠️ Partial | ⭐⭐ | Historical decisions |
| docs/README.md | ✅ Updated | ⭐⭐⭐⭐⭐ | — |

### Suggested Next Steps

1. Review each doc file and correct any inaccuracies.
2. Add historical decisions to DECISIONS.md as you recall them.
3. Start normal workflow: do work → $update-living-docs → $commit-pipeline
```

## Adaptation Rules

### Language Detection

- If the project's README and code comments are primarily in Chinese, write doc content in Chinese.
- If the project is primarily in English, write doc content in English.
- If mixed, follow the language of the README.
- The doc file headings and frontmatter always remain in English (matching the template).

### Project Type Adaptation

Different project types require different scanning emphases:

**Web Application (JS/TS)**
- Emphasize: routes, components, state management, API endpoints
- Check: `package.json` scripts, `next.config.*`, `vite.config.*`, `webpack.config.*`
- MAP focus: feature → component → API mapping

**Python Data/Research Project**
- Emphasize: data pipeline, analysis scripts, output artifacts, notebooks
- Check: `pyproject.toml`, `requirements.txt`, `setup.py`, data directories
- MAP focus: analysis → script → data input → output artifact mapping

**Backend API (any language)**
- Emphasize: API routes, middleware, database schema, auth
- Check: API definition files (OpenAPI, GraphQL schema), migration files
- MAP focus: endpoint → handler → service → model mapping

**CLI Tool**
- Emphasize: commands, flags, config file format
- Check: command registration, help text, man pages
- MAP focus: command → handler → config mapping

**Library/SDK**
- Emphasize: public API surface, examples, versioning
- Check: exports, published types, changelog
- MAP focus: public API → implementation mapping

**Monorepo**
- Treat each package/workspace as a mini-project within the top-level overview
- MAP should clearly delineate package boundaries
- PROGRESS tracks per-package status

### Large Repository Handling

For repositories with more than 500 files:

- Use `git ls-tree` and directory listing instead of full tree traversal
- Focus scanning on: top-level structure, src/ directories, config files, and entry points
- Skip: vendored code, generated files, large data files, build artifacts
- Explicitly note which areas were not deeply scanned in the completion report

## Error Handling

- If `docs/` does not exist → stop, instruct user to run `install_to_project.sh`
- If `docs/MEMORY_MANIFEST.yml` is missing → warn that templates may not be standard, proceed with caution
- If git is not initialized → skip Phase 1.3 entirely, note reduced confidence in STATUS and PROGRESS
- If README is missing → ask user for project description directly
- If the project is empty (no source code) → abort and tell user to init-memory after writing some code
- If a doc file write fails → report the error, continue with remaining files

## What This Skill Does NOT Do

- Does not create the `docs/` directory or install templates (use `install_to_project.sh`)
- Does not update docs after ongoing work (use `$update-living-docs`)
- Does not commit changes (use `$commit-pipeline`)
- Does not modify any source code
- Does not read `.env` files or files likely containing secrets
