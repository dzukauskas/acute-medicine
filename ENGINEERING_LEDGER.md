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
- Last updated: 2026-04-04T19:27:45.792937+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- Repo-engineering workflow docs now define a canonical CI parity / pre-push check recipe for the ledger guard plus the required unittest suite.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- docs/repo-engineering-workflow.md now includes the repo-engineering CI parity / pre-push section, and tests.test_repo_portability_docs now locks the guard command, required unittest command, and bootstrap-smoke distinction.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Treat the handoff issue as wording/governance drift, not as a full memory-model failure, because the canonical repo contract already points first to ledger or chapter artifacts.
- Treat the CI finding as split scope: `print_codex_resume_prompt` is a stronger candidate for required coverage than `write_codex_handoff`, which stays a fallback local scratch helper.
- Treat chapter-less translation resume prompts as incompatible with the repo's default chapter-scoped routing unless docs are explicitly relaxed.
- Treat template-manifest completeness as needing an explicit guard or explicit exemption list; relying on maintainers to remember manifest updates is insufficient.
- Treat the engineering-ledger continuity gap as a repo-local enforcement problem, not as proof that the runtime ideal should be removed from the docs.
- Treat `Accepted Decisions` and `Open Risks` as legitimate ledger sections, but not as sufficient on their own for the diff-aware checkpoint gate; that narrower rule is a CI guard policy, not the whole ledger model.
- Treat `docs/repo-engineering-workflow.md` as the canonical raw diff output contract; `AGENTS.md` and `docs/codex-workflow.md` should carry only short repo-level references to it.
- Treat positive contract assertions as the correct test boundary for safe raw diff fencing; do not add blanket rules or blanket tests that would forbid ordinary ``` examples elsewhere in the docs.
- Treat `_template` bootstrap as a manifest-driven runtime contract: unexpected filesystem files and missing manifest-managed files must both block bootstrap, and the copy layer must only materialize the validated manifest-covered surface.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Commit the docs/test hardening and confirm the follow-up GitHub Actions run is green.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- The engineering-ledger diff gate still cannot guarantee mid-session proactivity; it only blocks repo-engineering diffs that reach CI without a meaningful checkpoint in the same `MERGE_BASE..HEAD` window.
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
### 2026-04-04 18:59 | dependency-bump-ledger-checkpoint closed on main
- Closed the narrow dependency-bump ledger reconciliation theme on `main`.
- `ENGINEERING_LEDGER.md` now records the missing durable checkpoint after commit `53e4ea7` bumped `beautifulsoup4` to `4.14.3` and `EbookLib` to `0.20` in `requirements.txt`; that keeps the canonical repo-engineering memory aligned with the change that originally triggered the `Python Tests` continuity gate failure.

### 2026-04-04 09:51 | template-bootstrap-manifest-hardening closed on main
- Closed the narrow `_template` bootstrap contamination hardening theme on `main`.
- `scripts/workflow_book_template.py` now validates the real template filesystem against both the allowed manifest-covered surface and the required manifest-managed files before copying, hard-fails on unexpected or missing relative paths, and copies only validated files so local untracked trash cannot ride into a new book and missing template inputs cannot be silently skipped while `template_manifest.json` still stays out of the destination root.
- `tests.test_workflow_book_template` now locks the runtime contract with temp-template regressions for allowed-surface derivation, required-manifest coverage, unexpected-file and missing-file reporting, hard-fail behavior, and successful manifest-driven copy.

### 2026-04-03 23:27 | safe-raw-diff-output-contract closed on main
- Closed the narrow safe raw diff output contract hardening theme on `main`.
- `docs/repo-engineering-workflow.md` now defines the canonical repo-engineering raw diff contract, `AGENTS.md` plus `docs/codex-workflow.md` now reference it briefly, and `scripts/print_codex_resume_prompt.py` now injects the same rule into new engineering threads through one shared `ENGINEERING_RAW_DIFF_CONTRACT` string.
- `tests.test_print_codex_resume_prompt` and `tests.test_repo_portability_docs` now lock positive safe-fencing fragments without pretending that ordinary triple-backtick code fences are globally forbidden.

### 2026-04-03 22:31 | handoff-workflow-path-clarity closed on main
- Closed the narrow `write_codex_handoff.py` startup-checklist clarity cleanup on `main`.
- The handoff helper now names the repo-level workflow docs explicitly instead of telling the next thread to read an unspecified mode-specific workflow document, and `tests.test_write_codex_handoff` now locks that wording in for both generic and `--book-root` handoffs.

### 2026-04-03 21:24 | engineering-ledger-diff-gate closed on main
- Closed the engineering-ledger diff gate theme on `main`.
- `scripts/workflow_engineering_ledger.py` now centralizes marker-based ledger parsing, and `scripts/check_engineering_ledger_checkpoint.py` checks both changed engineering files plus meaningful ledger sections in the same `MERGE_BASE..HEAD` window.
- GitHub Actions `Python Tests` now runs a dedicated diff-aware checkpoint gate before the required unittest suite, and the repo docs now distinguish the runtime ledger ideal from the narrower repo-local CI guard policy.

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
