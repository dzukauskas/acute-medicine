# Codex Workflow Map

Šiame repo yra du skirtingi darbo režimai, ir jų nereikia maišyti.

## 1. Book translation workflow

Šis režimas galioja, kai dirbama su konkrečios knygos turiniu:

- `research`
- `chapter_pack`
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

## `handoffs/*.md` paskirtis

`handoffs/*.md` nėra kanoninis projekto workflow artefaktas. Jie yra tik trumpalaikė vykdymo būsena tarp thread'ų ar worktree.

Todėl:

- vertimo režime pirmiausia remkis `research`, `chapter_pack` ir QA artefaktais;
- repo engineering režime pirmiausia remkis `ENGINEERING_LEDGER.md`;
- `handoff` naudok tik kaip papildomą lokalų scratchpad, o ne kaip pagrindinę atmintį.

## Naujo thread promptai

Repo engineering:

```bash
python3 scripts/print_codex_resume_prompt.py --mode engineering
```

Book translation:

```bash
python3 scripts/print_codex_resume_prompt.py \
  --mode translation \
  --book-root books/<slug> \
  --chapter 001
```
