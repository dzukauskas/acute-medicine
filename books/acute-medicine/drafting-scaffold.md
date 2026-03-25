# Drafting Scaffold

Šis failas apibrėžia minimalią drafting discipliną, kai aktyvus `chapter_pack`.

## Privaloma seka

1. Perskaitykite PDF.
2. Užpildykite `research` failą.
3. Ginčytinus LT terminus, kolokacijas ir klinikinių kategorijų pavadinimus pirmiausia patikrinkite Lietuvos medicininėje literatūroje internete ir užrašykite šaltinį bei datą.
4. Jei vartotojas nurodo konkretų įrankį ar workflow, jo nekeiskite savo nuožiūra; jei jis neveikia, sustokite ir įvardykite blokatorių.
5. Sugeneruokite `chapter_pack`.
6. Tik tada generuokite LT skyrių.

Be `chapter_pack` drafting nelaikomas galiojančiu.

Jei `chapter_pack` turi `adjudication_candidate: true`, prieš galutinį polishą sugeneruokite ir `adjudication_pack`.

## Režimai

### `narrative-prose`

Naudoti:

- įžangoms;
- klinikinių principų paaiškinimams;
- hemodinamikos ir diagnostikos pastraipoms.

Tikslas:

- natūrali LT medicininė proza;
- trumpesni sakiniai;
- mažiau nominalizacijų;
- aiškios kolokacijos.

### `table-compression`

Naudoti:

- lentelėms;
- glaustiems diferencinės diagnostikos ar veiksmų pasirinkimo blokams.

Tikslas:

- aiški LT markdown lentelė ar punktinis blokas;
- jokio bereikalingo prozinimo;
- išlaikyta klinikinė struktūra.

### `algorithm-stepwise`

Naudoti:

- algoritmams;
- veiksmų sekoms;
- struktūruotiems „jei–tada“ sprendimams.

Tikslas:

- aktyvūs veiksmažodžiai;
- viena aiški komanda viename žingsnyje;
- minimalus EN karkasas.

### `local-context-callout`

Naudoti:

- UK→LT adaptacijoms;
- teisinių ar sistemos skirtumų paaiškinimams;
- studentiniams trumpiems aiškinimams, kai jie tikrai reikalingi.

Tikslas:

- trumpas, aiškus paaiškinimas;
- jokio perkrauto dvikalbio teksto;
- aiškiai atskirta, kas yra originalo kontekstas, o kas LT praktika.

## Papildomos taisyklės

- `chart` tipo blokai turi būti inventorizuojami atskirai, net jei LT variante jie sutraukiami į vieną aiškų paaiškinimą.
- Jei yra `before/after` pora, `review_delta` pirmiausia generuokite per `scripts/mine_review_deltas.py`, o ne pildykite nuo tuščio failo.
