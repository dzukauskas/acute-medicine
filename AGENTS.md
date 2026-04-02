Project agent rules for Acute Medicine.

Primary goal:
- Localize medical books into precise Lithuanian medical language for real clinical and educational use.
- Pagrindinis LT tekstas turi būti kuo artimesnis originaliam angliškam tekstui pagal prasmę, struktūrą ir sakinio funkciją.

Passive repo context index:
- repo_purpose | precise Lithuanian medical book localization for clinical and educational use
- workflow_modes | book-translation | repo-engineering
- static_passive_context | AGENTS.md | books/README.md | docs/codex-workflow.md | docs/book-translation-workflow.md | docs/repo-engineering-workflow.md | books/_template/workflow.md | books/_template/source-priority.md
- canonical_rule_base | AGENTS.md + binding workflow docs
- translation_durable_state | research/<slug>.md | chapter_packs/<slug>.yaml | term_candidates.tsv | lt/chapters/<slug>.md | adjudication_packs/<slug>.yaml | lt/figures/*
- repo_engineering_durable_state | ENGINEERING_LEDGER.md
- thread_history | not canonical; checkpoint state into canonical workflow artifacts before compact or new thread
- skill_precedence | AGENTS.md + binding workflow docs override conflicting repo-local skill text
- tool_layers | machine-level preferred tools when available | repo-local bootstrap guaranteed tools are the tracked minimum
- translation_qa | rerunnable pipeline via scripts/run_chapter_qa.py | not a stored machine-readable receipt
- thread_routing | same chapter or blocker cluster stays in one translation thread | same technical theme stays in one repo-engineering thread | switching modes or themes => recommend new thread | Hand off only for real parallel branch/worktree isolation

Binding workflow:
- Treat repo-relative `books/README.md`, `books/_template/workflow.md`, and `books/_template/source-priority.md` as operational rules, not optional guidance.
- Follow `shared/` plus `*.local.tsv` rule architecture exactly.
- Never reactivate legacy `books/<slug>/*.tsv` active rule files.
- If any repo-local skill text conflicts with the binding workflow above, `AGENTS.md` plus the binding workflow files take precedence.

Source fidelity:
- Default to source-faithful translation, not free rewriting.
- Do not summarize, simplify, reorganize, or generalize the original unless the source is clearly non-transferable and the change is explicitly marked in research.
- Keep the original section logic, ordering, rhetorical function, and level of specificity whenever Lithuanian allows it.
- Localization is a constrained exception layer, not the default writing mode.
- Source-faithful after LT/EU normalization means preserving the original meaning, structure, rhetorical role, and detail level, not preserving foreign-market normativity in the main LT prose.
- UK-specific, market-specific, or legal-context content cannot remain in the main LT text as if it were a Lithuanian / ES norminis standartas.
- If such source context is worth retaining, keep it only in an explicitly marked `Originalo kontekstas` block and record the reasoning in `research`.

Terminology rules:
- Never guess Lithuanian medical terminology.
- If an English medical term or abbreviation is not already locked in active shared/local lexicon files, verify it in Lithuanian sources before using it in translated output.
- Record the source and decision in the chapter research file.
- If the Lithuanian term cannot be locked confidently, treat it as a blocker or leave it in an explicit non-promoted status; do not improvise.

Automatic tool selection for this repo:
- Machine-level preferred tools when available:
  - Use `ebook-mcp` when EPUB structure, TOC, chapter segmentation, manifests, or embedded assets are unclear.
  - Use `brave-search` first to discover Lithuanian medical sources or official terminology pages.
  - Use `firecrawl` to crawl or extract from chosen Lithuanian domains such as `sam.lrv.lt`, `e-tar.lt`, `lsmu.lt`, `santa.lt`, `vlk.lt`, `nvsc.lrv.lt`, or similar.
  - Use `browserbase` when the target site is dynamic, interactive, JS-heavy, or plain fetch/search is insufficient.
  - Use `obsidian` to verify that synced chapters and figures really exist in the live vault when the repo mirror is not enough.
  - Use `whimsical-desktop` for figure recreation and board-side editing, and keep repo PNGs synced from Whimsical artifacts.
- Repo-local bootstrap guaranteed tools:
  - Tracked repo bootstrap/setup guarantees only `context7`, `pdf-reader`, `excalidraw`, `playwright`, and `whimsical-desktop`.
  - Treat `ebook-mcp`, `brave-search`, `firecrawl`, `browserbase`, and `obsidian` as wider machine-level tooling unless they are installed separately.

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
- If a thread may compact or a new thread may start, first write the current state into the canonical artifacts for the active workflow; thread history is not the durable checkpoint.
- For repo-engineering work, keep `ENGINEERING_LEDGER.md` as the primary long-lived execution memory and update it when decisions or next steps materially change.
- In normal paired repo-engineering work, the agent should update `ENGINEERING_LEDGER.md` proactively; the user should not need to run the ledger updater manually.
- When resuming repo-engineering work, read `ENGINEERING_LEDGER.md` before relying on thread history.
- Treat `handoffs/*.md` only as optional local scratch notes; they are not the primary or guaranteed cross-worktree memory mechanism.
