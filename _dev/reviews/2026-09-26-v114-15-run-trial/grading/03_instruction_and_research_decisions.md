# What the trial says about v1.14, and what remains for Alex

> **Status, 26 September 2026 (20:45 UTC):** recommendations on v1.14, kept as written. v1.14.1 has since been published as the cockpit default; its wording, not A1's "with a bound", governs residual cohorts (the retest's Mac-Gray residual is Did not submit, 23 July, Count 16). For what v1.14.1 settled, see `_dev/maintenance/2026-09-26-v1141-streamline/` and the [retest](../../2026-09-26-v1141-retest/README.md); for open questions, [research questions](../../../RESEARCH_QUESTIONS.md).

Companion to `01_blind_findings.md` (source findings) and `02_unblinded_comparison.md` (settings). This file separates three things the trial exposed: (A) places where the instruction's wording, not the extractor, produced divergent ledgers, with proposed clarifications offered as recommendations only; (B) decisions that only the researchers can make, marked as new or already pending in the 25 September *Questions on coding conventions, v1.14*; and (C) conventions the trial shows are settled and need no further attention. Nothing here changes the frozen instruction, any workbook or the live pipeline.

Evidence notation: MG, PW, ST are the three filings; "n of 5" counts the trial workbooks for that deal.

## A. Instruction problems (general, evidenced in two or more deals unless noted)

### A1. E14: closing an anonymous residual cohort whose entry dates are a window

**Evidence.** MG's sixteen unnamed financial NDA signers (NDAs "over the next two months", p. 32; IOIs due 23 July): closed Did not submit by 7/23 in 2 of 5 (one with a bound, one with an exact 16), Dropped by target by 8/27 in 2 of 5, Dropped by target by 9/11 in 1 of 5. PW's at-least-sixteen non-IOI signers (all "advised to submit … by May 10", p. 29): Did not submit by the due date in 3 of 5, Dropped by target by 6/1 in 2 of 5. This is the largest single source of cross-workbook variance in the count of live bidders at round 1, which is the instruction's first-ranked research use.

**Why the wording does it.** E14's first transition needs the party to be "eligible for a solicitation"; Part B forbids exact non-submitter counts for groups not eligible as a whole; E14's later transitions then offer two further dates. Readers who doubt eligibility jump to the advancement decision or even the final call; readers who accept the filing's "instructed to submit by July 23" stay at the due date. Both are literal.

**Recommendation (wording).** Add to E14, after the first transition: *"A cohort the filing says was furnished the solicitation, or advised of its due date, is eligible for it even where individual entry dates fall in a window; close its non-submitters as Did not submit by the due date, give Count as a bound where the window extends past the due date ('Count: at most 16'), and say so in the Note. Move the closure to a later transition only where the filing carries the cohort forward past the due date. Dropped by target applies to a residual only where the filing reports the target's exclusion or names a complete advancing set from parties that had bid."* This fixes the label; the count bound stays honest. Whether estimation treats such closures as dropouts or censoring is Alex's (B1).

### A2. E12: H2 "substantive" is undefined, and "a period for due diligence and negotiation"

**Evidence.** MG CSC 9/9: Heavy (H2) in 2 of 5 on the strength of "more in-depth and confirmatory due diligence" to follow (p. 34), Unclear in 3. PW Party E: Heavy (H2) in 1 of 5 because its 60-day exclusivity was "for due diligence and negotiation of definitive documentation" (p. 30), Unclear in 4. PW's four-week, 30-day and three-week diligence periods were Heavy in 5 of 5; the rule works when the filing names a diligence period.

**Recommendation (wording).** In E12 H2: *"Substantive diligence is diligence the filing describes as business, legal, financial, operational or on-site diligence still to be done, or as full, in-depth or complete diligence, as distinct from confirmatory. A period stated for exclusivity, negotiation or signing is not a diligence period even where diligence is to occur within it; a period is a diligence period only where the filing states it as the time the bidder requires, or the target grants, for diligence."* Under that wording MG 9/9 is Heavy (the target planned "in-depth" diligence for the next stage) and PW Party E is Unclear; either way five readers would agree.

### A3. E12: Light versus Unclear when a later passage calls what followed "confirmatory"

