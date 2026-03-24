#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

from book_workflow_support import (
    BOOK_ROOT,
    MARKDOWN_LINK_RE,
    load_yaml,
    parse_bool,
    read_tsv,
    strip_markdown,
    split_multi,
)


Rule = dict[str, str]
TERMBASE_PATH = BOOK_ROOT / "termbase.tsv"
ACRONYMS_PATH = BOOK_ROOT / "acronyms.tsv"
LEGACY_RULE_PATHS = [
    BOOK_ROOT / "disallowed_terms.tsv",
    BOOK_ROOT / "disallowed_phrases.tsv",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Flag terminology, acronym, and heading-policy issues in LT translation files."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["books/acute-medicine/lt/chapters"],
        help="Files or directories to scan. Defaults to books/acute-medicine/lt/chapters.",
    )
    parser.add_argument(
        "--termbase",
        default=str(TERMBASE_PATH),
        help="Path to the active termbase TSV.",
    )
    parser.add_argument(
        "--acronyms",
        default=str(ACRONYMS_PATH),
        help="Path to the active acronym TSV.",
    )
    parser.add_argument(
        "--chapter-pack",
        help="Optional chapter pack YAML. If provided, only chapter-scoped active terms and acronyms are enforced.",
    )
    parser.add_argument(
        "--legacy-rules",
        nargs="*",
        default=[str(path) for path in LEGACY_RULE_PATHS if path.exists()],
        help="Optional legacy banned-term TSV files kept for compatibility.",
    )
    return parser.parse_args()


def build_legacy_pattern(rule: Rule) -> re.Pattern[str]:
    banned = rule["banned"]
    match_type = rule["match_type"]
    if match_type == "word":
        return re.compile(rf"(?i)\b{re.escape(banned)}\b")
    if match_type == "phrase":
        return re.compile(re.escape(banned), re.IGNORECASE)
    if match_type == "regex":
        return re.compile(banned, re.IGNORECASE)
    raise ValueError(f"Unsupported match_type={match_type!r} in {rule['rule_file']}")


def load_legacy_rules(paths: list[Path]) -> list[Rule]:
    rows: list[Rule] = []
    for path in paths:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for row in reader:
                rows.append(
                    {
                        "rule_file": path.name,
                        "match_type": row.get("match_type", "word").strip() or "word",
                        "banned": row["banned"].strip(),
                        "preferred": row["preferred"].strip(),
                        "reason": row["reason"].strip(),
                    }
                )
    return rows


def normalize_line_for_scan(line: str) -> str:
    normalized = strip_markdown(line)
    normalized = MARKDOWN_LINK_RE.sub("", normalized)
    return normalized


def has_relaxed_lt_expansion(prefix_text: str, lt_form: str) -> bool:
    exact_pattern = re.compile(re.escape(lt_form), re.IGNORECASE)
    if exact_pattern.search(prefix_text):
        return True
    tokens = re.findall(r"[A-Za-zĄČĘĖĮŠŲŪŽąčęėįšųūž]+", lt_form.lower())
    stems = [token[:3] for token in tokens if len(token) >= 4]
    if not stems:
        return False
    return all(re.search(re.escape(stem), prefix_text, re.IGNORECASE) for stem in stems)


def iter_markdown_files(raw_paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in raw_paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(p for p in path.rglob("*.md") if p.is_file()))
        elif path.is_file():
            files.append(path)
    return files


def add_finding(findings: list[str], file_path: Path, lineno: int, check: str, message: str, line: str) -> None:
    findings.append(
        f"{file_path}:{lineno}: check='{check}' message='{message}'\n"
        f"  {line.strip()}"
    )


def is_reference_bullet(line: str) -> bool:
    return bool(re.match(r"^\s*-\s*\[", line))


def active_terms(termbase_path: Path, chapter_pack_path: Path | None) -> list[dict]:
    if chapter_pack_path:
        pack = load_yaml(chapter_pack_path)
        return pack.get("active_terms", [])
    rows = read_tsv(termbase_path)
    return [
        {
            "en": row["en"],
            "lt": row["lt"],
            "status": row["status"],
            "banned_lt": split_multi(row.get("banned_lt", "")),
            "first_use_policy": row.get("first_use_policy", ""),
            "section_scope": row.get("section_scope", "all"),
            "local_override_tag": row.get("local_override_tag", ""),
            "example_lt": row.get("example_lt", ""),
        }
        for row in rows
    ]


def active_acronyms(acronyms_path: Path, chapter_pack_path: Path | None) -> list[dict]:
    if chapter_pack_path:
        pack = load_yaml(chapter_pack_path)
        return pack.get("active_acronyms", [])
    return read_tsv(acronyms_path)


