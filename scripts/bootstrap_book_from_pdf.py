#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

import yaml

from workflow_rules import resolve_repo_path
from workflow_runtime import REPO_ROOT, ensure_python_module, obsidian_dest_for_title


ensure_python_module("fitz", package_name="PyMuPDF")
import fitz


TEMPLATE_ROOT = REPO_ROOT / "books" / "_template"
PAGE_HEADER_RE = re.compile(r"^page\s+.+\s+(\d+)\s*$", re.IGNORECASE)
TOC_LINE_RE = re.compile(
    r"^(Chapter)\s+(?P<number>\d+)\s+(?P<title>.+?)(?:\s*(?:\.{2,}|\u2026+|\s{2,})\s*(?P<page>\d{1,4}))?\s*$",
    re.IGNORECASE,
)
AUX_TOC_LINE_RE = re.compile(r"^(Section|Part|Appendix)\b", re.IGNORECASE)
TRAILING_PAGE_RE = re.compile(r"^(?P<body>.+?)\s*(?:\.{2,}|\u2026+|\s{2,})\s*(?P<page>\d{1,4})\s*$")
TEMPLATE_TOKEN_RE = re.compile(r"{{([A-Z0-9_]+)}}")
SIDE_CAR_REQUIRED_KEYS = {"chapters"}


def slugify(text: str) -> str:
    text = text.lower().replace("\xa0", " ")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new self-contained books/<slug> workspace from a source PDF using PyMuPDF."
    )
    parser.add_argument("--pdf", type=Path, required=True, help="Path to the source PDF.")
    parser.add_argument(
        "--contents-pages",
        help="Contents page range in PDF numbering, for example 7-14 or 7-8,10.",
    )
    parser.add_argument(
        "--page-offset",
        type=int,
        help="Physical PDF page minus printed book page for chapter content.",
    )
    parser.add_argument(
        "--backmatter-start",
        type=int,
        help="First printed book page after the last numbered chapter.",
    )
    parser.add_argument(
        "--chapter-map",
        type=Path,
        help="Optional YAML sidecar with explicit chapter boundaries. If omitted, uses <pdf-stem>.chapters.yaml when present.",
    )
    return parser.parse_args()


def normalize_text(text: str) -> str:
    text = text.replace("\f", "\n")
    text = text.replace("\xa0", " ")
    text = text.replace("\u00ad", "")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = text.replace("–\n", "–")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def strip_page_headers(text: str) -> str:
    kept_lines: list[str] = []
    for line in text.splitlines():
        if PAGE_HEADER_RE.match(line.strip()):
            continue
        kept_lines.append(line)
    return "\n".join(kept_lines)


def parse_page_spec(page_spec: str) -> list[int]:
    pages: list[int] = []
    for chunk in page_spec.split(","):
        item = chunk.strip()
        if not item:
            continue
        if "-" in item:
            left, right = item.split("-", 1)
            start = int(left)
            end = int(right)
            if end < start:
                raise SystemExit(f"Neteisingas puslapių intervalas: {item}")
            pages.extend(range(start, end + 1))
        else:
            pages.append(int(item))
    if not pages:
        raise SystemExit("Nerastas nei vienas `contents-pages` puslapis.")
    return pages


def extract_pdf_pages_text(pdf: fitz.Document, pages: list[int]) -> str:
    chunks: list[str] = []
    for physical_page in pages:
        if physical_page < 1 or physical_page > pdf.page_count:
            raise SystemExit(
                f"PDF puslapis {physical_page} išeina už ribų. PDF turi {pdf.page_count} puslapius."
            )
        page = pdf.load_page(physical_page - 1)
        text = normalize_text(page.get_text("text"))
        if not text:
            continue
        chunks.append(strip_page_headers(text))
    return "\n".join(chunks)


def parse_contents_entries(contents_text: str) -> list[dict[str, int | str]]:
    lines = [line.strip() for line in contents_text.splitlines()]
    lines = [line for line in lines if line]
    entries: list[dict[str, int | str]] = []
    seen_numbers: set[int] = set()

    for index, line in enumerate(lines):
        match = TOC_LINE_RE.match(line)
        if not match:
            continue
        number = int(match.group("number"))
        if number in seen_numbers:
            continue
        title = match.group("title").strip()
        page_match = match.group("page")
        if page_match:
            title = TRAILING_PAGE_RE.sub(lambda inner: inner.group("body").strip(), title)
        page_value: int | None = int(page_match) if page_match else None
        for offset in range(1, 13):
            if page_value is not None:
                break
            if index + offset >= len(lines):
                break
            candidate = lines[index + offset]
            if TOC_LINE_RE.match(candidate):
                break
            if AUX_TOC_LINE_RE.match(candidate):
                continue
            if re.fullmatch(r"\d{1,4}", candidate):
                page_value = int(candidate)
                break
            trailing = TRAILING_PAGE_RE.match(candidate)
            if trailing:
                page_value = int(trailing.group("page"))
                break
        if page_value is None:
            raise SystemExit(
                "Nepavyko patikimai nustatyti skyriaus pradžios iš turinio eilutės: "
                f"{line}\nNaudokite `--chapter-map <pdf-stem>.chapters.yaml` nestandartiniams PDF."
            )
        seen_numbers.add(number)
        entries.append(
            {
                "number": number,
                "title": title,
                "full_title": f"Chapter {number} {title}",
                "book_start_page": page_value,
            }
        )

    if not entries:
        raise SystemExit("Nepavyko aptikti nė vieno skyriaus turinyje.")
    return sorted(entries, key=lambda item: int(item["number"]))


