#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import re
import tempfile
import threading
import xml.etree.ElementTree as ET
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

from workflow_obsidian import default_obsidian_dest
from workflow_rules import resolve_book_root, resolve_repo_path
from workflow_subprocess import (
    DEFAULT_TIMEOUT_SECONDS,
    SHORT_TIMEOUT_SECONDS,
    WorkflowSubprocessError,
    run_checked_subprocess,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STORAGE_STATE = Path("~/.cache/codex-whimsical/storage-state.json").expanduser()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a Whimsical board from manifest as a clean PNG via official /svg export."
    )
    parser.add_argument("figure_id", nargs="?", help="Manifest figure_id to render.")
    parser.add_argument(
        "--book-root",
        help="Optional books/<slug> root. If omitted, uses MEDBOOK_ROOT.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="Path to manifest.tsv. Defaults to <book-root>/lt/figures/manifest.tsv.",
    )
    parser.add_argument(
        "--storage-state",
        type=Path,
        default=DEFAULT_STORAGE_STATE,
        help="Playwright storage-state JSON used for authenticated Whimsical access.",
    )
    parser.add_argument(
        "--login",
        action="store_true",
        help="Open a headed browser so you can log into Whimsical and save storage state.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=2400,
        help="Target PNG width in pixels after SVG conversion.",
    )
    parser.add_argument(
        "--padding",
        type=int,
        default=72,
        help="Extra padding to keep around the final PNG.",
    )
    parser.add_argument(
        "--sync-obsidian",
        action="store_true",
        help="After rendering, sync updated chapters/figures into the Obsidian vault.",
    )
    parser.add_argument(
        "--obsidian-dest",
        type=Path,
        help="Obsidian destination used when --sync-obsidian is set. Defaults to the path resolved from repo_config.toml.",
    )
    return parser.parse_args()


def infer_book_root(book_root_arg: str | None, manifest_path: Path | None) -> Path | None:
    book_root = resolve_book_root(book_root_arg)
    if book_root is not None:
        return book_root
    if manifest_path is not None:
        return manifest_path.resolve().parents[2]
    return None


def ensure_inkscape() -> None:
    try:
        run_checked_subprocess(
            ["inkscape", "--version"],
            phase="probe Inkscape runtime",
            timeout=SHORT_TIMEOUT_SECONDS,
            capture_output=True,
            text=True,
        )
    except WorkflowSubprocessError as exc:
        raise SystemExit(str(exc)) from exc


def load_manifest_row(manifest_path: Path, figure_id: str) -> dict[str, str]:
    with manifest_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            if row["figure_id"] == figure_id:
                return row
    raise SystemExit(f"Figure ID not found in manifest: {figure_id}")


def login_whimsical(storage_state_path: Path) -> None:
    storage_state_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1600, "height": 1200})
        page = context.new_page()
        page.goto("https://whimsical.com/login", wait_until="domcontentloaded", timeout=60000)
        print()
        print("Log into Whimsical in the opened browser window.")
        input("When login is complete, press Enter here to save the session...")
        context.storage_state(path=str(storage_state_path))
        browser.close()
    print(f"Saved Whimsical session to {storage_state_path}")


def fetch_svg(board_url: str, storage_state_path: Path) -> str:
    if not storage_state_path.exists():
        raise SystemExit(
            f"Whimsical session file not found: {storage_state_path}\n"
            "Run with --login first."
        )
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=str(storage_state_path),
            viewport={"width": 1600, "height": 2400},
        )
        page = context.new_page()
        page.goto(board_url, wait_until="domcontentloaded", timeout=60000)
        if "log in" in page.title().lower():
            browser.close()
            raise SystemExit("Whimsical session has expired. Re-run with --login.")
        svg_url = board_url.rstrip("/") + "/svg"
        payload = page.evaluate(
            """async (url) => {
                const response = await fetch(url, { credentials: 'include' });
                return {
                    status: response.status,
                    contentType: response.headers.get('content-type'),
                    text: await response.text(),
                };
            }""",
            svg_url,
        )
        browser.close()
    if payload["status"] != 200 or "svg" not in (payload["contentType"] or ""):
        raise SystemExit(
            f"Unexpected SVG response from Whimsical: {payload['status']} {payload['contentType']}"
        )
    if not payload["text"].lstrip().startswith("<svg"):
        raise SystemExit("Whimsical returned a non-SVG document. Re-run with --login.")
    return payload["text"]


def parse_dimension(value: str | None) -> float | None:
    if not value:
        return None
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)", value)
    return float(match.group(1)) if match else None


