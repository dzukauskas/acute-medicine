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
- Theme: audit-wave-002 template-contract hardening
- Branch: main
- Last updated: 2026-03-30T22:45:08+03:00
<!-- ledger:active_theme:end -->

## Summary
<!-- ledger:summary:start -->
- `audit-wave-002` pirma banga (`template-contract hardening`) įgyvendinta ir užfiksuota commit'ais `18ddbb0`, `3281812`, `098aa3d` ir `afefb9f`.
- `audit-wave-002` klasifikacija išlieka: `valid` = 1, 3, 4, 5, 6; `partial` = 2; `invalid` = 7; `needs-clarification` = nėra.
- Pirma banga uždarė bendrą template kontraktą tarp bootstrap, refresh, tracked `book_metadata.yaml` truth sluoksnio ir focused CI parity vartų.
- `plans/audit-wave-002.md` atnaujintas su pirmos bangos progresu; `5/6` palikti atskirai vėlesnei portability / docs clarity bangai.
- Supaprastinti ilgų Codex thread'ų darbą šiame repo, atskiriant vertimo ir repo-engineering atminties modelius.
- Nauja fazė: `audit-wave-001` findings pirmiausia klasifikuoti prieš realų repo, tik po to svarstyti įgyvendinimą.
- `audit-wave-001` suverifikuota prieš realų repo: patvirtinti portabilumo, bootstrap side-effect, workstation-local config, subprocess timeout ir global sync namespace rizikos sluoksniai.
- `audit-wave-001` dabar pereina į įgyvendinimo planavimo fazę; tracked planas užfiksuotas `plans/audit-wave-001.md`.
- Įgyvendintas pirmos bangos finding `1`: canonical artefaktų path laukai normalizuoti į stabilų book-relative formatą be host-specific prefixų.
- Finding `1` užfiksuotas atskiru commit'u `0728ece` (`Normalize canonical artifact paths`).
- Įgyvendintas pirmos bangos finding `2`: bootstrap pagal nutylėjimą lieka repo-local, o Obsidian sync integracija keliama į explicit opt-in sluoksnį.
- Finding `2` užfiksuotas atskiru commit'u `c852e55` (`Make bootstrap sync install opt-in`).
- Įgyvendintas pirmos bangos finding `7`: kritiniai subprocess keliai perkelti į bendrą timeout-aware wrapper sluoksnį.
- Finding `7` užfiksuotas atskiru commit'u `136f0ca` (`Add subprocess timeouts to workflow scripts`).
- Įgyvendintas jungtinis `4/8` sluoksnis: local repo config override ir worktree-aware Obsidian sync namespace hardening.
- Findings `4/8` užfiksuoti atskiru commit'u `ebd8f19` (`Harden local config and sync namespace`).
- `AGENTS.md` localization policy suderinta su LT/EU-first workflow ir `Originalo kontekstas` taisykle.
- Finding `3` užfiksuotas atskiru commit'u `84009a4` (`Align AGENTS localization policy with LT/EU workflow`).
- Repo papildytas deklaruotu dev/test kontraktu: `requirements-dev.txt`, dokumentuotas `python -m unittest` entrypoint ir focused GitHub Actions workflow.
- Findings `5/6` užfiksuoti atskiru commit'u `964b491` (`Add repo-declared dev test contract`).
- `audit-wave-001` planuota įgyvendinimo seka uždaryta; tolesni hardening darbai turi būti vedami kaip nauja banga ar tema.
<!-- ledger:summary:end -->

