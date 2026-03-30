#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timezone
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

import write_codex_handoff  # noqa: E402
from workflow_test_utils import silence_stdio  # noqa: E402


class WriteCodexHandoffTests(unittest.TestCase):
    def test_default_output_path_uses_timestamp_and_branch_slug(self) -> None:
        generated_at = datetime(2026, 3, 30, 9, 45, 0, tzinfo=timezone.utc)
        path = write_codex_handoff.default_output_path("codex/Parallel Fix", generated_at)
        self.assertEqual(
            path,
            write_codex_handoff.HANDOFFS_DIR / "20260330-094500-codex-parallel-fix.md",
        )

    def test_render_handoff_embeds_book_workflow_and_git_snapshot(self) -> None:
        book_root = REPO_ROOT / "books" / "jrcalc-clinical-guidelines-2025-reference-edition"
        snapshot = write_codex_handoff.GitSnapshot(
            branch="codex/research-pass",
            head="abc123def456",
            worktree=REPO_ROOT,
            status_lines=[" M docs/codex-workflow.md", "?? handoffs/example.md"],
            recent_commits=["abc123 Add docs", "def456 Fix tests"],
        )

        rendered = write_codex_handoff.render_handoff(
            title="Research pass handoff",
            generated_at=datetime(2026, 3, 30, 12, 0, 0, tzinfo=timezone.utc),
            snapshot=snapshot,
            book_root=book_root,
            goal="Užbaigti Codex thread continuity workflow.",
            completed=["Pridėtas handoff skriptas."],
            next_steps=["Peržiūrėti naują dokumentaciją."],
            risks=["Reikia patikrinti, ar startup tvarka aiški naujam thread."],
        )

        self.assertIn("# Research pass handoff", rendered)
        self.assertIn("books/jrcalc-clinical-guidelines-2025-reference-edition/workflow.md", rendered)
        self.assertIn(" M docs/codex-workflow.md", rendered)
        self.assertIn("abc123 Add docs", rendered)
        self.assertIn("Pridėtas handoff skriptas.", rendered)

    def test_main_writes_handoff_file(self) -> None:
        snapshot = write_codex_handoff.GitSnapshot(
            branch="codex/handoff",
            head="feedbeef",
            worktree=REPO_ROOT,
            status_lines=[],
            recent_commits=["feedbee Add handoff workflow"],
        )

        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            output_path = Path(tmp_dir) / "handoff.md"
            with patch.object(write_codex_handoff, "collect_git_snapshot", return_value=snapshot):
                with silence_stdio():
                    exit_code = write_codex_handoff.main(
                        [
                            "--title",
                            "Codex continuity",
                            "--goal",
                            "Išlaikyti būseną tarp thread ir worktree.",
                            "--completed",
                            "Paruoštas skripto skeletas.",
                            "--next-step",
                            "Paleisti testus.",
                            "--risk",
                            "Reikia aiškios dokumentacijos.",
                            "--generated-at",
                            "2026-03-30T12:30:00+00:00",
                            "--output",
                            str(output_path),
                        ]
                    )

            self.assertEqual(exit_code, 0)
            text = output_path.read_text(encoding="utf-8")
            self.assertIn("# Codex continuity", text)
            self.assertIn("Išlaikyti būseną tarp thread ir worktree.", text)
            self.assertIn("Paruoštas skripto skeletas.", text)
            self.assertIn("Paleisti testus.", text)
            self.assertIn("Reikia aiškios dokumentacijos.", text)


if __name__ == "__main__":
    unittest.main()
