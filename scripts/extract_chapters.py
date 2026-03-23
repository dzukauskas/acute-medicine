#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import fitz


PDF_NAME = (
    "Acute Medicine A Practical Guide to the Management of Medical Emergencies "
    "(Mridula Rajwani (Editor) etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf"
)


def normalize_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("\u00ad", "")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = text.replace("–\n", "–")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def slugify(text: str) -> str:
    text = text.lower().replace("\xa0", " ")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def chapter_entries(pdf: fitz.Document) -> list[dict]:
    toc = pdf.get_toc(simple=False)
    items: list[dict] = []
    for level, title, page, *_ in toc:
        title = title.replace("\xa0", " ").strip()
        if level == 2 and title.startswith("CHAPTER "):
            match = re.match(r"CHAPTER\s+(\d+)\s+(.*)", title)
            if not match:
                continue
            number = int(match.group(1))
            chapter_title = match.group(2).strip()
            items.append(
                {
                    "number": number,
                    "title": chapter_title,
                    "full_title": f"CHAPTER {number} {chapter_title}",
                    "start_page": page,
                }
            )
    for idx, item in enumerate(items):
        next_start = items[idx + 1]["start_page"] if idx + 1 < len(items) else pdf.page_count
        item["end_page"] = next_start - 1
        item["slug"] = f"{item['number']:03d}-{slugify(item['title'])}"
    return items


def extract_pages(pdf: fitz.Document, start_page: int, end_page: int) -> str:
    parts: list[str] = []
    for page_no in range(start_page, end_page + 1):
        page = pdf[page_no - 1]
        text = normalize_text(page.get_text("text"))
        if not text:
            continue
        parts.append(f"<!-- page:{page_no} -->\n{text}")
    return "\n\n".join(parts).strip()


def write_index(chapters: list[dict], out_dir: Path) -> None:
    index_json = out_dir / "chapters.json"
    index_md = out_dir / "chapters.md"
    index_json.write_text(json.dumps(chapters, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    lines = [
        "# Chapter Index",
        "",
        "| Nr. | Title | Pages | Source | Translation |",
        "| --- | ----- | ----- | ------ | ----------- |",
    ]
    for chapter in chapters:
        source = f"../en/{chapter['slug']}.md"
        translation = f"../lt/{chapter['slug']}.md"
        lines.append(
            f"| {chapter['number']} | {chapter['title']} | {chapter['start_page']}-{chapter['end_page']} "
            f"| {source} | {translation} |"
        )
    index_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_chapter_source(pdf: fitz.Document, chapter: dict, out_dir: Path) -> Path:
    target = out_dir / f"{chapter['slug']}.md"
    body = extract_pages(pdf, chapter["start_page"], chapter["end_page"])
    header = [
        f"# {chapter['full_title']}",
        "",
        f"- Pages: {chapter['start_page']}-{chapter['end_page']}",
        f"- PDF: {PDF_NAME}",
        "",
    ]
    target.write_text("\n".join(header) + body + "\n", encoding="utf-8")
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract chapter text from the PDF into Markdown.")
    parser.add_argument("--pdf", default=PDF_NAME, help="Path to the source PDF.")
    parser.add_argument("--chapter", type=int, help="Extract only one chapter number.")
    parser.add_argument("--all", action="store_true", help="Extract every chapter.")
    parser.add_argument("--out", default="study", help="Output directory root.")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    out_root = Path(args.out)
    en_dir = out_root / "en"
    index_dir = out_root / "index"
    en_dir.mkdir(parents=True, exist_ok=True)
    index_dir.mkdir(parents=True, exist_ok=True)

    pdf = fitz.open(pdf_path)
    chapters = chapter_entries(pdf)
    write_index(chapters, index_dir)

    if args.chapter:
        selected = [item for item in chapters if item["number"] == args.chapter]
    elif args.all:
        selected = chapters
    else:
        raise SystemExit("Use --chapter N or --all.")

    if not selected:
        raise SystemExit("No matching chapter found.")

    for chapter in selected:
        path = write_chapter_source(pdf, chapter, en_dir)
        print(path)


if __name__ == "__main__":
    main()
