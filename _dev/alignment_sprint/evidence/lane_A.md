# Lane A audit: stages, rounds, processes and deadlines

Instruction: `SEC_Deal_Ledger_Extraction_Instruction.md` v0 (cited by rule and line). Alex: voice notes (V¶n), collection instructions (CI p.N). STATUS: `_dev/STATUS.md`.

Filings checked: Kraton, Mac-Gray, sTec, Penford, Providence & Worcester, Synacor (SC TO-T), PetSmart, plus Meredith's round passages and Datalink's post-exclusivity passage.

## Not reopened (settled in STATUS)

- Meredith scope (LMG proposals are Other-scope, no exits for partial-only parties).
- sTec Company H dropped by May 16, "would not improve earlier offer".
- Non-submitter counts: Providence 16 (Party A plus 15); Mac-Gray 16 unnamed financial signers closed by July 23. None of the fixes below moves these.
- "Invitees left out of the next stage exit when it opens" (E14 inferred exit 1). A2 changes *when* a stage opens, not this rule.
- Commitment-only changes, Same-offer copying, the condition evidence window.
- Kraton ruling (three rounds, July 6 opens the second informal round) is used as a pass/fail test below.

## Summary table

| ID | Title | Type | Severity | Needs Alex |
|---|---|---|---|---|
| A1 | Improvement request to a narrowed field after a round's offers | CONFLICT | High | No (ruling decides Kraton) |
| A2 | Offer-less selection: round opens at the later request, Alex opens it at the decision | CONFLICT | High | Yes (confirm date) |
| A3 | Trigger (d): 30-day pause and exclusivity expiry | ADDED | Medium (High if A2 adopted) | Yes |
| A4 | Finality: "final round" label vs non-binding request (sTec) | AMBIGUOUS / CONFLICT | High | Yes (already open) |
| A5 | Round 1 in bidder-initiated deals: first NDA vs start of the sale process (Penford) | CONFLICT | High | Yes |
| A6 | Round 1 and sale decision not restricted to whole-company outreach | AMBIGUOUS | High | No |
| A7 | Round 1 dating: "within a week" of an undated outreach; which board meeting | AMBIGUOUS | Low | No |
| A8 | Unreported round opening dated at the first offer | AMBIGUOUS | Low | No |
| A9 | Process gap: 90 days, measured from which contact (sTec) | AMBIGUOUS / ADDED | High | Yes (already listed) |
| A10 | "Enforced" counts mere evaluation; Alex wants decisive action | CONFLICT | Medium | No |
| A11 | Effective deadline when late bids are accepted (Providence) | ADDED | Low | No |
| A12 | Mandatory round-boundary and deadline flags missing | MISSING | High | No |
| A13 | Round of a late answer to an earlier round's solicitation (Kraton Party J) | AMBIGUOUS | Low | No |
| A14 | Row order of a round opening vs the drops it causes (CI p.8) | AMBIGUOUS | Low | No |

Counts: 4 CONFLICT, 7 AMBIGUOUS (A4 and A9 are mixed), 2 ADDED (A3, A11), 1 MISSING (A12). By severity: 7 High, 2 Medium, 5 Low.

## Kraton under v0 and under the proposed fixes (the pass test)

- **v0 as written: 2 rounds (fails the ruling).**
  - Round 1: May 24, 2021.
  - A literal reader could also open a round in late 2020 on the CST outreach (A6).
  - July 6: continuation (A1). July 20: an offer-less selection, which opens no round (A2).
  - Round 2: August 11, opened by (b), Announced as final.
- **With A1, A2, A6 and A13: 3 rounds (passes).**
  - Round 1: May 24. A6 stops the 2020 CST outreach from opening a round.
  - Round 2: July 6 under A1. Party J's July 19 bid carries round 2 (A13).
  - Round 3: July 20 under A2. It is Announced as final by the August 11 letter. Parties I and J are Dropped by target on July 20.
- **Ruling check.** The ruling fixes July 6 but is silent on round 3's date. Under v0's l.187 it would be August 11; under Alex's rule it is July 20.

---

## A1. Improvement request to a narrowed field after a round's offers

