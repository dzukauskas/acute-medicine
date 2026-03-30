#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
TESTS_DIR = Path(__file__).resolve().parent
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

import completeness_guard  # noqa: E402
import workflow_markdown as wm  # noqa: E402
from workflow_test_utils import copy_fixture, seed_canonical_artifacts, write  # noqa: E402


class CompletenessGuardTests(unittest.TestCase):
    def test_chart_summary_marker_proves_coverage(self) -> None:
        lt_text = "# Skyrius\n\n## NEWS2 originalo kontekste\nTrumpa santrauka.\n<!-- chart-coverage: 1.1, 1.2 -->\n"
        sections = wm.parse_markdown_sections(lt_text)
        blocks = [
            {
                "block_id": "chart-1.1-news2",
                "block_type": "chart",
                "completion_hint": "NEWS2 originalo kontekste",
                "source_label": "1.1",
                "summary_allowed": True,
            },
            {
                "block_id": "chart-1.2-news2",
                "block_type": "chart",
                "completion_hint": "NEWS2 originalo kontekste",
                "source_label": "1.2",
                "summary_allowed": True,
            },
        ]

        errors = completeness_guard.check_summary_group(blocks, sections, Path("lt/chapters/001-mini.md"))

        self.assertEqual(errors, [])

    def test_chart_summary_marker_reports_missing_label(self) -> None:
        lt_text = "# Skyrius\n\n## NEWS2 originalo kontekste\nTrumpa santrauka.\n<!-- chart-coverage: 1.1 -->\n"
        sections = wm.parse_markdown_sections(lt_text)
        blocks = [
            {
                "block_id": "chart-1.1-news2",
                "block_type": "chart",
                "completion_hint": "NEWS2 originalo kontekste",
                "source_label": "1.1",
                "summary_allowed": True,
            },
            {
                "block_id": "chart-1.2-news2",
                "block_type": "chart",
                "completion_hint": "NEWS2 originalo kontekste",
                "source_label": "1.2",
                "summary_allowed": True,
            },
        ]

        errors = completeness_guard.check_summary_group(blocks, sections, Path("lt/chapters/001-mini.md"))

        self.assertEqual(len(errors), 1)
        self.assertIn("missing labels=1.2", errors[0])

    def test_main_reports_missing_structured_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            lt_path = tmp_path / "lt" / "chapters" / "001-mini.md"
            lt_path.parent.mkdir(parents=True, exist_ok=True)
            lt_path.write_text("# Skyrius\n\n## Ankstyvas įvertinimas\nTekstas.\n", encoding="utf-8")
            pack_path = tmp_path / "chapter_packs" / "001-mini.yaml"
            pack_path.parent.mkdir(parents=True, exist_ok=True)
            pack_path.write_text(
                "lt_target_md: lt/chapters/001-mini.md\n"
                "blocks:\n"
                "  - block_id: algorithm-1.1-airway-algorithm\n"
                "    block_type: algorithm\n"
                "    heading: Airway algorithm\n"
                "    source_label: '1.1'\n",
                encoding="utf-8",
            )

            result = subprocess.run(  # noqa: S603
                [sys.executable, str(SCRIPTS_DIR / "completeness_guard.py"), str(pack_path)],
                cwd=tmp_path,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("missing block_id='algorithm-1.1-airway-algorithm'", result.stdout)

    def test_chart_fixture_passes_with_complete_chart_coverage_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = copy_fixture(Path(tmp_dir), "chart_book")
            slug = seed_canonical_artifacts(book_root)

            result = subprocess.run(  # noqa: S603
                [sys.executable, str(SCRIPTS_DIR / "completeness_guard.py"), "--book-root", str(book_root), slug],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertIn("All checked structured blocks are represented", result.stdout)

    def test_chart_fixture_fails_when_one_chart_label_is_missing_from_coverage_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = copy_fixture(Path(tmp_dir), "chart_book")
            slug = seed_canonical_artifacts(book_root)
            chapter_path = book_root / "lt" / "chapters" / f"{slug}.md"
            write(
                chapter_path,
                chapter_path.read_text(encoding="utf-8").replace(
                    "<!-- chart-coverage: 1.1, 1.2 -->",
                    "<!-- chart-coverage: 1.1 -->",
                ),
            )

            result = subprocess.run(  # noqa: S603
                [sys.executable, str(SCRIPTS_DIR / "completeness_guard.py"), "--book-root", str(book_root), slug],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("chart coverage marker mismatch", result.stdout)
            self.assertIn("missing labels=1.2", result.stdout)
