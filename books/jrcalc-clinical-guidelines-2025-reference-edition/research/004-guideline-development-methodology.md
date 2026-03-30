# 4 skyrius. Guideline Development Methodology

- Puslapiai: EPUB segmentas `cMD.xhtml`
- Šaltinio segmentai: `cMD.xhtml`
- Originalo failas: `source/epub/JRCALC Clinical Guidelines 2025 Reference Edition.epub`
- Angliškas pagalbinis failas: `source/chapters-en/004-guideline-development-methodology.md`
- Lietuviškas failas: `lt/chapters/004-guideline-development-methodology.md`

## Source inventorius

### Poskyriai

- Guideline Development Methodology
- Guideline Selection
- Editorial Independence
- Citing the JRCALC Guidelines

### Lentelės

- Kol kas neužfiksuota

### Paveikslai / schemos / algoritmai

- Kol kas neužfiksuota

### Rėmeliai / papildomi blokai

- Kol kas neužfiksuota

## Rizikingi terminai

- JRCALC
- AGREE II
- NASMeD
- ALPG
- UK Ambulance Services Clinical Practice Guidelines
- preventing future death reports
- national service reconfigurations

## Lietuvos šaltiniai

| Šaltinis | Tipas | Data / versija | Kodėl naudotas |
| --- | --- | --- | --- |
| VLKK Terminų bankas | terminija | žiūrėta 2026-03-28 | LT metodologinei kalbai, antraštėms ir neutralioms gairių rengimo formuluotėms. |
| Greitosios medicinos pagalbos tarnybos vieša informacija | institucinis LT kontekstas | žiūrėta 2026-03-28 | Kad originalo JK tarnybų, service model ir komitetų logika nebūtų pateikta kaip LT organizacinis standartas. |

## Europos / tarptautiniai šaltiniai

| Šaltinis | Tipas | Data / versija | Kodėl naudotas |
| --- | --- | --- | --- |
| AGREE II (Appraisal of Guidelines for Research and Evaluation) | gairių metodologijos karkasas | žiūrėta 2026-03-28 | Kad LT tekste tiksliai perteikti, kokį metodologinį vertinimo karkasą mini originalas. |
| JRCALC Clinical Guidelines 2025 Reference Edition | originalus šaltinis | 2025 leidimas | Naudotas kaip konkretaus leidinio metodologijos, redakcinės nepriklausomybės ir citavimo formos šaltinis. |

## LT-source branduolio taikymas

| Sritis | Pagrindinis LT-source kelias | Konkretus LT šaltinis | ES fallback | Pastaba |
| --- | --- | --- | --- | --- |
| terminija | terminija_ir_kalbos_forma | VLKK Terminų bankas | tarptautinė nomenklatūra | Reikalinga natūraliai LT metodologinei kalbai. |
| institucinis_kontekstas | paramediko_kompetencija_ir_gmp | Greitosios medicinos pagalbos tarnybos vieša informacija | ERC; specialybinės ES gairės | Naudota tik tam, kad JK ambulance service ir komitetų logika liktų originalo kontekstu, ne LT standartu. |
| gairiu_metodologija | klinikinės_metodikos_ir_specialybines_rekomendacijos | tarptautinė gairių rengimo metodologija | AGREE II | Šiame skyriuje metodologinis karkasas yra tarptautinis, bet taikomas originalo leidinio rengimo procesui. |

## Jurisdikcijos ir rinkos signalai

| Signalas | Jurisdikcija | Tipas | Šaltinio vieta | Pastaba |
| --- | --- | --- | --- | --- |
| JRCALC | uk | gairės | `cMD.xhtml` visame skyriuje | Tai originalo leidinio gairių sistemos pavadinimas. |
| NASMeD | uk | service model | `cMD.xhtml` guideline selection pastraipa | JK ambulance service medicinos direktorių grupė. |
| ALPG | uk | service model | `cMD.xhtml` guideline selection pastraipa | JK ambulance lead paramedic grupės santrumpa. |

## LT/EU pakeitimo sprendimai

| Signalas | Veiksmas | Autoritetas | LT / EU sprendimas | Šaltinio nuoroda | Pastaba |
| --- | --- | --- | --- | --- | --- |
| JRCALC | original_context_callout | original-context-only | Palikti tik kaip konkretaus originalo leidinio gairių sistemos pavadinimą. | `shared/localization/localization_overrides.tsv` (`JRCALC`); originalus skyrius `cMD.xhtml` | Negalima pateikti kaip LT norminio ar metodologinio autoriteto. |
| NASMeD | original_context_callout | original-context-only | Palikti tik kaip oficialią originalo organizacinio tinklo santrumpą. | originalus skyrius `cMD.xhtml` | LT tekste nekurti lietuviško institucinio atitikmens. |
| ALPG | original_context_callout | original-context-only | Palikti tik kaip oficialią originalo profesinės grupės santrumpą. | originalus skyrius `cMD.xhtml` | LT tekste tai tik originalo organizacinio proceso dalis. |

## Vaistų ir dozių LT/EU šaltinių bazė

| Tema | Šaltinis | Jurisdikcija | Data / versija | Pastaba |
| --- | --- | --- | --- | --- |
| monitoring | JRCALC Clinical Guidelines 2025 Reference Edition | uk | 2025 leidimas | Skyriuje aprašoma, pagal kokius JK proceso signalus ir stebėsenos duomenis nustatomas gairių atnaujinimo poreikis; LT tekste tai paliekama tik kaip originalo metodologinio proceso kontekstas. |

