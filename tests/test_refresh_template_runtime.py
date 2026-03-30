#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import refresh_book_template  # noqa: E402
import workflow_book_template as wbt  # noqa: E402


class RefreshTemplateRuntimeTests(unittest.TestCase):
    def test_context_uses_generic_obsidian_dest_placeholder(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            book_root = Path(tmp_dir) / "books" / "mini-book"
            book_root.mkdir(parents=True)
            (book_root / "README.md").write_text("# Mini Book\n", encoding="utf-8")
            wbt.write_book_metadata(book_root, wbt.CanonicalSource(kind="epub", name="Mini Book.epub"))

            context = refresh_book_template.context_for_book(book_root)

        self.assertEqual(context["BOOK_TITLE"], "Mini Book")
        self.assertEqual(context["OBSIDIAN_DEST"], "<configured-obsidian-vault>/Mini Book")
        self.assertEqual(context["BOOK_SOURCE_KIND"], "epub")
        self.assertEqual(context["BOOK_SOURCE_NAME"], "Mini Book.epub")

    def test_context_prefers_tracked_metadata_over_filesystem_presence(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            book_root = Path(tmp_dir) / "books" / "mini-book"
            (book_root / "source" / "pdf").mkdir(parents=True)
            (book_root / "source" / "epub").mkdir(parents=True)
            (book_root / "README.md").write_text("# Mini Book\n", encoding="utf-8")
            (book_root / "source" / "pdf" / "Alternate.pdf").write_text("pdf", encoding="utf-8")
            (book_root / "source" / "epub" / "Mini Book.epub").write_text("epub", encoding="utf-8")
            wbt.write_book_metadata(book_root, wbt.CanonicalSource(kind="epub", name="Mini Book.epub"))

            context = refresh_book_template.context_for_book(book_root)

        self.assertEqual(context["BOOK_SOURCE_KIND"], "epub")
        self.assertEqual(context["BOOK_SOURCE_NAME"], "Mini Book.epub")
        self.assertEqual(context["BOOK_PDF_NAME"], "SOURCE.pdf")

    def test_refresh_uses_metadata_when_canonical_source_file_is_missing(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            book_root = Path(tmp_dir) / "books" / "mini-book"
            (book_root / "source" / "pdf").mkdir(parents=True)
            (book_root / "source" / "epub").mkdir(parents=True)
            (book_root / "README.md").write_text("# Mini Book\n", encoding="utf-8")
            wbt.write_book_metadata(book_root, wbt.CanonicalSource(kind="pdf", name="Canonical.pdf"))

            with patch.object(
                refresh_book_template,
                "parse_args",
                return_value=type("Args", (), {"book_root": str(book_root)})(),
            ):
                result = refresh_book_template.main()

            self.assertEqual(result, 0)
            readme_text = (book_root / "README.md").read_text(encoding="utf-8")
            self.assertIn("source/pdf/Canonical.pdf", readme_text)
