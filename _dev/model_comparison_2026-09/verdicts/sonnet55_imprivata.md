# Verdict: Imprivata / Thoma Bravo (DEFM14A, 08/10/2016)

## My reading of the filing (Background, pp. 26–37)

- **Before the sale effort.** Thoma Bravo (TB, private equity) approached the Company informally in early 2015 and again in June 2015. It made no proposal, and the Company said it was focused on its plan (p. 26). There was no reported sale contact until January 2016, more than 90 days later. In January 2016 TB repeated its interest and management said the Board would consider a proposal (p. 26). On 03/09/2016 TB sent an unsolicited, non-binding indication of $15.00 cash, to be funded entirely with its own funds' equity, with confirmatory diligence to take 30 days or less (p. 27).
- **Advisers and decision.** Goodwin is first shown acting on 03/10. Barclays was engaged on 04/15 (letter countersigned 04/19). On 05/05 the Board decided to explore a sale, and Barclays contacted 15 parties (11 strategic, 4 financial including TB) between 05/06 and 06/09. Seven signed NDAs: Strategic 1–3, Sponsor A, Sponsor B, TB (05/10) and one unnamed sponsor that "declined interest shortly after executing" (p. 29).
- **Round 1** (opened 05/05, not final). The bid letter went to six parties on 06/03, with indications due 06/09.
  - Strategic 1 withdrew on 06/08.
  - On 06/09 three indications arrived: Sponsor A $16.50, Sponsor B $17.00–18.00, and TB $17.25 "and also provided a form of equity commitment letter and draft merger agreement" (p. 30). The draft merger agreement makes TB's bid Formal by route 1.
  - Strategic 2 and Strategic 3 did not bid.
- **Round 2** (opened 06/12, announced as final).
  - The Board advanced Sponsor A, Sponsor B and TB, and told Barclays to urge Strategic 3 to bid.
  - Strategic 3 left on 06/14.
  - Sponsor A said on 06/15 that it could not meaningfully improve; there was no further contact after that.
  - Strategic 4 was contacted on 06/17 and declined on 06/23 without signing an NDA.
  - Final-bid letters went out on 06/24: markups due 07/07, bids due 07/08.
  - Sponsor B said on 06/29 that its bid would be "significantly below" its June range, and it did not bid on 07/08.
  - TB bid $19.00 cash on 07/08 (diligence complete, full equity commitment, markup sent 07/07).
  - After a request for its best and final offer, TB bid $19.25 on 07/09.
  - On 07/10 the Special Committee directed execution. On 07/11 the Company refused exclusivity.
  - The merger was signed and announced on 07/13 at $19.25 cash.
- **Process count under E5.** The 2015 approaches are a separate, lapsed process. The approach is dated to a month, TB can be followed through it, and no offer was outstanding. More than 90 days passed with no sale contact (June 2015 to January 2016), and the target then took up the new approach. So the deal has two processes, and Initiation (read from process 1) is bidder-led.

## Ranking

| Rank | Workbook | One-line reason | Gap to next |
|---|---|---|---|
| 1 | **C** | The only one that applies E5 correctly (two processes, bidder-led, auction screen split). Its bid and exit codings match A's, and its rows are the most disciplined. | **Small** to A |
| 2 | **A** | Bid, exit and round codings are as accurate as C's, and its Questions sheet is the richest. It misses the process split (it flags this as R1 but resolves it wrongly) and adds information-difference rows that the filing does not support. | **Small** to B |
| 3 | **B** | Has A's process error, plus a Conditions error on the winning $19.25 bid, a Rounds header that fails the schema, and an inconsistent round for Strategic 3's exit. | — |

All three agree on every bid, price, Formality value, exit type and exit reason, and on live counts. The spread between them is small.

## Scores (1–10)

| | Completeness | Accuracy of codings | Evidence | Handling of uncertainty | Instruction compliance |
|---|---|---|---|---|---|
| A | 8 | 8 | 9 | 8 | 7 |
| B | 7 | 7 | 8 | 7 | 6 |
| C | 9 | 9 | 8 | 8 | 8 |

## Verified errors

### Workbook A

| Sheet / row | Says | Should say | Filing passage | Severity |
|---|---|---|---|---|
| Deal ledger (process structure); Deal facts: Number of processes, Initiation, Auction screen, Earlier approaches; Questions R1 | One process. The 2015 approaches appear only in Deal facts. Initiation "mixed". Auction screen "Met (process 1): 7". | Process 1: TB's 2015 approaches (Bidder interest), lapsed. Then an inferred Process restarted in January 2016. Processes = 2. Initiation bidder-led. Screen "Not met (process 1): 0; Met (process 2): 7". Earlier approaches "None reported". Add the "Process:" Question. | "In early 2015, and again in June 2015, representatives of Thoma Bravo informally approached … No specific proposals were made" (p. 26); the next contact is "In January 2016" (p. 26). R1's reason ("January 2016 is within 90 days of the Bid") ignores the June 2015 → January 2016 gap. | Medium (flagged, but E5 decides it) |
| Deal ledger #33, #34, #36 | Other material event "Information difference" for the 06/27 dinner, the follow-up diligence sessions and the 07/01 merger-agreement form | #33: the dinner was offered to both bidders, so it belongs in a Note. #34 and #36: the filing reports no difference, and E2 gives a row only "wherever the filing reports it". | "A dinner … was also offered to Sponsor B. Sponsor B declined the offer." (p. 33) | Low |
| Questions | 10 of 13 entries exceed 60 words | At most 60 words (D4) | — | Low |

### Workbook B

