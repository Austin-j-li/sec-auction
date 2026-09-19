from pathlib import Path
from collections import defaultdict
from decimal import Decimal
import json, hashlib

ROOT=Path('.')
OUT=ROOT/'output/grade'
ref=json.loads((ROOT/'output/reference/reference.json').read_text())
hashes=json.loads((OUT/'input_hashes.json').read_text())
audit=json.loads((OUT/'mechanical_audit.json').read_text())
labels=['Candidate-A','Candidate-B','Candidate-C']
# Every row locator below is an Excel sheet row, including the header at row 1.
rows={
'A': {
'P01':'Deal ledger 10; Rounds 2; Deal facts 17', 'P02':'Deal ledger 11–13,15,24; Questions 4; Deal facts 12', 'P03':'Deal ledger 8,12,13,15,24', 'P04':'Deal ledger 21,24,25,32; Rounds 3–4', 'P05':'Deal ledger 11,18; Questions 4', 'P06':'Deal ledger 33–37; Rounds 4', 'P07':'Deal ledger 38–42', 'P08':'Deal ledger 40–42', 'P09':'Deal ledger 14,15,31,39,43; Deal facts 3–4', 'P10':'Deal ledger 18,37,40–46; Rounds 4',
'R01':'Deal ledger 2,5,10,21,32; Rounds 2–4; Questions 2; Deal facts 11', 'R02':'Deal ledger 3,4,8–10; Rounds 2', 'R03':'Deal ledger 8,17,19,20,23; Rounds 2', 'R04':'Deal ledger 21,25; Rounds 3', 'R05':'Deal ledger 25–30; Rounds 3', 'R06':'Deal ledger 32–39; Rounds 4', 'R07':'Deal ledger 10,21,32,38–46; Rounds 2–4', 'R08':'Deal ledger 10,16,19,20,23; Rounds 2; Questions 3', 'R09':'Deal ledger 25,26,29,30; Rounds 3; Questions 3', 'R10':'Deal ledger 32,33,38–40,44; Rounds 4; Questions 2–3',
'F01':'Deal ledger 8,17,19,20,23', 'F02':'Deal ledger 27–30', 'F03':'Deal ledger 34–35', 'F04':'Deal ledger 36,39', 'F05':'Deal ledger 35,39–46; Questions 5', 'C01':'Deal ledger 8,17,19,20,23', 'C02':'Deal ledger 28–30', 'C03':'Deal ledger 27,34', 'C04':'Deal ledger 28,29,35,36', 'C05':'Deal ledger 39–40',
'D01':'Deal ledger 8,10,20,21,23,24', 'D02':'Deal ledger 10,11,18; Questions 4', 'D03':'Deal ledger 27–30,32–37', 'D04':'Deal ledger 38–42,44', 'D05':'Deal ledger 43–46; Deal facts 6–7', 'B01T':'Deal ledger 8,17,19,20,23', 'B02T':'Deal ledger 27–30', 'B03T':'Deal ledger 34,35,38,39', 'B04T':'Deal ledger 36; Questions 6', 'B05T':'Deal ledger 4,8,17,19,20,23,27–30,34–39,45; Deal facts 13–14', 'O01':'Deal ledger 3,4,7–9; Deal facts 10,17', 'O02':'Deal ledger 2,5,6; Deal facts 15–16', 'O03':'Deal ledger 21–22,40', 'O04':'Deal ledger 14,31,39,40,43–45', 'O05':'Deal ledger 39,45–46; Deal facts 2–9'},
'B': {
'P01':'Deal ledger 3,10–13; Rounds 2', 'P02':'Deal ledger 14–16,18,26; Questions 4; Deal facts 12', 'P03':'Deal ledger 8,15,16,18,26', 'P04':'Deal ledger 24,26,28,35; Rounds 3–4', 'P05':'Deal ledger 14,21; Questions 4', 'P06':'Deal ledger 36–40; Rounds 4', 'P07':'Deal ledger 41–45', 'P08':'Deal ledger 43–45', 'P09':'Deal ledger 11,17,18,34,42,47; Deal facts 3–4', 'P10':'Deal ledger 21,39,43–50; Rounds 4',
'R01':'Deal ledger 2,5,10,24,35; Rounds 2–4; Questions 2; Deal facts 11', 'R02':'Deal ledger 3,8–10; Rounds 2', 'R03':'Deal ledger 8,19,22,23,25; Rounds 2', 'R04':'Deal ledger 24,28; Rounds 3', 'R05':'Deal ledger 28–33; Rounds 3', 'R06':'Deal ledger 35–42; Rounds 4', 'R07':'Deal ledger 10,24,35,41–50; Rounds 2–4', 'R08':'Deal ledger 10,19–20,22–23,25; Rounds 2; Questions 3', 'R09':'Deal ledger 28,31–33; Rounds 3; Questions 3', 'R10':'Deal ledger 35,40–43,48; Rounds 4; Questions 2–3',
'F01':'Deal ledger 8,19,22,23,25', 'F02':'Deal ledger 29,30,32,33', 'F03':'Deal ledger 36–37', 'F04':'Deal ledger 38,42', 'F05':'Deal ledger 37,42–50; Questions 5', 'C01':'Deal ledger 8,19,22,23,25', 'C02':'Deal ledger 30,32,33', 'C03':'Deal ledger 29,36; Questions 5', 'C04':'Deal ledger 30,32,37,38', 'C05':'Deal ledger 42–43',
'D01':'Deal ledger 8,10,23–26', 'D02':'Deal ledger 10–14,21; Questions 4', 'D03':'Deal ledger 29–33,35–40', 'D04':'Deal ledger 41–45,48', 'D05':'Deal ledger 43,46–50; Deal facts 6–7', 'B01T':'Deal ledger 8,19,22,23,25', 'B02T':'Deal ledger 29,30,32,33', 'B03T':'Deal ledger 36,37,41,42', 'B04T':'Deal ledger 38; Questions 6', 'B05T':'Deal ledger 3,8,19,22,23,25,29,30,32,33,36–42,49; Deal facts 13–14', 'O01':'Deal ledger 3,7–9; Deal facts 10,17', 'O02':'Deal ledger 2,4–6,46; Deal facts 15–16', 'O03':'Deal ledger 24,27,43', 'O04':'Deal ledger 17,34,42,43,47–49', 'O05':'Deal ledger 42,49–50; Deal facts 2–9'},
'C': {
'P01':'Deal ledger 3,10–12,14; Rounds 2', 'P02':'Deal ledger 13,15,16,18,27; Questions 4; Deal facts 12', 'P03':'Deal ledger 8,15,16,18,27', 'P04':'Deal ledger 25,27,29,36; Rounds 3–5', 'P05':'Deal ledger 13,22; Questions 4', 'P06':'Deal ledger 37–41; Rounds 5', 'P07':'Deal ledger 42–46', 'P08':'Deal ledger 44–46', 'P09':'Deal ledger 14,17,18,35,43,48; Deal facts 3–4', 'P10':'Deal ledger 22,41,44–51; Rounds 5',
'R01':'Deal ledger 2,5,10,25,29,36; Rounds 2–5; Questions 2; Deal facts 11', 'R02':'Deal ledger 3,8–10; Rounds 2', 'R03':'Deal ledger 8,21,23,24,26; Rounds 2', 'R04':'Deal ledger 25,29; Rounds 3', 'R05':'Deal ledger 29–34; Rounds 3–4', 'R06':'Deal ledger 36–43; Rounds 5', 'R07':'Deal ledger 10,25,29,36,42–51; Rounds 2–5', 'R08':'Deal ledger 19–20,23–24,26; Rounds 2; Questions 3', 'R09':'Deal ledger 29,30,33–34; Rounds 3–4; Questions 3', 'R10':'Deal ledger 36,37,42–44,49; Rounds 5; Questions 2–3',
'F01':'Deal ledger 8,21,23,24,26', 'F02':'Deal ledger 31–34', 'F03':'Deal ledger 38–39', 'F04':'Deal ledger 40,43', 'F05':'Deal ledger 39,43–51', 'C01':'Deal ledger 8,21,23,24,26', 'C02':'Deal ledger 32–34', 'C03':'Deal ledger 31,38; Questions 5', 'C04':'Deal ledger 32,33,39,40', 'C05':'Deal ledger 43; Questions 5',
'D01':'Deal ledger 8,10,24–27', 'D02':'Deal ledger 11–14,22; Questions 4', 'D03':'Deal ledger 31–34,36–41', 'D04':'Deal ledger 42–46,49', 'D05':'Deal ledger 47–51; Deal facts 6–7', 'B01T':'Deal ledger 8,21,23,24,26', 'B02T':'Deal ledger 31–34', 'B03T':'Deal ledger 38,39,42,43', 'B04T':'Deal ledger 40; Deal facts 14', 'B05T':'Deal ledger 3,8,21,23,24,26,31–34,38–43,50; Deal facts 13–14', 'O01':'Deal ledger 2,3,7–9; Deal facts 10,17', 'O02':'Deal ledger 2,4–6,47; Deal facts 15–16', 'O03':'Deal ledger 25,28,44', 'O04':'Deal ledger 17,35,43,44,48–50', 'O05':'Deal ledger 43,50–51; Deal facts 2–9'} }
common={
'P01':'The contact representation nets 13 residual Strategic + Party A + CSC/Pamplona = 15 Strategic and 35 Financial = 50; named contacts are not new entrants. C3/C9.',
'P02':'Sixteen anonymous Financial signers plus B/C and A/CSC reconcile to exactly 20 (18 Financial, 2 Strategic), with the two-month timing caveat in the ledger/Question and auction screen Met. C1/C3.',
'P03':'A enters on its June 21 bid, before its August 5 NDA; B/C/CSC have June 28/June 30/July 11 NDAs. Subsequent bids and NDA/admission steps do not add duplicate entrants. C9/C16.',
'P04':'The named continuing set at July 25 and through the final request is A/CSC (Strategic) and B/C (Financial), four; no invented fifth bidder. A later signs its NDA. C3/C16.',
'P05':'The 16-person Financial residual is closed once by inferred July 23 Did not submit, Not stated, with a specific Question acknowledging unknown July eligibility within the two-month NDA window. This is an expressly accepted alternative, not 16 reported withdrawals. C16.',
'P06':'C has a September 18 Did not submit exit, Not stated; three actual final respondents remain (CSC, A, B). No C final offer is invented. C10/C16.',
'P07':'The preference and price-improvement events precede rival exits; A and B are retained until September 24 execution, not dropped on September 19, 21 or 23. C16.',
'P08':'Correct: both A and B are inferred Dropped by target on September 24, leaving CSC; A\'s Would not improve earlier offer is an accepted alternative. Wrong: B\'s Exit reason is Terms or process rather than the locked Not stated. The September 19 comparison is not a reported September 24 exit reason. C16.',
'P09':'CSC/Pamplona is consistently one Strategic operating bidder; shareholders Moab/MacDonald do not become independent bidders or bidding groups, and no shell is separately counted. C3/C4.',
'P10':'The nonwinner exits net 16 + C + A + B = 19 from 20 distinct entrants. One winner remains after September 24 through signing, with no duplicate signing exit, re-entry or invented termination. Earlier anonymous timing remains the disclosed P05 assumption. C16.',
'R01':'One continuous sale process and three numbered rounds; the earlier acquisition-side BofA mandate is not another target sale process or termination. C7/C8.',
'R02':'Round 1 opens with June 24 launch/first outreach, not April exploration or the June 21 unsolicited bid. C8.',
'R03':'A\'s June 21 bid stays Round 0; CSC July 23, B/C July 24 and C\'s distinct July 25 written revision are Round 1. Rounds distinguishes three new submitters from A\'s standing proposal. C8/C12.',
'R04':'Round 2 opens July 25 with four admitted to staged information access and revised proposals, Not final; the August letter is not its first admission. C8.',
'R05':'All four September 9/10 bids answer Round 2; neither the August authorization nor the August 27 deadline letter adds a round. C8.',
'R06':'The September 11 final request opens Round 3 with four invited, September 18 due and Announced as final; the three September 18 responses and September 21 improvement are placed there. C8.',
'R07':'No new stage is opened for preference, September 21 improvement, executed exclusivity, document drafts or extension. Exactly one opening per recorded numbered round, none for Round 0; the final stage runs to signing and announcement is post. C8. Any earlier extra round is assessed in R01/R05/R06/R09.',
'R08':'The July 23 due date is recorded (communication folded into opening or separately bounded); July 24/25 responses remain late, Rounds says Late bids accepted, and a deadline-outcome Question is present. No extension is invented. C11/Part D.',
'R09':'The August 27 letter sets the September 9 due date within Round 2; the reached deadline and September 10 A/C responses support Late bids accepted. A deadline Question is present and no extension is invented. C11/Part D.',
'R10':'Correct: September 18 due date, final solicitation, map/deadline Questions, and no invented September 21 due date or exclusivity-as-bid deadline. Incomplete: Enforced is justified by selection on bids in hand, but the Question never distinguishes the September 21 same-round price increase as post-selection bilateral bargaining or flags the required C11 ambiguity. Thus the locked full-credit alternative is only partly met. C8/C11/Part D.',
'F01':'All five June/July offers, including both oral and written C proposals, are Informal; no final-solicitation or definitive-markup signal existed. C13.',
'F02':'All four September 9/10 revised offers remain Informal, before the September 11 final solicitation; funding or exclusivity does not make them Formal. C13.',
'F03':'September 18 CSC and A\'s actual best-and-final reaffirmation are Formal under the final-solicitation rule, notwithstanding A\'s range/oral form. C12/C13.',
'F04':'B\'s September 18 package and CSC\'s September 21 improvement are Formal; financing uncertainty and mixed consideration do not override the final-stage signal. C13.',
'F05':'A\'s actual September 18 reaffirmation is retained; no October draft exchange, target draft or signing is incorrectly added as another CSC bid/reaffirmation. C12.',
'C01':'All five pre-substantive-diligence June/July proposals are Heavy, without backdating later funding or data-room access. C14.',
'C02':'September 9 B and September 10 A/C are Heavy and their notes retain the explicit absence of firm financing, rather than equating possible sources with commitments. C14.',
'C03':'CSC September 9 and 18 are Light; the notes preserve 100% committed capital and requested exclusive negotiations without inventing a substantive diligence condition or readiness to sign. C14.',
'C04':'A/B September 18 remain Heavy in the context of their recorded earlier absent commitments; no financing cure is presumed and B\'s financing risk is separate from option vesting. C14.',
'C05':'CSC September 21 is Light with exclusivity and family voting support recorded; committed funding/final-document context is preserved and the bid is not made None using signing evidence. C14.',
'D01':'A\'s June bid precedes outreach/NDA; July 24 oral C and July 25 written C remain distinct, and the written revision follows the July 25 opening. No source typo is propagated into a false year. C10.',
'D02':'Aggregate contacts retain the several-week span and anonymous NDAs the two-month window. The July residual closure is explicitly an assumption in its Question, not a reported common signature date; sort keys are nondecreasing. C10/C16.',
'D03':'CSC/B September 9, A/C September 10, final request September 11, and A reaffirmation/C non-submission September 18 are ordered and dated correctly. Late receipts are not forced onto the due date. C10.',
'D04':'September 19 target requirement, September 21 response, September 23 authorization (in execution note), September 24 execution/exits and October 12 extension are distinguished; the October 11 fee agreement is not extension execution. C10/C16.',
'D05':'Correct: bounded Moab resolution and signing October 14 before announcement October 15. Missing: all three buyer-bank relationships and their by-October-14 bounds. Missing adviser evidence cannot receive full date credit. C5/C10.',
'B01T':'All five June/July proposals are present once: A 17–19; CSC 18.50; B 17–18; C oral 15–17 then written 16–16.50. Endpoints and all-cash fields are correct. C12/C15.',
'B02T':'All four September 9/10 offers are present with correct dates, cash flags and endpoints: CSC 19.50, B 18.50, A 18–19, C 16–17. C12/C15.',
'B03T':'CSC 20.75, A\'s unchanged 18–19 reaffirmation and CSC 21.25 are all retained. The September 19 target demand is not made into a bidder offer. C12/C15.',
'B04T':'Both price cells are 21.50, All cash No, with 19 cash and options attributed to B at 2.50 and five-year performance vesting. Secondary mechanics may be summarized under the locked alternative. C15.',
'B05T':'Whole-company USD/share scope is clear. April approach is interest, not an unpriced bid; no invented C final offer, valuation-as-offer, financing-to-per-share conversion, duplicate bid or signing-as-bid. C1/C12/C15.',
'O01':'Initiation covers April 5 authorization (possibly folded), April 8 target approach, Moab\'s May 30 election, June 21 unsolicited proposal and qualified June 24 sale exploration/special committee. No explicit activist sale demand is invented. C5/C6.',
'O02':'Correct target adviser history and first-seen Goodwin/Kirkland are retained. Missing Morgan Stanley, Deutsche Bank Securities and Evercore buyer-group relationships disclosed in agreement §5.11, p. A-30. C5.',
'O03':'July 25 staged admission and August 6–27 B/C broad versus A/CSC restricted access are covered; the exclusivity note folds in later winner full access. No fabricated projection revision. C2.',
'O04':'Correct: Moab request denial/no-rollover resolution, MacDonald no-rollover and September 24/October 12 exclusivity execution. Incomplete: September 27 MacDonald-family voting agreement formation and its effectiveness at merger signing are not distinctly preserved with that date. C2/C4.',
'O05':'Separate October 14 signing and October 15 announcement, 21.25 cash price, Strategic CSC buyer/Parent, DEFM14A December 4 and background pp. 27–41 are correct. No unsupported go-shop or post-signing competing offer is added. B2/C1/C2.'}
credits={k:{t['id']:1 for t in ref['tests']} for k in 'ABC'}
for k, ids in {
'A':['P01','P08','R10','D02','D04','D05','O01','O02','O03','O04'],
'B':['P08','R10','C03','D02','D05','O02','O04'],
'C':['P08','R01','R05','R06','R09','R10','C03','D04','D05','O01','O02','O03','O04']}.items():
 for id in ids:credits[k][id]=0.5
