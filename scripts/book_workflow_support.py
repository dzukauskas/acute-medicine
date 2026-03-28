#!/usr/bin/env python3
from __future__ import annotations

import csv
import importlib
import os
import re
import sys
import tomllib
from pathlib import Path
from typing import Callable, Iterable

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
BOOK_ROOT_ENV_VAR = "MEDBOOK_ROOT"
REPO_CONFIG_PATH = REPO_ROOT / "repo_config.toml"
SHARED_ROOT = REPO_ROOT / "shared"
SHARED_LEXICON_DIR = SHARED_ROOT / "lexicon"
SHARED_PROSE_DIR = SHARED_ROOT / "prose"
SHARED_LOCALIZATION_DIR = SHARED_ROOT / "localization"
SHARED_REVIEW_DIR = SHARED_ROOT / "review"
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
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
INVENTORY_PLACEHOLDER_RE = re.compile(r"^kol kas neužfiksuota$", re.IGNORECASE)
GENERATED_ARTIFACT_RE = re.compile(
    r"^(Sukurtas lietuviškas|Kanoninis šaltinis|Whimsical URL|Įrašyta į)\b",
    re.IGNORECASE,
)
STRUCTURED_SOURCE_HEADING_RE = re.compile(
    r"^(?P<kind>Table|Figure|Box|Chart)\s+"
    r"(?P<label>[0-9.]+)"
    r"(?:\s*[\u2000-\u200B]+\s*|\s{2,}|\s+)"
    r"(?P<title>.+?)\s*$"
)
TABLE_ROW_RE = re.compile(r"^\|.*\|$")
MARKDOWN_TABLE_SEPARATOR_RE = re.compile(r"^:?-{3,}:?$")

LOCALIZATION_REPLACEMENT_MODES = {
    "replace_lt",
    "replace_eu",
    "genericize",
    "original_context_callout",
    "omit_nontransferable",
}
CLINICAL_CLAIM_TYPES = {
    "dose",
    "indication",
    "contraindication",
    "route",
    "concentration",
    "algorithm_step",
    "monitoring",
    "legal_scope",
    "market_availability",
}
CLAIM_FINAL_RENDERINGS = {
    "keep_lt_normative",
    "keep_eu_normative",
    "original_context_callout",
    "omit",
}
STRUCTURED_BLOCK_STRATEGIES = {
    "rewrite_lt",
    "compress_lt",
    "recreate_figure",
    "original_context_callout",
    "omit",
}
AUDIT_STATUSES = {"ok", "sutvarkyta", "eskaluoti"}
MANUAL_AUDIT_AREAS = (
    "terminija",
    "kolokacijos",
    "gramatika",
    "semantika",
    "norminė logika",
    "atviros abejonės",
)
STRUCTURED_ALGORITHM_KEYWORDS = {"algorithm", "approach", "management"}
CLINICAL_CLAIM_TYPE_ALIASES = {
    "market availability": "market_availability",
    "market_availability": "market_availability",
    "legal scope": "legal_scope",
    "legal_scope": "legal_scope",
    "algorithm step": "algorithm_step",
    "algorithm_step": "algorithm_step",
}
LOCALIZATION_SIGNAL_MATCH_MODES = {"literal", "regex"}
CLINICAL_POLICY_MARKER_MATCH_MODES = {"literal", "regex"}

SOURCE_TERM_TO_CONTEXT = {
    "uk": "uk-specific",
    "australia": "australia-specific",
    "us": "us-specific",
    "mixed": "mixed-anglosphere",
    "mixed-anglosphere": "mixed-anglosphere",
    "market-specific": "mixed-anglosphere",
    "universal": "universal",
}
IGNORED_SOURCE_POLICY_SECTIONS = {"references", "further reading"}


def resolve_repo_path(raw: str | Path) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path.resolve()


def resolve_runtime_path(raw: str | Path, *, base_dir: str | Path | None = None) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        anchor = Path(base_dir).expanduser() if base_dir is not None else Path.cwd()
        path = anchor / path
    return path.resolve()


