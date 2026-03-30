#!/usr/bin/env python3
from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import workflow_book_template as wbt  # noqa: E402


class WorkflowBookTemplateTests(unittest.TestCase):
    def test_load_template_manifest_exposes_required_directories(self) -> None:
        manifest = wbt.load_template_manifest()

        self.assertIn("always_refresh", manifest)
        self.assertIn("required_directories", manifest)
        self.assertIn("source/pdf", manifest["required_directories"])

    def test_copy_template_tree_removes_internal_manifest(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            book_root = Path(tmp_dir) / "books" / "copied-book"
            wbt.copy_template_tree(book_root)

            self.assertTrue((book_root / "README.md").exists())
            self.assertFalse((book_root / "template_manifest.json").exists())

    def test_materialize_required_directories_recreates_missing_scaffolds(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            book_root = Path(tmp_dir) / "books" / "scaffold-book"
            wbt.copy_template_tree(book_root)

            shutil.rmtree(book_root / "source" / "pdf")
            shutil.rmtree(book_root / "source" / "epub")
            shutil.rmtree(book_root / "source" / "figures-raw")

            manifest = wbt.load_template_manifest()
            wbt.materialize_required_directories(book_root, manifest)

            self.assertTrue((book_root / "source" / "pdf").is_dir())
            self.assertTrue((book_root / "source" / "epub").is_dir())
            self.assertTrue((book_root / "source" / "figures-raw").is_dir())

    def test_book_metadata_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            book_root = Path(tmp_dir) / "books" / "meta-book"
            source = wbt.CanonicalSource(kind="epub", name="Sample.epub")

            metadata_path = wbt.write_book_metadata(book_root, source)
            loaded = wbt.load_book_metadata(book_root)

        self.assertEqual(metadata_path.name, "book_metadata.yaml")
        self.assertEqual(loaded, source)

    def test_load_book_metadata_rejects_invalid_kind(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            book_root = Path(tmp_dir) / "books" / "broken-book"
            metadata_path = book_root / "book_metadata.yaml"
            metadata_path.parent.mkdir(parents=True, exist_ok=True)
            metadata_path.write_text(
                "canonical_source:\n  kind: docx\n  name: Sample.docx\n",
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                wbt.load_book_metadata(book_root)

    def test_context_for_book_uses_declared_canonical_source(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            book_root = Path(tmp_dir) / "books" / "context-book"
            book_root.mkdir(parents=True)
            (book_root / "README.md").write_text("# Context Book\n", encoding="utf-8")

            context = wbt.context_for_book(
                book_root,
                wbt.CanonicalSource(kind="pdf", name="Context Book.pdf"),
            )

        self.assertEqual(context["BOOK_TITLE"], "Context Book")
        self.assertEqual(context["BOOK_SOURCE_KIND"], "pdf")
        self.assertEqual(context["BOOK_SOURCE_NAME"], "Context Book.pdf")
        self.assertEqual(context["BOOK_PDF_NAME"], "Context Book.pdf")
        self.assertEqual(context["OBSIDIAN_DEST"], "<configured-obsidian-vault>/Context Book")


if __name__ == "__main__":
    unittest.main()
