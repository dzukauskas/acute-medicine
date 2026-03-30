# 1 skyrius. Disclaimer

- Puslapiai: EPUB segmentas `c76.xhtml`
- Šaltinio segmentai: `c76.xhtml`
- Originalo failas: `source/epub/JRCALC Clinical Guidelines 2025 Reference Edition.epub`
- Angliškas pagalbinis failas: `source/chapters-en/001-disclaimer.md`
- Lietuviškas failas: `lt/chapters/001-disclaimer.md`

## Source inventorius

### Poskyriai

- Disclaimer
- Using these Guidelines

### Lentelės

- Kol kas neužfiksuota

### Paveikslai / schemos / algoritmai

- Kol kas neužfiksuota

### Rėmeliai / papildomi blokai

- Kol kas neužfiksuota

## Rizikingi terminai

- JRCALC
- NICE
- NHS
- advisory guidelines
- clinical judgement
- patient care record
- local clinical committees
- woman / women / mother vartosena ginekologinių ir nėštumo būklių kontekste

## Lietuvos šaltiniai

| Šaltinis | Tipas | Data / versija | Kodėl naudotas |
| --- | --- | --- | --- |
| Lietuvos medicinos norma MN 135:2019 „Paramedikas“ | medicinos norma | galiojanti suvestinė redakcija nuo 2024-01-23 | Paramediko kompetencijos, pareigų ir profesinės atsakomybės riboms lokalizuoti. |
| Lietuvos medicinos norma MN 167:2019 „Skubiosios medicinos pagalbos paramedikas“ | medicinos norma | galiojanti suvestinė redakcija nuo 2024-01-23 | GMP paramediko teisių, pareigų ir kompetencijos riboms bei klinikinio sprendimo atsakomybei lokalizuoti. |
| SAM įsakymas Nr. V-1234 „Dėl Kortelės Nr. 110/a „Greitosios medicinos pagalbos kvietimo kortelė“ duomenų sąrašo ir jos pildymo, pateikimo ir tikslinimo taisyklių patvirtinimo“ | dokumentavimo taisyklės | suvestinė redakcija nuo 2026-01-01 | Reikalavimui dokumentuoti klinikinius sprendimus ir nukrypimų priežastis paciento priežiūros dokumentuose. |
| SAM įsakymas Nr. V-1131 „Dėl Greitosios medicinos pagalbos paslaugų teikimo išlaidų apmokėjimo tvarkos aprašo patvirtinimo“ | GMP organizavimo aprašas | galiojanti suvestinė redakcija nuo 2025-11-27 | LT GMP organizacinio konteksto atskyrimui nuo JK NHS sistemos. |

## Europos / tarptautiniai šaltiniai

| Šaltinis | Tipas | Data / versija | Kodėl naudotas |
| --- | --- | --- | --- |
| JRCALC Clinical Guidelines 2025 Reference Edition | originalus šaltinis | 2025 leidimas | Naudotas originalo disclaimer struktūrai ir JK institucinio konteksto identifikavimui. |

## LT-source branduolio taikymas

| Sritis | Pagrindinis LT-source kelias | Konkretus LT šaltinis | ES fallback | Pastaba |
| --- | --- | --- | --- | --- |
| terminija | terminija_ir_kalbos_forma | VLKK Terminų bankas; LT medicininė mokomoji vartosena | tarptautinė nomenklatūra | Naudota terminams `klinikinis sprendimas`, `paciento priežiūros dokumentai`, `kompetencija`. |
| kompetencija_ir_gmp | paramediko_kompetencija_ir_gmp | MN 135:2019 „Paramedikas“; MN 167:2019 „Skubiosios medicinos pagalbos paramedikas“ | ERC / ES gairės, jei reikėtų klinikinių algoritmų | Šiame skyriuje aktualus bendras profesinės kompetencijos ir atsakomybės principas, ne JK ambulance service vidaus tvarka. |
| dokumentavimas_ir_teise | teise_ir_reguliavimas | SAM įsakymas Nr. V-1234 dėl Kortelės Nr. 110/a; MN 167:2019 | EUR-Lex / ES bendrieji pacientų saugos principai | Naudota teiginiui, kad klinikiniai sprendimai ir nukrypimų priežastys turi būti dokumentuojami. |
| organizacinis_kontekstas | paramediko_kompetencija_ir_gmp | SAM įsakymas Nr. V-1131 dėl GMP paslaugų teikimo išlaidų apmokėjimo tvarkos aprašo | ES ikihospitalinės pagalbos gairės | Naudota atskirti LT GMP organizacinę logiką nuo originalo NHS konteksto. |

