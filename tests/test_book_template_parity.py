#!/usr/bin/env python3
from __future__ import annotations

import difflib
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import workflow_book_template as wbt  # noqa: E402


class BookTemplateParityTests(unittest.TestCase):
    maxDiff = None

    def test_tracked_books_match_template_managed_docs(self) -> None:
        manifest = wbt.load_template_manifest()
        always_refresh = manifest.get("always_refresh", [])
        mismatches: list[str] = []

        books_root = REPO_ROOT / "books"
        for book_root in sorted(path for path in books_root.iterdir() if path.is_dir() and path.name != "_template"):
            canonical_source = wbt.load_book_metadata(book_root)
            context = wbt.context_for_book(book_root, canonical_source)

            for rel_path in always_refresh:
                template_path = wbt.TEMPLATE_ROOT / rel_path
                target_path = book_root / rel_path
                expected = wbt.render_template_text(template_path, context)
                if not target_path.exists():
                    mismatches.append(f"{book_root.relative_to(REPO_ROOT).as_posix()}/{rel_path}: missing file")
                    continue

                actual = target_path.read_text(encoding="utf-8")
                if actual == expected:
                    continue

                diff = "\n".join(
                    difflib.unified_diff(
                        actual.splitlines(),
                        expected.splitlines(),
                        fromfile=target_path.relative_to(REPO_ROOT).as_posix(),
                        tofile=f"rendered:{rel_path}",
                        lineterm="",
                    )
                )
                mismatches.append(
                    f"{target_path.relative_to(REPO_ROOT).as_posix()}: drift detected\n{diff}"
                )

        self.assertEqual(mismatches, [])


if __name__ == "__main__":
    unittest.main()
