# v1.14.1 candidate: change log

26 September 2026. Implements `V1141_SPEC.md` §10 steps 1, 2 and 4, the text work only. Nothing was published, deployed or run. No checker, analysis, cockpit or workbook was changed. §9, the engine switch, is not done.

> **Status, 26 September, about 20:45 UTC.** After this log, the candidate was edited with eight wording fixes Austin approved (candidate issues 2 and 4–10 of [`PIPELINE_UPGRADE_REPORT.md`](PIPELINE_UPGRADE_REPORT.md)); its SHA-256 is now `8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98`. The text this log describes is kept at [`checks/candidate-8bdb7c20-as-reviewed.md`](checks/candidate-8bdb7c20-as-reviewed.md), and `v1.14.1_candidate.diff` is against that text, not the edited one. Austin published it in the cockpit as v1.14.1 at 20:18 UTC (id `08caed447f7d`, SHA-256 `8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98`: the reviewed `8bdb7c20…8a79` plus candidate issues 2 and 4–10 of `PIPELINE_UPGRADE_REPORT.md`) and made it the cockpit default; the engine switch is live. D1–D6 were confirmed by Austin (Q3 of the report).

- **Candidate:** `SEC_Deal_Ledger_Extraction_Instruction_v1.14.1_candidate.md`, 6,417 words, SHA-256 `8bdb7c20…8a79` (full hash in `v1.14.1_candidate.sha256`).
- **Baseline:** `../2026-09-24-bid-terms-taxonomy/SEC_Deal_Ledger_Extraction_Instruction_v1.14_candidate.md`, 9,747 words, SHA-256 `c2d47a47…ab27`. It was not edited.
- **Line diff:** `v1.14.1_candidate.diff`.

## How it was made

1. **Drafting.** Three Opus agents drafted in parallel from the spec and the baseline: title block with A–D, E1–E8, and E9–F with Examples. The fragments were then assembled and harmonized (one home for Varies and for the Count qualifier, curly quotes).
2. **Consistency pass 1.** A fresh agent that had not seen the spec read the assembled text alone and reported contradictions, duplicate homes, invitations to hedge, gaps and ambiguities. The fixes adopted are listed below.
3. **Synthetic check (§10 step 4).** A fresh agent coded the five example passages from a copy of the text without its Examples block. All five codings matched the Examples block. It also found three gaps, all fixed: the order of the inferred-exit rules, what a revision row copies, and H2 for a period that covers more than diligence.
4. **Consistency pass 2.** A second fresh agent repeated the review on the revised text, and its adopted fixes and cuts were applied.

## Settled decisions and where they live

| Decision | Text |
|---|---|
| H1 Company H Dropped by target | E14 inferred exit 1 ("whatever it was told about coming back"); the reason follows what the bidder later reports (Would not improve earlier offer) |
| H2 P&W 16 non-submitters | E3 Cohorts, E14 inferred exit 4 |
| H3 Mac-Gray 16 by 23 July | E3 Cohorts, E14 inferred exit 4 (first due date after they appear) |
| H4 Commitment changes are Bid rows with no new price | E10 Revisions ("not a new price observation") |
| R1 Same offer | E10 Same offer; Part B ("Only a Same-offer row copies an earlier row"); D1 Note order |
| R2 Evidence window, forecasts count | Part B |
| R3 Unnamed cohort closure | E3 Cohorts and Count; E14 inferred exit 4; Example 1 |
| R4 H2 only for diligence alone | E12 H2; Example 4 |
| R5 Not invited, Dropped by target | E14 inferred exit 1; Re-entered; Example 3 |
| R6 Not begun only before an NDA | E12 Due diligence |
| D1 (a) A price-only revision must meet a route itself | E11 |
| D2 (a) A condition on proceeding is a Bid with H3 and a blank price | E10 Conditions on proceeding |
| D3 (a) Committed financing with silent diligence is Unclear | E12 (the second Light route is removed) |
| D4 Five Questions | F |
| D5 Nine exit reasons | E14 |
| D6 30 days, or an ended exclusivity period | E6 trigger (d) |

D1–D6 use the spec's recommendations and still await Austin's confirmation.

## Where the text departs from or adds to the spec

1. **Length is 6,417 words, not 5,000–5,500.** The spec's own per-section estimates in §4 add up to about 6,400, so its target and its section budgets disagree. The text now sits at the section budgets. Further cuts would mean dropping enum text or rules the spec keeps.
2. **The process Question does not count toward the five.** The spec's F text says "one of the five"; §7 (checker) and §10 (acceptance) say "five plus the process Question". The candidate follows §7 and §10. Choose one before the checker is changed.
3. **Additions from the reviews.** All are wording or default fixes; none changes a settled rule:
   - **Revisions:** a revision's other cells are coded from its own communication (E10), and only a Same-offer row copies (Part B).
   - **Inferred exits:** apply in time order, with list order breaking ties (E14).
   - **Re-entered:** also given to a bidder invited back into a stage. Without this, the live-count identity fails after an E6(d) reopening.
   - **Round 1 outreach** means two or more buyers. Sounding out a single party is Target interest, and round 1 then opens at the first NDA or price negotiation.
   - **Inferred final** is the round opened by trigger (c). **H2:** a period that also covers negotiation or exclusivity is not diligence alone.
   - **Levels:** after Heavy, None, Light and Unclear are taken in order.
   - **Other material event:** now includes any new target requirement of bidders, which E2 had given a row but D2 had no label for.
   - **Dates:** "on or about [day]" is that day. E9 with differing bidders takes the first outcome that fits any bidder.
   - **Rows and columns:** Round is 0 before round 1 opens. Count is filled on process markers and group changes. Stock % lists its values in D1.
   - **Offer outstanding** in E5 is defined. **Initiation** is judged from process 1. **Bid reaffirmed** follows the start of definitive negotiation with that bidder. The Note order is "Same as #n", then the trigger, then the rest.
4. **Cuts from pass 2:** duplicate homes for price feedback, the exclusivity-on-bid-row rule, inferred Round opened, signing prices, non-entry of partial-only parties, and "Conditions never change the label".

## Open points for Austin (not changed)

- **Price-only revisions lose the earlier terms.** Under R2 and the Revisions rule, a price bump the filing says nothing else about gets Not stated in the condition columns, and usually Conditions Unclear. Pass 2 proposed copying the terms when the filing says they are "otherwise unchanged". That would bring back a narrow form of the deleted express-incorporation rule, so it was left out. It affects use 3 (Formal and not Heavy). The retest will show how often it happens.
- **The required process Question** fires on outcomes the defaults already decide (more than one process, a trigger-(d) or inferred round). Pass 2 suggested moving the E5 results into Deal facts under Number of processes instead.
- **Formality route 2 for a revision the target requests inside an announced final round** is not decided. Only unsolicited bids are excluded.
- **Other-scope bid rows** still need Formality and Conditions under F check 2, as in v1.14. No rule codes them specially.

## Not done (needs Austin's go)

§7 checker and analysis changes, §9 engine switch and deploy, the §10 step 5 retest (five isolated Opus 5.5 medium runs), publishing in the cockpit, the questionnaire reconciliation and the doc updates.