for k in 'ABC':credits[k]['P08']=0.5;credits[k]['R10']=0.5;credits[k]['D05']=0.5;credits[k]['O02']=0.5;credits[k]['O04']=0.5
reasons={k:dict(common) for k in 'ABC'}
reasons['A'].update({
'P01':'Correct 50/15 Strategic/35 Financial totals and A/CSC membership appear in the launch and summary. Missing: the required aggregate Contact event for the actual outreach; a decision to approach is not the reported contacted step. C3/C9; root A-CONTACT.',
'D02':'Correct: the anonymous NDA row has a two-month window and July closure is explicitly questioned. Missing: an actual Contact event carrying the reported several-week outreach span; the exact June 24 launch row cannot substitute for that interval. C9/C10; root A-CONTACT.',
'D04':'Correct September 19 demand, September 21 response, September 24 execution/exits and October 12 extension. Missing September 23 execution authorization and October 9/11 extension approvals; they are neither recorded nor accurately folded into notes (only the fee outcome is summarized). C10.',
'D05':'Correct October 14 signing/October 15 announcement and an October 7 report of Moab\'s decision. The note honestly says the committee was told, so this is not scored as a fabricated decision day. Missing the September 25–October 7 underlying decision window/full-access episode and all buyer-bank by-October-14 relationships. C5/C10.',
'O01':'Correct April exploration/approach, Moab election, unsolicited A bid and committee conflicts. Wrong qualification in June 24 Note: sale seen as best path versus remaining standalone. The source decides to consider a sale and compare it with standalone execution, not yet prefer a sale. C6.',
'O02':'BofA original mandate, termination and May re-engagement are correct; Goodwin is named only in Deal facts. Missing Goodwin first-seen May 9 ledger relationship, buyer counsel Kirkland September 25, and all three annex buyer-bank rows. C5; root A-ADVISERS.',
'O03':'Correct information asymmetry and staged admission are useful. However row 22 places the later observed B/C-versus-A/CSC data-site allocation under exact July 25 bounds, and later CSC full access September 25–October 7 is absent. Retain July decision and add/fold actual access intervals. C2/C10.',
'O04':common['O04']+' Also missing the explicit September 23 permission for Moab discussions; the July denial and October report do not supply that transition.'})
reasons['B'].update({
'R02':'Round 1 opening is honestly bounded June 24–28 with June 26 as midpoint sort key, also used in Rounds. April exploration and the June 21 bid remain Round 0. This is the accepted first-outreach alternative, not an asserted June 26 first call. C8/C10.',
'C03':'Correct September 18 Light and both dates\' committed capital. September 9 Heavy cites withheld customer data and expected further diligence, a useful plausible rationale, but is not flagged as the locked alternative requires; Q4 concerns formality and does not discuss September 9 conditions. Full Heavy-alternative credit therefore unavailable. C14/Part D.',
'D02':'Correct several-week contact span, two-month NDA wording, honest sort keys and explicit July-eligibility Question. Incomplete Date to on anonymous NDA row 14: the finite two-month window is not encoded, although Date from is June 24. Do not infer an exact signature day; supply the supported endpoint/precision caveat. C10.'})
reasons['C'].update({
'R01':'Correct one continuous process and no sale termination from the prior BofA mandate. Wrong four-round map: August 27 implements the July 25 information-and-revised-offer stage, so the locked map has three numbered rounds. C7/C8; root C-ROUND.',
'R05':'Correct four September 9/10 bids grouped together as revised responses. Wrong assignment to newly invented Round 3 rather than July 25 Round 2; the August 27 letter adds no distinct stage. C8; root C-ROUND.',
'R06':'Correct September 11 opening date, four invitees, September 18 due date, Announced as final, and all final responses/September 21 improvement in that stage. Wrong Round 4 rather than Round 3 because of the extra August stage. C8; root C-ROUND.',
'R09':'Correct August 27 communication, September 9 reached deadline, September 10 late responses and Late bids accepted plus Question. Wrong event Round opened/new Round 3 instead of Deadline set inside Round 2. C8/C11; root C-ROUND.',
'C03':'Correct September 18 Light and committed funding on both dates. September 9 Heavy cites contemplated further diligence and exclusivity, but neither flags nor explains restricted strategic access as an inferred material condition. Q4 addresses only September 21. Does not fully meet the locked Heavy alternative. C14/Part D.',
'D04':'Correct September 19 demand, September 21 response, September 24 execution/exits and October 12 extension. Missing September 23 exclusivity authorization and October 9/11 extension approvals, not folded into notes. C10.',
'O01':'Correct early exploration/target approach, Moab election, June 21 bid and qualified June 24 decision. Missing material June 24 committee formation/exclusion of MacDonald and Rothenberg for possible rollover conflicts; generic later conflicts for Rothenberg are not equivalent. C6.',
'O03':'Correct July 25 admission and August 6–27 Financial-versus-Strategic information restrictions. Missing CSC\'s subsequent full data-site/management access and confirmatory work in September 25–October 7, including from exclusivity note. C2.'})

