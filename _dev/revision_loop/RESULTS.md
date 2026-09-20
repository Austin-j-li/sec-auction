# Revision loop, first trial (20 September 2026)

**Question.** If the merged checker's findings are handed back to the extractor for one revision pass, does the workbook get better?

**Set-up.** One sandboxed Claude Opus 5 (high) session per deal (`_dev/tools/sandbox/run_model.py prepare --revise-from ... --report ...`). The session sees the instruction, the filing, the finished workbook and the checker's findings as plain text (`_dev/tools/findings_text.py`), nothing else. It is told that "certain" findings come from exact rules and "model judgment" findings are often wrong, to change only what a finding shows to be a real error, and to write `revision_notes.md` with a decision on every finding. Three existing Opus workbooks were revised; Penford was first extracted blind (17 minutes), then revised. Revision passes took 4 to 9 minutes each.

## What happened

| Deal | Findings (certain / Jev) | After revision | Jev findings acted on | Ledger rows added or removed | Core cells changed (event, price, date, party) |
|---|---|---|---|---|---|
| Mac-Gray | 18 / 3 | 0 / 3 | 0 of 3 | 0 | 0 |
| PetSmart | 14 / 1 (a row Jev could not check) | 1 / 0 | 0 | 0 | 0 |
| Providence | 17 / 3 | 0 / 3 | 0 of 3 | 0 | 0 |
| Penford (unseen) | 82 / 6 | 0 / 6 | 0 of 6 | 0 | 0 (58 Round cells changed from text to number) |

- **Every mechanical finding was cleared.** Flag and "Rows affected" links were made consistent, over-long Questions were cut to length, over-long Accounts trimmed.
- **On Penford the mechanical checker caught a real defect on an unseen deal:** the whole Round column was written as text, which also broke the Rounds sheet link and the process count (61 errors, one cause). The revision fixed it.
- **No Jev finding led to a change, on any deal.** The extractor checked each against the filing and the instruction and wrote a reasoned refusal. It did not add trivial rows to satisfy flags, which was the main worry.
- **Nothing correct was broken** in the ledger. No row added, removed or re-priced.

## Against the known corrections (grading notes, the three graded deals)

| Deal | Known corrections | Fixed | Partly | Not touched |
|---|---|---|---|---|
| Mac-Gray | 8 | 0 | 0 | 8 |
| PetSmart | 4 | 0 | 1 (C-E3: the wrong p. 26 citation went when Q3 was shortened) | 3 |
| Providence | 7 | 1 (C-E3: the speculative Class I alternative went when Q3 was shortened) | 1 (C-E1: "never mentioned after March" became "not named after the April memorandum") | 5 |

The two and a half fixes are side effects of shortening Questions, not of any finding pointing at the error. The checker does not see the kinds of error the graders found (exit reasons, date bounds, conditions, adviser rows, unsupported qualifiers), so the loop cannot fix them.

- **Mac-Gray voting agreements** (Jev 0.96, and a graded omission, B-VOTING): the extractor refused, correctly noting that C2 asks for no separate row and that row #48's Note already mentions the agreements. The grader wanted the 27 September entry date folded into that Note. The flag pointed at the right place, the revision did not make that small edit.
- **Penford Jev price flags:** rows 42 and 52 are false alarms (the quotation states the recorded price exactly; the three-paragraph window also contains the other $19.00 / $18.50 figure). Row 46 (Party A "any offer would be below $17.50 - $18.00") is a real judgment call; the extractor kept its reading with reasons and the row already carries a Question.

## Things to watch

- **Shortening Questions loses content.** Cutting 130 words to 80 removed alternatives and page citations. Twice that removed an error; it could as easily remove something the reviewer needs.
- **Warnings can be silenced instead of fixed.** For "Rows affected cites a row without the flag", the extractor sometimes added the flag and sometimes deleted the citation. Providence Q1 no longer lists #40-46 although its text still discusses #44-52. Its reasons were stated each time, but the checker cannot tell the two apart.
- One observation outside the findings was reported and correctly left alone: PetSmart Deal facts "Number of processes" holds the date 01/01/1900 instead of 1. The mechanical checker missed it.

## Reading

The loop is a cheap, safe clean-up of form: it reliably clears mechanical findings and did no damage in four deals. It does not improve substance, because nothing in the findings points at the substantive errors, and the extractor (rightly) will not act on a bare model judgment. Whether it is worth running depends on whether clean form saves Austin and Alex checking time. Improving substance needs findings of a different kind (for example a second strong model reviewing exit reasons, date bounds and conditions), not more passes of this loop.

Small checker improvements suggested by this trial: catch a number field holding a date; widen or narrow the Jev price window so a neighbouring offer's price does not trigger "different price"; consider reporting "citation removed" separately when comparing rounds.

## Addendum, same day: sTec, and an independent grader

**sTec (unseen), same loop.** Blind Opus extraction 16 minutes, revision 6 minutes. Findings 19 certain / 5 Jev; after revision 0 / 5; Jev findings acted on 0 of 5; no ledger row added or removed. The Jev step at first skipped the deal because the section after the Background is headed "sTec's Reasons for the Merger"; `jev_pass.py` now accepts a company-name prefix on that heading.

**Against Alex's voice notes** (they cover Penford and sTec, so neither deal is truly unseen by the instruction). Penford: agrees on all 8 points; one wrinkle, the 8 October returned draft is also coded Formal (raised as Q4). sTec: agrees on 7 of 8; the miss is core: the workbook has one process, Alex sees two (contact gap November 2012 to February 2013), and no Question raises it.

**Independent grader.** The revised sTec workbook went to one clean-slate GPT-6 Astra session (xhigh) in the same bubblewrap sandbox, seeing only the instruction, the filing and the workbook, told to write its own timeline from the filing before opening the workbook. 24 minutes; workbook hash unchanged; result in `reports/stec.astra_grade.md`. It reported 7 core, 2 minor and 1 ambiguous finding, each with row, quoted passage, rule and proposed change; the quoted passages were spot-checked and are in the filing. Core: WDC's 17 April addendum to an existing NDA coded as "NDA signed"; Conditions = Heavy unsupported on two preliminary bids (C14); a duplicate Company B contact row with an invented date window; first contacts for WDC, E, F and G missing while subtracted from the 18; Company H's catch-up presentation only in a Note; cost-reduction projections given to WDC alone on 19 June (p. 46, outside the Background); Wells Fargo, WDC's financial adviser, missing. None of these was seen by the checker or Jev. Astra **agreed with one process**, so it did not find Alex's main point. The findings are not yet adjudicated by a person and were not fed back to the extractor.

## Files

- `reports/<deal>.round0.json|md`: checker report and the findings text handed to the revision. `round1.json`: checker on the revised workbook. `<deal>.diff.txt`: every changed cell (`_dev/tools/diff_workbooks.py`).
- `runs/<deal>_revise1/extraction/`: revised workbook and `revision_notes.md`. `runs/penford_extract/`: the blind Penford extraction. Each run folder has its prompt, metadata with input hashes, and the full session log.
- Penford has no graded reference, so its substance is unscored.
