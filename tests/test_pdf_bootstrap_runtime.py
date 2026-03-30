#!/usr/bin/env python3
from __future__ import annotations

import importlib
import importlib.util
import json
import sys
import tempfile
import unittest
import warnings
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
TEMPLATE_ROOT = REPO_ROOT / "books" / "_template"
TESTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

warnings.filterwarnings(
    "ignore",
    message=r"builtin type .* has no __module__ attribute",
    category=DeprecationWarning,
)

import bootstrap_book_from_pdf as pdf_bootstrap  # noqa: E402
from workflow_subprocess import WorkflowSubprocessError  # noqa: E402
from workflow_test_utils import silence_stdio  # noqa: E402


HAS_PDF_RUNTIME_DEPS = importlib.util.find_spec("fitz") is not None


def write_test_pdf(path: Path) -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message=r"builtin type .* has no __module__ attribute",
            category=DeprecationWarning,
        )
        fitz_runtime = importlib.import_module("fitz")

    doc = fitz_runtime.open()
    doc.set_metadata({"title": "PDF Test Book"})

    first_page = doc.new_page()
    first_page.insert_text((72, 72), "Front matter page.")

    second_page = doc.new_page()
    second_page.insert_text((72, 72), "First chapter intro paragraph.")

    third_page = doc.new_page()
    third_page.insert_text((72, 72), "Second chapter closing paragraph.")

    doc.save(path)
    doc.close()


class PdfBootstrapRuntimeTests(unittest.TestCase):
    def test_dependency_probe_runs_only_via_runtime_helper(self) -> None:
        calls: list[tuple[str, str | None]] = []

        def fake_ensure(module_name: str, package_name: str | None = None) -> None:
            calls.append((module_name, package_name))
            raise SystemExit("missing fitz")

        with (
            patch.object(pdf_bootstrap, "fitz", None),
            patch.object(pdf_bootstrap, "ensure_python_module", side_effect=fake_ensure),
        ):
            with self.assertRaises(SystemExit):
                pdf_bootstrap.ensure_pdf_runtime_dependencies(force_reload=True)

        self.assertEqual(calls, [("fitz", "PyMuPDF")])

    def test_install_obsidian_sync_rejects_non_macos(self) -> None:
        with patch.object(pdf_bootstrap.sys, "platform", "linux"):
            with self.assertRaises(SystemExit) as ctx:
                pdf_bootstrap.install_obsidian_sync(Path("/tmp/book-root"))

        self.assertIn("tik macOS", str(ctx.exception))

    def test_install_obsidian_sync_uses_timeout_wrapped_runner(self) -> None:
        book_root = REPO_ROOT / "books" / "test-book"

        with (
            patch.object(pdf_bootstrap.sys, "platform", "darwin"),
            patch.object(pdf_bootstrap, "run_checked_subprocess") as run_mock,
        ):
            pdf_bootstrap.install_obsidian_sync(book_root)

        run_mock.assert_called_once_with(
            [
                str(REPO_ROOT / "scripts" / "install_obsidian_sync_agent.sh"),
                "--book-root",
                "books/test-book",
            ],
            phase="install Obsidian sync agent",
            timeout=pdf_bootstrap.DEFAULT_TIMEOUT_SECONDS,
        )

    def test_install_obsidian_sync_converts_runner_failure_to_system_exit(self) -> None:
        book_root = REPO_ROOT / "books" / "test-book"

        with (
            patch.object(pdf_bootstrap.sys, "platform", "darwin"),
            patch.object(
                pdf_bootstrap,
                "run_checked_subprocess",
                side_effect=WorkflowSubprocessError("install Obsidian sync agent timed out after 300s."),
            ),
        ):
            with self.assertRaises(SystemExit) as ctx:
                pdf_bootstrap.install_obsidian_sync(book_root)

        self.assertIn("timed out after 300s", str(ctx.exception))


