#!/bin/zsh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_BIN="$REPO_ROOT/.venv/bin/python3"
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="$(command -v python3 || true)"
fi

BOOK_ROOT_REL="${MEDBOOK_ROOT:-}"
DEST_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --book-root)
      BOOK_ROOT_REL="$2"
      shift 2
      ;;
    --dest)
      DEST_DIR="$2"
      shift 2
      ;;
    *)
      if [[ -z "$DEST_DIR" ]]; then
        DEST_DIR="$1"
        shift
      else
        echo "Unexpected argument: $1" >&2
        exit 1
      fi
      ;;
  esac
done

if [[ -z "$BOOK_ROOT_REL" ]]; then
  echo "Set MEDBOOK_ROOT or pass --book-root books/<slug>." >&2
  exit 1
fi

if [[ "$BOOK_ROOT_REL" = /* ]]; then
  BOOK_ROOT="$BOOK_ROOT_REL"
else
  BOOK_ROOT="$REPO_ROOT/$BOOK_ROOT_REL"
fi
SRC_DIR="$BOOK_ROOT/lt"
README_PATH="$BOOK_ROOT/README.md"

if [[ ! -d "$SRC_DIR" ]]; then
  echo "Source directory not found: $SRC_DIR" >&2
  exit 1
fi
if [[ ! -f "$README_PATH" ]]; then
  echo "Book README not found: $README_PATH" >&2
  exit 1
fi
if [[ -z "$PYTHON_BIN" ]]; then
  echo "Python interpreter not found." >&2
  exit 1
fi

CONFIG_VALUES="$("$PYTHON_BIN" - "$REPO_ROOT" "$BOOK_ROOT" <<'PY'
import sys
from pathlib import Path

repo_root = Path(sys.argv[1])
book_root = Path(sys.argv[2])
sys.path.insert(0, str(repo_root / "scripts"))

from book_workflow_support import book_title_from_readme, default_obsidian_dest

print(book_title_from_readme(book_root))
print(default_obsidian_dest(book_root))
PY
)"

BOOK_TITLE="$(printf '%s\n' "$CONFIG_VALUES" | sed -n '1p')"
DEFAULT_DEST="$(printf '%s\n' "$CONFIG_VALUES" | sed -n '2p')"

DEST_DIR="${OBSIDIAN_BOOK_DEST:-${DEST_DIR:-$DEFAULT_DEST}}"
DEST_DIR="$("$PYTHON_BIN" - "$REPO_ROOT" "$BOOK_ROOT" "$DEST_DIR" "$PWD" <<'PY'
import sys
from pathlib import Path

repo_root = Path(sys.argv[1])
book_root = Path(sys.argv[2])
dest_dir = sys.argv[3]
cwd = Path(sys.argv[4])
sys.path.insert(0, str(repo_root / "scripts"))

from book_workflow_support import validate_obsidian_sync_destination

print(validate_obsidian_sync_destination(dest_dir, book_root, repo_root=repo_root, cwd=cwd))
PY
)"

STAGING_DIR="$(mktemp -d "${TMPDIR:-/tmp}/obsidian-sync-XXXXXX")"
cleanup() {
  rm -rf "$STAGING_DIR"
}
trap cleanup EXIT

"$PYTHON_BIN" - "$REPO_ROOT" "$BOOK_ROOT" "$STAGING_DIR" <<'PY'
import sys
from pathlib import Path

repo_root = Path(sys.argv[1])
book_root = Path(sys.argv[2])
staging_dir = Path(sys.argv[3])
sys.path.insert(0, str(repo_root / "scripts"))

from book_workflow_support import stage_obsidian_sync_tree

stage_obsidian_sync_tree(book_root, staging_dir)
PY

mkdir -p "$DEST_DIR"

# Mirror only the user-facing study assets needed by Obsidian. Repo chapter
# paths stay flat, but Obsidian receives a navigation-friendly chapter tree.
/usr/bin/rsync \
  -rlpgoD \
  --delete \
  --prune-empty-dirs \
  --omit-dir-times \
  --exclude '.DS_Store' \
  --include '*/' \
  --include '*.md' \
  --include '*.png' \
  --exclude '*' \
  "$STAGING_DIR/" \
  "$DEST_DIR/"
