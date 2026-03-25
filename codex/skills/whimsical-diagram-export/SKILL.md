---
name: whimsical-diagram-export
description: Use this skill when refreshing a repo PNG from a Whimsical board, especially when image quality matters, browser screenshots are blurry, or the board must be synced into Obsidian. It uses the official Whimsical /svg export route first, then rasterizes that SVG through Chromium with the repo script.
---

# Whimsical Diagram Export

Use this skill when a figure's canonical source is a `Whimsical` board and the repo needs a clean `PNG`.

## Default workflow

1. Treat the `Whimsical` board as the only editable source.
2. Prefer the official `.../svg` export over screenshot-based export.
3. Render the final `PNG` with:

```bash
.venv/bin/python scripts/render_whimsical_figure.py <figure_id>
```

4. If the Whimsical session is missing or expired, refresh auth first:

```bash
.venv/bin/python scripts/render_whimsical_figure.py --login
```

5. If the figure should appear in Obsidian immediately, run:

```bash
.venv/bin/python scripts/render_whimsical_figure.py <figure_id> --sync-obsidian
```

## Why this workflow

- Whimsical's normal PNG export can be blurry or limited.
- Whimsical officially recommends the experimental `/svg` route when exports fail or look blurry.
- The repo script renders the authenticated SVG export through Chromium so text metrics stay faithful to Whimsical, then falls back to `Inkscape` only if browser rasterization fails.

## Rules

- Do not keep manual browser screenshots as the final asset if `/svg` export works.
- Do not add a second editable source next to the Whimsical board.
- Keep the board URL and the target PNG path in the active book's `lt/figures/manifest.tsv`.
- After rendering, sync to Obsidian if the user wants live vault updates.
- Do not leave long Lithuanian headings sitting right on the note edge in Whimsical. If a title only barely fits, widen the block before export.
- If the exported PNG shows text touching a block edge, clipped text, or visibly smaller padding than in Whimsical, fix the board layout first and then re-render.

## Export QA

Before considering a figure done, visually check the rendered PNG:

1. Long titles still show visible inner padding on both sides.
2. No text line is clipped or pushed flush against a colored block edge.
3. The exported PNG matches the Whimsical board, especially in dense 2×2 note grids.
4. If Lithuanian text expands more than expected, widen the block instead of relying on renderer hacks.

## Current project paths

- Manifest: `books/<slug>/lt/figures/manifest.tsv`
- Renderer: `scripts/render_whimsical_figure.py`
- Obsidian sync: `scripts/sync_obsidian_book.sh`

## When to fall back

Only fall back to a screenshot-based export when:

- the `/svg` route fails even with a valid session;
- the board contains content that Whimsical's SVG export renders incorrectly;
- the user explicitly asks for a screenshot-based capture.
