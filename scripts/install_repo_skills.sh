#!/bin/zsh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC_SKILLS_DIR="$REPO_ROOT/codex/skills"
DEST_SKILLS_DIR="$HOME/.codex/skills"

mkdir -p "$DEST_SKILLS_DIR"

for skill_dir in "$SRC_SKILLS_DIR"/*; do
  [[ -d "$skill_dir" ]] || continue
  skill_name="$(basename "$skill_dir")"
  rm -rf "$DEST_SKILLS_DIR/$skill_name"
  mkdir -p "$DEST_SKILLS_DIR/$skill_name"
  rsync -a --exclude '.DS_Store' "$skill_dir/" "$DEST_SKILLS_DIR/$skill_name/"
  echo "Installed skill: $skill_name"
done
