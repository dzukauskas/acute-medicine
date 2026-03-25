# Lithuanian Language Style

Šis failas apibrėžia projekto LT medicininės kalbos branduolį.

Tikslas: rašyti aiškų, idiomatiškai skambantį, studentiškai suprantamą ir Lietuvos medicinos vartosenai artimą tekstą, o ne pažodinį EN→LT vertimą.

## LT medicininės prozos branduolys

Pagrindiniai principai:

- kolokacijų pirmumas: rinktis lietuvių medicininei kalbai natūralius veiksmažodžio ir daiktavardžio junginius;
- nominalizacijų mažinimas: pirmenybė veiksmažodžiui, ne konstrukcijoms kaip `atlikti įvertinimą`, `vykdyti stebėjimą`, `atlikti korekciją`;
- valentingumo ir linksnių tikrinimas: veiksmažodis turi valdyti semantiškai tinkamą objektą ir linksnį;
- aktyvesnė sintaksė: vengti pasyvių, biurokratinių konstrukcijų, jei jas galima perrašyti aiškesne lietuviška forma;
- genityvų grandinių skaidymas: nepalikti trijų ar daugiau kilmininkų iš eilės, jei sakinį galima aiškiau pertvarkyti;
- temos–remos tvarka: sakinio pradžioje palikti tai, kas skaitytojui jau aišku, o naują informaciją perkelti vėliau;
- sakinio ritmo kontrolė: per ilgus, sąlygomis perkrautus sakinius skaidyti į du ar daugiau trumpesnių;
- aprašomasis tikslinimas: jei pažodinis terminas ar junginys skamba svetimai, rinktis LT kalbai natūralesnę aprašomąją formą.

Praktiškai tai reiškia:

- geriau `įvertinkite`, ne `atlikite įvertinimą`;
- geriau `stebėkite`, ne `vykdykite stebėjimą`;
- geriau `koreguokite`, ne `atlikite korekciją`;
- geriau `nuspręskite` ar `aptarkite`, ne `sprendimas turi būti priimamas`.

Jei kyla abejonių dėl termino, kolokacijos ar klinikinės kategorijos pavadinimo, jo negalima rinktis vien iš intuicijos. Pirma patikrinkite Lietuvos medicininę vartoseną internete, o tik tada fiksuokite formuluotę tekste ar `termbase`.

## Tipografija ir techninė rašyba

Projekte laikomos norminėmis šios taisyklės:

- dešimtainis skirtukas yra kablelis: `3,5`, ne `3.5`;
- tarp skaičiaus ir vieneto rašomas nepertraukiamas tarpas: `3,5 mg`, `94–98 %`, `35–45 mmHg`;
- intervalams naudojamas `–`, ne paprastas brūkšnelis `-`;
- neigiamoms reikšmėms naudojamas `−`, ne `-`;
- formulėse ir matmenyse naudojamas `×`, ne `x`;
- pagrindinė forma visada yra SI / ES vienetai.

## Anglų terminų rodymo politika

Anglų terminas rodomas ribotai:

- tik tada, kai jis realiai padeda orientuotis studentui ar klinikiniam skaitytojui;
- dažniausiai pirmą kartą, prie sudėtingesnio ar lengvai supainiojamo termino;
- ne antraštėse;
- ne beveik prie kiekvieno termino;
- nepaliekami keli `(angl. …)` toje pačioje trumpoje pastraipoje, jei to galima išvengti.

Prioritetas visada teikiamas lietuviškam medicininiam tekstui, o ne dvikalbei išklotinei.

Pozityvūs gero LT sprendimo pavyzdžiai laikomi `gold_phrases.tsv`. Jei ta pati formuluotė po review kartojasi kaip gera alternatyva, ji turi keliauti ten, o ne likti tik viename skyriuje.

Jei po review išryškėja geras viso bloko sprendimas, jis turi keliauti į `gold_sections/`, o ne likti tik konkretaus skyriaus pastraipoje.

## Terminų paaiškinimai studentui

Terminų blokai ir trumpi paaiškinimai naudojami tik tada, kai tai padeda mokymuisi:

- tankiuose, naujų sąvokų pilnuose skyriuose;
- sudėtinguose algoritmuose ar lentelėse;
- vietose, kur vien terminas be trumpo paaiškinimo būtų nepakankamai aiškus.

Pagal nutylėjimą terminų blokas nepridedamas prie kiekvieno poskyrio.

## Akronimai

Dažniausi projekto trumpiniai fiksuojami `acronyms.tsv`.

Akronimų taisyklės:

- svarbūs ar potencialiai dviprasmiai trumpiniai pirmą kartą turi būti išskleidžiami;
- dažnai medicinoje nusistovėję trumpiniai gali būti paliekami po pirmos pilnos formos;
- jei tas pats trumpinys gali reikšti skirtingus dalykus, sprendimas priimamas pagal klinikinį kontekstą, o ne mechaniškai.

## QA padalijimas

Automatizuoti tik tai, kas patikimai aptinkama:

- dažnos kalkės ir vertimo karkasai;
- tipografijos klaidos;
- perteklinis anglų terminų rodymas akivaizdžiais atvejais.

Rankiniam auditui palikti:

- kolokacijų natūralumą;
- genityvų grandinių aiškumą sudėtingesniais atvejais;
- temos–remos tvarką;
- semantiškai subtilias formuluotes.

Tokias subtilias formuluotes prieš galutinai paliekant reikia sutikrinti su Lietuvos medicinine literatūra internete, jei yra bent menkiausia abejonė, kad pasirinktas LT variantas gali būti nenusistovėjęs ar dirbtinis.

Jei tokia rankinė pataisa kartojasi, ji turi būti perkelta bent į vieną iš sluoksnių:

- `gold_phrases.tsv`
- `gold_sections/`
- `calque_patterns.tsv`
- `regression_examples/`
- `localization_overrides.tsv`

High-risk blokams, ypač hemodinaminėms pastraipoms, algoritmams ir UK→LT lokalizacijos callout'ams, galima naudoti `adjudication_pack`, bet žmogaus review vis tiek lieka patvirtinimo vartais.
