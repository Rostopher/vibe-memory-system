#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  install_to_project.sh TARGET_PROJECT_PATH [--force]

What it does:
  - installs AGENTS.md into TARGET_PROJECT_PATH/AGENTS.md
  - installs docs_template/ into TARGET_PROJECT_PATH/docs
  - installs .claude/skills/ into TARGET_PROJECT_PATH/.claude/skills

Default behavior:
  - refuses to overwrite existing target paths unless --force is provided
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

FORCE=0
TARGET=""

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
      if [[ -z "$TARGET" ]]; then
        TARGET="$arg"
      else
        echo "Unexpected argument: $arg" >&2
        usage
        exit 1
      fi
      ;;
  esac
done

if [[ -z "$TARGET" ]]; then
  usage
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

TARGET="$(cd "$TARGET" && pwd)"

if [[ ! -d "$TARGET" ]]; then
  echo "Target project path does not exist: $TARGET" >&2
  exit 1
fi

install_path() {
  local src="$1"
  local dst="$2"

  if [[ -e "$dst" && "$FORCE" -ne 1 ]]; then
    echo "Refusing to overwrite existing path without --force: $dst" >&2
    exit 1
  fi

  mkdir -p "$(dirname "$dst")"
  rm -rf "$dst"
  cp -R "$src" "$dst"
  find "$dst" -name .DS_Store -type f -delete
}

echo "Installing vibe-memory-system into: $TARGET"

install_path "${REPO_ROOT}/AGENTS.md" "${TARGET}/AGENTS.md"
install_path "${REPO_ROOT}/docs_template" "${TARGET}/docs"
mkdir -p "${TARGET}/.claude"
install_path "${REPO_ROOT}/.claude/skills" "${TARGET}/.claude/skills"

echo
echo "Installed:"
echo "- ${TARGET}/AGENTS.md"
echo "- ${TARGET}/docs"
echo "- ${TARGET}/.claude/skills"
echo
echo "Next step:"
echo "- fill the placeholders in ${TARGET}/AGENTS.md and ${TARGET}/docs before treating them as project facts"
