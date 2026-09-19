# Batch 3 (19 Sep 2026): edits approved by Austin after the item-by-item review in item_review/.
# Base text: instruction_audit_2026-09-19/instruction_before_batch3.md -> SEC_Deal_Ledger_Extraction_Instruction.md
# Every edit asserts that its anchor occurs exactly once; nothing is written unless all succeed.
BASE='instruction_audit_2026-09-19/instruction_before_batch3.md'
P='SEC_Deal_Ledger_Extraction_Instruction.md'
s=open(BASE,encoding='utf-8').read(); log=[]
def rep(tag,old,new):
    global s
    n=s.count(old); assert n==1, f'{tag}: anchor found {n} times: {old[:80]!r}'
    s=s.replace(old,new); log.append(tag)
def span(tag,start,end,new):
    global s
    assert s.count(start)==1, f'{tag}: start anchor x{s.count(start)}: {start[:60]!r}'
    i=s.index(start); j=s.index(end,i)+len(end); s=s[:i]+new+s[j:]; log.append(tag)

# ---- section 1, 2, 3.3
rep('i9','as needed to resolve buyer type, consideration, dates, counts and conflicts.','as needed to resolve buyer type, consideration, dates and conflicts, and to cross-check counts (section 7.3).')
rep('fix-entered-2','- Close out every participant that entered a stage.','- Close out every participant that entered the process.')
rep('trim-2','and give every row an assigned Working date that respects the known order (section 8.1). A Working date is a sort key with a stated method, not an observed date.',
    'and give every row an assigned Working date — a sort key with a stated method, not an observed date (section 8.1).')
rep('trim-3.3',', never zero. Working date is the exception: it is an assigned sort key, always filled under section 8.1.',', never zero; Working date alone is always filled (section 8.1).')

# ---- section 4: information access narrowed to differences and changes; rollover row allowance
span('i11-access4','**Keep information-access events as rows:**','not one row per meeting.',
"**Keep differences and changes in information access as rows.** Use **Information access changed** (section 11.3) only when (a) bidders live at the same time are given different access — staged or tiered data-room access, management presentations or site visits given to some and not others, information withheld from a bidder or a bidder type, a late entrant's catch-up access — or (b) the target issues, revises or withholds projections or comparable business information after bidding has begun. Access given alike to everyone admitted to a stage (the memorandum sent to all NDA signers, the data room opened to all advancing bidders, presentations held with every finalist) is not a separate row: state it on the NDA, Round opened or selection row that admits them. Write one row per access decision, naming who received what, who did not, the stated reason and the dates; never one row per meeting, and none for transaction documents posted to a data room.")
rep('i6-denied','gets at most one row when it is permitted or formed and one when it is resolved.','gets at most one row when it is permitted, denied or formed and one when it is resolved.')

# ---- section 5.2 / 7.2 / 7.3: Count sentences reconciled with section 10.2
rep('fix-count-5.2','Count 0 means known inclusion or repetition, not uncertain overlap. Where overlap is unresolved, leave the additive Count empty, describe the known population, and qualify the total.',
    'Count 0 means known inclusion or repetition, not uncertain overlap (the Count-0 identity row of section 10.2 is the one exception). Where overlap is unresolved, leave the additive Count empty, describe the known population, and qualify the total; inferred closing rows follow section 10.2 instead.')
rep('fix-count-7.2a','- On participation outcomes or group changes, Count may record the exact number of affected units in that event.',
    '- On participation outcomes, Count records the number of affected units: 1 for an individual, the cohort size for a cohort, 0 on an Inferred: identity row whose exit is already inside a cohort row. On group changes it records the number of members affected.')
rep('fix-count-7.2b','- Leave Count blank on adviser, process-wide decision, scheduled milestone and pure offer-update rows.',
    '- Leave Count blank on adviser, process-wide decision, scheduled milestone and pure offer-update rows; a Process terminated row is the exception (section 10.2).')
rep('fix-count-7.3','Use numeric Count only for an established exact additive contribution.',
    'Use numeric Count only for an established exact additive contribution. The inferred closing rows of section 10.2 are the one exception: their Count follows the rule there and the qualification sits in Terms or outcome.')

