#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_SRC = REPO_ROOT / "scripts"


class ShellEntrypointTests(unittest.TestCase):
    maxDiff = None

    def write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def copy_script(self, repo_root: Path, name: str) -> Path:
        target = repo_root / "scripts" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SCRIPTS_SRC / name, target)
        target.chmod(0o755)
        return target

    def copy_python_module(self, repo_root: Path, name: str) -> None:
        target = repo_root / "scripts" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SCRIPTS_SRC / name, target)

    def make_book_repo(self, base_dir: Path) -> tuple[Path, Path]:
        repo_root = base_dir / "repo"
        book_root = repo_root / "books" / "sample-book"
        (book_root / "lt" / "chapters").mkdir(parents=True, exist_ok=True)
        (book_root / "lt" / "figures").mkdir(parents=True, exist_ok=True)
        (book_root / "source" / "index").mkdir(parents=True, exist_ok=True)

        self.write(repo_root / "repo_config.toml", "[obsidian]\nbase_dir = '~/Obsidian'\nvault_name = 'Vault'\nlaunch_agent_prefix = 'lt.medbook.sync'\n")
        self.write(book_root / "README.md", "# Sample Book\n")
        self.write(
            book_root / "source" / "index" / "chapters.json",
            '[{"number": 1, "title": "Intro", "slug": "001-intro"}]\n',
        )
        self.write(
            book_root / "lt" / "chapters" / "001-intro.md",
            "# Intro\n\nTekstas.\n\n![Fig](../figures/f1.png)\n",
        )
        (book_root / "lt" / "figures" / "f1.png").write_bytes(b"png")

        for name in ("sync_obsidian_book.sh", "install_obsidian_sync_agent.sh"):
            self.copy_script(repo_root, name)
        for name in ("workflow_obsidian.py", "workflow_rules.py", "workflow_runtime.py"):
            self.copy_python_module(repo_root, name)

        venv_bin = repo_root / ".venv" / "bin"
        venv_bin.mkdir(parents=True, exist_ok=True)
        os.symlink(sys.executable, venv_bin / "python3")

        return repo_root, book_root

    def make_temp_bin(self, base_dir: Path) -> tuple[Path, Path]:
        bin_dir = base_dir / "bin"
        bin_dir.mkdir(parents=True, exist_ok=True)
        log_path = base_dir / "commands.log"
        return bin_dir, log_path

    def write_executable(self, path: Path, text: str) -> None:
        self.write(path, text)
        path.chmod(0o755)

    def read_log_lines(self, log_path: Path) -> list[str]:
        if not log_path.exists():
            return []
        return [line.strip() for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def test_sync_obsidian_book_shell_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            repo_root, _book_root = self.make_book_repo(temp_root)
            dest_dir = temp_root / "vault" / "Sample Book"

            result = subprocess.run(  # noqa: S603
                [
                    str(repo_root / "scripts" / "sync_obsidian_book.sh"),
                    "--book-root",
                    "books/sample-book",
                    "--dest",
                    str(dest_dir),
                ],
                cwd=repo_root,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertTrue((dest_dir / "chapters" / "001-intro.md").exists())
            self.assertTrue((dest_dir / "figures" / "f1.png").exists())
            chapter_text = (dest_dir / "chapters" / "001-intro.md").read_text(encoding="utf-8")
            self.assertIn("../figures/f1.png", chapter_text)

    def test_install_obsidian_sync_agent_shell_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            repo_root, _book_root = self.make_book_repo(temp_root)
            dest_dir = temp_root / "vault" / "Sample Book"
            home_dir = temp_root / "home"

            result = subprocess.run(  # noqa: S603
                [
                    str(repo_root / "scripts" / "install_obsidian_sync_agent.sh"),
                    "--book-root",
                    "books/sample-book",
                    "--dest",
                    str(dest_dir),
                ],
                cwd=repo_root,
                capture_output=True,
                text=True,
                env={
                    **os.environ,
                    "HOME": str(home_dir),
                    "OBSIDIAN_SYNC_SKIP_LOAD": "1",
                },
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            plist_path = home_dir / "Library" / "LaunchAgents" / "lt.medbook.sync-sample-book.plist"
            self.assertTrue(plist_path.exists())
            plist_text = plist_path.read_text(encoding="utf-8")
            self.assertIn("scripts/sync_obsidian_book.sh", plist_text)
            self.assertIn("books/sample-book", plist_text)
            self.assertIn(str(dest_dir), plist_text)
            self.assertTrue((dest_dir / "chapters" / "001-intro.md").exists())
            self.assertIn("LaunchAgent loading skipped", result.stdout)

    def test_setup_codex_mcp_shell_configures_only_missing_servers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            repo_root = temp_root / "repo"
            script_path = self.copy_script(repo_root, "setup_codex_mcp.sh")
            bin_dir, log_path = self.make_temp_bin(temp_root)

            self.write_executable(
                bin_dir / "codex",
                """#!/bin/sh
echo "codex:$@" >> "$FAKE_LOG"
if [ "$1" = "mcp" ] && [ "$2" = "get" ]; then
  case " $FAKE_EXISTING_MCPS " in
    *" $3 "*) exit 0 ;;
  esac
  exit 1
fi
exit 0
""",
            )

            result = subprocess.run(  # noqa: S603
                [str(script_path)],
                cwd=repo_root,
                capture_output=True,
                text=True,
                env={
                    **os.environ,
                    "PATH": f"{bin_dir}:{os.environ['PATH']}",
                    "FAKE_LOG": str(log_path),
                    "FAKE_EXISTING_MCPS": "context7 pdf-reader",
                },
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            log_lines = self.read_log_lines(log_path)
            self.assertIn("codex:mcp get context7", log_lines)
            self.assertIn("codex:mcp get pdf-reader", log_lines)
            self.assertNotIn("codex:mcp add context7 --url https://mcp.context7.com/mcp", log_lines)
            self.assertNotIn("codex:mcp add pdf-reader -- pdf-reader-mcp", log_lines)
            self.assertIn("codex:mcp add excalidraw --url https://mcp.excalidraw.com", log_lines)
            self.assertIn("codex:mcp add playwright -- npx @playwright/mcp@latest", log_lines)
            self.assertIn("codex:mcp add whimsical-desktop --url http://localhost:21190/mcp", log_lines)

    def test_bootstrap_macos_shell_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            repo_root = temp_root / "repo"
            home_dir = temp_root / "home"
            bin_dir, log_path = self.make_temp_bin(temp_root)

            for name in ("bootstrap_macos.sh", "install_repo_skills.sh", "setup_codex_mcp.sh"):
                self.copy_script(repo_root, name)
            self.write(repo_root / "Brewfile", "brew \"ripgrep\"\n")
            self.write(repo_root / "requirements.txt", "beautifulsoup4==4.14.2\n")
            self.write(repo_root / "codex" / "skills" / "sample-skill" / "SKILL.md", "# Sample skill\n")

            self.write_executable(
                bin_dir / "brew",
                """#!/bin/sh
echo "brew:$@" >> "$FAKE_LOG"
exit 0
""",
            )
            self.write_executable(
                bin_dir / "npm",
                """#!/bin/sh
echo "npm:$@" >> "$FAKE_LOG"
if [ "$1" = "install" ] && [ "$2" = "-g" ] && [ "$3" = "@openai/codex" ]; then
  cat > "$FAKE_BIN/codex" <<'EOF'
#!/bin/sh
echo "codex:$@" >> "$FAKE_LOG"
if [ "$1" = "mcp" ] && [ "$2" = "get" ]; then
  exit 1
fi
exit 0
EOF
  chmod +x "$FAKE_BIN/codex"
fi
if [ "$1" = "install" ] && [ "$2" = "-g" ] && [ "$3" = "@sylphx/pdf-reader-mcp" ]; then
  cat > "$FAKE_BIN/pdf-reader-mcp" <<'EOF'
#!/bin/sh
exit 0
EOF
  chmod +x "$FAKE_BIN/pdf-reader-mcp"
fi
exit 0
""",
            )
            self.write_executable(
                bin_dir / "python3",
                """#!/bin/sh
echo "python3:$@" >> "$FAKE_LOG"
if [ "$1" = "-m" ] && [ "$2" = "venv" ]; then
  VENV="$3"
  mkdir -p "$VENV/bin"
  cat > "$VENV/bin/pip" <<'EOF'
#!/bin/sh
echo "pip:$@" >> "$FAKE_LOG"
exit 0
EOF
  cat > "$VENV/bin/python" <<'EOF'
#!/bin/sh
echo "venv-python:$@" >> "$FAKE_LOG"
exit 0
EOF
  chmod +x "$VENV/bin/pip" "$VENV/bin/python"
  cp "$VENV/bin/python" "$VENV/bin/python3"
  exit 0
fi
exit 1
""",
            )

            result = subprocess.run(  # noqa: S603
                [str(repo_root / "scripts" / "bootstrap_macos.sh")],
                cwd=repo_root,
                capture_output=True,
                text=True,
                env={
                    **os.environ,
                    "HOME": str(home_dir),
                    "PATH": f"{bin_dir}:/usr/bin:/bin:/usr/sbin:/sbin",
                    "FAKE_LOG": str(log_path),
                    "FAKE_BIN": str(bin_dir),
                },
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            log_lines = self.read_log_lines(log_path)
            self.assertIn(f"brew:bundle --file={repo_root / 'Brewfile'}", log_lines)
            self.assertIn("npm:install -g @openai/codex", log_lines)
            self.assertIn("npm:install -g @sylphx/pdf-reader-mcp", log_lines)
            self.assertIn(f"python3:-m venv {repo_root / '.venv'}", log_lines)
            self.assertIn("pip:install --upgrade pip", log_lines)
            self.assertIn(f"pip:install -r {repo_root / 'requirements.txt'}", log_lines)
            self.assertIn("venv-python:-m playwright install chromium", log_lines)
            self.assertIn("venv-python:-c import fitz", log_lines)
            self.assertIn("codex:mcp add context7 --url https://mcp.context7.com/mcp", log_lines)
            installed_skill = home_dir / ".codex" / "skills" / "sample-skill" / "SKILL.md"
            self.assertTrue(installed_skill.exists())
            self.assertIn("Bootstrap complete.", result.stdout)


if __name__ == "__main__":
    unittest.main()