| Sheet / row | Says | Should say | Filing passage | Severity |
|---|---|---|---|---|
| Deal ledger (process structure); Deal facts; Questions R1 | Same as A: one process, Initiation "mixed" | Same correction as A | Same passages (p. 26) | Medium |
| Deal ledger #40 (TB 07/09, $19.25) | Due diligence Not stated; Conditions None | Due diligence Incomplete; Conditions Light. The 07/11 CEO call precedes the 07/11 exclusivity row that closes the window, so it falls inside it. A and C code it this way. | "reviewed certain high-level confirmatory diligence questions" (p. 36) | Low |
| Rounds, header | "How ended" | "How it ended" (D3). The checker marks this as a fail, and it will break a header-keyed load. | — | Low |
| Deal ledger #28; Rounds round 2 | Strategic 3's exit is in Round 2, but #25 and the Rounds sheet say it was "not admitted to phase two" | Make these consistent: if it was not admitted, the exit carries round 1 ("An exit row carries the round being left", E8) | — | Low |
| Deal ledger #30 | Sponsor A Withdrew "by 06/17/2016" | 06/15/2016 | "Following this discussion there were no further discussions between Sponsor A and Barclays" (p. 31) | Low |

### Workbook C

| Sheet / row | Says | Should say | Filing passage | Severity |
|---|---|---|---|---|
| Questions R1 | Lists #23 and #42 as Formal bids that the filing calls non-binding | Also #39 (07/08, $19.00) | "…the terms of, and conditions to, its indication of interest" (p. 34) | Low |
| Deal ledger #39, #42 vs Questions Q3 | Flagged Q3, but Q3's Rows affected omits them | Flags and Rows affected should match (Part F, delivery condition 3) | — | Low |
| Questions | 3 entries exceed 60 words | At most 60 words (D4) | — | Low |

Checker warnings I did **not** count as errors:
- C's blank Count on Process restarted is correct. TB never entered in 2015 (no NDA, no bid), so the marker closes no participation.
- All three code Conditions Light with Due diligence "Not begun" on the 03/09 bid. That fits E12: "only confirmatory … diligence … remains", from TB's own letter.

## Where they differ

| Issue | A | B | C | Which is right |
|---|---|---|---|---|
| Process count and Initiation | 1, mixed | 1, mixed | 2, bidder-led | **C**, under E5 (see above) |
| TB 07/09 $19.25: Due diligence / Conditions | Incomplete / Light | Not stated / None | Incomplete / Light | **A and C** (p. 36 confirmatory call falls inside the window) |
| Round 2 deadline outcome | Passed without action | Passed without action | Enforced | Genuinely open. On 07/08 the SC both sought a higher price and told Goodwin to negotiate terms with TB. All three flag it, so it is not scored. |
| Strategic 3 in round 2 | Not admitted; exit in round 1 | Not admitted; exit in round 2 | Admitted ("Who was in" = 4); exit in round 2 | A and C are each internally consistent, and the filing's "encourage it to continue to participate" supports either. B contradicts itself. |
| Sponsor A exit date | 06/15 | by 06/17 | 06/15 | **A and C** |
| Information-difference rows | 4 (dinner, sessions, form, Q2 call) | 1 (bundled, anchored on the Q2 call) | 1 (Q2 call) | **C**. The 07/07 Q2 update to TB while Sponsor B was still invited is the only difference the filing reports. |
| ChipLinnemann, LLC (paid consultant on the sale, p. 49) | Flagged as R7 | Silent | Silent | A handles it best. Whether it counts as an adviser is open, so not scored. |
| Sponsor A's and Sponsor B's "would not be higher / would be below" remarks | Folded into the exit / Other material event | Other material event, with Q1 asking whether they are Bids | Folded into the exit / Other material event | All code them the same way. B's Q1 is a useful flag. |

**Shared codings I checked against the filing, all correct:**
- TB's 06/09 $17.25 bid is Formal because of the draft merger agreement.
- Stock % is "Not stated" on the 06/09 bids, which do not say cash.
- Strategic 2 is Did not submit by 06/09 (inferred), not Withdrew on 06/12.
- Strategic 3 has no exit at 06/09, because the Board asked it to bid.
- The round map: round 1 opened 05/05 (not final); round 2 opened 06/12 (announced as final by the 06/24 letters).
- Sponsor B is Did not submit on 07/08 with reason Value below earlier offer.
- Auction screen: 7 NDA signers.
- Agreed price $19.25 cash; termination fee $13.6m.

**Shared points I am unsure about, not counted:**
- **TB's 03/09 financing.** "Prepared to finance … entirely with equity from its private equity funds" could be coded Committed or Contingent. A raises this as Q1.
- **Sponsor B's exit reason** could arguably be "Would not improve earlier offer", since it was asked for an improved bid.
- **Possible missing Same-offer row.** In the later 07/09 discussions "Thoma Bravo made it clear that $19.25 per share was its best and final offer". None of the three records this as a separate Same-offer row.

## Fit for research

- **C: usable after light review.** Add #39 to R1 and tidy the Q3 flags. Nothing needs recoding.
- **A: usable after light review.**
  - Add the early-2015 Bidder interest row and an inferred Process restarted row, and renumber processes.
  - Set Initiation to bidder-led and split the auction screen.
  - Drop or fold #33, #34 and #36.
  - Bids, prices, Formality, exits and counts can be used as they are.
- **B: usable after light review, but fix it before any automated load.**
  - Make A's process fix.
  - Recode #40 to Incomplete / Light.
  - Rename the Rounds header.
  - Fix the round on Strategic 3's exit.
