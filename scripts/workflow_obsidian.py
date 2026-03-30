#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from pathlib import Path

from workflow_rules import normalize_key, require_book_root
from workflow_runtime import REPO_ROOT, obsidian_config, obsidian_dest_for_title


SECTION_TITLE_RE = re.compile(r"^Section\s+(?P<number>\d+)\s+[–-]\s+(?P<title>.+)$", re.IGNORECASE)
SYNC_OWNER_FILENAME = ".acute-medicine-sync-owner.json"


def resolve_runtime_path(raw: str | Path, *, base_dir: str | Path | None = None) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        anchor = Path(base_dir).expanduser() if base_dir is not None else Path.cwd()
        path = anchor / path
    return path.resolve()


def path_is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def validate_obsidian_sync_destination(
    dest_dir: str | Path,
    book_root: str | Path,
    *,
    repo_root: str | Path = REPO_ROOT,
    cwd: str | Path | None = None,
) -> Path:
    resolved_dest = resolve_runtime_path(dest_dir, base_dir=cwd)
    resolved_repo_root = resolve_runtime_path(repo_root, base_dir=cwd)
    resolved_book_root = resolve_runtime_path(book_root, base_dir=cwd)
    resolved_lt_root = resolved_book_root / "lt"

    for forbidden_root in (resolved_repo_root, resolved_book_root, resolved_lt_root):
        if path_is_within(resolved_dest, forbidden_root):
            raise SystemExit(
                "Nesaugi Obsidian sync paskirtis: "
                f"{resolved_dest}\n"
                "Sync paskirtis negali būti repo viduje, knygos darbo vietoje arba `lt/` kataloge."
            )

    return resolved_dest


def book_slug(book_root: Path) -> str:
    return book_root.name


def book_title_from_readme(book_root: Path) -> str:
    readme_path = book_root / "README.md"
    if readme_path.exists():
        for raw_line in readme_path.read_text(encoding="utf-8").splitlines():
            if raw_line.startswith("# "):
                title = raw_line[2:].strip()
                if title:
                    return title
    return book_root.name.replace("-", " ").title()


def default_obsidian_dest(book_root: Path) -> Path:
    return obsidian_dest_for_title(book_title_from_readme(book_root))


def repo_workspace_id(repo_root: str | Path = REPO_ROOT) -> str:
    resolved = resolve_runtime_path(repo_root)
    return hashlib.sha256(str(resolved).encode("utf-8")).hexdigest()[:8]


def obsidian_launch_agent_label(book_root: Path, *, repo_root: str | Path = REPO_ROOT) -> str:
    return f"{obsidian_config()['launch_agent_prefix']}-{book_slug(book_root)}-{repo_workspace_id(repo_root)}"


def obsidian_sync_owner_path(dest_root: str | Path) -> Path:
    return Path(dest_root) / SYNC_OWNER_FILENAME


def obsidian_sync_owner_payload(book_root: str | Path, *, repo_root: str | Path = REPO_ROOT) -> dict[str, str]:
    resolved_book_root = resolve_runtime_path(book_root)
    resolved_repo_root = resolve_runtime_path(repo_root)
    return {
        "workspace_id": repo_workspace_id(resolved_repo_root),
        "repo_root": str(resolved_repo_root),
        "book_root": str(resolved_book_root),
        "book_slug": book_slug(resolved_book_root),
        "book_title": book_title_from_readme(resolved_book_root),
    }


