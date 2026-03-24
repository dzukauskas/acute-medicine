#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from book_workflow_support import BOOK_ROOT, chapter_number_from_slug, read_tsv, resolve_chapter_slug


REVIEW_TAXONOMY_PATH = BOOK_ROOT / "review_taxonomy.tsv"
REVIEW_DELTAS_DIR = BOOK_ROOT / "review_deltas"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize review deltas into normalized promotion candidates."
    )
    parser.add_argument("chapter", help="Chapter slug or number.")
    parser.add_argument(
        "--emit-regression",
        action="store_true",
        help="Also print normalized JSONL candidates for regression_examples.",
    )
    return parser.parse_args()


def review_delta_path(slug: str) -> Path:
    return REVIEW_DELTAS_DIR / f"{slug}.tsv"


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
    return (
        f"{row['bad_form']}\t{row['fixed_form']}\t{chapter_number}\t"
        f"{row['notes']}\t{review_delta_path(slug)}\tgenerated candidate"
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


def main() -> int:
    args = parse_args()
    slug = resolve_chapter_slug(args.chapter)
    delta_path = review_delta_path(slug)
    if not delta_path.exists():
        raise SystemExit(f"Nerastas review delta failas: {delta_path}")

    taxonomy = {row["defect_class"]: row for row in read_tsv(REVIEW_TAXONOMY_PATH)}
    deltas = read_tsv(delta_path)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in deltas:
        grouped[row["promote_target"]].append(row)

    lines: list[str] = [
        f"# Promotion candidates for {slug}",
        "",
        f"- Review delta: `{delta_path}`",
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
        "gold_phrases.tsv": render_gold_phrase,
        "calque_patterns.tsv": render_calque_pattern,
        "localization_overrides.tsv": render_localization_override,
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
