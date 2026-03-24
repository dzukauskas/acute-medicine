#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import difflib
import re
from pathlib import Path

from book_workflow_support import load_yaml, normalize_key, strip_markdown


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a review_delta skeleton from before/after markdown files.")
    parser.add_argument("--chapter-pack", required=True, help="Path to chapter_pack YAML.")
    parser.add_argument("--before", required=True, help="Path to draft markdown.")
    parser.add_argument("--after", required=True, help="Path to final markdown.")
    parser.add_argument("--out", required=True, help="Output TSV path.")
    return parser.parse_args()


def chunk_markdown(text: str) -> list[dict[str, str]]:
    chunks: list[dict[str, str]] = []
    current_heading = ""
    buffer: list[str] = []

    def flush() -> None:
        if not buffer:
            return
        raw = "\n".join(buffer).strip()
        buffer.clear()
        if not raw:
            return
        normalized = normalize_key(raw)
        if normalized:
            chunks.append({"heading": current_heading, "raw": raw, "normalized": normalized})

    for line in text.splitlines():
        heading_match = HEADING_RE.match(line.strip())
        if heading_match:
            flush()
            current_heading = heading_match.group(2).strip()
            continue
        if not line.strip():
            flush()
            continue
        buffer.append(line.rstrip())

    flush()
    return chunks


def best_block_id(heading: str, text: str, blocks: list[dict]) -> str:
    normalized_heading = normalize_key(heading)
    normalized_text = normalize_key(text)
    best_score = 0
    best_block_id = "manual-review"

    for block in blocks:
        score = 0
        block_heading = normalize_key(block.get("heading", ""))
        source_anchor = normalize_key(block.get("source_anchor", ""))
        source_label = block.get("source_label", "")
        tags = {normalize_key(tag) for tag in block.get("tags", [])}

        if normalized_heading and normalized_heading == block_heading:
            score += 100
        elif normalized_heading and block_heading and (
            normalized_heading in block_heading or block_heading in normalized_heading
        ):
            score += 60

        if source_label and source_label in heading:
            score += 25
        if source_anchor and normalized_heading and normalized_heading in source_anchor:
            score += 20
        if block_heading and block_heading in normalized_text:
            score += 20
        score += len([tag for tag in tags if tag and tag in normalized_text]) * 5

        if score > best_score:
            best_score = score
            best_block_id = block.get("block_id", "manual-review")

    return best_block_id


def summarize_segment(chunks: list[dict[str, str]]) -> tuple[str, str]:
    heading = next((chunk["heading"] for chunk in chunks if chunk["heading"]), "")
    text = "\n\n".join(chunk["raw"] for chunk in chunks).strip()
    return heading, text


def build_rows(pack: dict, before_text: str, after_text: str) -> list[dict[str, str]]:
    before_chunks = chunk_markdown(before_text)
    after_chunks = chunk_markdown(after_text)
    matcher = difflib.SequenceMatcher(
        a=[chunk["normalized"] for chunk in before_chunks],
        b=[chunk["normalized"] for chunk in after_chunks],
    )

    rows: list[dict[str, str]] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue

        before_segment = before_chunks[i1:i2]
        after_segment = after_chunks[j1:j2]
        width = max(len(before_segment), len(after_segment))
        for index in range(width):
            before_chunk = before_segment[index] if index < len(before_segment) else {"heading": "", "raw": ""}
            after_chunk = after_segment[index] if index < len(after_segment) else {"heading": "", "raw": ""}
            before_raw = before_chunk["raw"].strip()
            after_raw = after_chunk["raw"].strip()
            if not before_raw and not after_raw:
                continue

            heading = after_chunk["heading"] or before_chunk["heading"]
            block_id = best_block_id(heading, after_raw or before_raw, pack.get("blocks", []))
            rows.append(
                {
                    "block_id": block_id,
                    "defect_class": "",
                    "bad_form": strip_markdown(before_raw),
                    "fixed_form": strip_markdown(after_raw),
                    "severity": "",
                    "promote_target": "",
                    "notes": "",
                }
            )

    return rows


def main() -> int:
    args = parse_args()
    pack = load_yaml(Path(args.chapter_pack))
    before_text = Path(args.before).read_text(encoding="utf-8")
    after_text = Path(args.after).read_text(encoding="utf-8")
    rows = build_rows(pack, before_text, after_text)

    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["block_id", "defect_class", "bad_form", "fixed_form", "severity", "promote_target", "notes"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
