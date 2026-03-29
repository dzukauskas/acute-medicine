# 6 skyrius. List of Abbreviations

- Puslapiai: EPUB segmentas `c1DC.xhtml`
- Šaltinio segmentai: `c1DC.xhtml`
- Originalo failas: `/Users/dzukauskas/Projects/Acute Medicine/books/jrcalc-clinical-guidelines-2025-reference-edition/source/epub/JRCALC Clinical Guidelines 2025 Reference Edition.epub`
- Angliškas pagalbinis failas: `/Users/dzukauskas/Projects/Acute Medicine/books/jrcalc-clinical-guidelines-2025-reference-edition/source/chapters-en/006-list-of-abbreviations.md`
- Lietuviškas failas: `/Users/dzukauskas/Projects/Acute Medicine/books/jrcalc-clinical-guidelines-2025-reference-edition/lt/chapters/006-list-of-abbreviations.md`

## Source inventorius

### Poskyriai

- List of Abbreviations

### Lentelės

- Santrumpų žodynas (`227` eilutės)

### Paveikslai / schemos / algoritmai

- Nėra

### Rėmeliai / papildomi blokai

- Nėra

## Pirminė 006 inventoriaus suvestinė

- Santrumpų eilučių: `227`
- Unikalių santrumpų: `221`
- Dubletai, kuriems reikia atskiro sprendimo: `CPP`, `CRT`, `CSE`, `ICD`, `IN`
- Jau padengta aktyvioje `shared` bazėje: `14`
- Dar nepadengta aktyvioje `shared` bazėje: `213`

## 006 darbo strategija

- Tai nėra naratyvinis skyrius; tai santrumpų žodynas.
- Kiekvieną santrumpą reikia priskirti vienai iš šių kategorijų:
  - aktyvus LT medicininis atitikmuo (`shared/lexicon`)
  - originalo JK / institucinis kontekstas
  - bendras techninis ar fiziologinis trumpinys
  - mnemonika ar kontrolinis sąrašas (`ABCDE`, `AVPU`, `ATMIST`, `FAST`, `SCENE`, `SOCRATES`)
  - dubletai su keliomis reikšmėmis, kuriems būtinas atskiras išskyrimas
- Angliškų medicininių santrumpų LT atitikmenys negali būti spėjami; nepadengtus vienetus reikia tikrinti LT interneto šaltiniuose po vieną.

## Jau užrakinti 006 vienetai iš aktyvios bazės

- `ACS` -> `ūminis koronarinis sindromas`
- `ALoC` -> `sutrikusi sąmonė`
- `ALS` -> `specializuotas gaivinimas`
- `BLS` -> `pradinis gaivinimas`
- `COPD` -> `lėtinė obstrukcinė plaučių liga`
- `DKA` -> `diabetinė ketoacidozė`
- `FBAO` -> `kvėpavimo takų obstrukcija svetimkūniu`
- `HVS` -> `hiperventiliacijos sindromas`
- `ICD` -> `implantuojamas kardioverteris-defibriliatorius`
- `LVAD` -> `kairiojo skilvelio pagalbinis įrenginys`
- `NLS` -> `naujagimio gaivinimas`
- `PE` -> `plaučių embolija`
- `ROSC` -> `spontaninės kraujotakos atsinaujinimas`
- `TIA` -> `praeinantis smegenų išemijos priepuolis`

## Lietuvos šaltiniai

| Šaltinis | Tipas | Data / versija | Kodėl naudotas |
| --- | --- | --- | --- |
| VLKK Terminų bankas | terminija | žiūrėta 2026-03-29 | Bendrajai LT terminijai ir santrumpų išskleidimams, kai yra kanoninis LT terminas. |
| LSMU / VU / Santaros vieši akademiniai tekstai | LT medicininė vartosena | žiūrėta 2026-03-29 | Klinikinių santrumpų LT atitikmenims ir jų realiai vartojamai formai patikrinti. |
| SAM / e-Seimas | norminė LT vartosena | žiūrėta 2026-03-29 | Oficialiems ir civilinės saugos / sistemos terminams patikrinti, kai santrumpa liečia reglamentuotą sritį. |

## 006 triage: A-B blokas (2026-03-29)

| Santrumpa | Originalas | LT sprendimas | Statusas | LT šaltinio kryptis | Pastaba |
| --- | --- | --- | --- | --- | --- |
| AAA | Abdominal Aortic Aneurysm | pilvinės aortos aneurizma | approved_global | LSMU kraujagyslių chirurgijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| ABCDE | Airway / Breathing / Circulation / Disability / Exposure | ABCDE vertinimas; lokalizuojami tik atskiri žingsniai | localization_only | plačiai vartojama GMP / skubiosios pagalbos schema | Santrumpė paliekama originali, nes raidės remiasi EN schema. |
| ABD | Acute behavioural disorder | palikti originalo forma šiame etape | original_context_only | LT šaltiniuose reikia atskiro, griežtesnio tikrinimo | Nesuplakti su `Acute Behavioural Disturbance`; kol kas nekelti į aktyvią bazę. |
| AC | Alternating Current | kintamoji srovė | localization_only | bendroji techninė vartosena | Tai techninis terminas, ne medicininės terminų bazės prioritetas. |
| ACS | Acute Coronary Syndrome | ūminis koronarinis sindromas | approved_global | LSMU kardiologijos vartosena | Jau užrakinta `shared/lexicon`. |
| ADHD | Attention Deficit Hyperactivity Disorder | aktyvumo ir dėmesio sutrikimas (ADHD) | approved_global | LT psichiatrijos / psichologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| ADRT | Advance Decision to Refuse Treatment | palikti originalo JK kontekste | original_context_only | JK teisės ir originalo kontekstas | Nenaudoti kaip LT norminio atitikmens. |
| AED | Automated External Defibrillation | automatinis išorinis defibriliatorius (AED) | approved_global | LT gaivinimo vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT vartosenoje kalbama apie prietaisą. |
| AHF | Acute Heart Failure | ūminis širdies nepakankamumas (AHF) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| ALoC | Altered level of consciousness | sutrikusi sąmonė | approved_global | LT klinikinė vartosena | Jau užrakinta `shared/lexicon`. |
| ALS | Advanced Life Support | specializuotas gaivinimas (ALS) | approved_global | LT gaivinimo vartosena | Jau užrakinta `shared/lexicon`. |
| AMHP | Approved Mental Health Professional | palikti originalo JK kontekste | original_context_only | JK paslaugų modelio terminas | Neperkelti į LT aktyvią bazę. |
| APC | Antero-Posterior Compression | lokaliai vartoti `horizontalaus spaudimo iš priekio arba iš užpakalio sukelti lūžiai` | localization_only | LT dubens traumų klasifikacijos vartosena | Originali `APC` santrumpa nekelta į `shared`; LT šaltiniuose vartojamas aprašomasis Young-Burgess klasifikacijos pavadinimas. |
| ARDS | Acute Respiratory Distress Syndrome | ūminis respiracinio distreso sindromas (ARDS) | approved_global | LT intensyviosios terapijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| ATMIST | Age / Time / Mechanism / Injuries / Signs / Treatment | ATMIST perdavimo schema | localization_only | GMP perdavimo mnemonika | Santrumpė paliekama originali, o LT tekste aiškinami jos komponentai. |
| ATP | Anti-Tachycardia Pacing | antitachikardinė stimuliacija (ATP) | approved_global | LT kardiologijos ir implantuojamų prietaisų vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| AV | Atrioventricular | atrioventrikulinis | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| AVPU | Alert / Voice / Pain / Unresponsive | AVPU vertinimas; lokalizuojami tik atsako lygiai | localization_only | GMP neurologinės būklės vertinimo schema | Santrumpė paliekama originali. |
| BBB | Bundle branch block | Hiso pluošto kojytės blokada | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| BG | Blood Glucose | lokaliai vartoti `gliukozė kraujyje` arba `glikemija` | localization_only | LT diabetologijos ir GMP vartosena | Originali `BG` santrumpa nekelta į `shared`; LT šaltiniuose aktyvesnės pilnos formos. |
| BIA | Best Interest Assessors | palikti originalo JK kontekste | original_context_only | JK paslaugų ir teisės modelis | Į LT aktyvią bazę nekelti. |
| BiPAP | Bilevel Positive Pressure Ventilation | dviejų lygių teigiamo slėgio ventiliacija (BiPAP) | approved_global | LT intensyviosios terapijos ir SAM metodinė vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| BLS | Basic Life Support | pradinis gaivinimas (BLS) | approved_global | LT gaivinimo vartosena | Jau užrakinta `shared/lexicon`. |
| BM | Stick Measures blood sugar | nekelti į aktyvią bazę | not_acronym | projekto terminų politika | Tai nepageidautinas, anglizuotas praktinis trumpinys. |
| BMI | Body mass index | lokaliai vartoti `kūno masės indeksas (KMI)` | localization_only | LT visuomenės sveikatos ir klinikinė vartosena | Originali `BMI` santrumpa nekelta į `shared`, nes LT aktyvi vartosena remiasi `KMI`. |
| BP | Blood Pressure | lokaliai vartoti `arterinis kraujospūdis` / `AKS` | localization_only | LT klinikinė ir kardiologinė vartosena | Originali `BP` santrumpa nekelta į `shared`. |
| bpm | Beats per minute | lokaliai vartoti `k./min.` arba `kartai per minutę` | not_acronym | vienetų ir matavimo žymėjimo vartosena | Tai vieneto žymėjimas, ne medicininės terminų bazės akronimas. |
| BR | Breech | lokaliai vartoti `vaisiaus sėdmenų pirmeiga` | localization_only | LT akušerinė vartosena | Remiasi jau užrakintu `Breech Birth -> vaisiaus sėdmenų pirmeiga`; trumpinys `BR` nekeliamas į `shared`. |
| BTCS | Bilateral Tonic-Clonic Seizures | lokaliai vartoti `abipusiai toniniai-kloniniai traukuliai` | localization_only | LT vaikų neurologijos vartosena | Originali `BTCS` santrumpa nekelta į `shared`, nes LT praktikoje aktyvaus akronimo vartosena nestabili. |
| BTS | British Thoracic Society | palikti originalo JK organizacijos kontekste | original_context_only | JK profesinė draugija | Ne LT medicininio termino bazės vienetas. |
| BVM | Bag-Valve-Mask | lokaliai vartoti konkretų prietaiso aprašą, pvz., `Ambu tipo kvėpavimo maišas su apsauginiu slėgio vožtuvu ir kauke` | localization_only | LT gaivinimo ir neonatologijos įrangos vartosena | Originali `BVM` santrumpa nekelta į `shared`; LT vartosena labiau aprašo konkretų prietaisą. |

## 006 triage: C-D blokas (2026-03-29)

