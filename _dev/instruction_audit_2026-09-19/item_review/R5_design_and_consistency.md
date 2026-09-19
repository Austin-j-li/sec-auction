# R5 — Item 11 (three design choices) and whole-document "can a model follow this?" review

Reviewer scope: item 11 of `BRIEF.md`, plus a start-to-finish read of `SEC_Deal_Ledger_Extraction_Instruction.md` (19 Sep 2026 revision, 11,719 words, 581 lines) as the extracting model would read it. Nothing was modified. "§" = section of the instruction. "HC nnnn" = Excel line in Alex's hand-collected sheet (`alex_hand_collected_9deals.txt`); "VN" = voice note (`alex_notes.txt`). Old-run evidence = the 12 workbooks in `extraction/*.xlsx` and their text dumps.

Bottom line:

| Design choice | Verdict | Confidence |
|---|---|---|
| `Date method` as its own column | **KEEP WITH REWORDING** (rename one value, define the method after an order-constraint move, give the method for the three inferred closing rows, add one consistency check) | High |
| `Outcome basis` as its own column, plus the `Inferred: …` opening words in Terms | **KEEP BOTH, WITH REWORDING** (opener only on inferred rows; column holds the bare value; one mechanical check) | High |
| `Information access changed` as its own label | **KEEP THE LABEL, REWRITE ITS DEFINITION** — as written it licenses a row for every uniform presentation series and collides with §4's own "no rows for meetings with bidders already under NDA" | High on the label, medium on the exact line drawn |

The whole-document read found no fatal contradiction, but it found twelve tensions (four serious, six moderate, two low; B1.1–B1.12), most of them created by today's edits sitting beside older sentences that were not updated. The three that matter most: (1) §10.1 defines "entered the process" as "responsive to contact, under NDA or bidding", which widens mandatory close-out rows from NDA signers (the fixed decision, and Alex's practice) to every party that answered a phone call; (2) §10.2 tells the model to close, at "a submission due date", "any participant … that has no evidenced outcome" — read literally this closes late submitters (P&W G&W on 07/20; Mac-Gray Party B and Party C on 07/23, Party A and Party C on 09/09) and then needs `Re-entered` a day later; (3) §9.1 gives three different instructions for a bidder-returned draft, and its "one such row per bidder per stage" is contradicted by example §12.C.

---

# PART A — Item 11

## A1. `Date method` as its own column

**(a) Current wording.** §8.1: "**Date method** says how the Working date was chosen: Reported, Inferred (cross-paragraph), Assigned: deadline, Assigned: decision day, Assigned: midpoint, Assigned: bound, or Assigned: sequence. An inferred or assigned date is never labelled Reported." §11.2 field table: "Date from; Date to; Working date; Date basis; Date method | Date bounds, always-filled assigned working date, timing basis and assignment method under section 8." §13.4: "Every row has a Working date and a Date method … no inferred or assigned date is labelled Reported."

**(b) Evidence from Alex.** His own flat schema already carries the distinction, as two date columns: `date_precise` and `date_rough` (header of the hand sheet). `date_rough` is always filled; `date_precise` is filled when he regards the day as known. Where he assigned a day he said how, in a free-text comment: HC 6033 (Party C NDA, precise blank, rough 07/01/2016) "Early july 2016 - what should be the appropriate date? July 1?"; HC 6035 (Party B LOI, 07/20) "Late july -- but the deadline was july 20". VN Providence 9 (line 17 of `alex_notes.txt`, black = important and easy) attributes the mis-ordering to "the inability of the AI to assign a precise date or range of dates to round two bids". So Alex (i) wants every row dated, (ii) wants to know which dates are real, and (iii) currently records the method ad hoc in comments. A controlled column is the systematic version of what he already does, and it gives an exact crosswalk to his schema: `date_rough` = Working date; `date_precise` = Working date if Date method is Reported or Inferred, else blank.

**(c) Can one column be derived from the other?** No.

| Date basis | Date methods it can legitimately pair with |
|---|---|
| Reported day | Reported only |
| Inferred day | Inferred only |
| Reported interval | Assigned: deadline, decision day, midpoint, sequence |
| Approximate window | Assigned: deadline, decision day, midpoint, sequence |
| Relative only | Assigned: decision day, bound, sequence |
| Undated | Assigned: sequence (or deadline / decision day when the row is a response or consequence) |

Basis → method is determinate only for the first two rows; the other four basis values fan out to three or four methods each. Method → basis is determinate only for Reported / Inferred. `Date basis` says what the filing gave; `Date method` says which of the six rules produced the sort key. They are different facts. What the table does show is that **only about 16 of the 42 combinations are valid** — the other 26 are the new error surface (e.g. `Reported day` + `Assigned: midpoint`), and nothing in §13 checks it.

**(d) Downstream and reversibility.** This is the strongest argument for the column. Rule 4 (midpoint) is still provisional pending Alex (changelog: "**Provisional:** rule 4 … pending A1"). With a column, a different ruling is one line in Stata after 400 deals (`replace workdate = datefrom if datemethod=="Assigned: midpoint"`). With the method only in `Why and evidence` prose, a different ruling means re-extraction. The column is also what lets Alex drop or down-weight `Assigned: sequence` rows in any date-sensitive exercise. Scale: under the old instruction 0–14 rows per workbook had no Working date (Opus P&W 14 of 70, Sol P&W 12 of 56, GLM P&W 10 of 62, Opus Mac-Gray 0 of 64), so roughly 5–20% of rows will carry an `Assigned:` value. Reviewer burden is nil: the column sits in a collapsed group.

**Problems with the current wording (all small, all fixable in place).**

1. *Value name.* `Inferred (cross-paragraph)` is narrower than the rule it labels. Rule 1 says "A reported day, or a day established by context", and the §8.1 table says "Inferred day if context rather than an explicit statement establishes it". Context is often in the same paragraph ("the following day", "two days later"). A model will either mislabel those `Reported` (forbidden by "never labelled Reported") or use a value whose name is false. The parentheses also invite drift in a controlled string. Rename to `Inferred`.
2. *Method after the order constraint moves a date.* §8.1: "Where a rule would break this, move the date to the nearest admissible day inside the row's own window and say so in the reason." No Date method value is given for the moved date. If the row keeps `Assigned: midpoint` the column is false; models will improvise. The moved date is, in substance, a sequence assignment.
3. *Inferred closing rows.* The §10.2 table has a "Working date" column (due date / execution date / signing date) but no Date method. The most likely model behaviour is `Reported` with Date from = Date to = the signing date, i.e. a false claim that a silent party left on the signing day. The last paragraph of §10.2 says what is actually known: the participant "was out by that transition".
4. *Advisers.* §5.4 "Use the earliest date the filing shows the adviser selected or acting for that client as the Working date" names no method. Where that day is stated it is `Reported`; where the adviser is merely "shown acting" by a date it is `Assigned: bound`. One clause fixes it.
5. *Circularity.* The order constraint is defined pairwise ("may not precede the Working date of a row the event is known to follow"), but when both rows are assigned, which one moves is undefined, and "inside the row's own window" may contain no admissible day. One sentence fixes the procedure.