**Evidence.** MG CSC 9/18 and 9/21: Light in 2–3 of 5 because p. 38 later says CSC "conducted confirmatory business and legal due diligence" during exclusivity; Unclear in the rest. PW Party B's 8/4 reaffirmation and G&W's 8/12 bid: Light in 1 of 5 (the same workbook), Unclear in 4. Part B already says a later passage counts only if it dates the fact; the Light definition ("subject only to confirmatory … diligence") invites reading the later description.

**Recommendation (wording).** In E12 Light: *"A later description of the diligence that in fact followed as confirmatory does not show that only confirmatory diligence remained at an earlier bid; use Light only where the bid itself, or a passage dated to it, limits the remaining diligence."*

### A4. E12: what triggers Regulatory = Concern, and Antitrust when it does

**Evidence.** MG's $15M reverse fee "in the event regulatory clearance is not obtained" (p. 37): Concern in 2 of 5 (one with Antitrust Y citing p. 85, one with Antitrust blank), Not stated in 3. PW's board comparing STB approval paths for G&W and B and finding "not materially different" (p. 32): Concern in 2 of 5, Not stated in 3. One workbook had Concern with Antitrust blank although the filing names HSR as the only clearance elsewhere.

**Recommendation (wording).** In E12 Regulatory, extend the Concern examples: *"… a reverse termination fee or other term payable on failure of a regulatory clearance, or a board comparison of bidders' approval paths or timing"*, and in Antitrust: *"Y where any part of the filing identifies the clearance as HSR, DOJ, FTC or another competition authority, with the page."* Whether these should be Concern at all is a research question (B4); the wording problem is that five readers split.

### A5. E10/E11: unpriced commitment revisions inside a final round or exclusivity

**Evidence.** MG 10/5 (Pamplona liability, cap unspecified) and 10/8 ($50M cap): Bid rows in 5 of 5 (one via Bid reaffirmed on 10/7), with $21.25 carried in 2, blank in 3; Formality Formal/Informal split on 10/8. ST WDC's 6/20–23 refusal to allow a standstill waiver, "may not move forward" if waived (p. 34): unpriced Bid Formal Heavy (H3) in 2 of 5, Other material event in 3. R01 (22 September) and v1.14 E10 make commitment changes Bid rows; the ledger then contains Bid rows with no price that a downstream reader will count as bids.

**Recommendation (wording and format).** (i) In E10: *"Begin the Note of a same-price commitment revision with 'Commitment revision:'; Bids received counts bidder units, not such rows."* (ii) In E10's express-incorporation paragraph: *"Where the target's exclusivity or standstill with the bidder is conditioned on the bidder not adversely changing its proposal, the price is shown unchanged for the exclusivity period and may be carried, marked Inferred."* (iii) In E12 H3, add the example: *"a bidder's statement during definitive negotiation that it may not proceed unless a term is retained (a standstill, a no-waiver clause)."* Whether such rows are price observations is Alex's (B6).

### A6. E11: formality of a price improvement answering the target's counter after a final due date

**Evidence.** MG CSC 9/21 "last and best" $21.25 answering the target's $21.25 requirement: Formal in 4 of 5, Informal in 1. All 5 coded Party A's 9/18 oral reiteration Formal by route 2. E11's "qualifies on its own under these routes" leaves the counter-answer case open.

**Recommendation (wording).** In E11: *"A bid made in the same final round in answer to the target's counter or request to improve is Formal where the bidder's response to that round's solicitation was Formal and the filing does not show the earlier terms withdrawn."*

### A7. E9: Unclear versus Extended (late bid accepted) when arrival days are unreported

**Evidence.** PW 5/19: nine IOIs "between May 19 and June 1", all considered on 5/23 and 6/1, no new date (p. 29). Unclear in 1 of 5, Extended (late bid accepted) in 4.

**Recommendation (wording).** In E9 outcome 2: *"… including where the filing reports responses received over a window that runs past the due date and the target considered them."*

### A8. E3/E7: later-named parties that may belong to an anonymous cohort

**Evidence.** PW's G&W (NDA dated 4/3 in Annex A) and Party B (introduced 4/21): entered separately beside the "11 strategic" cohort in 1 of 5 (double-count risk, disclosed), folded into the cohort in 2, bounded in 2. E3's "belongs to an earlier cohort only if the filing establishes it" pushes toward separate entries.

