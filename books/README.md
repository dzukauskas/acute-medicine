# Books

Repo yra book-agnostic: kiekviena nauja knyga bootstrap'inama į atskirą `books/<slug>/` katalogą, o reusable taisyklių bazė laikoma repo-global `shared/` sluoksnyje.

## Repo standartas

- šiame repo aprašytos workflow ir LT-source taisyklės yra privalomos, ne rekomendacinės;
- pagrindinis LT tekstas rašomas Lietuvos / ES logika;
- angliški medicininiai terminai negali būti verčiami „iš klausos“: prieš užrakinant LT atitikmenį juos privaloma patikrinti interneto LT šaltiniuose ir užfiksuoti `research` faile;
- UK, Australijos, JAV ar kitas originalo rinkos kontekstas negali likti pagrindiniame LT tekste kaip tariamas vietinis standartas;
- jei originalo kontekstą verta parodyti, jis leidžiamas tik aiškiai pažymėtame `Originalo kontekstas` bloke;
- vaistų pavadinimai pagrindiniame LT tekste pagal nutylėjimą yra bendriniai / INN, o dozės, vartojimo keliai ir indikacijos remiami LT, o jei jų nepakanka, ES šaltiniais.

Shared LT-source branduolys laikomas:

- `books/_template/source-priority.md`
- `shared/localization/lt_source_map.tsv`

## Ką laikome `books/`

```text
repo/
  shared/
  books/
    _template/
    <book-slug>/
```

- `shared/` yra vienintelis aktyvus reusable taisyklių sluoksnis.
- `books/_template/` yra bootstrap ir refresh scaffold šaltinis.
- `books/<book-slug>/` saugo knygos content artefaktus ir tik optional `*.local.tsv` override'us.

## Naujos knygos bootstrap

PDF kanoninis entrypoint:

```bash
python3 scripts/bootstrap_book_from_pdf.py \
  --pdf "/abs/path/to/book.pdf" \
  --contents-pages 7-14 \
  --page-offset 38 \
  --backmatter-start 343
```

Jei PDF turinys nestandartinis, naudokite chapter map sidecar:

```bash
python3 scripts/bootstrap_book_from_pdf.py \
  --pdf "/abs/path/to/book.pdf" \
  --chapter-map "/abs/path/to/book.chapters.yaml"
```

Ši komanda:

- išveda pavadinimą ir slug iš PDF;
- sukuria `books/<slug>/`;
- nukopijuoja PDF į `source/pdf/`;
- nukopijuoja `books/_template/` scaffold'us ir header-only local override stub'us;
- sugeneruoja `source/index/` ir `source/chapters-en/`;
- pagal nutylėjimą lieka repo-local ir neįdiegia globalaus Obsidian sync agento.

Jei šalia PDF yra `<pdf-stem>.chapters.yaml`, bootstrap jį pasiims automatiškai ir nebandys spėlioti skyrių ribų iš turinio puslapių.

Jei norite iškart įdiegti per-book Obsidian sync macOS aplinkoje, pridėkite:

```bash
python3 scripts/bootstrap_book_from_pdf.py \
  --pdf "/abs/path/to/book.pdf" \
  --install-obsidian-sync
```

PDF bootstrap ir chapter extraction šiame repo yra `PyMuPDF-first`. Jei skriptas paleidžiamas su sistemos `python3`, bet `PyMuPDF` ten nėra, jis automatiškai persijungia į repo `.venv`, jei ji paruošta.

EPUB kanoninis entrypoint:

```bash
python3 scripts/bootstrap_book_from_epub.py \
  --epub "/abs/path/to/book.epub"
```

Jei EPUB TOC / nav sluoksnis netvarkingas, naudokite chapter map sidecar:

```bash
python3 scripts/bootstrap_book_from_epub.py \
  --epub "/abs/path/to/book.epub" \
  --chapter-map "/abs/path/to/book.chapters.yaml"
```

EPUB bootstrap:

- nukopijuoja EPUB į `source/epub/`;
- sugeneruoja `source/index/chapters.{json,md}`;
- ištraukia skyrius į `source/chapters-en/`;
- išinventorizuoja chapter-referenced paveikslų kandidatus į `source/index/figures.tsv`;
- išsaugo originalius image assetus `source/figures-raw/`;
- pagal nutylėjimą lieka repo-local ir neįdiegia globalaus Obsidian sync agento.

Jei norite iškart įdiegti per-book Obsidian sync macOS aplinkoje, pridėkite:

```bash
python3 scripts/bootstrap_book_from_epub.py \
  --epub "/abs/path/to/book.epub" \
  --install-obsidian-sync
```

EPUB v1 šiame repo yra `repo-native`, be papildomo EPUB skill ar MCP serverio. Teksto extraction vykdomas per `EbookLib` ir `BeautifulSoup`.

Terminų rinkimo politika šiame repo yra `candidate inbox -> approved local/shared`, o ne tiesioginis auto-write į aktyvias bazes:

