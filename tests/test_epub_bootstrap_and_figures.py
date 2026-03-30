#!/usr/bin/env python3
from __future__ import annotations

import base64
import importlib.util
import subprocess
import sys
import tempfile
import textwrap
import unittest
import zipfile
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

import bootstrap_book_from_epub as epub_bootstrap  # noqa: E402
import register_whimsical_figure as figure_register  # noqa: E402
from workflow_test_utils import silence_stdio  # noqa: E402


PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4////fwAJ+wP9KobjigAAAABJRU5ErkJggg=="
)
FIGURE_INDEX_HEADER = "source_figure_id\tchapter_slug\tsource_href\tasset_path\tmedia_type\talt_text\tcaption_text\tnotes\n"
MANIFEST_HEADER = "figure_id\tfigure_number\tpng_path\tcanonical_source_type\tcanonical_source_path\tnotes\n"
HAS_EPUB_RUNTIME_DEPS = (
    importlib.util.find_spec("ebooklib") is not None
    and importlib.util.find_spec("bs4") is not None
)


def write_test_epub(path: Path) -> None:
    container_xml = textwrap.dedent(
        """\
        <?xml version="1.0" encoding="UTF-8"?>
        <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
          <rootfiles>
            <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
          </rootfiles>
        </container>
        """
    )
    content_opf = textwrap.dedent(
        """\
        <?xml version="1.0" encoding="utf-8"?>
        <package version="3.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid">
          <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
            <dc:identifier id="bookid">urn:test:epub-book</dc:identifier>
            <dc:title>EPUB Test Book</dc:title>
            <dc:language>en</dc:language>
          </metadata>
          <manifest>
            <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
            <item id="ch1" href="Text/ch1.xhtml" media-type="application/xhtml+xml"/>
            <item id="ch2" href="Text/ch2.xhtml" media-type="application/xhtml+xml"/>
            <item id="fig1" href="Images/fig1.png" media-type="image/png"/>
          </manifest>
          <spine>
            <itemref idref="ch1"/>
            <itemref idref="ch2"/>
          </spine>
        </package>
        """
    )
    nav_xhtml = textwrap.dedent(
        """\
        <?xml version="1.0" encoding="utf-8"?>
        <html xmlns="http://www.w3.org/1999/xhtml">
          <head><title>TOC</title></head>
          <body>
            <nav epub:type="toc" xmlns:epub="http://www.idpf.org/2007/ops">
              <ol>
                <li><a href="Text/ch1.xhtml">Chapter 1 First chapter</a></li>
                <li><a href="Text/ch2.xhtml">Chapter 2 Second chapter</a></li>
              </ol>
            </nav>
          </body>
        </html>
        """
    )
    chapter_one = textwrap.dedent(
        """\
        <?xml version="1.0" encoding="utf-8"?>
        <html xmlns="http://www.w3.org/1999/xhtml">
          <head><title>Chapter 1</title></head>
          <body>
            <h1>First chapter</h1>
            <p>First chapter intro paragraph.</p>
            <figure>
              <img src="../Images/fig1.png" alt="Airway figure"/>
              <figcaption>Figure 1.1 Airway overview</figcaption>
            </figure>
          </body>
        </html>
        """
    )
    chapter_two = textwrap.dedent(
        """\
        <?xml version="1.0" encoding="utf-8"?>
        <html xmlns="http://www.w3.org/1999/xhtml">
          <head><title>Chapter 2</title></head>
          <body>
            <h1>Second chapter</h1>
            <p>Second chapter closing paragraph.</p>
          </body>
        </html>
        """
    )

    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        archive.writestr("META-INF/container.xml", container_xml)
        archive.writestr("OEBPS/content.opf", content_opf)
        archive.writestr("OEBPS/nav.xhtml", nav_xhtml)
        archive.writestr("OEBPS/Text/ch1.xhtml", chapter_one)
        archive.writestr("OEBPS/Text/ch2.xhtml", chapter_two)
        archive.writestr("OEBPS/Images/fig1.png", PNG_BYTES)


