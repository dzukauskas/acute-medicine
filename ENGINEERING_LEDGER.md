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
- Theme: audit-wave-004 execution contract hardening
- Branch: main
- Last updated: 2026-03-31T17:16:01.051191+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- Execution contract hardened: Python floor pinned, required CI moved to a tracked manifest, and repo-local vs machine-level tool promises clarified.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- workflow_runtime.py now fails clearly on python3 < 3.11, and bootstrap_macos.sh enforces python3 >= 3.11 before creating .venv.
- The required Python CI suite moved from inline workflow YAML to tracked tests/python_test_suite.toml, and a dedicated contract test now enforces full classification.
- AGENTS.md, docs/new-mac-setup.md, books/README.md, the template README, and the tracked exemplar README now separate repo-local guaranteed tools from wider machine-level tooling and only show .venv/bin/python after repo bootstrap.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- The host execution floor in this repo is python3 >= 3.11; CI stays on Python 3.12.
- The required-suite helper must stay minimal: read the manifest and print required modules only.
- Repo-local bootstrap guarantees only context7, pdf-reader, excalidraw, playwright, and whimsical-desktop; broader tool routing remains machine-level.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Review the diff and, if it looks right, close this audit-wave-004 contract hardening theme on main.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Broader machine-level tools such as ebook-mcp, brave-search, firecrawl, browserbase, and obsidian still depend on workstation setup and are not a tracked bootstrap promise.
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
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