- **Instruction.** E6 (a), l.182: "selects which bidders advance and asks them for new offers". E6 l.189 continues the round for "asking the round's bidders to improve their offers, once or repeatedly, with or without a new deadline". E6 l.187: "When in doubt, the round continues."
- **Alex.** V¶82 (black): Kraton's second round starts on July 6, when "6 NDA agreements have been dropped out, and 4 of them have been allowed into the second round of the informal process". V¶173A (black): a meeting at or after a deadline where "some bidders are dropped and some bidders are approached again" indicates the next round. Kraton "had an interim meeting of the Board during informal bidding, where they dropped some bidders and continued the process; this signifies two rounds of informal bidding." V¶131, ¶146 (Claude's reading): a round starts when the target decides who advances.
- **Type / severity.** CONFLICT, High (round count).
- **Why the instruction fails Kraton.** On July 6 the board asked Party A, Party H, Parent and Party I for updated indications by July 19, "before making any determination regarding which potential acquirers, if any, should be invited into the second round" (p.35). Under E14 inferred exits 3–4, the six NDA signers who did not bid have already exited at the June 29 due date. So the four asked are exactly the round's live bidders. The request is "asking the round's bidders to improve their offers ... with a new deadline" (l.189). The round continues. The board's own words also deny a selection. Result under v0: round 1 (May 24), round 2 opened August 11 by the final bid procedures letter. **Two rounds, not the ruled three.**
- **Deals where it bites.**
  - Kraton: v0 gives 2 rounds; the ruling and Alex give 3 (July 6 = round 2).
  - PetSmart (must not change): on December 10 the ad hoc committee told the two written bidders to improve by December 12. Bidder 3 had given only a verbal "not above ~$78" and was told it was unlikely to be competitive. Alex (V¶61): "just a continuation of round two". A bare "someone eligible was left out" test would wrongly open a round here.
  - Providence (must not double-count): the mid-June LOI request went to all seven parties kept on June 1. It must not open a round beyond the June 1 selection (see A2).
- **Recommended fix.** Replace E6 (a) at l.182 and add one sentence after l.189:

  > (a) after the due date of the current round's offers, or after receiving them, sends a common request for new offers (the same terms and due date for all recipients) to some but not all of the round's eligible parties. The round's eligible parties are those that had entered the process (E3) and could bid in the round, whether or not they bid. A party that had withdrawn, or had been excluded, before the request no longer counts. Price feedback or an improvement request to one bidder is not a common request. The target's own description of the step ("updated indications", "before deciding who advances") does not change this. Count what the target did.

  Add after l.189:

  > Within a round announced as final, or opened by (c), further requests to the remaining bidders continue that round even if a bidder has dropped out.

  Keep "asking the round's bidders to improve" (l.189) as continuation when every eligible party is asked again.

  Tests where the rule must fire:
  - Kraton July 6 opens round 2 (the six NDA non-submitters and Party J were not asked).
  - sTec May 16 opens round 2. Company H had entered (NDA May 8, indication May 15) and was not sent letters. Company G had withdrawn on May 3.
  - Mac-Gray September 11 opens round 3 under (b).

  Tests where it must not fire:
  - PetSmart December 10 continues the final round (carve-out).
  - Providence mid-June: all seven eligible parties were asked.
  - Mac-Gray August 27: all four were asked.
  - Providence July 26: feedback to G&W alone, which Alex places in round 2 (V¶18).
  - sTec May 15: Company D alone was told to "meaningfully increase".

  An eligibility test based only on "invited to bid" would miss sTec, because the filing reports no process letter to Company H.
- **Needs Alex?** No. The Kraton ruling decides the case, and V¶173A states the general rule.
- **Confidence.** High on the conflict. Medium-high that the proposed wording matches Alex in unseen deals, because V¶173A is phrased as a flag trigger ("likely start"), not a definition.

## A2. Offer-less selection: when does the round open?

