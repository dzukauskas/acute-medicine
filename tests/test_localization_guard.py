#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import localization_guard  # noqa: E402


class LocalizationGuardTests(unittest.TestCase):
    def write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def pack(self) -> dict:
        return {
            "blocks": [
                {
                    "localization_action": "original_context_callout",
                    "matched_localization_terms": ["Custom UK Tool"],
                }
            ],
            "localization_decisions": [
                {"source_term": "Custom UK Tool", "replacement_mode": "original_context_callout"}
            ],
            "localization_overrides": [],
        }

    def test_allows_original_context_callout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            chapter_path = Path(tmp_dir) / "chapter.md"
            self.write(
                chapter_path,
                "# Skyrius\n\n> [!note] Originalo kontekstas\n> `Custom UK Tool` paliekamas tik kaip originalo kontekstas.\n",
            )

            errors = localization_guard.localization_errors(chapter_path, self.pack())

            self.assertEqual(errors, [])

    def test_rejects_restricted_signal_in_main_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            chapter_path = Path(tmp_dir) / "chapter.md"
            self.write(chapter_path, "# Skyrius\n\nCustom UK Tool paliekamas pagrindiniame tekste.\n")

            errors = localization_guard.localization_errors(chapter_path, self.pack())

            self.assertEqual(len(errors), 2)
            self.assertTrue(any("Custom UK Tool" in error for error in errors))
            self.assertTrue(any("UK" in error for error in errors))
