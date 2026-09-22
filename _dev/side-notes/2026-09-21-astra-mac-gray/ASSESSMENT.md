# Mac-Gray: assessment of the raw Astra extraction

The development lead checked the raw Astra workbook against the filing and frozen v1.13.2 instruction. These are lead assessments, not human benchmark labels. Event references below are ledger **#** values; Excel row is # + 1. No corrections were applied to Astra's output.

## Previously identified problems

The [protocol](PROTOCOL.md) fixed these checks before Astra ran. The comparison is with the preserved raw Opus v1.13.2 workbook, not an Opus revision.

| Prior finding | Astra evidence | Assessment |
| --- | --- | --- |
| F01: false claim that no bidder markup / formal reaffirmation could occur under the alternative interpretation | Q6 relies on the September 11 final solicitation and does not claim no markup was reported. The October 7 returned draft is in the filing, p.39. No extra reaffirmation is needed when the standing bid is already Formal in a final round (E10/E11). | Unsupported counterfactual not reproduced. This is avoidance of a false claim, not discovery of a new bid. |
| F06: April adviser row quoted an October 2012 engagement | #1 actually dates and describes the October 23, 2012 buy-side engagement; #2 describes April 5 authorization; #6 ends the old mandate May 15; #7 dates selection for the new mandate May 30. All quoted dates match their sources, pp.27, 29–30. | Original quotation/date mismatch not reproduced. Retaining the old buy-side mandate as a ledger row is a separate scope/representation concern; see below. |
| F07: permission for Moab talks supported only by a statement of Moab's wish | #58 quotes permission to resume rollover discussions, p.38. | Resolved. |
| F08: invented July end to outreach | #14–15 retain an unspecified upper bound; Date to is blank. Their When is “Several weeks after 06/24/2013,” and Notes explain the outreach context, p.32. | Unsupported end date avoided. The source's “During the next several weeks” would be slightly clearer wording. |
| F10: C's July 25 written bid treated as considered at the earlier meeting | #25 mentions B/C July 24 submissions; #32 and Q2 locate C's written revision later on July 25, after the stage decision, pp.33–34. | Resolved. |
| L01: all 16 unnamed signers closed by July 23 despite unknown signing dates | #27 retains the eventual 16 with a June 24–August 24 NDA window. #37 closes the cohort **by August 27**, Inferred = Y, anchored to the complete four-bidder solicitation on p.35. Q5 and Rounds preserve uncertainty over how many were live July 23/25. | Material improvement. This is a conservative common upper bound after the NDA-summary window, not an assertion that all 16 exited on August 27 or that none exited earlier. Earlier individual dates remain unknown. |
| L03: separate September 27 voting-agreement execution missing | #63 records execution by MacDonald, his wife and a trust; its Note distinguishes effectiveness at signing, p.39. #73 retains signing/effectiveness. | Material omission recovered. |
| L04: B's material option terms lost | #52 and Q7 preserve 10% of new equity, strike at initial cost, five-year base-case vesting excluding acquisitions, $19 cash plus options valued by B at $2.50, p.36. Price remains the bidder-attributed $21.50 and All cash = No. | Material terms recovered. |
| L05: extension request folded into October 12 execution | #66 records the request **by October 9**, with no invented exact request day; #67 records the October 11 condition; #68 records October 12 execution, pp.40–41. | Material omission recovered with supported timing. |
| L06a: unsupported alternative removes the first final solicitation as a round | Q1 keeps September 11 as R3; its alternative concerns the second-stage boundary instead. Q4 says later improvements continue the final round. | Original E6 error not reproduced. The proposed July 25/August 27 alternative remains a weaker representation choice than the recommended July 25 opening, which is tied to selected access and revised offers. |
| L06b: A's first-contact Count blank | #3 has Count = 1; #10 separately identifies entry by bid, pp.27, 30. | Resolved without making contact itself entry. |
| L06c: inferred exact deadline-communication timing not flagged | #23 reports the known instruction to bidders but leaves the communication date as June 24–July 23, rather than claiming it occurred by the first dated package. Sort date July 8 is the interval midpoint, not an asserted event day. | Original precision problem avoided. The communication is reported; using an E8 date window does not itself make the event inferred. |
| L06d: round-opening marker follows a row already assigned to that round | #12 is R1 before #13 Round opened, both June 24. Checker reports `round.opening_order`. | Remains. Reorder the same-date marker/trigger rows consistently; no new round or different opening date is needed. |

The four targeted material defects—cohort timing, voting-agreement execution, option terms and extension request—are addressed. The table is a targeted comparison, not an overall accuracy score.

## Bounded source inventory

The earlier inventory covers June 24–August 5, printed pp.30–34. Its original freeze predates both Opus outputs being read. It was withheld from Astra. Routine supporting context is distinguished from an event requiring its own row.

