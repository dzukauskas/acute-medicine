# New Mac Setup

Šis projektas jau paruoštas taip, kad jį būtų galima perkelti į naują `Mac Mini` su švaria `macOS` instaliacija.

## Ar perėjimas iš Ventura į naujausią macOS ką nors laužo?

Iš esmės ne.

Šiam repo svarbiausi komponentai yra:

- `git`
- `python`
- `node` / `npm`
- `launchd`
- `rsync`
- `Obsidian`
- `Whimsical`
- `Codex`

Tai yra normalūs ir dabartinėse `macOS` versijose palaikomi komponentai. Didžiausia rizika čia ne `Ventura` ar naujesnė sistema, o:

- pasikeitęs vartotojo vardas ar repo kelias;
- neprisijungtas `iCloud Drive`;
- neprisijungtas `Whimsical`;
- neatkurta `Codex` aplinka ir MCP serveriai.

Praktiškai naujesnė `macOS` čia dažniau padeda negu trukdo.

## Kas persikelia automatiškai

- `Obsidian` vault, jei prisijungsi tuo pačiu `Apple ID` ir įsijungsi `iCloud Drive`.
- `Whimsical` lentos, jei prisijungsi ta pačia paskyra.
- Repo turinys, jei jį pasiklonuosi iš `GitHub`.

## Kas nepersikelia automatiškai

- `~/.codex/config.toml`
- `~/.codex/skills/`
- `LaunchAgents`
- Python virtuali aplinka `.venv`
- `gh` / `codex` login būsena

Todėl naujame Mac reikia ne kopijuoti visą seną `~/.codex`, o atkurti minimalią darbinę aplinką.

## Rekomenduojamas kelias naujame Mac

1. Prisijunk prie `Apple ID` ir palauk, kol atsiras `PARAMEDIKAS` vault.
2. Įsidiek `Homebrew`.
3. Pasiklokuok šį repo.
4. Paleisk bootstrap skriptą.
5. Prisijunk prie `Codex`, `GitHub` ir `Whimsical`.
6. Susibootstrap'ink pirmą konkrečią knygą.
7. Patikrink, kad tos knygos `Obsidian` syncas veikia.

## Rekomenduojama katalogų struktūra

Jei nori mažiausiai papildomų pakeitimų, naudok tą pačią struktūrą:

- repo: `/Users/<username>/Projects/Acute Medicine`
- vault: `/Users/<username>/Library/Mobile Documents/iCloud~md~obsidian/Documents/PARAMEDIKAS`

Jei `username` ar kelių struktūra skirsis, nieko baisaus. Sync agentą ir `Codex` MCP setupą galima sugeneruoti pagal naujus kelius.
Repo dabar remiasi tracked `repo_config.toml` defaults ir optional `repo_config.local.toml` override. `Obsidian` vault bazinį kelią ar kitus workstation-specific nustatymus keisk `repo_config.local.toml`, ne shell skriptuose.

## Vieno paleidimo bootstrap

Paleisk:

```bash
cd "/Users/<username>/Projects/Acute Medicine"
./scripts/bootstrap_macos.sh
```

Šis skriptas:

- įdiegia `Homebrew` paketus iš `Brewfile`;
- įdiegia `Codex`, jei jo dar nėra;
- sukuria `.venv`;
- įdiegia Python priklausomybes iš `requirements-dev.txt`;
- įrašo repo custom skillus į `~/.codex/skills`;
- sukonfigūruoja pagrindinius MCP serverius;
- nekuria jokio book-specific sync agento; jis diegiamas tik eksplicitiškai per `--install-obsidian-sync` arba `scripts/install_obsidian_sync_agent.sh`.

Tracked shell entrypointai šiame repo naudoja `bash`, todėl papildomo `zsh` setup nereikia nei bootstrap kelyje, nei CI.

## Po bootstrap ranka padaryk dar šiuos veiksmus

```bash
codex login
gh auth login
```

Tada:

1. Atidaryk `Whimsical.app`
2. Prisijunk prie savo `Whimsical` paskyros
3. Vieną kartą išsaugok `Whimsical` browser sesiją render skriptui:

```bash
.venv/bin/python scripts/render_whimsical_figure.py --login
```

4. Bootstrap'ink konkrečią knygą:

```bash
python3 scripts/bootstrap_book_from_pdf.py \
  --pdf "/abs/path/to/book.pdf" \
  --contents-pages 7-14 \
  --page-offset 38 \
  --backmatter-start 343
```

Jei TOC parseris nesusitvarko su nestandartiniu PDF, paleisk su chapter map sidecar:

```bash
python3 scripts/bootstrap_book_from_pdf.py \
  --pdf "/abs/path/to/book.pdf" \
  --chapter-map "/abs/path/to/book.chapters.yaml"
```

Bootstrap pagal nutylėjimą apsiriboja repo-local workspace sukūrimu. Jei tame pačiame žingsnyje norite ir per-book Obsidian sync agento, macOS aplinkoje pridėkite `--install-obsidian-sync`.

