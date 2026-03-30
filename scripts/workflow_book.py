#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

import yaml
from workflow_rules import require_book_root
from workflow_runtime import REPO_ROOT


def repo_relative_path(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def first_pdf_path(book_root: Path) -> Path | None:
    pdf_dir = book_root / "source" / "pdf"
    if not pdf_dir.exists():
        return None
    pdfs = sorted(path for path in pdf_dir.glob("*.pdf") if path.is_file())
    return pdfs[0] if pdfs else None


def first_epub_path(book_root: Path) -> Path | None:
    epub_dir = book_root / "source" / "epub"
    if not epub_dir.exists():
        return None
    epubs = sorted(path for path in epub_dir.glob("*.epub") if path.is_file())
    return epubs[0] if epubs else None


def first_source_artifact(book_root: Path) -> tuple[str, Path] | None:
    pdf_path = first_pdf_path(book_root)
    if pdf_path is not None:
        return ("pdf", pdf_path)
    epub_path = first_epub_path(book_root)
    if epub_path is not None:
        return ("epub", epub_path)
    return None


def resolve_chapter_slug(raw: str, book_root: str | Path | None = None) -> str:
    candidate = raw.strip()
    source_chapters_dir = require_book_root(book_root) / "source" / "chapters-en"
    if re.fullmatch(r"\d{1,3}", candidate):
        prefix = f"{int(candidate):03d}-"
        matches = sorted(path.stem for path in source_chapters_dir.glob(f"{prefix}*.md"))
        if not matches:
            raise FileNotFoundError(f"Nerastas skyrius numeriu {candidate}.")
        return matches[0]
    if candidate.endswith(".md"):
        candidate = Path(candidate).stem
    return candidate


def chapter_paths_for_slug(slug: str, book_root: str | Path | None = None) -> dict[str, Path]:
    active_book_root = require_book_root(book_root)
    return {
        "source": active_book_root / "source" / "chapters-en" / f"{slug}.md",
        "lt": active_book_root / "lt" / "chapters" / f"{slug}.md",
        "research": active_book_root / "research" / f"{slug}.md",
        "pack": active_book_root / "chapter_packs" / f"{slug}.yaml",
    }


def chapter_number_from_slug(slug: str) -> str:
    match = re.match(r"^(\d{3})-", slug)
    if not match:
        raise ValueError(f"Nepavyko išgauti skyriaus numerio iš slug {slug!r}.")
    return match.group(1)


def scope_allows(scope: str, chapter_number: str) -> bool:
    cleaned = (scope or "all").strip().lower()
    if not cleaned or cleaned == "all":
        return True
    allowed = {item.strip() for item in re.split(r"[|,; ]+", cleaned) if item.strip()}
    return chapter_number in allowed or chapter_number.lstrip("0") in allowed


def dump_yaml(path: Path, data: dict | list) -> None:
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data or {}


def normalize_yaml_structure(value: object) -> object:
    if isinstance(value, dict):
        return {key: normalize_yaml_structure(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [normalize_yaml_structure(item) for item in value]
    return value
