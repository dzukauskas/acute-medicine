#!/usr/bin/env python3
from __future__ import annotations

import csv
import os
import re
import tempfile
from pathlib import Path
from typing import Callable, Iterable

from workflow_runtime import REPO_ROOT


BOOK_ROOT_ENV_VAR = "MEDBOOK_ROOT"
SHARED_ROOT = REPO_ROOT / "shared"
SHARED_EXAMPLES_DIR = SHARED_ROOT / "examples"
SHARED_GOLD_SECTIONS_DIR = SHARED_EXAMPLES_DIR / "gold_sections"

BOOK_LOCAL_OVERRIDE_FILENAMES = {
    "termbase": "termbase.local.tsv",
    "acronyms": "acronyms.local.tsv",
    "gold_phrases": "gold_phrases.local.tsv",
    "calque_patterns": "calque_patterns.local.tsv",
    "disallowed_terms": "disallowed_terms.local.tsv",
    "disallowed_phrases": "disallowed_phrases.local.tsv",
    "localization_overrides": "localization_overrides.local.tsv",
    "localization_signals": "localization_signals.local.tsv",
    "adjudication_profiles": "adjudication_profiles.local.tsv",
}

TERM_CANDIDATE_FIELDS = [
    "candidate_id",
    "candidate_kind",
    "source_term",
    "source_expansion",
    "chapter_slug",
    "source_context",
    "proposed_lt",
    "status",
    "scope",
    "candidate_origin",
    "reason",
    "banned_lt",
    "source_ref",
    "notes",
]

MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
INLINE_CODE_RE = re.compile(r"`([^`]*)`")


def resolve_repo_path(raw: str | Path) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path.resolve()


def resolve_book_root(raw: str | Path | None = None, *, required: bool = False) -> Path | None:
    candidate: str | Path | None = raw
    if candidate is None:
        env_value = os.environ.get(BOOK_ROOT_ENV_VAR, "").strip()
        candidate = env_value or None
    if candidate is None:
        if required:
            raise SystemExit(
                "Šiam skriptui reikia aiškios knygos darbo vietos. "
                f"Nustatykite {BOOK_ROOT_ENV_VAR}=books/<slug> arba perduokite --book-root."
            )
        return None
    return resolve_repo_path(candidate)


def activate_book_root(raw: str | Path | None) -> None:
    if raw is None:
        return
    os.environ[BOOK_ROOT_ENV_VAR] = str(raw)


def require_book_root(raw: str | Path | None = None) -> Path:
    return resolve_book_root(raw, required=True)


def optional_book_root(raw: str | Path | None = None) -> Path | None:
    return resolve_book_root(raw, required=False)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows: list[dict[str, str]] = []
        for row in reader:
            normalized_row: dict[str, str] = {}
            for key, value in row.items():
                if isinstance(value, list):
                    normalized_row[key] = " | ".join(part.strip() for part in value if part and part.strip())
                else:
                    normalized_row[key] = (value or "").strip()
            rows.append(normalized_row)
        return rows


