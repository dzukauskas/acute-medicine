#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from workflow_book import book_relative_path, chapter_paths_for_slug, resolve_chapter_slug
from workflow_markdown import (
    extract_source_structured_items,
    structured_block_id,
    structured_block_type,
)
from workflow_policy import (
    detect_clinical_policy_topics,
    detect_source_localization_signals,
    load_clinical_policy_markers,
    load_lt_source_map,
)
from workflow_rules import (
    activate_book_root,
    normalize_key,
    require_book_root,
)


CLAIM_TOPIC_TO_DOMAINS = {
    "dose": ("vaistu_registracija_ir_produkto_informacija", "farmakologija_ir_racionalus_skyrimas"),
    "indication": ("farmakologija_ir_racionalus_skyrimas", "vaistu_registracija_ir_produkto_informacija"),
    "contraindication": ("farmakologija_ir_racionalus_skyrimas", "vaistu_registracija_ir_produkto_informacija"),
    "route": ("vaistu_registracija_ir_produkto_informacija", "farmakologija_ir_racionalus_skyrimas"),
    "concentration": ("vaistu_registracija_ir_produkto_informacija", "farmakologija_ir_racionalus_skyrimas"),
    "algorithm_step": ("klinikinės_metodikos_ir_specialybines_rekomendacijos", "paramediko_kompetencija_ir_gmp"),
    "monitoring": ("klinikinės_metodikos_ir_specialybines_rekomendacijos", "paramediko_kompetencija_ir_gmp"),
    "legal_scope": ("teise_ir_reguliavimas", "paramediko_kompetencija_ir_gmp"),
    "market_availability": ("kompensavimas_ir_rinkos_prieinamumas", "vaistu_registracija_ir_produkto_informacija"),
}
SIGNAL_TYPE_TO_DOMAINS = {
    "regulatorius": ("teise_ir_reguliavimas",),
    "gairės": ("klinikinės_metodikos_ir_specialybines_rekomendacijos",),
    "teisė": ("teise_ir_reguliavimas",),
    "service model": ("paramediko_kompetencija_ir_gmp",),
    "brand name": ("kompensavimas_ir_rinkos_prieinamumas", "farmakologija_ir_racionalus_skyrimas"),
    "dose": ("vaistu_registracija_ir_produkto_informacija", "farmakologija_ir_racionalus_skyrimas"),
    "market availability": ("kompensavimas_ir_rinkos_prieinamumas",),
    "reference tool": ("farmakologija_ir_racionalus_skyrimas", "klinikinės_metodikos_ir_specialybines_rekomendacijos"),
}
BLOCK_TYPE_TO_DOMAINS = {
    "algorithm": ("klinikinės_metodikos_ir_specialybines_rekomendacijos", "paramediko_kompetencija_ir_gmp"),
    "table": ("farmakologija_ir_racionalus_skyrimas", "vaistu_registracija_ir_produkto_informacija"),
    "chart": ("klinikinės_metodikos_ir_specialybines_rekomendacijos", "paramediko_kompetencija_ir_gmp"),
    "callout": ("teise_ir_reguliavimas", "paramediko_kompetencija_ir_gmp"),
    "figure_caption": ("terminija_ir_kalbos_forma", "anatomija_fiziologija_patofiziologija"),
}
BLOCK_TYPE_TO_LT_STRATEGY = {
    "algorithm": "rewrite_lt",
    "table": "compress_lt",
    "chart": "original_context_callout",
    "callout": "rewrite_lt",
    "figure_caption": "recreate_figure",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a chapter-specific research checklist scaffold from source inventory and LT/EU localization signals."
    )
    parser.add_argument("--book-root", help="Optional books/<slug> root. If omitted, uses MEDBOOK_ROOT.")
    parser.add_argument("chapter", help="Chapter slug or number.")
    parser.add_argument(
        "--out",
        help="Optional output path. Defaults to research/<slug>.checklist.md.",
    )
    return parser.parse_args()


def source_subsections(source_text: str) -> list[str]:
    headings: list[str] = []
    for raw_line in source_text.splitlines():
        line = raw_line.strip()
        if not line.startswith("##"):
            continue
        if re.match(r"^##+\s+(Table|Figure|Box|Chart)\b", line):
            continue
        heading = re.sub(r"^##+\s+", "", line).strip()
        if heading and heading not in headings:
            headings.append(heading)
    return headings


def chapter_kind(signals: list[dict[str, str]], topics: list[str]) -> str:
    if topics and signals:
        return "mišrus norminis / lokalizacinis"
    if topics:
        return "norminis klinikinis"
    if signals:
        return "jurisdikciškai jautrus / lokalizacinis"
    return "fundamentinis / universalus"


def build_source_map_index() -> dict[str, dict[str, str]]:
    return {row["domain"]: row for row in load_lt_source_map()}


