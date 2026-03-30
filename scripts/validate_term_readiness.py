#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from workflow_book import resolve_chapter_slug
from workflow_policy import load_acronym_rows, load_termbase_rows
from workflow_rules import (
    activate_book_root,
    normalize_key,
    term_candidates_path,
)
from mine_term_candidates import refresh_term_candidates_for_chapter


HIGH_RISK_ORIGINS = {
    "research_risky_term",
    "source_heading",
    "source_guideline_title",
}
NON_BLOCKING_STATUSES = {
    "rejected",
    "original_context_only",
    "localization_only",
    "not_term",
    "not_acronym",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate that high-risk terminology has been resolved before chapter_pack drafting."
    )
    parser.add_argument("--book-root", help="Optional books/<slug> root. If omitted, uses MEDBOOK_ROOT.")
    parser.add_argument("chapter", help="Chapter slug or number.")
    return parser.parse_args()


def split_multi(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def candidate_origins(row: dict[str, str]) -> set[str]:
    return {normalize_key(origin).replace(" ", "_") for origin in split_multi(row.get("candidate_origin", ""))}


def candidate_status(row: dict[str, str]) -> str:
    return normalize_key(row.get("status", "")).replace(" ", "_")


def is_active_term(row: dict[str, str], approved_terms: set[str], approved_acronyms: set[str]) -> bool:
    if row.get("candidate_kind", "").strip() == "acronym":
        return row.get("source_term", "").strip() in approved_acronyms
    return normalize_key(row.get("source_term", "")) in approved_terms


def is_high_risk_candidate(row: dict[str, str]) -> bool:
    return bool(candidate_origins(row) & HIGH_RISK_ORIGINS)


def format_candidate_error(row: dict[str, str], candidates_path: Path) -> str:
    kind = row.get("candidate_kind", "").strip() or "term"
    source_term = row.get("source_term", "").strip() or "<be termino>"
    status = row.get("status", "").strip() or "candidate"
    source_context = row.get("source_context", "").strip()
    source_expansion = row.get("source_expansion", "").strip()
    suggested_targets = (
        "`shared/lexicon/acronyms.tsv` arba `books/<slug>/acronyms.local.tsv`"
        if kind == "acronym"
        else "`shared/lexicon/termbase.tsv` arba `books/<slug>/termbase.local.tsv`"
    )
    context_note = f" Kontekstas: {source_context}" if source_context else ""
    expansion_note = f" Išskleidimas: {source_expansion}." if source_expansion else ""
    return (
        f"{candidates_path}: aukštos rizikos {kind} kandidatas `{source_term}` liko neužrakintas "
        f"(statusas `{status}`).{expansion_note}{context_note}\n"
        "Repo taisyklės yra privalomos: prieš `chapter_pack` generavimą tokį vienetą reikia "
        f"arba įrašyti į aktyvią bazę ({suggested_targets}), arba aiškiai sužymėti kaip "
        "`rejected`, `original_context_only` ar `localization_only`, jei tai nėra aktyvus LT terminas. "
        "Medicininio LT atitikmens negalima spėti: prieš užrakinant reikia patikrinti interneto LT šaltiniuose "
        "pagal repo source-priority taisykles ir užrašyti šaltinį bei datą `research` faile."
    )


def validate_term_readiness(
    slug: str,
    *,
    book_root: str | Path | None = None,
    current_rows: list[dict[str, str]] | None = None,
) -> list[str]:
    approved_terms = {normalize_key(row.get("en", "")) for row in load_termbase_rows(book_root) if row.get("en", "").strip()}
    approved_acronyms = {row.get("acronym", "").strip() for row in load_acronym_rows(book_root) if row.get("acronym", "").strip()}
    candidates_path = term_candidates_path(book_root)
    chapter_rows = (
        current_rows
        if current_rows is not None
        else refresh_term_candidates_for_chapter(slug, book_root=book_root)
    )

    errors: list[str] = []
    for row in chapter_rows:
        if not is_high_risk_candidate(row):
            continue
        if is_active_term(row, approved_terms, approved_acronyms):
            continue
        if candidate_status(row) in NON_BLOCKING_STATUSES:
            continue
        errors.append(format_candidate_error(row, candidates_path))
    return errors


def validate_term_readiness_or_raise(
    slug: str,
    *,
    book_root: str | Path | None = None,
    current_rows: list[dict[str, str]] | None = None,
) -> None:
    errors = validate_term_readiness(slug, book_root=book_root, current_rows=current_rows)
    if errors:
        raise ValueError("\n".join(errors))


def main() -> int:
    args = parse_args()
    activate_book_root(args.book_root)
    slug = resolve_chapter_slug(args.chapter, args.book_root)
    validate_term_readiness_or_raise(slug, book_root=args.book_root)
    print(term_candidates_path(args.book_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
