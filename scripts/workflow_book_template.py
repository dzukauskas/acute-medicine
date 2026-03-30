#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import yaml

from workflow_obsidian import book_title_from_readme
from workflow_runtime import REPO_ROOT


TEMPLATE_ROOT = REPO_ROOT / "books" / "_template"
TEMPLATE_MANIFEST = TEMPLATE_ROOT / "template_manifest.json"
BOOK_METADATA_NAME = "book_metadata.yaml"
TOKEN_RE = re.compile(r"{{([A-Z0-9_]+)}}")
ALLOWED_SOURCE_KINDS = {"pdf", "epub"}


@dataclass(frozen=True)
class CanonicalSource:
    kind: str
    name: str


def load_template_manifest() -> dict[str, list[str]]:
    if not TEMPLATE_MANIFEST.exists():
        raise FileNotFoundError(f"Nerastas template manifest: {TEMPLATE_MANIFEST}")
    data = json.loads(TEMPLATE_MANIFEST.read_text(encoding="utf-8"))
    return {key: list(value) for key, value in data.items()}


def copy_template_tree(book_root: Path, *, template_root: Path = TEMPLATE_ROOT) -> None:
    if not template_root.exists():
        raise FileNotFoundError(f"Nerastas shared template katalogas: {template_root}")
    shutil.copytree(template_root, book_root)
    internal_manifest = book_root / "template_manifest.json"
    if internal_manifest.exists():
        internal_manifest.unlink()


def materialize_required_directories(book_root: Path, manifest: dict[str, list[str]]) -> None:
    for rel_dir in manifest.get("required_directories", []):
        (book_root / rel_dir).mkdir(parents=True, exist_ok=True)


def render_template_text(template_path: Path, context: dict[str, str]) -> str:
    text = template_path.read_text(encoding="utf-8")
    return TOKEN_RE.sub(lambda match: context.get(match.group(1), match.group(0)), text)


def render_book_tree(book_root: Path, context: dict[str, str]) -> None:
    for path in sorted(book_root.rglob("*")):
        if not path.is_file() or path.name == ".gitkeep":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rendered = TOKEN_RE.sub(lambda match: context.get(match.group(1), match.group(0)), text)
        path.write_text(rendered, encoding="utf-8")


def template_obsidian_dest_value(book_root: Path) -> str:
    title = book_title_from_readme(book_root)
    return (Path("<configured-obsidian-vault>") / title).as_posix()


def canonical_source_path(book_root: Path) -> Path:
    return book_root / BOOK_METADATA_NAME


def validate_canonical_source(kind: str, name: str) -> CanonicalSource:
    normalized_kind = kind.strip().lower()
    normalized_name = name.strip()
    if normalized_kind not in ALLOWED_SOURCE_KINDS:
        raise ValueError(
            f"Neteisinga canonical source kind reikšmė: {kind!r}. "
            f"Leidžiamos reikšmės: {sorted(ALLOWED_SOURCE_KINDS)}"
        )
    if not normalized_name:
        raise ValueError("Canonical source name negali būti tuščias.")
    return CanonicalSource(kind=normalized_kind, name=normalized_name)


def write_book_metadata(book_root: Path, canonical_source: CanonicalSource) -> Path:
    path = canonical_source_path(book_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "canonical_source": {
            "kind": canonical_source.kind,
            "name": canonical_source.name,
        }
    }
    path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )
    return path


def load_book_metadata(book_root: Path) -> CanonicalSource:
    path = canonical_source_path(book_root)
    if not path.exists():
        raise FileNotFoundError(f"Nerastas book metadata failas: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    canonical_source = data.get("canonical_source")
    if not isinstance(canonical_source, dict):
        raise ValueError(f"Book metadata faile {path} trūksta `canonical_source` objekto.")
    kind = str(canonical_source.get("kind", ""))
    name = str(canonical_source.get("name", ""))
    return validate_canonical_source(kind, name)


def context_for_book(
    book_root: Path,
    canonical_source: CanonicalSource,
) -> dict[str, str]:
    title = book_title_from_readme(book_root)
    return {
        "BOOK_TITLE": title,
        "BOOK_SLUG": book_root.name,
        "BOOK_ROOT": book_root.relative_to(REPO_ROOT).as_posix(),
        "BOOK_SOURCE_KIND": canonical_source.kind,
        "BOOK_SOURCE_NAME": canonical_source.name,
        "BOOK_PDF_NAME": canonical_source.name if canonical_source.kind == "pdf" else "SOURCE.pdf",
        "OBSIDIAN_DEST": template_obsidian_dest_value(book_root),
    }