| Santrumpa | Originalas | LT sprendimas | Statusas | LT šaltinio kryptis | Pastaba |
| --- | --- | --- | --- | --- | --- |
| <C>ABCDE | <C> – Catastrophic haemorrhage | `<C>ABCDE` schema; LT lokalizuoti tik komponentus | localization_only | GMP / traumos mnemonika | Santrumpė paliekama originali, nes remiasi EN raidėmis. |
| CAMHS | Child and Adolescent Mental Health Services | palikti originalo JK paslaugų kontekste | original_context_only | JK paslaugų modelis | Ne LT aktyvios medicininės bazės vienetas. |
| CBRNE | Chemical, Biological, Radiological, Nuclear and Explosive | lokaliai aiškinti LT forma, bet nekelti į `shared` | localization_only | LT civilinės saugos vartosenoje dominuoja `CBRN`, ne `CBRNE` | Šio leidinio originali santrumpa negali tapti kanoniniu LT bazės vienetu. |
| CBT | Cognitive Behavioural Therapy | kognityvinė elgesio terapija (CBT) | approved_global | LT psichiatrijos ir psichologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| CCF | Congestive cardiac failure | stazinis širdies nepakankamumas (CCF) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| CCS | Central Cord Syndrome | lokaliai vartoti `nugaros smegenų centrinio pluošto sindromas` | localization_only | VLK / TLK-10-AM vartosena ir dubleto kontrolė | Originali `CCS` santrumpa nekelta į `shared`, nes tame pačiame leidinyje ji vartojama ir kaip `casualty clearing station`. |
| CES | Cauda Equina Syndrome | arklio uodegos sindromas (CES) | approved_global | LT neurochirurgijos ir ortopedijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| CEW | Controlled Electrical Weapon | palikti originalo kontekste arba aiškinti aprašomai lokaliai | original_context_only | policijos / saugumo terminas, ne LT medicininės bazės branduolys | Į `shared/lexicon` nekelti. |
| CFR | Community first responder | palikti originalo JK reagavimo modelio kontekste | original_context_only | JK / Airijos ikihospitalinių paslaugų modelis | Ne LT norminis atitikmuo. |
| CMHT | Community Mental Health Team | palikti originalo JK paslaugų kontekste | original_context_only | JK psichikos sveikatos paslaugų struktūra | Ne LT aktyvios bazės vienetas. |
| CMI | Combined Mechanical Injury | kol kas nekelti į `shared`; reikia stipresnio LT dubens traumų šaltinio dėl kanoninio atitikmens | open | LT dubens traumų vartosena dar nepakankamai užrakinta | JRCALC aprašo tai kaip kelių mechanizmų derinį, bet stabilaus LT kanoninio termino interneto šaltiniuose dar neradau. |
| CNS | Central Nervous System | centrinė nervų sistema (CNS) | approved_global | LT neurologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| CO | Carbon monoxide | anglies monoksidas (CO) | approved_global | LT toksikologijos ir visuomenės sveikatos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| CO2 | Carbon dioxide | anglies dioksidas (CO2) | approved_global | LT akademinė ir standartizacijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| COP | Code of Practice | palikti originalo dokumento / teisės kontekste | original_context_only | JK teisės ir paslaugų reglamentavimo kontekstas | Ne LT medicininio termino bazės vienetas. |
| COPD | Chronic Obstructive Pulmonary Disease | lėtinė obstrukcinė plaučių liga (LOPL / COPD) | approved_global | LT pulmonologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT vartosenoje dažnesnė `LOPL`. |
| CPAP | Continuous Positive Airway Pressure | nuolatinis teigiamas kvėpavimo takų slėgis (CPAP) | approved_global | LT oficiali ir ligoninių vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| CPN | Community Psychiatric Nurse | palikti originalo JK paslaugų kontekste | original_context_only | JK paslaugų modelis | Į LT aktyvią bazę nekelti. |
| CPP | Cerebral Perfusion Pressure | lokaliai vartoti `smegenų perfuzinis spaudimas` | localization_only | LT neurotraumos ir neuroanesteziologijos vartosena | Dubletas su `coronary perfusion pressure`; aktyvios `CPP` santrumpos į `shared` nekelti. |
| CPP | Coronary perfusion pressure | lokaliai vartoti `vainikinių arterijų perfuzinis spaudimas` | localization_only | LT gaivinimo fiziologijos vartosena | Dubletas su `cerebral perfusion pressure`; aktyvios `CPP` santrumpos į `shared` nekelti. |
| CPR | Cardiopulmonary Resuscitation | kardiopulmoninis gaivinimas (CPR) | approved_global | LT gaivinimo vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| CPR-IC | CPR-induced consciousness | kol kas nekelti į `shared`; lokalizuoti aprašomai tik atitinkamame gaivinimo kontekste | open | LT šaltinio pagrindas silpnas | Neužrakinti be stipresnio LT pagrindo. |
| CRT | Capillary Refill Test | lokaliai vartoti `kapiliarų prisipildymo laikas`, bet originalios `CRT` santrumpos nekelti į `shared` | localization_only | LT skubiosios pagalbos vartosena | Dubletas su `cardiac resynchronisation therapy`; automatinis aktyvus akronimas būtų rizikingas. |
| CRT | Cardiac Resynchronisation Therapy | lokaliai vartoti `širdies resinchronizacijos terapija`, bet originalios `CRT` santrumpos nekelti į `shared` | localization_only | LT kardiologijos vartosena | Dubletas su `capillary refill test`; aktyvi santrumpa projekto bazėje būtų klaidinanti. |
| CSA | Child Sexual Abuse | lokaliai vartoti `seksualinė prievarta prieš vaikus` | localization_only | LT vaiko teisių ir medicininės pagalbos vartosena | Koncepcija universali, bet `CSA` nėra kanoninis LT aktyvios bazės akronimas. |
| CSE | Child Sexual Exploitation | lokaliai vartoti `vaikų seksualinis išnaudojimas` | localization_only | LT vaiko teisių ir apsaugos vartosena | Dubletas su neurologiniu `CSE`; nekelti į `shared` akronimus. |
| CSE | Convulsive status epilepticus | lokaliai vartoti `traukulinė epilepsinė būklė` | localization_only | LT vaikų neurologijos / skubiosios pagalbos vartosena | Dubletas su `Child Sexual Exploitation`; aktyviai santrumpai trūksta saugaus vienareikšmiškumo. |
| CT | Computerised Tomography | kompiuterinė tomografija (KT / CT) | approved_global | LT radiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| DBS | Disclosure and Barring Service | palikti originalo JK institucinės patikros kontekste | original_context_only | JK teisinis / institucinės patikros modelis | Ne LT medicininės terminijos vienetas. |
| DC | Direct Current | nuolatinė srovė | localization_only | bendroji techninė vartosena | Techninis terminas; nereikia aktyvaus medicininio akronimo sluoksnio. |
| DKA | Diabetic Ketoacidosis | diabetinė ketoacidozė (DKA) | approved_global | LT endokrinologijos vartosena | Jau užrakinta `shared/lexicon/acronyms.tsv`. |
| DM | Diabetes Mellitus | cukrinis diabetas (DM) | approved_global | LT endokrinologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| DNA | Deoxyribonucleic Acid | lokaliai vartoti `dezoksiribonukleorūgštis (DNR)` | localization_only | LT akademinė vartosena | LT santrumpa yra `DNR`, todėl originali `DNA` nekelta į aktyvią bazę. |
| DNACPR | Do Not Attempt Cardio-Pulmonary Resuscitation | palikti originalo JK dokumentavimo kontekste | original_context_only | JK gydymo apribojimų dokumentų modelis | Ne LT norminio sluoksnio atitikmuo. |
| DoLS | Deprivation of Liberty Safeguards | palikti originalo JK teisės kontekste | original_context_only | JK teisės sistema | Į LT aktyvią bazę nekelti. |
| DPA | Data Protection Act | palikti originalo JK teisės kontekste | original_context_only | JK teisės sistema | Į LT aktyvią bazę nekelti. |
| DVT | Deep Vein Thrombosis | giliųjų venų trombozė (DVT) | approved_global | LT kraujagyslių medicinos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |

## 006 triage: E-F blokas (2026-03-29)

