# Mac-Gray: adjudication of the fresh audit

21 September 2026. Development-lead assessment against the filing and frozen v1.13.2, not human acceptance of a research benchmark. No workbook has been revised. Ledger references use event **#**; Excel row is # + 1. All ten reviewer quotations were found in the filing; that check does not validate the claims attached to them.

Sources: [filing](/home/uctpiaj/Projects/sec-extraction/raw_filing/mac-gray_2013-12-04_DEFM14A.htm), [instruction](/home/uctpiaj/Projects/sec-extraction/SEC_Deal_Ledger_Extraction_Instruction.md), [raw new workbook](/home/uctpiaj/Projects/sec-extraction/_dev/reviews/2026-09-21-mac-gray-pilot/raw/extraction/mac-gray.xlsx), [verbatim audit](/home/uctpiaj/Projects/sec-extraction/_dev/reviews/2026-09-21-mac-gray-pilot/audit/review.md).

## Disposition of all ten audit findings

Five findings support limited corrections, three need judgment about representation or classification, and two are not accepted as stated. This is a count of reviewer claims, not an accuracy or completeness score.

| Finding | Disposition | Evidence, rule and concrete action |
| --- | --- | --- |
| **F01: Q9 says the alternative leaves no formal bid** | **Supported; correction to the Question** | Filing p.39 reports Kirkland's returned merger-agreement draft on October 7. Under E10/E11, an Informal standing offer would need reconsideration as a formal reaffirmation once its own agreement markup is returned during finalization. Correct Q9's counterfactual and its unqualified statement that no bidder markup is reported. Under the currently recommended Formal classification, add no reaffirmation row: #44 is already Formal in a final round. The baseline's Q7 contains the same defective counterfactual. |
| **F02: September 21–23 final-proposal terms need their own bid** | **Genuine E2/E10 boundary for Austin** | Filing pp.37–38 separately dates agreement on a $15m reverse termination fee, no financing contingency, and related terms after the September 21 price increase. E10 requires material economic changes; E2 folds routine legal negotiations. A reverse fee changes economic commitment and merits serious consideration as its own dated Bid event. Recommend recording the material change, with unchanged $21.25 price and no new round, if reverse-fee risk allocation is in scope. Do not call 100% Pamplona funding newly introduced here: it was already reported September 9 and 18. Do not retroactively attach later terms to the September 21 bid as contemporaneous facts. Both drafts currently fold these terms. |
| **F03: separate row for A's lack of the initial package** | **Representation judgment; not a confirmed omission** | Filing p.33 reports stalled NDA terms July 11–23; p.34 gives A's August 5 NDA and package. #28 and Rounds already preserve this distinction. The auditor reasonably invokes E2's information-asymmetry rule, but proposes an additional state row for an unadmitted bidder, with no separate access-changing act beyond the existing NDA/package event. Recommend making the package difference explicit in the existing R1 description and #28; do not count an additional row as required without deciding that granularity. Do not call A wholly “uninformed”: the source establishes the package timing, not absence of all information. This qualifies the source inventory's note-only treatment of S11 rather than proving a missed dated event. |
| **F04: April 5 Target sale decision label** | **Classification judgment** | Filing p.27 authorizes exploration of transactional opportunities and later postpones deciding on a sale process. New #1 itself says “not yet a sale decision.” Recommend Other material event or folding the authorization into the April 8 target-contact note, as in the baseline. A qualified exploration-of-sale label is arguable under D2, so this is not a new empirical fact or evidence that Round 1 began in April. It does not change the target-led first contact or June auction opening. |
| **F05: A's August NDA is allegedly erroneous evidence in Q5** | **Not accepted as stated; proposed retention of #23 rejected** | A's August 5 NDA does show that some of the 20 signings occurred after July 23. It does not prove that any of the 16 unnamed financial signers signed late, but Q5 does not explicitly claim that it does. Clarify that distinction if useful. The important error is instead the exact dated closure of all 16 despite unknown eligibility. The reviewer's suggestion to retain #23 with a caveat does not meet B/E3/E14; see L01 below. |
| **F06: BofA quote does not support the April date** | **Supported only as a quotation correction** | New #2 is dated April 5 but quotes the October 23, 2012 engagement for Mac-Gray's attempted purchase of CSC (p.27). Replace it with the April authorization / action passage, under Part B. Do not automatically delete #5/#6: the filing explicitly reports termination of the earlier engagement and a new mandate (pp.29–30), and D2 permits one Adviser row per relationship. The auditor itself acknowledges that counter-reading. |
| **F07: Moab permission quote supports only Moab's wish** | **Supported; quotation correction** | New #45 says the target allowed renewed rollover talks. Its quote only states Rothenberg wanted them. P.38 has the directly supporting clause, “to provide Moab with the opportunity to resume discussions with CSC/Pamplona regarding a possible equity rollover of Moab's shares in the transaction”. Use that clause; the event and date stay unchanged. Part B. |
| **F08: outreach When ends in July without a supported bound** | **Supported; precision correction** | New #11/#12 says late June–July but the source says “During the next several weeks” after June 24 (p.32), with no stated completion date. Date to is already blank. Use the source's wording consistently; retain June 24 lower bound and no invented upper bound. B/E8. |
| **F09: winner's Type is blank at signing** | **Rejected: false cell claim** | In the raw output, preserved copy and exact audit input, `Deal ledger!A53 = 52`, `D53 = Strategic`, and `M53 = 1`. All three workbook hashes are identical. The proposed value is already there. Do not change anything. A valid source quote does not rescue this claim. |
| **F10: July 25 written C bid described as considered at the selection meeting** | **Supported; narrow chronology correction** | New #22 groups C's July 24 oral and July 25 written offers as considered July 25. The source expressly places the written revision later that day after the meeting (p.34). Q4 already has the right order. Make #22 equally clear: oral bid reviewed at the meeting; written revision followed. Retain both bids and Late bids accepted. B/E8/E9. |

