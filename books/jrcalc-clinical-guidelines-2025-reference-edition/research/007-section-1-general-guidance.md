# 7 skyrius. Section 1 – General Guidance

- Puslapiai: EPUB segmentas `c2R8.xhtml`
- Šaltinio segmentai: `c2R8.xhtml`
- Originalo failas: `/Users/dzukauskas/Projects/Acute Medicine/books/jrcalc-clinical-guidelines-2025-reference-edition/source/epub/JRCALC Clinical Guidelines 2025 Reference Edition.epub`
- Angliškas pagalbinis failas: `/Users/dzukauskas/Projects/Acute Medicine/books/jrcalc-clinical-guidelines-2025-reference-edition/source/chapters-en/007-section-1-general-guidance.md`
- Lietuviškas failas: `/Users/dzukauskas/Projects/Acute Medicine/books/jrcalc-clinical-guidelines-2025-reference-edition/lt/chapters/007-section-1-general-guidance.md`

## Source inventorius

### Poskyriai

- Section 1 – General Guidance

### Lentelės

- Kol kas neužfiksuota

### Paveikslai / schemos / algoritmai

- Kol kas neužfiksuota

### Rėmeliai / papildomi blokai

- Kol kas neužfiksuota

## Rizikingi terminai

- General Guidance
- JRCALC

## Lietuvos šaltiniai

| Šaltinis | Tipas | Data / versija | Kodėl naudotas |
| --- | --- | --- | --- |
| VLKK Terminų bankas | terminija | žiūrėta 2026-03-29 | Bendrinei LT antraštės formuluotei ir natūraliam struktūrinės dalies pavadinimo wording'ui. |

## Europos / tarptautiniai šaltiniai

| Šaltinis | Tipas | Data / versija | Kodėl naudotas |
| --- | --- | --- | --- |
| JRCALC Clinical Guidelines 2025 Reference Edition | originalus šaltinis | 2025 leidimas | Naudotas kaip vienintelis sekcijos pavadinimo ir numeracijos šaltinis. |

## LT-source branduolio taikymas

| Sritis | Pagrindinis LT-source kelias | Konkretus LT šaltinis | ES fallback | Pastaba |
| --- | --- | --- | --- | --- |
| terminija | terminija_ir_kalbos_forma | VLKK Terminų bankas | originalus leidinys | Tai struktūrinė sekcijos antraštė be klinikinio turinio; svarbiausia natūrali LT formuluotė ir tiksli numeracija. |

## Jurisdikcijos ir rinkos signalai

| Signalas | Jurisdikcija | Tipas | Šaltinio vieta | Pastaba |
| --- | --- | --- | --- | --- |
| JRCALC | uk | gairės | `c2R8.xhtml` struktūrinis sekcijos viršelis | Signalas susijęs tik su originalo leidinio struktūra, ne su LT normine logika. |

## LT/EU pakeitimo sprendimai

| Signalas | Veiksmas | Autoritetas | LT / EU sprendimas | Šaltinio nuoroda | Pastaba |
| --- | --- | --- | --- | --- | --- |
| JRCALC | original_context_callout | original-context-only | Pagrindiniame LT tekste neakcentuoti JRCALC kaip LT norminio autoriteto; pateikti tik lokalizuotą sekcijos pavadinimą. | `shared/localization/localization_overrides.tsv`; originalus segmentas `c2R8.xhtml` | Šis skyrius yra tik struktūrinis dalies viršelis. |

## Vaistų ir dozių LT/EU šaltinių bazė

| Tema | Šaltinis | Jurisdikcija | Data / versija | Pastaba |
| --- | --- | --- | --- | --- |

## Norminių teiginių matrica

| claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Struktūrinių blokų lokalizacijos sprendimai

| block_id | block_type | lt_strategy | authority_source | original_context_allowed | note |
| --- | --- | --- | --- | --- | --- |

## Neperkeliamas originalo turinys

- Šiame segmente nėra atskiro klinikinio, norminio ar organizacinio turinio už sekcijos pavadinimo ribų.

## Adjudication sprendimai

## Lokalizacijos sprendimai

- `Section 1` lokalizuota kaip `1 dalis`, kad Obsidian ir LT skaitymo logika atitiktų knygos makrostruktūrą.
- `General Guidance` lokalizuota kaip `Bendrosios gairės`.
- Papildomo aiškinamojo teksto nepridėta, nes source segmentas yra tik struktūrinis viršelis.

## Vietos, kur originalas pakeistas pagal Lietuvos praktiką

- Struktūrinė antraštė suformuota pagal LT leidybos logiką: `1 dalis. Bendrosios gairės`, o ne pažodinis `Section 1`.

## Kalbinės rizikos vietos

- `Guidance` čia turi būti verčiama kaip struktūrinės dalies pavadinimas, ne kaip atskiras norminis dokumentas ar instrukcija.

## Anti-calque perrašymo pastabos

- Vengti pažodinės formos `Sekcija 1`.
- Nepridėti aiškinamųjų sakinių, kurių originale nėra.

## Atviros abejonės

- Kol kas neužfiksuota.

## Finalus agento auditas

| Sritis | Statusas | Pastaba |
| --- | --- | --- |
| terminija | sutvarkyta | Pavadinimas lokalizuotas kaip struktūrinė, o ne klinikinė antraštė. |
| kolokacijos | ok | Papildomos prozos nėra. |
| gramatika | ok |  |
| semantika | sutvarkyta | Išlaikyta originali sekcijos paskirtis kaip struktūrinio viršelio. |
| norminė logika | ok | Skyriuje nėra norminių klinikinių teiginių. |
| atviros abejonės | ok |  |

## Chapter pack ir review kilpa

- `research` paruoštas `chapter_pack` generavimui.
- `adjudication_pack` tikėtina nereikės, nes šaltinyje nėra konfliktiškų klinikinių blokų.

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
- [ ] Sugeneruotas `chapter_pack`
- [ ] Jei reikia, sugeneruotas `adjudication_pack`
- [ ] Jei sugeneruotas `adjudication_pack`, palikta `## Adjudication sprendimai` sekcija fiksuotu `- block_id | pasirinkimas | priežastis` formatu
- [ ] Lietuviškas skyrius parašytas nuo švaraus lapo
- [ ] Padarytas atskiras anti-calque perrašymas
- [x] Lentelės išverstos
- [x] Paveikslai / schemos atkurti lietuviškai
- [ ] Numeracija atitinka knygą
- [x] Užpildytas `Finalus agento auditas`
