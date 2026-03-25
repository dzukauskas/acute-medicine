# {{BOOK_TITLE}} Workflow

## Tikslas

Galutinis rezultatas yra lietuviškas mokymosi tekstas, pritaikytas Lietuvos medicinos ir, jei reikia, Europos gairių logikai.

Tai nėra pažodinis originalo rinkos vertimas.

## Kanoninis šaltinis

Kanoninis šaltinis visada yra:

- `books/{{BOOK_SLUG}}/source/pdf/{{BOOK_PDF_NAME}}`

`source/chapters-en/` failai yra tik pagalbinė navigacija. Jie niekada nepakeičia pilno PDF perskaitymo.
PDF bootstrap ir chapter extraction vykdomi per `PyMuPDF`, ne per ad hoc CLI dump'us.
Jei TOC parseris negali patikimai nustatyti skyrių ribų, naudojamas `chapter map` YAML sidecar (`<pdf-stem>.chapters.yaml`).

Bendri repo skriptai šiai knygai kviečiami su:

- `MEDBOOK_ROOT=books/{{BOOK_SLUG}}`

## Vienas skyrius = vienas užbaigtas ciklas

Skyrius laikomas baigtu tik kai:

1. perskaitytas visas PDF puslapių intervalas;
2. sudarytas pilnas skyriaus inventorius;
3. patikrinti naujausi prieinami Lietuvos šaltiniai;
4. jei jų nepakanka, patikrintos naujausios Europos ar tarptautinės gairės;
4a. `lt_source_map.tsv` ir `source-priority.md` pagalba parinktas teisingas LT-source kelias pagal skyriaus temą;
4b. `research` faile užfiksuoti visi UK / Australia / US / kiti rinkos signalai ir jiems parinktas LT/EU pakeitimo sprendimas;
5. sugeneruotas `chapter_pack`;
6. lietuviškas skyrius parašytas nuo švaraus lapo pagal `chapter_pack`;
7. padarytas atskiras anti-calque perrašymas;
8. lentelės pilnai išverstos;
9. schemos, paveikslai ir `chart` tipo originalo grafikai atkurti lietuviškai arba aiškiai sutraukti į LT bloką;
10. jei skyriuje yra `high-risk` blokų, jiems sugeneruotas `adjudication_pack`;
11. viskas sutikrinta su PDF;
12. paleistas terminų, prozos, tipografijos ir komplektiškumo QA;
13. jei skyrius buvo taisytas ranka, užfiksuotas `review_delta` ir parengti rule-promotion kandidatai.

## `Chapter pack` taisyklė

Prieš bet kokį drafting skyriui privaloma sugeneruoti `chapter_packs/<slug>.yaml`.

`chapter_pack` yra vykdomas preflight artefaktas, o ne papildoma dokumentacija. Jis turi apjungti:

- skyriaus blokų inventorių;
- blokų `tags[]` ir `adjudication_candidate`;
- aktyvius terminus ir akronimus;
- lokalizacijos override'us;
- stiliaus hotspot'us;
- pozityvius LT pavyzdžius iš `gold_phrases.tsv` ir `gold_sections/`.

Be `chapter_pack` drafteris negali pradėti generavimo.

`build_chapter_pack.py` taip pat yra LT/EU-first vartai: jei source skyriuje aptinkami UK / Australia / US signalai, bet `research` faile jiems nėra aiškaus LT/EU sprendimo, pack generavimas turi baigtis klaida.

Prieš research ir drafting visada pirmiausia nuspręskite, kuriam LT-source branduolio keliui priklauso skyrius ar konkretus blokas:

- paramediko kompetencija ir GMP;
- vaistų registracija ir produkto informacija;
- kompensavimas ir LT rinkos prieinamumas;
- farmakologija ir racionalus skyrimas;
- infekcijos ir visuomenės sveikata;
- klinikinės metodikos ir specialybinės rekomendacijos;
- teisė ir reguliavimas;
- terminija ir kalbos forma;
- anatomija, fiziologija ir patofiziologija.

