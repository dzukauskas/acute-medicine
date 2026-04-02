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
- Last updated: 2026-04-02T13:01:52+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- No active repo-engineering theme is open; the Whimsical figure workflow hardening wave is closed on `main` after runtime, validator, CI-manifest, and workflow-doc parity fixes.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- `render_whimsical_figure.py` now tries the canonical storage-state path, other discovered `storage-state*.json` files under the Whimsical cache, and cached `profile-copy*` browser profiles; on success it normalizes recovery back into the canonical storage-state path and on failure it prints an explicit `--login` recovery command.
- `register_whimsical_figure.py` now accepts `--login` / `--storage-state`, auto-embeds the registered figure into the mapped `lt/chapters/<slug>.md`, and can optionally `--sync-obsidian` only after the repo-facing completion steps succeed.
- `validate_figures_manifest.py` now enforces the reverse contract too: if an active manifest PNG belongs to a chapter, that PNG must be embedded in the corresponding LT chapter Markdown, not just exist in `lt/figures/`.
- Live checkpoint on `figure-9-4-009-conditions-requiring-specific-prehospital-clinical-management-fig-04` succeeded with `--sync-obsidian`; the PNG re-rendered and synced into the configured Obsidian vault, and `validate_figures_manifest.py --book-root ... 009` now passes end-to-end.
- The live checkpoint exposed one extra CLI success-path bug in `validate_figures_manifest.py`: the final success message resolved chapter numbers without `book_root`; this is now fixed and covered by a focused regression test.
- Required CI now includes `tests.test_register_whimsical_figure` and `tests.test_validate_figures_manifest`, template and tracked-book workflow docs are aligned with the new completion contract, and the full local `python -m unittest` suite is green (`139` tests).
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Treat Whimsical auth bootstrap, figure registration, chapter embedding, and Obsidian visibility as one narrow repo-engineering theme separate from chapter drafting.
- Do not assume an active Whimsical desktop app implies a valid Playwright storage-state for render_whimsical_figure.py.
- A figure is not done when PNG exists; completion must include chapter embed presence and, when relevant, live Obsidian visibility.
- When auth recovery succeeds from an alternate cache artifact, normalize it back into the canonical `~/.cache/codex-whimsical/storage-state.json` path so future runs stop depending on cache archaeology.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- No active repo-engineering theme is currently open.
- If future work is needed, start a new narrow theme either for explicit `--sync-obsidian` live-vault verification or for a standalone legacy figure-embed repair helper.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Live-vault visibility after `--sync-obsidian` is enforced today by workflow contract and one real checkpoint, not by a dedicated always-on acceptance test.
- Already-registered legacy figure rows can now be detected when chapter embeds are missing, but bulk repair of old rows still remains a manual or future-helper workflow.
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
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
