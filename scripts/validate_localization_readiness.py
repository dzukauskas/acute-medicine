#!/usr/bin/env python3
from __future__ import annotations

import argparse

from workflow_book import (
    chapter_number_from_slug,
    chapter_paths_for_slug,
    resolve_chapter_slug,
    scope_allows,
)
from workflow_markdown import (
    find_section_lines,
    markdown_table_rows,
    parse_markdown_sections,
)
from workflow_policy import (
    CLAIM_FINAL_RENDERINGS,
    CLINICAL_CLAIM_TYPES,
    LOCALIZATION_REPLACEMENT_MODES,
    STRUCTURED_BLOCK_STRATEGIES,
    detect_clinical_policy_topics,
    detect_source_localization_signals,
    extract_localization_research,
    load_localization_overrides,
    term_matches,
)
from workflow_rules import activate_book_root, localization_override_paths, normalize_key
from workflow_runtime import parse_bool


MANDATORY_LOCALIZATION_SECTIONS = (
    "LT-source branduolio taikymas",
    "Jurisdikcijos ir rinkos signalai",
    "LT/EU pakeitimo sprendimai",
    "Vaistų ir dozių LT/EU šaltinių bazė",
    "Norminių teiginių matrica",
    "Struktūrinių blokų lokalizacijos sprendimai",
    "Neperkeliamas originalo turinys",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate that research captures LT/EU-first localization decisions before drafting."
    )
    parser.add_argument("--book-root", help="Optional books/<slug> root. If omitted, uses MEDBOOK_ROOT.")
    parser.add_argument("chapter", help="Chapter slug or number.")
    return parser.parse_args()


def has_section(sections: dict[tuple[str, ...], list[str]], title: str) -> bool:
    return bool(find_section_lines(sections, title))


def matching_rows(rows: list[dict[str, str]], source_term: str) -> list[dict[str, str]]:
    return [row for row in rows if term_matches(row.get("source_term", ""), source_term)]


