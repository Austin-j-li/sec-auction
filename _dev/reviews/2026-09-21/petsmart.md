# PetSmart: substantive review of the current v1.11 workbook

**Verdict: strong with minor corrections, with bidder-group membership and the round-one start still requiring an explicit convention decision.** The workbook captures the difficult missing third initially high-valuing bidder, all material prices and revisions, the target's deadline extensions, and the distinction between Longview's rollover and a bidding consortium. The most important limitations are openly questioned rather than silently fabricated. Two small corrections concern an unmarked inferred residual and an omitted named buyer-side legal adviser.

## Coverage and reference quality

Reviewed the complete Background of the Merger P00739-P00779 (pp. 21-26), every current ledger event #1-#43, both Rounds rows, Q1-Q7 and all Deal facts. Also checked buyer definitions P00200/P00222/P00665, reasons P00788 (p. 27), the projections section P01090 onward, financing conditions, and the merger agreement's notices P02877-P02885 (p. A-46). Critical NDA/October meeting and adviser passages were checked directly against `raw_filing/petsmart_2015-02-02_DEFM14A.htm`. Read all PetSmart voice guidance V0053-V0065 and relevant recurring guidance V0131-V0143. Current rules used include C3-C5 and C8-C16. Labels identify the read-only exports in `/tmp/sec-extraction-review-20260921/petsmart/`.

Alex's older `deal_details` rows 6408-6460 contain 53 substantive rows, not just a target placeholder: 15 NDA identities, bids/ranges, deadline markers and exits. They are useful reference evidence but not a fully reliable gold standard. In particular, old row 6449 turns Bidder 3's ceiling valuation into a $78 point bid, while the filing does not establish an executable $78 offer. Old NDA anonymous identities should not be treated as source-proven identities for the current cohort. Newer voice guidance explicitly qualifies earlier collection.

## Independent reconstruction

PetSmart's spring discussions concerned potentially buying or combining with an industry participant that said it was not for sale. They do not establish a separate earlier auction of PetSmart. Activists pressed for a sale after weak results. The board chose to explore a sale August 13 and announced it August 19. Industry Participant was kept outside the process because of antitrust, information and timing concerns, even though the board would consider a proposal.

Exactly 27 parties approached J.P. Morgan: three strategic parties excluding Industry Participant and 24 financial parties. Exactly 15 financial buyers signed NDAs during the first week of October. Six submitted preliminary IOIs October 30; nine therefore did not. The three original ranges reaching $80 include Buyer Group ($81-$83), another bidder ($80-$85) and an otherwise undescribed third bidder. Bidder 2 originally bid $78 and then raised to $81-$84 during October 30-November 2. It is the fourth, not third, qualifying bidder after that increase. On November 3 the board advanced four and eliminated two.

Two parties subsequently formed Bidder 3, though the filing explicitly confirms only one member's final-round invitation. The leading reconstruction is that the two unnamed finalists combined, leaving three units. The final-round deadline moved from December 5 to December 10, and then to December 12. Buyer Group and Bidder 2 submitted final written offers; Bidder 3 said its valuation would not exceed about $78 and made no written offer. The final cash path is Buyer Group $80.70 -> $82.50 -> $83.00 and Bidder 2 $80.35 -> $81.50. Signing and announcement both occurred December 14.

## Confirmed or narrow corrections

### P1. Nine non-submitters are an inferred residual but are recorded as reported

