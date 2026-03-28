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

- `MEDBOOK_ROOT=books/jrcalc-clinical-guidelines-2025-reference-edition python3 scripts/generate_research_checklist.py 001`

Jis sukuria `research/<slug>.checklist.md` su:

- preliminaria norminių claim tipų matrica;
- preliminaria struktūrinių blokų lokalizacijos lentele;
- rekomenduojamais LT-source keliais pagal `shared/localization/lt_source_map.tsv`;
- aptiktais UK / Australia / US / rinkos signalais iš source skyriaus.

Review metu pasikartojančios taisyklės pirmiausia fiksuojamos `review_deltas/` ar book-local override sluoksnyje, o į `shared/` keliamos tik per review-gated promotion.

Diagramoms ir algoritmams šiame projekte naudojamas tik `Whimsical` workflow. Jei vartotojas nurodo konkretų įrankį, jo negalima savavališkai pakeisti kitu.

PDF šaltinių bootstrap ir tekstinis extraction šiame repo yra `PyMuPDF-first`. EPUB bootstrap ir XHTML extraction vyksta per `EbookLib` ir `BeautifulSoup`. Jei skriptas paleidžiamas su sistemos `python3`, bet trūksta reikalingų modulių, jis automatiškai persijungia į repo `.venv`, jei ji paruošta.

Jei PDF ar EPUB TOC parseris negali patikimai nustatyti skyrių ribų, naudokite chapter map sidecar:

- `source/<kind>/<book>.chapters.yaml`

arba bootstrap metu perduokite:

- `--chapter-map /abs/path/to/<book>.chapters.yaml`

EPUB bootstrap automatiškai sukuria `source/index/figures.tsv`, bet tai nėra aktyvus `Whimsical` manifestas. Į `lt/figures/manifest.tsv` patenka tik tie paveikslai, kuriems jau sukurtas `Whimsical` board ir sugeneruotas aktyvus `png`.

## Bendrų skriptų taikymas šiai knygai

Kai naudojate bendrus repo skriptus, aktyvią knygą nukreipkite per:

- `MEDBOOK_ROOT=books/jrcalc-clinical-guidelines-2025-reference-edition`

Pavyzdžiai:

- `MEDBOOK_ROOT=books/jrcalc-clinical-guidelines-2025-reference-edition python3 scripts/build_chapter_pack.py 001`
- `MEDBOOK_ROOT=books/jrcalc-clinical-guidelines-2025-reference-edition python3 scripts/run_chapter_qa.py 001`

## Obsidian sync

Numatytasis Obsidian kelias šiai knygai:

- `/Users/dzukauskas/Library/Mobile Documents/iCloud~md~obsidian/Documents/PARAMEDIKAS/JRCALC Clinical Guidelines 2025 Reference Edition`

Jis generuojamas iš root `repo_config.toml`, todėl vault ar `launchd` prefiksą keiskite ten, o ne book-specific skriptuose.

Vienkartinis sync:

- `MEDBOOK_ROOT=books/jrcalc-clinical-guidelines-2025-reference-edition scripts/sync_obsidian_book.sh`

Automatinis `launchd` sync agentas:

- `scripts/install_obsidian_sync_agent.sh --book-root books/jrcalc-clinical-guidelines-2025-reference-edition`
