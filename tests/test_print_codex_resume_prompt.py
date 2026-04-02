#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
TESTS_DIR = REPO_ROOT / "tests"
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

import print_codex_resume_prompt  # noqa: E402
from workflow_test_utils import copy_mini_book, silence_stdio  # noqa: E402


class PrintCodexResumePromptTests(unittest.TestCase):
    def test_engineering_prompt_uses_ledger_theme_and_next_step(self) -> None:
        ledger_text = """# Engineering Ledger

## Active Theme
<!-- ledger:active_theme:start -->
- Theme: Codex workflow cleanup
- Branch: main
- Last updated: 2026-03-30T15:00:00+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- Supaprastinti repo engineering darbo tęstinumą.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- State
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Decision
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Pirma peržiūrėti galutinį diff.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Risk
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
- Done
<!-- ledger:completed:end -->
"""
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            ledger_path = Path(tmp_dir) / "ENGINEERING_LEDGER.md"
            ledger_path.write_text(ledger_text, encoding="utf-8")
            with patch.object(print_codex_resume_prompt, "ENGINEERING_LEDGER", ledger_path):
                prompt = print_codex_resume_prompt.render_engineering_prompt()

        self.assertIn("Codex workflow cleanup", prompt)
        self.assertIn("Supaprastinti repo engineering darbo tęstinumą.", prompt)
        self.assertIn("Pirma peržiūrėti galutinį diff.", prompt)
        self.assertIn("Dabartinė būsena: State", prompt)
        self.assertIn("Priimti sprendimai: Decision", prompt)
        self.assertIn("Atviros rizikos: Risk", prompt)
        self.assertIn("Tęsk aktyvią temą", prompt)

    def test_engineering_prompt_handles_no_active_theme(self) -> None:
        ledger_text = """# Engineering Ledger

## Active Theme
<!-- ledger:active_theme:start -->
- Theme: no-active-theme
- Branch: main
- Last updated: 2026-03-30T15:00:00+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- Paskutinis sweep sulygino repo engineering dokumentaciją.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- State
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Decision
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Pasirinkti kitą siaurą temą.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Risk
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
### 2026-03-30 14:50 | Codex workflow cleanup
- Uždaryta.
<!-- ledger:completed:end -->
"""
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            ledger_path = Path(tmp_dir) / "ENGINEERING_LEDGER.md"
            ledger_path.write_text(ledger_text, encoding="utf-8")
            with patch.object(print_codex_resume_prompt, "ENGINEERING_LEDGER", ledger_path):
                prompt = print_codex_resume_prompt.render_engineering_prompt()

        self.assertIn("Ledger šiuo metu neturi aktyvios repo-engineering temos.", prompt)
        self.assertIn("Paskutinė uždaryta tema: Codex workflow cleanup.", prompt)
        self.assertIn("Paskutinis sweep sulygino repo engineering dokumentaciją.", prompt)
        self.assertIn("Dabartinė būsena: State", prompt)
        self.assertIn("Priimti sprendimai: Decision", prompt)
        self.assertIn("Atviros rizikos: Risk", prompt)
        self.assertIn("Pasirinkti kitą siaurą temą.", prompt)
        self.assertNotIn("Tęsk aktyvią temą", prompt)

    def test_translation_prompt_includes_book_workflow_and_term_candidates(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            book_root = copy_mini_book(Path(tmp_dir))
            chapter_pack = book_root / "chapter_packs" / "001-mini.yaml"
            chapter_pack.parent.mkdir(parents=True, exist_ok=True)
            chapter_pack.write_text("slug: 001-mini\n", encoding="utf-8")
            adjudication_pack = book_root / "adjudication_packs" / "001-mini.yaml"
            adjudication_pack.parent.mkdir(parents=True, exist_ok=True)
            adjudication_pack.write_text("[]\n", encoding="utf-8")
            prompt = print_codex_resume_prompt.render_translation_prompt(book_root, "001")

        self.assertIn("books/_template/workflow.md", prompt)
        self.assertIn("books/_template/source-priority.md", prompt)
        self.assertIn("docs/book-translation-workflow.md", prompt)
        self.assertIn("term_candidates.tsv", prompt)
        self.assertIn("Tęsk šio skyriaus darbą: 001.", prompt)
        self.assertIn("chapter_packs/001-mini.yaml", prompt)
        self.assertIn("001-mini.md", prompt)
        self.assertIn("adjudication_packs/001-mini.yaml", prompt)
        self.assertIn("Static passive repo context imk iš AGENTS.md, books/README.md ir workflow docs;", prompt)
        self.assertIn("current dynamic durable execution state imk iš šio skyriaus artefaktų.", prompt)
        self.assertIn("run_chapter_qa.py", prompt)
        self.assertIn("stored machine-readable receipt", prompt)

    def test_translation_prompt_without_chapter_still_mentions_qa_rerun(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            book_root = copy_mini_book(Path(tmp_dir))
            prompt = print_codex_resume_prompt.render_translation_prompt(book_root, None)

        self.assertIn(f"Tęsk aktyvų darbą knygoje {book_root.name}.", prompt)
        self.assertIn("run_chapter_qa.py", prompt)
        self.assertIn("Static passive repo context imk iš AGENTS.md, books/README.md ir workflow docs;", prompt)
        self.assertIn("current dynamic durable execution state imk iš aktyvaus darbo ir einamo skyriaus artefaktų.", prompt)
        self.assertNotIn("current dynamic durable execution state imk iš šio skyriaus artefaktų.", prompt)

    def test_translation_prompt_accepts_full_slug_token(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            book_root = copy_mini_book(Path(tmp_dir))
            chapter_pack = book_root / "chapter_packs" / "001-mini.yaml"
            chapter_pack.parent.mkdir(parents=True, exist_ok=True)
            chapter_pack.write_text("slug: 001-mini\n", encoding="utf-8")
            adjudication_pack = book_root / "adjudication_packs" / "001-mini.yaml"
            adjudication_pack.parent.mkdir(parents=True, exist_ok=True)
            adjudication_pack.write_text("[]\n", encoding="utf-8")
            prompt = print_codex_resume_prompt.render_translation_prompt(book_root, "001-mini")

        self.assertIn("Tęsk šio skyriaus darbą: 001-mini.", prompt)
        self.assertIn("research/001-mini.md", prompt)
        self.assertIn("chapter_packs/001-mini.yaml", prompt)
        self.assertIn("lt/chapters/001-mini.md", prompt)
        self.assertIn("adjudication_packs/001-mini.yaml", prompt)

    def test_translation_prompt_matches_manual_workflow_contract_fragments(self) -> None:
        workflow_text = (REPO_ROOT / "docs" / "book-translation-workflow.md").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            book_root = copy_mini_book(Path(tmp_dir))
            chapter_pack = book_root / "chapter_packs" / "001-mini.yaml"
            chapter_pack.parent.mkdir(parents=True, exist_ok=True)
            chapter_pack.write_text("slug: 001-mini\n", encoding="utf-8")
            prompt = print_codex_resume_prompt.render_translation_prompt(book_root, "001")

        shared_fragments = (
            "docs/book-translation-workflow.md",
            "Static passive repo context imk iš AGENTS.md, books/README.md ir workflow docs;",
            "current dynamic durable execution state imk iš šio skyriaus artefaktų.",
            "run_chapter_qa.py iš naujo; jis nėra stored machine-readable receipt.",
        )
        for fragment in shared_fragments:
            self.assertIn(fragment, workflow_text)
            self.assertIn(fragment, prompt)

    def test_main_prints_engineering_prompt(self) -> None:
        with silence_stdio():
            exit_code = print_codex_resume_prompt.main(["--mode", "engineering"])
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
