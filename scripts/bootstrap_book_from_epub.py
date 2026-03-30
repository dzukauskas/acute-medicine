#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import posixpath
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

from workflow_rules import resolve_repo_path, slugify, write_tsv
from workflow_runtime import REPO_ROOT, ensure_python_module, obsidian_dest_for_title


ITEM_DOCUMENT = None
ITEM_IMAGE = None
epub = None
BeautifulSoup = None
NavigableString = None
Tag = None


TEMPLATE_ROOT = REPO_ROOT / "books" / "_template"
CHAPTER_TITLE_RE = re.compile(r"^(?:chapter\s+)?(?P<number>\d+)(?:\s*[:.\-]\s*|\s+)(?P<title>.+)$", re.IGNORECASE)
TEMPLATE_TOKEN_RE = re.compile(r"{{([A-Z0-9_]+)}}")
SIDE_CAR_REQUIRED_KEYS = {"chapters"}
FIGURE_INDEX_FIELDS = [
    "source_figure_id",
    "chapter_slug",
    "source_href",
    "asset_path",
    "media_type",
    "alt_text",
    "caption_text",
    "notes",
]


def ensure_epub_runtime_dependencies(*, force_reload: bool = False) -> None:
    global ITEM_DOCUMENT, ITEM_IMAGE, epub, BeautifulSoup, NavigableString, Tag

    if epub is not None and BeautifulSoup is not None and not force_reload:
        return

    ensure_python_module("ebooklib", package_name="EbookLib")
    ensure_python_module("bs4", package_name="beautifulsoup4")

    from bs4 import BeautifulSoup as _BeautifulSoup, NavigableString as _NavigableString, Tag as _Tag
    from ebooklib import ITEM_DOCUMENT as _ITEM_DOCUMENT, ITEM_IMAGE as _ITEM_IMAGE, epub as _epub

    ITEM_DOCUMENT = _ITEM_DOCUMENT
    ITEM_IMAGE = _ITEM_IMAGE
    epub = _epub
    BeautifulSoup = _BeautifulSoup
    NavigableString = _NavigableString
    Tag = _Tag


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new self-contained books/<slug> workspace from a source EPUB."
    )
    parser.add_argument("--epub", type=Path, required=True, help="Path to the source EPUB.")
    parser.add_argument(
        "--chapter-map",
        type=Path,
        help="Optional YAML sidecar with explicit chapter segments. If omitted, uses <epub-stem>.chapters.yaml when present.",
    )
    parser.add_argument(
        "--install-obsidian-sync",
        action="store_true",
        help="After repo-local bootstrap, explicitly install the per-book Obsidian sync agent on macOS.",
    )
    return parser.parse_args()


def sidecar_path_for(epub_path: Path) -> Path:
    return epub_path.with_name(f"{epub_path.stem}.chapters.yaml")


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


def chapter_map_context(args: argparse.Namespace, epub_path: Path) -> tuple[dict[str, object] | None, Path | None]:
    chapter_map_path = resolve_repo_path(args.chapter_map) if args.chapter_map else sidecar_path_for(epub_path)
    if args.chapter_map or chapter_map_path.exists():
        return load_chapter_map(chapter_map_path), chapter_map_path
    return None, None


def normalize_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_href(raw_href: str) -> str:
    path = unquote(urlsplit(raw_href).path).strip()
    if not path:
        return ""
    return posixpath.normpath(path).lstrip("./")


def resolve_relative_href(base_href: str, raw_href: str) -> str:
    if not raw_href.strip():
        return ""
    parsed = urlsplit(raw_href)
    if parsed.scheme or raw_href.startswith("data:"):
        return ""
    raw_path = unquote(parsed.path).strip()
    if not raw_path:
        return ""
    if raw_href.startswith("/"):
        return normalize_href(raw_path)
    base_dir = posixpath.dirname(normalize_href(base_href))
    return normalize_href(posixpath.join(base_dir, raw_path))


