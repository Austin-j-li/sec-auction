# H1 — Dates, sequence and chronology

Slice: instruction §8 (8.1/8.2/8.3), §3 date aspects, §11.2 date columns, §12 B/C, §13 check 4.
Sources: `SEC_Deal_Ledger_Extraction_Instruction_v2.md`; `alex_collection_instructions.txt`; `alex_notes.txt`; `alex_hand_collected_9deals.txt` (269 rows, 9 deals); `model_review_2026-09-18/results/SEC_12_Extraction_Issue_Register.csv` (85 issues); the 12 workbooks in `extraction/`; filing backgrounds.

**Headline.** Austin's hypothesis holds, but narrowly and precisely. The instruction already assigns a working date to every *finite* window (and Pro enforces that — two findings ding models for *not* assigning). The whole gap comes from three sentences in §8.1 plus two in §8.2/§13.4 that (i) blank the date whenever a bound is one-sided, and (ii) forbid the two devices Alex actually uses — deadline-anchoring and predecessor-day anchoring. Net effect in the 12 workbooks: **62 of 706 ledger rows (9%) have no Working date**, concentrated on cohort NDAs, target-driven exits and non-submissions — exactly the rows Alex hand-dates. Second, and separate: where the instruction *does* assign a date, the blind **midpoint puts bid cohorts after the committee meetings that reviewed them** (Providence 05/25 vs the 05/23 review; 07/23–07/25 vs the 07/22 review). Alex's own convention is not "a rough date is fine" — it is "a date that satisfies the known before/after constraints", and the within-window choice depends on the event type.

## Findings

| # | Dir | Matters | Conf | One line |
|---|---|---|---|---|
| D1 | A | High | High | §8.1 blanks Working date for one-sided windows; Alex dates 267/269 rows |
| D2 | A | High | High | §8.1 "A deadline is not proof of arrival by that date" forbids Alex's default anchor |
| D3 | A/B | High | High | §12 example B contradicts Alex's own reading of the same Providence paragraph |
| D4 | A | High | High | §8.1 forbids placing an undated consequence on its deciding meeting's day; Alex does it routinely |
| D5 | A | High | Med-High | Blind midpoint places bid cohorts *after* the meetings that reviewed them (2 clean cases) |
| D6 | A | Med | High | No column is guaranteed monotone: # is reading order, Working date "need not increase" |
| D7 | C | Med | High | Date basis records the *source's* precision, never the *assignment rule* Alex complains about |
| D8 | C/A | Med | Med-High | An inferred, never-communicated effective deadline cannot be recorded; Alex records one |
| D9 | A/C | Med | High | Enforced/Extended/Unclear lives in Summary prose only, not in a ledger field |
| D10 | E | — | High | Finite-window midpoint + "populate the native dates" = what Alex wants; Pro enforces it |
| D11 | E | — | High | §8.2/§8.3/§13.4 same-day ordering, deadline-set vs due date, execution vs announcement all match Alex |
| D12 | D | Low | High | A Minor defect scored for 11/01 vs 10/31 on a window Alex would date 11/02 |
| D13 | F | Med | High | Alex's own cohort convention inverts a dated event and bunches contacts with NDAs |
| D14 | F | Med | Med | `date_precise` vs `date_rough` semantics in his sheet — needs a ruling from Alex |

---

**D1 — One-sided windows lose the date (A, High, High).**
Instruction §8.1: *"For a one-sided or unbounded window, leave Working date blank."* Table row: *"No supportable date | Leave numeric date fields empty and retain any supported position in the sequence."* §3.3: *"Leave unsupported numeric and date cells empty, never zero."*
Alex: of 269 hand-collected rows, **2 have a blank date** — Saks 7012 (Sponsor G Drop) and 7014 (Company H Drop), both rows he elsewhere marks junk (*"Should be deleted: unsolicited letter, no NDA, no further contact"*). His complaint is not that dates are assigned but that they are assigned badly — Providence item 2: *"date_assigned is oftentimes interpolated incorrectly, from the lower bounds and upper bound on the date that can be extracted from deal backgrounds."* Summary H: *"Exact dates are less interesting to me, but the order of events must be precise."*
Consequence: 62 blank Working dates across the 12 workbooks (counts below). The four Providence `Dropped by target` rows for Parties C/D/E/F — which Alex hand-dates 07/27/2016 (rows 6046–6049, `DropTarget`) — are blank in glm (4), sol (4) and opus (2). Providence NDA cohorts (his row 6027, 03/28/2016) are blank in opus, ds, sol.
Fix: replace with "assign a working date whenever any bound or anchor exists; leave blank only when nothing in the filing positions the event."

