#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from workflow_book_template import (
    context_for_book as template_context_for_book,
    load_book_metadata,
    load_template_manifest,
    materialize_required_directories,
    render_template_text,
)
from workflow_rules import resolve_repo_path
from workflow_runtime import REPO_ROOT


TEMPLATE_ROOT = REPO_ROOT / "books" / "_template"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refresh template-managed docs and scaffolds into an existing books/<slug> workspace."
    )
    parser.add_argument("--book-root", required=True, help="Target books/<slug> directory.")
    return parser.parse_args()

def context_for_book(book_root: Path) -> dict[str, str]:
    canonical_source = load_book_metadata(book_root)
    return template_context_for_book(book_root, canonical_source, repo_root=REPO_ROOT)


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

    try:
        manifest = load_template_manifest(TEMPLATE_ROOT)
        context = context_for_book(book_root)
    except (FileNotFoundError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc

    materialize_required_directories(book_root, manifest)

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
