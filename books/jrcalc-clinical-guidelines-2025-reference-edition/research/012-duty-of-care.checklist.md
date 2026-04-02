# Research checklist for 012-duty-of-care

- Angliškas failas: `source/chapters-en/012-duty-of-care.md`
- Research failas: `research/012-duty-of-care.md`
- Skyriaus tipas: `mišrus norminis / lokalizacinis`
- Aptikti norminių claim tipai: `monitoring, market_availability`
- Aptikti jurisdikciniai signalai: `JRCALC, NHS`
- Aptikti struktūriniai blokai: `0`

## Poskyrių inventorius

- Nepavyko automatiškai nustatyti poskyrių; peržiūrėkite source ranka.

## Aptikti jurisdikciniai / rinkos signalai

| Signalas | Jurisdikcija | Tipas | Pastaba |
| --- | --- | --- | --- |
| JRCALC | uk | guideline | UK ambulance guideline source. |
| NHS | uk | service model | UK health service context. |

## Rekomenduojami LT-source keliai

| Sritis | Kodėl įtraukta | Pagrindiniai LT šaltiniai | ES fallback | Pastaba |
| --- | --- | --- | --- | --- |
| terminija_ir_kalbos_forma | LT terminijai ir kolokacijoms. | VLKK Terminų bankas | ES / tarptautinė nomenklatūra | VLKK nėra klinikinis autoritetas, todėl medicininę reikšmę tikrinti kartu su klinikiniais šaltiniais. |
| klinikinės_metodikos_ir_specialybines_rekomendacijos | Reikalinga dėl aptikto claim tipo `monitoring`. | SAM metodikos ir rekomendacijos | Europos specialybinės gairės | Jei LT metodika sena ar nėra pakankama, pereiti į ES sluoksnį ir tai pažymėti research faile. |
| paramediko_kompetencija_ir_gmp | Reikalinga dėl aptikto claim tipo `monitoring`. | SAM; e-Seimas/TAR; Greitosios medicinos pagalbos tarnyba | ERC; specialybinės ES gairės | Pirmas norminis sluoksnis skubiajai medicinai Lietuvoje. |
| kompensavimas_ir_rinkos_prieinamumas | Reikalinga dėl aptikto claim tipo `market_availability`. | VLK kompensuojamieji vaistai; VLK kainynai | EMA | Naudoti, kai svarbu ne tik veiklioji medžiaga, bet ir paciento prieiga Lietuvoje. |
| vaistu_registracija_ir_produkto_informacija | Reikalinga dėl aptikto claim tipo `market_availability`. | VVKT registruotų vaistinių preparatų paieška; VVKT registracijos pažymėjimo priedai | EMA; ES SmPC / product information | Jei vaisto nėra LT rinkoje arba LT informacija nepakankama, pereiti į EMA / ES sluoksnį. |

## Preliminari norminių teiginių matrica

| claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| todo-monitoring-01 | monitoring | - Safe systems of work must also be reviewed periodically and/or when the work activity or risk changes. NHS ambulance services must also implement appropriate monitoring/supervision to ensure compliance with the safe system of work. | keep_lt_normative | LT | SAM metodikos ir rekomendacijos |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |
| todo-market-availability-02 | market_availability | / Duty of care to staff / Take all reasonable and practical steps to keep employees safe. / Perform approved activities and apply the controls specified in procedures. Ensure there is a generic risk assessment already in place. Ensure you are trained and competent to undertake the activity. Ensure the minimum equipment mandated by procedures is available and used (including your Personal Protective Equipment (PPE). / These are statutory duties under the Health and Safety at Work Act 1974 and associated regulatory provisions. These steps will help ensure you have a safe system of work. Most of these provisions should already be established prior to the incident. / | keep_lt_normative | LT | VLK kompensuojamieji vaistai; VLK kainynai |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |

## Preliminarūs struktūrinių blokų lokalizacijos sprendimai

- Source skyriuje automatiškai neaptikta atskirų lentelių, paveikslų, schemų ar rėmelių.

## Rankiniai veiksmai prieš draftą

- Peržiūrėkite originalo skyriaus intervalą ar šaltinio segmentus ranka ir patikslinkite, ar visi norminiai teiginiai sugaudyti.
- Jei claim lieka pagrindiniame LT tekste kaip norminis, jam būtinas konkretus LT šaltinis.
- Jei LT sluoksnio nepakanka ir tenka remtis ES, research faile užpildykite `lt_gap_reason`.
- `figure` ir `algorithm` editable šaltinis šiame repo lieka tik `Whimsical`.
- Po drafto būtinai užpildykite `## Finalus agento auditas` research faile.
