# Figures

Šiame kataloge laikomi lietuviški šios knygos paveikslai ir schemos.

Svarbu:

- `source/index/figures.tsv` yra source-side kandidatai iš originalo, ne aktyvūs paveikslai.
- `lt/figures/manifest.tsv` yra tik aktyvių `Whimsical` board'ų registras.

Privaloma taisyklė:

- redaguojamas šaltinis: `Whimsical` lenta
- naudojamas paveikslas: `*.png`
- atnaujinimas: oficialus `Whimsical` `.../svg` eksportas per `scripts/render_whimsical_figure.py`

Jei šioje sesijoje `Whimsical` kelias neveikia, reikia sustoti ir aiškiai įvardyti blokatorių. Negalima savavališkai pereiti į `Excalidraw`, savadarbį `SVG` workflow ar kitą pakaitalą.

Visi aktyvūs paveikslai ir jų kanoniniai šaltiniai turi būti surašyti:

- `manifest.tsv`

Jei source kandidatas ateina iš EPUB inventory, aktyvų įrašą kurkite per:

- `python3 scripts/register_whimsical_figure.py --book-root books/<slug> --source-figure-id <id> --figure-number <n> --whimsical-url <url>`
