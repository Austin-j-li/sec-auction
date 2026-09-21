# Instruction comparison: v1.11, v1.12, v1.12.1 on DeepSeek flash and Opus

21 September 2026. Thirty isolated runs, one instruction and one filing each, all producing a valid workbook. The per-run numbers are in [instruction_comparison.json](instruction_comparison.json).

- **DeepSeek flash, max variant:** v1.11, v1.12 and v1.12.1 on all eight deals (24 runs, $3.14 in total, about $0.13 a deal, 9–18 minutes each).
- **Opus 5 high:** v1.12 and v1.12.1 on Meredith, Synacor and sTec (6 runs, $29.27 in total). The Opus v1.11 baseline is the workbook in `extraction/`.

All eight deals shaped v1.12 and v1.12.1, so this is not a test on unseen filings. The substantive judgments below come from three model readers (one per hard deal) checking six workbooks each against the filing and the 21 September review; no human has adjudicated them.

## Mechanical results

DeepSeek totals over eight deals. "Opus" is the v1.11 baseline.

| | v1.11 | v1.12 | v1.12.1 | Opus |
| --- | --- | --- | --- | --- |
| Checker errors | 43 | 42 | 11 | 0 |
| Checker warnings | 75 | 109 | 62 | n/a |
| Ledger rows | 422 | 442 | 446 | 473 |
| Bid rows | 78 | 79 | 84 | 81 |
| Bid prices matching an Opus bid | 75 | 76 | 76 | 81 |
| Exit rows | 52 | 54 | 50 | 57 |
| Deals with Opus's round count | 6 | 7 | 5 | 8 |

Opus, three hard deals (errors are zero in every run):

| Deal | Version | Rows | Rounds | Questions | Bid rows | Inferred | Warnings | Cost |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Meredith | v1.11 | 79 | 3 | 9 | 6 | n/a | 15 | about $4 |
| Meredith | v1.12 | 76 | 3 | 7 | 6 | 5 | 11 | $5.07 |
| Meredith | v1.12.1 | 82 | 4 | 11 | 6 | 6 | 11 | $4.80 |
| sTec | v1.11 | 62 | 2 | 9 | 8 | n/a | 17 | about $4 |
| sTec | v1.12 | 66 | 2 | 6 | 9 | 0 | 7 | $3.81 |
| sTec | v1.12.1 | 62 | 3 | 7 | 7 | 0 | 18 | $3.80 |
| Synacor | v1.11 | 75 | 7 | 9 | 9 | n/a | 16 | about $4 |
| Synacor | v1.12 | 84 | 8 | 8 | 9 | 7 | 10 | $6.33 |
| Synacor | v1.12.1 | 75 | 6 | 10 | 9 | 5 | 11 | $5.46 |

## Substantive results on the three hard deals

**Both new instructions beat v1.11 on Opus.** The over-exact values the review found are largely gone: Synacor's unsupported count of 13 becomes a blank Count with a range under both; sTec's count of 13 becomes "12–14" under v1.12; Gray's hindsight-based Heavy condition in Meredith is fixed under both; WDC's Light condition in sTec is corrected to Unclear under both; Meredith's 28 January exit reasons become Not stated under both. No bid price, bidder or date is wrong in any Opus run.

**Neither new instruction clearly beats the other.**

| Deal | Better | Why |
| --- | --- | --- |
| sTec | v1.12 | Removes Company H's unsupported exact exit, keeps every bid. v1.12.1 keeps the H error, drops WDC's 30 May reaffirmation row, and adds a third round (11 June) that the filing does not support as a round. |
| Meredith | v1.12.1 | The only Opus run to separate the December diligence stage from the 12 January final-offer request, which is the review's largest Meredith finding. v1.12 still merges them despite its C8 edit. |
| Synacor | v1.12.1, slightly | Handles counts most carefully. v1.12 puts Company B inside process 1 and codes a priceless CLP remark as a bid. v1.12.1 regresses on Company E's exit reason and calls a non-binding letter Formal. |

**Round maps stay unstable.** Across the six Opus runs on these deals, round counts moved in both directions and no Synacor workbook carries all six stages the filing shows. Neither instruction has settled what opens a round.

**Unfixed under every instruction and model:** Meredith's whole-company scope flag (M1) and its missing 13 April structure revision (M3); sTec's 30 May deadline marked Enforced although later bids were taken; Synacor's 29 December "CLP's offer" with no Question raised.

## DeepSeek against Opus

DeepSeek gets prices, dates and named bidders right (about 93% of its bid prices match an Opus bid; no invented party in any workbook checked) at one-thirtieth of the cost. It is weaker and less stable on everything that needs judgment: processes (an invented second process in two sTec runs and one Meredith run, a fourth in one Synacor run), collapsed or missing stages, missing cohort closures, missing parties (no Company H rows in one Synacor run, the agreed $16.99 price never a bid row in one Meredith run), fabricated reaffirmation rows, and Conditions. It is usable as a cheap signal about an instruction, not as the extractor.

As an instruction signal, DeepSeek's one clear message is that the shorter v1.12.1 is easier to follow mechanically (11 checker errors against 42–43). It did not reproduce the Opus-level differences: for example DeepSeek under v1.11 already split Meredith's December and January stages, and under v1.12.1 it did not.
