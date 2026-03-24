# Acute Medicine Workflow

## Tikslas

Galutinis rezultatas yra lietuviškas medicininis konspektas, pritaikytas Lietuvos medicinos ir, kai taikoma, Lietuvos GMP logikai.

Tai nėra pažodinis JK šaltinio vertimas.

## Kanoninis šaltinis

Kanoninis šaltinis visada yra:

- `books/acute-medicine/source/pdf/Acute Medicine A Practical Guide to the Management of Medical Emergencies (Mridula Rajwani (Editor) etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf`

`source/chapters-en/` failai yra tik pagalbinė navigacija. Jie niekada nepakeičia pilno PDF perskaitymo.

## Vienas skyrius = vienas užbaigtas ciklas

Skyrius laikomas baigtu tik kai:

1. perskaitytas visas PDF puslapių intervalas;
2. sudarytas pilnas skyriaus inventorius;
3. patikrinti naujausi prieinami Lietuvos šaltiniai;
4. jei jų nepakanka, patikrintos naujausios Europos ar tarptautinės gairės;
5. sugeneruotas `chapter_pack`;
6. lietuviškas skyrius parašytas nuo švaraus lapo pagal `chapter_pack`;
7. padarytas atskiras anti-calque perrašymas, kai tekstas peržiūrimas jau nebe pagal anglų sakinį, o kaip lietuviška proza;
8. lentelės pilnai išverstos;
9. schemos ir paveikslai atkurti lietuviškai;
10. viskas sutikrinta su PDF;
11. paleistas terminų, prozos, tipografijos ir komplektiškumo QA;
12. jei skyrius buvo taisytas ranka, užfiksuotas `review_delta` ir parengti rule-promotion kandidatai.

## `Chapter pack` taisyklė

Prieš bet kokį drafting skyriui privaloma sugeneruoti `chapter_packs/<slug>.yaml`.

`chapter_pack` yra vykdomas preflight artefaktas, o ne papildoma dokumentacija. Jis turi apjungti:

- skyriaus blokų inventorių;
- aktyvius terminus ir akronimus;
- lokalizacijos override'us;
- stiliaus hotspot'us;
- pozityvius LT pavyzdžius.

Be `chapter_pack` drafteris negali pradėti generavimo.

## Section-type drafting

Skyriaus blokai generuojami ne vienu universaliu režimu, o pagal `draft_mode` iš `chapter_pack`:

- `narrative-prose`
- `table-compression`
- `algorithm-stepwise`
- `local-context-callout`

Tai leidžia neapdoroti lentelių, algoritmų ir lokalizacinių paaiškinimų tuo pačiu prose režimu.

## Lokalizacijos taisyklė

Kai originalo logika nesutampa su Lietuvos praktika:

- pagrindiniame tekste taikoma Lietuvos logika;
- neatitikimas pažymimas `research` faile;
- jei reikia, skyriuje paliekamas trumpas callout paaiškinimas.

## Dvigubas QA

Kiekvienas skyrius turi praeiti du atskirus kokybės vartus:

1. `Clinical QA`
   Tai tikrina, ar turinys atitinka originalų PDF, Lietuvos šaltinius ir, jei reikia, naujausias Europos gaires.
2. `Language QA`
   Tai tikrina, ar sakinys skamba kaip lietuviškai parašytas medicininis tekstas, o ne kaip vertimas iš anglų kalbos.

`Language QA` privalomai apima:

- atskirą anti-calque perrašymą;
- sutikrinimą su `language-style.md`;
- `scripts/prose_guard.py`;
- `scripts/lt_style_guard.py`;
- `scripts/terminology_guard.py` su `chapter_pack`, jei jis yra;
- `scripts/completeness_guard.py`;
- trumpą rankinį kalbinį auditą.

## LT medicininės kalbos modulis

Branduolinės LT kalbos taisyklės laikomos `language-style.md`.

Pozityvūs LT formuluočių pavyzdžiai laikomi `gold_phrases.tsv`.

Privalomi principai:

- kolokacijų pirmumas;
- nominalizacijų mažinimas;
- valentingumo ir linksnių tikrinimas;
- genityvų grandinių skaidymas;
- temos–remos tvarka;
- aktyvesnė, mažiau biurokratinė sintaksė;
- per ilgų sakinių skaidymas.

## Vienetų taisyklė

Pagrindinė forma visada yra Lietuvos / ES / SI vienetai:

- `kg`, `g`, `cm`, `m`, `mL`, `mmHg`, `kPa`, `mmol/L`, `g/L`, `°C`;
- tarp skaičiaus ir vieneto rašomas nepertraukiamas tarpas;
- intervalams naudojamas `–`, ne `-`;
- neigiamoms reikšmėms naudojamas `−`;
- formulėse ir matmenyse naudojamas `×`;
- JK / US / imperial vienetai gali likti tik kaip antrinė forma skliaustuose, jei tai padeda orientuotis.

## Anglų terminų ir studentinių paaiškinimų politika

Projekte anglų terminai rodomi ribotai:

- tik tada, kai jie realiai padeda orientuotis;
- dažniausiai pirmą kartą prie sudėtingesnio termino;
- ne antraštėse;
- ne beveik prie kiekvieno termino.

Terminų blokai ar trumpi paaiškinimai pridedami tik tada, kai tema yra tanki, nauja ar kitaip sunkiai suprantama be trumpo paaiškinimo.

Jei skyriuje pataisoma pasikartojanti LT formuluotė, pirmas klausimas po review yra:

- ar tai tik vietinė pataisa;
- ar verta ją promuoti į `gold_phrases.tsv`, `calque_patterns.tsv`, `termbase.tsv`, `acronyms.tsv` ar `localization_overrides.tsv`.

## Akronimų politika

Dažniausi projekto trumpiniai fiksuojami `acronyms.tsv`.

Taisyklės:

- svarbūs ar potencialiai dviprasmiai trumpiniai pirmą kartą turi būti išskleisti;
- po pirmos pilnos formos galima vartoti nusistovėjusį trumpinį;
- jei trumpinys gali reikšti kelis dalykus, sprendžiama pagal klinikinį kontekstą.

## Struktūrinė review kilpa

Jei skyrius po drafto buvo taisytas ranka, turi būti paliekamas `review_deltas/<slug>.tsv`.

`review_delta` paskirtis:

- atskirti vienkartines pataisas nuo sisteminių defektų;
- suteikti medžiagą `promote_rules.py`;
- pildyti `regression_examples/`;
- mažinti ateities rankinio taisymo kiekį.

Pirmoje iteracijoje rule promotion visada yra žmogaus patvirtinama. Skriptai gali tik parengti kandidatus.

## Paveikslų taisyklė

Kiekvienam paveikslui ar algoritmui:

1. parenkamas vienas kanoninis šaltinis ir jis įrašomas į `lt/figures/manifest.tsv`;
2. numatytoji redaguojama forma yra `Whimsical` lenta;
3. `manifest.tsv` turi saugoti redaguojamo šaltinio tipą ir jo nuorodą ar failo kelią;
4. jei reikia failinio atsarginio varianto arba `Whimsical` netinka konkrečiam atvejui, leidžiamas `Excalidraw`;
5. vienam paveikslui gali būti tik vienas aktyvus redaguojamas kanoninis šaltinis;
6. į repo saugomas galutinis `png`, skirtas `Obsidian` ir skyriaus `md` failams;
7. po bet kokio redagavimo `Whimsical` ar `Excalidraw` šaltinyje `png` turi būti atnaujintas;
8. po paveikslu paliekama trumpa lietuviška santrauka.

Projektuojant tekstinius blokus `Whimsical` lentoje galioja atsargos taisyklė:

- ilgesnės lietuviškos antraštės negali būti paliekamos „ant ribos“;
- jei antraštė ar bullet eilutė `Whimsical` lentoje vos telpa, bloką reikia platinti dar prieš eksportą;
- ilgesniems 2×2 informaciniams blokams paliekama aiški dešinė ir kairė vidinė paraštė, ne minimalus tarpas iki krašto.

Kai kanoninis šaltinis yra `Whimsical` lenta, numatytasis eksporto kelias yra:

1. autentifikuotas `.../svg` eksportas;
2. `svg -> png` rasterizavimas per `Chromium`, kad teksto plotis ir šriftai liktų kuo arčiau `Whimsical`;
3. jei reikia, `Inkscape` naudojamas tik kaip atsarginis fallback;
4. tik jei šie keliai neveikia, leidžiamas browser screenshot fallback.

Po kiekvieno `Whimsical` eksporto privalomas vizualus `Export QA`:

1. ar kuris nors tekstas nesiremia į bloko kraštą;
2. ar po ilgos antraštės dar aiškiai matosi foninė paraštė iš abiejų pusių;
3. ar nė viena eilutė nėra nukirsta, suspausta ar optiškai „prilipusi“ prie krašto;
4. ar eksportuotas `png` vizualiai sutampa su `Whimsical` lenta, ypač 2×2 apatinių blokų srityje.

Jei `Export QA` randa problemą, pirmiausia taisoma pati `Whimsical` lenta:

- platinamas blokas;
- trumpinama antraštė;
- pergrupuojamas tekstas;
- tik po to renderinama iš naujo.

Paveikslai turi būti kuo arčiau knygos 1:1, išskyrus vietas, kur reikia koreguoti pagal naujesnę Lietuvos medicinos informaciją.

## Skyriaus failai

1 skyriui numatyti failai:

- `source/chapters-en/001-cardiorespiratory-arrest-in-hospital.md`
- `lt/chapters/001-cardiorespiratory-arrest-in-hospital.md`
- `research/001-cardiorespiratory-arrest-in-hospital.md`
- `lt/figures/001-figure-1-1-advanced-life-support.png`
- `lt/figures/manifest.tsv`
- `Whimsical` lenta `ALS 1.1 test`

## Įrankiai

Kai tai duoda realią naudą, naudok:

- `pdf_reader` PDF puslapių, lentelių ir vaizdų tikrinimui;
- `whimsical-desktop` MCP schemų, algoritmų ir išdėstymo kūrimui;
- [Whimsical official export docs](https://help.whimsical.com/imports-exports/exporting-from-whimsical) kai reikia patikslinti oficialų `svg/png/pdf` eksporto kelią;
- [$excalidraw-diagram](/Users/dzukauskas/.codex/skills/excalidraw-diagram-skill/SKILL.md) kai reikia failinio šaltinio ar `Whimsical` nėra tinkamas;
- interneto paiešką naujausių šaltinių patikrai;
- `scripts/terminology_guard.py` terminų ir draudžiamų frazių kontrolei;
- `scripts/prose_guard.py` sakinio lygio kalkių ir vertimo karkaso kontrolei;
- `scripts/lt_style_guard.py` LT tipografijai, intervalams, nepertraukiamiems tarpams ir anglų terminų rodymo higienai;
- atitinkamus skills, kai užduotis sutampa su jų paskirtimi.
