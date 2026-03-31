# Audit Wave 003

## Purpose

Šis failas fiksuoja `audit-wave-003` findings triage rezultatą, sutartą pirmos bangos scope ir vykdymo seką.

## Findings

| ID | Tema | Statusas | Trumpa išvada |
| --- | --- | --- | --- |
| 1 | Guard verification depth CI yra siauresnis už deklaruotą chapter QA kontraktą | partial | Workflow ir `run_chapter_qa.py` aprašo platesnį Language QA sluoksnį, bet direct guard moduliai dar nebuvo privalomo CI paviršiaus dalis. |
| 2 | Binding shared/local rule-layering kontraktas per silpnai saugomas required automation | valid | `tests.test_repo_global_rules` nebuvo CI workflow, o lokaliai jame buvo realus refresh scenarijaus kritimas prieš metadata-first kontraktą. |
| 3 | Whimsical render/auth kelias lieka tik dalinai verifikuotas | partial | Repo turi render entrypointą ir mock lygio testus, bet realus auth + board render dar nebuvo gyvai įrodytas; 2026-03-31 validation attempt iki jo nenuėjo, nes nesusikūrė disposable validation workspace. |
| 4 | Realus macOS bootstrap kelias tebėra smoke/stub lygio įrodytas | partial | 2026-03-31 siauras `bootstrap_macos / Brewfile` hardening commit `b70d336` pašalino pradinį `brew bundle` lūžį: fresh disposable clone bootstrap rerun baigėsi `success`, bet pilnas `bootstrap_book_from_epub --install-obsidian-sync` checkpoint dar nebuvo pakartotas. |

## Recommended Waves

### First Implementation Wave

1. Findings `1` ir `2` kaip viena bendra `verification / CI contract hardening` tema.
2. Aiškiai atskirti:
   - realų esamą verification defektą `tests.test_repo_global_rules` refresh scenarijuje prieš `book_metadata.yaml` kontraktą;
   - verification-depth darbą, kuris išplečia required CI paviršių direct guard ir rule-layering testais.

### Later Live-Validation Checkpoint

- Finding `3`
- Finding `4`

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

## Risks / Notes

- Default sprendimas: `tests.test_repo_global_rules` refresh kritimas laikomas verification/test fixture defektu prieš metadata-first kontraktą, ne signalu peržiūrėti `audit-wave-002` runtime architektūrą.
- CI runtime padidės, bet direct guard ir rule-layering moduliai šiame wave nebedemotuojami iš privalomo paviršiaus.
- `Finding 3` ir `Finding 4` lieka sąmoningai out-of-scope iki atskiro live-validation / operability plano.
- 2026-03-31 live-validation parodė, kad artimiausias siauras follow-up turi būti `bootstrap_macos.sh` / `Brewfile` operability hardening ant macOS 13, ne Whimsical runtime refactor.
- Tas siauras hardening follow-up dabar įgyvendintas ir bazinis fresh-like bootstrap rerun yra žalias; kitas techninis etapas jau yra grįžimas į `Finding 4` pilną live-validation checkpointą, o po jo tik `Finding 3`.
