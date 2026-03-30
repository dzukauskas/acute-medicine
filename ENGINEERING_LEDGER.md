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
- Theme: GitHub Actions bootstrap smoke parity
- Branch: main
- Last updated: 2026-03-30T23:23:53.369154+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- Siaura parity pataisa: bootstrap_macos.sh kontraktas lieka macOS-only, o shell smoke testas dabar eksplicitiškai modeliuoja Darwin success vietoj runner OS priklausomybės.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- GitHub Actions run 23765628791 ant a23838b krito ubuntu-latest jobe ne dėl naujo skripto defekto, o dėl pasenusio test_bootstrap_macos_shell_smoke Linux success lūkesčio.
- tests.test_shell_entrypoints dabar success smoke scenarijuje stubina uname i Darwin, o atskiras test_bootstrap_macos_reports_macos_only ir toliau dengia non-Darwin failure kontrakto pusę.
- Lokaliai žali tiek python3 -m unittest tests.test_shell_entrypoints, tiek pilnas focused CI ekvivalentas iš GitHub workflow failo (57 tests / OK).
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- scripts/bootstrap_macos.sh guardas nelaikomas taisymo vieta; palaikomas elgesys modeliuojamas testų sluoksnyje per aiškų platformos stubą.
- .github/workflows/python-tests.yml šiai parity pataisai nekeičiamas, nes Linux runnerio kontraktui pakanka ištaisyti patį smoke testą.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Papildomo follow-up šiai temai nereikia, jei pushed GitHub Actions run sutaps su lokalia focused suite būsena.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Ateityje shell smoke regressijos gali grįžti, jei nauji testai vėl remsis host runner OS vietoj eksplicitinių platformos stubų.
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
### 2026-03-30 15:21 | Codex context continuity and repo-engineering memory
- Užbaigtas runtime dependency hardening ir smoke testų sluoksnis.
- Užbaigta focused acceptance fixtures plėtra ir papildomi workflow acceptance testai.
- Užbaigtas test output noise cleanup sluoksnis.
<!-- ledger:completed:end -->
