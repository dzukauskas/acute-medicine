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
- Theme: translation-quality hardening
- Branch: main
- Last updated: 2026-04-01T22:32:56+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- First `review_delta` skeletons for chapters 009-011 are now captured and wired into book-local terminology, localization, and prose guards instead of remaining implicit in manual chapter edits.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- `review_deltas/009-011.tsv` now cluster defects into terminology drift, localization-equivalence, section-function drift, and translation-shaped prose, with local promotion targets recorded in the TSV itself.
- Book-local hardening now includes a regex guard against `ikihospitalin-` drift, a consent-language collocation guard, and domestic-abuse-specific localization signals / overrides for UK-only legal and service-model terms.
- Full `run_chapter_qa.py` regression over currently translated chapters `001-011` is green after refreshing stale canonical `chapter_pack` artifacts and fixing one residual 009 wording drift surfaced by the new guard.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Treat this as one narrow repo-engineering theme separate from chapter drafting.
- Promote repeated fixes through review_deltas and book-local rules before considering shared-rule promotion.
- Keep the new 009-011 hardening rules book-local for now; do not promote them to `shared/` until the same patterns recur outside the current chapter cluster.
- Treat stale canonical `chapter_pack` drift discovered during regression as part of translation-quality hardening, because it can hide new rule coverage and invalidate QA results.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Watch upcoming translated chapters for the same `pre-hospital` wording drift, domestic-abuse / safeguarding UK service-model leakage, and consent-language calques before considering shared promotion.
- If more review waves depend on `review_delta` mining, decide separately whether `mine_review_deltas.py` should learn LT-heading-aware block mapping instead of relying on manual block reassignment.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Over-broad guard rules may create false positives and block source-faithful wording.
- Some localization rules remain intentionally book-local and context-heavy; premature promotion to `shared/` could overfit to the JRCALC safeguarding / consent cluster.
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
