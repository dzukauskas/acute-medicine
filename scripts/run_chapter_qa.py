#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from book_workflow_support import chapter_paths_for_slug, load_yaml, normalize_yaml_structure, resolve_chapter_slug


SCRIPT_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the canonical chapter QA pipeline against a fresh and semantically current chapter pack."
    )
    parser.add_argument("chapter", help="Chapter slug or number.")
    return parser.parse_args()


def run_step(label: str, args: list[str]) -> None:
    completed = subprocess.run(args, capture_output=True, text=True)
    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.stderr:
        print(completed.stderr.rstrip(), file=sys.stderr)
    if completed.returncode != 0:
        raise RuntimeError(f"{label} failed with exit code {completed.returncode}.")


def main() -> int:
    args = parse_args()
    slug = resolve_chapter_slug(args.chapter)
    paths = chapter_paths_for_slug(slug)
    lt_target = paths["lt"]
    pack_path = paths["pack"]

    run_step(
        "inventory validation",
        [sys.executable, str(SCRIPT_DIR / "validate_chapter_inventory.py"), slug],
    )

    if not pack_path.exists():
        raise SystemExit(
            f"Kanoninis chapter_pack neegzistuoja: {pack_path}\n"
            f"Pirma sugeneruokite jį per `python3 scripts/build_chapter_pack.py {slug}`."
        )

    with tempfile.TemporaryDirectory(prefix=f"{slug}-qa-") as temp_dir:
        temp_pack = Path(temp_dir) / f"{slug}.yaml"
        run_step(
            "fresh chapter_pack build",
            [
                sys.executable,
                str(SCRIPT_DIR / "build_chapter_pack.py"),
                slug,
                "--out",
                str(temp_pack),
            ],
        )

        canonical = normalize_yaml_structure(load_yaml(pack_path))
        fresh = normalize_yaml_structure(load_yaml(temp_pack))
        if canonical != fresh:
            raise SystemExit(
                f"Kanoninis chapter_pack pasenęs: {pack_path}\n"
                f"Šviežiai sugeneruotas pack semantiškai skiriasi. "
                f"Pirma persigeneruokite `python3 scripts/build_chapter_pack.py {slug}`."
            )

        run_step(
            "terminology_guard",
            [
                sys.executable,
                str(SCRIPT_DIR / "terminology_guard.py"),
                str(lt_target),
                "--chapter-pack",
                str(temp_pack),
            ],
        )
        run_step(
            "prose_guard",
            [sys.executable, str(SCRIPT_DIR / "prose_guard.py"), str(lt_target)],
        )
        run_step(
            "lt_style_guard",
            [sys.executable, str(SCRIPT_DIR / "lt_style_guard.py"), str(lt_target)],
        )
        run_step(
            "completeness_guard",
            [sys.executable, str(SCRIPT_DIR / "completeness_guard.py"), str(temp_pack)],
        )

    print(f"Chapter QA passed for {slug}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
