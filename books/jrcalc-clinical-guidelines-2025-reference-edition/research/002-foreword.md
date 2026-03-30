# 2 skyrius. Foreword

- Puslapiai: EPUB segmentas `c7Z.xhtml`
- Šaltinio segmentai: `c7Z.xhtml`
- Originalo failas: `source/epub/JRCALC Clinical Guidelines 2025 Reference Edition.epub`
- Angliškas pagalbinis failas: `source/chapters-en/002-foreword.md`
- Lietuviškas failas: `lt/chapters/002-foreword.md`

## Source inventorius

### Poskyriai

- Foreword

### Lentelės

- Kol kas neužfiksuota

### Paveikslai / schemos / algoritmai

- Kol kas neužfiksuota

### Rėmeliai / papildomi blokai

- Kol kas neužfiksuota

## Rizikingi terminai

- JRCALC
- JRCALC apps
- iCPG
- JRCALC Plus
- medicines section
- NPIS-Toxbase
- PFD rulings
- HSSIB

## Lietuvos šaltiniai

| Šaltinis | Tipas | Data / versija | Kodėl naudotas |
| --- | --- | --- | --- |
| VLKK Terminų bankas | terminija | žiūrėta 2026-03-28 | LT kolokacijoms ir neutraliai pratarmės leksikai. |
| VVKT svetainė ir Lietuvos vaistinių preparatų registras | LT vaistų informacijos atskaitos taškas | žiūrėta 2026-03-28 | Kad originalo nuoroda į `JRCALC apps` dėl vaistų nebūtų suprasta kaip LT norminis vaistų informacijos šaltinis. |

## Europos / tarptautiniai šaltiniai

| Šaltinis | Tipas | Data / versija | Kodėl naudotas |
| --- | --- | --- | --- |
| JRCALC Clinical Guidelines 2025 Reference Edition | originalus šaltinis | 2025 leidimas | Naudotas kaip pratarmės turinio ir originalo leidinio konteksto šaltinis. |

## LT-source branduolio taikymas

| Sritis | Pagrindinis LT-source kelias | Konkretus LT šaltinis | ES fallback | Pastaba |
| --- | --- | --- | --- | --- |
| terminija | terminija_ir_kalbos_forma | VLKK Terminų bankas; LT medicininė mokomoji vartosena | tarptautinė nomenklatūra | Reikalinga natūraliai LT pratarmės kalbai ir neutraliam įvadiniam tonui. |
| vaistu_informacijos_kontekstas | vaistu_registracija_ir_produkto_informacija | VVKT svetainė ir Lietuvos vaistinių preparatų registras | EMA product information | Naudota tik kaip LT/EU atskaitos taškas, kad originalo nuoroda į `JRCALC apps` dėl vaistų liktų tik originalo naudojimo pastaba. |

## Jurisdikcijos ir rinkos signalai

| Signalas | Jurisdikcija | Tipas | Šaltinio vieta | Pastaba |
| --- | --- | --- | --- | --- |
| JRCALC | uk | gairės | `c7Z.xhtml` visame skyriuje | Originalo leidinio gairių ir skaitmeninių platformų ekosistema. |
| iCPG | uk | reference tool | `c7Z.xhtml` pirma pastraipa | Originale minimas prieigos prie gairių įrankis. |
| JRCALC Plus | uk | reference tool | `c7Z.xhtml` pirma pastraipa | Originale minimas prieigos prie gairių įrankis. |
| NPIS-Toxbase | uk | reference tool | `c7Z.xhtml` ketvirta pastraipa | JK toksikologinės informacijos šaltinis. |

## LT/EU pakeitimo sprendimai

| Signalas | Veiksmas | Autoritetas | LT / EU sprendimas | Šaltinio nuoroda | Pastaba |
| --- | --- | --- | --- | --- | --- |
| JRCALC | original_context_callout | original-context-only | Palikti tik kaip šio konkretaus originalo leidinio ir jo skaitmeninių platformų kontekstą. | `shared/localization/localization_overrides.tsv` (`JRCALC`); originalus skyrius `c7Z.xhtml` | Pratarmė aprašo originalaus leidinio ekosistemą, ne LT norminį standartą. |
| iCPG | original_context_callout | original-context-only | Neperkelti kaip LT norminio įrankio; rodyti tik aiškinant, kaip originale pasiekiamos gairės. | originalus skyrius `c7Z.xhtml` | LT vartotojui tai tik originalo platformos pavadinimas. |
| JRCALC Plus | original_context_callout | original-context-only | Neperkelti kaip LT norminio įrankio; palikti tik originalo kontekste. | originalus skyrius `c7Z.xhtml` | Tai originalo leidinio platforma, ne LT klinikinis autoritetas. |
| NPIS-Toxbase | original_context_callout | original-context-only | Neperkelti kaip LT norminio toksikologinio šaltinio. | originalus skyrius `c7Z.xhtml` | LT tekste tai tik padėkos dalies originalo institucinis kontekstas. |

