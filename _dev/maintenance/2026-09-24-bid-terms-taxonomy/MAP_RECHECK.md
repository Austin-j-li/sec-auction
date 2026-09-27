# Map re-check under the v1.14 rules (package M)

25 September 2026. Read-only analysis for Austin, as specified in [V114_SPEC.md](V114_SPEC.md) §6. Package A2 quotes the Decision 1 and E9 sections below.

**What was checked.** Six deals' process and round maps and deadline outcomes, against the v1.14 rules as §3 of the spec states them (E5 processes, E6 rounds, E9 deadlines), with decisions D7, D8, D10, D11 and D17 (§1) and the §8 calls. The deals are Kraton, Datalink and sTec for E6; Synacor for the reopening rule; Mac-Gray and PetSmart for E9 under D11.

**How.** One analyst re-checked each deal and a separate skeptic checked each analysis. I then checked every error and omission a skeptic reported against the filing and the working-copy snapshot myself, and corrected the section where the skeptic was right. Where I side with the analyst, the deal's review notes say why in one line.

**Sources, all read-only.**

| Deal | Current map read from | Filing (SHA-256 prefix; Background, printed pages) |
|---|---|---|
| Kraton | Working copy revision 4 (latest), saved 24 Sep 06:56:26 UTC by `austin`: the authorized revert after the independent audit. Base `opus55-medium` `20cc6986…` | DEFM14A 11/04/2021, `c0d2abbd…`, pp. 31–41 |
| Datalink | No working-copy revisions. Base `extraction/datalink.xlsx` (Opus 5.5 medium, v1.13.2, `f28c711c…`: 71 events, 4 rounds, 8 Questions), and the verified pilot revision `_dev/reviews/2026-09-21-datalink-pilot/revision/datalink_revised.xlsx` (`aa14e6fe…`: 68 events, 5 rounds; made on the earlier Opus 5 draft; implements F9) | DEFM14A 11/29/2016, `437e0e7a…`, pp. 27–35 (and p. 36) |
| sTec | Working copy revision 1 (only), 23 Sep 21:46:20 UTC, `austin`. Base `467f739d…` | DEFM14A 08/08/2013, `b29adcd8…`, pp. 23–35 |
| Synacor | Working copy revision 1 (only), 23 Sep 21:49:34 UTC, `austin`. Base `4d261075…` | SC TO-T 03/03/2021, Offer to Purchase §11, `2ea05cee…`, pp. 30–38 |
| Mac-Gray | Working copy revision 8 (latest), 23 Sep 21:41:08 UTC, `austin`. Base `40761509…` | DEFM14A 12/04/2013, `e6ea7bd0…`, pp. 27–41 |
| PetSmart | Working copy revision 2 (latest), 24 Sep 06:57:36 UTC, `austin`: the authorized revert. Base `04c7d952…` | DEFM14A 02/02/2015, `52c93afa…`, pp. 21–26 (Reasons pp. 26–29) |

Snapshots came from the `revisions` table of `_dev/cockpit/state/workspace.sqlite3`, opened only through a `mode=ro` URI. Workbooks and filings were read from copies in a scratch folder. The `deal_review` table is empty. No workbook, working copy, cockpit state or instruction was edited, and nothing runs from this file. Alex's hand coding and voice notes are cited only as the independent audit (`lesson/independent-audit-2026-09-23/`) reports them; `ref/` was not read.

**Notation.** [F] marks what the filing reports; [I] marks an inference. Row numbers are the current map's `#`. "§3" means spec §3. "The draft" is the 24 September draft instruction (`f9595d74…`). "The candidate" is A1's `SEC_Deal_Ledger_Extraction_Instruction_v1.14_candidate.md` as it stood on 25 September (`6e0a8c41…`), cited only where it bears on a question below.

**Timing (D24).** Nothing below changes data now. Each map applies when that deal's v1.14 run is reviewed, and package MIG carries it into the deal's register.

## Summary

