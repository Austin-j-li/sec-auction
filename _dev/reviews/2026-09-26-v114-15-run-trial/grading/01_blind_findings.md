# First-pass findings, written blind (before opening `administration/blind-key.json`)

Grader: Claude Fable 5.1, 26 September 2026. Inputs: the frozen v1.14 instruction in `inputs/` (SHA-256 `c2d47a47…ab27`), the three complete filings in `inputs/raw_filing/`, and the fifteen anonymized workbooks in `blinded/`. No run folder, log, receipt, prior review or model identity was opened before this file was finished. Letters are randomized per deal and do not identify the same extractor across deals.

## 1. Method and scale

**Reading.** I read each Background section in full (Mac-Gray pp. 27–41; Providence & Worcester pp. 27–32; sTec pp. 23–35) and the passages the workbooks cite outside the background (financing, regulatory, termination fees, Annex A definitions, projections), then built a source inventory of dated acts per deal (section 3 below). Each workbook was then audited in both directions: every substantive row against the filing and the v1.14 rule it applies, and every inventory item against the workbook.

**Mechanical layer.** `mechanical_check.py` (saved beside this file) re-checks each blinded workbook for: four sheets in order; quotation containment in the filing text (punctuation-insensitive); quotations of 30 words or fewer with a page; Sort date never decreasing; every Bid / Bid reaffirmed / Other-scope bid row carrying Stock %, Formality, Conditions, Due diligence, Financing, Regulatory and Exclusivity; one Rounds line per Round opened row; and every Flag id matching a Question and vice versa. **All fifteen workbooks pass every mechanical check** (`mechanical_check_results.json`). Mechanics therefore do not separate the workbooks; the grading below is substantive.

**Severity classes.** Each finding is one of:

- **Material error (M)**: a wrong or unsupported price, date, party, type, round, process or exit that would mislead the estimation if not caught.
- **Convention deviation (C)**: the workbook applies a v1.14 rule differently from what the rule says, with a data effect (an exit label, a round boundary, a Heavy/Light level, an entry counted twice).
- **Omission (O)**: a source event that passes E2's row test and is absent.
- **Defensible alternative (D)**: a reading the instruction genuinely permits, ideally flagged in a Question. Not penalized; recorded because the researchers need to know where readings diverge.
- **Cosmetic (K)**: padding, duplication, wording; no data effect.

**Score.** Fitness as an input to the estimation after ordinary expert review, 0–10. Start at 10; subtract 2.0 per M, 1.0 per C with cohort-wide or round-level effect, 0.5 per C with single-row effect and per O, 0.25 per K. The scale is deliberately harsh on convention deviations because the ledgers must be comparable across deals and extractors; it does not reward verbosity. Bands: 9–10 research-ready after light review; 8–9 sound, a few cells to fix; 7–8 usable with moderate correction; below 7 needs structural rework.

**Headline before the detail.** No workbook contains a material factual error in a price, date, party, type or agreed term. All fifteen agree on the process count, the winner's path, the priced bids and the deadline calendar. Where they differ it is almost entirely inside the zones the instruction leaves open (H2 "substantive", Light versus Unclear, Regulatory Concern, the closure of anonymous residual cohorts, formality of price-only revisions inside a final round, unpriced commitment revisions). Section 5 lists those zones as instruction problems; section 6 lists what only the researchers can decide.

## 2. Mechanical summary

| Deal / label | Ledger rows | Round opened = Rounds lines | Questions | Inferred = Y rows | Mean Note words | Quote mismatches |
|---|---|---|---|---|---|---|
| Mac-Gray A | 72 | 3 = 3 | 7 | 4 | 25 | 0 |
| Mac-Gray B | 64 | 3 = 3 | 11 | 4 | 35 | 0 |
| Mac-Gray C | 64 | 3 = 3 | 8 | 6 | 18 | 0 |
| Mac-Gray D | 74 | 3 = 3 | 8 | 5 | 27 | 0 |
| Mac-Gray E | 64 | 3 = 3 | 10 | 5 | 36 | 0 |
| P&W A | 60 | 3 = 3 | 6 | 3 | 19 | 0 |
| P&W B | 66 | 3 = 3 | 8 | 6 | 24 | 0 |
| P&W C | 68 | 3 = 3 | 8 | 5 | 28 | 0 |
| P&W D | 66 | 3 = 3 | 12 | 3 | 32 | 0 |
| P&W E | 63 | 3 = 3 | 10 | 2 | 29 | 0 |
| sTec A | 66 | 2 = 2 | 7 | 1 | 32 | 0 |
| sTec B | 86 | 2 = 2 | 6 | 8 | 30 | 0 |
| sTec C | 74 | 2 = 2 | 9 | 1 | 24 | 0 |
| sTec D | 67 | 3 = 3 | 8 | 2 | 36 | 0 |
| sTec E | 70 | 2 = 2 | 6 | 1 | 22 | 0 |

Sort dates never decrease in any workbook; every bid row carries the seven required condition cells; every Flag reconciles to a Question.

