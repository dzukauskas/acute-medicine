# Research checklist for 006-list-of-abbreviations

- Angliškas failas: `source/chapters-en/006-list-of-abbreviations.md`
- Research failas: `research/006-list-of-abbreviations.md`
- Skyriaus tipas: `jurisdikciškai jautrus / lokalizacinis`
- Aptikti norminių claim tipai: `nenustatyta`
- Aptikti jurisdikciniai signalai: `CMI, JRCALC, NHS, ReSPECT, DNACPR`
- Aptikti struktūriniai blokai: `0`

## Poskyrių inventorius

- Nepavyko automatiškai nustatyti poskyrių; peržiūrėkite source ranka.

## Aptikti jurisdikciniai / rinkos signalai

| Signalas | Jurisdikcija | Tipas | Pastaba |
| --- | --- | --- | --- |
| CMI | australia | reference tool | Australian patient leaflet acronym. |
| JRCALC | uk | guideline | UK ambulance guideline source. |
| NHS | uk | service model | UK health service context. |
| ReSPECT | uk | law | UK treatment escalation / resuscitation framework. |
| DNACPR | uk | law | UK resuscitation legal framework. |

## Rekomenduojami LT-source keliai

| Sritis | Kodėl įtraukta | Pagrindiniai LT šaltiniai | ES fallback | Pastaba |
| --- | --- | --- | --- | --- |
| terminija_ir_kalbos_forma | LT terminijai ir kolokacijoms. | VLKK Terminų bankas | ES / tarptautinė nomenklatūra | VLKK nėra klinikinis autoritetas, todėl medicininę reikšmę tikrinti kartu su klinikiniais šaltiniais. |
| farmakologija_ir_racionalus_skyrimas | Reikalinga dėl jurisdikcinio / rinkos signalo `CMI` (reference tool). | SAM racionalus vaistų skyrimas ir vartojimas; VVKT | EMA; ESC; ESMO; kitos ES specialybinės gairės | Fundamentinė farmakologija gali remtis universaliu mokslu, bet norminiai sprendimai turi eiti per LT/EU šaltinius. |
| klinikinės_metodikos_ir_specialybines_rekomendacijos | Reikalinga dėl jurisdikcinio / rinkos signalo `CMI` (reference tool). | SAM metodikos ir rekomendacijos | Europos specialybinės gairės | Jei LT metodika sena ar nėra pakankama, pereiti į ES sluoksnį ir tai pažymėti research faile. |
| paramediko_kompetencija_ir_gmp | Reikalinga dėl jurisdikcinio / rinkos signalo `NHS` (service model). | SAM; e-Seimas/TAR; Greitosios medicinos pagalbos tarnyba | ERC; specialybinės ES gairės | Pirmas norminis sluoksnis skubiajai medicinai Lietuvoje. |

## Preliminari norminių teiginių matrica

- Šiame skyriuje automatiškai neaptikta norminių claim tipų.
- Jei po research paaiškės, kad skyriuje yra dozės, indikacijos, vartojimo keliai, algoritmai ar teisinės ribos, užpildykite `## Norminių teiginių matrica` ranka.

## Preliminarūs struktūrinių blokų lokalizacijos sprendimai

- Source skyriuje automatiškai neaptikta atskirų lentelių, paveikslų, schemų ar rėmelių.

## Rankiniai veiksmai prieš draftą

- Peržiūrėkite originalo skyriaus intervalą ar šaltinio segmentus ranka ir patikslinkite, ar visi norminiai teiginiai sugaudyti.
- Jei claim lieka pagrindiniame LT tekste kaip norminis, jam būtinas konkretus LT šaltinis.
- Jei LT sluoksnio nepakanka ir tenka remtis ES, research faile užpildykite `lt_gap_reason`.
- `figure` ir `algorithm` editable šaltinis šiame repo lieka tik `Whimsical`.
- Po drafto būtinai užpildykite `## Finalus agento auditas` research faile.