| Inventory ID | Astra row(s) | Source-based assessment |
| --- | --- | --- |
| S01 sale decision | #12 | Present, June 24; ordering defect above. |
| S02 first round | #13 | Present, June 24 decision directly followed by outreach. |
| S03 outreach | #3, #14–18 | 50 contacts reconcile: A 1 + CSC/Pamplona 1 + 13 other strategic + B 1 + C 1 + 33 other financial. Named B/C contact windows are marked inferred. Contacts are not counted as entries. |
| S04 eventual NDA total | #19, #20, #24, #27, #33 | 20 = four named + 16 other financial; exactly two named strategic signers. Timing uncertainty preserved. |
| S05 deadline communicated | #23 | Reported instruction, bounded communication window; no invented exact day. |
| S06 B NDA | #19 | June 28; information package in Note. |
| S07 C NDA | #20 | June 30; information package in Note. |
| S08 Moab rollover approach | #21 | July 3 request/support discussion retained; no additional bidder unit. |
| S09 restriction on Moab talks | #22 | July 6 denial retained. |
| S10 CSC/Pamplona NDA | #24 | July 11, one strategic bidder. |
| S11 A's delayed initial package | #33–34 and Rounds | August 5 catch-up explicit. Routine July 11–23 negotiation dates are omitted, but no earlier A NDA or initial package is invented. |
| S12 July 23 deadline | #25 | Present; Late bids accepted. |
| S13 CSC/Pamplona preliminary bid | #26 | July 23, $18.50 cash. |
| S14 B preliminary bid | #28 | July 24, $17–18 cash, late. |
| S15 C oral preliminary bid | #29 | July 24, $15–17 cash, late. |
| S16 second stage | #31 | July 25; four named invitees and A's NDA condition retained. |
| S17 residual closure without false precision | #37, Q5 and Rounds | Conservative August 27 closure, rather than unsupported exact July 23 count. See L01 above. |
| S18 C written change | #32 | Later July 25, $16–16.50 cash; separate from prior oral bid. |
| S19 A's NDA terms settled / discussions resumed July 27 | #33 context | NDA negotiations summarized without July 27 date or the filing's “2103” typo. E2 allows routine negotiation detail to be folded or omitted; no separate event is required. This is compressed context, not a recovered dated event. |
| S20 A executes NDA | #33 | August 5; A already entered through its June 21 bid. |

No missing required event was established in this bounded passage. That does not establish whole-filing completeness or an omission-recall rate.

## Remaining issues and unresolved choices

**Round 1 membership presentation needs tightening.** `Rounds!E2` correctly labels 50 as solicited and distinguishes the eventual NDA total; `J2` says the July 23 live total is unknown. However, D3 asks for an explicit account of admitted bidders and for a bidder such as A to be listed as “still being received, not admitted.” E2 currently says only that A was already live from June 21. It should explicitly name CSC/Pamplona, B and C as the confirmed first-stage admissions, retain uncertainty over the anonymous financial signers, and distinguish A's live offer from admission. This is a presentation defect, not evidence that Astra counted all 50 contacts as admitted.

**The October 2012 BofA row warrants a scope choice.** Its date and quotation are accurate, and it expressly identifies the buy-side mandate. It does not invent an earlier sale process. E1 nevertheless excludes Mac-Gray's attempt to buy CSC from its sale process, while D2 calls for the earliest adviser relationship. Prefer keeping the prior engagement as context to the first current-sale adviser action in April. Do not call the old quotation mismatch “fixed” without acknowledging this different representation. The separate May termination and new engagement are directly supported.

**The known economic-terms convention remains open.** September 21–23 reverse-fee/no-financing-contingency terms appear in #59's executed-exclusivity Note rather than a new Bid row. The boundary between a material economic bid change (E10) and routine legal negotiation (E2) was not settled by this trial. Astra avoids attributing these later terms to the September 21 priced offer as if contemporaneous.

**Extra information-access rows are not automatically errors.** #34 records A's catch-up package separately; #64 records expanded access during exclusivity. They preserve supported facts. Whether they should be folded into adjacent admission/exclusivity Notes remains the previously identified granularity choice, not a proven improvement or new material mistake.

**The conditions convention is unchanged.** All thirteen bids have the same core classifications as Opus, including Heavy for CSC/Pamplona's exclusive period and A's reiterated final offer, and Unclear for B's final financing. Q6 explains the different treatments. This agreement does not adjudicate the broader Heavy/Light convention.

The additional governance and shareholder-support rows were checked against pp.28–41. No unsupported new material price, bid-date, bidder identity or final-stage change was found in the inspected record. This is a bounded review conclusion, not certification of every possible omission or convention.

## Additional source coverage

#69–71 identify Morgan Stanley, Deutsche Bank Securities and Evercore from merger-agreement §5.11, p.A-30. The clause names them as exceptions to the representation that no retained/authorized investment banker, broker, finder or intermediary is entitled to transaction-related fees. Astra qualifies the role and date as buyer-side fee/intermediary relationships established by signing, rather than inventing appointment days or precise mandates. These rows are absent from the raw Opus ledger and are useful additional coverage, with the limited role description retained.

#72 separately records the October 14 delivery of the Pamplona commitment, using the background's delivery date (p.41) and the financing section's $594m commitment / $50m Pamplona damages limit (p.59). The damages cap is not a cap on the closing-funding commitment. A separate delivery row versus the signing Note is a granularity choice, not an additional price bid.

## Verification

- All 13 bid rows match Opus on date, bidder, round, price endpoints, All cash, Formality and Conditions, and the corresponding filing passages were reread (pp.30, 33–37).
- Every one of the 74 ledger quotations occurs on its cited printed page after whitespace normalization. This validates location and copying; semantic support was assessed separately.
- Eventual NDA population: 20. Closures: 16 anonymous + C + A + B = 19; winner: 1. A's NDA is not counted as a second entry after its June bid. Early populations remain explicitly uncertain.
- Checker v1.5: 1 error and 4 warnings. The error is the round-marker ordering above. Three warnings concern Question length. The deadline-outcome warning is a wording-detection false positive: Q2–Q4 explicitly address all three deadlines.
- Raw output and all protected inputs are checked by SHA-256 in the provenance record. No workbook revision, instruction edit, additional extraction or model audit was performed.