def path_is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def validate_obsidian_sync_destination(
    dest_dir: str | Path,
    book_root: str | Path,
    *,
    repo_root: str | Path = REPO_ROOT,
    cwd: str | Path | None = None,
) -> Path:
    resolved_dest = resolve_runtime_path(dest_dir, base_dir=cwd)
    resolved_repo_root = resolve_runtime_path(repo_root, base_dir=cwd)
    resolved_book_root = resolve_runtime_path(book_root, base_dir=cwd)
    resolved_lt_root = resolved_book_root / "lt"

    for forbidden_root in (resolved_repo_root, resolved_book_root, resolved_lt_root):
        if path_is_within(resolved_dest, forbidden_root):
            raise SystemExit(
                "Nesaugi Obsidian sync paskirtis: "
                f"{resolved_dest}\n"
                "Sync paskirtis negali būti repo viduje, knygos darbo vietoje arba `lt/` kataloge."
            )

    return resolved_dest


def ensure_python_module(module_name: str, package_name: str | None = None) -> None:
    try:
        importlib.import_module(module_name)
        return
    except ModuleNotFoundError:
        venv_python = REPO_ROOT / ".venv" / "bin" / "python"
        current_python = Path(sys.executable)
        if venv_python.exists() and current_python != venv_python:
            os.execv(str(venv_python), [str(venv_python), *sys.argv])
        package_hint = package_name or module_name
        raise SystemExit(
            f"Nerastas Python modulis `{module_name}`. "
            f"Įdiekite `{package_hint}` į aktyvią aplinką arba naudokite repo `.venv`."
        )


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


BOOK_ROOT = resolve_book_root()
SOURCE_CHAPTERS_DIR = BOOK_ROOT / "source" / "chapters-en" if BOOK_ROOT else None
LT_CHAPTERS_DIR = BOOK_ROOT / "lt" / "chapters" if BOOK_ROOT else None
RESEARCH_DIR = BOOK_ROOT / "research" if BOOK_ROOT else None
CHAPTER_PACKS_DIR = BOOK_ROOT / "chapter_packs" if BOOK_ROOT else None
ADJUDICATION_PACKS_DIR = BOOK_ROOT / "adjudication_packs" if BOOK_ROOT else None
GOLD_SECTIONS_DIR = BOOK_ROOT / "gold_sections" if BOOK_ROOT else None


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
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def split_multi(value: str) -> list[str]:
    if not value.strip():
        return []
    return [item.strip() for item in re.split(r"[|,;]", value) if item.strip()]


def join_multi(values: Iterable[str]) -> str:
    return " | ".join(value.strip() for value in values if value and value.strip())


def parse_bool(value: str, default: bool = False) -> bool:
    cleaned = (value or "").strip().lower()
    if not cleaned:
        return default
    return cleaned in {"1", "true", "yes", "y", "taip"}


def normalize_claim_type(value: str) -> str:
    cleaned = normalize_key(value).replace(" ", "_")
    cleaned = CLINICAL_CLAIM_TYPE_ALIASES.get(cleaned, cleaned)
    return cleaned if cleaned in CLINICAL_CLAIM_TYPES else ""


def normalize_claim_final_rendering(value: str) -> str:
    cleaned = normalize_key(value).replace(" ", "_")
    return cleaned if cleaned in CLAIM_FINAL_RENDERINGS else ""


def normalize_structured_block_strategy(value: str) -> str:
    cleaned = normalize_key(value).replace(" ", "_")
    return cleaned if cleaned in STRUCTURED_BLOCK_STRATEGIES else ""


def normalize_audit_status(value: str) -> str:
    cleaned = normalize_key(value)
    return cleaned if cleaned in AUDIT_STATUSES else ""


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


def require_book_root(raw: str | Path | None = None) -> Path:
    return resolve_book_root(raw, required=True)


def shared_rule_path(*parts: str) -> Path:
    return SHARED_ROOT.joinpath(*parts)


def optional_book_root(raw: str | Path | None = None) -> Path | None:
    return resolve_book_root(raw, required=False)


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


def load_toml(path: Path) -> dict[str, object]:
    with path.open("rb") as handle:
        data = tomllib.load(handle)
    return data or {}


def load_repo_config() -> dict[str, object]:
    if not REPO_CONFIG_PATH.exists():
        raise SystemExit(
            f"Nerastas repo config failas: {REPO_CONFIG_PATH}\n"
            "Sukurkite `repo_config.toml` pagal `repo_config.example.toml`."
        )
    return load_toml(REPO_CONFIG_PATH)


