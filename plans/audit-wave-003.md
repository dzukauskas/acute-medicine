# Audit Wave 003

## Purpose

Šis failas fiksuoja `audit-wave-003` findings triage rezultatą, sutartą pirmos bangos scope ir vykdymo seką.

## Findings

| ID | Tema | Statusas | Trumpa išvada |
| --- | --- | --- | --- |
| 1 | Guard verification depth CI yra siauresnis už deklaruotą chapter QA kontraktą | partial | Workflow ir `run_chapter_qa.py` aprašo platesnį Language QA sluoksnį, bet direct guard moduliai dar nebuvo privalomo CI paviršiaus dalis. |
| 2 | Binding shared/local rule-layering kontraktas per silpnai saugomas required automation | valid | `tests.test_repo_global_rules` nebuvo CI workflow, o lokaliai jame buvo realus refresh scenarijaus kritimas prieš metadata-first kontraktą. |
| 3 | Whimsical render/auth kelias lieka tik dalinai verifikuotas | partial | Repo turi render entrypointą ir mock lygio testus, bet realus auth + board render nėra CI contract dalis ir nebuvo gyvai įrodytas šiame wave. |
| 4 | Realus macOS bootstrap kelias tebėra smoke/stub lygio įrodytas | needs-live-validation | Shell smoke ir docs neuždaro pilno clean-mac bootstrap + auth + figure workflow priėmimo. |

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

1. `Plan audit wave 003`
   - pridėti `plans/audit-wave-003.md`;
   - perjungti `ENGINEERING_LEDGER.md` į `audit-wave-003 planning`;
   - funkcionalaus kodo ir CI šiame žingsnyje neliesti.
2. `Align repo-global-rules refresh test with metadata contract`
   - sutvarkyti `tests.test_repo_global_rules` refresh scenarijų taip, kad fixture kurtų minimalų validų `book_metadata.yaml`;
   - `refresh_book_template.py` metadata-first kontrakto nekeisti.
3. `Promote guard and rule-layering tests into required CI`
   - išplėsti `.github/workflows/python-tests.yml` explicit module list, įtraukiant:
     - `tests.test_localization_guard`
     - `tests.test_completeness_guard`
     - `tests.test_term_readiness_gate`
     - `tests.test_repo_global_rules`
   - `Finding 3` ir `Finding 4` testų į šį wave nekelti.

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

- Planning artifact sukurtas ir sulygintas su sutarta `Finding 1 + Finding 2` banga.
- Tolesni įgyvendinimo žingsniai vykdomi atskirais commit'ais pagal aukščiau užfiksuotą seką.

## Risks / Notes

- Default sprendimas: `tests.test_repo_global_rules` refresh kritimas laikomas verification/test fixture defektu prieš metadata-first kontraktą, ne signalu peržiūrėti `audit-wave-002` runtime architektūrą.
- CI runtime padidės, bet direct guard ir rule-layering moduliai šiame wave nebedemotuojami iš privalomo paviršiaus.
- `Finding 3` ir `Finding 4` lieka sąmoningai out-of-scope iki atskiro live-validation / operability plano.
