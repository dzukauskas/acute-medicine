# Research checklist for 005-update-analysis-what-s-changed

- Angliškas failas: `/Users/dzukauskas/Projects/Acute Medicine/books/jrcalc-clinical-guidelines-2025-reference-edition/source/chapters-en/005-update-analysis-what-s-changed.md`
- Research failas: `/Users/dzukauskas/Projects/Acute Medicine/books/jrcalc-clinical-guidelines-2025-reference-edition/research/005-update-analysis-what-s-changed.md`
- Skyriaus tipas: `mišrus norminis / lokalizacinis`
- Aptikti norminių claim tipai: `dose, indication, monitoring, algorithm_step`
- Aptikti jurisdikciniai signalai: `JRCALC, ReSPECT, DNACPR`
- Aptikti struktūriniai blokai: `0`

## Poskyrių inventorius

- Nepavyko automatiškai nustatyti poskyrių; peržiūrėkite source ranka.

## Aptikti jurisdikciniai / rinkos signalai

| Signalas | Jurisdikcija | Tipas | Pastaba |
| --- | --- | --- | --- |
| JRCALC | uk | guideline | UK ambulance guideline source. |
| ReSPECT | uk | law | UK treatment escalation / resuscitation framework. |
| DNACPR | uk | law | UK resuscitation legal framework. |

## Rekomenduojami LT-source keliai

| Sritis | Kodėl įtraukta | Pagrindiniai LT šaltiniai | ES fallback | Pastaba |
| --- | --- | --- | --- | --- |
| terminija_ir_kalbos_forma | LT terminijai ir kolokacijoms. | VLKK Terminų bankas | ES / tarptautinė nomenklatūra | VLKK nėra klinikinis autoritetas, todėl medicininę reikšmę tikrinti kartu su klinikiniais šaltiniais. |
| vaistu_registracija_ir_produkto_informacija | Reikalinga dėl aptikto claim tipo `dose`. | VVKT registruotų vaistinių preparatų paieška; VVKT registracijos pažymėjimo priedai | EMA; ES SmPC / product information | Jei vaisto nėra LT rinkoje arba LT informacija nepakankama, pereiti į EMA / ES sluoksnį. |
| farmakologija_ir_racionalus_skyrimas | Reikalinga dėl aptikto claim tipo `dose`. | SAM racionalus vaistų skyrimas ir vartojimas; VVKT | EMA; ESC; ESMO; kitos ES specialybinės gairės | Fundamentinė farmakologija gali remtis universaliu mokslu, bet norminiai sprendimai turi eiti per LT/EU šaltinius. |
| klinikinės_metodikos_ir_specialybines_rekomendacijos | Reikalinga dėl aptikto claim tipo `monitoring`. | SAM metodikos ir rekomendacijos | Europos specialybinės gairės | Jei LT metodika sena ar nėra pakankama, pereiti į ES sluoksnį ir tai pažymėti research faile. |
| paramediko_kompetencija_ir_gmp | Reikalinga dėl aptikto claim tipo `monitoring`. | SAM; e-Seimas/TAR; Greitosios medicinos pagalbos tarnyba | ERC; specialybinės ES gairės | Pirmas norminis sluoksnis skubiajai medicinai Lietuvoje. |

## Preliminari norminių teiginių matrica

| claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| todo-dose-01 | dose | / Allergic Reactions including Anaphylaxis / September 2021 / Reviewed and updated in line with RCUK guidance. Emphasis on repeat IM adrenaline doses. / | keep_lt_normative | LT | VVKT registruotų vaistinių preparatų paieška; VVKT registracijos pažymėjimo priedai |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |
| todo-indication-02 | indication | / Hypothermia / January 2024 / Contra-indications and cautions reviewed and revised and new wording in ALS section 10.4. / | keep_lt_normative | LT | SAM racionalus vaistų skyrimas ir vartojimas; VVKT |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |
| todo-monitoring-03 | monitoring | / Acute Behavioural Disturbance (ABD) / February 2021 / Additional wording to emphasise close monitoring of a restrained patient. / | keep_lt_normative | LT | SAM metodikos ir rekomendacijos |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |
| todo-algorithm-step-04 | algorithm_step | / Intravascular Fluid Therapy in Children / May 2021 / The duration over which non-shocked patients with DKA should be given an initial 10 ml/kg bolus has been decreased to 30 minutes (was previously 60 minutes). Figure 7.3 (Intravascular Fluid Therapy in Children algorithm) has been removed for clarity. / | keep_lt_normative | LT | SAM metodikos ir rekomendacijos |  |  | Patikslinkite konkrečią LT norminio teiginio formą ir šaltinį. |

## Preliminarūs struktūrinių blokų lokalizacijos sprendimai

- Source skyriuje automatiškai neaptikta atskirų lentelių, paveikslų, schemų ar rėmelių.

## Rankiniai veiksmai prieš draftą

- Peržiūrėkite originalo skyriaus intervalą ar šaltinio segmentus ranka ir patikslinkite, ar visi norminiai teiginiai sugaudyti.
- Jei claim lieka pagrindiniame LT tekste kaip norminis, jam būtinas konkretus LT šaltinis.
- Jei LT sluoksnio nepakanka ir tenka remtis ES, research faile užpildykite `lt_gap_reason`.
- `figure` ir `algorithm` editable šaltinis šiame repo lieka tik `Whimsical`.
- Po drafto būtinai užpildykite `## Finalus agento auditas` research faile.
