#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

from workflow_book import chapter_paths_for_slug, load_yaml, normalize_yaml_structure, resolve_chapter_slug
from workflow_rules import activate_book_root
from workflow_subprocess import (
    DEFAULT_TIMEOUT_SECONDS,
    LONG_TIMEOUT_SECONDS,
    WorkflowSubprocessError,
    format_failure_message,
    run_subprocess,
)


SCRIPT_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the canonical chapter QA pipeline against a fresh and semantically current chapter pack."
    )
    parser.add_argument("--book-root", help="Optional books/<slug> root. If omitted, uses MEDBOOK_ROOT.")
    parser.add_argument("chapter", help="Chapter slug or number.")
    return parser.parse_args()


def run_step(label: str, args: list[str], *, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> None:
    try:
        completed = run_subprocess(
            args,
            phase=label,
            timeout=timeout,
            capture_output=True,
            text=True,
        )
    except WorkflowSubprocessError as exc:
        raise RuntimeError(str(exc)) from exc
    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.stderr:
        print(completed.stderr.rstrip(), file=sys.stderr)
    if completed.returncode != 0:
        raise RuntimeError(
            format_failure_message(
                label,
                args,
                completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
            )
        )


def main() -> int:
    args = parse_args()
    activate_book_root(args.book_root)
    slug = resolve_chapter_slug(args.chapter, args.book_root)
    paths = chapter_paths_for_slug(slug)
    lt_target = paths["lt"]
    pack_path = paths["pack"]
    book_root = args.book_root or os.environ.get("MEDBOOK_ROOT", "")

    run_step(
        "inventory validation",
        [sys.executable, str(SCRIPT_DIR / "validate_chapter_inventory.py"), "--book-root", book_root, slug] if book_root else [sys.executable, str(SCRIPT_DIR / "validate_chapter_inventory.py"), slug],
    )
    run_step(
        "localization readiness",
        [sys.executable, str(SCRIPT_DIR / "validate_localization_readiness.py"), "--book-root", book_root, slug] if book_root else [sys.executable, str(SCRIPT_DIR / "validate_localization_readiness.py"), slug],
    )
    run_step(
        "figure manifest validation",
        [sys.executable, str(SCRIPT_DIR / "validate_figures_manifest.py"), "--book-root", book_root, slug] if book_root else [sys.executable, str(SCRIPT_DIR / "validate_figures_manifest.py"), slug],
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
                *([] if not book_root else ["--book-root", book_root]),
                slug,
                "--out",
                str(temp_pack),
            ],
            timeout=LONG_TIMEOUT_SECONDS,
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
            "adjudication resolution",
            [
                sys.executable,
                str(SCRIPT_DIR / "validate_adjudication_resolution.py"),
                *([] if not book_root else ["--book-root", book_root]),
                slug,
            ],
            timeout=LONG_TIMEOUT_SECONDS,
        )

        run_step(
            "terminology_guard",
            [
                sys.executable,
                str(SCRIPT_DIR / "terminology_guard.py"),
                *([] if not book_root else ["--book-root", book_root]),
                str(lt_target),
                "--chapter-pack",
                str(temp_pack),
            ],
        )
        run_step(
            "localization_guard",
            [
                sys.executable,
                str(SCRIPT_DIR / "localization_guard.py"),
                str(lt_target),
                "--chapter-pack",
                str(temp_pack),
            ],
        )
        run_step(
            "prose_guard",
            [sys.executable, str(SCRIPT_DIR / "prose_guard.py"), *([] if not book_root else ["--book-root", book_root]), str(lt_target)],
        )
        run_step(
            "lt_style_guard",
            [sys.executable, str(SCRIPT_DIR / "lt_style_guard.py"), *([] if not book_root else ["--book-root", book_root]), str(lt_target)],
        )
        run_step(
            "completeness_guard",
            [sys.executable, str(SCRIPT_DIR / "completeness_guard.py"), *([] if not book_root else ["--book-root", book_root]), str(temp_pack)],
        )
        run_step(
            "manual audit validation",
            [
                sys.executable,
                str(SCRIPT_DIR / "validate_manual_audit.py"),
                *([] if not book_root else ["--book-root", book_root]),
                slug,
            ],
        )

    print(f"Chapter QA passed for {slug}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
