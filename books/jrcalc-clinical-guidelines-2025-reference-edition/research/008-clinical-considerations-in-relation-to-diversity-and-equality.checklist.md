# Research checklist for 008-clinical-considerations-in-relation-to-diversity-and-equality

- Angliškas failas: `/Users/dzukauskas/Projects/Acute Medicine/books/jrcalc-clinical-guidelines-2025-reference-edition/source/chapters-en/008-clinical-considerations-in-relation-to-diversity-and-equality.md`
- Research failas: `/Users/dzukauskas/Projects/Acute Medicine/books/jrcalc-clinical-guidelines-2025-reference-edition/research/008-clinical-considerations-in-relation-to-diversity-and-equality.md`
- Skyriaus tipas: `mišrus norminis / lokalizacinis`
- Aptikti norminių claim tipai: `algorithm_step, legal_scope, market_availability`
- Aptikti jurisdikciniai signalai: `JRCALC, NHS, HCPC, ReSPECT, NEWS2`
- Aptikti struktūriniai blokai: `0`

## Poskyrių inventorius

- Nepavyko automatiškai nustatyti poskyrių; peržiūrėkite source ranka.

## Aptikti jurisdikciniai / rinkos signalai

| Signalas | Jurisdikcija | Tipas | Pastaba |
| --- | --- | --- | --- |
| JRCALC | uk | guideline | UK ambulance guideline source. |
| NHS | uk | service model | UK health service context. |
| HCPC | uk | regulator | UK regulator. |
| ReSPECT | uk | law | UK treatment escalation / resuscitation framework. |
| NEWS2 | uk | guideline | UK early warning score. |

## Rekomenduojami LT-source keliai

| Sritis | Kodėl įtraukta | Pagrindiniai LT šaltiniai | ES fallback | Pastaba |
| --- | --- | --- | --- | --- |
| terminija_ir_kalbos_forma | LT terminijai ir kolokacijoms. | VLKK Terminų bankas | ES / tarptautinė nomenklatūra | VLKK nėra klinikinis autoritetas, todėl medicininę reikšmę tikrinti kartu su klinikiniais šaltiniais. |
| klinikinės_metodikos_ir_specialybines_rekomendacijos | Reikalinga dėl aptikto claim tipo `algorithm_step`. | SAM metodikos ir rekomendacijos | Europos specialybinės gairės | Jei LT metodika sena ar nėra pakankama, pereiti į ES sluoksnį ir tai pažymėti research faile. |
| paramediko_kompetencija_ir_gmp | Reikalinga dėl aptikto claim tipo `algorithm_step`. | SAM; e-Seimas/TAR; Greitosios medicinos pagalbos tarnyba | ERC; specialybinės ES gairės | Pirmas norminis sluoksnis skubiajai medicinai Lietuvoje. |
| teise_ir_reguliavimas | Reikalinga dėl aptikto claim tipo `legal_scope`. | e-Seimas; TAR; SAM | EUR-Lex; EMA | Pirmiausia naudoti galiojančią suvestinę redakciją ir užrašyti datą. |
| kompensavimas_ir_rinkos_prieinamumas | Reikalinga dėl aptikto claim tipo `market_availability`. | VLK kompensuojamieji vaistai; VLK kainynai | EMA | Naudoti, kai svarbu ne tik veiklioji medžiaga, bet ir paciento prieiga Lietuvoje. |
| vaistu_registracija_ir_produkto_informacija | Reikalinga dėl aptikto claim tipo `market_availability`. | VVKT registruotų vaistinių preparatų paieška; VVKT registracijos pažymėjimo priedai | EMA; ES SmPC / product information | Jei vaisto nėra LT rinkoje arba LT informacija nepakankama, pereiti į EMA / ES sluoksnį. |

## Preliminari norminių teiginių matrica

| claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| todo-algorithm-step-01 | algorithm_step | - The JRCALC guidelines seek to set out the clinical practice and approach to the people who seek help from ambulance services. In a diverse society we need to understand how our clinical practice needs to flex and adapt to ensure an equity of care for all. | keep_lt_normative | LT | SAM metodikos ir rekomendacijos |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |
| todo-legal-scope-02 | legal_scope | - At an individual level practitioners should be aware that their preconceptions and liability to cognitive bias can influence how they perceive and care for patients and actively minimise their impact. 1 | keep_lt_normative | LT | e-Seimas; TAR; SAM |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |
| todo-market-availability-03 | market_availability | - Where relevant information regarding a patient’s sexuality has been obtained, this information should be recorded and handed over to other health care professionals with the patient’s consent, to ensure this information is available for those caring for the patient further along the chain of care. | keep_lt_normative | LT | VLK kompensuojamieji vaistai; VLK kainynai |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |

## Preliminarūs struktūrinių blokų lokalizacijos sprendimai

- Source skyriuje automatiškai neaptikta atskirų lentelių, paveikslų, schemų ar rėmelių.

## Rankiniai veiksmai prieš draftą

- Peržiūrėkite originalo skyriaus intervalą ar šaltinio segmentus ranka ir patikslinkite, ar visi norminiai teiginiai sugaudyti.
- Jei claim lieka pagrindiniame LT tekste kaip norminis, jam būtinas konkretus LT šaltinis.
- Jei LT sluoksnio nepakanka ir tenka remtis ES, research faile užpildykite `lt_gap_reason`.
- `figure` ir `algorithm` editable šaltinis šiame repo lieka tik `Whimsical`.
- Po drafto būtinai užpildykite `## Finalus agento auditas` research faile.
