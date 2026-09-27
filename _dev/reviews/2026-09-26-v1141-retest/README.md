# v1.14.1 retest, 26 September 2026

Ordered by Austin on 26 September ("publish it in the cockpit, and then do the 5 deal rerun"; Datalink "extracted with the new system"). Five cockpit extract jobs started as Austin, Opus 5.5 (`claude-opus-5-5`) at medium effort, instruction **v1.14.1** as published in the cockpit (id `08caed447f7d`, SHA-256 `8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98`, which is the reviewed candidate `8bdb7c20…8a79` plus the report's wording items 2, 4–10; see `../../maintenance/2026-09-26-v1141-streamline/deployment-v1141.json`). Checked after each run by checker 1.8 under the v1.14.1 rules. The workbooks live in the cockpit as versions "Opus 5.5 · medium · v1.14.1 — Austin, 26 Sep"; they are raw, unreviewed extractions.

| Deal | Version | Minutes | Cost (USD) | Checker 1.8 | Rows (trial) |
|---|---|---|---|---|---|
| mac-gray | opus55-medium-20260926-2019-1d1d60 | 8 | 2.25 | 0 errors, 2 warnings | 53 (64) |
| providence-worcester | opus55-medium-20260926-2019-366a73 | 9 | 2.29 | 0 errors, 2 warnings | 58 (63) |
| stec | opus55-medium-20260926-2027-0643aa | 7 | 1.77 | 1 error, 3 warnings | 56 (66) |
| synacor | opus55-medium-20260926-2028-342883 | 13 | 2.94 | 0 errors, 6 warnings | — |
| datalink | opus55-medium-20260926-2032-350a91 | 9 | 2.34 | 1 error, 4 warnings | — |

Three ran at once after the per-user cap (`runs.CAPS`, 2) was lifted to 3 for this batch and restored (worker restarted twice; running jobs survive a worker restart).

## Acceptance (`acceptance.json`, `retest_acceptance.py`)

- **Mac-Gray:** all pass: 16 unnamed signers Did not submit dated 23 July (row 17); October liability revisions are blank-price Bid rows (47, 48); Party A's 18 September bid Heavy (H1) and Formal (row 37).
- **P&W:** the script reports FAIL on "16 non-submitters, Count 16", but the workbook has 16: Party A's own Did not submit (row 16) and a cohort of 15 (row 17), as E3 requires (a named party keeps its own row). The check is too strict, not the workbook. Party E not H2, G&W Regulatory Concern (51) and Party C not Not begun (23) pass. REVIEW: NDA rows 8–10, 22 (Party C signed later, in round 2).
- **sTec:** Company H Dropped by target by 16 May, Would not improve earlier offer (37); WDC's standstill warning a Bid with H3, no price (54); two rounds.
- **Synacor:** 3 processes, 6 rounds, as recorded.
- **Datalink:** 1 process, **4 rounds** (recorded under F9: 5). Expected and accepted: Austin decided on 26 September that Datalink is extracted under the new text. Round 1 opens 28 January (first price negotiation with Party A), not F9's 29 January. Round 2 (6 June) and round 4 (1 October) are trigger (d); round 3 (16 August) is the announced final round.
- **All five:** no Note over 40 words; at most four Questions besides the process Question; fewer rows than the trial for the three trial deals.

## Checker findings

- **Error, sTec row 56 and Datalink row 76:** Count 1 on the Merger announced row, whose Who is the winner. D1 col. 20 blanks Count "on rows about no bidder"; both runs read an announcement naming the acquirer as a row about a bidder. The checker treats Merger announced as a no-bidder row. Candidate wording for v1.14.2: "Blank on rows about no bidder and on announcement rows (Sale process, Bid, Merger announced), except …".
- **Warnings:** Questions over 60 words in every deal (D4); Synacor's two Process restarted rows have blank Count (row 14, 22); sTec row 19 one-sided price without floor/ceiling wording; Datalink row 71 an Exclusivity changed row possibly repeating bid row 69.

Not graded with the trial rubric (see `RETEST_PLAN.md`).

## Formality readings

The agreement with Alex's labels (questionnaire 3.3(a)) was recomputed from these five workbooks with `derive_analysis.py` 0.3 `--rules v1.14.1`: `analysis/formality_agreement.json` (and `.csv`, from `analysis/formality_agreement.py`). Mac-Gray: T0 and T3 still 13 of 13. P&W: no reading matches all 14 any more (best 12 of 14).
