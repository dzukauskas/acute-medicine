#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC_SKILLS_DIR="$REPO_ROOT/codex/skills"
DEST_SKILLS_DIR="$HOME/.codex/skills"

if ! command -v rsync >/dev/null 2>&1; then
  echo "Required command not found: rsync. Install rsync before running scripts/install_repo_skills.sh." >&2
  exit 1
fi

if [[ ! -d "$SRC_SKILLS_DIR" ]]; then
  echo "Repo skills directory not found: $SRC_SKILLS_DIR" >&2
  exit 1
fi

mkdir -p "$DEST_SKILLS_DIR"

for skill_dir in "$SRC_SKILLS_DIR"/*; do
  [[ -d "$skill_dir" ]] || continue
  skill_name="$(basename "$skill_dir")"
  rm -rf "$DEST_SKILLS_DIR/$skill_name"
  mkdir -p "$DEST_SKILLS_DIR/$skill_name"
  rsync -a --exclude '.DS_Store' "$skill_dir/" "$DEST_SKILLS_DIR/$skill_name/"
  echo "Installed skill: $skill_name"
done
