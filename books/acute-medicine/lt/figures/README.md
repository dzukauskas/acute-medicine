# Figures

Šiame kataloge laikomi lietuviški šios knygos paveikslai ir schemos.

Kiekvienam paveikslui turi būti tik vienas kanoninis šaltinis.

Numatytoji taisyklė:

- redaguojamas šaltinis: `Whimsical` lenta
- naudojamas paveikslas: `*.png`
- atnaujinimas: oficialus `Whimsical` `.../svg` eksportas per `scripts/render_whimsical_figure.py`, kuris SVG rasterizuoja per `Chromium`, ne per rankinį screenshotą

Išimtis:

- jei `Whimsical` šiam atvejui netinka arba reikia failinio redaguojamo šaltinio, naudojamas `*.excalidraw`;
- vienam paveikslui negali likti du aktyvūs redaguojami šaltiniai.

Visi aktyvūs paveikslai ir jų kanoniniai šaltiniai turi būti surašyti:

- `manifest.tsv`

Dabartinė aktyvi 1.1 paveikslo būsena:

- `001-figure-1-1-advanced-life-support.png`
- kanoninis šaltinis: `Whimsical` lenta `ALS 1.1 test`

Po kiekvieno redagavimo `Whimsical` ar `Excalidraw` šaltinyje `png` turi būti atnaujinamas.

Jei `Whimsical` PNG eksportas atrodo neryškus, prioritetas teikiamas jų oficialiai rekomenduojamam `.../svg` keliui, o tada `svg` konvertuojamas į `png`.

Prieš laikant paveikslą baigtu, reikia greito vizualaus QA:

- ar tekstas nesiremia į spalvoto bloko kraštą;
- ar po ilgesnės antraštės dar lieka aiški vidinė paraštė;
- ar eksportas vizualiai sutampa su pačia `Whimsical` lenta.

Jei randamas toks neatitikimas, pirmiausia plečiamas ar pergrupuojamas pats blokas `Whimsical` lentoje, o ne bandoma „gelbėti“ vien renderiu.

Ankstesnio workflow figūrų failai pašalinti ir nebėra aktyvus šaltinis.
