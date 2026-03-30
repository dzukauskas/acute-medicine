# 3 skyrius. Guideline Developers and Contributors

- Puslapiai: EPUB segmentas `c8W.xhtml`
- Šaltinio segmentai: `c8W.xhtml`
- Originalo failas: `source/epub/JRCALC Clinical Guidelines 2025 Reference Edition.epub`
- Angliškas pagalbinis failas: `source/chapters-en/003-guideline-developers-and-contributors.md`
- Lietuviškas failas: `lt/chapters/003-guideline-developers-and-contributors.md`

## Source inventorius

### Poskyriai

- Guideline Developers and Contributors
- Editorial Leads
- JRCALC Committee Members
- JRCALC Contributors
- Contributors Prior to 2016

### Lentelės

- Kol kas neužfiksuota

### Paveikslai / schemos / algoritmai

- Kol kas neužfiksuota

### Rėmeliai / papildomi blokai

- Kol kas neužfiksuota

## Rizikingi terminai

- JRCALC
- Joint Royal Colleges Ambulance Liaison Committee
- NASMeD
- AACE
- NHS
- Ambulance Pharmacists Network

## Lietuvos šaltiniai

| Šaltinis | Tipas | Data / versija | Kodėl naudotas |
| --- | --- | --- | --- |
| VLKK Terminų bankas | terminija | žiūrėta 2026-03-28 | LT antraštėms, bendriniams vaidmenų pavadinimams ir natūraliam padėkos / credits skyriaus wording'ui. |
| Greitosios medicinos pagalbos tarnybos vieša informacija | institucinis LT kontekstas | žiūrėta 2026-03-28 | Kad JK ambulance service ir committee pavadinimai nebūtų neteisingai perteikti kaip Lietuvos institucijų atitikmenys. |

## Europos / tarptautiniai šaltiniai

| Šaltinis | Tipas | Data / versija | Kodėl naudotas |
| --- | --- | --- | --- |
| JRCALC Clinical Guidelines 2025 Reference Edition | originalus šaltinis | 2025 leidimas | Naudotas kaip oficialus šio leidinio rengėjų, komitetų ir bendraautorių sąrašas. |

## LT-source branduolio taikymas

| Sritis | Pagrindinis LT-source kelias | Konkretus LT šaltinis | ES fallback | Pastaba |
| --- | --- | --- | --- | --- |
| terminija | terminija_ir_kalbos_forma | VLKK Terminų bankas | tarptautinė nomenklatūra | Reikalinga antraštėms, padėkos formuluotėms ir bendrinių pareigų pavadinimų vertimui. |
| institucinis_kontekstas | paramediko_kompetencija_ir_gmp | Greitosios medicinos pagalbos tarnybos vieša informacija | ERC; specialybinės ES gairės | Naudota tik tam, kad JK institucijos ir service model pavadinimai nebūtų pateikti kaip tariami LT atitikmenys. |

## Jurisdikcijos ir rinkos signalai

| Signalas | Jurisdikcija | Tipas | Šaltinio vieta | Pastaba |
| --- | --- | --- | --- | --- |
| JRCALC | uk | gairės | `c8W.xhtml` visame skyriuje | Tai originalo leidinio gairių ir komiteto ekosistemos pavadinimas. |
| Joint Royal Colleges Ambulance Liaison Committee | uk | service model | `c8W.xhtml` įvadinė pastraipa ir editorial leads blokas | Oficialus JK komiteto pavadinimas. |
| NASMeD | uk | service model | `c8W.xhtml` editorial leads ir committee members blokai | JK ambulance service medicinos direktorių grupės pavadinimas. |
| AACE | uk | service model | `c8W.xhtml` editorial leads blokas | JK organizacinio konteksto santrumpa. |
| NHS | uk | service model | `c8W.xhtml` editorial leads blokas | JK sveikatos sistemos institucinis kontekstas. |

## LT/EU pakeitimo sprendimai

| Signalas | Veiksmas | Autoritetas | LT / EU sprendimas | Šaltinio nuoroda | Pastaba |
| --- | --- | --- | --- | --- | --- |
| JRCALC | original_context_callout | original-context-only | Palikti tik kaip konkretaus originalo leidinio ir jo rengėjų tinklo pavadinimą. | `shared/localization/localization_overrides.tsv` (`JRCALC`); originalus skyrius `c8W.xhtml` | Nenaudoti kaip LT klinikinio ar institucinio autoriteto pavadinimo. |
| Joint Royal Colleges Ambulance Liaison Committee | original_context_callout | original-context-only | Palikti oficialų komiteto pavadinimą originalo kalba. | originalus skyrius `c8W.xhtml` | Tai konkretaus JK komiteto vardas, ne LT institucijos atitikmuo. |
| NASMeD | original_context_callout | original-context-only | Palikti tik kaip oficialią originalo organizacinio tinklo santrumpą. | originalus skyrius `c8W.xhtml` | LT tekste nekurti dirbtinio lietuviško atitikmens. |
| AACE | original_context_callout | original-context-only | Palikti tik kaip oficialią originalo organizacijos santrumpą. | originalus skyrius `c8W.xhtml` | LT tekste tai tik originalo partnerinė organizacija. |
| NHS | original_context_callout | original-context-only | Palikti tik darboviečių ir afiliacijų kontekste. | originalus skyrius `c8W.xhtml` | Negalima pateikti kaip LT sveikatos sistemos analogo. |