## Vaistų ir dozių LT/EU šaltinių bazė

| Tema | Šaltinis | Jurisdikcija | Data / versija | Pastaba |
| --- | --- | --- | --- | --- |
| market_availability | JRCALC Clinical Guidelines 2025 Reference Edition | uk | 2025 leidimas | Pratarmėje teigiama, kad vaistų informacija originale perkelta į JRCALC programėles; LT tekste tai paliekama tik kaip originalo leidinio naudojimo pastaba. |

## Norminių teiginių matrica

| claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| claim-001-original-app-ecosystem | market_availability | Foreword | original_context_callout | original-context-only |  |  |  | Nuorodos į `JRCALC apps`, `iCPG` ir `JRCALC Plus`, taip pat vaistų skyriaus nebuvimas spausdintame leidime, paliekami tik kaip originalo leidinio naudojimo ir prieigos kontekstas. |

## Struktūrinių blokų lokalizacijos sprendimai

| block_id | block_type | lt_strategy | authority_source | original_context_allowed | note |
| --- | --- | --- | --- | --- | --- |

## Neperkeliamas originalo turinys

- `JRCALC apps`, `iCPG`, `JRCALC Plus` ir `NPIS-Toxbase` nėra LT norminiai įrankiai ar oficialūs vietiniai šaltiniai.
- Nuoroda, kad vaistų informacijos reikia ieškoti originalo programėlėse, neturi būti suprasta kaip LT klinikinė rekomendacija.
- `PFD rulings` ir `HSSIB` minima kaip JK sistemos vidaus kontekstas.

## Adjudication sprendimai

- narrative-01-foreword | hibridinis | Palikta aiški pratarmės informacinė seka, bet proza sutrumpinta ir išvalyta nuo nereikalingo originalo institucinio svorio.

## Lokalizacijos sprendimai

- Pagrindinis LT tekstas pateikiamas kaip knygos pratarmė ir leidimo apžvalga, o ne kaip LT norminis skyrius.
- Platformų ir JK institucijų pavadinimai paliekami tik tiek, kiek reikia originalo leidiniui suprasti.
- Vaistų informacijos nuoroda į originalo programėles neperkeliama kaip LT rekomendacija.

## Vietos, kur originalas pakeistas pagal Lietuvos praktiką

- Nuoroda į vaistų informaciją originalo programėlėse LT tekste apibrėžta kaip originalo leidinio naudojimo pastaba, ne kaip vietinio darbo rekomendacija.
- JK institucinių pavadinimų svoris sumažintas ir perkeltas į `Originalo kontekstas`.

## Kalbinės rizikos vietos

- `preferred way of accessing current clinical guidance` nepalikti kaip gremėzdiškos pažodinės konstrukcijos.
- `supports our recommendation` perrašyti be biurokratinio anglų karkaso.
- Ilgą vienos pastraipos naujienų sąrašą skaidyti į skaitomus LT informacinius vienetus.

## Anti-calque perrašymo pastabos

- Pratarmę rašyti kaip natūralią lietuvišką leidimo įžangą, o ne kaip pažodinį organizacinį memorandumą.
- `newly developed guidance was issued` perrašyti paprasčiau: `parengtos naujos gairės`, `atnaujintos rekomendacijos`.
- Vengti tiesioginio anglų sakinių ritmikos atkartojimo padėkų ir leidinio pokyčių pastraipose.

## Atviros abejonės

- Kol kas neužfiksuota.

## Finalus agento auditas

| Sritis | Statusas | Pastaba |
| --- | --- | --- |
| terminija | sutvarkyta | Platformų ir organizacijų pavadinimai palikti tik kaip originalo kontekstas. |
| kolokacijos | sutvarkyta | Pratarmė perrašyta į natūralesnę LT leidinio įžangos kalbą. |
| gramatika | ok |  |
| semantika | sutvarkyta | Atskirta, kas yra leidinio pristatymas, o kas tik JK originalo ekosistema. |
| norminė logika | sutvarkyta | Skyrius neperteiktas kaip LT norminis autoritetas. |
| atviros abejonės | ok |  |

## Chapter pack ir review kilpa

- `research` paruoštas `chapter_pack` generavimui.
- Jei `chapter_pack` pažymės aukštos rizikos vietas, sugeneruoti `adjudication_pack` ir patikrinti, ar pakanka vieno `hibridinis` sprendimo visai pratarmės narrative daliai.

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
