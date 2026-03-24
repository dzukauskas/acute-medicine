# Research

Vienas failas šiame kataloge = vienas skyrius.

Kiekviename faile turi būti:

- skyriaus numeris ir pavadinimas;
- PDF puslapių intervalas;
- pilnas skyriaus inventorius;
- rizikingi terminai;
- naudoti Lietuvos šaltiniai su datomis;
- naudoti Europos / tarptautiniai šaltiniai su datomis, jei jų reikėjo;
- lokalizacijos sprendimai;
- vietos, kur originalas pakeistas pagal Lietuvos praktiką;
- kalbinės rizikos vietos, iš kurių vėliau bus formuojami `chapter_pack` hotspot'ai;
- jei reikia, `chart` tipo originalo grafikai, kurie turi būti pažymėti kaip atskiras inventory vienetas;
- jei skyrius jau praėjo review, struktūrinė `review_delta` medžiaga ir promavimo pėdsakai;
- baigiamoji kontrolė.

`research` failas yra šaltinis `chapter_pack`, bet jo nepakeičia. Kai skyriaus preflight paruoštas, iš `research` turi būti sugeneruotas atskiras `chapter_packs/<slug>.yaml`.

Jei skyriuje yra high-risk blokų, po `chapter_pack` turi būti galima sugeneruoti ir `adjudication_packs/<slug>.yaml`.
