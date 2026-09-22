# Mac-Gray: revision notes for the controlled revision (C01–C13)

Input: raw v1.13.2 draft `extraction/mac-gray.xlsx` (53 events, 13 Bid rows, 3 rounds, 9 Questions). Output: the same workbook, edited in place. It now has 55 events, 13 Bid rows, 3 rounds and 9 Questions. The only sources used were the v1.13.2 instruction, the Mac-Gray DEFM14A (12/04/2013), the input workbook and the correction packet. `#` below means the **original** event number unless marked "new".

## Dispositions

| Item | Outcome | What changed |
|---|---|---|
| C01 | Applied | Q9 "Why" no longer says no bidder markup is reported. It now cites Kirkland's revised merger-agreement draft of 10/07 (p. 39). The counterfactual in "What changes" is corrected: under an Informal reading, CSC/Pamplona's standing $21.25 (#44) would need a Formal Bid reaffirmed row at 10/07, carried from #44 (E10/E11); Party A and Party B would have no Formal bid. Under the current map #44 is already Formal in a final round, so no reaffirmation row was added. No bid fields changed. |
| C02 | Applied | #2 Quote changed to "authorized Mac-Gray management to work with BofA Merrill Lynch to explore transactional opportunities that might be available to Mac-Gray" (p. 27, 19 words). The date (04/05), Note, and the later Adviser ended (#5) and new-engagement (#6) rows are unchanged. |
| C03 | Applied | #45 Quote changed to the permission passage "to provide Moab with the opportunity to resume discussions … of Moab's shares in the transaction" (p. 38, 22 words). The event, date and Note are unchanged. |
| C04 | Applied | #11 and #12 When changed from "late June–July 2013 (during the next several weeks after 06/24/2013)" to "during the next several weeks after 06/24/2013". Date from (06/24), blank Date to, Sort date, counts and position are unchanged. |
| C05 | Applied | The #22 (Deadline 07/23) Note now says Party C's oral 07/24 bid was reviewed at the 07/25 meeting and its written revision (new #26) came later on 07/25, after that meeting. Both Party C Bid rows, their dates, prices and round, and the "Late bids accepted" outcome are unchanged. Q4 changed only by renumbering. |
| C06 | Applied | See "Entry/exit reconciliation" below. #17 is kept (Count 16), with a Note caveat about what its placement does not show. #23 was moved and relabelled to one inferred cohort closure, "Dropped by target, by 09/11/2013" (new #37). Rounds R1 and R2 and Q5 were rewritten, and Q2 was changed where it depended on "19". |
| C07 | Applied | Inserted new #50, 09/27/2013, Other material event, for execution of the MacDonald voting agreements by Mr. MacDonald, his wife and one of his trusts. The quote is from p. 39 (30 words). The Note separates execution (09/27) from effectiveness at signing (10/14, new #54) and says this is not an entry, group change or offer. Price, cash, formality, conditions and Count cells are blank. |
| C08 | Applied | #40 Note now includes the option terms: 10% of the new equity, strike price equal to Party B's initial cost basis, vesting on achievement of the base case management projections (over five years), excluding future acquisitions. $21.50 stays Party B's own package value ($19.00 cash plus options Party B valued at $2.50). All cash = No, Conditions = Unclear, the financing qualification and all bid fields are unchanged. |
| C09 | Applied | Inserted new #52, "by 10/09/2013", CSC/Pamplona (Strategic, Count 1), Exclusivity changed, recording the extension *request* made through Kirkland. The quote is from p. 40. Date to and Sort date are 10/09; Date from is blank (see "Unresolved issues" below). The Note separates the request from the target's authorization (10/09, conditioned 10/11) and from execution (10/12, new #53). In #51 (new #53), "(reported 10/09)" became "(#52)"; its conditions are unchanged. No deadline event was created. |
| C10 | Applied | Q1 "Why": the 09/11 improvement-request alternative was replaced by "no supported alternative", with the E6 reason. Q1 "What changes": the claim that the round numeral would make the bids Informal was removed; Formality follows E11 (see Q9). The one-process, three-round map, the E5 tests and the gap evidence are unchanged. |
| C11 | Applied | #3 Count = 1. It is still a first contact (Target interest) and is not counted as an entry. |
| C12 | Applied | #14 Inferred = Y. The Note, dates and the 07/23 due date are unchanged. |
| C13 | Applied | The Round opened marker (#10) now comes before the 06/24 Target sale decision (#9), as new #9 and #10. Dates, content, R1 and its 06/24 start are unchanged. |

## Original-to-new event mapping

| Original # | New # | Note |
|---|---|---|
| 1–8 | 1–8 | unchanged numbers |
| 9 | 10 | swapped (C13) |
| 10 | 9 | swapped (C13) |
| 11–22 | 11–22 | unchanged numbers |
| 23 | 37 | cohort closure reclassified from Did not submit by 07/23 to Dropped by target by 09/11, and moved (C06) |
| 24–37 | 23–36 | shifted −1 |
| 38–49 | 38–49 | unchanged numbers |
| — | 50 | **inserted**: MacDonald voting agreements executed 09/27 (C07) |
| 50 | 51 | shifted +1 |
| — | 52 | **inserted**: CSC/Pamplona exclusivity-extension request, by 10/09 (C09) |
| 51 | 53 | shifted +2 |
| 52 | 54 | shifted +2 |
| 53 | 55 | shifted +2 |

No row was deleted. Every `#` reference in Notes, Rounds and Questions (including Rows affected) was remapped. Question IDs Q1–Q9 are unchanged, so Flag values did not need renumbering. Each Question's Rows affected matches the set of rows carrying its flag: Q5 = new #17 and #37, and the new rows #50 and #52 have no flag.

## Entry/exit reconciliation (C06)

**Population.** The filing reports 20 NDAs "over the next two months" (p. 32): 2 strategic (Party A, CSC/Pamplona) and 18 financial (including Party B and Party C). Dated individually: Party B 06/28, Party C 06/30, CSC/Pamplona 07/11 and Party A 08/05. The residual, 18 − Party B − Party C = **16** unnamed financial signers, is exact and stays on one NDA row (new #17, Count 16, Sort date 06/30, Date to blank). The #17 Note now says its round-1 placement and Sort date are sort keys only. They are not evidence that any of the 16 had signed, or had been admitted, by the 07/23 due date. Party A's 08/05 NDA shows signing continued after that date, but not which of the 16 signed late.

**What was removed.** The exact claim that all 16 "Did not submit by 07/23" (original #23), the Rounds R1 claims "19 admitted" and "16 out (inferred did not submit)", and Q2's "19 to 20" statement. Eligibility for the 07/23 request cannot be established for any of the 16.

**The chosen bound.** Each later transition was checked in order:
- **07/23 due date:** eligibility is unknown for each of the 16.
- **07/25 selection (p. 34):** it named the four advancing bidders, but members who signed after 07/25 were not yet in.
- **08/15 authorization and 08/27 letter (pp. 34–35):** addressed to the same four, but "over the next two months" after 06/24 could reach late August, so a signing after 08/27 cannot be ruled out.
- **09/11 request for final indications (new #36, p. 36):** addressed to "each of Party A, Party B, Party C and CSC/Pamplona". This is the complete continuing set, and it falls after the two-month signing window under any reading.

09/11 is therefore the first transition by which all 16 are established as out. Under E14 ("live in a stage, and the complete advancing set is named … without it"), the cohort gets **one** inferred closure, new #37: "by 09/11/2013", Dropped by target, Count 16, Exit reason Not stated, Inferred Y. Date to and Sort date are 09/11, Date from is blank, and Round is 1, the only stage these signers took part in. The quote anchors the named four-bidder request. The Note says this is a bound, not an exit date, and does not claim that members stayed active until then. Members eligible at 07/23 may in fact have not submitted then; others may have left at 07/25 or 08/27. That split is not invented. Exclusivity on 09/24 and signing on 10/14 are later backstops, and no second closure was recorded at either.

**Accounting (each entry closed once).**
- 20 NDA signers.
  - Party A: entered with the round-0 bid (#8); dropped at exclusivity (new #47).
  - Party B: NDA (#15); dropped at exclusivity (#48).
  - Party C: NDA (#16); Did not submit on 09/18 (#41).
  - CSC/Pamplona: NDA (#20); winner, signing (new #54).
  - 16 unnamed: NDA (#17); one closure by 09/11 (new #37).
- This gives 4 named closures or wins plus 16 = 20. There are no duplicate closures and no re-entries.
- **Live units at round openings.**
  - R1 (06/24): 1 (Party A, entered at its round-0 bid on 06/21 but not admitted to R1). The other entries came during R1.
  - R2 (07/25): the four named bidders are admitted. The number of unnamed signers still under NDA is unknown (0–16), and they are not admitted to R2.
  - R3 (09/11): the four named bidders. All 16 unnamed are out by this date.
- Rounds R1 now lists the three named NDA signers plus "some of 16 other financial NDA signers", with the number signed by 07/23 unknown. The four second-stage invitees are taken directly from p. 34, not by subtraction. R2 notes that unnamed signers were not admitted and that any still under NDA were out by 09/11 (#37).
- The reported contact totals (#11–#13, and Q3's entity-versus-bidder-unit question) and the auction screen (20 parties) are unchanged.

## Unresolved issues (left open deliberately)

- **C06 timing:** the individual signing dates, 07/23 eligibility and actual exit dates of the 16 remain unknown and are kept for later research (Q5). The exit label "Dropped by target" is correct at the bound. It may not describe the earlier path of members who were eligible at 07/23.
- **C09 lower bound:** no request day is reported. Execution of the exclusivity agreement on 09/24 is a logical, but not a reported, lower bound for a request to extend it, so Date from is left blank. Sort date is the single known bound, 10/09.
- **Excluded by the packet and not resolved:**
  - the F02 economic-terms boundary;
  - the F03 separate information-state row;
  - the F04 April label (the April 5 Target sale decision is not reclassified);
  - the withdrawn full-access-row candidate.
- **Other items not added or changed, as the packet directs:**
  - no bid or round for the legal negotiations;
  - no information-access row for Party A or for CSC/Pamplona during exclusivity;
  - no changes to Conditions on exclusivity-request bids, the Q3 question, the winner's Type or the deadline Questions.

## Self-check performed

- The input was compared cell by cell with the output. Every changed cell maps to C01–C13 or to a `#` dependency.
- All 13 Bid rows keep their bidder, When, dates, process, round, prices, All cash, Formality, Conditions, Count and Type.
- Round opened rows are new #9, #25 and #36. Round boundaries, finality, due dates and outcomes are unchanged.
- Sort date never decreases down the ledger. Date and number formats, styles, column widths, freeze panes and blank Reviewer notes are preserved. The filter was extended to A1:V56 for the two inserted rows.
- Every ledger quote matches the filing text exactly (whitespace-normalised) and has at most 30 words.
