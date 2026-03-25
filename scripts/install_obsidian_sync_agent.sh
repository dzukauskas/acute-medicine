#!/bin/zsh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SYNC_SCRIPT="$REPO_ROOT/scripts/sync_obsidian_book.sh"
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
  BOOK_ROOT_REL="${BOOK_ROOT#$REPO_ROOT/}"
else
  BOOK_ROOT="$REPO_ROOT/$BOOK_ROOT_REL"
fi
README_PATH="$BOOK_ROOT/README.md"
if [[ ! -d "$BOOK_ROOT" ]]; then
  echo "Book root not found: $BOOK_ROOT" >&2
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

from book_workflow_support import book_title_from_readme, default_obsidian_dest, obsidian_launch_agent_label

print(book_title_from_readme(book_root))
print(default_obsidian_dest(book_root))
print(obsidian_launch_agent_label(book_root))
PY
)"

BOOK_TITLE="$(printf '%s\n' "$CONFIG_VALUES" | sed -n '1p')"
DEFAULT_DEST="$(printf '%s\n' "$CONFIG_VALUES" | sed -n '2p')"
AGENT_LABEL="$(printf '%s\n' "$CONFIG_VALUES" | sed -n '3p')"

DEST_DIR="${DEST_DIR:-$DEFAULT_DEST}"
PLIST_PATH="$HOME/Library/LaunchAgents/$AGENT_LABEL.plist"
WATCH_CHAPTERS="$BOOK_ROOT/lt/chapters"
WATCH_FIGURES="$BOOK_ROOT/lt/figures"
LOG_PATH="/tmp/${AGENT_LABEL}.log"

mkdir -p "$HOME/Library/LaunchAgents" "$DEST_DIR"

cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "https://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>$AGENT_LABEL</string>

  <key>ProgramArguments</key>
  <array>
    <string>$SYNC_SCRIPT</string>
    <string>--book-root</string>
    <string>$BOOK_ROOT_REL</string>
    <string>--dest</string>
    <string>$DEST_DIR</string>
  </array>

  <key>RunAtLoad</key>
  <true/>

  <key>WatchPaths</key>
  <array>
    <string>$WATCH_CHAPTERS</string>
    <string>$WATCH_FIGURES</string>
  </array>

  <key>StandardOutPath</key>
  <string>$LOG_PATH</string>

  <key>StandardErrorPath</key>
  <string>$LOG_PATH</string>
</dict>
</plist>
EOF

if [[ "${OBSIDIAN_SYNC_SKIP_LOAD:-0}" != "1" ]]; then
  launchctl unload -w "$PLIST_PATH" 2>/dev/null || true
  launchctl load -w "$PLIST_PATH"
fi
"$SYNC_SCRIPT" --book-root "$BOOK_ROOT_REL" --dest "$DEST_DIR"

echo "Installed Obsidian sync agent:"
echo "  $PLIST_PATH"
echo "Book root:"
echo "  $BOOK_ROOT_REL"
echo "Sync destination:"
echo "  $DEST_DIR"
if [[ "${OBSIDIAN_SYNC_SKIP_LOAD:-0}" == "1" ]]; then
  echo "LaunchAgent loading skipped because OBSIDIAN_SYNC_SKIP_LOAD=1"
fi
