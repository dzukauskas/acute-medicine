# 1 skyrius. Mini chapter

- Puslapiai: 1-2
- Angliškas pagalbinis failas: source/chapters-en/001-mini.md
- Lietuviškas failas: lt/chapters/001-mini.md

## Source inventorius

### Poskyriai

- Early assessment
- Drug Tariff
- Custom UK Tool

### Lentelės

- Kol kas neužfiksuota

### Paveikslai / schemos / algoritmai

- Figure 1.1 Airway algorithm

### Rėmeliai / papildomi blokai

- Kol kas neužfiksuota

## Rizikingi terminai

- Sentinel Pathway

## Kalbinės rizikos vietos

- Išlaikyti originalo stebėjimų seką.

## Anti-calque perrašymo pastabos

- Gludinti lietuvišką sintaksę nekeičiat originalo logikos.

## Lokalizacijos sprendimai

- Drug Tariff pakeičiamas LT rinkos terminu.
- Custom UK Tool paliekamas tik originalo konteksto bloke.

## Vietos, kur originalas pakeistas pagal Lietuvos praktiką

- Drug Tariff pagrindiniame LT tekste pakeičiamas Lietuvos kompensavimo tvarkos nuoroda.

## LT-source branduolio taikymas

| Sritis | Pagrindinis LT-source kelias | Konkretus LT šaltinis | ES fallback | Pastaba |
| --- | --- | --- | --- | --- |
| rinkos prieinamumas | kompensavimas_ir_lt_rinkos_prieinamumas | VLK testinis šaltinis | EMA | Minimalus hermetiškas fixture |

## Jurisdikcijos ir rinkos signalai

| Signalas | Jurisdikcija | Tipas | Šaltinio vieta | Pastaba |
| --- | --- | --- | --- | --- |
| Drug Tariff | uk | market term | Drug Tariff | Market-specific label |
| Custom UK Tool | uk | reference tool | Custom UK Tool | Original context only |

## LT/EU pakeitimo sprendimai

| Signalas | Veiksmas | Autoritetas | LT / EU sprendimas | Šaltinio nuoroda | Pastaba |
| --- | --- | --- | --- | --- | --- |
| Drug Tariff | replace_lt | LT | Lietuvos kompensavimo tvarka | vlk-test | Replace with LT market context |
| Custom UK Tool | original_context_callout | original-context-only | Originalo kontekstas: JK orientacinis įrankis | source-book | Keep as original context |

## Vaistų ir dozių LT/EU šaltinių bazė

| Tema | Šaltinis | Jurisdikcija | Data / versija | Pastaba |
| --- | --- | --- | --- | --- |
| algorithm_step | Mini LT algoritmo atrama | LT | 2026-03-29 | Hermetiškas fixture authority source |

## Norminių teiginių matrica

| claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| claim-algorithm-1 | algorithm_step | Figure 1.1 Airway algorithm | keep_lt_normative | LT | Mini LT algoritmo atrama |  |  | Išlaikoma originalo žingsnių seka |

## Struktūrinių blokų lokalizacijos sprendimai

| block_id | block_type | lt_strategy | authority_source | original_context_allowed | note |
| --- | --- | --- | --- | --- | --- |
| algorithm-1.1-airway-algorithm | algorithm | rewrite_lt | Mini LT algoritmo atrama |  | Išlaikyti originalo žingsnių seką |

## Neperkeliamas originalo turinys

- Custom UK Tool paliekamas tik `Originalo kontekstas` bloke.

## Adjudication sprendimai

- narrative-01-early-assessment | A | Išlaikomas ištikimas vertimas be laisvo perpasakojimo.
- narrative-02-drug-tariff | hibridinis | Paliekama originalo mintis, bet rinkos terminas lokalizuojamas pagal LT sprendimą.
- narrative-03-custom-uk-tool | B | Originalo signalas rodomas tik `Originalo kontekstas` bloke.
- algorithm-1.1-airway-algorithm | hibridinis | Išlaikoma originalo seka, bet žingsniai formuluojami natūralia lietuvių kalba.

## Finalus agento auditas

| Sritis | Statusas | Pastaba |
| --- | --- | --- |
| terminija | ok |  |
| kolokacijos | ok |  |
| gramatika | ok |  |
| semantika | ok |  |
| norminė logika | ok |  |
| atviros abejonės | ok |  |
