---
name: medical-book-localization
description: Use this skill when translating or localizing a medical book, chapter, table, algorithm, or clinical figure into Lithuanian with source-faithful default behavior and tightly constrained LT/EU localization. Use it for source-artifact-first workflows, Lithuanian source research, unit conversion, diagram recreation, and anti-calque language polishing without free rewriting.
---

# Medical Book Localization

Use this skill for chapter-by-chapter Lithuanian localization of medical books and similar clinical source material.

If the repository defines binding workflow files or repo-level agent rules, follow those first. Treat this skill as an execution layer, not as permission to override stricter repo policy.

## Binding posture

- Prefer the repository's workflow contract over generic localization instincts.
- If the repo defines `books/README.md`, `books/_template/workflow.md`, `books/_template/source-priority.md`, or a book-local `workflow.md`, treat them as operational rules.
- If the repo defines tracked execution artifacts such as `research/`, `chapter_packs/<slug>.yaml`, `term_candidates.tsv`, `adjudication_packs/<slug>.yaml`, `review_deltas/<slug>.tsv`, or figure manifests, use them instead of inventing parallel structure.
- Never turn a translation task into repo-engineering unless a real tooling defect appears.

## Memory model

Restore the workflow contract and the current chapter state first from canonical repo artifacts, not from thread history or prior assumptions.

- `Static passive repo context`: repo rules and workflow docs describe the workflow contract, tool hierarchy, and canonical artifact locations.
- `Dynamic durable execution state`: translation state lives in `research/<slug>.md`, `chapter_packs/<slug>.yaml`, `term_candidates.tsv`, `lt/chapters/<slug>.md`, and when needed `adjudication_packs/<slug>.yaml`.
- `Non-canonical context`: `thread history` or scratch handoff notes can help, but they are not the state source.

## Core rules

- Treat the original source artifact as canonical. In practice this means the original PDF when the book is PDF-based, or the original EPUB/book source when the repo is EPUB-based.
- OCR or extracted markdown can help navigation, but they never replace reading the canonical source artifact directly.
- Default to source-faithful translation. Preserve meaning, structure, rhetorical function, and detail level unless a localized exception is explicitly justified in research.
- Drafting from a blank page is allowed only as a writing technique. It does not permit summarizing, reordering, or replacing the source with locally invented structure.
- Localization is a constrained exception layer, not the default writing mode.
- Do not leave UK-, US-, Australia-, or other market-specific normative context in the main Lithuanian prose as if it were a Lithuanian or EU standard.
- Prefer natural Lithuanian medical prose over translation-shaped wording, but do not let polish drift into semantic rewriting.
- Keep chapter, table, and figure numbering aligned with the book.
- Use SI / EU units as the main form. Convert imperial or UK units instead of carrying them over verbatim.
- Show English terms sparingly, usually only at the first truly useful mention of a harder term.
- Do not add pedagogical side blocks, glossary callouts, or student-facing term blocks unless the repo or book workflow explicitly allows that structure.

## Source priority

1. The source book remains canonical for meaning, structure, scope, argument order, and original framing.
2. Lithuanian official sources: SAM, e-seimas, TAR, GMP service, national laws, ministerial standards, approved methodologies.
3. Lithuanian academic and tertiary-care sources: VU, LSMU, Santaros klinikos, Kauno klinikos, specialist societies, university teaching material.
4. Current European guidelines.
5. Current international guidelines.

Use LT/EU sources to lock terminology and to justify explicitly localized normative replacements. Do not demote the source book into a mere thematic reference.

When a source may be outdated, verify the latest version and record exact dates in the research log.

## Terminology discipline

- Never guess Lithuanian medical terminology.
- If an English medical term, abbreviation, collocation, or category label is not already locked in the active shared/local lexicon, verify it in Lithuanian sources before using it in translated output.
- This rule applies even when the Lithuanian equivalent feels obvious.
- Record the source, date, and decision in the chapter research log.
- If the term cannot be locked confidently, treat it as a blocker or leave it in an explicit non-promoted candidate state; do not improvise.

## Workflow