## Norminių teiginių matrica

| claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| claim-001-methodology-monitoring | monitoring | Guideline Selection | original_context_callout | original-context-only |  |  |  | Originale aprašoma, pagal kokius JK proceso signalus ir stebėsenos duomenis parenkamos gairių atnaujinimo temos; LT tekste tai paliekama tik kaip originalo rengimo proceso paaiškinimas. |

## Struktūrinių blokų lokalizacijos sprendimai

| block_id | block_type | lt_strategy | authority_source | original_context_allowed | note |
| --- | --- | --- | --- | --- | --- |

## Neperkeliamas originalo turinys

- Originalo nuorodos į JK ambulance service trustus, coroners' reports ir national service reconfigurations nėra LT organizacinis standartas.
- Grįžtamojo ryšio el. pašto adresas ir originalo citavimo forma yra leidinio credits / bibliografinis kontekstas.

## Adjudication sprendimai

- narrative-02-guideline-selection | hibridinis | Gairių atrankos ir prioritetizavimo logika palikta kaip aiškus originalo proceso paaiškinimas, bet perrašyta glaustai ir perkelta į `Originalo kontekstas`, kad neskambėtų kaip LT norminis algoritmas.

## Lokalizacijos sprendimai

- Pagrindiniame LT tekste paliktas tik bendras metodologinis paaiškinimas.
- JK organizacinė gairių atrankos logika perkelta į `Originalo kontekstas` bloką.
- AGREE II paminėtas kaip metodologinis karkasas, bet ne kaip LT nacionalinis reguliacinis sluoksnis.

## Vietos, kur originalas pakeistas pagal Lietuvos praktiką

- Vengta perteikti JK service model ir incident reporting logiką kaip vietinį LT gairių rengimo standartą.
- Ceremoninis ir organizacinis originalo tonas sutrumpintas iki aiškios LT metodologinės santraukos.

## Kalbinės rizikos vietos

- `designed to comply with the criteria used by...` nepalikti gremėzdiškos pažodinės konstrukcijos.
- `provide a framework to` versti kaip aiškią paskirtį, ne tiesioginę anglų kalbos kalkę.
- `guideline developing` ir `national service reconfigurations` neperrašyti pažodžiui be paaiškinimo.

## Anti-calque perrašymo pastabos

- Pagrindinę pastraipą rašyti kaip trumpą metodologinę santrauką, ne kaip pažodinį procedūrinį anglišką aprašą.
- AGREE II funkcijas geriau perteikti punktų sąrašu.
- Redakcinę nepriklausomybę ir citavimo informaciją laikyti originalo leidinio kontekstu.

## Atviros abejonės

- Kol kas neužfiksuota.

## Finalus agento auditas

| Sritis | Statusas | Pastaba |
| --- | --- | --- |
| terminija | sutvarkyta | Metodologiniai terminai suvienodinti, JRCALC/NASMeD/ALPG palikti tik originalo kontekste. |
| kolokacijos | sutvarkyta | Procesinės angliškos formuluotės perrašytos į glaustesnę LT metodologinę kalbą. |
| gramatika | ok |  |
| semantika | sutvarkyta | Aiškiai atskirta bendroji metodologija nuo JK organizacinio proceso. |
| norminė logika | sutvarkyta | Skyrius neperteiktas kaip LT norminis gairių rengimo standartas. |
| atviros abejonės | ok |  |

## Chapter pack ir review kilpa

- `research` paruoštas `chapter_pack` generavimui.
- Jei vėliau kartosis AGREE II ar kitų metodologinių terminų formuluotės, jas kelti per `term_candidates.tsv`, o ne ranka dauginti atskiruose skyriuose.

## Baigiamoji kontrolė

- [x] Perskaitytas visas source skyriaus intervalas arba segmentų rinkinys
- [x] Užfiksuoti visi teksto blokai
- [x] Užfiksuotos visos lentelės
- [x] Užfiksuoti visi paveikslai ir schemos
- [x] Patikrinti Lietuvos šaltiniai ir jų datos
- [x] Jei reikėjo, patikrintos Europos / tarptautinės gairės
- [x] Užpildyta `LT-source branduolio taikymas` lentelė pagal `shared/localization/lt_source_map.tsv`
- [x] Užfiksuoti visi UK / Australia / US / rinkos signalai
- [x] Kiekvienam signalui paliktas LT/EU pakeitimo sprendimas
- [x] Vaistų ir dozių LT/EU šaltinių bazė užpildyta
- [x] Užpildyta `Norminių teiginių matrica`, jei skyriuje yra norminis klinikinis turinys
- [x] Užpildyti struktūrinių blokų lokalizacijos sprendimai
- [x] Sugeneruotas `chapter_pack`
- [x] Jei reikia, sugeneruotas `adjudication_pack`
- [x] Jei sugeneruotas `adjudication_pack`, palikta `## Adjudication sprendimai` sekcija fiksuotu `- block_id | pasirinkimas | priežastis` formatu
- [x] Lietuviškas skyrius parašytas nuo švaraus lapo
- [x] Padarytas atskiras anti-calque perrašymas
- [x] Lentelės išverstos
- [x] Paveikslai / schemos atkurti lietuviškai
- [x] Numeracija atitinka knygą
- [x] Užpildytas `Finalus agento auditas`
