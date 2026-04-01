# Research

Vienas failas šiame kataloge = vienas skyrius.

Kiekviename faile turi būti:

- skyriaus numeris ir pavadinimas;
- PDF puslapių intervalas arba source segmentų sąrašas;
- pilnas skyriaus inventorius;
- rizikingi terminai;
- naudoti Lietuvos šaltiniai su datomis;
- naudoti Europos / tarptautiniai šaltiniai su datomis, jei jų reikėjo;
- `## LT-source branduolio taikymas` lentelė;
- `## Jurisdikcijos ir rinkos signalai` lentelė;
- `## LT/EU pakeitimo sprendimai` lentelė;
- `## Vaistų ir dozių LT/EU šaltinių bazė` lentelė;
- `## Norminių teiginių matrica`, jei skyriuje yra norminis klinikinis turinys;
- `## Struktūrinių blokų lokalizacijos sprendimai` lentelė;
- `## Neperkeliamas originalo turinys` sekcija;
- jei buvo sugeneruotas `adjudication_pack`, `## Adjudication sprendimai` sekcija;
- lokalizacijos sprendimai;
- vietos, kur originalas pakeistas pagal Lietuvos praktiką;
- kalbinės rizikos vietos;
- `## Finalus agento auditas` lentelė;
- jei reikia, `chart` tipo originalo grafikai;
- baigiamoji kontrolė.

`research` failas yra šaltinis `chapter_pack`, bet jo nepakeičia.
Jei po `compact` ar naujo thread reikia atstatyti automatinio QA būseną, ją perleisk per `scripts/run_chapter_qa.py`; čia nefiksuok atskiro machine-readable pass receipt.

`## LT-source branduolio taikymas` lentelėje turi būti užrašyta:

- kuriam `shared/localization/lt_source_map.tsv` keliui priskirtas skyrius ar jo norminis turinys;
- koks konkretus LT šaltinis buvo pagrindinis;
- koks ES fallback buvo pasirinktas, jei LT sluoksnio nepakako;
- trumpa pastaba, kodėl pasirinktas būtent tas kelias.

Jei source skyriuje yra UK / Australia / US signalų ar rinkos-specifinių vaistų informacijos, `research` faile privalo būti aiškus LT/EU-first sprendimas, kitaip `build_chapter_pack.py` turi hard-fail'inti.

Jei source skyriuje yra norminių teiginių apie dozes, indikacijas, kontraindikacijas, vartojimo kelius, algoritmus ar profesines ribas, jie turi būti užrašyti claim-level matricoje. Pagrindiniame LT tekste norminiai teiginiai leidžiami tik su LT šaltiniu; ES leidžiamas tik kaip aiškiai pažymėtas fallback.

`## Adjudication sprendimai` sekcija turi būti machine-readable:

- `- <block_id> | <A|B|hibridinis> | <trumpa priežastis>`

`## Finalus agento auditas` yra privalomas paskutinis QA pėdsakas. Jis neužkrauna ilgo žmogaus review, bet verčia agentą aiškiai užfiksuoti, kad terminija, kolokacijos, gramatika, semantika ir norminė logika buvo ranka peržiūrėtos po automatinių guardų.
