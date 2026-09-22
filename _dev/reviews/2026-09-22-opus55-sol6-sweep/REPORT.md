# Opus 5.5 and GPT-6-Sol extraction sweep: report

22 September 2026. The design is in `PROTOCOL.md` and the departures from it are in `AMENDMENT.md`. The main departure: at Austin's instruction the sweep ran one replicate, 12 cells rather than 24. Every effort result below is therefore a direction from one run per deal, not a measured effect.

## Verdict

- **Opus 5.5: medium effort.**
  - Going from medium to high effort bought no reliable quality gain. High never beat medium by more than 2 points on two of three deals, which is the protocol's bar for the higher effort. That held with the frozen grades, with each grader family alone, and when every disputed grade was resolved against medium.
  - Which effort has the higher mean depends on disputed grades: 93.5 against 92.5 as frozen, 93.7 for high against 92.75 for medium in the worst case. So the evidence is "no gain from high", not "medium is better".
  - Medium used 11% fewer output tokens and cost 11% less.
- **GPT-6-Sol: xhigh effort.**
  - Xhigh beat high by more than 2 points on Mac-Gray (+13.1) and Synacor (+6.4), 91.1 against 84.3 on the mean. That held with each grader family alone and when every disputed grade was resolved in high's favour.
  - It rests on two single-run gaps. Sol high's Mac-Gray run was the lightest of all 12 runs.
- **Opus 5.5 medium or GPT-6-Sol xhigh: no quality difference this sweep can resolve.**
  - Opus medium led by 2.4 points on the frozen grades. The lead falls to 1.6 after the grader splits are settled and to 1.3 in the worst case. It is smaller than the up-to-5.5-point disagreement between grader families on single workbooks.
  - Opus medium won Datalink and Synacor in every scenario and lost Mac-Gray.
  - Sol xhigh wrote 61% fewer output tokens. Austin chose Opus for now (22 September, after this report).

All 12 runs completed on the first attempt. None needed a continuation or a retry. No run issued a network-capable shell command, or made any web, connector (MCP) or subagent call, in its event log.

## Scores

Scores are out of 100 against the frozen reference tests, as frozen before unblinding. Each is the family-balanced grade: the mean of two blind Claude Opus 5.5 graders, averaged with one blind GPT-6-Astra grader. There is one workbook per arm and deal.

| Arm | Mean | Datalink | Mac-Gray | Synacor | Claude graders | Astra |
|---|---|---|---|---|---|---|
| `opus-5-5-medium` | **93.50** | 92.50 | 93.50 | 94.50 | 94.25 | 92.75 |
| `opus-5-5-high` | 92.54 | 88.50 | 93.88 | 95.25 | 92.50 | 92.58 |
| `gpt-6-sol-xhigh` | 91.13 | 87.13 | 97.88 | 88.38 | 91.58 | 90.67 |
| `gpt-6-sol-high` | 84.25 | 86.00 | 84.75 | 82.00 | 85.58 | 82.92 |

### The decision rule, applied

The protocol prefers the higher effort only if it beats the lower effort by more than the larger of 2 points and the pooled replicate spread, on at least two of three deals. With one replicate there is no spread, so the threshold is 2 points.

| Provider | Higher minus lower: Datalink | Mac-Gray | Synacor | Deals above 2 points | Result |
|---|---|---|---|---|---|
| Opus 5.5 (high − medium) | −4.00 | +0.38 | +0.75 | 0 | medium |
| GPT-6-Sol (xhigh − high) | +1.13 | +13.13 | +6.38 | 2 | xhigh |

### Sensitivity: disputed grades and grader families

After unblinding, independent checks re-read the grades that drive the comparisons. Changing frozen grades once the arms are known would bias the result, so the primary scores above stand. This table shows what the disputes would do.

