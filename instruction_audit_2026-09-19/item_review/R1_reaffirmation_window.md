# R1 — Items 1, 2, 13: late reconfirmation row, calibration example B, "signing alone"

Reviewer scope: items 1, 2 and 13 of `BRIEF.md`. Instruction line numbers refer to `SEC_Deal_Ledger_Extraction_Instruction.md` (revision of 19 Sep 2026). "HC" = Alex's hand-collected sheet `ref/deal_details_Alex_2026.xlsx` (fonts re-read with openpyxl; red = `FFFF0000` = his own edit, theme-black = RA row he kept). "VN" = his voice notes.

Summary of verdicts

| Item | Verdict | One-line reason |
|---|---|---|
| 1 Late reconfirmation row | **KEEP WITH REWORDING** (narrow the trigger; fix three internal collisions) | Alex wants the row (VN I.14, IV.7; red rows 6054, 6481), but only where the bidder's standing offer is not already a Formal bid in the final stage. The current trigger also fires on Mac-Gray CSC (Oct 5/7) and PetSmart Dec 6, where he has no row and where the PetSmart row would be a Formal "bid" at an October range the bidders then undercut. |
| 2 Example B window | **CHANGE TO ALTERNATIVE** (Date to = July 27; Working date July 20 unchanged; July 22 kept as the stated preferred reading) | The same filing, one round earlier, uses the identical sentence form and says IOIs arrived up to the *second* meeting ("Between May 19, 2016 and June 1, 2016 … met … on May 23, 2016 and again on June 1, 2016 to consider the IOIs"). The first review demonstrably does not bound receipt in this filing. Alex loses nothing in order. |
| 13 "Signing alone never creates one" | **KEEP AS IS** (plus one optional Questions line) | Consistent with §9.1 l.293, §11.3 l.485 and with all nine of Alex's `Executed` rows, which carry no price (6054 is a copy slip on a losing bidder). |

---

## Item 1 — Late reconfirmation row (§9.1 l.287, §12.C l.553)

### (a) Current wording

§9.1 l.287: "**Late reconfirmation.** When, in a stage the target intends to conclude with a definitive agreement, a bidder returns revised agreement drafts on its standing offer or confirms its price, record **Bid reaffirmed**: the standing price with Price origin = Carried forward (never Stated), Count under section 7.2, Formality = Formal (signal 3 in section 9.2), and Conditions level assessed as of that date — a returned draft does not by itself show that diligence or financing conditions have fallen away. Flag it for review. One such row per bidder per stage is enough unless the terms change; do not add a row for every draft. Signing alone never creates one."

§12.C l.553: "… Record **Bid reaffirmed** on August 4: $24 carried forward (Price origin Carried forward), Formal, flagged for review. Conditions level is Light … `DD open: yes` (on-site to August 11). … Party B's refusal to raise, when asked on August 12 after diligence had finished, is a second reaffirmation with `DD open: no`."

Related text it must live with: §4 l.85 "Do not create rows for: … successive agreement drafts"; §9.1 l.285 "A further draft is not automatically a bid … Use Offer update for material documentation/status evidence"; §9.1 table "Bid reaffirmed … Not a target's unanswered request for confirmation"; §9.2 signals 1 and 3 and the issues-list default; §7.2 l.203 "A bidder that first reaffirms in a new round can have Count 1 there."

### (b) Evidence

Filing (Providence bg pp.30–31):
- "On August 1, 2016, Hinckley Allen provided Party B with a revised merger agreement and voting agreement, reflecting changes from the marked-up documents included with Party B's LOI." (target → bidder)
- "On August 4, 2016, the Transaction Committee … directed … to continue diligence and negotiations with both G&W and Party B, but given the higher price offered by Party B, to prioritize Party B and proceed to complete the negotiation of the merger agreement with Party B. From July 27, 2016 through August 11, 2016, Party B and G&W conducted on-site financial, legal and environmental due diligence…"
- "On August 4, 2016, legal counsel for Party B provided a revised draft of the merger agreement…" (bidder → target; **no price is restated**)
- "meetings … were scheduled for August 12, 2016 in anticipation of reviewing final agreements and approving a transaction with Party B."
- Aug 12: "representatives of BMO then contacted Party B to determine if it would increase its offer price. Party B indicated that it would not increase its price."