# ---- section 5.3: financing supporter; cohort members combining
span('i6-support',"A party that finances or supports another bidder's offer does not thereby bid. The supported bidder keeps",'if it had already exited, it gets no new row.',
"The supported bidder keeps its own name and Type, with `Support: [party] (financing)` in Terms or outcome and Related rows pointing to any earlier independent bid by the supporter. If the supporter was still a live independent bidder when the support began, close its independent participation on the date the support is reported: Joined group where the filing shows it became part of the bidding unit, otherwise Withdrew with `Support: [bidder] (financing)` in Terms or outcome and Decided by = Bidder; say which and why. If it had already exited, it gets no new row and no Re-entered.")
rep('i6-combine','so that stage counts reconcile by number rather than identity. Never backfill an NDA or entry row that the filing does not report.',
    'so that stage counts reconcile by number rather than identity. Where the members are individually recorded, close each with Joined group instead and say in Terms or outcome that the stage count falls by one; the Bidding group changed row then states the composition but carries no unit change of its own. Where it is not established that every member was live in the current stage, state the assumption in the row and in Questions. Never backfill an NDA or entry row that the filing does not report.')

# ---- section 5.4: adviser dates scoped to a mandate
rep('i12-adviser','Use the earliest date the filing shows the adviser selected or acting for that client as the Working date, and list every disclosed date (selected, first advice, engagement letter) in Terms or outcome.',
    'Use the earliest date the filing shows the adviser selected or acting on that mandate as the Working date of its first row for that mandate (Date method Reported when that day is stated, otherwise Assigned: bound); a later engagement, termination or re-engagement keeps its own date. List every disclosed date (selected, first advice, engagement letter) in Terms or outcome. An adviser the filing describes only generically, such as “a financial advisor”, is not evidence that a later-named firm was the one present.')

# ---- section 6.2: new-process test made one-directional; closure is per process
rep('i10-process','A largely new set of participants after the dormancy supports a new process; the same participants resuming supports the same process.',
    'After a dormancy that follows an earlier sale attempt, a largely new set of participants supports a new process. Continuity of participants does not by itself establish one process: a restarted attempt often returns to the same buyers, and a supported abandonment followed by a fresh start is a new process even when the same bidder returns. It supports one process only together with continuing negotiations or an unresolved earlier stage.')
rep('i5-perprocess','Keep stale NDAs in their original process.',
    'Keep stale NDAs in their original process. Closure is per process: Re-entered applies within a process; a participant that reappears in a later process enters that process afresh at its first row there, with Related rows to its earlier participation, and no second NDA is recorded.')

# ---- section 6.3: round-1 start; finality as a controlled field
span('i3-r1','Round 1 opens when the target or its banker begins soliciting potential buyers:','so that the boundary can be re-cut.',
"Round 1 opens when the target or its banker begins soliciting potential buyers. Use, in order: the first outreach wave; or the decision that launched it, where the filing reports the outreach as that decision's direct execution beginning within about a week; or, where the filing reports no target outreach and the participants came to the target instead, the first target-organized step that admits participants to a stage — the confidentiality-agreement wave or the process letter, whichever is earlier; or, in a bilateral case, the start of substantive sale negotiations. A single exploratory approach to one party, a sale-exploration decision or press release that defers or replaces outreach, and a vague earlier authorization are not the opening. Inbound enquiries, earlier approaches and unsolicited proposals before the opening remain in round 0; where such a proposal is still standing when round 1 is evaluated, the round map and Related rows must show the bidder as a round-1 participant even though its bid row sits in round 0. On the round 1 Round opened row, state `R1 anchor:` in Terms or outcome with the event used, list the Row ids of the other candidate anchors, and keep every rejected candidate as its own row so that the boundary can actually be moved.")
span('i7-finality','For each round, Summary records the opening, objective,','so that it can be filtered.',
"Summary's round map is specified in section 11.4(3). Give every round one finality value: **Announced as final** (the target told the bidders this was the final, binding or best-and-final stage), **Inferred final** (no such announcement, but the target moved to definitive negotiation with selected bidders or stated an intention to conclude an agreement) or **Not final** (neither, including a round for which no finality signal is found — say which in the reason). Record it in the expandable **Round finality** field on the round's Round opened row and describe it in Terms or outcome; where a Not final round is the last one observed, say so in Summary.")

