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
6. Patikrink, kad `Obsidian` syncas veikia.

## Rekomenduojama katalogų struktūra

Jei nori mažiausiai papildomų pakeitimų, naudok tą pačią struktūrą:

- repo: `/Users/<username>/Projects/Acute Medicine`
- vault: `/Users/<username>/Library/Mobile Documents/iCloud~md~obsidian/Documents/PARAMEDIKAS`

Jei `username` ar kelių struktūra skirsis, nieko baisaus. Sync agentą ir `Codex` MCP setupą galima sugeneruoti pagal naujus kelius.

## Vieno paleidimo bootstrap

Paleisk:

```bash
cd "/Users/<username>/Projects/Acute Medicine"
./scripts/bootstrap_macos.sh "/Users/<username>/Library/Mobile Documents/iCloud~md~obsidian/Documents/PARAMEDIKAS/Acute Medicine"
```

Šis skriptas:

- įdiegia `Homebrew` paketus iš `Brewfile`;
- įdiegia `Codex`, jei jo dar nėra;
- sukuria `.venv`;
- įdiegia Python priklausomybes iš `requirements.txt`;
- įrašo repo custom skillus į `~/.codex/skills`;
- sukonfigūruoja pagrindinius MCP serverius;
- įdiegia `Obsidian` sync agentą, jei perduotas vault kelias.

## Po bootstrap ranka padaryk dar šiuos veiksmus

```bash
codex login
gh auth login
```

Tada:

1. Atidaryk `Whimsical.app`
2. Prisijunk prie savo `Whimsical` paskyros
3. Atidaryk `Obsidian`
4. Patikrink, ar vault kataloge atsirado:
   - `Acute Medicine/chapters/`
   - `Acute Medicine/figures/`

## Repo custom skillas

Repo viduje laikomas projektinis skillas:

- `codex/skills/medical-book-localization/SKILL.md`

Jis įrašomas į:

- `~/.codex/skills/medical-book-localization/SKILL.md`

Todėl bent šita svarbi workflow logika nebepriklauso tik nuo seno Mac.

## Obsidian sync

Repo naudoja:

- `scripts/sync_obsidian_acute_medicine.sh`
- `scripts/install_obsidian_sync_agent.sh`

`install_obsidian_sync_agent.sh` sugeneruoja `LaunchAgent` pagal dabartinio kompiuterio kelius. Tai svarbu, nes `plist` failai su hardcoded keliais nėra patikimi tarp skirtingų Mac.

## Codex MCP

Pagrindiniai MCP naujame Mac atstatomi skriptu:

- `scripts/setup_codex_mcp.sh`

Jis konfigūruoja:

- `context7`
- `pdf-reader`
- `excalidraw`
- `playwright`
- `whimsical-desktop`

## Python priklausomybės

Šiam repo šiuo metu būtina bent:

- `PyMuPDF`

Ji įrašyta į:

- `requirements.txt`

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
