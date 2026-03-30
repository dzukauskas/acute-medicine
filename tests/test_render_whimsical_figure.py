#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
TESTS_DIR = Path(__file__).resolve().parent

HAS_RENDER_RUNTIME_DEPS = (
    importlib.util.find_spec("PIL") is not None
    and importlib.util.find_spec("playwright") is not None
)

import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

if HAS_RENDER_RUNTIME_DEPS:
    import render_whimsical_figure as render_whimsical  # noqa: E402
else:
    render_whimsical = None

from workflow_test_utils import silence_stdio  # noqa: E402


@unittest.skipUnless(HAS_RENDER_RUNTIME_DEPS, "requires Pillow and playwright")
class RenderWhimsicalFigureTests(unittest.TestCase):
    def write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def make_book_root(self, base_dir: Path) -> tuple[Path, Path]:
        repo_root = base_dir
        book_root = repo_root / "books" / "test-book"
        (book_root / "lt" / "figures").mkdir(parents=True, exist_ok=True)
        manifest_path = book_root / "lt" / "figures" / "manifest.tsv"
        self.write(
            manifest_path,
            "\n".join(
                [
                    "figure_id\tfigure_number\tpng_path\tcanonical_source_type\tcanonical_source_path\tnotes",
                    "figure-1\t1.1\tbooks/test-book/lt/figures/figure-1.png\twhimsical_board\thttps://whimsical.com/example-board\t",
                    "",
                ]
            ),
        )
        return book_root, manifest_path

    def test_main_returns_after_login_without_figure_id(self) -> None:
        storage_state = Path("/tmp/render-whimsical-login.json")

        with (
            patch.object(
                render_whimsical,
                "parse_args",
                return_value=Namespace(
                    figure_id=None,
                    book_root="/tmp/test-book",
                    manifest=None,
                    storage_state=storage_state,
                    login=True,
                    width=2400,
                    padding=72,
                    sync_obsidian=False,
                    obsidian_dest=None,
                ),
            ),
            patch.object(render_whimsical, "login_whimsical") as login_mock,
        ):
            with silence_stdio():
                result = render_whimsical.main()

        self.assertEqual(result, 0)
        login_mock.assert_called_once_with(storage_state)

    def test_main_falls_back_to_inkscape_after_browser_render_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            book_root, manifest_path = self.make_book_root(temp_root)
            converted: list[tuple[Path, Path, int]] = []

            def fake_convert(svg_path: Path, png_path: Path, width: int) -> None:
                converted.append((svg_path, png_path, width))
                png_path.write_bytes(b"png")

            with (
                patch.object(render_whimsical, "REPO_ROOT", temp_root),
                patch.object(
                    render_whimsical,
                    "parse_args",
                    return_value=Namespace(
                        figure_id="figure-1",
                        book_root=str(book_root),
                        manifest=manifest_path,
                        storage_state=Path("/tmp/storage-state.json"),
                        login=False,
                        width=1800,
                        padding=48,
                        sync_obsidian=False,
                        obsidian_dest=None,
                    ),
                ),
                patch.object(render_whimsical, "fetch_svg", return_value='<svg width="100" height="50"></svg>'),
                patch.object(render_whimsical, "render_svg_to_png_browser", side_effect=RuntimeError("browser render failed")),
                patch.object(render_whimsical, "ensure_inkscape") as ensure_inkscape_mock,
                patch.object(render_whimsical, "convert_svg_to_png", side_effect=fake_convert),
            ):
                with silence_stdio():
                    result = render_whimsical.main()

            self.assertEqual(result, 0)
            ensure_inkscape_mock.assert_called_once()
            self.assertEqual(len(converted), 1)
            _svg_path, png_path, width = converted[0]
            self.assertEqual(width, 1800)
            self.assertEqual(png_path, temp_root / "books" / "test-book" / "lt" / "figures" / "figure-1.png")
            self.assertTrue(png_path.exists())

    def test_main_syncs_obsidian_after_successful_render(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            book_root, manifest_path = self.make_book_root(temp_root)
            sync_calls: list[tuple[Path, Path]] = []
            default_dest = temp_root / "vault" / "Test Book"

            def fake_render(svg_text: str, png_path: Path, width: int, padding: int) -> None:
                self.assertEqual(svg_text, '<svg width="100" height="50"></svg>')
                self.assertEqual(width, 2400)
                self.assertEqual(padding, 72)
                png_path.write_bytes(b"png")

            def fake_sync(dest: Path, target_book_root: Path) -> None:
                sync_calls.append((dest, target_book_root))

            with (
                patch.object(render_whimsical, "REPO_ROOT", temp_root),
                patch.object(
                    render_whimsical,
                    "parse_args",
                    return_value=Namespace(
                        figure_id="figure-1",
                        book_root=str(book_root),
                        manifest=manifest_path,
                        storage_state=Path("/tmp/storage-state.json"),
                        login=False,
                        width=2400,
                        padding=72,
                        sync_obsidian=True,
                        obsidian_dest=None,
                    ),
                ),
                patch.object(render_whimsical, "fetch_svg", return_value='<svg width="100" height="50"></svg>'),
                patch.object(render_whimsical, "render_svg_to_png_browser", side_effect=fake_render),
                patch.object(render_whimsical, "default_obsidian_dest", return_value=default_dest),
                patch.object(render_whimsical, "sync_obsidian", side_effect=fake_sync),
            ):
                with silence_stdio():
                    result = render_whimsical.main()

            self.assertEqual(result, 0)
            self.assertEqual(len(sync_calls), 1)
            self.assertEqual(sync_calls[0][0], default_dest)
            self.assertEqual(sync_calls[0][1].resolve(), book_root.resolve())
            self.assertTrue((temp_root / "books" / "test-book" / "lt" / "figures" / "figure-1.png").exists())

    def test_ensure_inkscape_uses_short_timeout(self) -> None:
        with patch.object(render_whimsical, "run_checked_subprocess") as run_mock:
            render_whimsical.ensure_inkscape()

        run_mock.assert_called_once_with(
            ["inkscape", "--version"],
            phase="probe Inkscape runtime",
            timeout=render_whimsical.SHORT_TIMEOUT_SECONDS,
            capture_output=True,
            text=True,
        )

    def test_sync_obsidian_uses_timeout_wrapped_runner(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir).resolve()
            book_root = temp_root / "books" / "test-book"
            book_root.mkdir(parents=True, exist_ok=True)

            with (
                patch.object(render_whimsical, "REPO_ROOT", temp_root),
                patch.object(render_whimsical, "run_checked_subprocess") as run_mock,
            ):
                render_whimsical.sync_obsidian(temp_root / "vault" / "Test Book", book_root)

        run_mock.assert_called_once_with(
            [
                str(temp_root / "scripts" / "sync_obsidian_book.sh"),
                "--book-root",
                "books/test-book",
                "--dest",
                str(temp_root / "vault" / "Test Book"),
            ],
            phase="sync Obsidian book",
            timeout=render_whimsical.DEFAULT_TIMEOUT_SECONDS,
        )


if __name__ == "__main__":
    unittest.main()
