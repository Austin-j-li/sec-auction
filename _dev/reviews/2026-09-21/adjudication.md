# Adversarial adjudication of selected findings

Scope: bounded challenge of four candidate findings, not a duplicate full-deal review. Read the current v1.11 rules, selected filing passages, affected workbook rows/Questions/Rounds, and relevant voice paragraphs from the read-only exports. No extraction, workbook/instruction edits, web, historical grades, or git history. The individual case reports cover complete source and hand-coding coverage. Paragraph labels below refer to the review exports; cells refer to original workbooks.

## 1. Meredith: legal RemainCo versus economic whole target

**Confirmed: high severity, high confidence as an Alex-guidance/economic-scope mismatch. Qualify any claim that this is an unambiguous literal-instruction failure.**

- Cells: `Deal facts!B14` says "Yes" for whole-company bids; `Questions!C5:F5` (Q4) explicitly defends all-stock acquisition of post-spin Meredith. Affected `Deal ledger!E` cells are E16, E17, E18, E25, E28, E38, E45, E46, E47, E51, E52, E54, E57, E58, E60, E61, E66, E68, E69, E72, E74, E75, E76, E77, currently Bid (event IDs one less than worksheet row).
- Source: P01040 describes a "simultaneous sale of LMG RemainCo" and defines it as the Meredith legal entity owning the LMG segment only. P01052 (p. 60) describes LMG offers after a simultaneous NMG spin-off. P00638/P00932 explicitly say Gray acquires the LMG business segment, with NMG shares distributed separately. P01061 (p. 61) supplies the strongest defense: Gray would buy "all of the stock of LMG RemainCo."
- Alex V0095 excludes the deal from estimation because the acquired segment has no observed market price. V0097 explicitly treats these as partial bids and distinguishes a genuinely earlier spin-off from a simultaneous one. This is decisive for the requested economic interpretation. The later legal all-stock acquisition does not purchase the business represented by pre-spin Meredith's market price.
- Current C1 calls a whole-company acquisition Bid and a segment acquisition Other-scope bid, but does not explicitly define the reference company before versus after a simultaneous spin. The workbook's Q4 and target description make its interpretation transparent. Do not characterize it as failing to notice the spin-off.
- Smallest correction: under Alex's economic scope, change the listed LMG Bid events to Other-scope bid; set B14 to "No" with station/LMG scope explanation; revise Q4 and flag exclusion from whole-target estimation. Retain the economic terms, raw per-share amounts actually stated, and descriptive record. Do not invent a market-price adjustment or delete the deal. C15 already allows other-scope bid price treatment.
- Residual decision: explicitly define the reference target for simultaneous carve-outs in a future authorized instruction revision. This fixes interpretation across deals; it does not require reopening whether this particular deal meets Alex's estimation screen.

## 2. Meredith and Kraton: does the first final letter open another round?

**Confirmed under the explicit C8 first-final-request clause; medium severity, medium-high confidence. Economic stage count remains convention-sensitive.**

C8 says the first request for final/binding/best-and-final offers "also opens a round, even if the invited bidders are unchanged." Its exemption for a process letter applies "once a round has been opened as final." Both workbooks correctly identify an earlier information/advancement stage but later use the first final request only to set its deadline.