def obsidian_config() -> dict[str, str]:
    config = load_repo_config()
    raw_section = config.get("obsidian")
    if not isinstance(raw_section, dict):
        raise SystemExit(f"{REPO_CONFIG_PATH}: trūksta `[obsidian]` sekcijos.")
    section = {str(key): str(value).strip() for key, value in raw_section.items()}
    missing = [key for key in ("base_dir", "vault_name", "launch_agent_prefix") if not section.get(key, "")]
    if missing:
        raise SystemExit(
            f"{REPO_CONFIG_PATH}: `[obsidian]` sekcijoje trūksta laukų: {', '.join(missing)}."
        )
    return section


def obsidian_vault_root() -> Path:
    config = obsidian_config()
    return Path(config["base_dir"]).expanduser() / config["vault_name"]


def obsidian_dest_for_title(title: str) -> Path:
    return obsidian_vault_root() / title


def book_slug(book_root: Path) -> str:
    return book_root.name


def book_title_from_readme(book_root: Path) -> str:
    readme_path = book_root / "README.md"
    if readme_path.exists():
        for raw_line in readme_path.read_text(encoding="utf-8").splitlines():
            if raw_line.startswith("# "):
                title = raw_line[2:].strip()
                if title:
                    return title
    return book_root.name.replace("-", " ").title()


def default_obsidian_dest(book_root: Path) -> Path:
    return obsidian_dest_for_title(book_title_from_readme(book_root))


def obsidian_launch_agent_label(book_root: Path) -> str:
    return f"{obsidian_config()['launch_agent_prefix']}-{book_slug(book_root)}"


