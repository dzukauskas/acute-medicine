# Research checklist for 004-guideline-development-methodology

- Angliškas failas: `/Users/dzukauskas/Projects/Acute Medicine/books/jrcalc-clinical-guidelines-2025-reference-edition/source/chapters-en/004-guideline-development-methodology.md`
- Research failas: `/Users/dzukauskas/Projects/Acute Medicine/books/jrcalc-clinical-guidelines-2025-reference-edition/research/004-guideline-development-methodology.md`
- Skyriaus tipas: `mišrus norminis / lokalizacinis`
- Aptikti norminių claim tipai: `monitoring`
- Aptikti jurisdikciniai signalai: `JRCALC`
- Aptikti struktūriniai blokai: `0`

## Poskyrių inventorius

- Nepavyko automatiškai nustatyti poskyrių; peržiūrėkite source ranka.

## Aptikti jurisdikciniai / rinkos signalai

| Signalas | Jurisdikcija | Tipas | Pastaba |
| --- | --- | --- | --- |
| JRCALC | uk | guideline | UK ambulance guideline source. |

## Rekomenduojami LT-source keliai

| Sritis | Kodėl įtraukta | Pagrindiniai LT šaltiniai | ES fallback | Pastaba |
| --- | --- | --- | --- | --- |
| terminija_ir_kalbos_forma | LT terminijai ir kolokacijoms. | VLKK Terminų bankas | ES / tarptautinė nomenklatūra | VLKK nėra klinikinis autoritetas, todėl medicininę reikšmę tikrinti kartu su klinikiniais šaltiniais. |
| klinikinės_metodikos_ir_specialybines_rekomendacijos | Reikalinga dėl aptikto claim tipo `monitoring`. | SAM metodikos ir rekomendacijos | Europos specialybinės gairės | Jei LT metodika sena ar nėra pakankama, pereiti į ES sluoksnį ir tai pažymėti research faile. |
| paramediko_kompetencija_ir_gmp | Reikalinga dėl aptikto claim tipo `monitoring`. | SAM; e-Seimas/TAR; Greitosios medicinos pagalbos tarnyba | ERC; specialybinės ES gairės | Pirmas norminis sluoksnis skubiajai medicinai Lietuvoje. |

## Preliminari norminių teiginių matrica

| claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| todo-monitoring-01 | monitoring | JRCALC, NASMeD (National Ambulance Service Medical Directors) and the ALPG (Ambulance Lead Paramedic Group) will advise on those clinical guidelines which need updating and those clinical conditions which need a new guideline developing. These are then prioritised and assessed with regard, to urgency and risk. Clinical topics can be identified through a variety of means including the monitoring of serious incidents within individual UK Ambulance Service Trusts, preventing future death reports issued by coroners and national service reconfigurations. In addition JRCALC provide extensive clinical expertise and advice on potential new developments to ensure that the guidelines capture latest best practice and future innovations and encourage further research into pre hospital care. | keep_lt_normative | LT | SAM metodikos ir rekomendacijos |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |

## Preliminarūs struktūrinių blokų lokalizacijos sprendimai

- Source skyriuje automatiškai neaptikta atskirų lentelių, paveikslų, schemų ar rėmelių.

## Rankiniai veiksmai prieš draftą

- Peržiūrėkite originalo skyriaus intervalą ar šaltinio segmentus ranka ir patikslinkite, ar visi norminiai teiginiai sugaudyti.
- Jei claim lieka pagrindiniame LT tekste kaip norminis, jam būtinas konkretus LT šaltinis.
- Jei LT sluoksnio nepakanka ir tenka remtis ES, research faile užpildykite `lt_gap_reason`.
- `figure` ir `algorithm` editable šaltinis šiame repo lieka tik `Whimsical`.
- Po drafto būtinai užpildykite `## Finalus agento auditas` research faile.
