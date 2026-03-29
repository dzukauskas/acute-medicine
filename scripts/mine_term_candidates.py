#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from book_workflow_support import (
    TERM_CANDIDATE_FIELDS,
    activate_book_root,
    chapter_paths_for_slug,
    extract_inventory,
    load_acronym_rows,
    load_localization_overrides,
    load_localization_signal_specs,
    load_term_candidate_rows,
    load_termbase_rows,
    normalize_key,
    parse_markdown_sections,
    strip_markdown,
    read_tsv,
    resolve_chapter_slug,
    slugify,
    term_candidates_path,
    write_tsv,
)


ACRONYM_RE = re.compile(r"\b[A-Z][A-Z0-9-]{1,11}\b")
EXPANSION_BEFORE_RE = re.compile(
    r"(?P<expansion>[A-Za-z][A-Za-z0-9 ,/'-]{3,120}?)\s+\((?P<acronym>[A-Z][A-Z0-9-]{1,11})\)"
)
EXPANSION_AFTER_RE = re.compile(
    r"\b(?P<acronym>[A-Z][A-Z0-9-]{1,11})\s+\((?P<expansion>[A-Za-z][A-Za-z0-9 ,/'-]{3,120}?)\)"
)
ACRONYM_STOPWORDS = {
    "CSV",
    "ECG",
    "EMA",
    "EPUB",
    "EU",
    "GMP",
    "HTML",
    "LT",
    "LT/EU",
    "MD",
    "NHS",
    "PDF",
    "PNG",
    "README",
    "TODO",
    "TSV",
    "UK",
    "URL",
    "US",
    "YAML",
}
NON_TERMINOLOGY_KEYWORDS = {
    "app",
    "apps",
    "association",
    "board",
    "college",
    "committee",
    "contributors",
    "council",
    "developer",
    "developers",
    "edition",
    "guideline",
    "guidelines",
    "investigation",
    "panel",
    "platform",
    "plus",
    "portal",
    "program",
    "programme",
    "ruling",
    "rulings",
    "society",
    "tool",
    "tools",
    "website",
}
RESEARCH_NOTE_KEYWORDS = {
    "kalba",
    "kalbin",
    "kolok",
    "kontekst",
    "konstruk",
    "stili",
    "sakini",
    "vartosen",
    "formuluot",
}
MANUAL_PRESERVE_FIELDS = ("proposed_lt", "status", "scope", "banned_lt", "source_ref", "notes")
PERSON_TITLE_TOKENS = {"dr", "mr", "mrs", "ms", "prof", "professor"}
SOURCE_HEADING_RE = re.compile(r"^(?P<level>#{1,6})\s+(?P<title>.+)$")
TABLE_ROW_RE = re.compile(r"^\|.*\|$")
TABLE_SEPARATOR_RE = re.compile(r"^:?-{3,}:?$")
GENERIC_SOURCE_TITLE_TERMS = {
    "chapter",
    "general guidance",
    "guideline title",
    "introduction",
    "medical",
    "maternity",
    "resuscitation",
    "special situations",
    "test chapter",
    "trauma",
    "update analysis what s changed",
}
TITLE_QUALIFIER_PATTERNS = (
    re.compile(r"\s+\((?:formerly|previously)\b[^)]*\)\s*$", re.IGNORECASE),
    re.compile(r"\s+in\s+adults?(?:\s+and\s+children)?\s*$", re.IGNORECASE),
    re.compile(r"\s+in\s+children\s*$", re.IGNORECASE),
    re.compile(r"\s+during\s+pregnancy\b.*$", re.IGNORECASE),
    re.compile(r"\s+after\s+\d+\s+weeks?\s+gestation\b.*$", re.IGNORECASE),
    re.compile(r"\s+up\s+to\s+\d+\s+weeks?\s+gestation\b.*$", re.IGNORECASE),
)
TITLE_WORD_MIN = 2
TITLE_WORD_MAX = 6


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mine per-chapter terminology and acronym candidates into books/<slug>/term_candidates.tsv."
    )
    parser.add_argument("--book-root", help="Optional books/<slug> root. If omitted, uses MEDBOOK_ROOT.")
    parser.add_argument("chapter", help="Chapter slug or number.")
    parser.add_argument(
        "--out",
        help="Optional output TSV path. Defaults to books/<slug>/term_candidates.tsv.",
    )
    return parser.parse_args()