## Important lead findings that the audit did not resolve

These were written in `lead-findings-before-audit.md` before opening the fresh audit. Their final dispositions are below; the earlier candidate list remains unchanged for transparency.

### L01 — unsupported exact July 23 cohort closure: clear existing-rule mistake

- **Rows:** new #17/#23, Rounds R1, Q5; baseline #19/#22, Rounds R1, Q3.
- **Source:** p.32, “Over the next two months a total of 20 potential bidders”; it identifies two strategic and eighteen financial signers. B/C have dated June NDAs, CSC July 11, A August 5. No date is given for any of the remaining sixteen financial signers. Pp.33–34 name the four advancing bidders.
- **Rule:** B's exact-arithmetic and evidence requirements, E3 counts, E8 timing, E14's eligibility prerequisite for Did not submit. Unknown signing times do not establish that all sixteen were eligible for the July 23 solicitation. An inferred marker and a Question do not license unsupported numeric/date precision.
- **Correction proposed:** retain **16 as the eventual residual NDA total**. Remove **16 as an established July 23 non-submitter count** and remove the unqualified statement that nineteen had been admitted to the first solicitation. Represent the due-date population as uncertain, without guessing how many signed later. Close each residual participant once at a supported transition or conservative later bound, with the unresolved timing explicit. Preserve the four second-stage invitees from the direct source evidence, not from the invalid timing subtraction. A later revision must reconcile the entire participation path; simply changing July 23 to July 25 does not establish the dates of all sixteen signers either.
- **Audit outcome:** F05 notices the uncertainty but explicitly recommends retaining the exact closure. Its narrative even certifies live counts by `20 entered − 16 did not submit`. Thus this material defect remains after review. This requires applying an existing evidence rule, not inventing a new convention.

### L03 — September 27 voting agreements: supported material event omitted from the new ledger

- **Rows:** baseline #49; absent from new ledger, mentioned only in new signing #52.
- **Source:** p.37 says CSC/Pamplona requested MacDonald family voting agreements with its September 21 offer. P.39 states those agreements “were entered into by Mr. MacDonald, his wife and one of his trusts on September 27, 2013” and became effective when the merger agreement was entered.
- **Rule:** E2 records changes in commitment and transaction requirements; D2 permits Other material event. Execution of required shareholder support is substantive, not a routine draft exchange.
- **Correction proposed:** restore a September 27 Other material event, distinguishing execution then from effectiveness at signing. Preserve the source's conditional effectiveness. Do not turn shareholder support into a bidding group or a new bid.
- **Audit outcome:** no finding. This is a lead-supported omission outside the predeclared inventory scope; it is not used to estimate whole-filing omission recall.

