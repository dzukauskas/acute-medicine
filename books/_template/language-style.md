# Lithuanian Language Style

Šis failas apibrėžia projekto LT medicininės kalbos branduolį.

Tikslas: rašyti aiškų, idiomatiškai skambantį, studentiškai suprantamą ir Lietuvos medicinos vartosenai artimą tekstą, o ne pažodinį EN->LT vertimą.

## LT medicininės prozos branduolys

Pagrindiniai principai:

- kolokacijų pirmumas;
- nominalizacijų mažinimas;
- valentingumo ir linksnių tikrinimas;
- aktyvesnė sintaksė;
- genityvų grandinių skaidymas;
- temos-remos tvarka;
- sakinio ritmo kontrolė;
- aprašomasis tikslinimas.

Praktiškai tai reiškia:

- geriau `įvertinkite`, ne `atlikite įvertinimą`;
- geriau `stebėkite`, ne `vykdykite stebėjimą`;
- geriau `koreguokite`, ne `atlikite korekciją`;
- geriau `nuspręskite` ar `aptarkite`, ne `sprendimas turi būti priimamas`.

Jei kyla abejonių dėl termino, kolokacijos ar klinikinės kategorijos pavadinimo, jo negalima rinktis vien iš intuicijos. Pirma patikrinkite Lietuvos medicininę vartoseną internete, o tik tada fiksuokite formuluotę tekste ar `termbase`.

## LT/EU-first lokalizacija

- pagrindinis LT tekstas turi skambėti kaip Lietuvos / ES medicinos mokymosi tekstas, ne kaip UK, Australia ar US sistemos aprašas;
- UK / Australia / US terminai, institucijos, gairės ir reference įrankiai negali būti paliekami pagrindiniame tekste kaip norminis standartas;
- jei originalo kontekstą verta parodyti, jis rodomas tik `Originalo kontekstas` bloke;
- prekiniai pavadinimai yra išimtis, ne default'as; pagrindinėje prozoje ir lentelėse teikiamas bendrinis / INN pavadinimas;
- dozės, vartojimo keliai, indikacijos ir kontraindikacijos negali būti paliekami vien todėl, kad taip parašyta originalo rinkos knygoje.

## Tipografija ir techninė rašyba

- dešimtainis skirtukas yra kablelis: `3,5`, ne `3.5`;
- tarp skaičiaus ir vieneto rašomas nepertraukiamas tarpas;
- intervalams naudojamas `-` pakeičiamas į `–`;
- formulėse ir matmenyse naudojamas `×`;
- pagrindinė forma visada yra SI / ES vienetai.

## Anglų terminų rodymo politika

Anglų terminas rodomas ribotai:

- tik tada, kai jis realiai padeda orientuotis;
- dažniausiai pirmą kartą, prie sudėtingesnio termino;
- ne antraštėse;
- ne beveik prie kiekvieno termino.

## QA padalijimas

Automatizuoti tik tai, kas patikimai aptinkama:

- dažnos kalkės ir vertimo karkasai;
- tipografijos klaidos;
- perteklinis anglų terminų rodymas akivaizdžiais atvejais.

Rankiniam auditui palikti:

- kolokacijų natūralumą;
- genityvų grandinių aiškumą;
- semantiškai subtilias formuluotes.
