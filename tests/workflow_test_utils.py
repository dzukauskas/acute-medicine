#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
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


def fixture_path(name: str) -> Path:
    path = FIXTURES_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Nerastas test fixture: {path}")
    return path


def copy_fixture(base_dir: Path, fixture_name: str, *, name: str | None = None) -> Path:
    target_name = name or fixture_name.replace("_", "-")
    target = base_dir / target_name
    shutil.copytree(fixture_path(fixture_name), target)
    return target


def copy_mini_book(base_dir: Path, name: str = "mini-book") -> Path:
    return copy_fixture(base_dir, "mini_book", name=name)


def infer_fixture_slug(book_root: Path) -> str:
    chapters_index = book_root / "source" / "index" / "chapters.json"
    if chapters_index.exists():
        data = json.loads(chapters_index.read_text(encoding="utf-8"))
        if len(data) == 1 and data[0].get("slug"):
            return str(data[0]["slug"])

    source_chapters = sorted((book_root / "source" / "chapters-en").glob("*.md"))
    if len(source_chapters) == 1:
        return source_chapters[0].stem

    raise AssertionError(
        f"Nepavyko vienareikšmiškai nustatyti fixture skyriaus slug iš {book_root}."
    )


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


def seed_canonical_artifacts(book_root: Path, slug: str | None = None) -> str:
    resolved_slug = slug or infer_fixture_slug(book_root)
    pack_result = run_script("build_chapter_pack.py", "--book-root", str(book_root), resolved_slug)
    if pack_result.returncode != 0:
        raise AssertionError(pack_result.stdout + pack_result.stderr)

    adjudication_result = run_script("build_adjudication_pack.py", "--book-root", str(book_root), resolved_slug)
    if adjudication_result.returncode != 0:
        raise AssertionError(adjudication_result.stdout + adjudication_result.stderr)
    return resolved_slug


def drop_local_termbase_entry(book_root: Path, source_term: str) -> None:
    termbase_path = book_root / "termbase.local.tsv"
    if not termbase_path.exists():
        raise AssertionError(f"Nerastas local termbase failas: {termbase_path}")

    with termbase_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    kept_rows = [row for row in rows if row.get("en", "").strip() != source_term]
    if len(kept_rows) == len(rows):
        raise AssertionError(
            f"Fixture termbase neturi įrašo `{source_term}` faile {termbase_path}."
        )

    with termbase_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(kept_rows)


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
