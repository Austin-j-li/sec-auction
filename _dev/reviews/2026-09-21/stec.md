# sTec: substantive review of the current v1.11 workbook

**Verdict: usable after targeted corrections; process boundaries and some late-stage conventions require adjudication.** The workbook preserves the economically important rise to $9.15, withdrawal, return at $6.60-$7.10, and final $6.85. It is substantially better than a mere mechanically valid ledger. The principal confirmed issue is Company H's participation closure: it is dated as an observed May 23 exclusion instead of the earlier inferred closure required by the current instruction. The one-process choice also differs materially from Alex's newer two-process guidance, but the filing's uncertain last 2012 contact prevents treating that disagreement as an unambiguous source error.

## Coverage and reference quality

Reviewed every paragraph of Background of the Merger, P00551-P00663 (pp. 23-35), every current ledger event #1-#62, both Rounds rows, Q1-Q9 and all Deal facts. Cross-checked the projections discussion P00808-P00824 (pp. 45-46), buyer/adviser descriptions and merger-agreement references, and critical background text directly against `raw_filing/stec_2013-08-08_DEFM14A.htm`. Reviewed the full relevant voice section V0115-V0127 and recurring guidance V0131-V0143, V0146-V0153 and V0178. Current rules consulted include C3-C16 and D. Paragraph labels refer to the read-only exports in `/tmp/sec-extraction-review-20260921/stec/`.

Alex's older `deal_details` rows 7144-7171 are substantive hand-coding: 28 rows with named bidders, NDA dates, prices, types, exits and explanatory excerpts. They are not placeholders and are useful independent checks, but contain demonstrably coarse dates and different conventions. For example, Company F is `DropTarget` in AC7154 despite its own refusal in P00591; the current `Withdrew` is preferable. The old reference has $9.15 Formal in Z7164, $6.60-$7.10 Informal in Z7169 and $6.85 Formal in Z7170. Neither old dates nor old labels were treated as ground truth.

## Independent reconstruction

The November 2012 Company A approach was cancelled; a February 13, 2013 special committee and Company B approach restarted substantive activity after an uncertain roughly three-month gap. Company B declined before BofA's engagement. Company C was interested only in assets; Company D approached before the organized outreach. BofA began outreach April 1. Its reported population is exactly 18: 17 technology companies and one financial sponsor, divided into three whole-company IOI bidders, six asset-interested parties and nine uninterested parties (P00585).

There are exactly six sale-process NDA counterparties: E, D, F, G, WDC through its April 17 addendum, and H on May 8 (P00587, P00590, P00607). F refused further participation April 24; E was dropped shortly thereafter; G withdrew May 3. WDC and D received the May 3 solicitation, G received it April 26, and H joined later. D's May 10 submission was late; no target-granted extension is reported. H's May 15 bid was not necessarily late because it entered after the date was set.

On May 16 only WDC and D were sent the final-round letter and agreement. H's inadequate price did not secure admission. WDC submitted $9.15 with a markup May 28; D sought more time. A May 29 best-and-final request was due May 30, when WDC confirmed its price and the board chose to proceed with it. WDC stopped May 31, D had a renewed opportunity and disengaged June 5, and WDC returned June 10 with a much lower range. The target requested a specific best offer June 11; $6.85 arrived June 14; signing and announcement occurred June 23 and June 24 respectively.

Under current C8, two organized rounds are strongly supported: April 1 outreach and May 16 final-round solicitation. Keeping later improvement requests within the already-final second round follows the current rule. That rule should not be silently replaced by an older model's or banker's preferred numbering.

## Findings

### S1. Company H closure uses the wrong transition and overstates the observed date

