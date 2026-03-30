# Audit Wave 002

## Purpose

Šis failas fiksuoja `audit-wave-002` findings triage rezultatą ir rekomenduojamą įgyvendinimo seką.

## Findings

| ID | Tema | Statusas | Trumpa išvada |
| --- | --- | --- | --- |
| 1 | Template-managed book docs stale ir iš naujo atidaro localization contract drift | valid | `always_refresh` policy failai ir tracked JRCALC kopijos išsiskyrusios ne kosmetiškai, todėl operator contract drift realus. |
| 2 | Bootstrap ir refresh naudoja skirtingą template materialization kontraktą | partial | Struktūrinė skola reali, bet dabartinis live-break claim nepasitvirtino, nes required scaffold katalogai šiame checkout'e yra tracked. |
| 3 | Canonical source kind/name inferinamas iš live filesystem, ne iš tracked metadata | valid | Refresh remiasi source failų buvimu ir hard-prefer'ina PDF, todėl canonical source truth nėra deklaruota. |
| 4 | Focused CI nemato template-managed book parity invarianto | valid | CI gali būti žalias net esant realiam template/book drift, nes nėra bendro parity testo per tracked books. |
| 5 | Shell entrypointai išlieka environment-bound | valid | Paliekama vėlesnei portability / docs clarity bangai. |
| 6 | `AGENTS.md` vis dar neša workstation-specific absoliučius repo kelius | valid | Paliekama vėlesnei portability / docs clarity bangai. |
| 7 | Continuity model remiasi neegzistuojančiu `handoffs/README.md` | invalid | Failas repo egzistuoja ir yra tracked, todėl claim nepasitvirtino. |

## Recommended Waves

### First Implementation Wave

1. Findings `1`, `3` ir `4` kaip vienas bendras `template-contract hardening` branduolys
2. Finding `2` kaip partial to paties kontrakto simptomas, ne atskira nepriklausoma banga

### Later Wave

- Findings `5` ir `6` kaip atskiras portability / docs clarity sluoksnis

## Implementation Progress

- Planning phase: tracked planas sukurtas, o `ENGINEERING_LEDGER.md` perjungtas į `audit-wave-002 planning`.
- First wave: planned.
- Later wave (`5/6`): planned.

## Notes

- Šiame etape klasifikacija laikoma pakankamai stabilia pereiti iš findings validavimo į planavimo ir suskaidytos įgyvendinimo sekos fazę.
- Pirmos bangos tikslas yra vienas shared template kontraktas tarp bootstrap, refresh, tracked metadata ir CI parity vartų.
- `book_metadata.yaml` pirmoje bangoje tampa vieninteliu deklaruotu canonical source truth sluoksniu book lygmenyje.
- Nepakartotas `tests.test_completeness_guard...` signalas nelaikomas `audit-wave-002` planning faktu ir į šios bangos scope neįtraukiamas.