@unittest.skipUnless(HAS_PDF_RUNTIME_DEPS, "requires PyMuPDF")
class PdfBootstrapSmokeTests(unittest.TestCase):
    def test_bootstrap_honors_chapter_map_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            repo_root = temp_root / "repo"
            (repo_root / "books").mkdir(parents=True, exist_ok=True)

            pdf_path = temp_root / "book.pdf"
            chapter_map_path = temp_root / "book.chapters.yaml"
            write_test_pdf(pdf_path)
            chapter_map_path.write_text(
                "\n".join(
                    [
                        "book_title: Custom PDF",
                        "slug: custom-pdf",
                        "chapters:",
                        "  - number: 7",
                        "    title: Merged chapter",
                        "    pdf_start_page: 2",
                        "    pdf_end_page: 3",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            sync_calls: list[Path] = []

            with (
                patch.object(pdf_bootstrap, "REPO_ROOT", repo_root),
                patch.object(pdf_bootstrap, "TEMPLATE_ROOT", TEMPLATE_ROOT),
                patch.object(pdf_bootstrap, "install_obsidian_sync", side_effect=lambda book_root: sync_calls.append(book_root)),
                patch.object(pdf_bootstrap, "obsidian_dest_for_title", lambda title: Path("/tmp/obsidian") / title),
                patch.object(
                    pdf_bootstrap,
                    "parse_args",
                    return_value=Namespace(
                        pdf=pdf_path,
                        contents_pages=None,
                        page_offset=None,
                        backmatter_start=None,
                        chapter_map=chapter_map_path,
                        install_obsidian_sync=False,
                    ),
                ),
            ):
                with silence_stdio():
                    result = pdf_bootstrap.main()

            self.assertEqual(result, 0)
            book_root = repo_root / "books" / "custom-pdf"
            self.assertTrue((book_root / "source" / "pdf" / "book.pdf").exists())

            merged_chapter = book_root / "source" / "chapters-en" / "007-merged-chapter.md"
            self.assertTrue(merged_chapter.exists())
            merged_text = merged_chapter.read_text(encoding="utf-8")
            self.assertIn("First chapter intro paragraph.", merged_text)
            self.assertIn("Second chapter closing paragraph.", merged_text)
            self.assertIn("<!-- page:2 -->", merged_text)
            self.assertIn("<!-- page:3 -->", merged_text)

            chapters = json.loads((book_root / "source" / "index" / "chapters.json").read_text(encoding="utf-8"))
            self.assertEqual(len(chapters), 1)
            self.assertEqual(chapters[0]["slug"], "007-merged-chapter")
            self.assertEqual(chapters[0]["pdf_start_page"], 2)
            self.assertEqual(chapters[0]["pdf_end_page"], 3)
            self.assertEqual(sync_calls, [])

    def test_bootstrap_installs_obsidian_sync_only_when_requested(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            repo_root = temp_root / "repo"
            (repo_root / "books").mkdir(parents=True, exist_ok=True)

            pdf_path = temp_root / "book.pdf"
            chapter_map_path = temp_root / "book.chapters.yaml"
            write_test_pdf(pdf_path)
            chapter_map_path.write_text(
                "\n".join(
                    [
                        "book_title: Sync PDF",
                        "slug: sync-pdf",
                        "chapters:",
                        "  - number: 7",
                        "    title: Merged chapter",
                        "    pdf_start_page: 2",
                        "    pdf_end_page: 3",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            sync_calls: list[Path] = []

            with (
                patch.object(pdf_bootstrap, "REPO_ROOT", repo_root),
                patch.object(pdf_bootstrap, "TEMPLATE_ROOT", TEMPLATE_ROOT),
                patch.object(pdf_bootstrap, "install_obsidian_sync", side_effect=lambda book_root: sync_calls.append(book_root)),
                patch.object(pdf_bootstrap, "obsidian_dest_for_title", lambda title: Path("/tmp/obsidian") / title),
                patch.object(
                    pdf_bootstrap,
                    "parse_args",
                    return_value=Namespace(
                        pdf=pdf_path,
                        contents_pages=None,
                        page_offset=None,
                        backmatter_start=None,
                        chapter_map=chapter_map_path,
                        install_obsidian_sync=True,
                    ),
                ),
            ):
                with silence_stdio():
                    result = pdf_bootstrap.main()

            self.assertEqual(result, 0)
            self.assertEqual(sync_calls, [repo_root / "books" / "sync-pdf"])


if __name__ == "__main__":
    unittest.main()