**D2 — Deadline-anchoring is forbidden (A, High, High).**
§8.1: *"Tighten a window only when a passage actually constrains that event. **A deadline is not proof of arrival by that date.**"*
Alex, Providence row 6035 (Party B, $24 LOI), comment: *"Late july -- but the deadline was july 20"* → `date_rough` **07/20/2016**; the same for Parties E, D, C, F (rows 6036–6039). Providence row 6029: nine IOIs received *"Between May 19, 2016 and June 1, 2016"* → **05/19/2016**, the (postponed) IOI deadline. Consequence: all four models put the nine IOIs at **05/25** and the five undated LOIs at **07/23** (opus, ds, sol) or **07/25** (glm) — see D5.
Fix: add "when a solicitation deadline governs the window and no evidence places the event later, the deadline day is the default assigned date (Date basis: Deadline-anchored)."

**D3 — Calibration example B contradicts Alex on the same paragraph (A/B, High, High).**
§12 B: *"The other late-July LOIs are not all established as received by July 22 or before G&W. Where the review context supports it, July 27 bounds receipt of the offers it considered."*
Alex, Providence item 9: *"the deal background states that these bids happen in late July 2016. That's July 20 to July 31. The deadline of round two is July 20, but one of the bidders submits the bid on July 21. And then the Transaction Committee of the target meets on July 22. **This very narrowly limits the timing of round two bids to July 20 to July 22.**"* The filing supports him: *"The Transaction Committee met by telephone conference on July 22, 2016 and in person after the regular quarterly Board meeting on July 27, 2016, to review the LOIs"* (bg p.29–30) — the July 22 meeting reviewed LOIs, so at least part of the cohort was in by 07/22.
This is the clearest case of the instruction encoding a *narrower* epistemic standard than the data user, on the very example Pro chose to illustrate the rule.
Fix: Austin should put the July 22 reading to Alex and, if confirmed, rewrite B to endorse the tightening and keep only the "does not become an announced July 27 deadline" half.

**D4 — Predecessor-day / decision-day anchoring is forbidden (A, High, High).**
§8.1: *"Do not invent the missing endpoint or **assume a subsequent event happened on its predecessor's day**"*; *"Explain strict before/after bounds and same-day sequencing in the reason rather than silently shifting a date by a day."*
Alex does this systematically: Providence rows 6046–6049 — the four `DropTarget` exits, undated in the filing (*"representatives of GHF **subsequently** contacted the remaining bidders to inform them that they were no longer involved"*) — all dated **07/27/2016**, the committee day. Rows 6030/6031 — 16 `Drop` + 2 `DropTarget`, undated — both **06/01/2016**, the committee day. Mac-Gray item 8: *"the actual date of the dropout event is September 24"* — the exclusivity-execution day — for Party A and Party B, who are never individually dated in the filing.
Pro's own register penalises models for Alex's convention in one direction and for the alternative in the other: **PW-DS-04** (Moderate, *"Overprecise selection date … made exact June 1"*) dings ds for choosing exactly Alex's 06/01; **PW-GLM-06** dings glm for an *"artificial next day"* 07/28 while opus, which also used 07/28, and sol/glm, which left the rows blank, are equally far from Alex's 07/27.
Fix: allow "Predecessor-day" as an explicit assignment method with Date basis `Inferred day`, and drop the blanket prohibition.

