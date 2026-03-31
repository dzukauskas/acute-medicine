# Audit Wave 003

## Purpose

Šis failas fiksuoja `audit-wave-003` findings triage rezultatą, sutartą pirmos bangos scope ir vykdymo seką.

## Findings

| ID | Tema | Statusas | Trumpa išvada |
| --- | --- | --- | --- |
| 1 | Guard verification depth CI yra siauresnis už deklaruotą chapter QA kontraktą | partial | Workflow ir `run_chapter_qa.py` aprašo platesnį Language QA sluoksnį, bet direct guard moduliai dar nebuvo privalomo CI paviršiaus dalis. |
| 2 | Binding shared/local rule-layering kontraktas per silpnai saugomas required automation | valid | `tests.test_repo_global_rules` nebuvo CI workflow, o lokaliai jame buvo realus refresh scenarijaus kritimas prieš metadata-first kontraktą. |
| 3 | Whimsical render/auth kelias lieka tik dalinai verifikuotas | closed | 2026-03-31 tame pačiame disposable clone'e gyvai įrodytas `register -> first render -> second render without login` kelias su validation-only sesija ir PNG turinio hash pokyčiu po aiškaus board atnaujinimo. |
| 4 | Realus macOS bootstrap kelias tebėra smoke/stub lygio įrodytas | closed | Uždaryta 2026-03-31 pilnu disposable-clone checkpointu: po `b70d336` ir `826b6be` fresh bootstrap bazė buvo žalia, o `bootstrap_book_from_epub.py --install-obsidian-sync` disposable clone'e sėkmingai sukūrė runtime-derived LaunchAgent, owner marker ir automatinį vault payload sync be rankinio fallback. |

## Recommended Waves

### First Implementation Wave

1. Findings `1` ir `2` kaip viena bendra `verification / CI contract hardening` tema.
2. Aiškiai atskirti:
   - realų esamą verification defektą `tests.test_repo_global_rules` refresh scenarijuje prieš `book_metadata.yaml` kontraktą;
   - verification-depth darbą, kuris išplečia required CI paviršių direct guard ir rule-layering testais.

### Later Live-Validation Checkpoint

- Uždaryta 2026-03-31 per atskirą `Finding 3` live checkpoint.

## Commit Sequence

1. `8ce3730` `Plan audit wave 003`
   - pridėtas `plans/audit-wave-003.md`;
   - `ENGINEERING_LEDGER.md` perjungtas į `audit-wave-003 planning`.
2. `f6cff8a` `Align repo-global-rules refresh test with metadata contract`
   - `tests.test_repo_global_rules` refresh scenarijus sulygintas su metadata-first kontraktu per minimalų `book_metadata.yaml` seed.
3. `723e5d9` `Promote guard and rule-layering tests into required CI`
   - `.github/workflows/python-tests.yml` explicit module list papildytas:
     - `tests.test_localization_guard`
     - `tests.test_completeness_guard`
     - `tests.test_term_readiness_gate`
     - `tests.test_repo_global_rules`
   - `Finding 3` ir `Finding 4` testų į šį wave nekelta.
4. `b70d336` `Harden bootstrap runtime checks for macOS setup`
   - `Brewfile` nebelaiko `node` ir `python@3.12` deklaratyviu `brew bundle` sluoksniu;
   - `scripts/bootstrap_macos.sh` po `brew bundle` remiasi `node` / `npm` / `python3` ant `PATH`, o ne Homebrew formulės būsena;
   - `docs/new-mac-setup.md` ir shell smoke testai sulyginti su `.venv/bin/python ...` bei eksplicitiniu `Whimsical` `--book-root --login` keliu.
5. `826b6be` `Record bootstrap hardening rerun outcome`
   - `ENGINEERING_LEDGER.md` užfiksuotas žalias fresh disposable clone `bootstrap_macos.sh` rerun;
   - `Finding 4` po bazinio hardening nebeliko sustojęs ties `brew bundle`, bet pilnas book bootstrap + sync checkpoint dar laukė atskiro live-validation etapo.

## Test Plan

- Po 2 commit:
  - `python3 -m unittest tests.test_repo_global_rules`
  - patvirtinti, kad refresh scenarijus prieš metadata kontraktą tampa žalias.