**(e) Verdict: KEEP WITH REWORDING.** Exact replacements:

- §8.1, replace "Reported, Inferred (cross-paragraph), Assigned: deadline," with "Reported, Inferred, Assigned: deadline," and in rule 1 replace "(Reported, or Inferred (cross-paragraph))" with "(Reported; or Inferred when context, in the same or another paragraph, rather than an explicit statement establishes the day)".
- §8.1, order-constraint paragraph, replace "Where a rule would break this, move the date to the nearest admissible day inside the row's own window and say so in the reason." with "Fix Reported and Inferred days first; they never move. Then assign the remaining rows in # order. Where a rule would break the constraint, move the assigned date to the nearest admissible day inside the row's own window, set Date method to Assigned: sequence, and say so in the reason."
- §10.2, add one sentence directly under the table: "On these rows When reads “by [that date]”, Date to is that date, Date from is blank, and Date method is Assigned: deadline, Assigned: decision day and Assigned: bound respectively — never Reported."
- §5.4, append to the Working-date sentence: "(Date method Reported when that day is stated, otherwise Assigned: bound)".
- §13.4, after "no inferred or assigned date is labelled Reported" add: "; Date method is Reported exactly when Date basis is Reported day, and Inferred exactly when it is Inferred day".

Not checked: whether any model will actually honour the monotonicity rule; nothing has been run.

## A2. `Outcome basis` as its own column (and the mandated `Inferred: …` opening words)

**(a) Current wording.** §10.2: "Record what the filing reports first, with Outcome basis = Stated. Then … close any participant or residual cohort that has no evidenced outcome with **one inferred row**"; "Begin Terms or outcome with the same words as Outcome basis and show the arithmetic: “Inferred: residual — 15 NDA signers − 6 submitters = 9 non-submitters.”"; §10.3: "Outcome basis is **Stated**, **Inferred: residual**, **Inferred: exclusivity**, **Inferred: silent** or **Inferred: identity**"; §11.2: "Decided by; Exit reason; Outcome basis | Structured participation-outcome assessments, including whether the outcome is stated or inferred".

**(b) Evidence from Alex.** Austin's fixed condition is that the ledger "says clearly in what fashion it was out". Alex's own sheet has only `Drop` / `DropTarget` and never marks inference, although several of his rows *are* inferred residuals: HC 6030 "16 parties | Drop | 06/01/2016" (P&W: the filing never says sixteen parties dropped; it is 25 signers − 9 IOIs) and HC 6942 "16 financial bidders | Drop | 07/25/2013" (Mac-Gray: 20 NDAs − 4 bidders). HC 6057 "Party E/F | Drop | 08/12/2016", comment "Did not engage for a while", is his version of `Inferred: silent`. So the rows are his practice; the stated/inferred marker is Austin's addition and has no counterpart column in his schema. It must therefore survive export as its own variable, because his `Drop` code will absorb stated and inferred exits alike (changelog A3, still provisional).

**(c) Column versus text prefix.** The per-stage balance that §11.4(5) and §13.2 require ("participants entering − stated exits − inferred exits = participants continuing, with the inferred share visible") needs a SUMIFS criterion. `Outcome basis = "Stated"` / `"Inferred*"` on a drop-down column is robust. A wildcard on the free-text Terms column is not: all four old models already vary dashes, colons and capitalisation in Terms. For stacking 400 deals the column is one variable; a prefix is a regex per deal. Model burden is low because for the three inferred kinds the §10.2 table fixes label, basis, Decided by, Exit reason and Working date jointly — the model picks a table row, not five independent values.

**Is the duplicate opener useful or a trap?** Useful, on balance. The expandable groups are delivered collapsed (§11.2), so a hand reviewer sees only the fourteen visible columns; without the opener an inferred exit looks exactly like a reported one, which is the thing Alex would object to most. The trap is real but narrow: (i) the opener has sanctioned variants ("Inferred: residual (base assumes …)", "≥"), which a model may copy into the *column*, breaking the drop-down and the SUMIFS; (ii) a reviewer who corrects the column leaves a stale opener; (iii) read literally, "Begin Terms or outcome with the same words as Outcome basis" applies to `Stated` rows too, and one of four models will start every reported exit with "Stated —". Nothing in §13 checks agreement. All three are fixed by wording.

One further gap: the `Inferred: identity` row has no label. §10.2 says the named party "gets one exit row of its own with **Count 0** and Outcome basis = Inferred: identity" but not whether it is `Did not submit`, `Dropped by target` or `Not selected at signing`. By hand on P&W: Party A is a named NDA signer, never heard of again; Alex gives it "Drop 07/22" (HC 6042), reading it as the "One strategic buyer … elected not to submit an LOI" of the filing. Under §10.2 that is a stated two-party `Did not submit` cohort row plus a Count-0 identity row for Party A — but with which label? It should take the label of the cohort row that covers it.

**(d) Downstream risk.** Low. The worst case is a wrong basis on a row, which is visible and filterable. Dropping the column later is trivial; adding it later means re-reading every exit row of 400 deals. Keep.

**(e) Verdict: KEEP column and opener, WITH REWORDING.**

- §10.2, replace "Begin Terms or outcome with the same words as Outcome basis and show the arithmetic:" with "On an inferred row, begin Terms or outcome with the Outcome basis value and show the arithmetic:" and add after the example: "Stated rows take no opener. The Outcome basis cell holds only one of the five values; qualifiers such as “(base assumes …)” or “≥” belong in Terms or outcome."
- §10.2, in the named-party paragraph, after "Outcome basis = Inferred: identity," insert "under the same label as the cohort row that covers it,".
- §13.3, add: "On every Dropped by target, Withdrew, Did not submit, Participation paused and Not selected at signing row Outcome basis is filled, and an inferred row's Terms or outcome begins with the same value."

## A3. `Information access changed` as its own event label

**(a) Current wording.** §4: "**Keep information-access events as rows:** who was given what information, when, and who was not — staged or differentiated data-room access, management presentations given to some bidders and not others, projections supplied, updated or withheld, a late entrant's catch-up access. Use **Information access changed** (section 11.3), one row per distinct change in access (for example one row for a series of management presentations, naming the bidders and dates), not one row per meeting." §11.3: "Information access changed | Who was given, or denied, what information and when: staged or differentiated data-room access, management presentations, projections supplied, updated or withheld, a late entrant's catch-up access. One row per distinct change (section 4)." Against these, same §4 paragraph above: "**Do not create rows for:** … meetings, site visits, calls and document exchanges with bidders already under NDA".

