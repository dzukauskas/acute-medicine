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
- Theme: Codex context continuity and repo-engineering memory
- Branch: main
- Last updated: 2026-03-30T15:22:41.947287+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- Supaprastinti ilgų Codex thread'ų darbą šiame repo, atskiriant vertimo ir repo-engineering atminties modelius.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- Pridėtas tracked ENGINEERING_LEDGER.md kaip kanoninė repo-engineering būsena.
- Atskirtas book translation workflow nuo repo engineering workflow dokumentacijos.
- write_codex_handoff.py paliktas tik kaip papildomas lokalus scratchpad įrankis.
- Nauji ledger ir handoff testai žali; pilna .venv suite praeina.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Repo-engineering ilgalaikė atmintis šiame projekte gyvena ENGINEERING_LEDGER.md, ne vien thread istorijoje.
- Book translation režimas remiasi research, chapter_pack, term_candidates ir QA artefaktais, ne engineering ledger.
- gitignored handoff failai nėra laikomi patikimu pirminiu cross-worktree atminties mechanizmu.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Peržiūrėti galutinį diff ir sucommitinti workflow pokyčius atskiru commit'u.
- Toliau naudoti ledger kaip pagrindinę repo-engineering atmintį naujoms auditų bangoms.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Hand off UI vis dar lieka rankinis; agentas gali tik rekomenduoti ir paruošti būseną.
- Jei ledger nebus atnaujinamas reikšmingų sprendimų vietose, jo vertė mažės.
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
### 2026-03-30 15:21 | Codex context continuity and repo-engineering memory
- Užbaigtas runtime dependency hardening ir smoke testų sluoksnis.
- Užbaigta focused acceptance fixtures plėtra ir papildomi workflow acceptance testai.
- Užbaigtas test output noise cleanup sluoksnis.
<!-- ledger:completed:end -->