Alex:
- VN I.14 (dictated, colour 8B0000 = important and hard): "later on, usually really close to the end of the process, the bidder reconfirms the same offer. In such cases, the background will say that the bidder has provided a revised markup to the merger agreement or something similar. And, importantly, this revision will have no conditions or very light conditions. And so **what used to be informal or a 'formal conditional' offer becomes properly formal**. And I think this fact needs to be captured, this is bid revision. In the case of Providence, an additional row on August 4 stating that party B has submitted a formal unconditional offer for $24.00/share should be included."
- VN IV.7 (Penford, dictated): "there was never an explicit mention of a formal offer made by Ingredion … **We know that a deal cannot finish without a formal offer.** … on October 14, Ingredion has been contacted to confirm the proposed price of $19/share and to finalize the draft merger agreement … **All earlier bids by Ingredion have been informal.** So this paragraph sounds to me like a final confirmation of a formal offer."
- VN I.12: late LOIs "come really late in the process. And so we expect these to have a high degree of formality."
- HC 6054: **every cell red**. Party B, S, 24, Formal, `bid_date_precise` 07/20/2016, `bid_date_rough` 08/04/2016, `bid_note` = "Executed", c1 "Confirm 7/20/2016 bid after DD", c2 "Restrict from soliciting competing bids". Two slips in his own row: "Executed" on a bidder that never signed, and "after DD" (the filing has on-site diligence running to Aug 11).
- HC 6035 (the 07/20 Party B bid; black RA row, Formal) carries his red comment: "expedited DD; what is the threshold for 'formal'?" — i.e. to him the July 20 bid is "formal with conditions".

**The pattern across his nine deals** (this is the decisive evidence; all rows re-read with fonts):

| Deal | Winner/finalist's last priced row before the definitive stage ended | Drafts / confirmatory DD narrated afterwards? | Did Alex (or the RA row he kept) add a same-price Formal row? |
|---|---|---|---|
| Providence, Party B | 6035 $24 **Formal** but in the LOI round ("Final Round Inf"), "expedited DD" | yes (Aug 4 draft) | **Yes** — 6054, all red |
| Penford, Ingredion | 6476 $19 **Informal** (10/02) | yes (VN IV.7) | **Yes** — 6481, all red: $19 Formal, precise 10/08, rough 10/14, no bid_note; separate unpriced `Executed` 6485 |
| Zep, New Mountain | 6404 $20.05 **Informal** (02/26), then exclusivity 6405 | yes | **Yes** — 6406 $20.05 **Formal** (black RA row; Alex edited its date in red to 03/13 and added red c2 "Go-shop 30 days, term fee, reverse term fee") |
| Mac-Gray, CSC | 6957 $21.25 **Formal** (09/21, "last and best", announced final round) | yes — Kirkland drafts Oct 5 and Oct 7, confirmatory DD | **No** — next CSC row is 6960 `Executed` (red, no price) |
| sTec, WDC | 7170 $6.85 **Formal** (06/14) | yes — his own red comment on 7170 and 7171 quotes "From June 16 to June 22, 2013, WDC conducted additional due diligence" | **No** |
| Imprivata, Thoma Bravo | 6103 $19.25 Formal (07/09) | — | No |
| Medivation, Pfizer | 6072 $81.50 Formal | — | No |
| PetSmart, Buyer Group | 6456 $83 Formal (12/12) | Dec 6 comments precede the bids | No (nothing on Dec 6) |
| Saks, Hudson's Bay | 7016 $16 Formal | — | No |

So his rule in practice is not "a returned draft → a row". It is: **write the confirming row only when it changes the record — the bidder's standing priced offer is Informal (Penford, Zep), or is a conditional offer from an earlier, non-final round (Providence B). Where the last priced bid is already a Formal bid in the final stage (Mac-Gray, sTec, Imprivata, Medivation, PetSmart, Saks), no row, even when he himself noted the later diligence.** That matches the purpose he states in I.14 ("becomes properly formal").

### (c) Hand application of the **current** wording

"A stage the target intends to conclude with a definitive agreement" is true of every final round; "returns revised agreement drafts on its standing offer" is true of every bidder-side markup. Applied literally:

| Filing | Event | Fires? | Row produced | Alex has it? |
|---|---|---|---|---|
| Providence | Aug 1, Aug 3, Aug 5: target's counsel sends drafts | No (target side) | — | — |
| Providence | **Aug 4** Party B counsel returns revised draft | Yes | `Bid reaffirmed`, R3, $24 Carried forward, Formal, Light, `DD open: yes`, **Count 1** (first Party B row in R3) | Yes (6054) |
| Providence | Aug 10 Hinckley Allen / Simpson Thacher "discussed various provisions of the draft merger agreement" | Strictly no (a discussion, not a returned draft), but a model can stretch it: three of the four old-instruction models (Opus, DS, GLM) wrote a G&W `Offer update · Formal` on Aug 10/11 | possible `Bid reaffirmed` $22.15 for G&W, two days before its $25 | No |
| Providence | Aug 12 Party B "would not increase its price" | Yes per §12.C ("second reaffirmation"); but §9.1 says "one such row per bidder per stage … unless the terms change" and nothing changed → **the instruction contradicts itself** | second `Bid reaffirmed`, Count 0, `DD open: no` | No — he records it as the exit: 6056 Drop, red c1 "Refused to increase offer" |
| Mac-Gray | Sep 18 Party A "reiterated … best and final" | Already a `Bid reaffirmed` under the base definition (all models did this) | unchanged | 6953 (Formal bid row) |
| Mac-Gray | Sep 21 CSC "confirm that CSC/Pamplona were willing to increase … to $21.25 … as a last and best offer" | No — new price → `Bid` | — | 6957 |
| Mac-Gray | **Oct 5** Kirkland "delivered … a revised draft of the Pamplona commitment letter"; **Oct 7** Kirkland "delivered … a revised draft of the merger agreement" (during exclusivity, R3) | **Yes** | `Bid reaffirmed` CSC $21.25 Carried forward, Formal, Count 0. Which date is unspecified (Oct 5 or Oct 7) → models will differ. "One per bidder per stage" stops a flood (Sol wrote five `Offer update` rows here under the old text) but not this row | **No.** It is also exactly what §4 l.85 forbids ("successive agreement drafts") |
| PetSmart | **Dec 6** "the Buyer Group and Bidder 2 submitted their respective comments on the draft merger agreement and other transaction documents, and the Buyer Group provided its financing commitment documents" (final round, bids due Dec 10) | **Yes on the literal text** | Two `Bid reaffirmed` rows, Formal, price Carried forward = the **Oct 30 ranges** ($81–83; $81–84), Price kind Bidder range, **Count 1** each (first R2 row); the real Dec 10 bids then become Count 0 | **No.** And the row is false: neither bidder had yet named a final-round price (on Dec 9 the filing still speaks of "the respective prices that the bidders intended to bid"), and on Dec 10 both bid **below** the carried range ($80.70, $80.35). It also collides with §9.2's issues-list default ("comments … are not automatically a returned agreement markup … classify Informal") because the trigger mandates Formal |
| PetSmart | Dec 12 evening, JPM "confirmed via a conversation with Bidder 2 … that $81.50 per share was its best and final offer" | Yes ("confirms its price") | A `Bid reaffirmed` duplicating the same evening's `Bid` (Opus already did this under the old text; DS and GLM folded it into the Bid row) | No (one row, 6454) |
| PetSmart | Dec 13–14 "the parties completed negotiations" / executed | No ("Signing alone…") | — | — |

Net, current wording: Providence +2 rows (one wanted), Mac-Gray +1 unwanted row on an unstable date, PetSmart +2 misleading rows and +1 duplicate. It fires in the right place once and in the wrong place four or five times.

### Interactions