- Po 3 commit:
  - paleisti pilną workflow komandą su išplėstu explicit suite;
  - atskirai perleisti:
    - `tests.test_localization_guard`
    - `tests.test_completeness_guard`
    - `tests.test_term_readiness_gate`
    - `tests.test_repo_global_rules`
    - `tests.test_run_chapter_qa`
    - `tests.test_end_to_end_workflow_contract`
- Priėmimo kriterijai:
  - `tests.test_repo_global_rules` pilnai žalias lokaliai;
  - expanded required CI suite lokaliai žalias;
  - nėra scope creep į Whimsical live render ar realų macOS bootstrap.

## Implementation Progress

- Pirmos bangos `verification / CI contract hardening` scope įgyvendintas pilnai.
- Realus verification defektas `tests.test_repo_global_rules` refresh scenarijuje uždarytas per metadata-seed pataisymą.
- Required CI paviršius išplėstas direct guard ir rule-layering moduliais be scope creep į `Finding 3/4`.
- Lokaliai žalia:
  - `python3 -m unittest tests.test_repo_global_rules -v`
  - direct guard / chapter QA pjūvis
  - expanded workflow suite
- GitHub Actions `Python Tests` run `23790510572` ant `723e5d9` baigėsi `success`.
- Pirma banga laikoma uždaryta; likusi atskira tema yra tik `Finding 3/4` live-validation / operability checkpoint.
- 2026-03-31 disposable clone `/tmp/acute-medicine-audit-wave-003-validation` paruoštas su validation-only harness:
  - untracked `repo_config.local.toml`, nukreipiančiu Obsidian sync į `/tmp/acute-medicine-validation/Acute-Medicine-Validation`;
  - untracked `/tmp/jrcalc-validation.chapters.yaml`, aprašančiu `jrcalc-validation-harness` slug per `c3CK.xhtml`.
- Tas pats 2026-03-31 live-validation bandymas sustojo `./scripts/bootstrap_macos.sh` etape dar prieš `.venv` sukūrimą.
- `brew bundle` šio bandymo metu parodė du konkrečius bootstrap blocker'ius:
  - `node` priklausomybių grandinėje `z3` žingsnis krito su `FormulaUnavailableError: No available formula with the name "formula.jws.json"`;
  - `python@3.12` link žingsnis krito su `Could not symlink bin/2to3-3.12`, nes `/usr/local/bin/2to3-3.12` jau egzistuoja.
- Siauras follow-up `bootstrap_macos / Brewfile operability hardening` įgyvendintas commit'e `b70d336`.
- Po `b70d336` pakartotas fresh disposable clone bootstrap checkpointas tame pačiame kelyje `/tmp/acute-medicine-audit-wave-003-validation` baigėsi `success`; pilnas logas išsaugotas `/tmp/audit-wave-003-bootstrap-rerun.log`.
- Rerun metu ankstesni `FormulaUnavailableError` ir `Could not symlink bin/2to3-3.12` lūžiai nebepasikartojo; `./scripts/bootstrap_macos.sh` sėkmingai sukūrė `.venv`, įdiegė Python priklausomybes, repo skillus ir MCP setup.
- Kadangi `books/jrcalc-validation-harness` nesusikūrė, `Finding 3` register/render/live auth žingsniai sąmoningai nebuvo vykdomi per alternatyvų workaround.
- Po siauro hardening rerun `Finding 4` nebevertinamas kaip sustabdytas ties baziniu bootstrap sluoksniu, bet pilnas `bootstrap_book_from_epub --install-obsidian-sync` checkpoint dar lieka atskiras kitas žingsnis.
- 2026-03-31 pilnas `Finding 4` disposable-clone checkpointas pakartotas tame pačiame validation clone:
  - disposable clone'e atkurtas validation-only `repo_config.local.toml`, nukreipiantis sync į `/tmp/acute-medicine-validation/Acute-Medicine-Validation`;
  - actual resolved repo kelias buvo `/private/tmp/acute-medicine-audit-wave-003-validation`, todėl `workspace_id`, `AGENT_LABEL` ir plist suffix tikrinti helper'iais, ne hardcoded prielaida;
  - `.venv/bin/python scripts/bootstrap_book_from_epub.py --epub ... --chapter-map /tmp/jrcalc-validation.chapters.yaml --install-obsidian-sync` baigėsi `exit 0` ir sukūrė `books/jrcalc-validation-harness`.
