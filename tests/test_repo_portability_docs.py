#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS_PATH = REPO_ROOT / "AGENTS.md"
SHELL_DOCS = {
    REPO_ROOT / "docs" / "new-mac-setup.md": (
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

    def test_shell_portability_docs_reference_bash_and_not_zsh(self) -> None:
        for path, expected_fragments in SHELL_DOCS.items():
            text = path.read_text(encoding="utf-8")
            for fragment in expected_fragments:
                self.assertIn(fragment, text, msg=f"{path} is missing portability note: {fragment}")


if __name__ == "__main__":
    unittest.main()
