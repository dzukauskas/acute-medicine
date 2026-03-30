#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from workflow_book import load_yaml
from workflow_rules import normalize_key, strip_markdown


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
CALLOUT_RE = re.compile(r"^>\s*\[![^\]]+\]\s*Originalo kontekstas\b", re.IGNORECASE)
CODE_FENCE_RE = re.compile(r"^```")
REGISTERED_BRAND_RE = re.compile(r"\b[A-Z][A-Za-z0-9-]*®\b")
GEOGRAPHY_PATTERNS = (
    (re.compile(r"\bAustral(?:ija|ijos|ijoje)\b", re.IGNORECASE), "Australija"),
    (re.compile(r"\bAnglij(?:a|os|oje)\b", re.IGNORECASE), "Anglija"),
    (re.compile(r"\bJungtin(?:ė|es)\s+Karalyst(?:ė|ės|ėje)\b", re.IGNORECASE), "Jungtinė Karalystė"),
    (re.compile(r"\bJK\b", re.IGNORECASE), "JK"),
    (re.compile(r"\bUK\b", re.IGNORECASE), "UK"),
    (re.compile(r"\bJAV\b", re.IGNORECASE), "JAV"),
    (re.compile(r"\bUSA\b", re.IGNORECASE), "USA"),
    (re.compile(r"\bU\.?S\.?A?\.?\b", re.IGNORECASE), "US"),
    (
        re.compile(r"\bJungtin(?:ės|ių)\s+Amerikos\s+Valstij(?:os|ų|ose)\b", re.IGNORECASE),
        "Jungtinės Amerikos Valstijos",
    ),
    (re.compile(r"\bAmerik(?:a|os|oje)\b", re.IGNORECASE), "Amerika"),
)
IGNORED_SECTION_TITLES = {
    "literatūra",
    "papildoma literatūra",
    "tolimesni šaltiniai",
    "references",
    "further reading",
}
RESTRICTED_ACTIONS = {"genericize", "omit_nontransferable", "original_context_callout"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Guard LT/EU-first localization policy in the drafted chapter.")
    parser.add_argument("chapter_md", help="Path to the Lithuanian chapter markdown file.")
    parser.add_argument("--chapter-pack", required=True, help="Path to the fresh chapter pack YAML.")
    return parser.parse_args()


def term_pattern(term: str) -> re.Pattern[str]:
    escaped = re.escape(term)
    return re.compile(rf"(?<!\w){escaped}(?!\w)", re.IGNORECASE)


def collect_restricted_terms(pack: dict) -> list[tuple[str, re.Pattern[str]]]:
    values: set[str] = set()

    for block in pack.get("blocks", []):
        if (block.get("localization_action") or "").strip() not in RESTRICTED_ACTIONS:
            continue
        for term in block.get("matched_localization_terms", []):
            cleaned = str(term).strip()
            if cleaned:
                values.add(cleaned)

    for row in pack.get("localization_decisions", []):
        action = (row.get("replacement_mode") or "").strip()
        source_term = (row.get("source_term") or "").strip()
        if source_term and action in RESTRICTED_ACTIONS:
            values.add(source_term)

    for row in pack.get("localization_overrides", []):
        action = (row.get("replacement_mode") or "").strip()
        source_term = (row.get("source_term") or "").strip()
        if source_term and action in RESTRICTED_ACTIONS:
            values.add(source_term)

    return [(term, term_pattern(term)) for term in sorted(values)]


def localization_errors(chapter_path: Path, pack: dict) -> list[str]:
    lines = chapter_path.read_text(encoding="utf-8").splitlines()
    term_patterns = collect_restricted_terms(pack)
    errors: list[str] = []

    in_code_fence = False
    in_callout = False
    section_mode: tuple[str, int] | None = None

    for idx, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\n")
        if CODE_FENCE_RE.match(line.strip()):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            title_norm = normalize_key(title)

            if section_mode and level <= section_mode[1]:
                section_mode = None

            if "originalo kontekstas" in title_norm:
                section_mode = ("callout", level)
            elif title_norm in IGNORED_SECTION_TITLES:
                section_mode = ("ignored", level)

            in_callout = section_mode is not None and section_mode[0] == "callout"
            continue

        if CALLOUT_RE.match(line.strip()):
            in_callout = True
            continue
        if in_callout and line.strip().startswith(">"):
            continue
        if in_callout and not line.strip().startswith(">"):
            in_callout = False

        if section_mode and section_mode[0] == "ignored":
            continue
        if in_callout or (section_mode and section_mode[0] == "callout"):
            continue

        visible = strip_markdown(line)
        if not visible.strip():
            continue

        for pattern, label in GEOGRAPHY_PATTERNS:
            if pattern.search(visible):
                errors.append(
                    f"{chapter_path}:{idx}: UK/Australia/US geografinis kontekstas `{label}` paliktas pagrindiniame LT tekste. "
                    "Perkelkite į `Originalo kontekstas` bloką arba pašalinkite."
                )

        for term, pattern in term_patterns:
            if pattern.search(visible):
                errors.append(
                    f"{chapter_path}:{idx}: originalo signalas `{term}` paliktas pagrindiniame LT tekste. "
                    "Tokie terminai leidžiami tik `Originalo kontekstas` bloke."
                )

        if REGISTERED_BRAND_RE.search(visible):
            errors.append(
                f"{chapter_path}:{idx}: rastas rinkai specifinis prekinis pavadinimas su `®`. "
                "Pagrindiniame LT tekste naudokite INN / bendrinį pavadinimą arba perkelkite į `Originalo kontekstas`."
            )

    return errors


def main() -> int:
    args = parse_args()
    chapter_path = Path(args.chapter_md)
    pack = load_yaml(Path(args.chapter_pack))
    errors = localization_errors(chapter_path, pack)
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Localization guard passed for {chapter_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
