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
  mkdir -p "$DEST_SKILLS_DIR/$skill_name"
  cp "$skill_dir/SKILL.md" "$DEST_SKILLS_DIR/$skill_name/SKILL.md"
  echo "Installed skill: $skill_name"
done