- **Instruction.** E6 l.187: "A selection that asks for no offers opens no round; the round opens at the request that follows ((a) or (b))."
- **Alex.** V¶44 (black), Mac-Gray: "round two of informal bidding starts on July 25 ... Initially, round two did not have a deadline, but on August 27, this deadline was announced as September 9." V¶131 (Claude's reading, endorsed ¶168): "a round starts when the target decides who advances or launches the next stage". V¶173A (black): the meeting where bidders are dropped marks the likely start.
- **Type / severity.** CONFLICT, High (stage opening date; which events fall in which round; exit dates).
- **Deals where it bites.**
  - Mac-Gray: on July 25 the Special Committee approved "a proposed process for the second stage": management meetings, "and to then request that each of these parties submit a revised indication of interest". The written request went out on August 27. v0 opens round 2 on August 27; Alex opens it on July 25. Party A's August 5 NDA and first entry, and the four management presentations, fall in round 1 under v0 and in round 2 under Alex. Round count is 3 either way. The settled "16 closed by July 23" is unaffected, because those parties exit at the round-1 due date.
  - Kraton: on July 20 the board invited Party A, Party H and Parent "to the second round" with more diligence; the offer request is the August 11 final bid procedures letter. v0 opens round 3 on August 11; Alex's rule opens it on July 20. E14 inferred exit 1 moves with it: Party I and Party J are "Dropped by target" on August 11 under v0, three weeks after the filing shows they were left out. **Austin's ruling is silent on round 3's date.**
  - Providence: the Transaction Committee excluded the two low bidders (May 23 to June 1) and authorized presentations for seven. LOIs were requested in mid-June. v0 opens round 2 in mid-June; Alex's rule opens it at the June 1 decision. Party C's early-July entry falls in round 2 either way.
- **Recommended fix.** Replace the l.187 sentence with:

  > Where the target decides who advances and requests offers from them later, the round opens at the decision, provided a request for offers from those parties follows. If the decision is not reported, the round opens at the request. If no request follows and the target negotiates definitively with the selected parties, (c) applies at the decision.

  E14 inferred exit 1 then dates the non-selected parties' drops at the decision. Finality of a round opened at a decision is read from what the target told bidders during the stage. For Kraton, the August 11 "final bid procedures letter" makes round 3, opened July 20, Announced as final.
- **Needs Alex?** Yes. "When the target picks who advances but asks for new offers only weeks later (Mac-Gray July 25 → August 27; Kraton July 20 → August 11), does the next round start at the selection or at the request?" His Mac-Gray note answers "selection". Confirm it is general.
- **Confidence.** High for Mac-Gray (Alex is explicit). Medium as a general rule.

## A3. Trigger (d): 30-day pause and exclusivity expiry

- **Instruction.** E6 (d), l.185: "asks bidders for offers again after a pause of 30 days or more in which it solicited none, or after an exclusivity period with one bidder ended."
- **Alex.** Neither the 30-day pause nor the exclusivity-expiry trigger appears in his words. On Synacor (V¶109, dark red) he treats renewed contacts after one bidder's exclusivity lapses as the same *process*, and says nothing about rounds.
- **Type / severity.** ADDED. Medium; High if A2 is adopted, because the two then interact.
- **Deals where it bites.**
  - Mac-Gray: July 25 → August 27 is 33 days with no written request. Today this is harmless, because the round opens on August 27 under l.187 anyway. Under A2, round 2 opens on July 25. A literal (d) could then fire again on August 27, giving **four rounds**. Alex's note (V¶44) treats August 27 as setting round 2's deadline.
  - Synacor: E's exclusivity expired October 23, 2020. The October 27 and December 18–21 steps were outreach to gauge interest, not requests for offers, so (d) does not fire as the filing reads. Whether "re-initiate outreach" counts as asking for offers is itself a reading call.
  - Datalink (not discussed by Alex): Insight's exclusivity expired September 30, 2016. On October 1, Raymond James called Party B and Party C and sent them revised merger-agreement drafts, and Party C reaffirmed $11.25 on October 4. Under (d) this opens a new round after the final round. Alex has no stated view.
- **Recommended fix.** Replace (d) at l.185:

  > (d) asks for offers after the previous round has ended (its offers were acted on, or a winner or exclusivity was chosen) and either 30 days or more passed with no stage in progress (no solicitation, diligence or negotiation with any bidder), or an exclusivity period with one bidder ended. Carrying out a stage already decided under (a) or (b) is not asking "again".
- **Needs Alex?** Yes. "After exclusivity with one bidder lapses and the target goes back to earlier bidders for offers (Datalink October 2016), is that a new round of the same process, or a continuation of the final round?" Also: "Should a long pause inside one process, with no bidding, start a new round when bidding resumes?"
- **Confidence.** High that the interaction exists. Medium on Alex's answer.

## A4. Finality: "final round" label vs a request for non-binding offers

- **Instruction.** E6 (b), l.183: a round begins when the target "first asks for final, binding or best-and-final offers". Finality, l.195: "**Announced as final**: the target told bidders this was the final, binding or best-and-final stage". E6 l.179: "Infer rounds from what the target does, not from the filing's or the banker's vocabulary." E11 route 2 (l.251) makes every answer to a final solicitation Formal.
- **Alex.**
  - V¶124 (dark red): sTec's May 16 step started "round two of informal bidding".
  - V¶125 (dark red): WDC's May 28 bid came "even though this is not the final round".
  - V¶27 (dark red): the lucky case is the target "saying, this is the final round of bidding, or that everybody must submit formal committing bids".
  - CI p.8: "If there is also a final round of informal bids, record 'Final Round Inf Ann' and 'Final Round Inf'."
  - CI p.7 and p.9: bids after a final-round announcement are formal.
  - Alex's statements conflict with each other. STATUS "Open with Alex" already lists this.
- **Type / severity.** AMBIGUOUS in the instruction (l.179 against l.195) and CONFLICT with Alex on sTec. High (round count and finality).
- **sTec facts.** On May 16, "BofA Merrill Lynch sent final round process letters and a draft merger agreement to WDC and Company D". The May 29 paragraph calls this "sTec's request for non-binding proposals on May 28". On May 29 the board asked for "best and final" proposals by May 30.
  - Reading 1, label governs (l.195, V¶27): May 16 opens round 2, Announced as final. May 29 is not the *first* final request, so the round continues. **2 rounds.**
  - Reading 2, substance governs (l.179, V¶124–125): May 16 opens round 2 under (a), Not final, because it asked for non-binding proposals. May 29 opens round 3 under (b), Announced as final. **3 rounds.** Alex's reading is this one.
  - Datalink's August 16 "final proposals" letter and Kraton's August 11 "final bid procedures letter" are unaffected under either reading.
- **Recommended fix.** Do not pick; offer Alex two general rules.
  - Rule L (label): "A round is final when the target calls it the final round or asks for final, binding or best-and-final offers." This is v0 as written; it gives sTec 2 rounds.
  - Rule S (substance): "A round is final when the target asks for binding offers or best-and-final offers, or says no further round will follow. A letter titled 'final round' that asks for non-binding proposals opens a round under (a) but not a final one." This gives sTec 3 rounds and matches V¶124–125.
  - Either way, decouple E11 route 2 from the round label, so that CI p.8's "final round of informal bids" is representable. Route 2 would then apply only when the solicitation asked for binding or best-and-final offers.
- **Needs Alex?** Yes. "sTec's May 16 letters were titled 'final round' but asked for non-binding proposals with a merger-agreement markup; on May 29 the board asked for best and final. Which step starts the final round: the letter labelled final, or the first request for binding or best-and-final offers? And can a final round consist of informal bids (your CI p.8)?"
- **Confidence.** High that the conflict exists. The answer is Alex's call.

## A5. Round 1 in bidder-initiated deals: first NDA vs start of the sale process

- **Instruction.** E6 l.191: "where buyers came to the target, or it sounded out a single party (Target interest), at the first NDA or price negotiation the target holds with a whole-company bidder". Approaches and proposals before that are round 0.
- **Alex.**
  - V¶71 (black), Penford: "unless the starting date is explicitly stated in the background, round one of bidding starts at the point in time when a target starts the sale process". He lists Ingredion's round-1 bids as "$18.25-18.5, then $18.5, then $19". The August 10 $18.00 bid is not in the list.
  - V¶173A (black): with no stated start, round 1 starts "when the target's investment bank first starts contacting bidders".
  - V¶42 and ¶55 (black): the board meeting that decides to start the sale.
- **Type / severity.** CONFLICT, High (stage opening; round of the first priced bid). The round count is unchanged.
- **Penford.** Ingredion approached; the Secrecy Agreement took effect July 20, 2014; Ingredion offered $18.00 on August 10. The board approved a "market check" on August 28, and Deutsche Bank contacted six strategics "throughout early-to-mid September".
  - v0 opens round 1 on July 20, so the $18.00 bid is round 1.
  - Alex's rule opens round 1 on August 28 (board) or early September (first bank contact), so $18.00 is round 0. His list is consistent with this but does not say so outright.
  - Mac-Gray is unaffected: its June 21 Party A proposal falls before the June 24 launch under both.
- **Recommended fix.** Replace the "where buyers came to the target ..." clause of l.191 with:

  > Where buyers came to the target, or it dealt with a single party, round 1 opens when the target starts a sale process: the board's decision to solicit other buyers or to run a market check, or, if the target never solicits others, its decision to negotiate a sale with that bidder. Talks, confidentiality agreements and proposals before that are round 0.
- **Consequence to state.** In a purely bilateral deal with no market check, the proposed clause makes round 1 coincide with (c). Round 1 becomes the Inferred-final negotiation round, and every earlier priced exchange with the bidder is round 0. v0 instead gives such deals an informal round 1 (from the NDA or first price talk) and a final round 2 under (c).
- **Needs Alex?** Yes. "At Penford, is Ingredion's August 10 $18 indication round 0 (before the August 28 market-check decision) or round 1? More generally, do bilateral talks and an NDA with an approaching bidder open round 1 before the board decides to sell or market-check? In a purely bilateral deal, should the pre-negotiation price exchanges be an informal round 1, or round 0 before a single final round?"
- **Confidence.** Medium. His ¶71 list omits $18 but never labels it round 0.

## A6. Round 1 and the sale decision are not restricted to whole-company outreach

- **Instruction.** E6 l.191: "Round 1 opens at the target's first outreach to two or more prospective buyers". D2 l.85: "Target sale decision: the board decides to explore or pursue a sale". E6 l.179: a round is when the target "asks a set of bidders for offers on common terms". None says whole company. E1 restricts counts and exits, not rounds.
- **Alex.** V¶96 (black), Meredith: a board discussion of selling a segment "did not discuss the sale of the entire company, and yet the AI has recorded this as the start of the sale process. This is factually incorrect." CI p.7: only whole-company bids are collected.
- **Type / severity.** AMBIGUOUS, High (it breaks the Kraton test).
- **Deals where it bites.**
  - Kraton: in late 2020 and early 2021, management and J.P. Morgan discussed selling the CST business with Parties C, D, E, F and G. That is literally "outreach to two or more prospective buyers" and would open round 1 then. This gives Kraton **four rounds**, and puts the whole-company launch (May 20–24, 2021) in round 2.
  - Meredith: the filing's "first round" and "second round" for the select stations, and the LMG final-offer letters, would open rounds. Meredith is excluded from estimation (settled), but the rule is general.
- **Recommended fix.** In E6 l.179 and l.191, insert "for the whole company (E1)": "asks a set of bidders for offers for the whole company on common terms"; "first outreach to two or more prospective buyers of the whole company". In D2 l.85: "the board decides to explore or pursue a sale of the whole company". A solicitation for part of the company goes in the Note of the Other-scope bid rows and opens no round.
- **Needs Alex?** No. V¶96 and CI p.7 are clear.
- **Confidence.** High.

## A7. Round 1 dating details

- **Instruction.** E6 l.191: "dated at the board decision that launched it if the outreach followed within a week".
- **Alex.** V¶42: Mac-Gray's round 1 starts June 24, at the committee meeting. V¶55: PetSmart's October 3 meeting "would also indicate that ... round one ... starts on October 3". V¶173A: at the bank's first contact when no start is stated.
- **Type / severity.** AMBIGUOUS, Low (a few days' shift).
- **Deals where it bites.**
  - Mac-Gray: outreach ran "during the next several weeks" after June 24, with no start date, so "within a week" cannot be tested. v0 is undetermined: June 24, or "late June" with Date from June 24. Alex says June 24.
  - PetSmart: the launch decision was August 13 (announced August 19), and bidders contacted J.P. Morgan inbound. v0's buyers-came branch gives the first NDA, "first week of October" (Sort date October 1). Alex says October 3, the board meeting.
  - Providence: the March 24 committee authorization and "week of March 28" contacts straddle the one-week window.
- **Recommended fix.** Add to l.191:

  > If the outreach is undated but reported as following the decision, date round 1 at the decision.

  For an announced public sale process, the launching decision is the one that authorized the solicitation.
- **Needs Alex?** No.
- **Confidence.** Medium.

## A8. An unreported round opening is dated at the first offer

- **Instruction.** E6 l.187: "the Round opened row is Inferred = Y, dated at the first offer".
- **Alex.** V¶25 (dark red): when the start is not mentioned, infer it once "the previous round of bidding has finished, and ... the target has allowed them to continue bidding and contacted them for an offer update". This dates the opening at the target's permission or contact, before the first offer.
- **Type / severity.** AMBIGUOUS, Low. Rows between the permission and the first offer (diligence, drops) take the earlier round number.
- **Deals where it bites.** None of the checked deals has a completely unreported opening. The rule matters for unseen deals.
- **Recommended fix.** Replace "dated at the first offer" with:

  > dated 'by [first offer]', with Date from set to the last event of the previous round, and Sort date at the first offer.

  This is an explicit exception to E8's "'by [day]': Date to only" (l.212); say so in the text.
- **Needs Alex?** No.
- **Confidence.** Medium.

## A9. Process boundary: 90 days, measured from which contact?

- **Instruction.** E5 (b), l.171: "90 days or more pass with no reported sale contact between the target or its advisers and any prospective acquirer". E8 l.215: an undated event is bounded by its neighbours.
- **Alex.**
  - V¶118 (black), sTec: "a gap between contacts ... from November 2012 to February 2013. This is a 3 month gap ... clearly identifies two separate processes."
  - V¶108 (dark red), Synacor: a 9-month gap makes separate processes.
  - V¶109 (dark red): a 4-day gap after exclusivity lapsed, with the bidder still in, is one process.
  - V¶132 (Claude's reading): gap length plus continuity of participants.
  - Alex never states a number. STATUS lists "the process-boundary test (a reported end, or 90 days of silence)" among working conventions to confirm.
- **Type / severity.** AMBIGUOUS in measurement; ADDED threshold. High (process count).
- **sTec.** Company A's banker contacted sTec on November 14, 2012. Undated follow-ups came after: a proposed agenda, a draft NDA and a scheduled meeting, then the cancellation communicated to Company A. The follow-ups continued discussions. E8 bounds them by November 14 and the next dated paragraph, November 29. The next acquirer contact is Company B on February 13, 2013.
  - From the earliest bound (November 14): 91 days, so **two processes**.
  - From the latest bound (November 29): 76 days, so **one process**.
  - Conditions (a) and (c) hold: no offer was outstanding, and the special committee was formed on February 13. v0 does not say which bound to use, so the process count is undetermined.
- **Synacor passes either way.** Company C talks ended in October 2019, and Company E came in on July 13, 2020. The Company D talks in between are the target buying D, which E1 places outside the sale process. The October 23–27, 2020 gap is blocked by (a), because E's offer was outstanding. Both outcomes agree with Alex.
- **Recommended fix.** E5 must state how an undated contact enters the gap. Two general candidates:
  - Rule C (conservative): an undated contact takes its latest supported date. A new process needs the full 90 days on every reading. This gives sTec **one process**, against V¶118.
  - Rule M (month count): where either end of the gap is dated only to a month or a bounded range, count calendar months between the last contact month and the next contact month. Three or more months passes (b). This gives sTec **two processes** (November → February), agreeing with V¶118. Synacor and every exactly-dated gap are unchanged.

  I do not recommend choosing "earliest supported date" only because it reproduces Alex's sTec answer. That would be a rule justified by one deal. Rule M has an independent basis in Alex's own measure ("a 3 month gap"), but it too rests on this one comment. Also add, whichever rule is chosen: "A message that only ends, declines or cancels discussions does not count as a contact." This is a sound general principle, but on its own it does not decide sTec, because the continuing follow-ups are equally undated.
- **Needs Alex?** Yes, on the threshold and on the measurement (already on the STATUS list). "Is roughly three months of no contact with any buyer, with no offer outstanding and a fresh board step afterwards, the test for a new process? When the last contact is undated (sTec: follow-ups with Company A between November 14 and 29, 2012; next contact February 13, 2013), do you count months, or require 90 days on the latest possible date?"
- **Confidence.** High that v0 is undetermined on sTec. Low on which rule Alex wants.

## A10. "Enforced" counts mere evaluation; Alex wants decisive action

- **Instruction.** E9 l.227: "**Enforced**: after the date, the target acted on the bids in hand (evaluated, selected or gave feedback)". l.228: "**Passed without action**: bidding continued with no reported step on the bids in hand."
- **Alex.** V¶122 (dark red): sTec's May 3 deadline passed and "it doesn't look like the target has done anything decisive ... the bidders continued making offers without an announcement of the next round". That makes it soft. V¶124 treats enforcement as dropping bidders and starting the next round. V¶123 and ¶174B ask to record whether deadlines were enforced or extended.
- **Type / severity.** CONFLICT in definition, Medium. A board that only reviews the bids and lets bidding drift would be "Enforced" under v0 and "soft" for Alex.
- **Visible deadlines under the tightened wording:**

  | Deadline | Outcome, v0 and tightened |
  |---|---|
  | Kraton June 29 | Extended (late bid accepted) (J bid July 19) |
  | Kraton July 19 | Enforced (July 20 selection) |
  | Kraton September 15 | Extended (late bid accepted) (Party A September 17, considered September 18) |
  | PetSmart October 30 | Enforced (November 3 selection). Bidder 2's revision after feedback was not a late required response |
  | PetSmart December 10 | Extended |
  | sTec May 3 | Extended (late bid accepted) (D May 10, H May 15) |
  | sTec May 28 | Extended (May 30 due date set May 29) |
  | sTec May 30 | Enforced (May 30 decision) |
  | Mac-Gray July 23 | Extended (late bid accepted) (B and C on July 24) |
  | Mac-Gray September 9 | Extended (late bid accepted) (A and C on September 10) |
  | Mac-Gray September 18 | Enforced (September 19 choice) |
  | Providence May 19 | Extended (late bid accepted) (IOIs through June 1) |
  | Providence July 20 | Extended (late bid accepted) (G&W July 21 and 26) |

  None of the visible outcomes changes. This is evidence that the fix is general and not tuned to one deal. It matters in unseen deals where a deadline passes, the board reviews, and bidding continues with nobody cut.
- **Recommended fix.** Replace l.227–228:

  > 3. **Enforced**: after the date, and on the bids in hand, the target selected or excluded bidders, opened the next stage, or chose a bidder for negotiation or exclusivity.
  > 4. **Passed without action**: bidding continued with no such decision; board review or price feedback alone falls here.
- **Needs Alex?** No. V¶122–124 are explicit.
- **Confidence.** Medium-high.

## A11. Effective deadline when late bids are accepted

- **Instruction.** D3 l.113–114 record the stated due dates and one outcome each. E9 l.226: "Extended (late bid accepted)".
- **Alex.** V¶18 (black), Providence: G&W's July 26 revision "is still a part of round two of bidding, and July 27 is a fair assessment of the deadline". V¶17 uses the effective window to fix the order of events.
- **Type / severity.** ADDED, Low. v0 is consistent in substance: the revision stays in round 2 and the outcome shows softness. Alex also wants the effective close.
- **Deals where it bites.** Providence (July 20 stated; July 27 effective). Mac-Gray July 23 → 25. sTec May 3 → May 15.
- **Recommended fix.** Add to D3 Deadline outcome:

  > For "Extended (late bid accepted)", add "(last late response [date])".
- **Needs Alex?** No.
- **Confidence.** Medium.

## A12. Mandatory round-boundary and deadline flags are missing

- **Instruction.** F l.343: "Raise at most five Questions ... Applying a default is never a Question." l.345: the process Question is required only for more than one process, or a round opened by (d) or by inference. E6 l.187: "When in doubt, the round continues."
- **Alex.**
  - V¶170 (black): the costliest error is recording two rounds instead of three.
  - V¶173A (black): always flag any meeting at or just after a deadline, any drop-and-re-approach, an unstated round-1 start, and any case where the filing's round naming differs from the inferred rounds.
  - V¶174B (black): always flag "any bidding round extension OR the lack thereof following a stated bidding round deadline".
  - V¶110 (dark red): flag every multi-process deal.
  - STATUS notes that ¶169–178 are not implemented.
- **Type / severity.** MISSING, High. The default "the round continues" leans toward the under-count Alex fears most, and nothing forces a flag when it is applied.
- **Deals where it bites.** Every multi-round deal.
  - Kraton: July 6 would be silently coded as a continuation under v0.
  - Mac-Gray: July 25.
  - Providence: June 1 and July 27.
  - sTec: May 3, May 16 and May 29.
  - PetSmart: December 10.
- **Recommended fix.** Do not add a sixth Question, and do not force a list into D4's one-clause "What changes" column. Split the work in two.
  1. **Rounds sheet, new column 11 "Boundary check"** (every round). Give, briefly with pages:
     - the trigger that opened the round and the filing's own round name if different;
     - each board or committee meeting within seven days after one of its due dates, with the decision taken;
     - any drop-and-re-approach;
     - any alternative opening or closing date considered.

     Each due date's E9 outcome is already in column 7. This records Alex's A and B items for every round without using Questions.
  2. **Process Question (l.345).** Also require it, outside the five, whenever a Boundary check entry names an alternative that would change the number of rounds or processes. Its "What changes" names that count.

  Change l.187 to: "When in doubt, the round continues, and the alternative goes in the Boundary check."
- **Needs Alex?** No. He asked for this directly.
- **Confidence.** High.

## A13. Round of a late answer to an earlier round's solicitation

- **Instruction.** E6 l.191: "A bid belongs to the solicitation it answers". E11 l.251: an unsolicited bid during a final round carries that round's number.
- **Alex.** No direct statement. V¶17 places Providence's late entrant Party C in the round-2 sequence. V¶82 counts only the four as allowed into round 2.
- **Type / severity.** AMBIGUOUS, Low.
- **Deals where it bites.**
  - Kraton: Party J was invited in round 1, said it would bid "during the middle of July", was not among the four asked on July 6, and bid $38–41 by July 19. Under l.191 its bid answers the round-1 solicitation, so it would be a round-1 row after round 2 has opened. Alternatively it carries round 2.
  - Providence Party C (July 12) answered no round-2 letter, so it carries round 2 by the "returning unsolicited" clause.
- **Recommended fix.** Add to l.191:

  > A response to an earlier round's solicitation that arrives after the next round has opened carries the round open when it arrives. The Note says which solicitation it answers.
- **Needs Alex?** No.
- **Confidence.** Medium.

## A14. Row order of a round opening vs the drops it causes

- **Instruction.** E8 l.217: "A **Round opened** row is the first row of its round in the ledger." E6 l.191: "an exit row carries the round being left". Same-day order between the two is not fixed.
- **Alex.** CI p.8: the final-round announcement "should precede information in the Bidder Dropouts section ... ('DropTarget')".
- **Type / severity.** AMBIGUOUS, Low (ordering only).
- **Deals where it bites.** Kraton July 20 (I, J). PetSmart November 3 (two eliminated). Providence July 27 (D, E, F, others). Mac-Gray July 25 (under A2).
- **Recommended fix.** Add to E8:

  > On the day a round opens, the Round opened row comes before the exits it causes; those exits keep the round being left.
- **Needs Alex?** No.
- **Confidence.** High on the gap; low stakes.

---

## Checked and consistent

- Deadline set, revised and reached are separate events (V¶15, ¶62–63; CI p.8 "Ext Ann / Ext"): matches E9 l.221.
- "No deadline stated" (V¶75): matches D3 l.114.
- PetSmart December 10 → 12 is a continuation with an extension (V¶61): matches E6 l.189 and E9 "Extended".
- Round naming is inferred, not taken from the banker (V¶82, ¶131, ¶173A): matches E6 l.179.
- (c) rounds match Alex:
  - Penford October 3 opens the final round 2 (V¶72) via (c), Inferred final.
  - Providence July 27 opens an unannounced final round 3 (V¶27) via (c).
- One round column, not two (V¶16): matches D1 col.7.
- Synacor process splits (V¶108–109): E5 gives a new process after the 9-month gap and one process across the October 2020 exclusivity lapse ((a) blocks it).
- Multi-process deals flagged (V¶110): matches F l.345.
- No exit rows for pre-stage contacts or parties never contacted (V¶70, ¶140): matches E3 entry rule and E14.
- Exclusivity with a rival drops the others (V¶76): matches E14 inferred 2.
- Mac-Gray round 3 via September 11 "final indications" and Party A's "best and final" (V¶48): E6 (b), Announced as final.
- Kraton's final round is Announced as final (August 11 "final bid procedures letter").
- Earlier sale attempts recorded with Terminated and Restarted (CI p.9): matches E5 l.173, with the auction screen per process (CI p.4, E1).

## Outside my lane (brief)

- **E11 route 2 vs CI p.8.** Every answer to a final solicitation is Formal, so an informal final round cannot be recorded (see A4). This is Lane B's call.
- **End-of-final-round non-winners.** V¶76 has them "getting dropped out" by the target; E14 uses "Not selected at signing" for parties still in at signing. This is the exits lane.
- **Other mandatory flags.** V¶175–185 ask for flags on winner and formal-bidder type, uncertain NDA counts, dropout reasons, conditionality, IOI-looks-formal, partial-only deals and currency/EV bids. The five-Question cap and "applying a default is never a Question" block them. The A12 structure could host them.
- **Target stock price.** V¶117 asks to track the target's stock price through the process. v0 keeps only reference prices in Notes.
- **Filing link.** V¶170 asks to record the deal background link with page. Deal facts has no source-link field; page numbers are in quotes.