def is_acronym(value: str) -> bool:
    return bool(ACRONYM_RE.fullmatch(value.strip()))


def join_unique(existing: str, incoming: str, *, delimiter: str = " | ") -> str:
    seen: list[str] = []
    for raw_blob in (existing, incoming):
        for item in raw_blob.split(delimiter):
            cleaned = item.strip()
            if cleaned and cleaned not in seen:
                seen.append(cleaned)
    return delimiter.join(seen)


def clean_source_line(line: str) -> str:
    cleaned = line.strip()
    if not cleaned or cleaned.startswith("<!--"):
        return ""
    return cleaned


def find_source_context(source_text: str, marker: str) -> str:
    marker_norm = normalize_key(marker)
    if not marker_norm:
        return ""
    for raw_line in source_text.splitlines():
        line = clean_source_line(raw_line)
        if line and marker_norm in normalize_key(line):
            return line
    return ""


def extract_acronym_expansions(source_text: str) -> dict[str, str]:
    expansions: dict[str, str] = {}
    for pattern in (EXPANSION_BEFORE_RE, EXPANSION_AFTER_RE):
        for match in pattern.finditer(source_text):
            acronym = match.group("acronym").strip()
            expansion = re.sub(r"\s+", " ", match.group("expansion")).strip(" -,:;")
            if acronym and expansion and acronym not in expansions:
                expansions[acronym] = expansion
    return expansions


def approved_term_keys(book_root: str | Path | None = None) -> set[str]:
    return {normalize_key(row.get("en", "")) for row in load_termbase_rows(book_root) if row.get("en", "").strip()}


def approved_acronym_keys(book_root: str | Path | None = None) -> set[str]:
    return {row.get("acronym", "").strip() for row in load_acronym_rows(book_root) if row.get("acronym", "").strip()}


def localization_signal_terms(book_root: str | Path | None = None) -> set[str]:
    terms: set[str] = set()
    for row in load_localization_signal_specs(book_root):
        source_term = normalize_key(row.get("source_term", ""))
        if source_term:
            terms.add(source_term)
    for row in load_localization_overrides(book_root=book_root):
        source_term = normalize_key(row.get("source_term", ""))
        if source_term:
            terms.add(source_term)
    return terms


def looks_like_localization_signal(source_term: str, signal_terms: set[str]) -> bool:
    normalized = normalize_key(source_term)
    if not normalized:
        return False
    return any(signal == normalized or signal in normalized or normalized in signal for signal in signal_terms)


def candidate_row(
    *,
    chapter_slug: str,
    candidate_kind: str,
    source_term: str,
    source_context: str,
    candidate_origin: str,
    reason: str,
    source_expansion: str = "",
) -> dict[str, str]:
    return {
        "candidate_id": f"{chapter_slug}-{candidate_kind}-{slugify(source_term)}",
        "candidate_kind": candidate_kind,
        "source_term": source_term.strip(),
        "source_expansion": source_expansion.strip(),
        "chapter_slug": chapter_slug,
        "source_context": source_context.strip(),
        "proposed_lt": "",
        "status": "candidate",
        "scope": "book",
        "candidate_origin": candidate_origin,
        "reason": reason,
        "banned_lt": "",
        "source_ref": "",
        "notes": "",
    }


def looks_like_non_terminology_candidate(*values: str) -> bool:
    blob = normalize_key(" ".join(value for value in values if value))
    return any(keyword in blob for keyword in NON_TERMINOLOGY_KEYWORDS)


def looks_like_research_note(value: str, source_context: str) -> bool:
    normalized = normalize_key(value)
    if any(keyword in normalized for keyword in RESEARCH_NOTE_KEYWORDS):
        return True
    if "/" in value and not source_context:
        return True
    if len(value.split()) > 6 and not source_context:
        return True
    return False


