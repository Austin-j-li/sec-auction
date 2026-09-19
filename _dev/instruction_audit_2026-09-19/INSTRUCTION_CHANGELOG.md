# Instruction revision of 19 September 2026: change log for review

- Current instruction: `SEC_Deal_Ledger_Extraction_Instruction.md`. The previous text (Pro revision, 18 Sep 2026) was deleted from the repo on 19 Sep at your request; an identical copy is inside `model_review_2026-09-18/SEC_12_Extraction_Review_Package.zip`.
- Line diff against the 18 Sep text: `instruction_audit_2026-09-19/instruction_changes.diff`.
- Record of every edit: `instruction_audit_2026-09-19/apply_instruction_patch.py` (one tagged, asserted replacement per edit; its header says how to rebuild from the 18 Sep text in the zip).
- Nothing has been run with the revised instruction. Size: 8,939 words (18 Sep) → about 11,700 after batches 1–2 → about 13,600 after batch 3 (+52% overall; batch 3 alone +16%).
- Batch 3 only: `instruction_audit_2026-09-19/batch3_changes.diff`; its edits are in `apply_batch3.py`, which rebuilds the current text from `instruction_before_batch3.md`. The reviews behind batch 3 are in `item_review/`.

Status key: **Approved** = you approved it on 19 Sep 2026. **Provisional** = approved in substance but contains a default that one of the open questions for Alex could change. **Rode along** = I told you it would ride along; you did not answer it separately. **Proposed** = small audit edit I did not itemise for you; drop it if you prefer.

## New schema items (three expandable columns, one label)

| Item | Why | Status |
|---|---|---|
| `Page` column | Alex asked for the page beside each row | Approved |
| `Date method` column (Reported / Inferred (cross-paragraph) / Assigned: deadline / decision day / midpoint / bound / sequence) | A separate column keeps `Date basis` a clean drop-down; says how each Working date was chosen | Approved (dates); column design is mine |
| `Outcome basis` column (Stated / Inferred: residual / Inferred: exclusivity / Inferred: silent / Inferred: identity — the last added in batch 2) | Your condition for closing out every NDA signer: say clearly in what fashion they were out. A column filters and exports more reliably than a text prefix; Terms must begin with the same words | Approved (exits); column design is mine |
| `Information access changed` label | Keeps the information-access rows you want and stops `Material process update` being a catch-all | Approved (scope); label is my design |

## Edits by topic