5. Jei įdiegėte sync agentą, atidaryk `Obsidian`
6. Jei įdiegėte sync agentą, patikrink, ar vault kataloge atsirado:
   - `<Book Title>/chapters/`
   - `<Book Title>/figures/`

## Repo custom skillas

Repo viduje laikomas projektinis skillas:

- `codex/skills/medical-book-localization/SKILL.md`
- `codex/skills/whimsical-diagram-export/SKILL.md`

Jis įrašomas į:

- `~/.codex/skills/medical-book-localization/SKILL.md`
- `~/.codex/skills/whimsical-diagram-export/SKILL.md`

Todėl bent šita svarbi workflow logika nebepriklauso tik nuo seno Mac.

## Obsidian sync

Repo naudoja:

- `scripts/sync_obsidian_book.sh`
- `scripts/install_obsidian_sync_agent.sh`

`install_obsidian_sync_agent.sh` yra eksplicitinis integracijos žingsnis. Jį galite kviesti tiesiogiai arba per `scripts/bootstrap_book_from_pdf.py --install-obsidian-sync` ir `scripts/bootstrap_book_from_epub.py --install-obsidian-sync`. Be šio flag'o bootstrap lieka repo-local ir nerašo globalaus `LaunchAgent`.
Pagal nutylėjimą agento label dabar vardinamas su worktree / repo identitetu, o default sync paskirtis rezervuojama owner marker'iu. Tai saugo nuo situacijos, kai tas pats book slug ar title būtų tyliai perrašytas iš kito clone ar worktree.
`sync_obsidian_book.sh` lieka portable `bash` entrypointas, o `install_obsidian_sync_agent.sh` yra macOS-specific, nes remiasi `launchd` / `launchctl`.

## Codex MCP

Pagrindiniai MCP naujame Mac atstatomi skriptu:

- `scripts/setup_codex_mcp.sh`

Jis konfigūruoja:

- `context7`
- `pdf-reader`
- `excalidraw`
- `playwright`
- `whimsical-desktop`

## Codex thread continuity

Po bootstrap naujame Mac naudok repo-level `Codex` operating modelį:

- `docs/codex-workflow.md`
- `docs/book-translation-workflow.md`
- `docs/repo-engineering-workflow.md`
- `ENGINEERING_LEDGER.md`
- `handoffs/README.md`

Jei tęsiamas repo-engineering darbas kitame `Codex` thread ar naujame worktree, pirmiausia atnaujink `ENGINEERING_LEDGER.md`:

```bash
python3 scripts/update_engineering_ledger.py \
  --theme "Current engineering theme" \
  --summary "Trumpai įvardyk, ką tiksliai reikia tęsti." \
  --next-step "Pirmas konkretus žingsnis naujam thread."
```

Normalioje porinio darbo sesijoje to neturėtų reikėti daryti ranka kiekvieną kartą, nes ledger turi atnaujinti agentas. Ši komanda yra atsarginis kelias.

Tik jei dar reikia papildomo lokalaus scratchpad, sugeneruok `handoff`:

```bash
python3 scripts/write_codex_handoff.py \
  --title "Current task handoff" \
  --book-root books/<slug> \
  --goal "Trumpai įvardyk, ką tiksliai reikia tęsti." \
  --next-step "Pirmas konkretus žingsnis naujam thread."
```

Jei reikia tik minimalaus naujo thread prompto, naudok:

```bash
python3 scripts/print_codex_resume_prompt.py --mode engineering
```

## Python priklausomybės

Šiam repo šiuo metu būtina bent:

- `Pillow`
- `playwright`
- `PyMuPDF`

Ji įrašyta į:

- `requirements-dev.txt`

Po `requirements-dev.txt` įdiegimo bootstrap skriptas papildomai įrašo ir `Chromium`, nes jis reikalingas `Whimsical` render skriptui.

PDF bootstrap šiame repo yra `PyMuPDF-first`. Praktikoje tai reiškia:

- `PyMuPDF` turi būti repo `.venv`;
- paleidus `python3 scripts/bootstrap_book_from_pdf.py ...`, skriptas pats persijungs į `.venv`, jei sistemos interpreteryje `fitz` nėra.

## Verification entrypoint

Supported repo-native smoke / contract patikra naujai mašinai:

```bash
.venv/bin/python -m unittest \
  tests.test_workflow_runtime \
  tests.test_obsidian_sync_safety \
  tests.test_end_to_end_workflow_contract
```

Tai minimali dokumentuoto bootstrap kelio verifikacija. Platesni prieš-commit rinkiniai gali būti leidžiami papildomai, bet ši komanda turi veikti be papildomo neaprašyto setup.

## Ko nerekomenduojama kopijuoti iš seno Mac

Nerekomenduoju tiesiog perkelti viso:

- `~/.codex/`

nes ten yra:

- sesijų istorija;
- SQLite state failai;
- logai;
- lokalūs cache;
- auth būsena, kuri gali būti pasenusi arba klaidinanti.

Saugesnis kelias yra:

- repo iš `GitHub`;
- `iCloud` vault iš `Apple ID`;
- prisijungimai naujame Mac;
- bootstrap skriptas.
