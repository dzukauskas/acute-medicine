#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import refresh_book_template  # noqa: E402


class RefreshTemplateRuntimeTests(unittest.TestCase):
    def test_context_uses_generic_obsidian_dest_placeholder(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            book_root = Path(tmp_dir) / "books" / "mini-book"
            book_root.mkdir(parents=True)
            (book_root / "README.md").write_text("# Mini Book\n", encoding="utf-8")

            context = refresh_book_template.context_for_book(book_root)

        self.assertEqual(context["BOOK_TITLE"], "Mini Book")
        self.assertEqual(context["OBSIDIAN_DEST"], "<configured-obsidian-vault>/Mini Book")
