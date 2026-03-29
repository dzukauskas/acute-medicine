# Šaltinių Prioritetas

Šis failas apibrėžia ne tik bendrą prioritetą, bet ir kanoninį LT-source branduolį, kuriuo turi remtis kiekviena nauja knyga.
Čia aprašytos taisyklės šiame repo yra privalomos. Jos nėra rekomendaciniai patarimai ar „best effort“ gairės.

Greita taisyklė:

1. norminiam LT tekstui pirmiausia naudoti Lietuvos oficialius šaltinius;
2. jei jų nepakanka, naudoti Lietuvos universitetinius / tretinio lygio šaltinius;
3. jei LT sluoksnis per silpnas ar per senas, pereiti į Europos gaires;
4. originali knyga naudojama struktūrai ir kontekstui, ne vietinės normos nustatymui.

## LT-source branduolio žemėlapis

Repo-global failas:

- `shared/localization/lt_source_map.tsv`

Kiekviename `research/<slug>.md` faile turi būti aiškiai užrašyta, kuriuo šio žemėlapio keliu buvo remtasi.
Jei skyriuje yra aukštos rizikos terminas ar santrumpa, kurio LT atitikmuo nėra aktyvioje bazėje, prieš draftą reikia arba užrakinti jį `shared/lexicon/*.tsv` / `*.local.tsv`, arba aiškiai atmesti `term_candidates.tsv` faile kaip ne terminologinį ar tik originalo-konteksto vienetą.

Praktinis pirmas žingsnis prieš pildant research:

- paleisti `python3 scripts/generate_research_checklist.py --book-root books/<slug> <chapter>`

Checklist failas nepriima sprendimų už žmogų, bet automatiškai surenka:

- aptiktus jurisdikcinius signalus;
- preliminarius norminių claim tipų kandidatus;
- struktūrinių blokų `block_id`;
- rekomenduojamus LT-source kelius pagal šį žemėlapį.

Praktinis pirmas žingsnis prieš drafting:

- paleisti `python3 scripts/build_chapter_pack.py --book-root books/<slug> <chapter>`;
- jei pack generavimas sustoja dėl terminijos readiness klaidos, pirmiausia išspręsti terminų / santrumpų triage, o ne tęsti rašymą ranka apeinant vartus.
- jei angliškas medicininis terminas dar nėra aktyvioje bazėje, jo LT atitikmuo privalo būti patikrintas interneto LT šaltiniuose pagal šį prioritetą; spėjimas ar laisva improvizacija neleidžiami.

### 1. Paramediko kompetencija ir GMP

Pirmas pasirinkimas:

- SAM;
- `e-Seimas` / `TAR`;
- Greitosios medicinos pagalbos tarnyba.

Antras pasirinkimas:

- VASPVT;
- universitetinės ligoninės;
- profesinės draugijos.

ES fallback:

- ERC ir kitos Europos specialybinės gairės.

Naudoti:

- paramediko kompetencijai;
- GMP organizavimui;
- vietiniams algoritmams;
- aktyvavimo tvarkai;
- vietiniam skubios pagalbos kontekstui.

### 2. Vaistų registracija ir produkto informacija

Pirmas pasirinkimas:

- VVKT registruotų vaistinių preparatų paieška;
- VVKT registracijos pažymėjimo priedai.

Antras pasirinkimas:

- SAM reguliacinė medžiaga.

ES fallback:

- EMA;
- ES `SmPC` / product information.

Naudoti:

- indikacijoms;
- kontraindikacijoms;
- dozėms;
- vartojimo keliams;
- pakuotės lapeliui;
- preparato charakteristikų santraukai.

### 3. Kompensavimas ir LT rinkos prieinamumas

Pirmas pasirinkimas:

- VLK kompensuojamieji vaistai;
- VLK kainynai.

Antras pasirinkimas:

- VVKT.

ES fallback:

- EMA.

Naudoti:

- kompensavimui;
- realiam LT prieinamumui;
- rinkos statusui Lietuvoje.

### 4. Farmakologija ir racionalus skyrimas

Pirmas pasirinkimas:

- SAM racionalus vaistų skyrimas ir vartojimas;
- VVKT.

Antras pasirinkimas:

- LSMU;
- VU;
- universitetinės ligoninės.

ES fallback:

- EMA;
- Europos specialybinės gairės.

Naudoti:

- vaistų parinkimui;
- saugumui;
- racionalaus skyrimo principams;
- norminei farmakologinei informacijai.

Pastaba:

- fundamentinė farmakologija gali remtis universaliu mokslu, bet norminiai sprendimai turi eiti per LT/EU šaltinius.

### 5. Infekcijos ir visuomenės sveikata

Pirmas pasirinkimas:

- NVSC;
- Higienos institutas.

Antras pasirinkimas:

- SAM.

ES fallback:

- ECDC.

Naudoti:

- infekcijų kontrolei;
- epidemiologijai;
- visuomenės sveikatai;
- antimikrobiniam atsparumui.

### 6. Klinikinės metodikos ir specialybinės rekomendacijos

Pirmas pasirinkimas:

- SAM metodikos ir rekomendacijos.

Antras pasirinkimas:

- LSMU;
- VU;
- Santaros klinikos;
- Kauno klinikos;
- profesinės draugijos.

ES fallback:

- Europos specialybinės gairės.

Naudoti:

- klinikiniams algoritmams;
- diferencinei diagnostikai;
- gydymo taktikoms;
- specialybiniams sprendimams.

### 7. Teisė ir reguliavimas

Pirmas pasirinkimas:

- `e-Seimas`;
- `TAR`;
- SAM.

Antras pasirinkimas:

- VASPVT;
- VVKT.

ES fallback:

- EUR-Lex;
- EMA.

Naudoti:

- profesinėms riboms;
- teisėtam vaistų skyrimui;
- dokumentavimui;
- reguliaciniam kontekstui.

### 8. Terminija ir kalbos forma

Pirmas pasirinkimas:

- VLKK Terminų bankas.

Antras pasirinkimas:

- LSMU;
- VU;
- LT mokomoji literatūra.

ES fallback:

- tarptautinė nomenklatūra.

Naudoti:

- LT terminų formai;
- santrumpoms;
- kolokacijoms.

Svarbi riba:

- VLKK nėra klinikinis autoritetas, todėl medicininę reikšmę tikrinti kartu su klinikiniais šaltiniais.

### 9. Anatomija, fiziologija, patofiziologija

Pirmas pasirinkimas:

- LSMU;
- VU;
- LT akademinė mokomoji medžiaga.

Antras pasirinkimas:

- universitetiniai vadovėliai.

ES / international fallback:

- Europos ar tarptautiniai vadovėliai ir gairės.

Naudoti:

- fundamentiniams biologiniams ir medicininiams principams;
- LT terminijai;
- sąvokų paaiškinimui.

Svarbi riba:

- šiose temose vietinis norminis sluoksnis dažnai silpnesnis, todėl atskirti LT terminiją nuo universalaus mokslinio turinio.

## Aktualumo taisyklė

Prieš priimant klinikinį sprendimą kaip norminį:

1. patikrink datą;
2. patikrink, ar nėra naujesnės versijos;
3. jei Lietuvos šaltinis per senas arba nepakankamas, remkis naujesniu Europos šaltiniu;
4. originalą laikyk tik papildomu kontekstu;
5. datą, šaltinį ir sprendimą užfiksuok `research` faile.