## Vaistų ir dozių LT/EU šaltinių bazė

| Tema | Šaltinis | Jurisdikcija | Data / versija | Pastaba |
| --- | --- | --- | --- | --- |

## Norminių teiginių matrica

| claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Struktūrinių blokų lokalizacijos sprendimai

| block_id | block_type | lt_strategy | authority_source | original_context_allowed | note |
| --- | --- | --- | --- | --- | --- |

## Neperkeliamas originalo turinys

- Oficialūs JK komitetų, tarnybų, tinklų ir kolegijų pavadinimai neturi būti verčiami taip, lyg jie būtų Lietuvos institucijų vardai.
- Contributor ir committee sąrašai yra šio konkretaus leidinio credits informacija, ne LT norminis ar organizacinis modelis.

## Adjudication sprendimai

## Lokalizacijos sprendimai

- Skyrius LT versijoje pateikiamas kaip padėkos ir prisidėjusių asmenų sąrašas, o ne kaip vietinis organizacinis modelis.
- Oficialūs komitetų, tarnybų, tinklų ir kolegijų pavadinimai paliekami originalo kalba.
- Verčiami tik bendriniai vaidmenų pavadinimai ir skyriaus antraštės.

## Vietos, kur originalas pakeistas pagal Lietuvos praktiką

- Originalo ceremoninė padėkos proza sutrumpinta ir perrašyta į aiškesnę LT credits formą.
- Vengta kurti tariamus lietuviškus JK institucijų ir organizacijų pavadinimų atitikmenis.

## Kalbinės rizikos vietos

- `have given freely and generously of their time and expertise` nepalikti pažodine, iškilminga angliška konstrukcija.
- Neperversti oficialių organizacijų pavadinimų į dirbtinius lietuviškus vardus.
- Contributor sąrašų neperkrauti nereikalingais lietuviškais paaiškinimais.

## Anti-calque perrašymo pastabos

- Įžangą rašyti kaip trumpą lietuvišką padėką ir credits paaiškinimą, ne kaip pažodinę ceremoninę anglų kalbos pastraipą.
- `Other contributors have come from a variety of multidisciplinary groups` perrašyti paprasčiau ir natūraliau.
- Pareigų pavadinimus versti saikingai, oficialius institucijų vardus paliekant originalo forma.

## Atviros abejonės

- Kol kas neužfiksuota.

## Finalus agento auditas

| Sritis | Statusas | Pastaba |
| --- | --- | --- |
| terminija | sutvarkyta | Pareigų pavadinimai ir heading'ai išversti, oficialūs organizacijų vardai palikti originalo forma. |
| kolokacijos | sutvarkyta | Credits įžanga perrašyta į natūralesnį LT padėkos stilių. |
| gramatika | ok |  |
| semantika | sutvarkyta | Skyrius aiškiai pateiktas kaip originalo leidinio credits informacija. |
| norminė logika | sutvarkyta | JK organizacijos neperteiktos kaip LT sistemos ar autoriteto atitikmenys. |
| atviros abejonės | ok |  |

## Chapter pack ir review kilpa

- `research` paruoštas `chapter_pack` generavimui.
- Jei pack pažymės pasikartojančias kalbines contributor sąrašų klaidas, jas fiksuoti per `term_candidates.tsv` ar `review_deltas/`, o ne tiesiai bendrose aktyviose bazėse.

## Baigiamoji kontrolė

- [x] Perskaitytas visas source skyriaus intervalas arba segmentų rinkinys
- [x] Užfiksuoti visi teksto blokai
- [x] Užfiksuotos visos lentelės
- [x] Užfiksuoti visi paveikslai ir schemos
- [x] Patikrinti Lietuvos šaltiniai ir jų datos
- [ ] Jei reikėjo, patikrintos Europos / tarptautinės gairės
- [x] Užpildyta `LT-source branduolio taikymas` lentelė pagal `shared/localization/lt_source_map.tsv`
- [x] Užfiksuoti visi UK / Australia / US / rinkos signalai
- [x] Kiekvienam signalui paliktas LT/EU pakeitimo sprendimas
- [x] Vaistų ir dozių LT/EU šaltinių bazė užpildyta
- [x] Užpildyta `Norminių teiginių matrica`, jei skyriuje yra norminis klinikinis turinys
- [x] Užpildyti struktūrinių blokų lokalizacijos sprendimai
- [ ] Sugeneruotas `chapter_pack`
- [ ] Jei reikia, sugeneruotas `adjudication_pack`
- [ ] Jei sugeneruotas `adjudication_pack`, palikta `## Adjudication sprendimai` sekcija fiksuotu `- block_id | pasirinkimas | priežastis` formatu
- [ ] Lietuviškas skyrius parašytas nuo švaraus lapo
- [ ] Padarytas atskiras anti-calque perrašymas
- [x] Lentelės išverstos
- [x] Paveikslai / schemos atkurti lietuviškai
- [ ] Numeracija atitinka knygą
- [x] Užpildytas `Finalus agento auditas`
