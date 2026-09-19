# PetSmart reference (built from filing_background.txt only, before opening any candidate)

Source: "Background of the Merger", PetSmart DEFM14A. Quotes are from filing_background.txt. Where Alex's hand rows differ the filing wins (section H).

## A. Priced proposals (N = 11)

| # | Date | Bidder | Low | High | Per share | Formality signals in filing | Raw (as Alex labels) | Mapped |
|---|------|--------|-----|------|-----------|-----------------------------|----------------------|--------|
| P1 | 2014-10-30 | Buyer Group | 81.00 | 83.00 | yes | "non-binding preliminary indications of interest" | Informal | Informal |
| P2 | 2014-10-30 | unnamed "another bidder" (a finalist) | 80.00 | 85.00 | yes | same | Informal | Informal |
| P3 | 2014-10-30 | Bidder 2 (initial) | 78.00 | 78.00 | yes | same; "had initially indicated a price of $78.00" | Informal | Informal |
| P4 | 2014-10-30 to 11-02 (rough; after P3, before the Nov 3 board) | Bidder 2 (revised) | 81.00 | 84.00 | yes | "As a result of its discussions with J.P. Morgan ... increased its indication" | Informal | Informal |
| P5 | 2014-10-30 | unnamed third bidder whose initial range "reached at least $80.00" (voice note 3) | not stated (>= 80 reached) | not stated | yes | same | Informal | Informal |
| P6 | 2014-12-10 | Buyer Group | 80.70 | 80.70 | yes, cash | "final bid letters along with revised versions of the merger agreement"; financing commitments delivered Dec 6 | Formal | Formal |
| P7 | 2014-12-10 | Bidder 2 | 80.35 | 80.35 | yes, cash | final bid letter + revised merger agreement | Formal | Formal |
| P8 | 2014-12-10 | Bidder 3 (two NDA signers working together) | not stated | ~78 ("would not be above the current stock price of approximately $78") | yes | "verbal indication"; "did not submit a written offer" | Informal | Informal |
| P9 | 2014-12-12 (evening) | Bidder 2 | 81.50 | 81.50 | yes, cash | "best and final offer"; revised merger agreement + financing commitments | Formal | Formal |
| P10 | 2014-12-12 (evening, before P11) | Buyer Group | 82.50 | 82.50 | yes, cash | "initially submitted an oral offer ... working to increase" | Formal (Alex labels Formal; filing says oral, superseded within hours) | Formal |
| P11 | 2014-12-12 (later that evening) | Buyer Group | 83.00 | 83.00 | yes, cash | "best and final offer"; documents "in substantially executable form" | Formal | Formal |

Scoring rules for item 1 (fixed for all candidates)
- P5 counts as present if the ledger has a row, or an explicit cohort member/note, for a distinct third IOI bidder at >= $80 that is neither Buyer Group, the $80-85 bidder nor Bidder 2. Price right = no invented number (blank, ">=80", or low 80 with a flag). Two further Oct 30 IOIs (the two later eliminated) have no stated price; they are not priced bids but must exist for the counts (6 IOIs).
- P8 price right = 78 as point or as upper bound / "not above ~78".
- P3 and P4 must be separate rows; one row = merged bid. P10 and P11 must be separate rows.
- Raw formality follows Alex. P10 oral $82.50 is Formal raw. Mapped = raw for every bid: the filing describes no bid as heavily conditioned (Bidder 2's Dec 10 documents were only "less favorable"/more conditional relative to the Buyer Group's). A candidate that attaches heavy conditions to a formal bid gets mapped Informal and is marked wrong on mapped.
- Spurious = a bid row for something that is not a proposal: Dec 6 mark-ups / financing papers, Longview rollover willingness, Industry Participant interest, J.P. Morgan fairness opinion $83, an "aggregate" IOI row with a price, or a duplicate IOI-plus-bid row for one proposal.

## B. Processes and rounds

One process. Two rounds, the second extended.

