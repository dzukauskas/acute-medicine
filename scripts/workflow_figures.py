#!/usr/bin/env python3
from __future__ import annotations

import os
import re
from pathlib import Path

from workflow_book import chapter_paths_for_slug
from workflow_runtime import REPO_ROOT


IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def manifest_note_value(notes: str, key: str) -> str:
    match = re.search(rf"(?:^|;\s*){re.escape(key)}=([^;]+)", notes or "")
    return match.group(1).strip() if match else ""


def manifest_row_chapter_slug(row: dict[str, str]) -> str:
    return manifest_note_value(row.get("notes", ""), "chapter_slug")


def manifest_row_alt_text(row: dict[str, str]) -> str:
    return manifest_note_value(row.get("notes", ""), "alt_text")


def figure_heading(figure_number: str) -> str:
    return f"## {figure_number.strip()} paveikslas"


def chapter_image_repo_paths(chapter_path: Path) -> list[str]:
    refs: list[str] = []
    text = chapter_path.read_text(encoding="utf-8")
    for match in IMAGE_RE.finditer(text):
        resolved = (chapter_path.parent / match.group(1).strip()).resolve()
        try:
            refs.append(resolved.relative_to(REPO_ROOT).as_posix())
        except ValueError:
            continue
    return refs


def chapter_image_markdown(chapter_path: Path, row: dict[str, str]) -> str:
    png_path = row.get("png_path", "").strip()
    if not png_path:
        raise SystemExit(f"Manifest įrašui trūksta png_path: {row.get('figure_id', 'be-id')}")
    png_absolute = (REPO_ROOT / png_path).resolve()
    relative_ref = os.path.relpath(png_absolute, start=chapter_path.parent).replace(os.sep, "/")
    alt_text = manifest_row_alt_text(row) or f"{row.get('figure_number', '').strip()} paveikslas".strip()
    return f"![{alt_text or 'paveikslas'}]({relative_ref})"


def insert_figure_markdown(text: str, heading: str, image_markdown: str) -> str:
    heading_match = re.search(rf"^{re.escape(heading)}\s*$", text, flags=re.MULTILINE)
    if heading_match is not None:
        tail = text[heading_match.end() :].lstrip("\n")
        updated = text[: heading_match.end()] + f"\n\n{image_markdown}\n"
        if tail:
            updated += f"\n{tail}"
        return updated
    stripped = text.rstrip()
    if not stripped:
        return f"{heading}\n\n{image_markdown}\n"
    return f"{stripped}\n\n{heading}\n\n{image_markdown}\n"


def ensure_manifest_figure_embed(
    book_root: Path,
    row: dict[str, str],
) -> tuple[Path, bool]:
    figure_id = row.get("figure_id", "").strip() or "be-id"
    chapter_slug = manifest_row_chapter_slug(row)
    if not chapter_slug:
        raise SystemExit(f"Manifest įrašui `{figure_id}` notes lauke trūksta chapter_slug=...")

    chapter_path = chapter_paths_for_slug(chapter_slug, book_root)["lt"]
    if not chapter_path.exists():
        raise SystemExit(f"Nerastas LT skyrius aktyviam paveikslui `{figure_id}`: {chapter_path}")

    png_path = row.get("png_path", "").strip()
    if png_path in set(chapter_image_repo_paths(chapter_path)):
        return chapter_path, False

    figure_number = row.get("figure_number", "").strip()
    if not figure_number:
        raise SystemExit(f"Manifest įrašui `{figure_id}` trūksta figure_number.")

    updated = insert_figure_markdown(
        chapter_path.read_text(encoding="utf-8"),
        figure_heading(figure_number),
        chapter_image_markdown(chapter_path, row),
    )
    chapter_path.write_text(updated, encoding="utf-8")
    return chapter_path, True
