# Codex Handoffs

Šis katalogas yra lokalus `Codex` thread / worktree scratchpad inbox.

Paskirtis:

- čia trumpam išsaugoma lokali vykdymo būsena tarp `Codex` thread'ų ar worktree;
- failai gali padėti po `context compaction` ar lokaliame `Hand off`, bet tik kaip papildomas scratchpad;
- tai nėra pakaitalas `research`, `chapter_pack`, `review_delta` ar kitiems kanoniniams workflow artefaktams.
- jis dažniau reikalingas `repo engineering` darbui negu kasdieniam knygos vertimui.

Svarbu:

- `handoffs/*.md` yra `gitignore`'inami;
- todėl jie nėra patikimas pirminis būdas pernešti būseną į naują worktree;
- repo-engineering darbui pirmiausia naudok `ENGINEERING_LEDGER.md`.

Kaip naudoti:

```bash
.venv/bin/python scripts/write_codex_handoff.py \
  --title "Chapter 011 term triage" \
  --book-root books/jrcalc-clinical-guidelines-2025-reference-edition \
  --goal "Užbaigti neužrakintų terminų triage prieš drafting." \
  --completed "Peržiūrėtas 011 research failas." \
  --next-step "Paleisti build_chapter_pack.py 011 ir sutvarkyti blocker'ius." \
  --risk "Dar nepatikrintas vienas LT terminas iš SAM/E-tar."
```

Toliau:

1. Pirma atnaujink `ENGINEERING_LEDGER.md`, jei tai repo-engineering darbas.
2. Jei tai vertimo darbas, pirmiausia atkurk būseną iš konkretaus skyriaus kanoninių artefaktų.
3. Jei reikia paralelinės linijos, naudok `Hand off` mygtuką Codex app.
4. Naujame thread'e pirmiausia perskaityk kanoninius repo artefaktus pagal režimą.
5. Tik po kanoninių artefaktų, jei dar reikia lokalaus konteksto, perskaityk naujausią aktualų `handoffs/*.md`.
6. Po to skaityk `docs/codex-workflow.md` ir pasirink atitinkamą režimą:
   - `docs/book-translation-workflow.md`
   - `docs/repo-engineering-workflow.md`

Pastaba:

- generuojami `handoffs/*.md` failai pagal nutylėjimą yra `gitignore`'inami;
- jei handoff informacija turi tapti ilgalaike projekto būsena, ją perkelk į kanoninius repo failus.
