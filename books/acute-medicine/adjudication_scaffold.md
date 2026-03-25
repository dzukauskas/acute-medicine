# Targeted Adjudication Scaffold

Naudoti tik `high-risk` blokams iš `adjudication_pack`.

## Tikslas

Ne perrašyti viso skyriaus, o palyginti du mini variantus tam pačiam blokui:

- `Variant A`: maksimaliai kliniškai tikslus
- `Variant B`: natūralesnė LT medicininė proza

Galutinis pasirinkimas turi:

- išlaikyti klinikinę prasmę;
- remtis `chapter_pack`;
- laikytis `localization_overrides`;
- naudoti aktyvesnę LT sintaksę, jei tai nekeičia medicininės logikos;
- palikti trumpą sprendimo pėdsaką `research/<slug>.md` faile.

## Privalomi įėjimai

- `chapter_pack`
- konkretus `adjudication_pack`
- susiję `gold_examples`
- `language-style.md`

## Sprendimo disciplina

1. Pirmiausia tikrinkite, ar `Variant A` ir `Variant B` nekeičia klinikinės prasmės.
2. Jei abu kliniškai tinkami, rinkitės tą, kuris:
   - turi natūralesnes LT kolokacijas;
   - naudoja mažiau nominalizacijų;
   - turi trumpesnius, aiškesnius sakinius;
   - aiškiau atskiria LT praktiką nuo originalo konteksto.
3. Jei nei vienas netinka, parenkite trečią hibridinį variantą tik iš šių dviejų stipriausių dalių.
4. `research/<slug>.md` sekcijoje `## Adjudication sprendimai` užrašykite: `block_id`, pasirinktą variantą (`A`, `B` arba `hibridinis`) ir vienos eilutės priežastį.

## Kada taikyti

- algoritmams;
- JK→LT lokalizacijos callout'ams;
- hemodinaminiams ir kitokiems ilgų sąlyginių sakinių blokams.