## Current State
<!-- ledger:current_state:start -->
- `audit-wave-002` findings suklasifikuoti taip: `valid` = 1, 3, 4, 5, 6; `partial` = 2; `invalid` = 7; `needs-clarification` = nėra.
- Sukurtas tracked planas `plans/audit-wave-002.md`, o jo pirmos bangos progresas dabar užfiksuotas atskirais commit'ais.
- Pridėtas shared `workflow_book_template.py` helperis, kuris centralizuoja template manifest, required directories, template render ir `book_metadata.yaml` kontraktą.
- PDF ir EPUB bootstrap bei `refresh_book_template.py` perjungti ant shared template/materialization kontrakto ir nebeinferina canonical source iš live filesystem.
- JRCALC book root papildytas tracked `book_metadata.yaml`, o template-managed docs backfill'inti taip, kad sutaptų su template-rendered truth.
- Pridėtas `tests.test_book_template_parity` ir focused CI job dabar tikrina template-managed docs parity per tracked books.
- Focused CI ekvivalento paleidimas po pirmos bangos pakeitimų praėjo lokaliai: `51 tests / OK`.
- Tikslinis `tests.test_completeness_guard.CompletenessGuardTests.test_main_reports_missing_structured_block` pakartotinis paleidimas žalias, todėl tas signalas nelaikomas stabiliu `audit-wave-002` scope faktu.
- Pridėtas tracked ENGINEERING_LEDGER.md kaip kanoninė repo-engineering būsena.
- Atskirtas book translation workflow nuo repo engineering workflow dokumentacijos.
- write_codex_handoff.py paliktas tik kaip papildomas lokalus scratchpad įrankis.
- Pridėtas print_codex_resume_prompt.py, kad naujam thread būtų galima sugeneruoti minimalų promptą.
- Ledger atnaujinimas repo-engineering režime dokumentuotas kaip numatytasis agento darbas.
- `audit-wave-001` findings validavimo fazė užbaigta; pereita į planavimo ir pirmos įgyvendinimo bangos pradžią.
- `audit-wave-001` findings suklasifikuoti taip: `valid` = 1, 2, 4, 7, 8; `partial` = 3, 5, 6; `invalid` = nėra; `needs-clarification` = nėra.
- Portabilumo problema praktiškai patvirtinta ir eksperimentu: tas pats fixture skirtinguose laikinuose book root sugeneruoja nevienodus `chapter_pack` ir `adjudication_pack` failus dėl host-specific kelių.
- Sukurtas tracked plan failas `plans/audit-wave-001.md` su findings statusais ir bangų seka `1 -> 2 -> 7 -> 4/8`, o `3/5/6` palikti vėlesnei bangai.
- Pridėtas bendras canonical path normalizavimo helper sluoksnis generatoriams ir nauji portability regression testai.
- Realūs tracked `chapter_packs`, `adjudication_packs`, `research/*.checklist.md` ir susiję `research/*.md` metaduomenys backfill'inti į path-only relative formatą, neįtraukiant papildomo terminijos drift.
- Realus smoke patikrinimas `run_chapter_qa.py --book-root books/jrcalc-clinical-guidelines-2025-reference-edition 010` praėjo po backfill.
- Finding `1` atskirtas į savarankišką commit'ą `0728ece`, todėl nuo jo šalutinis drift jau izoliuotas.
- Finding `2` pakeičia PDF ir EPUB bootstrap kontraktą: be `--install-obsidian-sync` jie nebeįdiegia globalaus sync agento, o explicit install leidžiamas tik macOS.
- Focused bootstrap testai finding `2` sluoksniui praėjo: `tests.test_pdf_bootstrap_runtime`, `tests.test_epub_bootstrap_runtime`, `tests.test_epub_bootstrap_and_figures`, `tests.test_shell_entrypoints`.
- Finding `2` užfiksuotas atskiru commit'u `c852e55`, todėl pirmos bangos bootstrap side-effect sluoksnis jau izoliuotas.
- Pridėtas `workflow_subprocess.py` helperis su trumpu / numatytuoju / ilgu timeout profiliu ir aiškesniais phase-aware klaidų pranešimais.
- `run_chapter_qa.py`, `validate_adjudication_resolution.py`, PDF/EPUB bootstrap, `render_whimsical_figure.py` ir `register_whimsical_figure.py` kritiniai subprocess kvietimai perjungti į timeout-aware vykdymą.
- Focused finding `7` testai praėjo: `tests.test_workflow_subprocess`, `tests.test_run_chapter_qa`, `tests.test_validate_adjudication_resolution`, `tests.test_pdf_bootstrap_runtime`, `tests.test_epub_bootstrap_runtime`, `tests.test_render_whimsical_figure`, `tests.test_epub_bootstrap_and_figures`.
- Finding `7` užfiksuotas atskiru commit'u `136f0ca`, todėl timeout sluoksnis dabar izoliuotas nuo sekančios bangos.
- `workflow_runtime.py` dabar palaiko optional `repo_config.local.toml` override virš tracked `repo_config.toml` defaults, o `.gitignore` jo nebeseka.
- Bootstrap/template README nebeįkepa konkretaus workstation Obsidian kelio; vietoj to rodo generic runtime-resolved vault vietą.
- `workflow_obsidian.py` pridėtas worktree-aware LaunchAgent label suffix ir destination owner marker mechanizmas, kad tas pats default sync katalogas negalėtų būti tyliai perrašytas iš kito clone/worktree.
- Focused `4/8` testai praėjo: `tests.test_workflow_runtime`, `tests.test_obsidian_sync_safety`, `tests.test_refresh_template_runtime`, `tests.test_shell_entrypoints`, `tests.test_pdf_bootstrap_runtime`, `tests.test_epub_bootstrap_runtime`, `tests.test_epub_bootstrap_and_figures`.
- `4/8` diff peržiūrėtas kaip vientisas vieno kontrakto pjūvis: local config layering, generic tracked docs ir global sync namespace apsauga.
- `AGENTS.md` sulygintas su LT/EU-first workflow: foreign-market normativity pagrindiniame LT tekste nebeleidžiama, o išlaikomas kontekstas keliamas tik į `Originalo kontekstas`.
- Finding `3` commit'as `84009a4` izoliuoja policy alignment nuo likusio dev/test sluoksnio.
- Repo dabar turi deklaruotą dev/test kontraktą: `requirements-dev.txt`, bootstrap verification entrypoint ir focused `.github/workflows/python-tests.yml`.
- `scripts/bootstrap_macos.sh` diegia `requirements-dev.txt` ir išveda repo-native smoke / contract unittest žingsnį.
- Focused `5/6` testai praėjo: `tests.test_shell_entrypoints`, `tests.test_end_to_end_workflow_contract`, `tests.test_workflow_runtime`, `tests.test_obsidian_sync_safety`, `tests.test_refresh_template_runtime`.
- Findings `5/6` commit'as `964b491` izoliuoja dev/test kontrakto sluoksnį nuo policy pakeitimo.
- `audit-wave-001` bangos `1 -> 2 -> 7 -> 4/8 -> 3 -> 5/6` yra uždarytos.
<!-- ledger:current_state:end -->

