#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
from datetime import datetime
from pathlib import Path

from workflow_runtime import REPO_ROOT


DEFAULT_LEDGER_PATH = REPO_ROOT / "ENGINEERING_LEDGER.md"
SECTION_KEYS = (
    "active_theme",
    "summary",
    "current_state",
    "decisions",
    "next_steps",
    "risks",
    "completed",
)
LEDGER_TEMPLATE = """# Engineering Ledger

## Active Theme
<!-- ledger:active_theme:start -->
- Theme: _unset_
- Branch: _unset_
- Last updated: _unset_
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- _No active repo-engineering summary yet._
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- _No current state recorded._
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- _No accepted engineering decisions recorded._
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- _No next steps recorded._
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- _No open engineering risks recorded._
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
- _No completed engineering themes recorded._
<!-- ledger:completed:end -->
"""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update the tracked repo-engineering ledger used to survive long Codex threads."
    )
    parser.add_argument("--output", help="Optional ledger path. Defaults to ENGINEERING_LEDGER.md")
    parser.add_argument("--theme", help="Current active engineering theme.")
    parser.add_argument("--summary", help="One-line summary of the active engineering theme.")
    parser.add_argument(
        "--state",
        action="append",
        default=[],
        help="Current state bullet. Repeat for multiple items.",
    )
    parser.add_argument(
        "--decision",
        action="append",
        default=[],
        help="Accepted decision bullet. Repeat for multiple items.",
    )
    parser.add_argument(
        "--next-step",
        action="append",
        default=[],
        help="Next-step bullet. Repeat for multiple items.",
    )
    parser.add_argument(
        "--risk",
        action="append",
        default=[],
        help="Open-risk bullet. Repeat for multiple items.",
    )
    parser.add_argument(
        "--completed",
        action="append",
        default=[],
        help="Completed theme note. Repeat to append multiple notes.",
    )
    parser.add_argument(
        "--generated-at",
        help="Override timestamp in ISO 8601 format for deterministic output.",
    )
    parser.add_argument(
        "--branch",
        help="Override branch name. Defaults to current git branch when available.",
    )
    return parser.parse_args(argv)


def parse_generated_at(value: str | None) -> datetime:
    if not value:
        return datetime.now().astimezone()
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"Neteisingas --generated-at formatas: {value}") from exc


def render_bullets(items: list[str], placeholder: str) -> str:
    cleaned = [item.strip() for item in items if item.strip()]
    if not cleaned:
        return f"- {placeholder}"
    return "\n".join(f"- {item}" for item in cleaned)


def template_text() -> str:
    return LEDGER_TEMPLATE


def ensure_sections(text: str) -> str:
    for key in SECTION_KEYS:
        if f"<!-- ledger:{key}:start -->" not in text or f"<!-- ledger:{key}:end -->" not in text:
            raise SystemExit(f"Ledger faile trūksta sekcijos marker'ių: {key}")
    return text


def replace_section(text: str, key: str, body: str) -> str:
    pattern = re.compile(
        rf"(<!-- ledger:{key}:start -->\n)(.*?)(\n<!-- ledger:{key}:end -->)",
        flags=re.DOTALL,
    )
    updated, count = pattern.subn(rf"\1{body}\3", text, count=1)
    if count != 1:
        raise SystemExit(f"Nepavyko atnaujinti ledger sekcijos: {key}")
    return updated


def extract_section(text: str, key: str) -> str:
    pattern = re.compile(
        rf"<!-- ledger:{key}:start -->\n(.*?)\n<!-- ledger:{key}:end -->",
        flags=re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise SystemExit(f"Nepavyko perskaityti ledger sekcijos: {key}")
    return match.group(1).strip()


def detect_branch(override: str | None) -> str:
    if override:
        return override
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return "_unknown_"
    return result.stdout.strip() or "_unknown_"


def append_completed(existing_body: str, items: list[str], generated_at: datetime, theme: str | None) -> str:
    cleaned = [item.strip() for item in items if item.strip()]
    if not cleaned:
        return existing_body

    existing_lines = [line for line in existing_body.splitlines() if line.strip()]
    if existing_lines == ["- _No completed engineering themes recorded._"]:
        existing_lines = []

    stamp = generated_at.strftime("%Y-%m-%d %H:%M")
    theme_label = theme.strip() if theme and theme.strip() else "repo-engineering"
    new_lines = [f"### {stamp} | {theme_label}"]
    new_lines.extend(f"- {item}" for item in cleaned)

    if existing_lines:
        return "\n".join(new_lines + [""] + existing_lines)
    return "\n".join(new_lines)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    generated_at = parse_generated_at(args.generated_at)
    branch = detect_branch(args.branch)

    output_path = Path(args.output).expanduser() if args.output else DEFAULT_LEDGER_PATH
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path
    output_path = output_path.resolve()

    if output_path.exists():
        text = output_path.read_text(encoding="utf-8")
    else:
        text = template_text()
    text = ensure_sections(text)

    existing_active = extract_section(text, "active_theme")
    existing_summary = extract_section(text, "summary")
    existing_state = extract_section(text, "current_state")
    existing_decisions = extract_section(text, "decisions")
    existing_next_steps = extract_section(text, "next_steps")
    existing_risks = extract_section(text, "risks")
    existing_completed = extract_section(text, "completed")

    if args.theme:
        active_body = (
            f"- Theme: {args.theme.strip()}\n"
            f"- Branch: {branch}\n"
            f"- Last updated: {generated_at.isoformat()}"
        )
    else:
        active_body = existing_active
        if "Last updated:" in active_body:
            active_body = re.sub(
                r"Last updated: .*",
                f"Last updated: {generated_at.isoformat()}",
                active_body,
            )

    summary_body = render_bullets([args.summary], "_No active repo-engineering summary yet._") if args.summary else existing_summary
    state_body = render_bullets(args.state, "_No current state recorded._") if args.state else existing_state
    decisions_body = render_bullets(args.decision, "_No accepted engineering decisions recorded._") if args.decision else existing_decisions
    next_steps_body = render_bullets(args.next_step, "_No next steps recorded._") if args.next_step else existing_next_steps
    risks_body = render_bullets(args.risk, "_No open engineering risks recorded._") if args.risk else existing_risks
    completed_body = append_completed(existing_completed, args.completed, generated_at, args.theme)

    text = replace_section(text, "active_theme", active_body)
    text = replace_section(text, "summary", summary_body)
    text = replace_section(text, "current_state", state_body)
    text = replace_section(text, "decisions", decisions_body)
    text = replace_section(text, "next_steps", next_steps_body)
    text = replace_section(text, "risks", risks_body)
    text = replace_section(text, "completed", completed_body)

    output_path.write_text(text + ("" if text.endswith("\n") else "\n"), encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
