# 1 skyrius. Chart chapter

- Puslapiai: 1-2
- Angliškas pagalbinis failas: source/chapters-en/001-chart.md
- Lietuviškas failas: lt/chapters/001-chart.md

## Source inventorius

### Poskyriai

- Alerts

### Lentelės

- Kol kas neužfiksuota

### Paveikslai / schemos / algoritmai

- Chart 1.1 NEWS2 admission trend
- Chart 1.2 NEWS2 escalation trend

### Rėmeliai / papildomi blokai

- Kol kas neužfiksuota

## Rizikingi terminai

- 

## Kalbinės rizikos vietos

- Abi NEWS2 diagramos turi būti sujungtos po vienu originalo konteksto paaiškinimu.

## Anti-calque perrašymo pastabos

- Išlaikyti originalo orientacinę funkciją, bet neperteikti NEWS2 kaip vietinio standarto.

## Lokalizacijos sprendimai

- NEWS2 diagramos pagrindiniame LT tekste aptariamos tik kaip originalo kontekstas.

## Vietos, kur originalas pakeistas pagal Lietuvos praktiką

- NEWS2 nenurodomas kaip Lietuvos standartas.

## LT-source branduolio taikymas

| Sritis | Pagrindinis LT-source kelias | Konkretus LT šaltinis | ES fallback | Pastaba |
| --- | --- | --- | --- | --- |
| monitoring_context | stebejimo_sistemos_ir_originalo_kontekstas | Mini LT monitoring atrama | ES bendros rekomendacijos | Hermetiškas fixture |

## Jurisdikcijos ir rinkos signalai

| Signalas | Jurisdikcija | Tipas | Šaltinio vieta | Pastaba |
| --- | --- | --- | --- | --- |
| NEWS2 | uk | guideline | Chart 1.1 NEWS2 admission trend | UK early warning score |

## LT/EU pakeitimo sprendimai

| Signalas | Veiksmas | Autoritetas | LT / EU sprendimas | Šaltinio nuoroda | Pastaba |
| --- | --- | --- | --- | --- | --- |
| NEWS2 | original_context_callout | original-context-only | Originalo kontekstas: NEWS2 paliekamas tik kaip JK sistemos nuoroda. | sam-test | Naudoti tik originalo kontekste. |

## Vaistų ir dozių LT/EU šaltinių bazė

| Tema | Šaltinis | Jurisdikcija | Data / versija | Pastaba |
| --- | --- | --- | --- | --- |

## Norminių teiginių matrica

| claim_id | claim_type | source_anchor | final_rendering | authority_basis | primary_lt_source | eu_fallback_source | lt_gap_reason | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Struktūrinių blokų lokalizacijos sprendimai

| block_id | block_type | lt_strategy | authority_source | original_context_allowed | note |
| --- | --- | --- | --- | --- | --- |
| chart-1.1-news2-admission-trend | chart | original_context_callout |  | yes | Abi diagramos jungiamos po vienu originalo konteksto bloku. |
| chart-1.2-news2-escalation-trend | chart | original_context_callout |  | yes | Abi diagramos jungiamos po vienu originalo konteksto bloku. |

## Neperkeliamas originalo turinys

- NEWS2 paliekamas tik `Originalo kontekstas` bloke.

## Adjudication sprendimai

- chart-1.1-news2-admission-trend | hibridinis | Diagrama paliekama tik kaip originalo kontekstas.
- chart-1.2-news2-escalation-trend | hibridinis | Diagrama paliekama tik kaip originalo kontekstas.

## Finalus agento auditas

| Sritis | Statusas | Pastaba |
| --- | --- | --- |
| terminija | ok |  |
| kolokacijos | ok |  |
| gramatika | ok |  |
| semantika | ok |  |
| norminė logika | ok |  |
| atviros abejonės | ok |  |
