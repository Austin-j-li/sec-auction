# Handoff (20 September 2026)

**Working instruction:** `SEC_Deal_Ledger_Extraction_Instruction.md`, v1.8 lean, patched (Re-entered label, round-rule fix). 22-column ledger; sheets Deal ledger, Rounds, Deal facts, Questions.

**Canonical extraction:** the three workbooks in `extraction/` are the Claude Opus 5 (high) runs from the blind model comparison of 19 September. They are the only extraction kept in the working tree. Opus scored 96.4/100 against 87.1 (GPT-5.6-Sol) and 86.6 (DeepSeek); see `_dev/model_comparison/COMPARISON.md` and the per-deal `grading/` notes for the corrections each workbook still needs. They are not yet research-ready.

**What is in `_dev/`:**
- `tools/check_lean.py`: mechanical checker for the lean workbook (structure, consistency, quotations found in the filing). Run it after an extraction, never where the extracting agent can see it. `tools/sandbox/` holds the scripts that run one isolated extraction per deal (bubblewrap; paths are for the Ubuntu laptop).
- `model_comparison/`: report, rubric, scores, and per-deal source reference and scoring notes.
- `jev_checker/`: three rounds of experiments with TypeSafe's Jev model as a second reader. Read `RESULTS_round3.md` first. Proposal, not yet built: merge a price check and a missing-event check into the checker. The scripts here need the comparison workbooks and cached API responses, which are in git history only (see `CHRONOLOGY.md`).
- `OPEN_QUESTIONS_for_Alex.md`: convention questions awaiting Alex.
- `docs/claude_memory/`: copy of the assistant's project memory.
- `CHRONOLOGY.md`: what was done when, and which commit holds the removed material.

**Next:** build the merged checker; test on unseen deals (Penford, sTec; filings needed); put the open questions to Alex.