**D5 — The blind midpoint breaks real order (A, High, Med-High).** Two clean cases, both Providence:
- Nine IOIs, filing *"Between May 19, 2016 and June 1, 2016, the Company received nine written indications of interest"*; *"The Transaction Committee met … on May 23, 2016 and again on June 1, 2016 to consider the IOIs."* Instruction midpoint → **05/25** in all four workbooks (opus #21, glm #20, ds #19, sol #19). A sort therefore shows the IOI cohort arriving *after* the May 23 meeting that considered IOIs. Alex: 05/19.
- Five undated late-July LOIs → **07/23** (opus #34–38, ds #31–35, sol #28–33) / **07/25** (glm #30–36), i.e. after G&W's dated 07/21 LOI and after the July 22 review. Alex: 07/20, before G&W.
§8.1 already contains the cure — *"A committee review can bound offers it demonstrably considered"* — but §12 B tells the model not to apply it here, and nothing tells the model that the assigned point inside the window must respect other rows' dated events.

**D6 — Nothing in the ledger is a guaranteed chronology (A, Med, High).**
§11.2: *"# | Reading order … **Not a claim that all adjacent events have a known relative order.**"* §8.2: *"**Working dates need not increase down the ledger.** Never change facts or bounds to make assigned dates sort neatly."* §13 check 4: *"Working dates are assigned only under section 8 and **do not create historical order**."* §2: *"any bounded-window working date is an explicitly assigned convenience, not an observed date or proof of sequence."*
Alex's data model is the opposite: `bidderID` *"really just enumerates events in their historical order … so my dataset has non-integer numbers (e.g., if an IB signed a confidentiality agreement between event 1 and 2 … I would give 1.5)"*; summary H: *"the order of events must be precise."* He needs one column that sorts and one that breaks ties; the instruction guarantees neither.

**D7 — Date basis describes the source, not the assignment (C, Med, High).**
§8.1: *"Date basis is Reported day, Inferred day, Reported interval, Approximate window, Relative only or Undated."* None of these says *how* the working date was picked — the exact thing Alex complains about: *"date_assigned is oftentimes interpolated incorrectly, from the lower bounds and upper bound on the date that can be extracted from deal backgrounds"* (Providence item 2). A reviewer cannot filter for "dates I would re-do".

**D8 — An inferred effective deadline cannot be recorded (C/A, Med, Med-High).**
Alex, Providence row 6058: `Final Round | 08/12/2016`, comment *"The deadline apparently was not announced to the bidders, this was the time when the English auction was stopped by the target."* Voice-note addendum to item 9: *"July 27 is a fair assessment of the deadline."*
§8.3: *"**Deadline:** the scheduled due date itself, clearly a milestone rather than a submission or enforcement action"*; *"Preserve every stated deadline version"*; §12 B: *"it does not become an announced July 27 submission deadline."* The stated-deadline framing plus B leaves no slot for a never-communicated effective close. (The July 27 case is largely absorbed: Alex encodes it as `Final Round Ann` = the next round's start, which maps cleanly onto `Round opened`, and all four models produced a dated 07/27 Round opened. The 08/12 case is not absorbed.)

**D9 — Enforcement lives only in Summary prose (A/C, Med, High).**
§8.3: *"For each relevant deadline, the Summary map states **Enforced**, **Extended**, **Late bids accepted**, **Unclear**, or **No deadline stated**."* This is exactly Alex's ask (STEC item 5: *"I am wondering if it will be useful for us to record when round deadlines have been enforced and when they haven't … this is something that is critical for the analysis of sale processes"*), but his database is row-based — a Summary-only classification will not reach his `bid_note` column. Cheapest fix: a Deadline-status value in Terms or outcome on the Deadline row, mirrored to Summary.

**D10 — Genuine match: finite windows do get dates (E).**
§8.1: *"For a finite window, Working date defaults to its calendar midpoint."* Pro enforces it *for* completeness: **PS-DS-08** (*"Four rows have finite Date from/Date to windows but no Working date"*, adjudication: *"Apply the instruction's earlier-rounded midpoint … June 10, September 20, November 18 and November 15"*) and **PW-DS-03** (*"Party B's April 21 meeting is readable in When, but Date from, Date to, Working date and Date basis are empty … Populate the three native dates"*). Both are pro-Alex findings. Worth saying plainly: Pro is not anti-date; it is anti-unsupported-precision.
Also note the 2026 complaint in Alex's Providence item 9 — Party C's 07/12 bid recorded *after* its later-bidding rivals — is **fixed** in all four workbooks, precisely because they assigned midpoints instead of leaving the cohort undated.

**D11 — Other genuine matches (E).** §8.2 *"# orders the reading, respecting exact dates and supported precedence, **including same-day revisions**"* + §13.4 *"Same-day price revisions retain their known sequence"* answer PetSmart item 4 (*"on November 2, a single bidder submits two bids … event_order for these bids is reversed … arrange bids by the same bidder on the same day in the order in which they appear"*). §8.3's Deadline set / Deadline revised / Deadline trichotomy answers Providence item 7 (*"difficulties distinguishing between the date on which a round deadline has been set and the date on which it has expired"*) and PetSmart item 6 (Dec 5 → 10 → 12). *"Record extensions even when they do not create a round"* matches summary B. §8.3's *"A hoped-for signing date or the last board meeting is not a bid deadline"* and the signing/announcement separation match summary I and Providence item 15.

**D12 — Convention-compliance noise (D, Low, High).**
**PS-SOL-04** (Minor): *"For the October 30–November 2 revision window, Working date is November 1 rather than the earlier-rounded midpoint October 31."* Alex's own value for that row (6435) is **11/02/2014**. A reviewer item is spent on a one-day difference inside a cell Alex would overwrite anyway. Low stakes, but it is the type specimen of effort spent on the convention rather than the datum.

**D13 — Alex's convention has a real cost (F, Med, High).**
His Providence row 6027 — *"25 parties, including Parties A, B | 11S, 14F | NDA | 03/28/2016"* — dates the whole NDA cohort to the contact week (*"During the week of March 28, 2016 … representatives of GHF contacted 11 potential strategic buyers … and 18 potential financial buyers. Each of the potential strategic buyers and 14 potential financial buyers **subsequently** executed confidentiality agreements"*). But Party B's first contact is **April 21** (*"Subsequently, on April 21, 2016, the Company and representatives of GHF held an introductory meeting with another potential strategic buyer ('Party B')"*), so his cohort row places Party B's NDA three weeks before Party B was contacted — and it merges contacts with NDAs, which his own Providence item 3 forbids: *"There seems to be a bunching of events such as when the bidders get contacted versus when they sign non-disclosure agreements … they should be separate."* Austin should not adopt "date the cohort at the contact day" as a blanket rule; the constraint-based rule in Q4 gets 03/28 for the contacts row and "after 03/28, and after 04/21 for named late joiners" for the NDA row.

**D14 — `date_precise` vs `date_rough` (F, Med, Med).**
His email: *"In my edited 9 deals, I did not bother with this distinction and simply edited bid_date_rough."* In the file: 82/269 rows have a blank `date_precise`, 2 have a blank `date_rough`, and 37 rows disagree. The disagreements look like **stale Chicago values carried along when he inserted rows**, not a precise/rough distinction: Providence 6024 `Bidder Interest` carries `precise=07/22/2016` against `rough=12/31/2015` (the Q4-2015 row Austin flagged — 07/22 is the Chicago Party A drop date); sTec rows 7144/7145/7146 all carry `precise=04/04/2013`, the neighbouring NDA row's date; Mac-Gray 6956 `Final Round` carries `precise=09/11`, the adjacent `Final Round Ann` date. The `Executed` rows are the clearest tell: Providence 6059 `precise=08/15` (announcement) vs `rough=08/12` (execution), and his item 15 says these are *two different events needing two rows*, not two date columns.
Working conclusion: **treat `date_rough` as his single operative date**; do not build a two-column precise/rough design on this evidence. Question for Alex: *"Is bid_date_precise maintained at all, or legacy? Do you want one assigned date plus a bounds pair, or two dated columns?"*

## Blank Working dates in the 12 workbooks

| Workbook | Ledger rows | Blank Working date | What they are |
|---|---|---|---|
| opus_providence | 70 | **14** | 2 NDA cohorts, Party B + G&W NDAs ("date not disclosed"), 2 `Dropped by target`, 2 `Did not submit`, Party D `Withdrew` + exclusivity, Deadline set/revised |
| sol_providence | 56 | **12** | 2 NDA cohorts, 4 `Dropped by target`, 2 `Did not submit`, Deadline set, `by`-dated rows |
| glm_providence | 62 | **10** | 4 `Dropped by target`, 2 `Did not submit`, Deadline set, 2 adviser rows, 1 contact |
| ds_providence | 55 | 6 | 2 NDA cohorts, Party B's dated 04/21 contact (native cells empty), Deadline set/revised |
| ds_petsmart | 55 | 6 | the 27-contact cohort, activist window, Deadline set, group change, Nov update |
| opus_petsmart | 66 | 4 | adviser, 2 eliminated submitters `Dropped by target`, group change, Nov update |
| glm_petsmart | 57 | 3 | Target decision, **9 non-submitting NDA signers**, Q3-earnings update |
| glm_mac-gray | 58 | 2 | the 15 + 35 contact cohorts |
| sol_mac-gray | 52 | 2 | the 14 + 35 contact cohorts |
| sol_petsmart | 51 | 2 | 2 `Dropped by target`, Deadline set |
| ds_mac-gray | 60 | 1 | Deadline set |
| opus_mac-gray | 64 | 0 | — |
| **Total** | **706** | **62 (9%)** | |

Rows whose chronological position becomes ambiguous for a downstream sort: the four Providence `Dropped by target` rows (Alex: 07/27/2016) sort nowhere in glm/sol; the two Providence NDA cohorts (25 signers — the deal's entire participant population; Alex: 03/28/2016) sort nowhere in opus/ds/sol; PetSmart's 27-contact cohort (the single largest participation event; Alex has no row, the models' window is mid-Aug–end-Oct) sorts nowhere in ds; glm_petsmart's 9 non-submitting NDA signers — the row Alex explicitly asks for in PetSmart item 5 — sorts nowhere.

## Answers

**Q1. What Alex wants; what the instruction delivers.**
He wants (i) an event order that is right — `bidderID` *"enumerates events in their historical order"*, with fractional inserts; and (ii) a usable date on every row — 267/269 populated, the two exceptions being rows he wants deleted. Exactness is explicitly secondary: *"We want to know the sequence of events but not necessarily the exact date"* (March email); *"Exact dates are less interesting to me, but the order of events must be precise"* (summary H).
Rules that blank a date, forbid tightening, or forbid a contextual exact date. Alex would accept a blank only under rule 2 — when nothing in the filing anchors the event — and his own sheet shows he almost never finds that condition met (2/269):
1. §8.1 *"For a one-sided or unbounded window, leave Working date blank."* — not acceptable; this is the source of most of the 62.
2. §8.1 table, No supportable date: *"Leave numeric date fields empty and retain any supported position in the sequence."* — acceptable only if "supported position" is itself sortable, which it is not (D6).
3. §8.1 *"A contextual exact date requires actual evidence, not an interpolation rule."* — contradicts his 07/20 and 05/19 anchoring (he treats the deadline *as* the evidence).
4. §8.1 *"Tighten a window only when a passage actually constrains that event. A deadline is not proof of arrival by that date."* — directly contrary to his practice.
5. §8.1 *"…a committee review can bound offers it demonstrably considered, not all offers discussed in a paragraph covering several meetings."* — the safe half he agrees with; §12 B then withdraws it for Providence.
6. §8.1 table, "By [day]": *"Upper bound only unless an earlier bound is independently supported."* — produces blanks on `Deadline set` rows in 5 workbooks; he always dates these.
7. §8.1 table, "After/before/subsequently": *"Do not … assume a subsequent event happened on its predecessor's day."* — contrary to his 07/27 and 06/01 exits.
8. §8.1 *"Explain strict before/after bounds … rather than silently shifting a date by a day."* — fine as a transparency rule, not as a prohibition.
9. §3.3 *"Leave unsupported numeric and date cells empty, never zero."* — fine for prices; harmful for dates.
10. §8.2 *"Working dates need not increase down the ledger."* / §13.4 *"…do not create historical order."* — these deny him the product.
11. §12 B — see D3.
Counts and examples: table above.

**Q2. Every date-related register finding.** 25 of the 85 issues touch dates; only 5 bear on sequence.

| Issue | What the model did | What Pro wanted | What Alex would want | Harmless / helpful / harmful |
|---|---|---|---|---|
| **PW-GLM-06** (Mod) | late-July LOIs bounded 07/20–07/31, WD 07/25; exclusions shifted to 07/28 | bound by the 07/27 review; no "artificial next day" | LOIs **07/20** (deadline), exits **07/27** (committee day) | **Harmful** — 07/25 lands after the 07/22 review of the LOIs and after G&W's 07/21; Pro's own fix (≤07/27 → midpoint 07/23) still does |
| **PW-DS-04** (Mod) | advancement/exclusion made exact 06/01 | retain the 05/23–06/01 review window | **06/01** — his rows 6030/6031 use exactly that | **Helpful**; the finding penalises Alex's own convention |
| **PW-GLM-05** (Mod) | NDA cohorts bounded 03/28–04/27; selection exact 06/01 | don't borrow the neighbouring announcement as a terminal NDA date | NDA cohort **03/28**; selection 06/01 | Upper bound 04/27 is over-tight (Party B contacted 04/21, NDA after) but **harmless for order**; the 06/01 half is helpful and wrongly flagged |
| **PW-SOL-03** / **PW-DS-07** (Mod) | Party D's "would not proceed … at that time" fixed to 08/02 as *Reported day* | widen/qualify the date | **08/02** (his row 6053, `Drop`) | **Helpful.** The filing's paragraph is anchored at 08/02 ("Party E withdrew its revised proposal on August 2, 2016 … at which point Party D indicated that it would not proceed"). Pro's objection is to the *Reported day* basis, which is fair; the date is right |
| **PW-DS-03** (Mod) | 04/21 meeting readable in When, native date cells empty | populate them | same | **Helpful**, pro-Alex |
| **MG-GLM-02** (Mod) | 16 residual NDA signers bounded 06/28–08/05, WD 07/17 | preserve the source's "next two months" (06/24–08/24) | **07/15** (his row 6934) | GLM's 07/17 ≈ Alex. Pro's fix widens to a midpoint of **07/24**, which is *after* the 07/23 IOI deadline those signers were being furnished packages for — **harmful**; opus/ds/sol all already sit at 07/24 |
| **MG-GLM-05** (Major) | Party A and B `Dropped by target` 09/21 | no dated exclusion; use `Participation paused`/last-seen | **DropTarget 09/24** (rows 6958/6959; item 8: *"the actual date of the dropout event is September 24"*) | GLM's 09/21 is 3 days early — mildly **harmful**; Pro's fix removes the event Alex wants entirely. opus/ds date it 09/24 = Alex, but label it `Participation paused`, not an exit (exits slice) |
| **MG-OPUS-04** (Mod) | Moab's no-rollover decision dated 10/07 as *Reported day* | retain the 09/25–10/07 window | not in his ledger (not a bid event) | **Harmless** for order (it sits inside the drafting window); a basis-label defect only |
| **MG-DS-03 / MG-GLM-01 / PS-GLM-06** (Mod) | called deadlines *Enforced* on the strength of observed arrivals | enforcement needs positive support | he wants enforced-vs-soft recorded (STEC item 5) but as a judgment, flagged | **Helpful in kind, harmful in strength** — Pro is right that inference ≠ evidence, but a blanket "Unclear" loses a variable he calls critical |
| **PS-OPUS-06** (Mod) | Bidder 2's revision asserted to be after 10/30, used to establish accepted lateness | keep 10/30–11/02; call lateness unresolved | **11/02** (his row 6435) — i.e. he makes the same call | Date **helpful**; the *conclusion* (deadline not enforced) is what Alex wants flagged, not suppressed |
| **PS-SOL-04** (Minor) | WD 11/01 instead of midpoint 10/31 on the same window | 10/31 | 11/02 | **Harmless** — pure convention noise (D12) |
| **PS-DS-08** (Mod) | 4 finite windows with no Working date | apply the midpoint | dates on all rows | **Helpful**, pro-Alex |
| **PS-OPUS-07** (Mod) | called the 12/05 → 12/10 move an *acceleration* | it is an extension | extension (his `Final Round Ext Ann/Ext` rows; item 6) | **Helpful**, aligned |
| **PS-OPUS-08 / PS-SOL-08 / PS-DS-10 / PS-GLM-12** (Mod) | followed the background's July 3 JANA date without flagging the Reasons section's July 2 | flag the conflict | he uses **07/03** (row 6409) | **Harmless for order**; reviewer-workload cost only, ×4 workbooks |
| **PW-SOL-02** (Mod) | July 20 due date kept inside the Round opened row, no separate Deadline row | add the milestone row | he has both (`Final Round Inf Ann` 06/15, `Final Round Inf` 07/20) | **Helpful**, aligned |
| **MG-SOL-04** (Mod) | 09/18 bid points at a deadline row as its prior offer | point at the prior bid | same | Helpful, not a dating issue |
| remainder (PS-DS-03, PS-DS-05) | price-bound direction, group consolidation | — | — | not date findings |

**Q3. Where assigning a date goes wrong.**
*(a) The assigned date only has to be consistent with a known partial order — and a blind midpoint can violate it:*
- **Providence nine IOIs.** Bound: received 05/19–06/01; the 05/23 committee met "to consider the IOIs", so at least some were in by 05/23. Midpoint **05/25** (all four models) violates that bound for part of the cohort. 05/19 (Alex) or 05/23 satisfies everything.
- **Providence five late-July LOIs.** Bounds: due 07/20; both the 07/22 and the 07/27 meetings were "to review the LOIs"; G&W's dated 07/21. **07/23/07/25** puts the cohort after the 07/22 review. 07/20 satisfies every bound.
- **Mac-Gray 16 residual NDAs.** Midpoint of "over the next two months" = **07/24** (opus, ds, sol), one day *after* the 07/23 IOI deadline those signers were furnished packages to answer. Alex's 07/15 keeps NDA → deadline order. (Caveat below.)
- **PetSmart 15 NDAs, "first week of October".** The 10/03 board meeting precedes the outreach in Alex's reading (item 1: *"that further limits the date inference to October 3 – October 7"*), so the models' window 10/01–10/07 has a bad lower bound, though the midpoint 10/04 happens to land inside the right window. Harmless.
*(b) Genuinely unknown order — any assignment is a convention, and honesty must stay visible:*
- **Mac-Gray's 16 residual NDAs.** Party A signed **08/05**, after the 07/23 deadline, proving the "NDA precedes its round's deadline" constraint is not universal. The cohort's true spread is unknown; 07/15 and 07/24 are both conventions.
- **PetSmart's 27 contacts, "middle of August through the end of October".** The window *contains* the NDA date (first week of October) and runs to the IOI deadline; a single point (models: 09/20) makes all 27 contacts precede all 15 NDAs, which is right in kind and false in the tail.
- **Party D's Providence pause.** "at which point Party D indicated that it would not proceed with further due diligence at that time" is undated inside an 08/02-anchored paragraph. 08/02 is defensible (and is Alex's), but it is an anchor, not an observation — Pro's objection is to the *Reported day* label, and on that Pro is right.
- **Providence's four 07/27 exits.** "subsequently contacted the remaining bidders" — could be 07/27 or later; Alex's 07/27 is a convention that happens to be the only date that keeps them ahead of the 07/29 reengagement calls.
- **PetSmart Bidder 2's 10/30–11/02 revision.** Genuinely unknown; both 10/31 and 11/02 preserve "after the 10/30 IOIs, in response to J.P. Morgan's calls", which is the only order that matters.

**Q4. Proposed design.** Four changes; the fractional index already exists.
1. **Sort date (rename/repurpose Working date): always populated when any anchor exists.** Choose the point in the window that satisfies every known constraint, in this order: (i) a governing solicitation deadline inside the window; (ii) the day of the meeting/decision that caused the event, for undated consequences; (iii) a dated neighbour that bounds the event (a review meeting that considered it, a later dated act by the same party); (iv) the midpoint, only when no constraint bites. **Do not** replace "midpoint" with "window start" — Alex's within-window pick is event-type dependent ("early July" approach → 07/01; "first week of October" NDAs → 10/07; "week of March 28" contacts → 03/28; Q4 2015 meeting before a January board response → 12/31/2015).
2. **Keep Date from / Date to / When exactly as they are**, so the honesty stays visible, and **extend Date basis with the assignment method**: `Deadline-anchored`, `Decision-day`, `Bounded by later review`, `Midpoint`, `Reported`. This answers Alex's item 2 ("interpolated incorrectly") — a reviewer can filter on the method.
3. **Flip §8.2.** Current: *"Working dates need not increase down the ledger. Never change facts or bounds to make assigned dates sort neatly."* Replace with: "Sort date must be non-decreasing in #; where it is not, the inversion is a known same-day or genuinely unordered case and is explained in the reason. Never change facts or bounds — change the assigned point inside the window, or the reading order, instead." Keep # as the tie-break index with decimals (§11.2 already allows them), and mandate the narrative order for same-bidder same-day events (already in §8.2).
4. **Flag, don't suppress.** Every row whose Sort date came from methods (i)–(iii) gets a Review id. Alex asks for this himself (item 9: *"when we have to cross-check across multiple paragraphs for dates and for events … they should be flagged for human review"*).
Sentences of §8 that change: the two blank-producing clauses (*"For a one-sided or unbounded window, leave Working date blank"*; the No-supportable-date table row); the three prohibitions (*"A deadline is not proof of arrival by that date"*; *"A contextual exact date requires actual evidence, not an interpolation rule"*; *"…assume a subsequent event happened on its predecessor's day"*); the midpoint default sentence (becomes the last resort); and both §8.2 sentences above. §13 check 4 becomes: "every row has a Sort date or a stated reason for none; no Sort date contradicts a bound established elsewhere in the ledger."

**Q5. Deadline dating.** §8.3 keeps Alex's three-way distinction well — **Deadline set** ("when a due date was communicated"), **Deadline revised**, **Deadline** ("the scheduled due date itself") — and he uses the same triple (`Final Round Inf Ann` / `Final Round Ext Ann` / `Final Round Inf`). But §8.3 admits only *stated* deadlines (*"Preserve every stated **deadline version**"*; *"A hoped-for signing date or the last board meeting is not a bid deadline"*), and §12 B forbids the Providence inference outright (*"it does not become an announced July 27 submission deadline"*). So: **no**, a model cannot record his inferred effective deadline as a Deadline row.
Two sub-cases. The Providence July 27 one is mostly absorbed — Alex's sheet encodes it as `Final Round Ann` (row 6045), i.e. the next round's opening, which maps onto `Round opened`, and all four models produced a dated 07/27 Round opened; the loss is only that "the round-2 deadline effectively became 07/27" is not visible as a deadline fact. The Providence August 12 one is not absorbed at all: his row 6058 is a `Final Round` (deadline) row whose comment says *"The deadline apparently was not announced to the bidders, this was the time when the English auction was stopped by the target."* Smallest fix: permit a `Deadline` row with Date basis `Inferred` and an explicit "effective, not communicated" qualifier in Terms or outcome, carrying a Review flag — and move the Enforced / Extended / Late bids accepted / Unclear / No deadline stated classification out of Summary prose onto that row (D9).

## Questions only Alex can settle
1. Providence late July: is your 07/20 for the five LOIs a *claim* that they arrived by the deadline, or a sort convention you would accept being labelled as such? And do you accept the July 22 committee meeting as an upper bound for all six LOIs (your item 9) or only for some (Pro's reading)?
2. Should an undated consequence of a dated decision (the four 07/27 exits, the 06/01 drops, Mac-Gray's 09/24) carry the decision's date as standard? If yes, that is one instruction sentence to delete.
3. One date column or two — is `bid_date_precise` maintained or legacy (D14)?
4. Do you want a never-communicated effective deadline recorded as a deadline (your Providence 08/12 row), and if so how should it be distinguished from a stated one?
