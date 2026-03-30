#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import workflow_subprocess  # noqa: E402


class WorkflowSubprocessTests(unittest.TestCase):
    def test_run_subprocess_passes_timeout_to_subprocess_run(self) -> None:
        seen_timeouts: list[int] = []

        def fake_run(*_args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
            seen_timeouts.append(int(kwargs["timeout"]))
            return subprocess.CompletedProcess(["echo", "ok"], 0, stdout="", stderr="")

        with patch.object(workflow_subprocess.subprocess, "run", side_effect=fake_run):
            workflow_subprocess.run_subprocess(
                ["echo", "ok"],
                phase="demo phase",
                timeout=42,
                capture_output=True,
                text=True,
            )

        self.assertEqual(seen_timeouts, [42])

    def test_run_subprocess_raises_clear_timeout_error(self) -> None:
        with patch.object(
            workflow_subprocess.subprocess,
            "run",
            side_effect=subprocess.TimeoutExpired(["sleep", "10"], 42),
        ):
            with self.assertRaises(workflow_subprocess.WorkflowSubprocessError) as ctx:
                workflow_subprocess.run_subprocess(
                    ["sleep", "10"],
                    phase="demo phase",
                    timeout=42,
                )

        self.assertIn("demo phase timed out after 42s", str(ctx.exception))
        self.assertIn("sleep 10", str(ctx.exception))

    def test_run_checked_subprocess_includes_stdout_and_stderr(self) -> None:
        completed = subprocess.CompletedProcess(
            ["demo-tool", "--flag"],
            7,
            stdout="useful stdout",
            stderr="useful stderr",
        )

        with patch.object(workflow_subprocess, "run_subprocess", return_value=completed):
            with self.assertRaises(workflow_subprocess.WorkflowSubprocessError) as ctx:
                workflow_subprocess.run_checked_subprocess(
                    ["demo-tool", "--flag"],
                    phase="demo phase",
                    timeout=55,
                    capture_output=True,
                    text=True,
                )

        self.assertIn("demo phase failed with exit code 7", str(ctx.exception))
        self.assertIn("stderr:\nuseful stderr", str(ctx.exception))
        self.assertIn("stdout:\nuseful stdout", str(ctx.exception))
