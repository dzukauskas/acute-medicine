# Codex Handoffs

Šis katalogas yra lokalus `Codex` thread / worktree handoff inbox.

Paskirtis:

- čia trumpam išsaugoma darbinė būsena tarp `Codex` thread'ų;
- failai skirti išgyventi `context compaction` ir `Hand off` į naują worktree;
- tai nėra pakaitalas `research`, `chapter_pack`, `review_delta` ar kitiems kanoniniams workflow artefaktams.
- jis dažniau reikalingas `repo engineering` darbui negu kasdieniam knygos vertimui.

Svarbu:

- `handoffs/*.md` yra `gitignore`'inami;
- todėl jie nėra patikimas pirminis būdas pernešti būseną į naują worktree;
- repo-engineering darbui pirmiausia naudok `ENGINEERING_LEDGER.md`.

Kaip naudoti:

```bash
python3 scripts/write_codex_handoff.py \
  --title "Chapter 011 term triage" \
  --book-root books/jrcalc-clinical-guidelines-2025-reference-edition \
  --goal "Užbaigti neužrakintų terminų triage prieš drafting." \
  --completed "Peržiūrėtas 011 research failas." \
  --next-step "Paleisti build_chapter_pack.py 011 ir sutvarkyti blocker'ius." \
  --risk "Dar nepatikrintas vienas LT terminas iš SAM/E-tar."
```

Toliau:

1. Pirma atnaujink `ENGINEERING_LEDGER.md`, jei tai repo-engineering darbas.
2. Jei reikia paralelinės linijos, naudok `Hand off` mygtuką Codex app.
3. Naujame thread'e pirmiausia perskaityk `ENGINEERING_LEDGER.md`, jei tai repo-engineering darbas.
4. Tik po to, jei reikia, perskaityk naujausią aktualų `handoffs/*.md`.
5. Po to skaityk `docs/codex-workflow.md` ir pasirink atitinkamą režimą:
   - `docs/book-translation-workflow.md`
   - `docs/repo-engineering-workflow.md`

Pastaba:

- generuojami `handoffs/*.md` failai pagal nutylėjimą yra `gitignore`'inami;
- jei handoff informacija turi tapti ilgalaike projekto būsena, ją perkelk į kanoninius repo failus.