def repo_relative_path(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def first_pdf_path(book_root: Path) -> Path | None:
    pdf_dir = book_root / "source" / "pdf"
    if not pdf_dir.exists():
        return None
    pdfs = sorted(path for path in pdf_dir.glob("*.pdf") if path.is_file())
    return pdfs[0] if pdfs else None


def first_epub_path(book_root: Path) -> Path | None:
    epub_dir = book_root / "source" / "epub"
    if not epub_dir.exists():
        return None
    epubs = sorted(path for path in epub_dir.glob("*.epub") if path.is_file())
    return epubs[0] if epubs else None


def first_source_artifact(book_root: Path) -> tuple[str, Path] | None:
    pdf_path = first_pdf_path(book_root)
    if pdf_path is not None:
        return ("pdf", pdf_path)
    epub_path = first_epub_path(book_root)
    if epub_path is not None:
        return ("epub", epub_path)
    return None


def resolve_chapter_slug(raw: str, book_root: str | Path | None = None) -> str:
    candidate = raw.strip()
    source_chapters_dir = require_book_root(book_root) / "source" / "chapters-en"
    if re.fullmatch(r"\d{1,3}", candidate):
        prefix = f"{int(candidate):03d}-"
        matches = sorted(path.stem for path in source_chapters_dir.glob(f"{prefix}*.md"))
        if not matches:
            raise FileNotFoundError(f"Nerastas skyrius numeriu {candidate}.")
        return matches[0]
    if candidate.endswith(".md"):
        candidate = Path(candidate).stem
    return candidate


def chapter_paths_for_slug(slug: str, book_root: str | Path | None = None) -> dict[str, Path]:
    active_book_root = require_book_root(book_root)
    return {
        "source": active_book_root / "source" / "chapters-en" / f"{slug}.md",
        "lt": active_book_root / "lt" / "chapters" / f"{slug}.md",
        "research": active_book_root / "research" / f"{slug}.md",
        "pack": active_book_root / "chapter_packs" / f"{slug}.yaml",
    }


def term_candidates_path(book_root: str | Path | None = None) -> Path:
    return require_book_root(book_root) / "term_candidates.tsv"


def chapter_number_from_slug(slug: str) -> str:
    match = re.match(r"^(\d{3})-", slug)
    if not match:
        raise ValueError(f"Nepavyko išgauti skyriaus numerio iš slug {slug!r}.")
    return match.group(1)


def scope_allows(scope: str, chapter_number: str) -> bool:
    cleaned = (scope or "all").strip().lower()
    if not cleaned or cleaned == "all":
        return True
    allowed = {item.strip() for item in re.split(r"[|,; ]+", cleaned) if item.strip()}
    return chapter_number in allowed or chapter_number.lstrip("0") in allowed


def dump_yaml(path: Path, data: dict | list) -> None:
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data or {}


def parse_markdown_sections(text: str) -> dict[tuple[str, ...], list[str]]:
    sections: dict[tuple[str, ...], list[str]] = {}
    stack: list[str] = []
    current_key: tuple[str, ...] | None = None
    for line in text.splitlines():
        heading_match = HEADING_RE.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            stack = stack[: level - 1]
            stack.append(title)
            current_key = tuple(stack)
            sections.setdefault(current_key, [])
            continue
        if current_key is not None:
            sections[current_key].append(line)
    return sections


def source_text_for_policy_checks(source_text: str) -> str:
    sections = parse_markdown_sections(source_text)
    if not sections:
        return source_text

    included_chunks: list[str] = []
    prefix_lines: list[str] = []
    for line in source_text.splitlines():
        if line.startswith("## "):
            break
        prefix_lines.append(line)
    included_chunks.append("\n".join(prefix_lines))

    for key, lines in sections.items():
        if normalize_key(key[-1]) in IGNORED_SOURCE_POLICY_SECTIONS:
            continue
        included_chunks.append("\n".join(lines))
    return "\n".join(chunk for chunk in included_chunks if chunk.strip())


def find_section_lines(sections: dict[tuple[str, ...], list[str]], *suffix: str) -> list[str]:
    for key, lines in sections.items():
        if len(key) >= len(suffix) and tuple(key[-len(suffix):]) == suffix:
            return lines
    return []


def find_section_lines_any(
    sections: dict[tuple[str, ...], list[str]],
    suffix_options: Iterable[tuple[str, ...]],
) -> list[str]:
    for suffix in suffix_options:
        lines = find_section_lines(sections, *suffix)
        if lines:
            return lines
    return []


def bullet_items(lines: Iterable[str]) -> list[str]:
    items: list[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line.startswith("- "):
            continue
        value = strip_markdown(line[2:].strip())
        if value:
            items.append(value)
    return items


def markdown_table_rows(lines: Iterable[str]) -> list[dict[str, str]]:
    table_lines = [line.strip() for line in lines if line.strip() and TABLE_ROW_RE.match(line.strip())]
    if len(table_lines) < 2:
        return []

    def split_row(line: str) -> list[str]:
        return [cell.strip() for cell in line.strip().strip("|").split("|")]

    header_cells = split_row(table_lines[0])
    separator_cells = split_row(table_lines[1])
    if not header_cells or len(separator_cells) < len(header_cells):
        return []
    if not all(MARKDOWN_TABLE_SEPARATOR_RE.match(cell.replace(" ", "")) for cell in separator_cells[: len(header_cells)]):
        return []

    headers = [normalize_key(cell).replace(" ", "_") for cell in header_cells]
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = split_row(line)
        if len(cells) < len(headers):
            cells.extend([""] * (len(headers) - len(cells)))
        row = {headers[idx]: cells[idx].strip() for idx in range(len(headers))}
        if any(value for value in row.values()):
            rows.append(row)
    return rows


def metadata_value(lines: Iterable[str], label: str) -> str:
    prefix = f"- {label}:"
    for raw_line in lines:
        line = raw_line.strip()
        if line.startswith(prefix):
            return strip_markdown(line[len(prefix):].strip())
    return ""


def parse_structured_label(text: str) -> tuple[str, str]:
    match = re.match(r"^(Table|Figure|Box|Chart)\s+([0-9.]+)\s+(.*)$", text)
    if not match:
        return "", ""
    return match.group(1).lower(), match.group(2)


def structured_block_type(kind: str, title: str) -> str:
    normalized_title = normalize_key(title)
    if kind == "table":
        return "table"
    if kind == "figure":
        if any(word in normalized_title for word in STRUCTURED_ALGORITHM_KEYWORDS):
            return "algorithm"
        return "figure_caption"
    if kind == "box":
        return "callout"
    if kind == "chart":
        return "chart"
    return "figure_caption"


def structured_block_id(kind: str, label: str, title: str) -> str:
    block_type = structured_block_type(kind, title)
    if label:
        return f"{block_type}-{label}-{slugify(title)}"
    return f"{block_type}-{slugify(title)}"


def structured_completion_hint(kind: str, label: str, title: str) -> str:
    if kind == "table":
        return f"{label} lentelė"
    if kind == "figure":
        return f"{label} paveikslas"
    if kind == "box":
        return f"{label} rėmelis"
    if kind == "chart" and "news2" in normalize_key(title):
        return "NEWS2 originalo kontekste"
    if kind == "chart":
        return f"{label} diagrama"
    return title


def clean_inventory_items(items: list[str]) -> list[str]:
    cleaned: list[str] = []
    for item in items:
        stripped = item.strip()
        if not stripped:
            continue
        if INVENTORY_PLACEHOLDER_RE.match(stripped):
            continue
        if GENERATED_ARTIFACT_RE.match(stripped):
            continue
        cleaned.append(stripped)
    return cleaned


def extract_inventory(sections: dict[tuple[str, ...], list[str]]) -> dict[str, list[str]]:
    return {
        "subsections": clean_inventory_items(
            bullet_items(
                find_section_lines_any(
                    sections,
                    (
                        ("Source inventorius", "Poskyriai"),
                        ("PDF inventorius", "Poskyriai"),
                    ),
                )
            )
        ),
        "tables": clean_inventory_items(
            bullet_items(
                find_section_lines_any(
                    sections,
                    (
                        ("Source inventorius", "Lentelės"),
                        ("PDF inventorius", "Lentelės"),
                    ),
                )
            )
        ),
        "figures": clean_inventory_items(
            bullet_items(
                find_section_lines_any(
                    sections,
                    (
                        ("Source inventorius", "Paveikslai / schemos / algoritmai"),
                        ("PDF inventorius", "Paveikslai / schemos / algoritmai"),
                    ),
                )
            )
        ),
        "boxes": clean_inventory_items(
            bullet_items(
                find_section_lines_any(
                    sections,
                    (
                        ("Source inventorius", "Rėmeliai / papildomi blokai"),
                        ("PDF inventorius", "Rėmeliai / papildomi blokai"),
                    ),
                )
            )
        ),
        "risky_terms": bullet_items(find_section_lines(sections, "Rizikingi terminai")),
        "language_risks": bullet_items(find_section_lines(sections, "Kalbinės rizikos vietos")),
        "anti_calque": bullet_items(find_section_lines(sections, "Anti-calque perrašymo pastabos")),
        "localization_decisions": bullet_items(find_section_lines(sections, "Lokalizacijos sprendimai")),
        "local_practice_changes": bullet_items(
            find_section_lines(sections, "Vietos, kur originalas pakeistas pagal Lietuvos praktiką")
        ),
    }


def extract_source_structured_items(source_text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for raw_line in source_text.splitlines():
        line = raw_line.strip()
        match = STRUCTURED_SOURCE_HEADING_RE.match(line)
        if not match:
            continue
        kind = match.group("kind").lower()
        label = match.group("label")
        key = (kind, label)
        if key in seen:
            continue
        seen.add(key)
        items.append(
            {
                "kind": kind,
                "label": label,
                "title": strip_markdown(match.group("title").strip()),
                "raw": line,
            }
        )
    return items


def term_matches(left: str, right: str) -> bool:
    left_norm = normalize_key(left)
    right_norm = normalize_key(right)
    if not left_norm or not right_norm:
        return False
    return left_norm == right_norm or left_norm in right_norm or right_norm in left_norm


def load_termbase_rows(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return merge_keyed_rows(termbase_paths(book_root), "en")


def load_acronym_rows(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return merge_keyed_rows(acronym_paths(book_root), "acronym")


def load_gold_phrase_rows(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return merge_appended_rows(gold_phrase_paths(book_root))


def load_calque_pattern_rows(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return merge_appended_rows(calque_pattern_paths(book_root))


def load_disallowed_term_rows(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return merge_appended_rows(disallowed_term_paths(book_root))


def load_disallowed_phrase_rows(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return merge_appended_rows(disallowed_phrase_paths(book_root))


def load_term_candidate_rows(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return optional_tsv_rows(term_candidates_path(book_root))


def normalize_localization_override_row(row: dict[str, str]) -> dict[str, str]:
    replacement_mode = row.get("replacement_mode", "").strip() or "replace_lt"
    if replacement_mode not in LOCALIZATION_REPLACEMENT_MODES:
        replacement_mode = "replace_lt"
    jurisdiction = row.get("jurisdiction", "").strip().lower() or "universal"
    return {
        "source_term": row.get("source_term", "").strip(),
        "jurisdiction": jurisdiction,
        "replacement_mode": replacement_mode,
        "local_lt": row.get("local_lt", "").strip(),
        "eu_fallback": row.get("eu_fallback", "").strip(),
        "scope": row.get("scope", "").strip() or "all",
        "reason": row.get("reason", "").strip(),
        "source_ref": row.get("source_ref", "").strip(),
        "notes": row.get("notes", "").strip(),
    }


def load_localization_overrides(
    path: Path | None = None,
    *,
    book_root: str | Path | None = None,
) -> list[dict[str, str]]:
    if path is not None:
        return [normalize_localization_override_row(row) for row in require_tsv_rows(path)]
    return merge_keyed_rows(
        localization_override_paths(book_root),
        "source_term",
        row_normalizer=normalize_localization_override_row,
    )


def normalize_localization_signal_row(row: dict[str, str]) -> dict[str, str]:
    source_term = row.get("source_term", "").strip()
    match_mode = (row.get("match_mode", "") or "literal").strip().lower()
    if match_mode not in LOCALIZATION_SIGNAL_MATCH_MODES:
        match_mode = "literal"
    pattern = row.get("pattern", "").strip() or source_term
    return {
        "source_term": source_term,
        "jurisdiction": row.get("jurisdiction", "").strip().lower() or "universal",
        "signal_type": row.get("signal_type", "").strip() or "reference tool",
        "match_mode": match_mode,
        "pattern": pattern,
        "notes": row.get("notes", "").strip(),
    }


def load_localization_signal_specs(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return merge_keyed_rows(
        localization_signal_registry_paths(book_root),
        "source_term",
        row_normalizer=normalize_localization_signal_row,
    )


def localization_signal_matches(spec: dict[str, str], text: str) -> bool:
    if spec.get("match_mode", "literal") == "regex":
        return bool(re.search(spec.get("pattern", ""), text, flags=re.IGNORECASE))
    return normalize_key(spec.get("pattern", "")) in normalize_key(text)


def detect_source_localization_signals(source_text: str, book_root: str | Path | None = None) -> list[dict[str, str]]:
    content_text = source_text_for_policy_checks(source_text)
    signals: list[dict[str, str]] = []
    seen: set[str] = set()
    for spec in load_localization_signal_specs(book_root):
        if not localization_signal_matches(spec, content_text):
            continue
        key = normalize_key(spec["source_term"])
        if key in seen:
            continue
        seen.add(key)
        signals.append(
            {
                "source_term": spec["source_term"],
                "jurisdiction": spec["jurisdiction"],
                "signal_type": spec["signal_type"],
                "match_mode": spec["match_mode"],
                "pattern": spec["pattern"],
                "notes": spec["notes"],
            }
        )
    return signals


def normalize_clinical_policy_marker_row(row: dict[str, str]) -> dict[str, str]:
    topic = normalize_claim_type(row.get("topic", "").strip())
    match_mode = (row.get("match_mode", "") or "literal").strip().lower()
    if match_mode not in CLINICAL_POLICY_MARKER_MATCH_MODES:
        match_mode = "literal"
    pattern = row.get("pattern", "").strip() or topic
    return {
        "topic": topic,
        "match_mode": match_mode,
        "pattern": pattern,
        "notes": row.get("notes", "").strip(),
    }


def load_clinical_policy_markers(book_root: str | Path | None = None) -> list[dict[str, str]]:
    del book_root
    return [
        normalize_clinical_policy_marker_row(row)
        for row in require_tsv_rows(clinical_policy_markers_path())
        if row.get("topic", "").strip()
    ]


def load_lt_source_map(book_root: str | Path | None = None) -> list[dict[str, str]]:
    del book_root
    return require_tsv_rows(lt_source_map_path())


def load_review_taxonomy_rows() -> list[dict[str, str]]:
    return require_tsv_rows(review_taxonomy_path())


def load_adjudication_profile_rows(book_root: str | Path | None = None) -> list[dict[str, str]]:
    return merge_keyed_rows(adjudication_profile_paths(book_root), "profile_id")


def load_gold_section_examples(book_root: str | Path | None = None) -> list[dict[str, object]]:
    rows_by_id: dict[str, dict[str, object]] = {}
    order: list[str] = []

    for index, (index_path, source_root) in enumerate(gold_section_index_sources(book_root)):
        rows = require_tsv_rows(index_path) if index == 0 else optional_tsv_rows(index_path)
        for row in rows:
            example_id = row.get("example_id", "").strip()
            relative_path = row.get("path", "").strip()
            if not example_id or not relative_path:
                continue

            example_path = resolve_indexed_text_path(source_root, index_path, relative_path)
            if example_path is None:
                continue

            key = normalize_key(example_id)
            if key not in order:
                order.append(key)
            rows_by_key_row = {
                "kind": "section",
                "example_id": example_id,
                "source_chapter": row.get("source_chapter", "").strip(),
                "block_id": row.get("block_id", "").strip(),
                "block_type": row.get("block_type", "").strip(),
                "tags": split_multi(row.get("tags", "")),
                "text": example_path.read_text(encoding="utf-8").strip(),
                "notes": row.get("notes", "").strip(),
                "path": relative_path,
            }
            rows_by_id[key] = rows_by_key_row

    return [rows_by_id[key] for key in order if key in rows_by_id]


def clinical_policy_marker_matches(marker: dict[str, str], text: str) -> bool:
    if marker.get("match_mode", "literal") == "regex":
        return bool(re.search(marker.get("pattern", ""), text, flags=re.IGNORECASE))
    return normalize_key(marker.get("pattern", "")) in normalize_key(text)


def detect_clinical_policy_topics(source_text: str, book_root: str | Path | None = None) -> list[str]:
    content_text = source_text_for_policy_checks(source_text)
    topics: list[str] = []
    seen: set[str] = set()
    for marker in load_clinical_policy_markers(book_root):
        if not clinical_policy_marker_matches(marker, content_text):
            continue
        key = normalize_key(marker["topic"])
        if key in seen:
            continue
        seen.add(key)
        topics.append(marker["topic"])
    return topics


def source_has_clinical_normative_content(source_text: str, book_root: str | Path | None = None) -> bool:
    return bool(detect_clinical_policy_topics(source_text, book_root))


def extract_localization_research(sections: dict[tuple[str, ...], list[str]]) -> dict[str, object]:
    signal_rows = markdown_table_rows(find_section_lines(sections, "Jurisdikcijos ir rinkos signalai"))
    decision_rows = markdown_table_rows(find_section_lines(sections, "LT/EU pakeitimo sprendimai"))
    source_rows = markdown_table_rows(find_section_lines(sections, "Vaistų ir dozių LT/EU šaltinių bazė"))
    claim_rows = markdown_table_rows(find_section_lines(sections, "Norminių teiginių matrica"))
    structured_policy_rows = markdown_table_rows(find_section_lines(sections, "Struktūrinių blokų lokalizacijos sprendimai"))
    manual_audit_rows = markdown_table_rows(find_section_lines(sections, "Finalus agento auditas"))

    return {
        "signals": [
            {
                "source_term": row.get("signalas", "") or row.get("source_term", ""),
                "jurisdiction": (row.get("jurisdikcija", "") or row.get("jurisdiction", "")).strip().lower(),
                "signal_type": row.get("tipas", "") or row.get("signal_type", ""),
                "source_anchor": row.get("šaltinio_vieta", "") or row.get("saltinio_vieta", "") or row.get("source_anchor", ""),
                "notes": row.get("pastaba", "") or row.get("notes", ""),
            }
            for row in signal_rows
            if row.get("signalas", "") or row.get("source_term", "")
        ],
        "decisions": [
            {
                "source_term": row.get("signalas", "") or row.get("source_term", ""),
                "replacement_mode": row.get("veiksmas", "") or row.get("replacement_mode", ""),
                "authority_basis": row.get("autoritetas", "") or row.get("authority_basis", ""),
                "localization_note": row.get("lt_eu_sprendimas", "") or row.get("localization_note", ""),
                "source_ref": row.get("šaltinio_nuoroda", "") or row.get("saltinio_nuoroda", "") or row.get("source_ref", ""),
                "notes": row.get("pastaba", "") or row.get("notes", ""),
            }
            for row in decision_rows
            if row.get("signalas", "") or row.get("source_term", "")
        ],
        "authority_sources": [
            {
                "topic": normalize_claim_type(row.get("tema", "") or row.get("topic", "")),
                "source": row.get("šaltinis", "") or row.get("saltinis", "") or row.get("source", ""),
                "jurisdiction": row.get("jurisdikcija", "") or row.get("jurisdiction", ""),
                "date": row.get("data_versija", "") or row.get("date_version", ""),
                "notes": row.get("pastaba", "") or row.get("notes", ""),
            }
            for row in source_rows
            if row.get("tema", "") or row.get("topic", "")
        ],
        "claims": [
            {
                "claim_id": row.get("claim_id", "") or row.get("teiginio_id", ""),
                "claim_type": normalize_claim_type(row.get("claim_type", "") or row.get("teiginio_tipas", "")),
                "source_anchor": row.get("source_anchor", "") or row.get("šaltinio_vieta", "") or row.get("saltinio_vieta", ""),
                "final_rendering": normalize_claim_final_rendering(row.get("final_rendering", "") or row.get("galutinis_pateikimas", "")),
                "authority_basis": row.get("authority_basis", "") or row.get("autoritetas", ""),
                "primary_lt_source": row.get("primary_lt_source", "") or row.get("pagrindinis_lt_saltinis", "") or row.get("pagrindinis_lt_šaltinis", ""),
                "eu_fallback_source": row.get("eu_fallback_source", "") or row.get("eu_fallback_saltinis", "") or row.get("eu_fallback_šaltinis", ""),
                "lt_gap_reason": row.get("lt_gap_reason", "") or row.get("lt_spragos_priezastis", "") or row.get("lt_spragos_priežastis", ""),
                "note": row.get("note", "") or row.get("pastaba", ""),
            }
            for row in claim_rows
            if any(value.strip() for value in row.values())
        ],
        "structured_block_policies": [
            {
                "block_id": row.get("block_id", "") or row.get("bloko_id", ""),
                "block_type": row.get("block_type", "") or row.get("bloko_tipas", ""),
                "lt_strategy": normalize_structured_block_strategy(row.get("lt_strategy", "") or row.get("lt_strategija", "")),
                "authority_source": row.get("authority_source", "") or row.get("autoriteto_saltinis", "") or row.get("autoriteto_šaltinis", ""),
                "original_context_allowed": row.get("original_context_allowed", "") or row.get("originalo_kontekstas_leidziamas", "") or row.get("originalo_kontekstas_leidžiamas", ""),
                "note": row.get("note", "") or row.get("pastaba", ""),
            }
            for row in structured_policy_rows
            if any(value.strip() for value in row.values())
        ],
        "manual_audit": [
            {
                "area": normalize_key(row.get("sritis", "") or row.get("area", "")),
                "status": normalize_audit_status(row.get("statusas", "") or row.get("status", "")),
                "note": row.get("pastaba", "") or row.get("note", ""),
            }
            for row in manual_audit_rows
            if any(value.strip() for value in row.values())
        ],
        "nontransferable": bullet_items(find_section_lines(sections, "Neperkeliamas originalo turinys")),
    }


def extract_adjudication_decisions(sections: dict[tuple[str, ...], list[str]]) -> list[dict[str, str]]:
    decisions: list[dict[str, str]] = []
    for item in bullet_items(find_section_lines(sections, "Adjudication sprendimai")):
        parts = [part.strip() for part in item.split("|", 2)]
        block_id = parts[0] if len(parts) >= 1 else ""
        choice = parts[1] if len(parts) >= 2 else ""
        reason = parts[2] if len(parts) >= 3 else ""
        decisions.append({"block_id": block_id, "choice": choice, "reason": reason, "raw": item})
    return decisions


def normalize_authority_basis(value: str) -> str:
    cleaned = value.strip() or "LT"
    if cleaned in {"LT", "EU", "original-context-only"}:
        return cleaned
    return "LT"


def jurisdiction_to_pack_context(jurisdictions: Iterable[str]) -> str:
    normalized = {item.strip().lower() for item in jurisdictions if item and item.strip()}
    if not normalized:
        return "universal"
    if len(normalized) == 1:
        only = next(iter(normalized))
        return SOURCE_TERM_TO_CONTEXT.get(only, "mixed-anglosphere")
    return "mixed-anglosphere"


def normalize_yaml_structure(value: object) -> object:
    if isinstance(value, dict):
        return {key: normalize_yaml_structure(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [normalize_yaml_structure(item) for item in value]
    return value