| Santrumpa | Originalas | LT sprendimas | Statusas | LT šaltinio kryptis | Pastaba |
| --- | --- | --- | --- | --- | --- |
| ECG | Electrocardiograph | lokaliai vartoti `elektrokardiograma (EKG)` | localization_only | LT kardiologijos vartosena | LT aktyvi santrumpa yra `EKG`; originali `ECG` nekelta į `shared`. |
| ECT | Electro-convulsive therapy | lokaliai vartoti `elektrokonvulsinė terapija (EKT)` | localization_only | LT psichiatrijos vartosena | Originali `ECT` nekelta į `shared`, nes LT santrumpa yra `EKT`. |
| ECMO | ECMO Extra-corporeal membrane oxygenation | ekstrakorporinė membraninė oksigenacija (EKMO / ECMO) | approved_global | LT intensyviosios terapijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| ED | Emergency Department | lokaliai vartoti `skubiosios pagalbos skyrius` | localization_only | LT ligoninių ir SAM vartosena | Originali `ED` santrumpa nekelta į `shared`, nes LT sistemoje vartojami pilni pavadinimai ar vietiniai trumpiniai. |
| EDD | Estimated Date of Delivery | lokaliai vartoti `numatoma gimdymo data` | localization_only | LT akušerinė vartosena | Originali `EDD` nekelta į `shared`. |
| EF | Ejection fraction | išstūmio frakcija (IF / EF) | approved_global | LT kardiologijos ir echokardiografijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| EOC | Emergency Operations Centre | palikti originalo sistemos / operacijų valdymo kontekste | original_context_only | organizacinis / ekstremaliųjų situacijų modelis | Ne LT medicininės terminijos branduolys. |
| ERC | European Resuscitation Council | palikti originalo organizacijos pavadinimo kontekste | original_context_only | Europos profesinė organizacija | Į LT aktyvią bazę nekelti. |
| ESC | European Society of Cardiology | palikti originalo organizacijos pavadinimo kontekste | original_context_only | Europos profesinė organizacija | Į LT aktyvią bazę nekelti. |
| ET | Endotracheal | lokaliai vartoti `endotrachėjinis` | localization_only | LT anesteziologijos ir intensyviosios terapijos vartosena | Originali `ET` santrumpa nekelta į `shared`. |
| EtCO2 | Exhaled (end-tidal) carbon dioxide | iškvepiamo oro anglies dioksidas (EtCO2) | approved_global | LT anesteziologijos ir gaivinimo vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| FAST | F – Face / A – Arms / S – Speech / T – Test | FAST schema; LT lokalizuoti komponentus | localization_only | insulto atpažinimo mnemonika | Santrumpė paliekama originali, nes remiasi EN raidėmis. |
| FBAO | Foreign Body Airway Obstruction | kvėpavimo takų obstrukcija svetimkūniu (FBAO) | approved_global | LT skubiosios pagalbos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`, remiantis jau validuotu terminu. |
| FGM | Female genital mutilation | lokaliai vartoti `moterų lytinių organų žalojimas` | localization_only | LT žmogaus teisių, viešosios sveikatos ir pagalbos nukentėjusiems vartosena | Originali `FGM` santrumpa nekelta į `shared`; LT vartosenoje vyrauja pilna forma, o source žodyne eilutė dubliuojasi tik dėl raidžių dydžio. |
| FLACC | F – Face / L – Legs / A – Activity / C – Cry / C – Consolability | FLACC skausmo vertinimo skalė | localization_only | LT vaikų skausmo vertinimo metodikos | Santrumpė paliekama originali; LT metodikose vartojama kaip skalės pavadinimas. |
| FII | Fabricated or Induced Illness | lokaliai vartoti `medicininė prievarta prieš vaikus`, prireikus aiškinant kaip `įgaliotojo asmens Miunhauzeno sindromas` | localization_only | LT SAM vaikų metodikos ir LSMU psichiatrijos vartosena | Originali `FII` santrumpa nekelta į `shared`; LT šaltiniai šią sąvoką sieja su medicininiu vaikų išnaudojimu ir įgaliotojo asmens Miunhauzeno sindromu. |

## 006 triage: G-H blokas (2026-03-29)

| Santrumpa | Originalas | LT sprendimas | Statusas | LT šaltinio kryptis | Pastaba |
| --- | --- | --- | --- | --- | --- |
| g | Grams | lokaliai vartoti `g` / `gramai` pagal sakinį | not_acronym | matavimo vienetų vartosena | Tai vieneto žymėjimas, ne terminų bazės akronimas. |
| GBS | Group B Strep Infection | lokaliai vartoti `B grupės streptokoko infekcija` | localization_only | LT akušerinė ir neonatologinė vartosena | LT aplinkoje aktyviau vartojama `BGS`, todėl originali `GBS` santrumpa nekelta į `shared`. |
| GCS | Glasgow Coma Scale | lokaliai vartoti `Glazgo komos skalė (GKS)` | localization_only | LT neurochirurgijos ir skubiosios pagalbos vartosena | Originali `GCS` santrumpa nekelta į `shared`, nes LT vartosenoje įprasta `GKS` / `GIS`. |
| GDPR | General Data Protection Regulations 2018 | palikti originalo ES teisės kontekste | original_context_only | teisinis reguliavimas | Ne medicininės terminijos branduolys. |
| GP | General Practitioner | lokaliai vartoti `šeimos gydytojas` / `bendrosios praktikos gydytojas` pagal kontekstą | localization_only | LT pirminės sveikatos priežiūros vartosena | Originali `GP` santrumpa nekelta į `shared`. |
| GTN | Glyceryl Trinitrate | glicerolio trinitratas (nitroglicerinas, GTN) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| GUM | Genito-urinary medicine | palikti originalo JK specialybės / paslaugos kontekste | original_context_only | JK paslaugų struktūra | Ne LT aktyvios medicininės terminijos vienetas. |
| HART | Hazardous Area Response Team | palikti originalo JK reagavimo modelio kontekste | original_context_only | JK ikihospitalinių tarnybų modelis | Į LT aktyvią bazę nekelti. |
| HCP | Healthcare Professional | lokaliai vartoti `sveikatos priežiūros specialistas` | localization_only | LT SAM ir ASPĮ vartosena | Originali `HCP` santrumpa nekelta į `shared`. |
| HFpEF | Heart failure with preserved ejection fraction | širdies nepakankamumas su išlikusia kairiojo skilvelio išstūmio frakcija (HFpEF) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| HFrEF | Heart failure with reduced ejection fraction | širdies nepakankamumas su sumažėjusia kairiojo skilvelio išstūmio frakcija (HFrEF) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| HIV | Human Immunodeficiency Virus | žmogaus imunodeficito virusas (ŽIV / HIV) | approved_global | LT infekcinių ligų vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT vartosenoje dažnesnė santrumpa `ŽIV`. |
| HME | Heat moisture exchanger | lokaliai vartoti `šilumos ir drėgmės keitiklis (dirbtinė nosis)` | localization_only | LT tracheostomos ir kvėpavimo takų priežiūros vartosena | Originali `HME` santrumpa nekelta į `shared`, nes šiame leidinyje ta pati santrumpa vartojama ir kita reikšme (`Homemade Explosives`). |
| HPV | Human papillomavirus | žmogaus papilomos virusas (ŽPV / HPV) | approved_global | LT infekcinių ligų ir onkoprevencijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT vartosenoje dažnesnė santrumpa `ŽPV`. |
| HR | Heart Rate | lokaliai vartoti `širdies susitraukimų dažnis` | localization_only | LT kardiologinė ir monitoravimo vartosena | Originali `HR` santrumpa nekelta į `shared`; LT tekstuose dažnesnė pilna forma arba `ŠSD`. |
| HVS | Hyperventilation Syndrome | hiperventiliacijos sindromas (HVS) | approved_global | remiasi jau validuotu LT terminu | Užrakinta `shared/lexicon/acronyms.tsv`. |

## 006 triage: I-J blokas (2026-03-29)

| Santrumpa | Originalas | LT sprendimas | Statusas | LT šaltinio kryptis | Pastaba |
| --- | --- | --- | --- | --- | --- |
| IA | Impaired awareness | lokaliai vartoti `hipoglikemijos nejutimas` | localization_only | LT diabetologijos vartosena | Šiame leidinyje `IA` reiškia ne bendrą sąmoningumo sutrikimą, o sumažėjusį ar išnykusį hipoglikemijos jutimą. |
| IBS | Irritable Bowel Syndrome | dirgliosios žarnos sindromas (DŽS / IBS) | approved_global | LT gastroenterologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT vartosenoje dažnesnė santrumpa `DŽS`. |
| ICD | International Classification of Diseases | lokaliai vartoti `Tarptautinė ligų klasifikacija (TLK)` | localization_only | LT kodavimo ir klasifikavimo vartosena | Dubletas su `Implantable Cardioverter Defibrillator`; originalios `ICD` santrumpos į `shared` nekelti. |
| ICD | Implantable Cardioverter Defibrillator | lokaliai vartoti `implantuojamas kardioverteris-defibriliatorius (IKD)` | localization_only | LT kardiologijos vartosena | LT terminas jau užrakintas `shared/lexicon/termbase.tsv`, bet dėl dubleto aktyvios `ICD` santrumpos į `shared` nekelti. |
| ICE | Infant Cooling Evaluation | palikti originalo protokolo / tyrimo įrankio kontekste | original_context_only | specifinis originalo įrankis | Ne LT aktyvios medicininės terminijos branduolys. |
| ICP | Intracranial Pressure | intrakranijinis spaudimas (ICP) | approved_global | LT neurochirurgijos ir SAM metodinė vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| IHD | Ischemic Heart Disease | išeminė širdies liga (IŠL / IHD) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT vartosenoje dažnesnė santrumpa `IŠL`. |
| ILCOR | International Liaison Committee on Resuscitation | palikti originalo tarptautinės organizacijos kontekste | original_context_only | tarptautinė organizacija | Į LT aktyvią bazę nekelti. |
| IM | Intramuscular | lokaliai vartoti `į raumenis` / `intraraumeninis` | localization_only | LT klinikinė vartosena | Originali `IM` santrumpa nekelta į `shared`. |
| IMCA | Independent Mental Capacity Advocates | palikti originalo JK teisinio / paslaugų modelio kontekste | original_context_only | JK teisės ir paslaugų sistema | Į LT aktyvią bazę nekelti. |
| IN | Intranasal | lokaliai vartoti `intranazinis` / `per nosį` | localization_only | LT klinikinė vartosena | Ši santrumpa žodyne kartojasi du kartus; į `shared` nekelta. |
| IO | Intraosseous | lokaliai vartoti `intraosinis` / `į kaulą` | localization_only | LT skubiosios pagalbos ir procedūrų vartosena | Originali `IO` santrumpa nekelta į `shared`, nes LT aktyvi vartosena nėra pakankamai stabili. |
| IPAP | I – Intent / P – Plans / A – Actions / P – Protection | IPAP mnemonika; LT lokalizuoti tik komponentus | localization_only | psichikos sveikatos rizikos vertinimo mnemonika | Šiame skyriuje `IPAP` nėra kvėpavimo aparato parametras, todėl traktuojama kaip mnemonika. |
| ITD | Impedance threshold device | įkvėpimo impedancinio slenksčio vožtuvas (ITD) | approved_global | LSMU gaivinimo fiziologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT šaltinyje vartojama tiksli forma `įkvėpimo impedancinio slenksčio vožtuvas`. |
| ITU | Intensive Care Unit | lokaliai vartoti `intensyviosios terapijos skyrius` | localization_only | LT ligoninių vartosena | Originali `ITU` santrumpa nekelta į `shared`; LT sistemoje vartojami vietiniai trumpiniai ar pilnas pavadinimas. |
| IV | Intravenous | lokaliai vartoti `intraveninis` / `į veną` | localization_only | LT klinikinė vartosena | Originali `IV` santrumpa nekelta į `shared`; vartotina tik kaip vartojimo kelio žyma kontekste. |
| IVC | Inferior Vena Cava | apatinė tuščioji vena (ATV / IVC) | approved_global | LT skubiosios echoskopijos ir anatomijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT vartosenoje dažnesnė santrumpa `ATV`. |
| J | Joule | lokaliai vartoti `J` / `džaulis` pagal sakinį | not_acronym | SI vienetų vartosena | Tai vieneto žymėjimas, ne medicininis akronimas. |
| JESIP | Joint Emergency Services Interoperability Programme | palikti originalo JK tarpinstitucinio reagavimo modelio kontekste | original_context_only | JK sistemos modelis | Į LT aktyvią bazę nekelti. |
| JRCALC | Joint Royal Colleges Ambulance Liaison Committee | palikti originalo leidinio ir organizacijos kontekste | original_context_only | originalo šaltinio institucinis sluoksnis | Į LT aktyvią bazę nekelti. |
| JVP | Jugular Venous Pressure | jungo venų spaudimas (JVP) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |

## 006 triage: K-L blokas (2026-03-29)

| Santrumpa | Originalas | LT sprendimas | Statusas | LT šaltinio kryptis | Pastaba |
| --- | --- | --- | --- | --- | --- |
| kg | Kilogram | lokaliai vartoti `kg` / `kilogramas` pagal sakinį | not_acronym | SI vienetų vartosena | Tai vieneto žymėjimas, ne medicininis akronimas. |
| kPa | Kilopascal | lokaliai vartoti `kPa` / `kilopaskalis` pagal sakinį | not_acronym | SI vienetų vartosena | Tai vieneto žymėjimas, ne medicininis akronimas. |
| LBBB | Left Bundle Branch Block | kairiosios Hiso pluošto kojytės blokada (LBBB) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT vartosenoje galimi vietiniai trumpiniai, bet šiame leidinyje laikomasi originalios `LBBB` santrumpos. |
| LC | Lateral Compression | lokaliai vartoti `šoninio spaudimo sukelti lūžiai` / `lateralinės kompresijos pažeidimai` pagal kontekstą | localization_only | LT dubens traumų klasifikacijos vartosena | Originali `LC` santrumpa nekelta į `shared`; LT šaltiniuose aktyvesni aprašomieji Young-Burgess / AO klasifikacijos pavadinimai. |
| LMP | Last Menstrual Period | lokaliai vartoti `paskutinių mėnesinių pirmoji diena` | localization_only | LT akušerinė vartosena | Originali `LMP` santrumpa nekelta į `shared`, nes LT tekstuose dažniau vartojama pilna forma. |
| LOC | Level of Consciousness | lokaliai vartoti `sąmonės lygis` | localization_only | LT neurologinė ir skubiosios pagalbos vartosena | Originali `LOC` santrumpa nekelta į `shared`; LT klinikiniuose tekstuose paprastai vartojama pilna forma ar skalės pavadinimas. |
| LPA | Lasting Power of Attorney | palikti originalo JK teisės kontekste | original_context_only | JK teisės sistema | Ne medicininės terminijos branduolys. |
| LVAD | Left ventricular assist device | kairiojo skilvelio pagalbinis įrenginys (LVAD) | approved_global | LT kardiologijos vartosena | Jau užrakinta `shared/lexicon/acronyms.tsv`. |
| LVF | Left Ventricular Failure | kairiojo skilvelio nepakankamumas (LVF) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| LVSD | Left ventricular systolic dysfunction | kairiojo skilvelio sistolinė disfunkcija (LVSD) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |

## 006 triage: M-N blokas (2026-03-29)

| Santrumpa | Originalas | LT sprendimas | Statusas | LT šaltinio kryptis | Pastaba |
| --- | --- | --- | --- | --- | --- |
| MAOI | Monoamine Oxidase Inhibitor antidepressant | monoamino oksidazės inhibitoriai (MAOI) | approved_global | LT psichiatrijos ir farmakologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT šaltiniuose matomas ir variantas `monoaminooksidazės inhibitoriai`. |
| MAP | Mean Arterial Pressure | vidutinis arterinis kraujo spaudimas (MAP) | approved_global | LT anesteziologijos ir hemodinamikos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| MBRRACE | Mothers and Babies: Reducing Risk through Audits and Confidential Enquiries | palikti originalo JK audito ir konfidencialių tyrimų programos kontekste | original_context_only | JK sistemos ir audito modelis | Ne LT aktyvios medicininės terminijos branduolys. |
| MCA | Mental Capacity Act | palikti originalo JK teisės kontekste | original_context_only | JK teisės sistema | Į LT aktyvią bazę nekelti. |
| mcg | Microgram | lokaliai vartoti `mikrogramas` / `mkg` pagal sakinį | not_acronym | vienetų vartosena | Tai vieneto žymėjimas, ne medicininis akronimas. |
| mCPR | Mechanical chest compression devices | lokaliai vartoti `mechaniniai krūtinės ląstos paspaudimų prietaisai` | localization_only | LT gaivinimo įrangos vartosena | Originali `mCPR` santrumpa nekelta į `shared`, nes LT aktyvi vartosena nestabili. |
| MDMA | Methylene Dioxymethamphetamine | 3,4-metilenedioksimetamfetaminas (MDMA) | approved_global | LT toksikologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; viešojoje kalboje gali būti aiškinama kaip `ekstazis`. |
| MECC | Making Every Contact Count | palikti originalo visuomenės sveikatos programos kontekste | original_context_only | JK sveikatos stiprinimo modelis | Ne LT aktyvios medicininės terminijos branduolys. |
| mg | Milligram | lokaliai vartoti `mg` / `miligramas` pagal sakinį | not_acronym | vienetų vartosena | Tai vieneto žymėjimas, ne medicininis akronimas. |
| MHA | Mental Health Act | palikti originalo JK teisės kontekste | original_context_only | JK teisės sistema | Į LT aktyvią bazę nekelti. |
| MI | Myocardial Infarction | miokardo infarktas (MI) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; helper source eilutė pataisyta iš klaidingo `Ml` į `MI`. |
| MINAP | Myocardial Ischaemia National Audit Project | palikti originalo JK nacionalinio audito projekto kontekste | original_context_only | JK sistemos ir audito modelis | Ne LT aktyvios medicininės terminijos branduolys. |
| ml | Millilitre | lokaliai vartoti `ml` / `mililitras` pagal sakinį | not_acronym | vienetų vartosena | Tai vieneto žymėjimas, ne medicininis akronimas. |
| mmHG | Millimetres of Mercury | lokaliai vartoti `mmHg` / `mm gyvs. st.` pagal sakinį | not_acronym | vienetų vartosena | Tai matavimo vieneto žymėjimas; be to, source faile raidžių dydis nenuoseklus. |
| mmol | Millimoles | lokaliai vartoti `mmol` pagal sakinį | not_acronym | vienetų vartosena | Tai vieneto žymėjimas, ne medicininis akronimas. |
| mmol/l | Millimoles per Litre | lokaliai vartoti `mmol/l` arba `mmol/L` pagal projekto stilistiką | not_acronym | vienetų vartosena | Tai vieneto žymėjimas, ne medicininis akronimas. |
| MOI | Mechanisms of Injury | lokaliai vartoti `traumos mechanizmas` | localization_only | LT traumatologijos ir GMP vartosena | Originali `MOI` santrumpa nekelta į `shared`. |
| MSC | M – Motor / S – Sensation / C – Circulation | MSC vertinimas; LT lokalizuoti komponentus | localization_only | klinikinės vertinimo mnemonikos vartosena | Tai mnemonika, ne LT aktyvios terminų bazės akronimas. |
| msec | Millisecond | lokaliai vartoti `ms` / `milisekundė` pagal sakinį | not_acronym | vienetų vartosena | Tai vieneto žymėjimas, ne medicininis akronimas. |
| MTC | Major Trauma Centre | palikti originalo JK traumų sistemos kontekste | original_context_only | vidinė leidinio vartosena ir JK traumų tinklo modelis | 006 helper source eilutė buvo akivaizdžiai klaidinga kaip `Major Triage Centre`; kituose šios knygos skyriuose vartojama `Major Trauma Centre`. |
| NARU | National Ambulance Resilience Unit | palikti originalo JK sistemos kontekste | original_context_only | JK tarnybų modelis | Į LT aktyvią bazę nekelti. |
| NEET | Not in Education, Employment or Training | palikti originalo socialinės politikos kontekste | original_context_only | JK / socialinės politikos terminas | Ne medicininės terminijos branduolys. |
| NEWS | National Early Warning Score | ankstyvojo perspėjimo skalė (NEWS) | approved_global | LT skubiosios pagalbos ir sepsio vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT šaltiniuose plačiai matoma ir forma `NEWS2`. |
| NG | Nasogastric | lokaliai vartoti `nazogastrinis` / `nazogastrinis zondas` pagal sakinį | localization_only | LT klinikinė vartosena | Originali `NG` santrumpa nekelta į `shared`. |
| NHS | National Health Service | palikti originalo JK sveikatos sistemos kontekste | original_context_only | JK sistemos modelis | Į LT aktyvią bazę nekelti. |
| NICE | National Institute for Health and Care Excellence | palikti originalo JK gairių rengėjo kontekste | original_context_only | JK organizacinis / gairių leidėjo kontekstas | Į LT aktyvią bazę nekelti. |
| NLS | Newborn Life Support | naujagimio gaivinimas (NLS) | approved_global | LT neonatologijos ir gaivinimo vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| NPA | Nasopharyngeal airway | lokaliai vartoti `nazofaringinis vamzdelis` | localization_only | LT skubiosios pagalbos vartosena | Originali `NPA` santrumpa nekelta į `shared`, nes LT praktikoje dažniau vartojama pilna forma. |
| NPIS | National Poisons Information Service | palikti originalo JK toksikologinės informacijos tarnybos kontekste | original_context_only | JK sistemos modelis | Į LT aktyvią bazę nekelti. |
| NSAID | Non-Steroidal Anti-inflammatory Drug | lokaliai vartoti `nesteroidinis vaistas nuo uždegimo (NVNU)` | localization_only | LT farmakologijos ir klinikinė vartosena | Originali `NSAID` nekelta į `shared`, nes LT aktyvi santrumpa yra `NVNU`. |
| NSTEMI | Non-ST Segment Elevation Myocardial Infarction | miokardo infarktas be ST segmento pakilimo (NSTEMI) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT šaltiniuose matoma ir forma `MI be ST pakilimo`. |

## 006 triage: O-P blokas (2026-03-29)

| Santrumpa | Originalas | LT sprendimas | Statusas | LT šaltinio kryptis | Pastaba |
| --- | --- | --- | --- | --- | --- |
| O 2 | Oxygen | lokaliai vartoti `O2` / `deguonis` pagal sakinį | not_acronym | cheminių elementų ir dujų žymėjimas | Tai cheminio elemento formulė, ne medicininis akronimas. |
| OHCA | Out of Hospital Cardiac Arrest | širdies sustojimas už ligoninės ribų (OHCA) | approved_global | LT gaivinimo vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT vartosenoje pasitaiko ir `ŠSNL`. |
| OOH | Out of Hours | palikti originalo sistemos organizavimo kontekste | original_context_only | JK paslaugų organizavimo modelis | Ne LT aktyvios medicininės terminijos branduolys. |
| OPA | Oropharyngeal Airway | orofaringinis vamzdelis (OPA) | approved_global | LT skubiosios pagalbos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| ORS | Oral Rehydration Salt | oralinės rehidratacijos druskos (ORS) | approved_global | LT vaikų ligų ir SAM metodinė vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| P | Parity | lokaliai vartoti `gimdymų skaičius` / `paritetas` pagal lentelės kontekstą | localization_only | LT akušerinė vartosena | Vienos raidės žyma vartotina tik kontekste, ne aktyvioje bendroje bazėje. |
| PCO 2 | Measure of the Partial Pressure of Carbon dioxide | lokaliai vartoti `dalinis anglies dioksido slėgis`, pagal kontekstą dažniausiai `pCO2` / `PaCO2` | localization_only | LT anesteziologijos ir kraujo dujų vartosena | Source žyma nenuosekli, todėl nekelta į `shared` kaip atskiras aktyvus akronimas. |
| PE | Pulmonary Embolism | plaučių embolija (PE) | approved_global | LT kardiologijos ir akušerijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; remiasi jau validuotu termino įrašu. |
| PEaRL | Pupils Equal and Reacting to Light | PEaRL vertinimas; LT lokalizuoti kaip `vyzdžiai vienodi ir reaguoja į šviesą` | localization_only | klinikinio ištyrimo mnemonic tipo žyma | Santrumpė nekelta į `shared`, nes tai aprašomoji trumpa mnemonika. |
| PEA | Pulseless Electrical Activity | elektromechaninė disociacija (EMD / PEA) | approved_global | LT kardiologijos ir gaivinimo vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT šaltiniuose matoma ir aprašomoji forma `elektrinis aktyvumas be pulso`. |
| PEF | Peak Expiratory Flow | didžiausias iškvėpimo srovės greitis (PEF) | approved_global | LT pulmonologijos ir SAM vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| PEFR | Peak Expiratory Flow Rate | lokaliai vartoti tą pačią LT formą kaip `PEF` | localization_only | LT pulmonologijos vartosena | Neaktyvinta atskirai, kad nedubliuotų aktyvaus `PEF` įrašo. |
| PHECG | Pre-hospital 12-lead electrocardiogram | lokaliai vartoti `ikihospitalinė 12 derivacijų elektrokardiograma` | localization_only | LT GMP ir kardiologinė vartosena | Originali `PHECG` santrumpa nekelta į `shared`. |
| PNES | Psychogenic non-epileptic seizures | psichogeniniai neepilepsiniai priepuoliai (PNES) | approved_global | LT neurologijos ir epileptologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| PPCI | Primary Percutaneous Coronary Intervention | lokaliai vartoti `pirminė perkutaninė koronarinė intervencija`, prireikus aiškinant kaip `PKI` | localization_only | LT kardiologijos vartosena | Originali `PPCI` nekelta į `shared`, nes LT vartosenoje dažnesnė `PKI`. |
| PPE | Personal Protective Equipment | lokaliai vartoti `asmens apsaugos priemonės` | localization_only | LT SAM ir infekcijų kontrolės vartosena | Originali `PPE` nekelta į `shared`, nes LT tekstuose vartojama pilna forma. |
| PPH | Post-Partum Haemorrhage | lokaliai vartoti `pogimdyminis kraujavimas` | localization_only | LT akušerinė vartosena | Originali `PPH` nekelta į `shared`, nes LT vartosenoje aktyvi santrumpa nėra stabili. |
| PTSD | Post-traumatic Stress Disorder | potrauminio streso sutrikimas (PTSS / PTSD) | approved_global | LT psichikos sveikatos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT vartosenoje dažna ir santrumpa `PTSS`. |
| PRESS | Prehospital Recognition of Severe Sepsis | palikti originalo įrankio / score kontekste | original_context_only | specifinis originalo atpažinimo įrankis | Ne LT aktyvios medicininės terminijos branduolys. |
| PSP | Patient specific protocol | palikti originalo sistemos / vietinio protokolo kontekste | original_context_only | originalo tarnybos protokolinis sluoksnis | Į LT aktyvią bazę nekelti. |
| PV | Per Vaginam | lokaliai vartoti `vaginaliniu būdu` / `per makštį` pagal kontekstą | localization_only | LT akušerinė ir ginekologinė vartosena | Lotyniška žyma vartotina tik lokaliai, ne aktyvioje bendroje bazėje. |

## 006 triage: Q-R blokas (2026-03-29)

| Santrumpa | Originalas | LT sprendimas | Statusas | LT šaltinio kryptis | Pastaba |
| --- | --- | --- | --- | --- | --- |
| RBBB | Right bundle branch block | dešiniosios Hiso pluošto kojytės blokada (RBBB) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT vartosenoje galimi vietiniai trumpiniai, bet šiame leidinyje laikomasi originalios `RBBB` santrumpos. |
| RCT | Randomised Controlled Trial | atsitiktinių imčių kontroliuojamas tyrimas (RCT) | approved_global | LT mokslinė ir metodologinė vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| ReSPECT | Recommended Summary Plan for Emergency Care and Treatment | palikti originalo JK išankstinio priežiūros planavimo dokumento kontekste | original_context_only | JK sistemos ir teisės modelis | Į LT aktyvią bazę nekelti. |
| ROLE | Recognition Of Life Extinct | lokaliai vartoti `mirties fakto konstatavimas` / `pripažinimas mirusiu` pagal procedūros kontekstą | localization_only | LT GMP ir teisinės medicinos vartosena | Originali `ROLE` santrumpa nekelta į `shared`, nes tai specifinė originalo procedūrinė žyma. |
| ROSC | Return of Spontaneous Circulation | spontaninės kraujotakos atsinaujinimas (ROSC) | approved_global | LT gaivinimo vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; remiasi jau validuotu termino įrašu. |
| RR | Respiratory Rate | lokaliai vartoti `kvėpavimo dažnis` | localization_only | LT skubiosios pagalbos ir monitoravimo vartosena | Originali `RR` santrumpa nekelta į `shared`; LT tekstuose dažnesnė pilna forma arba vietinis trumpinys. |
| RSV | Respiratory Syncytial Virus | respiracinis sincitinis virusas (RSV) | approved_global | LT vaikų ligų ir infekcinių ligų vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| RTC | Road Traffic Collision | lokaliai vartoti `eismo įvykis` / `kelių eismo įvykis` pagal kontekstą | localization_only | LT GMP ir traumos vartosena | Originali `RTC` santrumpa nekelta į `shared`. |
| RVF | Right Ventricular Failure | dešiniojo skilvelio nepakankamumas (RVF) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| RVP | Rendezvous Point(s) | palikti originalo operacinio planavimo kontekste | original_context_only | operacinis / reagavimo modelis | Ne LT aktyvios medicininės terminijos branduolys. |

## 006 triage: S blokas (2026-03-29)

| Santrumpa | Originalas | LT sprendimas | Statusas | LT šaltinio kryptis | Pastaba |
| --- | --- | --- | --- | --- | --- |
| SARC | Sexual Assault Referral Centre | palikti originalo JK seksualinės prievartos pagalbos centro kontekste | original_context_only | JK paslaugų modelis | Ne LT aktyvios medicininės terminijos branduolys. |
| SBAR | S – Situation / B – Background / A – Assessment / R – Recommendation | SBAR perdavimo schema; LT lokalizuoti komponentus | localization_only | klinikinės komunikacijos mnemonika | Santrumpė paliekama originali, nes remiasi EN raidėmis. |
| SBI | Serious Bacterial Infection | sunki bakterinė infekcija (SBI) | approved_global | LT vaikų ligų vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| SBP | Systolic Blood Pressure | lokaliai vartoti `sistolinis arterinis kraujospūdis` | localization_only | LT klinikinė vartosena | Originali `SBP` santrumpa nekelta į `shared`; LT tekstuose dažnesnė pilna forma arba vietinis trumpinys. |
| SC | Subcutaneous | lokaliai vartoti `poodinis` / `po oda` | localization_only | LT klinikinė vartosena | Originali `SC` santrumpa nekelta į `shared`. |
| SCENE | S – Safety / C – Call for help / E – Emergency care / N – No further harm / E – Evaluate | SCENE schema; LT lokalizuoti komponentus | localization_only | mokymo / veiksmų sekos mnemonika | Santrumpė paliekama originali, nes remiasi EN raidėmis. |
| SCI | Spinal Cord Injury | nugaros smegenų pažeidimas (SCI) | approved_global | LT traumų ir neurochirurgijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| SGA | Supraglottic airway | lokaliai vartoti `supraglotinis kvėpavimo takų prietaisas` arba konkretaus prietaiso pavadinimą pagal kontekstą | localization_only | LT skubiosios pagalbos ir anesteziologijos vartosena | Neaktyvinta bendrai, nes LT vartosenoje dažnai naudojamas konkretaus prietaiso pavadinimas, o ne vienas stabilus bendrinis akronimas. |
| SOB | Shortness of breath | lokaliai vartoti `dusulys` | localization_only | LT klinikinė vartosena | Originali `SOB` santrumpa nekelta į `shared`. |
| SOBOE | Shortness of breath on exertion | lokaliai vartoti `dusulys fizinio krūvio metu` | localization_only | LT klinikinė vartosena | Originali `SOBOE` santrumpa nekelta į `shared`. |
| SOCRATES | S – Site / O – Onset / C – Character / R – Radiation / A – Associations / T – Time course / E – Exacerbating or relieving factors / S – Severity | SOCRATES skausmo vertinimo schema; LT lokalizuoti komponentus | localization_only | klinikinė mnemonika | Santrumpė paliekama originali, nes remiasi EN raidėmis. |
| SOP | Standard operating procedure | lokaliai vartoti `standartinė veiklos procedūra` tik esant poreikiui | original_context_only | procedūrinis / organizacinis sluoksnis | Ne LT medicininės terminijos branduolys. |
| SORT | Special Operations Response Team | palikti originalo specialiųjų operacijų reagavimo komandos kontekste | original_context_only | operacinis / reagavimo modelis | Ne LT aktyvios medicininės terminijos branduolys. |
| SpO 2 | Oxygen Saturation Measured With Pulse Oximeter | lokaliai vartoti `deguonies įsotinimas`, žymint kaip `SpO2` | localization_only | LT monitoravimo vartosena | Tai parametro žyma, o ne bendros terminų bazės akronimas. |
| SSRIs | Selective Serotonin Re-Uptake Inhibitors | selektyvieji serotonino reabsorbcijos inhibitoriai (SSRI / SSRIs) | approved_global | LT psichiatrijos ir farmakologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| STEMI | ST Segment Elevation Myocardial Infarction | miokardo infarktas su ST segmento pakilimu (STEMI) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT šaltiniuose matoma ir forma `MI su STP`. |
| SVT | Supraventricular Tachycardia | supraventrikulinė tachikardija (SVT) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |

## 006 triage: T blokas (2026-03-29)

| Santrumpa | Originalas | LT sprendimas | Statusas | LT šaltinio kryptis | Pastaba |
| --- | --- | --- | --- | --- | --- |
| TARN | Trauma Audit Research Network | palikti originalo JK traumų audito tinklo kontekste | original_context_only | JK audito ir kokybės stebėsenos modelis | Ne LT aktyvios medicininės terminijos branduolys. |
| TBI | Traumatic Brain Injury | trauminis galvos smegenų pažeidimas (TBI) | approved_global | LT neurochirurgijos ir traumų vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT vartosenoje matoma ir forma `galvos smegenų trauma`. |
| TBSA | Total Body Surface Area | lokaliai vartoti `viso kūno paviršiaus plotas` | localization_only | LT nudegimų ir chirurgijos vartosena | Originali `TBSA` santrumpa nekelta į `shared`, nes LT tekstuose dažniau vartojama pilna forma. |
| TIA | Transient Ischaemic Attack | praeinantis smegenų išemijos priepuolis (PSIP / TIA) | approved_global | LT neurologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`; LT vartosenoje aktyvi ir santrumpa `PSIP`. |
| TLoC | Transient loss of consciousness | lokaliai vartoti `trumpalaikis sąmonės netekimas` | localization_only | LT neurologijos ir skubiosios pagalbos vartosena | Originali `TLoC` santrumpa nekelta į `shared`. |

