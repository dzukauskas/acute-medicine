#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from book_workflow_support import (
    BOOK_ROOT,
    GOLD_SECTIONS_DIR,
    chapter_number_from_slug,
    chapter_paths_for_slug,
    dump_yaml,
    extract_inventory,
    metadata_value,
    normalize_key,
    parse_markdown_sections,
    parse_structured_label,
    read_tsv,
    resolve_chapter_slug,
    scope_allows,
    slugify,
    split_multi,
)
from validate_chapter_inventory import validate_chapter_inventory_or_raise


TERMBASE_PATH = BOOK_ROOT / "termbase.tsv"
ACRONYMS_PATH = BOOK_ROOT / "acronyms.tsv"
GOLD_PHRASES_PATH = BOOK_ROOT / "gold_phrases.tsv"
GOLD_SECTIONS_INDEX_PATH = GOLD_SECTIONS_DIR / "index.tsv"
LOCALIZATION_OVERRIDES_PATH = BOOK_ROOT / "localization_overrides.tsv"


BLOCK_TYPE_TO_MODE = {
    "narrative": "narrative-prose",
    "table": "table-compression",
    "algorithm": "algorithm-stepwise",
    "callout": "local-context-callout",
    "chart": "local-context-callout",
    "figure_caption": "local-context-callout",
    "legal_localization": "local-context-callout",
}

LOCALIZATION_KEYWORDS = {
    "news2",
    "acvpu",
    "avpu",
    "gks",
    "respect",
    "dnacpr",
    "2222",
    "legal",
}
COMPLEX_PROSE_KEYWORDS = {
    "shock",
    "cardiogenic",
    "hypotension",
    "critical",
    "perfusion",
    "vasopressor",
    "inotrope",
    "fluid",
    "echocardiography",
    "hemodynamic",
}

