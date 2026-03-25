# Books

Repo yra book-agnostic: kiekviena nauja knyga bootstrap'inama į atskirą `books/<slug>/` katalogą, o bendras shared šaltinis laikomas tik `books/_template/`.

## Repo standartas

- pagrindinis LT tekstas rašomas Lietuvos / ES logika;
- UK, Australijos, JAV ar kitas originalo rinkos kontekstas negali likti pagrindiniame LT tekste kaip tariamas vietinis standartas;
- jei originalo kontekstą verta parodyti, jis leidžiamas tik aiškiai pažymėtame `Originalo kontekstas` bloke;
- vaistų pavadinimai pagrindiniame LT tekste pagal nutylėjimą yra bendriniai / INN, o dozės, vartojimo keliai ir indikacijos remiami LT, o jei jų nepakanka, ES šaltiniais.

Shared LT-source branduolys laikomas:

- `books/_template/source-priority.md`
- `books/_template/lt_source_map.tsv`

## Ką laikome `books/`

```text
books/
  _template/
  <book-slug>/
```

- `books/_template/` yra vienintelis shared bootstrap ir refresh šaltinis.
- `books/<book-slug>/` yra pilnai self-contained vienos knygos darbo vieta.

## Naujos knygos bootstrap

Kanoninis entrypoint:

```bash
python3 scripts/bootstrap_book_from_pdf.py \
  --pdf "/abs/path/to/book.pdf" \
  --contents-pages 7-14 \
  --page-offset 38 \
  --backmatter-start 343
```

Jei PDF turinys nestandartinis, naudokite chapter map sidecar:

```bash
python3 scripts/bootstrap_book_from_pdf.py \
  --pdf "/abs/path/to/book.pdf" \
  --chapter-map "/abs/path/to/book.chapters.yaml"
```

Ši komanda:

- išveda pavadinimą ir slug iš PDF;
- sukuria `books/<slug>/`;
- nukopijuoja PDF į `source/pdf/`;
- nukopijuoja pilną `books/_template/`;
- sugeneruoja `source/index/` ir `source/chapters-en/`;
- automatiškai sukonfigūruoja Obsidian sync pagal `repo_config.toml` default'us, pvz. `PARAMEDIKAS/<Book Title>`.

Jei šalia PDF yra `<pdf-stem>.chapters.yaml`, bootstrap jį pasiims automatiškai ir nebandys spėlioti skyrių ribų iš turinio puslapių.

PDF bootstrap ir chapter extraction šiame repo yra `PyMuPDF-first`. Jei skriptas paleidžiamas su sistemos `python3`, bet `PyMuPDF` ten nėra, jis automatiškai persijungia į repo `.venv`, jei ji paruošta.

## Repo config

Shared repo nustatymai laikomi root faile:

- `repo_config.toml`

Šiuo metu jis valdo:

- `Obsidian` bazinį katalogą;
- vault vardą;
- `launchd` agentų prefiksą.

Jei reikia naujos mašinos ar kito vault kelio, keiskite `repo_config.toml`, o ne shell skriptus.

## Template refresh

Kai atnaujinamas `books/_template/`, jau bootstrap'intą knygą atnaujinkite taip:

```bash
python3 scripts/refresh_book_template.py --book-root books/<slug>
```

Refresh perrašo tik template-valdomus docs failus ir tuščius scaffold'us. Jis neliečia realių content artefaktų.

## Generic QA

Book-scoped skriptai nebeturi aktyvios knygos pagal nutylėjimą. Juos kvieskite taip:

```bash
MEDBOOK_ROOT=books/<slug> python3 scripts/run_chapter_qa.py 001
MEDBOOK_ROOT=books/<slug> python3 scripts/build_chapter_pack.py 001
MEDBOOK_ROOT=books/<slug> scripts/sync_obsidian_book.sh
```
