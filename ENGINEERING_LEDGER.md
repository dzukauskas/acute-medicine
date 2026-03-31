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
- Theme: Post-merge Python Tests CI parity
- Branch: main
- Last updated: 2026-03-31T15:47:00+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- Po `audit-wave-003` suvedimo į `main` GitHub Actions run `23797589493` krito ne dėl `bootstrap_macos.sh` kontrakto, o dėl `tests.test_shell_entrypoints` fixture, kuris CI runner'yje netyčia pasiėmė sisteminį `python3` ir nuėjo giliau nei tikėtasi.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- Sugedęs testas buvo `test_bootstrap_macos_requires_python3_on_path_after_brew_bundle`: vietoj laukto `Required command not found: python3...` GitHub runner'yje gautas `Could not open requirements file ... requirements-dev.txt`, nes `python3` buvo rastas per host PATH.
- `tests/test_shell_entrypoints.py` dabar izoliuoja tą scenarijų vykdydamas `bootstrap_macos.sh` per `/bin/bash` ir tik su fake `PATH`, kuriame yra stub'intas `dirname`, todėl testas nebegali netyčia pasiimti host `python3`.
- Lokaliai žali:
  - `.venv/bin/python -m unittest tests.test_shell_entrypoints -v`
  - tas pats focused CI suite kaip workflow faile: `81 tests`, `OK`
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Šitas lūžis klasifikuojamas kaip siauras CI parity / fixture bug, ne kaip naujas `bootstrap_macos.sh` runtime kontrakto defektas.
- Missing-`python3` shell testas turi izoliuoti host PATH pakankamai griežtai, kad runner aplinka negalėtų pakeisti laukiamo guard elgesio.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Užfiksuoti siaurą test-fixture pataisą į `main` ir patikrinti, kad kitas `Python Tests` run būtų žalias.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Iki kol naujas GitHub Actions run nebus žalias, remote pusėje šita parity tema lieka ne iki galo patvirtinta.
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
