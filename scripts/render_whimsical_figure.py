#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import csv
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from playwright.sync_api import sync_playwright


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = REPO_ROOT / "books/acute-medicine/lt/figures/manifest.tsv"
DEFAULT_STORAGE_STATE = Path("~/.cache/acute-medicine/whimsical-storage-state.json").expanduser()
DEFAULT_OBSIDIAN_DEST = Path(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/PARAMEDIKAS/Acute Medicine"
).expanduser()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a Whimsical board from manifest as a clean PNG via official /svg export."
    )
    parser.add_argument("figure_id", nargs="?", help="Manifest figure_id to render.")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="Path to manifest.tsv.",
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
        default=DEFAULT_OBSIDIAN_DEST,
        help="Obsidian destination used when --sync-obsidian is set.",
    )
    return parser.parse_args()


def ensure_inkscape() -> None:
    subprocess.run(["inkscape", "--version"], check=True, capture_output=True, text=True)


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
    svg_data_url = "data:image/svg+xml;base64," + base64.b64encode(
        prepared_svg.encode("utf-8")
    ).decode("ascii")
    html = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <style>
      html, body {{
        margin: 0;
        padding: 0;
        background: white;
      }}
      #frame {{
        display: inline-block;
        padding: {padding}px;
        background: white;
      }}
      img {{
        display: block;
        width: {render_width}px;
        height: {render_height}px;
      }}
    </style>
  </head>
  <body>
    <div id="frame"><img id="diagram" src="{svg_data_url}" alt=""></div>
  </body>
</html>
"""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": render_width + padding * 2, "height": min(1200, render_height + padding * 2)},
            device_scale_factor=1,
        )
        page = context.new_page()
        page.set_content(html, wait_until="load")
        page.locator("#diagram").wait_for()
        page.wait_for_timeout(1000)
        page.locator("#frame").screenshot(path=str(png_path))
        browser.close()


def convert_svg_to_png(svg_path: Path, png_path: Path, width: int) -> None:
    subprocess.run(
        [
            "inkscape",
            str(svg_path),
            "--export-type=png",
            f"--export-filename={png_path}",
            f"--export-width={width}",
            "--export-background=white",
            "--export-background-opacity=1",
        ],
        check=True,
    )


def sync_obsidian(dest: Path) -> None:
    subprocess.run(
        [str(REPO_ROOT / "scripts/sync_obsidian_acute_medicine.sh"), str(dest)],
        check=True,
    )


def main() -> int:
    args = parse_args()
    storage_state = args.storage_state.expanduser()
    if args.login:
        login_whimsical(storage_state)
        if not args.figure_id:
            return 0

    if not args.figure_id:
        raise SystemExit("Pass a figure_id or use --login.")

    manifest_row = load_manifest_row(args.manifest, args.figure_id)
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
        sync_obsidian(args.obsidian_dest.expanduser())
        print(f"Synced Obsidian vault -> {args.obsidian_dest.expanduser()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
