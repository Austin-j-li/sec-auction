# TypeSafe round 3: the two proposed checks, run on the real workbooks — 19 September 2026

**Status.** Review experiments only. No extraction was run; no workbook, instruction or checker was changed. Jev 1.13.0 (pinned) read the nine graded workbooks in `_dev/model_comparison_2026-09-19/workbooks/` against the three filings. 1,836 calls, 2.71M input tokens, about **$0.11** at the documented $0.042 per million, median latency 0.43 s. Every request and response is in `raw/`; the API key is in no file.

**Why this round.** Round 1 (`jev_experiments_2026-09-19`) ran on real rows but planted only easy price errors. Round 2 (`typesafe_followup_2026-09-19`) found the hard error (the same bidder's price from another event) and a fix, but on hand-written cases. Round 2 also showed row-or-`none` matching works when the event is supplied by hand. Round 3 asks whether both survive contact with the real workbooks, with every question built by code from ledger columns and filing text.

## P. Event-scoped price check on the 105 real priced rows (`exp_price.py`)

The question is built from `Who`, `When`, `Event`, the two price cells, and the row's position among that party's priced rows (for example "proposal 2 of 2 that this party made on that date"). The Note is left out because it often restates the price. The passage is the quoted paragraph plus two either side. Answers: `supported` / `contradicted` / `insufficient`. Planted errors: the same party's price from another of its rows (92 rows have one) and another party's price quoted within two paragraphs (93). Control: round 1's actor-only Noul in the same request.

| Check | 105 original rows | 92 same-party swaps | 93 near-party swaps |
|---|---|---|---|
| Round 1 actor-only Noul (flag if below 0.5) | 2 flagged | **67 caught, 25 missed** | 93 caught |
| Event-scoped Choice, ±2 paragraphs | 0 `contradicted`, 5 `insufficient` | **92 caught** | 93 caught |
| Same, window pulled back to the nearest dated paragraph | 2 `contradicted`, 4 `insufficient` | 92 caught | 93 caught |
| Same, eight paragraphs before (an accident of a regex bug, kept as evidence) | 6 `contradicted`, 3 `insufficient` | 92 caught | 93 caught |

- Round 2's result holds on real rows: the old question passes 27% of same-party swaps; the scoped question passes none. Lowest confidence on any planted catch was 0.56.
- The five `insufficient` originals: two are the Providence Party B `Bid reaffirmed` rows (Opus 47, DeepSeek 46), where the $24 is carried from an earlier row. That is the right answer and the same two rows round 1 flagged. The other three are one event in three workbooks: Providence Party E's late-July $21.26 LOI, a bullet with no date of its own, at confidence 0.07–0.17 (the three options near a third each). A false flag, but a visibly unsure one.
- **A wider passage makes it worse, not better.** More paragraphs bring in the party's other offers, and Providence Party C's $19.30 LOI (its earlier IOI was $21) turns into a false `contradicted` at up to 0.91. Keep ±2.
- No original row was called `contradicted` at ±2, so no real price error was found. The graded price-category deductions I read (a missing reaffirmation row, the CVR coded as non-cash) are not wrong numbers, so I know of no real wrong-price row in these workbooks. This run therefore shows a low false-flag rate and a high catch rate on planted swaps; it does not show a catch of a real price error.

## O. Omission discovery at sentence level (`exp_omit.py`)

Round 1's paragraph-level coverage score could not separate omitting from recording workbooks cleanly, and failed outright on the Providence April 7 Class I contacts. Here the unit is the sentence. Code splits the 438 sentences of the paragraphs round 1 tagged; Jev tags each sentence with the same eight event kinds (176 tagged); then, per tagged sentence and workbook, Jev selects the ledger row that records it (rows quoted within five paragraphs are the options), or `none`, or `not_an_event`. 528 selection calls.

Against the graded omissions that are sentence-sized events in Background:

| Graded omission | Graded as missing in | Result |
|---|---|---|
| Mac-Gray Sept 24–27 MacDonald voting agreements | all three | `none` at 0.96 / 0.97 / 0.97 |
| Mac-Gray CSC full data-site access | Sol, DeepSeek | `none` 0.99, 0.97; Opus matched to its exclusivity row |
| Mac-Gray 50-party outreach Contact | DeepSeek | `none` 0.79; Opus and Sol matched |
| Providence two Class I contacts by April 7 | Sol | `none` 0.93; Opus and DeepSeek matched their row 11 at 1.00 |
| Mac-Gray committee formation at initiation (Transaction Committee sentence) | Sol | `none` 0.90; Opus 0.72 and DeepSeek 0.84 also `none` on this sentence, so not cleanly separated |
| Providence Party B August 4 reaffirmation | Sol | **missed**: the returned-draft sentence is not tagged as a bid (as in round 1) |
| PetSmart unnamed June adviser | DeepSeek | **missed** at face value: matched to row 3 at only 0.36 (Opus 0.90 on its row) |
| PetSmart November projections update | all three | **missed**: matched to the admission rows the grader called partial coverage |

Five of eight found, with the right workbooks separated in four of the five, including the case round 1 could not do. Not testable this way: buyer-bank advisers in the annex, `Deadline reached` rows, missing Questions, note-level caveats, round boundaries and counts. Those remain most of the graded point losses.

Queue size, `none` answers per workbook (all / confidence ≥ 0.75 / ≥ 0.9):

| | Opus | Sol | DeepSeek |
|---|---|---|---|
| Mac-Gray (82 tagged sentences) | 9 / 3 / 2 | 23 / 10 / 6 | 21 / 10 / 4 |
| PetSmart (45) | 2 / 0 / 0 | 12 / 7 / 2 | 5 / 1 / 0 |
| Providence (49) | 5 / 1 / 0 | 8 / 2 / 1 | 7 / 2 / 0 |

At ≥ 0.9 the queue is 15 sentences across nine workbooks, against round 1's 44 paragraphs under its 0.2 cut. I checked all 15 by keyword search of the workbooks (my reading, not blind grading): in every case the event is indeed absent from the ledger text. They split as: seven graded omissions (voting agreements ×3, CSC full access ×2, Class I contacts ×1, Sol's Mac-Gray committee formation ×1); three are the Mac-Gray committee recommendation or board approval of October 14, which C2 lets an extractor fold into signing; two are Mac-Gray management presentations of August 8 and 14 (Sol and DeepSeek have no row or note for them; ungraded, I think real); Sol's PetSmart has no row or note for the June 18 ad hoc committee formation (the phrase appears only inside two quotation cells); and two are minor (the agreed $11 million fee, the Longview December 9 meetings). So at this cut the flags are accurate about absence, and the reviewer decides materiality.