### L04 — Party B's options: material terms lost in the new Note

- **Rows:** new #40; baseline #39 retains more of the terms.
- **Source:** p.36 says the options represent 10% of new equity, have a strike equal to Party B's initial cost basis, and vest on achievement of base-case management projections over five years, excluding future acquisitions.
- **Rule:** D1's Note records terms and conditions, and E13 attributes package value and basis. The contingent payout is central to why the nominally higher bid was not chosen (p.37).
- **Correction proposed:** restore strike, vesting basis, five-year horizon and the exclusion of future acquisitions in the bid Note. Retain $21.50 as Party B's own value, $19 cash plus options it values at $2.50, and All cash = No. Do not treat consideration contingency alone as proof of missing financing.
- **Audit outcome:** no finding on the lost terms. Its check of the total package price and cash classification is correct but incomplete. This is not a missed price.

### L05 — request to extend exclusivity: dated event folded in both drafts

- **Rows:** new #51 / baseline #52 mention the request only inside the October 12 extension.
- **Source:** p.40 reports at the October 9 meeting that Kirkland had requested extending the October 12 expiry; p.41 dates actual execution of the extension October 12.
- **Rule:** D2 explicitly distinguishes requested/executed/extended Exclusivity changed events; E2 preserves changes in process timing.
- **Correction proposed:** add a request event **by October 9** (not an invented exact request day), separately from the October 12 executed extension. Keep subsequent conditions on the extension in the relevant note. These are not bid deadlines.
- **Audit outcome:** no finding. This omission predates the rerun.

### L06 and smaller points

- **Q1's new alternative:** E6's first final-offer solicitation opens a round even with the same bidders. Treating September 11 as a mere repeated improvement request is not a supported alternative under the frozen convention. A round numeral also does not itself determine Formality. Correct the Question rather than creating a new research convention. The audit rejects this alternative in its prose but does not include a specific finding to repair Q1.
- **#3 Count:** one named Party A first contact supports Count = 1 under D1; the new workbook leaves it blank, whereas the baseline records 1. It is not bidder entry. Not flagged by the audit.
- **#14 inference flag:** the deadline-communication date is derived from the first dated information package, not directly stated as a dated request. Preserve the reasoning and mark Inferred = Y; baseline did, new does not. Not flagged by the audit.
- **Opening order:** new #9 is already R1 before the #10 Round opened marker. Reorder the same-date marker/decision as appropriate without moving the supported June 24 start or creating another round. The audit missed this checker error.
- **Checker warning rejected:** Q4, Q6 and Q8 explicitly discuss deadline outcomes. The checker's “no Question visibly mentions deadline outcomes” warning is a wording-detection false positive. Do not add a duplicate Question to silence it.

## Lead candidates not counted as confirmed errors

- **L02, full access during exclusivity:** the lead initially proposed restoring baseline #50's separate September 25–October 7 access row. The auditor points out that no rival remained live then; the new #46 Note retains the fact of full access. Given E2's equal-access/admission-note exception, a separate row is not established as mandatory. Keeping the supported timing window in that Note would improve precision. This is not counted as a confirmed material omission or regression.
- **34–35 financial contacts (new Q3):** the source reports 35 financial parties and subsequently treats CSC/Pamplona as a single strategic bidder. Its earlier “50 parties, including CSC and Pamplona” wording allows an entity-versus-bidding-unit question. Prefer preserving the reported 35 alongside any separate unit-count uncertainty. Do not count the new qualification as demonstrated improvement or automatically force an exact bidder-unit total without resolving membership.
- **Conditions on CSC's exclusivity requests:** both drafts and the audit choose Heavy under the current E12 parenthetical, with a Question about confirmatory diligence. This case supplies no new evidence that resolves the broader interpretation. Keep it distinct from Formality, which stays Formal for the final solicitation.

## Decision boundary

The accepted quote, chronology and evidence corrections above can be prepared without rewriting the instruction. Austin's substantive choice is most relevant to F02's boundary between economic commitment changes and routine legal negotiation; F03/F04 are narrower representation choices. Do not promote every unresolved date or omitted event into an instruction problem.

No revision was run. Therefore this trial measures discoveries, misses and proposed corrections—not actual corrected errors, revision regressions, or review time saved.