### C-D blokui faktiškai naudoti LT interneto šaltiniai

- VLK TLK-10-AM vartosena dėl `CCS`: `nugaros smegenų centrinio pluošto sindromas (nugaros smegenų nevisiškas nutraukimas) kaklo lygyje`  
  https://ebook.vlk.lt/e.vadovas_iki2016.12.31/topic/lt.webmedia.vlk.drg.icd.ebook.content/html/icd/19skyrius.html
- SAM sunkios traumos metodika dėl `CPP`: `galvos smegenų perfuzinis spaudimas`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Asmens_sveikatos_prieziura/Metodiniai%20dokumentai/SUNKIOS%20TRAUMOS.pdf
- LSMU / Medicina gaivinimo fiziologijos vartosena dėl `CPP`: `vainikinių arterijų perfuzinis spaudimas`  
  https://medicina.lsmuni.lt/med/0604/0604-11l.pdf
- SAM 2024 veiklos ataskaita dėl `CPAP`: `Continuous Positive Airway Pressure – nuolatinis teigiamas kvėpavimo takų slėgis`  
  https://sam.lrv.lt/public/canonical/1744181951/27435/24-03_SAM%2520VEIKLOS%2520ATASKAITA_final.pdf
- LSMU pulmonologijos vartosena dėl `COPD`: `lėtinė obstrukcinė plaučių liga (LOPL)`  
  https://lsmu.lt/cris/entities/publication/e5a911d6-1ebd-4643-93f6-60ea04d99c77
