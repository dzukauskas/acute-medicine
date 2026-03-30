#!/usr/bin/env python3
from __future__ import annotations

"""Backward-compatible facade for legacy workflow helpers.

New repo code should import from the focused ``workflow_*`` modules directly.
This shim remains only to avoid breaking external/local tooling that may still
import the historical helper surface.
"""

from workflow_book import (
    chapter_number_from_slug,
    chapter_paths_for_slug,
    dump_yaml,
    first_epub_path,
    first_pdf_path,
    first_source_artifact,
    load_yaml,
    normalize_yaml_structure,
    repo_relative_path,
    resolve_chapter_slug,
    scope_allows,
)
from workflow_markdown import (
    extract_inventory,
    extract_source_structured_items,
    find_section_lines,
    find_section_lines_any,
    bullet_items,
    markdown_table_rows,
    metadata_value,
    parse_markdown_sections,
    parse_structured_label,
    source_text_for_policy_checks,
    structured_block_id,
    structured_block_type,
    structured_completion_hint,
)
from workflow_obsidian import (
    book_slug,
    book_title_from_readme,
    default_obsidian_dest,
    load_chapter_index,
    obsidian_chapter_destinations,
    obsidian_launch_agent_label,
    stage_obsidian_sync_tree,
    validate_obsidian_sync_destination,
)
from workflow_policy import (
    AUDIT_STATUSES,
    CLAIM_FINAL_RENDERINGS,
    CLINICAL_CLAIM_TYPES,
    CLINICAL_CLAIM_TYPE_ALIASES,
    CLINICAL_POLICY_MARKER_MATCH_MODES,
    LOCALIZATION_REPLACEMENT_MODES,
    LOCALIZATION_SIGNAL_MATCH_MODES,
    SOURCE_TERM_TO_CONTEXT,
    STRUCTURED_BLOCK_STRATEGIES,
    detect_clinical_policy_topics,
    detect_source_localization_signals,
    extract_adjudication_decisions,
    extract_localization_research,
    jurisdiction_to_pack_context,
    load_acronym_rows,
    load_adjudication_profile_rows,
    load_calque_pattern_rows,
    load_clinical_policy_markers,
    load_disallowed_phrase_rows,
    load_disallowed_term_rows,
    load_gold_phrase_rows,
    load_gold_section_examples,
    load_localization_overrides,
    load_localization_signal_specs,
    load_lt_source_map,
    load_review_taxonomy_rows,
    load_term_candidate_rows,
    load_termbase_rows,
    normalize_audit_status,
    normalize_authority_basis,
    normalize_claim_final_rendering,
    normalize_claim_type,
    normalize_clinical_policy_marker_row,
    normalize_localization_override_row,
    normalize_localization_signal_row,
    normalize_structured_block_strategy,
    source_has_clinical_normative_content,
    term_matches,
)
from workflow_rules import (
    BOOK_ROOT_ENV_VAR,
    MARKDOWN_LINK_RE,
    TERM_CANDIDATE_FIELDS,
    activate_book_root,
    acronym_paths,
    adjudication_profile_paths,
    book_local_override_path,
    calque_pattern_paths,
    clinical_policy_markers_path,
    disallowed_phrase_paths,
    disallowed_term_paths,
    gold_phrase_paths,
    gold_section_index_sources,
    join_multi,
    local_gold_sections_dir,
    localization_override_paths,
    localization_signal_registry_paths,
    lt_source_map_path,
    merge_appended_rows,
    merge_keyed_rows,
    normalize_key,
    normalize_rule_key,
    normalize_row_signature,
    normalize_tsv_row,
    optional_book_root,
    optional_tsv_rows,
    read_tsv,
    require_book_root,
    require_tsv_rows,
    resolve_book_root,
    resolve_indexed_text_path,
    resolve_repo_path,
    review_taxonomy_path,
    shared_gold_sections_dir,
    shared_rule_path,
    strip_markdown,
    slugify,
    split_multi,
    term_candidates_path,
    termbase_paths,
    write_tsv,
)
from workflow_runtime import REPO_ROOT, ensure_python_module, obsidian_dest_for_title, parse_bool

MANUAL_AUDIT_AREAS = (
    "terminija",
    "kolokacijos",
    "gramatika",
    "semantika",
    "norminė logika",
    "atviros abejonės",
)


BOOK_ROOT = resolve_book_root()
SOURCE_CHAPTERS_DIR = BOOK_ROOT / "source" / "chapters-en" if BOOK_ROOT else None
LT_CHAPTERS_DIR = BOOK_ROOT / "lt" / "chapters" if BOOK_ROOT else None
RESEARCH_DIR = BOOK_ROOT / "research" if BOOK_ROOT else None
CHAPTER_PACKS_DIR = BOOK_ROOT / "chapter_packs" if BOOK_ROOT else None
ADJUDICATION_PACKS_DIR = BOOK_ROOT / "adjudication_packs" if BOOK_ROOT else None
GOLD_SECTIONS_DIR = BOOK_ROOT / "gold_sections" if BOOK_ROOT else None
