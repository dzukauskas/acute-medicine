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
- Theme: whimsical-figure-workflow-hardening
- Branch: main
- Last updated: 2026-04-02T11:40:09.628992+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- Live 009 fig-04 recreation exposed multiple workflow gaps between Whimsical board creation, manifest registration, chapter embedding, and Obsidian visibility.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- Whimsical board creation and /svg render succeeded only after manual --login; the repo default session path was missing and an older cached storage-state file existed in a different location but was stale.
- register_whimsical_figure.py correctly registers and renders, but it does not help recover auth state or point the user to alternative known storage-state locations.
- A rendered PNG plus manifest row still left the LT chapter visually incomplete because chapter Markdown embedding is a separate manual step with no helper or validator.
- Obsidian sync worked, but there is no explicit contract proving that active manifest figures are embedded into the chapter note and visible in the live vault.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Treat Whimsical auth bootstrap, figure registration, chapter embedding, and Obsidian visibility as one narrow repo-engineering theme separate from chapter drafting.
- Do not assume an active Whimsical desktop app implies a valid Playwright storage-state for render_whimsical_figure.py.
- A figure is not done when PNG exists; completion must include chapter embed presence and, when relevant, live Obsidian visibility.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Add a small helper or integrated workflow that maps source figure markers to active manifest figures and inserts the chapter Markdown image block automatically.
- Harden Whimsical auth discovery so render/register can either reuse a known valid storage-state location or fail with a precise recovery message instead of a generic missing-session blocker.
- Add a validator or acceptance test that fails when a chapter-referenced active figure exists in manifest and lt/figures but is not embedded in the corresponding lt/chapters markdown.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Future figure work will keep losing time to repeated manual login and session-path archaeology unless auth handling is normalized.
- Because chapter embedding is not coupled to manifest registration, it is easy to think figure work is finished while the reader-facing LT chapter still shows no image.
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
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
