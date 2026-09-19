# Record of every edit made on 19 Sep 2026 to the 18 Sep 2026 instruction (Pro revision).
# The 18 Sep text was deleted from the repo at Austin's request; an identical copy is inside
# model_review_2026-09-18/SEC_12_Extraction_Review_Package.zip (SEC_Deal_Ledger_Extraction_Instruction_v2.md).
# To rebuild: extract that file to BASE below, copy it to P, then run this script.
# The three header edits were afterwards reworded by hand to remove the version number.
BASE='SEC_Deal_Ledger_Extraction_Instruction_2026-09-18.md'
import sys
P='SEC_Deal_Ledger_Extraction_Instruction.md'
s=open(P,encoding='utf-8').read()
log=[]
def rep(tag,old,new):
    global s
    n=s.count(old)
    assert n==1, f'{tag}: anchor found {n} times: {old[:70]!r}'
    s=s.replace(old,new); log.append(tag)
def span(tag,start,end,new):
    global s
    assert s.count(start)==1, f'{tag}: start anchor x{s.count(start)}'
    i=s.index(start); j=s.index(end,i)+len(end)
    s=s[:i]+new+s[j:]; log.append(tag)

# ---------- header
rep('H1','# Reading a merger filing into a deal ledger: extraction instruction, version 2',
    '# Reading a merger filing into a deal ledger: extraction instruction, version 3 (draft)')
rep('H2','**Pro revision — 18 September 2026**  ',
    '**Draft of 19 September 2026.** Version 2 (Pro revision, 18 September 2026) revised after an audit against Alex Gorbenko\'s collection instructions, voice notes and hand-collected deals. Not yet run; not yet reviewed by Alex.  ')
rep('H3','This is the complete replacement for the earlier version 2, the ten-table instruction and the readable-Excel override.',
    'This replaces version 2 and every earlier instruction.')

# ---------- section 1 (P13, proposed)
rep('S1-counts','as needed to resolve buyer type, consideration, dates and conflicts.',
    'as needed to resolve buyer type, consideration, dates, counts and conflicts.')

# ---------- section 2 bullets
rep('S2-exits','- Record supported participation changes, not invented exits to close the ledger. Treat temporary suspension separately from withdrawal.',
    '- Close out every participant that entered a stage. Record evidenced outcomes as stated; close the rest with clearly marked inferred rows (section 10.2), never with invented dates, motives or identities.')
rep('S2-dates','- Preserve uncertain date expressions; any bounded-window working date is an explicitly assigned convenience, not an observed date or proof of sequence.',
    '- Preserve uncertain date expressions in When and the date bounds, and give every row an assigned Working date that respects the known order (section 8.1). A Working date is a sort key with a stated method, not an observed date.')

# ---------- section 3.3
rep('S3.3a','Leave unsupported numeric and date cells empty, never zero.',
    'Leave unsupported numeric cells and unsupported date bounds empty, never zero. Working date is the exception: it is an assigned sort key, always filled under section 8.1.')
rep('S3.3b','It must not include fabricated precision, identities or events.',
    'It must not include fabricated precision, identities or events. A Working date that carries its Date method, and a closing row marked as inferred under section 10.2, are disclosed conventions, not fabrication.')

# ---------- section 4 scope
rep('S4a','Routine calls, meetings, visits and document exchanges are not automatically rows.',
    'Routine calls, meetings, visits and document exchanges are not rows.')
span('S4b','This is not a comprehensive legal-terms project.','Routine legal drafting does not merit its own history.',
'''This is not a legal-terms project, and the ledger must stay small enough to review. **Do not create rows for:** negotiation of deal protection and legal terms (termination or reverse termination fees, liability caps, no-shop or fiduciary-out wording, voting agreements, post-signing covenants); successive agreement drafts; meetings, site visits, calls and document exchanges with bidders already under NDA; or the successive steps of a shareholder-rollover or financing-support discussion. Put a term that the filing makes consequential for selection, price or commitment on the related Bid, Target decision or signing row. A rollover or financing-support relationship gets at most one row when it is permitted or formed and one when it is resolved. After signing, record only competing proposals, go-shop activity, termination of the agreement and closing; regulatory filings, clearances and litigation belong, if anywhere, in one Summary line.

**Keep information-access events as rows:** who was given what information, when, and who was not — staged or differentiated data-room access, management presentations given to some bidders and not others, projections supplied, updated or withheld, a late entrant's catch-up access. Use **Information access changed** (section 11.3), one row per distinct change in access (for example one row for a series of management presentations, naming the bidders and dates), not one row per meeting.''')