def write_tsv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_fd, temp_path_raw = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temp_path = Path(temp_path_raw)
    try:
        with os.fdopen(temp_fd, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
            writer.writeheader()
            for row in rows:
                writer.writerow({field: row.get(field, "") for field in fieldnames})
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def split_multi(value: str) -> list[str]:
    if not value.strip():
        return []
    return [item.strip() for item in re.split(r"[|,;]", value) if item.strip()]


def join_multi(values: Iterable[str]) -> str:
    return " | ".join(value.strip() for value in values if value and value.strip())


def strip_markdown(text: str) -> str:
    text = INLINE_CODE_RE.sub(r"\1", text)
    text = MARKDOWN_LINK_RE.sub(r"\1", text)
    return text


def normalize_key(text: str) -> str:
    text = strip_markdown(text)
    text = text.replace("\xa0", " ").lower()
    text = re.sub(r"[_/]+", " ", text)
    text = re.sub(r"[^a-z0-9ąčęėįšųūž\- ]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def slugify(text: str) -> str:
    text = normalize_key(text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def shared_rule_path(*parts: str) -> Path:
    return SHARED_ROOT.joinpath(*parts)


def book_local_override_path(kind: str, book_root: str | Path | None = None) -> Path | None:
    filename = BOOK_LOCAL_OVERRIDE_FILENAMES.get(kind)
    if not filename:
        raise KeyError(f"Nežinomas local override tipas: {kind}")
    active_book_root = optional_book_root(book_root)
    if active_book_root is None:
        return None
    return active_book_root / filename


def termbase_paths(book_root: str | Path | None = None) -> list[Path]:
    paths: list[Path] = [shared_rule_path("lexicon", "termbase.tsv")]
    local_path = book_local_override_path("termbase", book_root)
    if local_path is not None:
        paths.append(local_path)
    return paths


def acronym_paths(book_root: str | Path | None = None) -> list[Path]:
    paths: list[Path] = [shared_rule_path("lexicon", "acronyms.tsv")]
    local_path = book_local_override_path("acronyms", book_root)
    if local_path is not None:
        paths.append(local_path)
    return paths


def gold_phrase_paths(book_root: str | Path | None = None) -> list[Path]:
    paths: list[Path] = [shared_rule_path("prose", "gold_phrases.tsv")]
    local_path = book_local_override_path("gold_phrases", book_root)
    if local_path is not None:
        paths.append(local_path)
    return paths


def calque_pattern_paths(book_root: str | Path | None = None) -> list[Path]:
    paths: list[Path] = [shared_rule_path("prose", "calque_patterns.tsv")]
    local_path = book_local_override_path("calque_patterns", book_root)
    if local_path is not None:
        paths.append(local_path)
    return paths


def disallowed_term_paths(book_root: str | Path | None = None) -> list[Path]:
    paths: list[Path] = [shared_rule_path("prose", "disallowed_terms.tsv")]
    local_path = book_local_override_path("disallowed_terms", book_root)
    if local_path is not None:
        paths.append(local_path)
    return paths


def disallowed_phrase_paths(book_root: str | Path | None = None) -> list[Path]:
    paths: list[Path] = [shared_rule_path("prose", "disallowed_phrases.tsv")]
    local_path = book_local_override_path("disallowed_phrases", book_root)
    if local_path is not None:
        paths.append(local_path)
    return paths


def localization_override_paths(book_root: str | Path | None = None) -> list[Path]:
    paths: list[Path] = [shared_rule_path("localization", "localization_overrides.tsv")]
    local_path = book_local_override_path("localization_overrides", book_root)
    if local_path is not None:
        paths.append(local_path)
    return paths


def localization_signal_registry_paths(book_root: str | Path | None = None) -> list[Path]:
    paths: list[Path] = [shared_rule_path("localization", "localization_signals.base.tsv")]
    local_path = book_local_override_path("localization_signals", book_root)
    if local_path is not None:
        paths.append(local_path)
    return paths


def adjudication_profile_paths(book_root: str | Path | None = None) -> list[Path]:
    paths: list[Path] = [shared_rule_path("review", "adjudication_profiles.tsv")]
    local_path = book_local_override_path("adjudication_profiles", book_root)
    if local_path is not None:
        paths.append(local_path)
    return paths


def review_taxonomy_path() -> Path:
    return shared_rule_path("review", "review_taxonomy.tsv")


def clinical_policy_markers_path() -> Path:
    return shared_rule_path("localization", "clinical_policy_markers.tsv")


def lt_source_map_path() -> Path:
    return shared_rule_path("localization", "lt_source_map.tsv")


def shared_gold_sections_dir() -> Path:
    return SHARED_GOLD_SECTIONS_DIR


def local_gold_sections_dir(book_root: str | Path | None = None) -> Path | None:
    active_book_root = optional_book_root(book_root)
    if active_book_root is None:
        return None
    return active_book_root / "gold_sections"


def gold_section_index_sources(book_root: str | Path | None = None) -> list[tuple[Path, Path]]:
    sources: list[tuple[Path, Path]] = [(shared_gold_sections_dir() / "index.tsv", shared_gold_sections_dir())]
    local_dir = local_gold_sections_dir(book_root)
    if local_dir is not None:
        sources.append((local_dir / "index.tsv", local_dir))
    return sources


def require_tsv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"Nerastas TSV failas: {path}")
    return read_tsv(path)


def optional_tsv_rows(path: Path | None) -> list[dict[str, str]]:
    if path is None or not path.exists():
        return []
    return read_tsv(path)


def normalize_tsv_row(row: dict[str, str]) -> dict[str, str]:
    return {key: (value or "").strip() for key, value in row.items()}


def normalize_rule_key(value: str) -> str:
    return normalize_key(value)


def normalize_row_signature(row: dict[str, str]) -> str:
    return "\u241f".join(f"{key}={normalize_key(value)}" for key, value in row.items())


def merge_keyed_rows(
    paths: Iterable[Path | None],
    key_field: str,
    *,
    row_normalizer: Callable[[dict[str, str]], dict[str, str]] | None = None,
    key_normalizer: Callable[[str], str] = normalize_rule_key,
) -> list[dict[str, str]]:
    rows_by_key: dict[str, dict[str, str]] = {}
    order: list[str] = []

    for index, path in enumerate(paths):
        rows = require_tsv_rows(path) if index == 0 and path is not None else optional_tsv_rows(path)
        for raw_row in rows:
            row = row_normalizer(raw_row) if row_normalizer else normalize_tsv_row(raw_row)
            key_value = row.get(key_field, "").strip()
            if not key_value:
                continue
            key = key_normalizer(key_value)
            if not key:
                continue
            if key not in order:
                order.append(key)
            rows_by_key[key] = row

    return [rows_by_key[key] for key in order if key in rows_by_key]


def merge_appended_rows(
    paths: Iterable[Path | None],
    *,
    row_normalizer: Callable[[dict[str, str]], dict[str, str]] | None = None,
    row_identity: Callable[[dict[str, str]], str] = normalize_row_signature,
) -> list[dict[str, str]]:
    merged_rows: list[dict[str, str]] = []
    seen: set[str] = set()

    for index, path in enumerate(paths):
        rows = require_tsv_rows(path) if index == 0 and path is not None else optional_tsv_rows(path)
        for raw_row in rows:
            row = row_normalizer(raw_row) if row_normalizer else normalize_tsv_row(raw_row)
            identity = row_identity(row)
            if not identity or identity in seen:
                continue
            seen.add(identity)
            merged_rows.append(row)

    return merged_rows


def resolve_indexed_text_path(source_root: Path, index_path: Path, relative_path: str) -> Path | None:
    raw_path = relative_path.strip()
    if not raw_path:
        return None
    candidates = [
        source_root / raw_path,
        index_path.parent / raw_path,
        REPO_ROOT / raw_path,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def term_candidates_path(book_root: str | Path | None = None) -> Path:
    return require_book_root(book_root) / "term_candidates.tsv"
