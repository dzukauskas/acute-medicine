#!/bin/zsh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OBSIDIAN_DEST="${1:-}"

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew is not installed."
  echo "Install it first from https://brew.sh and then rerun this script."
  exit 1
fi

brew bundle --file="$REPO_ROOT/Brewfile"

if ! command -v codex >/dev/null 2>&1; then
  npm install -g @openai/codex
fi

if ! command -v pdf-reader-mcp >/dev/null 2>&1; then
  npm install -g @sylphx/pdf-reader-mcp
fi

python3 -m venv "$REPO_ROOT/.venv"
"$REPO_ROOT/.venv/bin/pip" install --upgrade pip
"$REPO_ROOT/.venv/bin/pip" install -r "$REPO_ROOT/requirements.txt"

"$REPO_ROOT/scripts/install_repo_skills.sh"
"$REPO_ROOT/scripts/setup_codex_mcp.sh"

if [[ -n "$OBSIDIAN_DEST" ]]; then
  "$REPO_ROOT/scripts/install_obsidian_sync_agent.sh" "$OBSIDIAN_DEST"
else
  echo
  echo "Obsidian sync agent not installed yet."
  echo "Run scripts/install_obsidian_sync_agent.sh with your vault destination path when ready."
fi

echo
echo "Bootstrap complete."
echo "Next manual steps:"
echo "  1. Run: codex login"
echo "  2. Run: gh auth login"
echo "  3. Open Whimsical desktop and sign in."