# ---------- section 5.3 groups
rep('S5.3a','Use **Bidding group changed** for formation or material membership changes.',
    'Use **Bidding group changed** for formation of a group of prospective acquirers or a material change in which acquirers belong to it.')
rep('S5.3b','A request to work together is not proof that a joint bid was submitted.',
    'A request to work together is not proof that a joint bid was submitted.\n\nA shareholder rolling over its stake, a financing provider or another supporter admitted to the buyer\'s vehicle is **not** a membership change, even when the filing\'s defined term for the buyer later includes it. **Bidding group changed** applies only when a party that could have bid independently becomes part of, or leaves, the bidding unit.')

# ---------- section 5.4 advisers
rep('S5.4',"A bank's renaming or acquisition ordinarily remains one adviser relationship, with the change noted.",
    "A bank's renaming or acquisition ordinarily remains one adviser relationship, with the change noted. Never open a second adviser row for a renamed or acquired firm already on the ledger.")

# ---------- section 6.2 (P13, proposed)
rep('S6.2','There is no fixed gap length.',
    'There is no fixed gap length. A largely new set of participants after the dormancy supports a new process; the same participants resuming supports the same process.')

# ---------- section 6.3 rounds
rep('S6.3a','or moves to definitive negotiation with selected bidders. A single negotiating buyer',
    "or moves to definitive negotiation with selected bidders. The target's **first** request for final, binding or best-and-final offers also opens a new round, even when the invited bidders are unchanged. A single negotiating buyer")
rep('S6.3b','or another price-improvement request to the same finalists does not by itself create a round.',
    'or a further price-improvement request to the same finalists after a final solicitation has already opened does not by itself create a round.')
rep('S6.3c','Distinguish **announced as final**, **inferred final negotiation**, and merely **last observed**.',
    "Distinguish **announced as final**, **inferred final negotiation**, and merely **last observed**. State the same finality at the start of Terms or outcome on the round's Round opened row — `Announced as final`, `Inferred final` or `Not final` — so that it can be filtered.")

# ---------- section 7.3 counts
rep('S7.3','Do not convert a literal “at least” to exact merely because the narrative names no others.',
    'Do not convert a literal “at least” to exact merely because the narrative names no others. Equally, do not add “at least”, “approximately” or a range that the filing does not use: a number the filing states exactly is recorded as exact. Where a board update or the Reasons section states a total, use it to check the narrative count and reconcile the two in Summary.')

# ---------- section 8.1 dates
rep('S8.1a','The expandable fields preserve **Date from**, **Date to**, **Working date** and **Date basis**.',
    'The expandable fields preserve **Date from**, **Date to**, **Working date**, **Date basis** and **Date method**.')
rep('S8.1b','It describes timing, not the evidentiary basis of every fact in the row.',
    'It describes the timing the source gives, not the evidentiary basis of every fact in the row. **Date method** says how the Working date was chosen: Reported, Inferred (cross-paragraph), Assigned: deadline, Assigned: decision day, Assigned: midpoint, Assigned: bound, or Assigned: sequence. An inferred or assigned date is never labelled Reported.')
rep('S8.1c','| Upper bound only unless an earlier bound is independently supported. Do not turn the report date into the event date. |',
    '| Upper bound in Date to unless an earlier bound is independently supported. The report date is not the event date; it may serve as the assigned Working date under the rules below. |')
rep('S8.1d',"| Preserve the supported relative constraint and any ascertainable bound. Do not invent the missing endpoint or assume a subsequent event happened on its predecessor's day. |",
    "| Preserve the supported relative constraint and any ascertainable bound in Date from/Date to. Do not invent the missing endpoint. The predecessor's day may serve as the assigned Working date under the rules below; that is a sort position, not a finding that both happened on the same day. |")
rep('S8.1e','| Leave numeric date fields empty and retain any supported position in the sequence. |',
    '| Leave Date from and Date to empty. Assign the Working date from the supported position in the sequence (rule 6 below). |')
