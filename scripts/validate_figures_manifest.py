#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from workflow_book import chapter_paths_for_slug, resolve_chapter_slug
from workflow_figures import chapter_image_repo_paths, manifest_row_chapter_slug
from workflow_rules import read_tsv, resolve_book_root


REPO_ROOT = Path(__file__).resolve().parents[1]
ALLOWED_CANONICAL_TYPES = {"whimsical_board"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate active figure manifest rows and optional chapter image references."
    )
    parser.add_argument(
        "--book-root",
        help="Optional books/<slug> root. If omitted, uses MEDBOOK_ROOT.",
    )
    parser.add_argument("chapter", nargs="?", help="Optional chapter slug or number.")
    parser.add_argument(
        "--manifest",
        type=Path,
        help="Path to lt/figures/manifest.tsv. Defaults to <book-root>/lt/figures/manifest.tsv.",
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
        chapter_slug = manifest_row_chapter_slug(row)

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
            if not chapter_slug:
                errors.append(
                    f"manifest.tsv:{index} notes lauke trūksta chapter_slug=... ({figure_id or 'be id'})."
                )

    return errors, by_png_path


def validate_chapter_refs(
    chapter: str,
    rows: list[dict[str, str]],
    by_png_path: dict[str, dict[str, str]],
    book_root: Path | None,
) -> list[str]:
    errors: list[str] = []
    slug = resolve_chapter_slug(chapter, book_root)
    lt_path = chapter_paths_for_slug(slug, book_root)["lt"]
    if not lt_path.exists():
        return [f"Nerastas LT skyrius: {lt_path}"]

    repo_paths_in_chapter = set(chapter_image_repo_paths(lt_path))
    text = lt_path.read_text(encoding="utf-8")
    for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
        ref = match.group(1).strip()
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

    for row in rows:
        if manifest_row_chapter_slug(row) != slug:
            continue
        png_path = row.get("png_path", "").strip()
        if png_path and png_path not in repo_paths_in_chapter:
            errors.append(
                f"{lt_path}: aktyvus manifest paveikslas neįterptas į skyrių: "
                f"{row.get('figure_id', 'be-id')} ({row.get('figure_number', '').strip()}) -> {png_path}"
            )

    return errors


def main() -> int:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    manifest_path = args.manifest
    if manifest_path is None:
        if book_root is None:
            raise SystemExit("Nurodykite --manifest arba nustatykite MEDBOOK_ROOT / --book-root.")
        manifest_path = book_root / "lt" / "figures" / "manifest.tsv"
    elif book_root is None:
        resolved_manifest = manifest_path.expanduser().resolve()
        if (
            resolved_manifest.name == "manifest.tsv"
            and resolved_manifest.parent.name == "figures"
            and resolved_manifest.parent.parent.name == "lt"
        ):
            book_root = resolved_manifest.parents[2]
    rows = load_manifest_rows(manifest_path)
    errors, by_png_path = validate_manifest_rows(rows)

    if args.chapter:
        errors.extend(validate_chapter_refs(args.chapter, rows, by_png_path, book_root))
    elif book_root is not None:
        chapter_slugs = sorted({slug for row in rows if (slug := manifest_row_chapter_slug(row))})
        for chapter_slug in chapter_slugs:
            errors.extend(validate_chapter_refs(chapter_slug, rows, by_png_path, book_root))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    if args.chapter:
        print(
            f"Figure manifest valid and chapter image refs resolved for "
            f"{resolve_chapter_slug(args.chapter, book_root)}."
        )
    elif book_root is not None:
        print("Figure manifest and chapter embed contract valid.")
    else:
        print("Figure manifest valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
