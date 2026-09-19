# Jev (TypeSafe) experiments on the nine comparison workbooks — 19 September 2026

**Status.** Review experiments only. No extraction was run, no workbook and no instruction text was changed. Jev 1.13.0 read the nine finished workbooks in `_dev/model_comparison_2026-09-19/workbooks/` against the three filings. Ground truth is the blind grading in that folder (`grading/*/work/output/grade/scores.json`) plus errors I planted. 1,588 calls, 2.16M input tokens, about **$0.09**, median latency 0.27 s. Every request and response is in `raw/`. The API key is not stored in the repo.

Small sample: three development deals, nine workbooks, 422 located ledger rows. Thresholds below are illustrations, not tuned settings.

## Experiment A — does the quoted passage support the row? (`exp_rows.py`)

For each row the code finds the quoted paragraph in the filing (422 of 436 quotes located; DeepSeek's unquoted style is the weak spot) and sends it with two paragraphs either side. Jev answers narrow questions; code compares the answers with the ledger cells.

| Check | On original rows | On planted errors | Verdict |
|---|---|---|---|
| **Price** — "does the passage give $X for this party?" | 2 of 105 flagged; both are Providence Party B `Bid reaffirmed` rows (Opus 47, DeepSeek 46) whose Note says the $24 is carried from an earlier row, so the passage rightly lacks it | 105 of 105 shifted prices caught; 103 of 105 rows with the bidder swapped caught | **Works.** |
| **All cash** — Choice Yes / No / Not stated | 59 of 61 agree. The two disagreements are exactly Sol's Providence CVR rows 34–35, the graded B03 error (cash CVR coded No) | — | **Works**; found a real graded error with no false flags. |
| **Exit reason** — Choice over the nine C16 reasons | 30 of 56 agree. The 26 disagreements include all graded exit-reason errors: Mac-Gray Party B "Terms or process" in all three workbooks (grader: Not stated), and DeepSeek PetSmart row 25 "Not stated" (grader: would not improve). That is 4 graded errors in 26 flags, about 15% precision. The other 22 are rows the grader accepted, mostly "Lower offer than rivals", which needs the wider story, not the passage. Confidence does not separate them: true hits range 0.71–0.97, false ones 0.45–1.0 (Providence Party D is contradicted at 1.0 in all three workbooks and the grader accepted it) | — | **A review queue only** (about 3 rows per workbook, most of them fine), never a verdict. |
| **Exit reported or inferred** | 7 rows marked Inferred = Y where Jev reads the exit as stated in words. Two are confirmed (DeepSeek Providence rows 34–35, though the graded P07 error covers four rows and Jev missed the other two); two are known false (Opus 46 and Sol 49, Party E exits the grader accepted as inferred); three are unadjudicated. 16 rows not marked inferred where the passage does not state the exit; most are correct by convention (Not selected at signing) | — | **Weak.** 2 right, 2 wrong, 3 unknown. |
| **Exit label** | Agrees on only 26 of 56 original rows | 50 of 56 swapped labels contradicted | **Too noisy,** and it missed the one graded label error (Sol Providence row 53, Dropped by target 0.50 against Not selected at signing 0.42). The labels depend on C16 conventions and on context beyond the passage. |
| **Actor / event fits the label** (generic Nouls) | 55–63 of 422 flagged at 0.5 | 65 of 105 swapped actors caught | **Too noisy** on cohort rows and inferred rows. Drop. |

## Experiment B — is every event in the filing in the ledger? (`exp_coverage.py`)

Stage 1 tags each Background paragraph with eight event kinds. Stage 2 shows Jev the paragraph and the ledger rows quoted within five paragraphs of it, and asks whether each tagged kind is recorded.

- Tagging is reliable where tested: the paragraphs behind the graded omissions score 0.9 or more on the right kind (voting agreement 0.97, exclusivity extension 0.96, deadlines 0.94–0.97). The Providence August 4 reaffirmation is the exception at 0.59, a returned draft rather than an explicit bid.
- The coverage score carries signal but does not separate cleanly. On nine known omission paragraphs, workbooks that omit the event average 0.36 and workbooks that record it average 0.63; an omitting workbook scores below a recording one in 153 of 182 pairs. The Mac-Gray September 27 voting agreement, missed by all three models, scores 0.05–0.12. Two cases fail: the Providence April 7 Class I contacts and the August 4 reaffirmation show no difference.
- Queue size tracks graded quality. Paragraphs scoring under 0.2: Opus 5 across three deals, DeepSeek 18, Sol 21, the same order as the blind scores. Under 0.5 the queue is a third to two thirds of all tagged paragraphs, too long to save review time.
- Not testable here: buyer-bank advisers in the merger agreement annex (outside Background), round boundaries, bidder counts, sort-date rules. These are most of the graded point losses and are not passage-level questions.

## Proposed changes (none applied)

1. **Add a Jev pass to the checker, outside the extraction sandbox.** A new `_dev/tools/jev_check.py` beside `check_ledger.py`, running price against passage and All cash against passage as checks, and exit reason against passage as a low-priority reading list (about 15% of its flags were real errors here). Output is a list of rows for the reviewer, never an edit. Cost is about one cent per workbook and a few seconds.
2. **Hold the "exit reported in words?" check** until it is tested on more deals; on this sample it is as often wrong as right.
3. **Add an omission shortlist** limited to coverage below 0.2, sorted lowest first, with the paragraph text. On these nine workbooks that is 0–16 paragraphs each, and it puts the voting-agreement omission at the top. Treat it as a reading aid; it misses events and the threshold is untested on new deals.
4. **Do not use Jev** for exit labels, generic "is this row right" checks, rounds, counts or dates. Keep those with the checker's arithmetic and the human review.
5. **Quotation format.** 12 of the 14 unlocated quotes are DeepSeek cells written without outer quotation marks; where the filing text itself contains a quoted defined term (“Party C”), my parser takes that term as the quotation. The text is copied correctly, so this is fixable in the checker's parser and needs no instruction change. The other two are the Simpson Thacher notice address on p. A-46, outside Background. If Austin prefers, section D could also require outer quotation marks; no wording drafted.
6. **Before adopting any of this**, repeat A and B on the unseen deals (Penford, sTec) once they have graded workbooks, pin `jev-1.13.0`, and run the same narrow questions through a cheap generative model as a control. That comparison was not done here.

## Files

`lib.py` (paragraphs, quote location, cached API calls), `exp_rows.py`, `analyze_rows.py`, `exp_coverage.py`, `results_rows.json`, `results_coverage.json`, `raw/` (one JSON per call). Rerun with `TYPESAFE_API_KEY` set; cached calls are not repeated.