def row_value(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = row.get(key, "").strip()
        if value:
            return value
    return ""


def matching_claim_rows(rows: list[dict[str, str]], claim_type: str) -> list[dict[str, str]]:
    return [row for row in rows if row.get("claim_type", "").strip() == claim_type]


def validate_localization_readiness(slug: str) -> list[str]:
    paths = chapter_paths_for_slug(slug)
    source_text = paths["source"].read_text(encoding="utf-8")
    research_text = paths["research"].read_text(encoding="utf-8")
    sections = parse_markdown_sections(research_text)
    research = extract_localization_research(sections)
    lt_source_rows = markdown_table_rows(find_section_lines(sections, "LT-source branduolio taikymas"))
    chapter_number = chapter_number_from_slug(slug)
    override_sources = [path for path in localization_override_paths() if path.exists()]
    overrides = [
        row
        for row in load_localization_overrides()
        if scope_allows(row.get("scope", "all"), chapter_number)
    ]

    errors: list[str] = []
    for title in MANDATORY_LOCALIZATION_SECTIONS:
        if not has_section(sections, title):
            errors.append(f"{paths['research']}: trūksta privalomos sekcijos `## {title}`.")

    populated_lt_source_rows = [
        row
        for row in lt_source_rows
        if row_value(
            row,
            "sritis",
            "tema",
            "pagrindinis_lt-source_kelias",
            "konkretus_lt_saltinis",
            "konkretus_lt_šaltinis",
        )
    ]
    if not populated_lt_source_rows:
        errors.append(
            f"{paths['research']}: privaloma užpildyti bent vieną eilutę sekcijoje "
            "`## LT-source branduolio taikymas`."
        )
    else:
        for row in populated_lt_source_rows:
            if not row_value(row, "sritis", "tema"):
                errors.append(
                    f"{paths['research']}: `LT-source branduolio taikymas` eilutėje trūksta `Sritis`."
                )
            if not row_value(row, "pagrindinis_lt-source_kelias"):
                errors.append(
                    f"{paths['research']}: `LT-source branduolio taikymas` eilutėje trūksta "
                    "`Pagrindinis LT-source kelias`."
                )
            if not row_value(row, "konkretus_lt_saltinis", "konkretus_lt_šaltinis"):
                errors.append(
                    f"{paths['research']}: `LT-source branduolio taikymas` eilutėje trūksta "
                    "`Konkretus LT šaltinis`."
                )

    detected_signals = detect_source_localization_signals(source_text)
    for signal in detected_signals:
        signal_term = signal["source_term"]
        signal_rows = matching_rows(research["signals"], signal_term)
        if not signal_rows:
            errors.append(
                f"{paths['research']}: source signal `{signal_term}` ({signal['jurisdiction']}, {signal['signal_type']}) "
                "neužfiksuotas sekcijoje `## Jurisdikcijos ir rinkos signalai`."
            )

        decision_rows = matching_rows(research["decisions"], signal_term)
        if not decision_rows:
            errors.append(
                f"{paths['research']}: source signal `{signal_term}` neturi LT/EU sprendimo "
                "sekcijoje `## LT/EU pakeitimo sprendimai`."
            )
            continue

        for row in decision_rows:
            replacement_mode = row.get("replacement_mode", "").strip()
            if replacement_mode not in LOCALIZATION_REPLACEMENT_MODES:
                errors.append(
                    f"{paths['research']}: signalui `{signal_term}` nurodytas neleistinas "
                    f"`replacement_mode` `{replacement_mode}`."
                )
                continue
            if not row.get("source_ref", "").strip():
                errors.append(
                    f"{paths['research']}: signalui `{signal_term}` trūksta `Šaltinio nuoroda` "
                    "sekcijoje `## LT/EU pakeitimo sprendimai`."
                )
            authority_basis = row.get("authority_basis", "").strip()
            localization_note = row.get("localization_note", "").strip()
            notes = row.get("notes", "").strip()

            if replacement_mode == "replace_lt":
                if authority_basis != "LT":
                    errors.append(
                        f"{paths['research']}: signalui `{signal_term}` su `replace_lt` privalomas `Autoritetas = LT`."
                    )
                if not localization_note:
                    errors.append(
                        f"{paths['research']}: signalui `{signal_term}` su `replace_lt` trūksta `LT / EU sprendimas`."
                    )
            elif replacement_mode == "replace_eu":
                if authority_basis != "EU":
                    errors.append(
                        f"{paths['research']}: signalui `{signal_term}` su `replace_eu` privalomas `Autoritetas = EU`."
                    )
                if not localization_note:
                    errors.append(
                        f"{paths['research']}: signalui `{signal_term}` su `replace_eu` trūksta `LT / EU sprendimas`."
                    )
            elif replacement_mode in {"genericize", "omit_nontransferable"}:
                if not (localization_note or notes):
                    errors.append(
                        f"{paths['research']}: signalui `{signal_term}` su `{replacement_mode}` trūksta priežasties "
                        "(`LT / EU sprendimas` arba `Pastaba`)."
                    )

        if not any(term_matches(override.get("source_term", ""), signal_term) for override in overrides):
            errors.append(
                f"{', '.join(str(path) for path in override_sources) or 'shared/localization/localization_overrides.tsv'}: signalui `{signal_term}` "
                "nėra pasikartojančios lokalizacijos politikos įrašo."
            )

    detected_topics = detect_clinical_policy_topics(source_text)
    claim_rows = research["claims"]
    if detected_topics and not claim_rows:
        errors.append(
            f"{paths['research']}: source skyriuje aptiktas norminis klinikinis turinys ({', '.join(detected_topics)}), "
            "todėl privaloma užpildyti `## Norminių teiginių matrica`."
        )

    seen_claim_ids: set[str] = set()
    for row in claim_rows:
        claim_id = row.get("claim_id", "").strip()
        claim_type = row.get("claim_type", "").strip()
        source_anchor = row.get("source_anchor", "").strip()
        final_rendering = row.get("final_rendering", "").strip()
        authority_basis = row.get("authority_basis", "").strip()
        primary_lt_source = row.get("primary_lt_source", "").strip()
        eu_fallback_source = row.get("eu_fallback_source", "").strip()
        lt_gap_reason = row.get("lt_gap_reason", "").strip()
        note = row.get("note", "").strip()

        if not claim_id:
            errors.append(f"{paths['research']}: `Norminių teiginių matrica` eilutėje trūksta `claim_id`.")
        elif claim_id in seen_claim_ids:
            errors.append(f"{paths['research']}: `Norminių teiginių matrica` dubliuotas `claim_id` `{claim_id}`.")
        else:
            seen_claim_ids.add(claim_id)

        if claim_type not in CLINICAL_CLAIM_TYPES:
            errors.append(
                f"{paths['research']}: claim `{claim_id or '<be id>'}` turi neleistiną `claim_type` `{claim_type}`."
            )
        if not source_anchor:
            errors.append(
                f"{paths['research']}: claim `{claim_id or '<be id>'}` trūksta `source_anchor`."
            )
        if final_rendering not in CLAIM_FINAL_RENDERINGS:
            errors.append(
                f"{paths['research']}: claim `{claim_id or '<be id>'}` turi neleistiną `final_rendering` `{final_rendering}`."
            )

        if final_rendering == "keep_lt_normative":
            if authority_basis != "LT":
                errors.append(
                    f"{paths['research']}: claim `{claim_id or '<be id>'}` su `keep_lt_normative` privalo turėti `authority_basis = LT`."
                )
            if not primary_lt_source:
                errors.append(
                    f"{paths['research']}: claim `{claim_id or '<be id>'}` su `keep_lt_normative` privalo turėti `primary_lt_source`."
                )
        elif final_rendering == "keep_eu_normative":
            if authority_basis != "EU":
                errors.append(
                    f"{paths['research']}: claim `{claim_id or '<be id>'}` su `keep_eu_normative` privalo turėti `authority_basis = EU`."
                )
            if not eu_fallback_source:
                errors.append(
                    f"{paths['research']}: claim `{claim_id or '<be id>'}` su `keep_eu_normative` privalo turėti `eu_fallback_source`."
                )
            if not lt_gap_reason:
                errors.append(
                    f"{paths['research']}: claim `{claim_id or '<be id>'}` su `keep_eu_normative` privalo turėti `lt_gap_reason`."
                )
        elif final_rendering == "original_context_callout":
            if authority_basis != "original-context-only":
                errors.append(
                    f"{paths['research']}: claim `{claim_id or '<be id>'}` su `original_context_callout` privalo turėti `authority_basis = original-context-only`."
                )
            if not note:
                errors.append(
                    f"{paths['research']}: claim `{claim_id or '<be id>'}` su `original_context_callout` privalo turėti paaiškinimą `note`."
                )
        elif final_rendering == "omit" and not note:
            errors.append(
                f"{paths['research']}: claim `{claim_id or '<be id>'}` su `omit` privalo turėti paaiškinimą `note`."
            )

    if detected_topics and not research["authority_sources"]:
        errors.append(
            f"{paths['research']}: skyriuje yra norminio klinikinio turinio ({', '.join(detected_topics)}), "
            "todėl privaloma užpildyti `## Vaistų ir dozių LT/EU šaltinių bazė`."
        )

    for row in research["authority_sources"]:
        if not row.get("topic", "").strip():
            errors.append(
                f"{paths['research']}: `Vaistų ir dozių LT/EU šaltinių bazė` eilutėje trūksta `Tema`."
            )
        if not row.get("source", "").strip():
            errors.append(f"{paths['research']}: `Vaistų ir dozių LT/EU šaltinių bazė` eilutėje trūksta `Šaltinis`.")
        if not row.get("date", "").strip():
            errors.append(
                f"{paths['research']}: `Vaistų ir dozių LT/EU šaltinių bazė` eilutėje trūksta `Data / versija`."
            )

    for topic in detected_topics:
        if not any(term_matches(row.get("topic", ""), topic) for row in research["authority_sources"]):
            errors.append(
                f"{paths['research']}: norminiam turiniui `{topic}` trūksta atskiro įrašo "
                "sekcijoje `## Vaistų ir dozių LT/EU šaltinių bazė`."
            )
        if not matching_claim_rows(claim_rows, topic):
            errors.append(
                f"{paths['research']}: norminiam turiniui `{topic}` trūksta bent vienos claim-level eilutės "
                "sekcijoje `## Norminių teiginių matrica`."
            )

    for row in research["structured_block_policies"]:
        block_id = row.get("block_id", "").strip()
        block_type = normalize_key(row.get("block_type", ""))
        lt_strategy = row.get("lt_strategy", "").strip()
        authority_source = row.get("authority_source", "").strip()
        original_context_allowed = row.get("original_context_allowed", "").strip()

        if not block_id:
            errors.append(
                f"{paths['research']}: `Struktūrinių blokų lokalizacijos sprendimai` eilutėje trūksta `block_id`."
            )
        if not block_type:
            errors.append(
                f"{paths['research']}: `Struktūrinių blokų lokalizacijos sprendimai` eilutėje trūksta `block_type`."
            )
        if lt_strategy not in STRUCTURED_BLOCK_STRATEGIES:
            errors.append(
                f"{paths['research']}: block `{block_id or '<be id>'}` turi neleistiną `lt_strategy` `{lt_strategy}`."
            )
        if block_type == "algorithm" and not authority_source:
            errors.append(
                f"{paths['research']}: algorithm block `{block_id or '<be id>'}` privalo turėti `authority_source`."
            )
        if lt_strategy == "original_context_callout" and not parse_bool(original_context_allowed, default=False):
            errors.append(
                f"{paths['research']}: block `{block_id or '<be id>'}` su `original_context_callout` turi turėti `original_context_allowed = yes`."
            )

    return errors


def validate_localization_readiness_or_raise(slug: str) -> None:
    errors = validate_localization_readiness(slug)
    if errors:
        raise ValueError("\n".join(errors))


def main() -> int:
    args = parse_args()
    activate_book_root(args.book_root)
    slug = resolve_chapter_slug(args.chapter, args.book_root)
    try:
        validate_localization_readiness_or_raise(slug)
    except ValueError as exc:
        raise SystemExit(str(exc))

    print(f"Localization readiness passed for {slug}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
