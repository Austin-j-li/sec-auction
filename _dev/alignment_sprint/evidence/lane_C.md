# Lane C audit: participants, entry, counts, exits, advisers, dates

Auditor C, 27 September 2026. Sources: instruction v0 (`SEC_Deal_Ledger_Extraction_Instruction.md`, cited by rule and line), Alex's voice notes (V¶n, colour noted), Alex's collection instructions (CI p.N), `_dev/STATUS.md`. I checked the relevant passages in the Mac-Gray, Providence & Worcester, Penford, sTec and Kraton filings in `raw_filing/`. I did not read `_dev/ALEX_ALIGNMENT.md`, `extraction/`, `ref/` or git history. No settled ruling is reopened. Filing page numbers are the printed page, read from the page-footer markers in the filing text. Where a settled ruling bears on an item, it is cited as the result the fix must still produce.

Colour key: black = important/easier; dark red (8B0000) = important/difficult; blue (0000CD) = less important/easier; magenta (8B008B) = less important/difficult. V¶129–166 are "Claude's reading" and count for less than Alex's own words.

## Count

| Type | High | Medium | Low | Total |
|---|---|---|---|---|
| CONFLICT | 1 (C3) | 2 (C4, C5) | 0 | 3 |
| MISSING | 0 | 1 (C7) | 3 (C11, C15, C16) | 4 |
| ADDED | 0 | 1 (C6) | 1 (C13) | 2 |
| AMBIGUOUS | 1 (C1) | 2 (C2, C8) | 5 (C9, C10, C12, C14, C17) | 8 |
| **Total** | 2 | 6 | 9 | 17 |

The three most important are C1, C2 and C3.

---

## C1. A named party inside an unnamed group: entry totals versus later steps

- **Instruction:** E3 Cohorts, line 161: "A named party that may belong to the group stays inside it: do not enter it again as an additional entrant." E14 inferred exit 3, line 302: "A named bidder eligible for a solicitation, with no offer reported and never mentioned again → Did not submit at the due date."
- **Alex:** V¶21–24 (magenta). A party the filing names early and then never mentions again is presumed not to be the unnamed party in a later group: "since the deal background thought it prudent to mention bidder A initially, it would then continue mentioning this bidder". So Providence's Party A "never made it out of round one," and the round-2 strategic non-submitter "is unnamed, it's not bidder A". V¶41, V¶45 (dark red): the Mac-Gray NDA total must reconcile with named rows so that "the math has to check out".
- **Type / severity:** AMBIGUOUS, **High**. It decides which round a named bidder leaves in, and whether the anonymous groups are counted correctly.
- **Where it bites:**
  - *Providence & Worcester:* the filing says "11 potential strategic buyers (including Party A) and 18 potential financial buyers", and that "each of the potential strategic buyers and 14 potential financial buyers" signed NDAs, which is 25. It then reports nine unnamed IOIs, and in round 2 "one strategic buyer and one financial buyer elected not to submit an LOI" (p. 28–30).
    - Read literally, the line-161 clause lets Party A "stay inside" either later unnamed group: the nine IOI bidders, or the round-2 strategic non-submitter. Party A would then advance to round 2, or exit there.
    - E14 rule 3 instead closes Party A at the round-1 due date (19 May 2016). The settled ruling (16 inferred non-submitters: Party A plus a cohort of 15) needs rule 3 to win.
    - For entry totals the clause is correct. Party B and G&W are named later and must stay inside the 25 rather than being added as extra entrants. Otherwise the settled 25 − 9 = 16 arithmetic fails.
  - *Mac-Gray:* "a total of 20 potential bidders, including two strategic bidders (Party A and CSC/Pamplona) and 18 financial bidders (including Party B and Party C)" (p. 32; named NDAs p. 32–34). The clause and the Count rule give 20 − 4 named rows = 16 unnamed financial signers, which matches the settled ruling. The clause works here because this is an entry total.
