#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re

from workflow_book import chapter_paths_for_slug, resolve_chapter_slug
from workflow_markdown import (
    extract_inventory,
    extract_source_structured_items,
    parse_markdown_sections,
    parse_structured_label,
)
from workflow_rules import activate_book_root


RESEARCH_BUCKETS = ("tables", "figures", "boxes")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate that the research inventory covers all structured source blocks."
    )
    parser.add_argument("--book-root", help="Optional books/<slug> root. If omitted, uses MEDBOOK_ROOT.")
    parser.add_argument("chapter", help="Chapter slug or number.")
    return parser.parse_args()


def research_structured_items(inventory: dict[str, list[str]], research_path: str) -> tuple[list[dict[str, str]], list[str]]:
    items: list[dict[str, str]] = []
    errors: list[str] = []
    seen: dict[tuple[str, str], str] = {}

    for bucket in RESEARCH_BUCKETS:
        for raw_item in inventory.get(bucket, []):
            kind, label = parse_structured_label(raw_item)
            if not kind or not label:
                errors.append(
                    f"{research_path}: structured inventory item must start with "
                    f"`Table`, `Figure`, `Box` or `Chart` plus a label: `{raw_item}`"
                )
                continue
            title = re.sub(rf"^(Table|Figure|Box|Chart)\s+{re.escape(label)}\s+", "", raw_item).strip()
            key = (kind, label)
            if key in seen:
                errors.append(
                    f"{research_path}: duplicate structured inventory item for {kind.title()} {label}: "
                    f"`{raw_item}` duplicates `{seen[key]}`"
                )
                continue
            seen[key] = raw_item
            items.append({"kind": kind, "label": label, "title": title, "raw": raw_item})

    return items, errors


def validate_chapter_inventory(slug: str) -> list[str]:
    paths = chapter_paths_for_slug(slug)
    source_text = paths["source"].read_text(encoding="utf-8")
    research_text = paths["research"].read_text(encoding="utf-8")
    inventory = extract_inventory(parse_markdown_sections(research_text))

    source_items = extract_source_structured_items(source_text)
    research_items, errors = research_structured_items(inventory, str(paths["research"]))

    source_index = {(item["kind"], item["label"]): item for item in source_items}
    research_index = {(item["kind"], item["label"]): item for item in research_items}

    missing_keys = sorted(set(source_index) - set(research_index))
    for kind, label in missing_keys:
        source_item = source_index[(kind, label)]
        errors.append(
            f"{paths['research']}: Source inventorius missing {kind.title()} {label} "
            f"`{source_item['title']}` from {paths['source']}"
        )

    extra_keys = sorted(set(research_index) - set(source_index))
    for kind, label in extra_keys:
        research_item = research_index[(kind, label)]
        errors.append(
            f"{paths['research']}: Source inventorius lists {kind.title()} {label} "
            f"`{research_item['title']}`, but source chapter has no matching structured block"
        )

    return errors


def validate_chapter_inventory_or_raise(slug: str) -> None:
    errors = validate_chapter_inventory(slug)
    if errors:
        raise ValueError("\n".join(errors))


def main() -> int:
    args = parse_args()
    activate_book_root(args.book_root)
    slug = resolve_chapter_slug(args.chapter, args.book_root)
    try:
        validate_chapter_inventory_or_raise(slug)
    except ValueError as exc:
        raise SystemExit(str(exc))

    print(f"Structured inventory matches source chapter for {slug}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