def prepare_svg(svg_text: str, target_width: int) -> tuple[str, int, int]:
    root = ET.fromstring(svg_text)
    width = parse_dimension(root.get("width"))
    height = parse_dimension(root.get("height"))
    view_box = root.get("viewBox")
    if (width is None or height is None) and view_box:
        parts = [float(part) for part in view_box.replace(",", " ").split()]
        if len(parts) == 4:
            width = width or parts[2]
            height = height or parts[3]
    if width is None or height is None:
        raise SystemExit("Could not determine SVG dimensions.")
    scaled_height = int(round(target_width * (height / width)))
    root.set("width", str(target_width))
    root.set("height", str(scaled_height))
    return ET.tostring(root, encoding="unicode"), target_width, scaled_height


def render_svg_to_png_browser(svg_text: str, png_path: Path, width: int, padding: int) -> None:
    prepared_svg, render_width, render_height = prepare_svg(svg_text, width)
    with tempfile.TemporaryDirectory(prefix="whimsical-browser-render-") as tmpdir:
        root = Path(tmpdir)
        (root / "figure.svg").write_text(prepared_svg, encoding="utf-8")

        class QuietHandler(SimpleHTTPRequestHandler):
            def log_message(self, format: str, *args) -> None:
                return

        handler = partial(QuietHandler, directory=str(root))
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True)
                page = browser.new_page(
                    viewport={
                        "width": render_width,
                        "height": min(1600, render_height),
                    }
                )
                page.goto(f"http://127.0.0.1:{port}/figure.svg", wait_until="load", timeout=60000)
                page.wait_for_timeout(2000)
                page.locator("svg").screenshot(path=str(png_path))
                browser.close()
        finally:
            server.shutdown()
            thread.join(timeout=1)
    if padding > 0:
        add_padding_to_png(png_path, padding)


def add_padding_to_png(png_path: Path, padding: int) -> None:
    with Image.open(png_path) as source:
        canvas = Image.new("RGBA", (source.width + padding * 2, source.height + padding * 2), "white")
        canvas.paste(source, (padding, padding))
        canvas.save(png_path)


def convert_svg_to_png(svg_path: Path, png_path: Path, width: int) -> None:
    try:
        run_checked_subprocess(
            [
                "inkscape",
                str(svg_path),
                "--export-type=png",
                f"--export-filename={png_path}",
                f"--export-width={width}",
                "--export-background=white",
                "--export-background-opacity=1",
            ],
            phase="convert SVG to PNG",
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )
    except WorkflowSubprocessError as exc:
        raise SystemExit(str(exc)) from exc


def sync_obsidian(dest: Path, book_root: Path) -> None:
    book_root_rel = book_root.resolve().relative_to(REPO_ROOT)
    try:
        run_checked_subprocess(
            [
                str(REPO_ROOT / "scripts/sync_obsidian_book.sh"),
                "--book-root",
                str(book_root_rel),
                "--dest",
                str(dest),
            ],
            phase="sync Obsidian book",
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )
    except WorkflowSubprocessError as exc:
        raise SystemExit(str(exc)) from exc


def main() -> int:
    args = parse_args()
    manifest_path = args.manifest
    book_root = infer_book_root(args.book_root, manifest_path)
    if manifest_path is None:
        if book_root is None:
            raise SystemExit("Nurodykite --manifest arba nustatykite MEDBOOK_ROOT / --book-root.")
        manifest_path = book_root / "lt" / "figures" / "manifest.tsv"
    else:
        manifest_path = resolve_repo_path(manifest_path)
        book_root = infer_book_root(args.book_root, manifest_path)

    storage_state = args.storage_state.expanduser()
    if args.login:
        login_whimsical(storage_state)
        if not args.figure_id:
            return 0

    if not args.figure_id:
        raise SystemExit("Pass a figure_id or use --login.")

    manifest_row = load_manifest_row(manifest_path, args.figure_id)
    if manifest_row["canonical_source_type"] != "whimsical_board":
        raise SystemExit(
            f"Figure {args.figure_id} is not configured as a Whimsical board in the manifest."
        )

    board_url = manifest_row["canonical_source_path"]
    png_path = REPO_ROOT / manifest_row["png_path"]
    png_path.parent.mkdir(parents=True, exist_ok=True)

    svg_text = fetch_svg(board_url, storage_state)
    try:
        render_svg_to_png_browser(svg_text, png_path, args.width, args.padding)
    except Exception:
        ensure_inkscape()
        with tempfile.TemporaryDirectory(prefix="whimsical-export-") as tmpdir:
            svg_path = Path(tmpdir) / f"{args.figure_id}.svg"
            svg_path.write_text(svg_text, encoding="utf-8")
            convert_svg_to_png(svg_path, png_path, args.width)
    print(f"Rendered {args.figure_id} -> {png_path}")

    if args.sync_obsidian:
        if book_root is None:
            raise SystemExit("Nepavyko nustatyti knygos darbo vietos Obsidian sync veiksmui.")
        obsidian_dest = args.obsidian_dest.expanduser() if args.obsidian_dest else default_obsidian_dest(book_root)
        sync_obsidian(obsidian_dest, book_root)
        print(f"Synced Obsidian vault -> {obsidian_dest}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
