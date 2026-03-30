#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = Path(__file__).resolve().parent
import sys

if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from workflow_test_utils import (
    assert_mini_book_governance_contract,
    copy_mini_book,
    run_script,
    seed_canonical_artifacts,
    write,
)


class EndToEndWorkflowContractTests(unittest.TestCase):
    maxDiff = None

    def test_mini_book_smoke_passes_canonical_qa(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = copy_mini_book(Path(tmp_dir))
            seed_canonical_artifacts(book_root)

            assert_mini_book_governance_contract(book_root / "lt" / "chapters" / "001-mini.md")
            result = run_script("run_chapter_qa.py", "--book-root", str(book_root), "001-mini")

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertIn("Chapter QA passed for 001-mini.", result.stdout)

    def test_governance_contract_rejects_free_summary_rewrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = copy_mini_book(Path(tmp_dir))
            chapter_path = book_root / "lt" / "chapters" / "001-mini.md"
            write(
                chapter_path,
                chapter_path.read_text(encoding="utf-8").replace(
                    "Ankstyvas įvertinimas atliekamas ta pačia tvarka kaip originale ir išlaiko pagrindinę stebėjimų seką.",
                    "Skyriuje pateikiama trumpa bendra santrauka be originalo žingsnių sekos.",
                ),
            )

            with self.assertRaises(AssertionError):
                assert_mini_book_governance_contract(chapter_path)

    def test_run_chapter_qa_rejects_unmarked_original_context_signal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = copy_mini_book(Path(tmp_dir))
            seed_canonical_artifacts(book_root)
            chapter_path = book_root / "lt" / "chapters" / "001-mini.md"
            write(
                chapter_path,
                chapter_path.read_text(encoding="utf-8").replace(
                    "## Lietuvos kompensavimo tvarka\nRinkai specifinis pavadinimas pakeičiamas Lietuvos kompensavimo tvarkos nuoroda ir nepateikiamas kaip vietinis standartas.\n",
                    "## Lietuvos kompensavimo tvarka\nRinkai specifinis pavadinimas pakeičiamas Lietuvos kompensavimo tvarkos nuoroda ir nepateikiamas kaip vietinis standartas.\n\nCustom UK Tool paliekamas pagrindiniame tekste.\n",
                ),
            )

            result = run_script("run_chapter_qa.py", "--book-root", str(book_root), "001-mini")

            self.assertEqual(result.returncode, 1, msg=result.stdout + result.stderr)
            self.assertIn("originalo signalas `Custom UK Tool`", result.stdout + result.stderr)
