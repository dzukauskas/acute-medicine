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
- Theme: final repo stabilization sweep
- Branch: main
- Last updated: 2026-04-01T09:47:11.390172+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- Final stabilization sweep is implemented on main and locally green: term_candidates closeout wording now matches real CI scope, resume tooling understands explicit no-active-theme, and the post-bootstrap .venv/bin/python / smoke-test contract is aligned across docs and shell output.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- Required local unittest suite is green via python3 -m unittest $(python3 scripts/list_required_python_test_modules.py) (106 tests).
- The --clear-active-theme closeout path now preserves the previously active theme label when writing a completed heading.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Keep scope narrow to the three confirmed stabilization mismatches; do not reopen a broader audit wave or touch translation content.
- Fix the `term_candidates` mismatch by correcting closeout wording, not by promoting `tests.test_term_candidates_workflow` into required GitHub CI.
- Add explicit `no-active-theme` ledger semantics and make resume tooling respect them without erasing completed-theme history.
- Standardize post-bootstrap repo-native Python commands on `.venv/bin/python`; keep host `python3` only as a prerequisite / pre-bootstrap entrypoint.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Push main so GitHub Actions Python Tests can validate the updated resume/docs contract on the remote workflow.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Do not clear Active Theme in the tracked ledger until the remote required Python Tests workflow is green; that closeout stays a separate bookkeeping step.
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
### 2026-03-31 18:40 | build_chapter_pack term_candidates concurrency hardening closed on main
- Closed the narrow `term_candidates.tsv` concurrency hardening theme on `main` after commits `0b36cdf` and `ef87f68`, plus green required GitHub Actions `Python Tests` run `23806065856`; process-based parallel refresh regression coverage remains tracked in `tests.test_term_candidates_workflow`, not in required CI.

### 2026-03-31 17:27 | audit-wave-004 closed on main
- Closed the execution contract hardening wave on main after three scoped commits and a green Python Tests run 23802470349.

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
