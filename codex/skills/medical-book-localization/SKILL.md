---
name: medical-book-localization
description: Use this skill when translating or localizing a medical book, chapter, table, algorithm, or clinical figure into Lithuanian with source-faithful default behavior and tightly constrained LT/EU localization. Use it for PDF-first workflows, Lithuanian source research, unit conversion, diagram recreation, and anti-calque language polishing without free rewriting.
---

# Medical Book Localization

Use this skill for chapter-by-chapter Lithuanian localization of medical books and similar clinical source material.

If this repository also defines binding workflow files or repo-level agent rules, follow those first. Treat this skill as an execution layer, not as permission to override stricter repo policy.

## Core rules

- Treat the original PDF as the canonical source. OCR or extracted markdown can help navigation but never replace reading the real pages.
- Default to source-faithful translation. Keep the original chapter logic, ordering, rhetorical function, and level of specificity unless a localized exception is explicitly justified.
- Drafting from a blank page is allowed only as a writing technique. It does not permit free rewriting, summarizing, reordering, or replacing the source with a locally invented structure.
- Prefer current Lithuanian medical usage when choosing terminology, collocations, and explicitly justified LT/EU replacements. Do not treat local practice as a blanket license to rewrite the source.
- Keep chapter, table, and figure numbering aligned with the book.
- Use SI / EU units as the main form. Convert imperial or UK units instead of carrying them over verbatim.
- Prefer natural Lithuanian medical prose over translation-shaped wording, but do not let language polish drift into semantic rewriting.
- Show English terms sparingly: usually only at the first useful mention of a harder term, not in headings and not as a constant bilingual mirror.
- Add student-facing term blocks only when a section is genuinely dense or conceptually new.

## Source priority

1. The source book remains canonical for meaning, structure, scope, argument order, and original framing.
2. Lithuanian official sources: SAM, e-seimas, TAR, GMP service, national laws, ministerial standards, approved methodologies.
3. Lithuanian academic and tertiary-care sources: VU, LSMU, Santaros klinikos, Kauno klinikos, specialist societies, university teaching material.
4. Current European guidelines.
5. Current international guidelines.

Use LT/EU sources to lock terminology and to justify explicitly localized normative replacements. Do not demote the source book into a mere thematic reference.

When a source could be outdated, verify the latest version and record exact dates in the research log.

## Workflow

1. Read the full chapter page range from the PDF and inventory sections, tables, figures, algorithms, and boxed content.
2. Identify the chapter's clinical decision points and research Lithuanian practice for them before drafting.
3. If a Lithuanian term, collocation, or clinical category label is even slightly doubtful, verify current Lithuanian medical usage online before choosing the wording. Record the source and date in the research log.
4. Build or load the chapter-specific `chapter_pack` before generating any Lithuanian draft.
5. Draft per block type, not with one universal prose mode:
   - `narrative-prose`
   - `table-compression`
   - `algorithm-stepwise`
   - `local-context-callout`
   Treat `chart` content as a distinct source block type even when the LT output becomes one summarized local-context block.
6. If the chapter pack marks `adjudication_candidate` blocks, build or load the chapter-specific `adjudication_pack` before final polishing.
7. Draft from the `chapter_pack`, but preserve the source chapter's content order, sentence function, and level of detail. Do not use `chapter_pack` as permission to rewrite concept-first away from the source.
8. Translate tables fully into markdown when they remain readable.
9. Recreate figure text, labels, legends, algorithm steps, and `chart` content in Lithuanian.
10. For each figure, keep exactly one canonical editable source of truth. In this project, the active editable source is the `Whimsical` board recorded in `lt/figures/manifest.tsv`. Do not swap to another diagram tool unless the user explicitly approves that change and the repo workflow allows it.
11. Keep the repository `png` in sync with the active editable source after each diagram revision.
12. Use brief callouts only where local practice, safety, or interpretation needs emphasis.
13. Compare the finished chapter back to the PDF so no content block is missed.
14. Run both clinical QA and language QA before treating the chapter as complete.

## Language QA

After the first draft, polish translation-shaped language into natural Lithuanian medical prose without changing the source meaning, structure, or normative force.

Watch for translation-shaped patterns such as:

- passive bureaucratic frames like `sprendimas dėl ... turi būti ...`;
- English priority framing like `prioritetas yra ...`;
- literal action phrases like `eskaluoti pagalbą`;
- overlong conditional sentences that should be split in Lithuanian.
- Lithuanian typography drift such as decimal points, plain hyphens in ranges, missing non-breaking spaces before units, and `x` instead of `×`.

Use positive Lithuanian exemplars when available. If the repository contains `gold_phrases.tsv`, `gold_sections/`, or chapter-specific `gold_examples` inside the `chapter_pack`, treat them as stronger drafting guidance than generic style advice.

If the repository contains `scripts/terminology_guard.py`, `scripts/prose_guard.py`, or `scripts/lt_style_guard.py`, run them. If not, perform an equivalent manual review.
If the repository contains `scripts/completeness_guard.py`, run it as well to verify that structured blocks from the `chapter_pack` were not dropped.

If a chapter is manually corrected after drafting, leave a structured `review_delta` so recurring fixes can be promoted into reusable rules instead of being lost in a plain markdown diff. If you have a `before/after` pair, prefer generating the first review skeleton via `scripts/mine_review_deltas.py`.

## Tools

- Use PDF-reading tools to inspect source pages, tables, and figure text directly.
- Use web research for current Lithuanian and European medical sources when the information is time-sensitive.
- Use `whimsical-desktop` MCP as the primary diagram tool when it is available.
- If the user explicitly names a tool or workflow, do not silently substitute another one. If that tool is unavailable, stop and report the blocker instead of improvising.
- For this repository's active figures, follow the `Whimsical` export path and `lt/figures/manifest.tsv`; do not introduce `Excalidraw` as an active source unless the user explicitly changes that rule.
- If the repository already has workflow, terminology, acronym, or research templates, follow them before inventing new structure.

## Output expectations

- Work one completed chapter cycle at a time.
- Maintain a per-chapter research log with sources, dates, localization decisions, and unresolved questions.
- Prefer concise, clinically usable Lithuanian wording only after the source meaning and structure are preserved. Brevity is not a license to summarize or normalize away original content.