| Scenario | Opus high − medium (by deal) | Opus result | Sol xhigh − high (by deal) | Sol result | Opus medium − Sol xhigh (mean) |
|---|---|---|---|---|---|
| A. Frozen grades (primary) | −4.00, +0.38, +0.75 | medium | +1.13, +13.13, +6.38 | xhigh | +2.38 |
| B. The three grader splits settled | −4.00, +0.38, +3.00 | medium | +1.13, +10.88, +6.38 | xhigh | +1.63 |
| C. B, plus every contested reference item resolved for the arm that lost it | −0.50, +0.38, +3.00 | medium | −1.88, +9.38, +3.38 | xhigh | +1.29 |
| Frozen, Claude graders only | −3.50, −0.25, −1.50 | medium | +0.25, +9.75, +8.00 | xhigh | +2.67 |
| Frozen, Astra only | −4.50, +1.00, +3.00 | medium | +2.00, +16.50, +4.75 | xhigh | +2.08 |

Deals are in the order Datalink, Mac-Gray, Synacor.

- **B.**
  - *SY-R05, Opus medium's Synacor workbook.* Astra's fail is correct under the frozen rubric. The test requires the round-3 Rounds line to list Company H as a participant, and the workbook lists H as "contact only, not admitted". The two Claude graders passed it because H's non-entry is scored under another test, which the prompt ruled out. The score moves from 94.50 to 92.25, and the Opus mean from 93.50 to 92.75.
  - *MG-R08 and MG-B05, Sol high's Mac-Gray workbook.* The Claude passes are the better grades. Astra is right that Party A's 09/18 reiteration has no priced Bid row, but MG-B05 tests only for invented bids and MG-R08 only for misassigned rounds. The same omission is already penalised under four other tests (MG-B03, MG-F02, MG-F06, MG-F07).
- **C.**
  - DA-P06: an 8–12 financial non-submitter range is credited for Opus high and Sol high. The reference's 8–9 assumes that every unnamed financial bidder was among the contacted sponsors, a membership the filing does not state.
  - SY-R01 passed for Sol high: it separated the final process correctly and lost the test only by making the Company B talks a fourth process, which the reference itself leaves unscored.
  - MG-F04 at partial for Sol high.
  - DA-P08 at partial for Sol xhigh.

  The references for DA-R11, DA-P08 and MG-P04 were checked against the filings and instruction rules E10, E14 and Part B and hold as written. The misses on them are patterns shared within one model family, not reference errors.

## Where points were lost

The table gives points lost across the three deals, 300 points in all, by test category. The maximum for each category is three times its per-deal weight.

| Arm | Participation (of 90) | Rounds (of 75) | Formality and conditions (of 60) | Chronology (of 30) | Bids and prices (of 30) | Deal facts (of 15) | Total lost |
|---|---|---|---|---|---|---|---|
| `opus-5-5-medium` | 7.25 | 8.00 | 0.00 | 4.25 | 0.00 | 0.00 | 19.50 |
| `opus-5-5-high` | 10.25 | 4.63 | 3.00 | 4.50 | 0.00 | 0.00 | 22.38 |
| `gpt-6-sol-xhigh` | 13.13 | 1.88 | 2.75 | 8.88 | 0.00 | 0.00 | 26.63 |
| `gpt-6-sol-high` | 16.50 | 10.00 | 11.50 | 7.50 | 1.75 | 0.00 | 47.25 |

- **Sol high against xhigh on Mac-Gray: a light run and a few different readings.**
  - The Sol high Mac-Gray workbook is complete: four sheets, 56 ledger rows, a chronology through the 10/15/2013 announcement, and a clean exit. But it was the lightest of all 12 runs. It took 401 s and wrote 6,904 reasoning tokens, against xhigh's 612 s and 12,549. On Datalink and Synacor, Sol high reasoned as much as xhigh or more.
  - About 7 of the 13.1-point gap trace to one choice spread across six tests: recording Party A's 09/18 best-and-final reiteration as a non-bid rather than a priced Bid.
  - Another 3 points come from rating CSC/Pamplona's conditions Unclear rather than Heavy despite its exclusivity requests (MG-F04).