# ---- section 8.1: date method wording, order constraint, trims, tightening sentence
rep('i11-dm1','Reported, Inferred (cross-paragraph), Assigned: deadline,','Reported, Inferred, Assigned: deadline,')
rep('i11-dm2','→ that day (Reported, or Inferred (cross-paragraph)).','→ that day (Reported; or Inferred when context, in the same or another paragraph, rather than an explicit statement establishes the day).')
rep('i11-span','4. A finite window with nothing better → its calendar midpoint, rounding toward the earlier day (Assigned: midpoint).',
    '4. A finite window with nothing better → its calendar midpoint, rounding toward the earlier day (Assigned: midpoint). An event that itself spans the reported period — a diligence period, a series of presentations — takes its first day instead (Assigned: bound).')
rep('i11-seq','6. No date at all → the Working date of the row it follows in the sequence (Assigned: sequence).','6. No date at all → the Working date of the row it follows in # (Assigned: sequence).')
rep('i11-order',"Where a rule would break this, move the date to the nearest admissible day inside the row's own window and say so in the reason.",
    "Fix Reported and Inferred days first; they never move. Then assign the remaining rows in # order. Where a rule would break the constraint, move the assigned date to the nearest admissible day inside the row's own window, set Date method to Assigned: sequence, and say so in the reason.")
rep('trim-8.1a',' The report date is not the event date; it may serve as the assigned Working date under the rules below. |',' The report date is not the event date. |')
rep('trim-8.1b'," Do not invent the missing endpoint. The predecessor's day may serve as the assigned Working date under the rules below; that is a sort position, not a finding that both happened on the same day. |",' Do not invent the missing endpoint. |')
rep('trim-8.1c','| Leave Date from and Date to empty. Assign the Working date from the supported position in the sequence (rule 6 below). |','| Leave Date from and Date to empty. |')
rep('i2-tighten','a committee that reviewed offers bounds their receipt; an event narrated between two dated meetings is bounded by both.',
    'the meeting at which a committee is shown to have had the full set of offers before it — normally the one that compared them or decided on them — bounds their receipt, while an earlier review meeting bounds only the offers the filing shows it considered and is otherwise a preferred reading to state in the reason; an event that the filing places in sequence between two dated events is bounded by both.')

# ---- section 8.3: deadline treatment as a controlled field, with the three clarifications
rep('i8-field','Begin Terms or outcome on each Deadline row with the same value (`Treatment: Extended`, and so on) so that it can be filtered.',
    'Record the same value in the expandable **Deadline treatment** field on each Deadline row.')
rep('i8-clar','Values can combine; record both extension and later acceptance when both occurred.',
    "Only Extended and Late bids accepted can combine, written `Extended; Late bids accepted`; Enforced, Passed without action and Unclear are residual and never combine. A bid is late only where its Date from falls after the due date: a window that merely straddles the due date, or an assigned Working date, does not make a submission late. A price revision that the target itself solicited after the due date from a bidder that had already submitted on time belongs to the round's continuing negotiation and is not late acceptance. Where this due date replaced an earlier one, the extension is recorded on the Deadline revised row and in the Summary map; this row's treatment describes only what followed this date.")
rep('fix-finaldue','A target request, made after a final due date has arrived,','A target request, made after the due date of a round already opened as final has arrived,')

# ---- section 9.1: late reconfirmation narrowed
span('i1-reaff','**Late reconfirmation.** When, in a stage the target intends to conclude','Signing alone never creates one.',
"**Late reconfirmation.** A target can finalize a definitive agreement on an offer the bidder never formally restates. Record one **Bid reaffirmed** when all three hold: (a) the target has moved to finalize a definitive agreement with that bidder on its standing offer — a decision to negotiate or complete the agreement with it, or executed exclusivity — and is not awaiting a priced submission from it under a pending solicitation; (b) the row changes the record: the bidder's latest priced row is Informal, or sits in a round whose Round finality is Not final (section 6.3); (c) the filing reports a bidder-side act — the bidder or its counsel returns a revised agreement draft, or the bidder confirms its price. Use the first such act. The row carries the standing price with Price origin = Carried forward (never Stated), Count under section 7.2, Formality = Formal (signal 1 for a returned draft, signal 3 for a price confirmation) and Conditions level assessed as of that date — a returned draft does not by itself show that diligence or financing conditions have fallen away. Begin Terms or outcome with `Reaffirmed by: returned draft` or `Reaffirmed by: price confirmed`, and flag it for review. No other draft creates one: comments or markups sent ahead of a solicited bid belong to that bid; drafts exchanged after the bidder's Formal bid in the final or definitive stage get no row (section 4); a material change in readiness or financing is an Offer update. A confirmation given with a priced bid, or on the same day, is part of that Bid row. A target's draft, a discussion between counsel, a target's unanswered request and signing itself never create one.")
rep('trim-9.1','Signing records agreed consideration, not a separately submitted final bid on an invented earlier date. Do not invent a new price or an undated submission to supply a “missing formal offer”; a supported late reconfirmation is recorded as Bid reaffirmed (above).',
    'Signing records agreed consideration, not another bid (section 11.3). Do not invent a price or an undated submission to supply a “missing formal offer”.')

