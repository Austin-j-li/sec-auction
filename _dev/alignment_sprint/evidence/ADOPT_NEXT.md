# What to adopt next: v0 instruction against Alex's conventions (reconciled)

27 September 2026. Sources: four Opus 5.5 lane audits (`lane_A–D.md`, 64 items, 41 themes in `merged.md`), GPT-6 Astra (high) review (`astra_review.md`), and Claude's check of Astra's claims against the instruction, the voice notes and the filings. Nothing here is approved; each instruction change needs Austin's approval. No extraction was run.

## 1. Astra's claims, checked

### Right, and the lanes had missed or got wrong

| Claim | Check |
|---|---|
| F2 as drafted copies a price the bidder never restated | Confirmed. Bid reaffirmed is a Same-offer row (I l.243–245), which copies the earlier row. Providence Aug 4: counsel sent a revised draft; no price restated; on-site diligence ran to Aug 11 (filing p.30–31) |
| R2 would double-open: the later final letter fires E6(b) as a new round | Confirmed from E6 l.183, l.187. Needs a "letters implementing an admitted stage don't open another" clause |
| F7's blanket exemption would drop real closing conditions | Confirmed: Datalink Sep 29, Insight insisted accounting work and auditor consent be completed before closing (p.32) |
| R9: appending "(last late response …)" breaks the fixed Outcome values | Confirmed (D3 col 7 fixed list) |
| Datalink is the hardest round test | Confirmed: July 27 board kept five of nine; Aug 16 final letters to three; Sep 1 "the two other interested parties that remained in the process … were still considering whether they would submit" (p.29–30) |
| Synacor Dec 30, 2020 sought LOIs after exclusivity lapsed | Confirmed: "continue to seek non-binding letters of intent" (p.35–36). v0's trigger (d) already fires here |
| Kraton Party J: settled non-invitation rule gives a July 6 exit and July 19 re-entry | Confirmed mechanically. But the board on July 6 "noted that Party J had stated that it intended to submit a proposal … during the middle of July" (p.35): J was awaited, not left out |
| PetSmart: Alex's Oct 3 anchor rests on a premise the filing doesn't support | Confirmed: by Oct 3 the board heard of "communications with the 27 potentially interested parties … since the August 13 board meeting" (p.22–23). Contacts came before Oct 3, not after (contrary to V¶55's premise) |
| Mac-Gray Party A entered on June 21 (its Bid), not Aug 5 | Confirmed by E3 entry rule |
| Checker only accepts sequential Q ids | Confirmed: `QID_RE = Q[1-9]\d*` (check_lean.py:275) |
| Gap: bids in an inferred-final negotiation stage aren't automatically Formal, though V¶27 says only formal bids are considered then | Confirmed; belongs in the finality question |
| Merging market prices on Sort date conflicts with Sort date being an ordering aid | Correct |
| merged.md has 41 themes, not 37 | Correct (my error) |

### Where Astra is too cautious or over-engineers

| Theme | Astra | My call | Why |
|---|---|---|---|
| F2 | REJECT | ASK ALEX (Q5) | V¶30 is a general request ("Sometimes you see a bidder …"), not a Providence one-off. The settled-rule problem is only the copied price. A Bid row with blank price (as the settled commitment-only rows already do) records Alex's "becomes properly formal" event without inventing a price. The filing also contradicts Alex's "unconditional" (diligence ran to Aug 11), so ask |
| R2 | Tier 2 | Tier 1 | Two statements of Alex support it: V¶44 and the general V¶173 ("some bidders are dropped and some approached again … indicates the likely start of the next round"). V¶55 is not cited: its PetSmart premise fails. Its Datalink consequence (2 → 3 rounds) is what Q2 confirms |
| F4 | Tier 2 | Tier 1 | V¶19 names "extensive due diligence" as a heavy condition; the carve-out contradicts it. The two-week threshold is already v0 |
| R9 | Tier 2 | Tier 1 | V¶122 is explicit ("doesn't look like the target has done anything decisive") |
| R5 | Blocked | Tier 2 with Alex's wording | V¶71 and V¶173 give a general rule ("round one starts when the target's investment bank first starts contacting bidders"). Using that wording, not "the board's decision", avoids moving PetSmart to August |
| R7 late answers | New conditional rule plus a flag | Lane A13 as drafted | "Carries the round open when it arrives" gives the same Kraton answer, is simpler, and avoids out-of-order rows |
| O1 retirement | Category-specific, versioned retirement | A list of check categories Austin switches off when Alex agrees | Same effect, no machinery |
| O5 | Detailed normalization-input fields | Defer entirely | All whole-company bids in the nine deals are per share (lane B); nothing to record yet |
| O6 | Page plus locating phrase for every material classification | Lane D's "Also p. N" for date, count, identity | Notes are capped at 40 words |
| P8 | Add "use textual placement only where the narrative establishes order" | Drop that addition | Weakens v0's existing sound rule |
| Meredith | Schema change for a "descriptive container" process | No change | Process 1 plus "Whole-company bids: No" already covers it |
| R2 finality | "Do not backdate finality from a later letter" | No extra rule | Route 2 already ties Formality to answering the final solicitation |
| Astra tiering | Puts R1 in Tier 1 but says Q2 decides R1 | R1 Tier 1 | Austin's Kraton ruling needs it now |

## 2. What to adopt

### Tier 1: adopt now (general; no Alex answer needed)

**Rounds and deadlines**
1. **R1**: a common request for new offers to some but not all of the previous stage's eligible parties opens a round. Eligible includes non-submitters closed only by an inferred exit; excludes reported withdrawals and exclusions. Further requests inside a final solicitation continue it. (Kraton ruling; V¶82, V¶173) Consequence to approve knowingly: outside final rounds, an improvement request sent to the bidders but not to NDA signers who never bid now opens a round, so l.189's "asking the round's bidders to improve" continuation survives mainly inside final rounds. This is the largest behavioural change in Tier 1.
2. **R2**: a documented decision admitting named bidders to a next stage opens it at the decision, if the stage is carried out. Later access, letters and deadlines carrying out that stage do not open it again; a later further narrowing is tested under R1. Moves Mac-Gray to July 25 (V¶44); moves Kraton I and J's drops to July 20; makes Datalink 3 rounds (July 27, Aug 16), which Q2 confirms.
3. **R6**: rounds and the sale decision are for the whole company; partial-sale solicitations stay as Other-scope facts and in the Account. (V¶96, CI p.7)
4. **R7**: undated outreach reported as following a decision dates at the decision; an unreported opening is "by" the first offer, Date from at the previous round's last event; a late answer carries the round open when it arrives; Round opened precedes the exits it causes. (CI p.8)
5. **R9**: Enforced = the target selected or excluded bidders, opened the next stage or chose a bidder; review or feedback alone is Passed without action. Put the last late response date in How it ended. (V¶122–124)

**Bids and conditions**
6. **F4**: H2 covers a two-week-plus period for remaining non-confirmatory diligence even when it also covers exclusivity or negotiation; replace Example 4. (V¶19)
7. **F6**: an express lack of firm financing makes Financing Contingent whatever sources are named. (V¶47)
8. **F7** (Astra wording): routine bargaining over legal terms is not a Bid row; a reported change in price or commitment, or an explicit condition on proceeding, still is, wherever it appears; an adviser's prediction is not a bidder statement. Under this wording sTec June 20 (WDC "may not move forward" if sTec waived the standstill provisions) stays a Heavy H3 row; the lanes' broader exemption would have removed it but would also have dropped Datalink's accounting-before-closing demand. sTec June 20 becomes a Review item.
9. **F9**: a commitment letter alone does not make a bid Formal. (V¶47)
10. **F10** (Astra wording): a separately identified contingent extra payment is a CVR/earnout even with no stated payment date; keep the stated base price. (V¶84)
11. **F11** (Astra wording): a retrospective label alone doesn't turn interest or a market reference into a proposal. (V¶68)
12. **F12**: note a reported target preference between alternative structures. (V¶102)

**Participants and exits**
13. **P1**: a named party counts inside entry totals; it joins a later unnamed group only if exact identities and totals uniquely require it. (V¶21–24)
14. **P2**: subtract previously recorded parties from a cohort only where the filing or exact reconciliation places them in that aggregate. (V¶13, V¶121)
15. **P3**: an earlier inferred stage-opening exit beats a later reported withdrawal; the later report supplies the reason; Note "not invited" or "excluded". Reproduces sTec Company H.
16. **P4**: an agreement sent but not signed gets no row; signing is on or after sending; information sent under an agreement is an upper bound only if signing is shown to precede it; sending a memorandum never creates an NDA. (V¶12, CI p.6)
17. **P6, P8 (lane version), P9, P10 (Note, per CI p.7), P11, P7 (no compulsory tax rows).**

**Output**
18. **O3**: explicit Count/Who rule for signing and announcement rows; Count 1 on Merger agreement signed only when the signer is a whole-company bidder. Your requested clarification.
19. **O4**: record the signed acquirer's post-signing revisions, including returns to an earlier price; check the last price against the agreement summary and fairness opinion. (V¶104)
20. **O8**: define go-shop; a round only when solicitation under it is reported. (V¶113)
21. **O9**: Rounds counts reconcile to the ledger; explain supported differences.
22. **O1**: uncapped Review items (R1, R2 …) separate from the five Questions, plus a script-built review queue from the finished ledger; no seven-day cutoff; a Review item may point to a source event missing from the ledger; checker ID grammar extended in the same change. (V¶169–187)
23. **O6**: "Also p. N" when a date, count or identity rests on another page.

### Tier 2: adopt provisionally, confirm with Alex

24. **R5** in Alex's words: round 1 opens when the target or its banker first contacts prospective buyers; only where the target never does, at the first NDA or price negotiation. Penford's Aug 10 $18 becomes round 0. Confirm with Q1.
25. **R3**: keep (d) but add that carrying out an admitted stage is not asking again. Whether a lapse of exclusivity restarts bidding as a new round goes to Q2.

### Tier 3: blocked on Alex (eight questions)

1. **Round 1 start.** Is it the bank's first contact with buyers, the board decision, or (in bidder-approached deals) the first NDA? Note for PetSmart: the filing shows contacts before Oct 3, so the V¶55 anchor needs his confirmation. (R5, R7)
2. **What is a new stage?** Does an admitted stage run from the selection through the later offer letter? Does reopening after exclusivity lapses start a new round (Datalink Oct 1, Synacor Dec 30)? Should a party the target is still awaiting count as left out: Kraton J on July 6, and Datalink's two admitted parties that got no Aug 16 letter but "remained in the process" on Sep 1? The settled rule drops both. (R1–R3)
3. **Finality.** Can a final round be informal? Which step opens sTec's final round, May 16 or May 29? Are all bids in an inferred-final negotiation stage Formal (V¶27)? (R4, F3)
4. **Process gap.** Is roughly three months enough, and how is a gap straddling 90 days coded (sTec)? (R8)
5. **What makes an offer newly Formal?** Price with documents, documents alone, or an express price confirmation? For Providence Aug 4, the filing shows no restated price and diligence running to Aug 11. Would a blank-price formal row satisfy V¶30? What separates a valuation remark from a proposal (Penford Party A, Oct 4/13)? (F1, F2, F3, F11)
6. **Conditions.** Should "none reported" be kept apart from "light"? Does an exclusivity requirement count toward Heavy/Light, as V¶19 and V¶49 suggest ("record this conditionality in the same way we record … financing or due diligence"), or stay only in its own column as v0 has it (l.16, l.277)? None of the audits flagged this. (F5; F8 low priority)
7. **Initiation.** Is it the first mover, the trigger of the sale, or a recorded sequence? How should an activist who is only present differ from one who demanded the sale (sTec, Mac-Gray)? (P5)
8. **Real time.** Is a map check before the rows are written, plus a full review queue after the run, acceptable instead of live flags? (O2)

Also: V¶50 names Mac-Gray Parties B and C as dropped on Sep 24; the filing shows A and B.

### Tier 4: tooling or estimation

- Review-queue script, checker Q/R grammar, filing link from MANIFEST.csv, any cockpit pause step (O1, O7, O2).
- Price normalization and market prices at estimation; do not join market data on Sort date (O5, F8).

### Do not adopt

- F2 as drafted (it copies an unstated price).
- Astra's extras listed in section 1 as over-engineering.