**Recommendation (wording).** In E3 Cohorts: *"A later-named party of the cohort's type that entered within the cohort's window and received the cohort's solicitation is treated as a member unless the filing places it outside: give it its own dated row where the filing dates its step, mark the row 'inside cohort #n', and do not count it again. Where membership is uncertain, keep it inside and give the alternative count in a Question."*

### A9. E6: a "reopened" round after the leader withdraws

**Evidence.** ST: after WDC withdrew on 5/31 the target told still-live Company D it could continue (p. 31); 1 of 5 opened a third round there, 4 continued round 2. The round of WDC's 6/10 and 6/14 bids changes with the choice.

**Recommendation (wording).** In E6: *"Telling a participant already live that it may continue, or resuming talks with a bidder that withdrew, is not a reopening; a reopening solicits parties not then live."*

### A10. E1/E3: NDA signers that never proposed anything and later wanted only assets

**Evidence.** ST Companies E and F: entrants that Withdrew on their scope statement in 4 of 5; partial-only from the start in 1 (auction screen 6 versus 4). E1's "partial from the start" and E3's NDA-as-entry pull in opposite directions when the NDA is described as for "a potential sale of the company" but the party's only recorded interest is in assets.

**Recommendation.** Keep the four-of-five default and say so in E1: *"A party that signed the sale process's confidentiality agreement enters; a later statement of asset-only interest is its exit (Withdrew), not evidence that it was partial from the start."* Whether Alex wants such parties in the auction screen is B2.

### A11. D2: Adviser rows outside the sale process

**Evidence.** A BofA row dated 10/23/2012 for Mac-Gray's abandoned acquisition of CSC (4 of 5); Gibson Dunn dated October 2012 as corporate counsel (5 of 5); a proxy solicitor (1 of 5); three buyer-side brokers found only in Annex A (3 of 5). All harmless, all noise.

**Recommendation (wording).** In D2 Adviser: *"Advisers acting in the sale process; a pre-process engagement is a Note on the adviser's first acting row. Other parties' advisers are recorded where the background names them acting."*

### A12. Pipeline, not instruction: the checker's Note-length warning

Most `check.json` warnings are `ledger.note_length` at 41–48 words. D1 says "aim for 40 words; exceed 40 only to retain required facts", so the extractors are compliant and the warning is noise that scales with Note richness (30–34 warnings on the Opus workbooks, 3–12 on the others). Raise the warning threshold to 60, or give D1 a hard cap.

### A13. Not a problem: things the instruction got right in all fifteen

Process count and the E5 tests reported in every map Question; round maps identical in 14 of 15; every deadline outcome identical in 14 of 15 (the exception is A7); contingent options coded as CVR with upfront cash in 5 of 5; execution and announcement as two rows in 15 of 15; winner type resolved in 15 of 15; GHF/BMO as one adviser in 5 of 5; the Party B 8/4 reaffirmation that Alex's voice note asked for in 5 of 5; the differential data-room access in 5 of 5; Company H kept in reserve in 5 of 5; no invented dropouts, NDAs or bids.

## B. Decisions for Alex

Marked **new** (surfaced or sharpened by this trial) or **pending** (already in the 25 September Questions document, with the section). Each gives the choice, the default the trial workbooks mostly applied, and what changes.

**B1 (pending §3.2, §3.3c; sharpened).** Anonymous residual cohorts. When the filing gives NDAs over a window and one due date, are the non-submitters (i) Did not submit at the due date with a bound (the label three of five PW workbooks and two of five MG workbooks used), or (ii) closed at the target's next selection? And downstream, are inferred closures dropouts or censoring? Default proposed in A1: (i). Changes: the live count at round 1 and the exit-type shares for the largest cohorts in MG and PW.

**B2 (pending §2b item 2; new aspect).** NDA signers with no proposal that later state asset-only interest (ST E, F). Entrants that Withdrew (4 of 5) or partial-only (1 of 5)? Changes: ST's auction screen (6 versus 4) and two Withdrew exits.