span('S8.1f','For a finite window, Working date defaults to its calendar midpoint','rather than silently shifting a date by a day.',
'''**Working date is always filled.** It is an assigned sort key, never a claim about when the event happened, and it must not replace the honest expression in When or the bounds in Date from/Date to. Use the first rule that applies and record it in Date method:

1. A reported day, or a day established by context → that day (Reported, or Inferred (cross-paragraph)).
2. A response to a solicitation whose due date lies inside the event's window, arrival day not disclosed → the due date (Assigned: deadline). This covers submitted offers and recorded non-submission alike.
3. An undated consequence or communication of a dated decision — bidders “subsequently” told they were out after a committee meeting, an instruction given after a board decision → the decision day, or the last of the meetings when the decision spans several (Assigned: decision day).
4. A finite window with nothing better → its calendar midpoint, rounding toward the earlier day (Assigned: midpoint).
5. A window with only one known bound → that bound (Assigned: bound).
6. No date at all → the Working date of the row it follows in the sequence (Assigned: sequence).

Then apply the order constraint: a Working date may not precede the Working date of a row the event is known to follow, nor come after that of a row it is known to precede. Where a rule would break this, move the date to the nearest admissible day inside the row's own window and say so in the reason. Example: offers received “between May 19 and June 1” against a May 19 due date take May 19 under rule 2, which also keeps them ahead of the May 23 meeting that considered them; a blind midpoint of May 25 would not. Explain strict before/after bounds and same-day sequencing in the reason.''')
span('S8.1g','Tighten a window only when a passage actually constrains that event.','not all offers discussed in a paragraph covering several meetings.',
'''Tighten Date from/Date to whenever a passage — including one in a different paragraph — constrains the event: a committee that reviewed offers bounds their receipt; an event narrated between two dated meetings is bounded by both. Read across paragraphs for these constraints before assigning dates, cite the constraining passage, and list consequential cases in Questions. A deadline does not prove arrival by that date, so it does not by itself change Date to; it can still be the assigned Working date under rule 2.''')

# ---------- section 8.2
rep('S8.2','Working dates need not increase down the ledger. Never change facts or bounds to make assigned dates sort neatly. Sort by # to restore the review order.',
    'Working dates never decrease down the ledger: sorting by Working date, with # breaking ties, must reproduce the # order. Achieve this by choosing the assigned date inside its honest window (section 8.1) or by correcting the reading order — never by changing facts, When, or the Date from/Date to bounds. Where the order of two rows is genuinely unknown, say so in the reason; their shared or adjacent Working dates are then only a display convention.')

# ---------- section 8.3 deadlines
rep('S8.3a','Record extensions even when they do not create a round.',
    'Record extensions even when they do not create a round. A target request, made after a final due date has arrived, that the same bidders submit improved bids by a new date is a **Deadline revised** — an extension of that round, carrying the old and new due dates — not a fresh Deadline set and not a new round; its treatment is Extended.')
rep('S8.3b','the Summary map states **Enforced**, **Extended**, **Late bids accepted**, **Unclear**, or **No deadline stated**, with evidence.',
    'the Summary map states **Enforced**, **Extended**, **Late bids accepted**, **Passed without action**, **Unclear**, or **No deadline stated**, with evidence. Begin Terms or outcome on each Deadline row with the same value (`Treatment: Extended`, and so on) so that it can be filtered. Passed without action means the due date arrived, bidding or negotiation simply continued, and the target neither cut anyone off nor announced a new date.')

# ---------- section 9.1 reaffirmation
rep('S9.1a','Use Offer update for material documentation/status evidence; omit routine exchanges. An updated model assessment is not itself a bidder submission.',
    'Use Offer update for material documentation/status evidence; omit routine exchanges. An updated model assessment is not itself a bidder submission.\n\n**Late reconfirmation.** When, in a stage the target intends to conclude with a definitive agreement, a bidder returns revised agreement drafts on its standing offer or confirms its price, record **Bid reaffirmed**: the standing price with Price origin = Carried forward (never Stated), Count under section 7.2, Formality = Formal (signal 3 in section 9.2), and Conditions level assessed as of that date — a returned draft does not by itself show that diligence or financing conditions have fallen away. Flag it for review. One such row per bidder per stage is enough unless the terms change; do not add a row for every draft.')
rep('S9.1b','Never fabricate a “missing formal offer.”',
    'Do not invent a new price or an undated submission to supply a “missing formal offer”; a supported late reconfirmation is recorded as Bid reaffirmed (above).')

# ---------- section 9.3 financing phrase
rep('S9.3','Distinguish committed funding, represented availability, explicit absence of commitment and silence.',
    'Distinguish committed funding, represented availability, explicit absence of commitment and silence, and state which on every Bid and Bid reaffirmed row with one fixed phrase: `Financing: committed`, `Financing: represented available`, `Financing: explicitly not committed` or `Financing: not stated`. Never write that financing or a document was “not provided” merely because the filing does not mention it.')

