#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from book_workflow_support import activate_book_root, dump_yaml, load_yaml, read_tsv, require_book_root, resolve_chapter_slug, split_multi


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a targeted adjudication pack for high-risk blocks.")
    parser.add_argument("--book-root", help="Optional books/<slug> root. If omitted, uses MEDBOOK_ROOT.")
    parser.add_argument("chapter", help="Chapter slug or number.")
    parser.add_argument(
        "--out",
        help="Optional output path. Defaults to $MEDBOOK_ROOT/adjudication_packs/<slug>.yaml.",
    )
    return parser.parse_args()


def book_paths() -> dict[str, Path]:
    book_root = require_book_root()
    return {
        "profiles": book_root / "adjudication_profiles.tsv",
        "scaffold": book_root / "adjudication_scaffold.md",
        "chapter_packs": book_root / "chapter_packs",
        "adjudication_packs": book_root / "adjudication_packs",
    }


def load_profiles() -> dict[str, dict[str, object]]:
    profiles: dict[str, dict[str, object]] = {}
    for row in read_tsv(book_paths()["profiles"]):
        profiles[row["profile_id"]] = {
            "profile_id": row["profile_id"],
            "applies_to_block_types": split_multi(row.get("applies_to_block_types", "")),
            "requires_tags": split_multi(row.get("requires_tags", "")),
            "variant_a_goal": row.get("variant_a_goal", ""),
            "variant_b_goal": row.get("variant_b_goal", ""),
            "decision_criteria": row.get("decision_criteria", ""),
        }
    return profiles


def block_matches_override(block: dict, override: dict) -> bool:
    haystack = " ".join(
        [
            block.get("heading", ""),
            block.get("source_anchor", ""),
            " ".join(block.get("tags", [])),
        ]
    ).lower()
    return override.get("source_term", "").lower() in haystack


def relevant_hotspots(block: dict, pack: dict) -> list[dict]:
    block_blob = " ".join(
        [
            block.get("heading", ""),
            block.get("source_anchor", ""),
            " ".join(block.get("tags", [])),
            " ".join(block.get("risk_flags", [])),
        ]
    ).lower()
    selected: list[dict] = []
    for hotspot in pack.get("style_hotspots", []):
        hotspot_blob = hotspot.get("text", "").lower()
        if any(token in hotspot_blob for token in block.get("tags", [])) or any(
            token in hotspot_blob for token in block.get("risk_flags", [])
        ):
            selected.append(hotspot)
            continue
        if any(term in block_blob for term in hotspot_blob.split()[:3]):
            selected.append(hotspot)
    return selected[:6]


def choose_profile_from_profiles(block: dict, profiles: dict[str, dict[str, object]]) -> tuple[dict[str, object] | None, str]:
    block_type = block.get("block_type", "")
    tags = set(block.get("tags", []))

    best_profile: dict[str, object] | None = None
    best_score = -1
    best_reason = ""

    for profile in profiles.values():
        allowed_block_types = set(profile.get("applies_to_block_types", []))
        required_tags = set(profile.get("requires_tags", []))
        if allowed_block_types and block_type not in allowed_block_types:
            continue

        matched_tags = sorted(required_tags & tags)
        if required_tags and not matched_tags:
            continue

        score = len(matched_tags)
        if score > best_score:
            best_profile = profile
            best_score = score
            if matched_tags:
                best_reason = (
                    f"Matched profile `{profile['profile_id']}` via block_type `{block_type}` "
                    f"and tags {', '.join(matched_tags)}."
                )
            else:
                best_reason = f"Matched profile `{profile['profile_id']}` via block_type `{block_type}`."

    return best_profile, best_reason


def choose_profile_fallback(block: dict, profiles: dict[str, dict[str, object]]) -> tuple[dict[str, object] | None, str]:
    block_type = block.get("block_type", "")
    tags = set(block.get("tags", []))

    if block_type == "algorithm":
        return profiles.get("algorithm-stepwise"), "Fallback selected algorithm profile for block_type `algorithm`."
    if block_type in {"legal_localization", "chart"}:
        return profiles.get("local-context-callout"), (
            "Fallback selected local-context profile for legal_localization/chart block."
        )
    if tags & {"uk-localization", "legal-localization"}:
        return profiles.get("local-context-callout"), (
            "Fallback selected local-context profile from localization-oriented tags."
        )
    if tags & {"hemodynamic", "complex-prose"} or "complex_prose" in block.get("risk_flags", []):
        return profiles.get("hemodynamic-prose"), (
            "Fallback selected hemodynamic prose profile from tags or complex_prose risk."
        )
    if block_type == "callout":
        return profiles.get("local-context-callout"), "Fallback selected local-context profile for block_type `callout`."
    return None, ""


def is_high_risk(block: dict, pack: dict) -> bool:
    if block.get("adjudication_candidate"):
        return True
    if block.get("block_type") in {"algorithm", "legal_localization", "chart"}:
        return True
    if any(block_matches_override(block, override) for override in pack.get("localization_overrides", [])):
        return True
    return False


def build_pack(slug: str) -> dict[str, object]:
    paths = book_paths()
    pack_path = paths["chapter_packs"] / f"{slug}.yaml"
    pack = load_yaml(pack_path)
    profiles = load_profiles()

    candidates: list[dict[str, object]] = []
    for block in pack.get("blocks", []):
        if not is_high_risk(block, pack):
            continue
        profile, selection_reason = choose_profile_from_profiles(block, profiles)
        selection_mode = "profile_match"
        if profile is None:
            profile, selection_reason = choose_profile_fallback(block, profiles)
            selection_mode = "fallback"
        if profile is None:
            continue
        matched_overrides = [
            override for override in pack.get("localization_overrides", []) if block_matches_override(block, override)
        ]
        candidates.append(
            {
                "block_id": block.get("block_id"),
                "block_type": block.get("block_type"),
                "heading": block.get("heading"),
                "source_anchor": block.get("source_anchor"),
                "draft_mode": block.get("draft_mode"),
                "tags": block.get("tags", []),
                "risk_flags": block.get("risk_flags", []),
                "profile_id": profile["profile_id"],
                "selection_mode": selection_mode,
                "selection_reason": selection_reason,
                "decision_note_required": True,
                "variant_a_goal": profile["variant_a_goal"],
                "variant_b_goal": profile["variant_b_goal"],
                "decision_criteria": profile["decision_criteria"],
                "relevant_style_hotspots": relevant_hotspots(block, pack),
                "matched_localization_overrides": matched_overrides,
            }
        )

    return {
        "chapter_slug": slug,
        "chapter_pack": str(pack_path),
        "source_md": pack.get("source_md", ""),
        "lt_target_md": pack.get("lt_target_md", ""),
        "scaffold": str(paths["scaffold"]),
        "candidates": candidates,
    }


def main() -> int:
    args = parse_args()
    activate_book_root(args.book_root)
    slug = resolve_chapter_slug(args.chapter, args.book_root)
    data = build_pack(slug)
    output_path = Path(args.out) if args.out else book_paths()["adjudication_packs"] / f"{slug}.yaml"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dump_yaml(output_path, data)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
