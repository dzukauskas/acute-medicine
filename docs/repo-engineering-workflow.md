# Repo Engineering Workflow

Šis workflow galioja tada, kai tobulinamas pats projektas, o ne verčiamas konkretus knygos skyrius.

Pavyzdžiai:

- testų ir fixture plėtra;
- runtime hardening;
- shell ar Python entrypoint taisymai;
- workflow dokumentacijos keitimai;
- auditų findings įgyvendinimas;
- `Codex`, `Obsidian`, `Whimsical`, `MCP` ar bootstrap infrastruktūros taisymai.

## Memory model

Static passive repo context:

- pirmiausia remkis `AGENTS.md`, `docs/codex-workflow.md` ir `docs/repo-engineering-workflow.md`; jie aprašo repo paskirtį, workflow split, tool hierarchiją ir kanoninių artefaktų vietą.

Dynamic durable execution state:

- ši būsena yra workflow-specific ir turi būti perskaitoma iš `ENGINEERING_LEDGER.md`, o ne spėjama iš thread istorijos;
- einama repo-engineering būsena gyvena `ENGINEERING_LEDGER.md`.

Non-canonical context:

- `thread history` ir `handoffs/*.md` gali padėti, bet jie nėra kanoninė atmintis.

## Paprasta taisyklė

Viena techninė tema = vienas thread.

Pavyzdžiai:

- `PDF/EPUB runtime hardening`
- `acceptance fixtures`
- `test output cleanup`
- `Codex workflow docs`

Kol dirbi ta pačia tema, lieki tame pačiame thread.

Agentas turi pats tai nuspręsti proaktyviai. Praktikoje tai reiškia:

- kai tema nepasikeitė, agentas turi tiesiog tęsti darbą tame pačiame thread;
- kai prasideda nauja techninė tema, agentas turi aiškiai pasakyti, kad logiškas kitas žingsnis yra naujas thread;
- jei paralelinis worktree realiai nereikalingas, agentas neturi stumti naudoti `Hand off`.

## Kanoninė atmintis

Repo-engineering darbui kanoninė vykdymo atmintis yra:

- `ENGINEERING_LEDGER.md`

Tai tracked failas repo šaknyje. Jame turi gyventi:

- aktyvi techninė tema;
- trumpa aktyvios temos santrauka;
- dabartinė patikrinta būsena;
- priimti sprendimai;
- kiti žingsniai;
- atviri rizikos taškai.

Resume ar naujo thread metu pirma perskaityk static passive repo context iš `AGENTS.md` ir workflow docs, tada `ENGINEERING_LEDGER.md`, ir tik po to, jei reikia, papildomą thread istoriją ar `handoffs/*.md`.
Thread istorija čia nėra kanoninė. Jei pokalbis išsitęsia, naujas thread pirmiausia turi perskaityti `ENGINEERING_LEDGER.md`.
Jei tikėtinas `compact` arba naujas thread, ledger turi būti atnaujintas prieš būsenos pernešimą, kad nauja sesija galėtų remtis ledger, o ne thread istorija.

Normalioje porinio darbo sesijoje ledger turi atnaujinti agentas. Vartotojui nereikia kiekvieną kartą ranka leisti `update_engineering_ledger.py`.

Tai yra runtime idealas. Repo-local enforcement šiame repo yra siauresnė: diff-aware CI gate `scripts/check_engineering_ledger_checkpoint.py` gali patikrinti tik realų `MERGE_BASE..HEAD` diff'ą, o ne užtikrinti mid-session agento elgesį.

Guardas aktyvuojasi tada, kai tame pačiame diff lange yra bent vienas repo-engineering failas, kuris nėra vien `ENGINEERING_LEDGER.md`. Jei tame diff lange keistas tik `ENGINEERING_LEDGER.md`, gate praeina be papildomo checkpoint reikalavimo.

Kad gate laikytų ledger checkpointą prasmingu, tame pačiame `MERGE_BASE..HEAD` lange turi pasikeisti bent viena iš šių sekcijų: `Active Theme` (`Theme:` eilutė), `Summary`, `Current State`, `Next Steps` arba `Completed Themes`. Vien `Branch:`, `Last updated:` ar whitespace churn neužtenka.

`Accepted Decisions` ir `Open Risks` lieka pilnavertėmis ledger sekcijomis, bet šio CI guard policy prasme jie vieni patys nelaikomi pakankamu checkpointu.

Kai tema uždaroma, ji turi likti `Completed Themes` istorijoje, o `Active Theme` turi būti aiškiai išvalyta į `no-active-theme` būseną, kol prasidės kita siaura techninė tema.

## Kada kurti naują thread

Naują thread kurk tada, kai:

- prasideda kita aiškiai atskira techninė tema;
- nori švariai atskirti kitą pakeitimų bloką;
- nori kitą darbą vesti kitu branch ar worktree.

## Kada naudoti `Hand off`

Repo engineering darbui `Hand off` yra normalus įrankis, bet jo vis tiek nereikia kiekvieną kartą.

Naudok jį tik tada, kai:

- nori paralelinės darbo linijos;
- nori atsidaryti naują worktree kitai temai;
- palieki nebaigtą techninį darbą, kurio būsena dar nėra pakankamai aiški vien iš diff ir commit'ų.

Bet net ir tada:

- pirma atnaujink `ENGINEERING_LEDGER.md`;
- tik po to svarstyk `Hand off`.

## Kada kurti `handoff` failą

Kurti `handoff` failą verta tik tada, kai bent viena iš šių sąlygų teisinga:

- darbas nebaigtas;
- yra necommitintų pakeitimų;
- kitame thread reikės tiksliai žinoti, nuo ko tęsti;
- vien iš `git log`, `git diff` ir testų iškart nebus aišku, kas liko.

Jei pakeitimai jau:

- sucommitinti;
- aiškiai dokumentuoti;
- arba tema pilnai uždaryta,

tada `handoff` failo nereikia.

Svarbi išlyga:

- `handoffs/*.md` pagal nutylėjimą yra lokalūs ir `gitignore`'inami;
- todėl jie nėra patikimas pirminis būdas pernešti būseną į kitą worktree;
- dėl to pagrindinis būsenos pernešimo mechanizmas šiame repo yra `ENGINEERING_LEDGER.md`.

## Minimalus darbo modelis

1. Pasirenki vieną techninę temą.
2. Dirbi tame pačiame thread, kol tema neuždaryta.
3. Reikšmingai pasikeitus būsenai, agentas atnaujina `ENGINEERING_LEDGER.md`.
4. Jei pereini prie kitos temos, agentas turi tai aiškiai įvardyti ir rekomenduoti naują thread.
5. Jei reikia paralelinės linijos, tada naudok `Hand off`.
6. Jei reikia, pridėk lokalų `handoff`, bet tik kaip papildomą scratchpad.
7. Jei vyksta `compact`, pirmiausia turi būti užfiksuota paskutinė patikrinta būsena ledger'yje.

## Praktinis pavyzdys

Jei dabar taisai audit findings apie test harness:

- lieki tame pačiame thread, kol tvarkai visą tą findings grupę;
- jei po to pereini prie `Obsidian sync` infrastruktūros, pradedi naują thread;
- jei nori abu darbus laikyti lygiagrečiai skirtinguose worktree, tada naudok `Hand off`.

## Ledger komanda

Ši komanda yra atsarginis kelias, ne kasdienis privalomas ritualas. Paprastai ją leidžia agentas arba jos visai nereikia matyti vartotojui.

```bash
.venv/bin/python scripts/update_engineering_ledger.py \
  --theme "Acceptance fixtures follow-up" \
  --summary "Užbaigti likusius audit findings test harness sluoksnyje." \
  --state "Pridėti focused fixtures ir acceptance testai." \
  --next-step "Sutvarkyti review-cycle edge case'us." \
  --risk "Dar nepatikrintas vienas shell entrypoint smoke scenarijus."
```

Diff-aware CI gate lokaliai galima atkartoti taip:

```bash
.venv/bin/python scripts/check_engineering_ledger_checkpoint.py \
  --base-ref <base-ref> \
  --head-ref <head-ref>
```

Jei po to vis tiek reikia lokalaus papildomo scratchpad:

```bash
.venv/bin/python scripts/write_codex_handoff.py --title "Acceptance fixtures local handoff"
```

## Ką rašyti naujame thread

Paprasčiausias kelias:

```bash
.venv/bin/python scripts/print_codex_resume_prompt.py --mode engineering
```

Tai išspausdins trumpą promptą, kurį gali tiesiog įklijuoti į naują `Codex` thread.

Jei nenori leisti skripto, minimalus rankinis promptas yra toks:

```text
Perskaityk AGENTS.md, docs/codex-workflow.md, docs/repo-engineering-workflow.md ir ENGINEERING_LEDGER.md. Dirbk repo-engineering režimu. Static passive repo context imk iš AGENTS.md ir workflow docs; current dynamic durable execution state imk iš ENGINEERING_LEDGER.md. Thread history ar `handoffs/*.md` naudok tik jei ledger ir kanoninių artefaktų neužtenka. Jei ledger turi aktyvią temą, tęsk ją; jei aktyvios temos nėra, pradėk kitą siaurą temą pagal ledger santrauką, `Next Steps` ir paskutinę uždarytą temą.
```