| Round | Opened (what / when) | Deadline | Final? | Invited | Submitted |
|-------|----------------------|----------|--------|---------|-----------|
| R1 preliminary IOIs | Oct 3, 2014 board meeting, NDAs "first week of October" (accept Oct 3-7, +-3 days; voice note 1). Deadline communicated "During October" (Alex's rough 10/15 announcement row is an accepted alternative for the announcement row, not for the opening) | Oct 30, 2014 exact | non-final, informal | 15 NDA signers | 6 IOIs |
| R2 final round | Nov 3, 2014 exact: board "determined to allow the four bidders ... to proceed to the final round" (hand data differs: Alex rough 11/15) | initially Fri Dec 5; reset on Dec 4-5 to evening of Wed Dec 10 | final | 4 finalists (3 bidding groups after Bidder 3 pairing) | Dec 10: BG and Bidder 2 written, Bidder 3 verbal |
| R2 extension (not a new round, voice note 6) | Dec 10, 2014: ad hoc committee instructs J.P. Morgan to tell each bidder to improve | Dec 12, 2014 | final, "best and final" | BG, Bidder 2 | both, Dec 12 evening |

Opening dates scored: N = 3 (R1 Oct 3-7; R2 Nov 3; extension set Dec 10). rounds_count_right = true only if one process and two rounds with Dec 12 treated as an extension/continuation of round 2 (a separately labelled "round 3" is false; a "2b"/"extension" sub-stage is true).
Bids in right round: N = 11. P1-P5 in R1 (P4 is still R1: it precedes the Nov 3 selection). P6-P8 in R2. P9-P11 in R2 extension (R2 or an explicit extension of R2 both right; "round 3" is counted right for placement if the ledger's own numbering is coherent, since the rounds-count error is already charged once).
Deadline events Alex wants: Dec 5 initial; Dec 4-5 reset to Dec 10; Dec 10 extension to Dec 12; deadline reached Oct 30, Dec 10, Dec 12.

## C. Bidder 3 composition (decided once)

Filing: "Two of the bidders (one of which had been invited into the final round but had indicated a desire to work with an equity partner ..., and the other of which had indicated to J.P. Morgan that it would drop out of the process if not permitted to work together with another bidder) requested permission to work together."
Reference reading (a): both are among the four finalists ("drop out of the process" implies still in it; eliminated parties showed no "interest or ability to remain"; only three groups appear on Dec 10). So 4 finalists = BG, Bidder 2, and the two members of Bidder 3 (the $80-85 bidder and the third >= $80 bidder, in some order). Matches Alex dropping Unnamed 1 and 4 and introducing Bidder 3.
Alternative reading (b): partner came from outside the four. Acceptable only if the candidate flags the ambiguity and closes out the dangling fourth finalist exactly once; otherwise a bidder is left open.
Date of pairing: after Nov 3, before "During November" diligence; undated (accept Nov 3 to mid-Nov).

## D. Live-bidder boundaries (N = 5, same for every candidate)

| Boundary | Reference live count | Evidence |
|----------|----------------------|----------|
| L1 after NDA wave (first week Oct) | 15 (all financial) | "entered into confidentiality and standstill agreements with 15 potentially interested financial buyers" |
| L2 after IOI deadline Oct 30 (through Nov 2) | 6 | "six of the potentially interested parties submitted indications"; 9 non-submitters out, reason not stated |
| L3 after Nov 3 selection | 4 parties (= 3 bidding groups once Bidder 3 forms) | "allow the four bidders ... to proceed"; 2 eliminated by target |
| L4 at final bids Dec 10 | 3 groups bid (BG, Bidder 2, Bidder 3) | Dec 10 paragraph |
| L5 at revised bids Dec 12 / going into signing | 2 (BG, Bidder 2) | Bidder 3 told "unlikely to be competitive and accordingly ... did not submit a written offer" (exit Dec 10; Alex's 12/14 accepted as alternative because the filing has no explicit exit sentence) |

live_at_signing (JSON) = 2: bidders still live immediately before the Dec 13 board decision / Dec 14 execution (BG wins, Bidder 2 must then be closed as loser on Dec 13-14).
Accounting test: 15 signers = 1 winner (BG) + 14 closed exactly once: 9 no-IOI (Oct 30 to Nov 2, reason unknown), 2 eliminated (Nov 3, target), 2 members of Bidder 3 (closed once, via Bidder 3, Dec 10 or Dec 14), Bidder 2 (Dec 13-14, lost). Closing the two Bidder 3 members individually AND Bidder 3 again = double close-out unless the first is clearly a merge/re-label, not an exit. Cohort rows or one-row-per-bidder are both fine if counts add to 15.

## E. Counts (N = 7)

1. Contacts total = 27, exact ("J.P. Morgan was contacted by 27 potential participants"), inbound, mid-Aug to end-Oct; Industry Participant not counted.
2. Strategic = 3.
3. Financial = 24 (incl. lead buyers and large equity suppliers).
4. NDA total = 15, exact, first week of October.
5. NDA split = 15 financial / 0 strategic.
6. IOIs on Oct 30 = 6.
7. Finalists = 4.
Also: "approximately 15 parties had expressed interest" (Oct 3; approximate is correct here). Longview's confidentiality agreements (before Dec 9; with Buyer Group Dec 12) are not bidder NDAs and must not raise the NDA total. Any "at least 27"/"at least 15" is an error (voice note 2).

## F. Exits the filing states

- Industry Participant: never invited, no NDA; last contact Aug 27, 2014 (target-driven exclusion; not an NDA signer, so not part of the 15).
- 9 NDA signers: no IOI on Oct 30; reason not stated (Alex: unknown).
- 2 IOI submitters: eliminated after Nov 3 board; notified by J.P. Morgan; "none ... indicated any interest or ability to remain ... above their respective initial indications" (Alex: target drop).
- Bidder 3: Dec 10, valuation not above ~$78 market price; told unlikely competitive; no written offer.
- Bidder 2: best and final $81.50 lost to $83.00; closed at Dec 13 board / Dec 14 signing.

## G. Dates, initiation, advisers

- Spring 2014: PetSmart (as would-be acquirer) approaches Industry Participant, from March 2014; not a sale of PetSmart.
- May 21, 2014 weak Q1 results; late May-June stockholder communications.
- June 18, 2014 board: unnamed financial advisor + Wachtell Lipton (legal, first mention); ad hoc committee formed.
- July 2014: J.P. Morgan retained as target financial adviser (first mention; Alex rough 07/01).
- July 3, 2014 JANA 13D (9.9%) pushing a sale; July 7 Longview public letter; July 10 meetings. Activist-pressured initiation.
- Aug 7 Industry Participant calls J.P. Morgan; Aug 22 and Aug 27 calls; not invited.
- Aug 13, 2014 board decides to explore a sale (target initiation); Aug 19, 2014 press release (public sale announcement).
- Oct 3 board; first week Oct 15 NDAs; Oct 30 IOIs; Nov 3 selection; Dec 3 board; Dec 4-5 deadline reset; Dec 6 mark-ups (BG, Bidder 2) and BG financing papers; Dec 8 board + revised drafts; Dec 9 Longview intro meetings; Dec 10 final bids; Dec 11 J.P. Morgan calls Longview; Dec 12 Longview-BG confidentiality agreement, revised bids; Dec 13 board approves, J.P. Morgan fairness opinion; Dec 14, 2014 merger agreement executed AND press release (two events, same day).
- Advisers: J.P. Morgan (target, financial), Wachtell Lipton (target, legal). No bidder adviser named in the Background.
- Types: all 15 NDA signers financial; Buyer Group financial (BC Partners-led). Consideration all cash for P6-P11.
- Longview rollover (up to 7.5m shares) is not a consortium (voice note 7). Bidder 3 pairing is a genuine bidder consortium.

## H. Hand-data discrepancies (recorded now)

1. Alex has 8 no-IOI drops (Unnamed 5-12) but 15 - 6 = 9; "Bidder 1" (xl 6424) signs an NDA and never exits. Filing has no "Bidder 1".
2. Alex closes Unnamed 1 and Unnamed 4 on 12/10 and Bidder 3 again on 12/14; Bidder 3 has no NDA row. Not used as the item-3 standard.
3. Alex dates "Final Round Ann" 11/15 (rough); filing gives Nov 3 exact for the selection.
4. Alex dates Bidder 3's drop 12/14; filing implies Dec 10.
5. Alex records the third >=$80 bidder as low 80 with no high; filing gives no number beyond "reached at least $80.00".
6. Alex has no row for the Dec 5 initial deadline or the Dec 4-5 reset although voice note 6 / closing summary ask for them.

## I. Voice-note checklist (item 6), N = 7

| # | Point | Satisfied when |
|---|-------|----------------|
| V1 | Date inference: "first week of October" NDAs narrowed to Oct 3-7 using the Oct 3 board; round 1 starts Oct 3 | NDA date assigned within Oct 3-7 and round 1 opening tied to Oct 3 (partly if only one of the two) |
| V2 | 27 contacts is exact, not "at least" | no "at least"/">=" on 27 (or on 15) |
| V3 | The hidden third >= $80 bidder; four finalists | ledger notes or rows the unaccounted third bidder and four finalists |
| V4 | Bidder 2's initial $78 then revised $81-84 in narrative order | P3 row precedes P4 row |
| V5 | Dropout reasons: 2 eliminated = target decision; 9 no-IOI = unknown | both coded that way |
| V6 | Dec 12 is an extension of round 2, not a new round; deadline revisions recorded as rows (Dec 5 -> 10 -> 12) | extension not a new round AND revisions recorded (partly if one) |
| V7 | Longview rollover is not a consortium | no consortium/joint-bidder coding of Longview with Buyer Group |

## J. Item 8 fixed lists

Omissions checklist (10): (1) J.P. Morgan adviser row at first mention (July 2014); (2) Wachtell Lipton; (3) initiation: activist pressure (JANA Jul 3 / Longview Jul 7) ; (4) target board decision Aug 13; (5) Aug 19 public sale announcement; (6) Dec 14 signing and (7) Dec 14 announcement as separate events; (8) deadline set vs reached, incl. Dec 5 -> Dec 10 -> Dec 12 revisions; (9) Nov 3 selection / final round start; (10) Bidder 3 formation.
Rows Alex would delete (types): Dec 6 document submissions; Dec 8 draft circulation; Dec 9 Longview intro meetings; Dec 11 J.P. Morgan-Longview call; participation_count rows; IOI row duplicating a bid row; duplicate adviser rows; Longview "consortium"; board meetings with no process decision (Dec 3, Dec 8); Spring 2014 Industry Participant acquisition talks coded as bidder events/dropouts; fairness opinion rows; diligence/management presentation rows.

## K. Clarifications added after opening the candidates (applied identically to all six; no reference fact changed)

1. P8 (Bidder 3's verbal "not above ~$78"): counts as present only if it is a bid row with the bound in a price cell (Alex records it as an Informal bid at 78). A dedicated "Valuation statement" row with empty price and formality cells, or the figure carried only in the exit row's note, is scored "not recorded as a bid" (missed) in both cases; the notes say which form each candidate used.
2. Bids in right round is scored by the round label a researcher would read off the bid row. A ledger that inserts an extra empty round so that the final bids carry "3" instead of "2" has those bids in the wrong round by label; the notes record when a single relabel fixes it. (The section B remark about a "round 3" for the Dec 12 stage turned out not to be needed: no candidate does that.)
3. Rows Alex would delete = rows carrying no adviser, initiation, contact/NDA count, round or deadline, bid, exit, bidder-consortium, signing or announcement content, plus duplicates. One Industry Participant row is allowed (it explains the excluded strategic party); further Industry Participant rows, Longview rollover/confidentiality rows, document-exchange and projection-update rows, the June 18 capital-structure board row, the Dec 13 approval row, count-0 identity rows and second "joined group" rows count as deletable. The Oct 3 board row is kept (voice note 1 uses it). A bidder-counsel adviser row (Simpson Thacher) is not counted.
4. Facts that candidates take from outside the Background section (engagement letter date, rollover share count, "$250 million", "5 bidder groups", p. 27 quotes, Simpson Thacher, Innisfree) cannot be checked against filing_background.txt and are neither credited nor counted as errors.
5. A round-structure error is counted once under item 2 and once as a serious factual error under item 7 (the ledger asserts a round the filing does not support); an order inversion is counted under item 4 only.