**Meredith:** P01053 (p. 60) advances the station bidders after the December 21 meeting, grants full data-room access and describes several weeks of diligence. P01054/P01057 (pp. 60-61) explicitly date the first final-station-offer request to January 12. `Deal ledger!E20/G20/P20` (#19) opens round 2 after December 21; `E22/G22/P22` (#21) records January 12 only as Deadline set. `Rounds!C3/D3/H3` combines the two into one announced-final round; Q1 (`Questions!F2`) already names the extra-round alternative.

**Kraton:** P00585 (p. 36) admits A, H and Parent on July 20 for additional diligence "so that they could further evaluate" an acquisition. P00588 authorizes circulating the draft on August 11; P00592 (p. 37) says the final bid procedures letter followed that meeting. `Deal ledger!E34/G34/P34` (#33) opens round 3 on July 20; `E38/G38/P38` (#37) treats the final letter only as Deadline set. `Rounds!C4/D4/H4` merges these stages. Q1 (`Questions!F2`) discloses a fourth-round alternative.

**Best defense, not dismissed:** C8 begins with coherent purpose, prefers the smallest map, and tells the extractor to scan the entire round for finality. No intervening price submission or renewed selection is shown in either interval. The final letters could operationalize the diligence stage already underway. Alex V0082 also anticipates Kraton's formal stage as round three, although that is expressly a forward-looking comment made before the later background. These considerations make the economic map debatable and explain both extractions.

**Why the defense loses under the present operational wording:** evidence that an earlier stage was *already opened as final* is absent from these opening passages. Later finality cannot by itself nullify the separately explicit first-final-request trigger. Labeling an entire earlier stage Announced as final retroactively would largely erase that trigger.

Smallest C8-consistent corrections: make Meredith #21 a Round opened event, with its due date retained there; retain the preceding information stage as Not final; move subsequent pre-March-17 solicitation responses appropriately and renumber the existing final LMG round to 4. Make Kraton #37 a Round opened event, preserving its reported "after 08/11" precision; retain July 20 as round 3, Not final, and move final-stage participation/events and bid responses to round 4. Include H's August 20 withdrawal in the reassignment, not merely the bids beginning at #44. Update Rounds and map/deadline Questions. Do not mechanically reassign unrelated late entrants whose invitations answer earlier solicitations.

Residual uncertainty: dates and economic distinctness differ from the operational counting rule. If the intended convention is that an information stage and its first final solicitation constitute one round, that requires an authorized clarification of C8. Neither finding establishes that an additional economic auction really occurred.

## 3. sTec Company H: reported May 23 exit versus inferred advancement closure

**Downgrade the broad accusation; confirm the narrower evidence-status error. Medium severity. High confidence that May 23 is not a reported target exclusion; medium confidence in the preferred closure date.**

`Deal ledger!B40/E40/N40/O40/T40:V40` (#39) records an exact May 23 Dropped by target, reason Would not improve earlier offer, with no inferred flag. `Rounds!J2/E3` and `Questions!C5:F5` repeat that interpretation.

P00618 (p. 30) reports that H's price was insufficient for advancement but expressly invites a revised indication for committee consideration. P00620 reports final-round letters to WDC and D after the May 16 meeting. P00621 reports H's May 23 statement that it "remained interested" but could not increase its range. That last statement is not a target rejection and is not a withdrawal. Later P00656/P00657 (pp. 33-34) says H repeatedly restated its range and a superior proposal was considered remote; it does not supply a May 23 exclusion.

The strongest current-rule answer is C16's first complete-advancing-set closure: H was outside WDC/D on May 16, so infer Dropped by target **by May 16**, Inferred=Y, Exit reason=Not stated, with last supported live date May 15. Preserve the May 23 communication as subsequent continued interest without admission; do not create re-entry merely from that statement. Alex V0124's account also places the target's dropping of bidders at May 16.

However, C3/B3 recognize offers still being received from a bidder not admitted to the next stage, and P00618 leaves an opportunity for H to improve. Whether that means economic participation continues is a real convention issue. A later signing closure is defensible under an opportunity-based definition; it conflicts with a mechanical application of C16's earlier advancement closure. The workbook itself exposes this in Q4. Therefore do not present "H definitely stayed live until signing" as a high-confidence extraction correction.

Minimum correction independent of that decision: remove the assertion of a *reported, exact-date* May 23 target exit. Distinguish the source's May 23 bidder statement from whichever inferred closure is adopted; do not carry a stated exit reason into a C16 inferred exit. The current row's date/actor certainty is not cured by the presence of Q4.

## 4. sTec WDC May 28 and May 30 conditions

**Confirmed unsupported Light inference; medium severity, medium-high confidence. Reject automatic replacement with Heavy.**

Cells: `Deal ledger!L42/P42` (#41, May 28) and `L46/P46` (#45, May 30); `Questions!C6:F6` (Q5). P42 equates signing by June 3 with "expedited diligence"; Q5 repeats that inference.

P00622 (p. 30) supports the $9.15 bid, merger markup, ancillary agreements and a contemplated June 3 signing. It does not call remaining diligence confirmatory, limited or expedited. P00628/P00630 (p. 31) says WDC remained focused on June 3 and the target would endeavor to "complete diligence and negotiation"; the founders' lawyers were still reviewing the ancillary agreements. An intended signing date establishes an intended timetable, not the extent of diligence or a commitment to proceed after only limited work.

C14 requires affirmative support for Light and explicitly directs Unclear where narrative diligence remains open without a specified bid condition. The May 30 evidence fits that rule directly; the May 28 proposal likewise lacks the affirmative limited-diligence/final-documentation-only evidence needed for Light. The subsequent May 30 passage is supporting context, not a basis for importing a newly arisen condition backward.

Smallest correction: use Unclear on L42/L46, remove the inferred "expedited diligence" claim, and retain factual timing and ancillary demands. Begin the May 30 note with the required "Diligence open per narrative:" wording. Preserve Formal: the markup and final solicitation independently support it.

Heavy remains possible if the founders' covenant not to sue and associated demands are adjudicated as an unresolved material commercial requirement rather than remaining documentation. Their presence alone does not establish a financing contingency, a substantive multi-week diligence condition or an identified completion obstacle. Later negotiations over indemnification cannot automatically rewrite the May bids. Alex V0125 even describes May 28 as having "no conditions"; that supports the Formal judgment but does not resolve the fuller narrative/current C14 conflict. Flag the conditionality convention rather than claiming Alex independently confirms Heavy.

## 5. Mac-Gray: all 16 unnamed NDA signers out by July 25

**Confirmed unsupported common exit bound; medium severity, high confidence. Retain the exact total residual population, distinguish it from the population live at July 25.**

`Deal ledger!B25/E25/M25/V25` (#24) closes all 16 unnamed financial NDA signers by July 25. P00695 (p. 32) reports 20 signers "over the next two months" following June 24: two strategic (A, CSC/Pamplona), 18 financial (including B and C). Thus 18 minus B/C equals exactly 16 unnamed financial signers overall. But P00716 (p. 34) explicitly dates A's NDA to August 5, demonstrating that the aggregate spans the July 25 cutoff; it does not establish when the 16 financial signers signed.

Best defense: P00709 and the following selection passage identify only A/B/C/CSC-Pamplona as advancing on July 25; none of the 16 is later named as a bidder. That supports exclusion of any already-live residual members. It does not prove the 16 were all participants then. C16's advancement inference applies to those "live in a stage," and C3 forbids exiting nonparticipants. `Questions!D5/F5` acknowledges this timing problem explicitly.

Correction: retain the exact residual total of 16, but remove the assertion that all had exited by July 25. Use an aggregate closure bound supported after their entry window, potentially the August 27 four-party solicitation, or leave the July 25 subset count blank and reconcile later closure without double counting. Do not invent individual exit dates or automatically change all 16 to Did not submit July 23. Review the associated entry window and Rounds population together. Alex V0045 supports careful individual NDA timing but provides no date for these 16.

## 6. Synacor: exact 13 NDA non-submitters

**Confirmed unsupported exact residual; medium severity, high confidence. Reject a forced change to exactly 12.**

`Deal ledger!C41/M41/P41` (#40) records 13 other NDA signers as Did not submit by September 17, computed as 14 minus CLP. `Questions!C5:F5` acknowledges uncertainty about G/H and even E's membership. P00418 (p. 32) reports 37 outreach parties, 14 NDAs, and no indications "Other than as described below." P00420 records CLP's NDA; P00423/P00426 (pp. 32-33) records G's September 14 indication for software/services. The outreach expressly covered the company **and/or** software/services, so G's other-scope offer cannot simply be ignored as a non-submission to that outreach.

Best defense: no NDA is specifically attributed to G, and its entry may therefore first be evidenced by its offer. Correct event dating on that basis does not establish G's *nonmembership* in an unidentified NDA cohort. The source exception "as described below" is also inconsistent with the row's broad note that no other outreach party produced an indication.

Under the workbook's assumption that E is outside the 14, the NDA non-submitter total is 13 if G is outside and 12 if G is inside. C3/C16 require Count blank when the residual's membership is uncertain. Correct M41 to blank; describe this conditional 12-13 bound and the unresolved overlap, rather than selecting either endpoint. E membership can change the bound further, so do not present 12-13 as unconditional. Reconcile H's possible NDA membership against its individual admission/closure rows under C16's residual precedence rule; H's lack of an indication does not itself reduce the *total* non-submitter count but can create duplicate participant/exit accounting. Update Q4 and the affected Rounds count. No voice evidence independently identifies these cohort memberships.
