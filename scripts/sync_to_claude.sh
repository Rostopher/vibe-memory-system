#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  sync_to_claude.sh [--force]

What it does:
  - syncs .claude/skills/* from this repo into ~/.claude/skills/

Default behavior:
  - refuses to overwrite existing skill directories unless --force is provided
EOF
}

FORCE=0

for arg in "$@"; do
  case "$arg" in
    --force)
      FORCE=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unexpected argument: $arg" >&2
      usage
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SRC_DIR="${REPO_ROOT}/.claude/skills"
DST_DIR="${HOME}/.claude/skills"

mkdir -p "$DST_DIR"

for skill_dir in "${SRC_DIR}"/*; do
  [[ -d "$skill_dir" ]] || continue
  skill_name="$(basename "$skill_dir")"
  dst="${DST_DIR}/${skill_name}"

  if [[ -e "$dst" && "$FORCE" -ne 1 ]]; then
    echo "Refusing to overwrite existing Claude Code skill without --force: $dst" >&2
    exit 1
  fi

  rm -rf "$dst"
  cp -R "$skill_dir" "$dst"
  find "$dst" -name .DS_Store -type f -delete
  echo "Synced to Claude Code: ${skill_name}"
done

echo
echo "Done. Global Claude Code skills are now synced from:"
echo "- ${SRC_DIR}"
echo "to:"
echo "- ${DST_DIR}"