def looks_like_person_name_context(source_context: str, source_expansion: str) -> bool:
    if source_expansion.strip():
        return False
    tokens = re.findall(r"[A-Za-z]+", source_context)
    if not tokens or len(tokens) > 4:
        return False
    non_title_tokens = [token for token in tokens if token.lower() not in PERSON_TITLE_TOKENS]
    if not non_title_tokens:
        return False
    return all(token.isupper() for token in non_title_tokens)


def collapse_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def strip_title_qualifiers(title: str) -> str:
    candidate = collapse_spaces(strip_markdown(title))
    candidate = re.sub(r"^chapter\s+\d+\s*[:.\-–—]?\s*", "", candidate, flags=re.IGNORECASE)
    candidate = re.sub(r"\s*\([^)]*\)\s*$", "", candidate)
    for pattern in TITLE_QUALIFIER_PATTERNS:
        candidate = pattern.sub("", candidate)
    return collapse_spaces(candidate.strip(" -–—:;,."))


def is_title_candidate(value: str, *, source_context: str = "") -> bool:
    candidate = strip_title_qualifiers(value)
    normalized = normalize_key(candidate)
    if not normalized or normalized in GENERIC_SOURCE_TITLE_TERMS or normalized.endswith(" chapter"):
        return False
    words = candidate.split()
    if len(words) < TITLE_WORD_MIN or len(words) > TITLE_WORD_MAX:
        return False
    if looks_like_non_terminology_candidate(candidate, source_context):
        return False
    return True


def source_heading_titles(source_text: str) -> list[tuple[str, str]]:
    titles: list[tuple[str, str]] = []
    seen: set[str] = set()
    for raw_line in source_text.splitlines():
        match = SOURCE_HEADING_RE.match(raw_line.strip())
        if not match:
            continue
        title = strip_markdown(match.group("title").strip())
        candidate = strip_title_qualifiers(title)
        if not is_title_candidate(candidate, source_context=raw_line):
            continue
        normalized = normalize_key(candidate)
        if normalized in seen:
            continue
        seen.add(normalized)
        titles.append((candidate, raw_line.strip()))
    return titles


def source_guideline_titles(source_text: str) -> list[tuple[str, str]]:
    titles: list[tuple[str, str]] = []
    seen: set[str] = set()

    def split_row(line: str) -> list[str]:
        return [cell.strip() for cell in line.strip().strip("|").split("|")]

    def iter_table_blocks(text: str) -> list[list[str]]:
        blocks: list[list[str]] = []
        current: list[str] = []
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if TABLE_ROW_RE.match(line):
                current.append(line)
                continue
            if current:
                blocks.append(current)
                current = []
        if current:
            blocks.append(current)
        return blocks

    for block in iter_table_blocks(source_text):
        if len(block) < 3:
            continue
        header = split_row(block[0])
        separator = split_row(block[1])
        if not header or len(separator) < len(header):
            continue
        if not all(TABLE_SEPARATOR_RE.match(cell.replace(" ", "")) for cell in separator[: len(header)]):
            continue
        for line in block[2:]:
            cells = split_row(line)
            if not cells:
                continue
            first_cell = cells[0].strip()
            if not first_cell:
                continue
            if normalize_key(first_cell) in GENERIC_SOURCE_TITLE_TERMS:
                continue
            if len(cells) > 1 and all(not cell.strip() for cell in cells[1:]):
                continue
            candidate = strip_title_qualifiers(first_cell)
            if not is_title_candidate(candidate, source_context=first_cell):
                continue
            normalized = normalize_key(candidate)
            if normalized in seen:
                continue
            seen.add(normalized)
            titles.append((candidate, line))
    return titles


def merge_candidate_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    merged: dict[str, dict[str, str]] = {}
    order: list[str] = []

    for row in rows:
        candidate_id = row["candidate_id"]
        if candidate_id not in merged:
            merged[candidate_id] = dict(row)
            order.append(candidate_id)
            continue
        current = merged[candidate_id]
        current["candidate_origin"] = join_unique(current["candidate_origin"], row["candidate_origin"])
        current["reason"] = join_unique(current["reason"], row["reason"])
        if not current["source_context"] and row["source_context"]:
            current["source_context"] = row["source_context"]
        if not current["source_expansion"] and row["source_expansion"]:
            current["source_expansion"] = row["source_expansion"]

    return [merged[candidate_id] for candidate_id in order]


