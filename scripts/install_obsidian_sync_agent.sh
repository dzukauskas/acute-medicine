#!/bin/zsh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SYNC_SCRIPT="$REPO_ROOT/scripts/sync_obsidian_acute_medicine.sh"
DEST_DIR="${1:-$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/PARAMEDIKAS/Acute Medicine}"
PLIST_PATH="$HOME/Library/LaunchAgents/com.dzukauskas.acute-medicine-obsidian-sync.plist"
WATCH_CHAPTERS="$REPO_ROOT/books/acute-medicine/lt/chapters"
WATCH_FIGURES="$REPO_ROOT/books/acute-medicine/lt/figures"

mkdir -p "$HOME/Library/LaunchAgents" "$DEST_DIR"

cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "https://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.dzukauskas.acute-medicine-obsidian-sync</string>

  <key>ProgramArguments</key>
  <array>
    <string>$SYNC_SCRIPT</string>
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
  <string>/tmp/acute-medicine-obsidian-sync.log</string>

  <key>StandardErrorPath</key>
  <string>/tmp/acute-medicine-obsidian-sync.log</string>
</dict>
</plist>
EOF

launchctl unload -w "$PLIST_PATH" 2>/dev/null || true
launchctl load -w "$PLIST_PATH"
"$SYNC_SCRIPT" "$DEST_DIR"

echo "Installed Obsidian sync agent:"
echo "  $PLIST_PATH"
echo "Sync destination:"
echo "  $DEST_DIR"