- **Recommended fix.** Replace the sentence at line 161 ("A named party that may belong … later steps.") with:

  > "For a total of entrants (contacts, confidentiality agreements), a named party the filing includes in the total, or that may belong to it, counts inside it and is not added as another entrant. For a group at a later step (bids received, parties advanced, parties that did not submit), a named party belongs to the group only if the filing places it there or the group's total cannot be reached without it. A named party whose own mentions have ended is not placed in a later unnamed group; its participation closes under E14."

- **Needs Alex?** No. His V¶22 reasoning and the settled Providence ruling already give the answer. The fix is general.
- **Confidence:** High.

## C2. Re-contacted parties double counted in cohort totals

- **Instruction:** E3, line 161: "its Count is the filing's total minus those named rows". Line 161 also says "The cohort row holds the members not recorded by name for that step". E7, line 199: "Record first contacts within each process … a Target interest, Bidder interest or initiating Bid row carries that fact without a duplicate Contact row."
- **Alex:** V¶13 (black): participation_count "double counts some of the strategics that have been later contacted by the target again. This is a problem." V¶121 (black): in sTec "WDC and company H have already been recorded as contacts earlier … and then this information repeats itself." V¶134 and V¶147 (Claude's reading): de-duplicate re-contacts.
- **Type / severity:** AMBIGUOUS, **Medium**. Contact counts feed the entry stage. NDA totals have the same problem where an agreement is "expressly reused" (E7).
- **Where it bites:** The phrase "named rows for that step" does not say whether a party whose first contact sits on an earlier row under another label (Target interest, Bidder interest, an earlier Contact) counts as named for a later outreach.
  - *Mac-Gray:* the 24 June outreach went to "50 parties, including CSC and Pamplona … and Party A" (p. 32). Party A's first contact is the 8 April Target interest row (p. 27). One reading gives the Contact cohort 50 − 2 = 48. The other gives 49 or 50, counting Party A's contact twice.
  - *Providence & Worcester:* "11 potential strategic buyers (including Party A)" were contacted in the week of 28 March. Party A's first contact was in Q4 2015 (Bidder interest). The cohort is 28 under one reading and 29 under the other.
  - *sTec:* "BofA Merrill Lynch had discussions with 18 prospective acquirers". The 18 include WDC and Company A, which have earlier rows. Company A's earlier row may belong to a different process (see the Outside-lane note). WDC has pre-2013 contacts that are probably too vague to get a row under E5.
- **Recommended fix.** Add after "its Count is the filing's total minus those named rows" (line 161):

  > "Also subtract every member that already has a row in this process for the same kind of step (a first contact of any label, or a confidentiality agreement signed or reused), whenever that row is dated. A re-contact or re-sent agreement is not a new entry; the Note gives the total and what was subtracted."

- **Needs Alex?** No.
- **Confidence:** High on the gap. Medium on how often it bites under v0, because E7's "first contacts" wording already points the right way.

## C3. A later reported withdrawal against an earlier non-invitation exit, and the label for non-invitation

- **Instruction:** E14, line 298: "Record reported exits first. Close every other open whole-company participation at the earliest of these events". Rule 1, line 300: "Not invited into a stage when it opens → Dropped by target at the opening, whatever it was told about coming back." Line 298 also says the Exit reason is "the one the filing later reports for that bidder".
- **Alex:**
  - V¶72 (dark red), on Penford's final round opening on 3 October: the target is "also not explicitly excluding other bidders who have previously signed NDAs."
  - CI p.7: "Record 'DropTarget' if target does not invite the bidder to the final round."
  - V¶140 (Claude's reading): target-driven drops are those where "the target ends talks or grants exclusivity".
  - CI p.8: bidders "drop out around the target's announcement of the final round … (Some of these bidders were likely informed by the target that their bid was inadequate and decided to drop out on their own.)"
- **Settled, not reopened:** "Invitees left out of the next stage exit when it opens" (STATUS). Open in STATUS: "Non-invitation versus exclusion." The settled sTec Company H ruling ("dropped by the target by May 16; the reason is 'would not improve earlier offer'") is the same pattern: the exit falls at the stage opening, and the reason comes from what the bidder says later (23 May). The fix below reproduces it. The current "Record reported exits first" would instead turn a later statement of that kind into a later Withdrew.
- **Type / severity:** CONFLICT inside E14 when read against the settled ruling, plus an open label question. **High**, because it changes when a bidder leaves and whose decision it records.
- **Where it bites:** *Penford.* Round 2 opens on 3 October 2014 when the board directs management "to proceed to negotiate and finalize a definitive agreement with Ingredion" (p. 31). Parties A, C and D had signed NDAs.
  - Party D reports on 8 October that it "did not intend to move forward". Because reported exits come first, D gets Withdrew on 8 October and never gets the inferred 3 October Dropped by target. D therefore appears live in round 2, which it was never invited into.
  - Party A has no reported exit. It gets Dropped by target on 3 October (inferred). On 4 October the bank "encouraged Party A to submit a letter of interest", and A bids on 14 October. A therefore needs Re-entered.
  - C has no later mention, so it gets Dropped by target on 3 October.
  - Two parties in the same position (NDA signers not invited to round 2) end up with different exit dates and different deciders only because one of them later spoke.
- **Recommended fix.** Replace "Record reported exits first." (line 298) with:

  > "A reported exit governs only when it comes before every event below that would close the participation. When a bidder is not invited into a stage and later reports that it will not continue, its exit is at the opening (rule 1); the later report sets Exit reason and is quoted in the Note."

  Add to rule 1:

  > "The Note says 'not invited' where the filing reports no exclusion, and 'excluded' where the target tells the bidder it is out."

  Both labels stay Dropped by target, as the settled ruling and CI p.7 require. The Note lets estimation separate the two.
- **Needs Alex?** Yes, on the label only: "When the target opens a stage without a bidder but does not tell it that it is out (Penford 3 October: Parties A, C, D), do you want that recorded as a target drop (your DropTarget) with a Note 'not invited', or as a separate category from an explicit exclusion? The exit date at the stage opening is already settled."
- **Confidence:** High on the internal inconsistency. Medium on what Alex wants for the label.

## C4. NDA dating from the sending of the agreement points the wrong way

- **Instruction:** E7, line 199: "If the filing dates only the sending of the agreement or of information, When is 'by [that date]'."
- **Alex:** CI p.6: "if a confidentiality agreement was sent but not returned or signed, ignore." V¶12 (black): information sent to parties that have already signed must not be read as new NDAs.
- **Type / severity:** CONFLICT (a logic error the CI rule exposes). **Medium.** A wrong upper bound can put an entry before a round opens or before a rival's bid.
- **Where it bites:** Sending an agreement is a lower bound on signing, because signing comes after. Sending information under an agreement is an upper bound, because signing came before.
  - *Penford:* Party A's agreement was forwarded on 9 September and executed on 30 September. Party C's was forwarded on 11 September and executed on 15 September (p. 28–30). Had execution been undated, the rule would give "by 09/09", which is wrong.
  - Party B's agreement was forwarded on 9 September, and on 12 September B declined "to … sign a nondisclosure agreement" (p. 28). The sentence could lead an extractor to create an NDA row for B.
- **Recommended fix.** Replace the sentence at line 199 with:

  > "An agreement the filing reports as sent but not as signed gets no NDA signed row. Where execution is reported but not dated: the date the agreement was sent is a lower bound ('after [date]', Date from); the date information was provided under it is an upper bound ('by [date]', Date to)."

- **Needs Alex?** No.
- **Confidence:** High.

## C5. Activist: recording an activist that does not demand a sale, and the initiation precedence rule

- **Instruction:**
  - D2, line 86: "**Activist**: a shareholder presses the target for a sale."
  - D5, line 129: "**Initiation**, from process 1: activist-influenced if an Activist row precedes round 1; otherwise the earliest of these rows decides".
- **Alex:**
  - V¶119 (black), on sTec: the activist "did not openly try to make the target sell itself, but they did suggest … that selling itself would be one of the options. So I do not think that the sale process here is driven by the activist pressure … But it is still worthwhile to record the presence of an activist who would not be against the sale."
  - CI p.5: "Record … 'Activist Sale' if an activist is pressuring the target to sell itself. Normally this happens before 'Target Sale'."
- **Type / severity:** CONFLICT, **Medium**. It flips a Deal-facts classification used for selection; the ledger rows themselves are unchanged.
- **Where it bites:**
  - *sTec:* in mid-November 2012 the board authorised management to contact financial advisers "including a potential sale of the company". Company A's bank approached on 14 November. Balch Hill's 6 December letter urged the board "to reduce costs … and explore strategic alternatives" (p. 24–25).
    - If that letter earns an Activist row, line 129 makes the deal activist-influenced, even though the target's own sale step came first. The rule ignores order.
    - If the letter does not earn a row (it did not press "for a sale"), the activist Alex wants recorded is lost.
    - Either way the result departs from V¶119. STATUS lists this as raised, not settled.
  - *PetSmart:* the activist pushed for a sale before the board's decision (CI p.5 example). It is activist-influenced under both texts, which is consistent.
  - *Penford:* SEACOR's 13D stated only an intent to nominate directors (p. 24). It gets no Activist row under either reading, which is consistent.
- **Recommended fix.**
  - Replace D2 line 86 with:

    > "**Activist**: a shareholder campaign that presses for a sale or urges a review of strategic alternatives that includes one; the Note says what it urged."

  - Replace the start of line 129 with:

    > "**Initiation**, from process 1: the earliest of these rows decides: Target interest, Target sale decision or a target-opened Round opened row, target-led; Bidder interest or Bid, bidder-led; an Activist row that presses for a sale, activist-influenced (the existing value string). Add 'activist present' when an Activist row precedes round 1 but does not decide."

- **Needs Alex?** Yes: "Should 'activist-influenced' require that the activist pressed for a sale before the target's own first sale step, with a later or softer activist recorded only as present? sTec: board step mid-November 2012, Balch Hill letter 6 December urging a review of alternatives."
- **Confidence:** High on the sTec facts. Medium on the preferred wording.

## C6. Mixed initiation compressed into one value

- **Instruction:** D5, line 129. The earliest row decides a single value, target-led or bidder-led.
- **Alex:** V¶39 (black), on Mac-Gray: "Is this a target- or bidder-initiated deal? I don't know, a bit of both. So it is important to keep track of all these interactions so that we can reinterpret the data various ways". CI p.5: "Record both 'Target Sale' and 'Bidder Sale' in separate lines … if the target decided to sell itself, but a bidder approached it with a bid before the target starts the process."
- **Type / severity:** ADDED, **Medium**. The rows keep the sequence, so the information is still in the ledger. But the Deal-facts field forces a single label, and Alex says he is unsure which one applies.
- **Where it bites:** *Mac-Gray.* The bank called Party A on 8 April 2013 (Target interest). Party A made an unsolicited $17–19 bid on 21 June. The outreach to 50 parties followed on 24 June (p. 27, 31–32). The instruction gives "target-led". Alex's reading is "both".
- **Recommended fix.** Append to line 129:

  > "Where a bidder's Bid comes after a target-side first step but before the target's outreach to two or more parties, write 'target-led, then bidder bid (date)'. The Initiation value always names the first target-side and the first bidder-side row with dates."

- **Needs Alex?** Yes: "When the target sounds out one party and that party then bids before the target's broad outreach (Mac-Gray: 8 April call, 21 June bid, 24 June outreach), should initiation be target-led, bidder-led, or a separate 'both' value?"
- **Confidence:** Medium.

## C7. Mandatory human-review flags in lane C are not implemented

- **Instruction:** F, line 343: "Raise at most five Questions … Applying a default is never a Question." E3, line 159: "Look in the description of the parties and the financing before leaving the winner or any formal bidder Unknown" (search required, but no flag). E3, line 163: a qualified count leaves Count blank with a Note (no flag). E14, line 298: Exit reason defaults to Not stated (no flag).
- **Alex, own closing requirements, all black:**
  - V¶172: "the AI should ALWAYS flag for human review"
  - V¶175: unknown winner type
  - V¶176: unknown type of a formal bidder
  - V¶177: uncertain NDA counts "say 'more than 6' … and their types are 'mixed', without a good split … this must be flagged"
  - V¶178: "Any uncertainty about why a bidder dropped out … has to be flagged"
  - V¶182: "Any time an affiliation of an advisor is unclear, this should be flagged"
  - V¶17, V¶133: dates that need cross-paragraph reasoning should be flagged
  - V¶81: "the AI should very clearly flag all formal bids and all winning bidders who have not received the type."
- **Type / severity:** MISSING, **Medium**. It changes verification, not the recorded object. It still determines whether a wrong exit or count is caught, which V¶50 and V¶141 show happens.
- **Where it bites:** Every deal. Examples: Kraton cohort types (V¶80); sTec "at least" NDA counts (V¶121); every inferred exit with Not stated reason (PetSmart's nine non-IOI signers, V¶60).
- **Recommended fix.** Add a flag list separate from Questions: a Flag column value "R" (amend D1 line 73, which now defines Flag as Question ids only) or a short "Review" section. The five-Question cap in F does not apply to it. Add to Part F:

  > "Mark for review, without a Question and without limit: a winner or Formal bidder of Unknown Type; a qualified or type-unsplit count of confidentiality agreements; an exit row whose Exit reason is Not stated or rests on a later report; an adviser whose client is unclear; a date or order set by combining passages."

  This changes F (lines 343, 351) and needs Austin's approval.
- **Needs Alex?** No. He stated the list. Austin must approve the change to F.
- **Confidence:** High.

## C8. Type splits obtainable by arithmetic across passages

- **Instruction:** E3, line 161: "split by type only where the filing gives the split; an unsplit population of different types is Unknown."
- **Alex:** V¶148 (Claude's reading, endorsed at V¶168): "cohort types are usually pin-downable (STEC: of nine, one financial and eight strategic)." V¶80 (black), on Kraton: combine page 35's typing of Parties H and I with the contact total ("among those 15 contacted, at least 2 are financials").
- **Type / severity:** AMBIGUOUS, **Medium**. Type counts by stage are an estimation input.
- **Where it bites:** *sTec.* The bank had "discussions with 18 prospective acquirers, 17 of which were technology companies and one of which was a financial sponsor … nine prospective acquirers, including the financial sponsor and Company A, indicated they were not interested" (p. 27).
  - The nine therefore split exactly into 1 Financial and 8 Strategic, and Company A is named inside them.
  - "The filing gives the split" may or may not cover a split that needs two sentences and a subtraction.
  - Reading 1 gives a Contact/decline cohort of type Unknown. Reading 2 gives Financial 1 and Strategic 7 unnamed, plus the Company A row.
- **Recommended fix.** Replace "split by type only where the filing gives the split" with:

  > "split by type where the filing states the split or exact arithmetic from the filing's own figures gives it (for example, a total by type less named members of known type); otherwise an unsplit population of different types is Unknown and the Note gives any bound ('at least 2 financial')."

- **Needs Alex?** No.
- **Confidence:** Medium-high.

## C9. Adviser identity when renamed or acquired

- **Instruction:** D2, line 87: "one Adviser row per target financial or legal adviser, when first shown selected or acting".
- **Alex:** V¶29 (black): a bank renamed after acquisition "is a single adviser". V¶138 (Claude's reading): "reconcile renamed banks as a single adviser."
- **Type / severity:** AMBIGUOUS, **Low**.
- **Where it bites:** *Providence & Worcester.* GHF's business was acquired by BMO on 1 August 2016, and the filing says "BMO (which acquired the business of GHF on August 1, 2016)" (p. 30). Reading 1 gives one Adviser row. Reading 2 gives Adviser ended for GHF plus a new Adviser row for BMO.
- **Recommended fix.** Add to D2 Adviser:

  > "A renamed or acquired adviser that continues the same engagement keeps its one row; the Note gives the new name and date."

- **Needs Alex?** No.
- **Confidence:** High.

## C10. Adviser first-row date when the engagement predates the sale

- **Instruction:** D2, line 87: "when first shown selected or acting". E1, line 139: "A target's attempt to buy another company is not its sale process."
- **Alex:** V¶51 (black): record the first mention of the legal adviser (Goodwin Procter, 9 May). CI p.4: legal advisers are "often retained for a long time … there is no need to collect the date but the name". Financial advisers "sign agreements around the start of a deal process".
- **Type / severity:** AMBIGUOUS, **Low**.
- **Where it bites:** *Mac-Gray.* BofA Merrill Lynch was engaged on 23 October 2012 to advise on Mac-Gray's possible acquisition of CSC, and was used again for the sale from 5 April 2013 (p. 27). "Acting" could mean acting in any capacity (Oct 2012) or acting on the sale (Apr 2013).
- **Recommended fix.** Replace "when first shown selected or acting" with:

  > "when first shown selected or acting for the target on its sale or strategic review (an earlier engagement in another capacity goes in the Note)".

- **Needs Alex?** No.
- **Confidence:** Medium.

## C11. Advisers to parties that are neither the target nor a bidder; tax advisers

- **Instruction:** D2, line 87: "one Adviser row per target financial or legal adviser … Bidders' advisers go in the Note of the bidder's first row."
- **Alex:** V¶73 (black): the Penford legal advisers to the winner and to "a large target shareholder, SEACOR" should be recorded "whom they are legal advisers to". V¶98 (blue): Meredith's tax adviser (Deloitte) may shape deal structure.
- **Type / severity:** MISSING, **Low**.
- **Where it bites:**
  - *Penford:* Milbank, counsel to SEACOR, which signed the voting agreement (p. 31). SEACOR is neither target nor bidder, so no place records its adviser.
  - *Meredith:* the tax adviser has no row.
- **Recommended fix.** Add to D2 Adviser:

  > "A target tax adviser gets an Adviser row. An adviser to a shareholder that signs a support or voting agreement goes in the Note of the row recording that agreement or of Merger agreement signed, naming the client."

- **Needs Alex?** No.
- **Confidence:** High on the gap, low on its importance.

## C12. Date bounds from logical links, not only textual placement

- **Instruction:** E8, line 215: "An undated event placed between two dated events is bounded by them. A due date does not show arrival by that date."
- **Alex:**
  - V¶17 (black): Providence LOIs in "late July", with a 20 July deadline, a bid on 21 July and a committee meeting on 22 July. "This very narrowly limits the timing of round two bids to July 20 to July 22."
  - V¶55 (black): "first week of October" plus a 3 October meeting after which contacts start gives 3–7 October.
  - V¶180: "the order of events must be precise".
- **Type / severity:** AMBIGUOUS, **Low**. The bounds mostly affect Date to and the order relative to other late events such as Party C's steps.
- **Where it bites:** *Providence & Worcester.* The committee met on 22 July "to review the LOIs" (p. 30), which bounds the undated LOIs to "by 07/22". "Placed between" (textual position) may or may not cover this.
- **Recommended fix.** Replace the sentence at line 215 with:

  > "Bound an undated event by any dated event the filing links to it: a step that acts on it (a review, a response, a meeting that considers it) bounds it from above; a step it answers or follows bounds it from below; an undated event placed between two dated events is bounded by them."

- **Needs Alex?** No.
- **Confidence:** Medium.

## C13. Sort date for a range

- **Instruction:** E8, line 217: "Sort date: the reported day; otherwise the due date … otherwise Date from".
- **Alex:** CI p.3: "'in mid-February 20XX' … a rough date would be 2/15/20XX". V¶10 (black): date_assigned "interpolated incorrectly".
- **Type / severity:** ADDED, **Low**. Date from and Date to keep the whole interval, and Alex cares about order (V¶180), not the point date. The instruction is consistent with his intent as long as order is right.
- **Where it bites:** Any "mid-/late month" event without a due date. PetSmart and Providence each have several.
- **Recommended fix.** Add to E8: "Sort date is for ordering only; estimation uses Date from and Date to."
- **Needs Alex?** No.
- **Confidence:** High.

## C14. Order of an exit row and the next stage's opening row on the same date

- **Instruction:** E8, line 217: "A **Round opened** row is the first row of its round in the ledger." E6, line 191: "an exit row carries the round being left." Nothing orders an inferred exit (Sort date = the opening date, line 298) against the Round opened row that causes it.
- **Alex:** CI p.8: the final round announcement "should precede information in the Bidder Dropouts section above, in which the target decides to drop some of the bidders ('DropTarget')".
- **Type / severity:** AMBIGUOUS, **Low**.
- **Where it bites:** Every rule-1 exit. Examples: Kraton on 6 July (six NDA signers not continued); Penford on 3 October; Providence on 1 June.
- **Recommended fix.** Add to E8:

  > "On one Sort date, a Round opened row comes before the exits it causes."

- **Needs Alex?** No.
- **Confidence:** Medium.

## C15. Bidder names that change within a filing

- **Instruction:** E3, line 155: "Use the filing's names … An unnamed participant the filing lets you follow individually gets a descriptive name".
- **Alex:** CI p.6: unnamed signers are "a1, a2 … If later they get named update the name accordingly". CI p.7: "Name of bidder as recorded when they signed the NDA".
- **Type / severity:** MISSING, **Low**. Counts and exit checks group rows by Who, so one party under two names looks like two bidder units.
- **Where it bites:** Any filing that introduces a party anonymously and names it later, or labels a winner "Parent" in one place and by its name in another.
- **Recommended fix.** Add to E3 after the naming sentence:

  > "Keep one Who string per bidder unit on every row. Where the filing later names or renames a party, use the later name throughout and give the earlier one in the Note of its first row."

- **Needs Alex?** No.
- **Confidence:** Medium.

## C16. Public/private and non-US status of bidders

- **Instruction:** E3 Type, line 159: Strategic, Financial, Mixed or Unknown only.
- **Alex:** CI p.7: "also record status as public vs private and non-US if information is available … 'non-US public S'." The voice notes never repeat this request.
- **Type / severity:** MISSING, **Low**.
- **Where it bites:** Any deal with a foreign or private bidder the filing identifies.
- **Recommended fix.** If Alex still wants it, add:

  > "The Note of a bidder's first row gives 'public', 'private' and 'non-US' where the filing states them."

- **Needs Alex?** Yes: "Your March instructions ask for public/private and non-US status next to S/F. Do you still want that recorded?"
- **Confidence:** High on the gap, low on current importance.

## C17. Does the outreach that opens round 1 get Contact rows?

- **Instruction:** D2, line 88: "**Contact**: a first contact after round 1 opens (E7)." E6, line 191: round 1 "opens at the target's first outreach to two or more prospective buyers". E7, line 199: only "a Target interest, Bidder interest or initiating Bid row carries that fact without a duplicate Contact row".
- **Alex:** V¶40 (black), on Mac-Gray: "on June 24, 35 financials and 15 strategics has have been contacted by the target … but the event itself is not recorded."
- **Type / severity:** AMBIGUOUS, **Low**. The contacts made at the opening fall exactly on the boundary: "after round 1 opens" may or may not include the opening outreach, and Round opened is not listed as a row that carries first contacts.
- **Where it bites:** Every target-run auction. Examples: Mac-Gray on 24 June (50 parties); Providence in the week of 28 March (29 parties); Kraton in May–June (14 parties).
- **Recommended fix.** Replace D2 line 88 with:

  > "**Contact**: a first contact made at or after the opening of round 1, including the outreach that opens it (E7)."

- **Needs Alex?** No.
- **Confidence:** Medium.

---

## Checked and consistent

- **Contact and NDA are separate rows; NDA only when executed; no contacts after NDA** (V¶11, V¶12, V¶14; E7). Consistent.
- **Counts are constructed, not extracted** (V¶13, V¶134; E14 line 308 "Count is not summed across rows"). Consistent.
- **Exact totals rather than "at least"** (V¶56, V¶80, V¶121; E3 line 163 keeps the filing's precision). Consistent when the filing is exact.
- **Contacted parties that decline, or are never contacted, get no exit** (V¶70, V¶140). E3 entry (line 157) requires an NDA, a Bid or admission. Checked in Penford: SEACOR, Party B (declined the NDA 12 September) and Party E (no response) have no entry. Party G was never contacted. None gets an exit.
- **Mac-Gray NDA reconciliation** (V¶41, V¶45). Checked against p. 32–34. The E3 Count rule with named rows for B (28 June), C (30 June), CSC/Pamplona (11 July) and A (5 August) gives 16 unnamed financial signers, which matches the settled ruling. The risk that remains is C1's wording, not the arithmetic.
- **Providence Party A** (V¶21–24). E14 rule 3 closes A at the round-1 due date, which matches the settled ruling, provided C1 is fixed.
- **Target versus bidder-driven exits; exit reason vocabulary** (V¶83, V¶140; CI p.7–8). E14 labels and Exit reasons cover DropBelowM, DropBelowInf, DropAtInf and DropTarget. "Value at or below market price", "Would not improve earlier offer" and "Not selected at signing" are ADDED and fit Alex's intent (V¶76).
- **Exclusivity with a rival drops the others** (V¶50, V¶76; E14 rule 2). Mac-Gray: the filing shows C not submitting on 18 September (p. 36), while A and B submitted and were closed by the 24 September exclusivity (p. 37). V¶50 names "party B and party C" as the two dropped. That looks like a slip for A and B. The instruction gives A and B Dropped by target on 24 September and C Did not submit on 18 September. Low confidence; confirm with Alex: "In Mac-Gray, were the two bidders dropped on 24 September Parties A and B, with C not submitting on 18 September?"
- **PetSmart non-IOI signers, reason unknown; IOI bidders eliminated by the target** (V¶60). E14 rules 1 and 4. Consistent.
- **Rollover and board seat are not a consortium** (V¶64, V¶120; E4). Consistent.
- **Bidder interest without a bid; a price reference is not a bid** (V¶68; D2 line 84, E10 line 247). Consistent.
- **Target interest as the first move** (V¶38; D2 line 83). Consistent.
- **Re-entry keeps the earlier exit** (CI p.7; E14 line 306). Consistent.
- **Winner type from elsewhere in the filing** (V¶69, V¶81, V¶112; E3 line 159 and Part C step 1). The search is required. Only the flag is missing (C7).
- **Quarter and "week of" windows** (V¶9; E8). Consistent.
- **Same-day bids by one bidder in text order** (V¶59; E8 "# follows the filing's order"). Consistent.
- **Unaccounted bidder deduced by arithmetic** (V¶57, magenta; E3 "exact arithmetic", descriptive names). Consistent.
- **Auction screen by NDA count, excluding advisers and stale processes** (CI p.4; E1 line 145, E5). Consistent.

## Outside my lane (brief)

- **Kraton rounds** (STATUS ruling of 27 September) and the E6 rule that "a selection that asks for no offers opens no round". This is a known conflict and already in STATUS.
- **Penford Party A's 4 and 13 October valuation statements against its 14 October $16 bid** (E10 "Valuation remarks"). This is an open STATUS item. Any exit or re-entry for Party A in C3 depends on whether 4 October counts as a Bid.
- **sTec processes.** Company A's 14 November 2012 approach and the April 2013 contacts fall on either side of the gap Alex treats as a process break (V¶118). Whether Company A "enters afresh" in process 2 changes the C2 subtraction. That is lane A.
- **Mandatory flags for rounds and processes** (V¶173–174, V¶110). This is the same missing mechanism as C7, outside my lane.
