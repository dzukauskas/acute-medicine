# JRCALC Clinical Guidelines 2025 Reference Edition Workflow

## Tikslas

Galutinis rezultatas yra lietuviškas mokymosi tekstas, pritaikytas Lietuvos medicinos ir, jei reikia, Europos gairių logikai.

Tai nėra pažodinis originalo rinkos vertimas.

## Kanoninis šaltinis

Kanoninis šaltinis visada yra:

- `books/jrcalc-clinical-guidelines-2025-reference-edition/source/epub/JRCALC Clinical Guidelines 2025 Reference Edition.epub`

`source/chapters-en/` failai yra tik pagalbinė navigacija. Jie niekada nepakeičia pilno originalo perskaitymo.
PDF bootstrap ir chapter extraction vykdomi per `PyMuPDF`, o EPUB bootstrap ir XHTML extraction vykdomi per `EbookLib` bei `BeautifulSoup`.
Jei TOC parseris negali patikimai nustatyti skyrių ribų, naudojamas `chapter map` YAML sidecar (`<source-stem>.chapters.yaml`).

Bendri repo skriptai šiai knygai kviečiami su:

- `MEDBOOK_ROOT=books/jrcalc-clinical-guidelines-2025-reference-edition`

## Vienas skyrius = vienas užbaigtas ciklas

Skyrius laikomas baigtu tik kai:

1. perskaitytas visas source skyriaus intervalas arba segmentų rinkinys;
2. sudarytas pilnas skyriaus inventorius;
3. patikrinti naujausi prieinami Lietuvos šaltiniai;
4. jei jų nepakanka, patikrintos naujausios Europos ar tarptautinės gairės;
4a. `shared/localization/lt_source_map.tsv` ir `source-priority.md` pagalba parinktas teisingas LT-source kelias pagal skyriaus temą;
4b. `research` faile užfiksuoti visi UK / Australia / US / kiti rinkos signalai ir jiems parinktas LT/EU pakeitimo sprendimas;
4c. jei reikia, sugeneruotas `research/<slug>.checklist.md` per `python3 scripts/generate_research_checklist.py --book-root books/<slug> <chapter>`;
4d. norminiai klinikiniai teiginiai užfiksuoti claim-level matricoje, o struktūriniai blokai turi aiškią LT lokalizacijos strategiją;
5. sugeneruotas `chapter_pack`;
6. lietuviškas skyrius parašytas nuo švaraus lapo pagal `chapter_pack`;
7. padarytas atskiras anti-calque perrašymas;
8. lentelės pilnai išverstos;
9. schemos, paveikslai ir `chart` tipo originalo grafikai atkurti lietuviškai arba aiškiai sutraukti į LT bloką;
10. jei skyriuje yra `high-risk` blokų, jiems sugeneruotas `adjudication_pack`;
11. viskas sutikrinta su kanoniniu originalu;
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
- pozityvius LT pavyzdžius iš `shared/prose/gold_phrases.tsv`, `shared/examples/gold_sections/` ir, jei tokių yra, local `gold_sections/`.

Be `chapter_pack` drafteris negali pradėti generavimo.

`build_chapter_pack.py` taip pat yra LT/EU-first vartai: jei source skyriuje aptinkami UK / Australia / US signalai, bet `research` faile jiems nėra aiškaus LT/EU sprendimo, pack generavimas turi baigtis klaida.
Jei skyriuje aptinkamas norminis klinikinis turinys, `chapter_pack` taip pat negali būti sugeneruotas be claim-level LT/EU atramos ir struktūrinių blokų politikos.

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

Book-local taisyklės leidžiamos tik per `*.local.tsv` override'us arba local `gold_sections/`. Pasikartojančios reusable taisyklės po review promuojamos į `shared/`, ne į konkrečios knygos root.

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
- `scripts/validate_manual_audit.py`;
- trumpą, bet privalomą agento rankinį kalbinį ir semantinį auditą, užfiksuotą `research` faile.

## Paveikslų taisyklė

Kiekvienam paveikslui ar algoritmui:

1. source kandidatas pirmiausia užfiksuojamas `source/index/figures.tsv`, jei originalas buvo EPUB;
2. parenkamas vienas kanoninis aktyvus šaltinis ir jis įrašomas į `lt/figures/manifest.tsv`;
3. vienintelė aktyvi redaguojama forma šiame projekte yra `Whimsical` lenta;
4. į repo saugomas galutinis `png`, skirtas `Obsidian` ir skyriaus `md` failams;
5. jei `Whimsical` kelias šioje sesijoje neveikia, darbas stabdomas ir aiškiai įvardijamas blokatorius.
