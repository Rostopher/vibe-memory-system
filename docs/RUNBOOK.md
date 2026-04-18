---
memory_layer: base
update_mode: rewrite
role: "Operations manual — how to run, debug, and find outputs, from start to finish"
read_when: "running commands, debugging, looking for outputs, reproducing results"
not_for: "why it works this way (-> DECISIONS), rules to follow (-> CONVENTIONS)"
---

# Runbook

## Validate Shell Scripts

```bash
bash -n scripts/install_to_project.sh
bash -n scripts/sync_to_codex.sh
bash -n scripts/sync_to_claude.sh
```

## Smoke Test Installation

```bash
tmpdir="$(mktemp -d)"
mkdir -p "$tmpdir/target"
bash scripts/install_to_project.sh "$tmpdir/target"
test -f "$tmpdir/target/AGENTS.md"
find "$tmpdir/target" -maxdepth 3 -type f | sort
find "$tmpdir/target" -name .DS_Store -print
```

## Sync Skills

```bash
bash scripts/sync_to_codex.sh --force
bash scripts/sync_to_claude.sh --force
```

Use sync commands only when you intentionally want to overwrite global skill
copies.

## Release Checklist

- No personal absolute paths in public docs, scripts, or skills.
- `README.md` matches install script behavior.
- `docs_template/MEMORY_MANIFEST.yml` matches the template files.
- `docs/MEMORY_MANIFEST.yml` matches repository docs.
