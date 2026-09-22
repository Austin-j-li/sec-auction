# Independent audit of `draft.xlsx` against the Mac-Gray DEFM14A (filed 12/04/2013)

**Standard applied:** SEC_Deal_Ledger_Extraction_Instruction.md, v1.13.2 (21 September 2026).
**Evidence used:** that instruction, `raw_filing/mac-gray_2013-12-04_DEFM14A.htm`, and the read-only `draft.xlsx`. Nothing else. No anonymous bidder was identified. The workbook was not modified.

## 1. Summary verdict

The draft is careful and largely correct. All 53 ledger quotations match the filing verbatim on the cited printed page, each within 30 words, checked mechanically. On structure:

- Sort dates never decrease.
- All date cells are real dates formatted MM/DD/YYYY.
- Every sheet has a frozen header and filters, with no merged cells.
- Every flag has a Question, and every row a Question lists is flagged.
- Every Bid row has All cash, Formality and Conditions filled.

The process and round map agrees with my own reading, built independently from the source: one process; round 0 for the April contact and Party A's 06/21 proposal; round 1 from 06/24; round 2 from 07/25; round 3 (final) from 09/11. So do participation counts, entries, exits, the three deadline outcomes, prices and consideration, and advisers.

I found **no missing bid, no missing entry or exit, and no mispriced or misdated bid**. The ten findings are:

- **One clear error that could mislead adjudication:** Q9's stated consequence (F01).
- **Two possible missing rows, as convention questions:** the 09/21–09/23 “CSC/Pamplona final proposal” (F02) and Party A's round-1 information gap (F03).
- **One label question:** #1 as a Target sale decision (F04).
- **Six smaller errors:** a Question's misstated evidence (F05), two quotations that do not support their row's claim (F06, F07), an over-precise When (F08), a blank Type (F09), and an inaccurate Note (F10).

## 2. Process and round structure as established from the source

- **Before the process.** In winter 2011–2012 Mac-Gray discussed buying CSC, with BofA engaged 10/23/2012; this is buy-side and belongs in Deal facts. CSC was sold to Pamplona in May 2013.
- **Round 0.**
  - 04/05/2013: the Board authorizes management and BofA to explore “transactional opportunities”, including with Party A.
  - 04/08: BofA calls Party A (Target interest).
  - 05/09 and 05/10: the Board discusses a sale and forms the Transaction Committee, which invites three banks.
  - 05/15: the buy-side BofA letter is terminated.
  - 05/30–05/31: BofA is engaged for the strategic review “including a potential sale process”; Moab wins the proxy contest.
  - 06/12: Rothenberg is told he would be excluded if Moab wants a rollover.
  - 06/21: Party A makes an unsolicited $17–$19 cash proposal (entry).
- **Round 1 (06/24).**
  - The Special Committee is formed, concludes a sale should be considered, and decides to approach 50 parties (15 strategic, 35 financial). BofA contacts them over “the next several weeks”.
  - Twenty NDAs are signed over about two months: Party A, CSC/Pamplona, Party B, Party C and 16 unnamed financial parties.
  - Signers receive a package and a 07/23 due date for preliminary indications.
  - The Moab/Pamplona rollover exclusivity request is denied on 07/06.
  - Bids: CSC $18.50 (07/23); Party B $17–$18 (07/24); Party C oral $15–$17 (07/24); Party A's June proposal is reviewed alongside. Party C's written $16–$16.50 follows after the 07/25 meeting.
  - Deadline outcome: Late bids accepted.
- **Round 2 (07/25).**
  - Four are advanced (Party A conditional on an NDA, signed 08/05) into staged disclosure.
  - Management presentations run 08/06–08/14. Strategic bidders get limited data-room access with customer data withheld; financial bidders get broad access.
  - The 08/27 letter sets a 09/09 due date.
  - Bids: CSC $19.50 with Pamplona committed and a two-week exclusivity request; Party B $18.50 with no firm financing (both 09/09); Party A $18–$19 and Party C oral $16–$17 (both 09/10), neither with firm financing.
  - Deadline outcome: Late bids accepted.
