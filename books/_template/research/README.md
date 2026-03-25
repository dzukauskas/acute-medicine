# Research

Vienas failas šiame kataloge = vienas skyrius.

Kiekviename faile turi būti:

- skyriaus numeris ir pavadinimas;
- PDF puslapių intervalas;
- pilnas skyriaus inventorius;
- rizikingi terminai;
- naudoti Lietuvos šaltiniai su datomis;
- naudoti Europos / tarptautiniai šaltiniai su datomis, jei jų reikėjo;
- `## LT-source branduolio taikymas` lentelė;
- `## Jurisdikcijos ir rinkos signalai` lentelė;
- `## LT/EU pakeitimo sprendimai` lentelė;
- `## Vaistų ir dozių LT/EU šaltinių bazė` lentelė;
- `## Neperkeliamas originalo turinys` sekcija;
- jei buvo sugeneruotas `adjudication_pack`, `## Adjudication sprendimai` sekcija;
- lokalizacijos sprendimai;
- vietos, kur originalas pakeistas pagal Lietuvos praktiką;
- kalbinės rizikos vietos;
- jei reikia, `chart` tipo originalo grafikai;
- baigiamoji kontrolė.

`research` failas yra šaltinis `chapter_pack`, bet jo nepakeičia.

`## LT-source branduolio taikymas` lentelėje turi būti užrašyta:

- kuriam `lt_source_map.tsv` keliui priskirtas skyrius ar jo norminis turinys;
- koks konkretus LT šaltinis buvo pagrindinis;
- koks ES fallback buvo pasirinktas, jei LT sluoksnio nepakako;
- trumpa pastaba, kodėl pasirinktas būtent tas kelias.

Jei source skyriuje yra UK / Australia / US signalų ar rinkos-specifinių vaistų informacijos, `research` faile privalo būti aiškus LT/EU-first sprendimas, kitaip `build_chapter_pack.py` turi hard-fail'inti.

`## Adjudication sprendimai` sekcija turi būti machine-readable:

- `- <block_id> | <A|B|hibridinis> | <trumpa priežastis>`