def extract_toc_title(node: object) -> str:
    for attr in ("title", "label"):
        value = getattr(node, attr, "")
        if isinstance(value, str) and value.strip():
            return normalize_text(value)
    if hasattr(node, "get_name"):
        value = node.get_name()
        if isinstance(value, str) and value.strip():
            return normalize_text(Path(value).stem.replace("-", " "))
    return ""


def extract_toc_href(node: object) -> str:
    href = getattr(node, "href", "")
    if isinstance(href, str) and href.strip():
        return normalize_href(href)
    file_name = getattr(node, "file_name", "")
    if isinstance(file_name, str) and file_name.strip():
        return normalize_href(file_name)
    if hasattr(node, "get_name"):
        value = node.get_name()
        if isinstance(value, str) and value.strip():
            return normalize_href(value)
    return ""


def flatten_toc_nodes(nodes: object) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []

    def visit(node: object) -> None:
        if isinstance(node, list):
            for child in node:
                visit(child)
            return

        if isinstance(node, tuple):
            if len(node) == 2 and isinstance(node[1], (list, tuple)):
                parent, children = node
                href = extract_toc_href(parent)
                title = extract_toc_title(parent) or href
                if href:
                    entries.append({"title": title, "href": href})
                visit(list(children))
                return
            for child in node:
                visit(child)
            return

        href = extract_toc_href(node)
        title = extract_toc_title(node) or href
        if href:
            entries.append({"title": title, "href": href})

    visit(nodes)

    deduped: list[dict[str, str]] = []
    seen: set[str] = set()
    for entry in entries:
        href = entry["href"]
        if not href or href in seen:
            continue
        seen.add(href)
        deduped.append(entry)
    return deduped


def load_spine_documents(book: epub.EpubBook) -> list[dict[str, object]]:
    documents: list[dict[str, object]] = []
    for spine_entry in book.spine:
        item_id = spine_entry[0] if isinstance(spine_entry, tuple) else spine_entry
        item = book.get_item_with_id(item_id)
        if item is None or item.get_type() != ITEM_DOCUMENT:
            continue
        href = normalize_href(getattr(item, "file_name", "") or item.get_name())
        if not href:
            continue
        documents.append(
            {
                "id": item_id,
                "href": href,
                "item": item,
            }
        )
    return documents


def parse_title_components(raw_title: str, fallback_number: int) -> tuple[int, str]:
    cleaned = normalize_text(raw_title)
    match = CHAPTER_TITLE_RE.match(cleaned)
    if match:
        return int(match.group("number")), match.group("title").strip()
    return fallback_number, cleaned


def chapter_slug(number: int, title: str) -> str:
    return f"{number:03d}-{slugify(title)}"


def build_chapters_from_toc(book: epub.EpubBook) -> list[dict[str, object]]:
    spine_docs = load_spine_documents(book)
    if not spine_docs:
        raise SystemExit("EPUB spine dokumentų nerasta.")
    spine_index = {doc["href"]: index for index, doc in enumerate(spine_docs)}
    toc_entries = [entry for entry in flatten_toc_nodes(book.toc) if entry["href"] in spine_index]
    if not toc_entries:
        raise SystemExit(
            "Nepavyko aptikti nė vieno EPUB TOC įrašo, kuris atitiktų spine dokumentus. "
            "Naudokite `--chapter-map <epub-stem>.chapters.yaml` nestandartiniams EPUB."
        )

    numbered_entries = [entry for entry in toc_entries if CHAPTER_TITLE_RE.match(entry["title"])]
    start_entries = numbered_entries or toc_entries
    ordered_starts = sorted(
        ({entry["href"]: entry for entry in start_entries}).values(),
        key=lambda entry: spine_index[entry["href"]],
    )

    chapters: list[dict[str, object]] = []
    used_numbers: set[int] = set()
    next_fallback_number = 1
    for position, entry in enumerate(ordered_starts):
        start_idx = spine_index[entry["href"]]
        end_idx = (
            spine_index[ordered_starts[position + 1]["href"]]
            if position + 1 < len(ordered_starts)
            else len(spine_docs)
        )
        source_hrefs = [str(doc["href"]) for doc in spine_docs[start_idx:end_idx]]
        if not source_hrefs:
            continue

        fallback_number = next_fallback_number
        while fallback_number in used_numbers:
            fallback_number += 1
        number, title = parse_title_components(entry["title"], fallback_number)
        if number in used_numbers:
            number = fallback_number
        used_numbers.add(number)
        next_fallback_number = max(next_fallback_number, number + 1)
        title = title or Path(source_hrefs[0]).stem.replace("-", " ").title()
        chapters.append(
            {
                "number": number,
                "title": title,
                "full_title": f"Chapter {number} {title}",
                "slug": chapter_slug(number, title),
                "source_hrefs": source_hrefs,
                "start_href": source_hrefs[0],
            }
        )
    if not chapters:
        raise SystemExit("Nepavyko sugeneruoti nė vieno skyriaus iš EPUB TOC.")
    return sorted(chapters, key=lambda item: int(item["number"]))


