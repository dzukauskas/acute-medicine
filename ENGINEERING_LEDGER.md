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
- Theme: audit-wave-003 planning
- Branch: main
- Last updated: 2026-03-31T12:25:15+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- Audit-wave-003 planas uzfiksuotas tracked faile, o pirma banga suformuluota kaip `verification / CI contract hardening` tema be scope creep i live-validation sluoksnius.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- Sukurtas tracked planas `plans/audit-wave-003.md`, kuris fiksuoja findings klasifikacija, pirma banga, commit sequence, test plana ir scope ribas.
- Workflow-declared focused suite buvo lokaliai zalia validavimo fazeje.
- `tests.test_repo_global_rules` buvo uz CI ribu ir turejo realu lokalų refresh scenarijaus kritima del `book_metadata.yaml` / metadata-first kontrakto neatitikimo.
- Pirmos bangos scope apima tik metadata-seed pataisyma `tests.test_repo_global_rules` modulyje ir required CI module list ispletima Finding 1 + Finding 2 ribose.
- `Finding 3` ir `Finding 4` palikti velesniam live-validation / operability checkpoint ir siame wave nelieciami.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Pirma implementacijos banga yra vieninga `verification / CI contract hardening` tema, jungianti `Finding 1 + Finding 2`.
- `tests.test_repo_global_rules` refresh kritimas traktuojamas kaip verification fixture defektas pries metadata-first refresh kontrakta; `refresh_book_template.py` del to nekeiciamas.
- Required CI pavirsiaus ispletimas daromas per explicit unittest module list, ne per `unittest discover`.
- `Finding 3` ir `Finding 4` lieka uz sios bangos ribu iki atskiro live-validation / operability plano.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Atskirti `Plan audit wave 003` commit'a tik su `plans/audit-wave-003.md` ir `ENGINEERING_LEDGER.md`.
- Atskirti `Align repo-global-rules refresh test with metadata contract` commit'a tik su `tests/test_repo_global_rules.py`.
- Atskirti `Promote guard and rule-layering tests into required CI` commit'a tik su `.github/workflows/python-tests.yml`.
- Velesne atskira tema: `Finding 3` ir `Finding 4` live-validation / operability checkpoint.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Isplestas CI suite bus letesnis nei ankstesnis focused variantas, nors tai laikoma priimtina verification-depth kaina.
- Realus Whimsical auth/board render ir sviezio macOS bootstrap operability vis dar neirodyti vien is repo-local testu.
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
### 2026-03-31 09:28 | GitHub Actions bootstrap smoke parity
- Uzdaryta siaura CI parity tema: Darwin success smoke testas eksplicitiskai stubina platforma, o non-Darwin failure kontraktas paliktas atskiru testu.
- Po funkcinio commit o 0e95644 ledger isvalytas atskiru bookkeeping commit u, kad worktree vel butu svarus.

### 2026-03-30 15:21 | Codex context continuity and repo-engineering memory
- Užbaigtas runtime dependency hardening ir smoke testų sluoksnis.
- Užbaigta focused acceptance fixtures plėtra ir papildomi workflow acceptance testai.
- Užbaigtas test output noise cleanup sluoksnis.
<!-- ledger:completed:end -->
