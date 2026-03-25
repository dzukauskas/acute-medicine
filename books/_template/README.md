# {{BOOK_TITLE}}

Šis katalogas yra atskira darbo vieta knygai *{{BOOK_TITLE}}*.

## Kanoninis PDF

- `source/pdf/{{BOOK_PDF_NAME}}`

## Struktūra

- `source/pdf/`: kanoninis PDF.
- `source/chapters-en/`: iš PDF ištraukti angliški skyriai tik navigacijai ir sutikrinimui.
- `source/index/`: skyriaus indeksai ir puslapių intervalai.
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
- `termbase.tsv`, `acronyms.tsv`, `gold_phrases.tsv`, `gold_sections/`, `localization_overrides.tsv`: reusable taisyklių sluoksniai.
- `localization_signals.base.tsv`: shared UK / Australia / rinkos signalų registry.
- `localization_signals.tsv`: knygos papildomi signalai, jei shared registry nepakanka.
- `clinical_policy_markers.tsv`: norminio vaistų turinio detektoriaus markeriai.

## Taisyklė

Skyrių tekstas, lentelės, schemos ir paveikslai kuriami nuo naujo tik iš PDF ir naujausių patikrintų Lietuvos bei, jei reikia, Europos šaltinių.

Pagrindinis LT tekstas yra skirtas Lietuvos medicinos studijoms ir praktikai, todėl:

- pagrindiniame tekste paliekama tik LT / ES logika;
- UK, Australijos ar kitos originalo rinkos sistemos informacija negali likti kaip tariamas vietinis standartas;
- tokia informacija, jei ji pedagogiškai naudinga, leidžiama tik aiškiai pažymėtame `Originalo kontekstas` bloke;
- vaistų pavadinimai pagal nutylėjimą teikiami bendriniu / INN vardu, o ne originalo rinkos prekiniais vardais;
- dozės, vartojimo keliai, indikacijos ir kontraindikacijos negali būti perkeliami vien iš knygos be LT ar ES atramos.

Jei kyla abejonių dėl LT termino, kolokacijos ar klinikinės kategorijos pavadinimo, prieš pasirenkant formuluotę privaloma patikrinti Lietuvos medicininę vartoseną internete ir tą patikrą užfiksuoti `research` faile.

Diagramoms ir algoritmams šiame projekte naudojamas tik `Whimsical` workflow. Jei vartotojas nurodo konkretų įrankį, jo negalima savavališkai pakeisti kitu.

PDF šaltinių bootstrap ir tekstinis extraction šiame repo yra `PyMuPDF-first`. Jei skriptas paleidžiamas su sistemos `python3`, bet `PyMuPDF` ten nėra, jis automatiškai persijungia į repo `.venv`, jei ji paruošta.

Jei PDF turinio puslapiai nėra patikimai parsinuojami automatiškai, naudokite chapter map sidecar:

- `source/pdf/<book>.chapters.yaml`

arba bootstrap metu perduokite:

- `--chapter-map /abs/path/to/<book>.chapters.yaml`

## Bendrų skriptų taikymas šiai knygai

Kai naudojate bendrus repo skriptus, aktyvią knygą nukreipkite per:

- `MEDBOOK_ROOT=books/{{BOOK_SLUG}}`

Pavyzdžiai:

- `MEDBOOK_ROOT=books/{{BOOK_SLUG}} python3 scripts/build_chapter_pack.py 001`
- `MEDBOOK_ROOT=books/{{BOOK_SLUG}} python3 scripts/run_chapter_qa.py 001`

## Obsidian sync

Numatytasis Obsidian kelias šiai knygai:

- `{{OBSIDIAN_DEST}}`

Jis generuojamas iš root `repo_config.toml`, todėl vault ar `launchd` prefiksą keiskite ten, o ne book-specific skriptuose.

Vienkartinis sync:

- `MEDBOOK_ROOT=books/{{BOOK_SLUG}} scripts/sync_obsidian_book.sh`

Automatinis `launchd` sync agentas:

- `scripts/install_obsidian_sync_agent.sh --book-root books/{{BOOK_SLUG}}`
