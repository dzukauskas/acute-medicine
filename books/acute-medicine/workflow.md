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
5. lietuviškas skyrius parašytas nuo švaraus lapo;
6. padarytas atskiras anti-calque perrašymas, kai tekstas peržiūrimas jau nebe pagal anglų sakinį, o kaip lietuviška proza;
7. lentelės pilnai išverstos;
8. schemos ir paveikslai atkurti lietuviškai;
9. viskas sutikrinta su PDF;
10. paleistas terminų ir prozos QA.

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
- `scripts/prose_guard.py`;
- trumpą rankinį kalbinį auditą.

## Vienetų taisyklė

Pagrindinė forma visada yra Lietuvos / ES / SI vienetai:

- `kg`, `g`, `cm`, `m`, `mL`, `mmHg`, `kPa`, `mmol/L`, `g/L`, `°C`;
- JK / US / imperial vienetai gali likti tik kaip antrinė forma skliaustuose, jei tai padeda orientuotis.

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
- [$excalidraw-diagram](/Users/dzukauskas/.codex/skills/excalidraw-diagram-skill/SKILL.md) kai reikia failinio šaltinio ar `Whimsical` nėra tinkamas;
- interneto paiešką naujausių šaltinių patikrai;
- `scripts/terminology_guard.py` terminų ir draudžiamų frazių kontrolei;
- `scripts/prose_guard.py` sakinio lygio kalkių ir vertimo karkaso kontrolei;
- atitinkamus skills, kai užduotis sutampa su jų paskirtimi.
