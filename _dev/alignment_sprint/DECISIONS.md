# Alignment sprint: decision log

Started 27 September 2026. Austin and Claude go through every difference between the v0 instruction and Alex's conventions, one theme at a time, and record Austin's decision here as it is made. This file is the record; the chat is not.

Evidence is in `evidence/`: four Opus 5.5 lane audits (`lane_A–D.md`), the merged list of 41 themes (`merged.md`), the GPT-6 Astra review (`astra_review.md`), Claude's reconciliation (`ADOPT_NEXT.md`), and numbered text of Alex's voice notes and collection instructions.

A decision is one of:
- **Adopt**: the approved wording goes into the next general amendment.
- **Adopt, confirm with Alex**: goes in provisionally; the linked question goes to Alex.
- **Ask Alex**: no change until he answers; the question is recorded.
- **Defer**: tooling or estimation, not the instruction.
- **Reject**: no change.

Nothing here changes the instruction by itself. When the sprint ends, the adopted wording becomes one general amendment with a decision-to-clause map, the checker changes that go with it, and a mechanical check. Austin approves that amendment separately. No extraction runs without his command.

## Working rule (from 2026-09-27)

Where Alex has spoken, adopt his view. His later voice notes override his earlier collection instructions and hand-coded workbook; where the voice notes are silent, the collection instructions and workbook give his view; the filing governs facts (Austin, 27 Sep evening). Where he is silent in all three, use the simplest wording. Where he contradicts the filing or himself, Austin judges on his behalf or asks him. **Austin's earlier rulings are overturned where they contradict Alex** (Austin, 2026-09-27). Checked: only the same-offer rule contradicted Alex (V¶30), and F2 overturns it; the other settled rulings agree with Alex (V¶22, V¶41, V¶45, V¶95–97, V¶184, CI p.7) or he is silent on them. That check covered STATUS's settled list only. The VM's 25–26 September rulings (V114_SPEC, V1141_SPEC, root HANDOFF, on branch `vm-live-2026-09-26`) are also overturned where these decisions differ; `vm_check/lane_C_decisions.md` lists them (C1–C18). Austin's attention goes to what the research depends on: round counts, who is live at each stage, and formal versus informal bids. After the amendment, re-extract the nine deals (on Austin's command) and compare with Alex's hand coding; let disagreements show which details matter.

## Order of work

1. **Round map:** R1, R2, R3, R6, R7, R9, R5. After these, check the resulting round map on all nine deals.
2. **Exits and participants:** P3, P1, P2, P4, P6, P8, P9, P10, P11, P7.
3. **Bids and conditions:** F6, F9, F10, F11, F12, F7, F4, F5, F1, F2, F3, F8.
4. **Output and review:** O3, O4, O8, O9, O6, O1, O7, O5, O2.
5. **Conventions for Alex:** R4, R8, P5, and the final questionnaire.
6. **Amendment:** draft text, decision-to-clause map, checker changes, mechanical check.

## Decisions

| Theme | Title | Proposed | Decision | Date | Notes |
|---|---|---|---|---|---|
| R1 | Request to some but not all eligible parties opens a round | Adopt | **Adopt** | 2026-09-27 | As drafted |
| R2 | Round opens at the decision on who advances | Adopt | **Adopt** | 2026-09-27 | As drafted; Datalink awaited parties to Alex (Q2) |
| R3 | Trigger (d): pause or lapsed exclusivity | Adopt guard; rest to Alex | **Adopt guard; keep v0 triggers (Austin for Alex)** | 2026-09-27 | Restart after exclusivity lapses is a new round |
| R4 | Finality: label or substance; informal final round | Ask Alex | **Adopt (Austin for Alex): substance over label; bids in negotiation Formal** | 2026-09-27 | Off the Alex list |
| R5 | When round 1 starts | Adopt, confirm with Alex | **Adopt (Alex V¶71, V¶173); plus V¶55 meeting rule (PetSmart Oct 3)** | 2026-09-27 | Decision 1 batch; Q8 decided |
| R6 | Rounds only for the whole company | Adopt | **Adopt** | 2026-09-27 | Applies the settled partial rule (E1) to round rules; not a reopening |
| R7 | Round dating and ordering details | Adopt | **Adopt (Alex's view)** | 2026-09-27 | (a) V¶25, (c) CI p.8; (b) Alex silent, simplest option; round-1 dating moved to R5 |
| R8 | Process gap measurement | Ask Alex | **Adopt (Austin for Alex): measure from last dated contact** | 2026-09-27 | sTec 2 processes (V¶118) |
| R9 | "Enforced" means decisive action | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| F1 | When documents make a bid Formal | Ask Alex | **Adopt (Austin for Alex): markup must come with the bid** | 2026-09-27 | Reproduces V¶74 |
| F2 | Late markup without a price | Ask Alex | **Adopt (Austin for Alex): confirmation by documents copies the latest price** | 2026-09-27 | Amends the settled same-offer rule; accepts Penford Oct 8 |
| F3 | Price-only revision after a Formal bid | Ask Alex | **Adopt (Austin for Alex): Formality persists while markup on table** | 2026-09-27 | |
| F4 | Diligence bundled with exclusivity is Heavy | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| F5 | "None stated" against Unclear | Ask Alex | **Adopt (Austin for Alex): silence is None for Formal bids; required exclusivity at least Light** | 2026-09-27 | V¶125, V¶183, V¶19, V¶49 |
| F6 | "No firm commitment" means Contingent | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| F7 | Legal bargaining against conditions on proceeding | Adopt | **Adopt (Alex silent; simplest)** | 2026-09-27 | Decision 1 batch |
| F8 | Regulatory risk and Heavy | Defer | **Defer** | 2026-09-27 | Decision 1 batch |
| F9 | Commitment letter alone is not Formal | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| F10 | Contingent payment with no stated date | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| F11 | Later "indication" label | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| F12 | Target's preference between alternatives | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| P1 | Named party inside an unnamed group | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| P2 | Re-contacted parties double counted | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| P3 | Inferred stage-opening exit against later withdrawal | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| P4 | NDA dating and memoranda | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| P5 | Activist and initiation | Ask Alex | **Adopt (Austin for Alex): record activists broadly; influence only if a sale demand comes first; 'mixed' initiation** | 2026-09-27 | V¶119, V¶39, CI p.5 |
| P6 | Type split by exact arithmetic | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| P7 | Advisers | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| P8 | Date bounds from linked events | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| P9 | Bidder names that change | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| P10 | Public/private and non-US status | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| P11 | Contact rows for the opening outreach | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| O1 | Mandatory review items | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| O2 | Real-time review | Ask Alex | **Defer (Austin): work through the cockpit for now** | 2026-09-27 | No instruction change |
| O3 | Count and Who on signing and announcements | Adopt | **Adopt (Austin's request)** | 2026-09-27 | Decision 1 batch |
| O4 | Signed acquirer's post-signing revisions | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| O5 | Price normalization inputs | Defer | **Defer** | 2026-09-27 | Decision 1 batch |
| O6 | Pointers to other pages | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| O7 | Filing link | Defer | **Defer** | 2026-09-27 | Decision 1 batch |
| O8 | Go-shop definition | Adopt | **Adopt** | 2026-09-27 | Decision 1 batch |
| O9 | Rounds counts against the ledger | Adopt | **Adopt (Alex silent; simplest)** | 2026-09-27 | Decision 1 batch |

## Questions for Alex (built up as decisions are made)

None open. Every item was decided by Austin on Alex's behalf or resolved from Alex's notes.

Decided by Austin for Alex (off the list): finality (R4); process gap (R8); conditions (F5); initiation and activists (P5); PetSmart round-1 date (Q8, Alex's Oct 3); real-time review deferred to the cockpit (O2); negotiation-stage formality; F1–F3; Datalink parties "still considering" (dropped under the settled rule, CI p.7; Re-entered if they return); restart after exclusivity lapses is a new round (R3).

Resolved from Alex's own notes: Kraton Party J on July 6 is dropped (V¶82: "out of 10 NDA agreements, only 4 bidders ... will continue"), Re-entered at its July 19 bid, dropped again on July 20. *Superseded by ruling 1 of 28 September: J Did not submit June 29, Re-entered by July 19 (its indication is dated only “By July 19, 2021”, p.36), dropped July 20.*

Possible slip in Alex's notes (filing fact, not a convention): V¶50 names Mac-Gray Parties B and C as dropped on Sep 24; the filing shows C did not submit on Sep 18 and A and B were dropped at CSC/Pamplona's exclusivity on Sep 24. Follow the filing.

## Decision records

Each decided theme gets a short record here: the approved wording, the deals it changes, and anything Austin added.

### R1 (adopted 2026-09-27)

Replaces E6 (a), l.182:

> (a) after the due date of the current round's offers, or after receiving them, sends a common request for new offers to some but not all of the parties eligible in that round. Eligible parties entered the process and could bid in the round, including those whose only exit is an inferred Did not submit; a party whose withdrawal or exclusion was reported before the request is not eligible. Price feedback or a request to one bidder is not a common request. The request need not set a deadline. Within a round announced as final, further requests to the remaining bidders continue that round.

Sources: V¶82, V¶173; Kraton filing p.35. Effects: Kraton July 6 opens round 2 (ruling met); PetSmart Dec 10 continues the final round (V¶61); Providence mid-June and Mac-Gray Aug 27 open nothing; sTec May 16 opens round 2. Accepted consequence: outside final rounds, an improvement request that leaves out NDA signers who never bid opens a round.

### R2 (adopted 2026-09-27)

Replaces the E6 l.187 sentence "A selection that asks for no offers opens no round; the round opens at the request that follows ((a) or (b))":

> A documented target decision admitting named parties to a next stage (further diligence, management meetings, a later request for offers) opens that stage at the decision, if the stage is carried out. Later access, letters and due dates that carry out that stage do not open it again. A later request that leaves out some of the admitted parties is tested under (a) on its own. If no request for offers follows and the target negotiates definitively with the admitted parties, (c) applies at the decision.

Sources: V¶44, V¶173; Mac-Gray p.33, Kraton p.36, PetSmart Nov 3, Datalink p.29. Effects: Mac-Gray round 2 July 25 (was Aug 27); Kraton round 3 July 20 (was Aug 11), I and J dropped July 20; PetSmart final round Nov 3; Providence round 2 by June 1 (was mid-June); Datalink 3 rounds (was 2).

### R3 (adopted in part 2026-09-27)

Adds to the end of E6 (d), l.185:

> Carrying out a stage already opened is not asking again.

The 30-day pause and end-of-exclusivity triggers stay as in v0 until Alex answers Q2. Effect: Mac-Gray stays at 3 rounds (the Aug 27 letter carries out the July 25 stage). Datalink Oct 1 and Synacor Dec 30 remain new rounds under v0, pending Alex. Alex's V¶109 (Synacor, same process after exclusivity lapse) concerns processes, not rounds. *Superseded by evening ruling 1 (27 September): Synacor's reopened round opens Oct 27, 2020, and Dec 30 continues it.*

### R6 (adopted 2026-09-27)

Applies the settled whole-company rule (E1: partials don't count) to the round and sale-decision rules, which v0 left unrestricted. Not a reopening of the partial ruling.

- E6 l.179: "... asks a set of bidders for offers for the whole company (E1) on common terms."
- E6 l.191: "Round 1 opens at the target's first outreach to two or more prospective buyers of the whole company ..."
- D2 l.85: "Target sale decision: the board decides to explore or pursue a sale of the whole company; keep its qualifications."
- Add to E6: "A partial-sale solicitation opens no whole-company round. Preserve its material procedural facts with the relevant Other-scope rows and in the Account."

Sources: V¶96, CI p.7; Kraton p.32 (late 2020 CST-segment talks would otherwise open round 1 and give four rounds).

### R7 (adopted 2026-09-27, following Alex)

- (a) Unreported round opening (V¶25): E6 l.187 becomes "the Round opened row is Inferred = Y, When 'by [first offer]', Date from the last event of the previous round, Date to and Sort date the first offer (an exception to E8's 'by [day]: Date to only')."
- (b) Late answer (Alex silent; simplest option): add to E6 l.191 "A response to an earlier round's solicitation that arrives after the next round has opened carries the round open when it arrives. The Note says which solicitation it answers." Kraton J July 19 = round 2.
- (c) Same-day order (CI p.8): add to E8 "On the day a round opens, the Round opened row comes before the exits it causes; those exits keep the round being left."
- Round-1 dating when the outreach is undated moves to R5.

### Decision 1 batch (adopted 2026-09-27)

Adopted as one batch under the working rule. Wording to carry into the amendment:

- **R5** (V¶71, V¶173). Replace the "where buyers came to the target …" clause of E6 l.191: "Round 1 opens when the target or its banker first contacts two or more prospective buyers of the whole company, dated at the board decision that launched it if the outreach followed within a week or is undated but reported as following it. Where the target never contacts buyers beyond a party that approached it or one it sounded out, round 1 opens at the first NDA or price negotiation the target holds with a whole-company bidder." Penford's Aug 10 $18 becomes round 0. PetSmart's Oct 3 anchor (V¶55) rests on a premise the filing contradicts: Q8.
- **R9** (V¶122–124). E9 items 3–4: "Enforced: after the date, and on the bids in hand, the target selected or excluded bidders, opened the next stage, or chose a bidder for negotiation or exclusivity. Passed without action: bidding continued with no such decision; board review or price feedback alone falls here." D3 How it ended: "For Extended (late bid accepted), give the date of the last late response accepted." Outcome values stay the fixed list.
- **F4** (V¶19). H2: "the filing ties a period of two weeks or more to remaining diligence, alone or together with negotiation or exclusivity, and does not call that diligence confirmatory. Exclusivity or negotiation alone is not a diligence requirement." Example 4 ends "Conditions Heavy; Note 'H2: 45 days' exclusivity for diligence and negotiation'."
- **F6** (V¶47). Financing: "Where the filing says the bid lacks a firm or committed financing arrangement, Financing is Contingent, whatever sources it names."
- **F9** (V¶47). Route 1 drops "a commitment letter": "... a markup or its own draft of the merger agreement or of a voting agreement. A financing commitment letter alone does not make a bid Formal."
- **F10** (V¶84). E13 replaces "A price that depends on criteria is a CVR/earnout only if the extra amount is paid after closing; otherwise it is a range" with: "A separately identified contingent extra payment is a CVR/earnout, recorded apart from the stated upfront price, including when its payment date is unstated. An expressly upfront price adjustment or alternative upfront price is a range. Do not discard a stated base price because the contingent amount is unquantified."
- **F11** (V¶68). E10 Valuation remarks adds: "A retrospective label alone does not turn interest or a market-price reference into a proposal; judge from the passages that report the communication's terms and quote any later label in the Note."
- **F12** (V¶102). E10 adds: "Where the filing reports the target's preference between alternatives, the Note of each alternative row says so."
- **F7** (Alex silent). E10 Conditions on proceeding: "... is a Bid row coded H3 (E12), with the price blank unless restated, wherever the statement appears, including in draft negotiations. Routine drafting and bargaining over legal terms do not alone create a Bid row. An adviser's prediction of what bidders will require is not a bidder's statement." sTec June 20 stays H3 and becomes a Review item. *Superseded in part: the Review item lapsed, since no Review-item category covers this row and none was added for one deal (BUILD_REVIEW M1); the row stays one H3 Bid with no price.*
- **P1** (V¶21–24; settled Providence 16). E3 l.161 replaces "A named party that may belong to the group stays inside it …" with: "For a total of entrants (contacts, confidentiality agreements), a named party the filing includes in the total, or that may belong to it, counts inside it and is not added as another entrant. For a group at a later step (bids received, parties advanced, parties that did not submit), a named party belongs to it only if the filing places it there or exact reported identities and totals uniquely require it. Later silence is not evidence of membership; a named party whose mentions have ended closes under E14."
- **P2** (V¶13, V¶121). E3 adds: "Subtract a previously recorded party from a cohort only where the filing establishes, or exact reconciliation requires, its inclusion in this aggregate; a re-contact or re-sent agreement is not a new entry. The Note gives the total and what was subtracted."
- **P3** (settled sTec Company H). E14 replaces "Record reported exits first." with: "Close each participation at the earliest supported closing event, reported or inferred. Where a bidder not invited into a stage later reports that it will not continue, its exit is at the opening (rule 1); the later report sets Exit reason and is quoted in the Note, with no second exit." Rule 1 adds: "The Note says 'not invited' where the filing reports no exclusion, and 'excluded' where the target tells the bidder it is out."
- **P4** (V¶12, CI p.6). E7 replaces "If the filing dates only the sending of the agreement or of information, When is 'by [that date]'" with: "An agreement reported as sent but not as signed gets no NDA signed row. Where execution is reported but not dated, the sending date is a lower bound (signing on or after it); information sent under the agreement is an upper bound only where the filing shows signing came first. Sending a memorandum or opening a data room never creates an NDA signed row."
- **P6** (V¶80, V¶148). E3: "split by type where the filing states the split or exact arithmetic from the filing's figures gives it; otherwise an unsplit population of different types is Unknown, and the Note gives any bound ('at least 2 financial')."
- **P7** (V¶29, V¶51, V¶73). D2 Adviser: dated when first shown acting for the target on its sale or strategic review (an earlier engagement goes in the Note); a renamed or acquired bank continuing the engagement stays one adviser (both names in the Note, no Adviser ended); a shareholder's adviser goes in the Note of that shareholder's agreement row, naming the client; an unclear client is a Review item. No compulsory tax-adviser rows.
- **P8** (V¶17, V¶55, V¶180). E8 l.215: "Bound an undated event by any dated event the filing links to it: a step that acts on it bounds it from above; a step it answers or follows bounds it from below; an undated event placed between two dated events is bounded by them. Sort date is for ordering only."
- **P9** (CI p.6). E3: "Keep one Who string per bidder unit. Where the filing later names or renames a party it shows to be the same unit, use the later name throughout and give the earlier one in the Note of its first row. A change in the unit itself follows E4."
- **P10** (CI p.7). E3 Type: "On a bidder's first row, the Note says 'public', 'private' or 'non-US' where the filing states it."
- **P11** (V¶40). D2: "Contact: a first contact made at or after the opening of round 1, including the outreach that opens it (E7)."
- **O1** (V¶169–187). Part F adds uncapped Review items R1, R2 … on the Questions sheet, separate from the five Questions: a possible process or round boundary even where the count was kept; a target meeting at or soon after a due date; a selection, renewed approach or unstated opening that may mark a new round; a Formal bid the filing calls an indication, LOI or non-binding; an adviser with an unclear client; a date, count or identity resting on passages on different pages. Each gives pages, the coding chosen and rows affected, or names a source event the ledger omits; R ids go in Flag. F l.343 becomes "Applying a default is never a Question; it may be a Review item." Tooling: a script builds the rest of the queue from the ledger (Unknown types, qualified counts, inferred or unexplained exits, deadline outcomes, partial-only deals, price basis); checker accepts R ids; Austin switches categories off as Alex allows (V¶187). No seven-day cutoff.
- **O3** (Austin's request). D1 col 20: Count filled on bidder rows; Merger agreement signed: Who is the signing acquirer, Count 1 when it is a whole-company bidder, else blank; required on Process terminated, Process restarted, Bidding group changed; blank on Target sale decision, Activist, Adviser, Adviser ended, Round opened, deadline rows, Go-shop changed and the three announcement rows. D2: Who on Sale process announced and Merger announced is the target; on Bid announced, the bidder. Checker updated to match.
- **O4** (V¶104). E2 last sentence: after signing, record the merger announcement; proposals from others and their process events; each change the signed acquirer offers or agrees to in price, consideration or commitments, including a return to an earlier offer; an amendment changing them; go-shop activity; termination. C step 4 adds a check of the last agreed price against the merger-agreement summary and fairness opinion.
- **O6** (V¶17, V¶170). Part B adds: "Where a row's date, count or bidder identity also rests on a passage on another page, end the Note with 'Also p. N'."
- **O8** (V¶113). E6 adds: "A go-shop is a period after signing in which the merger agreement lets the target solicit competing proposals. Open a round only where the filing reports solicitation under that clause; a clause with no reported solicitation goes in the Note of Merger agreement signed."
- **O9** (V¶13). D3: "Who was in reconciles to admissions to that stage; Bids received to distinct whole-company bidder units in it. Where the ledger and these columns differ, correct whichever misstates the filing, or explain a supported difference in How it ended."
- **Deferred:** O5 (price normalization inputs, market prices at estimation; never join on Sort date), O7 (filing link written by the runner), F8 (regulatory risk and Heavy).

### R4 finality (adopted 2026-09-27, Austin judging for Alex)

Austin: "in the negotiation both parties will spam the word final to make they sound hard to get." Off the Alex questionnaire.

E6 l.195 Finality, and the same test in E6 (b) and E11 route 2:

> **Announced as final**: the target told bidders this was the final, binding or best-and-final stage, or that the next step is signing or exclusive negotiation with one of them. A request the filing describes as for non-binding proposals is not final, whatever it is called; the Note records the label.

Effects: sTec May 16 opens round 2 (Not final), May 29 "best and final" opens round 3 (final): 3 rounds (was 2), matching V¶124–125; WDC May 28 stays Formal by its markup (V¶125). Mac-Gray Sep 11 "final indications" with exclusivity next is final (V¶48). Kraton, Datalink, PetSmart final letters unchanged.

### R4 negotiation-stage formality (adopted 2026-09-27, Austin judging for Alex)

E11 route 3 becomes:

> (3) it is made after the target has begun definitive negotiation with that bidder, including a Bid reaffirmed (E10). A bidder that withdrew and returns starts again: its first bid after re-entry is Formal only by another route.

Source: V¶27 ("only formal bids … are allowed or seriously considered by the target at this stage"). Extends v0's route 3 from reaffirmations to revisions. Almost no change in the nine deals (Providence Aug 12 G&W $25 and Penford Oct 14 Ingredion were already Formal; Penford Party A Oct 14 and sTec WDC Jun 10 stay Informal); matters for phoned-in final price bumps in new deals.

### F1 and F3 (adopted 2026-09-27, Austin judging for Alex)

- **F1.** E11 route 1: "(1) the bid comes with a markup or the bidder's own draft of the merger agreement or a voting agreement: submitted in the same communication as the priced proposal, or in the bidder's response to a target request for both price and documents. Documents exchanged at another time do not make an earlier or later bid Formal." Part B adds: "Formality is judged at the bid's communication; the window applies to the condition columns." Effect: Penford Ingredion's Aug 10, Sep 17 and Oct 2 bids stay Informal despite the Sep 6 buyer draft (V¶71, V¶74).
- **F3.** E11 adds: "A revision that changes only price, consideration or conditions keeps route 1 while the bidder's markup or draft is still on the table (the filing reports no withdrawal or replacement of it)." Replaces "A later revision, including one that changes only the price, is Formal only if it meets a route itself." Effect: Providence G&W Jul 26 $22.15 stays Formal.

### F2 (adopted 2026-09-27, Austin judging for Alex)

Austin chose Alex's reading (V¶30) knowing that it amends the settled same-offer rule ("copy an offer only when the bidder says it stands") and adds Penford Oct 8, against V¶74. **STATUS.md's settled ruling must be updated when the amendment is approved.**

E10 adds, after Same offer:

> **Confirmation by documents.** After the target has begun definitive negotiation with a bidder, a revised markup or draft of the merger agreement that the bidder itself submits, with no new price, is a Bid reaffirmed row for that bidder's latest offer ("Same as #n"), copying its price. Code the condition columns from what the filing reports at that time. Record one such row per bidder at its first such submission, and another only if the filing reports a changed term with a later one. Drafts sent by the target never earn a row.

E10 Same offer begins "When a bidder says its earlier offer stands (…), or confirms it by documents (below), copy that bid row …". E2 "successive drafts" becomes "successive drafts, except a bidder's confirmation by documents (E10)".

Effects: Providence Aug 4 Party B, Bid reaffirmed at $24, Formal, conditions as the filing shows (on-site diligence to Aug 11, so not None). Penford Oct 8 Ingredion, Bid reaffirmed at $19, Formal (Alex dates Ingredion's formal offer Oct 14, V¶74); the Oct 14 phone confirmation is a second reaffirmation. Expect most deals' eventual winners to gain one such row at their first revised draft after negotiation began.

### Stage questions (decided 2026-09-27, Austin judging for Alex)

- **Parties the filing says remained in the process.** Austin: "if they didn't submit a new bid by the deadline, even if the filing said they were still considering, I will treat them as dropped. If they ever turn up later, they get a re-entry. A deadline becomes a joke if we allow them in." No exception to the settled rule (consistent with CI p.7). Datalink's two admitted parties not sent the Aug 16 final letters are Dropped by target at the Aug 16 opening; a later return would be Re-entered.
- **Restart after exclusivity lapses.** A new round; E6 (d) stays as in v0 plus the R3 guard. Datalink: 4 rounds (Oct 1). Synacor: the reopened round opens Oct 27, 2020, not Dec 30 (corrected in the evening rulings below).

### R8 (adopted 2026-09-27, Austin judging for Alex)

E5 (b) adds:

> Measure the gap from the last dated sale contact. Undated follow-ups to that contact, and messages that only end or cancel talks, do not restart the clock. Talks in which the target is buying another company, or merger-of-equals talks outside the contest (E1), are not sale contacts.

The 90-day threshold stays. Effects: sTec Nov 14, 2012 (Company A's bank) to Feb 13, 2013 (Company B) is 91 days, so 2 processes (V¶118). Synacor's Company D talks (target buying D) do not bridge Oct 2019 to Jul 2020, so the processes stay separate (V¶108).

### F5 (adopted 2026-09-27, Austin judging for Alex)

- **Silence.** E12 None adds: "or, for a Formal bid, the filing reports no remaining diligence, financing condition or regulatory concern for it." Informal bids with silence stay Unclear. sTec WDC May 28 (markup, nothing said) becomes None, as Alex reads it (V¶125, V¶183).
- **Exclusivity.** E12 Light adds "or Exclusivity is Required"; None requires Exclusivity not Required. A.3 (l.16) and E12 (l.277) change to: exclusivity never makes a bid Heavy or changes Formality, but a required exclusivity makes it at least Light. Follows V¶19 (exclusivity is a condition) without breaking V¶49 (it must not downgrade a Formal bid).

### P5 (adopted 2026-09-27, Austin judging for Alex)

- D2 Activist: "a shareholder urges the target to sell itself or to explore strategic alternatives. The Note begins 'Demands sale' or 'Sale one option' and quotes the demand."
- D5 Initiation: "activist-influenced only if an Activist row whose Note begins 'Demands sale' precedes the target's first sale step (Target interest, Target sale decision or a target-opened round)"; adds "mixed, where both a target-side first step (Target interest or Target sale decision) and a bidder's own Bid precede round 1; the Note names both with dates."
- Effects: sTec gets a Balch Hill Dec 6 Activist row ("Sale one option") and is not activist-influenced (V¶119). Mac-Gray is mixed: Apr 8 Target interest, Jun 21 Party A bid (V¶39, CI p.5). PetSmart stays activist-influenced. `derive_analysis.py` must read the Note prefix and the new value.

### Q8 PetSmart round 1 (decided 2026-09-27, Austin: Alex's date)

Round 1 opens Oct 3, 2014, as V¶55 says. General wording, added to the R5 clause of E6 l.191 (from V¶55's own general statement):

> Where the outreach itself is undated, round 1 opens at the board meeting on the sale process held immediately before the first confidentiality agreements.

PetSmart: Oct 3 board meeting, NDAs in the first week of October, so round 1 opens Oct 3. Other deals have dated outreach and are unchanged. Note: the filing reports communications with 27 parties between Aug 13 and Oct 3; Austin follows Alex's date.

### O2 (deferred 2026-09-27)

Austin: "ignore this interaction for now, we just work with the cockpit." No instruction change; human checking happens in the cockpit workflow. Revisit when the VM is back.

### Evening rulings (27 September 2026, after the VM check)

Austin approved these after the VM reconciliation (`VM_RECONCILIATION.md`, `vm_check/`), with Alex's sources checked for each.

1. **Synacor's reopened round opens Oct 27, 2020 (E6 (d)).** Company E's exclusivity ended Oct 23; on Oct 27 the special committee asked Canaccord to re-initiate outreach and the CEO contacted Company H the same day. The Dec 30 meeting reviewed "ongoing outreach" and continues the round (R3 guard). Alex: same process, contacts renewed on the expiry of exclusivity (V¶109); his workbook marks no round there. This corrects the Stage-questions line above.
2. **A bidder's own statement of the price it would offer is a Bid, including a ceiling or a range.** Source: Alex's workbook for Penford Party A (voice notes silent): Oct 4 ("any offer would be below $17.50–18.00") Informal 17.50–18.00; Oct 13 (value range reduced to $16–18) Informal 16–18; Oct 14 formal letter at $16, Informal (not invited to the Oct 3 final round; the letter's label doesn't decide); Party A exits Oct 14. F11 still holds for remarks without a price level of the bidder's own (a stock-price citation, V¶68).
3. **Route 2 inside a final round is confirmed:** every bid that a bidder invited to a round announced as final makes during that round (CI p.9, V¶27). A party not invited stays outside route 2 (Penford Party A).
4. **Kept as in v0, from Alex's sources:** Other-scope bid rows keep Formality and Conditions (his workbook labels partial bids Informal/Formal in Meredith and Synacor; V¶150); the process Question stays required for every multi-process deal and every round opened by (d) or inference (V¶110, V¶132); the nine exit reasons stay (his dropout codes fit them; no merge).
5. **Version label:** "Version 1".
6. **Workbook check:** the builder compares the draft's outcomes on the nine deals with Alex's workbook for every theme decided as "Alex silent" or "Austin judging for Alex", and lists disagreements for Austin. It changes nothing by itself.
7. **Build and deployment:** development moves to the VM; the build happens in a fresh VM clone on branch `version-1`, by whichever agent team Austin chooses; the app is rebuilt from the archived VM code (`vm-live-2026-09-26`) and wired to the new tools; the app restarts on a fresh catalog (13 deals and their filings, both accounts' sign-ins kept, old instruction versions and working copies archived, their review judgments carried into the Version 1 review by hand); the switch-over is a later step on Austin's order; the old folders are deleted a week after a clean switch-over. Full plan: `BUILD_SPEC.md`.


### Rulings of 28 September 2026 (after the Version 1 build and its review)

Austin approved these after four independent reviews of the build (`BUILD_REVIEW.md`), with Alex's sources checked for each.

1. **Missed due date.** Replaces the retained V114 D10 sentence (draft E14 l.326), the "missed due date by a bidder that continues" Other material event (D2 l.93) and "Name any bidder that missed a due date but continued" (D3 l.117) with:

   > A bidder asked to bid by a due date that has not bid by then exits at the due date (Did not submit), whatever it says about still considering. Exception: if the target takes its late bid before the next round opens, or admits it to the next round, it never left: there is no exit row, and the deadline row's outcome is Extended (late bid accepted). A bidder that returns after that is Re-entered.

   Austin: a bidder that says it is still considering and does nothing else is dropped; one that bids late and is accepted or advanced marks a deadline extension, as agreed with Alex. One observable test, no judgment about who "continues". Alex: late accepted bids stay in the round and set the effective deadline (V¶17–18); extensions and soft deadlines are recorded, not new rounds (V¶61–63, V¶122–123, V¶143, V¶174); DropTarget and re-entry (CI p.7). Alex never states when a non-submitter's exit is dated (his workbook uses the due date, the next opening or a later report); the due date is the simplest single clock. Effects: accepted late bids (Mac-Gray B/C July 24 and A/C September 10, sTec D May 10) stay live with Extended; Datalink's two parties still drop at August 16. **Kraton J: Did not submit June 29** (replaces the July 6 date resolved from V¶82 above; J is still outside round 2), Re-entered July 19, dropped July 20.
2. **Finality resets after a restart.** A round opened by (d) after exclusivity lapses starts the finality test afresh: (c)'s "with no final round yet" looks only at rounds since that restart. Effect: Synacor process 3 gains round 4 at January 6, 2021 (CLP selected for definitive negotiation; inferred final; the January 7 LOI carries it), so 4 rounds in process 3 (was 3). October 27 and December 30 unchanged.
3. **Financing: F6 wins.** Where the filing says a bid lacks firm or committed financing, Financing is Contingent even if the bid is stated not to be subject to a financing condition. Remove the draft's precedence clause (E12 l.288; reconciliation 16, from V114 D5). F6 as ruled; Alex V¶47.
4. **Round 1 date for loosely dated or undated outreach (no ranges).** Outreach dated only to a period counts from the period's start, so a period starting within a week of the launch decision dates round 1 at the decision (keeps Providence "week of March 28" and Kraton "end of May" at their anchors). Truly undated outreach: the board meeting on the sale process held immediately before the first confidentiality agreements; if there is none, the latest dated event the filing places before the outreach (such as the banker's engagement or the board's direction). Effects: Penford August 28, 2014 (was September 1–9); Synacor P1 May 8, 2018, P2 August 25, 2019, P3 July 13, 2020 (were bounded ranges).
5. **Ruling 1 refined; E9 unchanged (Austin, after the fix pass).** The exception also covers a bidder the target admits to the next round or gives more time, with or without a late bid; a new date it is given becomes its due date. Effect: sTec D, which never bid by May 28 or May 30 but was asked for a best-and-final proposal on May 29 and told on May 31 it "had an opportunity to continue in the process", stays live and Withdrew June 5 (Alex's June 5 drop agrees). E9 is left as drafted: a late required response the target considers counts toward Extended (late bid accepted) even after the next round has opened, while on the ledger that bid is a re-entry (Kraton June 29: Extended, last late response J's July 19). To avoid duplication the draft states the rule once, as E14 closing event 3; the due date's outcome lives only in E9 and re-entry only in the Re-entered rule.
6. **Late bids, more time and "Extended" defined (Austin, after the re-review; VERSION1_REREVIEW.md §1).**
   - (a) E9's Extended means a later due date for the same request, set before the target acted on the bids in hand; a new round's due date is not an extension.
   - (b) One verb for late bids and re-entry, used in E9, E14 closing event 3 and the Re-entered rule: the target *considers* a bid when it replies to the bidder about it or its board discusses that offer; a briefing on communications is not enough.
   - (c) The target *gives more time* when it asks or allows the bidder to bid after the due date, before the next round opens. Effects: sTec D live until it Withdrew June 5; Synacor H, encouraged on September 22 to submit a proposal, is live until the September 23 exclusivity (Dropped by target).
7. **Not invited, then asked (Austin, following Alex).** A bidder not invited into a stage when it opens, whom the target asks for an offer before that stage ends, never left: no exit at the opening and no Re-entered row. Its bids keep their own Formality (a bidder never invited into a round announced as final is not route 2). Source: Alex V¶72 (Penford: the October 3 decision is "not explicitly excluding other bidders") and his workbook (Party A continuous from its September 30 NDA to one Drop on October 14; no October 3 exit). Same principle as rulings 5 and 6: the target's own action decides. Effect: Penford Party A live September 30 to October 14 (Informal bids October 3–4, 13 and 14; Not selected at signing October 14). Other deals to be checked for spillover before adoption is final.

*Record corrections (28 September, re-review fix pass): sTec D gave a verbal indication above $5.60 on April 23, after the process letter, so the May 3 outcome is Enforced, not Extended (late bid accepted) at May 10 as ruling 1's effects said; D stays live either way. Ruling 7's spillover check found one further case, Providence D and E (see VERSION1_REREVIEW follow-up), pending Austin.*
8. **Ruling 7 limited (Austin).** Ruling 7 covers a bidder not invited into a stage, not one the target told it was out. Alex draws this line himself: Penford's October 3 decision was "not explicitly excluding other bidders" (V¶72), so Party A stays continuous; at Providence GHF told "the remaining bidders", D and E included, that they were "no longer involved in the process", and his workbook drops them July 27 and marks their August 1 bids "Reengaged". With the limit, ruling 7 changes only Penford Party A in the nine deals.
9. **Overfitting audit (Austin, after the single-case audit of 70bf602).** Apply the audit's cuts that reverse no ruling (about 220 words: flagged items with at most one case whose deletion or folding changes no coding in the nine deals beyond a Note or one date bound); keep one sentence defining an invitation to a returning bidder. F12 and P7 stay (Alex asked for them) with trimmed wording. Ruling 2 applies to Datalink as well: after the October 1 reopening, the October 26 move to exclusivity with Insight opens an inferred final round 5 (5 rounds, not 4), the same pattern as Synacor January 6. For the evaluation, report agreement on codings produced by single-deal rules (Synacor round 4, Penford A, PetSmart October 3, sTec rounds and processes, WDC June 10, Datalink August 16 and round 5, Meredith scope, Penford July 17, Kraton J) separately from the rest; only a held-out test measures generalization.

### Ruling of 8 October 2026 (after the voice-doc review)

Austin approved this after the review of Version 1 and its tools against Alex's voice notes.

1. **"Mixed" Initiation needs the target to move first.** D5 now reads: "Otherwise **mixed** where a target-side first step (Target interest or Target sale decision) comes before every Bidder interest and Bid row and a bidder's own Bid follows it, all before round 1". P5 (27 September) adopted "mixed" from Alex's Mac-Gray note but set no order, so a deal where a bidder bid first and the board then decided to sell also read "mixed". Alex: at Mac-Gray "the target has made the first move" and Party A bid later, "a bit of both" (V¶38–39, CI p.5); at Penford, Ingredion approached the target first, which is bidder interest (V¶68). Effects on the 13 Version 1 workbooks of 28 September: Penford (Ingredion Bidder interest July 17), Datalink (Party A Bid January 19) and Imprivata (Thoma Bravo Bidder interest January 1) become bidder-led; Pepco's recorded bidder-led now agrees with the rule; Mac-Gray stays mixed. `derive_analysis.py` applies the order test, so `review_list.py` flags the three recorded "mixed" values for review.

### Rulings of 9 October 2026 (after the GPT project review)

Austin decided these in the project thread after Claude's check of the GPT review (`_dev/reviews/2026-10-09/`).

1. **A time limit on an offer is not H3.** E12 H3 now reads: "A CVR/earnout, the bidder's own internal approvals and a time limit on the offer (an expiry, or a demand to sign or announce by a date) never trigger H3; give a time limit in the Note." Before, the 13 Version 1 workbooks of 28 September disagreed: Synacor #61 (the winning raise had to be signed that day) was Heavy, and Providence & Worcester #60 (an offer with an expiry) had no H3. Effect: Synacor #61's Conditions become None, with the time limit in the Note; Providence & Worcester #60 already agrees.
2. **A return to an older price is a revision, not a Same offer.** E10 Revisions already listed "a return to an older price" as a new Bid row, and Same offer did not exclude it. Same offer now ends: "A Same-offer row copies the bidder's latest stated offer; a return to an older price is a revision (Revisions above), not a Same offer." Effect: Providence & Worcester #52 (Party E's return to $21.26 after its $23.81 at #50, recorded "Same as #33") becomes a Bid row with its own price. The checker's `ledger.same_as_after_revision` warning (PR #9) flags rows of this kind.
3. **Kraton Parent financing is Committed.** Under E12 Financing, a bid stated not to be subject to a financing condition is Committed, and the Contingent override applies only where the filing says the bid lacks a firm or committed arrangement. Parent's 8 September markup said financing "would not be a condition"; nothing later says financing was not firm, and the Debt Commitment Letter was signed on 27 September. Effect: Kraton #49 becomes Committed; #41 stays Committed and #43 stays Not stated. No instruction change.
4. **Meredith is dropped from the project.** Its filing, its catalog and manifest entries and its seed row are removed (`make_seed.py` keeps it out of a rebuilt seed), and `DESCRIPTIVE_ONLY` in `derive_analysis.py` is empty. This supersedes the Meredith scope rulings and its place in ruling 9's single-deal list. The dated records (this log, the reviews, Alex's voice notes and workbook) keep what they say. In the live cockpit, Meredith leaves the deal list at the next release; its rows stay in the database and the backups.