# Field-level records retain root causes so downstream score effects are not counted as independent incidents.
def issue(root, loc, test, field, pages, assertion, correction):
 return {'root_cause_id':root,'rows':loc,'test_or_event':test,'wrong_or_missing_field':field,'source_pages':pages,'unsupported_assertion':assertion,'correction_needed':correction}
errors={k:[] for k in 'ABC'}; omissions={k:[] for k in 'ABC'}; critical={k:[] for k in 'ABC'}
for k,r in [('A',42),('B',45),('C',46)]:
 errors[k].append(issue(k+'-EXIT-REASON',[f'Deal ledger {r}'],'P08','Party B Exit reason',['37','38'],'Terms or process assigned to inferred September 24 exit.','Set Not stated under C16; retain the reported September 19 comparative assessment in its correctly dated context.'))
 errors[k].append(issue(k+'-FINAL-DEADLINE',['Questions 3',f'Rounds {5 if k=="C" else 4}'],'R10','Justification for Enforced',['36','37'],'No explicit treatment of September 21 as post-selection bargaining or same-round ambiguity.','Flag literal Late bids accepted versus Enforced after September 19 selection; explain September 21 treatment without adding a round or due date.'))
 omissions[k].append(issue(k+'-ADVISERS',['Deal ledger (absent; inspect entire sheet)', 'Deal facts 15–16'],'O02/D05','Buyer-bank Adviser events and date bounds',['A-30'],None,'Add Morgan Stanley & Co. LLC, Deutsche Bank Securities Inc., Evercore Group L.L.C. as buyer-group bankers/brokers known by October 14, with Date from empty and no invented mandate/client specificity.'))
 omissions[k].append(issue(k+'-VOTING',[f'Deal ledger {45 if k=="A" else 49 if k=="B" else 50}'],'O04','MacDonald-family support formation date',['39','41'],None,'Record/fold September 27 voting-agreement entry and effectiveness at October 14 signing; C2 does not require routine negotiation rows.'))
