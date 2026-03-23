#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / (
    "Acute Medicine A Practical Guide to the Management of Medical Emergencies "
    "(Mridula Rajwani (Editor) etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf"
)
OMEGAT_JAR = Path("/Applications/OmegaT.app/Contents/Java/OmegaT.jar")


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def export_glossary(termbase_path: Path, glossary_path: Path) -> None:
    rows: list[tuple[str, str, str]] = []
    with termbase_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            source = row["en"].strip()
            target = row["lt"].strip()
            note = row.get("note", "").strip()
            if not source:
                continue
            rows.append((source, target, note))

    with glossary_path.open("w", encoding="utf-8", newline="") as f:
        for source, target, note in rows:
            f.write(f"{source}\t{target}\t{note}\n")


def reset_dir(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        for child in path.iterdir():
            if child.is_symlink() or child.is_file():
                child.unlink()
            elif child.is_dir():
                reset_dir(child)
                child.rmdir()
    else:
        path.mkdir(parents=True, exist_ok=True)


def sync_source_files(en_dir: Path, source_dir: Path, manifest_path: Path) -> None:
    source_dir.mkdir(parents=True, exist_ok=True)
    lines = ["omegat_source\toriginal_markdown"]
    for md_file in sorted(en_dir.glob("*.md")):
        txt_name = md_file.stem + ".txt"
        target_file = source_dir / txt_name
        target_file.write_text(md_file.read_text(encoding="utf-8"), encoding="utf-8")
        lines.append(f"{txt_name}\t{md_file.name}")
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Set up an OmegaT project for chapter-by-chapter EN->LT translation.")
    parser.add_argument("--project-dir", default="study/omegat", help="OmegaT project directory.")
    args = parser.parse_args()

    study_dir = ROOT / "study"
    en_dir = study_dir / "en"
    termbase_path = study_dir / "termbase.tsv"
    project_dir = ROOT / args.project_dir

    run([".venv/bin/python", "scripts/extract_chapters.py", "--all"], cwd=ROOT)

    if project_dir.exists():
        if not project_dir.is_dir():
            raise RuntimeError(f"{project_dir} exists and is not a directory.")
    else:
        project_dir.mkdir(parents=True)

    if not (project_dir / "omegat.project").exists():
        run(["java", "-jar", str(OMEGAT_JAR), "team", "init", "en", "lt"], cwd=project_dir)

    for rel in [
        "target",
        "tm",
        "tm/auto",
        "tm/enforce",
        "tm/mt",
        "glossary",
        "dictionary",
        "omegat",
    ]:
        (project_dir / rel).mkdir(parents=True, exist_ok=True)

    source_dir = project_dir / "source"
    if source_dir.exists():
        reset_dir(source_dir)
    source_dir.mkdir(parents=True, exist_ok=True)
    sync_source_files(en_dir, source_dir, project_dir / "source_manifest.tsv")

    export_glossary(termbase_path, project_dir / "glossary" / "glossary.txt")

    readme = project_dir / "README.md"
    readme.write_text(
        "\n".join(
            [
                "# OmegaT Project",
                "",
                "- Source language: English (`en`)",
                "- Target language: Lithuanian (`lt`)",
                "- Source files: generated `.txt` mirror of `study/en/` for OmegaT compatibility",
                "- Glossary: `glossary/glossary.txt` generated from `study/termbase.tsv`",
                "",
                "Open this folder in OmegaT to translate chapter files from `source/`.",
                "Translated output files are generated in `target/`.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(project_dir)


if __name__ == "__main__":
    main()