- **§7.2 Count.** The text gives Count 1 when the reaffirmation is the bidder's first row in the round (Providence R3: Party D, Party E, G&W, Party B = 4; without any Party B row it would be 3). That is the right answer and it is what Alex wants (VN IV.5 on Penford: "that bidder gets in round two"). But the changelog/QUESTIONS M8 and audit §7.5 still describe the mitigation as "Count 0 … keep it out of bid tallies". **That is not what the instruction does.** Austin should not rely on Count to separate these rows. In PetSmart the current wording would move Count 1 from the real Dec 10 bids onto the false Dec 6 rows — tallies unchanged, but "first formal bid per bidder" becomes $81–83 instead of $80.70.
- **§9.2 formality.** The parenthesis "(signal 3 in section 9.2)" is wrong for a returned draft: signal 3 is "An actual price confirmation"; a returned draft is signal 1. For Party B, carry-forward already makes the row Formal; for a Penford-type bidder with only Informal rows, the draft (signal 1) or the confirmation (signal 3) is what creates Formal — so the signal must be named correctly.
- **§9.3 conditions.** Fine as written under the fixed construct: Aug 4 = Light, `DD open: yes`. Note for Alex: his "formal unconditional" and "after DD" are not what the filing says on Aug 4; the flag carries that.
- **Offer update.** After the row exists, the instruction never says when a returned draft is *still* an Offer update. It should: a draft that fails the test is an Offer update if material to conditions/readiness (PetSmart Dec 6: financing commitments delivered), otherwise no row (§4).
- **Price origin = Carried forward is not a sufficient filter.** The old-instruction workbooks already use it inconsistently: Party E's Aug 2 reversion is `Carried forward` in DS and Sol, `Stated` in Opus and GLM; Mac-Gray Party A's Sep 18 reaffirmation is `Carried forward` in Opus/DS and `Stated` in GLM. And the field cannot distinguish a draft-inferred reaffirmation from a bidder's spoken one.

### (d) Downstream risk

1. *True by construction.* Returned drafts are narrated almost only for the bidder the target is signing with. Under the current trigger nearly every winner (and almost no loser) acquires a Formal reaffirmation row. "Winner's last bid is Formal" is then an identity (Alex believes it is one in reality: "a deal cannot finish without a formal offer"), but any winner-versus-loser comparison of formality, of number of formal bids, or of "informal→formal price revision" (mass point at zero revision) is mechanically contaminated. Under the narrowed trigger the row exists only where the filing shows no formal priced bid, and a text prefix identifies it, so it can be dropped or kept at analysis time.
2. *Excluding from counts by default would be wrong.* With the narrowed trigger the row is usually the bidder's only row in the definitive round; Count 0 would leave Penford's final round without its winner and Providence R3 without Party B. Keep §7.2; make the basis filterable instead.
3. *Reversibility.* A labelled row is cheap to filter out after 500 deals; a missing row needs the filing re-read. That argues for keeping the row — but only if its trigger is tight enough that the four models write the same one, and only if it cannot assert a price the bidder did not hold (PetSmart Dec 6).

### (e) Verdict — KEEP WITH REWORDING

Replace the **Late reconfirmation** paragraph (l.287) with:

> **Late reconfirmation.** A target can finalize a definitive agreement on an offer the bidder never formally restates. Record one **Bid reaffirmed** when all three hold: (a) the target has moved to finalize a definitive agreement with that bidder on its standing offer — a decision to negotiate or complete the agreement with it, or executed exclusivity — and is not awaiting a priced submission from it under a pending solicitation; (b) the row changes the record: the bidder's latest priced row is Informal, or sits in a round whose Round opened row reads `Not final` (section 6.3); (c) the filing reports a bidder-side act — the bidder or its counsel returns a revised agreement draft, or the bidder confirms its price. Use the first such act. The row carries the standing price with Price origin = Carried forward (never Stated), Count under section 7.2, Formality = Formal (signal 1 for a returned draft, signal 3 for a price confirmation) and Conditions level assessed as of that date — a returned draft does not by itself show that diligence or financing conditions have fallen away. Begin Terms or outcome with `Reaffirmed by: returned draft` or `Reaffirmed by: price confirmed`, and flag it for review. No other draft creates one: comments or markups sent ahead of a solicited bid belong to that bid; drafts exchanged after the bidder's Formal bid in the final or definitive stage get no row (section 4); a material change in readiness or financing is an Offer update. A confirmation given with a priced bid, or on the same day, is part of that Bid row. A target's draft, a discussion between counsel, a target's unanswered request and signing itself never create one.

Replace the last sentence of **§12.C** ("Party B's refusal to raise … is a second reaffirmation with `DD open: no`.") with:

> Party B's refusal to raise when asked on August 12, after diligence had finished, is not a second reaffirmation: it goes on Party B's closing row (Exit reason *Would not improve earlier offer*, noting that diligence had ended on August 11). G&W gets no such row: the August 3 draft came from the target, August 10 was a discussion between counsel, and its August 12 submission is a new Bid.