def recommended_domains(
    topics: list[str],
    signals: list[dict[str, str]],
    structured_items: list[dict[str, str]],
) -> list[tuple[str, str]]:
    selected: dict[str, str] = {"terminija_ir_kalbos_forma": "LT terminijai ir kolokacijoms."}

    if not topics and not signals:
        selected.setdefault(
            "anatomija_fiziologija_patofiziologija",
            "Fundamentiniam ar universaliam moksliniam turiniui.",
        )

    for topic in topics:
        for domain in CLAIM_TOPIC_TO_DOMAINS.get(topic, ()):
            selected.setdefault(domain, f"Reikalinga dėl aptikto claim tipo `{topic}`.")

    for signal in signals:
        signal_type = signal.get("signal_type", "").strip()
        for domain in SIGNAL_TYPE_TO_DOMAINS.get(signal_type, ()):
            selected.setdefault(
                domain,
                f"Reikalinga dėl jurisdikcinio / rinkos signalo `{signal.get('source_term', '')}` ({signal_type}).",
            )

    for item in structured_items:
        block_type = structured_block_type(item["kind"], item["title"])
        for domain in BLOCK_TYPE_TO_DOMAINS.get(block_type, ()):
            selected.setdefault(
                domain,
                f"Reikalinga dėl struktūrinio bloko `{item['kind']} {item['label']}` ({block_type}).",
            )

    order = list(selected)
    return [(domain, selected[domain]) for domain in order]


def first_source_anchor_for_topic(source_text: str, topic: str) -> str:
    markers = [row for row in load_clinical_policy_markers() if row.get("topic") == topic]
    if not markers:
        return "TODO: nurodykite tikslią vietą source"

    lines = [line.strip() for line in source_text.splitlines() if line.strip()]
    for marker in markers:
        pattern = marker.get("pattern", "")
        if not pattern:
            continue
        if marker.get("match_mode") == "regex":
            regex = re.compile(pattern, re.IGNORECASE)
            for line in lines:
                if regex.search(line):
                    return line
            continue
        pattern_norm = normalize_key(pattern)
        for line in lines:
            if pattern_norm and pattern_norm in normalize_key(line):
                return line
    return "TODO: nurodykite tikslią vietą source"


def source_hint_for_domain(source_map: dict[str, dict[str, str]], domain: str) -> str:
    row = source_map.get(domain, {})
    return row.get("primary_lt_sources", "").strip()


def suggested_claim_rows(source_text: str, topics: list[str], source_map: dict[str, dict[str, str]]) -> list[str]:
    rows: list[str] = []
    seen: set[str] = set()
    for index, topic in enumerate(topics, start=1):
        if topic in seen:
            continue
        seen.add(topic)
        domains = CLAIM_TOPIC_TO_DOMAINS.get(topic, ())
        primary_hint = source_hint_for_domain(source_map, domains[0]) if domains else ""
        claim_id = f"todo-{topic.replace('_', '-')}-{index:02d}"
        source_anchor = first_source_anchor_for_topic(source_text, topic)
        rows.append(
            "| {claim_id} | {claim_type} | {source_anchor} | keep_lt_normative | LT | {primary_lt_source} |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |".format(
                claim_id=claim_id,
                claim_type=topic,
                source_anchor=source_anchor.replace("|", "/"),
                primary_lt_source=primary_hint or "TODO: įrašykite LT šaltinį",
            )
        )
    return rows


def suggested_structured_rows(
    structured_items: list[dict[str, str]],
    source_map: dict[str, dict[str, str]],
) -> list[str]:
    rows: list[str] = []
    for item in structured_items:
        block_type = structured_block_type(item["kind"], item["title"])
        domains = BLOCK_TYPE_TO_DOMAINS.get(block_type, ())
        authority_hint = source_hint_for_domain(source_map, domains[0]) if domains else ""
        strategy = BLOCK_TYPE_TO_LT_STRATEGY.get(block_type, "rewrite_lt")
        original_context_allowed = "yes" if strategy == "original_context_callout" else "no"
        rows.append(
            "| {block_id} | {block_type} | {lt_strategy} | {authority_source} | {original_context_allowed} | {note} |".format(
                block_id=structured_block_id(item["kind"], item["label"], item["title"]),
                block_type=block_type,
                lt_strategy=strategy,
                authority_source=(authority_hint or "TODO: parinkite LT/EU autoriteto šaltinį") if block_type in {"table", "algorithm", "chart", "callout"} else "",
                original_context_allowed=original_context_allowed,
                note=f"{item['kind'].title()} {item['label']} {item['title']}".strip().replace("|", "/"),
            )
        )
    return rows


def render_domain_table(
    recommended: list[tuple[str, str]],
    source_map: dict[str, dict[str, str]],
) -> list[str]:
    lines = [
        "| Sritis | Kodėl įtraukta | Pagrindiniai LT šaltiniai | ES fallback | Pastaba |",
        "| --- | --- | --- | --- | --- |",
    ]
    for domain, reason in recommended:
        row = source_map.get(domain, {})
        lines.append(
            "| {domain} | {reason} | {primary} | {eu} | {notes} |".format(
                domain=domain,
                reason=reason,
                primary=row.get("primary_lt_sources", ""),
                eu=row.get("eu_fallback", ""),
                notes=row.get("notes", ""),
            )
        )
    return lines


