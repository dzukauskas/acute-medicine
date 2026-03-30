#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
TESTS_DIR = Path(__file__).resolve().parent
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

import run_chapter_qa  # noqa: E402
from workflow_subprocess import WorkflowSubprocessError  # noqa: E402
from workflow_test_utils import copy_mini_book, drop_local_termbase_entry, run_script, seed_canonical_artifacts, silence_stdio  # noqa: E402


EXPECTED_STEPS = [
    "inventory validation",
    "localization readiness",
    "figure manifest validation",
    "fresh chapter_pack build",
    "adjudication resolution",
    "terminology_guard",
    "localization_guard",
    "prose_guard",
    "lt_style_guard",
    "completeness_guard",
    "manual audit validation",
]


class RunChapterQaTests(unittest.TestCase):
    def test_main_runs_expected_steps_in_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            lt_path = tmp_path / "001-mini.md"
            lt_path.write_text("# LT\n", encoding="utf-8")
            pack_path = tmp_path / "001-mini.yaml"
            pack_path.write_text("chapter_slug: 001-mini\n", encoding="utf-8")
            labels: list[str] = []

            step_timeouts: dict[str, int] = {}

            def fake_run_step(label: str, _: list[str], *, timeout: int = run_chapter_qa.DEFAULT_TIMEOUT_SECONDS) -> None:
                labels.append(label)
                step_timeouts[label] = timeout

            with (
                patch.object(run_chapter_qa, "parse_args", return_value=Namespace(book_root=str(tmp_path / "book"), chapter="001-mini")),
                patch.object(run_chapter_qa, "activate_book_root"),
                patch.object(run_chapter_qa, "resolve_chapter_slug", return_value="001-mini"),
                patch.object(run_chapter_qa, "chapter_paths_for_slug", return_value={"lt": lt_path, "pack": pack_path}),
                patch.object(run_chapter_qa, "load_yaml", return_value={"chapter_slug": "001-mini"}),
                patch.object(run_chapter_qa, "normalize_yaml_structure", side_effect=lambda value: value),
                patch.object(run_chapter_qa, "run_step", side_effect=fake_run_step),
            ):
                with silence_stdio():
                    result = run_chapter_qa.main()

            self.assertEqual(result, 0)
            self.assertEqual(labels, EXPECTED_STEPS)
            self.assertEqual(step_timeouts["fresh chapter_pack build"], run_chapter_qa.LONG_TIMEOUT_SECONDS)
            self.assertEqual(step_timeouts["adjudication resolution"], run_chapter_qa.LONG_TIMEOUT_SECONDS)
            self.assertEqual(step_timeouts["inventory validation"], run_chapter_qa.DEFAULT_TIMEOUT_SECONDS)

    def test_main_fails_fast_on_first_failed_step(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            lt_path = tmp_path / "001-mini.md"
            lt_path.write_text("# LT\n", encoding="utf-8")
            pack_path = tmp_path / "001-mini.yaml"
            pack_path.write_text("chapter_slug: 001-mini\n", encoding="utf-8")
            labels: list[str] = []

            def fake_run_step(label: str, _: list[str], *, timeout: int = run_chapter_qa.DEFAULT_TIMEOUT_SECONDS) -> None:
                labels.append(label)
                if label == "localization readiness":
                    raise RuntimeError("localization readiness failed with exit code 1.")

            with (
                patch.object(run_chapter_qa, "parse_args", return_value=Namespace(book_root=str(tmp_path / "book"), chapter="001-mini")),
                patch.object(run_chapter_qa, "activate_book_root"),
                patch.object(run_chapter_qa, "resolve_chapter_slug", return_value="001-mini"),
                patch.object(run_chapter_qa, "chapter_paths_for_slug", return_value={"lt": lt_path, "pack": pack_path}),
                patch.object(run_chapter_qa, "load_yaml", return_value={"chapter_slug": "001-mini"}),
                patch.object(run_chapter_qa, "normalize_yaml_structure", side_effect=lambda value: value),
                patch.object(run_chapter_qa, "run_step", side_effect=fake_run_step),
            ):
                with silence_stdio():
                    with self.assertRaises(RuntimeError):
                        run_chapter_qa.main()

            self.assertEqual(labels, ["inventory validation", "localization readiness"])

    def test_run_step_surfaces_timeout_message(self) -> None:
        with patch.object(
            run_chapter_qa,
            "run_subprocess",
            side_effect=WorkflowSubprocessError("inventory validation timed out after 30s while running `python step.py`."),
        ):
            with self.assertRaises(RuntimeError) as ctx:
                run_chapter_qa.run_step("inventory validation", ["python", "step.py"])

        self.assertIn("timed out after 30s", str(ctx.exception))

    def test_main_rejects_stale_canonical_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            lt_path = tmp_path / "001-mini.md"
            lt_path.write_text("# LT\n", encoding="utf-8")
            pack_path = tmp_path / "001-mini.yaml"
            pack_path.write_text("chapter_slug: 001-mini\n", encoding="utf-8")

            def fake_load_yaml(path: Path) -> dict[str, str]:
                if path == pack_path:
                    return {"version": "canonical"}
                return {"version": "fresh"}

            with (
                patch.object(run_chapter_qa, "parse_args", return_value=Namespace(book_root=str(tmp_path / "book"), chapter="001-mini")),
                patch.object(run_chapter_qa, "activate_book_root"),
                patch.object(run_chapter_qa, "resolve_chapter_slug", return_value="001-mini"),
                patch.object(run_chapter_qa, "chapter_paths_for_slug", return_value={"lt": lt_path, "pack": pack_path}),
                patch.object(run_chapter_qa, "load_yaml", side_effect=fake_load_yaml),
                patch.object(run_chapter_qa, "normalize_yaml_structure", side_effect=lambda value: value),
                patch.object(run_chapter_qa, "run_step"),
            ):
                with silence_stdio():
                    with self.assertRaises(SystemExit) as ctx:
                        run_chapter_qa.main()

            self.assertIn("Kanoninis chapter_pack pasenęs", str(ctx.exception))

    def test_cli_rejects_stale_canonical_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = copy_mini_book(Path(tmp_dir))
            slug = seed_canonical_artifacts(book_root)
            pack_path = book_root / "chapter_packs" / f"{slug}.yaml"
            pack_path.write_text(pack_path.read_text(encoding="utf-8") + "stale_marker: true\n", encoding="utf-8")

            result = run_script("run_chapter_qa.py", "--book-root", str(book_root), slug)

            self.assertEqual(result.returncode, 1)
            self.assertIn("Kanoninis chapter_pack pasenęs", result.stdout + result.stderr)

    def test_cli_blocks_unresolved_high_risk_term_before_qa(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            book_root = copy_mini_book(Path(tmp_dir))
            slug = seed_canonical_artifacts(book_root)
            drop_local_termbase_entry(book_root, "Sentinel Pathway")

            result = run_script("run_chapter_qa.py", "--book-root", str(book_root), slug)

            self.assertEqual(result.returncode, 1)
            self.assertIn("fresh chapter_pack build failed", result.stdout + result.stderr)
            self.assertIn("Sentinel Pathway", result.stdout + result.stderr)
            self.assertIn("liko neužrakintas", result.stdout + result.stderr)
