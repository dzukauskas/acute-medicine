#!/usr/bin/env python3
from __future__ import annotations

import argparse

from book_workflow_support import (
    activate_book_root,
    LOCALIZATION_REPLACEMENT_MODES,
    chapter_number_from_slug,
    chapter_paths_for_slug,
    detect_clinical_policy_topics,
    detect_source_localization_signals,
    extract_localization_research,
    find_section_lines,
    load_localization_overrides,
    parse_markdown_sections,
    resolve_chapter_slug,
    scope_allows,
    term_matches,
)


MANDATORY_LOCALIZATION_SECTIONS = (
    "Jurisdikcijos ir rinkos signalai",
    "LT/EU pakeitimo sprendimai",
    "Vaistų ir dozių LT/EU šaltinių bazė",
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


def validate_localization_readiness(slug: str) -> list[str]:
    paths = chapter_paths_for_slug(slug)
    source_text = paths["source"].read_text(encoding="utf-8")
    research_text = paths["research"].read_text(encoding="utf-8")
    sections = parse_markdown_sections(research_text)
    research = extract_localization_research(sections)
    chapter_number = chapter_number_from_slug(slug)
    overrides = [
        row
        for row in load_localization_overrides(paths["research"].parent.parent / "localization_overrides.tsv")
        if scope_allows(row.get("scope", "all"), chapter_number)
    ]

    errors: list[str] = []
    for title in MANDATORY_LOCALIZATION_SECTIONS:
        if not has_section(sections, title):
            errors.append(f"{paths['research']}: trūksta privalomos sekcijos `## {title}`.")

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
                f"{paths['research'].parent.parent / 'localization_overrides.tsv'}: signalui `{signal_term}` "
                "nėra pasikartojančios lokalizacijos politikos įrašo."
            )

    detected_topics = detect_clinical_policy_topics(source_text)
    if detected_topics and not research["authority_sources"]:
        errors.append(
            f"{paths['research']}: skyriuje yra dozių / indikacijų / kontraindikacijų / vartojimo kelių turinys, "
            "todėl privaloma užpildyti `## Vaistų ir dozių LT/EU šaltinių bazė`."
        )

    for row in research["authority_sources"]:
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
