# R4 — Close-out machinery: paper dry-run and verdicts on items 5, 6, 14, 15

Reviewer: R4. Date: 19 Sep 2026. Scope: §5.2, §5.3, §7, §10, §13.2–13.3 of
`SEC_Deal_Ledger_Extraction_Instruction.md` (rev. 19 Sep 2026), applied by hand to
Providence & Worcester, Mac-Gray and PetSmart, plus Alex's Zep and Saks rows.
Nothing was re-extracted; this is a paper run against the filing text
(`$SCRATCH/filing/*_bg.txt`), Alex's hand-collected sheet (`ref/deal_details_Alex_2026.xlsx`,
font-checked with openpyxl: **red = his own edit**, black = inherited RA row he kept),
his voice notes and his collection instructions.

Conventions used below: **E** = entrant (unit joining the live set), **X** = exit,
**R** = re-entry. "Stock" is the live bidder-unit count after the row.
Outcome basis abbreviations are the instruction's: Stated / Inf:res / Inf:excl /
Inf:silent / Inf:id.

---

## 1. Dry-run A — Providence & Worcester (G&W, signed 08/12/2016)

Base population: "GHF contacted 11 potential strategic buyers (including Party A) and 18
potential financial buyers. Each of the potential strategic buyers and 14 potential
financial buyers subsequently executed confidentiality agreements" (bg p.27) → **25 NDA
signers (11S + 14F)**. Party C signs later (bg p.29) → 26 signers in the process.

| # | Working date | Who | Row the instruction requires | Count | Basis | E/X/R | Stock |
|---|---|---|---|---|---|---|---|
| 1 | 03/28/2016 (wk of) | 25 NDA signers (11S+14F), incl. A, B, G&W | NDA signed (cohort) | 25 | Stated | +25 E | 25 |
| 2 | 05/19/2016 | 9 IOI submitters | Bid (cohort, envelope $17.93–26.50) | 9 | Stated | — | 25 |
| 3 | 05/19/2016 | 16 remaining signers | **Did not submit** (25 − 9) | 16 | **Inf:res** | −16 X | 9 |
| 4 | 06/01/2016 | 2 low bidders | Dropped by target | 2 | Stated | −2 X | 7 |
| 5 | ~07/01/2016 | Party C | NDA signed (late entrant) | 1 | Stated | +1 E | 8 |
| 6 | 07/12/2016 | Party C | Bid $21.00 | 1 | Stated | — | 8 |
| 7 | 07/20/2016 | B, G&W, E, D, C, F | Bid ×6 (LOIs) | 1 each | Stated | — | 8 |
| 8 | 07/20/2016 | 1 strategic + 1 financial | **Did not submit** ("One strategic buyer and one financial buyer elected not to submit an LOI") | 2 | **Stated** | −2 X | 6 |
| 9 | 07/20/2016 | Party A | **Did not submit — identity row** | **0** | **Inf:id** | 0 | 6 |
| 10 | 07/27/2016 | C, D, E, F | Dropped by target ("informed that they were no longer involved") | 4 | Stated | −4 X | 2 |
| 11 | 08/01/2016 | Party D | **Re-entered** + Bid $24.00 | — | Stated | +1 R | 3 |
| 12 | 08/01/2016 | Party E | **Re-entered** + Bid $23.81, `Support: Party F (financing)` | — | Stated | +1 R | 4 |
| 13 | 08/01/2016 | Party F | **no row** (§5.3: had already exited 07/27) | — | — | 0 | 4 |
| 14 | 08/02/2016 | Party E | Bid (reversion to $21.26) — not an exit | — | Stated | 0 | 4 |
| 15 | 08/02/2016 | Party D | Withdrew ("would not proceed with further due diligence at that time") | 1 | Stated | −1 X | 3 |
| 16 | 08/04/2016 | Party B | Bid reaffirmed $24 (item 1, not mine) | 0 | Stated | 0 | 3 |
| 17 | 08/12/2016 | Party B | Not selected at signing ("would not increase its price") | 1 | Stated | −1 X | 2 |
| 18 | 08/12/2016 | Party E | **Not selected at signing** (last seen 08/02) | 1 | **Inf:silent** | −1 X | 1 |
| 19 | 08/12/2016 | G&W | Merger agreement signed | — | Stated | — | **1 = winner** |

**Stock line.** Entrants 26 (25 + C) + re-entries 2 = 28; exit units 27
(16+2+2+0+4+1+1+1); 28 − 27 = **1, the winner. Balances.** Inferred share of exits:
17/27 units (16 residual + 1 silent); the Count-0 identity row adds nothing.

