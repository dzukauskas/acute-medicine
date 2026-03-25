#!/usr/bin/env python3
from __future__ import annotations

import csv
import importlib
import os
import re
import sys
import tomllib
from pathlib import Path
from typing import Iterable

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
BOOK_ROOT_ENV_VAR = "MEDBOOK_ROOT"
REPO_CONFIG_PATH = REPO_ROOT / "repo_config.toml"

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
LOCALIZATION_SIGNAL_MATCH_MODES = {"literal", "regex"}
CLINICAL_POLICY_MARKER_MATCH_MODES = {"literal", "regex"}

SOURCE_TERM_TO_CONTEXT = {
    "uk": "uk-specific",
    "australia": "australia-specific",
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


def first_pdf_path(book_root: Path) -> Path | None:
    pdf_dir = book_root / "source" / "pdf"
    if not pdf_dir.exists():
        return None
    pdfs = sorted(path for path in pdf_dir.glob("*.pdf") if path.is_file())
    return pdfs[0] if pdfs else None


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
        "subsections": clean_inventory_items(bullet_items(find_section_lines(sections, "PDF inventorius", "Poskyriai"))),
        "tables": clean_inventory_items(bullet_items(find_section_lines(sections, "PDF inventorius", "Lentelės"))),
        "figures": clean_inventory_items(
            bullet_items(find_section_lines(sections, "PDF inventorius", "Paveikslai / schemos / algoritmai"))
        ),
        "boxes": clean_inventory_items(
            bullet_items(find_section_lines(sections, "PDF inventorius", "Rėmeliai / papildomi blokai"))
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


def load_localization_overrides(path: Path) -> list[dict[str, str]]:
    return [normalize_localization_override_row(row) for row in read_tsv(path)]


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


def localization_signal_registry_paths(book_root: str | Path | None = None) -> list[Path]:
    active_book_root = require_book_root(book_root)
    return [
        active_book_root / "localization_signals.base.tsv",
        active_book_root / "localization_signals.tsv",
    ]


def load_localization_signal_specs(book_root: str | Path | None = None) -> list[dict[str, str]]:
    rows_by_term: dict[str, dict[str, str]] = {}
    order: list[str] = []
    for path in localization_signal_registry_paths(book_root):
        if not path.exists():
            if path.name == "localization_signals.base.tsv":
                raise SystemExit(f"Nerastas localization signal registry failas: {path}")
            continue
        for row in read_tsv(path):
            normalized = normalize_localization_signal_row(row)
            source_term = normalized.get("source_term", "")
            if not source_term:
                continue
            key = normalize_key(source_term)
            if key not in order:
                order.append(key)
            rows_by_term[key] = normalized
    return [rows_by_term[key] for key in order if key in rows_by_term]


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
    topic = row.get("topic", "").strip()
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
    active_book_root = require_book_root(book_root)
    marker_path = active_book_root / "clinical_policy_markers.tsv"
    if not marker_path.exists():
        raise SystemExit(f"Nerastas clinical policy marker failas: {marker_path}")
    return [normalize_clinical_policy_marker_row(row) for row in read_tsv(marker_path) if row.get("topic", "").strip()]


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
                "topic": row.get("tema", "") or row.get("topic", ""),
                "source": row.get("šaltinis", "") or row.get("saltinis", "") or row.get("source", ""),
                "jurisdiction": row.get("jurisdikcija", "") or row.get("jurisdiction", ""),
                "date": row.get("data_versija", "") or row.get("date_version", ""),
                "notes": row.get("pastaba", "") or row.get("notes", ""),
            }
            for row in source_rows
            if row.get("tema", "") or row.get("topic", "")
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
