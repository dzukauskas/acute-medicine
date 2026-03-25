#!/bin/zsh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

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
"$REPO_ROOT/.venv/bin/python" -m playwright install chromium
"$REPO_ROOT/.venv/bin/python" -c "import fitz"

"$REPO_ROOT/scripts/install_repo_skills.sh"
"$REPO_ROOT/scripts/setup_codex_mcp.sh"

echo
echo "Bootstrap complete."
echo "Next manual steps:"
echo "  1. Run: codex login"
echo "  2. Run: gh auth login"
echo "  3. Open Whimsical desktop and sign in."
echo "  4. Run: .venv/bin/python scripts/render_whimsical_figure.py --login"
echo "  5. Bootstrap a concrete book workspace with scripts/bootstrap_book_from_pdf.py"