- `books/<slug>/term_candidates.tsv` kaupia per skyrius surinktus terminų ir santrumpų kandidatus;
- `build_chapter_pack.py` automatiškai atnaujina einamo skyriaus kandidatų eilutes ir prieš pack generavimą paleidžia privalomą terminijos readiness vartą;
- aktyvūs QA sluoksniai vis dar skaito tik `shared/lexicon/*.tsv` ir `*.local.tsv`;
- vien `term_candidates.tsv` statusas aktyvios bazės nepakeičia: terminas laikomas užrakintu tik tada, kai jis patenka į `shared/lexicon/*.tsv` arba `*.local.tsv`, arba kai kandidatas aiškiai atmestas kaip `rejected`, `original_context_only` ar `localization_only`;
- promotion į `shared/lexicon/` lieka review-gated.

## Repo config

Shared repo nustatymai laikomi root faile:

- `repo_config.toml`

Šiuo metu jis valdo:

- `Obsidian` bazinį katalogą;
- vault vardą;
- `launchd` agentų prefiksą.

Jei reikia naujos mašinos ar kito vault kelio, keiskite `repo_config.toml`, o ne shell skriptus.

## Template refresh

Kai atnaujinamas `books/_template/`, jau bootstrap'intą knygą atnaujinkite taip:

```bash
python3 scripts/refresh_book_template.py --book-root books/<slug>
```

Refresh perrašo tik template-valdomus docs failus ir tuščius scaffold'us. Jis neliečia realių content artefaktų.
Ne tušti `*.local.tsv` override failai ir užpildyti local `gold_sections/` pavyzdžiai paliekami nepakeisti.

## Generic QA

Book-scoped skriptai nebeturi aktyvios knygos pagal nutylėjimą. Juos kvieskite taip:

```bash
MEDBOOK_ROOT=books/<slug> python3 scripts/run_chapter_qa.py 001
MEDBOOK_ROOT=books/<slug> python3 scripts/build_chapter_pack.py 001
MEDBOOK_ROOT=books/<slug> python3 scripts/generate_research_checklist.py 001
MEDBOOK_ROOT=books/<slug> python3 scripts/validate_term_readiness.py 001
MEDBOOK_ROOT=books/<slug> scripts/sync_obsidian_book.sh
```

Pagal nutylėjimą šie skriptai aktyvias taisykles krauna iš `shared/` ir, jei tokie yra, iš `books/<slug>/*.local.tsv`.
Obsidian sync nekeičia repo `lt/chapters/` struktūros, bet vault pusėje gali sugrupuoti skyrius į navigacinius `Section` aplankus pagal `source/index/chapters.json`.
Automatinį `launchd` sync agentą diekite tik eksplicitiškai: arba bootstrap metu su `--install-obsidian-sync`, arba vėliau per `scripts/install_obsidian_sync_agent.sh --book-root books/<slug>`.

## Codex thread continuity

`Codex` app thread istorija šiame repo nelaikoma kanonine atmintimi. Tačiau svarbu atskirti du režimus:

- knygos vertimas: `docs/book-translation-workflow.md`
- repo / sistemos tobulinimas: `docs/repo-engineering-workflow.md`

Repo-engineering režime pagrindinė ilgalaikė būsena turi būti laikoma:

- `ENGINEERING_LEDGER.md`

Jei darbas tęsis naujame thread ar naujame worktree, pirmiausia atnaujinkite ledger:

```bash
python3 scripts/update_engineering_ledger.py \
  --theme "Current engineering theme" \
  --summary "Trumpa aktyvios temos santrauka." \
  --next-step "Pirmas konkretus žingsnis kitam thread."
```

Normalioje porinio darbo sesijoje to ranka daryti neturite. Ledger šiame režime turi atnaujinti agentas; ši komanda yra atsarginis kelias.

Tik jei reikia papildomo lokalaus scratchpad, naudokite `handoffs/`:

```bash
python3 scripts/write_codex_handoff.py \
  --title "Chapter 011 terminology blocker" \
  --book-root books/<slug> \
  --goal "Užbaigti blocker'ius prieš drafting." \
  --next-step "Vėl paleisti build_chapter_pack.py 011."
```

Detalesnis operating modelis aprašytas:

- `docs/codex-workflow.md`
- `docs/book-translation-workflow.md`
- `docs/repo-engineering-workflow.md`
- `ENGINEERING_LEDGER.md`
- `handoffs/README.md`

`handoffs/*.md` nėra pakaitalas `research`, `chapter_pack`, `term_candidates.tsv`, QA artefaktams ar `ENGINEERING_LEDGER.md`. Jie skirti tik trumpalaikėms vietinėms pastaboms.

Jei reikia labai paprasto naujo thread starto, naudokite:

```bash
python3 scripts/print_codex_resume_prompt.py --mode engineering
```

arba vertimo darbui:

```bash
python3 scripts/print_codex_resume_prompt.py \
  --mode translation \
  --book-root books/<slug> \
  --chapter 001
```