def mine_risky_term_candidates(
    *,
    chapter_slug: str,
    source_text: str,
    research_text: str,
    book_root: str | Path | None = None,
) -> list[dict[str, str]]:
    inventory = extract_inventory(parse_markdown_sections(research_text))
    known_terms = approved_term_keys(book_root)
    known_acronyms = approved_acronym_keys(book_root)
    localization_terms = localization_signal_terms(book_root)
    expansions = extract_acronym_expansions(source_text)

    rows: list[dict[str, str]] = []
    for risky_term in inventory["risky_terms"]:
        cleaned = risky_term.strip()
        if not cleaned:
            continue
        if looks_like_localization_signal(cleaned, localization_terms):
            continue
        source_context = find_source_context(source_text, cleaned)
        if is_acronym(cleaned):
            if cleaned in known_acronyms or cleaned in ACRONYM_STOPWORDS:
                continue
            source_expansion = expansions.get(cleaned, "")
            if looks_like_non_terminology_candidate(cleaned, source_context, source_expansion):
                continue
            rows.append(
                candidate_row(
                    chapter_slug=chapter_slug,
                    candidate_kind="acronym",
                    source_term=cleaned,
                    source_expansion=source_expansion,
                    source_context=source_context,
                    candidate_origin="research_risky_term",
                    reason="Užfiksuota `## Rizikingi terminai`, bet nėra aktyvioje akronimų bazėje.",
                )
            )
            continue
        if normalize_key(cleaned) in known_terms:
            continue
        if looks_like_non_terminology_candidate(cleaned, source_context):
            continue
        if looks_like_research_note(cleaned, source_context):
            continue
        rows.append(
            candidate_row(
                chapter_slug=chapter_slug,
                candidate_kind="term",
                source_term=cleaned,
                source_context=source_context,
                candidate_origin="research_risky_term",
                reason="Užfiksuota `## Rizikingi terminai`, bet nėra aktyvioje terminų bazėje.",
            )
        )
    return merge_candidate_rows(rows)


def mine_source_acronym_candidates(
    *,
    chapter_slug: str,
    source_text: str,
    book_root: str | Path | None = None,
) -> list[dict[str, str]]:
    known_acronyms = approved_acronym_keys(book_root)
    localization_terms = localization_signal_terms(book_root)
    expansions = extract_acronym_expansions(source_text)

    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for match in ACRONYM_RE.finditer(source_text):
        acronym = match.group(0).strip()
        if acronym in seen or acronym in known_acronyms or acronym in ACRONYM_STOPWORDS:
            continue
        if looks_like_localization_signal(acronym, localization_terms):
            continue
        source_context = find_source_context(source_text, acronym)
        source_expansion = expansions.get(acronym, "")
        if looks_like_non_terminology_candidate(acronym, source_context, source_expansion):
            continue
        if looks_like_person_name_context(source_context, source_expansion):
            continue
        seen.add(acronym)
        rows.append(
            candidate_row(
                chapter_slug=chapter_slug,
                candidate_kind="acronym",
                source_term=acronym,
                source_expansion=source_expansion,
                source_context=source_context,
                candidate_origin="source_acronym",
                reason="Aptikta source tekste kaip santrumpa, bet nėra aktyvioje akronimų bazėje.",
            )
        )
    return rows