## 3. Source inventories and the consensus map

### 3.1 Mac-Gray (DEFM14A 4 Dec 2013; acquirer CSC ServiceWorks, sponsor Pamplona; $21.25 cash)

Material events, with the page: 4/5 board authorizes exploring transactions incl. Party A (27); 4/8 BofA sounds out Party A (27); 5/9 Transaction Committee, Goodwin acting (27–28); 5/30 BofA engaged, Moab's nominees elected after proxy contest (29); 6/21 Party A unsolicited $17–19 cash (30); 6/24 Special Committee; decision to consider a sale; 50-party outreach, 15 strategic + 35 financial (31–32); 20 NDAs over two months, 2 strategic + 18 financial incl. B and C; IOIs due 7/23 (32); 6/28 BofA reports Party A (synergies, financing sources) and Pamplona (minimal diligence) (32); NDAs B 6/28, C 6/30, CSC/Pamplona 7/11 (32–33); 7/3–7/6 Moab–Pamplona exclusive rollover request denied (32–33); 7/23 CSC $18.50; 7/24 B $17–18, C oral $15–17; 7/25 four advanced, staged disclosure; C written $16–16.50 (33–34); 8/5 Party A NDA (34); 8/6–8/27 financial bidders broad data access, strategic bidders limited (34); 8/27 letter, revised proposals by 9/9 (35); 9/9 CSC $19.50, Pamplona 100% capital, two weeks' exclusivity requested; B $18.50, no firm financing (35); 9/10 A $18–19 credit facilities or affiliated equity, C oral $16–17, neither with firm commitment (35); 9/11 MacDonald declines rollover; bidders unlikely to proceed without his support; final IOIs requested by 9/18 (35–36); 9/18 CSC $20.75; A reiterates $18–19 as best and final; B $19 cash + options valued by B at $2.50 ($21.50 package); C silent (36); 9/19 committee prefers CSC, sets $21.25 (37); 9/21 CSC $21.25 last and best, two weeks' exclusivity, MacDonald voting agreement (37); 9/21–23 final proposal: no financing contingency, Pamplona 100%, $15M reverse fee if regulatory clearance fails (37–38); 9/24 exclusivity executed to 10/12 (38); 9/25 Kirkland, draft agreement, full data access, Moab rollover talks then end (38); 9/27 MacDonald voting agreements (39); 10/5 Pamplona liability draft; 10/7 $15M target fee proposed; 10/8 $50M cap, $10.5M counter; 10/9 extension request; 10/11 $11M fee agreed; 10/12 exclusivity extended to 10/15; 10/14 signing; 10/15 announcement (39–41). Outside the background: HSR the only clearance (p. 85; waiting period expired 11/27/2013); $594M Pamplona commitment (58); Parent brokers Morgan Stanley, Deutsche Bank, Evercore (A-30); voting agreements ≈15% (p. 67); no go-shop.

**Consensus map (all five).** One process. Round 0: 4/8 approach and 6/21 bid. Round 1 opens 6/24 (outreach decision executed within days), due 7/23, outcome Extended (late bid accepted). Round 2 opens 7/25 (four advanced, staged diligence, revised offers), due 9/9, Extended (late bid accepted). Round 3 opens 9/11 (first request for final indications; Announced as final), due 9/18, Enforced. Party C exits Did not submit 9/18. Party A and Party B Dropped by target at the 9/24 exclusivity. Party B's options coded as CVR $2.50 with $19 upfront, Stock % 0, in all five. Information-access difference (8/6–8/27) recorded in all five. I agree with this map on every point.

### 3.2 Providence & Worcester (DEFM14A 20 Sep 2016; acquirer Genesee & Wyoming; $25.00 cash)

Events: Q4 2015 Party A (Class I rail partner) floats joint ventures and "acquiring equity" (27); board subcommittee hires GHF 1/27/2016 (27); 3/14 board adopts process, Transaction Committee (27–28); 3/22–23 management meets Party A (28); 3/24 outreach authorized; week of 3/28 GHF contacts 11 strategic incl. Party A and 18 financial; all 11 strategic and 14 financial sign NDAs, no standstill (28); 4/3–6 Convention meetings with five strategics incl. G&W; G&W NDA dated 4/3 (A-48); 4/7 two more Class I railroads approached; 4/21 Party B introduced (28); memorandum to NDA signers incl. A, B, G&W (28); IOIs due 5/10, postponed to 5/19 (29); 5/19–6/1 nine IOIs $17.93–26.50; two low bidders excluded; seven advance to presentations and data site (29); mid-June LOIs due 7/20 with markups; drafts posted 6/29, 6/30, 7/11 (29); early July Party C approaches, signs NDA, 7/12 IOI $21, data site and 7/14 presentation (29); late July six LOIs $19.20–24.00: B $24 (expedited diligence, markups); G&W 7/21 $21.15 = $20.02 cash + $1.13 CVR (three-week exclusive diligence, markups), 7/26 $22.15 after price feedback; E $21.26 (60-day exclusivity for diligence and documentation, issues summary only); D $21 (four-week diligence, markups); C $19.30 and F $19.20 (30-day diligence); one strategic and one financial did not submit (29–30); 7/22 and 7/27 committee proceeds with G&W and B; others told they are out (30); 7/29 D and E re-engage; 8/1 D $24, E $23.81 with financing support from F, both 30-day diligence; 8/2 E withdraws revision but confirms $21.26; D refuses to shorten diligence, asks for a no-sign commitment, refused, will not proceed "at that time" (30); 8/4 prioritize B; B's counsel returns revised agreement (30–31); 7/27–8/11 on-site diligence both; 8/9 G&W told the Company intends to sign with another bidder, allowed to continue diligence 8/10–11 (31); 8/12 morning G&W $25 cash, no CVR, markups, expires 6 p.m. 8/13; B told of higher bid; STB paths compared; B declines to raise; G&W superior; signed 8/12; announced 8/15 (31–32). Outside: fee $3.785M (55), G&W sufficient-funds representation (A-22), no financing condition (34), 53% premium to $16.30 (33), p. 33 summary "25 of whom entered into confidentiality agreements".