# ---- section 9.3: financing vocabulary, Heavy by context, trims, worked example
rep('fix-fin','`Fin: committed | represented | not committed | not stated;','`Fin: committed | no contingency | not needed | represented | not committed | not stated;')
rep('fix-heavyctx','is Heavy by context: it is inherently subject to that diligence.','is Heavy by context, whatever diligence wording the indication itself uses: it is inherently subject to that diligence. Substantive access means data-room or management access; a teaser or information memorandum alone is not.')
rep('trim-9.3a','Silence about financing neither raises nor lowers the level: record the **reported absence** of a commitment, which is what supports Heavy, and never treat silence as a commitment or as a failure to provide one. None requires affirmative support, not silence or the mere passage of time.',
    'Silence about financing neither raises nor lowers the level: only a **reported absence** of a commitment supports Heavy, and None requires affirmative support, not silence or the passage of time.')
rep('trim-9.3b','Never write that financing or a document was “not provided” merely because the filing does not mention it.','Write `not stated`, never “not provided”, when the filing is silent. A complete string reads: `Fin: committed; DD required: not stated; DD open: yes; Excl: requested (2 wks)`.')

# ---- section 9.4: price bounds in both directions
span('i4-bound','- “At least $X” or “at or above $X”: set Price kind = Bound only,','say so in Questions.',
"- A one-sided price statement fills the endpoint cell on the side of the inequality and leaves the other blank: a floor (“at least $X”, “at or above $X”, “in excess of $X”, “no less than $X”) in **Price low**; a ceiling (“up to $X”, “no more than $X”, “not above $X”) in **Price high**. Set Price kind = Bound only and begin Terms or outcome with `Bound: ≥ X` or `Bound: ≤ X` followed by the filing's words. A Bound only row states no bid level: leave Cash at closing blank, never average it with actual bids, and never treat the cell as a submitted endpoint. This applies to a communicated offer or indication; a valuation statement that is not an offer keeps its number in text under the bullet below. A bound on a premium, multiple or aggregate value is not a per-share bound and stays in Terms or outcome. An imprecise range (“low-to-mid $20s”) supplies no endpoints: leave both cells blank. Where the wording is ambiguous between a floor on the whole range and a level the range merely reached, say so in Questions.")

# ---- section 10.1: who has entered; who is live
rep('fix-entered-10.1','Outcome labels apply only to a participant that had entered the process — responsive to contact, under NDA or bidding.',
    'Outcome labels apply only to a participant that had entered the process — under NDA, bidding, or otherwise actually participating in diligence or negotiation; a positive reply to an enquiry is not yet entry. Live means entered and not yet closed by a recorded outcome; a paused bidder is live.')