1. Read the full source chapter range from the canonical source artifact and inventory sections, tables, figures, algorithms, boxed content, and charts.
2. Identify clinical, legal, and workflow decision points that may need LT/EU verification before drafting.
3. Research Lithuanian practice and terminology for those points before drafting. When needed, continue to EU and then international sources.
4. If the repo provides `generate_research_checklist.py`, use it when the chapter has substantial unresolved research surface.
5. Satisfy any pre-pack readiness gates the repo defines, especially localization and terminology readiness.
6. Build or load the chapter pack at `chapter_packs/<slug>.yaml` before generating any Lithuanian draft.
7. If the chapter pack marks `adjudication_candidate` blocks, build or load `adjudication_packs/<slug>.yaml` before final polishing.
8. Draft from the chapter pack, but preserve the source chapter's content order, sentence function, and detail level. Do not use the chapter pack as permission to rewrite concept-first away from the source.
9. Draft per block type, not with one universal prose mode:
   - `narrative-prose`
   - `table-compression`
   - `algorithm-stepwise`
   - `local-context-callout`
   - Treat `chart` content as a distinct source block type even when the LT output becomes one summarized local-context block, and keep repo-required coverage evidence when charts are summarized.
10. Translate tables fully into markdown when they remain readable.
11. Recreate figure text, labels, legends, algorithm steps, and chart content in Lithuanian.
12. For each figure, keep exactly one canonical editable source of truth. If the repo inventories source figure candidates in `source/index/figures.tsv`, register the active figure from that source instead of inventing a parallel path. In this project, the active editable source is the `Whimsical` board recorded in `lt/figures/manifest.tsv`.
13. Keep the repo completion contract in sync after each diagram revision: active manifest row, rendered repo PNG, and embed in `lt/chapters/<slug>.md`.
14. Use brief callouts only where local practice, safety, or interpretation truly needs emphasis and the repo workflow permits that structure.
15. Compare the finished chapter back to the canonical source so no content block is missed.
16. Run both clinical QA and language QA before treating the chapter as complete.

## QA expectations

After the first draft, polish translation-shaped language into natural Lithuanian medical prose without changing the source meaning, structure, or normative force.

Watch for translation-shaped patterns such as:

- passive bureaucratic frames like `sprendimas dėl ... turi būti ...`;
- English priority framing like `prioritetas yra ...`;
- literal action phrases like `eskaluoti pagalbą`;
- overlong conditional sentences that should be split in Lithuanian;
- Lithuanian typography drift such as decimal points, plain hyphens in ranges, missing non-breaking spaces before units, and `x` instead of `×`.

Use positive Lithuanian exemplars when available. If the repo contains `gold_phrases.tsv`, `gold_sections/`, or chapter-specific positive examples inside the chapter pack, treat them as stronger drafting guidance than generic style advice.

If the repo defines a canonical QA entrypoint, use it. In this project, the canonical path is `scripts/run_chapter_qa.py`; if you run checks individually, follow the repo's required readiness, figure-manifest, completeness, and manual-audit gates rather than ad hoc review.

If the repo requires a fixed `Adjudication` section or other structured decision log in `research`, follow that exact format.

If the repo requires `## Finalus agento auditas` in `research`, treat it as a required structured artifact, not an optional note.

If a chapter is manually corrected after drafting, leave a structured `review_deltas/<slug>.tsv` record so recurring fixes can be promoted into reusable rules instead of being lost in a plain markdown diff. If you have a `before/after` pair, prefer generating the first review skeleton via `scripts/mine_review_deltas.py`.

## Tools

- Use PDF/EPUB reading tools to inspect source pages, XHTML, tables, and figure text directly from the canonical source artifact.
- Use web research for current Lithuanian and European medical sources when the information is time-sensitive or terminology is not already locked.
- Prefer the repo's declared tool path for figures. In this project, use `whimsical-desktop` as the primary active diagram tool when it is available.
- If the user explicitly names a tool or workflow, do not silently substitute another one. If that tool is unavailable, stop and report the blocker instead of improvising.
- If the repo already has workflow, terminology, acronym, figure, or research templates, follow them before inventing new structure.
- Respect repo sync safety rules. Invalid sync targets are hard stops, not warnings; do not sync external note output into the repo, the book root, or `lt/`.

## Output expectations

- Work one completed chapter cycle at a time.
- Maintain a per-chapter research log with sources, dates, localization decisions, and unresolved questions.
- Keep terminology decisions auditable.
- Prefer concise, clinically usable Lithuanian wording only after the source meaning and structure are preserved. Brevity is not a license to summarize or normalize away original content.
