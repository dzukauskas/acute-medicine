# Terminology Source Priority

Use this order when choosing Lithuanian medical terminology.

## 1. Official Lithuanian institutional terminology

First choice:

- Lietuvos Respublikos terminų bankas
- Lietuvos Respublikos sveikatos apsaugos ministerijos metodikos, įsakymai, aprašai
- Valstybinės greitosios medicinos pagalbos / gaivinimo / skubiosios pagalbos metodikos, if available for the term

Use these when the term is procedural, regulatory, or already standardized in Lithuanian practice.

## 2. Established Lithuanian clinical usage

Second choice:

- Lithuanian medical textbooks
- peer-reviewed Lithuanian medical journals
- university teaching materials from Lithuanian medical schools

Use these when there is no clearly approved term in official terminology sources.

## 3. IATE / EU terminology

Third choice:

- IATE

Use this as a controlled multilingual reference, especially when Lithuanian public-sector terminology exists there.

## 4. English source meaning

Only after checking the above:

- infer the concept from the English source
- translate the concept, not the word shape

Never accept a term only because it is a close-looking literal rendering from English.

## Decision rule

For every important term, store one of these statuses in the termbase:

- approved
- preferred
- provisional
- banned

`approved` means backed by official Lithuanian terminology or national guidance.
`preferred` means strong Lithuanian clinical usage but not yet formally approved in this project.
`provisional` means acceptable for now but must be rechecked later.
`banned` means a calque, awkward literalism, or otherwise misleading wording.

## Completion gate

No chapter should be treated as finished until both are true:

- it follows [translation-style.md](/Users/dzukauskas/Projects/Acute%20Medicine/study/translation-style.md)
- `scripts/terminology_guard.py` passes cleanly
