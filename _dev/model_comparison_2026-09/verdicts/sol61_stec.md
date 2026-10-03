# Verdict: sTec / WDC (DEFM14A, Background pp. 23–35)

Row references below use the ledger's **#** column (event number), not the sheet row.

## Reference reading (what I checked the workbooks against)

- **Process 1 (Nov 2012):** the board decides on a formal review that includes a sale ("mid-November", p. 24). Company A's bank approaches on 11/14/2012; there is a draft NDA but none is signed. The gap to the next dated sale contact (02/13/2013) is 91 days, so under E5 this is two processes.
- **Process 2, round 0:** the special committee is formed on 02/13/2013. Company B shows interest on 02/13 and declines about two weeks later. Company C shows interest in assets only on 03/13. Company D approaches in mid-March.
- **Round 1:** opens 03/26 (board decision; BofA outreach starts 04/01).
  - Contacts: 18 in total. NDAs: E 04/04, D 04/10, F 04/11, G 04/17, WDC addendum 04/17, H 05/08.
  - Exits: F turns asset-only on 04/24 and E shortly after. G quits on 05/03.
  - Bids: D, oral, "greater than $5.60" (04/23); WDC $6.60–7.10 cash (05/03); D $5.75 cash, late (05/10); H $5.00–5.75 cash (05/15).
- **Round 2:** opens 05/16 by trigger (a). Letters and a draft merger agreement go to WDC and D only, so H is dropped as not invited. It is *Not final*, because p. 30 calls it "sTec's request for non-binding proposals". WDC bids $9.15 with a markup on 05/28 (Formal, route 1). D asks for about two more weeks.
- **Round 3:** opens 05/29 by trigger (b), asking for best-and-final bids by 05/30 (Announced as final).
  - WDC holds $9.15 on 05/30 and the board selects it. On 05/31 WDC is "not prepared to move forward … at that time" (Withdrew). D is told it may continue, then disengages on 06/05.
  - WDC re-enters on 06/10 at $6.60–7.10. This bid is Informal because the withdrawal lapsed its markup and invitation.
  - On 06/11 the board demands a single best price. WDC bids $6.85 on 06/14 (Formal by route 2; this is an open point).
  - The board selects WDC on 06/15. On 06/20 WDC sends a draft and makes a "may not move forward" statement over the don't-ask-don't-waive (DADW) waiver (condition H3).
  - Signed 06/23; announced 06/24.

**All three workbooks agree on every item above**, and I verified each against the filing:
- process split
- round dates, triggers and finality
- every bid's price, cash form and Formality
- every exit's date and type
- H's inferred exit on 05/16
- D kept live through the 05/28 and 05/30 due dates
- deadline outcomes
- signing and announcement

The checker's shared warnings are false positives. Process restarted correctly has a blank Count, because Company A never entered. The one-sided $5.60 Note does say "greater than".

## Ranking

| Rank | Workbook | Reason | Gap to next |
|---|---|---|---|
| 1 | **A** | Same correct skeleton as the others, with the most careful dating and E3 cohort arithmetic. It is the only one that records Company C properly and the only one that raises the open 06/14 Formality point as a real Question. Its errors are cosmetic or compliance issues. | A→B **negligible** |
| 2 | **B** | Same skeleton, with the most literal Conditions coding. However, it assigns contacts to cohorts without support in the filing and omits the 06/19 projections event. | B→C **small** |
| 3 | **C** | Same skeleton, but it miscodes Conditions on the pivotal $9.15 Formal bid, omits Company C entirely, and adds a debatable round-2 bid for H. | — |

For research use the three are close: the live counts, round map, Formality and prices would come out the same from any of them.

## Scores (1–10)

| | Completeness | Accuracy of codings | Evidence | Handling of uncertainty | Instruction compliance |
|---|---|---|---|---|---|
| A | 9 | 9 | 9 | 9 | 8 |
| B | 8 | 9 | 8 | 8 | 9 |
| C | 8 | 8 | 8 | 8 | 8 |

## Verified errors

### Workbook A

| Sheet / row | Says | Should say | Filing passage | Severity |
|---|---|---|---|---|
| Ledger #12 (WDC's first row) | Note omits public status | Note should say "public" (E3) | "the following seven publicly traded companies … Western Digital Corporation" (p. 41) | low |
| Deal facts, Account | six asset-only parties "including Companies E and F, stayed outside the whole-company contest" | E and F entered by NDA and left on turning partial, as A's own #19/#21/#27/#28 and auction screen code it | "In total sTec executed six non-disclosure agreements related to the exploration of a potential sale of the company" (p. 28) | low |
| Questions Q2 | Round-2 finality posed as a Question | E6 decides it, so it belongs at most in a Review item ("Applying a default is never a Question", F) | "in response to sTec's request for non-binding proposals on May 28, 2013" (p. 30) | low |
| Questions Q1–Q3 | 85, 73 and 65 words | ≤ 60 words (D4) | — | low |

### Workbook B