**What the machinery gets right.** Every one of Alex's red/black Providence exits is
reproduced: 16 residual (his 6030), 2 low bidders DropTarget (6031), the four told out on
07/27 (6046–49), D's and E's re-entries (6050–52), D's 08/02 drop (6053), B at signing
(6056) and — the one no model produced — **E closed at signing** (his 6057 "Party E/F ·
Drop" with the red comment "Did not engage for a while") = `Not selected at signing,
Inf:silent`. §10.2's third table row is Alex's row.

**Where it is ambiguous or differs from Alex.**

1. **Is Party B inside the 25?** Alex's **red** edit at 6027 says yes ("25 parties,
   including Parties A, B"), although B's first appearance is an "introductory meeting" on
   04/21, three weeks after the 03/28 wave, and the only evidence of its NDA is the
   memorandum sentence ("distributed to the potential buyers, including Party A, Party B
   and G&W, that had executed confidentiality agreements"). The instruction already
   licenses Alex's reading — §7.1 "An introductory meeting is not necessarily the first
   contact" — and §10.2's uncertain-base paragraph ("Use the filing's stated base") forces
   the stated 25 rather than 25+1. Same for G&W. **No change needed**, but the row must say
   "base assumes B and G&W are inside the 11 strategic signers"; if they are not, the
   residual is 18, not 16.
2. **The residual date.** §8.1 rule 2 assigns the 16 the 05/19 due date; Alex used 06/01
   (the end of the "between May 19 and June 1" arrival window and the second review
   meeting). The instruction's own §8.1 worked example puts the 9 IOIs on 05/19 too, so the
   *order* — bids and residual together, before the 06/01 exclusion — is Alex's order. No
   break here (contrast Mac-Gray below, where the same rule does break).
3. **Party A.** §10.2's Count-0 identity row fires at 07/20, the first transition whose
   continuing set is named without A (the six LOI submitters are all named), with Terms
   naming "the cohort row that already counts it". That wording makes the **07/20**
   cohort (2 LOI non-submitters) primary — which is exactly the reading Alex now rejects.
   VN I.11 (magenta, his own dictation): *"the fact that the background does not mention
   this implies, to me, that bidder A has never made it out of round one of bidding. And so
   indeed the strategic bidder that drops out in round two is unnamed, it's not bidder
   A."* His hand row 6042 ("Party A · Drop · 07/22") is **black** — an inherited RA row,
   i.e. the thing his 2026 note corrects. So the instruction lands the row on the right
   *date band* but asserts the wrong *cohort*. Stock-neutral (Count 0), fixable in one cell,
   but it should not state a single covering cohort as settled. Wording fix at item 14 below.
4. **Party F.** §5.3's "if it had already exited, it gets no new row" is right here and is
   stock-neutral: F was dropped 07/27, and "Both revised proposals contained a 30-day due
   diligence period" (two proposals, not three) confirms E+F is one submitting unit.
5. **Party D on 08/02** could be read as `Participation paused` ("at that time") instead of
   `Withdrew`. Terminal stock is 1 either way, but the live set at signing is 2 vs 3 and D
   gets one row vs two. The stock check cannot catch this; it is a §10.1 labelling choice,
   flagged for Questions.
6. **08/09 G&W** ("the Company intended to enter into a merger agreement with another
   bidder" but continued diligence was granted) is `Target decision` per §12.E, not an exit
   + Re-entered. If a model reads it as Dropped+Re-entered the stock nets to zero, so the
   check is robust to this; the round tally is not.

---

## 2. Dry-run B — Mac-Gray (CSC/Pamplona, signed 10/14/2013)

Base: "Over the next two months a total of 20 potential bidders, including two strategic
bidders (Party A and CSC/Pamplona) and 18 financial bidders (including Party B and Party
C), entered into confidentiality agreements" (bg p.31–32). Named/dated: CSC/Pamplona
07/11, Party A **08/05**, Party B 06/28, Party C 06/30 → **16 unnamed financial signers**
(Alex VN II.4, his 8B0000 "important & hard" note: *"CSC/Pamplona's NDA = July 11; party
A's NDA = August 5; NO other strategics sign an NDA"*).

Rows are shown **in Working-date order**, as §8.2 requires the ledger to sort, so that the
break at 07/23 is visible rather than asserted.

| # | Working date | Who | Row | Count | Basis | E/X/R | Stock |
|---|---|---|---|---|---|---|---|
| 1 | 06/21/2013 | Party A | Bid $17–19 (unsolicited, **pre-NDA**) | 1 | Stated | **+1 E?** | 1 |
| 2 | 06/28 | Party B | NDA signed | 1 | Stated | +1 E | 2 |
| 3 | 06/30 | Party C | NDA signed | 1 | Stated | +1 E | 3 |
| 4 | 07/11 | CSC/Pamplona | NDA signed | 1 | Stated | +1 E | 4 |
| 5 | 07/23 | CSC/Pamplona | Bid $18.50 | 1 | Stated | — | 4 |
| 6 | **07/23** | 16 unnamed financial signers | **Did not submit** (20 − 4 continuing) | 16 | **Inf:res** | −16 X | **−12** ← |
| 7 | 07/24 | Party B; Party C (oral) | Bid ×2 (late; treatment = Late bids accepted) | 1 each | Stated | — | −12 |
| 8 | **~07/24** (midpoint of 06/24–08/24) | 16 unnamed financial signers | NDA signed (residual cohort) | 16 | Stated | +16 E | 4 |
| 9 | 07/25 | Party C | Bid $16–16.50 (written) | 0 | Stated | — | 4 |
| 10 | 08/05 | Party A | NDA signed (entry already counted at #1) | 1 (NDA tally) | Stated | **0** | 4 |
| 11 | 09/09–10 | CSC/P, B, A, C | Bid ×4 (revised proposals) | — | Stated | — | 4 |
| 12 | 09/18 | CSC/P $20.75; A reaffirms $18–19; B $21.50 | Bid / Bid reaffirmed | — | Stated | — | 4 |
| 13 | 09/18 | Party C | Did not submit ("Party C did not submit a revised indication of interest or reiterate its prior indication … nor did it specify any reasons") | 1 | **Stated** | −1 X | 3 |
| 14 | 09/24 | Party A, Party B | **Dropped by target** (exclusivity executed with CSC/Pamplona) | 2 | **Inf:excl** | −2 X | 1 |
| 15 | 10/14 | CSC/Pamplona | Merger agreement signed | — | Stated | — | **1 = winner** |

**Stock line.** 20 entrants − 16 − 1 − 2 = **1. Balances**, and rows #12–13 reproduce
Alex's red bid_note edits at 6958/6959 exactly (his VN II.8 dictation says "party B and
party C" for the 09/24 pair — his own sheet says **Party A and Party B**, so the note is a
dictation slip; the instruction follows the sheet).

**Three real breaks.**

1. **Exit before entry (the headline break).** The 16-signer NDA cohort has no individual
   dates; §8.1 rule 4 (finite window, nothing better) gives the midpoint of 06/24–08/24 =
   **≈ 07/24**, one day *after* the 07/23 closure the §10.2 table mandates ("The
   solicitation's due date"). The cohort is then closed before it is recorded as entering:
   rows 6–8 of the table above take the stock to **−12**, which violates §8.2 ("Working
   dates never decrease down the ledger") and fails §13.3's "never negative". This is not
   hypothetical: under the old
   instruction three of four models wrote exactly that window —
   `ds_mac-gray` "between 06/24/2013 and 08/24", `opus_mac-gray` "over the two months
   following", `glm_mac-gray` "06/28/2013-08/05/2013". Alex's own sheet sidesteps it by
   assigning the cohort 07/15 (6934, black RA row he kept) and the drop 07/25 (6942).
   §8.1's order constraint would fix it *if* the model realised that a closing row entails
   its entry row — the instruction never says so.
2. **What is subtracted.** The table says "no submission reported; number known by
   subtraction". Three IOIs arrive by the 07/23 window (CSC/P, B, C); Party A's live
   06/21 proposal was reviewed at the 07/25 meeting alongside them ("the preliminary
   indications of interest received from Party B, Party C and CSC/Pamplona **as well as the
   Party A June 21 proposal**"). Subtracting *submitters* gives 17 and wrongly closes Party
   A; subtracting *participants shown to continue* gives Alex's 16 and the filing's "four
   interested bidders". The wording does not choose.
3. **"Entrants" for a pre-NDA bidder.** Party A enters at its 06/21 bid and signs an NDA on
   08/05. Its NDA row legitimately carries Count 1 in the NDA tally (§7.2 "1 for a newly
   represented individual"), so any stock computed by summing Count over entry-type rows
   double-counts Party A and ends at 2, not 1. §7.2 says outright that "Count is a tally
   contribution, **not a population balance**" — so item 14's balance cannot be computed
   from the ledger's own arithmetic column. This is the central defect of item 14.

**Moab (item 6 / §4 scope cut).** Threads: 07/03 Moab asks to partner exclusively with
CSC/Pamplona; 07/06 the Special Committee **denies** it "at this stage … but such
discussions would be permitted at a later stage"; 09/23 permission given; ~10/07 resolved
("Moab would not rollover any Moab shares"); 10/14 Moab voting agreement (not a rollover).
§4's cap is "at most one row when it is **permitted or formed** and one when it is
resolved" — the 07/06 **denial**, which is the process-relevant event (the target refusing
to let a 9% holder be locked to one bidder, to keep its equity available to all bidders),
has no slot in that wording. Alex has **no** Moab rows at all, so the cap is already
generous; the wording just needs to admit a denial. No stock effect (a rollover holder
never enters: §4 "Exclude lender-only, adviser and rollover-holder agreements").

---

## 3. Dry-run C — PetSmart (Buyer Group, signed 12/14/2014)

| # | Working date | Who | Row | Count | Basis | E/X/R | Stock |
|---|---|---|---|---|---|---|---|
| 0 | 08–10/2014 | 27 inbound contacts (3S + 24F) | Contact (cohort) | 27 | Stated | **see break 1** | — |
| 1 | 10/07/2014 (1st wk Oct) | 15 financial signers | NDA signed (cohort) | 15 | Stated | +15 E | 15 |
| 2 | 10/30 | 6 submitters (BG $81–83; one $80–85; one ≥$80; Bidder 2 $78→$81–84; +2 below) | Bid ×6 | 1 each | Stated | — | 15 |
| 3 | 10/30 | 9 remaining signers | **Did not submit** (15 − 6) | 9 | **Inf:res** | −9 X | 6 |
| 4 | 11/03 | 2 eliminated parties | Dropped by target ("J.P. Morgan notified the eliminated parties") | 2 | Stated | −2 X | 4 |
| 5 | ~11/03–11/15 | two bidders → "Bidder 3" | **Bidding group changed**, "2 of the 4 finalists combine; **units −1**" | 2 affected | Stated | −1 net | **3** |
| 6 | 12/10 | Buyer Group $80.70; Bidder 2 $80.35 | Bid ×2 (Formal) | — | Stated | — | 3 |
| 7 | 12/10 | Bidder 3 | Bid, `Bound: ≤ ~$78` verbal, then **Did not submit** ("accordingly Bidder 3 did not submit a written offer") | 1 | **Stated** | −1 X | 2 |
| 8 | 12/12 | Bidder 2 $81.50 (best and final); BG $82.50 → $83.00 | Bid ×3 | — | Stated | — | 2 |
| 9 | 12/14 | Bidder 2 | Not selected at signing | 1 | Stated (see break 3) | −1 X | 1 |
| 10 | 12/14 | Buyer Group | Merger agreement signed | — | Stated | — | **1 = winner** |

**Stock line.** 15 − 9 − 2 − 1 (group) − 1 − 1 = **1. Balances — but only under one reading
of the Bidder 3 sentence.**

**Break 1 — the contact population.** §10.1 says outcome labels apply to "a participant
that had entered the process — **responsive to contact**, under NDA or bidding", and §10.2
says every participant that entered a stage is closed out. Read literally, the 27 inbound
contacts all entered (they contacted J.P. Morgan), so a 12-unit residual row is owed at the
NDA transition — and, by the same logic, 4 units in Providence (29 contacted, 25 signed)
and **30** in Mac-Gray (50 approached, 20 signed). Alex writes none of these: his PetSmart
block starts at the 15 NDAs, his Mac-Gray block has no 30-party row, his Providence block
has no 4-party row. §13.3 offers no definition of "entrants" to stop it. This is item 14's
biggest risk: a rule whose purpose is to make the ledger complete instead adds three extra
residual cohort rows covering ~46 units across these three deals — populations Alex does not
track at all — and makes the reported "inferred share" incomparable between a deal whose
contacts are disclosed and one whose are not.

**Break 2 — who are Bidder 3's two members?** The filing: "Two of the bidders (one of which
**had been invited into the final round** but had indicated a desire to work with an equity
partner … and the other of which **had indicated to J.P. Morgan that it would drop out of
the process if not permitted to work together with another bidder**) requested permission
to work together." Only the first is said to be a finalist. Item 6's "units −1" arithmetic
under each reading:

| Reading of the 2nd member | Group row effect | Stock at 12/10 | Extra rows needed | Balances? |
|---|---|---|---|---|
| (a) also one of the 4 finalists (**Alex's**: red rows 6450/6451 close "Unnamed party 1" and "Unnamed party 4" at 12/10) | units −1 | 3 vs 3 bids | none | **yes** |
| (b) one of the 2 eliminated (11/03) | units +0 (one re-entry into a merged unit) | 4 vs 3 bids | `Re-entered` for the eliminated party + a residual of 1 at 12/10 | no |
| (c) one of the 9 non-submitters | units +0 | 4 vs 3 bids | `Re-entered` + a residual of 1 at 12/10 | no |

Only (a) reconciles, and only (a) matches the filing's "Each of the bidders invited into the
final round indicated some interest in a Longview rollover" followed by exactly three final
participants. **The stock check is what forces the reading** — a concrete demonstration that
item 14 earns its place. §5.3's "state the assumption in that row and in Questions" is the
right residual treatment. Note also that (b) is disfavoured by the immediately preceding
sentence: the eliminated parties showed no "interest or ability to remain in the process".

**Break 3 — cohort row vs Joined group.** §10.2 says "a bidder that joined a group is closed
by `Joined group`", while §5.3 says an anonymous-cohort combination is handled by one
`Bidding group changed` row stating "units −1". PetSmart is the collision: the two members
are individually *distinguishable* (§5.1 allows "Unnamed financial bidder 1/2" — Alex names
them), so §10.2 wants two `Joined group` rows, while §5.3 wants one cohort row. Either
reconciles (−1 net) provided the reader knows that a `Joined group` pair nets to −1 and a
"units −1" row nets to −1 — but the stock check reads **Terms**, not Count, on group rows
(§7.2: "On participation outcomes or group changes, Count may record the exact number of
affected units", i.e. 2, not −1). Item 14 must say so or the arithmetic silently
double-subtracts.

**Break 4 — `Inferred: silent` over-fires at signing.** Bidder 2 bid on 12/12 and is never
mentioned again; §10.2's third table row ("Last seen in the process … and never mentioned
again by signing") would label it Inf:silent, although the narrative plainly explains why it
lost. Same for Providence Party B. Over-use inflates the "inferred share" §11.4.5 asks
Summary to display, making a well-documented deal look poorly observed.

**Clean cases (no change needed).** Longview: rollover holder, never an entrant (§4, §5.3,
matching Alex's VN III.7 *"This is not a consortium formation to me"*); its 12/12
bidder-shareholder confidentiality agreement is not a bidder NDA (§7.1) — item 6's "never
backfill an NDA" holds. Industry Participant: never invited → `Target decision`, no outcome
row (§10.1), matching Alex's sheet (no Industry Participant rows).

---

## 4. Item 5 — a terminated process closes its participants

**Current wording (§10.2, last paragraph).** "A participant closed at one transition is not
closed again unless it has Re-entered. **When a process is terminated, its `Process
terminated` row closes the remaining participants; state how many where known.** Parties
that enter during a go-shop are closed at its expiry."

**Evidence.** No terminated process among the three filings. Alex's Zep rows (his own
**red** edits at 6401/6402): `Terminated · 06/26/2014` with the red comment "[THIS IS THE
EXAMPLE OF THE EARLIER AUCTION THAT WAS TERMINATED! CAN USE]", then `Restarted · New
Mountain Capital · 02/19/2015`. His collection instruction §3.9 (an "Alex's addition" box)
defines the two codes and leaves Bidder blank for `Terminated`, but names the bidder "as
recorded when they signed the NDA" for `Restarted`. §2 (Chicago RAs' text) says "Ignore any
confidentiality agreements from such a stale process" — for the auction-screen
classification only.

**Dry-run on Zep.** 24-party NDA cohort + NMC (03/19) = 25 entrants; 5 IOIs (04/14) leave
19 + NMC closed (6391/6392) → 5; Party X bids and drops (05/09, 05/14) → 4; Party Y signs
an NDA and bids 05/20 (+1) → 5; "five of the remaining six interested parties …" + Party Y
close on 05/23 (6399/6400) → **0**. The `Terminated` row on 06/26 therefore closes nobody in
Alex's own only example. **Consequence: item 5 changes nothing on the one case we can
check** — which is the best possible news for it, because it means the rule only fires where
the filing leaves someone dangling.

**Is item 5 needed at all?** Yes. Without it there is a hole, not a redundancy: §10.2's
table has three situations, of which the general sweep ("never mentioned again **by
signing**") presupposes a signing. An abandoned process has none, so a live participant at
abandonment would get no closing row and §13.3's balance could not be run on that process at
all (§13.3 rightly forbids inventing a winner for it). The alternative — one inferred exit
row per still-live participant of the abandoned attempt — is worse: it manufactures N
individual rows with an invented common date and no more information than the termination
row carries.

**Is "state how many where known" enough to close the old process's stock?** **No, as
written.** (a) It does not say where the number goes, and §7.2 says "Leave Count blank on
adviser, **process-wide decision**, scheduled milestone and pure offer-update rows" —
`Process terminated` is a process-wide decision row, so the two rules collide and the count
that the balance needs is the one the Count rules suppress. (b) "where known" leaves the
unknown case with no instruction; §13.2's bounded-balance escape ("show the balance with
bounds rather than forcing it") is in a different section.

**Stale signers who reappear.** Zep's NMC signs an NDA in process 1, is closed in process 1,
and returns to win process 2 with **no new NDA row** in Alex's sheet — consistent with §6.2
("Keep stale NDAs in their original process. Record expressly reused coverage without
inventing another execution"). But §10.1 makes `Re-entered` "required whenever a participant
bids, reaffirms or resumes diligence **after a recorded outcome**", with no process
qualifier. Applied across processes it either injects a re-entry into a terminated process
or gives process 2 a re-entry with no prior exit there — both break item 14's balance. The
fix belongs with item 5 because that is where the process boundary is drawn.

**Downstream risk.** Low and reversible: one row per abandoned process, filterable by event
label and process number; an estimation that wants individual exits can expand the row's
count. The unfixed Count collision is the reversible-but-annoying part (it silently zeroes a
stage balance).

**Verdict: KEEP WITH REWORDING.** Confidence **high** on keeping, **medium** on the exact
wording (no terminated process in the three tested filings; the Zep filing is not in the
repo, so the row set above is read off Alex's sheet, not the source).

Replacement for the §10.2 sentence:

> When a process is terminated, its `Process terminated` row closes the remaining
> participants: Count is the number still live in that process — this overrides the blank
> Count of section 7.2 for this row — and Terms or outcome shows the arithmetic and names
> them where the filing does. Leave Count blank, and say so, only where the number cannot be
> established; the balance for that process is then reported with bounds.

Add to §6.2, after "Keep stale NDAs in their original process.":

> Closure is per process. `Re-entered` applies within a process; a participant that
> reappears in a later process enters that process afresh at its first row there, with
> Related rows to its earlier participation, and no second NDA is recorded.

---

## 5. Item 6 — financing supporter, cohorts combining, no backfilled NDA

**Current wording (§5.3, last two paragraphs).** "A party that finances or supports another
bidder's offer does not thereby bid. The supported bidder keeps its own name and Type, with
`Support: [party] (financing)` in Terms or outcome and Related rows pointing to any earlier
independent bid by the supporter. **If the supporter was still a live independent bidder when
the support began, close its independent participation with Joined group; if it had already
exited, it gets no new row.**
When members of an anonymous cohort combine, the Bidding group changed row states the effect
on the number of bidding units ("2 of the 15 signers combine; units −1"), so that stage
counts reconcile by number rather than identity. **Never backfill an NDA or entry row that
the filing does not report.**"

**Evidence.**
- *Party E/F naming.* Alex's rows 6051, 6052, 6057 carry BidderName "Party E/F", type "S/F"
  — **black font**, i.e. **inherited RA naming that he kept**, not his own edit; only the
  comments ("Financing support from Party F", "Did not engage for a while") are red. So
  §5.3's "keeps its own name and Type" contradicts **no rule of Alex's**, only a legacy RA
  convention. The filing supports the instruction: "Party E submitted a revised LOI, along
  with financing support, from Party F" and "**Both** revised proposals contained a 30-day
  due diligence period" — two proposals (D's and E's), one unit each.
- *Longview.* VN III.7 (his own dictation): "This is not a consortium formation to me …
  Longview doesn't provide the bidder with financing. It doesn't provide it with additional
  synergies." §5.3's rollover paragraph already encodes this; §4 excludes rollover-holder
  agreements from NDA counts. Agreement.
- *Cohort combination.* Alex's **red** rows 6450/6451 close both Bidder 3 constituents at
  12/10 — i.e. he does exactly what "units −1" achieves, by identity rather than by number,
  and he is willing to write individual rows for anonymous parties (also red 6436).

**Dry-run results.** Providence: rule works, stock-neutral, matches Alex (Party F had
exited; no new row). PetSmart: works under reading (a); §5.3 vs §10.2 on whether the group
row or two `Joined group` rows do the closing is unresolved (break 3 above). Mac-Gray: the
"never backfill" clause does real work — Party A bids on 06/21 with an NDA only on 08/05 and
the temptation is to date its NDA to June; Alex's 8B0000 note II.4 is entirely about a model
having done the equivalent (crediting Party A with an early unnamed strategic NDA).

**The unseen case breaks the wording.** A live rival turning financier is directed to
`Joined group` — but the *same paragraph* says financing support "does not thereby bid",
§5.3 above says "Rollover, financing support … do not by themselves establish joint
bidding", and §11.3's own label gloss says `Bidding group changed; Joined group … **Not a
shareholder rollover or financing support (section 5.3)**`. So §5.3 instructs the one label
that §11.3 forbids for this fact pattern, and §10.1's gloss ("A former independent bidder now
participates through the group; **not an economic exit**") is wrong for a pure financier,
which has left the competition. The stock is right either way (−1 unit); the label lies.

**Downstream risk.** Medium and mostly reversible. A wrongly-applied `Joined group` is
reversible by relabelling; a **merged name** ("Party E/F") is not cheaply reversible,
because it destroys the fact that F bid $19.20 independently on 07/20 — which is why the
instruction's choice is the right one for estimation (Opus's Providence workbook kept E and
F separate and got a round tally of 6 rather than 5; the ledger must let both be recovered).
"Units −1" in free text is a latent risk: it is the only place a stage count changes without
a Count cell saying so.

**Verdict: KEEP WITH REWORDING** (three small fixes; the substance stands).

1. Replace the `Joined group` sentence in §5.3:

> If the supporter was still a live independent bidder when the support began, close its
> independent participation on the date the support is reported: `Joined group` where the
> filing shows it became part of the bidding unit, otherwise `Withdrew` with `Support:
> [bidder] (financing)` in Terms or outcome and Decided by = Bidder; say which and why. If
> it had already exited, it gets no new row and no `Re-entered`.

2. In §11.3, change the `Bidding group changed; Joined group` gloss to end: "Not a
   shareholder rollover; for financing support see section 5.3."

3. Append to the anonymous-cohort sentence in §5.3:

> Where the members are individually recorded, close each with `Joined group` instead and
> say in Terms or outcome that the stage count falls by one; the `Bidding group changed` row
> then states the composition but carries no unit change of its own. Where it is not
> established that every member was live in the current stage, state the assumption in the
> row and in Questions.

4. In §4, change "gets at most one row when it is permitted or formed and one when it is
   resolved" to "**gets at most one row when it is permitted, denied or formed and one when
   it is resolved**" (Mac-Gray's 07/06 denial otherwise has no slot).

Confidence **high** on 1–2 (a textual contradiction inside the document), **medium** on 3–4.

---

## 6. Item 14 — per-stage stock check

**Current wording.** §13.3: "Every participant ends in a stated outcome, an inferred closing
row, joining a group, or signing. A bid, reaffirmation or resumed diligence after a recorded
outcome requires a `Re-entered` row. **Participant stock per stage = entrants − exits +
re-entries; it is never negative, and only the winner remains at signing.** Do not require a
named exit for an anonymous outcome or fabricate a winner for an abandoned process."
§13.2: "**Per-stage balance:** for each process, participants entering a stage − stated exits
− inferred exits = participants continuing, ending with the winner alone; Summary shows the
balance and the inferred share." §11.4.5 repeats it.

**Evidence that it earns its place.** It catches errors that hand collection missed. In
Alex's own PetSmart block the fifteen signers are U1–U12 + Bidder 1 + Bidder 2 + Buyer
Group; six submit (U1, U2, U3, Buyer Group, U4, Bidder 2); the non-submitters he closes on
10/30 are U5–U12 — **eight**, not nine. **"Bidder 1" (row 6424) is never closed and never
appears again.** 15 − 6 = 9; his ledger accounts for 14 of 15 units. The label is doubly
telling: the PetSmart filing never uses "Bidder 1" at all — only Bidder 2, Bidder 3 and the
Buyer Group (grep over the background and the full filing) — so the row is an RA-invented
identity that then went uncounted. A stock check on his own sheet flags it in one line. It
also forces the only reconciling reading of PetSmart's
Bidder 3 (§3, break 2 above). All three deals balance to exactly one under the instruction's
own rows, which is the main positive result of this dry-run.

**Where it breaks or is ambiguous.**

| # | Break | Deals | Severity |
|---|---|---|---|
| 1 | **"Entrants" is never defined**, and §10.1's "responsive to contact" pulls the contact population in: 12 (PetSmart), 30 (Mac-Gray), 4 (P&W) residual units Alex never records | all three | high |
| 2 | **The balance cannot be computed from Count**, which §7.2 declares "not a population balance"; a pre-NDA bidder (Mac-Gray Party A) legitimately carries Count 1 on both its Bid and its later NDA row | Mac-Gray, Zep | high |
| 3 | **Group rows change the stock in free text, not in Count** ("units −1"), while Count on the same row is the number of affected units (2) | PetSmart | medium |
| 4 | **An inferred closing row can precede its entry row** (Mac-Gray: closure 07/23 vs cohort NDA midpoint ≈ 07/24), making the per-cohort stock negative | Mac-Gray | high |
| 5 | **What the residual subtracts** — submitters (→17, closes Party A) or participants shown to continue (→16) | Mac-Gray | medium |
| 6 | **Count-0 identity row asserts one covering cohort** ("names the cohort row that already counts it") where the evidence spans two, and picks the one Alex's VN I.11 rejects | P&W (Party A) | low (stock-neutral) |
| 7 | **"only the winner remains at signing"** is wrong for go-shop deals, where units enter after signing (item 15) | Saks | low |
| 8 | **Inf:silent over-fires** on a bidder that was active up to signing and simply lost | P&W, PetSmart | low–medium |

**Downstream risk.** The check itself is a *check*, not stored data, so keeping it is cheap
and dropping it later costs nothing. The risk is asymmetric and runs the other way: without a
definition of "entrants", different deals will silently use different populations
(contacts vs NDAs vs bidders), and the "inferred share" that Summary reports — a number a
reader will treat as a data-quality measure — becomes incomparable across deals. That is
expensive after hundreds of extractions.

**Verdict: KEEP WITH REWORDING** — the check is the single most useful thing in §13, but it
must define its own population. Confidence **high**.

Replace the §13.3 sentence with:

> Participant stock per stage = entrants − exits + re-entries; it is never negative, and at
> signing only the winner remains (and again after any go-shop expiry). A participant
> **enters** a process at its first `NDA signed` or `Bid` row in that process, or at the
> target decision that admits it to a stage, counted once as a whole-company bidder unit
> however many such rows it has; contacts that never became an NDA, a bid or an admission,
> and adviser, lender and rollover-holder agreements, never enter and are never closed. A
> `Bidding group changed` row that states "units −1" moves the stock by that stated amount,
> not by its Count.

Add to §10.2, immediately after the three-situation table:

> An inferred closing row may never precede the row that records the participant's entry.
> Where the transition's date is earlier — a cohort whose signing window straddles the due
> date — the entry row's Working date is moved earlier under section 8.1's order
> constraint, inside its own window, and the reason says so.

(The order-constraint direction matters: the closure row is dated by the transition and has
no window of its own, while the cohort NDA row does, so it is the *entry* that moves —
landing at or before 07/23, which is how Alex's 07/15 at 6934 comes out. Moving the closure
later instead would, with a wider window, push it past the 07/25 advancement decision that
revealed the absence.)

And in the first row of that table, replace "number known by subtraction" with:

> number known by subtraction: the stated base minus the participants the filing shows
> continuing past that transition, not merely minus the submitters

For break 6, in the Count-0 identity paragraph replace "Terms or outcome names the cohort row
that already counts it and the alternative reading" with:

> Terms or outcome names every cohort row that could already count it, recommended reading
> first, and gives the reason.

Break 8 is worth one clause in the third table row ("Last seen in the process … and never
mentioned again by signing"): append "— a bidder that was still bidding when the target chose
another is `Not selected at signing` with Outcome basis Stated, not Inferred: silent."

---

## 7. Item 15 — go-shop entrants closed at expiry

**Current wording (§10.2, final sentence).** "Parties that enter during a go-shop are closed
at its expiry." Related: §11.3 "`Go-shop changed` | Start, revision or end of an
agreement-provided post-signing solicitation period; identify the change. Ordinary
pre-signing contacts are not a go-shop."

**Evidence.** Alex's Saks rows: 7019 `Company I · S · NDA · 07/29/2013` (black RA row) with
his **red** comment "Go-shop until Sep 6", and 7020 `Company I · Drop · 09/06/2013` (black).
So the practice — one entry at the post-signing NDA, one closure dated exactly at expiry —
is in his sheet, and the red comment shows he read the go-shop window and kept the pair. His
VN VII.4 defines the thing: "This is when the target's management and board of directors
approach additional bidders **after a merger agreement has been signed**, to convince its
shareholders that it is maximizing their value." The instruction's §11.3 gloss matches that
definition. No go-shop deal is among the three filings, and the Saks filing is not in the
repo, so this rests on the row pair plus his definition.

**Is "closed at its expiry" the right label and date?** The date, yes: expiry is the
transition that reveals the absence of a proposal, exactly as a due date does. The label and
basis are the gap — the sentence names neither, and none of §10.2's three table rows is
written for it. Working through it: a go-shop is a solicitation with a due date, so the
natural row is **`Did not submit`**, Decided by Unknown, Exit reason Not stated, **Outcome
basis Stated** where the filing reports that the go-shop ended with no proposal (the common
case, since filings say so to justify the lower termination fee), **Inferred: residual**
where the outcome is only implied by the count. Alex's bidder-side "Drop" maps to `Did not
submit`, not to `Dropped by target` — nobody excluded Company I.

**Two defects.**
1. **Excluded parties.** Many go-shops let a party that *did* make a proposal before expiry
   continue past expiry as an "excluded party" at a reduced fee. "Parties that enter during a
   go-shop are closed at its expiry" closes that party too, on the wrong date and with the
   wrong label.
2. **It contradicts item 14's terminal condition** as drafted ("only the winner remains at
   signing"): a go-shop entrant enters *after* signing, so the stock goes 1 → 2 → 1. Fixed by
   the item-14 replacement text above.

**Downstream risk.** Small and contained — go-shop rows are filterable by process/round =
`post` and by the `Go-shop changed` label; the wrong label on a go-shop entrant is a one-cell
correction. But a go-shop entrant left *unclosed* is invisible, which is the failure mode the
sentence exists to prevent.

**Verdict: KEEP WITH REWORDING.** Confidence **medium-high** (right on the principle and on
Alex's practice; untested against any go-shop filing, and I could not verify whether the Saks
filing reports the go-shop's outcome in terms or only by the fee provision).

Replacement for the final sentence of §10.2:

> A party that enters during a go-shop and makes no proposal is closed at the go-shop's
> expiry: `Did not submit`, Outcome basis Stated where the filing reports that the period
> ended without a qualifying proposal, otherwise Inferred: residual. A party that does make
> a proposal is closed by that proposal's own outcome, which may fall after expiry.

---

## 8. Summary of verdicts

| Item | Verdict | One-line reason |
|---|---|---|
| 5 — terminated process closes its participants | **KEEP WITH REWORDING** | Fills a real hole (no signing ⇒ §10.2's table never fires), and is a no-op on Alex's only example; but "state how many where known" collides with §7.2's blank Count for process-wide rows, and `Re-entered` needs a process boundary |
| 6 — financing supporter / cohorts combining / no backfilled NDA | **KEEP WITH REWORDING** | Substance is right and the "Party E/F" merge it overrides is inherited RA naming, not Alex's rule; but §5.3 orders `Joined group` for a live financier and §11.3 forbids exactly that, and the group-vs-`Joined group` closing route is unresolved |
| 14 — per-stage stock check | **KEEP WITH REWORDING** | It caught an uncounted participant in Alex's own PetSmart sheet and forces the only reconciling reading of Bidder 3 — but "entrants" is undefined, §7.2 says Count is not a population balance, and Mac-Gray's 16-signer cohort can be closed before it enters |
| 15 — go-shop entrants closed at expiry | **KEEP WITH REWORDING** | Matches Alex's Saks pair and his VN VII.4 definition, but names no label or basis and wrongly closes an excluded party that bid before expiry |

None should be dropped. None should change to an alternative.

---

## 9. Not checked

- No terminated-process and no go-shop deal exists among the three filings; the Zep and Saks
  filings are not in `raw_filing/`, so items 5 and 15 rest on Alex's rows, his §3.9 and his
  VN VII.4 alone. The Zep stock reconstruction in §4 is read off his sheet, not the source.
- I did not verify whether the two unnamed PetSmart finalists are individually
  distinguishable enough for §5.1 names in every reviewer's judgment; the reading that makes
  the stock balance assumes they are.
- Providence: whether G&W and Party B are inside the 11 strategic signers is not resolvable
  from the text; both the 16-residual and an 18-residual are defensible. I followed Alex's
  red base of 25.
- I did not re-run any extraction. The model-behaviour evidence is the four old workbooks in
  `$SCRATCH/dump/` (built under the previous instruction), used only to show that the
  06/24–08/24 Mac-Gray cohort window is what models actually write.
- The interaction of the stock check with `Other-scope bid` units (§4) was not exercised —
  none of the three deals has one. My proposed entrant definition deliberately counts
  **whole-company** bidder units only, so a partial-scope-only bidder never enters and never
  needs closing; that is consistent with §4 keeping other-scope out of core counts, but it
  is untested and should be checked on a Meredith- or Kraton-type deal.
- Only Providence, Mac-Gray, PetSmart, Zep and Saks were worked through. Alex's Medivation,
  Imprivata, Penford and STEC blocks were not stock-checked (the brief asked for his other
  deals "where possible"; their filings are not in the repo and the deals raise no item-5/6/
  14/15 question that the five above do not).
- Alex's Providence row 6028 ("G&W · 04/13/2016", black, no bid note, no price) is an
  unexplained artifact of the RA sheet; I treated it as not adding a 26th signer.
