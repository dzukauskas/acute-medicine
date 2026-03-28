#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

from book_workflow_support import calque_pattern_paths, disallowed_phrase_paths, disallowed_term_paths, resolve_book_root


Rule = dict[str, str]
INLINE_CODE_RE = re.compile(r"`[^`]*`")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\([^)]+\)")


def load_rules(paths: list[Path]) -> list[Rule]:
    rows: list[Rule] = []
    seen: set[tuple[str, str, str, str, str, str, str]] = set()
    for path in paths:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                if path.name.startswith("disallowed_terms"):
                    normalized = {
                        "rule_file": path.name,
                        "match_type": "phrase",
                        "banned": row.get("banned", "").strip(),
                        "preferred": row.get("preferred", "").strip(),
                        "reason": row.get("reason", "").strip(),
                        "category": "term",
                        "severity": "medium",
                        "promoted_from": "",
                        "notes": "",
                    }
                elif path.name.startswith("disallowed_phrases"):
                    normalized = {
                        "rule_file": path.name,
                        "match_type": row.get("match_type", "phrase").strip() or "phrase",
                        "banned": row.get("banned", "").strip(),
                        "preferred": row.get("preferred", "").strip(),
                        "reason": row.get("reason", "").strip(),
                        "category": "phrase",
                        "severity": "medium",
                        "promoted_from": "",
                        "notes": "",
                    }
                else:
                    normalized = {
                        "rule_file": path.name,
                        "match_type": row.get("match_type", "phrase").strip() or "phrase",
                        "banned": row["banned"].strip(),
                        "preferred": row["preferred"].strip(),
                        "reason": row["reason"].strip(),
                        "category": row.get("category", "").strip(),
                        "severity": row.get("severity", "").strip(),
                        "promoted_from": row.get("promoted_from", "").strip(),
                        "notes": row.get("notes", "").strip(),
                    }

                identity = (
                    normalized["match_type"].lower(),
                    normalized["banned"].lower(),
                    normalized["preferred"].lower(),
                    normalized["reason"].lower(),
                    normalized["category"].lower(),
                    normalized["severity"].lower(),
                    normalized["notes"].lower(),
                )
                if identity in seen:
                    continue
                seen.add(identity)
                rows.append(normalized)
    return [row for row in rows if row["banned"]]


def build_pattern(rule: Rule) -> re.Pattern[str]:
    banned = rule["banned"]
    match_type = rule["match_type"]
    if match_type == "phrase":
        return re.compile(re.escape(banned), re.IGNORECASE)
    if match_type == "regex":
        return re.compile(banned, re.IGNORECASE)
    raise ValueError(f"Unsupported match_type={match_type!r} in {rule['rule_file']}")


def normalize_line_for_scan(line: str) -> str:
    normalized = INLINE_CODE_RE.sub("", line)
    normalized = MARKDOWN_LINK_RE.sub("", normalized)
    return normalized


def find_matches(text: str, rule: Rule) -> list[tuple[int, str]]:
    pattern = build_pattern(rule)
    matches: list[tuple[int, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        normalized = normalize_line_for_scan(line)
        if pattern.search(normalized):
            matches.append((lineno, line.strip()))
    return matches


def scan_file(file_path: Path, rules: list[Rule]) -> list[str]:
    text = file_path.read_text(encoding="utf-8")
    findings: list[str] = []
    for rule in rules:
        for lineno, line in find_matches(text, rule):
            findings.append(
                f"{file_path}:{lineno}: rule_file='{rule['rule_file']}' "
                f"match_type='{rule['match_type']}' banned='{rule['banned']}' "
                f"preferred='{rule['preferred']}' reason='{rule['reason']}' "
                f"category='{rule['category']}' severity='{rule['severity']}' "
                f"promoted_from='{rule['promoted_from']}' notes='{rule['notes']}'\n"
                f"  {line}"
            )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Flag Lithuanian prose calques and translation-shaped sentence patterns."
    )
    parser.add_argument(
        "--book-root",
        help="Optional books/<slug> root. If omitted, uses MEDBOOK_ROOT.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files or directories to scan. If omitted, scans <book-root>/lt/chapters.",
    )
    parser.add_argument(
        "--rules",
        nargs="*",
        help="One or more TSV rule files. Defaults to shared prose rules + matching <book-root>/*.local.tsv overrides.",
    )
    args = parser.parse_args()

    book_root = resolve_book_root(args.book_root)
    paths = args.paths or ([str(book_root / "lt" / "chapters")] if book_root else [])
    if not paths:
        raise SystemExit("Nurodykite scan kelią arba nustatykite MEDBOOK_ROOT / --book-root.")

    rules = args.rules or (
        [*(str(path) for path in calque_pattern_paths(book_root)), *(str(path) for path in disallowed_term_paths(book_root)), *(str(path) for path in disallowed_phrase_paths(book_root))]
        if book_root
        else []
    )
    if not rules:
        raise SystemExit("Nenurodytas rules failas. Perduokite --rules arba nustatykite MEDBOOK_ROOT / --book-root.")

    rules = load_rules([Path(raw) for raw in rules])
    files: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(p for p in path.rglob("*.md") if p.is_file()))
        elif path.is_file():
            files.append(path)

    findings: list[str] = []
    for file_path in files:
        findings.extend(scan_file(file_path, rules))

    if findings:
        print("\n\n".join(findings))
        return 1

    print("No translation-shaped prose patterns found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
