#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from workflow_markdown import (
    bullet_items,
    find_section_lines,
    markdown_table_rows,
    source_text_for_policy_checks,
)
from workflow_rules import (
    acronym_paths,
    adjudication_profile_paths,
    calque_pattern_paths,
    clinical_policy_markers_path,
    disallowed_phrase_paths,
    disallowed_term_paths,
    gold_phrase_paths,
    gold_section_index_sources,
    localization_override_paths,
    localization_signal_registry_paths,
    lt_source_map_path,
    merge_appended_rows,
    merge_keyed_rows,
    normalize_key,
    optional_tsv_rows,
    require_tsv_rows,
    resolve_indexed_text_path,
    review_taxonomy_path,
    split_multi,
    term_candidates_path,
    termbase_paths,
)


LOCALIZATION_REPLACEMENT_MODES = {
    "replace_lt",
    "replace_eu",
    "genericize",
    "original_context_callout",
    "omit_nontransferable",
}
CLINICAL_CLAIM_TYPES = {
    "dose",
    "indication",
    "contraindication",
    "route",
    "concentration",
    "algorithm_step",
    "monitoring",
    "legal_scope",
    "market_availability",
}
CLAIM_FINAL_RENDERINGS = {
    "keep_lt_normative",
    "keep_eu_normative",
    "original_context_callout",
    "omit",
}
STRUCTURED_BLOCK_STRATEGIES = {
    "rewrite_lt",
    "compress_lt",
    "recreate_figure",
    "original_context_callout",
    "omit",
}
AUDIT_STATUSES = {"ok", "sutvarkyta", "eskaluoti"}
CLINICAL_CLAIM_TYPE_ALIASES = {
    "market availability": "market_availability",
    "market_availability": "market_availability",
    "legal scope": "legal_scope",
    "legal_scope": "legal_scope",
    "algorithm step": "algorithm_step",
    "algorithm_step": "algorithm_step",
}
LOCALIZATION_SIGNAL_MATCH_MODES = {"literal", "regex"}
CLINICAL_POLICY_MARKER_MATCH_MODES = {"literal", "regex"}
SOURCE_TERM_TO_CONTEXT = {
    "uk": "uk-specific",
    "australia": "australia-specific",
    "us": "us-specific",
    "mixed": "mixed-anglosphere",
    "mixed-anglosphere": "mixed-anglosphere",
    "market-specific": "mixed-anglosphere",
    "universal": "universal",
}


def normalize_claim_type(value: str) -> str:
    cleaned = normalize_key(value).replace(" ", "_")
    cleaned = CLINICAL_CLAIM_TYPE_ALIASES.get(cleaned, cleaned)
    return cleaned if cleaned in CLINICAL_CLAIM_TYPES else ""


def normalize_claim_final_rendering(value: str) -> str:
    cleaned = normalize_key(value).replace(" ", "_")
    return cleaned if cleaned in CLAIM_FINAL_RENDERINGS else ""


def normalize_structured_block_strategy(value: str) -> str:
    cleaned = normalize_key(value).replace(" ", "_")
    return cleaned if cleaned in STRUCTURED_BLOCK_STRATEGIES else ""


def normalize_audit_status(value: str) -> str:
    cleaned = normalize_key(value)
    return cleaned if cleaned in AUDIT_STATUSES else ""


def term_matches(left: str, right: str) -> bool:
    left_norm = normalize_key(left)
    right_norm = normalize_key(right)
    if not left_norm or not right_norm:
        return False
    return left_norm == right_norm or left_norm in right_norm or right_norm in left_norm


