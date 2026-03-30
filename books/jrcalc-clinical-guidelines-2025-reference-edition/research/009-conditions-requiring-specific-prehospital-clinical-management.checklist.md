# Research checklist for 009-conditions-requiring-specific-prehospital-clinical-management

- Angliškas failas: `source/chapters-en/009-conditions-requiring-specific-prehospital-clinical-management.md`
- Research failas: `research/009-conditions-requiring-specific-prehospital-clinical-management.md`
- Skyriaus tipas: `mišrus norminis / lokalizacinis`
- Aptikti norminių claim tipai: `dose, route, concentration, algorithm_step, market_availability`
- Aptikti jurisdikciniai signalai: `JRCALC, NHS, ReSPECT`
- Aptikti struktūriniai blokai: `0`

## Poskyrių inventorius

- Nepavyko automatiškai nustatyti poskyrių; peržiūrėkite source ranka.

## Aptikti jurisdikciniai / rinkos signalai

| Signalas | Jurisdikcija | Tipas | Pastaba |
| --- | --- | --- | --- |
| JRCALC | uk | guideline | UK ambulance guideline source. |
| NHS | uk | service model | UK health service context. |
| ReSPECT | uk | law | UK treatment escalation / resuscitation framework. |

## Rekomenduojami LT-source keliai

| Sritis | Kodėl įtraukta | Pagrindiniai LT šaltiniai | ES fallback | Pastaba |
| --- | --- | --- | --- | --- |
| terminija_ir_kalbos_forma | LT terminijai ir kolokacijoms. | VLKK Terminų bankas | ES / tarptautinė nomenklatūra | VLKK nėra klinikinis autoritetas, todėl medicininę reikšmę tikrinti kartu su klinikiniais šaltiniais. |
| vaistu_registracija_ir_produkto_informacija | Reikalinga dėl aptikto claim tipo `dose`. | VVKT registruotų vaistinių preparatų paieška; VVKT registracijos pažymėjimo priedai | EMA; ES SmPC / product information | Jei vaisto nėra LT rinkoje arba LT informacija nepakankama, pereiti į EMA / ES sluoksnį. |
| farmakologija_ir_racionalus_skyrimas | Reikalinga dėl aptikto claim tipo `dose`. | SAM racionalus vaistų skyrimas ir vartojimas; VVKT | EMA; ESC; ESMO; kitos ES specialybinės gairės | Fundamentinė farmakologija gali remtis universaliu mokslu, bet norminiai sprendimai turi eiti per LT/EU šaltinius. |
| klinikinės_metodikos_ir_specialybines_rekomendacijos | Reikalinga dėl aptikto claim tipo `algorithm_step`. | SAM metodikos ir rekomendacijos | Europos specialybinės gairės | Jei LT metodika sena ar nėra pakankama, pereiti į ES sluoksnį ir tai pažymėti research faile. |
| paramediko_kompetencija_ir_gmp | Reikalinga dėl aptikto claim tipo `algorithm_step`. | SAM; e-Seimas/TAR; Greitosios medicinos pagalbos tarnyba | ERC; specialybinės ES gairės | Pirmas norminis sluoksnis skubiajai medicinai Lietuvoje. |
| kompensavimas_ir_rinkos_prieinamumas | Reikalinga dėl aptikto claim tipo `market_availability`. | VLK kompensuojamieji vaistai; VLK kainynai | EMA | Naudoti, kai svarbu ne tik veiklioji medžiaga, bet ir paciento prieiga Lietuvoje. |

## Preliminari norminių teiginių matrica

| claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| todo-dose-01 | dose | The treatments for acute episodes of MS are those that modify the inflammatory process and immune system are used in an attempt to minimise this demyelination and this often includes administration of high-dose cortico-steroids. | keep_lt_normative | LT | VVKT registruotų vaistinių preparatų paieška; VVKT registracijos pažymėjimo priedai |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |
| todo-route-02 | route | - Impaired swallow may make the oral route of medication administration unsuitable due to increased risk of aspiration. | keep_lt_normative | LT | VVKT registruotų vaistinių preparatų paieška; VVKT registracijos pažymėjimo priedai |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |
| todo-concentration-03 | concentration | There is a subset of MND patients who are at risk of loss of hypoxic drive when high concentrations of oxygen are provided, oxygen should be administered with caution in this group. Click here for more information on a short 3 minute video clip. | keep_lt_normative | LT | VVKT registruotų vaistinių preparatų paieška; VVKT registracijos pažymėjimo priedai |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |
| todo-algorithm-step-04 | algorithm_step | Recognition is the most important factor in the management of epiglottitis. Unrecognised epiglottitis may quickly become life-threatening. | keep_lt_normative | LT | SAM metodikos ir rekomendacijos |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |
| todo-market-availability-05 | market_availability | - As clinicians we appropriately have a lower threshold for wanting to convey these clinically complex patients to hospital, however careful consideration must be given to whether this really is the best option for the patient both medically and holistically. The constantly evolving community healthcare services available may better fit the patient’s overall needs. | keep_lt_normative | LT | VLK kompensuojamieji vaistai; VLK kainynai |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |

## Preliminarūs struktūrinių blokų lokalizacijos sprendimai

- Source skyriuje automatiškai neaptikta atskirų lentelių, paveikslų, schemų ar rėmelių.

## Rankiniai veiksmai prieš draftą

- Peržiūrėkite originalo skyriaus intervalą ar šaltinio segmentus ranka ir patikslinkite, ar visi norminiai teiginiai sugaudyti.
- Jei claim lieka pagrindiniame LT tekste kaip norminis, jam būtinas konkretus LT šaltinis.
- Jei LT sluoksnio nepakanka ir tenka remtis ES, research faile užpildykite `lt_gap_reason`.
- `figure` ir `algorithm` editable šaltinis šiame repo lieka tik `Whimsical`.
- Po drafto būtinai užpildykite `## Finalus agento auditas` research faile.