def normalize_optional_int(value: object) -> int | None:
    if value in (None, ""):
        return None
    if isinstance(value, int):
        return value
    try:
        return int(str(value).strip())
    except ValueError as exc:
        raise SystemExit(f"Neteisinga skaitinė reikšmė chapter map faile: {value!r}") from exc


def sidecar_path_for(pdf_path: Path) -> Path:
    return pdf_path.with_name(f"{pdf_path.stem}.chapters.yaml")


def load_chapter_map(path: Path) -> dict[str, object]:
    if not path.exists():
        raise SystemExit(f"Nerastas chapter map failas: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"Chapter map failas turi būti YAML objektas: {path}")
    if not SIDE_CAR_REQUIRED_KEYS.issubset(data):
        raise SystemExit(f"{path}: trūksta privalomo `chapters` rakto.")
    chapters = data.get("chapters")
    if not isinstance(chapters, list) or not chapters:
        raise SystemExit(f"{path}: `chapters` turi būti netuščias sąrašas.")
    return data


def chapter_map_context(
    args: argparse.Namespace,
    pdf_path: Path,
) -> tuple[dict[str, object] | None, Path | None]:
    chapter_map_path = resolve_repo_path(args.chapter_map) if args.chapter_map else sidecar_path_for(pdf_path)
    if args.chapter_map or chapter_map_path.exists():
        return load_chapter_map(chapter_map_path), chapter_map_path
    return None, None


def chapter_slug(number: int, title: str) -> str:
    return f"{number:03d}-{slugify(title)}"


def build_chapters_from_map(
    chapter_map: dict[str, object],
    *,
    cli_page_offset: int | None,
    cli_backmatter_start: int | None,
) -> list[dict[str, int | str | None]]:
    sidecar_page_offset = normalize_optional_int(chapter_map.get("page_offset"))
    sidecar_backmatter_start = normalize_optional_int(chapter_map.get("backmatter_start"))
    page_offset = cli_page_offset if cli_page_offset is not None else sidecar_page_offset
    _ = cli_backmatter_start if cli_backmatter_start is not None else sidecar_backmatter_start

    seen_numbers: set[int] = set()
    chapters: list[dict[str, int | str | None]] = []
    for index, raw_entry in enumerate(chapter_map.get("chapters", []), start=1):
        if not isinstance(raw_entry, dict):
            raise SystemExit(f"Chapter map: `chapters[{index}]` turi būti objektas.")
        number = normalize_optional_int(raw_entry.get("number"))
        title = str(raw_entry.get("title", "")).strip()
        if number is None or not title:
            raise SystemExit(f"Chapter map: `chapters[{index}]` turi turėti `number` ir `title`.")
        if number in seen_numbers:
            raise SystemExit(f"Chapter map: dubliuotas chapter number {number}.")
        seen_numbers.add(number)

        book_start = normalize_optional_int(raw_entry.get("book_start_page"))
        book_end = normalize_optional_int(raw_entry.get("book_end_page"))
        pdf_start = normalize_optional_int(raw_entry.get("pdf_start_page"))
        pdf_end = normalize_optional_int(raw_entry.get("pdf_end_page"))

        has_book_pair = book_start is not None or book_end is not None
        has_pdf_pair = pdf_start is not None or pdf_end is not None
        if has_book_pair and (book_start is None or book_end is None):
            raise SystemExit(
                f"Chapter map: `chapters[{index}]` su book puslapiais turi turėti ir `book_start_page`, ir `book_end_page`."
            )
        if has_pdf_pair and (pdf_start is None or pdf_end is None):
            raise SystemExit(
                f"Chapter map: `chapters[{index}]` su PDF puslapiais turi turėti ir `pdf_start_page`, ir `pdf_end_page`."
            )
        if not has_book_pair and not has_pdf_pair:
            raise SystemExit(
                f"Chapter map: `chapters[{index}]` turi turėti arba book puslapių porą, arba PDF puslapių porą."
            )

        if has_book_pair and not has_pdf_pair:
            if page_offset is None:
                raise SystemExit(
                    f"Chapter map: chapter {number} naudoja book puslapius, todėl reikia `page_offset` per CLI arba YAML."
                )
            pdf_start = book_start + page_offset
            pdf_end = book_end + page_offset
        elif has_pdf_pair and not has_book_pair:
            if page_offset is not None:
                book_start = pdf_start - page_offset
                book_end = pdf_end - page_offset
            else:
                book_start = None
                book_end = None

        chapters.append(
            {
                "number": number,
                "title": title,
                "full_title": f"Chapter {number} {title}",
                "book_start_page": book_start,
                "book_end_page": book_end,
                "pdf_start_page": pdf_start,
                "pdf_end_page": pdf_end,
                "slug": chapter_slug(number, title),
            }
        )

    return sorted(chapters, key=lambda item: int(item["number"]))


def finalize_ranges(
    entries: list[dict[str, int | str]],
    page_offset: int,
    backmatter_start: int | None,
) -> list[dict[str, int | str]]:
    finalized: list[dict[str, int | str]] = []
    for index, item in enumerate(entries):
        next_start = (
            int(entries[index + 1]["book_start_page"])
            if index + 1 < len(entries)
            else backmatter_start
        )
        if next_start is None:
            raise SystemExit("Paskutiniam skyriui reikia `--backmatter-start`, kad būtų aiškus pabaigos puslapis.")
        book_start = int(item["book_start_page"])
        book_end = next_start - 1
        pdf_start = book_start + page_offset
        pdf_end = book_end + page_offset
        finalized.append(
            {
                **item,
                "book_end_page": book_end,
                "pdf_start_page": pdf_start,
                "pdf_end_page": pdf_end,
                "slug": f"{int(item['number']):03d}-{slugify(str(item['title']))}",
            }
        )
    return finalized


def write_index(
    chapters: list[dict[str, int | str | None]],
    out_dir: Path,
    title: str,
    pdf_name: str,
    contents_pages: str,
    page_offset: int | None,
    backmatter_start: int | None,
) -> None:
    (out_dir / "chapters.json").write_text(
        json.dumps(chapters, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Chapter Index",
        "",
        f"- Book: `{title}`",
        f"- PDF: `{pdf_name}`",
        f"- Contents pages used: `{contents_pages}`",
        f"- Book-to-PDF page offset: `{page_offset:+d}`" if page_offset is not None else "- Book-to-PDF page offset: `n/a`",
    ]
    if backmatter_start is not None:
        lines.append(f"- Backmatter starts at printed book page: `{backmatter_start}`")
    lines.extend(
        [
            "",
            "| Nr. | Title | Book pages | PDF pages | Source | Translation | Research |",
            "| --- | ----- | ---------- | --------- | ------ | ----------- | -------- |",
        ]
    )
    for chapter in chapters:
        slug = str(chapter["slug"])
        if chapter["book_start_page"] is None or chapter["book_end_page"] is None:
            book_pages = "n/a"
        else:
            book_pages = f"{chapter['book_start_page']}-{chapter['book_end_page']}"
        lines.append(
            f"| {chapter['number']} | {chapter['title']} | "
            f"{book_pages} | "
            f"{chapter['pdf_start_page']}-{chapter['pdf_end_page']} | "
            f"../chapters-en/{slug}.md | ../../lt/chapters/{slug}.md | ../../research/{slug}.md |"
        )
    (out_dir / "chapters.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_chapter_sources(chapters: list[dict[str, int | str | None]], pdf: fitz.Document, pdf_name: str, out_dir: Path) -> None:
    for chapter in chapters:
        slug = str(chapter["slug"])
        book_pages = (
            f"{chapter['book_start_page']}-{chapter['book_end_page']}"
            if chapter["book_start_page"] is not None and chapter["book_end_page"] is not None
            else "n/a"
        )
        lines = [
            f"# {chapter['full_title']}",
            "",
            f"- Book pages: {book_pages}",
            f"- PDF pages: {chapter['pdf_start_page']}-{chapter['pdf_end_page']}",
            f"- PDF: {pdf_name}",
            "",
        ]
        for physical_page in range(int(chapter["pdf_start_page"]), int(chapter["pdf_end_page"]) + 1):
            if physical_page < 1 or physical_page > pdf.page_count:
                raise SystemExit(
                    f"Skyriaus `{slug}` PDF puslapis {physical_page} išeina už ribų. "
                    f"PDF turi {pdf.page_count} puslapius."
                )
            page = pdf.load_page(physical_page - 1)
            text = normalize_text(page.get_text("text"))
            if not text:
                continue
            lines.append(f"<!-- page:{physical_page} -->")
            lines.append(strip_page_headers(text))
            lines.append("")
        (out_dir / f"{slug}.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def derive_book_title(pdf: fitz.Document, pdf_path: Path) -> str:
    title = re.sub(r"\s+", " ", (pdf.metadata or {}).get("title", "").replace("\xa0", " ")).strip()
    if title:
        return title
    fallback = re.sub(r"[_-]+", " ", pdf_path.stem).strip()
    return re.sub(r"\s+", " ", fallback)


def copy_template(book_root: Path) -> None:
    if not TEMPLATE_ROOT.exists():
        raise SystemExit(f"Nerastas shared template katalogas: {TEMPLATE_ROOT}")
    shutil.copytree(TEMPLATE_ROOT, book_root)
    internal_manifest = book_root / "template_manifest.json"
    if internal_manifest.exists():
        internal_manifest.unlink()


def template_context(book_root: Path, title: str, pdf_name: str) -> dict[str, str]:
    return {
        "BOOK_TITLE": title,
        "BOOK_SLUG": book_root.name,
        "BOOK_ROOT": book_root.relative_to(REPO_ROOT).as_posix(),
        "BOOK_SOURCE_KIND": "pdf",
        "BOOK_SOURCE_NAME": pdf_name,
        "BOOK_PDF_NAME": pdf_name,
        "OBSIDIAN_DEST": obsidian_dest_for_title(title).as_posix(),
    }


def render_template_files(book_root: Path, context: dict[str, str]) -> None:
    for path in sorted(book_root.rglob("*")):
        if not path.is_file() or path.name == ".gitkeep":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rendered = TEMPLATE_TOKEN_RE.sub(lambda match: context.get(match.group(1), match.group(0)), text)
        path.write_text(rendered, encoding="utf-8")


def install_obsidian_sync(book_root: Path) -> None:
    book_root_rel = book_root.relative_to(REPO_ROOT).as_posix()
    subprocess.run(
        [
            str(REPO_ROOT / "scripts" / "install_obsidian_sync_agent.sh"),
            "--book-root",
            book_root_rel,
        ],
        check=True,
    )


def main() -> int:
    args = parse_args()
    pdf_path = resolve_repo_path(args.pdf)
    if not pdf_path.exists():
        raise SystemExit(f"Nerastas PDF: {pdf_path}")
    chapter_map, chapter_map_path = chapter_map_context(args, pdf_path)

    with fitz.open(pdf_path) as pdf:
        title = str(chapter_map.get("book_title", "")).strip() if chapter_map else ""
        if not title:
            title = derive_book_title(pdf, pdf_path)
        slug = str(chapter_map.get("slug", "")).strip() if chapter_map else ""
        slug = slug or slugify(title)
        if not slug:
            raise SystemExit(f"Nepavyko sugeneruoti slug iš pavadinimo `{title}`.")

        book_root = REPO_ROOT / "books" / slug
        if book_root.exists():
            raise SystemExit(f"Target book root jau egzistuoja: {book_root}")

        copy_template(book_root)

        source_index_dir = book_root / "source" / "index"
        source_chapters_dir = book_root / "source" / "chapters-en"
        source_pdf_dir = book_root / "source" / "pdf"
        target_pdf = source_pdf_dir / pdf_path.name
        shutil.copy2(pdf_path, target_pdf)

        render_template_files(book_root, template_context(book_root, title, target_pdf.name))

        if chapter_map:
            chapters = build_chapters_from_map(
                chapter_map,
                cli_page_offset=args.page_offset,
                cli_backmatter_start=args.backmatter_start,
            )
            contents_pages = args.contents_pages or f"chapter-map:{chapter_map_path.name}"
            page_offset = args.page_offset if args.page_offset is not None else normalize_optional_int(chapter_map.get("page_offset"))
            backmatter_start = (
                args.backmatter_start
                if args.backmatter_start is not None
                else normalize_optional_int(chapter_map.get("backmatter_start"))
            )
        else:
            if not args.contents_pages or args.page_offset is None:
                raise SystemExit(
                    "Automatiniam bootstrap be chapter map reikia `--contents-pages` ir `--page-offset`.\n"
                    "Jei PDF turinys nestandartinis, naudokite `--chapter-map <pdf-stem>.chapters.yaml`."
                )
            contents_text = extract_pdf_pages_text(pdf, parse_page_spec(args.contents_pages))
            chapters = finalize_ranges(
                parse_contents_entries(contents_text),
                args.page_offset,
                args.backmatter_start,
            )
            contents_pages = args.contents_pages
            page_offset = args.page_offset
            backmatter_start = args.backmatter_start

        write_index(
            chapters,
            source_index_dir,
            title,
            target_pdf.name,
            contents_pages,
            page_offset,
            backmatter_start,
        )
        write_chapter_sources(chapters, pdf, target_pdf.name, source_chapters_dir)

    install_obsidian_sync(book_root)
    print(book_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