# ---- section 10.2: rewritten with all approved fixes
span('fix-10.2','**Every participant that entered a stage is closed out in the ledger.**','not how or why.',
'''**Every participant that entered the process is closed out once in the ledger.** Only the winner has no exit row; a bidder that joined a group is closed by Joined group. A stage is a round of section 6.3, round 0 included. Record what the filing reports first, with Outcome basis = Stated. Then, at each transition — a submission due date, an advancement decision, executed exclusivity, signing, process termination, go-shop expiry — close any participant or residual cohort that has no evidenced outcome with **one inferred row**, at the first transition at which the filing names or counts the continuing participants without it. A bid that the target considered after the due date (Deadline treatment: Late bids accepted) is a submission to that solicitation, not an absence.

| Situation | Label | Outcome basis | Decided by; Exit reason | Working date; Date method |
|---|---|---|---|---|
| Eligible for a solicitation, no submission reported; number known by subtraction: the stated base minus every participant the filing accounts for at that transition (submitters, stated exits, and anyone shown to continue without submitting) | Did not submit | Inferred: residual | Unknown; Not stated | The solicitation's due date; Assigned: deadline |
| Bid or was live in a stage; the filing names or counts the advancing set without it and reports no notice to it | Dropped by target | Inferred: residual | Target; Not stated | Day of the advancement decision; Assigned: decision day |
| Live rival when the target executes exclusivity with another bidder | Dropped by target | Inferred: exclusivity | Target; stated reason, else Not stated | Execution date; Assigned: decision day |
| Last seen in the process — in diligence or under NDA — and never mentioned again by signing | Not selected at signing | Inferred: silent | Unknown; Not stated | Signing date; Assigned: bound |

A bidder that was still bidding when the target chose another is Not selected at signing with Outcome basis Stated, not Inferred: silent. On inferred rows When reads “by [that date]”, Date to is that date, Date from is blank, and Date method is as in the table — never Reported. An inferred row carries the Round in which its transition falls, quotes the passages that give the base and the continuing set or the participant's last appearance, and takes that page.

An inferred closing row may never precede the row that records the participant's entry. Where the transition's date is earlier — a cohort whose signing window straddles the due date — the entry row's Working date is moved earlier under section 8.1's order constraint, inside its own window, and the reason says so.

On an inferred row, begin Terms or outcome with the Outcome basis value and show the arithmetic: “Inferred: residual — 15 NDA signers − 6 submitters = 9 non-submitters.” Stated rows take no opener. The Outcome basis cell holds only one of the five values; qualifiers such as “(base assumes …)” or “≥” belong in Terms or outcome. Count is the residual. For example, if fifteen eligible participants and an exhaustive list of six submitters refer to the same solicitation and period, record nine non-submitters as one inferred cohort. Split the cohort by type when the filing allows. Do not infer decision dates, motives, identities or voluntary withdrawal from the arithmetic, and never write individual rows for anonymous members.

Where the base population is uncertain — overlap, eligibility or completeness — still write the row. Use the filing's stated base: Count = stated base − the participants accounted for, with Terms or outcome reading “Inferred: residual (base assumes …)” and giving the range the uncertainty allows. Where the base is a lower bound, Count is the lower-bound residual and Terms or outcome says “≥”. Leave Count blank only when the filing gives no number at all. Flag it.

A named party that the filing introduces and then never mentions again, and that may sit inside an anonymous residual, gets one exit row of its own with **Count 0** and Outcome basis = Inferred: identity, under the same label as the cohort row that covers it, at the first transition whose continuing set is identified without it. Terms or outcome names every cohort row that could already count it, recommended reading first, and gives the reason; list it in Questions. Never move counts from a cohort to a name on this basis. A participant closed at one transition is not closed again unless it has Re-entered.

When a process is terminated, its Process terminated row closes the remaining participants: Count is the number still live in that process — this overrides the blank Count of section 7.2 for this row — and Terms or outcome shows the arithmetic and names them where the filing does. Leave Count blank, and say so, only where the number cannot be established; the balance for that process is then reported with bounds. A party that enters during a go-shop and makes no proposal is closed at the go-shop's expiry: Did not submit, Outcome basis Stated where the filing reports that the period ended without a qualifying proposal, otherwise Inferred: residual. A party that does make a proposal is closed by that proposal's own outcome, which may fall after expiry.

Eventual non-acquisition does not reveal the bidder's path through the auction: an inferred row says only that the participant was out by that transition, not how or why.''')

# ---- section 11: controlled columns, column order, new fields, tags, labels, questions
rep('fix-lists','Controlled categories use Lists drop-downs.',
    'Controlled categories use Lists drop-downs. Controlled columns are What happened, Type, Formality, Conditions level, Include, Date basis, Date method, Price kind, Price origin, All cash, Deadline treatment, Round finality, Decided by, Exit reason and Outcome basis. Use the exact strings given in this instruction, including capitals, colons and spacing; Lists holds exactly these.')
rep('fix-order','Keep the following fields to the right in labelled, **collapsed expandable column groups**, not additional sheets:',
    'Keep the following fields to the right, in this order from left to right, in labelled, **collapsed expandable column groups**, not additional sheets:')
rep('i78-fields','| Due date | Submission due date only, where applicable. |',
    '| Due date; Deadline treatment; Round finality | Submission due date only, where applicable; the treatment value on Deadline rows (section 8.3); the finality value on Round opened rows (section 6.3). |')
