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

from workflow_test_utils import copy_fixture, copy_mini_book, infer_fixture_slug, run_script  # noqa: E402


class PortableCanonicalArtifactsTests(unittest.TestCase):
    maxDiff = None

    def test_build_chapter_pack_normalizes_absolute_research_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = copy_mini_book(Path(tmp_dir), name="portable-mini-book")
            slug = infer_fixture_slug(book_root)
            research_path = book_root / "research" / f"{slug}.md"
            source_path = book_root / "source" / "chapters-en" / f"{slug}.md"
            lt_path = book_root / "lt" / "chapters" / f"{slug}.md"
            research_text = research_path.read_text(encoding="utf-8")
            research_text = research_text.replace(
                f"source/chapters-en/{slug}.md",
                str(source_path.resolve()),
            ).replace(
                f"lt/chapters/{slug}.md",
                str(lt_path.resolve()),
            )
            research_path.write_text(research_text, encoding="utf-8")

            result = run_script("build_chapter_pack.py", "--book-root", str(book_root), slug)

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            pack_text = (book_root / "chapter_packs" / f"{slug}.yaml").read_text(encoding="utf-8")
            self.assertIn(f"source_md: source/chapters-en/{slug}.md", pack_text)
            self.assertIn(f"lt_target_md: lt/chapters/{slug}.md", pack_text)
            self.assertIn("term_candidates_path: term_candidates.tsv", pack_text)

    def test_chapter_pack_is_identical_across_book_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            book_root_a = copy_mini_book(tmp_path / "a", name="portable-mini-book")
            book_root_b = copy_mini_book(tmp_path / "b", name="portable-mini-book")
            slug_a = infer_fixture_slug(book_root_a)
            slug_b = infer_fixture_slug(book_root_b)

            result_a = run_script("build_chapter_pack.py", "--book-root", str(book_root_a), slug_a)
            result_b = run_script("build_chapter_pack.py", "--book-root", str(book_root_b), slug_b)

            self.assertEqual(result_a.returncode, 0, msg=result_a.stdout + result_a.stderr)
            self.assertEqual(result_b.returncode, 0, msg=result_b.stdout + result_b.stderr)
            text_a = (book_root_a / "chapter_packs" / f"{slug_a}.yaml").read_text(encoding="utf-8")
            text_b = (book_root_b / "chapter_packs" / f"{slug_b}.yaml").read_text(encoding="utf-8")
            self.assertEqual(text_a, text_b)

    def test_adjudication_pack_is_identical_across_book_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            book_root_a = copy_fixture(tmp_path / "a", "review_book", name="portable-review-book")
            book_root_b = copy_fixture(tmp_path / "b", "review_book", name="portable-review-book")
            slug_a = infer_fixture_slug(book_root_a)
            slug_b = infer_fixture_slug(book_root_b)

            pack_a = run_script("build_chapter_pack.py", "--book-root", str(book_root_a), slug_a)
            pack_b = run_script("build_chapter_pack.py", "--book-root", str(book_root_b), slug_b)
            result_a = run_script("build_adjudication_pack.py", "--book-root", str(book_root_a), slug_a)
            result_b = run_script("build_adjudication_pack.py", "--book-root", str(book_root_b), slug_b)

            self.assertEqual(pack_a.returncode, 0, msg=pack_a.stdout + pack_a.stderr)
            self.assertEqual(pack_b.returncode, 0, msg=pack_b.stdout + pack_b.stderr)
            self.assertEqual(result_a.returncode, 0, msg=result_a.stdout + result_a.stderr)
            self.assertEqual(result_b.returncode, 0, msg=result_b.stdout + result_b.stderr)
            text_a = (book_root_a / "adjudication_packs" / f"{slug_a}.yaml").read_text(encoding="utf-8")
            text_b = (book_root_b / "adjudication_packs" / f"{slug_b}.yaml").read_text(encoding="utf-8")
            self.assertEqual(text_a, text_b)

    def test_research_checklist_is_identical_across_book_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            book_root_a = copy_mini_book(tmp_path / "a", name="portable-mini-book")
            book_root_b = copy_mini_book(tmp_path / "b", name="portable-mini-book")
            slug_a = infer_fixture_slug(book_root_a)
            slug_b = infer_fixture_slug(book_root_b)

            result_a = run_script("generate_research_checklist.py", "--book-root", str(book_root_a), slug_a)
            result_b = run_script("generate_research_checklist.py", "--book-root", str(book_root_b), slug_b)

            self.assertEqual(result_a.returncode, 0, msg=result_a.stdout + result_a.stderr)
            self.assertEqual(result_b.returncode, 0, msg=result_b.stdout + result_b.stderr)
            text_a = (book_root_a / "research" / f"{slug_a}.checklist.md").read_text(encoding="utf-8")
            text_b = (book_root_b / "research" / f"{slug_b}.checklist.md").read_text(encoding="utf-8")
            self.assertEqual(text_a, text_b)


if __name__ == "__main__":
    unittest.main()