# ---------- section 9.4 CVR
rep('S9.4','Cash plus an expressly cash-settled earnout or CVR can be Yes; the term “CVR” alone does not establish settlement.',
    'Cash plus an earnout or CVR is Yes unless the filing indicates that the contingent piece is paid in shares or other securities: a contingent cash payment is not mixed consideration. Put the fixed part in Cash at closing and the contingent part, with its stated value and trigger, in Terms or outcome.')

# ---------- section 10
rep('S10.1h','### 10.1 Record a supported change, not an accounting closure','### 10.1 Outcome labels')
rep('S10.1a','| Dropped by target | Target excludes a participant or refuses admission to a stage.',
    "| Dropped by target | Target excludes a participant that had entered the process, refuses it admission to the next stage, or displaces it by executing exclusivity with a rival.")
rep('S10.1b',"| Participation paused | Negotiations or access are temporarily suspended, including evidenced displacement during another bidder's exclusivity. |",
    "| Participation paused | A bidder's own stated temporary stop, or a suspension the filing itself describes as temporary. Not used for rivals displaced by another bidder's exclusivity. |")
rep('S10.1c','| Not selected at signing | A bidder demonstrably remained a live alternative when the target signed with someone else.',
    '| Not selected at signing | A bidder whose participation had not ended through any earlier outcome when the target signed with someone else.')
span('S10.1d','Rival preference with continued participation is **Target decision**, not an exit.','Missing a deadline need not imply withdrawal.',
'''Rival preference with continued participation is **Target decision**, not an exit. **When the target executes exclusivity with one bidder, every other bidder still live in that stage gets Dropped by target on the execution date**: Decided by = Target, Outcome basis = Inferred: exclusivity unless the filing reports that they were told, Related rows pointing to the exclusivity row. A request for exclusivity, or its authorization, drops no one. A return request can use Material process update. **Re-entered** requires renewed activity, not necessarily formal admission, and is required whenever a participant bids, reaffirms or resumes diligence after a recorded outcome. Missing a deadline need not imply withdrawal: record Did not submit.

Outcome labels apply only to a participant that had entered the process — responsive to contact, under NDA or bidding. A decision not to invite a party that never entered is a **Target decision**, and a party declining an initial enquiry has its Contact and response (section 7.1); neither gets an outcome row.''')
span('S10.2','### 10.2 Silent participants','Eventual non-acquisition does not reveal the bidder\'s path through the auction.',
'''### 10.2 Closing out every participant

**Every participant that entered a stage is closed out in the ledger.** Only the winner has no exit row; a bidder that joined a group is closed by Joined group. Record what the filing reports first, with Outcome basis = Stated. Then, at each transition — a submission due date, an advancement decision, executed exclusivity, signing — close any participant or residual cohort that has no evidenced outcome with **one inferred row**, at the earliest transition that reveals its absence:

| Situation | Label | Outcome basis | Decided by; Exit reason | Working date |
|---|---|---|---|---|
| Eligible for a solicitation, no submission reported; number known by subtraction | Did not submit | Inferred: residual | Unknown; Not stated | The solicitation's due date |
| Live rival when the target executes exclusivity with another bidder | Dropped by target | Inferred: exclusivity | Target; stated reason, else Not stated | Execution date |
| Last seen in the process — bidding, in diligence or under NDA — and never mentioned again by signing | Not selected at signing | Inferred: silent | Unknown; Not stated | Signing date |

Begin Terms or outcome with the same words as Outcome basis and show the arithmetic: “Inferred: residual — 15 NDA signers − 6 submitters = 9 non-submitters.” Count is the residual. For example, if fifteen eligible participants and an exhaustive list of six submitters refer to the same solicitation and period, record nine non-submitters as one inferred cohort. Split the cohort by type when the filing allows. Do not infer decision dates, motives, identities or voluntary withdrawal from the arithmetic, and never write individual rows for anonymous members.

Where the base population is uncertain — overlap, eligibility, completeness, or whether a named party sits inside the anonymous residual — still write the row, leave Count blank, give the bounds in Terms or outcome and flag it. A named party that may sit inside an anonymous residual, such as an early signer never mentioned again, is covered by that cohort row and not given an individual row; say so in Summary and raise the identity question in Questions. A participant closed at one transition is not closed again unless it has Re-entered. When a process is terminated, its Process terminated row closes the remaining participants; state how many where known.

Eventual non-acquisition does not reveal the bidder's path through the auction: an inferred row says only that the participant was out by that transition, not how or why.''')
rep('S10.3a','fill the expandable **Decided by** and **Exit reason**, and state their meaning in Terms or outcome.',
    'fill the expandable **Decided by**, **Exit reason** and **Outcome basis**, and state their meaning in Terms or outcome. Outcome basis is **Stated**, **Inferred: residual**, **Inferred: exclusivity** or **Inferred: silent** (section 10.2).')