**Consensus map (all five).** One process. Round 1 opens 3/24 (outreach authorized, executed week of 3/28), due 5/10 → 5/19; round 2 opens at the seven-bidder selection (5/23–6/1), due 7/20, Extended (late bid accepted) on G&W's 7/21 LOI; round 3 opens 7/22–7/27 (definitive negotiation with G&W and B), Inferred final, no due date. C, D, E, F Dropped by target (Lower offer than rivals); D and E Re-entered 7/29; D Withdrew (Terms or process); E's 8/2 reversion is a Bid at $21.26 and E closes Not selected at signing (inferred); B closes Not selected at signing with Would not improve earlier offer; B's 8/4 markup is a Bid reaffirmed at $24 in all five; Party A's fate left inside the anonymous cohorts in all five. I agree with all of this.

### 3.3 sTec (DEFM14A 8 Aug 2013; acquirer Western Digital; $6.85 cash)

Events: 2011 and summer-2012 WDC lunches, no terms (24); 11/14/2012 Company A's banker seeks a meeting, later cancelled (24); mid-Nov 2012 board authorizes adviser search, two decline (24); Balch Hill 13D 11/16, letter 12/6, Potomac joins, 9.8%, proxy nominations (25); 2/13/2013 special committee (25); 2/13 Company B interest, declines ~two weeks later (25–26); 3/13 Company C asset-only interest (26); mid-March Company D interest, draft NDA 3/26 (27); 3/26 BofA retained, decision to approach strategics plus limited financial check (27); 4/1 outreach: 18 parties (17 tech, 1 sponsor); 3 whole-company IOIs (WDC, H, D), 6 asset-only, 9 uninterested incl. A and the sponsor (27); NDAs E 4/4, D 4/10, F 4/11, G 4/17, WDC addendum 4/17 to the 1/29/2009 NDA (A-3), H 5/8; DADW provisions for E, F, H (27–28); presentations WDC, D, G, E; C out 4/15; F declines 4/24 (asset-only); E asset-only shortly after (28); 4/23 process letters WDC and D, IOIs by 5/3; D verbal ">$5.60" (28); 4/26 letter to G (28); 5/1 H approaches, NDA 5/8, presentation 5/10, IOI 5/15 $5.00–5.75 (29); 5/2 D needs another week; 5/3 WDC $6.60–7.10; G will not continue (29); 5/10 WDC data room; D $5.75 with draft exclusivity agreement; 5/14 D data room; 5/15 D may continue if it raises meaningfully (29); H told range insufficient, may revise; 5/23 H cannot increase (30); 5/16 final-round letters and draft agreement to WDC and D, due 5/28 (30); 5/28 WDC $9.15 with markup and insider agreements; D needs two weeks (30); 5/29 best-and-final by 5/30; 5/30 WDC confirms $9.15, D needs time; board picks WDC (30–31); 5/31 WDC withdraws "at that time", stops diligence; D told it may continue (31); 6/1 materials for D; 6/1–6/10 WDC reconsidering; 6/5 D disengages (31–32); 6/10 WDC $6.60–7.10 otherwise on 5/28 terms; 6/11 board demands single best price; 6/14 WDC $6.85 best and final (32); 6/15 board proceeds; 6/18 clean team; 6/19 Cost-Reduction Projections to WDC (46); 6/20–23 WDC refuses DADW waiver, may not proceed if waived (33–34); 6/23 signing; 6/24 announcement (35). Outside: fees $9.4M and $17M (16–17), HSR and Taiwan (16), 12.37% voting agreements (p. 9), $3.59 close (11).