- **Sol high elsewhere.** On Synacor it coded the 2018–19 Company B merger-of-equals talks as a separate process, giving four processes where the test accepts three or two (SY-R01, contested above).
- **Patterns shared within a model family, stable across effort:**
  - Both Opus arms recorded Datalink Party C's unchanged 10/04/2016 reaffirmation as a new Bid row (DA-R11, 3 points each). Rule E10 allows no new Bid row for an unchanged confirmation.
  - Both Opus arms gave a caveated but over-precise single closure for Mac-Gray's 16 unnamed financial signers (MG-P04, partial).
  - Both Sol arms gave Datalink's Party A a definite individual exit, although its membership among the advancers is uncertain (DA-P08, 2 points each).
  - All four arms lost points on Datalink's non-submitter cohort ranges (DA-P06, contested above).
- **Convention-dependent tests.** These rest on conventions that are still open. They account for 8.50 of Opus medium's 19.50 lost points, 9.00 of Opus high's 22.38, 8.88 of Sol xhigh's 26.63 and 18.50 of Sol high's 47.25.

## Cost, tokens, time and checker

Figures are means per workbook over the three deals.

| Arm | Output tokens (of which thinking) | Input tokens (cached share) | List cost | Wall time |
|---|---|---|---|---|
| `opus-5-5-medium` | 93,489 (64,151) | 2.08 M (92%) | $3.63 | 861 s |
| `opus-5-5-high` | 105,479 (72,669) | 2.16 M (91%) | $4.06 | 965 s |
| `gpt-6-sol-xhigh` | 36,042 (16,409) | 1.83 M (94%) | not reported | 719 s |
| `gpt-6-sol-high` | 33,740 (15,465) | 2.20 M (96%) | not reported | 677 s |

- **Cost.**
  - Opus cost is repriced at list prices: $4 and $20 per million input and output tokens, $0.20 per million cache reads, $8 per million one-hour cache writes. The repriced figure equals the CLI's own.
  - The 6 Opus runs cost $23.07 at list price.
  - Runs are billed to the subscription, and Codex reports no cost, so the two providers' costs are not comparable.
- **Wall time.** Wall time is confounded with load, so compare tokens instead. The cut to 12 cells and the later restart ran the Datalink and Mac-Gray cells of the higher-effort arms early, with about 4 runs going at once. The lower-effort arms ran later, under 6 to 8. Token counts are not affected by load.
- **Output size.** Opus's Notes are about 1.8 times as long as Sol's (31 against 17 words per ledger row), and it writes more Questions. Graders were told not to reward length.

Checker results (`_dev/tools/check_lean.py`, which labels itself as checking instruction v1.13.1; the sweep used v1.13.2) are counts summed over the three deals:

| Code | Opus medium | Opus high | Sol xhigh | Sol high |
|---|---|---|---|---|
| Error `round.opening_order` | 4 | 1 | 1 | 0 |
| Error `rounds.no_deadline_pair` | 1 | 0 | 0 | 0 |
| Error `ledger.count_nonbidder` | 0 | 1 | 0 | 0 |
| Warning `questions.length` | 20 | 25 | 7 | 7 |
| Warning `ledger.note_length` | 18 | 16 | 0 | 0 |
| Warning `exit.inferred_reason` | 2 | 3 | 5 | 3 |
| Warning `questions.deadline_outcomes` | 1 | 2 | 3 | 3 |
| Warning `questions.rows_unparsed` | 0 | 0 | 0 | 6 |
| Warning `facts.account_sentences` | 0 | 1 | 0 | 0 |

- **Errors.** By deal, the errors fall Datalink / Mac-Gray / Synacor as follows: Opus medium 0/0/5, Opus high 1/1/0, Sol xhigh 1/0/0, Sol high 0/0/0.
  - The four `round.opening_order` errors in Opus medium's Synacor workbook are real but mechanical. In each, a same-day row (an adviser engagement, the sale decision, an exclusivity change) sits in the new round ahead of its Round opened row.
  - None of the errors belongs to the one documented false-positive class (a quotation split across a page break).
  - Errors did not track the graded score: that Synacor workbook scored 94.50 as frozen.
- **Warnings.** Opus's extra warnings are almost all length warnings on Notes and Questions.

## Can the grades be trusted?

The figures below are over the 12 unique workbooks; the duplicate re-grades are excluded.

