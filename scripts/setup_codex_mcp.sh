#!/bin/zsh

set -euo pipefail

ensure_http_mcp() {
  local name="$1"
  local url="$2"
  if codex mcp get "$name" >/dev/null 2>&1; then
    echo "MCP already configured: $name"
  else
    codex mcp add "$name" --url "$url"
    echo "Configured MCP: $name"
  fi
}

ensure_stdio_mcp() {
  local name="$1"
  shift
  if codex mcp get "$name" >/dev/null 2>&1; then
    echo "MCP already configured: $name"
  else
    codex mcp add "$name" -- "$@"
    echo "Configured MCP: $name"
  fi
}

ensure_http_mcp "context7" "https://mcp.context7.com/mcp"
ensure_stdio_mcp "pdf-reader" "pdf-reader-mcp"
ensure_http_mcp "excalidraw" "https://mcp.excalidraw.com"
ensure_stdio_mcp "playwright" "npx" "@playwright/mcp@latest"
ensure_http_mcp "whimsical-desktop" "http://localhost:21190/mcp"

echo
echo "Whimsical MCP will respond only when the Whimsical desktop app is running and you are signed in."
