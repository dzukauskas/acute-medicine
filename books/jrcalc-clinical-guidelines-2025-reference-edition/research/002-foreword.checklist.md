# Research checklist for 002-foreword

- Angliškas failas: `/Users/dzukauskas/Projects/Acute Medicine/books/jrcalc-clinical-guidelines-2025-reference-edition/source/chapters-en/002-foreword.md`
- Research failas: `/Users/dzukauskas/Projects/Acute Medicine/books/jrcalc-clinical-guidelines-2025-reference-edition/research/002-foreword.md`
- Skyriaus tipas: `mišrus norminis / lokalizacinis`
- Aptikti norminių claim tipai: `market_availability`
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
| kompensavimas_ir_rinkos_prieinamumas | Reikalinga dėl aptikto claim tipo `market_availability`. | VLK kompensuojamieji vaistai; VLK kainynai | EMA | Naudoti, kai svarbu ne tik veiklioji medžiaga, bet ir paciento prieiga Lietuvoje. |
| vaistu_registracija_ir_produkto_informacija | Reikalinga dėl aptikto claim tipo `market_availability`. | VVKT registruotų vaistinių preparatų paieška; VVKT registracijos pažymėjimo priedai | EMA; ES SmPC / product information | Jei vaisto nėra LT rinkoje arba LT informacija nepakankama, pereiti į EMA / ES sluoksnį. |

## Preliminari norminių teiginių matrica

| claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| todo-market-availability-01 | market_availability | New for this edition are significant updates in the Maternity section. There are now standalone guidelines for Breech Birth, Cord Prolapse, Shoulder Dystocia, and bleeding up to and after 20 weeks’ gestation. We have also introduced the Prehospital Maternity Decision Tool to be used when assessing patients who are pregnant and up to 4 weeks’ post-partum. We have expanded our guidance on behavioural emergencies, with three new guidelines, Behavioural Emergencies, Delirium and Agitated Patients. These are intended to be used in conjunction with one another to aid paramedic decision-making. There have also been significant updates to trauma guidelines; overdose and poisoning, sepsis and pain management. Many more updates have been made across medical, trauma and general guidance, often in response to queries being raised and new evidence becoming available. | keep_lt_normative | LT | VLK kompensuojamieji vaistai; VLK kainynai |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |

## Preliminarūs struktūrinių blokų lokalizacijos sprendimai

- Source skyriuje automatiškai neaptikta atskirų lentelių, paveikslų, schemų ar rėmelių.

## Rankiniai veiksmai prieš draftą

- Peržiūrėkite originalo skyriaus intervalą ar šaltinio segmentus ranka ir patikslinkite, ar visi norminiai teiginiai sugaudyti.
- Jei claim lieka pagrindiniame LT tekste kaip norminis, jam būtinas konkretus LT šaltinis.
- Jei LT sluoksnio nepakanka ir tenka remtis ES, research faile užpildykite `lt_gap_reason`.
- `figure` ir `algorithm` editable šaltinis šiame repo lieka tik `Whimsical`.
- Po drafto būtinai užpildykite `## Finalus agento auditas` research faile.
