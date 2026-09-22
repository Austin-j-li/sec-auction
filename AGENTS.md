# AGENTS.md

This project turns the "Background of the Merger" section of an SEC merger filing into an Excel deal ledger, for research on informal and formal bidding in takeover auctions (Austin Li and Alex Gorbenko).

## If you are asked to extract a deal
- Follow `SEC_Deal_Ledger_Extraction_Instruction.md` exactly. Use only that instruction and the filing you are given in `raw_filing/`.
- Save the workbook in `extraction/` as `<deal>.xlsx`.
- Do not read `_dev/`, `ref/`, other workbooks in `extraction/`, or git history. They contain earlier analyses and the researcher's hand-coded answers, and reading them invalidates the extraction.
- Do not use the web. Do not identify anonymous bidders from outside knowledge.

## Layout
- `SEC_Deal_Ledger_Extraction_Instruction.md`: the working instruction (v1.13.2, frozen; further edits require Austin's approval).
- `raw_filing/`: filings to extract, fetched from EDGAR by `_dev/tools/fetch_filing.py`. `MANIFEST.csv` records each file's source link and SHA-256.
- `extraction/`: preserved canonical Opus originals: eight v1.13 runs and Datalink under v1.13.2. `_dev/cockpit/catalog.json` selects the newer v1.13.2 raw outputs and verified correction candidates stored under active review packets. Nine deals and twenty immutable Opus versions are retained; they are not all human-adjudicated or research-ready. Preserve raw outputs when a separate revision is authorized.
- `ref/`: Alex's collection instructions, voice notes and hand-coded deals. For evaluation only. `seed.csv` (built by `_dev/tools/make_seed.py`) lists each deal's filing link and holds no answers.
- `_dev/`: pipeline tools and current development guidance, not for extraction runs. Start with `_dev/HANDOFF.md`; use `_dev/RESEARCH_QUESTIONS.md` for pending conventions. Active Opus review packets support the cockpit; working edits live separately in ignored `_dev/cockpit/state/`. Retired Grok/Sol extraction results were deleted. The Astra experiment is retained only under `_dev/side-notes/`, excluded from the cockpit and current development plan. Older instruction history is in Git; see `_dev/CHRONOLOGY.md`. Never restore an old instruction into the checkout. Historical reports are evidence, not current instructions; v1.12-and-earlier rule numbers C1–C16 became E1–E14 in v1.13.

## If you are asked to work on the pipeline itself
- Read `_dev/HANDOFF.md` first.
- Astra handles design, reasoning and review; GPT Sol subagents handle code implementation and engineering execution. Claude Opus 5 high remains the extraction model; Astra is not the routine extractor because Austin considers it too expensive.
- Change the instruction only with Austin's approval, and run extractions only on his command. Change it only where the change is general (objective, work process, honesty about uncertainty, a repaired contradiction, a deletion); never add a rule justified by one reviewed deal.
- Comparison runs must be isolated: one instruction and one filing per sandboxed session (`_dev/tools/sandbox/run_model.py`; usage in `_dev/tools/README.md`). Run the checker after the run, never where the extracting agent can see it. Revision mode is a separate, explicitly requested pass that may see the selected workbook and findings.
- Checking is mechanical and offline. Delete run folders and other scaffolding once their results are recorded.
- Commit and push only when asked.
