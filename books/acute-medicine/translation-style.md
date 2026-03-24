# Vertimo Stilius

## Pagrindas

Rašyk natūralia lietuviška medicinine kalba.

Versk sąvoką, o ne angliško sakinio formą.

Prieš drafting turi būti sugeneruotas `chapter_pack`, o po review pasikartojančios pataisos turi būti promuojamos į taisyklių sluoksnį.

## Anti-Calque taisyklė

Po pirmo vertimo skyrius turi būti perrašomas dar kartą, jau nebežiūrint į angliško sakinio formą.

Tikrinimo klausimas:

- ar taip parašytų lietuviškai medicinos dėstytojas, gydytojas ar metodikos autorius?

Jei sakinys skamba kaip vertimas, jį reikia perrašyti net tada, kai terminai yra teisingi.

Dažniausi rizikos ženklai:

- `sprendimas dėl ... turi būti ...`;
- `prioritetas yra ...`;
- `yra viena svarbiausių ...`;
- `gali būti naudojama / gali būti naudinga`;
- `orientuojantis į ...`;
- `eskaluoti pagalbą`;
- per ilgi sakiniai su keliomis loginėmis išlygomis.

Tokie sakiniai turi būti keičiami į aktyvesnę, trumpesnę ir natūralesnę lietuvišką formą.

## Lokalizacija

- pirmenybė teikiama Lietuvos medicinos vartosenai;
- Lietuvos GMP orientuotuose konspektuose prioritetas teikiamas vietinei praktikai;
- JK vidaus sistemos negali likti pateiktos kaip universalus standartas.

## Vienetai

- naudok Lietuvos / ES / SI vienetus kaip pagrindinę formą;
- dešimtainiams skaičiams naudok kablelį;
- imperial vienetus konvertuok.

## Lentelės ir schemos

- lentelės verčiamos pilnai į `Markdown`, jei jos išlieka įskaitomos;
- schemos ir algoritmai atkuriami lietuviškai;
- figūros numeracija turi sutapti su knyga.
- algoritmai, lentelės ir lokalizaciniai paaiškinimai neturi būti draftinami tuo pačiu prose režimu; naudok `chapter_pack` nurodytą `draft_mode`.

## Callout

Kai reikia, naudok trumpus `Obsidian` callout:

- `> [!NOTE]`
- `> [!TIP]`
- `> [!WARNING]`
- `> [!IMPORTANT]`

## Baigimo sąlyga

Skyrius nelaikomas baigtu, kol:

1. pilnai sutikrintas su PDF;
2. užpildytas `research` failas;
3. schemos ir lentelės užbaigtos;
4. padarytas atskiras anti-calque perrašymas;
5. `scripts/terminology_guard.py` grąžina švarų rezultatą;
6. `scripts/prose_guard.py` grąžina švarų rezultatą;
7. `scripts/lt_style_guard.py` grąžina švarų rezultatą;
8. `scripts/completeness_guard.py` neberanda prapuolusių struktūrinių blokų;
9. jei buvo rankinių pataisų, užpildytas `review_deltas/<slug>.tsv`.
