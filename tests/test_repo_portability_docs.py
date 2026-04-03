#!/usr/bin/env python3
from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS_PATH = REPO_ROOT / "AGENTS.md"
GITIGNORE_PATH = REPO_ROOT / ".gitignore"
NEW_MAC_SETUP_PATH = REPO_ROOT / "docs" / "new-mac-setup.md"
CODEX_WORKFLOW_PATH = REPO_ROOT / "docs" / "codex-workflow.md"
REPO_ENGINEERING_WORKFLOW_PATH = REPO_ROOT / "docs" / "repo-engineering-workflow.md"
BOOK_TRANSLATION_WORKFLOW_PATH = REPO_ROOT / "docs" / "book-translation-workflow.md"
BOOKS_README_PATH = REPO_ROOT / "books" / "README.md"
HANDOFFS_README_PATH = REPO_ROOT / "handoffs" / "README.md"
BOOTSTRAP_MACOS_PATH = REPO_ROOT / "scripts" / "bootstrap_macos.sh"
SETUP_CODEX_MCP_PATH = REPO_ROOT / "scripts" / "setup_codex_mcp.sh"
PASSIVE_INDEX_PATTERN = re.compile(r"Passive repo context index:\n((?:- .+\n)+)")
TIME_SENSITIVE_STATE_MARKERS = ("Active Theme", "Completed Themes", "Last updated")
SHELL_DOCS = {
    NEW_MAC_SETUP_PATH: (
        "naudoja `bash`",
        "`zsh` setup nereikia",
        "macOS-specific",
    ),
    REPO_ROOT / "books" / "README.md": (
        "remiasi `bash`",
        "`zsh` requirement nėra",
        "macOS-specific",
    ),
    REPO_ROOT / "books" / "_template" / "README.md": (
        "remiasi `bash`",
        "`zsh` requirement nėra",
        "macOS-specific",
    ),
    REPO_ROOT
    / "books"
    / "jrcalc-clinical-guidelines-2025-reference-edition"
    / "README.md": (
        "remiasi `bash`",
        "`zsh` requirement nėra",
        "macOS-specific",
    ),
}


