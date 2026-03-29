#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from book_workflow_support import (
    CLINICAL_CLAIM_TYPES,
    activate_book_root,
    chapter_number_from_slug,
    chapter_paths_for_slug,
    detect_source_localization_signals,
    dump_yaml,
    extract_inventory,
    extract_localization_research,
    jurisdiction_to_pack_context,
    load_acronym_rows,
    load_gold_phrase_rows,
    load_gold_section_examples,
    load_localization_overrides,
    load_termbase_rows,
    metadata_value,
    normalize_authority_basis,
    normalize_claim_type,
    normalize_key,
    parse_markdown_sections,
    parse_structured_label,
    resolve_chapter_slug,
    term_candidates_path,
    scope_allows,
    slugify,
    structured_block_id,
    structured_block_type,
    structured_completion_hint,
    split_multi,
)
from mine_term_candidates import refresh_term_candidates_for_chapter
from validate_chapter_inventory import validate_chapter_inventory_or_raise
from validate_localization_readiness import validate_localization_readiness_or_raise
from validate_term_readiness import validate_term_readiness_or_raise


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
HIGH_RISK_REASON_BY_CLAIM_TYPE = {
    "dose": "dose-claim",
    "route": "dose-claim",
    "concentration": "dose-claim",
    "indication": "drug-selection",
    "contraindication": "drug-selection",
    "algorithm_step": "algorithm-step",
    "monitoring": "algorithm-step",
    "legal_scope": "legal-scope",
    "market_availability": "market-localization",
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
    parser.add_argument("--book-root", help="Optional books/<slug> root. If omitted, uses MEDBOOK_ROOT.")
    parser.add_argument("chapter", help="Chapter slug or number, for example 002 or 002-the-critically-ill-patient.")
    parser.add_argument(
        "--out",
        help="Optional output path. Defaults to $MEDBOOK_ROOT/chapter_packs/<slug>.yaml.",
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
        "page_range": metadata_value(pre_heading_lines, "Puslapiai")
        or metadata_value(pre_heading_lines, "Šaltinio segmentai"),
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
    for row in load_termbase_rows():
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
    for row in load_acronym_rows():
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
    for row in load_localization_overrides():
        if not scope_allows(row.get("scope", "all"), chapter_number):
            continue
        if normalize_key(row["source_term"]) not in blob:
            continue
        rows.append(row)
    return rows


def phrase_examples() -> list[dict[str, object]]:
    examples: list[dict[str, object]] = []
    for row in load_gold_phrase_rows():
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
    gold_examples.extend(phrase_examples())

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


def extract_source_excerpt(source_text: str, anchor: str, *, window: int = 8) -> str:
    anchor_norm = normalize_key(anchor)
    if not anchor_norm:
        return ""

    lines = [
        line.strip()
        for line in source_text.splitlines()
        if line.strip() and not line.lstrip().startswith("<!--")
    ]
    tokens = [token for token in anchor_norm.split() if len(token) > 2]
    best_index = -1
    best_score = 0

    for index, line in enumerate(lines):
        line_norm = normalize_key(line)
        if anchor_norm in line_norm:
            best_index = index
            best_score = 999
            break
        if not tokens:
            continue
        score = sum(1 for token in tokens if token in line_norm)
        if score > best_score and score >= max(1, len(tokens) // 2):
            best_index = index
            best_score = score

    if best_index < 0:
        return ""

    excerpt_lines: list[str] = []
    for line in lines[best_index : best_index + window]:
        if excerpt_lines and line.startswith("# "):
            break
        excerpt_lines.append(line)
    return "\n".join(excerpt_lines).strip()


def make_structured_block(kind: str, label: str, title: str, source_anchor: str, source_text: str) -> dict[str, object]:
    normalized_title = normalize_key(title)
    block_type = structured_block_type(kind, title)

    risk_flags: list[str] = ["structured_content"]
    if any(keyword in normalized_title for keyword in LOCALIZATION_KEYWORDS):
        risk_flags.append("localization_override")
    if any(keyword in normalized_title for keyword in COMPLEX_PROSE_KEYWORDS):
        risk_flags.append("complex_prose")

    tags = detect_tags(title, block_type, risk_flags)
    source_excerpt = extract_source_excerpt(source_text, source_anchor or title)
    return {
        "block_id": structured_block_id(kind, label, title),
        "block_type": block_type,
        "heading": title,
        "source_anchor": source_anchor,
        "source_label": label,
        "source_excerpt": source_excerpt,
        "risk_flags": sorted(set(risk_flags)),
        "tags": tags,
        "draft_mode": BLOCK_TYPE_TO_MODE[block_type],
        "adjudication_candidate": is_adjudication_candidate(block_type, risk_flags, tags),
        "completion_hint": structured_completion_hint(kind, label, title),
        "summary_allowed": kind == "chart",
    }


def build_blocks(inventory: dict[str, list[str]], source_text: str) -> list[dict[str, object]]:
    blocks: list[dict[str, object]] = []
    for idx, item in enumerate(inventory["subsections"], start=1):
        block_type, risk_flags, tags = classify_narrative_block(item)
        blocks.append(
            {
                "block_id": f"{block_type}-{idx:02d}-{slugify(item)}",
                "block_type": block_type,
                "heading": item,
                "source_anchor": item,
                "source_excerpt": extract_source_excerpt(source_text, item),
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
            blocks.append(make_structured_block(kind or "figure", label, title, item, source_text))
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


def block_mentions_term(block_blob: str, term: str) -> bool:
    term_norm = normalize_key(term)
    return bool(term_norm) and term_norm in block_blob


def default_localization_policy(block: dict[str, object]) -> dict[str, object]:
    tags = set(block.get("tags", []))
    block_type = block.get("block_type", "")
    if block_type in {"legal_localization", "chart"} or "uk-localization" in tags or "legal-localization" in tags:
        return {
            "jurisdiction_context": "mixed-anglosphere",
            "localization_action": "original_context_callout",
            "authority_basis": "original-context-only",
            "localization_note": "Pagrindiniame LT tekste nepalikite kaip vietinio standarto; jei reikia, rodykite tik `Originalo kontekstas` bloke.",
            "matched_localization_terms": [],
        }
    return {
        "jurisdiction_context": "universal",
        "localization_action": "replace_lt",
        "authority_basis": "LT",
        "localization_note": "Pagrindiniame LT tekste remkitės Lietuvos, o jei jų nepakanka, ES šaltiniais.",
        "matched_localization_terms": [],
    }


def infer_authority_basis_from_action(action: str) -> str:
    if action == "replace_eu":
        return "EU"
    if action in {"original_context_callout", "omit_nontransferable"}:
        return "original-context-only"
    return "LT"


def claim_matches_block(claim: dict[str, str], block: dict[str, object]) -> bool:
    source_anchor = normalize_key(claim.get("source_anchor", ""))
    if not source_anchor:
        return False
    haystacks = [
        normalize_key(str(block.get("heading", ""))),
        normalize_key(str(block.get("source_anchor", ""))),
        normalize_key(str(block.get("source_excerpt", ""))),
    ]
    return any(source_anchor in haystack or haystack in source_anchor for haystack in haystacks if haystack)


def matching_claims_for_block(claims: list[dict[str, str]], block: dict[str, object]) -> list[dict[str, str]]:
    matched = [claim for claim in claims if claim_matches_block(claim, block)]
    matched.sort(key=lambda row: (row.get("claim_type", ""), row.get("claim_id", "")))
    return matched


def matching_structured_policy_for_block(
    policies: list[dict[str, str]],
    block: dict[str, object],
) -> dict[str, str] | None:
    block_id = str(block.get("block_id", "")).strip()
    for row in policies:
        if row.get("block_id", "").strip() == block_id:
            return row
    return None


def semantic_risk_reason_set(
    block: dict[str, object],
    matched_claims: list[dict[str, str]],
) -> list[str]:
    reasons: set[str] = set()
    for claim in matched_claims:
        claim_type = normalize_claim_type(claim.get("claim_type", ""))
        if claim_type in HIGH_RISK_REASON_BY_CLAIM_TYPE:
            reasons.add(HIGH_RISK_REASON_BY_CLAIM_TYPE[claim_type])

    block_type = block.get("block_type", "")
    tags = set(block.get("tags", []))
    if block_type == "algorithm":
        reasons.add("algorithm-step")
    if block_type == "legal_localization" or tags & {"legal-localization"}:
        reasons.add("legal-scope")
    if block.get("localization_action") in {"genericize", "omit_nontransferable"}:
        reasons.add("market-localization")
    return sorted(reasons)


def semantic_risk_level_for(block: dict[str, object], reasons: list[str]) -> str:
    if reasons or block.get("block_type") in {"algorithm", "legal_localization", "chart"}:
        return "high"
    tags = set(block.get("tags", []))
    risk_flags = set(block.get("risk_flags", []))
    if tags & {"hemodynamic", "monitoring", "uk-localization", "legal-localization"} or risk_flags & {
        "complex_prose",
        "algorithmic_narrative",
    }:
        return "medium"
    return "low"


def required_authority_basis_for(
    block: dict[str, object],
    matched_claims: list[dict[str, str]],
) -> str:
    final_renderings = {claim.get("final_rendering", "").strip() for claim in matched_claims}
    if "keep_lt_normative" in final_renderings:
        return "LT"
    if "keep_eu_normative" in final_renderings:
        return "EU"
    if final_renderings & {"original_context_callout", "omit"}:
        return "original-context-only"
    return str(block.get("authority_basis", "") or "LT")


def annotate_block_localization(
    block: dict[str, object],
    localization_research: dict[str, object],
    overrides: list[dict[str, str]],
) -> dict[str, object]:
    block_blob = normalize_key(
        " ".join(
            [
                str(block.get("heading", "")),
                str(block.get("source_anchor", "")),
                str(block.get("source_excerpt", "")),
                " ".join(str(tag) for tag in block.get("tags", [])),
            ]
        )
    )
    matched_signals = [
        row for row in localization_research["signals"] if block_mentions_term(block_blob, row.get("source_term", ""))
    ]
    matched_decisions = [
        row for row in localization_research["decisions"] if block_mentions_term(block_blob, row.get("source_term", ""))
    ]
    matched_overrides = [row for row in overrides if block_mentions_term(block_blob, row.get("source_term", ""))]

    if not matched_signals and not matched_decisions and not matched_overrides:
        return default_localization_policy(block)

    if matched_signals and not matched_decisions:
        matched_terms = ", ".join(sorted({row.get("source_term", "") for row in matched_signals if row.get("source_term", "")}))
        raise ValueError(
            f"Blokui `{block.get('block_id', 'unknown')}` aptikti jurisdikciniai signalai ({matched_terms}), "
            "bet nėra tikslaus `LT/EU pakeitimo sprendimai` atitikmens research faile."
        )

    jurisdictions = [
        row.get("jurisdiction", "")
        for row in matched_signals + matched_overrides
        if row.get("jurisdiction", "").strip()
    ]
    action = ""
    authority_basis = ""
    localization_note = ""

    if matched_decisions:
        first_decision = matched_decisions[0]
        action = first_decision.get("replacement_mode", "").strip()
        authority_basis = normalize_authority_basis(first_decision.get("authority_basis", ""))
        localization_note = first_decision.get("localization_note", "").strip() or first_decision.get("notes", "").strip()

    if not action and matched_overrides:
        first_override = matched_overrides[0]
        action = first_override.get("replacement_mode", "").strip()
        authority_basis = infer_authority_basis_from_action(action)
        localization_note = first_override.get("local_lt", "").strip() or first_override.get("reason", "").strip()

    if not action:
        fallback = default_localization_policy(block)
        action = str(fallback["localization_action"])
        authority_basis = str(fallback["authority_basis"])
        localization_note = str(fallback["localization_note"])

    return {
        "jurisdiction_context": jurisdiction_to_pack_context(jurisdictions),
        "localization_action": action,
        "authority_basis": authority_basis or infer_authority_basis_from_action(action),
        "localization_note": localization_note,
        "matched_localization_terms": sorted(
            {
                row.get("source_term", "")
                for row in matched_signals + matched_decisions + matched_overrides
                if row.get("source_term", "").strip()
            }
        ),
    }


def annotate_block_semantics(
    block: dict[str, object],
    localization_research: dict[str, object],
) -> dict[str, object]:
    matched_claims = matching_claims_for_block(localization_research["claims"], block)
    structured_policy = matching_structured_policy_for_block(
        localization_research["structured_block_policies"], block
    )

    if block.get("block_type") in {"table", "algorithm", "figure_caption", "callout", "chart"} and structured_policy is None:
        raise ValueError(
            f"Blokui `{block.get('block_id', 'unknown')}` trūksta eilutės "
            "`## Struktūrinių blokų lokalizacijos sprendimai` lentelėje."
        )

    if structured_policy:
        lt_strategy = structured_policy.get("lt_strategy", "").strip()
        authority_source = structured_policy.get("authority_source", "").strip()
        if block.get("block_type") == "algorithm" and not authority_source:
            raise ValueError(
                f"Algorithm block `{block.get('block_id', 'unknown')}` privalo turėti `authority_source` "
                "sekcijoje `## Struktūrinių blokų lokalizacijos sprendimai`."
            )
        if block.get("block_type") == "table" and matched_claims and not authority_source:
            raise ValueError(
                f"Norminį klinikinį turinį turinti lentelė `{block.get('block_id', 'unknown')}` "
                "negali būti palikta be `authority_source`."
            )
        if lt_strategy == "original_context_callout" and structured_policy.get("original_context_allowed", "").strip().lower() not in {
            "yes",
            "true",
            "taip",
            "1",
        }:
            raise ValueError(
                f"Block `{block.get('block_id', 'unknown')}` su `original_context_callout` privalo turėti "
                "`original_context_allowed = yes`."
            )

    semantic_risk_reasons = semantic_risk_reason_set(block, matched_claims)
    semantic_risk_level = semantic_risk_level_for(block, semantic_risk_reasons)
    required_authority_basis = required_authority_basis_for(block, matched_claims)

    return {
        "matched_claim_ids": [row.get("claim_id", "") for row in matched_claims if row.get("claim_id", "").strip()],
        "matched_claim_types": sorted(
            {row.get("claim_type", "") for row in matched_claims if row.get("claim_type", "").strip()}
        ),
        "semantic_risk_level": semantic_risk_level,
        "semantic_risk_reasons": semantic_risk_reasons,
        "required_authority_basis": required_authority_basis,
        "structured_block_policy": structured_policy,
        "adjudication_candidate": bool(block.get("adjudication_candidate")) or semantic_risk_level == "high",
    }


def enrich_blocks_with_localization(
    blocks: list[dict[str, object]],
    localization_research: dict[str, object],
    overrides: list[dict[str, str]],
) -> list[dict[str, object]]:
    enriched: list[dict[str, object]] = []
    for block in blocks:
        enriched_block = dict(block)
        enriched_block.update(annotate_block_localization(enriched_block, localization_research, overrides))
        enriched_block.update(annotate_block_semantics(enriched_block, localization_research))
        enriched.append(enriched_block)
    return enriched


def infer_chapter_title(slug: str, lt_text: str, source_text: str) -> str:
    for text in (lt_text, source_text):
        first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
        if first_line.startswith("# "):
            return first_line[2:].strip()
    return slug.split("-", 1)[1].replace("-", " ").title()


def attach_claim_block_matches(
    claims: list[dict[str, str]],
    blocks: list[dict[str, object]],
) -> list[dict[str, object]]:
    enriched_claims: list[dict[str, object]] = []
    for claim in claims:
        matched_block_ids = [
            str(block.get("block_id", ""))
            for block in blocks
            if claim_matches_block(claim, block)
        ]
        enriched_claim = dict(claim)
        enriched_claim["matched_block_ids"] = matched_block_ids
        enriched_claims.append(enriched_claim)
    return enriched_claims


def main() -> int:
    args = parse_args()
    activate_book_root(args.book_root)
    slug = resolve_chapter_slug(args.chapter, args.book_root)
    try:
        validate_chapter_inventory_or_raise(slug)
        validate_localization_readiness_or_raise(slug)
    except ValueError as exc:
        raise SystemExit(str(exc))
    paths = chapter_paths_for_slug(slug)
    context = load_chapter_context(slug)
    term_candidates = refresh_term_candidates_for_chapter(slug, book_root=args.book_root)
    try:
        validate_term_readiness_or_raise(slug, book_root=args.book_root, current_rows=term_candidates)
    except ValueError as exc:
        raise SystemExit(str(exc))
    inventory = extract_inventory(context["research_sections"])
    localization_research = extract_localization_research(context["research_sections"])
    overrides = select_localization_overrides(slug, context["source_text"], context["research_text"])
    try:
        blocks = enrich_blocks_with_localization(
            build_blocks(inventory, context["source_text"]),
            localization_research,
            overrides,
        )
    except ValueError as exc:
        raise SystemExit(str(exc))
    clinical_claims = attach_claim_block_matches(localization_research["claims"], blocks)
    unmatched_claims = [claim["claim_id"] for claim in clinical_claims if claim.get("claim_id") and not claim.get("matched_block_ids")]
    if unmatched_claims:
        raise SystemExit(
            "Nepavyko claim-level įrašų susieti su chapter_pack blokais: "
            + ", ".join(unmatched_claims)
            + ". Patikrinkite `source_anchor` reikšmes `## Norminių teiginių matrica`."
        )
    block_ids = {str(block.get("block_id", "")) for block in blocks}
    unknown_structured_policies = [
        row.get("block_id", "")
        for row in localization_research["structured_block_policies"]
        if row.get("block_id", "").strip() and row.get("block_id", "").strip() not in block_ids
    ]
    if unknown_structured_policies:
        raise SystemExit(
            "Struktūrinių blokų lokalizacijos sprendimuose rasti nežinomi `block_id`: "
            + ", ".join(unknown_structured_policies)
            + "."
        )
    data = {
        "chapter_slug": slug,
        "chapter_title": infer_chapter_title(slug, context["lt_text"], context["source_text"]),
        "page_range": context["page_range"],
        "source_md": context["source_md"],
        "lt_target_md": context["lt_target_md"],
        "blocks": blocks,
        "clinical_claims": clinical_claims,
        "structured_block_policies": localization_research["structured_block_policies"],
        "active_terms": select_active_terms(slug, inventory, context["source_text"], context["research_text"]),
        "active_acronyms": select_active_acronyms(slug, context["source_text"], context["research_text"]),
        "localization_overrides": overrides,
        "source_jurisdiction_signals": detect_source_localization_signals(context["source_text"], args.book_root),
        "localization_decisions": localization_research["decisions"],
        "style_hotspots": build_style_hotspots(inventory),
        "gold_examples": select_gold_examples(slug, blocks),
        "term_candidates_path": str(term_candidates_path(args.book_root)),
        "term_candidates": term_candidates,
    }

    output_path = Path(args.out) if args.out else paths["pack"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dump_yaml(output_path, data)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
