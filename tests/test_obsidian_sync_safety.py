#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from unittest.mock import patch
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

    def test_claim_writes_owner_marker_for_first_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            repo_root = tmp_path / "repo"
            book_root = repo_root / "books" / "sample-book"
            dest_dir = tmp_path / "obsidian-vault" / "Sample Book"
            (book_root / "lt").mkdir(parents=True)
            (book_root / "README.md").write_text("# Sample Book\n", encoding="utf-8")

            claimed = wo.claim_obsidian_sync_destination(
                dest_dir,
                book_root,
                repo_root=repo_root,
                cwd=repo_root,
            )

            owner_path = dest_dir / ".acute-medicine-sync-owner.json"
            self.assertEqual(claimed, dest_dir.resolve())
            self.assertTrue(owner_path.exists())
            self.assertIn("sample-book", owner_path.read_text(encoding="utf-8"))

    def test_claim_rejects_different_workspace_for_same_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            first_repo_root = tmp_path / "repo-a"
            second_repo_root = tmp_path / "repo-b"
            first_book_root = first_repo_root / "books" / "sample-book"
            second_book_root = second_repo_root / "books" / "sample-book"
            dest_dir = tmp_path / "obsidian-vault" / "Sample Book"
            for book_root in (first_book_root, second_book_root):
                (book_root / "lt").mkdir(parents=True)
                (book_root / "README.md").write_text("# Sample Book\n", encoding="utf-8")

            wo.claim_obsidian_sync_destination(
                dest_dir,
                first_book_root,
                repo_root=first_repo_root,
                cwd=first_repo_root,
            )

            with self.assertRaises(SystemExit) as ctx:
                wo.claim_obsidian_sync_destination(
                    dest_dir,
                    second_book_root,
                    repo_root=second_repo_root,
                    cwd=second_repo_root,
                )

            self.assertIn("jau rezervuota kitai darbo vietai", str(ctx.exception))

    def test_launch_agent_label_is_workspace_aware(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            book_root = tmp_path / "books" / "sample-book"
            book_root.mkdir(parents=True)

            with patch.object(wo, "obsidian_config", return_value={"launch_agent_prefix": "lt.medbook.sync"}):
                label_a = wo.obsidian_launch_agent_label(book_root, repo_root=tmp_path / "repo-a")
                label_b = wo.obsidian_launch_agent_label(book_root, repo_root=tmp_path / "repo-b")

        self.assertNotEqual(label_a, label_b)
        self.assertTrue(label_a.startswith("lt.medbook.sync-sample-book-"))


if __name__ == "__main__":
    unittest.main()
