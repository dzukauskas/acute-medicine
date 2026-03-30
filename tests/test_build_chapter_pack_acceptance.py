#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = Path(__file__).resolve().parent
import sys

if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from workflow_test_utils import copy_fixture, run_script  # noqa: E402


class BuildChapterPackAcceptanceTests(unittest.TestCase):
    maxDiff = None

    def test_table_fixture_routes_structured_block_to_table_compression(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = copy_fixture(Path(tmp_dir), "table_book")

            result = run_script("build_chapter_pack.py", "--book-root", str(book_root), "001-table")

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            pack_path = book_root / "chapter_packs" / "001-table.yaml"
            pack = yaml.safe_load(pack_path.read_text(encoding="utf-8"))
            table_block = next(
                block for block in pack["blocks"] if block["block_id"] == "table-1.1-early-warning-trigger-table"
            )

            self.assertEqual(table_block["block_type"], "table")
            self.assertEqual(table_block["draft_mode"], "table-compression")
            self.assertEqual(table_block["completion_hint"], "1.1 lentelė")
            self.assertFalse(table_block["summary_allowed"])


if __name__ == "__main__":
    unittest.main()