- LSMU kritinių būklių neurologijos vartosena dėl `CSE`: `generalizuota traukulinė epilepsinė būklė`  
  https://lsmu.lt/cris/entities/publication/d4a964b7-c466-448f-bc46-b5ecf64903ec
- ESSC / metodikos vartosena dėl `CRT`: `kapiliarų prisipildymo laikas`  
  https://essc.lrv.lt/media/viesa/saugykla/2023/8/pC6i_AAUZo8.pdf
- VDU akademinė vartosena dėl `DNA`: `dezoksiribonukleorūgštis (DNR)`  
  https://www.vdu.lt/cris/bitstream/20.500.12259/31911/3/9786094671050_2015.pdf

### Papildomi A-B ir E-F blokų LT interneto šaltiniai

- VGTU biomechanikos / traumatologijos darbas dėl `APC`: `horizontalaus spaudimo iš priekio arba iš užpakalio sukelti lūžiai` Young-Burgess klasifikacijoje  
  https://gs.elaba.lt/object/elaba%3A2144459/2144459.pdf
- SAM / LSMU vartosena dėl `BMI`: `kūno masės indeksas (KMI)`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/visuomenes-sveikatos-prieziura/mityba-ir-fizinis-aktyvumas/Sveikos_ir_tvarios_mitybos_rekom_ilgos_2022.pdf
- LSMU vartosena dėl `BP`: `arterinis kraujospūdis (AKS)`  
  https://lsmu.lt/cris/entities/publication/7c8fb233-3610-4232-ba9f-d626c30d0698
- LSMU vartosena dėl `BTCS`: `toniniai-kloniniai`, `generalizuoti toniniai-kloniniai traukuliai`  
  https://lsmu.lt/cris/entities/publication/8131199e-99ae-4e5e-b669-352e03b02ea0
- LSMU / SAM vartosena dėl `ATP`: `antitachikardinė stimuliacija`  
  https://lsmu.lt/cris/entities/publication/7e8cf9a7-f717-48ce-9b40-416dedd756de