@unittest.skipUnless(HAS_EPUB_RUNTIME_DEPS, "requires EbookLib and beautifulsoup4")
class EpubBootstrapTests(unittest.TestCase):
    maxDiff = None

    def test_bootstrap_creates_chapters_and_figure_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            repo_root = temp_root / "repo"
            (repo_root / "books").mkdir(parents=True, exist_ok=True)
            epub_path = temp_root / "book.epub"
            write_test_epub(epub_path)
            sync_calls: list[Path] = []

            with (
                patch.object(epub_bootstrap, "REPO_ROOT", repo_root),
                patch.object(epub_bootstrap, "TEMPLATE_ROOT", TEMPLATE_ROOT),
                patch.object(epub_bootstrap, "install_obsidian_sync", side_effect=lambda book_root: sync_calls.append(book_root)),
                patch.object(epub_bootstrap, "obsidian_dest_for_title", lambda title: Path("/tmp/obsidian") / title),
                patch.object(
                    epub_bootstrap,
                    "parse_args",
                    return_value=Namespace(epub=epub_path, chapter_map=None, install_obsidian_sync=False),
                ),
            ):
                with silence_stdio():
                    result = epub_bootstrap.main()

            self.assertEqual(result, 0)
            book_root = repo_root / "books" / "epub-test-book"
            self.assertTrue((book_root / "source" / "epub" / "book.epub").exists())
            self.assertTrue((book_root / "source" / "chapters-en" / "001-first-chapter.md").exists())
            self.assertTrue((book_root / "source" / "chapters-en" / "002-second-chapter.md").exists())

            chapter_text = (book_root / "source" / "chapters-en" / "001-first-chapter.md").read_text(encoding="utf-8")
            self.assertIn("Šaltinio segmentai:", chapter_text)
            self.assertIn("First chapter intro paragraph.", chapter_text)
            self.assertIn("<!-- source_href:", chapter_text)

            figure_rows = (book_root / "source" / "index" / "figures.tsv").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(figure_rows), 2)
            self.assertIn("001-first-chapter-fig-01", figure_rows[1])
            self.assertIn("Figure 1.1 Airway overview", figure_rows[1])
            self.assertTrue((book_root / "source" / "figures-raw" / "001-first-chapter-fig-01.png").exists())

            manifest_lines = (book_root / "lt" / "figures" / "manifest.tsv").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(manifest_lines), 1)
            self.assertEqual(sync_calls, [])

    def test_bootstrap_honors_chapter_map_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            repo_root = temp_root / "repo"
            (repo_root / "books").mkdir(parents=True, exist_ok=True)
            epub_path = temp_root / "book.epub"
            chapter_map_path = temp_root / "book.chapters.yaml"
            write_test_epub(epub_path)
            chapter_map_path.write_text(
                textwrap.dedent(
                    """\
                    book_title: Custom EPUB
                    slug: custom-epub
                    chapters:
                      - number: 7
                        title: Merged chapter
                        hrefs:
                          - Text/ch1.xhtml
                          - Text/ch2.xhtml
                    """
                ),
                encoding="utf-8",
            )
            sync_calls: list[Path] = []

            with (
                patch.object(epub_bootstrap, "REPO_ROOT", repo_root),
                patch.object(epub_bootstrap, "TEMPLATE_ROOT", TEMPLATE_ROOT),
                patch.object(epub_bootstrap, "install_obsidian_sync", side_effect=lambda book_root: sync_calls.append(book_root)),
                patch.object(epub_bootstrap, "obsidian_dest_for_title", lambda title: Path("/tmp/obsidian") / title),
                patch.object(
                    epub_bootstrap,
                    "parse_args",
                    return_value=Namespace(epub=epub_path, chapter_map=chapter_map_path, install_obsidian_sync=False),
                ),
            ):
                with silence_stdio():
                    result = epub_bootstrap.main()

            self.assertEqual(result, 0)
            book_root = repo_root / "books" / "custom-epub"
            merged_chapter = book_root / "source" / "chapters-en" / "007-merged-chapter.md"
            self.assertTrue(merged_chapter.exists())
            merged_text = merged_chapter.read_text(encoding="utf-8")
            self.assertIn("First chapter intro paragraph.", merged_text)
            self.assertIn("Second chapter closing paragraph.", merged_text)
            self.assertFalse((book_root / "source" / "chapters-en" / "001-first-chapter.md").exists())
            self.assertEqual(sync_calls, [])

    def test_bootstrap_installs_obsidian_sync_only_when_requested(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            repo_root = temp_root / "repo"
            (repo_root / "books").mkdir(parents=True, exist_ok=True)
            epub_path = temp_root / "book.epub"
            write_test_epub(epub_path)
            sync_calls: list[Path] = []

            with (
                patch.object(epub_bootstrap, "REPO_ROOT", repo_root),
                patch.object(epub_bootstrap, "TEMPLATE_ROOT", TEMPLATE_ROOT),
                patch.object(epub_bootstrap, "install_obsidian_sync", side_effect=lambda book_root: sync_calls.append(book_root)),
                patch.object(epub_bootstrap, "obsidian_dest_for_title", lambda title: Path("/tmp/obsidian") / title),
                patch.object(
                    epub_bootstrap,
                    "parse_args",
                    return_value=Namespace(epub=epub_path, chapter_map=None, install_obsidian_sync=True),
                ),
            ):
                with silence_stdio():
                    result = epub_bootstrap.main()

            self.assertEqual(result, 0)
            self.assertEqual(sync_calls, [repo_root / "books" / "epub-test-book"])


class RegisterWhimsicalFigureTests(unittest.TestCase):
    def write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def make_book_root(self, base_dir: Path) -> Path:
        book_root = base_dir / "books" / "test-book"
        (book_root / "source" / "index").mkdir(parents=True, exist_ok=True)
        (book_root / "lt" / "figures").mkdir(parents=True, exist_ok=True)
        self.write(book_root / "source" / "index" / "figures.tsv", FIGURE_INDEX_HEADER)
        self.write(book_root / "lt" / "figures" / "manifest.tsv", MANIFEST_HEADER)
        return book_root

    def test_register_creates_manifest_row_without_render_side_effects(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            book_root = self.make_book_root(temp_root)
            self.write(
                book_root / "source" / "index" / "figures.tsv",
                FIGURE_INDEX_HEADER
                + "001-first-chapter-fig-01\t001-first-chapter\tText/ch1.xhtml\tsource/figures-raw/001-first-chapter-fig-01.png\timage/png\tAirway figure\tFigure 1.1 Airway overview\tsource_asset_href=Images/fig1.png\n",
            )

            with (
                patch.object(figure_register, "repo_relative_path", lambda path: path.resolve().relative_to(temp_root.resolve()).as_posix()),
                patch.object(figure_register, "render_registered_figure", lambda *_: None),
                patch.object(
                    figure_register,
                    "parse_args",
                    return_value=Namespace(
                        book_root=book_root,
                        source_figure_id="001-first-chapter-fig-01",
                        figure_number="3.1",
                        whimsical_url="https://whimsical.com/example-board",
                        notes="LT perdarytas variantas",
                    ),
                ),
            ):
                with silence_stdio():
                    result = figure_register.main()

            self.assertEqual(result, 0)
            manifest_rows = (book_root / "lt" / "figures" / "manifest.tsv").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(manifest_rows), 2)
            self.assertIn("figure-3-1-001-first-chapter-fig-01", manifest_rows[1])
            self.assertIn("https://whimsical.com/example-board", manifest_rows[1])
            self.assertIn("source_figure_id=001-first-chapter-fig-01", manifest_rows[1])

    def test_register_rolls_back_manifest_when_render_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            book_root = self.make_book_root(temp_root)
            self.write(
                book_root / "source" / "index" / "figures.tsv",
                FIGURE_INDEX_HEADER
                + "001-first-chapter-fig-01\t001-first-chapter\tText/ch1.xhtml\tsource/figures-raw/001-first-chapter-fig-01.png\timage/png\tAirway figure\tFigure 1.1 Airway overview\tsource_asset_href=Images/fig1.png\n",
            )

            def failing_render(*_args: object) -> None:
                raise subprocess.CalledProcessError(1, ["render_whimsical_figure.py"])

            with (
                patch.object(figure_register, "repo_relative_path", lambda path: path.resolve().relative_to(temp_root.resolve()).as_posix()),
                patch.object(figure_register, "render_registered_figure", failing_render),
                patch.object(
                    figure_register,
                    "parse_args",
                    return_value=Namespace(
                        book_root=book_root,
                        source_figure_id="001-first-chapter-fig-01",
                        figure_number="3.1",
                        whimsical_url="https://whimsical.com/example-board",
                        notes="LT perdarytas variantas",
                    ),
                ),
            ):
                with silence_stdio():
                    with self.assertRaises(SystemExit):
                        figure_register.main()

            manifest_text = (book_root / "lt" / "figures" / "manifest.tsv").read_text(encoding="utf-8")
            self.assertEqual(manifest_text, MANIFEST_HEADER)


if __name__ == "__main__":
    unittest.main()
