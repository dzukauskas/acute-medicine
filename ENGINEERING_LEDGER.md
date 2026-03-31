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
- Theme: bootstrap_macos / Brewfile operability hardening completed
- Branch: codex/audit-wave-003-operability
- Last updated: 2026-03-31T14:22:38+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- `bootstrap_macos.sh` / `Brewfile` follow-up hardening įdiegtas ir patvirtintas fresh disposable clone rerun: commit `b70d336` pašalino ankstesnį `brew bundle` blokatorių, o `/tmp/acute-medicine-audit-wave-003-validation` bootstrap checkpointas baigėsi `success`. Pilnas `Finding 4` book bootstrap + sync checkpoint dar lieka atskiras kitas žingsnis.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- Disposable clone sukurtas `/tmp/acute-medicine-audit-wave-003-validation`.
- Clone'e paliktas tik validation-only harness:
  - untracked `repo_config.local.toml`, nukreipiantis Obsidian sync į `/tmp/acute-medicine-validation/Acute-Medicine-Validation`;
  - untracked `/tmp/jrcalc-validation.chapters.yaml`, apibrėžiantis `jrcalc-validation-harness` slug per `c3CK.xhtml`.
- Pradinis `./scripts/bootstrap_macos.sh` clone'e buvo kritęs dar prieš `.venv` sukūrimą.
- Tą kritimą sukėlė du konkretūs blokatoriai:
  - `node` priklausomybių grandinėje `z3` žingsnis krito su `FormulaUnavailableError: No available formula with the name "formula.jws.json"`;
  - `python@3.12` link žingsnis krito su `Could not symlink bin/2to3-3.12`, nes `/usr/local/bin/2to3-3.12` jau egzistuoja.
- Lokaliai ant branch'o įdėtas hardening sluoksnis:
  - `Brewfile` palikti tik `gh`, `obsidian`, `whimsical`;
  - `scripts/bootstrap_macos.sh` po `brew bundle` tikrina `node`, `npm`, `python3` ant `PATH` ir krenta su aiškiu operatoriaus klaidos tekstu, jei jų nėra;
  - `docs/new-mac-setup.md` atnaujintas su prerequisites bloku ir `.venv/bin/python ...` pavyzdžiais;
  - sena `Whimsical` login komanda pakeista į variantą su `--book-root`.
- Siaura regresinė danga žalia:
  - `.venv/bin/python -m unittest tests.test_shell_entrypoints`
  - `.venv/bin/python -m unittest tests.test_repo_portability_docs`
- Hardening sluoksnis atskirtas į funkcinį commit `b70d336` `Harden bootstrap runtime checks for macOS setup`.
- Po `b70d336` pakartotas fresh disposable clone bootstrap checkpointas tame pačiame `/tmp/acute-medicine-audit-wave-003-validation` kelyje:
  - `./scripts/bootstrap_macos.sh` baigėsi `exit 0`;
  - pilnas logas išsaugotas `/tmp/audit-wave-003-bootstrap-rerun.log`;
  - ankstesni `FormulaUnavailableError` ir `Could not symlink bin/2to3-3.12` lūžiai nebepasikartojo.
- `Finding 4` bazinis macOS bootstrap blokatorius laikomas pašalintu, bet pilnas `bootstrap_book_from_epub --install-obsidian-sync` checkpoint dar nepakartotas; `Finding 3` pagal susitarimą vis dar neliečiamas.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- `Finding 4` bootstrap kritimas traktuojamas kaip realus operability blokatorius, ne kaip signalas apeiti planą rankiniu `.venv` kūrimu ar tracked harness artefaktais.
- `bootstrap_macos.sh` turi remtis realiu runtime poreikiu, ne Homebrew formulės būsena; operatoriui svarbu, kad `node`, `npm` ir `python3` būtų ant `PATH`.
- `node` ir `python@3.12` nebelaikomi repo `Brewfile` deklaratyviu sluoksniu, nes fresh-like macOS validaciją jie blokavo ne runtime trūkumu, o Homebrew install/link šalutiniais efektais.
- Validation-only `repo_config.local.toml` ir chapter-map lieka tik disposable clone'e ir netampa merge target.
- Net po sėkmingo bazinio bootstrap rerun `Finding 3` nejudinamas, kol nebus atskirai pakartotas pilnas `Finding 4` book bootstrap + sync checkpointas.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Pradėti naują siaurą etapą nuo pakartotinio `Finding 4` disposable clone checkpointo po sėkmingo bazinio bootstrap: sukurti validation harness, paleisti `.venv/bin/python scripts/bootstrap_book_from_epub.py ... --install-obsidian-sync` ir patikrinti sync rezultatą disposable vault'e.
- Tik sėkmingai susikūrus `jrcalc-validation-harness` workspace tęsti `Finding 3` gyvą Whimsical register/render checkpointą.
- Kadangi `bootstrap_macos / Brewfile` tema užbaigta, tolesnį `Finding 4` live-validation etapą rekomenduojama tęsti naujame repo-engineering thread'e.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Realus Whimsical auth/board render vis dar neįrodytas, nes `Finding 3` sąmoningai atidėtas iki pakartotinio `Finding 4` bootstrap checkpointo.
- Hardening dabar jau patvirtintas ir fresh disposable clone bootstrap rerun, bet dar neįrodytas pilname `book bootstrap + Obsidian sync` kelyje.
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
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
