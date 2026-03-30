#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_adjudication_resolution  # noqa: E402
from workflow_subprocess import WorkflowSubprocessError  # noqa: E402


class ValidateAdjudicationResolutionTests(unittest.TestCase):
    def write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def research_text(self, decision_line: str) -> str:
        return (
            "# Test\n\n"
            "## Adjudication sprendimai\n\n"
            f"{decision_line}\n"
        )

    def test_accepts_machine_readable_decision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            research_path = Path(tmp_dir) / "research.md"
            self.write(research_path, self.research_text("- block-1 | A | Aiški priežastis"))

            errors = validate_adjudication_resolution.validate_research_decisions(research_path, ["block-1"])

            self.assertEqual(errors, [])

    def test_rejects_invalid_choice(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            research_path = Path(tmp_dir) / "research.md"
            self.write(research_path, self.research_text("- block-1 | C | Neteisingas pasirinkimas"))

            errors = validate_adjudication_resolution.validate_research_decisions(research_path, ["block-1"])

            self.assertEqual(len(errors), 1)
            self.assertIn("neleistiną pasirinkimą `C`", errors[0])

    def test_reports_missing_candidate_decision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            research_path = Path(tmp_dir) / "research.md"
            self.write(research_path, "# Test\n\n## Adjudication sprendimai\n\n")

            errors = validate_adjudication_resolution.validate_research_decisions(research_path, ["block-1"])

            self.assertEqual(len(errors), 1)
            self.assertIn("trūksta adjudication sprendimo block `block-1`", errors[0])

    def test_run_build_surfaces_timeout_message(self) -> None:
        with patch.object(
            validate_adjudication_resolution,
            "run_subprocess",
            side_effect=WorkflowSubprocessError(
                "fresh adjudication_pack build timed out after 900s while running `python build_adjudication_pack.py`."
            ),
        ):
            with self.assertRaises(SystemExit) as ctx:
                validate_adjudication_resolution.run_build("/tmp/book", "001-mini", Path("/tmp/out.yaml"))

        self.assertIn("timed out after 900s", str(ctx.exception))
