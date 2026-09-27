# Independent grading of the v1.14 fifteen-run trial

> **Status, 26 September 2026 (20:45 UTC):** a grading of v1.14, kept as evidence. Since then the clarification pass became v1.14.1, which Austin published as the cockpit default and retested on five deals, not the two proposed below ([retest](../../2026-09-26-v1141-retest/README.md)). v1.14.1 closes the Mac-Gray residual as Did not submit on 23 July with Count 16, not "with a bound", and caps Notes at 40 words. The scoring here and `mechanical_check.py` (no Note cap) do not apply to v1.14.1 ([`RETEST_PLAN.md`, Acceptance](../../../maintenance/2026-09-26-v1141-streamline/retest/RETEST_PLAN.md)). Opus 5.5 medium is the live default engine. Current state: [current status and decisions](../../../RESEARCH_QUESTIONS.md).

Grader: Claude Fable 5.1, 26 September 2026. Scope: the fifteen anonymized workbooks in `../blinded/`, the frozen v1.14 instruction and the three complete filings in `../inputs/`. Model identities were opened only after `01_blind_findings.md` was written. Nothing outside this folder was changed; no extraction, correction pass, deployment, commit or push was made.

## Files

| File | What it is |
|---|---|
| `01_blind_findings.md` | Method and scale; mechanical summary; source inventory and consensus map per deal; row-level findings for all fifteen workbooks with severity; instruction problems and research decisions as seen blind; blind score table. |
| `02_unblinded_comparison.md` | The key; scores by model/effort setting (blind and revised, with the two revisions explained); runtime, tokens, cost and checker warnings per run; what the pilot does and does not support about the settings; agreement and disagreement with the GPT Pro review. |
| `03_instruction_and_research_decisions.md` | Twelve instruction clarifications with proposed wording (recommendations only, each tied to two or more deals); eleven decisions for Alex, marked new or already pending; what the trial settles. |
| `04_fable_vs_pro_disagreements.md` | Added after both reviews: the ten issues on which this grading and the GPT Pro review disagree, with filing text, rule text, workbook rows and a verdict for each. It corrects `02` §6 on three points and moves the corrected ranking to Astra high first, Opus medium second. |
| `scores.csv` | Per-workbook blind and revised scores with itemized deductions and run ids. |
| `mechanical_check.py`, `mechanical_check_results.json` | The grader's own re-check of the blinded files (quotes, sort order, required cells, flags, sheet structure). All fifteen pass. |

## Concise answer for Austin

**Adopt v1.14, with a short clarification pass first.** Fifteen blind runs on three hard deals produced no material factual error: every price, date, party, type and agreed term is right, every quotation is in the filing, and all fifteen agree on the process count, the winner's path, the bid ladder and the deadline calendar. The voice-note failure modes of August (duplicated NDAs, invented dropouts, IOI-and-bid double rows, execution and announcement conflated, winner type missing) did not occur once. That is a strong result for the instruction.

What the trial did expose is that six rule zones let careful readers of the same text produce different ledgers, and the differences land on the research variables that matter most: the number of live bidders at round 1 and the Heavy/Light level of final bids. In order of data impact, change these first (wording proposed in `03` §A):

1. **E14 residual cohort closure** (A1): say that a cohort the filing says was told the due date is eligible for it; close non-submitters by Did not submit at the due date with a bound. Five workbooks used three different dates and two labels for the same sixteen Mac-Gray signers.
2. **E12 H2 "substantive" and diligence periods** (A2), and **Light versus later "confirmatory"** (A3).
3. **E12 Regulatory Concern trigger and Antitrust** (A4).
4. **E10 commitment-revision marker and the standstill-ultimatum example** (A5).
5. **E6 "reopening" and E3 named parties inside cohorts** (A8, A9).

Each is general and each was hit in at least two deals. None waits on Alex: they fix wording so that five readers agree; the research choice underneath (B1, B2, B4–B6) can stay provisional. A retest of the clarified text on Mac-Gray and P&W, one run each on Opus 5.5 medium and Astra high, is enough to confirm the wording closes the splits before re-extracting the catalog.

**Model and effort.** Keep Opus 5.5 medium as the default extractor: best mean score on this pilot (9.25 revised), the most consistent across the three deals, and the cheapest and fastest Claude setting (13 minutes, $3.2–3.7 per deal). Astra high produced the single best workbook (Mac-Gray) and a mislabelled cohort exit (P&W); use it as the second coder where a deal is double-coded. Neither xhigh setting beat its cheaper counterpart on any deal; both added rows and inference rather than removing errors. Sol xhigh is fast and structurally sound but was the only setting with unsupported Note claims. One run per cell on three deals cannot rank models reliably; these are pilot observations.

**Where I differ from the GPT Pro review.** Pro ranks Astra high, then Astra xhigh, then Sol and Opus medium tied, then Opus xhigh. The difference comes down to three convention calls that Pro graded as settled and I grade as open or as decided the other way by v1.14's text: the Mac-Gray residual (Pro penalizes Did not submit heavily), the P&W residual (Pro rewards Dropped by target, which E14 does not support where the filing says every buyer was advised to submit), and the weight given to flagged alternatives in the Opus xhigh P&W workbook. Pro did catch four small slips I had missed and its reading of the sTec standstill ultimatum as an E10 commitment revision is right; I adopted both and show blind and revised scores side by side.

**What genuinely remains for Alex** (`03` §B): the closure convention for anonymous cohorts and whether inferred closures are dropouts or censoring (B1); whether NDA signers that never proposed and later wanted only assets are entrants (B2); the Regulatory Concern trigger (B4); the H2 definition (B5); whether same-price commitment revisions and a standstill ultimatum are bids (B6); Company H's exit, where the frozen text and the 25 September proposal disagree (B7); the sTec round map (B8, where the text favours Map A); which source governs when the voice notes and the hand coding conflict, with three specific conflicts listed (B9); and a one-line initiation rule (B10). Everything else the September questions raised about these three deals is either settled by the trial (`03` §C) or already pending in `lesson/alex-questions.md`.
