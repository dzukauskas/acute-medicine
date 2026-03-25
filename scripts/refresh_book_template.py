#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from book_workflow_support import REPO_ROOT, book_title_from_readme, default_obsidian_dest, first_pdf_path, resolve_repo_path


TEMPLATE_ROOT = REPO_ROOT / "books" / "_template"
TEMPLATE_MANIFEST = TEMPLATE_ROOT / "template_manifest.json"
TOKEN_RE = re.compile(r"{{([A-Z0-9_]+)}}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refresh template-managed docs and scaffolds into an existing books/<slug> workspace."
    )
    parser.add_argument("--book-root", required=True, help="Target books/<slug> directory.")
    return parser.parse_args()


def load_template_manifest() -> dict[str, list[str]]:
    if not TEMPLATE_MANIFEST.exists():
        raise SystemExit(f"Nerastas template manifest: {TEMPLATE_MANIFEST}")
    return json.loads(TEMPLATE_MANIFEST.read_text(encoding="utf-8"))


def render_template_text(template_path: Path, context: dict[str, str]) -> str:
    text = template_path.read_text(encoding="utf-8")
    return TOKEN_RE.sub(lambda match: context.get(match.group(1), match.group(0)), text)


def context_for_book(book_root: Path) -> dict[str, str]:
    title = book_title_from_readme(book_root)
    pdf_path = first_pdf_path(book_root)
    pdf_name = pdf_path.name if pdf_path else "SOURCE.pdf"
    return {
        "BOOK_TITLE": title,
        "BOOK_SLUG": book_root.name,
        "BOOK_ROOT": book_root.relative_to(REPO_ROOT).as_posix(),
        "BOOK_PDF_NAME": pdf_name,
        "OBSIDIAN_DEST": default_obsidian_dest(book_root).as_posix(),
    }


def is_effectively_empty_scaffold(path: Path) -> bool:
    if not path.exists():
        return True
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return len(lines) <= 1


def write_rendered(template_rel: str, book_root: Path, context: dict[str, str]) -> None:
    template_path = TEMPLATE_ROOT / template_rel
    target_path = book_root / template_rel
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(render_template_text(template_path, context), encoding="utf-8")


def main() -> int:
    args = parse_args()
    book_root = resolve_repo_path(args.book_root)
    if not book_root.exists():
        raise SystemExit(f"Nerastas book root: {book_root}")
    if book_root == TEMPLATE_ROOT:
        raise SystemExit("Negalima refresh'inti pačio books/_template katalogo.")

    manifest = load_template_manifest()
    context = context_for_book(book_root)

    for rel_dir in manifest.get("required_directories", []):
        (book_root / rel_dir).mkdir(parents=True, exist_ok=True)

    refreshed: list[str] = []
    preserved: list[str] = []

    for rel_path in manifest.get("always_refresh", []):
        write_rendered(rel_path, book_root, context)
        refreshed.append(rel_path)

    for rel_path in manifest.get("refresh_if_empty", []):
        target_path = book_root / rel_path
        if is_effectively_empty_scaffold(target_path):
            write_rendered(rel_path, book_root, context)
            refreshed.append(rel_path)
        else:
            preserved.append(rel_path)

    print(f"Refreshed template into {book_root}")
    if refreshed:
        print("Updated:")
        for rel_path in refreshed:
            print(f"  - {rel_path}")
    if preserved:
        print("Preserved existing content:")
        for rel_path in preserved:
            print(f"  - {rel_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