def claim_obsidian_sync_destination(
    dest_dir: str | Path,
    book_root: str | Path,
    *,
    repo_root: str | Path = REPO_ROOT,
    cwd: str | Path | None = None,
) -> Path:
    resolved_dest = validate_obsidian_sync_destination(
        dest_dir,
        book_root,
        repo_root=repo_root,
        cwd=cwd,
    )
    resolved_dest.mkdir(parents=True, exist_ok=True)
    owner_path = obsidian_sync_owner_path(resolved_dest)
    expected = obsidian_sync_owner_payload(book_root, repo_root=repo_root)

    if owner_path.exists():
        try:
            current = json.loads(owner_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(
                f"Nepavyko perskaityti Obsidian sync owner failo: {owner_path}"
            ) from exc
        current_workspace = str(current.get("workspace_id", "")).strip()
        current_book = str(current.get("book_slug", "")).strip()
        if current_workspace != expected["workspace_id"] or current_book != expected["book_slug"]:
            raise SystemExit(
                "Obsidian sync paskirtis jau rezervuota kitai darbo vietai arba kitai knygai: "
                f"{resolved_dest}\n"
                f"Rasta workspace_id={current_workspace or '_missing_'}, book_slug={current_book or '_missing_'}; "
                f"tikėtasi workspace_id={expected['workspace_id']}, book_slug={expected['book_slug']}."
            )
        return resolved_dest

    owner_path.write_text(
        json.dumps(expected, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return resolved_dest


def chapter_index_path(book_root: str | Path | None = None) -> Path:
    return require_book_root(book_root) / "source" / "index" / "chapters.json"


def load_chapter_index(book_root: str | Path | None = None) -> list[dict[str, object]]:
    path = chapter_index_path(book_root)
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit(f"Netikėtas chapter index formatas: {path}")
    return [item for item in data if isinstance(item, dict)]


def _obsidian_section_folder_name(section_number: int, section_title: str) -> str:
    clean_title = re.sub(r"\s+", " ", section_title.replace("–", "-")).strip(" -")
    return f"{section_number:02d} Section {section_number} - {clean_title}"


def obsidian_chapter_destinations(book_root: str | Path | None = None) -> dict[str, Path]:
    chapters = load_chapter_index(book_root)
    if not chapters:
        return {}

    has_sections = any(
        SECTION_TITLE_RE.match(str(chapter.get("title", "")).strip()) for chapter in chapters
    )
    if not has_sections:
        return {
            str(chapter.get("slug", "")).strip(): Path("chapters") / f"{str(chapter.get('slug', '')).strip()}.md"
            for chapter in chapters
            if str(chapter.get("slug", "")).strip()
        }

    current_folder = Path("chapters") / "00 Front Matter"
    destinations: dict[str, Path] = {}
    for chapter in chapters:
        slug = str(chapter.get("slug", "")).strip()
        title = str(chapter.get("title", "")).strip()
        if not slug:
            continue
        section_match = SECTION_TITLE_RE.match(title)
        if section_match:
            current_folder = Path("chapters") / _obsidian_section_folder_name(
                int(section_match.group("number")),
                section_match.group("title"),
            )
            destinations[slug] = current_folder / f"{slug}.md"
            continue
        if normalize_key(title) == "index":
            destinations[slug] = Path("chapters") / "99 Reference" / f"{slug}.md"
            continue
        destinations[slug] = current_folder / f"{slug}.md"
    return destinations


def rewrite_obsidian_chapter_markdown(markdown: str, destination_relpath: Path) -> str:
    chapter_parent = destination_relpath.parent
    target_figures_dir = Path("figures")
    figures_prefix = os.path.relpath(target_figures_dir, start=chapter_parent).replace(os.sep, "/")
    return markdown.replace("../figures/", f"{figures_prefix}/")


def stage_obsidian_sync_tree(book_root: str | Path | None, destination_root: str | Path) -> None:
    active_book_root = require_book_root(book_root)
    destination = Path(destination_root)
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    src_lt_root = active_book_root / "lt"
    src_chapters_dir = src_lt_root / "chapters"
    src_figures_dir = src_lt_root / "figures"

    if src_figures_dir.exists():
        shutil.copytree(src_figures_dir, destination / "figures", dirs_exist_ok=True)

    destinations = obsidian_chapter_destinations(active_book_root)
    for chapter_path in sorted(src_chapters_dir.glob("*.md")):
        destination_relpath = destinations.get(chapter_path.stem, Path("chapters") / chapter_path.name)
        destination_path = destination / destination_relpath
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        markdown = chapter_path.read_text(encoding="utf-8")
        destination_path.write_text(
            rewrite_obsidian_chapter_markdown(markdown, destination_relpath),
            encoding="utf-8",
        )