rep('S10.3b','Prioritize an informative stated constraint without changing actual agency.',
    'Prioritize an informative stated constraint without changing actual agency: a bidder that is asked to improve and declines takes **Would not improve earlier offer**, even where the target then chooses a rival and Decided by is Target.')

# ---------- section 11.2 fields
rep('S11.2a','| Date from; Date to; Working date; Date basis | Date bounds, explicitly qualified working date and timing basis under section 8. |',
    '| Date from; Date to; Working date; Date basis; Date method | Date bounds, always-filled assigned working date, timing basis and assignment method under section 8. |')
rep('S11.2b','| Decided by; Exit reason | Structured participation-outcome assessments. |',
    '| Decided by; Exit reason; Outcome basis | Structured participation-outcome assessments, including whether the outcome is stated or inferred (section 10). |')
rep('S11.2c','| Related rows | Stable Row ids',
    '| Page | Printed page of the main source paragraph, as a number, so that rows can be filtered and checked against the filing. |\n| Related rows | Stable Row ids')

# ---------- section 11.3 labels
rep('S11.3a','| Material process update | Material information/access change, business update, confidentiality change/reuse, return request, financing/rollover relationship or other consequential development.',
    '| Information access changed | Who was given, or denied, what information and when: staged or differentiated data-room access, management presentations, projections supplied, updated or withheld, a late entrant\'s catch-up access. One row per distinct change (section 4). |\n| Material process update | Business update, confidentiality change/reuse, return request, the permitted/formed and resolved steps of a rollover or financing-support relationship (at most one row each; section 4), or another consequential development with no specific label.')
rep('S11.3b',"| Bidding group changed; Joined group | Formation/composition changes and the end of a member's independent participation. |",
    "| Bidding group changed; Joined group | Formation/composition changes among prospective acquirers and the end of a member's independent participation. Not a shareholder rollover or financing support (section 5.3). |")

# ---------- section 11.4 summary
rep('S11.4a','first and last observed activities and outcome or observation limit.',
    'first and last observed activities and closing outcome with its basis (stated or inferred).')
rep('S11.4b','Outcome tallies, when useful, are labelled as occurrences or affected units rather than unique permanent exits.',
    'Show the per-stage balance: participants entering − stated exits − inferred exits = participants continuing, with the inferred share visible. Outcome tallies are labelled as occurrences or affected units rather than unique permanent exits.')

# ---------- section 11.5 questions
rep('S11.5a','- Uncertain agency/reasons for supported participation outcomes, and material unobserved-history gaps. Recommend preserving undisclosed history where that is the defensible answer; do not ask the reviewer to invent it.',
    '- Uncertain agency/reasons for participation outcomes, and **every inferred closing row** (section 10.2), grouped by transition with its arithmetic and any uncertainty about the base population.')
rep('S11.5b','- Consequential source conflicts, inferred dates/order, and working conventions that materially change interpretation.',
    '- Consequential source conflicts, inferred dates/order, and working conventions that materially change interpretation — including, in one grouped question, rows whose assigned Working date decides their order within a round.')

# ---------- section 12 examples
span('S12A','If later only some firms are discussed, do not manufacture withdrawal dates for the others.','not merely missing names.',
    'If only four of them later submit, close the other sixteen with one inferred row at the submission due date — Did not submit, Count 16, Outcome basis Inferred: residual, arithmetic shown — never with individual dates, motives or identities. If the base population is uncertain, write the row with Count blank and flag it.')
span('S12B','Keep the two G&W dates exact. The other late-July LOIs','not a fabricated formal extension.',
    "Keep the two G&W dates exact. Give the five undated late-July LOIs Working date July 20 (Assigned: deadline) and place them in # ahead of G&W's July 21 LOI, noting that their order relative to G&W is not actually known. The first review on July 22 is read as bounding their receipt (window July 20–22), flagged for review as a cross-paragraph inference. July 27 is the round's observed end, not an announced submission deadline. The July 21 offer considered in the process supports late acceptance, not a fabricated formal extension.")
