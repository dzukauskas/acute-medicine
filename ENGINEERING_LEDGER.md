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
- Last updated: 2026-03-30T19:25:33+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- Supaprastinti ilgų Codex thread'ų darbą šiame repo, atskiriant vertimo ir repo-engineering atminties modelius.
- Nauja fazė: `audit-wave-001` findings pirmiausia klasifikuoti prieš realų repo, tik po to svarstyti įgyvendinimą.
- `audit-wave-001` suverifikuota prieš realų repo: patvirtinti portabilumo, bootstrap side-effect, workstation-local config, subprocess timeout ir global sync namespace rizikos sluoksniai.
- `audit-wave-001` dabar pereina į įgyvendinimo planavimo fazę; tracked planas užfiksuotas `plans/audit-wave-001.md`.
- Įgyvendintas pirmos bangos finding `1`: canonical artefaktų path laukai normalizuoti į stabilų book-relative formatą be host-specific prefixų.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- Pridėtas tracked ENGINEERING_LEDGER.md kaip kanoninė repo-engineering būsena.
- Atskirtas book translation workflow nuo repo engineering workflow dokumentacijos.
- write_codex_handoff.py paliktas tik kaip papildomas lokalus scratchpad įrankis.
- Pridėtas print_codex_resume_prompt.py, kad naujam thread būtų galima sugeneruoti minimalų promptą.
- Ledger atnaujinimas repo-engineering režime dokumentuotas kaip numatytasis agento darbas.
- Darbinis medis šiuo metu švarus `main` brancho būsenoje.
- `audit-wave-001` findings validavimo fazė užbaigta; pereita į planavimo ir pirmos įgyvendinimo bangos pradžią.
- `audit-wave-001` findings suklasifikuoti taip: `valid` = 1, 2, 4, 7, 8; `partial` = 3, 5, 6; `invalid` = nėra; `needs-clarification` = nėra.
- Portabilumo problema praktiškai patvirtinta ir eksperimentu: tas pats fixture skirtinguose laikinuose book root sugeneruoja nevienodus `chapter_pack` ir `adjudication_pack` failus dėl host-specific kelių.
- Sukurtas tracked plan failas `plans/audit-wave-001.md` su findings statusais ir bangų seka `1 -> 2 -> 7 -> 4/8`, o `3/5/6` palikti vėlesnei bangai.
- Pridėtas bendras canonical path normalizavimo helper sluoksnis generatoriams ir nauji portability regression testai.
- Realūs tracked `chapter_packs`, `adjudication_packs`, `research/*.checklist.md` ir susiję `research/*.md` metaduomenys backfill'inti į path-only relative formatą, neįtraukiant papildomo terminijos drift.
- Realus smoke patikrinimas `run_chapter_qa.py --book-root books/jrcalc-clinical-guidelines-2025-reference-edition 010` praėjo po backfill.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Repo-engineering ilgalaikė atmintis šiame projekte gyvena ENGINEERING_LEDGER.md, ne vien thread istorijoje.
- Book translation režimas remiasi research, chapter_pack, term_candidates ir QA artefaktais, ne engineering ledger.
- gitignored handoff failai nėra laikomi patikimu pirminiu cross-worktree atminties mechanizmu.
- Naujo thread startui pirmiausia siūlomas minimalus resume promptas, o ne vartotojo improvizacija.
- Audit findings nebus įgyvendinami aklai; kiekvienas teiginys pirmiausia turi būti klasifikuotas kaip `valid`, `invalid`, `partial` arba `needs-clarification` pagal realų repo.
- `audit-wave-001` 3-iasis finding'as laikomas tik dalinai teisingu: book workflow failai jau duoda LT/EU-first operacinį default'ą, bet `AGENTS.md` formuluotė lieka dviprasmė ir turi būti suderinta.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- Pereiti prie finding `2`: atskirti core bootstrap nuo globalaus Obsidian / LaunchAgent integracijos sluoksnio ir įvesti explicit sync semantiką.
- Po finding `2` pereiti prie subprocess timeout sluoksnio (`7`), tada prie `repo_config` ir global sync namespace temos (`4/8`).
- Vėlesnėse bangose spręsti `AGENTS.md` politikos suderinimą, test environment / CI kontraktą ir test harness gylio spragas.
<!-- ledger:next_steps:end -->

## Open Risks
<!-- ledger:risks:start -->
- Hand off UI vis dar lieka rankinis; agentas gali tik rekomenduoti ir paruošti būseną.
- Jei ledger nebus atnaujinamas reikšmingų sprendimų vietose, jo vertė mažės.
- Kol neapsispręsta dėl 8-o finding'o produkto lygio kontrakto, lieka atskiras klausimas, ar same-book multi-worktree / multi-clone sync bus oficialiai palaikomas, ar tik saugiai blokuojamas.
<!-- ledger:risks:end -->

## Completed Themes
<!-- ledger:completed:start -->
### 2026-03-30 15:21 | Codex context continuity and repo-engineering memory
- Užbaigtas runtime dependency hardening ir smoke testų sluoksnis.
- Užbaigta focused acceptance fixtures plėtra ir papildomi workflow acceptance testai.
- Užbaigtas test output noise cleanup sluoksnis.
<!-- ledger:completed:end -->
