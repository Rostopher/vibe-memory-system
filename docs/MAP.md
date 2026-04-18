---
memory_layer: scaling
update_mode: patch
role: "Navigation map — where concepts, features, and artifacts live in the codebase"
read_when: "locating implementation, tracing artifact origin, feature-to-file mapping"
not_for: "term definitions (-> GLOSSARY), current status (-> STATUS/PROGRESS)"
---

# Map

| Concept / Artifact / Feature | File or Entry Point | Notes |
|---|---|---|
| Clean target-project template | `docs_template/` | Default install source for target `docs/` |
| Teaching example template | `docs_template_example/` | Explanatory version with examples |
| Repository memory | `docs/` | Docs for this repository itself |
| Agent entry template | `AGENTS.md` | Copyable root Agent instructions for target repositories |
| Install template into a project | `scripts/install_to_project.sh` | Copies `AGENTS.md`, clean docs, and skills |
| Sync skills to Codex | `scripts/sync_to_codex.sh` | Copies `.claude/skills/*` to `~/.codex/skills/` |
| Sync skills to Claude Code | `scripts/sync_to_claude.sh` | Copies `.claude/skills/*` to `~/.claude/skills/` |
| Docs maintenance skill | `.claude/skills/update-living-docs/SKILL.md` | Classifies updates into memory layers |
| Memory initialization skill | `.claude/skills/init-memory/SKILL.md` | Scans existing repo and populates empty docs templates; includes placeholder replacement, git reliability checks, and optional read-only sub-agent investigation |
| Research engineering skill | `.claude/skills/research-engineering/SKILL.md` | Optional for Python research workflows |