def mine_source_title_term_candidates(
    *,
    chapter_slug: str,
    source_text: str,
    book_root: str | Path | None = None,
) -> list[dict[str, str]]:
    known_terms = approved_term_keys(book_root)
    localization_terms = localization_signal_terms(book_root)
    rows: list[dict[str, str]] = []
    for origin, titles in (
        ("source_heading", source_heading_titles(source_text)),
        ("source_guideline_title", source_guideline_titles(source_text)),
    ):
        for source_term, source_context in titles:
            if normalize_key(source_term) in known_terms:
                continue
            if looks_like_localization_signal(source_term, localization_terms):
                continue
            rows.append(
                candidate_row(
                    chapter_slug=chapter_slug,
                    candidate_kind="term",
                    source_term=source_term,
                    source_context=source_context,
                    candidate_origin=origin,
                    reason="Aptikta aukštos vertės source antraštėje ar guideline title lauke, todėl prieš draftą turi būti sutikrinta su LT-source sluoksniu.",
                )
            )
    return merge_candidate_rows(rows)


def mine_chapter_term_candidates(
    slug: str,
    *,
    book_root: str | Path | None = None,
) -> list[dict[str, str]]:
    paths = chapter_paths_for_slug(slug, book_root)
    source_text = paths["source"].read_text(encoding="utf-8")
    research_text = paths["research"].read_text(encoding="utf-8")

    rows = []
    rows.extend(
        mine_risky_term_candidates(
            chapter_slug=slug,
            source_text=source_text,
            research_text=research_text,
            book_root=book_root,
        )
    )
    rows.extend(
        mine_source_acronym_candidates(
            chapter_slug=slug,
            source_text=source_text,
            book_root=book_root,
        )
    )
    rows.extend(
        mine_source_title_term_candidates(
            chapter_slug=slug,
            source_text=source_text,
            book_root=book_root,
        )
    )
    rows = merge_candidate_rows(rows)
    rows.sort(key=lambda row: (row["candidate_kind"], normalize_key(row["source_term"])))
    return rows


def preserve_manual_fields(current_row: dict[str, str], previous_row: dict[str, str] | None) -> dict[str, str]:
    if previous_row is None:
        return current_row
    merged = dict(current_row)
    for field in MANUAL_PRESERVE_FIELDS:
        previous_value = previous_row.get(field, "").strip()
        if previous_value:
            merged[field] = previous_value
    return merged


def refresh_term_candidates_for_chapter(
    slug: str,
    *,
    book_root: str | Path | None = None,
    output_path: str | Path | None = None,
) -> list[dict[str, str]]:
    default_path = term_candidates_path(book_root)
    target_path = Path(output_path) if output_path is not None else default_path
    existing_rows = load_term_candidate_rows(book_root) if target_path == default_path else (
        [] if not target_path.exists() else read_tsv(target_path)
    )
    current_rows = mine_chapter_term_candidates(slug, book_root=book_root)
    previous_by_id = {
        row.get("candidate_id", "").strip(): row
        for row in existing_rows
        if row.get("chapter_slug", "").strip() == slug and row.get("candidate_id", "").strip()
    }
    current_rows = [preserve_manual_fields(row, previous_by_id.get(row["candidate_id"])) for row in current_rows]
    current_ids = {row["candidate_id"] for row in current_rows}

    retained_rows: list[dict[str, str]] = []
    for row in existing_rows:
        row_slug = row.get("chapter_slug", "").strip()
        candidate_id = row.get("candidate_id", "").strip()
        if row_slug != slug:
            retained_rows.append({field: row.get(field, "") for field in TERM_CANDIDATE_FIELDS})
            continue
        if candidate_id in current_ids:
            continue
        if row.get("status", "").strip() not in {"", "candidate"}:
            retained_rows.append({field: row.get(field, "") for field in TERM_CANDIDATE_FIELDS})

    final_rows = retained_rows + current_rows
    final_rows.sort(
        key=lambda row: (
            row.get("chapter_slug", ""),
            row.get("candidate_kind", ""),
            normalize_key(row.get("source_term", "")),
        )
    )
    write_tsv(target_path, TERM_CANDIDATE_FIELDS, final_rows)
    return current_rows


def main() -> int:
    args = parse_args()
    activate_book_root(args.book_root)
    slug = resolve_chapter_slug(args.chapter, args.book_root)
    target_path = Path(args.out) if args.out else term_candidates_path(args.book_root)
    refresh_term_candidates_for_chapter(slug, book_root=args.book_root, output_path=target_path)
    print(target_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
