# Figures

Šiame kataloge laikomi lietuviški šios knygos paveikslai ir schemos.

Kiekvienam paveikslui turi būti tik vienas kanoninis šaltinis.

Privaloma taisyklė:

- redaguojamas šaltinis: `Whimsical` lenta
- naudojamas paveikslas: `*.png`
- atnaujinimas: oficialus `Whimsical` `.../svg` eksportas per `scripts/render_whimsical_figure.py`, kuris SVG rasterizuoja per `Chromium`, ne per rankinį screenshotą

Jei šioje sesijoje `Whimsical` kelias neveikia, reikia sustoti ir aiškiai įvardyti blokatorių. Negalima savavališkai pereiti į `Excalidraw`, savadarbį `SVG` workflow ar kitą pakaitalą.

- vienam paveikslui negali likti du aktyvūs redaguojami šaltiniai;
- `*.svg` gali būti tik laikinas techninis artefaktas ar archyvas, bet ne aktyvus kanoninis šaltinis.

Visi aktyvūs paveikslai ir jų kanoniniai šaltiniai turi būti surašyti:

- `manifest.tsv`

`manifest.tsv` aktyviam workflow leidžiamas tik vienas `canonical_source_type`:

- `whimsical_board`

`svg_file`, `excalidraw_file` ar bet kuris kitas pakaitinis tipas kaip aktyvus kanoninis šaltinis nebeleidžiamas ir turi būti stabdomas per `scripts/validate_figures_manifest.py`.

Po kiekvieno redagavimo `Whimsical` lentoje `png` turi būti atnaujinamas.

Jei `Whimsical` PNG eksportas atrodo neryškus, prioritetas teikiamas jų oficialiai rekomenduojamam `.../svg` keliui, o tada `svg` konvertuojamas į `png`.

Prieš laikant paveikslą baigtu, reikia greito vizualaus QA:

- ar tekstas nesiremia į spalvoto bloko kraštą;
- ar po ilgesnės antraštės dar lieka aiški vidinė paraštė;
- ar eksportas vizualiai sutampa su pačia `Whimsical` lenta.

Jei randamas toks neatitikimas, pirmiausia plečiamas ar pergrupuojamas pats blokas `Whimsical` lentoje, o ne bandoma „gelbėti“ vien renderiu.

Ankstesnio workflow figūrų failai gali likti tik archyve; aktyviame `lt/figures/` medyje jie negali būti laikomi kanoniniu šaltiniu.
