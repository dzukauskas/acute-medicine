#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
TESTS_DIR = REPO_ROOT / "tests"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

import check_engineering_ledger_checkpoint as checkpoint  # noqa: E402


def render_ledger(
    *,
    theme: str = "no-active-theme",
    branch: str = "main",
    last_updated: str = "2026-04-03T20:15:05+03:00",
    summary: str = "- Narrow summary.",
    current_state: str = "- Current state.",
    decisions: str = "- Accepted decision.",
    next_steps: str = "- Next step.",
    risks: str = "- Open risk.",
    completed: str = "- _No completed engineering themes recorded._",
) -> str:
    return f"""# Engineering Ledger

## Active Theme
<!-- ledger:active_theme:start -->
- Theme: {theme}
- Branch: {branch}
- Last updated: {last_updated}
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
{summary}
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
{current_state}
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
{decisions}
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
{next_steps}
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
{risks}
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
{completed}
<!-- ledger:completed:end -->
"""


class CheckEngineeringLedgerCheckpointUnitTests(unittest.TestCase):
    def test_is_repo_engineering_path_uses_single_source_of_truth(self) -> None:
        self.assertTrue(checkpoint.is_repo_engineering_path("docs/repo-engineering-workflow.md"))
        self.assertTrue(checkpoint.is_repo_engineering_path("books/_template/workflow.md"))
        self.assertTrue(checkpoint.is_repo_engineering_path("ENGINEERING_LEDGER.md"))
        self.assertFalse(
            checkpoint.is_repo_engineering_path(
                "books/jrcalc-clinical-guidelines-2025-reference-edition/lt/chapters/001-disclaimer.md"
            )
        )

    def test_guard_trigger_paths_ignore_ledger_only(self) -> None:
        self.assertEqual(checkpoint.guard_trigger_paths(["ENGINEERING_LEDGER.md"]), [])
        self.assertEqual(
            checkpoint.guard_trigger_paths(["ENGINEERING_LEDGER.md", "docs/repo-engineering-workflow.md"]),
            ["docs/repo-engineering-workflow.md"],
        )

    def test_meaningful_changed_sections_accept_summary_and_current_state(self) -> None:
        before = render_ledger()
        after = render_ledger(summary="- Updated summary.", current_state="- Updated state.")
        self.assertEqual(
            checkpoint.meaningful_changed_sections(before, after),
            ["Summary", "Current State"],
        )

    def test_meaningful_changed_sections_accept_active_theme_theme_line_only(self) -> None:
        before = render_ledger(theme="theme-a")
        after = render_ledger(theme="theme-b")
        self.assertEqual(checkpoint.meaningful_changed_sections(before, after), ["Active Theme"])

    def test_meaningful_changed_sections_ignore_last_updated_only(self) -> None:
        before = render_ledger(last_updated="2026-04-03T20:15:05+03:00")
        after = render_ledger(last_updated="2026-04-03T21:00:00+03:00")
        self.assertEqual(checkpoint.meaningful_changed_sections(before, after), [])

    def test_meaningful_changed_sections_ignore_branch_only(self) -> None:
        before = render_ledger(branch="main")
        after = render_ledger(branch="codex/branch")
        self.assertEqual(checkpoint.meaningful_changed_sections(before, after), [])

    def test_meaningful_changed_sections_ignore_decisions_and_risks_only(self) -> None:
        before = render_ledger()
        after = render_ledger(decisions="- Another decision.", risks="- Another risk.")
        self.assertEqual(checkpoint.meaningful_changed_sections(before, after), [])

    def test_meaningful_changed_sections_ignore_whitespace_only_churn(self) -> None:
        before = render_ledger(summary="- Summary line.\n- Another line.", completed="### 2026-04-03 20:00 | theme\n- Closed.")
        after = render_ledger(
            summary="  - Summary line.  \n\n - Another line.   ",
            completed="### 2026-04-03 20:00 | theme  \n  - Closed.   ",
        )
        self.assertEqual(checkpoint.meaningful_changed_sections(before, after), [])


