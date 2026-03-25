#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from book_workflow_support import chapter_paths_for_slug, read_tsv, resolve_chapter_slug


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "books/acute-medicine/lt/figures/manifest.tsv"
ALLOWED_CANONICAL_TYPES = {"whimsical_board"}
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate active figure manifest rows and optional chapter image references."
    )
    parser.add_argument("chapter", nargs="?", help="Optional chapter slug or number.")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=MANIFEST_PATH,
        help="Path to lt/figures/manifest.tsv.",
    )
    return parser.parse_args()


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def load_manifest_rows(manifest_path: Path) -> list[dict[str, str]]:
    if not manifest_path.exists():
        raise SystemExit(f"Nerastas manifest failas: {manifest_path}")
    return read_tsv(manifest_path)


def validate_manifest_rows(rows: list[dict[str, str]]) -> tuple[list[str], dict[str, dict[str, str]]]:
    errors: list[str] = []
    figure_ids: set[str] = set()
    figure_numbers: set[str] = set()
    png_paths: set[str] = set()
    canonical_paths: set[tuple[str, str]] = set()
    by_png_path: dict[str, dict[str, str]] = {}

    for index, row in enumerate(rows, start=2):
        figure_id = row.get("figure_id", "").strip()
        figure_number = row.get("figure_number", "").strip()
        png_path_value = row.get("png_path", "").strip()
        canonical_type = row.get("canonical_source_type", "").strip()
        canonical_path_value = row.get("canonical_source_path", "").strip()

        if not figure_id:
            errors.append(f"manifest.tsv:{index} trūksta figure_id.")
        elif figure_id in figure_ids:
            errors.append(f"manifest.tsv:{index} dubliuotas figure_id: {figure_id}")
        else:
            figure_ids.add(figure_id)

        if not figure_number:
            errors.append(f"manifest.tsv:{index} trūksta figure_number ({figure_id or 'be id'}).")
        elif figure_number in figure_numbers:
            errors.append(f"manifest.tsv:{index} dubliuotas figure_number: {figure_number}")
        else:
            figure_numbers.add(figure_number)

        if not png_path_value:
            errors.append(f"manifest.tsv:{index} trūksta png_path ({figure_id or 'be id'}).")
        else:
            if not png_path_value.endswith(".png"):
                errors.append(f"manifest.tsv:{index} png_path turi baigtis .png: {png_path_value}")
            if png_path_value in png_paths:
                errors.append(f"manifest.tsv:{index} dubliuotas png_path: {png_path_value}")
            else:
                png_paths.add(png_path_value)

            png_path = REPO_ROOT / png_path_value
            if not png_path.exists():
                errors.append(f"manifest.tsv:{index} nerastas PNG failas: {png_path_value}")
            by_png_path[png_path_value] = row

        if canonical_type not in ALLOWED_CANONICAL_TYPES:
            errors.append(
                f"manifest.tsv:{index} neleistinas canonical_source_type: {canonical_type!r}. "
                f"Leidžiami tik: {', '.join(sorted(ALLOWED_CANONICAL_TYPES))}."
            )
            continue

        if not canonical_path_value:
            errors.append(f"manifest.tsv:{index} trūksta canonical_source_path ({figure_id or 'be id'}).")
            continue

        duplicate_key = (canonical_type, canonical_path_value)
        if duplicate_key in canonical_paths:
            errors.append(
                f"manifest.tsv:{index} dubliuotas kanoninis šaltinis: {canonical_type} {canonical_path_value}"
            )
        else:
            canonical_paths.add(duplicate_key)

        if canonical_type == "whimsical_board":
            if not re.match(r"^https://whimsical\.com/", canonical_path_value):
                errors.append(
                    f"manifest.tsv:{index} whimsical_board turi būti Whimsical URL, gauta: "
                    f"{canonical_path_value}"
                )

    return errors, by_png_path


def extract_image_refs(chapter_path: Path) -> list[str]:
    refs: list[str] = []
    text = chapter_path.read_text(encoding="utf-8")
    for match in IMAGE_RE.finditer(text):
        refs.append(match.group(1).strip())
    return refs


def validate_chapter_refs(chapter: str, by_png_path: dict[str, dict[str, str]]) -> list[str]:
    errors: list[str] = []
    slug = resolve_chapter_slug(chapter)
    lt_path = chapter_paths_for_slug(slug)["lt"]
    if not lt_path.exists():
        return [f"Nerastas LT skyrius: {lt_path}"]

    for ref in extract_image_refs(lt_path):
        resolved = (lt_path.parent / ref).resolve()
        try:
            repo_path = repo_relative(resolved)
        except ValueError:
            errors.append(f"{lt_path}: paveikslėlio nuoroda išeina už repo ribų: {ref}")
            continue
        if repo_path not in by_png_path:
            errors.append(
                f"{lt_path}: paveikslėlio nuoroda nerasta manifeste: {ref} -> {repo_path}"
            )
            continue
        if not resolved.exists():
            errors.append(f"{lt_path}: paveikslėlio failas neegzistuoja: {ref}")

    return errors


def main() -> int:
    args = parse_args()
    rows = load_manifest_rows(args.manifest)
    errors, by_png_path = validate_manifest_rows(rows)

    if args.chapter:
        errors.extend(validate_chapter_refs(args.chapter, by_png_path))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    if args.chapter:
        print(f"Figure manifest valid and chapter image refs resolved for {resolve_chapter_slug(args.chapter)}.")
    else:
        print("Figure manifest valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
