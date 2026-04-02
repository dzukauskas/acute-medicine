#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from workflow_book import repo_relative_path
from workflow_figures import ensure_manifest_figure_embed, manifest_note_value
from workflow_obsidian import default_obsidian_dest, sync_book_to_obsidian
from workflow_rules import require_book_root, resolve_repo_path, slugify, read_tsv, write_tsv
from workflow_subprocess import DEFAULT_TIMEOUT_SECONDS, WorkflowSubprocessError, run_checked_subprocess


MANIFEST_FIELDS = [
    "figure_id",
    "figure_number",
    "png_path",
    "canonical_source_type",
    "canonical_source_path",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Register a source EPUB figure candidate as an active Whimsical-backed figure."
    )
    parser.add_argument("--book-root", required=True, help="Target books/<slug> directory.")
    parser.add_argument("--source-figure-id", required=True, help="Row ID from source/index/figures.tsv.")
    parser.add_argument("--figure-number", required=True, help="Book-visible figure number, for example 3.1.")
    parser.add_argument("--whimsical-url", required=True, help="Whimsical board URL.")
    parser.add_argument("--notes", help="Optional extra note appended to the manifest row.")
    parser.add_argument(
        "--storage-state",
        type=Path,
        help="Optional storage-state path forwarded to render_whimsical_figure.py.",
    )
    parser.add_argument(
        "--login",
        action="store_true",
        help="Open Whimsical login before rendering the newly registered figure.",
    )
    parser.add_argument(
        "--sync-obsidian",
        action="store_true",
        help="After render + chapter embed, sync the updated chapter and figures into Obsidian.",
    )
    parser.add_argument(
        "--obsidian-dest",
        type=Path,
        help="Optional Obsidian destination used when --sync-obsidian is set.",
    )
    return parser.parse_args()


def source_figure_index_path(book_root: Path) -> Path:
    return book_root / "source" / "index" / "figures.tsv"


def manifest_path(book_root: Path) -> Path:
    return book_root / "lt" / "figures" / "manifest.tsv"


def load_source_figure_row(book_root: Path, source_figure_id: str) -> dict[str, str]:
    index_path = source_figure_index_path(book_root)
    if not index_path.exists():
        raise SystemExit(f"Nerastas source figure indeksas: {index_path}")
    rows = read_tsv(index_path)
    for row in rows:
        if row.get("source_figure_id", "").strip() == source_figure_id:
            return row
    raise SystemExit(f"Nerastas source_figure_id `{source_figure_id}` faile {index_path}")


def load_manifest_rows(book_root: Path) -> list[dict[str, str]]:
    path = manifest_path(book_root)
    if not path.exists():
        raise SystemExit(f"Nerastas aktyvus manifest failas: {path}")
    return read_tsv(path)


def existing_source_figure_id(notes: str) -> str:
    return manifest_note_value(notes, "source_figure_id")


def normalize_whimsical_url(raw_url: str) -> str:
    url = raw_url.strip()
    if not url.startswith("https://whimsical.com/"):
        raise SystemExit(f"Whimsical URL turi prasidėti `https://whimsical.com/`, gauta: {url}")
    return url


def deterministic_figure_id(figure_number: str, source_figure_id: str) -> str:
    figure_number_slug = slugify(figure_number) or "figure"
    source_slug = slugify(source_figure_id) or "source"
    return f"figure-{figure_number_slug}-{source_slug}"


def manifest_png_path(book_root: Path, figure_id: str) -> str:
    return repo_relative_path(book_root / "lt" / "figures" / f"{figure_id}.png")


def build_notes(source_row: dict[str, str], extra_notes: str | None) -> str:
    parts = [
        f"source_figure_id={source_row['source_figure_id']}",
        f"chapter_slug={source_row['chapter_slug']}",
        f"source_href={source_row['source_href']}",
        f"asset_path={source_row['asset_path']}",
    ]
    if source_row.get("media_type", "").strip():
        parts.append(f"media_type={source_row['media_type']}")
    if source_row.get("alt_text", "").strip():
        parts.append(f"alt_text={source_row['alt_text']}")
    if source_row.get("caption_text", "").strip():
        parts.append(f"caption_text={source_row['caption_text']}")
    if source_row.get("notes", "").strip():
        parts.append(f"source_notes={source_row['notes']}")
    if extra_notes and extra_notes.strip():
        parts.append(f"user_notes={extra_notes.strip()}")
    return "; ".join(parts)


def display_path(path: Path) -> str:
    try:
        return repo_relative_path(path)
    except ValueError:
        return str(path)