**(b) Evidence from Alex.** Three places, all his own comments attached to a row he already had, never a row of their own (Excel comments carry no colour code, so authorship rests on the capitals and brackets being his annotation style):
- HC 6945 (Mac-Gray, on Party A's NDA row): "[DIFFERENT DD INFO FOR DIFFERENT BIDDERS, S VS F + DEGREE OF INTEREST] Party B and Party C, in light of the fact that they were financial bidders, were given broad access to an electronic data site, and Party A and CSC/Pamplona … somewhat limited access …".
- HC 6939 (Mac-Gray, on the "Final Round Inf" marker): "the Special Committee concluded that it would be advisable to stage the disclosure of such information to each of the bidders to the extent that a bidder's indication of interest … demonstrated its seriousness".
- HC 6031 (P&W, on the two-party `DropTarget` row): the passage about seven buyers getting in-person management presentations and the data site.
Every one is about **differentiation** — who got more than whom, and why. Against that, VN Providence 6 (black = important and easy): "once those agreements have been signed, it can be assumed that the parties will talk to each other regularly … there is simply no need to record all of them, because that's gonna blow up the database." The 18 Sep audit (`pro_review_2026-09-18/audit_notes_2026-09-18.md`, row table near line 1028) already classed "r30 Party C data-site access + management presentation 07/14" and "r43 On-site diligence 07/27–08/11" as VN I.6 violations — yet §4 now names "a late entrant's catch-up access" as a kept row. Austin's decision (rows kept) stands; the point is that Alex's tolerance here is thin, so the definition must be tight.

**(c) What the four models produced under the old instruction (label `Material process update`, plus a few `Target decision` rows), counted from the dumps.**

| Deal | Opus | GLM | DS | Sol |
|---|---|---|---|---|
| Mac-Gray | 3 (r29 presentations 08/06–08/14; r30 broad vs limited data site; r54 CSC full access 09/25–10/07) | 2 (r30 presentations + differentiated access in one row; r52) | 2 (r27 one combined row; r47) | 1 (r24 broad vs limited access; presentations folded into the round-2 `Round opened` row) |
| P&W | 5 (r17 memorandum to all signers; r25 draft documents posted to data site; r26 "differentiated diligence stage"; r30 Party C catch-up; r47 on-site diligence for B and G&W) | 3 (r16, r24, r28) | 3 (r15, r23, r27) | 2 (r15, r27) |
| PetSmart | 3 (r22 October diligence by all 15; r37 November diligence; r39 projection update) | 2 (r34, r36) | 1 (r31, everything in one row) | 1 (r27, everything in one row) |

So the old catch-all already yielded 1–5 such rows per deal, and the spread between models (1 versus 3 on Mac-Gray, 2 versus 5 on P&W) is the problem a definition has to solve. About half of these rows are uniform access (the memorandum to all 25 signers; October diligence by all 15 signers; presentations to all four Mac-Gray bidders) or not information about the target at all (draft merger agreement posted to the data site — three of four models made that a row).

**Applying the current wording by hand.** Mac-Gray: the §4 parenthetical "one row for a series of management presentations, naming the bidders and dates" is a near-description of 08/06 (B), 08/08 (C), 08/12 (CSC/Pamplona), 08/14 (A) — every live bidder got one, so there is no differentiation, yet the example orders a row. Add broad-versus-limited data-site access (the row Alex cares about), CSC/Pamplona's "full access" during exclusivity, and possibly the 07/25 staging decision: 3–4 rows. P&W: memorandum to all signers, data-site access for the seven advancing bidders on 06/01 (already the `Round opened` / `Dropped by target` story), Party C catch-up on 07/14, on-site diligence for the two finalists from 07/27 (already the 07/27 selection): 4 rows, one of which Alex would want. PetSmart: October access for all 15, November access for finalists, the projection update; and because §11.3 says "given, **or denied**", the August decision not to invite Industry Participant over "competitively advantageous information" is a candidate too, although §10.1 makes it a `Target decision`. 3–4 rows, one wanted.

**Does "one row per distinct change in access" conflict with "no rows for meetings … with bidders already under NDA"?** Yes, directly, through the parenthetical example. §4's own bullet is careful — "management presentations given to some bidders and not others" — but the example that follows it, and the §11.3 definition ("management presentations", unqualified), drop the qualifier. A model resolves a rule-versus-example conflict in favour of the example. "Distinct change in access" is also undefined (see B3): distinct by bidder, by date, by type of information?

**Is a dedicated label worth having?** Yes. The rows will exist either way (fixed decision). With a label they are one filter click for Alex to hide and one `drop if` at export — the fully reversible design. Left in `Material process update` they are inseparable from rollover threads and business updates, which is what happened in the 12 workbooks (4–17 `Material process update` rows each, counted from the xlsx files). The alternative in `QUESTIONS_evaluation.md` A12 (an `Information access:` text prefix on MPU rows; it never entered the instruction) is a weaker version of the same thing. The cost of a label is that a named label attracts rows; that is a reason to tighten the definition, not to drop the label.

**(d) Downstream risk.** If loose: 3–5 extra rows per deal × 400 deals that Alex hides by filter — an irritation, not a data error, because these rows carry no Count, price or outcome. If a model duplicates a selection decision as an access row, nothing double-counts. Reversible at any time. The real cost is reviewer goodwill (VN I.6).

**(e) Verdict: KEEP THE LABEL; REPLACE THE TWO DEFINITIONS.**

§4, replace the whole paragraph beginning "**Keep information-access events as rows:**" with:

> **Keep differences and changes in information access as rows.** Use **Information access changed** (section 11.3) only when (a) bidders live at the same time are given different access — staged or tiered data-room access, management presentations or site visits given to some and not others, information withheld from a bidder or a bidder type, a late entrant's catch-up access — or (b) the target issues, revises or withholds projections or comparable business information after bidding has begun. Access given alike to everyone admitted to a stage (the memorandum sent to all NDA signers, the data room opened to all advancing bidders, presentations held with every finalist) is not a separate row: state it on the NDA, Round opened or selection row that admits them. Write one row per access decision, naming who received what, who did not, the stated reason and the dates; never one row per meeting, and none for transaction documents posted to a data room. Refusing to admit a party that never entered is a Target decision (section 10.1).

§11.3, replace the label's Use cell with:

> Differentiated, staged, withheld or catch-up access among live bidders, and projections or comparable information issued, revised or withheld once bidding has begun (section 4). Not uniform stage access; not individual meetings. Count blank.

By hand this gives Mac-Gray 2 rows (broad versus limited data site with the four presentation dates inside it; full access for CSC/Pamplona in exclusivity), P&W 1 (Party C's catch-up, by telephone rather than in person), PetSmart 1 (the post-Q3 projection update). That is the set Alex annotated plus the one class §4 already promised (projections).

One related ambiguity to settle at the same time: these rows are usually periods ("Between August 6, 2013 and August 27, 2013"), and §8.1 rule 4 sends a period to its midpoint. For a spanning event the natural sort key is its start. Add to rule 4: "An event that itself spans a reported period (a diligence period, a series of presentations) takes its first day (Assigned: bound)."

Not checked: Alex has never been asked whether he wants these as rows at all; his three instances are comments on other rows.

---

# PART B — Whole-document review

Read as the extracting model would: top to bottom, taking every sentence literally, resolving a rule-versus-example conflict in favour of the example and a general-versus-specific conflict in favour of whichever comes later.

## B1. Contradictions and tensions introduced by the edits

Ordered by how much damage a literal reading does. S = serious (changes rows or counts), M = moderate, L = low.

**B1.1 (S) "Entered the process" is wider than the fixed decision and than Alex's practice.**
§10.1: "Outcome labels apply only to a participant that had entered the process — responsive to contact, under NDA or bidding." §10.2: "**Every participant that entered a stage is closed out in the ledger.**" §2 bullet: "Close out every participant that entered a stage." Together these require a closing row for every party that answered an enquiry positively, NDA or not. The fixed decision is narrower ("Every NDA signer who did not win gets an exit row"), and so is Alex: Mac-Gray contacted "50 parties" and "a total of 20 potential bidders" signed NDAs; his sheet has one residual `Drop`, for the "16 financial bidders" under NDA (HC 6942), and nothing for the thirty contacted parties that never signed. VN line 70 (black): "I think we should record the contact, and that's that." A model that reads "responsive to contact" broadly will close the contacted-but-unsigned parties with a residual row (Mac-Gray: 50 − 20 = 30) and start the §13.3 stock from 50, not 20; one that reads it narrowly will not, so the four models will differ on the first-order count.
Fix, §10.1: replace "responsive to contact, under NDA or bidding" with "under NDA, bidding, or otherwise actually participating (in diligence or negotiation); a positive reply to an enquiry is not yet entry". §10.2 and §2: replace "entered a stage" with "entered the process" (see B3 on "stage").

**B1.2 (S) The close-out sweep catches late submitters.**
§10.2: "at each transition — a submission due date, an advancement decision, executed exclusivity, signing — close any participant or residual cohort that has no evidenced outcome with **one inferred row**, at the earliest transition that reveals its absence". On a due date a bidder that submits the next day "has no evidenced outcome". This is not hypothetical. P&W: due 07/20, G&W submitted 07/21. Mac-Gray round 1: indications were "to submit by July 23, 2013"; "July 24, 2013, Party B submitted a preliminary indication of interest" and Party C "presented an oral preliminary indication" the same day (HC 6940–6941). Mac-Gray round 2: due 09/09; "On September 10, 2013, Party A submitted a revised indication of interest" and Party C telephoned its bid the same day. A literal sweep writes `Did not submit` for each of the five and then, under §10.1 ("**Re-entered** … is required whenever a participant bids … after a recorded outcome"), a `Re-entered` row the next day: ten junk rows across two of the three pilot deals.
Fix, §10.2: after "at the earliest transition that reveals its absence" add the sentence "A bid that the target considered after the due date (Treatment: Late bids accepted) is a submission to that solicitation, not an absence." (A wider exemption such as "does not appear again in that process" would be wrong: it would also spare a bidder that skips a round and returns two rounds later, leaving it in the live stock of the round it skipped.)

**B1.3 (S) Three instructions for one bidder-returned draft; and rule versus example C.**
§4: "**Do not create rows for:** … successive agreement drafts". §9.1: "A further draft is not automatically a bid or reduced conditionality. Use Offer update for material documentation/status evidence". §9.1, new paragraph: "a bidder returns revised agreement drafts on its standing offer or confirms its price, record **Bid reaffirmed**". For Party B's 08/04 draft all four old models chose `Offer update`; the new paragraph wants `Bid reaffirmed`; §4 wants no row. The model has no tie-break. Separately, §9.1 says "One such row per bidder per stage is enough unless the terms change", while §12.C ends "Party B's refusal to raise, when asked on August 12 … is a second reaffirmation" — same bidder, same stage, same $24. And §9.1 says "Formality = Formal (signal 3 in section 9.2)", but signal 3 is "An actual price confirmation"; a returned draft is signal 1 ("Bidder-returned acquisition agreement markups").
Fix (leaving the item-1 decision itself to its reviewer): in the Late reconfirmation paragraph replace "Formality = Formal (signal 3 in section 9.2)" with "Formality = Formal (signal 1 or 3 in section 9.2)"; replace "One such row per bidder per stage is enough unless the terms change; do not add a row for every draft." with "The first returned draft in the stage is that row; later drafts get no row (section 4), and Offer update is kept for a change of status that is not a returned draft or a price confirmation (financing papers delivered, diligence declared complete, a proposal withdrawn)." That leaves the rule-versus-§12.C conflict over the 08/12 row, which must be settled with item 1 and not by me: either delete the last sentence of §12.C, or add to §9.1 "A bidder's answer to a target request to improve or confirm is its own Bid reaffirmed row." Note that Alex's sheet points to deletion: HC 6056 records Party B on 08/12/2016 as "Drop", comment "Refused to increase offer" — the refusal is the exit (§10.3 `Would not improve earlier offer`), not another bid row; his only late Party B bid row is HC 6054 (08/04, "Confirm 7/20/2016 bid after DD").

**B1.4 (S) Count: three older sentences forbid what §10.2 now requires, and two leave holes in the stage balance.**
§7.3: "Use numeric Count only for an established exact additive contribution." §7.2: "Leave an uncertain additive contribution blank rather than entering a convenient zero." §5.2: "Where overlap is unresolved, leave the additive Count empty". Against: §10.2 "Where the base population is uncertain … still write the row … Count = stated base − evidenced exits" and "Where the base is a lower bound, Count is the lower-bound residual". Batch 2 rewrote §10.2 but not the three older sentences. Also §5.2: "Count 0 means known inclusion or repetition, not uncertain overlap" versus the §10.2 identity row, which is Count 0 precisely because inclusion is *not* known. Also §7.2: "On participation outcomes or group changes, Count **may** record the exact number of affected units" and "Leave Count blank on adviser, process-wide decision … rows", while §13.2's balance needs a number on every exit row and §10.2 makes the process-wide `Process terminated` row close "the remaining participants; state how many where known" — with nowhere numeric to state it. (Old runs did fill Count on every outcome row, 3–9 per workbook, so the "may" is a wording risk rather than an observed failure.)
Fix: §7.3, append to the quoted sentence "The inferred closing rows of section 10.2 are the one exception: their Count follows the rule there and the qualification sits in Terms or outcome." §7.2, replace "Count may record the exact number of affected units in that event" with "Count records the number of affected units (1 for an individual; 0 on an Inferred: identity row, whose exit is already inside a cohort row)". §10.2, replace "state how many where known" with "put the number in Count where known".

**B1.5 (M) §8.3 "a final due date" versus §6.3 "first request for final … offers".**
§6.3: "The target's **first** request for final, binding or best-and-final offers also opens a new round, even when the invited bidders are unchanged." §8.3: "A target request, made after a final due date has arrived, that the same bidders submit improved bids by a new date is a **Deadline revised** … not a new round". "A final due date" can be read as "the last due date so far". Mac-Gray tests it: the 09/09 due date (round 2, not final) arrives; on 09/11 the committee instructs the banker "to request final" proposals from the same four bidders. §6.3 says new round (Alex agrees: HC 6951 "Final Round Ann 09/11/2013"); the loose reading of §8.3 says `Deadline revised`, no round.
Fix, §8.3: replace "made after a final due date has arrived" with "made after the due date of a round already opened as final has arrived".

**B1.6 (M) Finality: two vocabularies in consecutive sentences.**
§6.3: "Distinguish **announced as final**, **inferred final negotiation**, and merely **last observed**. State the same finality at the start of Terms or outcome on the round's Round opened row — `Announced as final`, `Inferred final` or `Not final`". "Last observed" and "Not final" are not the same thing (an intermediate round is Not final but not last observed), and §11.4(3) has a third wording, "announced or inferred finality".
Fix: replace the first sentence with "Distinguish `Announced as final`, `Inferred final` and `Not final`; where a Not final round is the last one observed, say so in Summary."

**B1.7 (M) The four transitions and the three table rows.**
§10.2 lists four transitions ("a submission due date, an advancement decision, executed exclusivity, signing") but its table has rows for three. A bidder that bid, is absent from the advancing set, and is not reported as told has no row; the model must choose between stretching `Did not submit` and waiting for `Inferred: silent` at signing, which keeps a dead bidder in the live count of every intermediate stage — the first-order variable. Related: §6.3 "Exclusions carry the round being left" does not say which Round an inferred row carries when the participant was last seen two rounds earlier.
Fix (needs Austin's call on agency; minimal version): add a table row "Bid or was live in a stage; the filing names or counts the advancing set without it and reports no notice | Dropped by target | Inferred: residual | Unknown; Not stated | Day of the advancement decision", and add under the table "An inferred row carries the Round in which its transition falls."

**B1.8 (M) §3.1 demands a quotation that an inferred-silent row cannot have.**
§3.1: "Every substantive row needs **Why and evidence** and **Source**: a concise reason, a short exact quotation and printed page." A `Not selected at signing — Inferred: silent` row rests on absence. Models will either quote something irrelevant (failing §13.7, "the passage actually supports the associated claim") or leave Source and Page blank.
Fix, §10.2, add: "An inferred row quotes the passages that give the base and the continuing set, or the participant's last appearance, and takes that page."

**B1.9 (M) §10.1 `Did not submit` "is not necessarily permanent withdrawal" versus §10.2, which uses it as a closing row; §13.3 "exits" undefined.**
§10.2 settles it implicitly ("A participant closed at one transition is not closed again unless it has Re-entered"; a pause "does not close a participant"), but §13.3's "Participant stock per stage = entrants − exits + re-entries" never says which labels are exits.
Fix, §13.3, after "re-entries" add: "(exits are Dropped by target, Withdrew, Did not submit, Not selected at signing and Joined group rows, and participants closed by a Process terminated row or at go-shop expiry; Participation paused is not an exit)".

**B1.10 (M) §9.3: the fixed `Fin:` vocabulary cannot express a fact in one of the three pilot filings; "Heavy by context" has no stated precedence.**
§9.3 None test: "financing committed or not needed"; same section: "A commitment and absence of a financing contingency differ." But the format offers only "`Fin: committed | represented | not committed | not stated`". Mac-Gray's winning proposal is described by "the fact that there would be no financing contingency". None of the four values fits; four models will invent four strings. Separately, "A preliminary non-binding indication made before the bidder has had substantive diligence access is Heavy by context" and the Light test ("subject only to confirmatory, expedited or limited diligence") both apply to a first-round IOI that says "subject to confirmatory due diligence"; nothing says which wins.
Fix: make the format "`Fin: committed | no contingency | not needed | represented | not committed | not stated`"; and after "Heavy by context: it is inherently subject to that diligence" add ", whatever diligence wording the indication itself uses".

**B1.11 (L) §13.3 versus the identity row.** §13.3: "Do not require a named exit for an anonymous outcome" reads as excusing the §10.2 Count-0 row. Add "(the Count-0 identity row of section 10.2 excepted)".

**B1.12 (L) §11.5 "all conditionality assessments during the pilot".** "The pilot" is defined nowhere, and the header says "Not yet run". With `Conditions detail` now on every bid row this bullet is also the largest single driver of Questions length. Replace with "every Conditions level that turns on a stated diligence period, and every None".

**Checked and found consistent:** §3.3 versus the always-filled Working date and inferred rows (the two exception sentences do the job); §5.2 "Do not invent individual identities" versus the Count-0 row (the last sentence of the §5.2 paragraph covers it); §9.2 formality carry-forward versus the reaffirmation row; §9.3 versus §12.D; §12.B versus §8.1 rule 2 and "A deadline does not prove arrival by that date"; §8.3 "Create a Deadline row for a due date reached while still operative" versus the extension rule (the old due date gets a `Deadline` row with `Treatment: Extended`, the new one its own row); §10.1 table versus §10.2 table on exclusivity; §8.2 monotonicity versus §13.4. No surviving sentence says a Working date may be blank or that a silent participant needs no row; the nearest is §10.3 "Do not append an exit just because a valuation sounds uncompetitive", which now means only "not on the valuation date".

## B2. Competing "begin Terms or outcome with …" demands

Every mandated phrase, in document order:

| # | Where | Row type | Exact demand | Position demanded | Structured twin? |
|---|---|---|---|---|---|
| 1 | §5.3 | Bid / Bid reaffirmed by a supported bidder | "`Support: [party] (financing)` in Terms or outcome" | anywhere | none |
| 2 | §5.3 | Bidding group changed (anonymous members) | "states the effect on the number of bidding units (“… units −1”)" | anywhere | none (not in Count) |
| 3 | §6.3 | Round opened, round 1 | "state `R1 anchor:` with the event used and list the Row ids of the other candidate anchors" | cell not named | Related rows, partly |
| 4 | §6.3 | every Round opened | "State the same finality at the start of Terms or outcome … `Announced as final`, `Inferred final` or `Not final`" | start | Summary map only |
| 5 | §8.3 | Deadline | "Begin Terms or outcome on each Deadline row with the same value (`Treatment: Extended`, and so on)"; "Values can combine" | start | Summary map only |
| 6 | §9.1 | alternative structures | "marked **one communication, one bidder**" | anywhere | none |
| 7 | §9.4 | Bound-only price | "begin the constraint in Terms or outcome with `Bound: ≥ X`" | start of the constraint | Price kind, Price low |
| 8 | §9.4 | carried price | "Mark it visibly as carried, not restated." | anywhere | Price origin |
| 9 | §10.2 | inferred exits | "Begin Terms or outcome with the same words as Outcome basis and show the arithmetic" | start | Outcome basis |
| 10 | §10.2 | uncertain base | "beginning “Inferred: residual (base assumes …)”" | start | Outcome basis (bare) |
| 11 | §11.3 | Material process update | "Begin Terms or outcome with the precise action" | start (free text) | none |
| 12 | §11.3 | Exclusivity changed | "explicitly state which" (requested, authorized, granted, extended, ended) | anywhere | none |

Rows where two or more apply at once:
- **The round-1 `Round opened` row: #3 and #4 always**, and usually the deadline set in the same instruction (§8.3 lets a Round opened row carry it). In a one-round bilateral deal the same row is also `Inferred final`. This is the only hard collision: one phrase "at the start", another with no cell named.
- A `Bid` that is bound-only, from a supported bidder, as one of two alternatives: #1, #6, #7. None claims the first position, but the order is undefined. P&W Party E's 08/01 LOI ("along with financing support, from Party F") is a live #1 case.
- A `Bid reaffirmed` with a carried price from a supported bidder: #1 and #8.
- No collision between #5 and #9: they sit on different rows (the `Deadline` row and the `Did not submit` row of the same date).

Other weaknesses: "Values can combine" (#5) gives no combined spelling, so `Treatment: Extended; Late bids accepted`, `Extended + late` and `Extended and Late bids accepted` will all occur; `No deadline stated` can never begin a Deadline row because there is none; `Inferred final` (#4) and `Inferred: residual` (#9) share a first word, harmless only because the labels differ.

**Proposed single convention** — add once, in §11.2 directly under the field table, and leave the individual rules as they are apart from pointing #3 at Terms or outcome:

> **Tags.** Where this instruction prescribes a fixed phrase for Terms or outcome, write it exactly as spelled, before the prose; separate tags with a semicolon and the last tag from the prose with a dash, as in “Inferred: residual — 15 NDA signers − 6 submitters = 9 non-submitters.” When several apply use this order: finality (`Announced as final` / `Inferred final` / `Not final`); `R1 anchor: …`; `Treatment: …` (combined values joined by ` + `, in the order listed in section 8.3); `Inferred: …`; `Bound: ≥ X`; `Support: …`. A tag repeats a structured field or a Summary entry and must agree with it; filters should test "contains", not "begins with".

and in §6.3 replace "state `R1 anchor:` with the event used" with "state `R1 anchor:` in Terms or outcome, after the finality tag, with the event used". Forty-odd words buy a convention that is checkable by regex (see B5).

## B3. Ambiguous or undefined terms

| Term | Where | Why a model stumbles | Minimal fix |
|---|---|---|---|
| "stage" | §10.1 "still live in that stage"; §10.2 "entered a stage"; §9.1 "per bidder per stage"; §13.2–13.3 "per stage" | §6.3 defines a round as a "stage", but the NDA/pre-bid phase, exclusivity and a go-shop are also called stages. "Entered a stage … is closed out" can be read as one exit row per stage. | §10.2, first sentence: "**Every participant that entered the process is closed out once in the ledger.** A stage is a round of section 6.3, round 0 included." |
| "transition" | §10.2 | The list is given by example and omits process termination and go-shop expiry, which the same section later uses as closing points. | "at each transition — a submission due date, an advancement decision, executed exclusivity, signing, process termination, go-shop expiry —" |
| "live" | §10.1, §5.3 "still a live independent bidder" | Never defined. Is a paused bidder live? One silent for two rounds? | §10.1, after the bolded exclusivity sentence: "Live means entered and not yet closed by a recorded outcome; a paused bidder is live." |
| "entered the process" | §10.1 | See B1.1. | as B1.1 |
| "at once" | §6.3 "the launch decision when outreach follows at once" | Days? Weeks? PetSmart's 08/19 announcement and its early-October outreach are about six weeks apart; Mac-Gray's committee decided on 06/24 and the banker made contact "During the next several weeks" — is that "at once"? (Alex anchors on 06/24, HC 6933.) | "when outreach follows without a stated deferral, normally within about two weeks" (item 3's reviewer should confirm the number) |
| "substantive diligence access" | §9.3 "before the bidder has had substantive diligence access" | Is a confidential memorandum substantive? It decides Heavy-by-context for every first-round IOI. | add "(data-room or management access; a teaser or information memorandum alone is not)" |
| "substantive" diligence period | §9.3 Heavy test | Partly defined ("a stated multi-week or exclusive diligence period counts"). P&W Party B's "expedited" is Light by example C; an undated "further due diligence" is not covered. | add to the Heavy cell: "an unquantified “further due diligence” is Light unless the filing describes it as extensive" — or leave it and accept Questions traffic |
| "distinct change in access" | §4, §11.3 | Distinct by bidder, by date or by kind of information? | replaced by "one row per access decision" in A3 |
| "earliest transition that reveals its absence" | §10.2 | Absence from what? A named list, a count, the narrative? | "the first transition at which the filing names or counts the continuing participants without it" (the same test the identity-row sentence already uses) |
| "a stage the target intends to conclude with a definitive agreement" | §9.1 | Every sale process fits. | "a stage in which the target is negotiating the definitive agreement with that bidder" |
| "largely new set of participants", "substantial dormancy" | §6.2 | Judgement terms; acceptable because §6.2 orders a Questions entry for every multi-process call. | none |
| "row it follows in the sequence" | §8.1 rule 6 | Narrative sequence or # sequence? They differ where §8.2 says "Paragraph order is not necessarily event order." | "the row it follows in #" |

## B4. Trims that do not change meaning

The growth is mostly new rules, not repetition. I found about 230 words (2%) of pure restatement, nearly all of it a batch-2 sentence repeating a batch-1 sentence. The five best, with counted savings:

**T1 — §8.1 timing table: three cells restate rules 5 and 6 that follow immediately (−55 words).**
- "By [day]" cell. Before: "Upper bound in Date to unless an earlier bound is independently supported. The report date is not the event date; it may serve as the assigned Working date under the rules below." After: "Upper bound in Date to unless an earlier bound is independently supported. The report date is not the event date."
- "After / before / subsequently" cell. Before: "… Do not invent the missing endpoint. The predecessor's day may serve as the assigned Working date under the rules below; that is a sort position, not a finding that both happened on the same day." After: "… Do not invent the missing endpoint." (The sort-position point is made two paragraphs later: "It is an assigned sort key, never a claim about when the event happened".)
- "No supportable date" cell. Before: "Leave Date from and Date to empty. Assign the Working date from the supported position in the sequence (rule 6 below)." After: "Leave Date from and Date to empty."

**T2 — §12.A and §12.E: sentences that recite §10.2 rather than calibrate it (−73 words).**
- §12.A. Before: "… arithmetic shown — never with individual dates, motives or identities. If the base population is uncertain, still write the row from the filing's stated base, say what the base assumes, and flag it." After: "… arithmetic shown."
- §12.E. Delete the last two sentences ("A rival displaced when another bidder obtains executed exclusivity is Dropped by target (Inferred: exclusivity) and gets Re-entered if it returns. A party last seen in the process and never mentioned again is closed at signing: Not selected at signing, Inferred: silent."). Both are rows of the §10.2 table with no added case detail.

**T3 — §9.3: financing silence is stated three times in one section (−24 words).**
- Before: "Silence about financing neither raises nor lowers the level: record the **reported absence** of a commitment, which is what supports Heavy, and never treat silence as a commitment or as a failure to provide one. None requires affirmative support, not silence or the mere passage of time." After: "Silence about financing neither raises nor lowers the level: only a **reported absence** of a commitment supports Heavy, and None requires affirmative support, not silence or the passage of time."
- Before: "Never write that financing or a document was “not provided” merely because the filing does not mention it." After: "Write `not stated`, never “not provided”, when the filing is silent."

**T4 — §9.1: signing is said not to be a bid three times (here twice, and in §11.3) (−17 words).**
Before: "Signing records agreed consideration, not a separately submitted final bid on an invented earlier date. Do not invent a new price or an undated submission to supply a “missing formal offer”; a supported late reconfirmation is recorded as Bid reaffirmed (above)." After: "Signing records agreed consideration, not another bid (section 11.3). Do not invent a price or an undated submission to supply a “missing formal offer”."

**T5 — cross-section restatements (−42 words).**
- §6.3. Before: "For each round, Summary records the opening, objective, relevant participants, deadline history, contemporaneous finality, observed ending and submitting-bidder tally." After: "Summary's round map is specified in section 11.4(3)." (−13; the list is repeated there almost word for word.)
- §2, fourth bullet. Before: "… and give every row an assigned Working date that respects the known order (section 8.1). A Working date is a sort key with a stated method, not an observed date." After: "… and give every row an assigned Working date — a sort key with a stated method, not an observed date (section 8.1)." (−8)
- §3.3. Before: "Working date is the exception: it is an assigned sort key, always filled under section 8.1." After (joined to the previous sentence): "; Working date alone is always filled (section 8.1)." (−8)
- §5.3, fifth paragraph: delete its first sentence "A party that finances or supports another bidder's offer does not thereby bid." — the third and fourth paragraphs have just said so twice. (−13)

Total about −210 words. Against that, every replacement proposed in this report, if all were adopted, adds roughly 800 words (Part A about 300, B1 about 250, the tag convention, definitions and plumbing sentences about 250), so the net would be about +600 (+5%). The minimum set listed at the end of this report is about +450. Length itself is not the main first-run risk; the stacked exceptions in §7 and §10 are (B1.4), and a model follows one explicit sentence better than it reconciles two conflicting ones.

## B5. Schema plumbing

**New columns and values — where each appears.**

| Item | §11.2 | Defining § | §11.4 Summary | §11.5 Questions | §13 check |
|---|---|---|---|---|---|
| `Date method` | yes | §8.1 (values listed in prose) | not needed | yes, last bullet ("rows whose assigned Working date decides their order") | §13.4: filled, never Reported when assigned. **Missing:** agreement with Date basis (A1) |
| `Outcome basis` | yes | §10.2 table, §10.3 | yes, items 4 and 5 | yes ("every inferred closing row") | §13.2–13.3 by implication. **Missing:** filled on the five labels; opener agrees (A2) |
| `Conditions detail` | yes | §9.3 | no (fine) | only through the "pilot" bullet | §13.5: present "in the fixed format". **Gap:** the format has placeholders and a missing value (B1.10), and no complete worked string anywhere — §12.C shows only "`DD open: yes`" |
| `Page` | yes | §11.2 only | no | no | **none** |
| `Information access changed` | — | §4, §11.3 | no | no | §13.1 "material information/selection changes" only |
| finality tag | — | §6.3 | item 3 | first bullet | **none** |
| `Treatment:` tag | — | §8.3 | item 3 | second bullet | **none** |
| `R1 anchor:` | — | §6.3 | no | first bullet ("inferred starts") | **none** |

One sentence closes every "none" and "missing" cell. Add to §13.6: "Tags and structured fields agree: every Round opened row carries a finality tag and the round-1 row an `R1 anchor:`; every Deadline row a `Treatment:` tag matching the Summary map; every inferred outcome row an opener equal to its Outcome basis; Date basis and Date method are a permitted pair; Page is filled wherever Source is."

**Exact strings.** §11.1 says "Controlled categories use Lists drop-downs" but no section lists which columns are controlled. In the old workbooks the four models agreed on eleven lists and then diverged (DS added Currency, Process and Round lists; GLM added Process and Round; Opus and Sol neither). For stacking, header names and values must be identical across deals. Add to §11.1: "Controlled columns are What happened, Type, Formality, Conditions level, Include, Date basis, Date method, Price kind, Price origin, All cash, Decided by, Exit reason and Outcome basis. Use the exact strings given in this instruction, including capitals, colons and spacing; Lists holds exactly these." Strings most likely to drift: `Inferred (cross-paragraph)` (rename, A1), `Assigned: decision day` (three words, a colon), `Inferred: residual` versus the Terms variant "Inferred: residual (base assumes …)" (A2), and `Information access changed` (long; models shorten labels).

**Column order.** §11.2 presents the expandable fields as a table of groups ("Row id; Include | …") and never says the order is binding. All four old models happened to follow table order (Row id = column O, Include = P, Count = Q … Deal = AG), and their Summary SUMIFS and the AI-original conditional format are hard-wired to those letters (`'Deal ledger'!$Q:$Q`, `$P:$P`, `MATCH($O2,'AI original'!$O:$O,0)`). The three new columns are inserted mid-table (`Date method` after Date basis, `Conditions detail` after Cash at closing, `Outcome basis` after Exit reason, `Page` before Related rows), so every letter from V onward shifts and the sheet becomes 37 columns, A–AK. Within one workbook nothing breaks as long as the model computes its letters afresh and gives AI original the same layout. Across workbooks it breaks stacking if any model appends the new columns at the end instead. Add to §11.2, in the sentence introducing the second table: "in this order, left to right".

**Summary SUMIFS and the per-stage balance.** The balance in §11.4(5) and §13.2 can be formula-driven only if every exit has a numeric Count and a Round. Holes: (i) §7.2 "may record" (B1.4); (ii) `Process terminated` has Count blank by §7.2 yet closes participants by §10.2; (iii) "units −1" (§5.3) lives only in Terms, so a combination of anonymous signers lowers the stock without any numeric cell — put 1 in Count on that Bidding group changed row and say in Terms that it is a reduction in units; (iv) lower-bound residuals are numeric in Count with "≥" only in Terms, so a SUMIFS total silently treats them as exact — §11.4's "Show bounds or incomplete coverage explicitly" covers it if the model remembers; (v) the Round on an inferred row is unspecified (B1.7). Round holds numbers and the text "post"; SUMIFS criteria coerce, so that is safe.

**AI original.** §11.7 "including all expandable fields and Row ids" already covers the new columns. The comparison formulas match on Row id plus column position, so they survive the wider sheet. One old weakness is unchanged by the edits and worth knowing before the run: GLM's Mac-Gray and PetSmart workbooks contain no conditional-format rule at all (its P&W workbook has one), so correction highlighting cannot be assumed; Opus, DS and Sol each built a Row-id-matched rule.

## B6. What is most likely to go wrong in the first real run, and how to see it in the workbook

1. **Working dates: monotonic on paper, false in substance.** Models satisfy "sorting by Working date … reproduces #" by labelling assigned dates `Reported`, by copying the assigned day into Date from and Date to, or by reshuffling # away from the narrative. *Look for:* rows where Date method starts "Assigned" but Date from = Date to = Working date; Date basis/Date method pairs outside the A1 table; a sort by Working date then # that does not reproduce #; on P&W, whether the five undated LOIs sit at 07/20 ahead of G&W's 07/21 with Date to 07/22 and When still "late July 2016"; every inferred exit row for Date method = Reported.
2. **Close-out over-generation.** Late submitters closed and re-entered (B1.2); contacted-but-never-signed parties closed (B1.1); a bidder closed twice. *Look for:* any `Re-entered` within two days of a `Did not submit` for the same party (G&W 07/20–21; Mac-Gray Party B and C 07/23–24, Party A and C 09/09–10); an inferred residual whose base is a contact count (Mac-Gray "50"); more than one exit row per named bidder without a `Re-entered` between them; row count against the old run (old ledgers 51–70 rows; more than about +10 needs a reason).
3. **The stage balance does not close, or closes by a fudge.** Count-0 identity rows entered as Count 1 (double-counting P&W's Party A, who is already inside one of the cohort exits), lower-bound Counts summed as exact, no Count on individual exits, inferred rows all parked at signing. *Look for:* rebuild the balance yourself with a pivot of Count by Round × What happened × Outcome basis and compare with Summary block 5 — P&W should run 25 signers → 9 IOIs (16 inferred residual) → 7 advance (2 dropped, stated) + Party C → 6 LOIs (2 stated non-submitters) → 2 selected (4 told, stated) → D and E re-enter → signing; any stage where the stock is negative or where `Inferred: silent` exceeds one or two units.
4. **`Bid reaffirmed` inflation and price contamination.** Every returned draft becomes a Formal row with a carried price; stacked, these look like bids. *Look for:* filter Price origin = Carried forward — expect at most one or two per bidder per round (P&W: Party B 08/04 and 08/12; Mac-Gray: Party A 09/18 "best and final"); any such row with Count 1 in a round where the bidder already has a Bid; any with Price origin = Stated; an `Offer update` and a `Bid reaffirmed` for the same draft.
5. **Tag and fixed-format drift.** `Treatment:`, finality, `Inferred:` and the Conditions detail string are free text that must behave like codes. *Look for:* a regex pass — every Deadline row `^Treatment: (Enforced|Extended|Late bids accepted|Passed without action|Unclear)`, every Round opened row one of the three finality strings, every inferred row's first words equal to its Outcome basis, every Bid and Bid reaffirmed row matching `^Fin: .*; DD required: .*; DD open: .*; Excl: .*$` with values inside the vocabulary (expect "no contingency" on Mac-Gray CSC/Pamplona, and "expedited" written where "confirmatory" is the listed value); then cross-tabulate Conditions level against the string — Heavy with `Fin: not stated` and `DD required: confirmatory` is a contradiction.
6. **`Information access changed` as the new catch-all.** *Look for:* more than two such rows in a deal; any whose Who is every live bidder (uniform access); any dated to a single meeting; the P&W draft-documents-posted row; PetSmart's Industry Participant decision under this label instead of `Target decision`.
7. **Layout divergence between models.** New columns appended at the end, missing from AI original or Lists, or no drop-down on Date method / Outcome basis. *Look for:* compare row 1 of `Deal ledger` and `AI original` across all workbooks as strings; confirm 37 headers in the §11.2 order; confirm data validation exists on the two new controlled columns; open one Summary SUMIFS and check that its ranges land on the Count and Include headers.
8. **Round map shifts caused by the new round rules, propagating into Count.** The "first final request opens a round" rule together with the ambiguous §8.3 sentence (B1.5) can split or merge Mac-Gray's 09/09–09/18 sequence differently across models, and each bidder's Count 1/0 pattern follows the round. *Look for:* Mac-Gray should show round 2 due 09/09 (treatment: late bids accepted, A and C on 09/10) and a new round opened 09/11 with due date 09/18, `Announced as final`; the round-1 row carries `R1 anchor:` with alternatives listed (PetSmart: 10/03 anchor, 08/19 press release among the candidates).


## Minimum edit set before the first run

If only a few edits are made, these remove the behaviours most likely to corrupt first-order variables (live-bidder counts, order, bid list), in this order:

1. B1.2 — add the late-bid sentence to the §10.2 sweep (five late submitters in the pilot deals).
2. B1.1 — narrow "entered the process" in §10.1; "entered a stage" → "entered the process" in §10.2 and §2.
3. B1.4 — the three Count sentences (§7.3 exception; §7.2 "records … 1 … 0 on an identity row"; Count on `Process terminated`).
4. A1 — Date method for the three inferred closing rows and after an order-constraint move; rename `Inferred (cross-paragraph)` to `Inferred`.
5. B1.3 — the draft / Offer update / Bid reaffirmed tie-break and the signal-number correction; settle the 08/12 second reaffirmation in §12.C together with item 1 (Alex's HC 6056 treats it as the exit, not a bid row).
6. A3 — replace the §4 access paragraph and the §11.3 definition.
7. A2 — opener on inferred rows only; bare value in the column; identity row takes the covering cohort's label.
8. B2 — the Tags paragraph in §11.2, and `R1 anchor:` pointed at Terms or outcome.
9. B5 — "in this order, left to right" in §11.2; the controlled-columns sentence in §11.1; the one-sentence tag/field agreement check in §13.6; `no contingency` and `not needed` added to `Fin:`.
10. B1.5 and B1.6 — the two one-phrase fixes for "a final due date" and the finality vocabulary.

What I could not check: nothing has been run, so every statement about model behaviour is inferred from the 12 old workbooks and the text; Alex has not seen any of the three design choices; font colours in the hand sheet were not re-read, so "his own comment" rests on his bracketed-capitals annotation style and on the H4 helper's note that Excel comments carry no colour code; items 1–10 and 12–15 were read only for consistency, not re-decided.
