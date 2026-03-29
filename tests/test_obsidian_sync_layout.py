#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import book_workflow_support as bws  # noqa: E402


class ObsidianSyncLayoutTests(unittest.TestCase):
    def test_section_folders_are_derived_from_chapter_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            book_root = repo_root / "books" / "sample-book"
            chapters_dir = book_root / "lt" / "chapters"
            figures_dir = book_root / "lt" / "figures"
            index_dir = book_root / "source" / "index"
            chapters_dir.mkdir(parents=True)
            figures_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)

            chapter_index = [
                {"number": 1, "title": "Disclaimer", "slug": "001-disclaimer"},
                {"number": 7, "title": "Section 1 – General Guidance", "slug": "007-section-1-general-guidance"},
                {"number": 8, "title": "Clinical Topic", "slug": "008-clinical-topic"},
                {"number": 25, "title": "Section 2 – Resuscitation", "slug": "025-section-2-resuscitation"},
                {"number": 26, "title": "ALS Overview", "slug": "026-als-overview"},
                {"number": 109, "title": "Index", "slug": "109-index"},
            ]
            (index_dir / "chapters.json").write_text(
                json.dumps(chapter_index, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            (chapters_dir / "001-disclaimer.md").write_text("# Disclaimer\n", encoding="utf-8")
            (chapters_dir / "007-section-1-general-guidance.md").write_text(
                "# Section 1\n![Fig](../figures/f1.png)\n",
                encoding="utf-8",
            )
            (chapters_dir / "008-clinical-topic.md").write_text(
                "# Topic\n![Fig](../figures/f1.png)\n",
                encoding="utf-8",
            )
            (chapters_dir / "025-section-2-resuscitation.md").write_text("# Section 2\n", encoding="utf-8")
            (chapters_dir / "026-als-overview.md").write_text("# ALS\n", encoding="utf-8")
            (chapters_dir / "109-index.md").write_text("# Index\n", encoding="utf-8")
            (figures_dir / "f1.png").write_bytes(b"png")

            staging_dir = Path(tmp_dir) / "staging"
            bws.stage_obsidian_sync_tree(book_root, staging_dir)

            self.assertTrue((staging_dir / "chapters" / "00 Front Matter" / "001-disclaimer.md").exists())
            self.assertTrue(
                (
                    staging_dir
                    / "chapters"
                    / "01 Section 1 - General Guidance"
                    / "007-section-1-general-guidance.md"
                ).exists()
            )
            self.assertTrue(
                (
                    staging_dir
                    / "chapters"
                    / "01 Section 1 - General Guidance"
                    / "008-clinical-topic.md"
                ).exists()
            )
            self.assertTrue(
                (
                    staging_dir
                    / "chapters"
                    / "02 Section 2 - Resuscitation"
                    / "025-section-2-resuscitation.md"
                ).exists()
            )
            self.assertTrue(
                (
                    staging_dir
                    / "chapters"
                    / "02 Section 2 - Resuscitation"
                    / "026-als-overview.md"
                ).exists()
            )
            self.assertTrue((staging_dir / "chapters" / "99 Reference" / "109-index.md").exists())
            self.assertTrue((staging_dir / "figures" / "f1.png").exists())

            rewritten = (
                staging_dir
                / "chapters"
                / "01 Section 1 - General Guidance"
                / "008-clinical-topic.md"
            ).read_text(encoding="utf-8")
            self.assertIn("../../figures/f1.png", rewritten)

    def test_books_without_sections_remain_flat(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            book_root = repo_root / "books" / "sample-book"
            chapters_dir = book_root / "lt" / "chapters"
            index_dir = book_root / "source" / "index"
            chapters_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)

            chapter_index = [
                {"number": 1, "title": "Intro", "slug": "001-intro"},
                {"number": 2, "title": "Chapter Two", "slug": "002-chapter-two"},
            ]
            (index_dir / "chapters.json").write_text(
                json.dumps(chapter_index, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            (chapters_dir / "001-intro.md").write_text("# Intro\n", encoding="utf-8")
            (chapters_dir / "002-chapter-two.md").write_text("# Two\n", encoding="utf-8")

            staging_dir = Path(tmp_dir) / "staging"
            bws.stage_obsidian_sync_tree(book_root, staging_dir)

            self.assertTrue((staging_dir / "chapters" / "001-intro.md").exists())
            self.assertTrue((staging_dir / "chapters" / "002-chapter-two.md").exists())


if __name__ == "__main__":
    unittest.main()
