#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from book_workflow_support import chapter_paths_for_slug, load_yaml, normalize_key, resolve_chapter_slug


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether structured chapter-pack blocks are represented in the LT chapter."
    )
    parser.add_argument("chapter", help="Chapter slug, chapter number, or direct path to a chapter pack YAML.")
    return parser.parse_args()


def load_pack_and_target(raw: str) -> tuple[dict, Path]:
    path = Path(raw)
    if path.suffix in {".yaml", ".yml"} and path.is_file():
        pack = load_yaml(path)
        lt_target = Path(pack.get("lt_target_md", ""))
        return pack, lt_target
    slug = resolve_chapter_slug(raw)
    paths = chapter_paths_for_slug(slug)
    pack = load_yaml(paths["pack"])
    return pack, Path(pack.get("lt_target_md", "")) if pack.get("lt_target_md") else paths["lt"]


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
    if source_label and block_type == "chart":
        return bool(re.search(r"##\s*`?NEWS2`?\s+originalo\s+kontekste", lt_text, re.IGNORECASE))
    return False


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
    pack, lt_target = load_pack_and_target(args.chapter)
    if not lt_target.exists():
        raise SystemExit(f"Nerastas LT failas: {lt_target}")

    lt_text = lt_target.read_text(encoding="utf-8")
    missing: list[str] = []
    for block in pack.get("blocks", []):
        if not should_check(block):
            continue
        if not block_present(block, lt_text):
            missing.append(
                f"{lt_target}: missing block_id='{block.get('block_id')}' "
                f"block_type='{block.get('block_type')}' heading='{block.get('heading')}'"
            )

    if missing:
        print("\n".join(missing))
        return 1

    print("All checked structured blocks are represented in the LT chapter.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