def load_termbase_rows(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return merge_keyed_rows(termbase_paths(book_root), "en")


def load_acronym_rows(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return merge_keyed_rows(acronym_paths(book_root), "acronym")


def load_gold_phrase_rows(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return merge_appended_rows(gold_phrase_paths(book_root))


def load_calque_pattern_rows(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return merge_appended_rows(calque_pattern_paths(book_root))


def load_disallowed_term_rows(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return merge_appended_rows(disallowed_term_paths(book_root))


def load_disallowed_phrase_rows(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return merge_appended_rows(disallowed_phrase_paths(book_root))


def load_term_candidate_rows(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return optional_tsv_rows(term_candidates_path(book_root))


def normalize_localization_override_row(row: dict[str, str]) -> dict[str, str]:
    replacement_mode = row.get("replacement_mode", "").strip() or "replace_lt"
    if replacement_mode not in LOCALIZATION_REPLACEMENT_MODES:
        replacement_mode = "replace_lt"
    jurisdiction = row.get("jurisdiction", "").strip().lower() or "universal"
    return {
        "source_term": row.get("source_term", "").strip(),
        "jurisdiction": jurisdiction,
        "replacement_mode": replacement_mode,
        "local_lt": row.get("local_lt", "").strip(),
        "eu_fallback": row.get("eu_fallback", "").strip(),
        "scope": row.get("scope", "").strip() or "all",
        "reason": row.get("reason", "").strip(),
        "source_ref": row.get("source_ref", "").strip(),
        "notes": row.get("notes", "").strip(),
    }


def load_localization_overrides(
    path: Path | None = None,
    *,
    book_root: str | Path | None = None,
) -> list[dict[str, str]]:
    if path is not None:
        return [normalize_localization_override_row(row) for row in require_tsv_rows(path)]
    return merge_keyed_rows(
        localization_override_paths(book_root),
        "source_term",
        row_normalizer=normalize_localization_override_row,
    )


def normalize_localization_signal_row(row: dict[str, str]) -> dict[str, str]:
    source_term = row.get("source_term", "").strip()
    match_mode = (row.get("match_mode", "") or "literal").strip().lower()
    if match_mode not in LOCALIZATION_SIGNAL_MATCH_MODES:
        match_mode = "literal"
    pattern = row.get("pattern", "").strip() or source_term
    return {
        "source_term": source_term,
        "jurisdiction": row.get("jurisdiction", "").strip().lower() or "universal",
        "signal_type": row.get("signal_type", "").strip() or "reference tool",
        "match_mode": match_mode,
        "pattern": pattern,
        "notes": row.get("notes", "").strip(),
    }


def load_localization_signal_specs(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return merge_keyed_rows(
        localization_signal_registry_paths(book_root),
        "source_term",
        row_normalizer=normalize_localization_signal_row,
    )


def localization_signal_matches(spec: dict[str, str], text: str) -> bool:
    if spec.get("match_mode", "literal") == "regex":
        return bool(re.search(spec.get("pattern", ""), text, flags=re.IGNORECASE))
    return normalize_key(spec.get("pattern", "")) in normalize_key(text)


def detect_source_localization_signals(source_text: str, book_root: str | Path | None = None) -> list[dict[str, str]]:
    content_text = source_text_for_policy_checks(source_text)
    signals: list[dict[str, str]] = []
    seen: set[str] = set()
    for spec in load_localization_signal_specs(book_root):
        if not localization_signal_matches(spec, content_text):
            continue
        key = normalize_key(spec["source_term"])
        if key in seen:
            continue
        seen.add(key)
        signals.append(
            {
                "source_term": spec["source_term"],
                "jurisdiction": spec["jurisdiction"],
                "signal_type": spec["signal_type"],
                "match_mode": spec["match_mode"],
                "pattern": spec["pattern"],
                "notes": spec["notes"],
            }
        )
    return signals


def normalize_clinical_policy_marker_row(row: dict[str, str]) -> dict[str, str]:
    topic = normalize_claim_type(row.get("topic", "").strip())
    match_mode = (row.get("match_mode", "") or "literal").strip().lower()
    if match_mode not in CLINICAL_POLICY_MARKER_MATCH_MODES:
        match_mode = "literal"
    pattern = row.get("pattern", "").strip() or topic
    return {
        "topic": topic,
        "match_mode": match_mode,
        "pattern": pattern,
        "notes": row.get("notes", "").strip(),
    }


def load_clinical_policy_markers(book_root: str | Path | None = None) -> list[dict[str, str]]:
    del book_root
    return [
        normalize_clinical_policy_marker_row(row)
        for row in require_tsv_rows(clinical_policy_markers_path())
        if row.get("topic", "").strip()
    ]


def load_lt_source_map(book_root: str | Path | None = None) -> list[dict[str, str]]:
    del book_root
    return require_tsv_rows(lt_source_map_path())


def load_review_taxonomy_rows() -> list[dict[str, str]]:
    return require_tsv_rows(review_taxonomy_path())


def load_adjudication_profile_rows(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return merge_keyed_rows(adjudication_profile_paths(book_root), "profile_id")


def load_gold_section_examples(book_root: str | Path | None = None) -> list[dict[str, object]]:
    rows_by_id: dict[str, dict[str, object]] = {}
    order: list[str] = []

    for index, (index_path, source_root) in enumerate(gold_section_index_sources(book_root)):
        rows = require_tsv_rows(index_path) if index == 0 else optional_tsv_rows(index_path)
        for row in rows:
            example_id = row.get("example_id", "").strip()
            relative_path = row.get("path", "").strip()
            if not example_id or not relative_path:
                continue

            example_path = resolve_indexed_text_path(source_root, index_path, relative_path)
            if example_path is None:
                continue

            key = normalize_key(example_id)
            if key not in order:
                order.append(key)
            rows_by_key_row = {
                "kind": "section",
                "example_id": example_id,
                "source_chapter": row.get("source_chapter", "").strip(),
                "block_id": row.get("block_id", "").strip(),
                "block_type": row.get("block_type", "").strip(),
                "tags": split_multi(row.get("tags", "")),
                "text": example_path.read_text(encoding="utf-8").strip(),
                "notes": row.get("notes", "").strip(),
                "path": relative_path,
            }
            rows_by_id[key] = rows_by_key_row

    return [rows_by_id[key] for key in order if key in rows_by_id]


def clinical_policy_marker_matches(marker: dict[str, str], text: str) -> bool:
    if marker.get("match_mode", "literal") == "regex":
        return bool(re.search(marker.get("pattern", ""), text, flags=re.IGNORECASE))
    return normalize_key(marker.get("pattern", "")) in normalize_key(text)


def detect_clinical_policy_topics(source_text: str, book_root: str | Path | None = None) -> list[str]:
    content_text = source_text_for_policy_checks(source_text)
    topics: list[str] = []
    seen: set[str] = set()
    for marker in load_clinical_policy_markers(book_root):
        if not clinical_policy_marker_matches(marker, content_text):
            continue
        key = normalize_key(marker["topic"])
        if key in seen:
            continue
        seen.add(key)
        topics.append(marker["topic"])
    return topics


def source_has_clinical_normative_content(source_text: str, book_root: str | Path | None = None) -> bool:
    return bool(detect_clinical_policy_topics(source_text, book_root))


def extract_localization_research(sections: dict[tuple[str, ...], list[str]]) -> dict[str, object]:
    signal_rows = markdown_table_rows(find_section_lines(sections, "Jurisdikcijos ir rinkos signalai"))
    decision_rows = markdown_table_rows(find_section_lines(sections, "LT/EU pakeitimo sprendimai"))
    source_rows = markdown_table_rows(find_section_lines(sections, "Vaistų ir dozių LT/EU šaltinių bazė"))
    claim_rows = markdown_table_rows(find_section_lines(sections, "Norminių teiginių matrica"))
    structured_policy_rows = markdown_table_rows(find_section_lines(sections, "Struktūrinių blokų lokalizacijos sprendimai"))
    manual_audit_rows = markdown_table_rows(find_section_lines(sections, "Finalus agento auditas"))

    return {
        "signals": [
            {
                "source_term": row.get("signalas", "") or row.get("source_term", ""),
                "jurisdiction": (row.get("jurisdikcija", "") or row.get("jurisdiction", "")).strip().lower(),
                "signal_type": row.get("tipas", "") or row.get("signal_type", ""),
                "source_anchor": row.get("šaltinio_vieta", "") or row.get("saltinio_vieta", "") or row.get("source_anchor", ""),
                "notes": row.get("pastaba", "") or row.get("notes", ""),
            }
            for row in signal_rows
            if row.get("signalas", "") or row.get("source_term", "")
        ],
        "decisions": [
            {
                "source_term": row.get("signalas", "") or row.get("source_term", ""),
                "replacement_mode": row.get("veiksmas", "") or row.get("replacement_mode", ""),
                "authority_basis": row.get("autoritetas", "") or row.get("authority_basis", ""),
                "localization_note": row.get("lt_eu_sprendimas", "") or row.get("localization_note", ""),
                "source_ref": row.get("šaltinio_nuoroda", "") or row.get("saltinio_nuoroda", "") or row.get("source_ref", ""),
                "notes": row.get("pastaba", "") or row.get("notes", ""),
            }
            for row in decision_rows
            if row.get("signalas", "") or row.get("source_term", "")
        ],
        "authority_sources": [
            {
                "topic": normalize_claim_type(row.get("tema", "") or row.get("topic", "")),
                "source": row.get("šaltinis", "") or row.get("saltinis", "") or row.get("source", ""),
                "jurisdiction": row.get("jurisdikcija", "") or row.get("jurisdiction", ""),
                "date": row.get("data_versija", "") or row.get("date_version", ""),
                "notes": row.get("pastaba", "") or row.get("notes", ""),
            }
            for row in source_rows
            if row.get("tema", "") or row.get("topic", "")
        ],
        "claims": [
            {
                "claim_id": row.get("claim_id", "") or row.get("teiginio_id", ""),
                "claim_type": normalize_claim_type(row.get("claim_type", "") or row.get("teiginio_tipas", "")),
                "source_anchor": row.get("source_anchor", "") or row.get("šaltinio_vieta", "") or row.get("saltinio_vieta", ""),
                "final_rendering": normalize_claim_final_rendering(row.get("final_rendering", "") or row.get("galutinis_pateikimas", "")),
                "authority_basis": row.get("authority_basis", "") or row.get("autoritetas", ""),
                "primary_lt_source": row.get("primary_lt_source", "") or row.get("pagrindinis_lt_saltinis", "") or row.get("pagrindinis_lt_šaltinis", ""),
                "eu_fallback_source": row.get("eu_fallback_source", "") or row.get("eu_fallback_saltinis", "") or row.get("eu_fallback_šaltinis", ""),
                "lt_gap_reason": row.get("lt_gap_reason", "") or row.get("lt_spragos_priezastis", "") or row.get("lt_spragos_priežastis", ""),
                "note": row.get("note", "") or row.get("pastaba", ""),
            }
            for row in claim_rows
            if any(value.strip() for value in row.values())
        ],
        "structured_block_policies": [
            {
                "block_id": row.get("block_id", "") or row.get("bloko_id", ""),
                "block_type": row.get("block_type", "") or row.get("bloko_tipas", ""),
                "lt_strategy": normalize_structured_block_strategy(row.get("lt_strategy", "") or row.get("lt_strategija", "")),
                "authority_source": row.get("authority_source", "") or row.get("autoriteto_saltinis", "") or row.get("autoriteto_šaltinis", ""),
                "original_context_allowed": row.get("original_context_allowed", "") or row.get("originalo_kontekstas_leidziamas", "") or row.get("originalo_kontekstas_leidžiamas", ""),
                "note": row.get("note", "") or row.get("pastaba", ""),
            }
            for row in structured_policy_rows
            if any(value.strip() for value in row.values())
        ],
        "manual_audit": [
            {
                "area": normalize_key(row.get("sritis", "") or row.get("area", "")),
                "status": normalize_audit_status(row.get("statusas", "") or row.get("status", "")),
                "note": row.get("pastaba", "") or row.get("note", ""),
            }
            for row in manual_audit_rows
            if any(value.strip() for value in row.values())
        ],
        "nontransferable": bullet_items(find_section_lines(sections, "Neperkeliamas originalo turinys")),
    }


def extract_adjudication_decisions(sections: dict[tuple[str, ...], list[str]]) -> list[dict[str, str]]:
    decisions: list[dict[str, str]] = []
    for item in bullet_items(find_section_lines(sections, "Adjudication sprendimai")):
        parts = [part.strip() for part in item.split("|", 2)]
        block_id = parts[0] if len(parts) >= 1 else ""
        choice = parts[1] if len(parts) >= 2 else ""
        reason = parts[2] if len(parts) >= 3 else ""
        decisions.append({"block_id": block_id, "choice": choice, "reason": reason, "raw": item})
    return decisions


def normalize_authority_basis(value: str) -> str:
    cleaned = value.strip() or "LT"
    if cleaned in {"LT", "EU", "original-context-only"}:
        return cleaned
    return "LT"


def jurisdiction_to_pack_context(jurisdictions: Iterable[str]) -> str:
    normalized = {item.strip().lower() for item in jurisdictions if item and item.strip()}
    if not normalized:
        return "universal"
    if len(normalized) == 1:
        only = next(iter(normalized))
        return SOURCE_TERM_TO_CONTEXT.get(only, "mixed-anglosphere")
    return "mixed-anglosphere"
