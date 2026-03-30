#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import workflow_obsidian as wo  # noqa: E402


class ObsidianSyncSafetyTests(unittest.TestCase):
    def test_rejects_destination_inside_book_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            book_root = repo_root / "books" / "sample-book"
            (book_root / "lt").mkdir(parents=True)

            with self.assertRaises(SystemExit):
                wo.validate_obsidian_sync_destination(
                    book_root,
                    book_root,
                    repo_root=repo_root,
                    cwd=repo_root,
                )

    def test_rejects_destination_inside_repo_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            book_root = repo_root / "books" / "sample-book"
            dest_dir = repo_root / "vault-copy"
            (book_root / "lt").mkdir(parents=True)

            with self.assertRaises(SystemExit):
                wo.validate_obsidian_sync_destination(
                    dest_dir,
                    book_root,
                    repo_root=repo_root,
                    cwd=repo_root,
                )

    def test_allows_destination_outside_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            repo_root = tmp_path / "repo"
            book_root = repo_root / "books" / "sample-book"
            dest_dir = tmp_path / "obsidian-vault" / "Sample Book"
            (book_root / "lt").mkdir(parents=True)

            resolved = wo.validate_obsidian_sync_destination(
                dest_dir,
                book_root,
                repo_root=repo_root,
                cwd=repo_root,
            )

            self.assertEqual(resolved, dest_dir.resolve())


if __name__ == "__main__":
    unittest.main()