## Jurisdikcijos ir rinkos signalai

| Signalas | Jurisdikcija | Tipas | Šaltinio vieta | Pastaba |
| --- | --- | --- | --- | --- |
| JRCALC | uk | gairės | `c76.xhtml` pirmas, antras ir paskutinis pastraipų blokai | Originalo JK paramedikų gairių sistema; LT tekste negali būti palikta kaip norminis autoritetas. |
| NHS | uk | service model | `c76.xhtml` antra ir penkta pastraipos | JK sveikatos sistemos ir ambulance service organizacinis kontekstas. |
| NICE | uk | gairės | `c76.xhtml` antra pastraipa | Originale minimos NICE gairės skirtos NHS England kontekstui. |

## LT/EU pakeitimo sprendimai

| Signalas | Veiksmas | Autoritetas | LT / EU sprendimas | Šaltinio nuoroda | Pastaba |
| --- | --- | --- | --- | --- | --- |
| JRCALC | original_context_callout | original-context-only | Pagrindiniame LT tekste nevartoti kaip norminio autoriteto; palikti tik `Originalo kontekstas` bloke. | `shared/localization/localization_overrides.tsv` (`JRCALC`); originalus skyrius `c76.xhtml` | Disclaimer taikomas konkrečiam JK leidiniui. |
| NHS | omit_nontransferable | original-context-only | Pagrindiniame LT tekste pakeisti į bendrą LT GMP organizacinį kontekstą; NHS palikti tik aiškinamajame bloke. | `shared/localization/localization_overrides.tsv` (`NHS`); SAM įsakymas Nr. V-1131 | NHS nėra LT norminė sistema. |
| NICE | original_context_callout | original-context-only | NICE minima tik kaip originalo leidinyje naudotas šaltinis; LT norminiam tekstui neperkeliama. | originalus skyrius `c76.xhtml` | NICE turinys originale nurodomas kaip nepatikrintas dėl atkartojimo tikslumo šiame leidinyje. |

## Vaistų ir dozių LT/EU šaltinių bazė

| Tema | Šaltinis | Jurisdikcija | Data / versija | Pastaba |
| --- | --- | --- | --- | --- |
| algorithm_step | MN 167:2019 „Skubiosios medicinos pagalbos paramedikas“; MN 135:2019 „Paramedikas“ | LT | galiojančios suvestinės redakcijos nuo 2024-01-23 | Naudota tik bendram principui, kad rekomendacijos nepakeičia profesinės kompetencijos ir klinikinio sprendimo. |
| legal_scope | SAM įsakymas Nr. V-1234 dėl Kortelės Nr. 110/a; MN 167:2019 | LT | suvestinė redakcija nuo 2026-01-01; galiojanti suvestinė redakcija nuo 2024-01-23 | Dokumentavimo ir profesinės atsakomybės principui. |
| market_availability | SAM įsakymas Nr. V-1131 dėl GMP paslaugų teikimo išlaidų apmokėjimo tvarkos aprašo | LT | galiojanti suvestinė redakcija nuo 2025-11-27 | Naudota atskirti LT GMP organizacinį modelį nuo teiginio apie JK prieinamas paramedikų intervencijas. |

## Norminių teiginių matrica

| claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| claim-001-competence | algorithm_step | Using these Guidelines | keep_lt_normative | LT | MN 167:2019; MN 135:2019 |  |  | LT tekste paliekamas bendras principas, kad rekomendacijos nepakeičia klinikinio sprendimo ir taikomos tik turint atitinkamą kompetenciją. |
| claim-002-documentation | legal_scope | Using these Guidelines | keep_lt_normative | LT | SAM įsakymas Nr. V-1234 dėl Kortelės Nr. 110/a; MN 167:2019 |  |  | LT tekste paliekamas dokumentavimo ir profesinės atsakomybės principas, be JK sistemos institucinių nuorodų. |
| claim-003-uk-availability | market_availability | Using these Guidelines | original_context_callout | original-context-only |  |  |  | Tai JK rinkos ir organizacinės aprėpties teiginys; LT tekste rodomas tik kaip originalo kontekstas, ne kaip LT norminis standartas. |

## Struktūrinių blokų lokalizacijos sprendimai