- **Round 3 (09/11).**
  - Background: MacDonald declines a rollover, and BofA reports that bidders need his support.
  - All four are asked for “final indications” by 09/18.
  - Bids: CSC $20.75; Party A reiterates $18–$19 as “best and final”; Party B offers $19 cash plus options it values at $2.50 ($21.50); Party C does not submit.
  - Deadline outcome: Enforced. On 09/19 the Special Committee prefers CSC and sets a $21.25 price for exclusivity.
  - 09/21: CSC accepts $21.25 as “last and best”, conditional on two-week exclusivity.
  - 09/21–09/23: the “final proposal” terms are negotiated.
  - 09/24: exclusivity is executed, dropping Party A and Party B by inference.
  - Moab's rollover talks run 09/25–10/07 and end with no rollover.
  - 10/12: exclusivity is extended to 10/15.
  - 10/14: signing.
- **Post.** The merger is announced 10/15. The agreement has a no-shop with a fiduciary out and no go-shop. No post-signing proposals are reported.

Alternative boundaries checked:

- **09/11 as an improvement request within round 2.** Rejected, because E6 treats the first request for final offers as a new round.
- **08/27 as a new round.** Rejected: the same four bidders, and the stage planned on 07/25.
- **April as round 1.** Rejected: a single sounding outside organized outreach.

The only gap of about two months or more is 04/08–06/21 (74 days). E5 does not support a second process.

## 3. Findings

Ranked by consequence for the research. Full fields are in `extraction/findings.json`.

### F01 — incorrect_row

- **Affected:** Questions: Q9 (Excel row 10); Deal ledger #38 (Excel row 39); #39 (row 40); #40 (row 41); #44 (row 45)
- **Source date / page:** 10/07/2013 (also 10/05/2013 commitment letter) / p. 39
- **Quote:** “Kirkland delivered to Goodwin Procter a revised draft of the merger agreement which, among other things, proposed a $15 million Mac-Gray termination fee” (p. 39)
- **Rule:** E10 (Bid reaffirmed by returning its own markup); E11 rule 1; Part F (Questions must state what changes if answered differently)
- **Problem:** Q9 says that if the round-3 responses are read as Informal, 'the deal has no formal bid before signing'. That is wrong under the rules. On 10/07/2013, during exclusivity and with its $21.25 price standing, CSC/Pamplona's counsel returned its own revised draft (markup) of the merger agreement; on 10/05 it returned a revised draft of the Pamplona commitment letter engaging definitive terms. Under E10/E11 rule 1, that returned markup establishes a Formal offer through a Bid reaffirmed row whenever the latest priced row is Informal.
- **Proposed correction:** Rewrite Q9 'What changes if answered differently' along these lines: 'If round-3 responses are Informal, #38/#39/#40/#44 become Informal and a Bid reaffirmed row is required for CSC/Pamplona on 10/07/2013 ($21.25 carried from #44, Formal via its returned merger-agreement markup, Conditions as they stood then), with a Question; Party A and Party B would then have no formal bid.' Leave the current rows unchanged while Q9 recommends Formal.
- **Why it matters:** Formality is research use 3. The adjudicator of Q9 is told that the alternative leaves the deal with no formal bid at all. Under the rules, the winner still has a formal (reaffirmed) bid, so the alternative's real effect falls only on the losing bidders.
- **Counter-reading:** If Q9 is answered as recommended (Formal), no Bid reaffirmed row is needed because #44 is already Formal in a final round (E10), so the ledger rows themselves are unaffected; only the Question's stated consequence is wrong.

### F02 — convention_question