rep('S12Ch','**C. Documents, not an invented new commitment.**','**C. A late reconfirmation, not an invented new price.**')
span('S12C','A material Offer update can retain the draft and the continuing offer.','the document exchange itself is not that evidence.',
    "Record **Bid reaffirmed** on August 4: $24 carried forward (Price origin Carried forward), Formal, Conditions level Heavy because on-site diligence was still open, flagged for review. Do not enter $24 as a newly stated price or infer Light/None from the draft alone. Party B's later refusal to raise, when asked on August 12 after diligence had finished, is a second reaffirmation and can support Light.")
rep('S12D','A package described as cash plus a CVR retains the components, but All cash remains Not stated unless the settlement of the CVR is established.',
    "A package described as cash plus a CVR retains the components: All cash is Yes unless the filing indicates settlement in securities, Cash at closing carries the fixed part, and the CVR's stated value and trigger stay in the text.")
rep('S12E1','with admission distinguished from the return attempt.',
    'with admission distinguished from the return attempt and a Re-entered row ahead of its new bid.')
rep('S12E2','A party never mentioned again has an observation limit in Summary, not automatically Not selected at signing.',
    'A rival displaced when another bidder obtains executed exclusivity is Dropped by target (Inferred: exclusivity) and gets Re-entered if it returns. A party last seen in the process and never mentioned again is closed at signing: Not selected at signing, Inferred: silent.')

# ---------- section 13 checks
rep('S13.2','There is **no universal NDA-minus-exits-minus-one-winner balance requirement**.',
    '**Per-stage balance:** for each process, participants entering a stage − stated exits − inferred exits = participants continuing, ending with the winner alone; Summary shows the balance and the inferred share. Where a base population is uncertain, show the balance with bounds rather than forcing it.')
rep('S13.3','Accept supported withdrawal, temporary suspension, re-entry, joining a group, signing, continued activity or an unobserved ending.',
    'Every participant ends in a stated outcome, an inferred closing row, joining a group, or signing. A bid, reaffirmation or resumed diligence after a recorded outcome requires a Re-entered row.')
rep('S13.4','Working dates are assigned only under section 8 and do not create historical order.',
    'Every row has a Working date and a Date method; sorting by Working date with # as tie-breaker reproduces #; no Working date falls outside its own Date from/Date to or contradicts a bound established elsewhere in the ledger; no inferred or assigned date is labelled Reported.')

open(P,'w',encoding='utf-8').write(s)
print(len(log),'edits applied:',' '.join(log))

# ---------- consistency sweep (second pass; run after the block above)
s=open(P,encoding='utf-8').read(); log=[]
rep('C1','## 10. Participation outcomes and unobserved history','## 10. Participation outcomes and closing out participants')
rep('C2','| Distinct supported participation outcomes. |','| Distinct participation outcomes, stated or inferred (section 10). |')
rep('C3','Supplied-source limitations and later unobserved outcomes are explicit.','Supplied-source limitations and inferred closings are explicit.')
rep('C4',"Not used for rivals displaced by another bidder's exclusivity. |","Not used for rivals displaced by another bidder's exclusivity. A pause does not close a participant: one that never resumes is still closed under section 10.2. |")
open(P,'w',encoding='utf-8').write(s)
print(len(log),'consistency edits applied:',' '.join(log))

# =====================================================================
# BATCH 2 — from the questions evaluation (agreed with Austin 19 Sep 2026)
# =====================================================================
s=open(P,encoding='utf-8').read(); log=[]

