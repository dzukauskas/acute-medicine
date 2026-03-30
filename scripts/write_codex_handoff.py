#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from workflow_runtime import REPO_ROOT


HANDOFFS_DIR = REPO_ROOT / "handoffs"


@dataclass(frozen=True)
class GitSnapshot:
    branch: str
    head: str
    worktree: Path
    status_lines: list[str]
    recent_commits: list[str]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write a Codex handoff note that survives thread compaction or worktree handoff."
    )
    parser.add_argument("--title", default="Codex handoff", help="Short handoff title.")
    parser.add_argument("--book-root", help="Optional repo-relative books/<slug> path.")
    parser.add_argument("--goal", default="", help="Current user goal or task focus.")
    parser.add_argument(
        "--completed",
        action="append",
        default=[],
        help="Completed item. Repeat for multiple bullets.",
    )
    parser.add_argument(
        "--next-step",
        action="append",
        default=[],
        help="Next step. Repeat for multiple bullets.",
    )
    parser.add_argument(
        "--risk",
        action="append",
        default=[],
        help="Open risk or blocker. Repeat for multiple bullets.",
    )
    parser.add_argument(
        "--generated-at",
        help="Override timestamp in ISO 8601 format for deterministic output.",
    )
    parser.add_argument(
        "--output",
        help="Optional output Markdown path. Defaults to handoffs/<timestamp>-<branch>.md",
    )
    parser.add_argument(
        "--recent-commits",
        type=int,
        default=5,
        help="How many recent commits to embed in the handoff.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite an existing output file.",
    )
    return parser.parse_args(argv)


def git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout).strip() or f"`git {' '.join(args)}` failed."
        raise SystemExit(message)
    return result.stdout.strip()


def git_lines(*args: str) -> list[str]:
    output = git_output(*args)
    return [line for line in output.splitlines() if line.strip()]


def collect_git_snapshot(recent_commits: int) -> GitSnapshot:
    return GitSnapshot(
        branch=git_output("rev-parse", "--abbrev-ref", "HEAD"),
        head=git_output("rev-parse", "HEAD"),
        worktree=REPO_ROOT,
        status_lines=git_lines("status", "--short"),
        recent_commits=git_lines("log", f"--max-count={recent_commits}", "--pretty=format:%h %s"),
    )


def parse_generated_at(value: str | None) -> datetime:
    if not value:
        return datetime.now().astimezone()
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"Neteisingas --generated-at formatas: {value}") from exc


def sanitize_filename(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-._")
    return cleaned or "handoff"


def default_output_path(branch: str, generated_at: datetime) -> Path:
    timestamp = generated_at.strftime("%Y%m%d-%H%M%S")
    return HANDOFFS_DIR / f"{timestamp}-{sanitize_filename(branch)}.md"


def resolve_book_root(raw_value: str | None) -> Path | None:
    if not raw_value:
        return None
    candidate = Path(raw_value).expanduser()
    if not candidate.is_absolute():
        candidate = REPO_ROOT / candidate
    candidate = candidate.resolve()
    if not candidate.exists():
        raise SystemExit(f"Nerastas --book-root katalogas: {candidate}")
    return candidate


def repo_relative(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def bullet_section(items: list[str], placeholder: str) -> str:
    if items:
        return "\n".join(f"- {item}" for item in items)
    return f"- {placeholder}"


def render_status_block(snapshot: GitSnapshot) -> str:
    if not snapshot.status_lines:
        return "- Working tree: clean"
    lines = "\n".join(snapshot.status_lines)
    return f"- Working tree: dirty\n\n```text\n{lines}\n```"


def render_commits_block(snapshot: GitSnapshot) -> str:
    if not snapshot.recent_commits:
        return "_No local commit history found._"
    return "```text\n" + "\n".join(snapshot.recent_commits) + "\n```"


def startup_checklist(book_root: Path | None) -> str:
    steps = [
        "1. Perskaityk `AGENTS.md`.",
        "2. Perskaityk `books/README.md`.",
        "3. Perskaityk `docs/codex-workflow.md`.",
        "4. Jei tai repo-engineering darbas, perskaityk `ENGINEERING_LEDGER.md`.",
        "5. Perskaityk šį handoff failą prieš tęsiant darbus.",
        "6. Tęsk tame pačiame branch/worktree arba naudok Codex app `Hand off`, jei reikia paralelinės linijos.",
    ]
    if book_root is not None:
        workflow_path = book_root / "workflow.md"
        if workflow_path.exists():
            steps.insert(3, f"4. Perskaityk `{repo_relative(workflow_path)}`.")
            steps[4] = "5. Jei tai repo-engineering darbas, perskaityk `ENGINEERING_LEDGER.md`."
            steps[5] = "6. Perskaityk šį handoff failą prieš tęsiant darbus."
            steps[6] = "7. Tęsk tame pačiame branch/worktree arba naudok Codex app `Hand off`, jei reikia paralelinės linijos."
    return "\n".join(steps)


def render_handoff(
    *,
    title: str,
    generated_at: datetime,
    snapshot: GitSnapshot,
    book_root: Path | None,
    goal: str,
    completed: list[str],
    next_steps: list[str],
    risks: list[str],
) -> str:
    book_root_line = f"- Book root: `{repo_relative(book_root)}`\n" if book_root is not None else ""
    return (
        f"# {title}\n\n"
        "## Metadata\n\n"
        f"- Generated: `{generated_at.isoformat()}`\n"
        f"- Repo: `{REPO_ROOT.as_posix()}`\n"
        f"- Worktree: `{snapshot.worktree.as_posix()}`\n"
        f"- Branch: `{snapshot.branch}`\n"
        f"- HEAD: `{snapshot.head}`\n"
        f"{book_root_line}"
        "\n## Goal\n\n"
        f"{bullet_section([goal] if goal else [], 'Aprašyk pagrindinį vartotojo tikslą arba problemą.')}\n\n"
        "## Repo Snapshot\n\n"
        f"{render_status_block(snapshot)}\n\n"
        "### Recent commits\n\n"
        f"{render_commits_block(snapshot)}\n\n"
        "## Completed\n\n"
        f"{bullet_section(completed, 'Užrašyk, kas jau padaryta ir patikrinta.')}\n\n"
        "## Next steps\n\n"
        f"{bullet_section(next_steps, 'Užrašyk pirmą konkretų veiksmą naujam thread ar worktree.')}\n\n"
        "## Risks / blockers\n\n"
        f"{bullet_section(risks, 'Užrašyk blokatorius, prielaidas arba rizikingas vietas.')}\n\n"
        "## Next-thread startup\n\n"
        f"{startup_checklist(book_root)}\n"
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    generated_at = parse_generated_at(args.generated_at)
    snapshot = collect_git_snapshot(args.recent_commits)
    book_root = resolve_book_root(args.book_root)
    output_path = Path(args.output).expanduser() if args.output else default_output_path(snapshot.branch, generated_at)
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path
    output_path = output_path.resolve()

    if output_path.exists() and not args.overwrite:
        raise SystemExit(f"Išvesties failas jau egzistuoja: {output_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_handoff(
            title=args.title,
            generated_at=generated_at,
            snapshot=snapshot,
            book_root=book_root,
            goal=args.goal.strip(),
            completed=[item.strip() for item in args.completed if item.strip()],
            next_steps=[item.strip() for item in args.next_step if item.strip()],
            risks=[item.strip() for item in args.risk if item.strip()],
        ),
        encoding="utf-8",
    )
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