rep('fix-tags','These are fields of the same ledger, not another data model.',
    "**Tags.** Where this instruction prescribes a fixed phrase for Terms or outcome, write it exactly as spelled, before the prose; separate tags with a semicolon and the last tag from the prose with a dash, as in “Inferred: residual — 15 NDA signers − 6 submitters = 9 non-submitters.” When several apply use this order: `R1 anchor: …`; `Inferred: …`; `Reaffirmed by: …`; `Bound: ≥ X` or `Bound: ≤ X`; `Support: …`. A tag repeats a structured field or a Summary entry and must agree with it.\n\nThese are fields of the same ledger, not another data model.")
span('i11-access11','| Information access changed | Who was given, or denied, what information and when:','(section 4). |',
    '| Information access changed | Differentiated, staged, withheld or catch-up access among live bidders, and projections or comparable information issued, revised or withheld once bidding has begun (section 4). Not uniform stage access; not individual meetings. Count blank. |')
rep('i6-gloss','Not a shareholder rollover or financing support (section 5.3). |','Not a shareholder rollover; for financing support see section 5.3. |')
rep('fix-pilot','and **all conditionality assessments during the pilot**, with affected rows identified.',
    'every Conditions level that turns on a stated diligence period, every None, every late reconfirmation row, and a winner that reaches signing with no Formal row — with affected rows identified.')

# ---- section 12: examples
rep('trim-12A',"arithmetic shown — never with individual dates, motives or identities. If the base population is uncertain, still write the row from the filing's stated base, say what the base assumes, and flag it.",'arithmetic shown.')
rep('i2-exB','The first review on July 22 is read as bounding their receipt (window July 20–22), flagged for review as a cross-paragraph inference.',
    "Their Date from/Date to window is July 20–27: the July 27 meeting, which compared all six and chose two, is the first point by which every LOI is established as received. The July 22 review makes July 20–22 the likelier window, and the reason says so and flags it, but it is not entered as a bound: the filing does not say which LOIs were before the first meeting, G&W's own LOI arrived after the deadline, and in the previous round the same filing reports offers arriving up to the second of two review meetings.")
span('i1-exC',"Party B's refusal to raise, when asked on August 12",'`DD open: no`.',
    "Begin Terms or outcome with `Reaffirmed by: returned draft`. Party B's refusal to raise when asked on August 12, after diligence had finished, is not a second reaffirmation: it goes on Party B's closing row (Exit reason Would not improve earlier offer, noting that diligence had ended on August 11). G&W gets no such row: the August 3 draft came from the target, August 10 was a discussion between counsel, and its August 12 submission is a new Bid.")
span('trim-12E',' A rival displaced when another bidder obtains executed exclusivity is Dropped by target','Not selected at signing, Inferred: silent.','')

# ---- section 13: checks
rep('fix-13.3a','Participant stock per stage = entrants − exits + re-entries; it is never negative, and only the winner remains at signing.',
    "Participant stock per stage = entrants − exits + re-entries; it is never negative, and at signing only the winner remains (and again after any go-shop expiry). A participant **enters** a process at its first NDA signed or Bid row in that process, or at the target decision that admits it to a stage, counted once as a whole-company bidder unit however many such rows it has; contacts that never became an NDA, a bid or an admission, and adviser, lender and rollover-holder agreements, never enter and are never closed. Exits are Dropped by target, Withdrew, Did not submit, Not selected at signing and Joined group rows, and participants closed by a Process terminated row or at go-shop expiry; Participation paused is not an exit. A Bidding group changed row that states “units −1” moves the stock by that stated amount, not by its Count. On every outcome row Outcome basis is filled, and an inferred row's Terms or outcome begins with the same value.")
rep('fix-13.3b','Do not require a named exit for an anonymous outcome or fabricate a winner for an abandoned process.',
    'Do not require a named exit for an anonymous outcome (the Count-0 identity row of section 10.2 excepted) or fabricate a winner for an abandoned process.')
rep('fix-13.4','no inferred or assigned date is labelled Reported.',
    'no inferred or assigned date is labelled Reported; Date method is Reported exactly when Date basis is Reported day, and Inferred exactly when it is Inferred day.')
rep('fix-13.6','Bidder types, adviser clients and group changes are consistent without erasing genuine changes.',
    'Bidder types, adviser clients and group changes are consistent without erasing genuine changes. Tags and structured fields agree: every Round opened row has a Round finality value and the round-1 row an `R1 anchor:` tag; every Deadline row has a Deadline treatment matching the Summary map; every inferred outcome row opens with its Outcome basis; Date basis and Date method are a permitted pair; Page is filled wherever Source is.')

open(P,'w',encoding='utf-8').write(s)
print(len(log),'batch-3 edits applied')