class RepoPortabilityDocsTests(unittest.TestCase):
    def extract_passive_index_block(self) -> str:
        text = AGENTS_PATH.read_text(encoding="utf-8")
        match = PASSIVE_INDEX_PATTERN.search(text)
        self.assertIsNotNone(match, msg="AGENTS.md is missing the passive repo context index block.")
        return match.group(1)

    def test_portability_docs_do_not_bake_host_repo_root(self) -> None:
        host_repo_root = str(REPO_ROOT)
        paths = [AGENTS_PATH, *SHELL_DOCS.keys()]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(
                host_repo_root,
                text,
                msg=f"{path} still contains the host-specific repo root.",
            )

    def test_agents_binding_workflow_uses_repo_relative_paths(self) -> None:
        text = AGENTS_PATH.read_text(encoding="utf-8")
        self.assertIn(
            "Treat repo-relative `books/README.md`, `books/_template/workflow.md`, "
            "and `books/_template/source-priority.md` as operational rules, not optional guidance.",
            text,
        )

    def test_python_version_docs_pin_python311_floor(self) -> None:
        for path in (NEW_MAC_SETUP_PATH, BOOKS_README_PATH):
            text = path.read_text(encoding="utf-8")
            self.assertIn("`python3 >= 3.11`", text, msg=f"{path} is missing the pinned Python floor.")

    def test_repo_local_mcp_docs_match_tracked_setup(self) -> None:
        script_text = SETUP_CODEX_MCP_PATH.read_text(encoding="utf-8")
        configured_mcps = set(re.findall(r'ensure_(?:http|stdio)_mcp "([^"]+)"', script_text))
        self.assertEqual(
            configured_mcps,
            {"context7", "pdf-reader", "excalidraw", "playwright", "whimsical-desktop"},
        )

        docs_text = NEW_MAC_SETUP_PATH.read_text(encoding="utf-8")
        for name in sorted(configured_mcps):
            self.assertIn(f"`{name}`", docs_text, msg=f"{NEW_MAC_SETUP_PATH} is missing MCP: {name}")

    def test_agents_separate_machine_level_and_repo_local_tooling(self) -> None:
        text = AGENTS_PATH.read_text(encoding="utf-8")
        self.assertIn("Machine-level preferred tools when available:", text)
        self.assertIn("Repo-local bootstrap guaranteed tools:", text)
        self.assertIn("`ebook-mcp`", text)
        self.assertIn("`context7`", text)

    def test_agents_include_passive_repo_context_index(self) -> None:
        text = AGENTS_PATH.read_text(encoding="utf-8")
        self.assertIn("Passive repo context index:", text)
        self.assertIn("static_passive_context | AGENTS.md | books/README.md | docs/codex-workflow.md", text)
        self.assertIn("translation_durable_state | research/<slug>.md | chapter_packs/<slug>.yaml", text)
        self.assertIn("repo_engineering_durable_state | ENGINEERING_LEDGER.md", text)
        self.assertIn("skill_precedence | AGENTS.md + binding workflow docs override conflicting repo-local skill text", text)
        self.assertIn("translation_qa | rerunnable pipeline via scripts/run_chapter_qa.py | not a stored machine-readable receipt", text)

    def test_agents_passive_index_stays_compact_and_non_temporal(self) -> None:
        index_block = self.extract_passive_index_block()
        index_lines = [line for line in index_block.splitlines() if line.strip()]
        self.assertLessEqual(len(index_lines), 14, msg="AGENTS.md passive index should stay compact.")
        for marker in TIME_SENSITIVE_STATE_MARKERS:
            self.assertNotIn(marker, index_block, msg=f"AGENTS.md passive index should not store `{marker}`.")
        self.assertIsNone(
            re.search(r"\b20\d{2}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:[+-]\d{2}:\d{2})?)?\b", index_block),
            msg="AGENTS.md passive index should not accumulate time-sensitive date state.",
        )

    def test_agents_include_retrieval_led_rule(self) -> None:
        text = AGENTS_PATH.read_text(encoding="utf-8")
        self.assertIn("Dirbk retrieval-led principu:", text)
        self.assertIn("workflow kontraktus, active rules / terminology locks, chapter state, repo-engineering state", text)
        self.assertIn("kanoninių repo artefaktų", text)

    def test_generated_term_candidates_lock_file_is_gitignored(self) -> None:
        text = GITIGNORE_PATH.read_text(encoding="utf-8")
        self.assertIn(".term_candidates.tsv.lock", text)

    def test_shell_portability_docs_reference_bash_and_not_zsh(self) -> None:
        for path, expected_fragments in SHELL_DOCS.items():
            text = path.read_text(encoding="utf-8")
            for fragment in expected_fragments:
                self.assertIn(fragment, text, msg=f"{path} is missing portability note: {fragment}")

    def test_post_bootstrap_python_docs_use_venv_entrypoints(self) -> None:
        books_readme = BOOKS_README_PATH.read_text(encoding="utf-8")
        self.assertIn(".venv/bin/python scripts/bootstrap_book_from_pdf.py", books_readme)
        self.assertIn(".venv/bin/python scripts/bootstrap_book_from_epub.py", books_readme)
        self.assertNotIn("python3 scripts/bootstrap_book_from_pdf.py", books_readme)
        self.assertNotIn("python3 scripts/bootstrap_book_from_epub.py", books_readme)

        codex_workflow = CODEX_WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn(".venv/bin/python scripts/print_codex_resume_prompt.py --mode engineering", codex_workflow)
        self.assertIn(".venv/bin/python scripts/print_codex_resume_prompt.py \\", codex_workflow)

        repo_workflow = REPO_ENGINEERING_WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn(".venv/bin/python scripts/update_engineering_ledger.py", repo_workflow)
        self.assertIn(".venv/bin/python scripts/write_codex_handoff.py", repo_workflow)
        self.assertIn(".venv/bin/python scripts/print_codex_resume_prompt.py --mode engineering", repo_workflow)

        translation_workflow = BOOK_TRANSLATION_WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn(".venv/bin/python scripts/print_codex_resume_prompt.py \\", translation_workflow)

    def test_translation_resume_docs_require_concrete_chapter(self) -> None:
        for path in (CODEX_WORKFLOW_PATH, BOOK_TRANSLATION_WORKFLOW_PATH, BOOKS_README_PATH):
            text = path.read_text(encoding="utf-8")
            self.assertIn(
                "reikalauja konkretaus `--chapter`",
                text,
                msg=f"{path} should require a concrete translation chapter.",
            )

    def test_handoffs_readme_keeps_local_scratchpad_semantics(self) -> None:
        text = HANDOFFS_README_PATH.read_text(encoding="utf-8")
        self.assertIn("lokalus `Codex` thread / worktree scratchpad inbox", text)
        self.assertIn("papildomas scratchpad", text)
        self.assertIn("nėra patikimas pirminis būdas pernešti būseną į naują worktree", text)
        self.assertNotIn("skirti išgyventi `context compaction` ir `Hand off` į naują worktree", text)

    def test_repo_engineering_workflow_docs_cover_no_active_theme(self) -> None:
        text = REPO_ENGINEERING_WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("`no-active-theme`", text)
        self.assertIn("Jei ledger turi aktyvią temą, tęsk ją", text)
        self.assertIn("jei aktyvios temos nėra", text)

    def test_workflow_docs_separate_static_and_dynamic_context(self) -> None:
        expected_dynamic_fragments = {
            CODEX_WORKFLOW_PATH: "Dynamic durable execution state:",
            REPO_ENGINEERING_WORKFLOW_PATH: "Dynamic durable execution state:",
            BOOK_TRANSLATION_WORKFLOW_PATH: "Dynamic durable execution state:",
        }
        for path, dynamic_fragment in expected_dynamic_fragments.items():
            text = path.read_text(encoding="utf-8")
            self.assertIn("Static passive repo context:", text, msg=f"{path} is missing static context guidance.")
            self.assertIn(dynamic_fragment, text, msg=f"{path} is missing durable state guidance.")
            self.assertIn("Non-canonical context:", text, msg=f"{path} is missing non-canonical context guidance.")
            self.assertIn("thread history", text, msg=f"{path} should explicitly demote thread history.")
            self.assertIn("workflow-specific", text, msg=f"{path} should explain that dynamic state is workflow-specific.")
            self.assertNotIn(
                "retrievable durable workflow context",
                text,
                msg=f"{path} should keep the Stage 1 memory-model terminology stable.",
            )

    def test_workflow_docs_keep_static_dynamic_split_consistent(self) -> None:
        codex_text = CODEX_WORKFLOW_PATH.read_text(encoding="utf-8")
        translation_text = BOOK_TRANSLATION_WORKFLOW_PATH.read_text(encoding="utf-8")
        engineering_text = REPO_ENGINEERING_WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertIn("kanoninių artefaktų", codex_text)
        self.assertIn("kanoninių chapter artefaktų", translation_text)
        self.assertIn("`ENGINEERING_LEDGER.md`", engineering_text)
        self.assertIn("o ne spėjama iš thread istorijos", engineering_text)

    def test_translation_workflow_uses_chapter_pack_term_and_concrete_path(self) -> None:
        for path in (CODEX_WORKFLOW_PATH, BOOK_TRANSLATION_WORKFLOW_PATH):
            text = path.read_text(encoding="utf-8")
            self.assertIn("chapter pack", text, msg=f"{path} should use the artifact-type term `chapter pack`.")
            self.assertIn("chapter_packs/<slug>.yaml", text, msg=f"{path} should name the concrete chapter pack path.")
            self.assertNotIn("`chapter_pack`", text, msg=f"{path} should avoid the legacy `chapter_pack` label.")

    def test_translation_workflow_docs_capture_guideline_freshness_guard(self) -> None:
        text = BOOK_TRANSLATION_WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("source / version / year / jurisdiction", text)
        self.assertIn("norminė informacija nesusimaišytų", text)

    def test_post_bootstrap_verification_contract_is_consistent(self) -> None:
        expected_modules = (
            "tests.test_workflow_runtime",
            "tests.test_obsidian_sync_safety",
            "tests.test_end_to_end_workflow_contract",
        )
        for path in (BOOKS_README_PATH, NEW_MAC_SETUP_PATH, BOOTSTRAP_MACOS_PATH):
            text = path.read_text(encoding="utf-8")
            self.assertIn(".venv/bin/python -m unittest", text, msg=f"{path} is missing the canonical unittest entrypoint.")
            for module in expected_modules:
                self.assertIn(module, text, msg=f"{path} is missing verification module: {module}")


if __name__ == "__main__":
    unittest.main()