def scan_legacy_rules(file_path: Path, text: str, rules: list[Rule]) -> list[str]:
    findings: list[str] = []
    for rule in rules:
        pattern = build_legacy_pattern(rule)
        for lineno, line in enumerate(text.splitlines(), start=1):
            if pattern.search(normalize_line_for_scan(line)):
                add_finding(
                    findings,
                    file_path,
                    lineno,
                    "legacy_rule",
                    f"banned='{rule['banned']}' preferred='{rule['preferred']}' reason='{rule['reason']}'",
                    line,
                )
    return findings


def build_variant_pattern(variant: str) -> re.Pattern[str]:
    escaped = re.escape(variant)
    if re.fullmatch(r"[\wĄČĘĖĮŠŲŪŽąčęėįšųūž-]+", variant):
        return re.compile(rf"(?i)\b{escaped}\b")
    return re.compile(escaped, re.IGNORECASE)


def scan_terms(file_path: Path, text: str, term_rows: list[dict]) -> list[str]:
    findings: list[str] = []
    for row in term_rows:
        for banned_variant in row.get("banned_lt", []):
            pattern = build_variant_pattern(banned_variant)
            for lineno, line in enumerate(text.splitlines(), start=1):
                if is_reference_bullet(line):
                    continue
                normalized = normalize_line_for_scan(line)
                if pattern.search(normalized):
                    add_finding(
                        findings,
                        file_path,
                        lineno,
                        "termbase_variant",
                        f"Venkite `{banned_variant}`; rinkitės `{row['lt']}`.",
                        line,
                    )
        heading_en_pattern = build_variant_pattern(row["en"])
        for lineno, line in enumerate(text.splitlines(), start=1):
            if not line.lstrip().startswith("#"):
                continue
            normalized = normalize_line_for_scan(line)
            if heading_en_pattern.search(normalized):
                add_finding(
                    findings,
                    file_path,
                    lineno,
                    "english_term_in_heading",
                    f"Antraštėje venkite EN termino `{row['en']}`; rinkitės LT formą `{row['lt']}`.",
                    line,
                )
    return findings


def scan_acronyms(file_path: Path, text: str, acronym_rows: list[dict]) -> list[str]:
    findings: list[str] = []
    cleaned_lines = [normalize_line_for_scan(line) for line in text.splitlines()]
    cleaned_text = "\n".join(cleaned_lines)
    raw_lines = text.splitlines()
    for row in acronym_rows:
        acronym = row["acronym"]
        acronym_pattern = re.compile(rf"\b{re.escape(acronym)}\b")
        first_acronym_match = acronym_pattern.search(cleaned_text)
        if not first_acronym_match:
            continue

        lt_form = row.get("lt", "")
        if parse_bool(row.get("must_expand_first", ""), default=False) and lt_form:
            prefix = cleaned_text[: first_acronym_match.start()]
            lineno = prefix.count("\n") + 1
            same_line_text = cleaned_lines[lineno - 1]
            if not has_relaxed_lt_expansion(prefix, lt_form) and not has_relaxed_lt_expansion(same_line_text, lt_form):
                add_finding(
                    findings,
                    file_path,
                    lineno,
                    "acronym_first_use",
                    f"Trumpinį `{acronym}` pirmą kartą išskleiskite kaip `{lt_form}`.",
                    raw_lines[lineno - 1],
                )

        if not parse_bool(row.get("allowed_in_headings", ""), default=True):
            for lineno, line in enumerate(raw_lines, start=1):
                if not line.lstrip().startswith("#"):
                    continue
                if acronym_pattern.search(cleaned_lines[lineno - 1]):
                    add_finding(
                        findings,
                        file_path,
                        lineno,
                        "acronym_heading_policy",
                        f"Trumpinys `{acronym}` neturėtų būti vartojamas antraštėje be aiškios išimties.",
                        line,
                    )
    return findings


def main() -> int:
    args = parse_args()
    chapter_pack_path = Path(args.chapter_pack) if args.chapter_pack else None
    term_rows = active_terms(Path(args.termbase), chapter_pack_path)
    acronym_rows = active_acronyms(Path(args.acronyms), chapter_pack_path)
    legacy_rules = load_legacy_rules([Path(raw) for raw in args.legacy_rules])

    findings: list[str] = []
    for file_path in iter_markdown_files(args.paths):
        text = file_path.read_text(encoding="utf-8")
        findings.extend(scan_legacy_rules(file_path, text, legacy_rules))
        findings.extend(scan_terms(file_path, text, term_rows))
        findings.extend(scan_acronyms(file_path, text, acronym_rows))

    if findings:
        print("\n\n".join(findings))
        return 1

    print("No terminology, acronym, or banned phrase issues found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
