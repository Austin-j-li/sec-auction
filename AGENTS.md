# AGENTS.md

This project turns the "Background of the Merger" section of an SEC merger filing into an Excel deal ledger, for research on informal and formal bidding in takeover auctions (Austin Li and Alex Gorbenko).

## If you are asked to extract a deal
- Follow `SEC_Deal_Ledger_Extraction_Instruction.md` exactly. Use only that instruction and the filing you are given in `raw_filing/`.
- Save the workbook in `extraction/` as `<deal>.xlsx`.
- Do not read `_dev/`, `ref/`, other workbooks in `extraction/`, or git history. They contain earlier analyses and the researcher's hand-coded answers, and reading them invalidates the extraction.
- Do not use the web. Do not identify anonymous bidders from outside knowledge.

## Layout
- `SEC_Deal_Ledger_Extraction_Instruction.md`: the working instruction (v1.9 lean).
- `raw_filing/`: filings to extract, fetched from EDGAR by `_dev/tools/fetch_filing.py`. `MANIFEST.csv` records each file's source link and SHA-256.
- `extraction/`: finished ledgers. The Claude Opus 5 workbooks here are the only canonical extraction.
- `ref/`: Alex's collection instructions, voice notes and hand-coded deals. For evaluation only. `seed.csv` (built by `_dev/tools/make_seed.py`) lists each deal's filing link and holds no answers.
- `_dev/`: development history, not for extraction runs. Start with `_dev/HANDOFF.md`. It holds the ledger checker and sandbox scripts, the blind model comparison that selected the Opus extractions, the Jev checker experiments and a copy of the assistant's project memory. Older material is in git history; see `_dev/CHRONOLOGY.md`.

## If you are asked to work on the pipeline itself
- Read `_dev/HANDOFF.md` first.
- Change the instruction only with Austin's approval, and run extractions only on his command.
- Comparison runs must be isolated: one instruction and one filing per sandboxed session (`_dev/tools/sandbox/sandbox_run.sh`). Run the checker after the run, never where the extracting agent can see it.
- Commit and push only when asked.