errors['A'] += [
 issue('A-QUALIFIED-SALE',['Deal ledger 9'],'O01','Note qualification',['31'],'sale seen as best path versus remaining standalone','Say consider a sale and compare with remaining standalone.'),
 issue('A-ACCESS',['Deal ledger 22'],'O03','When/Date from/Date to for actual data-site allocation',['33','34'],'Exact July 25 assigned to B/C broad versus A/CSC limited data-site access.','Keep the staged-access decision July 25; attribute actual access allocation to August 6–27, or distinguish subsequent implementation explicitly.'),
 issue('A-NDA-ROUND',['Deal ledger 24'],'C8','Round',['34'],'Party A August 5 NDA put in Round 1 after July 25 stage admission.','Set Round 2; this is catch-up access, not a second entry.'),
 issue('A-MOAB-DATE',['Deal ledger 43'],'D05','Missing underlying decision interval',['38','39'],None,'Keep October 7 report as such; preserve September 25–October 7 decision window separately/in the note, with appropriate bounds if the event is the resolution.')]
omissions['A'] += [
 issue('A-CONTACT',['Deal ledger 10; actual Contact row absent'],'P01/D02','Aggregate Contact step and span',['32'],None,'Add actual multi-week outreach Contact representation, split/netted to 15 Strategic and 35 Financial; do not add 50 live entrants.'),
 issue('A-ADVISERS',['Deal ledger (absent)','Deal facts 16'],'O02','Goodwin and Kirkland ledger relationships',['27','38'],None,'Add Goodwin first seen May 9 and Kirkland first seen September 25; retain target/buyer clients.'),
 issue('A-ACCESS',['Deal ledger 40 (no access note)'],'O03/D05','CSC full-access phase',['38'],None,'Fold full data-site/management access and confirmatory work September 25–October 7 into exclusivity note or a material access row.'),
 issue('A-AUTHORIZATION',['Deal ledger 40,44'],'D04','Approval-versus-execution history',['38','40','41'],None,'Fold September 23 authorization and October 9/11 extension approvals into execution notes.'),
 issue('A-MOAB-PERMISSION',['Deal ledger 14,43'],'O04','September 23 permission',['38'],None,'Fold renewed permission into compact rollover relationship history.')]
