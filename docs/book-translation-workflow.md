# Book Translation Workflow

Šis workflow galioja tada, kai dirbama su konkrečios knygos turiniu:

- `research`
- `term_candidates.tsv`
- chapter pack
- adjudication pack
- `lt/chapters`
- `lt/figures`

## Paprasta taisyklė

Vienas skyrius arba vienas aiškus skyriaus blokatorių rinkinys = vienas thread.

Kol darbas lieka tame pačiame skyriuje, naujo thread paprastai nereikia.
Jei tikėtinas `compact` arba naujas thread, dabartinė skyriaus būsena turi būti jau užfiksuota kanoniniuose artefaktuose, o ne tik chat istorijoje.

## Ką pirmiausia skaityti

Kai pradedamas vertimo darbas, pirmiausia remkitės:

1. `AGENTS.md`
2. `books/README.md`
3. `books/_template/workflow.md`
4. `books/_template/source-priority.md`
5. `docs/book-translation-workflow.md`
6. konkrečios knygos `books/<slug>/workflow.md`
7. konkretaus skyriaus `research/<slug>.md`, `chapter_packs/<slug>.yaml` ir `term_candidates.tsv`
8. jei skyrius jau pažengęs, ir `lt/chapters/<slug>.md`
9. jei skyriuje buvo reikalingas targeted adjudication, ir `adjudication_packs/<slug>.yaml`

## Memory model

Static passive repo context:

- `AGENTS.md`, `books/README.md`, `books/_template/workflow.md`, `books/_template/source-priority.md`, `docs/book-translation-workflow.md` ir `books/<slug>/workflow.md` aprašo repo paskirtį, source-priority taisykles, workflow ribas ir thread-routing.

Dynamic durable execution state:

- ši būsena yra workflow-specific ir turi būti perskaitoma iš kanoninių chapter artefaktų, o ne spėjama iš ankstesnio pokalbio;
- einamo skyriaus būsena gyvena `research/<slug>.md`, `chapter_packs/<slug>.yaml`, `term_candidates.tsv`, `lt/chapters/<slug>.md` ir, kai reikia, `adjudication_packs/<slug>.yaml`.
- Jei research sluoksnyje fiksuoji guideline-sensitive ar kitą norminį sprendimą, palik pakankamą source / version / year / jurisdiction kontekstą, kad sena ir nauja norminė informacija nesusimaišytų.

Non-canonical context:

- `thread history` ir `handoffs/*.md` gali padėti, bet jie nėra kanoninė atmintis; `ENGINEERING_LEDGER.md` vertimo režimui nėra state source.

## Kada likti tame pačiame thread

Lik tame pačiame thread, jei:

- tęsi tą patį skyrių;
- tvarkai to paties skyriaus terminų blocker'ius;
- taisai to paties skyriaus QA klaidas;
- darbas vis dar aiškiai matomas `research`, chapter pack faile `chapter_packs/<slug>.yaml` ir diff'e.

## Kada kurti naują thread

Kurti naują thread verta tik tada, kai:

- pereini prie kito skyriaus;
- pereini prie kitos savarankiškos užduoties, pavyzdžiui, nuo terminų triage prie figure workflow;
- dabartinis pokalbis tapo per ilgas ir nebeaiškus.

## Kada nereikia `Hand off`

Dažniausiai vertimo workflow `Hand off` nereikia.

Jei visa svarbi būsena jau yra:

- `research` faile, įskaitant `## Finalus agento auditas`;
- chapter pack faile `chapter_packs/<slug>.yaml`;
- `term_candidates.tsv`;
- jei reikia, adjudication pack faile `adjudication_packs/<slug>.yaml`;
- commit'uose arba aiškiame diff'e,

tada naujas thread gali tiesiog perskaityti tuos failus.
Automatinis QA šiame workflow yra rerunnable pipeline per `scripts/run_chapter_qa.py`, o ne stored machine-readable receipt.

## Kada gali prireikti `Hand off`

`Hand off` verta naudoti tik tada, kai:

- nori paraleliai dirbti kitame branch / worktree;
- palieki nebaigtą ir dar nepakankamai failuose matomą būseną;
- reikia perduoti tikslią trumpalaikę vykdymo būseną į naują thread.

Jei taip nutinka, prieš handoff:

1. pirma užrašyk realią būseną kanoniniuose artefaktuose;
2. tik tada, jei dar lieka trumpalaikių vykdymo pastabų, gali sugeneruoti `handoffs/*.md`;
3. vertimo režime `ENGINEERING_LEDGER.md` nenaudojamas, nes jis skirtas tik repo-engineering darbui.

## Vertimo workflow esmė

Vertime pagrindinė atmintis turi būti ne pokalbio istorijoje, o pačiuose workflow artefaktuose.

Todėl pagrindinė taisyklė yra:

- pirmiausia pildyk `research`, chapter pack failus `chapter_packs/<slug>.yaml`, `term_candidates.tsv`, `lt/chapters` ir, jei reikia, `adjudication_packs`;
- tik po to remkis thread istorija.

## Ką rašyti naujame thread

Paprasčiausias kelias:

```bash
.venv/bin/python scripts/print_codex_resume_prompt.py \
  --mode translation \
  --book-root books/<slug> \
  --chapter 001
```

Tai išspausdins trumpą promptą, kurį gali tiesiog įklijuoti į naują `Codex` thread. Translation resume helperis šiame repo reikalauja konkretaus `--chapter`; book-level resume be skyriaus nelaikomas galiojančiu keliu.

Jei nenori leisti skripto, minimalus rankinis promptas yra toks:

```text
Perskaityk AGENTS.md, books/README.md, books/_template/workflow.md, books/_template/source-priority.md, docs/book-translation-workflow.md, books/<slug>/workflow.md, research/<chapter>.md, chapter_packs/<chapter>.yaml, term_candidates.tsv, jei skyrius jau pažengęs, lt/chapters/<chapter>.md, o jei buvo targeted adjudication, adjudication_packs/<chapter>.yaml. Dirbk book-translation režimu ir tęsk tą patį skyrių. Static passive repo context imk iš AGENTS.md, books/README.md ir workflow docs; current dynamic durable execution state imk iš šio skyriaus artefaktų. Jei po resume svarbus automatinis QA statusas, perleisk run_chapter_qa.py iš naujo; jis nėra stored machine-readable receipt. Jei tai tas pats skyrius ar tas pats blocker'ių rinkinys, lik tame pačiame thread kontekste; jei prasideda kitas skyrius ar kita vertimo tema, aiškiai pasakyk, kad logiška pradėti naują thread.
```
