# Vertimo Stiliaus Taisyklės

Šių taisyklių laikykis kiekvienam naujam skyriaus vertimui.

## Pagrindinė taisyklė

Versk sąvoką, o ne angliško sakinio formą.

Jei sakinys skamba kaip vertimas, jį reikia perrašyti tol, kol jis skambės kaip natūrali lietuviška medicininė proza.

## Nekeičiamos taisyklės

- Pirmenybę teik nusistovėjusiai lietuviškai medicinos terminijai, o ne į anglų kalbą panašioms kalkėms.
- Palik kliniškai nusistovėjusius terminus, pvz. `hipoksemija`, `perfuzija`, `stridoras`, jei jie tikrai vartojami lietuviškoje medicinoje.
- Nepalik pažodinių frazių vien todėl, kad kiekvienas žodis atskirai yra „teisingas“.
- Ilgas angliškas sakinių grandines skaidyk į trumpesnius lietuviškus sakinius, jei taip tekstas tampa aiškesnis.
- Venk daiktavardinių biurokratinių konstrukcijų ten, kur lietuviškai geriau veikia tiesioginis veiksmažodis.
- Jungtinės Karalystės pareigybes ar sistemos žymas adaptuok į aiškų lietuvišką aprašą, jei nėra tiesioginio vietinio atitikmens.
- Formaliame medicininiame tekste venk šnekamųjų formuluočių, pvz. `To išvengsi`, nebent visas tekstas sąmoningai rašomas instrukciniu tonu.

## LT/EU lokalizacija

- Pagrindinis standartas yra Lietuvos / ES medicininė rašysena, ne JK formos.
- Dešimtainiams skaičiams naudok kablelį, pvz. `4,0 mmol/L`, `35,0 °C`, `0,05 mikrogramo/kg/min.`.
- Išlaikyk Lietuvoje įprastus vienetus kaip pagrindinius: `mmHg`, `kPa`, `mmol/L`, `g/L`, `mL`, `°C`, `mikrogramai`.
- Jei šaltinyje pateikiami keli vienetai, pirmą pateik Lietuvoje / ES įprastą formą, o alternatyvų vienetą gali palikti skliaustuose, jei jis padeda suprasti tekstą.
- Vaistų vartojimo kelią prozoje pirmą kartą išrašyk lietuviškai, o jei reikia santrumpos, rinkis Lietuvoje įprastą formą: `į veną (į/v.)`, `į raumenis (į/r.)`.
- Poodiniam skyrimui pagrindiniame tekste teik pirmenybę pilnai formai `po oda` arba `į poodį`; `s/c.` naudok tik jei ji būtina lentelėje ar šaltinis pats taip pateikia.
- Angliškų vartojimo kelių santrumpų, pvz. `IV`, `IM`, `SC`, `IO`, lietuviškame pagrindiniame tekste nepalik.
- JK vidaus sistemos elementų, pvz. `2222`, `NHS`, `ReSPECT`, `DNACPR`, `NEWS2`, negalima palikti kaip universalaus standarto. Pagrindiniame tekste juos lokalizuok arba aiškiai pažymėk, kad tai JK kontekstas.
- Bibliografijoje ir oficialių dokumentų pavadinimuose originalių pavadinimų nelokalizuok.

## Trumpinių politika

- Jei Lietuvoje yra aiškiai nusistovėjęs lietuviškas trumpinys, vartok jį: pvz. `SV`, `GKS`, `VAS`, `AID`, `PKI`, `EKMO`, `CVS`, `į/v.`, `į/r.`.
- Jei lietuviško trumpinio nėra arba jis nėra aiškiai nusistovėjęs, pagrindiniame tekste teik pirmenybę pilnam lietuviškam terminui, o tarptautinį trumpinį gali paminėti tik pirmą kartą aiškinamojoje vietoje.
- Procedūrų ir fiziologijos atmintinės, pvz. `ABCDE`, `DRS ABC`, gali būti paliekamos originalia forma, jei jos tuoj pat paaiškinamos tekste.
- Tarptautinius rodiklius ar technologijų trumpinius, kurie realiai vartojami ir Lietuvoje, pvz. `SpO2`, `PaO2`, `CPAP`, galima palikti, bet pirmą kartą jie turi būti aiškiai paaiškinti.
- Oficialių užsienio dokumentų ir organizacijų pavadinimų trumpinių, pvz. `RCUK`, `NHS`, `NCAA`, `ReSPECT`, `DNACPR`, nekeisk, nes tai yra tikriniai vardai, o ne lokalūs klinikiniai trumpiniai.

## Dažniausi rizikos požymiai

Tai ženklai, kad sakinį dar reikia perrašyti:

- angliška loginė jungtis perkelta į lietuvišką sakinio tvarką
- pareigybės pavadinimas išverstas žodis į žodį iš UK ligoninės hierarchijos
- prietaiso ar procedūros aprašas skamba techniškai, bet nelietuviškai
- pavartotas veiksmažodis tinka kraujo produktams, bet netinka skysčiams, arba atvirkščiai
- skalė ar slenkstis išreikštas palyginamuoju būdu, nors lietuviškai geriau tiesiai įvardyti klinikinę ribą

## Privalomas darbo procesas

Prieš versdamas skyrių:

1. Išsitrauk 15-30 rizikingiausių medicininių terminų.
2. Patikrink juos pagal [source-priority.md](/Users/dzukauskas/Projects/Acute%20Medicine/study/source-priority.md).
3. Įrašyk patvirtintus arba pasirinktus variantus į `study/termbase.tsv`.
4. Aiškiai blogas kalkes įrašyk į `study/disallowed_terms.tsv` arba `study/disallowed_phrases.tsv`.

Prieš laikydamas skyrių baigtu:

1. Kartą perskaityk visą skyrių tik dėl lietuviško skambesio, o ne dėl terminų.
2. Perrašyk visus sakinius, kurie vis dar skamba kaip vertimas.
3. Padaryk trumpą studento aiškumo perėjimą ir ten, kur reikia, įterpk trumpas `Studijų pastaba` žymes pačiame tekste.
4. Paleisk:

```bash
.venv/bin/python scripts/terminology_guard.py
```

5. Skyrius nelaikomas baigtu, kol guard'as negrįžta švarus.

Jei skyriuje yra svarbus paveikslas ar algoritmas, bet OCR jo neištraukė:

1. Nepalik vien tuščios antraštės ar vienos eilutės su šaltiniu.
2. Jei mokymosi medžiaga skirta `Obsidian` ar kitai `Markdown` skaityklei su `Mermaid` palaikymu, pirmenybę teik `mermaid` blokui pačiame `.md` faile.
3. Po ta pačia antrašte papildomai palik lietuvišką tekstinę schemą arba aiškų algoritminį santraukos bloką kaip atsarginį variantą.
4. Schema turi būti pakankama mokymuisi net ir nežiūrint į originalų paveikslą.
5. Aiškiai pažymėk, kad tai yra lietuviškai perkurta mokymosi versija pagal originalų šaltinį.

## Jei randama nauja kalkė

Iš karto padaryk visus tris veiksmus:

1. Pataisyk skyriaus tekstą.
2. Įrašyk blogą formą į draudžiamų taisyklių failą.
3. Jei tai kartotinas terminas ar frazė, įrašyk gerą variantą į `study/termbase.tsv`.