**B3 (pending §3.3a).** Which Formality reading is primary. Trial facts to weigh: all five workbooks coded MG Party A's oral 9/18 reiteration of an $18–19 range Formal by route 2 (Alex's voice note item 6 agrees); four of five coded CSC's 9/21 counter-answer Formal; PW's price-only 7/26 and 8/1 revisions were Informal in all five under D9. No new decision; the trial confirms the readings are applied consistently.

**B4 (new).** Is a reverse termination fee payable on failure of regulatory clearance, or a board comparison of bidders' approval paths, a "Regulatory Concern"? MG and PW split 2–3. Changes: Regulatory and Antitrust on the winner's final bids in both deals; never the Conditions level (E12 already says Concern is not H3 by itself).

**B5 (new; D14 covers exclusivity only).** Define H2's "substantive" and rule on a period "for due diligence and negotiation". MG 9/9 (2 of 5 Heavy) and PW Party E (1 of 5 Heavy). Changes: Heavy versus Unclear on two bids.

**B6 (pending §3.3b; new example).** Same-price commitment revisions: price observations or not (MG 10/5, 10/8)? And is a bidder's stated refusal to proceed unless a standstill is retained (ST 6/20–23) a commitment revision (Bid, H3) or negotiation of legal terms? Two of five typed it as a Bid; the instruction's text supports them. Changes: one unpriced Heavy Bid row in WDC's final-round series.

**B7 (pending §3.4; divergence to flag to Austin).** sTec Company H. The frozen v1.14 text (E14: "leaving a bidder out of one stage while the target keeps it in reserve … is not an exit") led all five workbooks to keep H live and close it Not selected at signing (four with Would not improve earlier offer). The 25 September proposal to Alex reads "the target did not advance H, with the exit dated as a window" (Dropped by target). The proposal and the text disagree; if Alex chooses the proposal, E14's reserve sentence needs an exception for a bidder told its price "was not sufficient to move them forward".

**B8 (pending §3.1).** sTec round map. Four of five workbooks chose Map A (16 May opens the final round; 30 May Enforced; WDC's return inside round 2); one chose Map B (a round 3 from 31 May); none chose Map C (the voice note's "not the final round"). The filing's "final round process letters" (p. 30) is why. Alex's choice stands, but the trial shows Map A is what careful readers of the text produce.

**B9 (pending §3.5).** Which governs when the voice notes and the hand coding conflict. The trial found three places where the voice notes conflict with the filing as v1.14 reads it: sTec "two separate processes" (all five: one process, gap under or about three months with an undated endpoint); sTec 3 May "soft, not extended" (all five: Extended (late bid accepted), because D's late IOI was taken up); MG item 8 says "party B and party C" were dropped at the 24 September exclusivity, where the filing has A and B dropped and C silent on 18 September (all five workbooks have the filing's version). PW "Party A never made it out of round one" (voice note) versus a 22 July drop (hand coding): all five kept Party A inside the anonymous cohorts, as the pending Providence question (lesson/alex-questions.md) recommends.

**B10 (new, low stakes).** Initiation. MG: all five say target-led; Alex's voice note says "a bit of both". PW: all five say mixed. ST: target-led in two, mixed in three. The Deal facts field needs a one-line rule (e.g. "bidder-led if a bidder's proposal preceded the target's decision; mixed if a bidder's approach without a proposal did").

**B11 (pending; lesson/alex-questions PROVIDENCE-PARTYA-EXIT).** PW Party A's identity among the anonymous exits. All five left it unresolved with a Question, which is the right default. Nothing new.

## C. Settled by the trial (no decision needed)

- Contingent options as CVR at the bidder's stated value with upfront cash in the price cells (MG Party B): 5 of 5, matching Decided item D4.
- Deadline outcomes under D11: MG 7/23 and 9/9 Extended (late bid accepted), 9/18 Enforced; ST 5/3 Extended (late bid accepted), 5/28 Extended, 5/30 Enforced; PW 7/20 Extended (late bid accepted): unanimous.
- One process in each deal, with the E5 tests reported: unanimous.
- Execution and announcement as separate rows; winner type; adviser de-duplication across a bank acquisition; information-access rows; the PW 8/4 reaffirmation: unanimous.
- No workbook needed the checker to catch a quotation, a sort-order break, a missing condition cell or a dangling Flag.
