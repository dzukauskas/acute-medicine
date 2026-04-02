#!/usr/bin/env python3
from __future__ import annotations

import io
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stderr, redirect_stdout
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

import validate_figures_manifest as validate_figures  # noqa: E402
import workflow_figures as workflow_figures  # noqa: E402


class ValidateFiguresManifestTests(unittest.TestCase):
    def write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def make_book_root(self, repo_root: Path, *, with_embed: bool) -> tuple[Path, Path]:
        book_root = repo_root / "books" / "test-book"
        manifest_path = book_root / "lt" / "figures" / "manifest.tsv"
        image_ref = "![1.1 paveikslas](../figures/figure-1.png)\n" if with_embed else ""
        self.write(
            book_root / "lt" / "chapters" / "001-mini.md",
            f"# Mini skyrius\n\n## 1.1 paveikslas\n\n{image_ref}",
        )
        self.write(
            manifest_path,
            "\n".join(
                [
                    "figure_id\tfigure_number\tpng_path\tcanonical_source_type\tcanonical_source_path\tnotes",
                    "figure-1\t1.1\tbooks/test-book/lt/figures/figure-1.png\twhimsical_board\thttps://whimsical.com/example-board\tsource_figure_id=001-mini-fig-01; chapter_slug=001-mini",
                    "",
                ]
            ),
        )
        (book_root / "lt" / "figures" / "figure-1.png").parent.mkdir(parents=True, exist_ok=True)
        (book_root / "lt" / "figures" / "figure-1.png").write_bytes(b"png")
        self.write(book_root / "source" / "chapters-en" / "001-mini.md", "# Source\n")
        return book_root, manifest_path

    def test_main_fails_when_active_manifest_figure_is_not_embedded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir).resolve()
            book_root, manifest_path = self.make_book_root(repo_root, with_embed=False)
            stderr = io.StringIO()

            with (
                patch.object(validate_figures, "REPO_ROOT", repo_root),
                patch.object(workflow_figures, "REPO_ROOT", repo_root),
                patch.object(
                    validate_figures,
                    "parse_args",
                    return_value=Namespace(book_root=str(book_root), chapter="001-mini", manifest=manifest_path),
                ),
                redirect_stdout(io.StringIO()),
                redirect_stderr(stderr),
            ):
                result = validate_figures.main()

        self.assertEqual(result, 1)
        self.assertIn("aktyvus manifest paveikslas neįterptas į skyrių", stderr.getvalue())

    def test_main_validates_global_embed_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir).resolve()
            book_root, manifest_path = self.make_book_root(repo_root, with_embed=True)
            stdout = io.StringIO()

            with (
                patch.object(validate_figures, "REPO_ROOT", repo_root),
                patch.object(workflow_figures, "REPO_ROOT", repo_root),
                patch.object(
                    validate_figures,
                    "parse_args",
                    return_value=Namespace(book_root=str(book_root), chapter=None, manifest=manifest_path),
                ),
                redirect_stdout(stdout),
                redirect_stderr(io.StringIO()),
            ):
                result = validate_figures.main()

        self.assertEqual(result, 0)
        self.assertIn("Figure manifest and chapter embed contract valid.", stdout.getvalue())

    def test_main_validates_single_chapter_contract_with_book_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir).resolve()
            book_root, manifest_path = self.make_book_root(repo_root, with_embed=True)
            stdout = io.StringIO()

            with (
                patch.object(validate_figures, "REPO_ROOT", repo_root),
                patch.object(workflow_figures, "REPO_ROOT", repo_root),
                patch.object(
                    validate_figures,
                    "parse_args",
                    return_value=Namespace(book_root=str(book_root), chapter="001", manifest=manifest_path),
                ),
                redirect_stdout(stdout),
                redirect_stderr(io.StringIO()),
            ):
                result = validate_figures.main()

        self.assertEqual(result, 0)
        self.assertIn("Figure manifest valid and chapter image refs resolved for 001-mini.", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
