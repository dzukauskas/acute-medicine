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
- Theme: audit-wave-003 first-wave closed
- Branch: main
- Last updated: 2026-03-31T12:36:09+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- Audit-wave-003 pirma banga `verification / CI contract hardening` uzdaryta: metadata-contract test fix ir required CI ispletimas jau origin/main, o GitHub Actions run `23790510572` yra success.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- `8ce3730`, `f6cff8a` ir `723e5d9` jau pushinti i `origin/main`.
- `tests.test_repo_global_rules` refresh scenarijus sulygintas su metadata-first kontraktu per minimalu `book_metadata.yaml` seed.
- `.github/workflows/python-tests.yml` required explicit suite dabar apima `tests.test_localization_guard`, `tests.test_completeness_guard`, `tests.test_term_readiness_gate` ir `tests.test_repo_global_rules`.
- Lokaliai zali tiek `tests.test_repo_global_rules`, tiek expanded workflow suite.
- GitHub Actions `Python Tests` run `23790510572` ant `723e5d9` baigesi `success`.
- `Finding 3` ir `Finding 4` palikti velesniam live-validation / operability checkpoint ir siame wave nelieciami.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Pirma implementacijos banga yra vieninga `verification / CI contract hardening` tema, jungianti `Finding 1 + Finding 2`.
- `tests.test_repo_global_rules` refresh kritimas traktuojamas kaip verification fixture defektas pries metadata-first refresh kontrakta; `refresh_book_template.py` del to nekeiciamas.
- Required CI pavirsiaus ispletimas daromas per explicit unittest module list, ne per `unittest discover`.
- `Finding 3` ir `Finding 4` lieka uz sios bangos ribu iki atskiro live-validation / operability plano.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Si pirma banga uzdaryta.
- Jei bus testiama `audit-wave-003`, kita atskira tema yra `Finding 3/4` live-validation / operability checkpoint.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Isplestas CI suite letesnis nei ankstesnis focused variantas, bet tai priimta kaip verification-depth kaina.
- Realus Whimsical auth/board render ir sviezio macOS bootstrap operability vis dar neirodyti vien is repo-local testu.
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
