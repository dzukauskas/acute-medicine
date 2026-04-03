#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
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
    def tracked_template_files(self) -> set[str]:
        result = subprocess.run(
            ["git", "ls-files", "books/_template"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return {
            path.removeprefix("books/_template/")
            for path in result.stdout.splitlines()
            if path.strip()
        }

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

    def test_tracked_template_files_are_manifest_managed_or_explicitly_exempt(self) -> None:
        manifest = wbt.load_template_manifest()
        tracked_files = self.tracked_template_files()
        manifest_files = set(manifest.get("always_refresh", [])) | set(manifest.get("refresh_if_empty", []))
        required_dirs = set(manifest.get("required_directories", []))
        allowed_files = manifest_files | {"template_manifest.json"} | {
            f"{rel_dir}/.gitkeep" for rel_dir in required_dirs
        }

        unexpected = sorted(tracked_files - allowed_files)
        self.assertEqual(unexpected, [], msg=f"Tracked template files missing manifest coverage: {unexpected}")

    def test_required_directories_match_gitkeep_scaffolds_or_tracked_content(self) -> None:
        manifest = wbt.load_template_manifest()
        tracked_files = self.tracked_template_files()
        required_dirs = set(manifest.get("required_directories", []))
        gitkeep_dirs = {
            rel_path.removesuffix("/.gitkeep")
            for rel_path in tracked_files
            if rel_path.endswith("/.gitkeep")
        }

        unexpected_gitkeep_dirs = sorted(gitkeep_dirs - required_dirs)
        self.assertEqual(
            unexpected_gitkeep_dirs,
            [],
            msg=f"Template .gitkeep directories missing from required_directories: {unexpected_gitkeep_dirs}",
        )

        missing_dir_backing: list[str] = []
        for rel_dir in sorted(required_dirs):
            has_gitkeep = f"{rel_dir}/.gitkeep" in tracked_files
            has_tracked_content = any(
                rel_path.startswith(f"{rel_dir}/") and rel_path != f"{rel_dir}/.gitkeep"
                for rel_path in tracked_files
            )
            if not has_gitkeep and not has_tracked_content:
                missing_dir_backing.append(rel_dir)

        self.assertEqual(
            missing_dir_backing,
            [],
            msg=f"required_directories entries are not backed by template scaffolds: {missing_dir_backing}",
        )


if __name__ == "__main__":
    unittest.main()