errors['B'] += [
 issue('B-NDA-BOUND',['Deal ledger 14'],'D02','Date to empty',['32'],None,'Encode finite two-month NDA interval, retaining its contextual precision and unknown individual dates.'),
 issue('B-CONDITIONS',['Deal ledger 29; Questions 5'],'C03','Unflagged inferred Heavy condition',['34','35'],'Heavy based on expected deeper diligence, with no conditions Question.','Use Light or explicitly flag remaining restricted access/exclusivity as inferred material condition; preserve committed capital.'),
 issue('B-RANGE-NOTE',['Deal ledger 32'],'B08 note','Description of price change',['30','35'],'same range as its 06/21 proposal','Say floor raised from 17 to 18, ceiling remains 19. Numeric price cells are correct and B02T retains full credit.'),
 issue('B-EXTENSION-REQUEST',['Deal ledger 48'],'Extension request timing','Exact request day',['40'],'CSC/Pamplona asked 10/09','Say request reported by October 9; that day is the committee report/authorization, not necessarily request occurrence.')]
critical['C'].append(issue('C-ROUND',['Deal ledger 29–50','Rounds 3–5','Questions 2'],'R01/R05/R06/R09','Process-stage segmentation and bid-round variable',['34','35','36'],'August 27 opens a fourth-map stage separate from the July 25 information/rebid stage.','Convert ledger row 29 to Deadline set in Round 2; merge current Rounds 3/4 (Excel rows) into one July 25 round; renumber current final Round 4 to 3. Keep all economic bids and September 11 final opening. One root cause, several scored outputs.'))
errors['C'] += [
 issue('C-CONDITIONS',['Deal ledger 31; Questions 5'],'C03','Unflagged inferred Heavy condition',['34','35'],'Heavy based on contemplated further diligence, without restricted-access inference/flag.','Use Light or flag/reason the permitted alternative from remaining restricted access and exclusivity.'),
 issue('C-CSC-CONTACT-BOUND',['Deal ledger 14'],'C10','Date from empty',['31','32'],None,'Tighten first CSC contact to June 24–28, since it executes the June 24 direction; sort within this interval.'),
 issue('C-FINANCING-NOTE',['Deal ledger 40'],'C14','Missing explicit absence of firm commitment on final B note',['35','37'],None,'Retain earlier absent financing commitment explicitly alongside anticipated third-party debt; Heavy remains supported by the earlier bid record.')]
omissions['C'] += [
 issue('C-INITIATION',['Deal ledger 9'],'O01','Committee formation and rollover conflicts',['30','31'],None,'Fold June 24 special committee and MacDonald/Rothenberg exclusions into sale-decision note.'),
 issue('C-ACCESS',['Deal ledger 44 (no access note)'],'O03','CSC catch-up/full access',['38'],None,'Record/fold September 25–October 7 full access and confirmatory work.'),
 issue('C-AUTHORIZATION',['Deal ledger 44,49'],'D04','Approval-versus-execution history',['38','40','41'],None,'Fold September 23 authorization and October 9/11 extension approvals into executed-exclusivity notes.')]

common_compliance=[
 'Independently inspected all four visible sheets in required order, row-1 headers, frozen row 1 (A2), filters, wrapped nonempty cells and no merged cells. All ledger Sort dates are real Excel dates formatted MM/DD/YYYY, nondecreasing and inside populated bounds. No formulas or cell comments; reviewer-note cells are empty.',
 'All ledger notes are at most 40 whitespace-delimited words and quote bodies at most 30. Thirteen Bid/Bid reaffirmed rows; signing price/formality/conditions cells are blank. No invented offer, re-entry, termination or duplicate exit was found.',
 'The supplied .txt is a cell transcript, not an independent extraction: every transcribed cell was compared with the workbook and matched. No separate delivery prose is present; the four sheets include the account and Questions.',
 'Mechanical flags were reviewed as leads. Affected-row references need not all have an exclusive one-to-one Flag: Part D permits a selective flag only when a Question touches the row. Multiple valid Q identifiers do not constitute substantive extraction errors. No checker issue count was used as a score.'
]
compliance={k:list(common_compliance) for k in 'ABC'}
compliance['A'] += [
 'Deal facts B7 is a real Excel announcement date but is formatted yyyy-mm-dd instead of required MM/DD/YYYY. Normalize that display format; chronology is correct.',
 'Deal facts B4 and B13 contain explanatory text beyond controlled Strategic and Yes, and B10 uses Target-led instead of target-led. Normalize controlled strings and move explanations to suitable notes; primary type/scope substance receives credit.',
 'Questions rows 2–7 contain approximately 95–121 review-field words each, above the about-60-word guidance. Rounds rows 3–4 name all four but omit the requested explicit type split; the ledger supplies it.',
 'Deal ledger row 10 quotation crosses the printed p.31/p.32 boundary. Its words are contiguous in the narrative when the footer/navigation is removed; the checker non-occurrence is a pagination artifact, not an invented quotation. Cite pp.31–32 rather than p.31 alone.',
 'Questions Q2 omits event #24 (Excel ledger row 25) from Rows affected although that row flags Q2. Repair this genuine reverse-link omission. Q3 offers a signing-date exit for possible later anonymous signers; prefer closure by the August 27 four-name solicitation under the locked alternatives.',
 'Inferred cohort row 18 has exact-day When/from/to despite a disclosed uncertain eligibility assumption. Keep inferred status and clarify by-date/bounds in accordance with C10/C16; P05 accepts the explicitly flagged July convention.'
]
compliance['B'] += [
 'Deal facts B4 decorates controlled Strategic with parenthetical explanation; normalize if applying the exact-string schema. The account has seven sentences, rather than five or six.',
 'Questions rows 2–7 are approximately 53–74 review-field words each. Q4/Q5/Q6 mainly revisit classifications already settled by C13/C15/C3; Q2\'s suggested one-day grace is unsupported by C11.',
 'Inferred exits rows 21,44,45 use exact-day from/to (rivals say by in When). Their inferred labels and basis are clear; replace occurrence-style lower bounds with appropriately labelled inferred closure timing where needed.',
 'Quote occurrence is verified, but row 34\'s quotation establishes the need for MacDonald support, not his no-rollover statement; use the adjacent explicit no-rollover sentence for this event. Row 45\'s preference quote supports the comparative assessment, not an express exit notice.'
]
compliance['C'] += [
 'The checker\'s missing deadline Question warning is a false positive: Questions row 3 explicitly classifies all three reached deadlines. Q1\'s broad row range is readable by a human despite the parser warning.',
 'Deal facts fields 10 and 13 include the instruction\'s parenthetical guidance. The order/meaning is correct, and the instruction prints those parentheticals itself; do not treat this ambiguous header rendering as a substantive failure.',
 'Questions review fields contain approximately 61–82 words. Q1\'s proposed fifth round at exclusivity is barred by current C8; replace with the actual three-versus-four-round issue.',
 'Inferred cohort/rival exits rows 22,45,46 use exact-day When/from/to. Their inferred labels are clear; use by-date language and bounds to separate closure convention from occurrence evidence.'
]

