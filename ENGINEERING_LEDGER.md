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
- Theme: audit-wave-004 closed on main
- Branch: main
- Last updated: 2026-03-31T17:27:42.823061+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- audit-wave-004 execution contract hardening is closed on main after the execution-contract pin, manifest-based required CI migration, and repo-local tool-promise clarification landed cleanly.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- Commit 9e6711a pinned the python3 >= 3.11 execution contract across runtime, bootstrap, tests, and README parity files.
- Commit de0a72c moved the required Python CI suite into tracked tests/python_test_suite.toml with a minimal helper and a dedicated suite contract test.
- Commit 53d9649 clarified repo-local vs machine-level tool guarantees, and GitHub Actions run 23802470349 is green on that commit.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- audit-wave-004 is closed as a narrow contract-hardening theme on main; no broader provisioning expansion is part of this closure.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- The next repo-engineering topic should start in a new thread.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- There is no active audit-wave-004 blocker; wider machine-level tooling still depends on workstation setup and remains outside the tracked repo bootstrap promise.
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
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
