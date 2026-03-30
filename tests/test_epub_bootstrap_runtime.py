#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import bootstrap_book_from_epub as epub_bootstrap  # noqa: E402


class EpubBootstrapRuntimeTests(unittest.TestCase):
    def test_dependency_probe_runs_only_via_runtime_helper(self) -> None:
        calls: list[tuple[str, str | None]] = []

        def fake_ensure(module_name: str, package_name: str | None = None) -> None:
            calls.append((module_name, package_name))
            if module_name == "bs4":
                raise SystemExit("missing bs4")

        with patch.object(epub_bootstrap, "ensure_python_module", side_effect=fake_ensure):
            with self.assertRaises(SystemExit):
                epub_bootstrap.ensure_epub_runtime_dependencies(force_reload=True)

        self.assertEqual(
            calls,
            [
                ("ebooklib", "EbookLib"),
                ("bs4", "beautifulsoup4"),
            ],
        )

    def test_install_obsidian_sync_rejects_non_macos(self) -> None:
        with patch.object(epub_bootstrap.sys, "platform", "linux"):
            with self.assertRaises(SystemExit) as ctx:
                epub_bootstrap.install_obsidian_sync(Path("/tmp/book-root"))

        self.assertIn("tik macOS", str(ctx.exception))