**Current-instruction error. Severity: low; confidence: high.** Cells: Deal ledger O24, B24/U24/V24 and P24/Q24 (event #23).

P00755 establishes 15 financial NDA signers; P00760 says "six ... submitted indications of interest" and that J.P. Morgan later spoke with parties "including those that did not submit an indication" (pp. 23-24). The exact nine is subtraction, not a directly enumerated statement identifying nine exits. The workbook correctly records Count = 9, `Did not submit`, and reason `Not stated`, but leaves Inferred blank and gives an observed-day presentation.

C16 expressly places the known-by-subtraction non-submitter case under inferred closures. Minimum correction: O24 = Y and `by 10/30/2014`; Date to/Sort date October 30, with any Date from based on actual last supported live evidence rather than implying nine observed same-day departures. Retain the 15 - 6 arithmetic and current reason. This changes provenance and temporal certainty, not the economic total or correct exit category. V0060 supports unknown reasons for these nine.

### P2. Named buyer-side legal adviser is omitted

**Narrow C5 omission. Severity: low; confidence: high that the relationship is supported, with counsel role inferred from the notice block.** No existing row: add alongside the by-signing adviser facts, without altering prices or counts.

The executed merger agreement's Section 8.7 has "To Parent or Merger Sub" (P02878), then Argos, "with a copy to" and "Simpson Thacher and Bartlett LLP" (P02880-P02881, p. A-46). The symmetric Company block names Wachtell Lipton (P02882-P02885), already recorded as target counsel. The source therefore supports Simpson as the Parent/Merger Sub legal representative by signing, although it gives no earlier engagement date or explicit narrative retention sentence.

C5 covers other parties' advisers named anywhere in the filing. Add an Adviser row with client Parent/Merger Sub, date bound by December 14 signing, and a Note that the relationship is identified from the notice-copy provision, not an observed hiring date. Do not date the engagement to the later proxy filing. This is ancillary completeness, not an auction-quality failure.

## Newer Alex guidance and unresolved decisions

### P3. October 3 versus the first-week NDA wave as the round opening

**Newer-guidance mismatch / source interpretation. Severity: medium for stage timing; confidence: high in mismatch, medium in correction.** Cells: B14/U14/V14/T14 (#13 opening), U15/V15 (#14 NDAs), Rounds C2/D2, Questions C2/D2.

Alex V0055 recommends using the October 3 meeting to bound ensuing first-week contacts to October 3-7 and to start round one on October 3. The workbook instead uses October 1-7 and an October 4 sort date, with round one opened by the NDA wave. The source P00754 (p. 23) describes the October 3 meeting as receiving a process update and reaffirming exclusion of Industry Participant; P00755 then reports NDAs "In the first week of October 2014." It does not explicitly say that the meeting authorized those NDAs or that none predated it.

Current C8 fallback 3 supports the first target-organized admission where buyers approached the target, and C10 defines first week as 1-7 unless context narrows it. Thus the workbook is defensible under the literal instruction, while the newer Alex reading infers a stronger causal sequence. Decide whether to adopt that inference. If adopted, round opening becomes October 3 and NDA bounds October 3-7; do not merely replace sort dates without changing the documented basis. This is a localized start-date issue, not evidence for more rounds.

### P4. Bidder 3's two members are not both expressly identified

**Source ambiguity, already well flagged. Severity: medium; confidence: high in ambiguity.** Cells: C30/P30/O30 (#29 group change), C35 (#34), Rounds E3 and Questions row 5.

The filing says one member "had been invited into the final round" and the other would drop out unless allowed to team up (P00762, p. 24). It does not expressly identify them as the two unnamed finalists, A and B. Four advanced (P00761), and eventually there were Buyer Group and two other groups (P00788), so the workbook's A+B inference is parsimonious. It is not uniquely proven: one member could be an eliminated IOI submitter or another prior participant, accompanied by an otherwise unreported exit of a fourth finalist.

The workbook marks the group change inferred and poses Q4. Retain that uncertainty; do not treat the arithmetic 4 -> 3 as independent proof of member identity. Its alternative answer should avoid claiming that joining a group necessarily requires a standalone `Re-entered` row: C4 says the group-change row handles membership changes without duplicate exit/re-entry rows. Nor must the count of previously eliminated bidders automatically fall from two to one if one later joins a consortium: a reported earlier exclusion remains historical. Decide the participating predecessor units first, then record only the transitions actually supported. Older rows 6450-6451 and 6459 contain separate anonymous drops and a later Bidder 3 drop, but do not resolve membership.

### P5. The six-party IOI account and five-group summary are not necessarily incompatible

**Source aggregation ambiguity, already questioned. Severity: low to medium; confidence: high.** Cells: Questions C3-F3, P22/P24/P26, Rounds I2.

The detailed background states six submitting parties (P00760); reasons say "first round indications of interest from 5 bidder groups" (P00788, p. 27). Current Q2 properly retains six and flags the difference. Six original parties with two later combining yield five historical groups, so changing the residual counts to 1/10/1 solely to follow the summary could manufacture a correction. The current counts 6 IOI parties, 9 non-submitters and 2 target exclusions are the better supported primary record. They match V0057-V0060, including the otherwise missing third initially high bidder.

### P6. Whether December 5 was reached before revision remains uncertain

**Source timing ambiguity, adequately flagged. Severity: low; confidence: high.** Cells: Rounds F3/G3, P31/U31/V31 (#30), Questions row 6.

P00764 and P00767 (pp. 24-25) place the decision on "December 4 and December 5" and move the deadline to December 10. The workbook treats December 5 as superseded before arrival. Because the original time-of-day cutoff is not given, a same-day revision before submission time is plausible; a reached-date interpretation is also possible under a calendar-day convention. Q5 records the alternative Deadline row and Extended outcome. No forced correction is warranted. The later December 10 -> December 12 extension is explicit and correctly stays inside the final round under C8/C11 and V0061-V0063.

## Price, condition and recipient audit

All final prices are cash per share; early IOIs do not explicitly establish all-cash consideration, so `Not stated` is sound. J.P. Morgan received or discussed the submissions on the target's behalf. No material background price communication was omitted.

| Event / cells | Source | Assessment |
|---|---|---|
| #17, H18:I18, Oct 30 Buyer Group $81-$83 | P00760, p. 24 | Correct original Informal range. |
| #18, H19:I19, Oct 30 unnamed A $80-$85 | P00760 | Correct Informal range; identity carried descriptively without external identification. |
| #19, H20:I20 blank, Oct 30 unnamed B | P00760 | Correctly preserves the third original range reaching $80 without inventing endpoints. Old V6428 = 80 is not proof of a $80 lower endpoint: a range can reach $80 while starting below it. |
| #20, H21:I21, Oct 30 Bidder 2 $78 | P00760 | Correct initial point price before revision. |
| #21, H22:I22 blank, 2 other submitters | P00760-P00761 | Correct residual offers without fabricated prices or identities. |
| #24, H25:I25, Oct 30-Nov 2 Bidder 2 $81-$84 | P00760 | Correct Informal revision and tighter source-supported window; not forced to old AB6435 = Nov 2. |
| #31, H32:I32, Dec 10 Buyer Group $80.70 | P00768/P00771 | Formal with returned documents, Light supported by financing commitment documents and no reported diligence condition. |
| #32, H33:I33, Dec 10 Bidder 2 $80.35 | P00771 | Formal; Unclear conditions correctly avoid inventing missing financing commitments or equating comparative conditionality with Heavy. |
| #34, no price cells, Dec 10 Bidder 3 ceiling about $78 | P00771 | Correct valuation in exit Note, not a point Bid; `Value at or below market price` preserves the signal. Q6 records event-label uncertainty. |
| #37, H38:I38, Dec 12 Bidder 2 $81.50 | P00777 | Correct Formal cash price, financing documents, best-and-final confirmation. |
| #38 then #39, H39:I39 then H40:I40, Dec 12 Buyer Group $82.50 then $83 | P00777 | Correct order and separate economic revisions; oral interim $82.50 can stay Formal following the December 10 Formal offer and final-stage solicitation. |

`Unclear` is reasonable for preliminary conditions, but P19/P20/P22 should not be read as proof that every initial submitter actually performed November diligence: P00763 describes the continuing bidders. This is a minor explanatory overreach, not a wrong price or conditionality label. In particular the two eliminated parties were no longer in the November stage.

The late $83 offer need not be `None`: "with few exceptions, in substantially executable form" and the December 13 board's remaining-open-points caveat (P00777-P00778) support Light. No unsupported post-signing readiness was retroactively imposed on an earlier bid.

## Correctly captured and rejected apparent errors

- **Counts stay exact:** 3 strategic + 24 financial contacts = 27, 15 NDA signers, 6 initial IOI parties, 9 non-submitters and 4 advanced. The approximate 15 expressions of interest is not substituted for the exact NDA total. This addresses V0056.
- **Industry Participant never entered:** an unsolicited expression of interest and permission to send a proposal are not admission under C3; recording target refusal as an Other material event, without an exit, is correct. Its spring exploration is explained in Deal facts rather than turned into a sale process without support.
- **High-bid arithmetic:** the additional unnamed $80-reaching bidder is present in #19, as required by V0057-V0058. Bidder 2's later increase is not used to erase that participant.
- **Target versus bidder decisions:** two low IOI submitters are Dropped by target, while nine never submitted and have no invented exit motives. V0060's claim that the nine were not approached by the bank is not literal source truth: P00760 explicitly says the bank spoke with all parties, including non-submitters. The workbook correctly notes those conversations while leaving their undisclosed reasons unknown.
- **No extra final round:** the November 3 advancement begins round 2; the December 10 improvement request extends that already-final round. Both December 5 -> 10 and 10 -> 12 changes are recorded, improving on old references that emphasize only the second extension.
- **Longview is support:** #16/#36 record rollover terms and permission without a group change or extra auction NDA. The filing's Buyer Group defined term adds Longview after December 12 (P00200), but C4 and V0064 correctly distinguish that legal definition from an independent bidder joining a competing group.
- **Information:** #27 captures updated FY2014 forecasts and distinguishes longer extrapolations not provided to Buyer Group, grounded in P00763/P01091. No blanket claim that all model projections reached bidders is made.
- **Dates and outcome:** December 12 same-bidder prices are ordered correctly; signing and announcement both get December 14 events. Alex V0059 mentions two bids on November 2, but the source dates Bidder 2's initial offer October 30 and its revision October 30-November 2 (P00760); the explicit same-day Buyer Group sequence is December 12 (P00777). Preserve the actual source dates and current correct ordering rather than force the voice note's shorthand date.

## Limits and next decision

No instruction, workbook or source was changed. Correct the small provenance/adviser gaps, adjudicate October 3 stage timing, and preserve Q4's uncertainty until the desired group-transition convention is settled. The core prices, winner type, participation totals and final-stage chronology are ready for a focused human review; continuous bidder identities across the consortium transition are not yet a fully adjudicated research input.