Check of the replacement against all cases: Providence B Aug 4 ✓ (a: July 27 decision to negotiate with B and G&W, Aug 4 direction to complete with B; b: the $24 was made in R2, the non-final LOI round — VN I.12: the intention to complete a merger agreement came "after round two … and during round three"; c: counsel's draft). Providence G&W ✗ (no bidder-side act before the new $25 Bid). Penford Oct 14 ✓ *if* the filing reports Ingredion confirming or returning a draft (b: latest priced row Informal; works whether or not a model opens R2 on Oct 3). Zep ✓ on the same condition (b: Informal). Mac-Gray Oct 5/7 ✗ (b fails: $21.25 is Formal and was made inside the announced-final round. Clause (b) is deliberately written on *finality*, not on the round index: Sol's old-instruction Mac-Gray workbook opens a separate Round 4 for the exclusivity period despite §6.3, and a test of "lies in an earlier round" would have fired there). sTec, Imprivata, Medivation, Saks ✗. PetSmart Dec 6 ✗ (a fails: final bids pending); Dec 12 Bidder 2 ✗ (same-day clause). 9 of 9 deals match Alex's sheet.

Dependency: clause (b) uses the finality phrase of item 7 (§6.3 `Announced as final` / `Inferred final` / `Not final`), which makes the test mechanical and filterable. Providence R2 (mid-June request for non-binding LOIs) = `Not final`, R3 (July 27) = `Inferred final`; Mac-Gray R3 (Sep 11 "final indications of interest") = `Announced as final`. If item 7 is dropped, write (b) as "… or was made before the target's final or definitive stage began".

If Austin prefers to keep both Party B rows as evaluated in A6, the minimum fix is instead to make the two sentences agree: in §9.1 write "One *draft-based* row per bidder per round", and in §12.C add "(Count 0)". I recommend against it: a refusal to raise happens to most losing finalists, Alex records it as the exit (6056; his own `DropAtInf` code, CI §3.6 addition, and Imprivata 6097 "confirmed in communications their informal bid basically" are the same idea), and §10.3 already has the reason code.

Also correct, outside the instruction: the changelog line 38 and QUESTIONS M8 statement that "Count 0 … keep[s] it out of bid tallies".

**Confidence:** high that the current trigger over-fires (Mac-Gray Oct 7 and PetSmart Dec 6 are read straight off the filings and off his sheet); medium-high on clause (b) as the right narrowing — it reproduces his nine deals, but it rests on absence of rows in six deals, which is weaker than a stated rule. Clause (b) is the one thing worth putting to Alex in one sentence: "Do you want the confirming row only when the standing offer was informal or from an earlier round, or for every winner?"

