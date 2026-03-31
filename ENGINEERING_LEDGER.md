# Engineering Ledger

Šis failas yra kanoninė `repo engineering` vykdymo būsena šiame projekte.

Naudok jį tada, kai darbas susijęs su:

- testais
- skriptais
- bootstrap / MCP / Codex / Obsidian / Whimsical infrastruktūra
- audit findings
- workflow dokumentacija

Jis nėra skirtas knygos vertimo būsenai. Vertimo darbui kanoniniai artefaktai lieka:

- `research`
- `chapter_pack`
- `term_candidates.tsv`
- QA artefaktai

## Active Theme
<!-- ledger:active_theme:start -->
- Theme: Finding 3 Whimsical live checkpoint completed
- Branch: codex/audit-wave-003-operability
- Last updated: 2026-03-31T15:23:01+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- `Finding 3` gyvas Whimsical register/render/auth checkpointas uždarytas tame pačiame disposable clone'e: validation-only `HOME` sesija buvo sukurta per `--login`, tas pats auth state panaudotas `register_whimsical_figure.py` child render'iui ir vėlesniam second render be `--login`, o PNG turinio hash pasikeitė po aiškaus tos pačios Whimsical lentos `V2` atnaujinimo.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- Tas pats disposable clone `/tmp/acute-medicine-audit-wave-003-validation` ir anksčiau sukurtas `books/jrcalc-validation-harness` buvo panaudoti `Finding 3` proof be papildomo repo cleanup; prieš startą harness `manifest.tsv` buvo švarus ir neturėjo seno `validation-009-01` įrašo ar PNG.
- Buvo sukurta laikina Whimsical validation lenta `HCus8S` (`Audit Wave 003 Validation Board`) ir naudotas konkretus harness kandidatas `source_figure_id=009-conditions-requiring-specific-prehospital-clinical-management-fig-01`.
- Validation-only auth būsena laikyta tik `/tmp/acute-medicine-whimsical-validation-home/.cache/codex-whimsical/storage-state.json`; tas pats `HOME` buvo naudotas `--login`, `register_whimsical_figure.py` ir second render be login.
- Kadangi izoliuotame `HOME` Playwright nerado browser binary, vykdymui buvo prisegtas `PLAYWRIGHT_BROWSERS_PATH=/Users/dzukauskas/Library/Caches/ms-playwright`; tai leido išlaikyti sesijos izoliaciją nereikalaujant naujo browser install į temp katalogą.
- `register_whimsical_figure.py` sėkmingai sukūrė manifest įrašą ir pirmą render'į:
  - `figure_id=figure-validation-009-01-009-conditions-requiring-specific-prehospital-clinical-management-fig-01`;
  - baseline PNG hash `3240362001450a41635e0d818245bfb6cdfd990ddc2cf8382c6dcee5a93363b2`.
- Po laikinos lentos atnaujinimo į `Validation Render V2` per `whimsical-desktop` second render buvo paleistas be `--login` su tuo pačiu validation-only session state ir sugeneravo naują PNG hash `eed1efae3b2530596bdd3fced9e0bbd1a4e3e6d1a47a8aa6815328c95bd533b1`.
- Hash pokytis laikomas galutiniu įrodymu, kad realus `register -> render -> second render without login` kelias veikia gyvai.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- `Finding 3` proof turi naudoti tą patį validation-only `HOME` per visą `--login -> register -> second render` grandinę, nes `register_whimsical_figure.py` child render remiasi default Playwright storage-state keliu po `HOME`.
- Kai validation-only `HOME` neturi savo Playwright browser cache, reikia prisegti `PLAYWRIGHT_BROWSERS_PATH` prie jau esančio lokalaus cache, o ne perinstaliuoti browserius ar atsisakyti sesijos izoliacijos.
- Realus second-render proof priimamas tik tada, kai po aiškaus tos pačios lentos pakeitimo pasikeičia PNG turinio hash; vien failo perrašymo laikas nėra pakankamas įrodymas.
- `Finding 4` uždarytas commit'e `dcfc146` neliečiamas pakartotinai, nebent atsirastų naujas konkretus bootstrap blocker'is.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Užfiksuoti `Finding 3` uždarymą `plans/audit-wave-003.md` ir laikyti `audit-wave-003` live-validation sluoksnį užbaigtu.
- Jei šitos validation-only aplinkos nebereikės, atskirai nuspręsti dėl laikinos Whimsical lentos, disposable manifest įrašo / PNG ir `/tmp/acute-medicine-whimsical-validation-home` cleanup.
- Kita repo-engineering tema jau turėtų eiti naujame thread'e, nes `audit-wave-003 operability` banga dabar uždaryta.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Validation-only artefaktai tebėra palikti lokaliai: laikina Whimsical lenta, disposable clone `manifest.tsv` įrašas / PNG ir `/tmp/acute-medicine-whimsical-validation-home` session state.
- `whimsical-desktop` MCP transportas šiame proof trumpam buvo nutrūkęs, kol `Whimsical.app` nebuvo atidarytas rankiniu `open -a "Whimsical"` veiksmu; jei tai kartosis, reikės laikyti tai atskiru desktop-connector stabilumo follow-up.
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
### 2026-03-31 15:23 | Finding 3 live Whimsical checkpoint
- Uždarytas realus `Whimsical` register/render/auth checkpointas tame pačiame disposable clone'e, kuris buvo paruoštas `Finding 4`.
- Validation-only `HOME` sesija buvo panaudota per `--login`, `register_whimsical_figure.py` child render ir second render be login.
- Baseline PNG hash `3240362001450a41635e0d818245bfb6cdfd990ddc2cf8382c6dcee5a93363b2` pasikeitė į `eed1efae3b2530596bdd3fced9e0bbd1a4e3e6d1a47a8aa6815328c95bd533b1` po aiškaus desktop-board `V2` atnaujinimo, todėl `Finding 3` laikomas uždarytu.

### 2026-03-31 12:25 | Audit wave 003 first wave
- Uzdaryta `Finding 1 + Finding 2` banga: `tests.test_repo_global_rules` refresh scenarijus sulygintas su metadata-first kontraktu, o required CI suite isplestas direct guard ir rule-layering moduliais.
- Lokalus expanded suite ir GitHub Actions run `23790510572` yra zali; `Finding 3/4` palikti velesniam live-validation checkpoint.

### 2026-03-31 09:28 | GitHub Actions bootstrap smoke parity
- Uzdaryta siaura CI parity tema: Darwin success smoke testas eksplicitiskai stubina platforma, o non-Darwin failure kontraktas paliktas atskiru testu.
- Po funkcinio commit o 0e95644 ledger isvalytas atskiru bookkeeping commit u, kad worktree vel butu svarus.

### 2026-03-30 15:21 | Codex context continuity and repo-engineering memory
- Užbaigtas runtime dependency hardening ir smoke testų sluoksnis.
- Užbaigta focused acceptance fixtures plėtra ir papildomi workflow acceptance testai.
- Užbaigtas test output noise cleanup sluoksnis.
<!-- ledger:completed:end -->
