#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
import re
from pathlib import Path

from book_workflow_support import (
    activate_book_root,
    chapter_paths_for_slug,
    load_yaml,
    normalize_key,
    parse_markdown_sections,
    resolve_book_root,
    resolve_chapter_slug,
)


CHART_COVERAGE_RE = re.compile(r"<!--\s*chart-coverage:\s*([0-9.,\s]+)\s*-->", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether structured chapter-pack blocks are represented in the LT chapter."
    )
    parser.add_argument("--book-root", help="Optional books/<slug> root. If omitted, uses MEDBOOK_ROOT.")
    parser.add_argument("chapter", help="Chapter slug, chapter number, or direct path to a chapter pack YAML.")
    return parser.parse_args()


def load_pack_and_target(raw: str) -> tuple[dict, Path]:
    path = Path(raw)
    if path.suffix in {".yaml", ".yml"} and path.is_file():
        pack = load_yaml(path)
        active_book_root = resolve_book_root()
        base_root = active_book_root or path.resolve().parents[1]
        lt_target = Path(pack.get("lt_target_md", ""))
        if lt_target and not lt_target.is_absolute():
            lt_target = base_root / lt_target
        return pack, lt_target
    slug = resolve_chapter_slug(raw)
    paths = chapter_paths_for_slug(slug)
    pack = load_yaml(paths["pack"])
    if pack.get("lt_target_md"):
        lt_target = Path(pack.get("lt_target_md", ""))
        if not lt_target.is_absolute():
            lt_target = paths["pack"].resolve().parents[1] / lt_target
    else:
        lt_target = paths["lt"]
    return pack, lt_target


def block_present(block: dict, lt_text: str) -> bool:
    heading = block.get("completion_hint", "") or block.get("heading", "")
    source_label = block.get("source_label", "")
    normalized_lt = normalize_key(lt_text)
    normalized_heading = normalize_key(heading)
    if heading and normalized_heading and normalized_heading in normalized_lt:
        return True

    block_type = block.get("block_type", "")
    if source_label and block_type == "table":
        return bool(re.search(rf"##\s*{re.escape(source_label)}\s*lente", lt_text, re.IGNORECASE))
    if source_label and block_type in {"algorithm", "figure_caption"}:
        return bool(re.search(rf"##\s*{re.escape(source_label)}\s*paveiksl", lt_text, re.IGNORECASE))
    if source_label and block_type in {"callout", "legal_localization"}:
        return bool(re.search(rf"##\s*{re.escape(source_label)}\s*rėmel", lt_text, re.IGNORECASE))
    return False


def section_lines_for_heading(sections: dict[tuple[str, ...], list[str]], heading: str) -> list[str]:
    normalized_heading = normalize_key(heading)
    for key, lines in sections.items():
        if key and normalize_key(key[-1]) == normalized_heading:
            return lines
    return []


def parse_chart_coverage_markers(section_text: str) -> set[str]:
    labels: set[str] = set()
    for raw_value in CHART_COVERAGE_RE.findall(section_text):
        for part in raw_value.split(","):
            label = part.strip()
            if label:
                labels.add(label)
    return labels


def visible_chart_label_present(label: str, section_text: str) -> bool:
    patterns = [
        rf"\bChart\s*{re.escape(label)}\b",
        rf"\b{re.escape(label)}\s*diagrama\b",
    ]
    return any(re.search(pattern, section_text, re.IGNORECASE) for pattern in patterns)


def check_summary_group(blocks: list[dict], sections: dict[tuple[str, ...], list[str]], lt_target: Path) -> list[str]:
    heading = blocks[0].get("completion_hint", "") or blocks[0].get("heading", "")
    section_lines = section_lines_for_heading(sections, heading)
    if not section_lines:
        return [
            f"{lt_target}: missing summary heading for completion_hint='{heading}' "
            f"covering block_ids={','.join(block.get('block_id', '') for block in blocks)}"
        ]

    section_text = "\n".join(section_lines)
    expected_labels = {str(block.get("source_label", "")).strip() for block in blocks if block.get("source_label")}
    coverage_labels = parse_chart_coverage_markers(section_text)
    if coverage_labels:
        if coverage_labels != expected_labels:
            missing_labels = sorted(expected_labels - coverage_labels)
            unexpected_labels = sorted(coverage_labels - expected_labels)
            details: list[str] = []
            if missing_labels:
                details.append(f"missing labels={','.join(missing_labels)}")
            if unexpected_labels:
                details.append(f"unexpected labels={','.join(unexpected_labels)}")
            return [
                f"{lt_target}: chart coverage marker mismatch for completion_hint='{heading}' "
                f"({' ; '.join(details)})"
            ]
        return []

    missing_visible = sorted(label for label in expected_labels if not visible_chart_label_present(label, section_text))
    if missing_visible:
        return [
            f"{lt_target}: summary section '{heading}' does not prove chart coverage for labels="
            f"{','.join(missing_visible)}"
        ]
    return []


def should_check(block: dict) -> bool:
    return block.get("block_type") in {
        "table",
        "algorithm",
        "figure_caption",
        "callout",
        "chart",
        "legal_localization",
    }


def main() -> int:
    args = parse_args()
    activate_book_root(args.book_root)
    pack, lt_target = load_pack_and_target(args.chapter)
    if not lt_target.exists():
        raise SystemExit(f"Nerastas LT failas: {lt_target}")

    lt_text = lt_target.read_text(encoding="utf-8")
    lt_sections = parse_markdown_sections(lt_text)
    missing: list[str] = []
    summary_groups: dict[str, list[dict]] = defaultdict(list)
    for block in pack.get("blocks", []):
        if not should_check(block):
            continue
        if block.get("summary_allowed"):
            group_key = block.get("completion_hint", "") or block.get("heading", "")
            summary_groups[group_key].append(block)
            continue
        if not block_present(block, lt_text):
            missing.append(
                f"{lt_target}: missing block_id='{block.get('block_id')}' "
                f"block_type='{block.get('block_type')}' heading='{block.get('heading')}'"
            )

    for blocks in summary_groups.values():
        missing.extend(check_summary_group(blocks, lt_sections, lt_target))

    if missing:
        print("\n".join(missing))
        return 1

    print("All checked structured blocks are represented in the LT chapter.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
