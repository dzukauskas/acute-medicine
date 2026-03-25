#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Iterable

import yaml


BOOK_ROOT = Path("books/acute-medicine")
SOURCE_CHAPTERS_DIR = BOOK_ROOT / "source" / "chapters-en"
LT_CHAPTERS_DIR = BOOK_ROOT / "lt" / "chapters"
RESEARCH_DIR = BOOK_ROOT / "research"
CHAPTER_PACKS_DIR = BOOK_ROOT / "chapter_packs"
ADJUDICATION_PACKS_DIR = BOOK_ROOT / "adjudication_packs"
GOLD_SECTIONS_DIR = BOOK_ROOT / "gold_sections"

MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
INLINE_CODE_RE = re.compile(r"`([^`]*)`")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
INVENTORY_PLACEHOLDER_RE = re.compile(r"^kol kas neužfiksuota$", re.IGNORECASE)
GENERATED_ARTIFACT_RE = re.compile(
    r"^(Sukurtas lietuviškas|Kanoninis šaltinis|Whimsical URL|Įrašyta į)\b",
    re.IGNORECASE,
)
STRUCTURED_SOURCE_HEADING_RE = re.compile(
    r"^(?P<kind>Table|Figure|Box|Chart)\s+"
    r"(?P<label>[0-9.]+)"
    r"(?:\s*[\u2000-\u200B]+\s*|\s{2,})"
    r"(?P<title>.+?)\s*$"
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows: list[dict[str, str]] = []
        for row in reader:
            normalized_row: dict[str, str] = {}
            for key, value in row.items():
                if isinstance(value, list):
                    normalized_row[key] = " | ".join(part.strip() for part in value if part and part.strip())
                else:
                    normalized_row[key] = (value or "").strip()
            rows.append(normalized_row)
        return rows


def split_multi(value: str) -> list[str]:
    if not value.strip():
        return []
    return [item.strip() for item in re.split(r"[|,;]", value) if item.strip()]


def join_multi(values: Iterable[str]) -> str:
    return " | ".join(value.strip() for value in values if value and value.strip())


def parse_bool(value: str, default: bool = False) -> bool:
    cleaned = (value or "").strip().lower()
    if not cleaned:
        return default
    return cleaned in {"1", "true", "yes", "y", "taip"}


def strip_markdown(text: str) -> str:
    text = INLINE_CODE_RE.sub(r"\1", text)
    text = MARKDOWN_LINK_RE.sub(r"\1", text)
    return text


def normalize_key(text: str) -> str:
    text = strip_markdown(text)
    text = text.replace("\xa0", " ").lower()
    text = re.sub(r"[_/]+", " ", text)
    text = re.sub(r"[^a-z0-9ąčęėįšųūž\- ]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def slugify(text: str) -> str:
    text = normalize_key(text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def resolve_chapter_slug(raw: str) -> str:
    candidate = raw.strip()
    if re.fullmatch(r"\d{1,3}", candidate):
        prefix = f"{int(candidate):03d}-"
        matches = sorted(path.stem for path in SOURCE_CHAPTERS_DIR.glob(f"{prefix}*.md"))
        if not matches:
            raise FileNotFoundError(f"Nerastas skyrius numeriu {candidate}.")
        return matches[0]
    if candidate.endswith(".md"):
        candidate = Path(candidate).stem
    return candidate


def chapter_paths_for_slug(slug: str) -> dict[str, Path]:
    return {
        "source": SOURCE_CHAPTERS_DIR / f"{slug}.md",
        "lt": LT_CHAPTERS_DIR / f"{slug}.md",
        "research": RESEARCH_DIR / f"{slug}.md",
        "pack": CHAPTER_PACKS_DIR / f"{slug}.yaml",
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


def parse_markdown_sections(text: str) -> dict[tuple[str, ...], list[str]]:
    sections: dict[tuple[str, ...], list[str]] = {}
    stack: list[str] = []
    current_key: tuple[str, ...] | None = None
    for line in text.splitlines():
        heading_match = HEADING_RE.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            stack = stack[: level - 1]
            stack.append(title)
            current_key = tuple(stack)
            sections.setdefault(current_key, [])
            continue
        if current_key is not None:
            sections[current_key].append(line)
    return sections


def bullet_items(lines: Iterable[str]) -> list[str]:
    items: list[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line.startswith("- "):
            continue
        value = strip_markdown(line[2:].strip())
        if value:
            items.append(value)
    return items


def metadata_value(lines: Iterable[str], label: str) -> str:
    prefix = f"- {label}:"
    for raw_line in lines:
        line = raw_line.strip()
        if line.startswith(prefix):
            return strip_markdown(line[len(prefix):].strip())
    return ""


def parse_structured_label(text: str) -> tuple[str, str]:
    match = re.match(r"^(Table|Figure|Box|Chart)\s+([0-9.]+)\s+(.*)$", text)
    if not match:
        return "", ""
    return match.group(1).lower(), match.group(2)


def clean_inventory_items(items: list[str]) -> list[str]:
    cleaned: list[str] = []
    for item in items:
        stripped = item.strip()
        if not stripped:
            continue
        if INVENTORY_PLACEHOLDER_RE.match(stripped):
            continue
        if GENERATED_ARTIFACT_RE.match(stripped):
            continue
        cleaned.append(stripped)
    return cleaned


def extract_inventory(sections: dict[tuple[str, ...], list[str]]) -> dict[str, list[str]]:
    def find_lines(*suffix: str) -> list[str]:
        for key, lines in sections.items():
            if len(key) >= len(suffix) and tuple(key[-len(suffix):]) == suffix:
                return lines
        return []

    return {
        "subsections": clean_inventory_items(bullet_items(find_lines("PDF inventorius", "Poskyriai"))),
        "tables": clean_inventory_items(bullet_items(find_lines("PDF inventorius", "Lentelės"))),
        "figures": clean_inventory_items(
            bullet_items(find_lines("PDF inventorius", "Paveikslai / schemos / algoritmai"))
        ),
        "boxes": clean_inventory_items(bullet_items(find_lines("PDF inventorius", "Rėmeliai / papildomi blokai"))),
        "risky_terms": bullet_items(find_lines("Rizikingi terminai")),
        "language_risks": bullet_items(find_lines("Kalbinės rizikos vietos")),
        "anti_calque": bullet_items(find_lines("Anti-calque perrašymo pastabos")),
        "localization_decisions": bullet_items(find_lines("Lokalizacijos sprendimai")),
        "local_practice_changes": bullet_items(find_lines("Vietos, kur originalas pakeistas pagal Lietuvos praktiką")),
    }


def extract_source_structured_items(source_text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for raw_line in source_text.splitlines():
        line = raw_line.strip()
        match = STRUCTURED_SOURCE_HEADING_RE.match(line)
        if not match:
            continue
        kind = match.group("kind").lower()
        label = match.group("label")
        key = (kind, label)
        if key in seen:
            continue
        seen.add(key)
        items.append(
            {
                "kind": kind,
                "label": label,
                "title": strip_markdown(match.group("title").strip()),
                "raw": line,
            }
        )
    return items


def normalize_yaml_structure(value: object) -> object:
    if isinstance(value, dict):
        return {key: normalize_yaml_structure(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [normalize_yaml_structure(item) for item in value]
    return value
