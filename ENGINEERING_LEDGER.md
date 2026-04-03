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
- `lt/chapters`
- `adjudication_packs`, jei reikia
- rankinis QA pėdsakas `research` faile

## Active Theme
<!-- ledger:active_theme:start -->
- Theme: no-active-theme
- Branch: main
- Last updated: 2026-04-03T20:15:05+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- No active repo-engineering theme is open; `main` now includes the closed continuity/template contract hardening wave, so chapter-scoped translation resume, tracked `_template` surface completeness guards, and scratchpad-only handoff semantics are part of the repo-engineering baseline.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- `scripts/print_codex_resume_prompt.py` now rejects chapter-less translation resumes with an explicit `--chapter` / concrete-chapter error, and both helper-level plus real CLI tests lock that behavior in.
- `tests.test_workflow_book_template` now enforces tracked `_template` surface completeness against `template_manifest.json` plus `.gitkeep` / `required_directories`, while `tests.test_book_template_parity` still guards rendered tracked-book parity.
- `handoffs/README.md` and `scripts/write_codex_handoff.py` now describe handoffs as local scratchpads only, and generated startup instructions send the next thread to canonical repo artifacts before any optional handoff note.
- Local verification is green: the focused continuity/template slice passed, and the full required Python suite passed (`138` tests) through the repo's canonical `list_required_python_test_modules.py` entrypoint.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Treat the handoff issue as wording/governance drift, not as a full memory-model failure, because the canonical repo contract already points first to ledger or chapter artifacts.
- Treat the CI finding as split scope: `print_codex_resume_prompt` is a stronger candidate for required coverage than `write_codex_handoff`, which stays a fallback local scratch helper.
- Treat chapter-less translation resume prompts as incompatible with the repo's default chapter-scoped routing unless docs are explicitly relaxed.
- Treat template-manifest completeness as needing an explicit guard or explicit exemption list; relying on maintainers to remember manifest updates is insufficient.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- No active repo-engineering theme is currently open.
- If future work is needed, start a new narrow theme rather than reopening this closed continuity/template hardening wave.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- The new `_template` guard covers tracked surface only; workstation-local untracked trash inside `books/_template/` would still be a local hygiene issue because bootstrap copytree sees filesystem state, not just git-tracked files.
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
### 2026-04-03 20:15 | continuity-and-template-contract-audit closed on main
- Closed the continuity/template contract hardening wave on `main`.
- `scripts/print_codex_resume_prompt.py` now requires chapter-scoped translation resume, `tests.test_workflow_book_template` guards tracked `_template` surface completeness, and `handoffs/README.md` plus `scripts/write_codex_handoff.py` now define handoffs as local scratchpads rather than primary cross-worktree memory.
- `tests.test_print_codex_resume_prompt` is now part of the required suite, while `tests.test_write_codex_handoff` remains non-required because the handoff helper stays a local scratchpad fallback rather than the primary continuity path.

### 2026-04-02 15:02 | retrieval-led memory hardening closed on main
- Closed the Stage 2 retrieval-led memory hardening wave on `main` in commit `6783379` on `2026-04-02 15:02:26 +03:00` (`Harden retrieval-led memory contracts`).
- `AGENTS.md`, the workflow docs, the resume prompt generator, and contract tests now explicitly require retrieval-led reconstruction from canonical repo artifacts instead of model memory or thread history.

### 2026-04-02 14:04 | passive repo context hardening closed on main
- Closed the Stage 1 passive repo context hardening wave on `main` in commit `fe33b29` on `2026-04-02 14:04:18 +03:00` (`Harden passive repo context contracts`).
- `AGENTS.md` gained the passive repo context index, the workflow-doc triplet adopted the static/dynamic/non-canonical memory split, and resume-prompt/test coverage was aligned to that contract.

### 2026-04-02 13:01 | whimsical-figure-workflow-hardening closed on main
- Closed the Whimsical figure workflow hardening theme on `main` after commits `087b7ad` and `db96d55`.
- The closed scope includes auth discovery/recovery hardening, register-to-chapter auto-embed, reverse chapter-embed validation, a successful live `009` render+`--sync-obsidian` checkpoint, required CI manifest updates, and workflow/template parity refresh.
- Local full `python -m unittest` coverage is green at closeout (`139` tests); stricter live-vault verification and legacy embed repair are intentionally deferred to any future narrow theme.

### 2026-04-01 20:09 | context-amnesia repo design validation
- Closed the context-amnesia repo design validation theme on main after Stage 1 implementation, lock-file cleanup, tracked-book template parity refresh, and green GitHub Actions Python Tests run 23860970385.

### 2026-04-01 09:49 | final repo stabilization sweep
- Closed the final stabilization sweep on main after commit f76b807 and green GitHub Actions Python Tests run 23835834218.
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
