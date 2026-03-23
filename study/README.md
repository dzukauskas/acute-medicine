# Study Workflow

This workspace is prepared for chapter-by-chapter study and translation.

## Structure

- `study/index/chapters.md`: chapter list with page ranges.
- `study/en/`: extracted source chapters in English.
- `study/lt/`: Lithuanian chapter files for reading and study.

## Extract a chapter

```bash
.venv/bin/python scripts/extract_chapters.py --chapter 1
```

## Extract all chapters

```bash
.venv/bin/python scripts/extract_chapters.py --all
```

## Notes

- Chapter extraction keeps page markers so it is easier to cross-check the PDF.
- Blank separator pages are skipped automatically.
- Figures are not transcribed; only extractable text is saved.