- **The two Claude graders nearly always agree.** Their scores for the same workbook differed by 0.46 points on average, and they gave the same grade on 99.2% of items (520 of 524).
- **Claude and Astra agree closely on items but differ in score.** They gave the same grade on 97.1% of item comparisons. The Claude graders scored 1.25 points higher on average. A workbook's two family scores differed by 1.67 points on average, and by as much as 5.5 on one workbook. That spread is as large as the Opus effort gaps and the gap between Opus medium and Sol xhigh, so those comparisons are no sharper than the grading. The Sol effort gaps on Mac-Gray and Synacor are far larger and hold within each family.
- **No sign of family favouritism in 12 workbooks.** The Claude-minus-Astra gap by arm was +1.50 for Opus medium, −0.08 for Opus high, +2.67 for Sol high and +0.92 for Sol xhigh. The largest positive gap was on a Sol arm. With three workbooks per arm, a bias of a point or two cannot be excluded. And since both families graded against the same Claude-built references, a bias the two families share would not show up.
- **Duplicate controls came back identical.** One Opus and one Sol workbook were graded a second time under fresh labels. Every grader gave the same grade on every item (gap 0.0). This shows each grader is consistent, not that the families agree.
- **Pass-versus-fail splits.** There were three, all Astra failing an item that both Claude graders passed: SY-R05 (Opus medium, Synacor), and MG-R08 and MG-B05 (Sol high, Mac-Gray). They are settled in scenario B above. Each moves its arm's mean by at most 0.75 points, but SY-R05 moves one deal by 2.25, enough to cross the per-deal threshold.
- **Blinding held.**
  - The access audit covered all 42 grader sessions. One Claude grader listed the shared work folder, which shows only opaque labels. No session read another bundle's files, the repository, the run receipts or the key.
  - The access audit read only the key's label set. The grade files were hashed into `grades-freeze.json` before the key's mapping from labels to arms was used.

## Limits

- **One run per cell.** Run-to-run variation is not measured, and the rule's 2-point threshold was designed alongside a replicate spread that this sweep lacks. The Sol result rests on two single-run gaps (13.1 and 6.4); if either were run noise, the rule would flip. The Opus result is a finding of no reliable gain rather than a measured difference.
- **Familiar deals.** The instruction was developed on these three deals, so this compares arms rather than estimating accuracy on new filings.
- **Model-built references.** Claude Opus 5.5 agents wrote the references, which no human has adjudicated. A Claude-leaning reference could disadvantage the Sol arms and cannot be tested here. Scenario C shows the verdicts survive the contested items that were found.
- **Sol's served model is not independently confirmed.** Codex does not report the served model in its event stream, so Sol runs record the requested `gpt-6-sol`. Opus runs confirm `claude-opus-5-5` from the stream.
- **Load and timing.** At Austin's instruction the last five cells launched together, so up to eight ran at once, against the protocol's four. This unbalanced load by arm and confounds wall time (see above). No run failed.
- **Grader transcripts are not in the packet.** The Claude graders' transcripts stay in the session store because they carry session context. `grading/access-audit.json` records every path each session touched.

## Files

- `plan.json`, `pin.json`, `protocol-freeze.json`: the frozen design and inputs.
- `runs/<cell>/`: receipts, event logs, workbooks and checker output for the 12 cells.
- `summary.json`: run-side metrics, from `effort_sweep.py summarize`.
- `grades.json`: unblinded frozen scores per cell.
- `grades-freeze.json`: hashes of the grade files, taken before unblinding.
- `grading/`:
  - `grades/`: 42 grade files, `<label>.<grader>.json`.
  - `label-key.json`: the unblinding key.
  - `bundle-scores.json` and `analysis.json`: scores per bundle and the analysis behind this report. `analysis.json`'s pooled agreement figures include the duplicate re-grades.
  - `access-audit.json`, `inputs.json`: the grader access audit and the hashes of the inputs copied to graders.
  - `astra-logs/`: the Codex event logs.
  - `scripts/`: the blinding, grading, saving, freezing and analysis code, the grader prompt and the Claude grading workflow.
- `calibration/`: the pre-sweep Providence & Worcester runs.
