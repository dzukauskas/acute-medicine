#!/usr/bin/env python3
from __future__ import annotations

import json
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

    def write_template_manifest(
        self,
        template_root: Path,
        *,
        always_refresh: list[str] | None = None,
        refresh_if_empty: list[str] | None = None,
        required_directories: list[str] | None = None,
    ) -> dict[str, list[str]]:
        manifest = {
            "always_refresh": always_refresh or [],
            "refresh_if_empty": refresh_if_empty or [],
            "required_directories": required_directories or [],
        }
        (template_root / "template_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
        )
        return manifest

    def write_template_file(self, template_root: Path, rel_path: str, content: str = "sample\n") -> Path:
        path = template_root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

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

    def test_allowed_template_files_include_manifest_entries_and_required_gitkeeps(self) -> None:
        manifest = {
            "always_refresh": ["README.md", "research/README.md"],
            "refresh_if_empty": ["term_candidates.tsv"],
            "required_directories": ["research", "source/pdf"],
        }

        self.assertEqual(
            wbt.allowed_template_files(manifest),
            {
                "README.md",
                "research/README.md",
                "term_candidates.tsv",
                "template_manifest.json",
                "research/.gitkeep",
                "source/pdf/.gitkeep",
            },
        )

    def test_required_manifest_files_include_manifest_managed_files_and_manifest(self) -> None:
        manifest = {
            "always_refresh": ["README.md", "research/README.md"],
            "refresh_if_empty": ["term_candidates.tsv"],
            "required_directories": ["research", "source/pdf"],
        }

        self.assertEqual(
            wbt.required_manifest_files(manifest),
            {
                "README.md",
                "research/README.md",
                "term_candidates.tsv",
                "template_manifest.json",
            },
        )

    def test_unexpected_template_files_detects_relative_extra_paths(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            template_root = Path(tmp_dir) / "template"
            template_root.mkdir(parents=True)
            manifest = self.write_template_manifest(
                template_root,
                always_refresh=["README.md"],
                required_directories=["source/pdf"],
            )
            self.write_template_file(template_root, "README.md", "# Template\n")
            self.write_template_file(template_root, "source/pdf/.gitkeep", "")
            self.write_template_file(template_root, "rogue/extra.txt", "rogue\n")

            self.assertEqual(
                wbt.unexpected_template_files(template_root, manifest),
                ["rogue/extra.txt"],
            )

    def test_missing_template_files_detects_relative_missing_manifest_paths(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            template_root = Path(tmp_dir) / "template"
            template_root.mkdir(parents=True)
            manifest = self.write_template_manifest(
                template_root,
                always_refresh=["README.md", "research/README.md"],
                refresh_if_empty=["term_candidates.tsv"],
                required_directories=["research", "source/pdf"],
            )
            self.write_template_file(template_root, "README.md", "# Template\n")
            self.write_template_file(template_root, "source/pdf/.gitkeep", "")

            self.assertEqual(
                wbt.missing_template_files(template_root, manifest),
                ["research/README.md", "term_candidates.tsv"],
            )

    def test_copy_template_tree_hard_fails_on_missing_manifest_managed_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            template_root = Path(tmp_dir) / "template"
            template_root.mkdir(parents=True)
            self.write_template_manifest(
                template_root,
                always_refresh=["README.md", "research/README.md"],
                refresh_if_empty=["term_candidates.tsv"],
                required_directories=["research", "source/pdf"],
            )
            self.write_template_file(template_root, "README.md", "# Template\n")
            self.write_template_file(template_root, "source/pdf/.gitkeep", "")

            book_root = Path(tmp_dir) / "books" / "blocked-book"
            with self.assertRaisesRegex(
                ValueError,
                r"Template root failed validation\. Missing manifest-managed template files: "
                r"research/README\.md, term_candidates\.tsv",
            ):
                wbt.copy_template_tree(book_root, template_root=template_root)

            self.assertFalse(book_root.exists())

    def test_copy_template_tree_hard_fails_on_unexpected_template_files(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            template_root = Path(tmp_dir) / "template"
            template_root.mkdir(parents=True)
            self.write_template_manifest(
                template_root,
                always_refresh=["README.md"],
                required_directories=["source/pdf"],
            )
            self.write_template_file(template_root, "README.md", "# Template\n")
            self.write_template_file(template_root, "source/pdf/.gitkeep", "")
            self.write_template_file(template_root, "__probe_untracked_copytree__.txt", "probe\n")

            book_root = Path(tmp_dir) / "books" / "blocked-book"
            with self.assertRaisesRegex(
                ValueError,
                r"Template root failed validation\. Unexpected template files not covered by template_manifest\.json: "
                r"__probe_untracked_copytree__\.txt",
            ):
                wbt.copy_template_tree(book_root, template_root=template_root)

            self.assertFalse(book_root.exists())

    def test_copy_template_tree_copies_manifest_driven_surface(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            template_root = Path(tmp_dir) / "template"
            template_root.mkdir(parents=True)
            manifest = self.write_template_manifest(
                template_root,
                always_refresh=["README.md", "research/README.md"],
                refresh_if_empty=["term_candidates.tsv"],
                required_directories=["research", "source/pdf"],
            )
            self.write_template_file(template_root, "README.md", "# Template\n")
            self.write_template_file(template_root, "research/README.md", "Research\n")
            self.write_template_file(template_root, "term_candidates.tsv", "term\tcandidate\n")
            self.write_template_file(template_root, "source/pdf/.gitkeep", "")

            book_root = Path(tmp_dir) / "books" / "copied-book"
            wbt.copy_template_tree(book_root, template_root=template_root, manifest=manifest)

            self.assertTrue((book_root / "README.md").exists())
            self.assertTrue((book_root / "research" / "README.md").exists())
            self.assertTrue((book_root / "term_candidates.tsv").exists())
            self.assertTrue((book_root / "source" / "pdf" / ".gitkeep").exists())
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
        allowed_files = wbt.allowed_template_files(manifest)

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