## Section-type drafting

Skyriaus blokai generuojami ne vienu universaliu režimu, o pagal `draft_mode` iš `chapter_pack`:

- `narrative-prose`
- `table-compression`
- `algorithm-stepwise`
- `local-context-callout`

`chart` tipo blokai turi būti inventorizuojami atskirai nuo `table`, `figure_caption` ir `callout`, net jei LT variante jie sutraukiami į vieną aiškų paaiškinamąjį bloką.

Jei keli `chart` blokai sutraukiami į vieną LT summary sekciją, joje turi būti coverage įrodymas:

- arba matomi per-chart pėdsakai;
- arba techninis markeris `<!-- chart-coverage: 1,2,3 -->`.

## Targeted adjudication

Jei `chapter_pack` pažymi `adjudication_candidate: true`, prieš galutinį polishą reikia sugeneruoti `adjudication_packs/<slug>.yaml`.

Po targeted adjudication `research/<slug>.md` faile turi likti `## Adjudication sprendimai` sekcija fiksuotu formatu:

- `- <block_id> | <A|B|hibridinis> | <trumpa priežastis>`

Bet koks kitas laisvas formatas laikomas klaida.

## Lokalizacijos taisyklė

Kai originalo logika ar sistemos kontekstas nesutampa su Lietuvos praktika:

- pagrindiniame tekste taikoma Lietuvos logika;
- neatitikimas pažymimas `research` faile;
- jei reikia, skyriuje paliekamas trumpas `Originalo kontekstas` callout.

Šiai knygai privalomas LT/EU-first principas:

- pagrindinis LT tekstas negali rodyti UK, Australijos ar JAV sistemos kaip norminio standarto;
- UK / Australia / US institucijos, guideline vardai, teisės mechanizmai ir reference įrankiai paliekami tik tada, kai jie aiškiai pažymėti kaip originalo kontekstas;
- vaistų pavadinimai pagal nutylėjimą turi būti bendriniai / INN;
- jei originalo rinkos prekinis vardas mokymuisi nereikalingas, jis išmetamas;
- jei LT oficialaus šaltinio nėra, pagrindiniame tekste remiamasi ES šaltiniu, o tai užfiksuojama `research` faile.

Jei kyla abejonių dėl LT termino, kolokacijos ar klinikinės kategorijos pavadinimo, sprendimo negalima priimti „iš klausos“. Pirma reikia patikrinti Lietuvos medicininę vartoseną internete ir `research` faile užrašyti bent šaltinį bei datą.

## Dvigubas QA

Kiekvienas skyrius turi praeiti du atskirus kokybės vartus:

1. `Clinical QA`
2. `Language QA`

`Language QA` privalomai apima:

- atskirą anti-calque perrašymą;
- `scripts/validate_localization_readiness.py` prieš pack generavimą;
- `scripts/validate_adjudication_resolution.py`, jei skyriuje yra `adjudication_candidate`;
- sutikrinimą su `language-style.md`;
- `scripts/prose_guard.py`;
- `scripts/lt_style_guard.py`;
- `scripts/terminology_guard.py` su `chapter_pack`, jei jis yra;
- `scripts/localization_guard.py` su `chapter_pack`;
- `scripts/completeness_guard.py`;
- trumpą rankinį kalbinį auditą.

## Paveikslų taisyklė

Kiekvienam paveikslui ar algoritmui:

1. parenkamas vienas kanoninis šaltinis ir jis įrašomas į `lt/figures/manifest.tsv`;
2. vienintelė aktyvi redaguojama forma šiame projekte yra `Whimsical` lenta;
3. į repo saugomas galutinis `png`, skirtas `Obsidian` ir skyriaus `md` failams;
4. jei `Whimsical` kelias šioje sesijoje neveikia, darbas stabdomas ir aiškiai įvardijamas blokatorius.