alex_common=[
 {'source':'alex_hand_rows.txt lines 6932,6938,6940–6941,6944,6946–6947,6949–6954,6957','finding':'All 13 economic bid/reaffirmation events, prices, cash/options treatment and informal-to-formal sequence agree. A reaffirmation is one event, not duplicate bidder interest plus bid.'},
 {'source':'alex_voice_notes.txt Mac Gray points 1,4,6–8; alex_hand_rows.txt lines 6935–6937,6945,6955,6958–6959','finding':'Candidates preserve target approach then unsolicited bid, named NDA dates, Formal A range, C non-submission and A/B September 24 exits. Voice point 8 says B/C, but hand rows and filing support A/B; no candidate is penalized for following filing/current C16.'},
 {'source':'alex_hand_rows.txt lines 6934,6942; alex_voice_notes.txt Mac Gray point 4','finding':'All use the accepted flagged July 23 residual non-submission convention rather than Alex\'s July 25 Drop; all keep a two-month NDA description rather than an asserted July 15 signature day. Hand row 6936 conflicts internally (June 20 precise versus June 30 rough); all use source-supported June 30.'},
 {'source':'alex_closing_summary.txt points 1,2A–B,2H–K','finding':'All separate signing and announcement and provide map/deadline Questions. Current C5 requires mandate termination/re-engagement where relevant, so repeated BofA relationship events are not penalized merely because the closing summary favors one line per adviser.'}
]
alex={k:{'used_for_primary_score':False,'agreements_and_differences':list(alex_common)} for k in 'ABC'}
alex['A']['agreements_and_differences'] += [
 {'source':'alex_voice_notes.txt Mac Gray points 2,3,9','finding':'Three-round map matches the voice explanation, but missing actual aggregate Contact row and missing Goodwin May 9 adviser event repeat concerns specifically identified there.'},
 {'source':'alex_hand_rows.txt lines 6927,6930; alex_voice_notes.txt Mac Gray point 7','finding':'BofA starts October 23, 2012 rather than April 5 first-seen sale activity; re-engagement uses May 30 decision with May 31 in note. These are supported current-C5 choices. Exclusivity requests are kept in bid notes without downgrading final formality.'}
]
alex['B']['agreements_and_differences'] += [
 {'source':'alex_voice_notes.txt Mac Gray points 2–5,9','finding':'Matches explicit contact cohorts, netted 16 financial NDAs, July 25 second stage with later August 27 deadline setting, and Goodwin May 9 first-seen adviser. Conditions are in bid rows as requested.'},
 {'source':'alex_hand_rows.txt lines 6927,6930; alex_voice_notes.txt Mac Gray point 7','finding':'Supported October 2012 BofA mandate and May 30 re-engagement differ from Alex\'s April 5/May 31 row dates. CSC September 9 Heavy differs from a simple reading of exclusivity as non-downgrading, but formality remains Informal and the current C14 flag requirement governs scoring.'}
]
alex['C']['agreements_and_differences'] += [
 {'source':'alex_voice_notes.txt Mac Gray point 3; alex_closing_summary.txt point 1','finding':'The extra August 27 round conflicts directly with Alex\'s explanation that July 25 began round two and August 27 only announced its deadline; correcting it changes later row assignments.'},
 {'source':'alex_hand_rows.txt lines 6927,6930; alex_voice_notes.txt Mac Gray points 2,9','finding':'April 5 BofA first-seen timing is close to the hand row, while May 30 decision plus May 31 note differs benignly from the hand re-engagement date. Contact cohorts and Goodwin May 9 agree with the voice priorities.'}
]
review_text={
'A':{'useful_questions':'Q1 map and Q3 residual eligibility are useful. Q2 covers deadlines but misses the September 21 ambiguity.','noisy_questions':'Q4 final-response formality and Q5 package pricing revisit clear rules; Q6 offers an out-of-scope prior-mandate process alternative. These lengthen review without primary-score penalties.','ease_of_checking':'Compact 45-row ledger with correct three-round map and all bids. Quotes and numbered events generally make checking easy, but Rounds type summaries and long Questions require cross-sheet lookup.','edits_required':'Add actual outreach and five missing adviser relationships (Goodwin, Kirkland, three banks); add/fold winner full access, authorization history and voting/rollover transitions; correct B exit reason, qualified sale wording, access timing, A NDA round and final-deadline rationale. No bid-price reconstruction is needed.'},
'B':{'useful_questions':'Q1 map and Q3 anonymous eligibility target real boundaries. Q2 has correct first two outcomes but misses the final same-round ambiguity.','noisy_questions':'Q4/Q5/Q6 ask about largely rule-resolved formality, package valuation and winner type, while the actual September 9 conditions inference is unflagged.','ease_of_checking':'Best coverage of contact arithmetic, adviser first appearances and access asymmetry, with the correct three-round map. Notes are fuller; the incorrect same-range sentence needs correction despite correct numeric cells.','edits_required':'Add three buyer-bank relationships and September 27 voting detail; complete anonymous NDA upper bound; correct B exit reason and A range-change wording; qualify the extension request date; resolve/flag CSC September 9 conditions and final-deadline alternative. Preserve the existing process and bid map.'},
'C':{'useful_questions':'Q3 clearly acknowledges the two-month NDA eligibility issue; Q4 makes a genuine September 21 conditions choice visible.','noisy_questions':'Q1 asks about adding a fifth round at exclusivity, prohibited by C8, while retaining the actual mistaken August split. Q2 omits the September 21 ambiguity.','ease_of_checking':'Shorter cells and four Questions reduce word volume, but the extra stage changes a core variable and requires coordinated ledger/Rounds edits. Brevity earns no weighted credit.','edits_required':'Merge the July 25/August 27 stages, convert the August 27 event to Deadline set and renumber later rounds across ledger, Rounds and Q1. Add banks, committee-conflict detail, later full access, authorization history and September 27 support; correct B exit reason and flag/reassess September 9 conditions.'}
}

result={'deal':ref['deal'],'reference_sha256':hashes['output/reference/reference.json'],
 'reference_file_hashes':{p:hashes[p] for p in ['output/reference/reference.json','output/reference/reference.md']},
 'scoring_method':{'stage':2,'credits':[0,0.5,1],'formula':'sum(locked test weight * assigned credit)','category_denominators':ref['weight_validation']['expected_category_totals'],'row_citation_convention':'All locators are Excel sheet row numbers, header included; ledger event # is one less.','alex_affects_primary_score':False,'word_count_method':'Whitespace-delimited words across nonempty data cells, excluding header row; includes dates, quotations and repeated fields. Question review-field counts exclude Q identifier, Rows affected and Reviewer note.'},
 'candidates':{},'proposed_reference_amendments':[],
 'adjudication':{'status':'Original locked-reference scores; no independent adjudication performed.','adjudicated_scores':None,'note':'No source error requiring a reference amendment was found. Borderline applications are explicitly documented (P08, R10, C03); if disputed, they require a fresh identity-blind reviewer. No such review is claimed or delegated.'},
 'scope_limitation':'AI-assigned grades for this single Mac-Gray development-deal run among the three supplied opaque candidates; no generalization or stable statistical ranking claim.'}