| block_id | block_type | lt_strategy | authority_source | original_context_allowed | note |
| --- | --- | --- | --- | --- | --- |

## Neperkeliamas originalo turinys

- JK institucinis derinys `Association of Ambulance Chief Executives`, `JRCALC`, `NICE`, `NHS England` LT tekste nepaliekamas kaip norminis autoritetas.
- Teiginys, kad gairės universaliai taikomos `NHS ambulance services`, neperkeliama kaip Lietuvos sistemos standartas.
- Nuoroda, kad naujausias turinys skelbiamas `JRCALC apps`, rodoma tik kaip originalo leidinio pastaba.

## Adjudication sprendimai

- narrative-01-disclaimer | hibridinis | Pagrindiniame bloke palikta tiksli atsakomybės logika, bet sakinynas sutrumpintas ir perrašytas į natūralesnę LT disclaimer formą.
- narrative-02-using-these-guidelines | hibridinis | Sujungta norminė aiškumo logika ir aiškus `Originalo kontekstas` atskyrimas, kad JK signalai neliktų tariamu LT standartu.

## Lokalizacijos sprendimai

- Pagrindinis LT tekstas perrašomas kaip bendras naudojimo ir atsakomybės ribojimo skyrius, be JK institucijų norminio svorio.
- JK-specific terminai ir organizaciniai modeliai perkeliami į atskirą `Originalo kontekstas` bloką.
- Teiginys apie dokumentavimą paliekamas pagrindiniame LT tekste, nes jis turi aiškų LT norminį atitikmenį.

## Vietos, kur originalas pakeistas pagal Lietuvos praktiką

- `NHS ambulance services` pakeista į bendrą LT GMP organizacinį kontekstą.
- `patient care record` konkretinta kaip `paciento priežiūros dokumentai`.

## Kalbinės rizikos vietos

- `advisory` nepalikti kaip pažodinio `advisory guidelines`; rašyti `konsultacinio pobūdžio rekomendacijos`.
- `sound clinical judgement` neversti pažodžiui kaip `garsus klinikinis sprendimas`; rinktis `klinikinis sprendimas` arba `profesinis klinikinis vertinimas`.
- `variation from standard clinical practice` perrašyti natūraliai, vengiant biurokratinio sakinio karkaso.

## Anti-calque perrašymo pastabos

- Vengti pažodinių karkasų `sprendimų priėmimo procesui paremti` ir `užtikrinti tinkamą interpretaciją`; rinktis trumpesnes LT medicininės kalbos formas.
- Ilgas disclaimer pastraipas skaidyti į trumpesnius informacinius vienetus.
- UK institucines nuorodas iškelti iš pagrindinės prozos, kad LT tekstas neskambėtų kaip vertimas iš JK vidaus dokumento.

## Atviros abejonės

- Kol kas neužfiksuota.

## Finalus agento auditas

| Sritis | Statusas | Pastaba |
| --- | --- | --- |
| terminija | sutvarkyta | JK signalai atskirti nuo LT norminio teksto. |
| kolokacijos | sutvarkyta | Disclaimer perrašytas į natūralesnes LT naudojimo ir atsakomybės formuluotes. |
| gramatika | ok |  |
| semantika | sutvarkyta | Atskirta, kas lieka bendru principu, o kas tik originalo kontekstu. |
| norminė logika | sutvarkyta | Kompetencijos ir dokumentavimo teiginiai paremti LT norminiu sluoksniu. |
| atviros abejonės | ok |  |

## Chapter pack ir review kilpa

- Sugeneruotas `chapter_packs/001-disclaimer.yaml`.
- Sugeneruotas `adjudication_packs/001-disclaimer.yaml`.
- Abiem narrative blokams pasirinktas `hibridinis` sprendimas: išlaikyta disclaimer logika, bet proza perrašyta į natūralesnį LT naudojimo tekstą.

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
- [x] Sugeneruotas `chapter_pack`
- [x] Jei reikia, sugeneruotas `adjudication_pack`
- [x] Jei sugeneruotas `adjudication_pack`, palikta `## Adjudication sprendimai` sekcija fiksuotu `- block_id | pasirinkimas | priežastis` formatu
- [x] Lietuviškas skyrius parašytas nuo švaraus lapo
- [x] Padarytas atskiras anti-calque perrašymas
- [x] Lentelės išverstos
- [x] Paveikslai / schemos atkurti lietuviškai
- [x] Numeracija atitinka knygą
- [x] Užpildytas `Finalus agento auditas`