**Consensus map (four of five).** One process (the Nov 2012–Feb 2013 gap examined and rejected as a process break in every workbook). Round 1 opens 3/26 (outreach from 4/1), due 5/3, Extended (late bid accepted) on D's 5/10 IOI. Round 2 opens 5/16 (final-round letters; Announced as final), due 5/28 → 5/30, outcomes Extended; Enforced. WDC Withdrew 5/31 and Re-entered 6/10; D Withdrew 6/5; G Withdrew 5/3; H kept in reserve and closed Not selected at signing (inferred); C partial-only with no exit; WDC's 5/28, 6/10 and 6/14 bids Formal (markup, then express incorporation), Conditions Unclear. Workbook D alone adds a third round. Four of five treat E and F as NDA entrants that Withdrew when they limited scope; E alone treats them as partial-only. I agree with the four-of-five reading on both points, with E's alternative genuinely permitted by E1.

## 4. Findings by workbook

Row numbers are the workbook's `#` column. Pages are the filing's printed pages.

### 4.1 Mac-Gray

**A (72 rows).**
- K: #1 BofA Adviser row dated 10/23/2012 for the 2011–2012 buy-side mandate (Mac-Gray considering acquiring CSC). Not a sale-process relationship; harmless, flagged Q1. Also in B, D, E.
- D: #33 residual 16 financial NDA signers closed "Dropped by target by 08/27/2013" (first complete continuing set after the two-month NDA window), Count 16, Inferred. E14's first transition (Did not submit at the 7/23 due date) would apply only if the cohort's eligibility on 7/23 were established, which the filing does not do. Defensible; well argued in Q5. The five workbooks split three ways on this row (7/23 Did not submit: B, E; 8/27 Dropped: A, C; 9/11 Dropped: D). See section 5.
- D: #44 Party A 9/18 Formal by route 2 with financing carried Contingent ("terms as #38"), Heavy H1. The filing's "reiterated … its previous indication" supports express incorporation.
- D: #50 (9/21) and #51 (9/21–23) Formal; #61 (10/5) Bid Formal Light with blank prices; #62 (10/8) Bid Informal Unclear with blank prices. Strict application of E10's express-incorporation rule. Consistent.
- D: #68–#70 buyer-side advisers (Morgan Stanley, Deutsche Bank, Evercore) from Parent's brokers'-fees representation, A-30 (verified: Section 5.11, a Parent representation). Supported; optional under D2.
- Coverage: complete against the inventory. Exit reasons for A and B "Not stated" (defensible; A's best-and-final refusal would also support Would not improve earlier offer).
- **Score 9.75.** Deductions: K 0.25.

**B (64 rows).**
- K: #1 as above. K: #11 contact cohort "Other contacted parties (47–48)", Count blank, because the filing's "50 parties, including CSC and Pamplona" might count CSC and Pamplona as two; a fair reading but pedantic.
- D: #24 residual closed Did not submit by 7/23, Count blank ("up to 16 missed the deadline"), Q2. Honest about eligibility.
- D: #41 Party B 9/18 Financing Contingent, Inferred = Y, from the committee's 9/19 remark (p. 37) that B "would likely be financing" with affiliated equity and third-party debt; Heavy H1, flagged Q5. A permitted inference under Part B (the passage describes the bid's financing); C and D code Not stated.
- D: #47 9/21–23 Light on the later "confirmatory" description (p. 38), flagged Q7. #55 (10/5) and #57 (10/8) Bid rows Formal Light Committed with $21.25 carried "unchanged through signing"; #56 (10/7 $15M fee draft) Other material event. Q7/Q10 explain.
- D: Exit reasons A "Would not improve earlier offer", B "Terms or process", flagged Q11. Supported by pp. 36–37.
- Coverage complete. Regulatory Not stated with the reverse fee in the Note (Q10), a defensible reading.
- **Score 9.5.** Deductions: K 0.25 + K 0.25.

**C (64 rows).**
- C (single row): #36 CSC 9/9 coded Heavy (H2) on the ground that "more in-depth and confirmatory due diligence" was to follow (p. 34). E12 makes H2 depend on diligence "the filing reports as substantive" or a stated period of two weeks or more, and its Unclear clause says a narrative that only shows diligence open, "without calling it substantive", does not meet H2. "In-depth" is arguable but the row is not flagged in any Question (Q6 covers later CSC bids only). Same call in E, where it is flagged.
- C (single row): #51 9/21–23 Regulatory = Concern with Antitrust blank. E12 fills Antitrust wherever Regulatory is Concern; the filing identifies HSR as the only clearance (p. 85), so Y is the supported value, or the Note should say why blank.
- O: no Exclusivity changed row for the 10/9 extension request (p. 40); E10 makes a later request its own row. Folded into #61's Note.
- K: Q1 states "No interval of about two months without reported acquirer contact"; the 4/8–6/21 interval (74 days) is one, and the other four list it. Part F asks for every such interval.
- K: #14, #17 inferred Contact rows for B and C ("by 06/28", "by 06/30") add nothing the NDA rows do not.
- D: #50 (9/21) Informal, #51 Informal, #58 (10/5) Informal blank price, #59 (10/7) Bid reaffirmed Formal $21.25 (Kirkland's revised agreement while finalizing), #60 (10/8) Informal. Internally consistent with E10's "changes the record" test.
- Coverage otherwise complete. Notes are terse (mean 18 words) but within D1's guidance.
- **Score 8.25.** Deductions: C 0.5 + C 0.5 + O 0.5 + K 0.25 + K 0.25.

**D (74 rows).**
- K: #1 as above. K: #29 (7/25 admission, Other material event) duplicates #28 Round opened. K: inferred Contact rows #13, #14 for B and C.
- C (single row, flagged): #42 residual 16 closed "Dropped by target by 09/11/2013". The first complete continuing set after the NDA window is the 8/27 letter to the four (as A and C use), not the 9/11 final call; dating the closure 9/11 overstates live units during 8/27–9/11 (the Rounds sheet gives round 2 "live count 4–20"). Flagged Q5, alternatives stated.
- C (single row): #64 10/8 Pamplona $50M cap proposal coded Formal. It was a telephone proposal between counsel (p. 39); route 1 needs a markup. A codes it Informal.
- D: #52 9/21 Formal, DD Not stated; #53 9/21–23 Light with DD Not stated; #63 10/5 Formal Light blank price. Flagged Q7.
- D: buyer advisers from A-30 as in A. Exits A/B Not stated.
- Coverage complete.
- **Score 8.25.** Deductions: C 0.5 + C 0.5 + K 0.25 × 3.

**E (64 rows).**
- K: #1 as above. K: #4 labels the 5/9 board meeting a Target sale decision on the strength of "would discuss … engaging in a potential sale process, at its next meeting"; the decision was deferred. Qualified in the Note.
- D: #23 residual closed Did not submit by 7/23, Count 16, flagged Q2 with the eligibility caveat.
- D: #31 CSC 9/9 Heavy (H2) on "in-depth" (as C), but flagged in Q5(a) with the Unclear alternative.
- D: #37 CSC 9/18 Light and #44/#45 Light on the later "confirmatory" description; #45 Regulatory Concern, Antitrust Y (HSR only, p. 85); #53/#54 10/5 and 10/8 Bid rows Formal Light Committed Concern Y with $21.25 carried and marked Inferred. All flagged (Q5, Q10). Internally the most consistent treatment of the regulatory columns.
- K: #39 Party B 9/18 Financing Contingent from p. 37 without Inferred = Y (B marks it).
- D: exits A "Lower offer than rivals", B "Terms or process", Date from 9/19, flagged Q9.
- Richest Notes (mean 36 words) with page-cited fee, premium and voting-agreement facts, all verified.
- **Score 9.25.** Deductions: K 0.25 × 3.

### 4.2 Providence & Worcester

**A (60 rows).**
- C (single value): Rounds round 1 Deadline outcome "Unclear" (Q2). The filing reports nine IOIs received 5/19–6/1, all considered on 5/23 and 6/1 with no new date (p. 29); E9's list puts Extended (late bid accepted) before Unclear, and the receipt window ending after the due date supports it. The other four code Extended (late bid accepted).
- O: no row for management's 3/22–23 meetings with Party A (p. 28; the execution of the 3/14 decision to "proceed with discussions with Party A"). O: no Contact or NDA row for Party B (4/21 introductory meeting; NDA before the memorandum, p. 28); B first appears at its LOI (#27). E7 asks for first contacts.
- D: #10 "10–11 other initial strategic NDA signers", Count blank, because G&W (NDA 4/3, A-48) may or may not be among the 11. #17 "At least 16 initial NDA signers without IOIs", Did not submit, Count blank. Honest bounds.
- D: G&W 8/12 Regulatory Not stated; E LOI Unclear/Required; B reaffirmation Unclear.
- Coverage otherwise complete; leanest Notes (mean 19 words).
- **Score 9.0.** Deductions: C 0.5 + O 0.25 + O 0.25.

**B (66 rows).**
- C (cohort-wide): #18 "Original NDA signers not among nine IOI bidders (16–24)" closed as **Dropped by target** by 6/1. E14's first applicable transition for parties eligible for a solicitation who submitted nothing and are never mentioned again is **Did not submit** by the due date; the Note itself says they submitted no IOI. The label changes the exit statistics for the largest cohort in the deal. Same in C.
- K: the "16–24" range treats the nine IOI bidders as possibly outside the 25 signers; nothing in the filing suggests IOIs came from non-signers (Party C had not yet appeared). A, D and E state "at least 16".
- K: #65, #66 post-signing rows on BMO's undisclosed lender relationship and the 9/6 board review. E2 limits post-signing rows to the announcement, competing proposals, go-shop activity and termination.
- O: no row for the 3/22–23 Party A meetings.
- D: unnamed STB counsel as an Adviser row (#57) — supported (p. 32). #12 Party B Contact 4/21 with Inferred = Y for direction.
- Coverage otherwise complete; good Questions (Q4 on the 25-versus-26 NDA total).
- **Score 8.25.** Deductions: C 1.0 + K 0.25 + K 0.25 + O 0.25.

**C (68 rows).**
- C (cohort-wide): #18 "16 other initial NDA participants" closed **Dropped by target** by 6/1, Count 16. As for B, the supported label is Did not submit.
- O: no row for the 3/22–23 Party A meetings; no Contact row for Party B's 4/21 meeting (B is placed inside the 10-strategic cohort without a dated row).
- K: marginal Other material event rows (#52 Company answers B's diligence questions 8/3; #58 G&W "possible intention" 8/11; #47 inferred Company request to shorten D's diligence). None wrong.
- D: Round opened for round 3 marked Inferred = Y with a 7/22–7/27 window; sound.
- D: Deal facts auction screen "26 parties" with the p. 33 total of 25 flagged in Q4.
- **Score 8.25.** Deductions: C 1.0 + O 0.25 + O 0.25 + K 0.25.

**D (66 rows).**
- C (single row, flagged): separate NDA entries for G&W (#11, 4/3, Count 1) and Party B (#16, Count 1) alongside the "11 strategic NDA signers" cohort (#9, Count 11). If either is among the 11, entries are double-counted; Q3 gives both readings (28 entries versus 26; non-submitters 18 versus 16). E3 says a named party belongs to a cohort only if the filing establishes it, so the literal rule supports D, but the natural reading (used by C and E) places both inside the 11. The uncertainty is fully disclosed.
- D (flagged Q8): #30 and #49 Party E Heavy (H2) because the 60-day exclusivity period is expressly "for due diligence and negotiation of definitive documentation" (p. 30). E12 excludes an exclusivity or negotiation period from H2, but this one names diligence; the other four code Unclear. Genuinely open.
- D (flagged Q12): #58 G&W 8/12 Light (physical diligence just completed, documents finalized that day) and Regulatory Concern (Board weighed STB risks). Light is a stretch (no statement that only documentation remained); the alternative is given.
- D (flagged Q6): #18 nine IOI bidders and #26 Party C IOI with Due diligence "Not begun" because data-site access followed the IOIs. Reasonable; E codes Incomplete/Not begun similarly.
- Most complete early-contact record: #4 Party A 3/22–23 Target interest; #12 five strategics at the Convention; #15 Party B contact; #13 two Class I railroads. Twelve Questions, all specific.
- K: #14 Deadline set Sort date 4/10 inside a 3/24–4/27 window; harmless.
- **Score 9.0.** Deductions: C 0.5 + D-as-stretch 0.25 (G&W Light) + K 0.25.

**E (63 rows).**
- O: no row for G&W's dated NDA (4/3/2016, Annex A p. A-48). E7 asks for dated execution evidence from the annexes; this is the winner's entry date. E folds G&W into the 11-strategic cohort (#9) and says so in the Rounds sheet; the date itself is lost.
- O: no row for the 3/22–23 Party A meetings (mentioned in #5's Note).
- D: #2 labels the Q4-2015 subcommittee appointment a Target sale decision (exploratory, qualified). #18 Did not submit "at least 16", Count blank. #30 Party E Unclear/Required; #56 G&W 8/12 Unclear, Regulatory Concern; #52 B reaffirmed Unclear.
- D: Party D's 8/1–8/2 exclusivity request, refusal and withdrawal all sorted 8/1 with Date from 8/1 and no Date to (the filing reports them with E's 8/2 step). Inside the supported window.
- Ten Questions, each with the alternative and its row effect.
- **Score 9.25.** Deductions: O 0.5 + O 0.25.

### 4.3 sTec

**A (66 rows).**
- K: #1 Gibson Dunn Adviser dated October 2012 (engagement as corporate counsel, p. 25) before the process. In all five; harmless.
- D: E and F as NDA entrants that Withdrew (Other stated reason) when they limited scope (#23, #24); C partial-only with no exit; Q2 gives the partial-from-the-start alternative and its effect (auction screen 6 versus 4).
- D: #47 WDC's 5/30 oral confirmation as Other material event, not Bid reaffirmed (E10: latest priced row already Formal in a final round). #55/#57 6/10 and 6/14 Formal by express incorporation, Unclear.
- D: #63 WDC's 6/20 refusal of a DADW waiver as Other material event (B and C make it an unpriced Bid).
- D: #65 Company H Not selected at signing (inferred), Would not improve earlier offer, Q5.
- Coverage complete, including the 6/19 Cost-Reduction Projections to WDC (p. 46) as an information-access row and Wells Fargo as WDC's adviser. Seven Questions covering the process map, scope, both deadlines, H, formality/conditions and WDC's withdrawal.
- **Score 9.75.** Deductions: K 0.25.

**B (86 rows).**
- K: four inferred Contact rows (#17 E, #19 F, #20 WDC, #21 G, all Inferred = Y, "first contact inferred within banker outreach") that carry no information beyond the NDA rows.
- K: two Adviser rows for Latham & Watkins (#51 as sTec's litigation counsel, #52 as Manouch Moshayedi's). D2 asks for one row per relationship; arguably two relationships, but the split is not useful.
- C (single row, flagged Q6): #82 WDC's 6/20–23 no-waiver ultimatum recorded as an unpriced **Bid**, Formal, Heavy (H3), price cells blank. E10 does make "a same-price change to conditions … a bidder's … liability" a Bid row, and E2 folds "negotiation of legal terms and successive drafts" into Notes; the filing frames this as a negotiating position on the merger agreement. The row inserts a priceless Heavy bid into WDC's final-round series. C does the same; A, D, E record it as Other material event.
- D: #44 "10 other strategic bank-discussion parties" Count 10 (17 less A, D, E, F, G, H, WDC) and #46 "3–4 additional asset-interest" parties, Inferred; arithmetic is right.
- Coverage complete; longest workbook; Notes cite pages consistently.
- **Score 8.5.** Deductions: C 0.5 + K 0.5 (padding) + K 0.25 + K 0.25.

**C (74 rows).**
- C (single row, flagged Q9): #70 unpriced Bid for the ultimatum, Formal Heavy H3, as in B.
- K: #13 "Earlier financial-buyer contacts (count unknown)" Contact row from the board's 3/26 recollection of undated prior communications (p. 27); E5 sends undated earlier approaches to Deal facts.
- K: #35 Company E Withdrew dated in a 4/25–5/16 window (Sort 5/5); the filing's "shortly thereafter" the 4/24 event points to late April, and the upper bound (the 5/16 final selection) is loose. A dates it 4/24 with no upper bound.
- D: Company B given three rows (interest, presentation, decline); fine.
- Coverage complete; nine Questions.
- **Score 8.75.** Deductions: C 0.5 + K 0.25 + K 0.25 + K 0.25.

**D (67 rows).**
- C (round-level, flagged Q3): #51 inferred **Round 3 opened 5/31/2013**, "after WDC withdrew, BofA told D the process was delayed and D could continue", Finality Announced as final (from the 6/11 demand for WDC's best offer). E6 opens a new round after a suspension only where the target "deliberately reopens the solicitation of rival bidders"; here the target told a still-live bidder it could continue, set no due date and solicited no one else, and WDC's return is "one bidder returning unsolicited", which E6 says continues the round. The extra round moves WDC's 6/10 and 6/14 bids and D's withdrawal into a round the other four do not have, which hurts comparability on the instruction's second research use. The Question gives the alternative.
- D: E/F as entrants that Withdrew (Other stated reason); H reserve then Not selected at signing (Would not improve earlier offer); WDC Withdrew (Other stated reason)/Re-entered; ultimatum as Other material event (#64). All sound.
- K: #1 Gibson Dunn October 2012. One Note over 60 words (#66, signing terms; the content is required facts).
- Coverage complete; Deal facts the most detailed on earlier approaches and fees (verified: $9.4M and $17M, 12.37%).
- **Score 8.5.** Deductions: C 1.25 (round-level) + K 0.25.

**E (70 rows).**
- D (flagged Q4): Companies E and F treated as partial-only from entry: NDA rows #15 and #17 carry no Count, no exits, auction screen 4. E1 permits this where "the filing shows [involvement] was partial from the start"; the p. 27 summary's "six potential strategic acquirers expressed an interest in purchasing limited, select assets" supports it, while the NDAs' description as "related to the exploration of a potential sale of the company" (p. 28) supports the other four. Genuinely open; recorded as a research decision (section 6).
- C (single row): #53 WDC Withdrew with Exit reason **Terms or process**. WDC left because it was "reevaluating its interest" and internally divided (pp. 31–32); nothing about the target's terms or process is reported. Other stated reason (A, D) or Not stated (B, C) is supported.
- K: #10 MacKenzie Partners (proxy solicitor) as an Adviser; not a sale-process adviser.
- D: #68 Company H Not selected at signing with Exit reason Not stated (the others use Would not improve earlier offer; both allowed).
- D: cohort accounting through three Other material event rows (#36 the 18, #37 six asset-interest, #38 nine uninterested) plus a Count-blank Contact row (#14). Reconciles.
- Coverage complete; leanest Notes (mean 22 words); six Questions.
- **Score 8.5.** Deductions: D-as-convention 0.5 (E/F) + C 0.5 + K 0.25 + K 0.25.

## 5. Where the instruction, not the extractor, produced the divergence

These are places where careful readers of the same text split, and the split follows from the rule's wording. Each is general, not deal-specific.

1. **E14 closure of anonymous residual cohorts.** Mac-Gray's 16 unnamed financial NDA signers were closed three different ways (Did not submit 7/23 in two workbooks; Dropped by target 8/27 in two; Dropped by target 9/11 in one). P&W's 16-plus non-IOI signers were Did not submit in three and Dropped by target in two. The rule's first transition needs eligibility "at that deadline", which filings that give NDA totals "over the next two months" never establish; readers then fall to different later transitions. This is the single largest source of cross-workbook variance in "how many bidders are live at each stage".
2. **E12 H2 "substantive".** Undefined. "More in-depth and confirmatory due diligence" (Mac-Gray p. 34) made CSC's 9/9 bid Heavy in two workbooks and Unclear in three. P&W's 60-day exclusivity "for due diligence and negotiation" made Party E Heavy in one, Unclear in four.
3. **E12 Light versus Unclear** when the narrative shows diligence still open at the bid but a later passage calls what followed "confirmatory" (Mac-Gray CSC 9/18 and 9/21; P&W B's 8/4 reaffirmation; G&W 8/12). Part B forbids projecting later facts backward, yet the Light definition invites reading the later description. Splits 2–3 in each case.
4. **E12 Regulatory = Concern trigger.** A reverse termination fee payable if regulatory clearance fails (Mac-Gray) was Concern in two workbooks, Not stated in three; a board comparing STB approval paths and finding no material difference (P&W) was Concern in two, Not stated in three. Antitrust Y/blank followed inconsistently (one workbook Concern with Antitrust blank although HSR is the only clearance).
5. **E10 same-price commitment revisions during exclusivity or final documentation.** Sponsor-liability caps (Mac-Gray 10/5, 10/8) became Bid rows in four workbooks, with prices carried in two and left blank in two; a DADW ultimatum (sTec 6/20) became an unpriced Heavy Bid in two workbooks and an Other material event in three. The rule is explicit that such changes are Bid rows, but it produces priceless bid rows inside final rounds and does not say whether they count in Bids received or the price series.
6. **E11 formality of price-only revisions inside a final round.** The 9/21 CSC "last and best" answer to the target's $21.25 counter was Formal in four, Informal in one; Kirkland's 10/8 oral cap proposal was Formal in one, Informal in others. E11's "qualifies on its own under these routes" is hard to apply to bargaining after a final solicitation.
7. **E9 Unclear versus Extended (late bid accepted)** when arrival days are unreported but the reported receipt window runs past the due date and the target considered all responses (P&W 5/19): one Unclear, four Extended (late bid accepted).
8. **E3/E7 named parties inside anonymous cohorts.** P&W's G&W (NDA dated in Annex A) and Party B (introduced 4/21) may or may not be among "11 potential strategic buyers". One workbook enters them separately (double-count risk), two fold them in, two give bounds. E3's "only if the filing establishes it" pushes toward separate entries and inflated totals.
9. **E6 "reopened" rounds.** One sTec workbook opened a round when the target told a still-live bidder it could continue after the leader withdrew. The clause "deliberately reopens the solicitation of rival bidders" should say that a continuation invitation to an existing participant, with no new solicitation, is not a reopening.
10. **E1 partial-only from the start.** NDA signers that never made any proposal and later said they wanted only assets (sTec E, F): entrants that Withdrew in four workbooks, partial-only in one. The auction screen then reads 6 or 4.
11. **D2 Adviser rows** for pre-process mandates (Mac-Gray BofA 2012; sTec Gibson Dunn October 2012; a proxy solicitor) and for buyer-side brokers found only in Annex A. All harmless; the rule could confine Adviser rows to advisers acting in the sale process.
12. **Part F map Question**: only one workbook omitted a two-month gap; the requirement works.

## 6. What only the researchers can decide (blind list)

1. Whether anonymous NDA signers that never bid are live competitors until the first due date (Did not submit) or until the target's advancement decision (Dropped by target), and which date fixes the live count at round 1.
2. Whether NDA signers that never made a whole-company proposal and later sought only assets (sTec E, F) count as entrants and in the auction screen.
3. Which formality reading they want for (a) oral reiterations answering a final solicitation (Mac-Gray Party A 9/18) and (b) price improvements after a target counter within a final round (CSC 9/21). Both were coded Formal by most workbooks under route 2.
4. Whether reverse termination fees tied to regulatory clearance, and boards weighing approval paths, are "Regulatory Concern".
5. The definition of H2's "substantive" and whether a period "for due diligence and negotiation" counts as a diligence period.
6. Whether same-price commitment revisions during exclusivity (sponsor liability, no-waiver ultimatums) belong in the bid series as unpriced Bid rows or in Notes.
7. Whether a bidder's own valuation of contingent options ($2.50, Mac-Gray Party B) is the CVR value they want, or whether options should be treated as stock. All five workbooks chose CVR at the bidder's value.
8. Initiation labels where a bidder's approach preceded a target-led auction (P&W: mixed in five; sTec: target-led in two, mixed in three).

## 7. Blind score table

| Deal | A | B | C | D | E |
|---|---|---|---|---|---|
| Mac-Gray | 9.75 | 9.5 | 8.25 | 8.25 | 9.25 |
| Providence & Worcester | 9.0 | 8.25 | 8.25 | 9.0 | 9.25 |
| sTec | 9.75 | 8.5 | 8.75 | 8.5 | 8.5 |

Material factual errors found: **0 of 15 workbooks**. Convention deviations with cohort- or round-level effect: P&W B and C (residual exit label), sTec D (extra round). Everything else is single-row or cosmetic. Any of the fifteen is usable for the research after a reviewer resolves the section-6 items once for all deals; the score spread measures how much of that resolution the workbook already did correctly and how much padding the reviewer must read past.
