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
- Theme: context-amnesia repo design validation
- Branch: main
- Last updated: 2026-04-01T19:44:27+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- Validate and narrow ChatGPT Pro `context amnesia` repo-design proposal against the real repo, keeping only the smallest justified changes in scope.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- `Current-State Assessment` and `Gap Analysis` are treated as calibrated after the first follow-up round; do not reopen them unless new repo evidence conflicts.
- ChatGPT Pro follow-up answers converged on a minimal first stage: docs plus `print_codex_resume_prompt.py` plus existing artifacts, without any new tracked file.
- Rewritten `Design Proposal` / `Implementation Roadmap` draft was directly repo-validated and accepted as a narrow planning baseline for Stage 1 only.
- Detailed compaction-safe scratch context is now captured in `handoffs/20260401-192624-context-amnesia-pre-design-validation-checkpoint.md`.
- Stage 1 docs and resume-tooling changes are now implemented locally: wording explicitly ties `compact` / new-thread starts to durable checkpoints, translation docs now distinguish rerunnable auto-QA from stored receipts, and `print_codex_resume_prompt.py` now exposes more ledger state plus translation artifacts like `lt/chapters` and `adjudication_packs` when present.
- Local Stage 1 verification is green for `tests.test_print_codex_resume_prompt`, `tests.test_repo_portability_docs`, and `git diff --check`.
- `chapter_packs/<slug>.qa.yaml` remains only a possible later-stage option if a durable machine-readable auto-QA receipt is still needed after Stage 1.
- Broad promotion of `tests.test_term_candidates_workflow` remains out of scope; only narrowly extracted durability-sensitive assertions stay plausible CI hardening candidates.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Work in co-op mode with ChatGPT Pro: his claims are validated against the repo first, then narrowed with follow-up questions before any design acceptance.
- Treat `Current-State Assessment` and `Gap Analysis` as the calibrated baseline for the next round.
- Treat docs plus resume-tooling plus existing artifacts as the minimal first-stage path for `compact only at durable checkpoint`.
- Do not treat `chapter_packs/<slug>.qa.yaml` as required unless the smaller stage still leaves a proven durable auto-QA receipt gap.
- Do not promote whole workflow modules like `tests.test_term_candidates_workflow`; any CI hardening must be narrowed to exact durability-sensitive assertions.
- The rewritten `Design Proposal` / `Implementation Roadmap` no longer needs another clarification round before planning; it can be used as a candidate plan as long as implementation starts with Stage 1 only.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- After any context compaction, first read `AGENTS.md`, `docs/codex-workflow.md`, `docs/repo-engineering-workflow.md`, `ENGINEERING_LEDGER.md`, and `handoffs/20260401-192624-context-amnesia-pre-design-validation-checkpoint.md`.
- If the user wants to proceed, the next decision is whether to accept this local Stage 1 implementation as the final minimal continuity change set or request another narrow review pass before commit.
- Keep Stage 2 (durable auto-QA receipt) and Stage 3 (optional CI hardening) explicitly unaccepted unless later evidence justifies them.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Stage 1 is intentionally wording-heavy, so the remaining risk is semantic drift if later edits reintroduce broad `QA artefaktai` language without preserving the rerunnable-vs-durable distinction.
- Later discussion could still drift back into Stage 2/Stage 3 scope unless the implementation closeout keeps those explicitly unaccepted.
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
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
