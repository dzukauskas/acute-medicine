# Audit Wave 001

## Purpose

Šis failas fiksuoja `audit-wave-001` findings triage rezultatą ir rekomenduojamą įgyvendinimo seką.

## Findings

| ID | Tema | Statusas | Trumpa išvada |
| --- | --- | --- | --- |
| 1 | Canonical pack freshness yra environment-coupled per absolute paths | valid | Generatoriai ir QA lyginimas tikrai daro canonical artefaktus path-sensitive. |
| 2 | Core bootstrap ne side-effect free, nes automatiškai įdiegia globalų Obsidian/launchd sync | valid | PDF ir EPUB bootstrap abu unconditionally kviečia sync install sluoksnį. |
| 3 | Repo neturi vieno visiškai vienareikšmio localization default | partial | Book workflow jau yra LT/EU-first, bet `AGENTS.md` formuluotė dar palieka dviprasmybę. |
| 4 | Workstation-local config ir path prielaidos vis dar tracked kaip shared truth | valid | Runtime remiasi tracked `repo_config.toml`, o docs ir dalis artefaktų vis dar neša lokalios mašinos kelių tiesą. |
| 5 | Dokumentuotas bootstrap kelias neprovisionina aiškiai repo-defined test environment, CI nematyti | partial | CI ir dev packaging nematyti, bet `.venv` + `requirements.txt` jau sudaro bazinę repo-native vykdymo terpę. |
| 6 | Testai stipriausi saugiausiose vietose, o trapiausios vietos labiau stub'intos | partial | Riskas realus, bet repo jau turi ir realių acceptance/contract testų sluoksnį. |
| 7 | Kritiniuose subprocess keliuose nėra timeout | valid | Patikrintuose skriptuose `subprocess.run(...)` kviečiamas be `timeout`. |
| 8 | LaunchAgent ir default Obsidian destination gali koliduoti tarp worktree/clone to paties book | valid | Label ir default destination vardinami tik iš book slug/title, todėl globali būsena gali konfliktuoti. |

## Recommended Waves

### First Implementation Wave

1. Finding `1`
2. Finding `2`
3. Finding `7`
4. Findings `4` ir `8` kaip vienas bendras global-state / config sluoksnis

### Later Wave

- Finding `3`
- Finding `5`
- Finding `6`

## Notes

- Šiame etape klasifikacija laikoma pakankamai stabilia pereiti iš findings validavimo į įgyvendinimo planavimą.
- Pirmas implementacijos tikslas yra environment-agnostic canonical artefaktai, kad QA freshness vartai nebebūtų host-path sensitive.