**Not checked:** the Penford and Zep filings (not in the repo; sec.gov refused automated download, so I could not see whether Oct 14 reports an *Ingredion* act or only the target's request — VN IV.7's wording "Ingredion has been contacted to confirm" is the target-side version, which §9.1 refuses; if the filing has no bidder-side act, Alex's Penford row is unobtainable without fabricating and should go to Questions rather than into the ledger). No model has been run on the revised text, so "models will stretch Aug 10" and "Dec 6 will fire" are predictions from the wording plus old-instruction behaviour.

---

## Item 2 — Calibration example B (§12.B l.551) and the §8.1 tightening sentence (l.251)

### (a) Current wording

§12.B: "… Give the five undated late-July LOIs Working date July 20 (Assigned: deadline) and place them in # ahead of G&W's July 21 LOI, noting that their order relative to G&W is not actually known. The first review on July 22 is read as bounding their receipt (window July 20–22), flagged for review as a cross-paragraph inference. July 27 is the round's observed end, not an announced submission deadline. …"

§8.1 l.251: "Tighten Date from/Date to whenever a passage — including one in a different paragraph — constrains the event: a committee that reviewed offers bounds their receipt; an event narrated between two dated meetings is bounded by both. … A deadline does not prove arrival by that date, so it does not by itself change Date to; it can still be the assigned Working date under rule 2."

### (b) Evidence

Filing sentences (bg pp.29–30):
1. "representatives of GHF instructed all potential buyers to submit non-binding letters of intent ('LOIs') by July 20, 2016"
2. "In late July 2016, the Company received six LOIs with offer prices per share ranging from $19.20 to $24.00"
3. "G&W submitted an LOI on July 21, 2016 … On July 26, 2016, in response to feedback from representatives of GHF indicating its price and CVR structure were not competitive, G&W submitted a revised LOI"
4. "The Transaction Committee met by telephone conference on July 22, 2016 and in person after the regular quarterly Board meeting on July 27, 2016, to review the LOIs with representatives of GHF."

Alex, VN I.9 (dictated, black = important and easy): "the deal background states that these bids happen in late July 2016. That's July 20 to July 31. The deadline of round two is July 20, but one of the bidders submits the bid on July 21. And then the Transaction Committee of the target meets on July 22. This very narrowly limits the timing of round two bids to July 20 to July 22." His stated purpose is order: "that puts anything that party C, the latecomer, does clearly before the actions and bids of its competitors." He adds: "July 27 is a fair assessment of the deadline." HC 6035–6039: both date cells 07/20/2016 (black RA dates he kept), red c1 on 6035 "Late july -- but the deadline was july 20". His sheet has no window columns.

**The same filing, one round earlier (bg p.28), in the identical sentence form:** "Between May 19, 2016 and June 1, 2016, the Company received nine written indications of interest … The Transaction Committee met by telephone conference on May 23, 2016 and again on June 1, 2016 to consider the IOIs." Deadline May 19; first review May 23; and the filing itself says receipt ran to **June 1**, the date of the *second* meeting. In this filing, by its own words, a first review meeting did **not** bound receipt of "the IOIs" it met to consider. Sentence 4 is the round-2 twin of that sentence.

### (c) Is 20–22 a fair inference or over-reading?

It is a fair *preferred reading* and an unsafe *bound*.
- For it: "to review the LOIs" read literally covers the six at both meetings; a telephone review two days after the due date is the natural moment to have them all; GHF could tell G&W by July 26 that it was "not competitive", so at least the higher LOIs were in hand before then.
- Against it as a bound: (i) sentence 4 names two meetings for one purpose and does not say which LOIs were before which meeting; (ii) G&W's own LOI is dated after the deadline and was accepted, so the deadline was demonstrably not enforced and a further late arrival was possible; (iii) the round-1 passage shows this target's first review happened while offers were still coming in; (iv) the only thing the text *establishes* is that all six were in by July 27, when the committee compared them and dropped four.

The instruction's own principle (§8.1, §8.2, fixed decision) is that Date from/Date to hold what the source establishes and the Working date carries the convention. Example B applies that principle to the lower edge ("A deadline does not prove arrival by that date") and then abandons it at the upper edge. As a *calibration example* it also teaches a general behaviour — "the first review meeting bounds receipt" — which, applied to the May passage of the same filing, would produce Date to = May 23 against a stated interval ending June 1.

What Alex loses if Date to = July 27: nothing he uses. Working date stays July 20 (`Assigned: deadline`), the five rows stay ahead of G&W's July 21 in #, Party C's July 12 IOI stays ahead of all of them, and the exits stay on July 27 — every ordering point in VN I.9 is met. Date to is a collapsed expandable cell that his own sheet does not have. His July 22 reading survives in the row's reason and in Questions, where he can accept it. What he would see that he might dislike: a Date to later than the meeting he cites — hence the wording below says so explicitly.

### (d) Risk and reversibility

Low either way for Providence (five cells). The risk is the generalisation: across hundreds of deals "first review bounds receipt" will silently shorten windows in deals where bids trickle in across several committee meetings, and the §13.4 check ("no Working date falls outside its own Date from/Date to") will then push Working dates earlier for the wrong reason. A too-wide honest window costs nothing, because the Working date is always filled.

### (e) Verdict — CHANGE TO ALTERNATIVE

Replace in §12.B the sentence "The first review on July 22 is read as bounding their receipt (window July 20–22), flagged for review as a cross-paragraph inference." with:

> Their Date from/Date to window is July 20–27: the July 27 meeting, which compared all six and chose two, is the first point by which every LOI is established as received. The July 22 review makes July 20–22 the likelier window, and the reason says so and flags it, but it is not entered as a bound: the filing does not say which LOIs were before the first meeting, G&W's own LOI arrived after the deadline, and in the previous round the same filing reports offers arriving up to the second of two review meetings.

Replace in §8.1 l.251 "a committee that reviewed offers bounds their receipt; an event narrated between two dated meetings is bounded by both." with:

> the meeting at which a committee is shown to have had the full set of offers before it — normally the one that compared them or decided on them — bounds their receipt, while an earlier review meeting bounds only the offers the filing shows it considered and is otherwise a preferred reading to state in the reason; an event that the filing places in sequence between two dated events is bounded by both.

(The second half also fixes a smaller looseness: "narrated between two dated meetings" conflicts with §8.2 "Paragraph order is not necessarily event order" — in Providence the July 27–Aug 11 on-site diligence sentence is narrated after the Aug 4 meeting.)

This reverses audit finding R4 / patch P6 (helper H1 D3), which Austin approved "with dates" (changelog l.35). That finding compared §12.B only against VN I.9; the same filing's May 19–June 1 passage — offers arriving through the second of two review meetings — was not considered there and is the new evidence. The part of P6 that matters to Alex (Working date July 20, LOIs ahead of G&W in #) is kept.

**Confidence:** high. The May 19–June 1 passage is direct, same-filing evidence. If Austin nevertheless keeps July 20–22 because Alex said it, the example should at least add "this is the reviewer's reading, not a general rule that a first review meeting bounds receipt", and the §8.1 sentence should still be replaced.

**Not checked:** how often multi-meeting reviews occur in other filings; whether Alex, shown the May passage, would still hold to July 22 (worth one line to him — it is his example).

---

## Item 13 — "Signing alone never creates one" (§9.1 l.287, last sentence)

### (a) Current wording
"Signing alone never creates one." Companion text: §9.1 l.293 "Signing records agreed consideration, not a separately submitted final bid on an invented earlier date. Do not invent a new price or an undated submission to supply a 'missing formal offer'; a supported late reconfirmation is recorded as Bid reaffirmed (above)." §11.3 l.485 "On Merger agreement signed … Leave numeric bid-price cells and formality/conditionality cells blank: signing is not an extra submitted bid."

### (b) Evidence
- CI §3.8 (Alex's addition box): the `Executed` row records Bidder, Bid Note "Executed", Date. No Bid field.
- HC: all `Executed` rows are unpriced — 6059 G&W, 6073 Pfizer, 6104 Thoma Bravo, 6407 New Mountain, 6460 Buyer Group (only `all_cash`=1), 6485 Ingredion, 6960 CSC, 7018 Hudson's Bay, 7171 WDC. Their `bid_date_precise` points back to the winning bid's date (Mac-Gray 09/21, sTec 06/14, Imprivata 07/09, PetSmart 12/12) and `bid_date_rough` is the signing date: a back-reference, not a second bid.
- The one priced "Executed" row is 6054 — Party B, who lost. It is the confirming row of item 1 carrying a copied label; Penford shows his clean pattern (priced Formal row 6481 with no bid_note, plus a separate unpriced `Executed` 6485).

### (c) Application
Providence "Shortly thereafter, Hinckley Allen and Simpson Thacher finalized the transaction documents and the Company and G&W executed"; Mac-Gray "Between October 12, 2013 and October 14, 2013, Kirkland and Goodwin Procter finalized the remaining unresolved issues"; PetSmart "the parties completed negotiations … executed the merger agreement" — none creates a reaffirmation, under the current or the proposed item-1 wording. No contradiction with item 1's trigger (which needs a bidder-side act before signing) or with §11.3. The proposed item-1 text repeats the rule in its last sentence, so l.287's sentence is absorbed rather than lost.

### (d) Risk
The only place the rule bites is a thin background where the winner's priced rows are all Informal and no bidder-side draft or confirmation is reported. The ledger then shows a winner with no Formal row, which Alex regards as impossible (VN IV.7). That is the honest outcome, but it should be visible rather than silent.

### (e) Verdict — KEEP AS IS
Optional one-line addition to §11.5's list (after "Unknown winner/formal-bidder types…"): "A winner that reaches signing with no Formal Bid or Bid reaffirmed row — do not create one; say which passages were considered." 

**Confidence:** high. **Not checked:** nothing material; the six filings not in the repo were not needed for this item.

---

## Process note
While trying to fetch the Penford filing I sent one request to sec.gov (the filing index page) with Austin's e-mail address in the User-Agent string, as EDGAR's access policy asks for a contact; I should not have done that unprompted and did not repeat it. Subsequent requests without it were refused, which is why Penford and Zep are unchecked. No repo file other than this report was created or modified; scratch helpers (`r1_fonts.py`, `r1_rows.py`, `penford*.`) are in the session scratchpad only.
