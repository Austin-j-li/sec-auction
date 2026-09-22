# Mac-Gray acceptance review: supported corrections

The user authorized a full source acceptance review, supported Opus corrections, and verification of every change. This packet contains the lead's adjudicated corrections under the frozen v1.13.2 instruction. It is not an automatic checker report.

Input: the previously verified 55-event candidate, SHA-256 `f54295a242057b0e6f72fddf9555d6b4c007eea10c9fc13b1202b659439e112e`. Event numbers below refer to that input. Preserve the existing 13 bids' core fields, all process/round assignments and population bounds. Do not decide the separate research question concerning fee/guarantee negotiations. Do not add economic-term bids in this pass.

## A01 — three omitted named buyer intermediaries

Annex A, section 5.11 (printed p. A-30), names Morgan Stanley & Co. LLC, Deutsche Bank Securities Inc. and Evercore Group L.L.C. as exceptions to the statement that no investment banker, broker, finder or other intermediary retained/authorized for Parent or its affiliates is entitled to a transaction fee. The signed agreement is dated October 14, 2013. This is sufficient for D2 Adviser rows; the exact advisory role and engagement dates are not disclosed.

Add one Adviser row per named firm immediately before existing signing #54. When `by 10/14/2013`, Process 1, Round 3, Sort date and Date to 10/14/2013, Date from empty. Type, Count, price/offer fields, Exit reason and Inferred empty. Reported relationship with a supported latest bound; do not call October 14 the engagement date or identify them as lenders. Use the same exact quote on each:

`“Except for Morgan Stanley & Co. LLC, Deutsche Bank Securities Inc. and Evercore Group L.L.C., there is no investment banker, broker, finder or other agent or intermediary” (p. A-30)`

Note for each: `Named buyer-side intermediary in Annex A §5.11's transaction-fee clause, acting for Parent or its affiliates. Specific role and engagement day are not disclosed; relationship is established by the 10/14/2013 signed agreement.`

## A02 — Kirkland's first involvement is bounded, not exactly September 25

P. 38 dates delivery of the first merger draft to Kirkland September 25. P. 39 reports Kirkland's voting-agreement negotiations during September 24–27. The candidate's statement that September 25 is its earliest reported role is too strong. Actual engagement date is unknown (D2/B/E8).

For #49 only: When `by 09/25/2013`; clear Date from; leave Sort date and Date to September 25. Replace Note with: `Buyer outside legal counsel. Received Goodwin's first merger draft 09/25; also negotiated family voting agreements during 09/24–09/27 (pp. 38–39), so earlier involvement is possible. Engagement day is not stated. Later negotiated Moab's voting agreement.` Keep the existing quotation.

## A03 — quote the direction of the first approach

For #3, replace Quote and page with: `“representatives of BofA Merrill Lynch, as instructed by the Board, telephoned a representative of Party A to discuss generally a possible business combination” (p. 27)`.

The current quote shows Party A's reply; the replacement directly supports target-initiated contact. No other field changes.

## A04 — remove unsupported delivery-medium claims

- #8: replace `Unsolicited written proposal` with `Unsolicited proposal` in Note. P. 30 does not identify a written medium.
- #23: replace `Written preliminary indication` with `Preliminary indication` in Note. P. 33 does not identify a written medium.
- #29: replace Note with `BofA letter to all four bidders (authorized 08/15): revised written proposals due 09/09/2013 to continue to in-depth diligence. Follow-up diligence: Party B telephone call 08/27; Party C in-person session 08/29; Party A telephone call 09/03 (p. 35).`

These do not change Formality or Conditions.

## A05 — distinguish an instruction from completed communication

#19 Note: replace `Communicated to CSC/Pamplona (by BofA) and Rothenberg (by Goodwin).` with `Instructed BofA and Goodwin to convey the decision to CSC/Pamplona and Rothenberg, respectively.` P. 33 reports the instruction, not a dated completed communication.

## A06 — distinguish possible exclusion from implemented exclusion

#7 Note: replace `Moab won a proxy contest: its nominees Rothenberg (Moab general partner) and Hyman elected. Moab owned about 9%; its interest in a possible equity rollover led to Rothenberg's exclusion from the sale process (06/12, 06/24/2013).` with `Moab won a proxy contest: its nominees Rothenberg (Moab general partner) and Hyman elected. Moab owned about 9%. Possible exclusion for rollover conflicts was discussed 06/12; Rothenberg was excluded from the sale review on 06/24 (pp. 29–30).`

## A07 — preserve the timing of full information access

#46 Note: replace `It then got full data-room and management access for confirmatory diligence.` with `During 09/25–10/07 it got full data-room and management access for confirmatory diligence.` P. 38 supplies this window. No separate access row: exclusivity has already displaced both named rivals, and access is retained on the admission/exclusivity row under E2.

## A08 — make the exit comparison chronologically explicit

#47 Note: replace `Its $18.00–$19.00 best and final was below CSC/Pamplona's $20.75; not mentioned again.` with `Its $18.00–$19.00 best and final was below CSC/Pamplona's $20.75 on 09/18 and $21.25 on 09/21; not mentioned again.` Keep Exit reason = Not stated and the inference unchanged. The price comparison is context, not proof of a revealed exit valuation.

## A09 — remove deadline alternatives that contradict fixed E9

Only the `What changes if answered differently` cells:

- Q4: `No supported alternative deadline outcome under E9: the filing reports late bids that the target considered. Party C's later 07/25 written revision is assigned to round 1 because it answers that solicitation; its actual arrival follows the round-2 opening.`
- Q6: `No supported alternative under E9: the 09/10 submissions arrived after the 09/09 due date and were considered. Ignoring a one-day delay would change the fixed convention.`
- Q8: `No supported alternative under E9: the target acted on the bids in hand on 09/19. Subsequent price negotiation with the preferred bidder does not undo that action.`

Keep Recommended answer values and row flags unchanged. This resolves reading/application, not a new research convention.

## A10 — describe the cohort closure as a conservative bound

Q5 Recommended answer: replace with `Unresolved timing. Account for the cohort once by an inferred Dropped by target by 09/11/2013 (#37), a conservative final-stage bound. Leave individual signing dates, 07/23 eligibility and actual exit dates unknown; do not treat the bound as observed timing or a revealed exit reason.`

Do not alter the cohort Count, Sort dates, event type, Date bounds, or Rounds. The filing does not support a unique earliest day for closure of all 16.

## A11 — distinguish non-submission from voluntary withdrawal in the account

Deal facts Account: replace only `and Party C dropped out.` with `and Party C did not submit or reiterate its earlier offer.` P. 36 expressly reports non-submission and no reason; the ledger already uses the correct exit label.

## Permitted dependent work and delivery

Renumber all events after adding the three adviser rows; update every internal `#n` reference and Questions row list, flag relationship and filter range if affected. Preserve exactly the four sheets, headers, formatting, widths, freeze panes, dates as Excel dates, and blank Reviewer note columns. Do not reformat/rewrite unrelated content. Three new rows must inherit the relevant existing adviser row formatting.

Save `extraction/mac-gray.xlsx` and `extraction/revision_notes.md`. The notes must identify each correction and disclose anything not performed. Compare the full workbook against the supplied original before finishing. The mechanical checker will run separately outside this session.