TAG_KEYWORDS = {
    "resuscitation": {
        "resuscitation",
        "cpr",
        "cardiac arrest",
        "defibrillator",
        "defibrillation",
        "rhythm",
        "adrenaline",
        "amiodarone",
        "rosc",
    },
    "uk-localization": {
        "news2",
        "acvpu",
        "respect",
        "dnacpr",
        "2222",
    },
    "hemodynamic": {
        "shock",
        "hypotension",
        "perfusion",
        "cardiogenic",
        "vasopressor",
        "inotropic",
        "inotrope",
        "fluid",
        "jvp",
        "map",
        "echocardiography",
        "oedema",
    },
    "airway": {
        "airway",
        "breathing",
        "ventilation",
        "intubation",
        "oxygen",
        "respiratory",
    },
    "neurological": {
        "neurological",
        "conscious",
        "gks",
        "avpu",
        "hypoglycaemia",
        "seizure",
        "brain",
    },
    "monitoring": {
        "news2",
        "observation",
        "observations",
        "monitor",
        "ecg",
        "spo2",
        "chart",
    },
    "legal-localization": {
        "dnacpr",
        "respect",
        "legal",
        "decision",
        "consent",
        "2222",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a chapter-specific preflight pack.")
    parser.add_argument("chapter", help="Chapter slug or number, for example 002 or 002-the-critically-ill-patient.")
    parser.add_argument(
        "--out",
        help="Optional output path. Defaults to books/acute-medicine/chapter_packs/<slug>.yaml.",
    )
    return parser.parse_args()


def load_chapter_context(slug: str) -> dict[str, object]:
    paths = chapter_paths_for_slug(slug)
    source_text = paths["source"].read_text(encoding="utf-8")
    research_text = paths["research"].read_text(encoding="utf-8")
    lt_text = paths["lt"].read_text(encoding="utf-8") if paths["lt"].exists() else ""
    sections = parse_markdown_sections(research_text)
    pre_heading_lines = []
    for line in research_text.splitlines():
        if line.startswith("## "):
            break
        pre_heading_lines.append(line)
    return {
        "source_text": source_text,
        "research_text": research_text,
        "lt_text": lt_text,
        "research_sections": sections,
        "page_range": metadata_value(pre_heading_lines, "Puslapiai"),
        "source_md": metadata_value(pre_heading_lines, "Angliškas pagalbinis failas") or str(paths["source"]),
        "lt_target_md": metadata_value(pre_heading_lines, "Lietuviškas failas") or str(paths["lt"]),
    }
def chapter_scope_number(slug: str) -> str:
    return chapter_number_from_slug(slug)


def detect_tags(text: str, block_type: str, risk_flags: list[str]) -> list[str]:
    normalized = normalize_key(text)
    tags: set[str] = set()

    if block_type == "algorithm":
        tags.add("algorithmic")
    elif block_type == "table":
        tags.add("table-structured")
    elif block_type == "chart":
        tags.add("chart-summary")
    elif block_type in {"callout", "legal_localization", "figure_caption"}:
        tags.add("contextual")

    if "complex_prose" in risk_flags:
        tags.add("complex-prose")
    if "localization_override" in risk_flags:
        tags.add("uk-localization")

    for tag, keywords in TAG_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            tags.add(tag)

    return sorted(tags)


def is_adjudication_candidate(block_type: str, risk_flags: list[str], tags: list[str]) -> bool:
    tag_set = set(tags)
    if block_type in {"algorithm", "legal_localization", "chart"}:
        return True
    if "localization_override" in risk_flags:
        return True
    if block_type in {"narrative", "callout"} and tag_set & {"hemodynamic", "uk-localization", "legal-localization"}:
        return True
    if "complex_prose" in risk_flags and block_type in {"narrative", "callout"}:
        return True
    return False


def select_active_terms(slug: str, inventory: dict[str, list[str]], source_text: str, research_text: str) -> list[dict[str, object]]:
    chapter_number = chapter_scope_number(slug)
    risky_norms = {normalize_key(item) for item in inventory["risky_terms"]}
    source_blob = normalize_key("\n".join([source_text, research_text]))
    rows = []
    for row in read_tsv(TERMBASE_PATH):
        if not scope_allows(row.get("section_scope", "all"), chapter_number):
            continue
        en_norm = normalize_key(row["en"])
        if en_norm in risky_norms or en_norm in source_blob:
            rows.append(
                {
                    "en": row["en"],
                    "lt": row["lt"],
                    "status": row["status"],
                    "banned_lt": split_multi(row.get("banned_lt", "")),
                    "first_use_policy": row.get("first_use_policy", ""),
                    "section_scope": row.get("section_scope", "all"),
                    "local_override_tag": row.get("local_override_tag", ""),
                    "example_lt": row.get("example_lt", ""),
                }
            )
    return rows


def select_active_acronyms(slug: str, source_text: str, research_text: str) -> list[dict[str, str]]:
    chapter_number = chapter_scope_number(slug)
    blob = f"{source_text}\n{research_text}"
    rows = []
    for row in read_tsv(ACRONYMS_PATH):
        acronym = row["acronym"]
        if acronym not in blob and row["lt"] not in blob and row["en"] not in blob:
            continue
        rows.append(
            {
                "acronym": acronym,
                "lt": row["lt"],
                "en": row["en"],
                "policy": row["policy"],
                "notes": row["notes"],
                "must_expand_first": row.get("must_expand_first", ""),
                "allowed_in_headings": row.get("allowed_in_headings", ""),
                "ambiguous_context": row.get("ambiguous_context", ""),
                "preferred_lt_context": row.get("preferred_lt_context", ""),
                "section_scope": chapter_number,
            }
        )
    return rows


def select_localization_overrides(slug: str, source_text: str, research_text: str) -> list[dict[str, str]]:
    chapter_number = chapter_scope_number(slug)
    blob = normalize_key(f"{source_text}\n{research_text}")
    rows = []
    for row in read_tsv(LOCALIZATION_OVERRIDES_PATH):
        if not scope_allows(row.get("scope", "all"), chapter_number):
            continue
        if normalize_key(row["source_term"]) not in blob:
            continue
        rows.append(row)
    return rows


def load_gold_section_examples() -> list[dict[str, object]]:
    if not GOLD_SECTIONS_INDEX_PATH.exists():
        return []

    rows: list[dict[str, object]] = []
    for row in read_tsv(GOLD_SECTIONS_INDEX_PATH):
        relative_path = row.get("path", "")
        if not relative_path:
            continue
        example_path = BOOK_ROOT / relative_path
        if not example_path.exists():
            continue
        rows.append(
            {
                "kind": "section",
                "example_id": row["example_id"],
                "source_chapter": row["source_chapter"],
                "block_id": row["block_id"],
                "block_type": row["block_type"],
                "tags": split_multi(row.get("tags", "")),
                "text": example_path.read_text(encoding="utf-8").strip(),
                "notes": row.get("notes", ""),
                "path": row["path"],
            }
        )
    return rows


def load_gold_phrase_examples() -> list[dict[str, object]]:
    examples: list[dict[str, object]] = []
    for row in read_tsv(GOLD_PHRASES_PATH):
        tags = detect_tags(f"{row['bad_en_shaped_lt']} {row['preferred_lt']}", "narrative", [])
        examples.append(
            {
                "kind": "phrase",
                "source_chapter": row["source_chapter"],
                "block_type": "any",
                "tags": tags,
                "text": row["preferred_lt"],
                "notes": row["notes"],
                "category": row["category"],
                "bad_en_shaped_lt": row["bad_en_shaped_lt"],
            }
        )
    return examples


def select_gold_examples(slug: str, blocks: list[dict[str, object]]) -> list[dict[str, object]]:
    chapter_number = chapter_scope_number(slug)
    chapter_tags = {tag for block in blocks for tag in block.get("tags", [])}
    chapter_block_types = {block.get("block_type", "") for block in blocks}

    gold_examples: list[dict[str, object]] = []
    gold_examples.extend(load_gold_phrase_examples())

    scored_sections: list[tuple[int, dict[str, object]]] = []
    for example in load_gold_section_examples():
        score = 0
        tags = set(example.get("tags", []))
        if example["source_chapter"] == chapter_number:
            score += 4
        if example["block_type"] in chapter_block_types:
            score += 2
        score += len(tags & chapter_tags)
        if score > 0:
            scored_sections.append((score, example))

    scored_sections.sort(key=lambda item: (-item[0], item[1]["example_id"]))
    gold_examples.extend(example for _, example in scored_sections[:8])
    return gold_examples


def classify_narrative_block(item: str) -> tuple[str, list[str], list[str]]:
    normalized = normalize_key(item)
    risk_flags: list[str] = []
    block_type = "narrative"
    if any(keyword in normalized for keyword in LOCALIZATION_KEYWORDS):
        block_type = "legal_localization"
        risk_flags.append("localization_override")
    if any(keyword in normalized for keyword in COMPLEX_PROSE_KEYWORDS):
        risk_flags.append("complex_prose")
    if "management" in normalized or "approach" in normalized:
        risk_flags.append("algorithmic_narrative")
    tags = detect_tags(item, block_type, risk_flags)
    return block_type, sorted(set(risk_flags)), tags


def completion_hint_for(kind: str, label: str, title: str) -> str:
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


def make_structured_block(kind: str, label: str, title: str, source_anchor: str) -> dict[str, object]:
    normalized_title = normalize_key(title)
    if kind == "table":
        block_type = "table"
    elif kind == "figure":
        block_type = "algorithm" if any(word in normalized_title for word in {"algorithm", "approach", "management"}) else "figure_caption"
    elif kind == "box":
        block_type = "callout"
    elif kind == "chart":
        block_type = "chart"
    else:
        block_type = "figure_caption"

    risk_flags: list[str] = ["structured_content"]
    if any(keyword in normalized_title for keyword in LOCALIZATION_KEYWORDS):
        risk_flags.append("localization_override")
    if any(keyword in normalized_title for keyword in COMPLEX_PROSE_KEYWORDS):
        risk_flags.append("complex_prose")

    tags = detect_tags(title, block_type, risk_flags)
    return {
        "block_id": f"{block_type}-{label}-{slugify(title)}" if label else f"{block_type}-{slugify(title)}",
        "block_type": block_type,
        "heading": title,
        "source_anchor": source_anchor,
        "source_label": label,
        "risk_flags": sorted(set(risk_flags)),
        "tags": tags,
        "draft_mode": BLOCK_TYPE_TO_MODE[block_type],
        "adjudication_candidate": is_adjudication_candidate(block_type, risk_flags, tags),
        "completion_hint": completion_hint_for(kind, label, title),
        "summary_allowed": kind == "chart",
    }


def build_blocks(inventory: dict[str, list[str]]) -> list[dict[str, object]]:
    blocks: list[dict[str, object]] = []
    for idx, item in enumerate(inventory["subsections"], start=1):
        block_type, risk_flags, tags = classify_narrative_block(item)
        blocks.append(
            {
                "block_id": f"{block_type}-{idx:02d}-{slugify(item)}",
                "block_type": block_type,
                "heading": item,
                "source_anchor": item,
                "risk_flags": risk_flags,
                "tags": tags,
                "draft_mode": BLOCK_TYPE_TO_MODE[block_type],
                "adjudication_candidate": is_adjudication_candidate(block_type, risk_flags, tags),
            }
        )

    for bucket in ("tables", "figures", "boxes"):
        for item in inventory[bucket]:
            kind, label = parse_structured_label(item)
            title = item
            if kind and label:
                title = re.sub(rf"^(Table|Figure|Box|Chart)\s+{re.escape(label)}\s+", "", item)
            blocks.append(make_structured_block(kind or "figure", label, title, item))
    return blocks


def build_style_hotspots(inventory: dict[str, list[str]]) -> list[dict[str, str]]:
    hotspots: list[dict[str, str]] = []
    for text in inventory["language_risks"]:
        hotspots.append({"category": "language_risk", "text": text})
    for text in inventory["anti_calque"]:
        hotspots.append({"category": "anti_calque", "text": text})
    for text in inventory["localization_decisions"]:
        hotspots.append({"category": "localization_decision", "text": text})
    for text in inventory["local_practice_changes"]:
        hotspots.append({"category": "local_practice_change", "text": text})
    return hotspots


def infer_chapter_title(slug: str, lt_text: str, source_text: str) -> str:
    for text in (lt_text, source_text):
        first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
        if first_line.startswith("# "):
            return first_line[2:].strip()
    return slug.split("-", 1)[1].replace("-", " ").title()


def main() -> int:
    args = parse_args()
    slug = resolve_chapter_slug(args.chapter)
    try:
        validate_chapter_inventory_or_raise(slug)
    except ValueError as exc:
        raise SystemExit(str(exc))
    paths = chapter_paths_for_slug(slug)
    context = load_chapter_context(slug)
    inventory = extract_inventory(context["research_sections"])
    blocks = build_blocks(inventory)
    data = {
        "chapter_slug": slug,
        "chapter_title": infer_chapter_title(slug, context["lt_text"], context["source_text"]),
        "page_range": context["page_range"],
        "source_md": context["source_md"],
        "lt_target_md": context["lt_target_md"],
        "blocks": blocks,
        "active_terms": select_active_terms(slug, inventory, context["source_text"], context["research_text"]),
        "active_acronyms": select_active_acronyms(slug, context["source_text"], context["research_text"]),
        "localization_overrides": select_localization_overrides(slug, context["source_text"], context["research_text"]),
        "style_hotspots": build_style_hotspots(inventory),
        "gold_examples": select_gold_examples(slug, blocks),
    }

    output_path = Path(args.out) if args.out else paths["pack"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dump_yaml(output_path, data)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