**Confirmed current-instruction error. Severity: medium, high confidence.** Cells: Deal ledger B40, E40, N40, O40, T40, U40, V40 and P40 (event #39); related P39 (#38), Rounds E3/J2 and Questions C5-F5.

The workbook calls H `Dropped by target` on **05/23/2013**, not inferred, quoting H's statement that it "remained interested" but "was not able to increase its indicated value range" (P00621, p. 30). That statement supports refusal to improve; it does not report a target exclusion on that date. Earlier, the complete advancing set is WDC and D: "sent final round process letters and a draft merger agreement to WDC and Company D" after the May 16 board meeting (P00619-P00620, p. 30). P00618 also says H's range was "not sufficient to move them forward" while allowing a revised indication to be considered.

C16 requires inferred `Dropped by target` at the complete advancement decision, with Inferred = Y and Exit reason = Not stated. The minimum correction is a **by May 16** inferred closure, Date from May 15 (last supported live bid), Date to and Sort date May 16. Preserve H's May 23 inability to improve as a subsequent communication in the Note or an appropriate non-entry event. Do not claim the filing proves an observed May 16 withdrawal or invent a May 23 re-entry: willingness to receive a revised proposal alone is not readmission under C3.

The present Question is useful but omits the current-rule alternative: it offers May 23 versus signing. Its later refusal-to-improve evidence must not be projected backward into the inferred May 16 exit reason. Consequence: one extra live bidder is incorrectly carried from May 16 to May 23; the identity of the target's finalist set is correctly recorded separately.

### S2. Light conditions on the $9.15 sequence rest on an insufficiently established diligence characterization

**Unsupported condition characterization under C14; materiality requires adjudication. Severity: medium; high confidence in the evidence gap, medium in the preferred replacement.** Cells: L42/P42 and L46/P46 (#41 and #45), Questions C6-F6.

The workbook says the May 28 offer contemplated June 3 signing, therefore "expedited diligence," and assigns Light. The filing actually says "contemplated signing definitive documentation ... by no later than June 3" (P00622, p. 30). On May 30 the board was still "endeavoring to complete diligence and negotiation of the merger agreement and ancillary agreements" (P00630, p. 31). It also discusses the founders' continuing review of the covenant not to sue. A short hoped-for signing timetable does not itself establish that the bid's diligence condition was only confirmatory, expedited or limited.

Under C14, recommend **Unclear** unless the signing objective is expressly accepted as enough to establish Light. Heavy is a separately defensible interpretation if the founders' unresolved covenants are material requirements, as existing Q5 already recognizes. None is unsupported: Alex's V0125 description of "no conditions" is useful guidance about why the markup makes this Formal, but the source does not establish unconditional readiness to sign. Do not infer financing status from silence or later signing. Economic consequence: the high $9.15 proposal may otherwise appear more executable than the contemporaneous evidence supports. The Formal label in K42/K46 is correct under C13 regardless of this decision.

## Newer Alex guidance and unresolved conventions

### S3. One process versus Alex's explicit two-process reading

**Newer-guidance mismatch, not a proven filing contradiction. Severity: high for research classification; confidence: high that there is a mismatch, medium on the boundary.** Cells: Deal facts B11, all ledger F cells from #6 onward, Rounds A2/A3, Questions C2/D2/F2.

Alex V0118 explicitly calls the November-February interval a "3 month gap" and identifies "two separate processes"; V0132 repeats this. The workbook chooses one process because the Company A cancellation contact is undated, so three contact-free months are not established. That qualification is grounded in P00559: after the November 14 contact, the bank followed up, a meeting was scheduled, then cancelled with concerns communicated to A. The next dated buyer contact is February 13 (P00566), and the special committee was formed that day (P00565). November 14-February 13 is about three months, but November 14 is not demonstrably the last contact.

C7 explicitly says not to round up a gap whose endpoint is undated. Its tests (a) and (c) are met, while (b) depends on how much uncertainty "about three months" tolerates. The ongoing internal strategic review does not itself defeat a break, because C7 excludes internal steps from buyer contacts. Recommend adjudicating the tolerance and then applying it consistently. The workbook's categorical "A process break ... is not supported" overstates the case; the two-process reading has real evidence and is Alex's expressed preference. If chosen, add an inferred restart on February 13, move subsequent events to process 2 and reconcile fresh first-contact accounting for A rather than borrowing its 2012 row into the 2013 outreach. No old live participant needs a fabricated individual exit.

### S4. The last deadline is marked Enforced despite accepted later bids in the same round

**Convention question with a literal C11 tension. Severity: medium; confidence: high in the tension.** Cells: Rounds G3, P48 (#47), Questions C4/D4/F4; compare #53/#55 (rows 54/56).

May 30 is `Enforced` because the board selected WDC then. Yet the same round includes WDC's June 10 range and June 14 price, both considered by the target (P00641-P00644). C11 gives `Late bids accepted` priority over `Enforced` where the bidder had the due date and the new bid's Date from is later. On a literal whole-round application, June 10 fits. A sensible contrary interpretation is that these are renegotiation after withdrawal and re-entry, after the original solicitation had been resolved. Current C11 does not expressly supply that exception. Existing Q3 discusses D's continued opportunity but does not resolve the later WDC bids. Decide whether later renegotiation after an acted-on deadline changes its outcome; otherwise apply the literal rule. Do not manufacture a new due date or a third round solely to preserve Enforced.

### S5. Company D's non-submission, re-entry and final exit

**Convention-dependent, already appropriately questioned. Severity: medium; confidence: medium.** Cells: E47 (#46 Did not submit), E51 (#50 Re-entered), E52 (#51 Withdrew), Questions row 7.

P00629 records the missed best-and-final submission; P00630 selects WDC; P00634 says D "had an opportunity to continue" and would consider it, followed by new responsive materials June 1 (P00635). P00640 expressly reports D disengaging June 5. C16 treats non-submission as a closure and allows re-entry, making the current sequence defensible. Economically, uninterrupted live interest is also plausible. There was no executed exclusivity with WDC. Do not turn preference for WDC into a reported exclusive arrangement or claim D permanently withdrew May 30. Existing Q6 is valuable and this is not counted as a confirmed error.

## Price and formality audit

All prices below are per share. BofA is the recipient/intermediary except the April 23 call also includes management. No material priced proposal in the background is omitted.

| Ledger event / cells | Filing basis | Assessment |
|---|---|---|
| #21, H22:I22, Apr 23 Company D >$5.60 | P00594, p. 28 | Correct one-sided low only, not a $5.60 point bid; consideration not stated; Informal. Additional diligence requirements support caution. |
| #25, H26:I26, May 3 WDC $6.60-$7.10 | P00603, p. 29 | Correct cash range, Informal, Unclear; no data-room access until May 10. |
| #32, H33:I33, May 10 D $5.75 | P00611, p. 29 | Correct cash point price, Informal; draft exclusivity request is not a merger-agreement markup. Late submission is correctly recognized. |
| #34, H35:I35, May 15 H $5.00-$5.75 | P00613, p. 29 | Correct cash range, Informal, Unclear. |
| #41, H42:I42, May 28 WDC $9.15 | P00622, p. 30 | Correct cash point price and Formal markup-based offer; conditions require S2 decision. |
| #45, H46:I46, May 30 WDC $9.15 | P00628, p. 31 | Correct explicit reaffirmation, not a new higher bid; Formal; conditions as S2. |
| #53, H54:I54, June 10 WDC $6.60-$7.10 | P00641, p. 32 | Correct lower cash range. Formal is defensible under continuing proposed May 28 transaction terms, despite old Z7169 = Informal. Q9 makes this visible. |
| #55, H56:I56, June 14 WDC $6.85 | P00643-P00644, p. 32 | Correct Formal best-offer response, cash point price; Light is more supportable here because subsequent diligence is described as including confirmatory calls. |

The June 10 return is not a mere continuation at $9.15, and June 14 is not retrospectively made formal only because it wins. The older written instruction's section 3.5 says any range is Informal; current C13 expressly permits Formal ranges and continuing definitive terms, so old Z7169 is not an automatic correction. No additional June 20 C12 reaffirmation is required once the latest bid is Formal in a final round. The May 31 withdrawal and June 10 re-entry comply with C16's explicit "for now" rule and are supported by P00632, P00636/P00639 and P00641. Old reference omission of the temporary withdrawal does not make the current rows wrong.

## Correctly captured and rejected apparent errors

- **Exactly six NDA parties:** rows 16-20 and 30 reconcile to the source. The WDC April 17 special addendum correctly brings its January 29, 2009 agreement into this sale; there is no new 2009 sale-process entry or duplicate count. This addresses V0121.
- **Soft May 3 deadline:** `Late bids accepted` in Rounds G2 is a more precise implementation of V0122-V0123. D, unlike H, received the date and then submitted May 10. No unsupported target extension was invented.
- **Final round May 16:** the source explicitly calls the letters "final round." V0124's "round two of informal bidding" and V0125's "not the final round" should not override that source and current C8 without a deliberate convention change. V0146's generalized mention of a third-round start does not identify a definite additional source transition. Old AC7162 and AC7166-7167 also record final announcement and extension, not an unambiguous third round.
- **Initiation and activists:** Deal facts B10 sensibly distinguishes target review from concurrent activist pressure; #4/#5 preserve Balch Hill and Potomac context. Adding Bahri to a committee is not a bidding-group formation, consistent with V0119-V0120.
- **Information differences:** #31/#33 distinguish WDC's May 10 data room and D's May 14 access. #59 records the June 19 Cost-Reduction Projections only after price agreement; P00817/P00824 establish that those differ from earlier Operating Projections. #58 correctly identifies Wells Fargo as WDC's financial adviser. No bidder-wide access to standalone cost-cut projections is invented.
- **Adviser relationships:** Company A's unnamed bank is not attributed to the target; C5 only requires other-party advisers when named. BofA retention uses March 26 board approval with March 28 engagement in the Note. Gibson Dunn, Latham, Shearman, Paul Hastings and Wells Fargo relationships are identified; the proxy solicitor is retained in facts.
- **Signing versus announcement:** #61 is June 23 and #62 is June 24, matching P00662-P00663 and V0126. The $3.59 reference share price is distinguished from the bid prices and given its own June 21 date.

## Limits and next decision

No gold-standard accuracy percentage is justified. Both the outreach membership of C versus B (existing Q2) and process-gap tolerance remain interpretation-dependent, while the six NDA identities and core price series are well supported. The workbook has not been changed. First correct the H inference/date representation, then adjudicate S2-S5 and the two-process voice preference before using continuous participation or deadline enforcement as estimation inputs.
