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
| 5 | Shell entrypointai išlieka environment-bound | valid | Uždaryta antroje bangoje per vieningą `bash` kontraktą, focused smoke guard'us ir CI be specialaus `zsh` provisioning. |
| 6 | `AGENTS.md` vis dar neša workstation-specific absoliučius repo kelius | valid | Uždaryta antroje bangoje per repo-relative binding references ir docs portability kontrakto testą. |
| 7 | Continuity model remiasi neegzistuojančiu `handoffs/README.md` | invalid | Failas repo egzistuoja ir yra tracked, todėl claim nepasitvirtino. |

## Recommended Waves

### First Implementation Wave

1. Findings `1`, `3` ir `4` kaip vienas bendras `template-contract hardening` branduolys
2. Finding `2` kaip partial to paties kontrakto simptomas, ne atskira nepriklausoma banga

### Later Wave

- Findings `5` ir `6` kaip atskiras portability / docs clarity sluoksnis

## Implementation Progress

- Planning phase: completed in `27bed05` (`Plan audit wave 002`).
- First wave helper/metadata contract: completed in `18ddbb0` (`Add shared book template helper`).
- First wave bootstrap/refresh wiring: completed in `3281812` (`Wire book template contract into bootstrap and refresh`).
- First wave JRCALC backfill: completed in `098aa3d` (`Backfill JRCALC template-managed docs`).
- First wave parity gate + focused CI: completed in `afefb9f` (`Add book template parity gate`).
- First wave (`template-contract hardening`): completed.
- Later wave shell contract: completed in `577fe81` (`Standardize shell entrypoints on bash`).
- Later wave docs/AGENTS clarity: completed in `b29f3a0` (`Clarify portability contract in docs and AGENTS`).
- Later wave (`5/6`): completed.

## Notes

- Pirmos bangos tikslas buvo vienas shared template kontraktas tarp bootstrap, refresh, tracked metadata ir CI parity vartų; ši banga uždaryta.
- `book_metadata.yaml` pirmoje bangoje tampa vieninteliu deklaruotu canonical source truth sluoksniu book lygmenyje.
- Nepakartotas `tests.test_completeness_guard...` signalas nelaikomas `audit-wave-002` planning faktu ir į šios bangos scope neįtraukiamas.
- Antroji banga sąmoningai sprendė tik `5/6` portability / docs clarity sluoksnį ir nebejudino pirmos bangos template kontrakto.
- Shell portability šioje bangoje sąmoningai standartizuota per vieningą `bash` kontraktą; pilna POSIX shell refaktorizacija į scope neįtraukta.