def normalize_href_list(value: object) -> list[str]:
    if not isinstance(value, list) or not value:
        raise SystemExit("Chapter map `hrefs` turi būti netuščias sąrašas.")
    hrefs = [normalize_href(str(item)) for item in value if normalize_href(str(item))]
    if not hrefs:
        raise SystemExit("Chapter map `hrefs` sąraše nerasta nei vieno galiojančio href.")
    return hrefs


def build_chapters_from_map(book: epub.EpubBook, chapter_map: dict[str, object]) -> list[dict[str, object]]:
    spine_docs = load_spine_documents(book)
    if not spine_docs:
        raise SystemExit("EPUB spine dokumentų nerasta.")
    spine_index = {str(doc["href"]): index for index, doc in enumerate(spine_docs)}

    chapters: list[dict[str, object]] = []
    for index, raw_entry in enumerate(chapter_map.get("chapters", []), start=1):
        if not isinstance(raw_entry, dict):
            raise SystemExit(f"Chapter map: `chapters[{index}]` turi būti objektas.")
        number_raw = str(raw_entry.get("number", "")).strip()
        title = str(raw_entry.get("title", "")).strip()
        if not number_raw.isdigit() or not title:
            raise SystemExit(f"Chapter map: `chapters[{index}]` turi turėti `number` ir `title`.")
        hrefs_value = raw_entry.get("hrefs")
        start_href_value = str(raw_entry.get("start_href", "")).strip()
        if hrefs_value:
            source_hrefs = normalize_href_list(hrefs_value)
            start_href = source_hrefs[0]
        elif start_href_value:
            source_hrefs = []
            start_href = normalize_href(start_href_value)
        else:
            raise SystemExit(
                f"Chapter map: `chapters[{index}]` turi turėti arba `hrefs`, arba `start_href`."
            )
        if start_href not in spine_index:
            raise SystemExit(
                f"Chapter map: `chapters[{index}]` start href nerastas EPUB spine: {start_href}"
            )
        for href in source_hrefs:
            if href not in spine_index:
                raise SystemExit(f"Chapter map: `chapters[{index}]` href nerastas EPUB spine: {href}")
        chapters.append(
            {
                "number": int(number_raw),
                "title": title,
                "full_title": f"Chapter {int(number_raw)} {title}",
                "slug": chapter_slug(int(number_raw), title),
                "start_href": start_href,
                "source_hrefs": source_hrefs,
            }
        )

    ordered = sorted(chapters, key=lambda item: spine_index[str(item["start_href"])])
    seen_numbers: set[int] = set()
    assigned_hrefs: set[str] = set()
    for idx, chapter in enumerate(ordered):
        number = int(chapter["number"])
        if number in seen_numbers:
            raise SystemExit(f"Chapter map: dubliuotas chapter number {number}.")
        seen_numbers.add(number)

        if not chapter["source_hrefs"]:
            start_idx = spine_index[str(chapter["start_href"])]
            next_start_idx = (
                spine_index[str(ordered[idx + 1]["start_href"])]
                if idx + 1 < len(ordered)
                else len(spine_docs)
            )
            chapter["source_hrefs"] = [str(doc["href"]) for doc in spine_docs[start_idx:next_start_idx]]
        for href in chapter["source_hrefs"]:
            if href in assigned_hrefs:
                raise SystemExit(f"Chapter map: tas pats href priskirtas keliems skyriams: {href}")
            assigned_hrefs.add(href)
    return ordered


