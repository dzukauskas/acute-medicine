# Figure Workflow

Šiame kataloge laikomi knygos paveikslų perpiešti variantai.

## Tikslas

Tikslas nėra vien atkurti loginę eigą. Tikslas yra kuo arčiau atkartoti knygos figūros:

- bendrą kompoziciją;
- šakų išdėstymą;
- spalvų grupes;
- grįžtamąsias rodykles;
- apačios paaiškinimų blokus;
- antraštės hierarchiją.

## Kanoninis formatas

Naudok šią pirmenybės tvarką:

1. `*.drawio.svg` yra kanoninis, redaguojamas šaltinis.
2. `*.png` yra patogi peržiūra ir įkėlimas į `Markdown`.
3. `*.svg` gali būti laikomas kaip papildomas eksportas, jei reikia vektorinės peržiūros.
4. `*.d2` ar `Mermaid` tinka tik loginiam supaprastinimui arba tekstinei studijų versijai, bet ne kaip autorinis knygos paveikslo šaltinis.

## Pavadinimai

Naudok tokią vardų schemą:

- `001-figure-1-1-advanced-life-support.drawio.svg`
- `001-figure-1-1-advanced-life-support.png`
- jei reikia, `001-figure-1-1-advanced-life-support.svg`

Principas:

- pirmi trys skaitmenys: skyriaus numeris;
- po to originalus paveikslo numeris;
- pabaigoje trumpas anglų kalbos `slug`, kad failus būtų lengva rūšiuoti.

## Rekomenduojama eiga

1. Pirmiausia atsiversk originalų paveikslą ir suskaidyk jį į blokus, o ne į tekstą.
2. `draw.io` faile atkurk tik kompoziciją: dėžes, rodykles, šakų kryptis, poraštes, apatinius paaiškinimų stulpelius.
3. Tik tada perkelk lietuvišką tekstą į mazgus.
4. Kai išdėstymas stabilus, eksportuok `PNG`.
5. Jei skyriui reikia kompaktiškos versijos `Obsidian` skaitymui, pačiame `.md` faile papildomai palik `Mermaid` arba tekstinę schemą.

## Kokybės kriterijai

Paveikslas laikomas pakankamai geru tik jei:

- iš pirmo žvilgsnio atpažįstama ta pati kompozicija kaip knygoje;
- pagrindinė šaka, kairė šaka, dešinė šaka ir `ROSC` blokas yra tose pačiose santykinėse vietose;
- spalvos atskiria būsenų grupes, o ne yra atsitiktinės;
- apačios santraukos blokai nėra sugrūsti į vieną dėžę, jei originale jie yra atskiri;
- `Mermaid` versija, jei ji palikta, yra aiškiai pažymėta kaip supaprastinta mokymosi versija.
