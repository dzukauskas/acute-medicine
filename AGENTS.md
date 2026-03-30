Project agent rules for Acute Medicine.

Primary goal:
- Localize medical books into precise Lithuanian medical language for real clinical and educational use.
- Pagrindinis LT tekstas turi būti kuo artimesnis originaliam angliškam tekstui pagal prasmę, struktūrą ir sakinio funkciją.

Binding workflow:
- Treat `/Users/dzukauskas/Projects/Acute Medicine/books/README.md`, `/Users/dzukauskas/Projects/Acute Medicine/books/_template/workflow.md`, and `/Users/dzukauskas/Projects/Acute Medicine/books/_template/source-priority.md` as operational rules, not optional guidance.
- Follow `shared/` plus `*.local.tsv` rule architecture exactly.
- Never reactivate legacy `books/<slug>/*.tsv` active rule files.
- If any repo-local skill text conflicts with the binding workflow above, `AGENTS.md` plus the binding workflow files take precedence.

Source fidelity:
- Default to source-faithful translation, not free rewriting.
- Do not summarize, simplify, reorganize, or generalize the original unless the source is clearly non-transferable and the change is explicitly marked in research.
- Keep the original section logic, ordering, rhetorical function, and level of specificity whenever Lithuanian allows it.
- Localization is a constrained exception layer, not the default writing mode.
- UK-specific, market-specific, or legal-context content should usually stay in the LT text as original context, not be replaced with broad Lithuanian generalities.

Terminology rules:
- Never guess Lithuanian medical terminology.
- If an English medical term or abbreviation is not already locked in active shared/local lexicon files, verify it in Lithuanian sources before using it in translated output.
- Record the source and decision in the chapter research file.
- If the Lithuanian term cannot be locked confidently, treat it as a blocker or leave it in an explicit non-promoted status; do not improvise.

Automatic tool selection for this repo:
- Use `ebook-mcp` when EPUB structure, TOC, chapter segmentation, manifests, or embedded assets are unclear.
- Use `brave-search` first to discover Lithuanian medical sources or official terminology pages.
- Use `firecrawl` to crawl or extract from chosen Lithuanian domains such as `sam.lrv.lt`, `e-tar.lt`, `lsmu.lt`, `santa.lt`, `vlk.lt`, `nvsc.lrv.lt`, or similar.
- Use `browserbase` when the target site is dynamic, interactive, JS-heavy, or plain fetch/search is insufficient.
- Use `obsidian` to verify that synced chapters and figures really exist in the live vault when the repo mirror is not enough.
- Use `whimsical-desktop` for figure recreation and board-side editing, and keep repo PNGs synced from Whimsical artifacts.

Obsidian and sync safety:
- Never sync Obsidian output into the repo, a book root, or `lt/`.
- Treat sync destination validation failures as hard stops.

Working style:
- Advance chapter by chapter in order unless the user explicitly reprioritizes.
- Keep research, term triage, and QA green before moving on.
- If a translated chapter drifts too far from the original wording or structure, rewrite it toward the source rather than defending the localization.
- Treat book translation and repo engineering as separate workflows; use `docs/book-translation-workflow.md` for chapter work and `docs/repo-engineering-workflow.md` for system/tooling work.
- The agent should proactively decide whether the current request belongs in the same Codex thread or should start a new one, and state that recommendation briefly when a task boundary changes.
- Default thread routing:
  - same chapter or same blocker cluster in translation work -> stay in the same thread;
  - same technical theme in repo-engineering work -> stay in the same thread;
  - switching translation <-> repo engineering -> recommend a new thread;
  - switching to a different technical theme in repo-engineering work -> usually recommend a new thread;
  - use `Hand off` only when parallel worktree / branch isolation is actually useful.
- For repo-engineering work, keep `ENGINEERING_LEDGER.md` as the primary long-lived execution memory and update it when decisions or next steps materially change.
- When resuming repo-engineering work, read `ENGINEERING_LEDGER.md` before relying on thread history.
- Treat `handoffs/*.md` only as optional local scratch notes; they are not the primary or guaranteed cross-worktree memory mechanism.
