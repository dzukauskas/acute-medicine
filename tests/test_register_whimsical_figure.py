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

import register_whimsical_figure as register_whimsical  # noqa: E402
import workflow_figures as workflow_figures  # noqa: E402


class RegisterWhimsicalFigureTests(unittest.TestCase):
    def write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def make_book_root(self, repo_root: Path) -> Path:
        book_root = repo_root / "books" / "test-book"
        self.write(
            book_root / "source" / "index" / "figures.tsv",
            "\n".join(
                [
                    "source_figure_id\tchapter_slug\tsource_href\tasset_path\tmedia_type\talt_text\tcaption_text\tnotes",
                    "001-mini-fig-01\t001-mini\tchapter.xhtml\tsource/figures-raw/001-mini-fig-01.jpg\timage/jpeg\tKvėpavimo takų algoritmas\t\t",
                    "",
                ]
            ),
        )
        self.write(
            book_root / "lt" / "figures" / "manifest.tsv",
            "figure_id\tfigure_number\tpng_path\tcanonical_source_type\tcanonical_source_path\tnotes\n",
        )
        self.write(
            book_root / "lt" / "chapters" / "001-mini.md",
            "# Mini skyrius\n\n## 1.1 paveikslas\n\n1. Atverkite kvėpavimo takus.\n",
        )
        return book_root

    def test_main_registers_and_embeds_figure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir).resolve()
            book_root = self.make_book_root(repo_root)
            storage_state = repo_root / "storage-state.json"
            stdout = io.StringIO()

            def fake_repo_relative(path: Path) -> str:
                return path.resolve().relative_to(repo_root).as_posix()

            with (
                patch.object(
                    register_whimsical,
                    "parse_args",
                    return_value=Namespace(
                        book_root=str(book_root),
                        source_figure_id="001-mini-fig-01",
                        figure_number="1.1",
                        whimsical_url="https://whimsical.com/example-board",
                        notes=None,
                        storage_state=storage_state,
                        login=True,
                        sync_obsidian=False,
                        obsidian_dest=None,
                    ),
                ),
                patch.object(register_whimsical, "repo_relative_path", side_effect=fake_repo_relative),
                patch.object(register_whimsical, "render_registered_figure") as render_mock,
                patch.object(workflow_figures, "REPO_ROOT", repo_root),
                redirect_stdout(stdout),
                redirect_stderr(io.StringIO()),
            ):
                result = register_whimsical.main()

            self.assertEqual(result, 0)
            render_mock.assert_called_once_with(
                book_root,
                "figure-1-1-001-mini-fig-01",
                storage_state=storage_state,
                login=True,
            )
            manifest_text = (book_root / "lt" / "figures" / "manifest.tsv").read_text(encoding="utf-8")
            self.assertIn("figure-1-1-001-mini-fig-01", manifest_text)
            chapter_text = (book_root / "lt" / "chapters" / "001-mini.md").read_text(encoding="utf-8")
            self.assertIn("![Kvėpavimo takų algoritmas](../figures/figure-1-1-001-mini-fig-01.png)", chapter_text)
            self.assertIn("Repo completion succeeded (manifest + PNG + chapter embed)", stdout.getvalue())

    def test_main_rolls_back_manifest_when_embed_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir).resolve()
            book_root = repo_root / "books" / "test-book"
            self.write(
                book_root / "source" / "index" / "figures.tsv",
                "\n".join(
                    [
                        "source_figure_id\tchapter_slug\tsource_href\tasset_path\tmedia_type\talt_text\tcaption_text\tnotes",
                        "001-mini-fig-01\t001-mini\tchapter.xhtml\tsource/figures-raw/001-mini-fig-01.jpg\timage/jpeg\t\t\t",
                        "",
                    ]
                ),
            )
            self.write(
                book_root / "lt" / "figures" / "manifest.tsv",
                "figure_id\tfigure_number\tpng_path\tcanonical_source_type\tcanonical_source_path\tnotes\n",
            )

            def fake_repo_relative(path: Path) -> str:
                return path.resolve().relative_to(repo_root).as_posix()

            with (
                patch.object(
                    register_whimsical,
                    "parse_args",
                    return_value=Namespace(
                        book_root=str(book_root),
                        source_figure_id="001-mini-fig-01",
                        figure_number="1.1",
                        whimsical_url="https://whimsical.com/example-board",
                        notes=None,
                        storage_state=None,
                        login=False,
                        sync_obsidian=False,
                        obsidian_dest=None,
                    ),
                ),
                patch.object(register_whimsical, "repo_relative_path", side_effect=fake_repo_relative),
                patch.object(register_whimsical, "render_registered_figure"),
                patch.object(workflow_figures, "REPO_ROOT", repo_root),
                redirect_stdout(io.StringIO()),
                redirect_stderr(io.StringIO()),
            ):
                with self.assertRaises(SystemExit) as ctx:
                    register_whimsical.main()

            self.assertIn("Nerastas LT skyrius aktyviam paveikslui", str(ctx.exception))
            manifest_text = (book_root / "lt" / "figures" / "manifest.tsv").read_text(encoding="utf-8")
            self.assertEqual(
                manifest_text,
                "figure_id\tfigure_number\tpng_path\tcanonical_source_type\tcanonical_source_path\tnotes\n",
            )


if __name__ == "__main__":
    unittest.main()
