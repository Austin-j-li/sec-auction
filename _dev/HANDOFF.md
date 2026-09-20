# Handoff (20 September 2026)

**Working instruction:** `SEC_Deal_Ledger_Extraction_Instruction.md`, v1.9 lean (20 Sep: adopted provisionally from `_dev/OPEN_QUESTIONS_recommendations_2026-09-20.md`, all but Q3 and Q7; the three canonical workbooks were made under v1.8 and are not yet updated). 22-column ledger; sheets Deal ledger, Rounds, Deal facts, Questions.

**Canonical extraction:** the three workbooks in `extraction/` are the Claude Opus 5 (high) runs from the blind model comparison of 19 September. They are the only extraction kept in the working tree. Opus scored 96.4/100 against 87.1 (GPT-5.6-Sol) and 86.6 (DeepSeek); see `_dev/model_comparison/COMPARISON.md` and the per-deal `grading/` notes for the corrections each workbook still needs. They are not yet research-ready.

**What is in `_dev/`:**
- `tools/check_lean.py`: the checker for the lean workbook. Mechanical checks always (structure, consistency, quotations found in the filing); with `TYPESAFE_API_KEY` set it adds Jev's model judgments (`tools/jev_pass.py`: prices that look contradicted, events that look missing) to the same report. Run it after an extraction, never where the extracting agent can see it. `tools/sandbox/` holds the scripts that run one isolated extraction per deal (bubblewrap; paths are for the Ubuntu laptop).
- `tools/make_seed.py` builds `ref/seed.csv` from Alex's workbook (390 deals, identifying columns only; 21 rows marked for review). `tools/fetch_filing.py <deal>` fetches a filing on demand into `raw_filing/` and records it in `raw_filing/MANIFEST.csv`; `--verify` re-checks every file against EDGAR. It cuts the document out of the submission text file because EDGAR now adds a tracking script to served HTML pages. Tender offers (SC TO-T, 34 deals) are not handled yet.
- `model_comparison/`: report, rubric, scores, and per-deal source reference and scoring notes.
- `jev_checker/`: TypeSafe's Jev model as a cheap second reader of finished ledgers. **Start with `jev_checker/README.md`**: what Jev is in plain words, what three rounds of experiments found, and the decisions Austin and the assistant reached (keep Jev a checker, merge it with the mechanical script into one command and one report, then try a revision loop). The `RESULTS_round*.md` files have the detail.
- `revision_loop/`: first trial of the revision loop (20 September): checker findings handed back to Opus for one pass on the three workbooks and on a blind Penford extraction. **Read `revision_loop/RESULTS.md`.** Short version: it clears every mechanical finding and breaks nothing, but fixes almost none of the graded substantive errors, and the extractor refused every Jev finding. `tools/sandbox/run_model.py` now runs on the VM and has a revise mode; `tools/findings_text.py` and `tools/diff_workbooks.py` support it.
- `OPEN_QUESTIONS_for_Alex.md`: convention questions awaiting Alex.
- `docs/claude_memory/`: copy of the assistant's project memory.
- `CHRONOLOGY.md`: what was done when, and which commit holds the removed material.

**Next:** set the merged checker's flags against the grading notes for the three workbooks; test on unseen deals (Penford, sTec; filings fetched 20 September); the revision-loop experiment (needs Austin's go-ahead); put the open questions to Alex.