- SAM diabetologinė vartosena dėl `BG`: `glikemija`, `gliukozės koncentracija kraujyje`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Asmens_sveikatos_prieziura/Metodiniai%20dokumentai/CUKRINIS%20DIABETAS.pdf
- SAM širdies nepakankamumo metodika dėl `BiPAP`: `dviejų lygių teigiamo slėgio ventiliacija`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Asmens_sveikatos_prieziura/Diagnostikos_metodikos_ir_rekomendacijos/Metodikos/Sirdies_nepakankamumas_Metodika_2017%20m_NEW.pdf
- SAM metodika dėl `BVM`: `Ambu tipo kvėpavimo maišas su apsauginiu slėgio vožtuvu`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Programos_ir_projektai/Sveicarijos_parama/Akuserines%20metodikos/Cezario%20pjuvio%20operacija_%20Indikacijos.pdf
- Moterų informacijos centro ir Europos Parlamento LT vartosena dėl `FGM`: `moterų lytinių organų žalojimas` / `moterų lyties organų žalojimas`  
  https://lygus.lt/wp-content/uploads/2024/05/Metodika_.pdf
- Moterų informacijos centro LT vartosena dėl `FGM`: `moterų lytinių organų žalojimas (MLOŽ)`  
  https://lygus.lt/kategorija/lyciu-lygybe/page/9/
- SAM vaikų metodinė vartosena dėl `FII`: `medicininė prievarta prieš vaikus – medicininis vaikų išnaudojimas`, susidedantis iš vaiko ligos išgalvojimo arba sukėlimo  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Asmens_sveikatos_prieziura/19_%20Vaiku%20vemimas.pdf
- LSMU vartosena dėl `FII` pediatrinio ekvivalento: `įgaliotojo asmens Miunhauzeno sindromas`  
  https://sam.lrv.lt/uploads/sam/documents/files/%C5%BDurnalas%20Sveikatos%20mokslai%202021%20m_%20Nr_%204.pdf
- SAM vartosena dėl `ECG`: `EKG – elektrokardiograma (angl. ECG)`  
  https://sam.lrv.lt/public/canonical/1732168008/26447/kardioonkologija_2023_spaudai.pdf
- VU vartosena dėl `ECT`: `elektrokonvulsinė terapija`  
  https://www.zurnalai.vu.lt/neurologijos_seminarai/article/view/38295
- SAM vartosena dėl `ECMO`: `ekstrakorporinė membraninė oksigenacija (EKMO)`  
  https://sam.lrv.lt/uploads/sam/documents/files/Komisijos%20ir%20darbo%20grup%C4%97s/Asmens%20sveikatos%20prie%C5%BEi%C5%ABros%20komitetas/LARD_COVID_2020_12_02_SAM.pdf
- SAM vartosena dėl `EDD`: `numatoma gimdymo data`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Programos_ir_projektai/Sveicarijos_parama/Akuserines%20metodikos/Uzsiteses%20nestumas.pdf
- LSMU vartosena dėl `EF`: `išstūmio frakcija`  
  https://lsmu.lt/cris/entities/publication/e4ed04b5-fb44-4a5b-8ef0-11fff12d8d43
- SAM vartosena dėl `ED`: `skubiosios pagalbos skyrius`  
  https://sam.lrv.lt/lt/news/sklandesniam-skubiosios-pagalbos-skyriu-darbui-stebesenos-ir-analizes-irankis/
- SAM vartosena dėl `FLACC`: `FLACC skausmo vertinimo skalė`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Asmens_sveikatos_prieziura/41_%20Vaiku%20reabilitacinio%20gydymo%20poreikio%20vertinimas.pdf
- Anesteziologijos / gaivinimo vartosena dėl `EtCO2`: `iškvepiamo oro anglies dioksidas`  
  https://akl.lt/wp-content/uploads/2016/01/GAIR%C4%96S_Pirmoji-pagalba-gaivinimas_2011.pdf

### G-H blokui faktiškai naudoti LT interneto šaltiniai

- LSMU / akušerinė vartosena dėl `GBS`: `B grupės streptokokas`, `B grupės streptokoko kolonizacija / infekcija`  
  https://lsmu.lt/cris/entities/person/ea3a62f5-4e47-4b5d-a337-8fb87c5594a7/full
- LSMU vartosena dėl `GCS`: `Glazgo komos skalė`  
  https://lsmu.lt/cris/entities/etd/894b2c78-446b-4a21-8afb-83ee0afaede2
- SAM / LSMU vartosena dėl `GTN`: `glicerolio trinitratas`, klinikinėje praktikoje siejamas su nitroglicerinu  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Sveikatos_mokslai/2022%20SM3%28Internetas%29.pdf
- LSMUL Kauno klinikų vartosena dėl `HME`: `šilumos – drėgmės keitiklis (dirbtinė nosis)`  
  https://www.kaunoklinikos.lt/media/file/Tracheostominio%20vamzdelio%20prie%C5%BEi%C5%ABra.pdf
- SAM vartosena dėl `HCP`: `sveikatos priežiūros specialistas`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/E.%20sveikata/El._sveikatos_paslaugu_ir_bendradarbiavimo_infrastrukturos_IS/ESPBIISspecifikacija.pdf
- LSMU vartosena dėl `HFpEF` ir `HFrEF`: `širdies nepakankamumas su išlikusia / sumažėjusia išstūmio frakcija`  
  https://lsmu.lt/cris/entities/etd/894b2c78-446b-4a21-8afb-83ee0afaede2
- Santaros klinikų vartosena dėl `HIV`: `žmogaus imunodeficito virusas (ŽIV)`  
  https://www.santa.lt/naujienos/hepatitas-c-jau-galima-isvengti-kepenu-vezio-ir-cirozes/
- NVSC / SAM vartosena dėl `HPV`: `žmogaus papilomos virusas (ŽPV)`  
  https://nvsc.lrv.lt/lt/naujienos/svarbus-priminimas-tevams-pasirupinkite-vaiku-skiepais-dar-pries-prasidedant-mokslo-metams-cSG4/
- SAM / LSMU vartosena dėl `HVS`: `hiperventiliacijos sindromas`  
  remiasi jau validuotu termino įrašu `Hyperventilation Syndrome` ir LT medicinine vartosena

### I-J blokui faktiškai naudoti LT interneto šaltiniai

- SAM / Sveikatos mokslai vartosena dėl `IBS`: `dirgliosios žarnos sindromas (DŽS)`, angl. `IBS`  
  https://sam.lrv.lt/uploads/sam/documents/files/%21%21%E2%99%A52021%20SM5%28SAM_Internetas%29.pdf
- NVSC / oficiali santrumpų vartosena dėl `ICD`: LT dokumentuose vartojama `TLK – tarptautinė ligų klasifikacija`  
  https://nvsc.lrv.lt/uploads/nvsc/documents/files/VIRUSINIO%20HEPATITO%20A%20EPIDEMIOLOGIJOS%2C%20KLINIKOS%20IR%20PROFILAKTIKOS%20METODIN%C4%96S%20REKOMENDACIJOS.pdf
- LSMU kardiologinė vartosena dėl `ICD`: `implantuojamasis kardioverteris defibriliatorius (IKD)`  
  https://lsmu.lt/cris/entities/publication/7e8cf9a7-f717-48ce-9b40-416dedd756de
- SAM / neuroanesteziologinė vartosena dėl `ICP`: `intrakranijinis spaudimas`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Sveikatos_mokslai/Moksliniai_straipsniai%E2%80%93zurnalas_Sveikatos%20mokslai/2010m/2010SM_5VIdalisindd.pdf
- LSMU vartosena dėl `IHD`: `išeminė širdies liga`  
  https://lsmu.lt/cris/entities/publication/26645598-41b7-4688-af21-55eb76882f97
- LSMU vartosena dėl `IM`: `į raumenis`  
  https://lsmu.lt/cris/entities/etd/508f136e-d479-4a06-80f9-4c8343b5bcd1
- SAM / Sveikatos mokslai vartosena dėl `IN`: `intranazalinis vaistų skyrimo būdas`  
  https://sam.lrv.lt/media/viesa/saugykla/2025/4/HMtsoFlyAIE.pdf
- LSMU / Medas vartosena dėl `IVC`: `apatinė tuščioji vena`  
  https://medas.lsmu.lt/lt/kursas/1992763669
- LSMU diabetologinė vartosena dėl `IA`: `hipoglikemijos nejutimas`  
  https://lsmu.lt/cris/entities/publication/3d954eb3-0330-4807-9dca-e4d11e5baaa8
- VU / SAM vartosena dėl `JVP`: `padidėjęs jungo venų spaudimas`  
  https://sam.lrv.lt/media/viesa/saugykla/2025/4/HMtsoFlyAIE.pdf

### K-L blokui faktiškai naudoti LT interneto šaltiniai

- LSMU kardiologinė vartosena dėl `LBBB`: `kairiosios Hiso pluošto kojytės blokada`  
  https://lsmu.lt/cris/entities/publication/d8fc6bd9-8cb7-4013-a073-bedb6a7dc9cc
- VGTU biomechanikos / traumatologijos darbas dėl `LC`: `šoninio spaudimo sukelti lūžiai`; tame pačiame LT šaltinyje aprašoma ir dubens žiedo lūžių Young-Burgess klasifikacija  
  https://gs.elaba.lt/object/elaba%3A2144459/2144459.pdf
- E-TAR akušerinės formos vartosena dėl `LMP`: `paskutinių normalių mėnesinių data` / pirmosios paskutinių mėnesinių dienos logika  
  https://www.e-tar.lt/rs/legalact/3916e6203cf911efbdaea558de59136c/
- SAM metodinė vartosena dėl `LOC`: `sąmonės lygis`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Asmens_sveikatos_prieziura/Diagnostikos_metodikos_ir_rekomendacijos/Metodikos/galvos_smegenu_insulto_metodika.pdf
- gov.uk teisinis kontekstas dėl `LPA`: `Lasting Power of Attorney` kaip JK teisinis dokumentas  
  https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/211141/LPA117_property_and_financial_affairs_LPA.pdf
- LSMU / kardiologinė vartosena dėl `LVF`: `kairiojo skilvelio nepakankamumas`  
  https://lsmu.lt/cris/entities/publication/48a0ea4c-217a-4c31-b769-45fa88955f40
- LSMU kardiologinė vartosena dėl `LVSD`: `kairiojo skilvelio sistolinė disfunkcija`  
  https://lsmu.lt/cris/bitstream/20.500.12512/107759/2/66667688_MAIN.pdf

### M-N blokui faktiškai naudoti LT interneto šaltiniai

- SAM ir LSMU vartosena dėl `MAOI`: `monoamino oksidazės inhibitoriai` / `monoaminooksidazės inhibitoriai`  
  https://sam.lrv.lt/public/canonical/1740031268/27191/Nutukimo_gydymas_2024%20metodin%C4%97s%20rekomendacijos.pdf
- SAM / LSMU vartosena dėl `MAP`: `vidutinis arterinis kraujo spaudimas (MAP)`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Sveikatos_mokslai/Moksliniai_straipsniai%E2%80%93zurnalas_Sveikatos%20mokslai/2015m/2015%20SM4%28Online%29.pdf
- LSMU toksikologinė vartosena dėl `MDMA`: `3,4-metilenedioksimetamfetaminas`, `ekstazis (MDMA)`  
  https://lsmu.lt/cris/entities/publication/9e90a73c-c9ad-4749-8b97-cbf45625cfda
- LSMU vartosena dėl `MI`: `miokardo infarktas (MI)`  
  https://lsmu.lt/cris/entities/publication/1ed313f1-764d-4697-9cf7-f87d5a2b8a54/full
- Vidinė leidinio vartosena dėl `MTC`: 006 helper source eilutė klaidingai nurodyta kaip `Major Triage Centre`, tačiau 086 skyriuje vartojama `Major Trauma Centre`; traktuoti kaip helper source korekciją, ne LT termino promotion.
- LSMU vartosena dėl `NEWS`: `NEWS (angl. National Early Warning Score)` / `NEWS2` skalė  
  https://lsmu.lt/cris/entities/etd/fbd31011-69c3-4c2b-b4c1-2b79fc0b777f/full
