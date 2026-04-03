# Codex Workflow Map

Šiame repo yra du skirtingi darbo režimai, ir jų nereikia maišyti.

Jei tikėtinas `compact` arba naujas thread, pirma užfiksuok dabartinę būseną kanoniniuose to režimo artefaktuose. Thread istorija čia nėra checkpoint.

## Memory model

Static passive repo context:

- `AGENTS.md` ir workflow docs aprašo, kas yra šis repo, kokie yra darbo režimai, kur gyvena kanoninės taisyklės ir kaip sluoksniuojami tool'ai.

Dynamic durable execution state:

- ši būsena yra workflow-specific ir turi būti perskaitoma iš kanoninių artefaktų, o ne spėjama iš modelio atminties ar thread istorijos;
- vertimo režime būsena gyvena `research/<slug>.md`, chapter pack failuose `chapter_packs/<slug>.yaml`, `term_candidates.tsv`, `lt/chapters/<slug>.md` ir, kai reikia, `adjudication_packs/<slug>.yaml`;
- repo-engineering režime būsena gyvena `ENGINEERING_LEDGER.md`.

Non-canonical context:

- `thread history` ir `handoffs/*.md` gali padėti, bet jie nėra kanoninė atmintis.

## 1. Book translation workflow

Šis režimas galioja, kai dirbama su konkrečios knygos turiniu:

- `research`
- chapter pack
- `term_candidates.tsv`
- `lt/chapters`
- `lt/figures`

Naudok:

- `books/README.md`
- `books/_template/workflow.md`
- `books/_template/source-priority.md`
- `books/<slug>/workflow.md`
- `docs/book-translation-workflow.md`

Trumpa taisyklė:

- vienas skyrius arba vienas jo blocker'ių rinkinys = vienas thread;
- `Hand off` vertimo režime dažniausiai nereikia.
- agentas turi pats pasakyti, jei mato, kad jau prasidėjo naujas skyrius ar kita savarankiška vertimo tema.
- jei po `compact` ar naujo thread reikės atstatyti būseną, remkis `research`, chapter pack failais `chapter_packs/<slug>.yaml`, `term_candidates.tsv`, `lt/chapters` ir, kai reikia, `adjudication_packs`; `## Finalus agento auditas` yra durable QA pėdsakas, o automatinis QA šiandien yra rerunnable pipeline, ne stored machine-readable receipt.

## 2. Repo engineering workflow

Šis režimas galioja, kai tobulinamas pats projektas:

- testai
- skriptai
- bootstrap
- MCP / Codex / Obsidian / Whimsical integracijos
- audit findings
- dokumentacija

Naudok:

- `AGENTS.md`
- `docs/repo-engineering-workflow.md`
- `ENGINEERING_LEDGER.md`
- `handoffs/README.md`

Trumpa taisyklė:

- viena techninė tema = vienas thread;
- `Hand off` naudok tik tada, kai reikia paralelinės linijos arba palieki nebaigtą techninę būseną.
- agentas turi pats trumpai pasakyti, ar likti tame pačiame thread, ar geriau pradėti naują.
- ilgų repo-engineering temų atmintis turi gyventi `ENGINEERING_LEDGER.md`, ne vien thread istorijoje.
- jei ledger neturi aktyvios temos, naujas thread turi pradėti kitą siaurą techninę temą pagal ledger santrauką ir `Next Steps`, o ne tęsti jau uždarytą darbą.
- jei tikėtinas `compact` arba naujas thread, prieš tai atnaujink `ENGINEERING_LEDGER.md`; tada naujas thread gali remtis ledger ir kanoniniais repo artefaktais, o ne thread istorija.

## `handoffs/*.md` paskirtis

`handoffs/*.md` nėra kanoninis projekto workflow artefaktas. Jie yra tik trumpalaikė vykdymo būsena tarp thread'ų ar worktree.

Todėl:

- vertimo režime pirmiausia remkis `research`, chapter pack failais `chapter_packs/<slug>.yaml`, `term_candidates.tsv`, `lt/chapters` ir, kai reikia, `adjudication_packs`;
- repo engineering režime pirmiausia remkis `ENGINEERING_LEDGER.md`;
- `handoff` naudok tik kaip papildomą lokalų scratchpad, o ne kaip pagrindinę atmintį.

## Naujo thread promptai

Repo engineering:

```bash
.venv/bin/python scripts/print_codex_resume_prompt.py --mode engineering
```

Book translation:

```bash
.venv/bin/python scripts/print_codex_resume_prompt.py \
  --mode translation \
  --book-root books/<slug> \
  --chapter 001
```

Translation resume helperis šiame repo reikalauja konkretaus `--chapter`; book-level resume be skyriaus nelaikomas galiojančiu keliu.