| Sheet / row | Says | Should say | Filing passage | Severity |
|---|---|---|---|---|
| Ledger #18 (and #17) | Count basis puts Company G among the nine uninterested parties and leaves Company B outside the 18 | The filing never places G in either group. Company B may belong to the 18, so E3 counts it inside. That leaves 8 residual unnamed contacts, not 9. | "nine prospective acquirers, including the financial sponsor and Company A, indicated they were not interested" (p. 27); "Company G indicated it would not continue in the process" (p. 29) | low |
| Ledger #17 | Company C appears only inside a round-1 Contact cohort dated from 04/01/2013 | C's first contact was 03/13/2013, before round 1 | "expressed a potential interest in exploring an acquisition of particular assets of sTec's business" (p. 26) | low |
| (omitted) | No record of the Cost-Reduction Projections | This is an E2 information event on 06/19/2013 ("projections … withheld after bidding began"); C gives it a row, A a Note | "The Cost-Reduction Projections were also provided to WDC and Wells Fargo Securities, LLC, WDC's financial advisor, on June 19, 2013" (p. 46) | low |
| Ledger #58 | D's call dated exactly 05/31/2013 | The call is undated, so on or after 05/31 (A bounds it correctly) | "At the request of our board of directors, representatives of BofA Merrill Lynch had a call with representatives of Company D" (p. 31) | low |
| Deal facts, Initiation | Sale decision placed "before Company A's 11/14 approach" | The filing gives only "mid-November", so the order is uncertain (A flags this as R1). The conclusion, target-led, stands. | "Consequently, in mid-November, 2012, our board of directors authorized management to contact potential financial advisors" (p. 24) | low |

### Workbook C

| Sheet / row | Says | Should say | Filing passage | Severity |
|---|---|---|---|---|
| Ledger #50 (WDC $9.15, Formal) | Due diligence Incomplete; Conditions Unclear | Due diligence Not stated; Conditions None. The filing says nothing about WDC's diligence between this bid and WDC's 05/30 bid, and silence on a Formal bid reads as None (E12). | "WDC submitted a written second-round indication of interest at a price per share of $9.15 in cash, with a mark-up of the merger agreement" (p. 30); the next mention of diligence is the 05/30 board meeting, after WDC's 05/30 bid | medium |
| (omitted) | Company C absent from every sheet | Needs a dated row or Note for its 03/13 approach and the 04/15 end of talks | "On April 15, 2013, Company C indicated that it was only interested in purchasing limited, select assets of the company" (p. 28) | low |
| Ledger #59 | D's call dated exactly 05/31/2013 | Undated; on or after 05/31 | same passage as B #58 (p. 31) | low |

### Uncertain, not counted

- **A #61, #63 and C #64: Conditions Light for "confirmatory diligence".** The filing says "WDC conducted additional due diligence, including confirmatory due diligence calls" (p. 33). The word "including" suggests that more than confirmatory diligence remained, so B's Unclear is the more literal coding. Still, a week of diligence after the price was agreed could be read as limited.
- **A #52: Light for WDC's 05/30 bid.** A reads it as expedited diligence ("endeavoring to complete diligence … to be in a position to announce a transaction on June 3", p. 31); B and C code it Unclear. Both are defensible.
- **C #48: H's 05/23 statement coded as a Same-offer Bid in round 2.** See "Where they differ".
- **C #67: the DADW condition treated as part of the 06/20 draft and dated 06/20.** The filing does not date the statement, but C flags this as R14.
- **Filing date 08/08/2013 in all three Deal facts.** It does not appear in the supplied text (the proxy is dated 08/07/2013 and mailed on or about 08/09/2013), so I can't verify it.

## Where they differ

| Point | A | B | C | Which is right |
|---|---|---|---|---|
| Conditions on WDC's 05/28 $9.15 Formal bid | None | None | Unclear | **A/B**: nothing in the window says diligence remained |
| Conditions on WDC's 06/14 bid and 06/20 reaffirmation | Light | Unclear | Light (06/14) | Leans **B**: "additional due diligence, including confirmatory" (p. 33) is not "only confirmatory" |
| H's 05/23 "remained interested … not able to increase its indicated value range" (p. 30) | Exit reason only | Exit reason only | Also a Same-offer Bid in round 2, so Rounds shows 2 bidders in round 2 | Genuinely open. A/B follow the instruction's worked example; C has support from E10 ("holds it"; p. 34 says H "could not increase its price above the range"). Note that C counts an uninvited, exited party as a round-2 bidder. |
| 06/20 draft and DADW "may not move forward" statement | Two rows: Bid reaffirmed 06/20 + H3 Bid dated 06/20–06/23 | Same as A | One H3 Bid dated 06/20 | A/B are more faithful to the undated statement; C's single-communication reading is defensible |
| Company C (assets only) | Bidder interest 03/13 + Other material event 04/15 | Folded into a round-1 cohort | Absent | **A** |
| Contact cohort residual | 8 (18 less 10 named) | 4 + 6, with G assigned to "not interested" and B excluded | 9 (17 technology companies less 8 named; C inside) | **A and C** apply E3's "may belong" rule; **B** invents G's group |
| 06/19 Cost-Reduction Projections | In a Note | Omitted | Own row | **C**, with A acceptable |
| D's post-05/31 call | Bounded 05/31–06/05 | 05/31 exact | 05/31 exact | **A** |
| Exit reasons for E, F and D | Other stated reason | Other stated reason | Terms or process | Both defensible |
| Regulatory / Financing on the H3 row | Concern + Antitrust Y / Not stated | Concern + Antitrust Y / Not needed | Not stated / Not needed | All defensible (from the board weighing at signing, p. 36) |
| June 14 Formality (route 2 after the round-3 selection) | Raised as Question Q3 | Review item | Review item | A handles this best; it is the most consequential open reading |

## Fit for research

- **A: usable after light review.** Fix the WDC "public" Note and the E/F sentence in the Account, and consider whether Light on #61/#63 should be Unclear. There is nothing high-severity.
- **B: usable after light review.** Correct the #17/#18 cohort basis, redate #58, and add the 06/19 projections event. The core codings are sound.
- **C: usable after light review.** Recode #50 to Conditions None, decide on H's 05/23 bid row and the round-2 bidder count, add Company C, and redate #59. The round map, prices, Formality and exits are sound.