- LSMU / SAM vartosena dėl `NLS`: `naujagimio gaivinimas`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Programos_ir_projektai/Sveicarijos_parama/Neonatologines_metodikos/Naujagimio%20gaivinimas.pdf
- SAM / LSMU vartosena dėl `NPA`: `nazofaringinis vamzdelis`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Sveikatos_mokslai/2022%20SM3%28Internetas%29.pdf
- LSMU vartosena dėl `NSAID`: `nesteroidiniai vaistai nuo uždegimo (NVNU)`  
  https://lsmu.lt/cris/entities/publication/8bc63f08-163e-46ec-be29-2579fe9a4cfd
- LSMU vartosena dėl `NSTEMI`: `miokardo infarktas be ST pakilimo`, originali `NSTEMI` santrumpa  
  https://lsmu.lt/cris/entities/etd/855e6443-ff0a-4efb-b0a0-c188b584c01e

### O-P blokui faktiškai naudoti LT interneto šaltiniai

- LSMU / VU vartosena dėl `OHCA`: `širdies sustojimas už ligoninės ribų` / `ne ligoninėje`  
  https://epublications.vu.lt/object/elaba%3A119278351/119278351.pdf
- SAM sunkios traumos metodika dėl `OPA`: `orofaringinis vamzdelis`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Asmens_sveikatos_prieziura/Metodiniai%20dokumentai/SUNKIOS%20TRAUMOS.pdf
- SAM / vaikų ligų metodinė vartosena dėl `ORS`: `oralinės rehidratacijos druskos`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Asmens_sveikatos_prieziura/20_%20Vaiku%20viduriu%20pokyciai.pdf
- SAM metodinė vartosena dėl `PE`: `plaučių embolija (PE)`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Programos_ir_projektai/Sveicarijos_parama/1%20knyga_%20Normalus%20n%C4%97%C5%A1tumas%20ir%20gimdymas.pdf
- LSMU / SAM vartosena dėl `PEF`: `didžiausias iškvėpimo srovės greitis`  
  https://lsmu.lt/cris/entities/publication/233d8eb2-6515-4330-9608-f8f33e6e95be
- LSMU kardiologinė vartosena dėl `PEA`: `elektrinis aktyvumas be pulso (anksčiau vadinta elektromechanine disociacija)`  
  https://lsmu.lt/cris/bitstream/20.500.12512/106194/2/ISBN9789955860051.pdf
- VU / neurologijos vartosena dėl `PNES`: `psichogeniniai neepilepsiniai priepuoliai`  
  https://www.zurnalai.vu.lt/neurologijos_seminarai/article/view/38295
- VU / LSMU vartosena dėl `PTSD`: `potrauminio streso sutrikimas`  
  https://lsmu.lt/cris/entities/publication/21e4f809-c61e-45d1-a3fe-70939f7060d9
- LSMU vartosena dėl `PPCI`: `pirminė perkutaninė koronarinė intervencija`, LT praktikoje trumpinama kaip `PKI`  
  https://lsmu.lt/cris/entities/publication/48a0ea4c-217a-4c31-b769-45fa88955f40
- SAM triage metodika dėl `PPE`: `asmens apsaugos priemonės`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Asmens_sveikatos_prieziura/16_%20Triage-rusiavimo%20metodika%202022-11-28.pdf
- LSMU akušerinė vartosena dėl `PPH`: `pogimdyminis kraujavimas`  
  https://lsmu.lt/cris/entities/publication/a60f0df5-7943-4888-a4b3-c96d848621a1

### Q-R blokui faktiškai naudoti LT interneto šaltiniai

- SAM / LSMU vartosena dėl `RBBB`: `dešiniosios Hiso pluošto kojytės blokada`  
  https://sam.lrv.lt/public/canonical/1728889289/26134/Kardiomiopatijos_galutinis.pdf
- LSMU ir Higienos instituto vartosena dėl `RCT`: `atsitiktinių imčių kontroliuojamas tyrimas`  
  https://lsmu.lt/cris/entities/publication/0fddc92a-46d0-4ddb-b973-ae0fe175064c
- LT gaivinimo vartosena dėl `ROSC`: `spontaninės kraujotakos atsinaujinimas`  
  https://lsmu.lt/cris/entities/etd/2492865d-db82-4dcf-8577-002c8f78cb67
- LT vaikų ligų ir infekcinių ligų vartosena dėl `RSV`: `respiracinis sincitinis virusas (RSV)`  
  https://lsmu.lt/cris/entities/publication/24d3d2f7-5f31-4cb8-a8ea-1eb7f823782d
- LT kardiologijos vartosena dėl `RVF`: `dešiniojo skilvelio nepakankamumas`  
  https://sam.lrv.lt/public/canonical/1728889289/26134/Kardiomiopatijos_galutinis.pdf
- LT akušerinė ir klinikinė vartosena dėl `RR`: `kvėpavimo dažnis`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Programos_ir_projektai/Sveicarijos_parama/1%20knyga_%20Normalus%20n%C4%97%C5%A1tumas%20ir%20gimdymas.pdf

### S blokui faktiškai naudoti LT interneto šaltiniai

- LSMU / vaikų ligų vartosena dėl `SBI`: `sunki bakterinė infekcija`  
  https://lsmu.lt/cris/entities/publication/61cc9c95-d558-4d25-9d0a-48c0a38b6ce9
- SAM traumų metodika ir LSMU neurochirurginė vartosena dėl `SCI`: `nugaros smegenų pažeidimas`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Asmens_sveikatos_prieziura/Metodiniai%20dokumentai/SUNKIOS%20TRAUMOS.pdf
- LT psichiatrijos ir farmakologijos vartosena dėl `SSRIs`: `selektyvieji serotonino reabsorbcijos inhibitoriai`  
  https://www.zurnalai.vu.lt/neurologijos_seminarai/article/view/40238
- LSMU / Santaros klinikų vartosena dėl `STEMI`: `miokardo infarktas su ST segmento pakilimu`  
  https://lsmu.lt/cris/entities/publication/3477386c-5551-444a-adfc-0baed8ffdac7
- SAM / LSMU vartosena dėl `SVT`: `supraventrikulinė tachikardija`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Sveikatos_mokslai/2022%20SM3%28Internetas%29.pdf
- LT monitoravimo vartosena dėl `SBP`, `SpO2`: `sistolinis arterinis kraujospūdis`, `deguonies įsotinimas`  
  https://lsmu.lt/cris/entities/etd/81a790c9-51aa-4cd7-9077-4ab3bea1255f

### T blokui faktiškai naudoti LT interneto šaltiniai

- LSMU neurointensyviosios terapijos vartosena dėl `TBI`: `trauminis galvos smegenų pažeidimas`, kartu su originalia `TBI` santrumpa  
  https://lsmu.lt/cris/entities/etd/754c3e6d-1e1e-41c3-a844-c9ff7d1dc2cb/full
- VU chirurginė vartosena dėl `TBSA`: `viso kūno paviršiaus plotas` nudegimų kontekste  
  https://www.journals.vu.lt/lietuvos-chirurgija/article/download/5332/3486/4118
- LSMU neurologinė vartosena dėl `TIA`: `praeinantis smegenų išemijos priepuolis`  
  https://lsmu.lt/cris/entities/publication/c85a0b65-5bc1-4488-82c7-bb94f3daeff3
- LSMU kardiologinė / sinkopių vartosena dėl `TLoC`: `trumpalaikis sąmonės netekimas`  
  https://lsmu.lt/cris/entities/publication/437f62c2-d358-429f-9ff3-9ab978f8f357

## 006 triage: U-V blokas (2026-03-29)

| Santrumpa | Originalas | LT sprendimas | Statusas | LT šaltinio kryptis | Pastaba |
| --- | --- | --- | --- | --- | --- |
| URTI | Upper Respiratory Tract Infection | lokaliai vartoti `viršutinių kvėpavimo takų infekcija` | localization_only | LT pediatrijos ir šeimos medicinos vartosena | Originali `URTI` santrumpa nekelta į `shared`; LT šaltiniuose aktyvesnė pilna forma ir `ŪVKTI`. |
| UTI | Urinary Tract Infection | lokaliai vartoti `šlapimo takų infekcija` | localization_only | LT pediatrijos, nefrologijos ir šeimos medicinos vartosena | Originali `UTI` santrumpa nekelta į `shared`; LT tekstuose dažnesnė pilna forma. |
| VF | Ventricular Fibrillation | skilvelių virpėjimas (VF) | approved_global | LT gaivinimo ir kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| VS | Vertical Shear | lokaliai vartoti `vertikalaus spaudimo sukelti lūžiai` / `vertikalus ir horizontalus dubens nestabilumas` pagal kontekstą | localization_only | LT dubens traumų klasifikacijos vartosena | Originali `VS` santrumpa nekelta į `shared`; LT šaltiniuose vartojami aprašomieji Young-Burgess ir AO C tipo klasifikacijos terminai. |
| VT | Ventricular Tachycardia | skilvelinė tachikardija (VT) | approved_global | LT kardiologijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |
| VTE | Venous Thromboembolism | venų tromboembolija (VTE) | approved_global | LT kraujagyslių, vidaus ligų ir akušerijos vartosena | Užrakinta `shared/lexicon/acronyms.tsv`. |

### U-V blokui faktiškai naudoti LT interneto šaltiniai

- LSMU vartosena dėl `URTI`: `ūminė viršutinių kvėpavimo takų infekcija (ŪVKTI)`  
  https://lsmu.lt/cris/entities/publication/7f5aaf5b-61df-4c1a-9058-fd2f4e629f51
- SAM metodinis dokumentas dėl `UTI`: `šlapimo takų infekcija` vaikų diferencinėje diagnostikoje  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Asmens_sveikatos_prieziura/19_%20Vaiku%20vemimas.pdf
- LSMU vartosena dėl `VF`: `skilvelių virpėjimas`  
  https://lsmu.lt/cris/entities/publication/f2d2128d-b3ce-45ef-9796-5aa648b5f3c0
- VGTU biomechanikos / traumatologijos darbas dėl `VS`: `vertikalaus spaudimo sukelti lūžiai` Young-Burgess klasifikacijoje  
  https://gs.elaba.lt/object/elaba%3A2144459/2144459.pdf
- LSMU vartosena dėl `VT`: `skilvelinė tachikardija`  
  https://lsmu.lt/cris/entities/publication/42b40013-8f9b-4153-a97b-392d2e02838d
- SAM metodika dėl `VTE`: `venų tromboembolija (VTE)`  
  https://sam.lrv.lt/uploads/sam/documents/files/Veiklos_sritys/Asmens_sveikatos_prieziura/Diagnostikos_metodikos_ir_rekomendacijos/Metodikos/VTEmetodika20150112galutine.pdf

## 006 triage: W-Z blokas (2026-03-29)

| Santrumpa | Originalas | LT sprendimas | Statusas | LT šaltinio kryptis | Pastaba |
| --- | --- | --- | --- | --- | --- |
| WHO | World Health Organisation | palikti tarptautinės organizacijos kontekste; LT forma `Pasaulio sveikatos organizacija (PSO)` | original_context_only | LT oficiali SAM vartosena | Originali `WHO` santrumpa nekelta į `shared`; LT vartosenoje aktyvi santrumpa `PSO`. |

### W-Z blokui faktiškai naudoti LT interneto šaltiniai

- SAM oficiali vartosena dėl `WHO`: `Pasaulio sveikatos organizacija (PSO)`  
  https://sam.lrv.lt/lt/veiklos-sritys/tarptautinis-bendradarbiavimas/tarptautines-organizacijos-1/pasaulio-sveikatos-organizacija-1/

## Tarpinė pažanga po A-D blokų

