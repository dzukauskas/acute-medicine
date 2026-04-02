# JRCALC Clinical Guidelines 2025 Reference Edition

Šis katalogas yra atskira darbo vieta knygai *JRCALC Clinical Guidelines 2025 Reference Edition*.

## Kanoninis originalo failas

- `source/epub/JRCALC Clinical Guidelines 2025 Reference Edition.epub`

## Struktūra

- `source/pdf/`: kanoninis PDF, jei knyga bootstrap'inta iš PDF.
- `source/epub/`: kanoninis EPUB, jei knyga bootstrap'inta iš EPUB.
- `source/chapters-en/`: iš originalo ištraukti angliški skyriai tik navigacijai ir sutikrinimui.
- `source/index/`: skyriaus indeksai ir source inventory failai.
- `source/index/figures.tsv`: chapter-referenced source paveikslų kandidatų inventorius.
- `source/figures-raw/`: iš originalo ištraukti source image assetai.
- `lt/chapters/`: nuo naujo rašomi lietuviški skyriai.
- `lt/figures/`: lietuviškos schemos ir paveikslai.
- `lt/figures/manifest.tsv`: aktyvių paveikslų kanoninių `Whimsical` šaltinių registras.
- `chapter_packs/`: chapter-specific preflight paketai.
- `adjudication_packs/`: high-risk blokų targeted adjudication paketai.
- `research/`: skyriaus šaltinių ir sprendimų failai.
- `review_deltas/`: struktūriniai rankinio review skirtumai.
- `term_candidates.tsv`: book-level terminų ir santrumpų kandidatų inbox, renkamas per skyrių workflow prieš promotion.
- `regression_examples/`: trumpi „blogai -> gerai“ pavyzdžiai būsimiems promptams ir regresijų kontrolei.
- `archive/`: knygos vidinis archyvas.
- `workflow.md`: kanoninis šios knygos darbo workflow.
- `source-priority.md`: šaltinių prioritetas klinikinėms ir terminologinėms vietoms.
- `language-style.md`: LT medicininės prozos, tipografijos ir anglų terminų rodymo taisyklės.
- `translation-style.md`: vertimo ir anti-calque disciplina.
- `drafting-scaffold.md`: minimali drafting seka, kai aktyvus `chapter_pack`.
- `termbase.local.tsv`, `acronyms.local.tsv`, `gold_phrases.local.tsv`, `calque_patterns.local.tsv`, `disallowed_terms.local.tsv`, `disallowed_phrases.local.tsv`, `localization_overrides.local.tsv`, `localization_signals.local.tsv`, `adjudication_profiles.local.tsv`: optional book-local override stub'ai.
- `gold_sections/`: optional local pozityvių pavyzdžių sluoksnis.

Repo-global aktyvios taisyklės laikomos `shared/` kataloge:

- `shared/lexicon/`: termbase ir akronimai.
- `shared/prose/`: gold phrase, calque ir disallowed taisyklės.
- `shared/localization/`: localization override'ai, signalai, clinical marker'iai ir `lt_source_map`.
- `shared/review/`: review taxonomy ir adjudication profiliai.
- `shared/examples/gold_sections/`: bendri pozityvūs skyrių pavyzdžiai.

## Codex thread continuity

Jei thread gali kompaktuotis arba reikės naujo thread, pirmiausia užfiksuok paskutinę patikrintą būseną kanoniniuose artefaktuose. Šiai knygai tai reiškia `research`, `chapter_packs/<slug>.yaml`, `term_candidates.tsv`, `lt/chapters/` ir, jei reikia, `adjudication_packs/<slug>.yaml`.

Automatinis QA šiame workflow yra rerunnable pipeline per `scripts/run_chapter_qa.py`, o ne stored machine-readable receipt.

## Taisyklė

Skyrių tekstas, lentelės, schemos ir paveikslai kuriami nuo naujo tik iš kanoninio originalo failo ir naujausių patikrintų Lietuvos bei, jei reikia, Europos šaltinių.

Pagrindinis LT tekstas yra skirtas Lietuvos medicinos studijoms ir praktikai, todėl:

- pagrindiniame tekste paliekama tik LT / ES logika;
- UK, Australijos, JAV ar kitos originalo rinkos sistemos informacija negali likti kaip tariamas vietinis standartas;
- tokia informacija, jei ji pedagogiškai naudinga, leidžiama tik aiškiai pažymėtame `Originalo kontekstas` bloke;
- vaistų pavadinimai pagal nutylėjimą teikiami bendriniu / INN vardu, o ne originalo rinkos prekiniais vardais;
- dozės, vartojimo keliai, indikacijos ir kontraindikacijos negali būti perkeliami vien iš knygos be LT ar ES atramos.

Jei kyla abejonių dėl LT termino, kolokacijos ar klinikinės kategorijos pavadinimo, prieš pasirenkant formuluotę privaloma patikrinti Lietuvos medicininę vartoseną internete ir tą patikrą užfiksuoti `research` faile.

Prieš pildydami `research` failą, naudokite `shared/localization/lt_source_map.tsv` ir `source-priority.md`, kad iškart pasirinktumėte teisingą LT-source kelią pagal temą: paramediko kompetencija, GMP, farmakologija, vaistų registracija, kompensavimas, infekcijos, specialybinės rekomendacijos, terminija ar fundamentiniai mokslai.

Prieš pildydami realų `research/<slug>.md`, galite sugeneruoti pagalbinį checklist failą:

- `MEDBOOK_ROOT=books/jrcalc-clinical-guidelines-2025-reference-edition .venv/bin/python scripts/generate_research_checklist.py 001`

Jis sukuria `research/<slug>.checklist.md` su:

- preliminaria norminių claim tipų matrica;
- preliminaria struktūrinių blokų lokalizacijos lentele;
- rekomenduojamais LT-source keliais pagal `shared/localization/lt_source_map.tsv`;
- aptiktais UK / Australia / US / rinkos signalais iš source skyriaus.

Review metu pasikartojančios taisyklės pirmiausia fiksuojamos `review_deltas/` ar book-local override sluoksnyje, o į `shared/` keliamos tik per review-gated promotion.

`term_candidates.tsv` nėra aktyvi taisyklių bazė. Tai tik kandidatinis inbox:

- `build_chapter_pack.py` automatiškai atnaujina einamo skyriaus kandidatus;
- kandidatai renkami iš `## Rizikingi terminai` ir iš source aptiktų nežinomų santrumpų;
- jei kandidatas jau yra `shared/lexicon/` bazėse arba yra tik lokalizacijos signalas / rinkos proper noun, jis į inbox nepatenka;
- `shared/lexicon/termbase.tsv` ir `shared/lexicon/acronyms.tsv` pildomi tik po review.

Diagramoms ir algoritmams šiame projekte naudojamas tik `Whimsical` workflow. Jei vartotojas nurodo konkretų įrankį, jo negalima savavališkai pakeisti kitu.

PDF šaltinių bootstrap ir tekstinis extraction šiame repo yra `PyMuPDF-first`. EPUB bootstrap ir XHTML extraction vyksta per `EbookLib` ir `BeautifulSoup`. Jei skriptas paleidžiamas su sistemos `python3`, bet trūksta reikalingų modulių, jis automatiškai persijungia į repo `.venv`, jei ji paruošta.
Po repo bootstrap canonical interpreterius šios knygos Python skriptams yra `.venv/bin/python`.

Jei PDF ar EPUB TOC parseris negali patikimai nustatyti skyrių ribų, naudokite chapter map sidecar:

- `source/<kind>/<book>.chapters.yaml`

arba bootstrap metu perduokite:

- `--chapter-map /abs/path/to/<book>.chapters.yaml`

EPUB bootstrap automatiškai sukuria `source/index/figures.tsv`, bet tai nėra aktyvus `Whimsical` manifestas. Į `lt/figures/manifest.tsv` patenka tik tie paveikslai, kuriems jau sukurtas `Whimsical` board ir sugeneruotas aktyvus `png`.

Aktyvaus paveikslo completion kontraktas:

- `scripts/register_whimsical_figure.py` registracijos metu ne tik sukuria manifest įrašą ir sugeneruoja `png`, bet ir automatiškai įterpia paveikslą į atitinkamą `lt/chapters/<slug>.md`;
- paveikslas laikomas užbaigtu repo viduje tik tada, kai egzistuoja visi trys sluoksniai: `lt/figures/manifest.tsv`, `lt/figures/*.png` ir įterptas paveikslas `lt/chapters/*.md`;
- `scripts/validate_figures_manifest.py` tikrina ne tik manifest -> failas, bet ir active manifest -> chapter embed kontraktą;
- jei reikia iškart atnaujinti live vault, naudokite `scripts/register_whimsical_figure.py --sync-obsidian` arba atskirą `scripts/sync_obsidian_book.sh`.

## Bendrų skriptų taikymas šiai knygai

Kai naudojate bendrus repo skriptus, aktyvią knygą nukreipkite per:

- `MEDBOOK_ROOT=books/jrcalc-clinical-guidelines-2025-reference-edition`

Pavyzdžiai:

- `MEDBOOK_ROOT=books/jrcalc-clinical-guidelines-2025-reference-edition .venv/bin/python scripts/build_chapter_pack.py 001`
- `MEDBOOK_ROOT=books/jrcalc-clinical-guidelines-2025-reference-edition .venv/bin/python scripts/run_chapter_qa.py 001`

## Obsidian sync

Numatytasis Obsidian kelias šiai knygai:

- `<configured-obsidian-vault>/JRCALC Clinical Guidelines 2025 Reference Edition`

Jis runtime metu sprendžiamas iš root `repo_config.toml` ir pasirenkamo `repo_config.local.toml`, todėl workstation-specific override laikykite ten, o ne book-specific skriptuose.

Vienkartinis sync:

- `MEDBOOK_ROOT=books/jrcalc-clinical-guidelines-2025-reference-edition scripts/sync_obsidian_book.sh`

Repo `lt/chapters/` lieka flat, bet sync į Obsidian gali sugrupuoti skyrius į `Section` aplankus pagal `source/index/chapters.json`, kad vault navigacija atitiktų leidinio struktūrą.
`sync_obsidian_book.sh` remiasi `bash`; atskiro `zsh` requirement nėra.

Automatinis `launchd` sync agentas:

- `scripts/install_obsidian_sync_agent.sh --book-root books/jrcalc-clinical-guidelines-2025-reference-edition`

`install_obsidian_sync_agent.sh` yra macOS-specific, nes naudoja `launchd` / `launchctl`.
Sync paskirtis papildomai rezervuojama konkrečiai darbo vietai, todėl kitas clone ar worktree negali tyliai perrašyti to paties default katalogo.