class CheckEngineeringLedgerCheckpointCLITests(unittest.TestCase):
    def write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def init_repo(self, repo_root: Path) -> None:
        subprocess.run(["git", "init", "-b", "main"], cwd=repo_root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.name", "Codex Tests"], cwd=repo_root, check=True)
        subprocess.run(["git", "config", "user.email", "codex@example.com"], cwd=repo_root, check=True)
        (repo_root / "scripts").mkdir(parents=True, exist_ok=True)
        for name in (
            "check_engineering_ledger_checkpoint.py",
            "workflow_engineering_ledger.py",
            "workflow_runtime.py",
        ):
            shutil.copy2(SCRIPTS_DIR / name, repo_root / "scripts" / name)

    def commit_all(self, repo_root: Path, message: str) -> str:
        subprocess.run(["git", "add", "."], cwd=repo_root, check=True)
        subprocess.run(["git", "commit", "-m", message], cwd=repo_root, check=True, capture_output=True, text=True)
        return (
            subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=repo_root,
                check=True,
                capture_output=True,
                text=True,
            )
            .stdout.strip()
        )

    def run_checker(self, repo_root: Path, base_ref: str, head_ref: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(repo_root / "scripts" / "check_engineering_ledger_checkpoint.py"),
                "--base-ref",
                base_ref,
                "--head-ref",
                head_ref,
            ],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )

    def test_cli_uses_same_merge_base_window_for_diff_and_ledger(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)
            self.write(repo_root / "ENGINEERING_LEDGER.md", render_ledger(summary="- Merge-base summary."))
            self.write(repo_root / "docs" / "guide.md", "base\n")
            base_commit = self.commit_all(repo_root, "base")

            subprocess.run(["git", "checkout", "-b", "feature"], cwd=repo_root, check=True, capture_output=True, text=True)
            self.write(repo_root / "docs" / "guide.md", "feature change\n")
            head_commit = self.commit_all(repo_root, "feature change")

            subprocess.run(["git", "checkout", "main"], cwd=repo_root, check=True, capture_output=True, text=True)
            self.write(repo_root / "ENGINEERING_LEDGER.md", render_ledger(summary="- Main branch moved ahead."))
            advanced_base = self.commit_all(repo_root, "main ledger change")

            result = self.run_checker(repo_root, advanced_base, head_commit)

            self.assertEqual(result.returncode, checkpoint.EXIT_POLICY, msg=result.stdout + result.stderr)
            self.assertIn("Repo-engineering diff requires a meaningful `ENGINEERING_LEDGER.md` checkpoint.", result.stdout)
            self.assertIn("docs/guide.md", result.stdout)

    def test_cli_passes_for_ledger_only_diff(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)
            self.write(repo_root / "ENGINEERING_LEDGER.md", render_ledger(summary="- Base summary."))
            base_commit = self.commit_all(repo_root, "base")

            self.write(repo_root / "ENGINEERING_LEDGER.md", render_ledger(summary="- Updated summary."))
            head_commit = self.commit_all(repo_root, "ledger only")

            result = self.run_checker(repo_root, base_commit, head_commit)

            self.assertEqual(result.returncode, checkpoint.EXIT_OK, msg=result.stdout + result.stderr)
            self.assertIn("skipped", result.stdout)

    def test_cli_fails_for_bad_refs(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)
            self.write(repo_root / "ENGINEERING_LEDGER.md", render_ledger())
            self.commit_all(repo_root, "base")

            result = self.run_checker(repo_root, "missing-base", "missing-head")

            self.assertEqual(result.returncode, checkpoint.EXIT_GIT_ERROR, msg=result.stdout + result.stderr)
            self.assertIn("Nepavyko rasti base ref", result.stderr)

    def test_cli_fails_when_merge_base_is_missing(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)
            self.write(repo_root / "ENGINEERING_LEDGER.md", render_ledger())
            self.commit_all(repo_root, "base")

            subprocess.run(["git", "checkout", "--orphan", "other-root"], cwd=repo_root, check=True, capture_output=True, text=True)
            subprocess.run(["git", "rm", "-rf", "."], cwd=repo_root, check=True, capture_output=True, text=True)
            self.write(repo_root / "ENGINEERING_LEDGER.md", render_ledger(summary="- Orphan summary."))
            orphan_commit = self.commit_all(repo_root, "orphan")
            subprocess.run(["git", "checkout", "main"], cwd=repo_root, check=True, capture_output=True, text=True)
            main_commit = (
                subprocess.run(
                    ["git", "rev-parse", "main"],
                    cwd=repo_root,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                .stdout.strip()
            )

            result = self.run_checker(repo_root, main_commit, orphan_commit)

            self.assertEqual(result.returncode, checkpoint.EXIT_GIT_ERROR, msg=result.stdout + result.stderr)
            self.assertIn("Nepavyko rasti merge-base", result.stderr)

    def test_cli_fails_when_ledger_is_missing_at_diff_boundary(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)
            self.write(repo_root / "ENGINEERING_LEDGER.md", render_ledger())
            self.write(repo_root / "docs" / "guide.md", "base\n")
            base_commit = self.commit_all(repo_root, "base")

            self.write(repo_root / "docs" / "guide.md", "changed\n")
            (repo_root / "ENGINEERING_LEDGER.md").unlink()
            head_commit = self.commit_all(repo_root, "remove ledger")

            result = self.run_checker(repo_root, base_commit, head_commit)

            self.assertEqual(result.returncode, checkpoint.EXIT_GIT_ERROR, msg=result.stdout + result.stderr)
            self.assertIn("Nepavyko perskaityti `ENGINEERING_LEDGER.md`", result.stderr)


if __name__ == "__main__":
    unittest.main()
