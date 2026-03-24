#!/bin/zsh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC_DIR="$REPO_ROOT/books/acute-medicine/lt"
DEST_DIR="${1:-/Users/dzukauskas/Library/Mobile Documents/iCloud~md~obsidian/Documents/PARAMEDIKAS/Acute Medicine}"

mkdir -p "$DEST_DIR"

# Mirror only the user-facing study assets needed by Obsidian while preserving
# the chapters/figures directory structure and relative image links.
/usr/bin/rsync \
  -a \
  --delete \
  --prune-empty-dirs \
  --exclude '.DS_Store' \
  --include '*/' \
  --include '*.md' \
  --include '*.png' \
  --exclude '*' \
  "$SRC_DIR/" \
  "$DEST_DIR/"
