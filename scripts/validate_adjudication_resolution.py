#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from book_workflow_support import (
    activate_book_root,
    chapter_paths_for_slug,
    extract_adjudication_decisions,
    load_yaml,
    normalize_yaml_structure,
    parse_markdown_sections,
    require_book_root,
    resolve_chapter_slug,
)


SCRIPT_DIR = Path(__file__).resolve().parent
ALLOWED_CHOICES = {"A", "B", "hibridinis"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate that adjudication candidates have a fresh adjudication pack and machine-readable decisions."
    )
    parser.add_argument("--book-root", help="Optional books/<slug> root. If omitted, uses MEDBOOK_ROOT.")
    parser.add_argument("chapter", help="Chapter slug or number.")
    return parser.parse_args()


def run_build(book_root: str, slug: str, out_path: Path) -> None:
    args = [sys.executable, str(SCRIPT_DIR / "build_adjudication_pack.py")]
    if book_root:
        args.extend(["--book-root", book_root])
    args.extend([slug, "--out", str(out_path)])
    completed = subprocess.run(args, capture_output=True, text=True)
    if completed.returncode != 0:
        raise SystemExit(
            completed.stderr.strip()
            or completed.stdout.strip()
            or f"build_adjudication_pack.py failed for {slug}."
        )


def validate_research_decisions(research_path: Path, candidate_ids: list[str]) -> list[str]:
    sections = parse_markdown_sections(research_path.read_text(encoding="utf-8"))
    parsed = extract_adjudication_decisions(sections)
    errors: list[str] = []

    if not candidate_ids:
        if parsed:
            errors.append(
                f"{research_path}: rasta `## Adjudication sprendimai` įrašų, nors šviežias adjudication pack neturi kandidatų."
            )
        return errors

    by_block_id: dict[str, dict[str, str]] = {}
    for row in parsed:
        block_id = row.get("block_id", "").strip()
        choice = row.get("choice", "").strip()
        reason = row.get("reason", "").strip()
        raw = row.get("raw", "").strip()

        if not block_id or not choice or not reason:
            errors.append(
                f"{research_path}: `## Adjudication sprendimai` eilutė turi būti formato "
                "`- <block_id> | <A|B|hibridinis> | <trumpa priežastis>`, gauta: `{raw}`."
            )
            continue
        if choice not in ALLOWED_CHOICES:
            errors.append(
                f"{research_path}: block `{block_id}` turi neleistiną pasirinkimą `{choice}`. "
                "Leidžiami: A, B, hibridinis."
            )
        if block_id in by_block_id:
            errors.append(f"{research_path}: dubliuotas adjudication sprendimas block `{block_id}`.")
            continue
        by_block_id[block_id] = row

    candidate_set = set(candidate_ids)
    for block_id in candidate_ids:
        if block_id not in by_block_id:
            errors.append(
                f"{research_path}: trūksta adjudication sprendimo block `{block_id}`."
            )
    for block_id in sorted(set(by_block_id) - candidate_set):
        errors.append(
            f"{research_path}: rastas adjudication sprendimas nežinomam arba nebeaktualiam block `{block_id}`."
        )

    return errors


def main() -> int:
    args = parse_args()
    activate_book_root(args.book_root)
    slug = resolve_chapter_slug(args.chapter, args.book_root)
    book_root = require_book_root(args.book_root)
    book_root_arg = args.book_root or os.environ.get("MEDBOOK_ROOT", "")
    research_path = chapter_paths_for_slug(slug, book_root)["research"]
    canonical_path = book_root / "adjudication_packs" / f"{slug}.yaml"

    with tempfile.TemporaryDirectory(prefix=f"{slug}-adjudication-") as temp_dir:
        fresh_path = Path(temp_dir) / f"{slug}.yaml"
        run_build(book_root_arg, slug, fresh_path)
        fresh = load_yaml(fresh_path)
        candidates = fresh.get("candidates", []) or []

        if not candidates and not canonical_path.exists():
            print(f"Adjudication resolution passed for {slug}: no candidates.")
            return 0

        if not canonical_path.exists():
            raise SystemExit(
                f"Kanoninis adjudication_pack neegzistuoja: {canonical_path}\n"
                f"Pirma sugeneruokite jį per `python3 scripts/build_adjudication_pack.py {slug}`."
            )

        canonical = normalize_yaml_structure(load_yaml(canonical_path))
        fresh_normalized = normalize_yaml_structure(fresh)
        if canonical != fresh_normalized:
            raise SystemExit(
                f"Kanoninis adjudication_pack pasenęs: {canonical_path}\n"
                f"Šviežiai sugeneruotas pack semantiškai skiriasi. "
                f"Pirma persigeneruokite `python3 scripts/build_adjudication_pack.py {slug}`."
            )

        errors = validate_research_decisions(
            research_path,
            [str(candidate.get("block_id", "")).strip() for candidate in candidates if str(candidate.get("block_id", "")).strip()],
        )
        if errors:
            raise SystemExit("\n".join(errors))

    print(f"Adjudication resolution passed for {slug}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