# ---------- B2-1 conditions construct (section 9.3 rewritten; supersedes batch-1 tag S9.3)
span('B2-cond','**Conditions level** measures unresolved material diligence','Reassess rather than blindly carry an earlier level forward.',
'''**Conditions level** measures the conditions **the bid itself carries** when it is made or reaffirmed: the bidder's financing position, the further diligence the bidder still requires, and any other material condition it attaches. It is separate from formality, from uncertainty about the amount ultimately paid, and from whether diligence was in fact still under way at that date, which is recorded separately below.

| Value | Test |
|---|---|
| None | The filing reports that the bidder is ready to sign: no further diligence required, financing committed or not needed, no other material condition. Ordinary closing requirements do not prevent this classification. |
| Light | No Heavy trigger is reported, and the bid is subject only to confirmatory, expedited or limited diligence or to final documentation — or the filing reports committed financing and attaches no diligence condition. |
| Heavy | Any one of: the filing reports that financing is not committed or is a contingency; the bid is subject to a further substantive diligence period (a stated multi-week or exclusive diligence period counts); or another material stated condition, such as a repricing right, an unresolved commercial requirement or an identified completion obstacle. |
| Insufficient evidence | The filing reports the price but nothing about the bid's financing, diligence or other conditions, or gives only a comparison, and the stage supplies no context. State what is known and a preferred reading when supported. |
| Varies | A cohort contains materially different condition states that cannot be assigned individually. Use only for cohorts. |

A preliminary non-binding indication made before the bidder has had substantive diligence access is Heavy by context: it is inherently subject to that diligence. “Non-binding” or a price range alone does not establish Heavy. Silence about financing neither raises nor lowers the level: record the **reported absence** of a commitment, which is what supports Heavy, and never treat silence as a commitment or as a failure to provide one. None requires affirmative support, not silence or the mere passage of time.

Fill the expandable **Conditions detail** on every Bid and Bid reaffirmed row in this fixed format, so that other constructs can be computed later: `Fin: committed | represented | not committed | not stated; DD required: none | confirmatory | substantive (N wks) | not stated; DD open: yes | no | not disclosed; Excl: requested (N wks) | granted | none | not stated`. **DD required** is what the bidder attaches to the bid. **DD open** is whether, on the narrative, that bidder's diligence was in fact still under way on that date; it does not move the level. Never write that financing or a document was “not provided” merely because the filing does not mention it. A commitment and absence of a financing contingency differ. Reassess at each new bid or reaffirmation rather than blindly carrying an earlier level forward.''')
rep('B2-cond2','Its associated substantive diligence or funding requirement may justify Heavy.',
    'A substantive diligence period or funding requirement attached to the same bid may justify Heavy.')
rep('B2-cond3','| Conditions level | Section 9 assessment on the same applicable rows. |',
    '| Conditions level | Section 9 assessment on the same applicable rows; its components sit in the expandable Conditions detail. |')
rep('B2-cond4','| All cash; Cash at closing | Settlement assessment and fixed closing cash per share. |',
    '| All cash; Cash at closing | Settlement assessment and fixed closing cash per share. |\n| Conditions detail | Fixed-format components behind Conditions level: financing, diligence required by the bidder, diligence open on the narrative, exclusivity (section 9.3). |')
rep('B2-cond5','including explicit insufficient evidence where necessary.',
    'including explicit insufficient evidence where necessary, and every Bid and Bid reaffirmed row has a Conditions detail string in the fixed format.')
span('B2-exC','Record **Bid reaffirmed** on August 4: $24 carried forward','and can support Light.',
    "Record **Bid reaffirmed** on August 4: $24 carried forward (Price origin Carried forward), Formal, flagged for review. Conditions level is Light, because the only condition Party B ever attached was an expedited diligence review; Conditions detail records `DD open: yes` (on-site to August 11). Do not enter $24 as a newly stated price or infer None from the draft alone. Party B's refusal to raise, when asked on August 12 after diligence had finished, is a second reaffirmation with `DD open: no`.")
rep('B2-exD','A non-binding LOI with bidder-returned acquisition agreement markups and substantial unfinished diligence is Formal and Heavy.',
    'A non-binding LOI with bidder-returned acquisition agreement markups that is subject to a further multi-week diligence period is Formal and Heavy; the same LOI subject only to an expedited or confirmatory review is Formal and Light.')

# ---------- B2-2 close-out details (uncertain base; named party that vanishes; stock check; go-shop)
span('B2-base','Where the base population is uncertain — overlap, eligibility, completeness, or whether a named party sits inside the anonymous residual','raise the identity question in Questions.',
'''Where the base population is uncertain — overlap, eligibility or completeness — still write the row. Use the filing's stated base: Count = stated base − evidenced exits, with Terms or outcome beginning “Inferred: residual (base assumes …)” and giving the range the uncertainty allows. Where the base is a lower bound, Count is the lower-bound residual and Terms or outcome says “≥”. Leave Count blank only when the filing gives no number at all. Flag it.

A named party that the filing introduces and then never mentions again, and that may sit inside an anonymous residual, gets one exit row of its own with **Count 0** and Outcome basis = Inferred: identity, at the first transition whose continuing set is identified without it. Terms or outcome names the cohort row that already counts it and the alternative reading; list it in Questions. Never move counts from a cohort to a name on this basis.''')
rep('B2-basis','Outcome basis is **Stated**, **Inferred: residual**, **Inferred: exclusivity** or **Inferred: silent** (section 10.2).',
    'Outcome basis is **Stated**, **Inferred: residual**, **Inferred: exclusivity**, **Inferred: silent** or **Inferred: identity** (section 10.2).')