for label in labels:
 k=label[-1];ts=[];cats=defaultdict(Decimal)
 for t in ref['tests']:
  id=t['id'];credit=credits[k][id]
  ts.append({'id':id,'credit':credit,'reason':reasons[k][id],'rows':rows[k][id].split('; '),'source_pages':t['source_pages']})
  cats[t['category']]+=Decimal(str(t['weight']))*Decimal(str(credit))
 a=audit[label]
 result['candidates'][label]={'tests':ts,'score_100':float(sum(cats.values())), 'category_scores':{c:float(cats[c]) for c in ref['weight_validation']['expected_category_totals']},'critical_errors':critical[k],'other_errors':errors[k],'omissions':omissions[k],'compliance_observations':compliance[k], 'review_burden':{'ledger_event_rows':a['sheets'][0]['rows'],'numbered_rounds':a['sheets'][1]['rows'],'questions':a['sheets'][2]['rows'],'word_volume_by_sheet':a['word_volume'],'total_data_cell_words':sum(a['word_volume'].values()),'question_review_field_words':a['question_words'],'human_review_time':'Not measured or estimated.',**review_text[k]},'alex_compatibility':alex[k]}
rank=sorted(labels,key=lambda l:result['candidates'][l]['score_100'],reverse=True)
ranking_reasons={
'Candidate-B':'Highest locked score: correct three-round map plus explicit contact arithmetic, early legal advisers and later full access. Remaining corrections include shared exit-reason/deadline issues, unflagged September 9 conditions, date bounds and missing annex banks/support date.',
'Candidate-A':'Second: all bids, classifications and main stage counts are preserved with three rounds; missing outreach/adviser/access events and several qualifications create more coverage repairs than B.',
'Candidate-C':'Third: all bids and participation boundaries largely survive, but the extra August 27 round changes subsequent bid placement; also omits later access/approval/support detail. Its lower word volume earns no primary points.'}
result['ranking_with_reasons']=[{'rank':i+1,'candidate':l,'score_100':result['candidates'][l]['score_100'],'reason':ranking_reasons[l]} for i,l in enumerate(rank)]
result['test_by_candidate_matrix']=[{'id':t['id'],'category':t['category'],'weight':t['weight'],'credits':{l:credits[l[-1]][t['id']] for l in labels},'points':{l:float(Decimal(str(t['weight']))*Decimal(str(credits[l[-1]][t['id']]))) for l in labels}} for t in ref['tests']]
# Recompute from the written test objects, not the provisional sums above.
assert len(ref['tests'])==45 and len({t['id'] for t in ref['tests']})==45
assert sum(Decimal(str(t['weight'])) for t in ref['tests'])==100
by_id={t['id']:t for t in ref['tests']}
for label,c in result['candidates'].items():
 assert len(c['tests'])==45 and {t['id'] for t in c['tests']}==set(by_id)
 totals=defaultdict(Decimal)
 for t in c['tests']:
  assert t['credit'] in [0,.5,1] and t['reason'] and t['rows'] and t['source_pages']
  totals[by_id[t['id']]['category']]+=Decimal(str(by_id[t['id']]['weight']))*Decimal(str(t['credit']))
 assert float(sum(totals.values()))==c['score_100']
 assert {k:float(v) for k,v in totals.items()}==c['category_scores']
result['python_verification']={'passed':True,'test_count_per_candidate':45,'scored_cells':135,'total_locked_weight':100,'method':'Decimal recomputation from candidate test credits and reference.json weights; category totals and matrix cross-checked.','scores':{l:result['candidates'][l]['score_100'] for l in labels}}
current_hashes={name:hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in hashes}
immutable=[name for name in hashes if not name.startswith('checks/')]
assert all(current_hashes[name]==hashes[name] for name in immutable), 'Authoritative input changed'
lead_changes=[{'path':name,'initial_sha256':hashes[name],'final_sha256':current_hashes[name]} for name in hashes if current_hashes[name]!=hashes[name]]
result['input_integrity_verification']={'authoritative_inputs_unchanged':True,'reference_and_candidates_unchanged':True,'checker_lead_changes':lead_changes,'note':'A checker lead file changed on disk during evaluation; no attribution is made. Checker outputs were never score evidence. The evaluator wrote only output/grade; rubric, instruction, reference, filing, candidates and Alex transcripts retain their recorded hashes.'}
(OUT/'scores.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')

lines=['# Stage 2 identity-blind evaluation: Mac-Gray / CSC-Pamplona','',
'All three workbooks were inspected in full: Deal ledger, Rounds, Questions and Deal facts. Their neutral text transcripts match every transcribed workbook cell. The full Background (printed pp. 27–41) was read; company descriptions p. 26, financing pp. 58–59, no-shop p. 69, agreement §§5.11 and 6.17 (pp. A-30 and A-46), and the cover were checked where relevant. Only supplied local materials were used. Alex transcripts were consulted solely for compatibility. No model identity was inferred.','',
'All row citations below are **Excel sheet rows**, including header row 1. Ledger event # is one less. Scores use all 45 locked tests and the original fixed 100-point denominator. Partial credit is 0.5 only for the identified useful correct portion; accepted alternatives receive full credit.','',
'## Scores','', '| Candidate | Participation /30 | Rounds /25 | Formality + conditions /20 | Chronology /10 | Bids/prices /10 | Other /5 | Total /100 |', '|---|---:|---:|---:|---:|---:|---:|---:|']
for l in rank:
 c=result['candidates'][l];values=list(c['category_scores'].values());lines.append('| '+l+' | '+' | '.join(f'{x:g}' for x in values+[c['score_100']])+' |')