## Accepted Decisions
<!-- ledger:decisions:start -->
- Repo-engineering ilgalaikė atmintis šiame projekte gyvena ENGINEERING_LEDGER.md, ne vien thread istorijoje.
- Book translation režimas remiasi research, chapter_pack, term_candidates ir QA artefaktais, ne engineering ledger.
- gitignored handoff failai nėra laikomi patikimu pirminiu cross-worktree atminties mechanizmu.
- Naujo thread startui pirmiausia siūlomas minimalus resume promptas, o ne vartotojo improvizacija.
- Audit findings nebus įgyvendinami aklai; kiekvienas teiginys pirmiausia turi būti klasifikuotas kaip `valid`, `invalid`, `partial` arba `needs-clarification` pagal realų repo.
- `audit-wave-002` šiame etape laikoma nauja repo-engineering banga, bet ne nauja technine tema už jos ribų, todėl validavimo darbą logiška tęsti šiame pačiame thread, kol nepasikeis scope.
- `audit-wave-002` pirma įgyvendinimo banga užrakinama kaip vienas `template-contract hardening` branduolys: findings `1 + 3 + 4`, o finding `2` laikomas partial to paties kontrakto simptomu, ne atskira banga.
- `audit-wave-002` pirma banga laikoma užbaigta, kai shared template helper, metadata truth sluoksnis, JRCALC backfill ir parity gate visi kartu yra žali focused suite kontekste.
- `audit-wave-002` findings `5/6` sąmoningai paliekami atskirai vėlesnei portability / docs clarity bangai.
- `audit-wave-002` finding `2` laikomas tik dalinai teisingu: shared materialization kontraktas tarp bootstrap ir refresh tikrai išsiskyręs, bet reportuotas dabartinis live failure nepasitvirtino, nes template required katalogai šiame checkout'e yra tracked ir bootstrap testai praeina.
- `audit-wave-002` finding `7` laikomas neteisingu: `handoffs/README.md` repo egzistuoja ir yra tracked, todėl continuity modelio reference nėra sulūžęs.
- `audit-wave-001` 3-iasis finding'as laikomas tik dalinai teisingu: book workflow failai jau duoda LT/EU-first operacinį default'ą, bet `AGENTS.md` formuluotė lieka dviprasmė ir turi būti suderinta.
- `audit-wave-001` finding `2` sprendžiamas taip: core bootstrap pagal nutylėjimą lieka repo-local, o globalus Obsidian / `launchd` integracijos žingsnis tampa explicit opt-in per `--install-obsidian-sync`.
- `audit-wave-001` finding `7` sprendžiamas per bendrą subprocess wrapper sluoksnį su default timeout'ais ir aiškesniais klaidų pranešimais.
- `audit-wave-001` finding `7` timeout politika naudoja bendrą helper'į ir palieka ilgesnį profilį build tipo veiksmams (`chapter_pack`, `adjudication_pack`), o trumpą profilį lightweight probe veiksmams.
- `audit-wave-001` finding `4` sprendžiamas per tracked defaults + optional `repo_config.local.toml` override modelį ir per docs/template sluoksnį, kuris nebeįkepa workstation-specific vault kelių.
- `audit-wave-001` finding `8` sprendžiamas per worktree-aware LaunchAgent label bei destination owner marker'į, kuris blokuoja tylų default sync katalogo perėmimą iš kitos darbo vietos.
- `audit-wave-001` finding `3` sprendžiamas sulyginant `AGENTS.md` su binding LT/EU-first workflow ir aiškiai iškeliant foreign-market normativity iš pagrindinio LT teksto į `Originalo kontekstas`.
- `audit-wave-001` findings `5/6` šiame etape sprendžiami per deklaruotą repo-native dev/test kontraktą, o ne per pilną visų stub'intų acceptance kelių eliminaciją vienu wave.
<!-- ledger:decisions:end -->

## Next Steps
<!-- ledger:next_steps:start -->
- `audit-wave-002` pirmą bangą laikyti uždaryta.
- Jei bus tęsiamas `audit-wave-002`, kitą darbą planuoti tik kaip atskirą `5/6` portability / docs clarity bangą.
- Kai bus patogu, po pirmo realaus push patikrinti GitHub Actions workflow rezultatą, nes focused CI šioje bangoje verifikuotas lokaliai, bet dar ne live run'u.
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
