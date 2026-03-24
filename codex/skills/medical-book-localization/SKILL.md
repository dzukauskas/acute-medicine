---
name: medical-book-localization
description: Use this skill when translating or localizing a medical book, chapter, table, algorithm, or clinical figure into Lithuanian, especially when the result must follow current Lithuanian medical or Lithuanian GMP practice instead of being a literal English translation. Use it for PDF-first workflows, Lithuanian source research, unit conversion, diagram recreation, and anti-calque rewriting.
---

# Medical Book Localization

Use this skill for chapter-by-chapter Lithuanian localization of medical books and similar clinical source material.

## Core rules

- Treat the original PDF as the canonical source. OCR or extracted markdown can help navigation but never replace reading the real pages.
- Write each Lithuanian chapter from a blank page unless the user explicitly asks to revise an older draft.
- Prefer current Lithuanian medical usage and Lithuanian GMP practice when local practice differs from the book.
- Keep chapter, table, and figure numbering aligned with the book.
- Use SI / EU units as the main form. Convert imperial or UK units instead of carrying them over verbatim.
- Prefer natural Lithuanian medical prose over translation-shaped wording: native collocations, fewer nominalizations, clearer valency, split genitive chains, and active syntax where possible.
- Show English terms sparingly: usually only at the first useful mention of a harder term, not in headings and not as a constant bilingual mirror.
- Add student-facing term blocks only when a section is genuinely dense or conceptually new.

## Source priority

1. Lithuanian official sources: SAM, e-seimas, TAR, GMP service, national laws, ministerial standards, approved methodologies.
2. Lithuanian academic and tertiary-care sources: VU, LSMU, Santaros klinikos, Kauno klinikos, specialist societies, university teaching material.
3. Current European guidelines.
4. Current international guidelines.
5. The source book for structure, scope, and original framing.

When a source could be outdated, verify the latest version and record exact dates in the research log.

## Workflow

1. Read the full chapter page range from the PDF and inventory sections, tables, figures, algorithms, and boxed content.
2. Identify the chapter's clinical decision points and research Lithuanian practice for them before drafting.
3. Write the Lithuanian chapter concept-first, not sentence-by-sentence from English.
4. Translate tables fully into markdown when they remain readable.
5. Recreate figure text, labels, legends, and algorithm steps in Lithuanian.
6. For each figure, keep exactly one canonical editable source of truth. Prefer a `Whimsical` board by default. If a file-based editable source is required, use `Excalidraw`. Do not keep parallel active sources for the same figure.
7. Keep the repository `png` in sync with the active editable source after each diagram revision.
8. Use brief callouts only where local practice, safety, or interpretation needs emphasis.
9. Compare the finished chapter back to the PDF so no content block is missed.
10. Run both clinical QA and language QA before treating the chapter as complete.

## Language QA

After the first draft, stop following the English sentence shape and rewrite the text as natural Lithuanian medical prose.

Watch for translation-shaped patterns such as:

- passive bureaucratic frames like `sprendimas dėl ... turi būti ...`;
- English priority framing like `prioritetas yra ...`;
- literal action phrases like `eskaluoti pagalbą`;
- overlong conditional sentences that should be split in Lithuanian.
- Lithuanian typography drift such as decimal points, plain hyphens in ranges, missing non-breaking spaces before units, and `x` instead of `×`.

If the repository contains `scripts/terminology_guard.py`, `scripts/prose_guard.py`, or `scripts/lt_style_guard.py`, run them. If not, perform an equivalent manual review.

## Tools

- Use PDF-reading tools to inspect source pages, tables, and figure text directly.
- Use web research for current Lithuanian and European medical sources when the information is time-sensitive.
- Use `whimsical-desktop` MCP as the primary diagram tool when it is available.
- Use `Excalidraw` when a file-based editable source is needed or when `Whimsical` is not the right fit.
- If the repository already has workflow, terminology, acronym, or research templates, follow them before inventing new structure.

## Output expectations

- Work one completed chapter cycle at a time.
- Maintain a per-chapter research log with sources, dates, localization decisions, and unresolved questions.
- Prefer concise, clinically usable Lithuanian text over literal fidelity to English sentence structure.