## Proposed changes (none applied)

1. **Build `_dev/tools/jev_check.py`, run after extraction and outside the sandbox, beside `check_ledger.py`.** Read-only; writes a review list, never edits a cell. Two passes:
   - **Price pass.** Question text exactly as in `exp_price.py::questions` (`scoped`), passage ±2 paragraphs, Note excluded. Report `contradicted` rows first. Report `insufficient` rows separately with their confidence, and mark as expected those whose Event is `Bid reaffirmed` or whose Note says the price is carried. A confidence cut does not sort these: the three false flags sit at 0.07–0.17 but one of the two correct carry-forward answers is at 0.45, so show the number and let the carried-price rule do the sorting. On these nine workbooks that is 0 `contradicted` and 5 `insufficient` (2 expected, 3 low-confidence false flags): under one row per workbook to look at. Replace round 1's actor-only price question; it is shown here to pass a quarter of same-bidder mix-ups.
   - **Omission pass.** Sentence tagging and row-or-`none` selection as in `exp_omit.py`. List `none` at confidence ≥ 0.9 as "probably absent", 0.75–0.9 as a second tier, each with the sentence and page. That is 0–6 sentences per workbook at the top tier here. This replaces round 1's proposal 3 (paragraph coverage below 0.2). Two caveats for the build: sentences are examined only inside paragraphs that the round 1 paragraph tagger scored above 0.5, so on a new deal that tagging is stage 0 of the checker, its cut is untested, and an event in an untagged paragraph is invisible; and the sentence splitter needs more abbreviations (it split at "5 p.m." and cut a sentence at "among other." here, without changing a conclusion).
   - Cost for both passes is about one to two cents and under a minute per workbook.
2. **Keep round 1's All-cash check** as proposed there; nothing here changes it. Keep exit labels, generic row checks, rounds, counts and dates out of Jev, as before.
3. **Two known blind spots to cover by other means.** A reaffirmation made by returning a draft is not recognised as a bid event, so the Providence August 4 kind of omission needs the checker's own rule (a party with a live bid at a deadline and no row in that round). Low-confidence matches (the PetSmart June adviser at 0.36) suggest a third tier, "matched but unsure", which I have not evaluated.
4. **No instruction change.** Nothing here points at the instruction. The only extraction-side note is round 1's: DeepSeek's unquoted cells are harder to locate, and unlocated rows get neither check.

## Limits, stated plainly

- Same three development deals as rounds 1 and 2. The gate both earlier rounds set, a test on unseen deals (Penford, sTec) with graded workbooks, still cannot be met because those workbooks do not exist. The 0.9 and 0.75 cuts were read off this data and are not validated.
- No generative-model control was run; this key covers TypeSafe only. A cheap LLM may do as well on the same questions.
- Planted price errors are swaps of real prices. They are harder than round 1's but still synthetic; there were no real price errors in these workbooks to catch.
- The omission truth set is seven graded events; the audit of the 15 top-tier flags is my keyword check, not Alex's or a blind grader's. Whether an absent event matters under C2 is a research judgment the tool does not make.
- One run, no repeats; run-to-run variation was not measured.

## Files

`exp_price.py` (set `LEADIN=1` for the dated-lead-in window), `exp_omit.py`, `analyze.py`, `results_price.json`, `results_price_leadin.json`, `results_price_wide8.json`, `results_omit.json`, `results_omit_sentences.json`, `raw/`. The scripts import round 1's `lib.py` and reuse its paragraph tags. Rerun with `TYPESAFE_API_KEY` set in the environment; cached calls are not repeated. `analyze.py` needs no key.
