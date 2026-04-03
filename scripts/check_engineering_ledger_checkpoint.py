#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys

from workflow_engineering_ledger import CHECKPOINT_SECTION_KEYS, ensure_sections, extract_section, extract_theme_label
from workflow_runtime import REPO_ROOT


LEDGER_PATH = "ENGINEERING_LEDGER.md"
EXIT_OK = 0
EXIT_POLICY = 1
EXIT_GIT_ERROR = 2
ENGINEERING_SCOPE_RULES = {
    "root_files": frozenset(
        {
            ".gitignore",
            "AGENTS.md",
            "Brewfile",
            "ENGINEERING_LEDGER.md",
            "repo_config.example.toml",
            "repo_config.toml",
            "requirements-dev.txt",
            "requirements.txt",
        }
    ),
    "root_dirs": frozenset({".github", "codex", "docs", "plans", "scripts", "tests"}),
    "exact_paths": frozenset({"books/README.md", "handoffs/README.md"}),
    "prefixes": ("books/_template/",),
}
CHECKPOINT_SECTION_LABELS = {
    "active_theme": "Active Theme",
    "summary": "Summary",
    "current_state": "Current State",
    "next_steps": "Next Steps",
    "completed": "Completed Themes",
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fail repo-engineering diffs that do not include a meaningful ENGINEERING_LEDGER checkpoint."
    )
    parser.add_argument("--base-ref", required=True, help="Base git ref used to compute merge-base.")
    parser.add_argument("--head-ref", required=True, help="Head git ref used to compute the diff window.")
    return parser.parse_args(argv)


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def normalize_repo_path(path: str) -> str:
    normalized = path.strip().replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def is_repo_engineering_path(path: str) -> bool:
    normalized = normalize_repo_path(path)
    if not normalized:
        return False
    if normalized in ENGINEERING_SCOPE_RULES["root_files"]:
        return True
    if normalized in ENGINEERING_SCOPE_RULES["exact_paths"]:
        return True
    if any(normalized.startswith(prefix) for prefix in ENGINEERING_SCOPE_RULES["prefixes"]):
        return True
    first_segment = normalized.split("/", 1)[0]
    return first_segment in ENGINEERING_SCOPE_RULES["root_dirs"]


def guard_trigger_paths(changed_paths: list[str]) -> list[str]:
    return [
        normalized
        for normalized in (normalize_repo_path(path) for path in changed_paths)
        if normalized != LEDGER_PATH and is_repo_engineering_path(normalized)
    ]


def normalize_section_body(body: str) -> str:
    return "\n".join(line.strip() for line in body.splitlines() if line.strip())


def active_theme_value(text: str) -> str:
    return extract_theme_label(extract_section(text, "active_theme"))


def meaningful_changed_sections(base_text: str, head_text: str) -> list[str]:
    ensure_sections(base_text)
    ensure_sections(head_text)

    changed: list[str] = []
    for key in CHECKPOINT_SECTION_KEYS:
        if key == "active_theme":
            if active_theme_value(base_text) != active_theme_value(head_text):
                changed.append(CHECKPOINT_SECTION_LABELS[key])
            continue
        if normalize_section_body(extract_section(base_text, key)) != normalize_section_body(extract_section(head_text, key)):
            changed.append(CHECKPOINT_SECTION_LABELS[key])
    return changed

def verify_commit_ref(ref: str, label: str) -> str:
    result = run_git("rev-parse", "--verify", f"{ref}^{{commit}}")
    if result.returncode != 0:
        raise RuntimeError(
            f"Nepavyko rasti {label} ref `{ref}` lokaliame git objekte. "
            f"Patikrinkite, kad CI checkout turi reikiamą istoriją.\n{result.stderr.strip()}".strip()
        )
    return result.stdout.strip()


def read_ledger_at_ref(ref: str) -> str:
    result = run_git("show", f"{ref}:{LEDGER_PATH}")
    if result.returncode != 0:
        raise RuntimeError(
            f"Nepavyko perskaityti `{LEDGER_PATH}` iš ref `{ref}`.\n{result.stderr.strip()}".strip()
        )
    return result.stdout


def merge_base(base_ref: str, head_ref: str) -> str:
    result = run_git("merge-base", base_ref, head_ref)
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError(
            f"Nepavyko rasti merge-base tarp `{base_ref}` ir `{head_ref}`. "
            "Diff-aware ledger gate reikalauja bendro commit protėvio."
        )
    return result.stdout.strip()


def changed_paths_between(base_ref: str, head_ref: str) -> list[str]:
    result = run_git("diff", "--name-only", f"{base_ref}..{head_ref}")
    if result.returncode != 0:
        raise RuntimeError(
            f"Nepavyko apskaičiuoti pakeistų failų tarp `{base_ref}` ir `{head_ref}`.\n{result.stderr.strip()}".strip()
        )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        base_commit = verify_commit_ref(args.base_ref, "base")
        head_commit = verify_commit_ref(args.head_ref, "head")
        diff_base = merge_base(base_commit, head_commit)
        changed_paths = changed_paths_between(diff_base, head_commit)
        trigger_paths = guard_trigger_paths(changed_paths)
        if not trigger_paths:
            print(
                "Engineering ledger checkpoint gate skipped: no repo-engineering diff beyond "
                f"`{LEDGER_PATH}` in {diff_base}..{head_commit}."
            )
            return EXIT_OK

        base_ledger = read_ledger_at_ref(diff_base)
        head_ledger = read_ledger_at_ref(head_commit)
        changed_sections = meaningful_changed_sections(base_ledger, head_ledger)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_GIT_ERROR
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_GIT_ERROR

    if changed_sections:
        print(
            "Engineering ledger checkpoint gate passed: meaningful checkpoint detected in "
            f"{diff_base}..{head_commit} ({', '.join(changed_sections)})."
        )
        return EXIT_OK

    print(
        "Repo-engineering diff requires a meaningful `ENGINEERING_LEDGER.md` checkpoint.\n"
        f"Changed repo-engineering paths: {', '.join(trigger_paths)}\n"
        "Sufficient sections for this CI guard policy: Active Theme (`Theme:` line only), "
        "Summary, Current State, Next Steps, Completed Themes.\n"
        "Guard policy note: `Accepted Decisions` and `Open Risks` remain valid ledger sections, "
        "but by themselves do not satisfy this checkpoint gate.\n"
        "Timestamp-only, branch-only, or whitespace-only ledger churn does not satisfy the gate."
    )
    return EXIT_POLICY


if __name__ == "__main__":
    raise SystemExit(main())