def render_signals_table(signals: list[dict[str, str]]) -> list[str]:
    lines = [
        "| Signalas | Jurisdikcija | Tipas | Pastaba |",
        "| --- | --- | --- | --- |",
    ]
    for signal in signals:
        lines.append(
            "| {term} | {jurisdiction} | {signal_type} | {notes} |".format(
                term=signal.get("source_term", ""),
                jurisdiction=signal.get("jurisdiction", ""),
                signal_type=signal.get("signal_type", ""),
                notes=signal.get("notes", ""),
            )
        )
    return lines


def render_text(
    slug: str,
    book_root: Path,
    source_path: Path,
    research_path: Path,
    source_text: str,
    signals: list[dict[str, str]],
    topics: list[str],
    structured_items: list[dict[str, str]],
) -> str:
    source_map = build_source_map_index()
    recommended = recommended_domains(topics, signals, structured_items)
    subsection_lines = source_subsections(source_text)
    claim_rows = suggested_claim_rows(source_text, topics, source_map)
    structured_rows = suggested_structured_rows(structured_items, source_map)

    lines: list[str] = [
        f"# Research checklist for {slug}",
        "",
        f"- Angliškas failas: `{book_relative_path(source_path, book_root)}`",
        f"- Research failas: `{book_relative_path(research_path, book_root)}`",
        f"- Skyriaus tipas: `{chapter_kind(signals, topics)}`",
        f"- Aptikti norminių claim tipai: `{', '.join(topics) if topics else 'nenustatyta'}`",
        f"- Aptikti jurisdikciniai signalai: `{', '.join(signal['source_term'] for signal in signals) if signals else 'nenustatyta'}`",
        f"- Aptikti struktūriniai blokai: `{len(structured_items)}`",
        "",
        "## Poskyrių inventorius",
        "",
    ]
    if subsection_lines:
        lines.extend(f"- {heading}" for heading in subsection_lines)
    else:
        lines.append("- Nepavyko automatiškai nustatyti poskyrių; peržiūrėkite source ranka.")

    lines.extend(["", "## Aptikti jurisdikciniai / rinkos signalai", ""])
    if signals:
        lines.extend(render_signals_table(signals))
    else:
        lines.append("- Jurisdikcinių ar rinkos signalų automatiškai neaptikta.")

    lines.extend(["", "## Rekomenduojami LT-source keliai", ""])
    lines.extend(render_domain_table(recommended, source_map))

    lines.extend(["", "## Preliminari norminių teiginių matrica", ""])
    if claim_rows:
        lines.extend(
            [
                "| claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
                *claim_rows,
            ]
        )
    else:
        lines.extend(
            [
                "- Šiame skyriuje automatiškai neaptikta norminių claim tipų.",
                "- Jei po research paaiškės, kad skyriuje yra dozės, indikacijos, vartojimo keliai, algoritmai ar teisinės ribos, užpildykite `## Norminių teiginių matrica` ranka.",
            ]
        )

    lines.extend(["", "## Preliminarūs struktūrinių blokų lokalizacijos sprendimai", ""])
    if structured_rows:
        lines.extend(
            [
                "| block_id | block_type | lt_strategy | authority_source | original_context_allowed | note |",
                "| --- | --- | --- | --- | --- | --- |",
                *structured_rows,
            ]
        )
    else:
        lines.append("- Source skyriuje automatiškai neaptikta atskirų lentelių, paveikslų, schemų ar rėmelių.")

    lines.extend(
        [
            "",
            "## Rankiniai veiksmai prieš draftą",
            "",
            "- Peržiūrėkite originalo skyriaus intervalą ar šaltinio segmentus ranka ir patikslinkite, ar visi norminiai teiginiai sugaudyti.",
            "- Jei claim lieka pagrindiniame LT tekste kaip norminis, jam būtinas konkretus LT šaltinis.",
            "- Jei LT sluoksnio nepakanka ir tenka remtis ES, research faile užpildykite `lt_gap_reason`.",
            "- `figure` ir `algorithm` editable šaltinis šiame repo lieka tik `Whimsical`.",
            "- Po drafto būtinai užpildykite `## Finalus agento auditas` research faile.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    activate_book_root(args.book_root)
    slug = resolve_chapter_slug(args.chapter, args.book_root)
    require_book_root(args.book_root)
    paths = chapter_paths_for_slug(slug)
    source_path = paths["source"]
    research_path = paths["research"]
    output_path = Path(args.out) if args.out else research_path.with_name(f"{slug}.checklist.md")

    source_text = source_path.read_text(encoding="utf-8")
    signals = detect_source_localization_signals(source_text, args.book_root)
    topics = detect_clinical_policy_topics(source_text, args.book_root)
    structured_items = extract_source_structured_items(source_text)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_text(slug, require_book_root(args.book_root), source_path, research_path, source_text, signals, topics, structured_items),
        encoding="utf-8",
    )
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