rep('B2-5.2','Put a defensible identity hypothesis in Questions, not into the ledger as settled identity.',
    'Put a defensible identity hypothesis in Questions, not into the ledger as settled identity. The Count-0 row of section 10.2 is the one exception: it records that a named party was out by a given transition, not which anonymous exit was its own.')
rep('B2-goshop','When a process is terminated, its Process terminated row closes the remaining participants; state how many where known.',
    'When a process is terminated, its Process terminated row closes the remaining participants; state how many where known. Parties that enter during a go-shop are closed at its expiry.')
rep('B2-stock','A bid, reaffirmation or resumed diligence after a recorded outcome requires a Re-entered row.',
    'A bid, reaffirmation or resumed diligence after a recorded outcome requires a Re-entered row. Participant stock per stage = entrants − exits + re-entries; it is never negative, and only the winner remains at signing.')

# ---------- B2-3 deadline treatment defined from the ledger (Alex's soft-deadline note)
span('B2-enf','Passed without action means the due date arrived','not merely absence of disclosed later bids.',
'''Decide the treatment from what followed in the same round. **Extended:** a Deadline revised row moves this due date, whenever it was issued. **Late bids accepted:** the target considered a bid dated after the due date without any revision. **Enforced:** the date passed with neither of these, and the target took its next step — selection, exclusion, next round or exclusivity — on the bids in hand. **Passed without action:** the date passed with no extension and no selection step, and bidding or negotiation simply continued. **Unclear:** the filing does not say what followed. Values can combine; record both extension and later acceptance when both occurred.''')

# ---------- B2-4 recommended items not individually confirmed
span('B2-R1','Round 1 starts at an established operative launch;','Earlier approaches/proposals remain in round 0.',
    "Round 1 opens when the target or its banker begins soliciting potential buyers: the first outreach wave, or the launch decision when outreach follows at once; in a bilateral case, the start of substantive sale negotiations. A sale-exploration decision or press release that defers outreach to a later date is not the opening, and a vague earlier authorization is insufficient. Inbound enquiries, earlier approaches and unsolicited proposals before the opening remain in round 0. On the round 1 Round opened row, state `R1 anchor:` with the event used and list the Row ids of the other candidate anchors, so that the boundary can be re-cut.")
rep('B2-bound','- “A range reached at least $80” constrains its upper endpoint, not its lower endpoint. Leave both numeric price cells blank, set Bound only, and write the precise constraint in Terms or outcome.',
    "- “At least $X” or “at or above $X”: set Price kind = Bound only, put X in Price low, leave Price high blank, and begin the constraint in Terms or outcome with `Bound: ≥ X` followed by the filing's words. The cell is a bound, not a bid. Where the wording is ambiguous between a floor on the whole range and a level the range merely reached, say so in Questions.")
rep('B2-support','**Bidding group changed** applies only when a party that could have bid independently becomes part of, or leaves, the bidding unit.',
    "**Bidding group changed** applies only when a party that could have bid independently becomes part of, or leaves, the bidding unit.\n\nA party that finances or supports another bidder's offer does not thereby bid. The supported bidder keeps its own name and Type, with `Support: [party] (financing)` in Terms or outcome and Related rows pointing to any earlier independent bid by the supporter. If the supporter was still a live independent bidder when the support began, close its independent participation with Joined group; if it had already exited, it gets no new row.\n\nWhen members of an anonymous cohort combine, the Bidding group changed row states the effect on the number of bidding units (“2 of the 15 signers combine; units −1”), so that stage counts reconcile by number rather than identity. Never backfill an NDA or entry row that the filing does not report.")
rep('B2-adviser','Long-standing service may have no ascertainable commencement date.',
    'Long-standing service may have no ascertainable commencement date. Use the earliest date the filing shows the adviser selected or acting for that client as the Working date, and list every disclosed date (selected, first advice, engagement letter) in Terms or outcome.')
rep('B2-signing','One such row per bidder per stage is enough unless the terms change; do not add a row for every draft.',
    'One such row per bidder per stage is enough unless the terms change; do not add a row for every draft. Signing alone never creates one.')

rep('B2-exA','If the base population is uncertain, write the row with Count blank and flag it.',
    "If the base population is uncertain, still write the row from the filing's stated base, say what the base assumes, and flag it.")
open(P,'w',encoding='utf-8').write(s)
print(len(log),'batch-2 edits applied:',' '.join(log))
