# Handoff (20 September 2026)

**Working instruction:** `SEC_Deal_Ledger_Extraction_Instruction.md`, v1.8 lean, patched (Re-entered label, round-rule fix). 22-column ledger; sheets Deal ledger, Rounds, Deal facts, Questions.

**Canonical extraction:** the three workbooks in `extraction/` are the Claude Opus 5 (high) runs from the blind model comparison of 19 September. They are the only extraction kept in the working tree. Opus scored 96.4/100 against 87.1 (GPT-5.6-Sol) and 86.6 (DeepSeek); see `_dev/model_comparison/COMPARISON.md` and the per-deal `grading/` notes for the corrections each workbook still needs. They are not yet research-ready.

**What is in `_dev/`:**
- `tools/check_lean.py`: mechanical checker for the lean workbook (structure, consistency, quotations found in the filing). Run it after an extraction, never where the extracting agent can see it. `tools/sandbox/` holds the scripts that run one isolated extraction per deal (bubblewrap; paths are for the Ubuntu laptop).
- `model_comparison/`: report, rubric, scores, and per-deal source reference and scoring notes.
- `jev_checker/`: TypeSafe's Jev model as a cheap second reader of finished ledgers. **Start with `jev_checker/README.md`**: what Jev is in plain words, what three rounds of experiments found, and the decisions Austin and the assistant reached (keep Jev a checker, merge it with the mechanical script into one command and one report, then try a revision loop). The `RESULTS_round*.md` files have the detail.
- `OPEN_QUESTIONS_for_Alex.md`: convention questions awaiting Alex.
- `docs/claude_memory/`: copy of the assistant's project memory.
- `CHRONOLOGY.md`: what was done when, and which commit holds the removed material.

**Next:** build the merged checker described in `jev_checker/README.md`; test on unseen deals (Penford, sTec; filings needed); put the open questions to Alex.