def metadata_title(book: epub.EpubBook, chapter_map: dict[str, object] | None) -> str:
    if chapter_map:
        title = str(chapter_map.get("book_title", "")).strip()
        if title:
            return title
    values = book.get_metadata("DC", "title")
    if values:
        return normalize_text(str(values[0][0]))
    return "Untitled EPUB"


def slug_from_title(book_title: str, chapter_map: dict[str, object] | None) -> str:
    if chapter_map:
        slug = str(chapter_map.get("slug", "")).strip()
        if slug:
            return slug
    return slugify(book_title)


def render_markdown_table(table: Tag) -> str:
    rows: list[list[str]] = []
    header_row_index: int | None = None
    for tr in table.find_all("tr"):
        cells = tr.find_all(["th", "td"])
        if not cells:
            continue
        row = [normalize_text(cell.get_text(" ", strip=True)) for cell in cells]
        if not any(row):
            continue
        if header_row_index is None and tr.find("th") is not None:
            header_row_index = len(rows)
        rows.append(row)
    if not rows:
        return ""
    column_count = max(len(row) for row in rows)
    padded_rows = [row + [""] * (column_count - len(row)) for row in rows]
    if header_row_index is not None:
        header = padded_rows[header_row_index]
        data_rows = padded_rows[:header_row_index] + padded_rows[header_row_index + 1 :]
    else:
        header = [f"Col {index}" for index in range(1, column_count + 1)]
        data_rows = padded_rows
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in data_rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def extract_caption_text(img_tag: Tag) -> str:
    figure = img_tag.find_parent("figure")
    if figure is not None:
        figcaption = figure.find("figcaption")
        if figcaption is not None:
            return normalize_text(figcaption.get_text(" ", strip=True))
    sibling = img_tag.find_next_sibling(["figcaption", "p"])
    if sibling is not None:
        text = normalize_text(sibling.get_text(" ", strip=True))
        if text:
            return text
    return ""


def render_block(node: object) -> list[str]:
    if isinstance(node, NavigableString):
        text = normalize_text(str(node))
        return [text] if text else []
    if not isinstance(node, Tag):
        return []

    name = node.name.lower()
    if name in {"script", "style", "nav"}:
        return []
    if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        level = min(int(name[1]) + 1, 6)
        text = normalize_text(node.get_text(" ", strip=True))
        return [f"{'#' * level} {text}"] if text else []
    if name == "img":
        src = node.get("src", "").strip()
        if not src:
            return []
        alt = normalize_text(node.get("alt", ""))
        line = f"<!-- image_asset: {src} -->"
        if alt:
            line = f"{line} {alt}"
        return [line]
    if name in {"ul", "ol"}:
        lines: list[str] = []
        for index, item in enumerate(node.find_all("li", recursive=False), start=1):
            text = normalize_text(item.get_text(" ", strip=True))
            if not text:
                continue
            prefix = f"{index}." if name == "ol" else "-"
            lines.append(f"{prefix} {text}")
        return lines
    if name == "table":
        rendered = render_markdown_table(node)
        return [rendered] if rendered else []
    if name == "figure":
        lines: list[str] = []
        for image in node.find_all("img"):
            lines.extend(render_block(image))
        caption = extract_caption_text(node.find("img")) if node.find("img") is not None else ""
        if caption:
            lines.append(caption)
        return lines
    if name in {"body", "section", "article", "main", "div"}:
        lines: list[str] = []
        for child in node.children:
            lines.extend(render_block(child))
        return lines
    text = normalize_text(node.get_text(" ", strip=True))
    return [text] if text else []


