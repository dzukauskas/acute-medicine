#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
MINI_BOOK_FIXTURE = FIXTURES_DIR / "mini_book"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def copy_mini_book(base_dir: Path, name: str = "mini-book") -> Path:
    target = base_dir / name
    shutil.copytree(MINI_BOOK_FIXTURE, target)
    return target


def run_script(script_name: str, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script_name), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        env=merged_env,
    )


def seed_canonical_artifacts(book_root: Path, slug: str = "001-mini") -> None:
    pack_result = run_script("build_chapter_pack.py", "--book-root", str(book_root), slug)
    if pack_result.returncode != 0:
        raise AssertionError(pack_result.stdout + pack_result.stderr)

    adjudication_result = run_script("build_adjudication_pack.py", "--book-root", str(book_root), slug)
    if adjudication_result.returncode != 0:
        raise AssertionError(adjudication_result.stdout + adjudication_result.stderr)


def assert_mini_book_governance_contract(chapter_path: Path) -> None:
    text = chapter_path.read_text(encoding="utf-8")
    required_fragments = (
        "## Ankstyvas įvertinimas",
        "ta pačia tvarka kaip originale",
        "pagrindinę stebėjimų seką",
        "## Lietuvos kompensavimo tvarka",
        "## 1.1 paveikslas",
        "Originalo kontekstas",
        "Custom UK Tool",
    )
    missing = [fragment for fragment in required_fragments if fragment not in text]
    if missing:
        raise AssertionError(f"Mini-book governance contract broken; missing fragments: {missing}")