- **Affected:** Deal ledger: no row exists; belongs after #44 (Excel row 45) and before #45; #44 (row 45); #46 (row 47)
- **Source date / page:** between 09/21/2013 and 09/23/2013 (reviewed by Special Committee 09/23/2013) / p. 38
- **Quote:** “Representatives from Goodwin Procter reviewed the terms of the CSC/Pamplona final proposal with the Special Committee, including the $21.25 per share cash consideration, the $15 million CSC reverse termination fee” (p. 38)
- **Rule:** E10 (every change of price or material economic terms the bidder communicates is its own Bid row); E12 (later changes do not rewrite earlier rows); E2 (legal-term negotiation folds)
- **Problem:** The filing defines a distinct 'CSC/Pamplona final proposal', negotiated 09/21–09/23. It adds to the 09/21 $21.25 offer (#44) a $15 million reverse termination fee, an agreed absence of any financing contingency, Pamplona's commitment to fund 100%, and automatic termination of exclusivity if CSC adversely changes those terms. No row records it; the terms appear only in #44's Note ('Terms settled 09/21–09/23'), attached to an earlier bid whose conditions they post-date.
- **Proposed correction:** Either add a Bid row: When 'between 09/21/2013 and 09/23/2013', Who CSC/Pamplona, Strategic, Process 1, Round 3, Price 21.25/21.25, All cash Yes, Formal (same final round), Conditions Heavy (two-week exclusive period still part of the proposal; state in Note that financing is now reported committed with no contingency and a $15m reverse fee), Sort date 09/22/2013, Date from 09/21, Date to 09/23, Note 'revises #44 terms; price unchanged'; then trim #44's Note to what was offered on 09/21. Or keep the fold and raise a Question recording the choice.
- **Why it matters:** The winning bid's commitment terms (financing certainty, reverse fee) are part of what the model reads for formality and conditionality, and E12 requires them to sit on the row where they were made, not on the earlier 09/21 row. The price is unchanged, so price series are unaffected.
- **Counter-reading:** E2 folds 'negotiation of legal terms'. A reverse termination fee and financing-contingency terms can be read as negotiated deal terms rather than a new economic offer from the bidder, and Conditions would stay Heavy under E12 either way because of the exclusive period. So the fold is defensible, provided it is recorded as a choice.

### F03 — convention_question

- **Affected:** Deal ledger: no row exists; belongs between #20 (Excel row 21) and #21 (row 22); #28 (row 29); Rounds: round 1 'Who was in' (row 2)
- **Source date / page:** between 07/11/2013 and 07/23/2013 (resolved 07/27, NDA and package 08/05/2013) / p. 33
- **Quote:** “did not come to agreement on the terms of the customer and employee non-solicitation provisions” (p. 33)
- **Rule:** E2 (a difference in information access among live bidders earns a row wherever the filing reports it); E3 (Party A live from its 06/21 bid)
- **Problem:** Party A was live from its 06/21 bid (#8). Throughout round 1, every NDA signer received the informational package used to formulate preliminary indications, but Party A did not: NDA talks stalled on non-solicitation terms between 07/11 and 07/23, and it got the package only on 08/05. On 07/25 its uninformed 06/21 proposal was reviewed alongside the three informed indications. The ledger records this only in #28's Note and in the Rounds 'not admitted' remark; no row records the information difference.
- **Proposed correction:** Add an Other material event row: When 'between 07/11/2013 and 07/23/2013', Who Mac-Gray (or Party A), Process 1, Round 1, Sort date 07/17/2013, Date from 07/11, Date to 07/23. Note: 'Information access: Party A (live since #8) had no NDA and no informational package during round 1, because NDA talks stalled over customer/employee non-solicitation terms; its 06/21 proposal was reviewed 07/25 against indications from package recipients; package given 08/05 (#28).' Quote the passage above.
- **Why it matters:** Research use 5 (differences in what bidders were told or shown). The model compares Party A's $17–$19 with the round-1 indications at the 07/25 selection, and Party A's bid was made without the data the others had.
- **Counter-reading:** The difference arose from a failed bilateral negotiation, not a target decision to withhold, and Party A had not been admitted to round 1. Recording it in #28's Note and in Rounds may be considered enough, since E2 targets access 'given to some and not others'.

### F04 — convention_question

- **Affected:** Deal ledger #1 (Excel row 2); Deal facts: Initiation (row 10)
- **Source date / page:** 04/05/2013 / p. 27
- **Quote:** “authorized Mac-Gray management to work with BofA Merrill Lynch to explore transactional opportunities that might be available to Mac-Gray, including opportunities with another strategic party” (p. 27)
- **Rule:** D2 (Target sale decision: the board decides to explore or pursue a sale; keep its qualifications); Part A (classify as it stood at the time)
- **Problem:** The 04/05 authorization is to explore 'transactional opportunities', including a business combination with Party A. It is not a decision to explore a sale: the Board deferred the sale question to 05/09, and on 05/09 it again deferred ('would discuss ... engaging in a potential sale process, at its next meeting'). The row's own Note says 'not yet a sale decision', which contradicts its label. The first board-level step toward a sale is the 05/30 adviser mandate 'including a potential sale process', and the explicit decision is 06/24 (#9).
- **Proposed correction:** Relabel #1 as Other material event, beginning the Note 'Board authorized exploration of transactional opportunities (not a sale decision) ...'. Keep #9 (06/24) as the Target sale decision. Optionally raise a Question if the label is kept.
- **Why it matters:** Two Target sale decision rows date the start of the sale effort to April rather than June, and this is inconsistent with round 0 treatment of the April contact. Anyone using the first Target sale decision to time initiation or measure pre-launch contacts will get it wrong.
- **Counter-reading:** 'Business combination' with a competitor could be read as a sale, and BofA's 04/08 call was about Party A potentially combining with Mac-Gray, so a qualified Target sale decision label is arguable. Initiation remains target-led under either label.

### F05 — incorrect_row

- **Affected:** Questions: Q5 (Excel row 6); Deal ledger #17 (row 18); #23 (row 24)
- **Source date / page:** late June–August 2013 ('over the next two months' from 06/24/2013) / p. 32
- **Quote:** “Over the next two months a total of 20 potential bidders, including two strategic bidders (Party A and CSC/Pamplona) and 18 financial bidders” (p. 32)
- **Rule:** Part B (inferences must rest on the reported fact); E14 (Did not submit only for participants eligible for the solicitation); Part F
- **Problem:** Q5's 'Why' states: 'Party A's NDA (08/05) shows that some signings came after 07/23.' Party A is not among the 16 unnamed financial signers in #17/#23. Its late NDA therefore shows nothing about when those 16 signed. The filing gives no signing date for any of the 16, so the reasoning presents the possibility of late signers as evidenced when it is merely open.
- **Proposed correction:** Revise Q5's 'Why': 'The 20 NDAs were signed over roughly two months from 06/24 (p. 32), and the only dated post-07/23 signing is Party A (08/05), which is outside the cohort. The 16 have no reported dates, so whether any signed after 07/23 is unknown. On 07/25 only four ‘interested bidders’ were named (pp. 33–34).' Keep the recommendation and #23 as is, or state in #23's Note 'Count: 16 exits; label Did not submit assumes all 16 signed by 07/23'.
- **Why it matters:** This bears on research use 1 (participation and exit type for 16 of 20 NDA signers) and on the round-1 admitted count. The adjudicator should decide Q5 on the correct evidence.
- **Counter-reading:** The two-month window extends to about 08/24, so late signings among the 16 remain possible. The recommendation itself is reasonable; only the stated evidence is wrong.

### F06 — incorrect_row

- **Affected:** Deal ledger #2 (Excel row 3); #5 (row 6); #6 (row 7)
- **Source date / page:** 04/05/2013 (row date); quotation is of 10/23/2012 / p. 27
- **Quote:** “authorized Mac-Gray management to work with BofA Merrill Lynch to explore transactional opportunities” (p. 27)
- **Rule:** Part B (the quotation supports that row's specific claim); D2 (one Adviser row per relationship, at the earliest date the filing shows that adviser selected or acting); E1 (a target's attempt to buy another company is not its sale process)
- **Problem:** Row #2 dates BofA's role in the target's review to 04/05/2013 but quotes 'Mac-Gray engaged BofA Merrill Lynch on October 23, 2012'. That quotation concerns the buy-side mandate for Mac-Gray's possible acquisition of CSC, not BofA acting in this process on 04/05, so it does not support the row's claim. Relatedly, the ledger gives BofA three rows (#2 Adviser, #5 Adviser ended for the buy-side letter, #6 Adviser for the sale mandate), although the terminated 2012 letter belonged to the target's attempt to buy CSC, which E1 places outside the sale process.
- **Proposed correction:** Replace #2's quotation with the 04/05 passage quoted here (p. 27) or the 04/08 call ('representatives of BofA Merrill Lynch, as instructed by the Board, telephoned a representative of Party A', p. 27). Consider treating BofA as one sale-process relationship at 04/05 (Note: acting under a pre-existing buy-side letter, terminated 05/15, re-engaged for the strategic review 05/30–05/31), and removing #5/#6 or folding them into #2's Note. If the three rows are kept, record the choice in a Question.
- **Why it matters:** Low for estimation (advisers are not bidders), but the quotation mismatch would fail the reviewer's claim check. An 'Adviser ended' row in the middle of the process misreads as a lapse in the target's representation.
- **Counter-reading:** The filing does describe a formal termination (05/15) and a new engagement (05/30–05/31), so reading these as two relationships with an Adviser ended in between is defensible. Only the quotation on #2 is clearly deficient.

### F07 — incorrect_row

- **Affected:** Deal ledger #45 (Excel row 46)
- **Source date / page:** 09/23/2013 / p. 38
- **Quote:** “to provide Moab with the opportunity to resume discussions with CSC/Pamplona regarding a possible equity rollover of Moab's shares in the transaction” (p. 38)
- **Rule:** Part B (quotation supports the row's specific claim); D2 (Other material event: begin the Note with the action)
- **Problem:** The row's claim is a target action ('Allowed Moab to resume equity-rollover talks with CSC/Pamplona'). Its quotation, 'Mr. Rothenberg indicated he would like to discuss the possibility of an equity rollover with CSC/Pamplona', records only Moab's wish, not the target's permission.
- **Proposed correction:** Replace the quotation with the passage above (p. 38, 30 words or fewer) and keep the Note.
- **Why it matters:** Low. It is a claim/quotation mismatch on the rollover-relationship row that reopened Moab's 9% stake to the leading bidder, and the reviewer checks quotations mechanically against claims.
- **Counter-reading:** The same sentence goes on to say BofA 'would arrange and facilitate such a discussion', which implies permission; the existing quotation is adjacent but still not the supporting clause.

### F08 — incorrect_row

- **Affected:** Deal ledger #11 (Excel row 12); #12 (row 13)
- **Source date / page:** from 06/24/2013, 'during the next several weeks' / p. 32
- **Quote:** “During the next several weeks, in accordance with the directives of the Special Committee, BofA Merrill Lynch contacted the strategic and financial parties identified” (p. 32)
- **Rule:** Part B (a date no narrower than its evidence); E8 (When keeps the filing's precision)
- **Problem:** The When cells read 'late June–July 2013 (during the next several weeks after 06/24/2013)'. The filing gives no end date for the outreach. NDAs from it were signed 'over the next two months' (to about late August), so 'July' as the end is narrower than the evidence. Date to is correctly left empty, so When and Date to are inconsistent.
- **Proposed correction:** Set When on #11 and #12 to 'from 06/24/2013, during the next several weeks'. Keep Date from 06/24/2013 and Date to empty.
- **Why it matters:** Minor. It affects the stated timing of the outreach (research use 4) and consistency with the E8 date columns.
- **Counter-reading:** 'Several weeks' from 06/24 would ordinarily end in July, so the label is a natural reading, but it is still not stated.

### F09 — incorrect_row

- **Affected:** Deal ledger #52 (Excel row 53)
- **Source date / page:** 10/14/2013 / p. 41
- **Quote:** “Later in the day, on October 14, 2013, the merger agreement was executed, the Pamplona commitment letter was delivered” (p. 41)
- **Rule:** D1 column 4 (Type: Strategic, Financial, Mixed or Unknown for bidders and cohorts); E3
- **Problem:** #52 (Merger agreement signed) has Who = CSC/Pamplona, a bidder, but Type is blank. Every other CSC/Pamplona row, including the non-bid Exclusivity changed rows #46 and #51, carries Strategic.
- **Proposed correction:** Set Type on #52 to Strategic.
- **Why it matters:** Minor. A filter on the winner's signing row by bidder type drops it.
- **Counter-reading:** One could treat the signing row as a deal-level event like an announcement, but D1 ties Type to the Who, which is a bidder here.

### F10 — incorrect_row

- **Affected:** Deal ledger #22 (Excel row 23)
- **Source date / page:** 07/25/2013 / p. 34
- **Quote:** “Later on July 25, 2013, Party C submitted a written indication of interest at an all-cash purchase price of $16.00 to $16.50 per share.” (p. 34)
- **Rule:** Part B; E8/E9 (what the target considered at the due date's next step)
- **Problem:** #22's Note says Party B and Party C '(07/24 oral, 07/25 written) bid after it and were considered on 07/25/2013'. Party C's written indication came 'later on July 25', after the meeting that reviewed the indications and chose the four (p. 34). Only its 07/24 oral indication can have been considered. Q4 states this correctly, so the Note contradicts Q4.
- **Proposed correction:** Revise the Note: 'Due date for preliminary indications. CSC/Pamplona bid on the day; Party B (07/24 written) and Party C (07/24 oral) bid after it and were reviewed on 07/25/2013; Party C's written revision (#27) followed the meeting.'
- **Why it matters:** Minor. It affects the account of which late bids were accepted at the round-1 deadline (E9), though the outcome label (Late bids accepted) is unchanged.
- **Counter-reading:** The Note may have meant Party C as a bidder, not each of its submissions; the wording is still inaccurate.

## 4. Checked and found correct (no finding)

- **Participation and counts.**
  - Contacts: 50 approached reconcile to Party A (#3) + CSC/Pamplona (#13) + 13 strategic (#11) + 34–35 financial (#12, Count blank, Q3).
  - NDAs: 20 = Party A (#28), CSC/Pamplona (#20), Party B (#15), Party C (#16), 16 (#17).
  - Live units: 4 at the round-2 and round-3 openings (20 entered − 16 did not submit).
  - Exits: Party C Did not submit 09/18, reported, with reason Not stated as in the filing. Party A and Party B are inferred Dropped by target at the 09/24 exclusivity execution (E14). CSC/Pamplona wins.
  - Auction screen: Met, 20.
- **Types.** Party A is Strategic (a laundry competitor). Parties B and C are Financial (among the “18 financial bidders”). CSC/Pamplona is Strategic (a sponsor-owned operating company, E3), and the Parties section confirms CSC as the operating acquirer.
- **Formality and conditions.** Round 1 and 2 indications are Informal. Heavy on #32, #34 and #35 rests on reported absence of firm financing. Heavy on CSC's bids follows the two-week exclusivity request (E12; Q7). #40 Party B 09/18 is Unclear: the 09/18 bid itself reports no absence of commitment, so Unclear is right under E12's financing-silence rule. #40 All cash is No because of the options, and its price is Party B's stated package value (E13). Round-3 responses are Formal under E11 rule 2, which is reasonable; Q9 raises it.
- **Deadlines.** 07/23 Late bids accepted; 09/09 Late bids accepted; 09/18 Enforced. Deadline set rows sit on the communication dates (by 06/28; 08/27), and round 3's due date is set by its Round opened row.
- **Information access.** The staged, unequal data-room access in round 2 (#29) is recorded. CSC's full access during exclusivity came when no rival was live, so it rightly sits in a Note.
- **Advisers.** BofA and Goodwin (target), Kirkland (CSC/Pamplona). Party A's, Moab's and MacDonald's counsel are unnamed, so they get no rows.
- **Deal facts.** Every field checked against the filing: price $21.25 cash; the $594m Pamplona commitment (pp. 58–59); signing 10/14; announcement 10/15; DEFM14A dated 12/04/2013; Background pp. 27–41; Initiation target-led; one process; earlier approaches; auction screen; currency; advisers; account.
- **Supporting sections read.** Parties (p. 26), Reasons (pp. 42–45), BofA opinion including fee and Pamplona relationships (pp. 45–52), Projections (June 2013; no reported selective sharing with bidders, from p. 52), Financing (pp. 58–59), no-solicitation/fiduciary-out summary, merger agreement §6.02 and §6.17 (the CSC NDA is dated 07/11/2013, consistent with #20), and the Annex B opinion letter. None adds an event under E2 beyond what the ledger holds.

## 5. Source coverage

I read the entire Background (pp. 27–41) paragraph by paragraph, in order. I checked it both ways: each paragraph's events against rows, and each row against its paragraph. The table of contents and summary were skimmed; the supporting sections are listed above. I converted the HTML to text with page markers taken from the printed page numbers and verified all ledger and finding quotations against that text.

## 6. Residual uncertainties (not raised as findings)

- **Q3 (CSC/Pamplona as one or two of the 50).** #11's Count 13 assumes CSC (or CSC/Pamplona) is among the 15 strategics. That is supported by the filing's later treatment of CSC/Pamplona as a strategic bidder, but is not stated for the 50-party split.
- **Party A's 09/18 reiteration (#39) as a Bid row.** E10 creates Bid rows for changes and Bid reaffirmed rows only at finalization; it is silent on an unchanged reiteration answering a final solicitation. The draft's treatment, Formal under E11 rule 2 and flagged Q2/Q9, is defensible and does not alter the earlier Informal #34.
- **Date bounds.** #47/#48 could carry a Date from lower bound (both bidders' proposals were still being weighed on 09/19), and #17 could carry an approximate Date to (“over the next two months”). Empty cells are acceptable under Part B, so I did not raise these.
- **Moab rows (#7, #18) labelled Activist.** Other material event (a rollover relationship) would also fit #18. Nothing in the model's uses turns on the choice.
- **16 unnamed signers.** Their signing dates, and therefore the exact exit label, remain unknown (Q5; see F05).