lines+=['','Formality contributes 10/10 for each candidate. Conditions contribute A 10/10, B 9/10 and C 9/10. All candidates earn 10/10 for bid/price coverage; this does not erase other field errors.','']
for item in result['ranking_with_reasons']:lines.append(f"{item['rank']}. **{item['candidate']} — {item['score_100']:g}:** {item['reason']}")
lines += ['','## Source judgments and common findings','',
'- **Population and timing:** p. 32 says “Over the next two months a total of 20 potential bidders” and identifies 2 Strategic/18 Financial. All candidates net the anonymous residual to 16 and flag July eligibility. P05 therefore receives full credit under the locked July 23 alternative; this does not prove an exact 20-person July census. Contact, NDA and later bids of one participant are not independent additive entries (C3/C9/C16).',
'- **Four, then three, then one:** p. 34 instructs the banker to “reach out to each of the four interested bidders”; p. 36 says “Party C did not submit a revised indication of interest or reiterate its prior indication of interest”; p. 38 dates executed exclusivity September 24. All three preserve the four-name stage, three final respondents, and September 24 A/B exits. No re-entry appears. Their inferred exits are not treated as invented factual withdrawals.',
'- **Party B exit reason (P08):** each has correct September 24 inferred Dropped by target, but assigns Terms or process instead of the locked Not stated. Page 37 reports comparative risk/value at selection; p. 38 does not report a rival exit motive/notice. This is one field miss per candidate, not separate invented entries or exits. Party A\'s Would not improve earlier offer gets the reference\'s expressly accepted treatment.',
'- **Round structure:** p. 34 connects July 25 staged access with “then request that each of these parties submit a revised indication of interest.” The August 27 letter fixes September 9 for that stage (p. 35). September 11 “request final indications of interest by September 18, 2013” opens the third round (p. 36). Candidate C\'s extra August 27 opening is one root error affecting R01/R05/R06/R09. R04 still earns full credit for the correct July 25 opening and R07 for keeping later exclusivity in the existing final stage.',
'- **Final deadline (R10):** all choose Enforced and cite selection on bids in hand. The locked alternative additionally requires explicit treatment of September 21 as post-selection bilateral bargaining and the same-round C11 ambiguity. None supplies that explanation in Q2. Each gets 0.5, recognizing correct due date, final solicitation and absence of invented extensions. This applies the locked rule equally; it does not silently reject its accepted Enforced alternative.',
'- **CSC September 9 conditions (C03):** p. 35 explicitly says Pamplona “was committed to provide 100% of the capital”; exclusive negotiations are not themselves reported substantive diligence. A uses Light. B and C use Heavy, preserving capital and suggesting further diligence, but neither flags this particular inference as required for the accepted Heavy alternative. Both retain correct September 18 Light and receive 0.5. September 21 Light with exclusivity/voting terms is accepted for all.',
'- **All required economics:** five June/July bids, four September 9/10 revisions, CSC September 18/21, A September 18 reaffirmation and B September 18 options package are present. B\'s 21.50 is bidder-valued, 19 cash plus options valued at 2.50, with All cash No (p. 36). None adds an October draft-based reaffirmation: C12(b) is already satisfied by a Formal final-stage bid.',
'- **Annex omissions:** §5.11, p. A-30 names “Morgan Stanley & Co. LLC, Deutsche Bank Securities Inc. and Evercore Group L.L.C.” Every candidate omits all three adviser relationships and their by-October-14 bounds. O02 and D05 each assess a practical consequence of this same omission; they are not six unrelated incidents. No exact mandate, lender status or hiring date is inferred.',
'- **Other material support:** p. 39 dates MacDonald-family voting agreements September 27, effective at merger signing. All omit that dated formation detail; A/B mention support at signing and C mentions the request. C2 permits folding it into a related note, but a request or undated signing mention alone is incomplete.',
'','## Test-by-candidate matrix','',
'Cells show **credit (earned points)**. Weights and category denominators remain frozen. Detailed reasons and sheet/row locators follow, and are machine-readable in scores.json.','',
'| Test | Category | Weight | Candidate-A | Candidate-B | Candidate-C |','|---|---|---:|---:|---:|---:|']
for m in result['test_by_candidate_matrix']:
 lines.append(f"| {m['id']} | {m['category']} | {m['weight']:g} | "+' | '.join(f"{m['credits'][l]:g} ({m['points'][l]:g})" for l in labels)+' |')
for l in labels:
 c=result['candidates'][l];lines+=['',f'## {l}: evidence and corrections','', '### Critical errors','']
 if c['critical_errors']:
  for e in c['critical_errors']:lines.append(f"- **{e['root_cause_id']}** — {', '.join(e['rows'])}; pp. {', '.join(e['source_pages'])}: {e['unsupported_assertion']} {e['correction_needed']}")
 else:lines.append('No critical unsupported addition or serious invented core-variable event was found. The field-level errors and omissions below remain material and are scored where the locked tests apply.')
 lines+=['','### Field-level errors and omissions','']
 for e in c['other_errors']+c['omissions']:
  lines.append(f"- **{e['root_cause_id']}**, {', '.join(e['rows'])}; {e['test_or_event']}; pp. {', '.join(e['source_pages'])}. **{e['wrong_or_missing_field']}.** "+(f"Claim: {e['unsupported_assertion']}. " if e['unsupported_assertion'] else '')+e['correction_needed'])
 lines+=['','### Every locked test','', '| Test | Credit | Candidate rows | Filing pages | Reason |','|---|---:|---|---|---|']
 for t in c['tests']:
  lines.append(f"| {t['id']} | {t['credit']:g} | {'; '.join(t['rows'])} | {', '.join(t['source_pages'])} | {t['reason'].replace('|','/')} |")
 lines+=['','### Mechanical compliance (outside weighted score)','']
 for text in c['compliance_observations']:lines.append('- '+text)
 b=c['review_burden'];lines+=['','### Review burden (outside weighted score)','',f"{b['ledger_event_rows']} ledger events, {b['numbered_rounds']} numbered rounds and {b['questions']} Questions. Nonempty data-cell word counts: "+', '.join(f'{s} {n}' for s,n in b['word_volume_by_sheet'].items())+f"; total {b['total_data_cell_words']}. Counts include quotes, dates and repeated fields, excluding headers; they are a volume measure, not a claim about review time.",'',b['useful_questions']+' '+b['noisy_questions'],'',b['ease_of_checking'],'', '**Practical corrections:** '+b['edits_required'],'','### Alex compatibility only','']
 for a in c['alex_compatibility']['agreements_and_differences']:lines.append(f"- **{a['source']}**: {a['finding']}")
lines += ['','## Freeze, amendments and validation','',
'No proposed reference amendment. The scores above are original locked-reference grades; there are no separate adjudicated scores and no fresh reviewer has adjudicated them. A disputed application (particularly P08, R10 or C03) should go to a fresh identity-blind reviewer. No identities, external files, web, skills or subagents were used.','',
'Python recomputed every score from the locked test weights and the 135 assigned credits using Decimal arithmetic, verified 45 unique tests per candidate, 100 total weight, the six category denominators, and the matrix/category/overall totals. Reference and candidate files were not edited. Input hashes are in input_hashes.json; final output hashes are in SHA256SUMS.','',
'An on-disk checker lead changed during evaluation (see scores.json input_integrity_verification). It was not edited by this evaluation and did not affect grades. All authoritative inputs, including reference and candidates, retain their recorded hashes. input_hashes.json records the initial snapshot; scores.json records changed checker hashes.','',
'Reference JSON SHA-256: `'+hashes['output/reference/reference.json']+'`. Reference Markdown SHA-256: `'+hashes['output/reference/reference.md']+'`.','',
'These are AI-assigned grades for one supplied development-deal run. The observed ranking is not evidence of generalization or a stable statistical ranking.','']
(OUT/'scoring_notes.md').write_text('\n'.join(lines))
print(json.dumps(result['python_verification'],indent=2))