| Deal | What would move | Conflict with a recorded ruling | Recommendation |
|---|---|---|---|
| Kraton | E6: the 07/20 admission and the later final bid procedures letter become one round. #49 changes from Round opened to Deadline set; #50–#74 move from round 3 to round 2; the round-3 Rounds line merges into round 2. E9: 09/15 becomes `Extended (late bid accepted)`. D7, as a separate step: #73 and #74 go and #75 becomes #73 | None. The 24 September revert (r4) is untouched, provided round 3's Bids received text moves into round 2 verbatim | Two rounds, for Austin and Alex in Decision 1. The three-round map is the alternative |
| Datalink | Round 1 moves to the January bilateral stage (#3–#12 into round 1; a new Round opened row on 01/29), as F9 already requires. Whether 07/27–08/16 is one round (four overall) or two (five overall) turns on count-once | The base conflicts with F9 on round 1. F9's recorded decision also says "keep five rounds", so count-once would revise an accepted map | Keep F9's round 1. The five-round map stands until Austin decides; count-once (four rounds) is a proposed change for Decision 1. 08/30 becomes `Extended (late bid accepted)` |
| sTec | Map A: no round 3. #50 becomes an Other material event and #51–#60 move to round 2. Round 1's outcome becomes `Extended (late bid accepted)` | No ruling; the register's provisional hold is lifted. Map A contradicts Alex's voice note ("not the final round") but matches his hand coding on the round count | Map A. Map B (current, round 3 reopened) and Map C (Alex's voice note) go to Decision 1 |
| Synacor | Round map unchanged (three processes, six rounds). #48 stays 10/27 but is anchored on the dated outreach. The changes come from D7 and D17: a new E Withdrew row on 12/14; #64 is no longer an exit; #62 and #46 go; four Company B rows | Working-copy Q8/#64 (E out on 01/04) and Q10/#62 are recommendations, not rulings; D7 overrides them | Main map. Alternatives: Alt-R2 (10/27 read as follow-up), Alt-B (Company B a sale), and a Company D (2020) alternative |
| Mac-Gray | Map unchanged. Outcomes become Extended (late bid accepted); Extended (late bid accepted); Enforced. Round 1's Who was in and #21's Count become bounds | Austin's 23 Sep comment agreed Q4 and Q5 as "Late bids accepted": a relabel on the same facts. The provisional 16-signer assumption yields to E3/E4 bounds | Keep the map. Record the D11 outcomes at rebase. Q7-A's prediction (09/18 Enforced) holds |
| PetSmart | 10/30 changes from Unclear to Enforced (reading A); round 2 is unchanged. Round 1's opening (08/13, 08/19 or October) stays an open question | The 24 Sep revert (r2) kept Unclear under v1.13.2's rule. D11 changes the label, not the facts, and r2 stays as it is | Enforced, with Unclear as the genuine alternative. Q7-A's prediction holds only on reading A |

## Kraton

### 1. Current map (working copy r4)

One process. Round 0 runs from September 2020 (#1, J.P. Morgan in the strategy meetings) to 05/20/2021 (#1–#7): the corporate development plan and talks on selling the CST segment (pp. 31–32).

| | Round 1 | Round 2 | Round 3 |
|---|---|---|---|
| Round opened | #8, 05/24/2021: the Board directs contact of 14 parties "and to commence the first round of the process" (p. 33) | #47, 07/20/2021: the Board instructs J.P. Morgan "to invite Party A, Party H, and Parent to the second round of the transaction process, and to provide these parties with additional financial and other due diligence materials" (p. 36) | #49, "after 08/11/2021", window 08/11–09/07, Sort date 08/11: the final bid procedures letter (p. 37) |
| Rows | #8–#46 | #47–#48 | #49–#74 (#75 is post) |
| Who was in | "15 units": 11 whole-company NDA signers (including K "chemical segment only" and the post-Reuters signer), plus C, D, E and G as segment-only parties admitted by #7 (Inferred = Y) | A, H, Parent; C, G and K "still being received, not admitted" | A, H, Parent; K and C "still being received" |
| Due dates | #19 Deadline set → #23 Deadline 06/29 → #32 Deadline revised 07/06 (07/19 for A, H, Parent and I) → #43 Deadline 07/19 | none stated | #58 Deadline 09/15 |
| Deadline outcome | Extended; Enforced | No deadline stated | Late bids accepted |
| Finality | Not final | Not final | Announced as final |
| Bids received | 5 whole-company bidders (A, H, Parent, I; J by 07/19); partial bids from K, C, G | 0 | Parent and A; also K's update (09/09) and A's polymer alternative (09/17) |
| How it ended | Selection on 07/20. I (#44) and J (#45) Dropped by target; #46 Did not submit, sorted at 07/20 | "Final bid procedures letter … opens round 3"; G withdrew 08/04 (#48) | Signing 09/27 (#71); H withdrew 08/20 (#52); A (#72), K (#73, inferred) and C (#74, inferred) Not selected at signing |

The 09/08 markup due date appears among ledger rows only in #49's Note. Q2 and Q7 discuss it. Rounds R3 How opened omits it, although the audit disposition KR-09/08-DEADLINE (`questions-disposition.md:137`) said to record it there. #8, #32, #47 and #49 are Needs decision; Q2 gives the merge as the alternative. No cockpit comment exists for Kraton.

### 2. Map under §3

**Round 1 is unchanged.** [F] On 05/24 the Board decided to contact 14 parties and "commence the first round" (p. 33); outreach ran "During the end of May and June 2021" (p. 34). [I] Outreach followed within about a week, so under "the earliest supported of" round 1 stays on 05/24. The CST talks stay in round 0: they concerned a segment only (D7), and no offers were requested (p. 32).

**07/06 stays inside round 1.** [F] On 07/06 the Board asked A, H, Parent and I for "updated indications of interest … by July 19 … that ascribed a greater value to Kraton before making any determination regarding which potential acquirers, if any, should be invited into the second round" (p. 35; the filing prints "2020"). Nobody was excluded; J's bid by 07/19 was reported with the others (p. 36). This is repeated bargaining with a new due date, which "stay[s] within the round" (§3 E6).

**07/20 to the letter: one round under count-once.**
- [F] The steps: admission and diligence materials on 07/20 (p. 36); "due diligence management meetings with Party A, Party H, and Parent" in the week of 08/09 (p. 36); on 08/11, a draft merger agreement "that would be provided to Party A, Party H, and Parent" (p. 36); then, "Following the Board meeting on August 11, 2021 … a final bid procedures letter" asking for markups by 09/08 and "final indications of interest by September 15, 2021" (p. 37).
- §3 E6: "Admission, common diligence and a later letter setting that stage's submission are steps within one round." That describes this sequence.
- Against it: §3 keeps the trigger "makes its first request for final, binding or best-and-final offers, even to unchanged bidders" (draft line 171), and the letter is such a request. §3 does not say which sentence governs when the letter setting a stage's submission is also the first final request. The candidate keeps both in one paragraph (line 181) without saying either. This is the question for Decision 1.
- [I] The deleted trigger ("opens a distinct information stage tied to new offers") bears on it only in part. The 07/20 selection asked for no offers, and the kept selection trigger reads "selects who advances and asks for updated offers"; the asking came in the letter. So the three-round map now depends on the first-final-request trigger overriding count-once. §3's own rule that another round "needs a distinct solicitation or selection" is a necessary condition and does not settle it.
- The filing's vocabulary is consistent with one round but does not decide it: media reports of 08/13 and 08/16 say acquirers "had been invited to the second round" (p. 37), the 05/24 plan was a "two-phase transaction process" (p. 33), and no third round is mentioned.

**No reopened round.** The post-Reuters invitations (p. 35) came while round 1 was open. The 08/30 request "to request an updated proposal from Party K regarding its possible acquisition of Kraton's chemical segment" (p. 38) went to a partial-only party (D7), so it is an event within the round.

**E9 under D11.**
- 06/29: **Extended**. A later due date (07/19) was set after the bids in hand were evaluated (confirmed in D27). J missed 06/29, said it would bid "during the middle of July" (p. 35) and bid by 07/19 (p. 36); under D10 it gets no exit. Room: if 07/06 is read as a new request rather than a later date for the 06/29 solicitation, rule 2 fits first (`Extended (late bid accepted)`), on the inference that the Board considered J's bid.
- 07/19: **Enforced**. All four responses were in "By July 19, 2021" (p. 36), and the Board acted on them on 07/20.
- 09/15: **Extended (late bid accepted)**. [F] Parent bid on 09/15; A bid on 09/17; on 09/18 "the Board reviewed the updated proposals submitted by Parent, Party A and Party K" (p. 39). No new date was set. The later exchanges (the request that Parent go to $46.50; A's bids of 09/21 and 09/24; pp. 39–40) are bargaining within the round. The 09/08 markup date stays a document milestone ("Only bid due dates are deadlines").

**Finality.** The merged round is Announced as final ("final bid procedures letter", "final indications", p. 37).

| | Round 1 | Round 2 (merged) |
|---|---|---|
| Round opened | #8, 05/24/2021 (p. 33) | #47, 07/20/2021 (p. 36) |
| Rows | #8–#46 | #47–#74 |
| Who was in | Keep apart those admitted to the 06/29 solicitation, those eligible but not admitted, and continuing partial alternatives (§3 D3, D7) | Admitted: A, Parent, H. Continuing partial alternatives: K (chemical; update requested 08/30), C (CST), G (CST, until 08/04), A's polymer alternative (09/17) |
| Due dates | 06/29 → 07/19 | 09/15 final indications (markups due 09/08 noted, not a deadline) |
| Deadline outcome | Extended; Enforced | Extended (late bid accepted) |
| Finality | Not final | Announced as final |
| How it ended | 3 advanced; I and J Dropped by target; J missed 06/29 and bid by 07/19 | Signing 09/27; H withdrew 08/20 before any submission; A bid two days after 09/15, was considered, and lost at signing |

### 3. Rows and Rounds lines that would move

**The merge (E6 and E9).** No row is added or deleted, so nothing is renumbered.

| Item | Now | Under §3 |
|---|---|---|
| #49 `bd4025d5` | Round opened, round 3 | **Deadline set**, round 2. When, window and Sort date unchanged (E8's decision-day rule applies: this is not a reopened round). The Note says the letter sets round 2's submission: markups by 09/08 (milestone), final indications by 09/15. Flags Q2 and Q7 stay |
| #50–#74 (25 rows) | Round 3 | Round 2. #75 stays post |
| #47 `af472b5b` Note | "No bid requested" | Add that the stage's submission was set later by the letter (#49) |
| Rounds R3 `916a2681` | Present | Deleted; content moves to R2 |
| Rounds R2 `fef7dfe8` | Offer-less, Not final | Opened stays 07/20. Seven cells rewritten: How opened (07/20 invitation and diligence; the letter after 08/11 setting 09/15; markups due 09/08, as KR-09/08-DEADLINE asked); Who was in; Due dates "09/15/2021 (final indications)"; Deadline outcome `Extended (late bid accepted)`; Finality Announced as final; Bids received (r4's R3 text, verbatim); How it ended |
| Rounds R1 How it ended | J's missed date absent | Add J's missed 06/29 and its bid by 07/19 (§3 D2). J's miss is already in #23's Note, its own row #31, #38's Note and Q4. [I] #31 passes the row test (a dated, reported message from a bidder about its submission, which explains its later bid), so it stays |
| Q2 `114dd867` | Recommends three rounds | Recommend two; keep three rounds, and Alex's 07/06 split, as alternatives |
| Q7 `b4abe638` | "Round 3 … Late bids accepted" | "Round 2 … Extended (late bid accepted)" |
| Q4 `4bb92c89` | Alternative "Late bids accepted" for 06/29 | Rename the alternative `Extended (late bid accepted)` |

**D7, a separate later step (not E6).** K "was only interested in acquiring Kraton's chemical segment" (p. 35), so it never entered the whole-company contest; the same holds for C, D, E and G. This step does renumber:
- #73 `92ec226c` (K) and #74 `c079f341` (C), both inferred Not selected at signing, are removed; #75 becomes #73. Q1's Rows affected (which lists #73 and #74) and any other `#` references are updated.
- #21 (E), #22 (D) and #48 (G) lose their exit labels. §3 E1 puts how talks ended in the Note of the party's last row; for D, E and G that row predates the reported withdrawal, so the readings are an Other material event row or a Note. This is for A1/R.
- #7 is no longer an entry (Inferred cleared).
- R1 Who was in stops counting K; the auction screen becomes 10–11 whole-company prospective acquirers, still Met.
- Q1 `22ad3b43` becomes D7's Question, naming C, D, E, G, K and A's polymer alternative.

**Dependent points for the v1.14 review (outside E6 and E9).**
- #29 (Count 1) and #30 (Count 2) are exact residuals resting on Q3's inferred membership of J and K. Under §3 E3/E4 and the rewritten E14 they become bounds; Q3 itself says 2–3 if J or K were outside.
- #44 (Party I, inferred Dropped by target) carries Exit reason "Would not improve earlier offer". Under F.3 an inferred exit's reason is Not stated unless the filing reports one; the filing reports I's refusal to raise (p. 36), not a reason for its exclusion. Q6 already offers Not stated.
- #66 and #69 (A's 09/21 and 09/24 bids) cite "markup #55" as their Formal basis; recheck under E11 and D9.

**Mechanical check.** The analyst rebuilt r4 and a merged variant in scratch and ran a copy of checker 1.6. r4 gives 0 errors and 20 warnings, matching the revert record. The merged variant gives 0 errors and 21 warnings (the extra is `ledger.note_length` on #49). The variant kept the legacy value and copied r4's R3 Who was in verbatim, so it approximates the proposed map rather than reproducing it.

### 4. Conflicts with recorded rulings

- **The 24 September revert (r4).** Reason text: "#55 Party A's 09/08 markup restored from Bid reaffirmed $45 Formal to Other material event (terms not reported; E10 finalize condition not met); #59 Note, Rounds R3 Bids received and Q8 answer updated to match, restoring A's polymer alternative." No conflict: the merge leaves #55, #59 and Q8 alone, and round 3's restored Bids received text must move verbatim into round 2. §3 supports the revert (E10 keeps the reaffirmation gate; E11 adds "a letter alone").
- **Datalink F9.** Datalink-specific. Astra's E6 lists "Kraton's admission/procedure-letter sequence" among the cases to reconcile before the rule is finalized (ASTRA_APPROVAL_SPEC.md:198). Whatever Austin decides should apply to Kraton, Datalink and Meredith alike.
- **No other ruling.** `RESEARCH_QUESTIONS.md` is silent; the round rows are Needs decision.
- **Alex's reported reading (not a ruling).** As the audit quotes his summary 2A and voice note V.3, he makes 07/06 a second informal round and 07/20 plus the letter one formal round. He agrees with §3 on the merge and differs on 07/06.

### 5. Recommendation

Adopt the two-round map as Kraton's v1.14 map and put it to Alex in Decision 1, with the three-round map as the alternative. The basis is §3 E6's count-once sentence, which describes the 07/20 → 08/11 sequence (pp. 36–37). The three-round map needs the first-final-request trigger to override that sentence, and it leaves a round with no request, due date or bid, against E6's definition of a round as a stage in which the target "asks a set of bidders for offers". The merge also matches Alex's reported reading of the later stage and needs no row insertion.

- **Alternative B, three rounds (current).** It holds if the first-final-request trigger governs. R3's Opened then stays on 08/11, the authorization day, under E8's decision-day rule; §3's outreach-date rule covers only reopened rounds.
- **Alternative C, Alex's 2A.** Round 2 from 07/06; round 3 from 07/20, formal. It needs D8 to change, since §3 keeps 07/06 within round 1.
- **Meredith** (12/21 admission → 01/12 final letter; its working copy splits them) has the same structure but is not in §6's list. The lead or Austin should schedule it with this decision.

### Review notes (skeptic)

Adopted: the renumbering caveat for the D7 step; J's miss already in #31, #38 and Q4, with #31's row-test disposition; round 0 from September 2020; seven cells, not six; the 09/08 date in Q2, Q7 and KR-09/08-DEADLINE; Astra's E6 as flagging Kraton for reconciliation, with spec §3 E6 as the basis; #29/#30 and #44 as dependent points; the merged variant as an approximation; "C29" is challenge C29 of the independent audit (`challenge/response-R3.md:15`), not systemic audit C. I also applied the Datalink skeptic's point on the deleted trigger (see Datalink).

## Datalink

### 1. Current map (base) and the verified pilot

One process. Talks with Party A ran "During February, March, April and May" (p. 27), and Party A was on the June list (p. 28), so there is no E5 break.

| Round | Opened (row) | How opened | Due dates → outcome | Finality | Bids received | How it ended |
|---|---|---|---|---|---|---|
| 0 | none | #1–#12: Party A's unsolicited $10.00 letter 01/19 (#1); price signal 01/28 (#2); board 01/29; RJ and NDA 02/04; mid-March request (#7); bids 03/29 and 04/12; 04/20 "at that time"; boards 05/25 and 06/01 (pp. 27–28) | — | — | — | — |
| 1 | #13, 06/06 | RJ outreach: 13 strategic from 06/06, 14 sponsors later in June (p. 28) | 07/18 and 07/21 (Deadline set #25; Deadlines #28, #32) → Enforced; Enforced | Not final | 10 (9 new IOIs plus A's standing 03/29 offer) | Five advanced 07/27; #29 (5) and #33 (8) inferred Did not submit; #34 (5) inferred Dropped by target |
| 2 | #35, 07/27 | Board keeps the five highest-priced IOIs; presentations, diligence, drafts (#36). "No offers requested yet" | none → No deadline stated | Not final | 0 | Carried into round 3 by the 08/16 letters |
| 3 | #37, 08/16 | Instruction letters "relating to their final proposals", due 5:00 p.m. ET 08/30 (p. 29) | 08/30 (#40) → Late bids accepted (Insight 08/31, #41) | Announced as final | 3 | Exclusivity with Insight 09/02 (#50); two unnamed did not submit (#47); B and C inferred Dropped at exclusivity (#51, #52); lapse 09/30 (#55) |
| 4 | #56, 10/01, Inferred = Y | RJ re-contacts B and C and sends revised drafts (p. 32) | none → No deadline stated | Inferred final | 1 (Insight) | B withdrew 10/24 (#64); C dropped at 10/26 exclusivity (#66); signing 11/06 (#70) |
| post | — | #71 announcement 11/07 | | | | |

Base round sizes: #1–#12 round 0; #13–#34 round 1; #35–#36 round 2; #37–#55 round 3; #56–#70 round 4; #71 post.

**Pilot (F9 implemented).** Round openings: pilot #3 on 01/29 (Inferred = Y, "bilateral stage with Party A"), #13 on 06/06, #30 on 07/27, #33 on 08/16, #53 on 10/01. Five rounds.

### 2. Map under §3

**January–May: round 1, as F9 already rules.** [F] On 01/29 the board "determined that our management should continue to pursue the opportunity with Party A" and had management approach Raymond James "in connection with the proposed process" (contacted 02/01; engaged 02/04). The NDA was signed 02/04, and "As we requested in mid-March 2016, on March 29, 2016, Party A provided a written proposal" (p. 27). [I] This is a sale stage the target organized, with a requested bid. §3 E6 opens round 1 at "the earliest supported sale stage the target organized, including substantive bilateral negotiation", and "later broad outreach does not push a genuine earlier requested-bid stage back to round 0".
- #1 (the unsolicited letter) stays in round 0.
- #2 (01/28): [F] "at the direction of Messrs. Ousley, Blackey and Meland", the CEO told Party A that $10.00 "was at the very low end of the range" the board would consider (p. 27). [I] It is a reply to the unsolicited letter before the board took it up, so it stays in round 0, but it is the one earlier candidate for "the start of substantive sale negotiations" and the Question should name it.
- Under "the earliest supported of", the question is whether 01/29 is supported, not which later date to prefer. F9 fixes 01/29, Inferred = Y. Only if 01/29 were not supported would the next candidate be 02/04 (the NDA that admitted Party A).

**The June round** is dated at the outreach (06/06). As round 2 it is not a round-1 launching-decision case. [I] Under Alex's reported bank-contact reading, where June is round 1, "the earliest supported of" would allow the 06/01 authorization, with outreach five days later (p. 28).

**07/27 and 08/16: the same question as Kraton.** [F] On 07/27 "Raymond James reviewed the initial indications of interest that had been received", and the board "directed our management and the Raymond James team to continue to pursue a transaction with the five parties that submitted the highest-priced initial indications of interest" (p. 29). Presentations, diligence and drafts followed; nothing was requested until the 08/16 "instruction letter relating to their final proposals", due 08/30 (p. 29). The two advancers with no reported letter still "remained in the process" and "were still considering" on 09/01 (pp. 30–31).
- **Reading A, count once (four rounds overall).** The letter set the stage's first submission and did not change the set, so admission, diligence and letter are one round.
- **Reading B, two rounds (five overall; the pilot and the standing F9 map).** The 08/16 letter is the first request for final offers (the kept trigger), and 07/27 is a distinct selection.
- [I] As for Kraton, the kept selection trigger needs a request for offers, which came only on 08/16, so Reading B depends on the first-final-request trigger overriding count-once.

**October: a new round under either reading.** [F] On 09/29 the board "directed management to allow Insight's exclusivity period to expire and to approach Party B and Party C" (p. 32); on 10/01 "Raymond James contacted Party B and Party C … each of whom expressed interest … in reengaging" (p. 32). A deliberate reopening after a suspension, dated at the outreach (10/01), not the 09/29 authorization; Inferred = Y; same process.

**E9 under D11.**
- 07/18 and 07/21: **Enforced; Enforced**. No later date and no overdue response is reported; the board acted on the IOIs in hand on 07/27 (p. 29).
- 08/30: **Extended (late bid accepted)**. "On August 30, 2016, each of Parties B and C submitted … and on August 31, 2016, Insight submitted its proposal" (p. 29); Insight's bid was considered (pp. 30–31). The later improvement requests are bargaining within the round. The two unnamed advancers get no exit then (D10) and close by the reported Did not submit (#47).
- Round 1 (January) and October: no date set → No deadline stated.

**Finality.** January and June: Not final. The final-proposal stage (either reading): Announced as final ("final proposals", p. 29; "best and final", p. 36). October: Inferred final (the move to definitive negotiation with Insight, pp. 33–34).

| Round | Reading A (count once) | Reading B (standing F9 map) |
|---|---|---|
| 0 | #1, #2 | #1, #2 |
| 1 | 01/29 bilateral stage, new Round opened row, Inferred = Y; No deadline stated; Not final; 1 bid (A, 03/29; 04/12 update) | Same |
| 2 | 06/06 outreach; Enforced; Enforced; Not final | Same |
| 3 | 07/27 selection through the 08/16 letter; 08/30 → Extended (late bid accepted); Announced as final; 3 bids | 07/27 selection only; No deadline stated; Not final; 0 bids |
| 4 | 10/01, Inferred = Y; No deadline stated; Inferred final; signing 11/06 | 08/16 letter; 08/30 → Extended (late bid accepted); Announced as final; 3 bids |
| 5 | — | 10/01, as Reading A's round 4 |

### 3. Rows and Rounds lines that would move (base → §3)

**Both readings.**
- Insert a Round opened row (process 1, round 1, 01/29/2016, Inferred = Y, Note naming the bilateral stage and F9) before #3. Every later `#` shifts by one.
- #3–#12 move from round 0 to round 1; #13–#34 from round 1 to round 2.
- #40's Note and the final-proposal round's Deadline outcome: `Late bids accepted` → `Extended (late bid accepted)`. Q6's value is renamed.
- Rounds: a new line 1 (opened 01/29; Party A; none stated; No deadline stated; Not final; 1 bid; carried into round 2). Old line 1 becomes line 2 ("carried over from round 1"; Bids received "9 new IOIs plus Party A's standing round-1 offer considered").
- Q1 is rewritten because the map changes and row references shift. (Its "about two months" wording is correct: Part F asks for every interval of about two months or more, v1.13.2 line 258, draft line 277.)

**Reading A only.** #35–#36 move from round 2 to round 3; #35's Note stops calling the stage one with no offers. #37 changes from Round opened to **Deadline set** and stays in round 3. #38–#71 keep their rounds. Old Rounds lines 2 and 3 merge (opened 07/27; due 08/30; Extended (late bid accepted); Announced as final; "5 admitted; letters reported to 3"; 3 bids). Line 4 unchanged.

**Reading B only.** #35–#36 move from round 2 to round 3; #37 stays Round opened; #37–#55 move from round 3 to 4 and #56–#70 from round 4 to 5. Rounds lines 1–5 as in the pilot.

**Dependent points for the v1.14 review (outside E6).**
- #29 and #33: exact counts 5 and 8 come from subtraction; E14's rewritten transition and pilot F1 give 5–7 and 8–9.
- #34 (inferred Dropped by target at 07/27) has Exit reason "Lower offer than rivals". Under F.3 it is Not stated unless the filing reports one; whether "the five parties that submitted the highest-priced initial indications" is a reported reason is for the reviewer. The pilot uses Not stated.
- #51/#52 (B and C Dropped at the 09/02 exclusivity) and #57/#58 (Re-entered). §3 E14 checks for a still-active offer or reserve status before inferring a departure. The evidence at the time: on 09/01 the board weighed "further negotiations with either Party B or Party C" (p. 31), and on 09/29 noted "we would be free to contact other interested parties, including Party B and Party C, after exclusivity expired" (p. 32). Later passages (B "withdrawing its earlier proposal" on 10/24; C reaffirming on 10/04) cannot be projected back to 09/02 (§3 B). Both readings stay open; the round boundary does not depend on them.

### 4. Conflicts with recorded rulings

- **Base vs F9 (round 1).** Catalog `datalink-f9`, recorded decision: "Retain January's bilateral stage as round 1 and June's broad outreach as round 2; keep five rounds. January 29 remains inferred." The base puts #3–#12 in round 0. §3 agrees with F9 on round 1.
- **Count-once vs F9's "five rounds".** The recorded decision says five rounds in so many words: "The five-round map remains" and "Keep the existing five-round map" (`ADJUDICATION.md`, lines 13 and 85); the verified revision "preserves the five-round map" (`VERIFICATION.md`, line 3). What Austin was asked was the round-1 choice ("sure i agree, keep the earlier run"), and the adjudication says "This decision resolves F9 only". Astra's E6 (line 198) reads in full: "reconcile Datalink's retained July/August split, Kraton's admission/procedure-letter sequence, and Alex's sTec finality reading. The earlier Datalink adjudication retains January bilateral negotiations; it does not separately settle whether the later admission and letter constitute two rounds. Do not silently revise an accepted map while claiming merely to clarify prose." So the 07/27–08/16 split was retained, not argued. Under D8 ("Austin's Datalink F9 ruling stands until he decides otherwise") the five-round map is the standing map, and Reading A would change it.
- **Alex's reported reading.** The questions-for-alex README summarizes his voice notes (summary 2A) as "round 1 starts when the target's bank first contacts bidders", which points to June and against F9. His reported Kraton answer (one round for an admission followed by a letter) is analogous to Reading A. Both are secondhand.
- **No conflict on dates.** Both outreach rounds are dated at the outreach (06/06; 10/01, not 09/29). None of the 24 September reverts concerns Datalink.

### 5. Recommendation

- **Round 1: keep F9.** Open it on 01/29, Inferred = Y, with #3–#12 in it. §3, D8 and F9 agree, on the filing's requested bid (p. 27).
- **07/27–08/30: the five-round map stands until Austin decides.** My reading of §3 favours Reading A (one round, four overall): nothing was requested between 07/27 and 08/16, the letter set that stage's first submission, and it did not change the set. Because this revises an accepted map, it needs Austin's explicit decision, and it should go to Alex in Decision 1 with Reading B beside it.
- **October** stays a round, dated 10/01, Inferred = Y.
- **08/30** becomes `Extended (late bid accepted)`; the June outcomes stay Enforced; Enforced.
- There is no working copy, so apply the decided map when reviewing Datalink's v1.14 run.

### Review notes (skeptic)

Adopted: F9's recorded "keep five rounds", so Reading B is the standing map and Reading A a proposed change; Q1's E5(b) wording is not a misstatement; "Raymond James reviewed" (not the board); the 01/28 candidate; the "earliest supported" framing; the evidence at the time for #51/#52; #34's exit reason; Astra line 198 in full. Partly sided with the analyst on the deleted trigger: the skeptic is right that the decisive contest is count-once against the kept first-final-request trigger, and the case now rests there; but the deletion is not irrelevant, because without it an offer-less selection stage matches no listed trigger by itself.

## sTec

### 1. Current map (working copy r1)

One process (Deal facts: 1). Round 0 holds #1–#12 (Company A, board decisions, Companies B, C and D, BofA); #61 is post.

| | Round 1 | Round 2 | Round 3 |
|---|---|---|---|
| Round opened | #13, 04/01/2013 (p. 27) | #39, "after 05/16/2013", window 05/16–05/28, Sort date 05/16 (p. 30) | #50, 05/31/2013, Inferred = Y, Date from = Date to = 05/31 (p. 31) |
| How opened | BofA began contacting acquirers after the 03/26 decision | Final-round process letters and a draft merger agreement to WDC and D after the 05/16 board meeting | "after WDC's withdrawal undid the round-2 selection", the target told D it could continue |
| Who was in | 6 NDA entrants (E, D, F, G, WDC, H). Letters to WDC and D (04/23, #22) and G (04/26, #26); none to H | WDC and D; H "still live until 05/23 but not admitted" | D, then WDC after re-entry (#52, 06/10) |
| Due dates | 05/03 (#22, #26 Deadline set; #30 Deadline) | 05/28 (#45) → 05/30 best and final (#46 Deadline revised; #47 Deadline) | none stated |
| Deadline outcome | Late bids accepted (D's written IOI 05/10, #34) | Extended; Enforced | No deadline stated |
| Finality | Not final | Announced as final | Announced as final |
| Bids | WDC #28; D #23, #34; H #37 | WDC #44, $9.15 (05/28), confirmed orally 05/30 in #47's Note; D none | WDC #53 $6.60–$7.10 (06/10); #54 range refused 06/11; WDC #55 $6.85 (06/14) |
| How it ended | WDC and D advanced (#38: D allowed to continue 05/15, round 1); F withdrew (#24); E dropped (#25); G withdrew (#29); H dropped 05/23 (#41, #42) | WDC selected 05/30 (#48); WDC withdrew 05/31 (#49) | D withdrew 06/05 (#51); WDC selected 06/15 (#56); signing 06/23 (#60) |

Rows #47–#49 are in round 2; #50–#60 in round 3. Q2 keeps the map "provisionally"; Q4, Q7, Q8 and Q9 cover the round-1 outcome, round-2 outcomes, WDC's withdrawal and re-entry, and #53's Formality. The register (`lesson/alex-questions.md`, STEC-MAY31-ROUND) says "Keep current map provisional".

### 2. Map under §3

**(a) 16 May is final.** [F] "at the direction of the board, BofA Merrill Lynch sent final round process letters and a draft merger agreement to WDC and Company D, requesting a response by May 28, 2013" (p. 30). On 29 May the board directed BofA "to request a "best and final" proposal from WDC and a "best and final" written proposal from Company D by May 30, 2013" (p. 30). Pointing the other way: the minutes speak of "sTec's request for non-binding proposals on May 28, 2013" (p. 30), and bidding continued to 14 June. §3 E6: "Finality describes the procedure the target announced or visibly put in place. It is separate from which bid came last, and from E11." The target announced "final round" letters and ran a final-round procedure (a draft agreement for markup to two selected bidders, then best and final), so round 2 is **Announced as final**. "Non-binding" describes the kind of bid asked for, and the later bids are "which bid came last". The 29 May request stays in round 2: it was not the first request for final offers.

**(b) Where round 2 starts (count-once).** The current map already counts the stage once. Only the date is open:
- A1: 05/15, D's admission ("Company D would be allowed to continue in the process with the understanding that Company D would need to meaningfully increase its proposal", p. 29), the stage's first reported step. #38 would move to round 2.
- A2: after 05/16 (current). WDC has no reported admission; the set {WDC, D} is visible only in the 05/16 meeting and its letters.
Nothing but #38's round and the Round opened row's place depends on it. It should follow the Kraton and Datalink decision.

**(c) 31 May: round 3 or round 2 continuing.** [F] On 05/30 the board "unanimously determined to move forward with WDC" (p. 31), with no exclusivity. On 05/31 WDC was "not prepared to move forward … at that time" and stopped diligence (p. 31). Then, undated, "At the request of our board of directors, representatives of BofA Merrill Lynch had a call with representatives of Company D on which they informed Company D's representatives that timing for sTec's process had been delayed, and that Company D had an opportunity to continue in the process" (p. 31); on 06/01 sTec posted D's requested diligence materials. From 06/01 to 06/10 BofA talked with WDC "at the direction of the board" (pp. 31–32). WDC's 06/10 and 06/14 bids were on "the transaction terms previously proposed on May 28, 2013" (p. 32). On 06/11 the board "would not respond to a proposal with a range" (p. 32).
- **Reading A: round 2 continues.** No distinct solicitation or selection, and no changed basis for bids: no new letter, due date or draft; the message to D is extra time for one bidder; WDC's bids reuse its 05/28 terms; 06/11 is a request to name a single price. No rival was told it was out, so no suspension is reported.
- **Reading B: round 3 (current).** After a final round, "the selection of a winner … is how that round ends"; when the selection collapsed, the board deliberately solicited the rival again ("reopening … after a suspension"). [I] The "suspension" would be the 05/30 selection itself, which lasted at most a day and was not communicated to D.
- Reading A needs no inferred step; Reading B needs both the suspension and the reopening to be inferred. §3 leaves room at the word "suspension".

**(d) Round 1: 03/26 or 04/01.** [F] On 03/26 the board decided "to confidentially approach strategic buyers" and directed that BofA be told of the approach (p. 27); on 04/01, "as directed by the special committee, BofA Merrill Lynch began contacting potential acquirers" (p. 27). Under "the earliest supported of" with line 173's route kept, round 1 opens on 03/26, six days before the outreach. The room is whether 04/01 was that decision's "direct execution" (the engagement letter, the list and the committee's own direction came between). This is a general consequence of the new wording (any deal whose outreach follows its decision within a week moves the same way), not something particular to sTec. 04/01 also matches Alex's summary 2A. The earlier approaches (Company A, 11/14/2012; Company B, 02/13; Company D, mid-March) are preliminary approaches that "alone do not open" round 1.

**(e) Deadlines (E9 under D11).**
- Round 1, 05/03: **Extended (late bid accepted)**. D said on 05/02 it "would need an additional week to confirm their verbal indication of interest in writing", submitted on 05/10, was given data-room access on 05/14 and was allowed to continue on 05/15 (p. 29). No new date is reported. H's 05/15 IOI was not a required response (no letter). Alternative, as Q4 already says: if D's 04/23 oral indication was its response, the 05/10 letter revises an on-time response, rule 2 does not fit, and the outcome is Enforced (the target's next step used the responses in hand), or Unclear.
- Round 2, 05/28: **Extended** (a new date, 05/30, set on 05/29 for both bidders, p. 30).
- Round 2, 05/30: **Enforced**. The board acted on the bids in hand on 05/30 (p. 31). Under Map A no later date is set, and WDC's 06/10 and 06/14 bids are not overdue required responses (WDC had answered on 05/30; D never submitted). D's position goes in the Notes.
- Round 3 (Map B only): No deadline stated.

**(f) Next to E6, not decided here.** One process under E5 (the cancellation sent to Company A is undated, p. 24), against Alex's two-process reading (voice item 1). Company D: no exit and no re-entry under every map (D10, §9.3). Company H: actor, timing and reason kept apart with bounds (§9.3); #42's exact 05/23 is an E14 question.

**The maps.**
- **Map A (recommended).** Round 1 opens 03/26 (or 04/01); due 05/03, Extended (late bid accepted); Not final. Round 2 opens at D's admission on 05/15 (or after 05/16); the final-round letters are its solicitation; due 05/28 → 05/30, Extended; Enforced; Announced as final; admitted WDC and D, H eligible but not admitted and out 05/23; the round runs through the 05/31 collapse, D's extra time and exit, WDC's return and bids, the 06/11 single-price demand, the 06/15 selection and signing 06/23. Bids received: 1 (WDC). No round 3.
- **Map B (current, restated under §3).** As Map A to 05/30, then an inferred round 3 (Inferred = Y) dated at the undated call to D: window 05/31–06/01, Sort date 06/01, after the authorization day (§3 E6). No due date. Finality: Announced as final only on the 06/11 "best offer" request, otherwise Inferred final (definitive negotiation from 06/15–16). WDC's own "best and final" (p. 32) cannot ground it.
- **Map C (Alex's voice note).** Round 2 (05/15 or 05/16) is Not final, and 05/28 is Enforced. The 29 May best-and-final request is then the first final request and opens round 3 on 05/29: Announced as final, due 05/30, Enforced, continuing to signing. Round 4 from 05/31 only if Reading B is also taken. Map C contradicts §3's finality rule (the letters were announced as "final round") and is admissible only if the researchers let "non-binding proposals" (p. 30) outweigh the target's label.

Under every map, entries, exits, live counts, prices, Formality and Conditions are unchanged. #44 is Formal through its markup. #53 and #55 are Formal through express reference to the 05/28 terms (D9). In Maps A and C, #53 is an unsolicited bid inside an announced-final round, so E11's final-solicitation route does not apply to it. #55 answers the board's 06/11 request "that if WDC desired to proceed, WDC must submit a proposal reflecting its best offer" (p. 32), so under Map B (and arguably Map A) the final-solicitation route may also apply to #55. Its label (Formal) is unchanged either way.

### 3. Rows and Rounds lines that would move

**Map A.**
1. Round 1 at 03/26: Round opened #13 moves to 03/26 and before #12 (the two swap numbers); #12 (Target sale decision) moves from round 0 to round 1; the 04/01 outreach stays in a Note. R1 Opened 04/01 → 03/26.
2. Round 2 at 05/15: a Round opened row is inserted at 05/15 before #38, renumbering every later row; #38 moves from round 1 to 2; #39 changes from Round opened to Deadline set ("after 05/16", due 05/28). R2 Opened 05/16 → 05/15.
3. Round 3 folded into round 2: #50 changes from Round opened to Other material event, round 3 → 2, Inferred Y → blank; When "after the 05/31/2013 board meeting", Date from 05/31, Date to 06/01, Sort date 05/31; flags Q2 and Q8 stay. #51–#60 move from round 3 to 2. The R3 line is deleted. R2 Bids received: "1: WDC ($9.15 05/28, confirmed as best 05/30; $6.60–$7.10 06/10; $6.85 06/14). Company D did not submit." R2 How it ended: "WDC selected 05/30, withdrew 05/31, re-entered 06/10; Company D missed 05/28 and 05/30, was invited to continue after the 05/31 board meeting (by 06/01) and withdrew 06/05; WDC selected at $6.85 06/15; signing 06/23." R2's Due dates, outcome and Finality are unchanged.
4. R1 Deadline outcome → `Extended (late bid accepted)`. Q4's recommended answer changes to match, and its "What changes" field keeps Enforced as the alternative.
5. Who was in (§3 D3): R1 separates the six entrants, the recipients of the 05/03 solicitation (WDC, D, G), and H (no letter; IOI received). R2: "2 admitted: WDC, D; Company H eligible to submit a revised indication but not admitted; out 05/23."
6. Questions: Q2 rewritten for two rounds; Q8's round-3 clause dropped; Q9 notes #53 as an unsolicited bid in a final round, Formal through express reference. Q7 unchanged.

**Map B.** Items 1, 2, 4, 5 and 6 as Map A. #50 stays Round opened (round 3, Inferred = Y) with When "after the 05/31/2013 board meeting", window 05/31–06/01, Sort date 06/01. R3 Opened 05/31 → 06/01. R3 Finality cites the 06/11 request or becomes Inferred final.

**Map C.** #46 changes from Deadline revised to Round opened (round 3, 05/29; it sets 05/30). #47–#49 move from round 2 to 3. #50 becomes an Other material event (Inferred blank, window 05/31–06/01); or, with Reading B as well, round 4's Round opened, with #51–#60 moving to round 4. Otherwise #51–#60 stay in round 3. The existing R3 line is rewritten (opened 05/29; WDC and D; due 05/30; Enforced; Announced as final; WDC's path as in Map A; signing 06/23). R2: Due dates 05/28, Enforced, Not final, Bids received "1: WDC $9.15", How it ended "best and final requested from WDC and D 05/29".

**Untouched under every map:** #1–#11, #14–#37 and #40–#45 (row content; numbers shift where a row is inserted). #46–#49 change only under Map C. Every price, Formality, Conditions, entry and exit cell, and Deal facts.

### 4. Conflicts with recorded rulings

- **Working copy r1 and its register.** "Keep current map provisional; retain withdrawal/re-entry facts either way" (STEC-MAY31-ROUND). A provisional hold, not a ruling; Map A would lift it after Austin decides (D8).
- **The 24 September questions README** (`questions-for-alex/README.md`), under "Removed because the voice notes answer them": "sTec 6: the 28 May round "is not the final round" and bidding continued", and "Adopting the removed answers implies ledger changes that have not been made: … sTec processes and rounds". Map A agrees with "bidding continued" (no round 3) and contradicts "not the final round". Spec §5 reopens the point ("sTec's finality on 16 May. Show both maps from package M"). The same README records "sTec 1: two processes" (against E5's one process) and summary 2A (against 03/26).
- **Alex's hand coding** (as `deals/stec.md` reports it, C36 and §6). Row 7166 codes a "Final Round Ext Ann" for Company D (05/16–05/28), row 7167 "Later extended until 6/10", row 7168 D's only drop on 06/05; no round 3. Map A agrees on the round count and on 16 May being final. It differs in two ways: Map A records 05/30 as Enforced where the hand coding extends to 06/10, although the filing reports no due date after 05/30 (pp. 31–32; the 06/11 request sets none); and under A1 Map A starts round 2 on 05/15, not 05/16. The 05/30 outcome difference belongs in Decision 1 and in the D11 question to Alex.
- **Audit recommendations (not rulings).** A1 "sTec continues round 2"; A15(c) "sTec's 05/16 letters are the final round". Both match Map A. `RESEARCH_QUESTIONS.md` item 2 is still pending.
- Datalink F9 does not apply. §9.3's Company D row holds under every map.

### 5. Recommendation

Adopt **Map A**: round 2 Announced as final, and no round 3. After 05/30 the filing reports no distinct solicitation or selection and no changed basis for bids, only extra time for one bidder, a withdrawal and return on the 05/28 terms, and a single-price demand, all of which §3 and line 171 keep in the round. Put Map A beside Map C in Decision 1, quoting Alex's voice note and hand coding side by side, and note the 05/30 outcome difference. **Map B** is the genuine alternative under §3's "reopening … after a suspension"; if Austin prefers it, date #50 to its window with Sort date 06/01. The round-1 date (03/26 or 04/01) is a general wording question for A1 and R across all deals. The round-2 date (05/15 or 05/16) follows the Kraton and Datalink decision. In every map, relabel round 1's outcome and give #50 its undated window. No data changes until Austin decides.

### Review notes (skeptic)

Adopted: Map C's bookkeeping (#47–#49 move; #50 needs a disposition; the R3 line is rewritten, not added); #46–#49 change under Map C; the hand-coding agreement narrowed, with the 05/30 outcome and start-date differences listed as conflicts; the undated call to D; Q4's counterfactual (Enforced is the right alternative under D11, as Q4 says); #55's possible final-solicitation route.

## Synacor

### 1. Current map (working copy r1)

Deal facts: "Number of processes: 3". Company B's merger-of-equals talks and Synacor's bid for Company D are in Earlier approaches, "not treated as sales"; B has no rows. Rows #9, #60, #62 and #68 are Needs decision.

| P | R | Round opened | Who was in | Deadline outcome | Finality | How it ended | Rows |
|---|---|---|---|---|---|---|---|
| 1 | 0 | none | A: NDA 01/10/2018, IOIs 02/06 and 04/25/2018 | — | — | — | #1–#5 |
| 1 | 1 | #6, "after 05/08/2018 (undated)", Sort 05/08: Liontree contacts about 12 parties | A; ~12 contacts, none entered | No deadline stated | Not final | A withdrew 06/20/2018 (#8); lapsed | #6–#8 |
| 2 | 0 | #9 Process restarted, inferred, March 2019 (C's NDA) | C; E (segment NDA 07/30/2019) | — | — | — | #9–#14 |
| 2 | 1 | #15, "after 08/25/2019 (undated)": Canaccord's outreach to 18 | C, E, F (segment IOI 09/15/2019) | No deadline stated | Not final | C withdrew October 2019 (#18); F's talks failed (undated); #19 closes E and F (Count 2) | #15–#18 |
| 3 | 0 | #19 Process restarted, inferred, 07/13/2020 | E | — | — | — | #19–#21 |
| 3 | 1 | #22, mid-July 2020: Canaccord outreach to 37 (#23), 14 NDAs (#24), 8 portal prospects (#25) | E; 12–14 other signers; CLP; G (segment); H contacted | 09/17/2020 (#26, #35): Enforced | Not final | Exclusivity with E 09/23; CLP #45, G #46 Dropped by target; #36 Did not submit (11–14) | #22–#42, #45–#46 |
| 3 | 2 | #43, 09/23/2020: E's LOI signed, exclusivity to 10/23 | E | No deadline stated | Inferred final | Exclusivity expired 10/23 (#47) | #43–#44, #47 |
| 3 | 3 | **#48, 10/27/2020**, quoting the committee's request that Canaccord "re-initiate outreach" | E; I (portal only); CLP (Re-entered #55); H solicited, not entered; G re-contacted | No deadline stated | Not final | CLP selected 01/06; **E withdrew 01/04/2021 (#64)**; I Did not submit (#62); H never bid | #48–#68 |
| 3 | 4 | #69, 01/06/2021: CLP's $2.00 LOI | CLP | No deadline stated | Inferred final | Signing 02/10/2021 (#76); #77 post | #69–#76 |

### 2. Map under §3

**What the filing reports at the contested points.** [F] Suspension, 09/23: "the Company and Canaccord Genuity also terminated other active discussions with other parties" (p. 34). Reopening, 10/27: the committee "requested that Canaccord Genuity re-initiate outreach to various parties which had previously expressed some interest"; "Also, on October 27, 2020, Mr. Bhise again reached out to Company H" (p. 34). Canaccord's outreach is undated. E's switch on 12/14 to "$2.00 per Share for 35% of the outstanding Shares" (p. 34), no longer interested in "100%" (p. 35). "Further outreach" to CLP, G and H on 12/18–12/21 (p. 35). On 12/30 the committee decided "to continue to seek non-binding letters of intent" from CLP, H and I, with no due date (pp. 35–36). On 01/04 E declined to return to 100% (p. 36).

**Processes (E5): three, on the main reading.**
- P1 → P2: (a) A withdrew, nothing outstanding; (b) 8.4–9.4 months from 06/20/2018 to March 2019 on reported contacts, with Liontree's undated outreach the caveat; (c) C's NDA. B's talks are not sale contacts in the main map (D17, below).
- P2 → P3: (a) under D7, E and F were partial-only in 2019; (b) 8.4–9.4 months from C's October 2019 exit, with F's end ("ultimately unable to agree on terms", p. 31) and the 18-party outreach undated (about 6 months remain even if the outreach ran to Canaccord's 01/15/2020 term end); (c) 07/13/2020.
- **Company D (2020) rests on an inference.** [F] Synacor's 07/01/2019 IOI was "to acquire" Company D, which let it expire (p. 31). The 2020 transaction is described only as "a non-binding letter of intent on January 1, 2020, proposing a transaction with all-stock consideration and a combined company ownership split", a merger agreement of 02/11/2020 and its termination on 06/29/2020 (p. 31); no acquiring side is named for 2020. [I] The working copy's "Company D deal was Synacor as buyer" (#19) infers the 2020 role from the 2019 bid. If the 2020 combination were read as a sale of Synacor, the P2 → P3 quiet period would be 06/29–07/13/2020, about two weeks, and E5(b) would fail. D17's rule (record the talks, flag the unclear scope and give the alternative map) may reach it. The main map can stay, but Q1 should give this alternative.
- 23–27 October 2020 and 14–18 December 2020 are not breaks: E's negotiation (then its partial offer) was live, and the gaps are days long.

**Rounds (E6 under D8): six, with every Round opened date unchanged.**
- **P3 R3 is the rule's own case**: a reported suspension (09/23), then a deliberate reopening. It is dated at the outreach, never at the authorization. [I] The CEO's contact with H on 10/27 is the first dated act of the reopened solicitation: made the day of the decision, to a party the 09/23 termination had covered, while E's talks continued. So R3 stays opened 10/27/2020, anchored on that outreach, and E8's decision-day Sort rule is not needed.
- The 12/18–12/21 "further outreach" follows no new suspension, and the 12/30 decision to "continue to seek" LOIs with no due date sets the reopened stage's submission: both are steps within R3. D8 adopted the 24 September option A ("Synacor 27 October 2020"), not B (30 December) or C (two rounds). E's 12/14 switch is a bidder act and opens nothing.
- R2 (exclusive negotiation with E) and R4 (CLP) are distinct selections. The 09/17 request for E's "best offer on purchase price" (p. 33) went to one bidder, with no final procedure: bargaining within R1.
- #6 and #15 keep line 173's route (round 1; decision-day Sort dates allowed).

**Deadlines (E9 under D11).** 09/17/2020: **Enforced**, unchanged. No later date; no overdue required response considered (E's 09/18 letter answered the 09/17 best-offer request; H never submitted); the committee acted on the bids in hand on 09/21 and invited improvements with no new date. Every other round: No deadline stated (E's "would expire by January 4, 2021", p. 35, is a bidder's expiry, not a due date). Finality unchanged.

**D7.** E leaves the whole-company contest at the 12/14 switch (§9.3): a new Withdrew row, Exit reason Not stated, Note that talks continued on a partial basis. #64 is no longer an exit and E gets no Re-entered. F (2019), E (2019 segment NDA), G (software only) and I (portal only) were partial from the start: no exit rows. **Live whole-company units in R3 depend on Q5.** If H is contact-only (the working copy's provisional answer): E alone from 10/27, none from 12/14, CLP from 12/18–12/21, so CLP's $1.88 and $2.00 bids met no live whole-company rival. If H entered, through the R1 NDA cohort or the 12/30 invitation, H is live beside CLP from 12/18–12/21 (or 12/30) to the 01/06 selection and the R3 count is 2. The 14–18 December gap is not a break either way (E's partial offer was under evaluation on 12/17 and H "remained interested").

**D17, Company B.** [F] "In October 2018, the Company and … ("Company B") entered into a mutual non-disclosure agreement to explore a potential business combination. Later that month, the Company delivered a non-binding indication of interest letter to Company B proposing a "merger of equals" which, following further discussion and negotiation, was executed by the parties in December 2018"; talks ended March 2019 (p. 30). Four dated Other material event rows, outside the counts; the alternative map goes in the Question.

### 3. Rows and Rounds lines that would move (main map; r1 numbers)

- **#48** (Round opened, P3 R3): date stays 10/27/2020; Quote, Note and Rounds How opened move from the committee's request to the outreach (the CEO's 10/27 contact with H, plus Canaccord's undated re-initiated outreach). Inferred stays blank. No row changes round.
- Unchanged: #6, #15, #22, #43, #69; #26 and #35; every Deadline outcome and Finality cell; three processes.
- **D7:** a new Company E Withdrew row, 12/14/2020, P3 R3, next to #54 (no rule fixes before or after). #64 → Other material event, Exit reason cleared. #54 and #59 stay Other-scope bids, with Price low and high blanked (D18) and "$2.00 per share for 35%" in the Note. Q8's answer flips to 12/14. #62 (I) is removed and I's end goes in #58's Note; Q10 is withdrawn. #46 (G) is no longer an exit (fold into #44/#45's Note or make it an Other material event; G's end goes in #57's Note). #19's Count 2 becomes 0 whole-company closures. The Notes of #11, #17, #30 and #51 drop whole-company "enters" wording. A new D7 Question names G, E after 12/14 and I.
- **D17:** four new Other material event rows for B between #8 and #9 (p. 30), outside the counts; every later `#` shifts by four. The spec does not say which Process and Round a non-sale row in a gap between processes carries; the conservative choice is the then-current P1 R1. #9's Note and Deal facts Earlier approaches point to the new rows; Company D stays in Deal facts.
- **Rounds.** P2 R1: Who was in names E and F as partial-only; Bids received "0 whole-company; partial-only: F (09/15/2019)". P3 R1: G partial-only; Bids received "2 whole-company (E, CLP); partial-only: G". P3 R3: How opened is the outreach; Who was in: E (whole-company until 12/14, then a partial alternative to 01/04), CLP (re-entered), I (partial-only), H (solicited, not admitted, subject to Q5); Bids received "1 whole-company: CLP ($1.88 01/04; $2.00 by 01/06); partial-only: E (12/14, 12/29), I (12/08, 12/29)". P1 R1, P3 R2 and P3 R4 unchanged.
- **Deal facts, Auction screen:** P2 "Not met: 1 whole-company party (C); partial-only E, F"; P3's upper bound drops I. The 2020 outreach was for "the Company and/or its software and services business" (p. 32), so the scope of the 14 signers needs a reviewer's look.
- **Questions:** Q1 restated with the D17 alternative map, the Company D (2020) alternative, R3 dated at the outreach and Alt-R2; the 12/30 option-B alternative dropped. Q5 stays open.
- **Outside this re-check:** D14 recodes the same upgrade forces (§9.3, "an exclusivity period is not a diligence period"): #37 (Heavy on exclusivity "for diligence"), and #66 and #72 (Heavy partly on CLP's "30-day period of exclusivity"). Listed for the v1.14 review.

Net: 77 rows become 80 or 81 before renumbering; six Rounds lines and three processes stay.

**Alternative maps.**
- **Alt-R2: the CEO's 10/27 contact is routine follow-up.** The reopened outreach is Canaccord's, undated: #48 becomes "after 10/27/2020 (undated)", Date from 10/27, Date to 12/21/2020, Sort date **11/23/2020** (the midpoint, rounding earlier). #49 (H, 10/27), #50 (H, 11/02) and #51 (I's NDA, 11/19) move to R2. Not recommended: it treats a dated, same-day, target-initiated solicitation of a suspended rival as follow-up.
- **Alt-R3 (weak): the reopening is the 12/18–12/21 outreach.** #48 becomes an Other material event in R2; a new Round opened row (Sort 12/19) goes before #55. It conflicts with "further outreach" (p. 35), the dated 10/27 contact and D8's adoption of option A.
- **Alt-B (D17): B's talks are a sale.** P2 begins October 2018 (#9 moves). B gets an NDA signed row and a Withdrew row (March 2019); the proposal was Synacor's, and B's act in December 2018 was executing it, so any bid row must not credit B with a bid it did not make. P2 R1 would open at the bilateral negotiation and Canaccord's outreach would open P2 R2 (seven rounds); the spec does not settle this. P1 and P2 stay apart on reported dates (3.4–4.4 months), unless Liontree's undated outreach ran close enough to October 2018 to fail E5(b).
- **Company D (2020) as a sale of Synacor** (above): P2 and P3 separated by about two weeks; the process map would need rework. For the Question, not recommended as the main map.
- **Alt-D: P1's round 1 at A's "discussion between the parties"** (02/06–04/25/2018). Not recommended: the filing shows no target-organized stage before Liontree.

### 4. Conflicts with recorded rulings

- **The map: none.** r1's reason ("preserving the three-process/six-round map") holds; R3's 10/27 matches the 24 September Q3 option A, which D8 adopted; Alex's voice note (as the audit reports it, `deals/synacor.md` §6 item 1b) that the 23–27 October lapse is not a new process holds; the revert does not touch Synacor.
- **#48's anchor:** wording only. §9.3 requires the "Date of the outreach itself, not the board authorization"; the dates coincide.
- **Q8 and #64 (Reviewed) vs D7.** "Use 01/04/2021 (Withdrew, reason Not stated): E stayed in negotiation with a live, if partial, proposal." A working-copy recommendation, not an Austin ruling; D7 (provisional) and §9.3 put the exit at 12/14.
- **Q10 and #62 (Needs decision) vs D7/D27.** Mooted: partial-only parties get no exit rows.
- **Q5 (H's admission) and Alex's coding of H.** r1 keeps H outside "provisionally" and asks Alex; the audit reports Alex codes an H NDA in about 08/2020 and a drop on 11/02/2020 (`deals/synacor.md`). Open, and it decides R3's live whole-company count.
- **Company B vs D17.** r1 has no B rows; D17 requires them. r1's Q1 on the process effect agrees with D17's alternative map.
- **Alex's other hand coding** (as reported): E's exit at "12/04" agrees with D7 in substance (the filing date is 12/14); his B entry and exit are D17's alternative map; his I exit at signing differs from D7.

### 5. Recommendation

Adopt the main map: three processes and six rounds, every Round opened date unchanged; R3 opened on 10/27/2020 and anchored on the dated outreach, with the committee's request in the Note; the December contacts and the 12/30 LOI request as steps within R3; 09/17 Enforced. The data changes come from D7 (E out on 12/14; no exits for G and I) and D17 (B's rows), not from E6. Keep Q5 open: R3's live count depends on it. The genuine alternative for Austin is Alt-R2. Q1 should also carry the Alt-B and Company D alternatives.

### Review notes (skeptic)

Adopted: Alt-R2's Sort date 11/23 (not 11/24); Synacor's 2020 buyer role labelled as an inference, with the two-week alternative; the R3 live counts made conditional on Q5, with Alex's H coding added; D14 rows listed as outside scope; F's undated end in the P2 → P3 test; B's execution of Synacor's proposal in Alt-B. The Company D point is extended by me: [I] D17 may reach the 2020 all-stock combination.

## Mac-Gray

### 1. Current map (working copy r8)

One process. Round 0 holds #1–#8 (BofA's buy-side engagement 10/23/2012; the target's call to Party A 04/08/2013; Party A's unsolicited $17–$19 proposal 06/21; the Special Committee's sale decision 06/24; pp. 27–31).

| Round | Opened | Who was in | Due date (rows) | Outcome | Finality | Bids | How it ended |
|---|---|---|---|---|---|---|---|
| 1 | #9, 06/24/2013 (p. 32) | "Assuming Q3: 19 NDA-admitted bidders by July 23"; Party A's round-0 proposal under consideration, NDA 08/05 | 07/23 (#9; #19) | Late bids accepted (Q4) | Not final | 3: CSC/Pamplona, B, C | Four advanced; "Sixteen unnamed financial non-submitters are inferred" (#21, Count 16) |
| 2 | #24, 07/25 (p. 34) | 4: A (from 08/05, #26), CSC/Pamplona, B, C | 09/09 (#29 on 08/27; #30) | Late bids accepted (Q5) | Not final | 4 | "four advanced …; none out" |
| 3 | #36, 09/11 (p. 36) | 4 | 09/18 (#36; #37) | Enforced (Q7) | Announced as final | 3 distinct | C did not submit (#41); exclusivity with CSC/Pamplona at $21.25 on 09/24 (#46); A and B inferred Dropped by 09/24 (#47, #48); signing 10/14 (#57) |

[F] At each due date:
- 07/23: signers "were instructed to submit by July 23, 2013" (p. 32). CSC/Pamplona bid on 07/23; Party B submitted "a preliminary indication of interest" on 07/24, and Party C bid orally the same day (p. 33). On 07/25 BofA reviewed the indications "received from Party B, Party C and CSC/Pamplona as well as the Party A June 21 proposal" (p. 33), and the Committee admitted all four to the next stage (p. 34). No new date.
- 09/09: the 08/27 letter asked for revised proposals "no later than September 9, 2013 if such bidders wished to proceed further" (p. 35). CSC/Pamplona and B bid on 09/09, A and C on 09/10; all four reviewed 09/11 (p. 35).
- 09/18: CSC/Pamplona, A and B responded on 09/18; C "did not submit a revised indication of interest or reiterate its prior indication" (p. 36). On 09/19 the Committee discussed "the three revised proposals" and authorized exclusivity at $21.25 (p. 37), which CSC/Pamplona accepted on 09/21 "as a last and best offer" (p. 37).
- The 10/12 exclusivity expiry (extended to 10/15) is not a bid due date.

### 2. Map under §3

**E5: one process.** The 04/08 → 06/21 gap is under three months, and Party A was kept in view (reported to the Board on 05/09, p. 27; named for approach on 06/24, p. 31).

**E6: rounds unchanged.**
- Round 1 stays 06/24 (#9). The 04/08 call was "to discuss generally a possible business combination" (p. 27) and the 06/21 proposal was "unsolicited" (p. 30): preliminary approaches, not substantive bilateral negotiation. BofA had reached Party A and Pamplona by 06/28 (p. 32), so the launching decision is the earliest supported date.
- Round 2 stays 07/25 (#24): the Committee selected four bidders and decided "to then request that each of these parties submit a revised indication of interest" (p. 34). The admission, the 08/06–08/27 diligence and the 08/27 letter are steps within one round (count-once). Q1's "Why" rests on the deleted wording ("a staged information stage tied to revised offers") and should be regrounded on the selection plus the request for revised offers.
- Round 3 stays 09/11 (#36): the first request for "final indications of interest by September 18, 2013", with the exclusivity carrot (p. 36). Announced as final.
- No round is unannounced or reopened, so no Round opened row gets Inferred = Y and the Sort-date carve-out does not arise.

**D7 and D17 do not apply.** Mac-Gray has no partial-company bidder and no merger-of-equals episode; Party B's package terms are consideration (D4), not a change of scope.

**E9 under D11.**

| Due date | Rule 1, Extended? | Rule 2, Extended (late bid accepted)? | Rule 3, Enforced? | v1.14 outcome |
|---|---|---|---|---|
| 07/23 | No later date was set for this solicitation; 09/09 belongs to round 2's own request | **Yes.** B and C were signers "instructed to submit by July 23" (p. 32), responded 07/24, were reviewed 07/25 (p. 33) and admitted (p. 34) | — | **Extended (late bid accepted)** |
| 09/09 | No (only if the 09/11 request were read as a later date for the same solicitation; alternative (a)) | **Yes.** A and C sent their revised responses on 09/10, reviewed 09/11 (p. 35). D11 covers "revised" responses | — | **Extended (late bid accepted)** |
| 09/18 | No new date | No overdue response: all three responders were on time; C never responded | **Yes.** The Committee acted on "the three revised proposals" on 09/19 (p. 37); the $21.25 improvement was invited afterwards with no new date | **Enforced** |

Party A's 06/21 proposal, reviewed on 07/25, does not count under rule 2: Party A had no NDA and had not been given the 07/23 instruction. The v1.13.2 alternative in Q4 and Q5 ("Enforced if one-day lateness is immaterial") is closed: E9 takes the first rule that fits.

**D10 and D2.** B and C missed 07/23, and A and C missed 09/09; all continued, so none gets an exit or re-entry (none has). Each miss belongs in the Deadline row's Note (#19 and #30 already record it) and in the Rounds line's How it ended (missing now). C's 09/18 non-submission ends its participation: #41 Did not submit stands, Exit reason Not stated.

**The NDA interval.** The 20 NDAs were signed "over the next two months" (p. 32); Party A's on 08/05 (p. 34). Under §3 E3/E4 and §5 ("The ledger always keeps the bounds"), round 1's Who was in cannot state 19 as an exact number admitted by 07/23. Only three named signers are dated before 07/23: B (06/28), C (06/30), CSC/Pamplona (07/11). The 07/23 outcome does not depend on this.

### 3. Rows and Rounds lines that would move (at the D24 rebase; the v1.13.2 working copy cannot hold the new value)

- **Rounds:** R1 and R2 Deadline outcome `Late bids accepted` → `Extended (late bid accepted)`; R3 Enforced unchanged. R1 Who was in becomes a bound: "Party B (06/28), Party C (06/30), CSC/Pamplona (07/11), plus 0–16 of the 16 unnamed financial signers, whose signing dates are not reported (p. 32). Party A: still being received, not admitted (06/21 proposal; NDA 08/05)." R1 How it ended adds "Party B and Party C missed 07/23 and bid 07/24; considered 07/25" and replaces the 16 inferred non-submitters with bounded closures (below). R2 How it ended adds "Party A and Party C missed 09/09 and bid 09/10; considered 09/11".
- **#21 and the 16 unnamed signers.** Count 16 becomes a bound. Under v1.14 the labels follow E14's transitions (F.3); they are not Alex's question. Signers eligible at 07/23 who did not bid close as Did not submit by 07/23 (bound 0–16). Any who signed after 07/23 and by 07/25 were live when the Committee named the complete advancing set without them (p. 34), so they close as Dropped by target by 07/25 (the draft's transition at line 265). Any who signed after 07/25 fall under a later transition. The bounds together account for all 16, with no one closed twice. Alex's Decision 3 is how estimation uses the ranges (D22). #18's 16 signers stays exact.
- **No event row moves round or changes type** under E5, E6 or E9. #19 and #30 Notes already record due date, responders, lateness and review date.
- **Questions.** Q4 and Q5: value renamed and the Enforced alternative closed; retire or rewrite. Q7: answer unchanged, the "Passed without action" alternative excluded by rule 3's text; retire or rewrite. Q1: answer unchanged; regrounded as above; its 08/27 alternative should note that count-once favours 07/25; its "Party A kept in view (pp. 28, 31)" should read pp. 27, 31. Q3 becomes the ranges question. Q8: the still-open link fix recorded in the revert file (its Rows affected omit #44, #53 and #54; its "What changes" still proposes a Kirkland 10/07 reaffirmation that R01 superseded).

### 4. Conflicts with recorded rulings

- **Austin's whole-deal comment, 23 Sep 20:09:28 UTC** (thread `682f1b3f…`): "Q1, Q2, Q4, Q5, Q7, Q8 and Q9: agree, and all match Alex's hand data." For Q4 and Q5 only the label changes, on the same facts; the consequence is that two one-day-late deadlines now read as extensions (soft deadlines) under any grouping of the Extended values. Q7 and Q1 do not conflict.
- **The same comment ("#21 keeps 16 as a stated assumption (Q3, to confirm with Alex)") and r8's reason** ("Keep the 16-person total and provisional exit coding; mark #18/#21 Needs decision"). These yield to §3 E3/E4, §9.3's "Mac-Gray NDA interval" row and §5's bounds. A provisional working choice, not a final ruling. Bearing on Q3: the audit notes p. 32 "ties the package and the 07/23 instruction to NDA signers", which partly supports eligibility (lessons-disposition MG-O4), and that Alex's hand coding has the 16 signing about 07/15 and dropping on 07/25 (`deals/mac-gray.md`, line 110; the "07/23 non-submission against a 07/25 exclusion" choice at line 150).
- **R01** (Austin, 22 September; `RESEARCH_DECISION.md`, line 3): commitment changes "are same-price Bids carrying the standing price". The decision implies no new round and no exit, which agrees with keeping #44, #53 and #54 in round 3 and 09/18 Enforced. (Line 7 is the pre-decision analysis; the audit's MG-B3 warns not to follow it.)
- **Independent audit** (`deals/mac-gray.md` §5): found the 07/24 late bids accepted, round 2 at 07/25, the 08/27 letter for 09/09, the 09/10 late bids and round 3 at 09/11 correct. Its item "Restore the phrase" ("still being received, not admitted") is adopted by §3 D3.
- The 24 September revert did not touch Mac-Gray.

### 5. Recommendation

Keep the process and the three rounds (06/24, 07/25, 09/11) and their Finality. At rebase, record the outcomes as **Extended (late bid accepted); Extended (late bid accepted); Enforced**, on reported dates for every response and review (pp. 32–37). Apply the Rounds text and #21 changes above. Q4, Q5 and Q7 can be retired under D12 (the rule now decides each), or merged into one Question while D11 is provisional. Do not edit the v1.13.2 working copy. Weaker alternatives: (a) merging rounds 2 and 3 (09/09 would then be Extended); (b) round 2 at the 08/27 letter (no outcome changes); (c) round 1 at the 04/08 call.

### Review notes (skeptic)

Adopted: #21's labels follow E14's transitions, with bounded closures and Alex's question limited to estimation (I adopted the principle and the transitions; the exact row split is the reviewer's); R01 cited at its decision (line 3), not line 7; Q1's regrounding and page fix; D7/D17 stated as not applicable; MG-O4 and Alex's 07/25 drop added; the Q8 link fix; Party B's 07/24 indication is not described as written.

## PetSmart

### 1. Current map (working copy r2)

47 rows, 2 Rounds lines, 9 Questions. Evaluation material also includes `inventory/petsmart.csv` and `challenge/response-R2.md` (R2 accepted C14's October reading of round 1).

- **One process.** The spring 2014 Industry Participant talks, where PetSmart was the potential buyer (p. 21), are in Deal facts.
- **Round 0:** #1–#8, including Industry Participant's 08/07 Bidder interest (#7) and the 08/13 Target sale decision (#8).
- **Round 1:** Round opened #9, 08/19/2014, Inferred = Y, Needs decision (quote from p. 22: "which would ensure that interested parties not contacted would become aware of the process and could contact J.P. Morgan on their own initiative"); #10 Sale process announced 08/19; Industry Participant refused admission 08/27 (#11); 15 NDAs in the first week of October (#14); Deadline set #15 and Deadline #17, 10/30, outcome **Unclear**; six IOIs on 10/30 (#18–#22); #24 Bidder 2's revision from $78 to $81–$84, window 10/30–11/02; Not final; four advanced on 11/03, #25 two Dropped by target, #23 Did not submit (at most 9).
- **Round 2:** #26, 11/03: "the four bidders that had indicated a price or range at or above $80.00 per share to proceed to the final round" (p. 24). Due dates 12/05 (superseded, #28) → 12/10 (#30, #33, Extended) → 12/12 (#37, #39, Enforced). Announced as final. Board approval 12/13 (#43); signing 12/14 (#45); #46 Bidder 2 Not selected at signing; #36 Bidder 3 Did not submit 12/10. Post #47.
- **Questions:** Q1 the map (alternatives: round 1 in October; round 3 at 12/10); Q2 "Unclear, Late bids accepted or Enforced?", recommended Unclear; Q3 the round-2 chain.

### 2. Map under §3

**E5: unchanged.** One process.

**E6, round 2: unchanged and better supported.** The 11/03 selection opens it. The November diligence, the form merger agreement circulated "with instructions that the bidders submit any proposed comments … together with their final bids" (p. 24) and the 12/04–12/05 re-dating are steps within it (count-once). The 12/10 request to improve is repeated bargaining: the same two written bidders, the same documents, no new selection and no changed basis. Bidder 3 had told J.P. Morgan its valuation "would not be above the current stock price", and "J.P. Morgan communicated to Bidder 3 that it was unlikely to be competitive and accordingly Bidder 3 did not submit a written offer" (p. 25). So Q1's alternative (ii), a round 3 at 12/10, loses support. Finality stays Announced as final ("the final round of the sale process", p. 24).

**E6, round 1: still open, and §3 widens it.** On 08/13 the board decided on a public announcement so that "interested parties not contacted would become aware of the process and could contact J.P. Morgan on their own initiative" (p. 22); the press release followed on 08/19 (p. 23). No dated outbound wave is reported: J.P. Morgan "was contacted by 27 potential participants" (p. 23). §3 does not say whether an announcement inviting inbound contact is an outreach wave.

| Reading | Round 1 opens | Basis |
|---|---|---|
| (a) The announcement is outreach | 08/13 | Under "the earliest supported of", the launching decision (six days before) comes first. New under §3 |
| (b) Current | 08/19 | Harder to reach under §3 than under v1.13.2's ordered list |
| (c) The announcement is not outreach | First week of October | The first target-organized admission step is the NDAs (p. 23); audit R2's post-challenge reading (C14) and Alex's voice note III.1 as the audit reports it |

No bid, entry or exit changes round under any of the three. Round opened keeps **Inferred = Y** under every reading: the 08/19 press release announced only that PetSmart "determined to explore strategic alternatives … including a possible sale of the Company" (p. 23), not a round or a procedure, and the opening is chosen among readings.

**D7 and D17.** No partial-scope party exists. Industry Participant's approaches spoke of "a possible combination of the two Companies" (08/07 and 08/27, pp. 22–23), but the board weighed "an acquisition by or a combination with Industry Participant" (p. 22), and in spring 2014 Industry Participant said it was not for sale while PetSmart considered acquiring it (p. 21; Deal facts). [I] The roles are disclosed, so this is not an unresolved merger-of-equals episode; #7 and Q8 stand.

**E9 under D11.**
- **10/30/2014 (#17): Enforced on reading A; Unclear on reading B.**
  - [F] "On October 30, six of the potentially interested parties submitted indications of interest. From October 30 to November 2, 2014, representatives of J.P. Morgan spoke by telephone with all of the potentially interested parties, including those that did not submit an indication of interest, to hear the parties' respective rationales …"; "As a result of its discussions with J.P. Morgan, … Bidder 2 …, which had initially indicated a price of $78.00, increased its indication to a range of $81.00 to $84.00 per share" (p. 24). On 11/03 the board advanced the four "at or above $80.00" (p. 24); Bidder 2 is among them only because of its revision. The filing gives neither the revision's day nor any invitation to revise, and reports no late first IOI.
  - Rule 1: no later due date was set. Rule 2: needs an overdue *required* response. Bidder 2's required response, its $78 IOI, arrived on time; its revision was not a response the target asked for (§3 E9: "Do not infer an invitation only because conversations with the banker came before a price increase"); no non-submitter bid later. So rule 2 does not fit, whatever day the revision arrived.
  - **Reading A: Enforced.** The 11/03 step used the six IOIs submitted on 10/30 together with Bidder 2's revision of its on-time IOI (window 10/30–11/02; day and any invitation not reported). No late first response and no submission by a non-submitter was considered. The case for Enforced rests on rule 2 not fitting; it does not rest on the target having acted only on what it held at the cutoff, which the filing does not show. This matches Q7-A's prediction ("both Enforced; PetSmart no longer depends on the unreported day").
  - **Reading B: Unclear.** Rule 3's text covers improvements the target "invited afterwards", and D11 speaks of improvements "the target invites after acting on the bids in hand". Bidder 2's revision is neither shown to be invited nor shown to follow a target step, unless J.P. Morgan's calls count as acting on the bids. On that reading no rule fits cleanly. This is a general wording gap (an uninvited revision from an on-time bidder before the target's next step), which R could close; D11's wording also echoes Q7 option C.
- **12/05: superseded before arrival; no outcome.** Unchanged (Q3 keeps its alternative).
- **12/10 (#33): Extended.** A later date was set after the bids were evaluated: "submit improved bids on December 12, 2014" (p. 25); confirmed in D27.
- **12/12 (#39): Enforced.** All responses came on 12/12, and the board acted on 12/13 on "the final bids" (p. 26).

**D10.** No bidder missed a due date and carried on. #36 stands (Bidder 3 is not mentioned again). #23 stands as an exit, but its timing is for the v1.14 review: J.P. Morgan spoke with the non-submitters until 11/02 about their "rationales for not submitting", so under E14 (no exact date from a disappearance) its window should probably run to 11/02 or 11/03 rather than end on 10/30. No count changes.

### 3. Rows and Rounds lines that would move

| Where | Change (reading A) |
|---|---|
| Rounds P1 R1, Deadline outcome | Unclear → **Enforced** |
| #17 Deadline (10/30), Note | Record the outcome and why: the 11/03 selection used the six 10/30 IOIs and Bidder 2's revision of its on-time IOI (window 10/30–11/02; day and any invitation not reported); no late first response or non-submitter's bid was considered; the revision is not an overdue required response |
| #24 Bid (Bidder 2), Note | Optional: "revises an on-time response; not an overdue required response". No field changes |
| Q2 | Question: "Round 1 deadline outcome: the 10/30/2014 IOI due date. Enforced, Extended (late bid accepted) or Unclear?" Recommended: Enforced, alternative Unclear. Why and What changes rewritten on the grounds above; the revision's day no longer matters |
| Possible new row | J.P. Morgan's 10/30–11/02 calls as an Other material event (price feedback, §3 E2 and D2), a judgment call; the filing describes them as hearing rationales |
| #23 | Window to 11/02 or 11/03 (E14; above) |
| No change | Rounds R2; #28, #30, #33, #37, #39; Q3's answer (its "What changes" cites Q1 alternative (ii), which count-once weakens) |

Only if Austin or Alex picks another round-1 opening: under (a), the Round opened row moves to 08/13 ahead of the Target sale decision (new #8 Round opened; new #9 Target sale decision, moving from round 0 to 1); under (c), #10–#13 move to round 0 (renumbered #9–#12) and Round opened becomes #13, first week of October (10/01–10/07, Sort date by 10/04), with Industry Participant leaving R1 Who was in. Q1 gains the 08/13 reading and drops or weakens alternative (ii).

### 4. Conflicts with recorded rulings

- **The 24 September revert (r2).** Reason: "Q2 restored to the Part F deadline-outcome question instead of asking a fact the filing cannot supply; Unclear added as an option to match the current Rounds outcome." `revert-2026-09-24.md`: "Unclear is added because the Rounds outcome is now, correctly, Unclear." That ruling applied v1.13.2's E9, under which the unreported day decides. Reading A changes the label, not the ruling's fact (the day is still unknown); D11 makes the day immaterial. §6 and §9.3 already record this. Under D24 r2 stays unchanged; Enforced must not be written into the v1.13.2 working copy, and replaying r2 onto a v1.14 run must not bring Unclear back (audit B, O3).
- **Audit A16** ("Unclear or Late bids accepted") is overtaken: `Late bids accepted` is not a v1.14 value, and an unrequired revision is not an extension.
- **No other conflict.** The audit verified the round-2 chain and Alex III.6 ("not a new round"); §3 keeps both. Round 1's opening has no ruling (#9 and Q1 are Needs decision).

### 5. Recommendation

For the v1.14 review, code **10/30 Enforced**, with the reasoning in #17's Note and Q2, and leave round 2 as it is (12/05 superseded; 12/10 Extended; 12/12 Enforced). The genuine alternative is **Unclear**, if Austin reads D11's "after acting on the bids in hand" as the boundary; R could close the wording gap generally. If Alex answers Q7 otherwise: option C gives Unclear, option B `Extended (late bid accepted)`. Leave r2 unchanged. Put §3's 08/13 reading beside 08/19 and October in the round-1 question; the filing gives October the most direct support, and nothing but the opening row and a few round-0/1 labels moves.

### Review notes (skeptic)

Adopted: the Enforced reasoning no longer claims the 11/03 step used only what was received by the cutoff; Inferred = Y stays on round 1 under every reading; `inventory/petsmart.csv` and `response-R2.md` exist and are listed; D7/D17 addressed; #23's window; J.P. Morgan's statement to Bidder 3 kept. The conclusion (Enforced on reading A, Unclear as the alternative) is unchanged.

## For Decision 1 (Alex)

**The shared question.** When the target selects who advances, gives them diligence, and only later sends a letter asking for final offers, is that one round or two? §3 E6 says "Admission, common diligence and a later letter setting that stage's submission are steps within one round". It also keeps the older rule that the target's "first request for final, binding or best-and-final offers, even to unchanged bidders" opens a round. §3 does not say which governs when the letter is also the first final request; the candidate (line 181) keeps both sentences in one paragraph. Kraton and Datalink turn on this; sTec turns on whether 16 May was final and whether 31 May reopened the contest. Meredith (12/21 admission → 01/12 final letter) has Kraton's structure and should follow the same answer.

**Kraton** (pp. 33–40)

| | Current map (r4) | Map under §3 (count once) |
|---|---|---|
| Round 1 | 05/24/2021 → 07/20; due 06/29 → 07/19; Extended; Enforced; Not final | Same |
| Round 2 | 07/20 admission of A, H, Parent; diligence; no request; No deadline stated; Not final; 0 bids | 07/20 admission, diligence (week of 08/09) and the final bid procedures letter after 08/11; due 09/15 (markups 09/08, not a deadline); Extended (late bid accepted); Announced as final; bids from Parent and A |
| Round 3 | Letter after 08/11 (Sort 08/11); due 09/15; Late bids accepted; Announced as final | — |
| Recorded ruling | None; round rows Needs decision | — |
| Alex (as reported) | — | Agrees on merging 07/20 and the letter; would make 07/06 a separate informal round, which §3 keeps in round 1 |

**Datalink** (pp. 27–36)

| | Current: base (v1.13.2 run) | Standing: F9 map (pilot, five rounds) | §3 with count once (four rounds) |
|---|---|---|---|
| January–May | Round 0 | Round 1 from 01/29 (inferred) | Round 1 from 01/29 (inferred) |
| June outreach | Round 1 from 06/06; Enforced; Enforced | Round 2 | Round 2 |
| 07/27 selection | Round 2; no request; 0 bids | Round 3; no request; 0 bids | Round 3 opens here… |
| 08/16 final letter | Round 3; due 08/30; Late bids accepted; Announced as final | Round 4; Extended (late bid accepted) | …and the letter is a step in it; due 08/30; Extended (late bid accepted); Announced as final |
| 10/01 re-approach | Round 4 (inferred); Inferred final | Round 5 | Round 4 |
| Ruling | Conflicts with F9 on round 1 | Austin's F9 (21 Sep): "keep five rounds" | Would revise F9's five-round count; needs Austin's decision |

Alex's reported reading (round 1 starts at the bank's first contact) would put round 1 at the June outreach, as in the base.

**sTec** (pp. 27–32)

| | Current map (r1) | Map A under §3 (recommended) | Map C (Alex's voice note) |
|---|---|---|---|
| Round 1 | 04/01 → 05/16; due 05/03; Late bids accepted; Not final | 03/26 (or 04/01); due 05/03; Extended (late bid accepted); Not final | Same as Map A |
| Round 2 | After 05/16: "final round process letters" and draft agreement to WDC and D; due 05/28 → 05/30; Extended; Enforced; Announced as final | From 05/15 (or 05/16) to signing; same due dates and outcomes; Announced as final; includes WDC's 05/31 withdrawal and 06/10 return, D's exit 06/05, and WDC's $6.85 on 06/14 | 05/15 or 05/16 → 05/29; due 05/28; Enforced; **Not final** |
| Round 3 | Inferred, 05/31 → signing; no due date; Announced as final | — | From the 29 May best-and-final request; due 05/30; Enforced; Announced as final; to signing |
| What decides it | — | The target announced a final round (p. 30); nothing after 05/30 is a new solicitation or selection | "sTec's request for non-binding proposals" (p. 30) outweighs the target's "final round" label |
| Alex's record | Voice note: 28 May round "is not the final round" and bidding continued | Hand coding: one final round, extended to 06/10, no round 3 (agrees on round count; differs on the 05/30 outcome) | Voice note |

Map B (the current map restated under §3: round 3 from the undated call to D, window 05/31–06/01, Sort date 06/01) is the alternative if the 05/30 selection counts as a suspension.

## E9 under D11: Mac-Gray and PetSmart against Q7-A

On 24 September Alex was offered Q7-A: "Late bids accepted only when a bidder missed the due date and its first response was still considered; improvements the target invites afterwards are bargaining within the round". It predicted "both Enforced; PetSmart no longer depends on the unreported day", meaning Mac-Gray's 09/18 and PetSmart's 10/30 due dates. D11 adopts Q7-A with two changes: an accepted late response is recorded as `Extended (late bid accepted)` (Alex's convention, reported verbally by Austin), and it covers any overdue required response, "first, revised or final".

| Deal and due date | What happened | Outcome under D11 | Q7-A's prediction | Holds? |
|---|---|---|---|---|
| Mac-Gray 07/23 | B and C bid 07/24; reviewed 07/25; admitted (pp. 32–34) | Extended (late bid accepted) | (Not part of the prediction; v1.13.2 Late bids accepted) | Relabel |
| Mac-Gray 09/09 | A and C sent revised proposals 09/10; reviewed 09/11 (p. 35) | Extended (late bid accepted), because D11 covers revised responses | (Not part of the prediction) | Relabel |
| Mac-Gray 09/18 | All three responders on time; Committee acted 09/19; $21.25 invited afterwards, no new date (pp. 36–37) | **Enforced** | Enforced | Yes |
| PetSmart 10/30 | Six IOIs on 10/30; Bidder 2's uninvited revision of its on-time IOI, day unreported; board acted 11/03 (p. 24) | **Enforced** (reading A); Unclear (reading B) | Enforced | Yes on reading A |
| PetSmart 12/05 | Superseded 12/04–12/05 | No outcome | — | — |
| PetSmart 12/10 | New date (12/12) set after evaluation (p. 25) | Extended | — | — |
| PetSmart 12/12 | All responses on time; board acted 12/13 (p. 26) | Enforced | — | — |

For the case appendix: under D11, Mac-Gray's two deadlines missed by one day, whose late responses were considered, become extensions (soft deadlines), while the 09/18 deadline followed by a target counter to the preferred bidder is Enforced. PetSmart's 10/30 is Enforced only if an uninvited revision of an on-time bid, made before the target's next step, counts as outside rule 2 and inside rule 3; D11's words ("after acting on the bids in hand") leave that open, and R could settle it generally.

## Questions only Austin can decide

1. Count-once against the first-final-request trigger (Kraton, Datalink, Meredith). If count-once governs, Datalink's F9 "five rounds" is revised to four.
2. sTec: Map A (round 2 continues) or Map B (round 3 reopened after the 05/30 selection).
3. Synacor: whether the CEO's 10/27 contact with Company H is the reopened outreach (main map) or routine follow-up (Alt-R2).
4. The round-1 date under "the earliest supported of" (sTec 03/26 against 04/01; PetSmart 08/13, 08/19 or October): a general wording question for A1 and R rather than a per-deal call.
5. Spec silences met here, where I took the conservative choice: which Process and Round a D17 non-sale row carries when it falls between processes (the then-current round); and the date of a later, non-reopened round opened by an undated letter after a dated decision (E8's decision-day rule).