def validate_new_row(manifest_rows: list[dict[str, str]], new_row: dict[str, str]) -> None:
    new_source_figure_id = existing_source_figure_id(new_row["notes"])
    for row in manifest_rows:
        if row.get("figure_id", "") == new_row["figure_id"]:
            raise SystemExit(f"Manifest already contains figure_id `{new_row['figure_id']}`.")
        if row.get("figure_number", "") == new_row["figure_number"]:
            raise SystemExit(f"Manifest already contains figure_number `{new_row['figure_number']}`.")
        if row.get("canonical_source_path", "") == new_row["canonical_source_path"]:
            raise SystemExit(f"Manifest already contains Whimsical URL `{new_row['canonical_source_path']}`.")
        if existing_source_figure_id(row.get("notes", "")) == new_source_figure_id:
            raise SystemExit(f"Source figure `{new_source_figure_id}` jau susietas su aktyviu manifest įrašu.")


def append_manifest_row(book_root: Path, new_row: dict[str, str]) -> str:
    path = manifest_path(book_root)
    original_text = path.read_text(encoding="utf-8")
    rows = load_manifest_rows(book_root)
    validate_new_row(rows, new_row)
    rows.append(new_row)
    write_tsv(path, MANIFEST_FIELDS, rows)
    return original_text


def rollback_manifest(book_root: Path, original_text: str) -> None:
    manifest_path(book_root).write_text(original_text, encoding="utf-8")


def render_registered_figure(
    book_root: Path,
    figure_id: str,
    *,
    storage_state: Path | None = None,
    login: bool = False,
) -> None:
    args = [
        sys.executable,
        str(Path(__file__).resolve().with_name("render_whimsical_figure.py")),
        "--book-root",
        str(book_root),
    ]
    if storage_state is not None:
        args.extend(["--storage-state", str(storage_state)])
    if login:
        args.append("--login")
    args.append(figure_id)
    run_checked_subprocess(
        args,
        phase="render registered figure",
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )


def remove_rendered_png_if_present(row: dict[str, str]) -> None:
    png_path = resolve_repo_path(row.get("png_path", "").strip())
    if png_path.exists():
        png_path.unlink()


def main() -> int:
    args = parse_args()
    book_root = require_book_root(resolve_repo_path(args.book_root))
    whimsical_url = normalize_whimsical_url(args.whimsical_url)
    source_row = load_source_figure_row(book_root, args.source_figure_id.strip())
    figure_id = deterministic_figure_id(args.figure_number, source_row["source_figure_id"])

    new_row = {
        "figure_id": figure_id,
        "figure_number": args.figure_number.strip(),
        "png_path": manifest_png_path(book_root, figure_id),
        "canonical_source_type": "whimsical_board",
        "canonical_source_path": whimsical_url,
        "notes": build_notes(source_row, args.notes),
    }

    original_text = append_manifest_row(book_root, new_row)
    storage_state = getattr(args, "storage_state", None)
    login = bool(getattr(args, "login", False))
    sync_obsidian = bool(getattr(args, "sync_obsidian", False))
    obsidian_dest_arg = getattr(args, "obsidian_dest", None)
    try:
        render_storage_state = storage_state.expanduser() if storage_state else None
        if render_storage_state is None and not login:
            render_registered_figure(book_root, figure_id)
        else:
            render_registered_figure(
                book_root,
                figure_id,
                storage_state=render_storage_state,
                login=login,
            )
    except WorkflowSubprocessError as exc:
        rollback_manifest(book_root, original_text)
        remove_rendered_png_if_present(new_row)
        raise SystemExit(
            f"Nepavyko sugeneruoti PNG po manifest registracijos; manifest atstatytas. "
            f"{exc}"
        ) from exc

    try:
        chapter_path, inserted = ensure_manifest_figure_embed(book_root, new_row)
    except SystemExit:
        rollback_manifest(book_root, original_text)
        remove_rendered_png_if_present(new_row)
        raise

    print(f"Registered {figure_id} -> {new_row['png_path']}")
    print(
        f"{'Embedded' if inserted else 'Embed already present for'} {figure_id} -> {display_path(chapter_path)}"
    )

    if sync_obsidian:
        obsidian_dest = obsidian_dest_arg.expanduser() if obsidian_dest_arg else default_obsidian_dest(book_root)
        try:
            sync_book_to_obsidian(obsidian_dest, book_root)
        except SystemExit as exc:
            raise SystemExit(
                "Repo completion succeeded (manifest + PNG + chapter embed), bet Obsidian sync nepavyko. "
                f"{exc}"
            ) from exc
        print(f"Synced Obsidian vault -> {obsidian_dest}")
    else:
        print(
            "Repo completion succeeded (manifest + PNG + chapter embed). "
            f"Obsidian matomumui dar paleiskite sync: scripts/sync_obsidian_book.sh --book-root {display_path(book_root)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