- Install kontraktas buvo patvirtintas gyvai:
  - `~/Library/LaunchAgents/lt.medbook.obsidian-sync-jrcalc-validation-harness-814f7242.plist` rodo į disposable clone `scripts/sync_obsidian_book.sh` ir validation vault paskirtį;
  - owner marker disposable vault'e turi `workspace_id=814f7242`, `book_slug=jrcalc-validation-harness` ir `/private/tmp/...` repo root;
  - `launchctl list` matė exact runtime-derived label'į su `exit 0`.
- Post-install sync patikra baigėsi žaliai be rankinio fallback:
  - disposable harness `lt/chapters/009-conditions-requiring-specific-prehospital-clinical-management.md` buvo sukurtas kaip sentinel payload;
  - po riboto automatinio triggerio lango sentinel vault'e atsirado iškart `t+0s`;
  - `scripts/sync_obsidian_book.sh` ranka leisti nereikėjo.
- `Finding 4` dabar laikomas uždarytu repo lygiu; vienintelė likusi šio audit wave live-validation tema yra `Finding 3`.
- 2026-03-31 `Finding 3` uždarytas tame pačiame disposable clone'e:
  - sukurta laikina Whimsical validation lenta `Audit Wave 003 Validation Board`;
  - naudotas konkretus harness kandidatas `source_figure_id=009-conditions-requiring-specific-prehospital-clinical-management-fig-01` ir `figure_number=validation-009-01`;
  - validation-only sesija laikyta `/tmp/acute-medicine-whimsical-validation-home/.cache/codex-whimsical/storage-state.json`, o tas pats `HOME` naudotas `--login`, `register_whimsical_figure.py` ir second render be login.
- Izoliuotame `HOME` Playwright pradžioje nerado browser binary, todėl proof buvo vykdomas su `PLAYWRIGHT_BROWSERS_PATH=/Users/dzukauskas/Library/Caches/ms-playwright`; repo kodo dėl to keisti nereikėjo.
- `register_whimsical_figure.py` sėkmingai sukūrė `figure-validation-009-01-009-conditions-requiring-specific-prehospital-clinical-management-fig-01` ir pirmą PNG render'į.
- Baseline PNG hash po first render buvo `3240362001450a41635e0d818245bfb6cdfd990ddc2cf8382c6dcee5a93363b2`.
- Po aiškaus desktop-board atnaujinimo į `Validation Render V2` second render be `--login` baigėsi `exit 0`, o naujas PNG hash tapo `eed1efae3b2530596bdd3fced9e0bbd1a4e3e6d1a47a8aa6815328c95bd533b1`.
- `Finding 3` laikomas uždarytu, todėl visas `audit-wave-003` live-validation / operability sluoksnis dabar yra užbaigtas.

## Risks / Notes

- Default sprendimas: `tests.test_repo_global_rules` refresh kritimas laikomas verification/test fixture defektu prieš metadata-first kontraktą, ne signalu peržiūrėti `audit-wave-002` runtime architektūrą.
- CI runtime padidės, bet direct guard ir rule-layering moduliai šiame wave nebedemotuojami iš privalomo paviršiaus.
- Po pirmos bangos `Finding 3` ir `Finding 4` buvo sąmoningai palikti atskiram live-validation / operability planui; abu checkpointai dabar uždaryti.
- 2026-03-31 live-validation parodė, kad artimiausias siauras follow-up turi būti `bootstrap_macos.sh` / `Brewfile` operability hardening ant macOS 13, ne Whimsical runtime refactor.
- Siauras `bootstrap_macos.sh` / `Brewfile` hardening follow-up dabar įgyvendintas ir jo rezultatas patvirtintas pilnu disposable clone `Finding 4` checkpointu.
- `audit-wave-003` nebeturi atvirų live-validation findings; kitas techninis darbas jau turi eiti kaip nauja atskira repo-engineering tema.
- Validation-only artefaktai po `Finding 3` tebėra lokalūs: laikina Whimsical lenta, disposable manifest įrašas / PNG ir validation-only `HOME`, todėl prieš kitą nepriklausomą rerun verta juos sąmoningai išvalyti arba pradėti nuo naujos disposable aplinkos.
