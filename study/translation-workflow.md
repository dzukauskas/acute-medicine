# Best Free Workflow

This project will use a chapter-by-chapter workflow that stays local by default.

## Core stack

1. PDF extraction with local scripts and Python libraries already installed in this workspace.
2. Chapter source files in `study/en/`.
3. Lithuanian study translations in `study/lt/`.
4. Shared terminology in `study/termbase.tsv`.
5. Manual QA for numbers, doses, abbreviations, and clinical logic.
6. Automated terminology lint with `scripts/terminology_guard.py`.

## Why this is the best free option here

- It works now on macOS without paid APIs.
- It does not depend on Windows-only CAT tools.
- It keeps the source and translation aligned by chapter.
- It is safer for medical study than blind raw machine translation.

## Optional layer

OmegaT is the only CAT tool that is both free and realistic for this Mac setup. It is optional, not required.

Use OmegaT only if one of these becomes necessary:

- you want translation memory suggestions inside a CAT interface;
- you want glossary highlighting while editing;
- you want to export/import TMX workflows later.

## Optional external MT

If you are eligible and later decide to add free machine translation:

- eTranslation is the best free candidate;
- use it only for draft generation;
- every chapter still needs human revision for medical accuracy.

## QA rules

- Keep all numbers, units, doses, and timings exact.
- Keep abbreviations such as CPR, PEA, VF, ROSC unless there is a strong reason to localize them.
- Prefer established Lithuanian medical wording over literal English syntax.
- Translate for study readability first, but never by removing clinical detail.
- Run terminology lint before treating a chapter as finished.

## Terminology guard

Run:

```bash
.venv/bin/python scripts/terminology_guard.py
```

This checks translated chapters for banned calques listed in `study/disallowed_terms.tsv`.
