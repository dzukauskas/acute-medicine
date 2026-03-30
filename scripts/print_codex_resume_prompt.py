#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from workflow_runtime import REPO_ROOT


ENGINEERING_LEDGER = REPO_ROOT / "ENGINEERING_LEDGER.md"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a minimal prompt the user can paste into a new Codex thread."
    )
    parser.add_argument(
        "--mode",
        choices=("engineering", "translation"),
        default="engineering",
        help="Prompt type to print.",
    )
    parser.add_argument("--book-root", help="Required for translation mode: books/<slug> path.")
    parser.add_argument("--chapter", help="Optional chapter slug or number for translation mode.")
    return parser.parse_args(argv)


def extract_ledger_value(section_key: str, text: str) -> str:
    pattern = re.compile(
        rf"<!-- ledger:{section_key}:start -->\n(.*?)\n<!-- ledger:{section_key}:end -->",
        flags=re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return ""
    return match.group(1).strip()


def extract_first_bullet(text: str) -> str:
    for line in text.splitlines():
        cleaned = line.strip()
        if cleaned.startswith("- "):
            return cleaned[2:].strip()
    return ""


def extract_active_theme(text: str) -> str:
    section = extract_ledger_value("active_theme", text)
    match = re.search(r"Theme:\s*(.+)", section)
    return match.group(1).strip() if match else ""


def render_engineering_prompt() -> str:
    if ENGINEERING_LEDGER.exists():
        ledger_text = ENGINEERING_LEDGER.read_text(encoding="utf-8")
        theme = extract_active_theme(ledger_text) or "aktyvi repo-engineering tema"
        summary = extract_first_bullet(extract_ledger_value("summary", ledger_text))
        next_step = extract_first_bullet(extract_ledger_value("next_steps", ledger_text))
    else:
        theme = "aktyvi repo-engineering tema"
        summary = ""
        next_step = ""

    lines = [
        "Perskaityk AGENTS.md, docs/codex-workflow.md, docs/repo-engineering-workflow.md ir ENGINEERING_LEDGER.md.",
        "Dirbk repo-engineering režimu.",
        f"Tęsk aktyvią temą: {theme}.",
    ]
    if summary and not summary.startswith("_No "):
        lines.append(f"Santrauka: {summary}")
    if next_step and not next_step.startswith("_No "):
        lines.append(f"Pirmas prioritetas: {next_step}")
    lines.append("Jei tema nepasikeitė, lik tame pačiame thread kontekste; jei tema jau kita, aiškiai pasakyk, kad logiška pradėti naują thread.")
    return " ".join(lines)


def resolve_book_root(raw_value: str | None) -> Path:
    if not raw_value:
        raise SystemExit("Translation mode reikalauja --book-root books/<slug>.")
    candidate = Path(raw_value).expanduser()
    if not candidate.is_absolute():
        candidate = REPO_ROOT / candidate
    candidate = candidate.resolve()
    if not candidate.exists():
        raise SystemExit(f"Nerastas --book-root katalogas: {candidate}")
    return candidate


def resolve_translation_targets(book_root: Path, chapter: str | None) -> tuple[str, list[str]]:
    targets = [
        "AGENTS.md",
        "books/README.md",
        "books/_template/workflow.md",
        "books/_template/source-priority.md",
        book_root.relative_to(REPO_ROOT).as_posix() + "/workflow.md",
    ]
    if chapter:
        chapter_token = chapter.strip()
        if chapter_token.isdigit():
            prefix = f"{int(chapter_token):03d}-"
            research_matches = sorted((book_root / "research").glob(prefix + "*.md"))
            pack_matches = sorted((book_root / "chapter_packs").glob(prefix + "*.yaml"))
        else:
            research_matches = sorted((book_root / "research").glob(chapter_token + "*.md"))
            pack_matches = sorted((book_root / "chapter_packs").glob(chapter_token + "*.yaml"))
        if research_matches:
            targets.append(research_matches[0].relative_to(REPO_ROOT).as_posix())
        if pack_matches:
            targets.append(pack_matches[0].relative_to(REPO_ROOT).as_posix())
        targets.append(book_root.relative_to(REPO_ROOT).as_posix() + "/term_candidates.tsv")
        return chapter_token, targets
    return "", targets


def render_translation_prompt(book_root: Path, chapter: str | None) -> str:
    chapter_token, targets = resolve_translation_targets(book_root, chapter)
    lines = [
        "Perskaityk " + ", ".join(targets[:-1]) + f" ir {targets[-1]}.",
        "Dirbk book-translation režimu.",
    ]
    if chapter_token:
        lines.append(f"Tęsk šio skyriaus darbą: {chapter_token}.")
    else:
        lines.append(f"Tęsk aktyvų darbą knygoje {book_root.name}.")
    lines.append("Jei tai tas pats skyrius ar tas pats blocker'ių rinkinys, lik tame pačiame thread kontekste; jei prasideda kitas skyrius ar kita vertimo tema, aiškiai pasakyk, kad logiška pradėti naują thread.")
    return " ".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.mode == "engineering":
        print(render_engineering_prompt())
        return 0

    book_root = resolve_book_root(args.book_root)
    print(render_translation_prompt(book_root, args.chapter))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
