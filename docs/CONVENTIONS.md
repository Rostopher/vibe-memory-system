---
memory_layer: base
update_mode: patch
role: "Hard rules and contracts — what must be followed, not why (why -> DECISIONS)"
read_when: "before editing code, style/contract questions, checking naming rules"
not_for: "decision rationale (-> DECISIONS), how to run (-> RUNBOOK), one-off preferences"
---

# Conventions

## Public Safety

- Do not commit private machine paths, global virtualenv paths, secrets, tokens,
  or account identifiers.
- Use placeholders such as `<project-root>` and portable paths such as `.venv`.

## Template Rules

- Keep root `AGENTS.md` usable as a copyable Agent entry template for target
  repositories.
- Put repository-specific maintenance rules in `docs/`, not as hard-coded
  assumptions inside the reusable `AGENTS.md` template.
- Keep `docs_template/` concise and installable.
- Keep explanatory examples in `docs_template_example/`.
- Keep manifests synchronized with their docs tree.
- Do not let template placeholders read like completed project facts.

## Script Rules

- Install scripts should refuse overwrites unless `--force` is passed.
- Default install behavior should be reflected in `README.md`.
- Avoid machine-specific assumptions in script output.

## Skills Rules

- Skill-specific workflows belong in each `SKILL.md`.
- Repository-level Agent files may mention when to use skills, but should not
  duplicate full skill instructions.