- Eilučių iš viso: `227`
- Jau padengta aktyvioje `shared` bazėje: `24`
- Dar nepadengta aktyvioje `shared` bazėje: `203`
- C-D bloke papildomai užrakinta į `shared/lexicon/acronyms.tsv`: `CBT`, `CCF`, `CES`, `CNS`, `CO`, `CO2`, `COPD`, `CPAP`, `CPR`, `CT`, `DM`, `DVT`
- C-D bloke sąmoningai nekelta į aktyvią bazę dėl dubletų ar JK konteksto: `CAMHS`, `CCS`, `CEW`, `CFR`, `CMHT`, `CMI`, `COP`, `CPN`, `CPP`, `CPR-IC`, `CRT`, `CSA`, `CSE`, `DBS`, `DC`, `DNA`, `DNACPR`, `DoLS`, `DPA`

## Tarpinė pažanga po A-F blokų

- Eilučių iš viso: `227`
- Jau padengta aktyvioje `shared` bazėje: `28`
- Dar nepadengta aktyvioje `shared` bazėje: `199`
- A-B blokas uždarytas pilnai; praleistų santrumpų nebėra.
- E-F bloke papildomai užrakinta į `shared/lexicon/acronyms.tsv`: `ECMO`, `EF`, `EtCO2`, `FBAO`
- E-F bloke sąmoningai nekelta į aktyvią bazę dėl LT santrumpų skirtumo, mnemonikos ar originalios EN santrumpos netinkamumo LT aktyviam sluoksniui: `ECG`, `ECT`, `ED`, `EDD`, `EOC`, `ERC`, `ESC`, `ET`, `FAST`, `FGM`, `FLACC`, `FII`

## Tarpinė pažanga po A-H blokų

- Eilučių iš viso: `227`
- Jau padengta aktyvioje `shared` bazėje: `34`
- Dar nepadengta aktyvioje `shared` bazėje: `193`
- G-H bloke papildomai užrakinta į `shared/lexicon/acronyms.tsv`: `GTN`, `HFpEF`, `HFrEF`, `HIV`, `HPV`, `HVS`
- G-H bloke sąmoningai nekelta į aktyvią bazę dėl LT santrumpų skirtumo, JK konteksto ar daugiareikšmiškumo: `g`, `GBS`, `GCS`, `GDPR`, `GP`, `GUM`, `HART`, `HCP`, `HME`, `HR`

## Tarpinė pažanga po A-J blokų

- Eilučių iš viso: `227`
- Jau padengta aktyvioje `shared` bazėje: `39`
- Dar nepadengta aktyvioje `shared` bazėje: `188`
- I-J bloke papildomai užrakinta į `shared/lexicon/acronyms.tsv`: `IBS`, `ICP`, `IHD`, `IVC`, `JVP`
- I-J bloke sąmoningai nekelta į aktyvią bazę dėl dubletų, LT santrumpų skirtumo, JK konteksto ar techninio prietaiso neaiškumo: `IA`, `ICD`, `ICE`, `ILCOR`, `IM`, `IMCA`, `IN`, `IO`, `IPAP`, `ITD`, `ITU`, `IV`, `J`, `JESIP`, `JRCALC`

## Tarpinė pažanga po A-L blokų

- Eilučių iš viso: `227`
- Jau padengta aktyvioje `shared` bazėje: `42`
- Dar nepadengta aktyvioje `shared` bazėje: `185`
- K-L bloke papildomai užrakinta į `shared/lexicon/acronyms.tsv`: `LBBB`, `LVF`, `LVSD`
- K-L bloke sąmoningai nekelta į aktyvią bazę dėl vienetų žymėjimo, JK konteksto ar nepakankamo LT pagrindo: `kg`, `kPa`, `LC`, `LMP`, `LOC`, `LPA`

## Tarpinė pažanga po A-N blokų

- Eilučių iš viso: `227`
- Jau padengta aktyvioje `shared` bazėje: `49`
- Dar nepadengta aktyvioje `shared` bazėje: `178`
- M-N bloke papildomai užrakinta į `shared/lexicon/acronyms.tsv`: `MAOI`, `MAP`, `MDMA`, `MI`, `NEWS`, `NLS`, `NSTEMI`
- M-N bloke sąmoningai nekelta į aktyvią bazę dėl vienetų žymėjimo, JK konteksto ar LT santrumpų skirtumo: `MBRRACE`, `MCA`, `mcg`, `mCPR`, `MECC`, `mg`, `MHA`, `MINAP`, `ml`, `mmHG`, `mmol`, `mmol/l`, `MOI`, `MSC`, `msec`, `MTC`, `NARU`, `NEET`, `NG`, `NHS`, `NICE`, `NPA`, `NPIS`, `NSAID`

## Tarpinė pažanga po A-P blokų

- Eilučių iš viso: `227`
- Jau padengta aktyvioje `shared` bazėje: `56`
- Dar nepadengta aktyvioje `shared` bazėje: `171`
- O-P bloke papildomai užrakinta į `shared/lexicon/acronyms.tsv`: `OHCA`, `OPA`, `ORS`, `PE`, `PEF`, `PEA`, `PNES`, `PTSD`
- O-P bloke sąmoningai nekelta į aktyvią bazę dėl vienetų žymėjimo, LT santrumpų skirtumo, JK konteksto ar nepakankamo LT pagrindo: `O2`, `OOH`, `P`, `PCO2`, `PEaRL`, `PEFR`, `PHECG`, `PPCI`, `PPE`, `PPH`, `PRESS`, `PSP`, `PV`

## Tarpinė pažanga po A-R blokų

- Eilučių iš viso: `227`
- Jau padengta aktyvioje `shared` bazėje: `61`
- Dar nepadengta aktyvioje `shared` bazėje: `166`
- Q-R bloke papildomai užrakinta į `shared/lexicon/acronyms.tsv`: `RBBB`, `RCT`, `ROSC`, `RSV`, `RVF`
- Q-R bloke sąmoningai nekelta į aktyvią bazę dėl LT santrumpų skirtumo, JK konteksto ar procedūrinio / operacinio pobūdžio: `ReSPECT`, `ROLE`, `RR`, `RTC`, `RVP`

## Tarpinė pažanga po A-S blokų

- Eilučių iš viso: `227`
- Jau padengta aktyvioje `shared` bazėje: `66`
- Dar nepadengta aktyvioje `shared` bazėje: `161`
- S bloke papildomai užrakinta į `shared/lexicon/acronyms.tsv`: `SBI`, `SCI`, `SSRIs`, `STEMI`, `SVT`
- S bloke sąmoningai nekelta į aktyvią bazę dėl mnemoninio pobūdžio, LT santrumpų skirtumo, parametro žymėjimo ar JK konteksto: `SARC`, `SBAR`, `SBP`, `SC`, `SCENE`, `SGA`, `SOB`, `SOBOE`, `SOCRATES`, `SOP`, `SORT`, `SpO2`

## Tarpinė pažanga po A-T blokų

- Eilučių iš viso: `227`
- Jau padengta aktyvioje `shared` bazėje: `68`
- Dar nepadengta aktyvioje `shared` bazėje: `159`
- T bloke papildomai užrakinta į `shared/lexicon/acronyms.tsv`: `TBI`, `TIA`
- T bloke sąmoningai nekelta į aktyvią bazę dėl LT santrumpų nestabilumo ar originalo konteksto: `TARN`, `TBSA`, `TLoC`

## Tarpinė pažanga po A-V blokų

- Eilučių iš viso: `227`
- Jau padengta aktyvioje `shared` bazėje: `71`
- Dar nepadengta aktyvioje `shared` bazėje: `156`
- U-V bloke papildomai užrakinta į `shared/lexicon/acronyms.tsv`: `VF`, `VT`, `VTE`
- U-V bloke sąmoningai nekelta į aktyvią bazę dėl LT santrumpų skirtumo ar nepakankamai stabilaus LT pagrindo: `URTI`, `UTI`, `VS`

## Tarpinė pažanga po A-Z blokų

- Eilučių iš viso: `227`
- Jau padengta aktyvioje `shared` bazėje: `75`
- Dar nepadengta aktyvioje `shared` bazėje: `152`
- Po papildomo `open` vienetų tikslinimo į `shared/lexicon/acronyms.tsv` dar papildomai užrakinta: `BiPAP`, `PEA`, `ATP`, `ITD`.
- W-Z bloke papildomai nieko neužrakinta į `shared/lexicon/acronyms.tsv`.
- `WHO` sąmoningai nekelta į aktyvią bazę, nes LT oficiali vartosena remiasi forma `Pasaulio sveikatos organizacija (PSO)`, o `X`, `Y`, `Z` source įrašų šiame skyriuje nėra.

## Atviros abejonės

- Iš aktyvioje `shared` bazėje nepadengtų `152` eilučių nemaža dalis jau sąmoningai palikta `localization_only` ar `original_context_only`; atvirai neišspręstų `open` statuso vienetų po papildomo `FGM`, `HME`, `IA`, `MTC`, `FII` ir `ITD` patikslinimo liko `2`.
- Dar atviri tik šie vienetai: `CMI`, `CPR-IC`.
- Dubletai (`CPP`, `CRT`, `CSE`, `ICD`, `IN`) jau išspręsti taip, kad LT žodyne abi reikšmės neliktų supainiotos.
- JK institucinės ir teisės santrumpos (`ADRT`, `DNACPR`, `DoLS`, `MCA`, `NICE`, `NHS`, `ReSPECT` ir kt.) turi būti atskirtos nuo aktyvios LT medicininės terminijos.

## Papildomas LT-source patikrinimas likusiems open vienetams (2026-03-29)

- `CMI`: papildomai tikrinta LT dubens traumų ir biomechanikos vartosena; patikimo kanoninio LT atitikmens `Combined Mechanical Injury` nerasta. Kol kas palikta `open`.
- `CPR-IC`: papildomai tikrinta LT gaivinimo ir ikihospitalinės medicinos interneto vartosena; patikimo kanoninio LT termino `CPR-induced consciousness` nerasta. Kol kas palikta `open`.
- `FII`: papildomai tikrinta LT vaikų apsaugos, pediatrijos ir sveikatos politikos vartosena; rasta pakankamas LT pagrindas lokaliam sprendimui `medicininė prievarta prieš vaikus`, aiškinant ryšį su `įgaliotojo asmens Miunhauzeno sindromu`. Į `shared` nekelta.
- `ITD`: papildomai tikrinta LT gaivinimo įrangos ir anesteziologijos vartosena; LSMU šaltinyje rastas kanoninis atitikmuo `įkvėpimo impedancinio slenksčio vožtuvas`, todėl vienetas perkeltas į `approved_global`.
- Likusiems dviem atviriems vienetams galioja ta pati taisyklė: kol nėra pakankamo LT interneto šaltinio pagrindo, nei į `shared`, nei į lokalų aktyvų sluoksnį jų nekelti.

## Finalus agento auditas

| Sritis | Statusas | Pastaba |
| --- | --- | --- |
| terminija | vykdoma | `A-Z` source santrumpų triage užbaigtas; po papildomo patikslinimo atviri liko tik `CMI` ir `CPR-IC`. |
| kolokacijos | ok | Tai santrumpų žodynas, ne naratyvinis skyrius. |
| gramatika | ok |  |
| semantika | vykdoma | Reikia tiksliai atskirti klinikines santrumpas nuo originalo JK konteksto ir mnemonikų. |
| norminė logika | vykdoma | JK organizacinės ir teisinės santrumpos negali būti automatiškai lokalizuotos kaip LT norminis sluoksnis. |
| atviros abejonės | yra | Likę du atviri vienetai: `CMI`, `CPR-IC`. |
