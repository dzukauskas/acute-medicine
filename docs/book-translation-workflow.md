# Book Translation Workflow

Šis workflow galioja tada, kai dirbama su konkrečios knygos turiniu:

- `research`
- `term_candidates.tsv`
- `chapter_pack`
- `adjudication_pack`
- `lt/chapters`
- `lt/figures`

## Paprasta taisyklė

Vienas skyrius arba vienas aiškus skyriaus blokatorių rinkinys = vienas thread.

Kol darbas lieka tame pačiame skyriuje, naujo thread paprastai nereikia.

## Ką pirmiausia skaityti

Kai pradedamas vertimo darbas, pirmiausia remkitės:

1. `AGENTS.md`
2. `books/README.md`
3. `books/_template/workflow.md`
4. `books/_template/source-priority.md`
5. konkrečios knygos `books/<slug>/workflow.md`
6. konkretaus skyriaus `research/<slug>.md`, `chapter_packs/<slug>.yaml` ir `term_candidates.tsv`

## Kada likti tame pačiame thread

Lik tame pačiame thread, jei:

- tęsi tą patį skyrių;
- tvarkai to paties skyriaus terminų blocker'ius;
- taisai to paties skyriaus QA klaidas;
- darbas vis dar aiškiai matomas `research`, `chapter_pack` ir diff'e.

## Kada kurti naują thread

Kurti naują thread verta tik tada, kai:

- pereini prie kito skyriaus;
- pereini prie kitos savarankiškos užduoties, pavyzdžiui, nuo terminų triage prie figure workflow;
- dabartinis pokalbis tapo per ilgas ir nebeaiškus.

## Kada nereikia `Hand off`

Dažniausiai vertimo workflow `Hand off` nereikia.

Jei visa svarbi būsena jau yra:

- `research` faile;
- `chapter_pack`;
- `term_candidates.tsv`;
- QA rezultatuose;
- commit'uose arba aiškiame diff'e,

tada naujas thread gali tiesiog perskaityti tuos failus.

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

- pirmiausia pildyk `research`, `chapter_pack`, terminų ir QA artefaktus;
- tik po to remkis thread istorija.

## Ką rašyti naujame thread

Paprasčiausias kelias:

```bash
python3 scripts/print_codex_resume_prompt.py \
  --mode translation \
  --book-root books/<slug> \
  --chapter 001
```

Tai išspausdins trumpą promptą, kurį gali tiesiog įklijuoti į naują `Codex` thread.

Jei nenori leisti skripto, minimalus rankinis promptas yra toks:

```text
Perskaityk AGENTS.md, books/README.md, books/_template/workflow.md, books/_template/source-priority.md, books/<slug>/workflow.md, research/<chapter>.md, chapter_packs/<chapter>.yaml ir term_candidates.tsv. Dirbk book-translation režimu ir tęsk tą patį skyrių.
```
