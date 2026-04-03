#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from workflow_runtime import REPO_ROOT


ENGINEERING_LEDGER = REPO_ROOT / "ENGINEERING_LEDGER.md"
NO_ACTIVE_THEME = "no-active-theme"
INACTIVE_THEME_MARKERS = {"", "_unset_", NO_ACTIVE_THEME}
ENGINEERING_RAW_DIFF_CONTRACT = (
    "Kai atsakyme rodai raw diff, naudok tik `~~~~diff` pradžią ir `~~~~` pabaigą; "
    "nenaudok triple backticks aplink visą raw diff bloką. "
    "Tarp `diff --git ...` ir closing fence nedėk paprasto komentaro. "
    "Jei diff ilgas, rodyk jį po failą atskiruose blokuose. "
    "Niekada neiškelk atskirų `+` ar `-` eilučių už fenced diff bloko ribų."
)


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
    parser.add_argument("--chapter", help="Required for translation mode: chapter slug or number.")
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


def extract_latest_completed_theme(text: str) -> str:
    section = extract_ledger_value("completed", text)
    for line in section.splitlines():
        cleaned = line.strip()
        if not cleaned.startswith("### "):
            continue
        heading = cleaned[4:].strip()
        if "|" in heading:
            return heading.split("|", 1)[1].strip()
        return heading
    return ""


def has_active_theme(theme: str) -> bool:
    return theme.strip() not in INACTIVE_THEME_MARKERS


def render_engineering_prompt() -> str:
    if ENGINEERING_LEDGER.exists():
        ledger_text = ENGINEERING_LEDGER.read_text(encoding="utf-8")
        theme = extract_active_theme(ledger_text) or "aktyvi repo-engineering tema"
        summary = extract_first_bullet(extract_ledger_value("summary", ledger_text))
        current_state = extract_first_bullet(extract_ledger_value("current_state", ledger_text))
        accepted_decisions = extract_first_bullet(extract_ledger_value("decisions", ledger_text))
        open_risks = extract_first_bullet(extract_ledger_value("risks", ledger_text))
        next_step = extract_first_bullet(extract_ledger_value("next_steps", ledger_text))
        last_completed = extract_latest_completed_theme(ledger_text)
    else:
        theme = NO_ACTIVE_THEME
        summary = ""
        current_state = ""
        accepted_decisions = ""
        open_risks = ""
        next_step = ""
        last_completed = ""

    lines = [
        "Perskaityk AGENTS.md, docs/codex-workflow.md, docs/repo-engineering-workflow.md ir ENGINEERING_LEDGER.md.",
        "Dirbk repo-engineering režimu.",
        "Static passive repo context imk iš AGENTS.md ir workflow docs; current dynamic durable execution state imk iš ENGINEERING_LEDGER.md.",
    ]
    if has_active_theme(theme):
        lines.append(f"Tęsk aktyvią temą: {theme}.")
    else:
        lines.append("Ledger šiuo metu neturi aktyvios repo-engineering temos.")
        if last_completed:
            lines.append(f"Paskutinė uždaryta tema: {last_completed}.")
    if summary and not summary.startswith("_No "):
        lines.append(f"Santrauka: {summary}")
    if current_state and not current_state.startswith("_No "):
        lines.append(f"Dabartinė būsena: {current_state}")
    if accepted_decisions and not accepted_decisions.startswith("_No "):
        lines.append(f"Priimti sprendimai: {accepted_decisions}")
    if next_step and not next_step.startswith("_No "):
        lines.append(f"Pirmas prioritetas: {next_step}")
    if open_risks and not open_risks.startswith("_No "):
        lines.append(f"Atviros rizikos: {open_risks}")
    lines.append("Thread history ar handoffs naudok tik jei ledger ir kanoninių repo artefaktų neužtenka.")
    lines.append(ENGINEERING_RAW_DIFF_CONTRACT)
    if has_active_theme(theme):
        lines.append("Jei tema nepasikeitė, lik tame pačiame thread kontekste; jei tema jau kita, aiškiai pasakyk, kad logiška pradėti naują thread.")
    else:
        lines.append("Jei tai natūrali tos pačios techninės linijos tąsa, aiškiai įvardyk naują siaurą temą ir atnaujink ledger; jei tema jau kita, pradėk naują thread.")
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


def require_translation_chapter(chapter: str | None) -> str:
    chapter_token = (chapter or "").strip()
    if not chapter_token:
        raise SystemExit("Translation resume šiame repo reikalauja --chapter ir konkretaus skyriaus.")
    return chapter_token


def resolve_translation_targets(book_root: Path, chapter: str) -> tuple[str, list[str]]:
    targets = [
        "AGENTS.md",
        "books/README.md",
        "books/_template/workflow.md",
        "books/_template/source-priority.md",
        "docs/book-translation-workflow.md",
        book_root.relative_to(REPO_ROOT).as_posix() + "/workflow.md",
    ]
    chapter_token = require_translation_chapter(chapter)
    if chapter_token.isdigit():
        research_pattern = f"{int(chapter_token):03d}-*.md"
        pack_pattern = f"{int(chapter_token):03d}-*.yaml"
    else:
        research_pattern = chapter_token + "*.md"
        pack_pattern = chapter_token + "*.yaml"
    research_matches = sorted((book_root / "research").glob(research_pattern))
    pack_matches = sorted((book_root / "chapter_packs").glob(pack_pattern))
    if research_matches:
        targets.append(research_matches[0].relative_to(REPO_ROOT).as_posix())
    if pack_matches:
        targets.append(pack_matches[0].relative_to(REPO_ROOT).as_posix())
    chapter_draft_matches = sorted((book_root / "lt" / "chapters").glob(research_pattern))
    if chapter_draft_matches:
        targets.append(chapter_draft_matches[0].relative_to(REPO_ROOT).as_posix())
    adjudication_matches = sorted((book_root / "adjudication_packs").glob(pack_pattern))
    if adjudication_matches:
        targets.append(adjudication_matches[0].relative_to(REPO_ROOT).as_posix())
    targets.append(book_root.relative_to(REPO_ROOT).as_posix() + "/term_candidates.tsv")
    return chapter_token, targets


def render_translation_prompt(book_root: Path, chapter: str) -> str:
    chapter_token, targets = resolve_translation_targets(book_root, chapter)
    lines = [
        "Perskaityk " + ", ".join(targets[:-1]) + f" ir {targets[-1]}.",
        "Dirbk book-translation režimu.",
        f"Tęsk šio skyriaus darbą: {chapter_token}.",
        "Static passive repo context imk iš AGENTS.md, books/README.md ir workflow docs; current dynamic durable execution state imk iš šio skyriaus artefaktų.",
    ]
    lines.append("Jei po resume svarbus automatinis QA statusas, perleisk run_chapter_qa.py iš naujo; jis nėra stored machine-readable receipt.")
    lines.append("Jei tai tas pats skyrius ar tas pats blocker'ių rinkinys, lik tame pačiame thread kontekste; jei prasideda kitas skyrius ar kita vertimo tema, aiškiai pasakyk, kad logiška pradėti naują thread.")
    return " ".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.mode == "engineering":
        print(render_engineering_prompt())
        return 0

    book_root = resolve_book_root(args.book_root)
    chapter = (args.chapter or "").strip()
    if not chapter:
        raise SystemExit("Translation resume šiame repo reikalauja --chapter ir konkretaus skyriaus.")
    print(render_translation_prompt(book_root, chapter))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