def render_document_markdown(item: epub.EpubHtml) -> str:
    soup = BeautifulSoup(item.get_content(), "html.parser")
    root = soup.find("body") or soup
    blocks: list[str] = []
    for child in root.children:
        blocks.extend(render_block(child))
    cleaned_blocks = [block for block in blocks if block and block.strip()]
    return "\n\n".join(cleaned_blocks)


def write_index(chapters: list[dict[str, object]], out_dir: Path, title: str, epub_name: str) -> None:
    (out_dir / "chapters.json").write_text(
        json.dumps(chapters, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Chapter Index",
        "",
        f"- Book: `{title}`",
        f"- EPUB: `{epub_name}`",
        "",
        "| Nr. | Title | Source segments | Source | Translation | Research |",
        "| --- | ----- | --------------- | ------ | ----------- | -------- |",
    ]
    for chapter in chapters:
        slug = str(chapter["slug"])
        source_segments = "<br>".join(str(href) for href in chapter["source_hrefs"])
        lines.append(
            f"| {chapter['number']} | {chapter['title']} | {source_segments} | "
            f"../chapters-en/{slug}.md | ../../lt/chapters/{slug}.md | ../../research/{slug}.md |"
        )
    (out_dir / "chapters.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_chapter_sources(
    chapters: list[dict[str, object]],
    docs_by_href: dict[str, epub.EpubHtml],
    epub_name: str,
    out_dir: Path,
) -> None:
    for chapter in chapters:
        slug = str(chapter["slug"])
        lines = [
            f"# {chapter['full_title']}",
            "",
            f"- Šaltinio segmentai: {' | '.join(str(href) for href in chapter['source_hrefs'])}",
            f"- EPUB: {epub_name}",
            "",
        ]
        for href in chapter["source_hrefs"]:
            item = docs_by_href.get(str(href))
            if item is None:
                raise SystemExit(f"EPUB spine dokumentas nerastas pagal href: {href}")
            lines.append(f"<!-- source_href: {href} -->")
            markdown = render_document_markdown(item)
            if markdown:
                lines.append(markdown)
            lines.append("")
        (out_dir / f"{slug}.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def asset_suffix_for(item: epub.EpubItem, resolved_href: str) -> str:
    suffix = Path(resolved_href).suffix.lower()
    if suffix:
        return suffix
    media_type = getattr(item, "media_type", "")
    if media_type == "image/png":
        return ".png"
    if media_type == "image/jpeg":
        return ".jpg"
    if media_type == "image/svg+xml":
        return ".svg"
    if media_type == "image/gif":
        return ".gif"
    return ".bin"


def write_figure_inventory(
    chapters: list[dict[str, object]],
    docs_by_href: dict[str, epub.EpubHtml],
    image_items: dict[str, epub.EpubItem],
    book_root: Path,
) -> None:
    rows: list[dict[str, str]] = []
    figures_raw_dir = book_root / "source" / "figures-raw"

    for chapter in chapters:
        seen_assets: set[str] = set()
        figure_counter = 0
        for source_href in chapter["source_hrefs"]:
            item = docs_by_href.get(str(source_href))
            if item is None:
                continue
            soup = BeautifulSoup(item.get_content(), "html.parser")
            for img_tag in soup.find_all("img"):
                raw_src = img_tag.get("src", "").strip()
                resolved_asset_href = resolve_relative_href(str(source_href), raw_src)
                if not resolved_asset_href or resolved_asset_href in seen_assets:
                    continue
                image_item = image_items.get(resolved_asset_href)
                if image_item is None:
                    continue
                seen_assets.add(resolved_asset_href)
                figure_counter += 1
                source_figure_id = f"{chapter['slug']}-fig-{figure_counter:02d}"
                asset_rel_path = Path("source") / "figures-raw" / f"{source_figure_id}{asset_suffix_for(image_item, resolved_asset_href)}"
                target_asset_path = book_root / asset_rel_path
                target_asset_path.parent.mkdir(parents=True, exist_ok=True)
                target_asset_path.write_bytes(image_item.get_content())

                rows.append(
                    {
                        "source_figure_id": source_figure_id,
                        "chapter_slug": str(chapter["slug"]),
                        "source_href": str(source_href),
                        "asset_path": asset_rel_path.as_posix(),
                        "media_type": getattr(image_item, "media_type", ""),
                        "alt_text": normalize_text(img_tag.get("alt", "")),
                        "caption_text": extract_caption_text(img_tag),
                        "notes": f"source_asset_href={resolved_asset_href}",
                    }
                )

    write_tsv(book_root / "source" / "index" / "figures.tsv", FIGURE_INDEX_FIELDS, rows)


def copy_template(book_root: Path) -> None:
    if not TEMPLATE_ROOT.exists():
        raise SystemExit(f"Nerastas shared template katalogas: {TEMPLATE_ROOT}")
    shutil.copytree(TEMPLATE_ROOT, book_root)
    internal_manifest = book_root / "template_manifest.json"
    if internal_manifest.exists():
        internal_manifest.unlink()


def template_context(book_root: Path, title: str, epub_name: str) -> dict[str, str]:
    return {
        "BOOK_TITLE": title,
        "BOOK_SLUG": book_root.name,
        "BOOK_ROOT": book_root.relative_to(REPO_ROOT).as_posix(),
        "BOOK_SOURCE_KIND": "epub",
        "BOOK_SOURCE_NAME": epub_name,
        "BOOK_PDF_NAME": "SOURCE.pdf",
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
    if sys.platform != "darwin":
        raise SystemExit(
            "Obsidian sync install per bootstrap palaikomas tik macOS aplinkoje. "
            "Paleiskite bootstrap be `--install-obsidian-sync`."
        )
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
    ensure_epub_runtime_dependencies()
    epub_path = resolve_repo_path(args.epub)
    if not epub_path.exists():
        raise SystemExit(f"Nerastas EPUB: {epub_path}")
    chapter_map, _ = chapter_map_context(args, epub_path)

    book = epub.read_epub(str(epub_path))
    title = metadata_title(book, chapter_map)
    slug = slug_from_title(title, chapter_map)
    if not slug:
        raise SystemExit(f"Nepavyko sugeneruoti slug iš pavadinimo `{title}`.")

    book_root = REPO_ROOT / "books" / slug
    if book_root.exists():
        raise SystemExit(f"Target book root jau egzistuoja: {book_root}")

    copy_template(book_root)

    source_index_dir = book_root / "source" / "index"
    source_chapters_dir = book_root / "source" / "chapters-en"
    source_epub_dir = book_root / "source" / "epub"
    target_epub = source_epub_dir / epub_path.name
    shutil.copy2(epub_path, target_epub)

    render_template_files(book_root, template_context(book_root, title, target_epub.name))

    chapters = (
        build_chapters_from_map(book, chapter_map)
        if chapter_map is not None
        else build_chapters_from_toc(book)
    )

    docs_by_href = {
        str(doc["href"]): doc["item"]
        for doc in load_spine_documents(book)
    }
    image_items = {
        normalize_href(getattr(item, "file_name", "") or item.get_name()): item
        for item in book.get_items_of_type(ITEM_IMAGE)
        if normalize_href(getattr(item, "file_name", "") or item.get_name())
    }

    write_index(chapters, source_index_dir, title, target_epub.name)
    write_chapter_sources(chapters, docs_by_href, target_epub.name, source_chapters_dir)
    write_figure_inventory(chapters, docs_by_href, image_items, book_root)
    if args.install_obsidian_sync:
        install_obsidian_sync(book_root)

    print(f"Bootstrapped EPUB workspace: {book_root}")
    print(f"Source EPUB: {target_epub}")
    print(f"Chapters indexed: {len(chapters)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
