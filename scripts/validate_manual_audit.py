#!/usr/bin/env python3
from __future__ import annotations

import argparse

from book_workflow_support import (
    AUDIT_STATUSES,
    MANUAL_AUDIT_AREAS,
    activate_book_root,
    chapter_paths_for_slug,
    extract_localization_research,
    parse_markdown_sections,
    resolve_chapter_slug,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate that the required final manual agent audit is present and machine-readable."
    )
    parser.add_argument("--book-root", help="Optional books/<slug> root. If omitted, uses MEDBOOK_ROOT.")
    parser.add_argument("chapter", help="Chapter slug or number.")
    return parser.parse_args()


def validate_manual_audit(slug: str) -> list[str]:
    research_path = chapter_paths_for_slug(slug)["research"]
    sections = parse_markdown_sections(research_path.read_text(encoding="utf-8"))
    research = extract_localization_research(sections)
    rows = research["manual_audit"]

    errors: list[str] = []
    if not rows:
        errors.append(
            f"{research_path}: trūksta arba neužpildyta sekcija `## Finalus agento auditas`."
        )
        return errors

    seen_areas: set[str] = set()
    for row in rows:
        area = row.get("area", "").strip()
        status = row.get("status", "").strip()
        note = row.get("note", "").strip()

        if not area:
            errors.append(f"{research_path}: `Finalus agento auditas` eilutėje trūksta `Sritis`.")
            continue
        if area in seen_areas:
            errors.append(f"{research_path}: `Finalus agento auditas` dubliuota sritis `{area}`.")
            continue
        seen_areas.add(area)

        if status not in AUDIT_STATUSES:
            errors.append(
                f"{research_path}: audito sritis `{area}` turi neleistiną statusą `{status}`."
            )
        if status == "eskaluoti" and not note:
            errors.append(
                f"{research_path}: audito sritis `{area}` su statusu `eskaluoti` privalo turėti `Pastaba`."
            )

    for area in MANUAL_AUDIT_AREAS:
        if area not in seen_areas:
            errors.append(
                f"{research_path}: `Finalus agento auditas` trūksta privalomos srities `{area}`."
            )

    return errors


def main() -> int:
    args = parse_args()
    activate_book_root(args.book_root)
    slug = resolve_chapter_slug(args.chapter, args.book_root)
    errors = validate_manual_audit(slug)
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Manual audit validation passed for {slug}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
