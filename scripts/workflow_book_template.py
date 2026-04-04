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
BOOK_METADATA_NAME = "book_metadata.yaml"
TEMPLATE_MANIFEST_NAME = "template_manifest.json"
TOKEN_RE = re.compile(r"{{([A-Z0-9_]+)}}")
ALLOWED_SOURCE_KINDS = {"pdf", "epub"}


@dataclass(frozen=True)
class CanonicalSource:
    kind: str
    name: str


def load_template_manifest(template_root: Path = TEMPLATE_ROOT) -> dict[str, list[str]]:
    template_manifest = template_root / TEMPLATE_MANIFEST_NAME
    if not template_manifest.exists():
        raise FileNotFoundError(f"Nerastas template manifest: {template_manifest}")
    data = json.loads(template_manifest.read_text(encoding="utf-8"))
    return {key: list(value) for key, value in data.items()}


def allowed_template_files(manifest: dict[str, list[str]]) -> set[str]:
    manifest_files = set(manifest.get("always_refresh", [])) | set(manifest.get("refresh_if_empty", []))
    required_dirs = set(manifest.get("required_directories", []))
    return manifest_files | {TEMPLATE_MANIFEST_NAME} | {f"{rel_dir}/.gitkeep" for rel_dir in required_dirs}


def required_manifest_files(manifest: dict[str, list[str]]) -> set[str]:
    return set(manifest.get("always_refresh", [])) | set(manifest.get("refresh_if_empty", [])) | {
        TEMPLATE_MANIFEST_NAME
    }


def template_files_on_disk(template_root: Path) -> set[str]:
    if not template_root.exists():
        raise FileNotFoundError(f"Nerastas shared template katalogas: {template_root}")
    return {
        path.relative_to(template_root).as_posix()
        for path in template_root.rglob("*")
        if path.is_file()
    }


def unexpected_template_files(
    template_root: Path,
    manifest: dict[str, list[str]],
) -> list[str]:
    return sorted(template_files_on_disk(template_root) - allowed_template_files(manifest))


def missing_template_files(
    template_root: Path,
    manifest: dict[str, list[str]],
) -> list[str]:
    return sorted(required_manifest_files(manifest) - template_files_on_disk(template_root))


def validated_template_files_to_copy(
    template_root: Path,
    manifest: dict[str, list[str]],
) -> list[str]:
    disk_files = template_files_on_disk(template_root)
    allowed_files = allowed_template_files(manifest)
    missing = sorted(required_manifest_files(manifest) - disk_files)
    unexpected = sorted(disk_files - allowed_files)
    if missing or unexpected:
        validation_problems: list[str] = []
        if missing:
            validation_problems.append(f"Missing manifest-managed template files: {', '.join(missing)}")
        if unexpected:
            validation_problems.append(
                "Unexpected template files not covered by template_manifest.json: "
                f"{', '.join(unexpected)}"
            )
        raise ValueError("Template root failed validation. " + " ".join(validation_problems))
    return sorted(rel_path for rel_path in disk_files if rel_path in allowed_files and rel_path != TEMPLATE_MANIFEST_NAME)


def copy_template_tree(
    book_root: Path,
    *,
    template_root: Path = TEMPLATE_ROOT,
    manifest: dict[str, list[str]] | None = None,
) -> None:
    manifest = load_template_manifest(template_root) if manifest is None else manifest
    files_to_copy = validated_template_files_to_copy(template_root, manifest)
    book_root.mkdir(parents=True, exist_ok=False)
    for rel_path in files_to_copy:
        source_path = template_root / rel_path
        target_path = book_root / rel_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)


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
    *,
    book_title: str | None = None,
    repo_root: Path = REPO_ROOT,
) -> dict[str, str]:
    title = book_title.strip() if book_title is not None else book_title_from_readme(book_root)
    return {
        "BOOK_TITLE": title,
        "BOOK_SLUG": book_root.name,
        "BOOK_ROOT": book_root.relative_to(repo_root).as_posix(),
        "BOOK_SOURCE_KIND": canonical_source.kind,
        "BOOK_SOURCE_NAME": canonical_source.name,
        "BOOK_PDF_NAME": canonical_source.name if canonical_source.kind == "pdf" else "SOURCE.pdf",
        "OBSIDIAN_DEST": template_obsidian_dest_value(book_root),
    }


def bootstrap_template_workspace(
    book_root: Path,
    *,
    book_title: str,
    canonical_source: CanonicalSource,
    template_root: Path = TEMPLATE_ROOT,
    repo_root: Path = REPO_ROOT,
) -> None:
    manifest = load_template_manifest(template_root)
    copy_template_tree(book_root, template_root=template_root, manifest=manifest)
    materialize_required_directories(book_root, manifest)
    write_book_metadata(book_root, canonical_source)
    render_book_tree(
        book_root,
        context_for_book(
            book_root,
            canonical_source,
            book_title=book_title,
            repo_root=repo_root,
        ),
    )
