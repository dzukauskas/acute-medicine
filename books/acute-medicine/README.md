# Acute Medicine

Šis katalogas yra vienintelė aktyvi darbo vieta knygai *Acute Medicine: A Practical Guide to the Management of Medical Emergencies*.

## Struktūra

- `source/pdf/`: kanoninis PDF.
- `source/chapters-en/`: iš PDF ištraukti angliški skyriai tik navigacijai ir sutikrinimui.
- `source/index/`: skyriaus indeksai ir puslapių intervalai.
- `lt/chapters/`: naujai nuo nulio rašomi lietuviški skyriai.
- `lt/figures/`: lietuviškos schemos ir paveikslai.
- `lt/figures/manifest.tsv`: aktyvių paveikslų kanoninių `Whimsical` šaltinių registras.
- `chapter_packs/`: chapter-specific preflight paketai, kurie privalomai įkeliami prieš drafting.
- `adjudication_packs/`: high-risk blokų pre-second-pass paketai.
- `research/`: skyriaus šaltinių ir sprendimų failai.
- `review_deltas/`: struktūriniai rankinio review skirtumai, naudojami taisyklių promavimui.
- `regression_examples/`: trumpi „blogai → gerai“ pavyzdžiai būsimiems promptams ir regresijų kontrolei.
- `archive/`: knygos vidinis archyvas, jei prireiktų tarpinių ar atmestų variantų.
- `workflow.md`: kanoninis šios knygos darbo workflow.
- `language-style.md`: kanoninės LT medicininės prozos, tipografijos ir anglų terminų rodymo taisyklės.
- `acronyms.tsv`: dažniausių projekto trumpinių registras.
- `gold_phrases.tsv`: pozityvių LT medicininės prozos pavyzdžių sluoksnis.
- `gold_sections/`: pozityvių LT blokinio lygmens etalonų sluoksnis.
- `localization_overrides.tsv`: UK ar kito originalo konteksto perrašymo į LT praktiką registras.
- `adjudication_profiles.tsv`: high-risk blokų adjudication profiliai.
- `adjudication_scaffold.md`: targeted adjudication sprendimo disciplina.

## Taisyklė

Skyrių tekstas, lentelės, schemos ir paveikslai kuriami nuo naujo tik iš PDF ir naujausių patikrintų Lietuvos bei, jei reikia, Europos šaltinių.

Ankstesnio workflow artefaktai pašalinti; aktyvus pagrindas yra tik šis katalogas.

Diagramoms ir algoritmams šiame projekte naudojamas tik `Whimsical` workflow. Jei vartotojas nurodo konkretų įrankį, jo negalima savavališkai pakeisti kitu. Jei `Whimsical` kelias šioje sesijoje neveikia, darbas stabdomas ir aiškiai įvardijamas blokatorius, o ne tyliai pereinama į kitą įrankį.

Aktyviame `lt/figures/manifest.tsv` leidžiamas tik `whimsical_board`; ad hoc `svg_file`, `excalidraw_file` ar kiti pakaitiniai kanoniniai šaltiniai nelaikomi galiojančiais.

Jei kyla abejonių dėl LT termino, kolokacijos ar klinikinės kategorijos pavadinimo, prieš pasirenkant formuluotę privaloma patikrinti Lietuvos medicininę vartoseną internete ir tą patikrą užfiksuoti `research` faile.

Kalbinei kokybei naudojamas dviejų sluoksnių `Language QA`:

- `scripts/prose_guard.py` gaudo dažnas kalkes ir vertimo karkasus;
- `scripts/lt_style_guard.py` tikrina LT tipografiją, intervalų rašybą, tarpus tarp skaičių ir vienetų bei akivaizdžiai perteklinį anglų terminų rodymą.
- `scripts/terminology_guard.py` aktyviai tikrina terminus ir akronimus iš `termbase.tsv`, `acronyms.tsv` ir, jei pateiktas, `chapter_pack`.

Draftinimas nuo šiol nelaikomas pilnu be šių artefaktų:

1. `research/<slug>.md`
2. `chapter_packs/<slug>.yaml`
3. `adjudication_packs/<slug>.yaml`, jei `chapter_pack` turi `adjudication_candidate`
4. LT skyriaus drafto
5. `review_deltas/<slug>.tsv`, jei skyrius jau buvo per rankinį auditą
