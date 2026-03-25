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

## Lokalizacija

- pirmenybė teikiama Lietuvos medicinos vartosenai;
- vietinės klinikinės praktikos skyriuose prioritetas teikiamas Lietuvos ar ES logikai;
- UK / Australia / US vidaus sistemos negali likti pateiktos kaip universalus standartas;
- prieš norminį perrašymą reikia pasirinkti teisingą LT-source kelią iš `lt_source_map.tsv`.

## Vienetai

- naudok Lietuvos / ES / SI vienetus kaip pagrindinę formą;
- dešimtainiams skaičiams naudok kablelį;
- imperial vienetus konvertuok.

## Lentelės ir schemos

- lentelės verčiamos pilnai į `Markdown`, jei jos išlieka įskaitomos;
- schemos ir algoritmai atkuriami lietuviškai;
- figūros numeracija turi sutapti su knyga.

## Baigimo sąlyga

Skyrius nelaikomas baigtu, kol:

1. pilnai sutikrintas su PDF;
2. užpildytas `research` failas;
3. schemos ir lentelės užbaigtos;
4. padarytas atskiras anti-calque perrašymas;
5. paleisti atitinkami QA vartai;
6. jei buvo rankinių pataisų, užpildytas `review_deltas/<slug>.tsv`.
