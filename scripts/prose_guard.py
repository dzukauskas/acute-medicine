#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


Rule = dict[str, str]
INLINE_CODE_RE = re.compile(r"`[^`]*`")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\([^)]+\)")


def load_rules(paths: list[Path]) -> list[Rule]:
    rows: list[Rule] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                rows.append(
                    {
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
                )
    return rows


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
        "paths",
        nargs="*",
        default=["books/acute-medicine/lt/chapters"],
        help="Files or directories to scan. Defaults to books/acute-medicine/lt/chapters.",
    )
    parser.add_argument(
        "--rules",
        nargs="*",
        default=["books/acute-medicine/calque_patterns.tsv"],
        help="One or more TSV rule files. Defaults to the active book calque rule set.",
    )
    args = parser.parse_args()

    rules = load_rules([Path(raw) for raw in args.rules])
    files: list[Path] = []
    for raw in args.paths:
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
