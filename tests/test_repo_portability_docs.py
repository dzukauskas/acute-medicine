#!/usr/bin/env python3
from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS_PATH = REPO_ROOT / "AGENTS.md"
NEW_MAC_SETUP_PATH = REPO_ROOT / "docs" / "new-mac-setup.md"
CODEX_WORKFLOW_PATH = REPO_ROOT / "docs" / "codex-workflow.md"
REPO_ENGINEERING_WORKFLOW_PATH = REPO_ROOT / "docs" / "repo-engineering-workflow.md"
BOOKS_README_PATH = REPO_ROOT / "books" / "README.md"
BOOTSTRAP_MACOS_PATH = REPO_ROOT / "scripts" / "bootstrap_macos.sh"
SETUP_CODEX_MCP_PATH = REPO_ROOT / "scripts" / "setup_codex_mcp.sh"
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

    def test_repo_engineering_workflow_docs_cover_no_active_theme(self) -> None:
        text = REPO_ENGINEERING_WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("`no-active-theme`", text)
        self.assertIn("Jei ledger turi aktyvią temą, tęsk ją", text)
        self.assertIn("jei aktyvios temos nėra", text)

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
