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
- Last updated: 2026-03-31T09:28:56+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- Uzdaryta siaura bookkeeping pataisa: is ENGINEERING_LEDGER.md pasalintas atsitiktinai patekes terminalo ir Homebrew logu triuksmas, paliekant tik tiksline sios temos santrauka.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- Funkcinis commit 0e95644 yra origin/main, tests.test_shell_entrypoints zaliai praeina, o GitHub Actions run 23765982759 yra success.
- ENGINEERING_LEDGER.md vel turi tik sios temos santrauka: Darwin -> success smoke modeli, non-Darwin -> failure kontrakto puse ir sprendima neliesti bootstrap_macos.sh bei python-tests workflow.
- Po sio bookkeeping commit lokali repo busena vel gali buti laikoma svaria, o tema uzdaryta.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Ledgerio taisymas siame commit e yra tik bookkeeping sluoksnis; shell testai, workflow ir bootstrap skriptai nekeiciami.
- Si technine tema laikoma pilnai uzdaryta po svaraus ledger atkurimo, o kitas repo-engineering darbas turi buti pradedamas kaip nauja tema ir naujas thread.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Kita repo-engineering tema pradeti naujame thread.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Nera atviru riziku siai uzdarytai temai.
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
### 2026-03-31 09:28 | GitHub Actions bootstrap smoke parity
- Uzdaryta siaura CI parity tema: Darwin success smoke testas eksplicitiskai stubina platforma, o non-Darwin failure kontraktas paliktas atskiru testu.
- Po funkcinio commit o 0e95644 ledger isvalytas atskiru bookkeeping commit u, kad worktree vel butu svarus.

### 2026-03-30 15:21 | Codex context continuity and repo-engineering memory
- Užbaigtas runtime dependency hardening ir smoke testų sluoksnis.
- Užbaigta focused acceptance fixtures plėtra ir papildomi workflow acceptance testai.
- Užbaigtas test output noise cleanup sluoksnis.
<!-- ledger:completed:end -->
