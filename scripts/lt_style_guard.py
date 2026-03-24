#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


MARKDOWN_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]+\)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
URL_RE = re.compile(r"https?://\S+")
ABS_PATH_RE = re.compile(r"/Users/\S+")
REPO_PATH_RE = re.compile(r"\b(?:books|scripts|codex)/[A-Za-z0-9._/\- ]+")
FENCE_RE = re.compile(r"^\s*```")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?(?:\s*:?-+:?\s*\|)+\s*$")
METADATA_RE = re.compile(
    r"^\s*-\s*(Autoriai originale|Autorė originale|Puslapiai|PDF|Angliškas pagalbinis failas|Lietuviškas failas|Tipas):"
)
HTML_COMMENT_RE = re.compile(r"^\s*<!--.*-->\s*$")
ASCII_RANGE_RE = re.compile(r"\b\d+(?:,\d+)?\s*-\s*\d+(?:,\d+)?\b")
ASCII_X_RE = re.compile(r"\b\d+(?:,\d+)?\s*x\s*\d+(?:,\d+)?\b")
NBSP = "\u00A0"
UNITS = (
    "mmol/L",
    "mol/L",
    "g/L",
    "mmHg",
    "kPa",
    "L/min.",
    "mL",
    "ml",
    "kg",
    "mg",
    "µg",
    "ng",
    "cm",
    "mm",
    "m",
    "min.",
    "s",
    "%",
    "°C",
)
UNIT_PATTERN = "|".join(re.escape(unit) for unit in sorted(UNITS, key=len, reverse=True))
DECIMAL_DOT_RE = re.compile(
    rf"\b\d+\.\d+(?=(?:{NBSP}|[ \t])(?:{UNIT_PATTERN})\b)"
)
SPACE_BEFORE_UNIT_RE = re.compile(
    rf"(?P<number>\d+(?:,\d+)?(?:–\d+(?:,\d+)?)?)(?P<space>[ \t]+)(?P<unit>{UNIT_PATTERN})\b"
)
NO_SPACE_BEFORE_UNIT_RE = re.compile(
    rf"(?P<number>\d+(?:,\d+)?(?:–\d+(?:,\d+)?)?)(?P<unit>{UNIT_PATTERN})\b"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Flag Lithuanian medical typography and low-noise style issues."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["books/acute-medicine/lt/chapters"],
        help="Files or directories to scan. Defaults to books/acute-medicine/lt/chapters.",
    )
    return parser.parse_args()


def normalize_line_for_scan(line: str) -> str:
    normalized = INLINE_CODE_RE.sub("", line)
    normalized = MARKDOWN_LINK_RE.sub(r"\1", normalized)
    normalized = URL_RE.sub("", normalized)
    normalized = ABS_PATH_RE.sub("", normalized)
    normalized = REPO_PATH_RE.sub("", normalized)
    return normalized


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


def is_false_positive_unit(normalized: str, match: re.Match[str]) -> bool:
    unit = match.group("unit")
    next_char = normalized[match.end(): match.end() + 1]
    return unit in {"m", "s"} and next_char == "."


def scan_file(file_path: Path) -> list[str]:
    findings: list[str] = []
    in_fence = False
    for lineno, raw_line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
        if FENCE_RE.match(raw_line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if HTML_COMMENT_RE.match(raw_line):
            continue
        if METADATA_RE.match(raw_line):
            continue
        if TABLE_SEPARATOR_RE.match(raw_line):
            continue

        normalized = normalize_line_for_scan(raw_line)
        if not normalized.strip():
            continue

        if DECIMAL_DOT_RE.search(normalized):
            add_finding(
                findings,
                file_path,
                lineno,
                "decimal_comma",
                "Naudokite dešimtainį kablelį, ne tašką.",
                raw_line,
            )
        if ASCII_RANGE_RE.search(normalized):
            add_finding(
                findings,
                file_path,
                lineno,
                "range_dash",
                "Skaitiniams intervalams naudokite en dash `–`, ne paprastą brūkšnelį `-`.",
                raw_line,
            )
        if ASCII_X_RE.search(normalized):
            add_finding(
                findings,
                file_path,
                lineno,
                "times_sign",
                "Formulėse ir matmenyse naudokite `×`, ne `x`.",
                raw_line,
            )
        if raw_line.lstrip().startswith("#") and "(angl." in normalized:
            add_finding(
                findings,
                file_path,
                lineno,
                "english_in_heading",
                "Antraštėse anglų terminų skliaustuose venkite.",
                raw_line,
            )
        if normalized.count("(angl.") > 1:
            add_finding(
                findings,
                file_path,
                lineno,
                "english_parenthetical_cluster",
                "Vienoje eilutėje ar pastraipoje per daug anglų terminų skliaustuose.",
                raw_line,
            )

        for match in SPACE_BEFORE_UNIT_RE.finditer(normalized):
            if is_false_positive_unit(normalized, match):
                continue
            if match.group("space") != NBSP:
                add_finding(
                    findings,
                    file_path,
                    lineno,
                    "nbsp_before_unit",
                    "Tarp skaičiaus ir vieneto naudokite nepertraukiamą tarpą.",
                    raw_line,
                )
                break

        for match in NO_SPACE_BEFORE_UNIT_RE.finditer(normalized):
            if is_false_positive_unit(normalized, match):
                continue
            start = match.start()
            if start > 0 and normalized[start - 1].isdigit():
                continue
            end = match.end()
            if end < len(normalized) and normalized[end].isalnum():
                continue
            add_finding(
                findings,
                file_path,
                lineno,
                "space_before_unit",
                "Tarp skaičiaus ir vieneto trūksta tarpo.",
                raw_line,
            )
            break

    return findings


def main() -> int:
    args = parse_args()
    findings: list[str] = []
    for file_path in iter_markdown_files(args.paths):
        findings.extend(scan_file(file_path))

    if findings:
        print("\n\n".join(findings))
        return 1

    print("No Lithuanian style or typography issues found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
