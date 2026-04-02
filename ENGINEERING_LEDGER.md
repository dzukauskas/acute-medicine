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
- Last updated: 2026-04-02T15:26:38+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- No active repo-engineering theme is open; `main` already contains the closed Stage 1 passive repo context hardening wave (`fe33b29`) and the closed Stage 2 retrieval-led memory hardening wave (`6783379`), so the repo-engineering baseline is the hardened memory model rather than the earlier Whimsical closeout state.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- `AGENTS.md` now includes a compact passive repo context index that names the repo purpose, canonical passive context, durable state locations, tool layers, QA model, and thread-routing contract.
- `AGENTS.md` and the workflow docs now carry the retrieval-led rule explicitly: recover workflow contracts and durable state from canonical repo artifacts before relying on model memory or thread history.
- `docs/codex-workflow.md`, `docs/book-translation-workflow.md`, and `docs/repo-engineering-workflow.md` are aligned on the Stage 1 memory-model triplet: static passive repo context, dynamic durable execution state, and non-canonical context.
- `scripts/print_codex_resume_prompt.py` now emits both engineering and translation resume prompts in the same memory-model language, and `tests.test_print_codex_resume_prompt` keeps those prompts aligned with the workflow docs.
- Drift/budget and behavior guards already live in tests: `tests.test_repo_portability_docs` enforces passive-index compactness/non-temporal limits plus retrieval-led/workflow parity, `tests.test_book_template_parity` catches tracked-book drift, and the required suite still includes rule/QA guards such as `tests.test_repo_global_rules` and `tests.test_run_chapter_qa`.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Passive repo context belongs in `AGENTS.md` and workflow docs; time-sensitive repo-engineering execution state belongs in `ENGINEERING_LEDGER.md`, not in passive docs or thread history.
- Resume and new-thread flows must be retrieval-led: reconstruct state from canonical repo artifacts first, then use thread history or `handoffs/*.md` only as fallback context.
- When a narrow repo-engineering theme is closed on `main`, keep it in `Completed Themes` and reset `Active Theme` back to explicit `no-active-theme`.
- Workflow docs, generated resume prompts, and their contract tests must stay textually aligned with the shared memory model.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- No active repo-engineering theme is currently open.
- If future work is needed, start a new narrow theme either for explicit `--sync-obsidian` live-vault verification, for a standalone legacy figure-embed repair helper, or for a separate closeout/process-hardening follow-up if `main` later drifts again.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Live-vault visibility after `--sync-obsidian` is enforced today by workflow contract and one real checkpoint, not by a dedicated always-on acceptance test.
- Already-registered legacy figure rows can now be detected when chapter embeds are missing, but bulk repair of old rows still remains a manual or future-helper workflow.
- Stage 1 and Stage 2 are closed on `main`, but future documentation/prompt/test drift is still possible if the shared memory model changes without synchronized updates to all guarded artifacts.
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
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
