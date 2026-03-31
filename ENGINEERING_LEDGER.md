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
- Theme: Finding 4 disposable-clone full checkpoint completed
- Branch: codex/audit-wave-003-operability
- Last updated: 2026-03-31T14:44:28+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- `bootstrap_macos.sh` / `Brewfile` operability hardening jau buvo žalias, o dabar pilnas `Finding 4` disposable-clone checkpointas taip pat pakartotas sėkmingai: disposable clone'e atkurtas validation harness, `bootstrap_book_from_epub.py --install-obsidian-sync` baigėsi `exit 0`, runtime-derived LaunchAgent / owner marker susikūrė korektiškai, o sentinel chapter payload į disposable vault'ą pateko nuo automatinio `launchd` triggerio be rankinio `scripts/sync_obsidian_book.sh` fallback.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- Disposable clone `/tmp/acute-medicine-audit-wave-003-validation` yra išlikęs po žalio bazinio bootstrap rerun ir turi veikiančią `.venv`.
- Clone'e yra kanoninis šaltinis pilnam `Finding 4` checkpointui:
  - `books/jrcalc-clinical-guidelines-2025-reference-edition/source/epub/JRCALC Clinical Guidelines 2025 Reference Edition.epub`;
  - `/tmp/jrcalc-validation.chapters.yaml`, apibrėžiantis `jrcalc-validation-harness` slug per `c3CK.xhtml`.
- Disposable clone'e validation-only `repo_config.local.toml` buvo atkurtas su Obsidian override į `/tmp/acute-medicine-validation` / `Acute-Medicine-Validation`, todėl live-checkpointas nerašė į realų default `PARAMEDIKAS` vault'ą.
- Actual resolved disposable clone kelias yra `/private/tmp/acute-medicine-audit-wave-003-validation`, todėl runtime-derived reikšmės buvo tikrinamos helper'iais, ne hardcoded suffix'u:
  - `workspace_id=814f7242`;
  - `AGENT_LABEL=lt.medbook.obsidian-sync-jrcalc-validation-harness-814f7242`;
  - plist kelias `/Users/dzukauskas/Library/LaunchAgents/lt.medbook.obsidian-sync-jrcalc-validation-harness-814f7242.plist`.
- `.venv/bin/python scripts/bootstrap_book_from_epub.py --epub ... --chapter-map /tmp/jrcalc-validation.chapters.yaml --install-obsidian-sync` disposable clone'e baigėsi `exit 0` ir sukūrė `books/jrcalc-validation-harness` su 1 indexed chapter bei 4 ištrauktomis source figūromis.
- Install kontraktas patvirtintas:
  - plist rodo į disposable clone `scripts/sync_obsidian_book.sh`, `books/jrcalc-validation-harness` ir disposable vault paskirtį `/private/tmp/acute-medicine-validation/Acute-Medicine-Validation/JRCALC Validation Harness`;
  - owner marker `/private/tmp/acute-medicine-validation/Acute-Medicine-Validation/JRCALC Validation Harness/.acute-medicine-sync-owner.json` turi teisingus `workspace_id=814f7242`, `book_slug=jrcalc-validation-harness` ir `repo_root=/private/tmp/acute-medicine-audit-wave-003-validation`;
  - `launchctl list` mato exact runtime-derived label'į su `exit 0`.
- Kadangi fresh harness neturėjo realaus `lt` payload'o, disposable clone'e buvo sukurtas chapter sentinel `lt/chapters/009-conditions-requiring-specific-prehospital-clinical-management.md`.
- Deterministinė sync patikra baigėsi žaliai:
  - pirma duotas ribotas automatinio triggerio langas;
  - sentinel chapter disposable vault'e atsirado iškart `t+0s`, dar prieš bet kokį rankinį fallback;
  - todėl `scripts/sync_obsidian_book.sh` ranka nebuvo paleistas.
- `Finding 4` pilnas disposable-clone checkpointas laikomas praeitu; `Finding 3` pagal susitarimą vis dar neliečiamas ir lieka kitas atskiras etapas.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- `Finding 4` bootstrap kritimas traktuojamas kaip realus operability blokatorius, ne kaip signalas apeiti planą rankiniu `.venv` kūrimu ar tracked harness artefaktais.
- `bootstrap_macos.sh` turi remtis realiu runtime poreikiu, ne Homebrew formulės būsena; operatoriui svarbu, kad `node`, `npm` ir `python3` būtų ant `PATH`.
- `node` ir `python@3.12` nebelaikomi repo `Brewfile` deklaratyviu sluoksniu, nes fresh-like macOS validaciją jie blokavo ne runtime trūkumu, o Homebrew install/link šalutiniais efektais.
- Validation-only `repo_config.local.toml` ir chapter-map lieka tik disposable clone'e ir netampa merge target.
- Net po sėkmingo bazinio bootstrap rerun `Finding 3` nejudinamas, kol nebus atskirai pakartotas pilnas `Finding 4` book bootstrap + sync checkpointas.
- `Finding 4` vykdymo plane `AGENT_LABEL`, plist kelias ir `workspace_id` nelaikomi iš anksto užfiksuotomis konstantomis: jie turi būti paimami iš actual install output arba perskaičiuojami tuo pačiu helper'iu, kuris naudojamas pačiame skripte, nes resolved clone kelias gali pereiti per `/private/tmp`.
- Post-install sync patikra turi būti deterministinė: po sentinel payload sukūrimo pirmiausia duodamas trumpas, ribotas langas `launchd` triggeriui; tik jei payload neatsiranda vault'e, vieną kartą paleidžiamas rankinis `scripts/sync_obsidian_book.sh` diagnostinis fallback ir rezultatas atskirai užfiksuojamas.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- `Finding 4` checkpointui esant žaliam, kitas siauras etapas yra tik `Finding 3` gyvas Whimsical register/render/auth checkpointas.
- Kadangi tai kita techninė tema po uždaryto `Finding 4`, ją rekomenduojama pradėti naujame repo-engineering thread'e, pirmiausia perskaičius atnaujintą `ENGINEERING_LEDGER.md`.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Realus Whimsical auth/board render vis dar neįrodytas, nes `Finding 3` dar nepradėtas net ir po žalio `Finding 4` checkpointo.
- Disposable clone'e paliktas užkrautas harness-specific LaunchAgent ir validation vault payload, todėl prieš būsimą pakartotinį operability rerun gali reikėti sąmoningo cleanup arba naujo disposable clone.
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
