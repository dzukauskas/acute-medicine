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
- Theme: build_chapter_pack term_candidates concurrency hardening
- Branch: main
- Last updated: 2026-03-31T18:34:46+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- Narrow repo-engineering theme to harden concurrent `build_chapter_pack.py` / `refresh_term_candidates_for_chapter()` access to book-level `term_candidates.tsv` after real JRCALC parallel runs produced NUL-byte corruption and lost status updates.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- `refresh_term_candidates_for_chapter()` now serializes default `books/<slug>/term_candidates.tsv` refreshes through a per-book lock file adjacent to the target TSV.
- Shared `write_tsv()` now writes via temp file + `fsync` + `os.replace`, removing the in-place truncate/torn-write window for TSV callers.
- Focused tests `tests.test_term_candidates_workflow`, `tests.test_term_readiness_gate`, `tests.test_build_chapter_pack_acceptance`, and `tests.test_portable_canonical_artifacts` are green after the hardening change.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Keep scope narrow: harden only `build_chapter_pack.py` / `refresh_term_candidates_for_chapter()` interaction with `term_candidates.tsv`, not the wider translation workflow.
- Use a term-candidates-specific per-book lock, not a global workflow lock.
- Put atomic TSV replacement into shared `write_tsv()`, while keeping locking local to the `term_candidates.tsv` refresh path.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Decide whether to keep this theme open for any broader regression coverage or close it after review / commit.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- The lock is intentionally narrow to default book-level `term_candidates.tsv` refreshes; custom `--out` TSV paths are left unlocked by design because they are not the shared workflow artifact.
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
