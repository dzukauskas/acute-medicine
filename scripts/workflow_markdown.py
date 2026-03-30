#!/usr/bin/env python3
from __future__ import annotations

import re
from typing import Iterable

from workflow_rules import normalize_key, slugify, strip_markdown


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
INVENTORY_PLACEHOLDER_RE = re.compile(r"^kol kas neužfiksuota$", re.IGNORECASE)
GENERATED_ARTIFACT_RE = re.compile(
    r"^(Sukurtas lietuviškas|Kanoninis šaltinis|Whimsical URL|Įrašyta į)\b",
    re.IGNORECASE,
)
STRUCTURED_SOURCE_HEADING_RE = re.compile(
    r"^(?P<kind>Table|Figure|Box|Chart)\s+"
    r"(?P<label>[0-9.]+)"
    r"(?:\s*[\u2000-\u200B]+\s*|\s{2,}|\s+)"
    r"(?P<title>.+?)\s*$"
)
TABLE_ROW_RE = re.compile(r"^\|.*\|$")
MARKDOWN_TABLE_SEPARATOR_RE = re.compile(r"^:?-{3,}:?$")
STRUCTURED_ALGORITHM_KEYWORDS = {"algorithm", "approach", "management"}
IGNORED_SOURCE_POLICY_SECTIONS = {"references", "further reading"}


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


def source_text_for_policy_checks(source_text: str) -> str:
    sections = parse_markdown_sections(source_text)
    if not sections:
        return source_text

    included_chunks: list[str] = []
    prefix_lines: list[str] = []
    for line in source_text.splitlines():
        if line.startswith("## "):
            break
        prefix_lines.append(line)
    included_chunks.append("\n".join(prefix_lines))

    for key, lines in sections.items():
        if normalize_key(key[-1]) in IGNORED_SOURCE_POLICY_SECTIONS:
            continue
        included_chunks.append("\n".join(lines))
    return "\n".join(chunk for chunk in included_chunks if chunk.strip())


def find_section_lines(sections: dict[tuple[str, ...], list[str]], *suffix: str) -> list[str]:
    for key, lines in sections.items():
        if len(key) >= len(suffix) and tuple(key[-len(suffix):]) == suffix:
            return lines
    return []


def find_section_lines_any(
    sections: dict[tuple[str, ...], list[str]],
    suffix_options: Iterable[tuple[str, ...]],
) -> list[str]:
    for suffix in suffix_options:
        lines = find_section_lines(sections, *suffix)
        if lines:
            return lines
    return []


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


def markdown_table_rows(lines: Iterable[str]) -> list[dict[str, str]]:
    table_lines = [line.strip() for line in lines if line.strip() and TABLE_ROW_RE.match(line.strip())]
    if len(table_lines) < 2:
        return []

    def split_row(line: str) -> list[str]:
        return [cell.strip() for cell in line.strip().strip("|").split("|")]

    header_cells = split_row(table_lines[0])
    separator_cells = split_row(table_lines[1])
    if not header_cells or len(separator_cells) < len(header_cells):
        return []
    if not all(MARKDOWN_TABLE_SEPARATOR_RE.match(cell.replace(" ", "")) for cell in separator_cells[: len(header_cells)]):
        return []

    headers = [normalize_key(cell).replace(" ", "_") for cell in header_cells]
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = split_row(line)
        if len(cells) < len(headers):
            cells.extend([""] * (len(headers) - len(cells)))
        row = {headers[idx]: cells[idx].strip() for idx in range(len(headers))}
        if any(value for value in row.values()):
            rows.append(row)
    return rows


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


def structured_block_type(kind: str, title: str) -> str:
    normalized_title = normalize_key(title)
    if kind == "table":
        return "table"
    if kind == "figure":
        if any(word in normalized_title for word in STRUCTURED_ALGORITHM_KEYWORDS):
            return "algorithm"
        return "figure_caption"
    if kind == "box":
        return "callout"
    if kind == "chart":
        return "chart"
    return "figure_caption"


def structured_block_id(kind: str, label: str, title: str) -> str:
    block_type = structured_block_type(kind, title)
    if label:
        return f"{block_type}-{label}-{slugify(title)}"
    return f"{block_type}-{slugify(title)}"


def structured_completion_hint(kind: str, label: str, title: str) -> str:
    if kind == "table":
        return f"{label} lentelė"
    if kind == "figure":
        return f"{label} paveikslas"
    if kind == "box":
        return f"{label} rėmelis"
    if kind == "chart" and "news2" in normalize_key(title):
        return "NEWS2 originalo kontekste"
    if kind == "chart":
        return f"{label} diagrama"
    return title


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
    return {
        "subsections": clean_inventory_items(
            bullet_items(
                find_section_lines_any(
                    sections,
                    (
                        ("Source inventorius", "Poskyriai"),
                        ("PDF inventorius", "Poskyriai"),
                    ),
                )
            )
        ),
        "tables": clean_inventory_items(
            bullet_items(
                find_section_lines_any(
                    sections,
                    (
                        ("Source inventorius", "Lentelės"),
                        ("PDF inventorius", "Lentelės"),
                    ),
                )
            )
        ),
        "figures": clean_inventory_items(
            bullet_items(
                find_section_lines_any(
                    sections,
                    (
                        ("Source inventorius", "Paveikslai / schemos / algoritmai"),
                        ("PDF inventorius", "Paveikslai / schemos / algoritmai"),
                    ),
                )
            )
        ),
        "boxes": clean_inventory_items(
            bullet_items(
                find_section_lines_any(
                    sections,
                    (
                        ("Source inventorius", "Rėmeliai / papildomi blokai"),
                        ("PDF inventorius", "Rėmeliai / papildomi blokai"),
                    ),
                )
            )
        ),
        "risky_terms": bullet_items(find_section_lines(sections, "Rizikingi terminai")),
        "language_risks": bullet_items(find_section_lines(sections, "Kalbinės rizikos vietos")),
        "anti_calque": bullet_items(find_section_lines(sections, "Anti-calque perrašymo pastabos")),
        "localization_decisions": bullet_items(find_section_lines(sections, "Lokalizacijos sprendimai")),
        "local_practice_changes": bullet_items(
            find_section_lines(sections, "Vietos, kur originalas pakeistas pagal Lietuvos praktiką")
        ),
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
