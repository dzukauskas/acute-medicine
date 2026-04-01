# Research checklist for 011-domestic-abuse

- Angliškas failas: `source/chapters-en/011-domestic-abuse.md`
- Research failas: `research/011-domestic-abuse.md`
- Skyriaus tipas: `mišrus norminis / lokalizacinis`
- Aptikti norminių claim tipai: `route, algorithm_step, market_availability`
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
| vaistu_registracija_ir_produkto_informacija | Reikalinga dėl aptikto claim tipo `route`. | VVKT registruotų vaistinių preparatų paieška; VVKT registracijos pažymėjimo priedai | EMA; ES SmPC / product information | Jei vaisto nėra LT rinkoje arba LT informacija nepakankama, pereiti į EMA / ES sluoksnį. |
| farmakologija_ir_racionalus_skyrimas | Reikalinga dėl aptikto claim tipo `route`. | SAM racionalus vaistų skyrimas ir vartojimas; VVKT | EMA; ESC; ESMO; kitos ES specialybinės gairės | Fundamentinė farmakologija gali remtis universaliu mokslu, bet norminiai sprendimai turi eiti per LT/EU šaltinius. |
| klinikinės_metodikos_ir_specialybines_rekomendacijos | Reikalinga dėl aptikto claim tipo `algorithm_step`. | SAM metodikos ir rekomendacijos | Europos specialybinės gairės | Jei LT metodika sena ar nėra pakankama, pereiti į ES sluoksnį ir tai pažymėti research faile. |
| paramediko_kompetencija_ir_gmp | Reikalinga dėl aptikto claim tipo `algorithm_step`. | SAM; e-Seimas/TAR; Greitosios medicinos pagalbos tarnyba | ERC; specialybinės ES gairės | Pirmas norminis sluoksnis skubiajai medicinai Lietuvoje. |
| kompensavimas_ir_rinkos_prieinamumas | Reikalinga dėl aptikto claim tipo `market_availability`. | VLK kompensuojamieji vaistai; VLK kainynai | EMA | Naudoti, kai svarbu ne tik veiklioji medžiaga, bet ir paciento prieiga Lietuvoje. |

## Preliminari norminių teiginių matrica

| claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| todo-route-01 | route | / Assess <C>ABCDE If any TIME-CRITICAL features present major ABCDE problems: Start correcting <C>ABCDE problems. Undertake a TIME-CRITICAL transfer to nearest receiving hospital. Continue patient management en route. Provide an ATMIST information call. / | keep_lt_normative | LT | VVKT registruotų vaistinių preparatų paieška; VVKT registracijos pažymėjimo priedai |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |
| todo-algorithm-step-02 | algorithm_step | For the assessment and management of domestic abuse, refer to Table 1.1 . | keep_lt_normative | LT | SAM metodikos ir rekomendacijos |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |
| todo-market-availability-03 | market_availability | / 1. / HM Government. Tackling Domestic Abuse Plan . 2022. Available from: https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1064427/E02735263_Tackling_Domestic_Abuse_CP_639_Accessible.pdf . / | keep_lt_normative | LT | VLK kompensuojamieji vaistai; VLK kainynai |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |

## Preliminarūs struktūrinių blokų lokalizacijos sprendimai

- Source skyriuje automatiškai neaptikta atskirų lentelių, paveikslų, schemų ar rėmelių.

## Rankiniai veiksmai prieš draftą

- Peržiūrėkite originalo skyriaus intervalą ar šaltinio segmentus ranka ir patikslinkite, ar visi norminiai teiginiai sugaudyti.
- Jei claim lieka pagrindiniame LT tekste kaip norminis, jam būtinas konkretus LT šaltinis.
- Jei LT sluoksnio nepakanka ir tenka remtis ES, research faile užpildykite `lt_gap_reason`.
- `figure` ir `algorithm` editable šaltinis šiame repo lieka tik `Whimsical`.
- Po drafto būtinai užpildykite `## Finalus agento auditas` research faile.
