#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import run_chapter_qa  # noqa: E402


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

            def fake_run_step(label: str, _: list[str]) -> None:
                labels.append(label)

            with (
                patch.object(run_chapter_qa, "parse_args", return_value=Namespace(book_root=str(tmp_path / "book"), chapter="001-mini")),
                patch.object(run_chapter_qa, "activate_book_root"),
                patch.object(run_chapter_qa, "resolve_chapter_slug", return_value="001-mini"),
                patch.object(run_chapter_qa, "chapter_paths_for_slug", return_value={"lt": lt_path, "pack": pack_path}),
                patch.object(run_chapter_qa, "load_yaml", return_value={"chapter_slug": "001-mini"}),
                patch.object(run_chapter_qa, "normalize_yaml_structure", side_effect=lambda value: value),
                patch.object(run_chapter_qa, "run_step", side_effect=fake_run_step),
            ):
                result = run_chapter_qa.main()

            self.assertEqual(result, 0)
            self.assertEqual(labels, EXPECTED_STEPS)

    def test_main_fails_fast_on_first_failed_step(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            lt_path = tmp_path / "001-mini.md"
            lt_path.write_text("# LT\n", encoding="utf-8")
            pack_path = tmp_path / "001-mini.yaml"
            pack_path.write_text("chapter_slug: 001-mini\n", encoding="utf-8")
            labels: list[str] = []

            def fake_run_step(label: str, _: list[str]) -> None:
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
                with self.assertRaises(RuntimeError):
                    run_chapter_qa.main()

            self.assertEqual(labels, ["inventory validation", "localization readiness"])

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
                with self.assertRaises(SystemExit) as ctx:
                    run_chapter_qa.main()

            self.assertIn("Kanoninis chapter_pack pasenęs", str(ctx.exception))
