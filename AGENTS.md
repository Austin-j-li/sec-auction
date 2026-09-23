# AGENTS.md

This project turns the "Background of the Merger" section of an SEC merger filing into an Excel deal ledger, for research on informal and formal bidding in takeover auctions (Austin Li and Alex Gorbenko).

## If you are asked to extract a deal
- Follow `SEC_Deal_Ledger_Extraction_Instruction.md` exactly. Use only that instruction and the filing you are given in `raw_filing/`.
- Save the workbook in `extraction/` as `<deal>.xlsx`.
- Do not read `_dev/`, `ref/`, other workbooks in `extraction/`, or git history. They contain earlier analyses and the researcher's hand-coded answers, and reading them invalidates the extraction.
- Do not use the web. Do not identify anonymous bidders from outside knowledge.

## Layout
- `SEC_Deal_Ledger_Extraction_Instruction.md`: the working instruction (v1.13.2, frozen). Agents edit it only with Austin's approval. Once the cockpit app's instruction editor exists, Austin and Alex may version instructions there (see below).
- `raw_filing/`: filings to extract, fetched from EDGAR by `_dev/tools/fetch_filing.py`. `MANIFEST.csv` records each file's source link and SHA-256.
- `extraction/`: the current blind extractions, made by Claude Opus 5.5 at medium effort under v1.13.2 on 22 September (`_dev/reviews/2026-09-22-opus55-reextraction/`; the replaced Opus 5 high workbooks are archived outside the checkout and recoverable from Git at `03d59b1`). `_dev/cockpit/catalog.json` holds one immutable version per deal, these nine extractions, which are unreviewed and not research-ready. Earlier Opus 5 drafts and correction passes remain only as evidence in their review packets. Preserve raw outputs when a separate revision is authorized.
- `ref/`: Alex's collection instructions, voice notes and hand-coded deals. For evaluation only. `seed.csv` (built by `_dev/tools/make_seed.py`) lists each deal's filing link and holds no answers.
- `_dev/`: pipeline tools and current development guidance, not for extraction runs. Start with `_dev/HANDOFF.md`; use `_dev/RESEARCH_QUESTIONS.md` for pending conventions. Active Opus review packets support the cockpit; working edits live separately in ignored `_dev/cockpit/state/`. Retired Grok/Sol extraction results were deleted. The Astra experiment is retained only under `_dev/side-notes/`, excluded from the cockpit and current development plan. Older instruction history is in Git; see `_dev/CHRONOLOGY.md`. Never restore an old instruction into the checkout. Historical reports are evidence, not current instructions; v1.12-and-earlier rule numbers C1–C16 became E1–E14 in v1.13.

## If you are asked to work on the pipeline itself
- Read `_dev/HANDOFF.md` first.
- For engineering, pick models by task: Astra for hard design and review (strong but expensive, sometimes erratic), Sol for well-specified implementation, Opus 5.5 or Fable 5.1 for design, implementation and integration. Claude Opus 5.5 at medium effort is the default extraction model (22 September effort sweep, `_dev/reviews/2026-09-22-opus55-sol6-sweep/`).
- The cockpit is being extended into a shared extraction app; the approved spec is `_dev/COCKPIT_APP_SPEC.md` (23 September). In that app, Austin and Alex may each add deals and start extractions on their own subscription, choosing Opus 5.5, Fable 5.1, GPT-6-Sol or GPT-6-Astra at any allowed effort, and may create, run and publish instruction versions and change the default (frozen versions never change). Each app action is attributed to the person who takes it.
- Outside the app, an agent changes the instruction only with Austin's approval and runs extractions only on his command. Building or testing the app does not authorize a real model run. Change it only where the change is general (objective, work process, honesty about uncertainty, a repaired contradiction, a deletion); never add a rule justified by one reviewed deal.
- Comparison runs must be isolated: one instruction and one filing per sandboxed session (`_dev/tools/sandbox/run_model.py`; usage in `_dev/tools/README.md`). Run the checker after the run, never where the extracting agent can see it. Revision mode is a separate, explicitly requested pass that may see the selected workbook and findings.
- Checking is mechanical and offline. Delete run folders and other scaffolding once their results are recorded.
- Commit and push only when asked.
