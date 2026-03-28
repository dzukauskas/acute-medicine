#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from book_workflow_support import (
    activate_book_root,
    chapter_number_from_slug,
    load_review_taxonomy_rows,
    read_tsv,
    require_book_root,
    resolve_chapter_slug,
    review_taxonomy_path,
)


PROMOTION_TARGET_ALIASES = {
    "termbase.tsv": "shared/lexicon/termbase.tsv",
    "acronyms.tsv": "shared/lexicon/acronyms.tsv",
    "gold_phrases.tsv": "shared/prose/gold_phrases.tsv",
    "calque_patterns.tsv": "shared/prose/calque_patterns.tsv",
    "localization_overrides.tsv": "shared/localization/localization_overrides.tsv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize review deltas into normalized promotion candidates."
    )
    parser.add_argument("--book-root", help="Optional books/<slug> root. If omitted, uses MEDBOOK_ROOT.")
    parser.add_argument("chapter", help="Chapter slug or number.")
    parser.add_argument(
        "--emit-regression",
        action="store_true",
        help="Also print normalized JSONL candidates for regression_examples.",
    )
    return parser.parse_args()


def review_delta_path(slug: str) -> Path:
    return require_book_root() / "review_deltas" / f"{slug}.tsv"


def render_gold_phrase(row: dict[str, str], slug: str) -> str:
    chapter_number = chapter_number_from_slug(slug)
    return (
        f"{row['defect_class']}\t{row['bad_form']}\t{row['fixed_form']}\t"
        f"{row['notes']}\t{chapter_number}"
    )


def render_calque_pattern(row: dict[str, str], slug: str) -> str:
    chapter_number = chapter_number_from_slug(slug)
    return (
        f"phrase\t{row['bad_form']}\t{row['fixed_form']}\t{row['notes']}\t"
        f"{row['defect_class']}\t{row['severity']}\t{chapter_number}\tgenerated from review_deltas"
    )


def render_localization_override(row: dict[str, str], slug: str) -> str:
    chapter_number = chapter_number_from_slug(slug)
    defect_class = row.get("defect_class", "").strip()
    replacement_mode = "replace_lt"
    if defect_class == "brand_drift":
        replacement_mode = "genericize"
    elif defect_class == "market_drift":
        replacement_mode = "genericize"
    elif defect_class == "jurisdiction_drift":
        replacement_mode = "original_context_callout"
    elif defect_class == "dose_drift":
        replacement_mode = "replace_lt"
    return (
        f"{row['bad_form']}\tmixed-anglosphere\t{replacement_mode}\t{row['fixed_form']}\t\t{chapter_number}\t"
        f"{row['notes']}\t{review_delta_path(slug)}\tgenerated from defect_class={defect_class or 'unknown'}"
    )


def render_regression_example(row: dict[str, str], slug: str) -> str:
    payload = {
        "chapter_slug": slug,
        "block_id": row["block_id"],
        "defect_class": row["defect_class"],
        "bad_form": row["bad_form"],
        "fixed_form": row["fixed_form"],
        "note": row["notes"],
    }
    return json.dumps(payload, ensure_ascii=False)


def normalize_promotion_target(target: str) -> str:
    cleaned = target.strip()
    if not cleaned:
        return ""
    return PROMOTION_TARGET_ALIASES.get(cleaned, cleaned)


def resolved_target(row: dict[str, str], taxonomy: dict[str, dict[str, str]]) -> str:
    explicit_target = row.get("promote_target", "").strip()
    if explicit_target:
        return normalize_promotion_target(explicit_target)

    defect_class = row.get("defect_class", "").strip()
    taxon = taxonomy.get(defect_class)
    default_target = (taxon or {}).get("default_promote_target", "").strip()
    if default_target:
        return normalize_promotion_target(default_target)

    return "manual-review"


def main() -> int:
    args = parse_args()
    activate_book_root(args.book_root)
    slug = resolve_chapter_slug(args.chapter, args.book_root)
    delta_path = review_delta_path(slug)
    if not delta_path.exists():
        raise SystemExit(f"Nerastas review delta failas: {delta_path}")

    taxonomy = {row["defect_class"]: row for row in load_review_taxonomy_rows()}
    deltas = read_tsv(delta_path)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in deltas:
        grouped[resolved_target(row, taxonomy)].append(row)

    lines: list[str] = [
        f"# Promotion candidates for {slug}",
        "",
        f"- Review delta: `{delta_path}`",
        f"- Taxonomy: `{review_taxonomy_path()}`",
        "",
        "## Taxonomy summary",
    ]
    for defect_class in sorted({row["defect_class"] for row in deltas}):
        taxon = taxonomy.get(defect_class, {})
        lines.append(
            f"- `{defect_class}`: {taxon.get('description', 'nėra aprašymo')} "
            f"(default promote target: `{taxon.get('default_promote_target', 'n/a')}`)"
        )

    renderers = {
        "shared/prose/gold_phrases.tsv": render_gold_phrase,
        "shared/prose/calque_patterns.tsv": render_calque_pattern,
        "shared/localization/localization_overrides.tsv": render_localization_override,
        "regression_examples": render_regression_example,
    }

    for target in sorted(grouped):
        lines.extend(["", f"## Candidates for `{target}`", ""])
        renderer = renderers.get(target)
        if renderer is None:
            lines.append("- Manual follow-up required; no normalized renderer is defined for this target.")
            for row in grouped[target]:
                lines.append(
                    f"  - `{row['block_id']}` {row['defect_class']}: {row['bad_form']} -> {row['fixed_form']}"
                )
            continue
        if target == "regression_examples" and not args.emit_regression:
            lines.append("- Use `--emit-regression` to print JSONL-ready regression examples.")
            continue
        if target == "regression_examples":
            lines.extend(renderer(row, slug) for row in grouped[target])
        else:
            lines.extend(renderer(row, slug) for row in grouped[target])

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