| Topic | Sections touched (patch tags) | What changed | Status |
|---|---|---|---|
| Header | title, preamble (H1–H3) | Marked "Revision of 19 September 2026", no version number, not yet run or reviewed by Alex. "No companion document… is required" kept | Housekeeping |
| Rollover is not a group change | §5.3, §11.3 (S5.3a, S5.3b, S11.3b) | `Bidding group changed` only when a party that could have bid independently joins or leaves the bidding unit; a rollover holder or financing provider never triggers it, even if the filing's defined buyer term later includes it | Approved |
| Never-entered party gets no outcome row | §10.1 (S10.1d, 2nd paragraph) | Outcome labels apply only to a participant that entered the process; declining to invite an outsider is a `Target decision` | Approved |
| Exclusivity drops rivals; `Re-entered` | §10.1 table and text, §12.E, §13.3 (S10.1a–d, S12E1, S12E2, S13.3, C4) | Executed exclusivity → each live rival `Dropped by target` on that date, basis `Inferred: exclusivity`. `Participation paused` restricted to a bidder's own or an expressly temporary stop. A bid after a recorded outcome requires `Re-entered` | Approved. Lapsing-exclusivity case (Synacor) still open for Alex (A11) |
| Declined to raise | §10.3 (S10.3b) | Exit reason `Would not improve earlier offer` even when Decided by is Target | Approved |
| Post-deadline call for improved bids = extension | §8.3 (S8.3a) | Recorded as `Deadline revised`, treatment Extended; not a new deadline, not a round | Approved |
| First final solicitation opens a round | §6.3 (S6.3a, S6.3b) | The first final / binding / best-and-final request opens a round even with unchanged bidders; only *further* improvement requests do not | Approved |
| CVR / earn-out = all cash | §9.4, §12.D (S9.4, S12D) | All cash = Yes unless the contingent piece is paid in securities; fixed part in Cash at closing | Approved |
| Renamed adviser | §5.4 (S5.4) | Never a second adviser row for a renamed or acquired firm | Approved |
| Financing wording | §9.3 (S9.3) | One fixed phrase on every bid row (`Financing: committed / represented available / explicitly not committed / not stated`); never "not provided" from silence | Approved |
| Exact counts stay exact | §7.3 (S7.3) | Do not add "at least" the filing does not use; check narrative counts against board-update or Reasons totals | Approved |
| Every row gets a sortable date | §2 bullet, §3.3, §8.1, §8.2, §11.2, §11.5, §13.4 (S2-dates, S3.3a, S8.1a–g, S8.2, S11.2a, S11.5b, S13.4) | Working date always filled by a six-rule order (reported/inferred day → deadline → decision day → midpoint → bound → sequence), then an order constraint; Working dates never decrease down the ledger; honest window stays in Date from/Date to; cross-paragraph tightening now encouraged; assigned dates never labelled Reported | Approved. **Provisional:** rule 4 (midpoint inside a vague window) pending A1 |
| Calibration example B | §12.B (S12B) | Undated late-July Providence LOIs get 07/20 (deadline), sit ahead of G&W's 07/21 in #, window 07/20–07/22 flagged as cross-paragraph inference | Approved with dates. **Provisional:** the 07/22 upper bound is Alex's reading, flagged in the text |
| Close out every participant | §2 bullet, §3.3, §10 heading, §10.1 heading, §10.2 (rewritten), §10.3, §11.2, §11.4, §11.5, §12.A, §12.E, §13.2, §13.3 (S2-exits, S3.3b, S10.1h, S10.2, S10.3a, S11.2b, S11.4a, S11.4b, S11.5a, S12A, S12E2, S13.2, S13.3, C1–C3) | Every participant that entered a stage gets an exit row; stated outcomes first, then one inferred row per residual cohort at the earliest revealing transition (table of three situations); arithmetic shown; uncertain base → row with Count blank and a flag; Summary shows per-stage balance with the inferred share; every inferred row listed in Questions | Approved. **Provisional:** how these export to Alex's Drop code (A3); a named party possibly inside an anonymous residual is covered by the cohort row, not individually (A13); a terminated process closes its participants via the `Process terminated` row (my default — not discussed) |
| Scope cut, information access kept | §4, §11.3 (S4a, S4b, S11.3a) | No rows for deal-terms negotiation, successive drafts, post-NDA meetings/calls/visits, rollover or financing-support threads (max one row formed + one resolved); post-signing limited to competing proposals, go-shop, termination, closing; information-access changes kept as rows, one per distinct change | Approved |
| Late reconfirmation | §9.1, §12.C (S9.1a, S9.1b, S12Ch, S12C) | A returned draft or price confirmation late in a definitive-agreement stage → `Bid reaffirmed`, price Carried forward, Formal, conditions assessed as of that date, flagged; one per bidder per stage. Example C now records Providence Party B on 08/04 (Heavy, diligence open) and again 08/12 (Light) | **Rode along. Provisional:** Aug 4 vs Aug 12 pending A6 |
| Round finality phrase | §6.3 (S6.3c) | `Announced as final / Inferred final / Not final` at the start of Terms on each `Round opened` row | Proposed |
| Deadline treatment phrase | §8.3 (S8.3b) | `Treatment: …` at the start of Terms on each `Deadline` row; new value `Passed without action` for soft deadlines (Alex's STEC note). "Enforced requires positive support" left as is | Proposed. **Provisional:** definition of Enforced pending A7 |
| Counts in the consult list | §1 (S1-counts) | "…to resolve buyer type, consideration, dates, **counts** and conflicts" | Proposed |
| New-process test | §6.2 (S6.2) | New participants after dormancy → new process; same participants resuming → same process (Alex's Synacor note) | Proposed |

## Batch 2 — from the questions evaluation (added 19 Sep 2026, after batch 1)

Source: `QUESTIONS_evaluation.md`. Patch tags start with `B2-`. **Agreed** = you said yes to it as one of the three discussion items. **Recommended** = from the "rest" list, which I endorsed and you did not object to but did not confirm item by item; drop any by deleting its tagged line.

One more schema item: a `Conditions detail` column (fixed format: `Fin: …; DD required: …; DD open: …; Excl: …`). It replaces the batch-1 `Financing:` text phrase, which is gone.

| Topic | Sections touched (tags) | What changed | Status |
|---|---|---|---|
| What "Heavy" means | §9.3 rewritten, §11.2, §13.5, §12.C, §12.D (B2-cond, B2-cond2–5, B2-exC, B2-exD) | Conditions level now rates what the bid itself carries. Heavy = financing reported not committed, or a further substantive (multi-week or exclusive) diligence period, or another material stated condition. Light = no Heavy trigger and only confirmatory / expedited diligence or documentation left, or committed financing with no diligence condition. None = reported ready to sign. Early non-binding indications before diligence access stay Heavy by context. Financing silence neither raises nor lowers the level. Whether diligence was in fact still open goes in `DD open` and does not move the level. Example C: Party B on 08/04 is now Light with `DD open: yes`. Struck: "a specified number of diligence days alone does not establish Heavy" | **Agreed. Provisional:** the Light/Heavy line for stated diligence periods ("expedited" vs "three-week") rests on five of Alex's Providence cells — first thing to show him |
| Close-out: uncertain base | §10.2, §12.A (B2-base, B2-exA) | Count = the filing's stated base − evidenced exits, Terms "Inferred: residual (base assumes …)" with the range; "≥" when the base is a lower bound; blank only when the filing gives no number | **Agreed** (replaces batch 1's "leave Count blank") |
| Close-out: named party that vanishes | §10.2, §10.3, §5.2 (B2-base, B2-basis, B2-5.2) | One Count-0 exit row, Outcome basis `Inferred: identity`, naming the cohort that already counts it and the alternative reading; listed in Questions; counts never move from a cohort to a name | **Agreed** (replaces batch 1's "covered by the cohort row only") |
| Deadline treatment defined | §8.3 (B2-enf) | Extended / Late bids accepted / Enforced / Passed without action / Unclear, each defined from rows already in the ledger. Enforced = date passed, no extension, target took its next step on the bids in hand. Struck: "Enforced requires positive support for an actual cutoff" | **Agreed** |
| Stock check; go-shop | §13.3, §10.2 (B2-stock, B2-goshop) | Participant stock per stage = entrants − exits + re-entries, never negative, only the winner left at signing; go-shop entrants closed at go-shop expiry | Recommended |
| Round 1 start | §6.3 (B2-R1) | R1 opens at the target's first solicitation of buyers (first outreach wave, or the launch decision when outreach follows at once); a sale decision or press release that defers outreach stays round 0; the round-1 row states `R1 anchor:` and lists the other candidate rows so the boundary can be re-cut. **Superseded by batch 3** (the batch-2 wording did not in fact reach Oct 3 for PetSmart, which has no outreach wave, and its bilateral clause could have pulled Mac-Gray's round 1 back to the Apr 8 call) | Superseded |
| "At least $X" | §9.4 (B2-bound) | X goes in Price low, Price high blank, Price kind Bound only, Terms begins `Bound: ≥ X`; ambiguity raised in Questions. Replaces "leave both price cells blank" | Recommended |
| Financing supporter; cohort members combining | §5.3 (B2-support) | Supported bidder keeps its name and Type with `Support: [party] (financing)`; supporter gets Joined group only if it was still a live bidder; when anonymous signers combine, the row states "units −1"; never backfill an NDA the filing does not report | Recommended |
| Adviser dates | §5.4 (B2-adviser) | Working date = earliest date the adviser is shown selected or acting; all disclosed dates listed | Recommended |
| Signing is not a reaffirmation | §9.1 (B2-signing) | "Signing alone never creates one" | Recommended |

Needs no instruction change (handled at export, or already in batch 1): within-window day (midpoint after order constraints), residual exit label and Alex's Drop code, legacy formal/informal label (computed as Formal and not Heavy), both Party B reaffirmation rows, cohort rows vs a1…aN, all-cash presumption for financial buyers, PetSmart Bidder 3's $78 (already an exit in all four models), lapsing exclusivity, information-access rows.

Still open, not blocking: **will any Chicago-coded deals be pooled with AI-extracted deals without re-extraction?** If yes, Alex's legacy codes need an exact crosswalk.

## Batch 3 — after the item-by-item review (approved by you on 19 Sep 2026, including the one call)

Five review agents tested the 15 unconfirmed items by hand against the three filings and Alex's documents (`item_review/R1`–`R5`). You approved all recommendations. Tags in `apply_batch3.py`: `i1`…`i12` = the numbered items, `fix-` = faults found in rules approved earlier, `trim-` = cuts that do not change meaning.

Two more schema items: `Round finality` and `Deadline treatment` columns, in the collapsed group next to `Due date`. They replace the text prefixes of batch 1 (the old workbooks wrote four treatment values in nine spellings). The ledger is now 14 visible + 25 expandable columns; §11.2 fixes their left-to-right order and §11.1 lists the controlled columns and requires exact strings.

| Item | What changed | Note |
|---|---|---|
| 1 Late reconfirmation | Three-part test: target has moved to finalize with that bidder; the bidder's latest priced row is Informal or in a Not final round; the filing reports a bidder-side act. Tag `Reaffirmed by: …`. Party B's Aug 12 refusal moves to its exit row. | Reproduces Alex's nine deals on paper; **Penford filing not read** — if it reports only the target's request to confirm, his Penford row cannot be produced and should surface in Questions. Count on the row is 1 when it is the bidder's first row in the round (the earlier "Count 0" note in this log was wrong). |
| 2 Providence example B | Window July 20–27; Working date still July 20; July 22 kept as the flagged preferred reading. General "tighten the window" sentence narrowed to the meeting shown to have had the full set of offers. | Reverses part of the batch-1 date edit. |
| 3 Round-1 start | Ordered test: first outreach wave; launch decision if outreach begins within about a week; for inbound-only processes the first target-organized admitting step (NDA wave or process letter); bilateral negotiations. A single exploratory approach never opens round 1. | PetSmart reaches Oct 3 via the NDA wave bounded by the Oct 3 meeting; Mac-Gray stays Jun 24. |
| 4 Price bounds | Floors in Price low, ceilings in Price high, `Bound: ≥ X` / `Bound: ≤ X`; a Bound only row is never a bid level; valuation statements and premium/aggregate bounds stay in text. | |
| 5 Terminated process | `Process terminated` row carries Count of those still live; closure is per process; a participant reappearing in a later process enters afresh. | No example among the three deals. |
| 6 Supporter / combining | Live financier → Joined group if it became part of the bidding unit, else Withdrew with a `Support:` note; individually recorded members that combine are each closed by Joined group; assumption about finalist status must be stated; rollover thread may have a "denied" row. | |
| 7, 8 Finality and deadline treatment | Controlled fields, defined values; only Extended and Late bids accepted combine; a bid is late only if its Date from is after the due date; target-solicited improvements from on-time bidders are not late. | |
| 9 Counts | "…and to cross-check counts (section 7.3)". | |
| 10 New-process test | One-directional: new participants support a new process; returning ones prove nothing alone (Alex's Zep). | |
| 11 Design choices | `Inferred` (renamed); Date method stated for inferred closing rows and after an order-constraint move; opener on inferred rows only; identity row takes the covering cohort's label; `Information access changed` narrowed to differentiated/staged/withheld/catch-up access and projections issued or changed mid-process — uniform access is stated on the NDA, Round opened or selection row. | **Narrows the "keep information-access rows" decision**: expect 1–2 such rows per deal. |
| 12 Adviser dates | Earliest date applies to the first row of that mandate only; later engagement/termination/re-engagement rows keep their own dates. | |
| 13 Signing never a reaffirmation | Unchanged (now inside the item-1 paragraph). | |
| 14 Stock check | Entrant defined (first NDA, Bid or admitting decision; once per unit); exits listed; group "units −1" moves the stock. | Balanced to exactly one bidder in all three deals on paper. |
| 15 Go-shop | Label and basis named; a go-shop party that made a proposal is closed by that proposal's outcome. | |
| Your call | A bidder that bid, is absent from the advancing set and is not reported as told: Dropped by target, Inferred: residual, Decided by Target, dated at the advancement decision. | |
| Faults fixed in approved rules | "Entered the process" = under NDA, bidding or actually participating (not merely responsive to contact); late submitters are not swept as absent; an inferred exit may never precede its entry (the entry date moves); three older Count sentences reconciled with §10.2; `Fin:` gains `no contingency` and `not needed`; "final due date" and the finality vocabulary made consistent; inferred rows say what to quote and which Round they carry; Tags convention; §13 checks that tags, fields and date pairs agree. | |
| Trims | About 200 words of restatement removed (§2, §3.3, §6.3, §8.1 table, §9.1, §9.3, §12.A, §12.E). | |

Still provisional, to show Alex on re-run workbooks: the midpoint-in-window rule; the Light/Heavy line for stated diligence periods; clause (b) of the reconfirmation test; residual exits exported as his Drop code; the Count-0 identity row. Open question for you or Alex: will Chicago-coded deals be pooled without re-extraction?

## Deliberately not changed

- **No interactive pause.** §1 "Continue without requiring a reply" stays, as you decided.
- After batch 2, nothing in the instruction still waits on Alex; the items to show him are listed in `QUESTIONS_evaluation.md` §4.
- Audit edits held back as too minor or not yet discussed: initiation phrases ("Initiating bid", "Decision includes public announcement"), public / non-US suffix on Type, two review-list clauses (absence of an extension; adviser duplication), filing URL in Summary.
- Pro's cautions the audit said to keep are untouched: §5.2 anonymous-identity rule, §7 double-count rules, §3.2 "financing silence is not commitment".

## Checks done on the draft

- All replacements (63 in batch 1, 19 in batch 2) hit exactly one anchor; before the old text was deleted, the script rebuilt the revised instruction from it byte-for-byte.
- Swept for leftover sentences contradicting the new rules ("observation limit", "leave Working date blank", "need not increase", "unobserved ending"); four fixed (C1–C4).
- Walked the six date rules by hand over the 14 Providence rows Opus left undated: all get a date; order holds (NDA cohorts land on the contact rows' date, not before them; LOIs 07/20 → G&W 07/21; Party D's undated stop lands on 08/02 behind Party E's reversion).
- **Not done:** no model has been run on the revised instruction; whether models follow the longer §8.1 and §10.2 is untested.
