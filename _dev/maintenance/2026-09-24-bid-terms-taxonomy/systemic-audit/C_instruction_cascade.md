# C. Instruction cascade audit: V114_SPEC §2–§4 against the 24 September draft

25 September 2026. Read-only text audit. Base: `SEC_Deal_Ledger_Extraction_Instruction_v1.14_draft.md` (289 lines; cited as bare line numbers). Spec: `V114_SPEC.md` (cited `S:n`). Checker: `_dev/tools/check_lean.py` (cited `ck:n`). No repo file was changed except this report.

Tags: **[V]** verified by reading the text or code; **[I]** my inference or judgment.

## Headline findings

1. **[V] D1 "on those rows" anchor (55–64).** Items 10, 11 and 13–19 all say "on those rows", which points back to item 8's list "Bid, Bid reaffirmed and Other-scope bid rows" (53). Items 11 and 12 say it as well. If A1 narrows item 8 to "Bid and Bid reaffirmed rows" as S:151 directs, Stock %, Formality, Conditions and all five condition columns silently stop applying to Other-scope rows. That contradicts D18 ("the other bid columns stay required") and F.4 (286). The spec does not mention the anchor.
2. **[V] Three sentences directly contradict adopted rules, and the spec names none of them:**
   - 230: "Required … including a bidder that stops when refused" contradicts §4's "a later refusal or departure does not show that an earlier request was conditional" (S:331).
   - 208: "Alternative structures in one communication are separate Bid rows" contradicts "One offer communication is one row" (S:258).
   - 160: E5(b) "three months or more … with no reported contact" contradicts "Silence about contacts does not prove inactivity" (S:213).
3. **[V] 210 (Bid reaffirmed) keeps a state carry.** It reads: "… as they stand at that date, updated by anything the filing reports by then". This is TAXONOMY_DRAFT5 §3.3(a), which D1's note (S:95) says express incorporation replaces. S:263 says only "code its fields by the same rule", and §9.1 ("no text still says to copy…") will fail if 210 survives.
4. **[V] D10 is not carried into E14's inference list.** Line 264 still infers **Did not submit** from "eligible for a solicitation and no submission reported". Its example ("21 signers − 2 earlier exits − 8 submitters = 11") subtracts from lifetime signers, which S:207–208 forbids. Line 257's "not necessarily permanent" must go.
5. **[V] D7 misses several places:**
   - E4's live units (153) and E5's closure Count (163);
   - E14: only entrants get exits (260), Withdrew's definition (256) against "usually Withdrew" for a switch (S:182), and the inferred-exit transitions (262–269);
   - D3 Bids received (112);
   - the "unresolved scope" case in 129.
6. **[V] Spec decision IDs collide with the instruction's own section IDs D1–D5.** Examples: "a CVR (D4) or exclusivity (D14)" (S:317); "follow D17" (S:187); "(D18)" (S:151, S:171). Copied into the candidate, "(D4)" would point a model to the Questions sheet. The candidate must carry no D-numbers from §1.
7. **[V] The candidate would still carry a deal-derived example.** Line 247 has "Ref: $12.10 close 08/08/2014; 49% premium", which is Penford's disclosed figure: $12.10 close on 8 August 2014, against an $18.00 indication, is 48.8%. The line comes unchanged from v1.13.2. The §9.1 name grep will not catch it.

---

## 1. The change map

Kind: **R** = replacement, **I** = insertion, **D** = deletion, **P** = already present in the draft (a no-op or a rewording at most), **X** = cross-reference only. Every cascade line below was located by exhaustive search [V]. Whether a cascade needs a change is marked [I] where it is a judgment.

### §2 Part A (verified: the §2 text differs from draft lines 8–20 by exactly the four stated edits)

| Spec item | Draft lines | Kind | Cascade lines | Notes |
|---|---|---|---|---|
| Departures sentence (S:109) | 10, after "…then collects formal bids." | I | none required | Operative forms already exist: E1 129; E5 157–163; E6 169–173; E9 204. |
| "for the whole company" (S:113) | 14 | I | E1 129 and 131; E3 143 and 149; E4 153 ("live units"); E5 163 ("closes all participation … Count"); E14 260, 262–269 and 271; D3 108, 112 and 113; F.1 283; D5 121 (label must stay verbatim, §4) | The spec carries it only to E3, the E14 formula, F.1 and D3 Who was in (S:160, S:188–191). |
| Item 3 rewritten (S:115) | 16 | R | E10 208 ("price or material economic terms" must cover condition and commitment changes, because Part A now says "a later revision that changes them is a new bid"); E12 224 ("the five condition columns" includes Exclusivity, which Part A now calls "a term") [I]; E12 241 (CVR sentence); E11 220 | Also drops Part A's "keep Not stated apart from a negative". Its operative form survives at 232 [V]. |
| "upgrade" → "change" (S:119) | 20 | R | none | The only occurrence of "upgrade" [V]. |

### §3 Instruction changes

**Header, B and C**

| Spec item | Draft lines | Kind | Cascade lines | Notes |
|---|---|---|---|---|
| Header (S:127) | 3: "**Revision of 24 September 2026, v1.14 (draft).**" | R | none | Keep the bold and the final period (the v1.13.2 form). No code parses the header: I searched `_dev/tools/**/*.py`, and only synthetic test fixtures mimic the format [V]. |
| B: four kinds of value (S:130–134) | 24: "Every cell is one of three things" | R | 26 (lists "an exit label or reason the filing does not establish" as false precision); 285 (F.3: "every inference carries Inferred = Y") | "Three things" has no slot for exact calculations or classifications. |
| B: field-level Inferred (S:135) | 24; 67 (D1 item 22: "Y where the event is your inference") | R | 28 ("On an inferred row, quote the reported fact that anchors the inference": an inferred field's anchor may lie elsewhere, so the Note should give the page, as at 232); 68 ("on an inferred row, how you know": name the field); 285; 163 and 262 (existing Inferred = Y uses) | [I] 171 ("An unannounced round is inferred") and 177 ("Inferred final") use "inferred" as a classification. Say whether a Round opened row for an unannounced round takes Inferred = Y. |
| B: evidence at its own date (S:136–139) | new text after 26 | I | 224 (copy rule; replaced via E10); 210 (Bid reaffirmed state carry, Headline 3); 226 (Due diligence "from the bid or from the rest of the background": later passages count only if they date the fact) | 224's last sentence (the outside-background timing rule) is consistent [V]. |
| B: an inferred closure may have an unknown reason (S:140) | 285 | X | 262 ("Exit reason = Not stated", unconditional); 26 | See F.3 below. |
| B: keep (S:141) | 26, 28 | P | — | |
| C Read: inventory (S:144) | 32 | I | — | |
| C Map: relationships (S:145) | 33 | I | 108; 143 | |
| C Reread: both directions (S:146) | 35 | P | — | 35 already checks each paragraph "two ways" [V]. |
| C: reconcile after correction (S:147) | 36 and/or 281 | I | 283–286 | |
| C: no human checkpoint (S:148) | none | no-op | 10 ("An expert reviewer will check your workbook by hand") is later review, not a checkpoint | The draft promises no checkpoint [V]. Add nothing. |

**D1 to D5 and F**

| Spec item | Draft lines | Kind | Cascade lines | Notes |
|---|---|---|---|---|
| D1 items 8, 9, 12 (S:151) | 53, 54, 57 | R | **55–64, "on those rows"** (Headline 1); E1 129 ("leave whole-company prices to whole-company bids" is weaker than D18); E13 245 (Price low and Price high: no Other-scope exception), 247 and 251 (CVR value); F.4 286 | Define the bid-row set once (for example in item 10) and state the D18 blanks separately. |
| D1 items 11, 18: Y, Varies or blank (S:152) | 56 ("Y … ; else blank"), 63 (same) | R | E12 229 (Antitrust "Y … ; blank for …"); E13 251 ("CVR/earnout is Y where …"); E12 232 (already says "A Y on a cohort row means every member carries it"; only "if only some do, Varies" is new); **57/251: say CVR/earnout value is filled only when CVR/earnout = Y** (checker `bid.cvr_value_marker`, ck:630); E13 249 (Stock % Varies, D16) | |
| D1 item 22 (S:153) | 67 | R | 24, 28, 68, 285 | |
| D2 Bidder interest (S:156) | 81 ("An approach that names a price is a Bid") | R | 208 ("A valuation statement made without an offer is not a Bid"); 89 (Other material event: "a valuation statement without an offer"); 90 and 129 ("undisclosed-price proposals") | [I] Keep the first-contact Note clause from 81. |
| D2 Did not submit (S:157) | 93; 257 | R (via E14) | **264** (Headline 4); 271; 283; 89 (add missed submission and price feedback to the Other material event list) [I] | **The "round's deadline account" is not a field.** The Rounds sheet has Due dates, Deadline outcome, Bids received and How it ended (104–113); the ledger has the Deadline row's Note (202). Name the place. |
| D3 Who was in (S:160) | 108 | R | 113 ("five advanced, eleven out"); 143 | Keep "still being received, not admitted" (108) [V]. |
| D3 Deadline outcome values (S:161) | 110 | R | E9 204; 202; 109 ("none stated"); F 277 | The list order differs from E9's first-that-fits order; this is cosmetic. |
| D3 Bids received (S:162) | 112 ("number of bidders that bid, with names") | R | 113 | **D7 scope is not stated**: do Other-scope bidders count? [I] Whole-company only, listing partial bids separately. |
| F: keep a range or an unknown (S:165) | 279 | I | 117 (Recommended answer) | |
| F: issue type (S:166) | 279 or 117 | I | 117 | There is no new column: name the existing column that carries it (checker `QUESTION_COLUMNS` is fixed, ck:119). |
| F: group rows (S:167) | 279 | I | 279 ("Flag every row a Question touches") | |
| F: audit for omitted events (S:168) | 281 | I | 35 | |
| F.1 (S:169) | 283 | R | 260; 271; 163 | |
| F.3 (S:170) | 285 | I | **262** ("with Inferred = Y, Exit reason = Not stated": add "unless the filing reports one"); 26 | Checker `exit.inferred_reason` (ck:924–932). |
| F.4 (S:171) | 286 | I | 53–64 anchor | The spec's first sentence is 286 verbatim [V]; only the D18 sentence is new. |
| D5 (S:173) | 121 | no text change | 40 ("exactly four sheets") | **Do not edit 121's field labels or their parentheticals**: the checker accepts only those strings (ck:131–169; §4 below). |

**E1 to E5**

| Spec item | Draft lines | Kind | Cascade lines | Notes |
|---|---|---|---|---|
| E1: whole-company contest primary (S:176) | 129 | I | 14 | |
| E1: partial-only bidders (S:177–181) | 129; 131 | I/R | 143 (E3 entry by "bids" currently includes Other-scope bids); 181 (a reused agreement "becomes its entry"); **260 (only entrants get exits: how does partial-only participation end?)**; 163; 153; 112; 137 ("among live bidders") [I] | [I] 129's "unresolved scope" Other-scope rows: counted in the contest or not? The spec is silent. |
| E1: switch to partial (S:182) | new text | I | **256** (Withdrew = "the bidder says it will not continue"; a switch does not fit; widen the definition or name the case); 94 | |
| E1: re-entry after a switch (S:183) | new text | I | 94; 260 | |
| E1: a later partial proposal (S:184) | new text | I | B date rule | |
| E1: break-up Question (S:185) | new text | I | 279 ("the Questions the conventions call for") | |
| E1: screen (S:186) | 131 | R | 121 (label unchanged) | |
| E1: MoE (S:187) | new text | I | 277 (alternative map); E5 | Write D17's content in the instruction's own words, not "follow D17". |
| E1: carry-through (S:188–191) | 143; 271; 283 | R | also 14, 108, 112, 153, 163, 256, 260, 262–269 | |
| E2: drafts (S:194) | 135 ("negotiation of legal terms and successive drafts") | R | 208 | |
| E2: routine circulation (S:195) | 135 | P | — | |
| E2: requirement vs acceptance (S:196) | 135; 89 | I | 89 | |
| E2: feedback and information (S:197) | 135; 137 | I | 89 | |
| E3/E4: four statuses (S:200–204) | 143 | I | 108; 264 | |
| E3/E4: counts (S:205–208) | 149 | I | **264's example**; 26 | |
| E3/E4: named vs cohort (S:209) | 147; 269 | P | — | |
| E3/E4: joint bidding (S:210) | 153 | P | — | |
| E5: silence (S:213) | 160(b) | I | **160(b)** (Headline 2); 277 ("interval of about two months or more with no reported contact") | Astra kept (b) (ASTRA:182). Reconcile it explicitly. |
| E5: NDA ≠ negotiation (S:214) | 159(a) | I | — | |
| E5: termination vs lapse (S:215) | 163 | P | — | |
| E5: close once (S:216) | 163; 260 | P/I | 271 | |
| E5: returning participants (S:217) | 163 ("enters it afresh") | P | — | |
| E5: MoE continuity (S:218) | new text | I | 277 | |

**E6 to E9**

| Spec item | Draft lines | Kind | Cascade lines | Notes |
|---|---|---|---|---|
| E6: "Use the earliest supported of:" (S:222) | 173 ("Use, in order:") | R | 173's own list: "the decision that launched it" is always earliest when outreach follows within a week; compare S:231 ("not the earlier board authorization") [I] | The only occurrence [V]. |
| E6: earliest organized stage, including bilateral (S:223) | 173 | R | **173 lead sentence** ("Round 1 opens when the target or its banker begins soliciting buyers") does not fit bilateral negotiation; 169 | |
| E6: unsolicited approach (S:224) | 173 ("Earlier approaches and unsolicited proposals are round 0") | P | — | |
| E6: outreach does not demote (S:225) | 173 | I | — | |
| E6: count once (S:226–228) | 171 | I | 33 | |
| E6: delete "opens a distinct information stage tied to new offers" (S:229) | 171 | D | none | The only occurrence [V]. |
| E6: reopened outreach (S:230–232) | 171 | I | 161 (E5(c) "a new outreach" is a fresh-start test; the spec's "unless E5" covers it); 173 (decision date); **198** (Sort date "the decision day for an undated consequence of a dated decision" gives the authorization date when the outreach is undated) [I] | |
| E6: extensions stay in the round (S:233) | 171 | P | — | |
| E6: Finality (S:234) | 177 | I | 111; 217 | |
| E7: contacts (S:237) | 181 | I | — | |
| E7: annexes (S:238) | 181 or 32 | I | — | |
| E8: order (S:239) | 198 | I | 198 ("Reported days never move") | Consistent [V]. |
| E8: Round opened is the first row (S:240) | 86 or 198 | I | 44; 106; 173 ("an exit row carries the round being left") | The checker enforces this today (`round.opening_order`, ck:1171–1179) but the draft never states it [V]. |
| E9: outcomes (S:243–248) | 204 | R | 110; 202; 171; 220 | S:245's "This follows Alex's convention" must not ship (§5). |
| E9: record the facts first (S:249) | 204 | I | — | |
| E9: outcomes differ by bidder (S:250) | 204 | I | 110 ("one value per due date") | |
| E9: superseded date (S:251) | 202 | P | — | |
| E9: missed response vs exit (S:252) | new text | I | 257; 264 | |

**E10 to E14**

| Spec item | Draft lines | Kind | Cascade lines | Notes |
|---|---|---|---|---|
| E10: a Bid is a communicated proposal (S:255) | 208 | I | **129** (a second definition of Bid; §9.1 wants one) [I]; 81 | |
| E10: material revision, including same-price (S:256) | 208 ("Every change of price or material economic terms") | R | 135; 210 (reaffirmation gate); 16; 68 (Note list: add reverse fee) [I]; 96 | "The target's termination fee stays in a dated Note": say which row's Note. The draft never mentions fees [V]. |
| E10: signing adds no row (S:257) | 96 | P | — | |
| E10: one communication, one row (S:258) | 208 | I | **208 alternatives** (Headline 2); 230; 88 | |
| E10: express incorporation (S:259–262) | 224 ("then copy the earlier row's values and write “Terms: as #n” in the Note") | R | **210**; 232; 241 | The Note gains "(p. x)" and names what was carried. |
| E10: reaffirmed, same rule (S:263) | 210 | R | — | Replace "as they stand at that date, updated by anything the filing reports by then". |
| E11: price-only revision (S:266) | 214–220 | I | 224/E10 | |
| E11: later document work (S:267) | 216 | I | B | |
| E11: final-round label (S:268) | 217 | I | 173 ("A bid belongs to the solicitation it answers") [I] | An unsolicited bid during a final round: which round does it take? |
| E11: keep (S:269) | 220 | P, except "a letter alone", which is new | — | |
| E13: compatible subtraction (S:274) | 247 | I | 245 ("never added in"); 251 | **Gap**: the spec does not say what fills the price cells when the bases are incompatible [I]. |
| E13: share-price series (S:275) | 247 | I | — | |
| E14: check before inferring (S:278–282) | 262 | I | 264–267 | |
| E14: Did not submit (S:283) | 257 | R | 93; **264** | |
| E14: missed but continuing (S:284) | 257; 260 | I | 94 | "See D2" resolves to the instruction's D2 [V]. |
| E14: Re-entered (S:285) | 94; 260 | I | E1 | |
| E14: selection, scope, signing (S:286) | 255; 258 | I | **255** ("refuses it the next stage"); **265** (inferred Dropped by target when "the complete advancing set is named or counted without it") both need the reserve or continuing-discussion exception | |
| E14: actor, timing, reason (S:287) | 255–258 | I | — | |
| E14: no valuation or date from a disappearance (S:288) | 262 | I | 14 (verbatim Part A: "an exit tells the model something about that bidder's valuation") [I] | Word E14 so that the extractor records and the model interprets. |
| E14: price comparison in the Note (S:289) | 273 | I | — | |
| E14: regulatory exits deferred (S:290) | none | no text | — | Adding "deferred" would be project-status text (§5). |

### §4 Conditions (E12)

| Spec item | Draft lines | Kind | Cascade lines | Notes |
|---|---|---|---|---|
| Structure and order (S:304) | 234 | P | — | |
| H1 (S:307) | 238 | R | 227; 241 ("Begin a bid row's Note with the fact driving its level": name H1–H3) [I] | |
| H2 (S:308–311) | 238 ("a stated multi-week period counts") | R | **237** (Light: "confirmatory, **expedited** or limited"; H2's defeat names only "confirmatory or limited"); 239 (Unclear clause); 226 | |
| H3 (S:312–317) | 238 ("a right to reprice or an identified obstacle to completion") | R | **228** (Concern includes "doubt about closing", which overlaps "an obstacle to completion that the filing identifies for this bid"; state the boundary) [I]; 236 ("no other material condition"); 220 | |
| None, Light, Unclear kept (S:319) | 236–239 | P | — | |
| Due diligence: Not begun (S:322) | 226 | I | — | |
| Financing: D5 (S:323–326) | 227 | I + R | 227's Contingent list ("a highly confident letter …", "any part uncommitted") must also yield to the precedence, not only its last sentence; 68 | |
| Regulatory and Antitrust (S:327) | 228; 229 | I (Note) | — | |
| Exclusivity (S:328–333) | 230 | R + I | **230 "including a bidder that stops when refused"**; 88 (Exclusivity changed); 208 | [I] A request made inside the bid's own letter: one row or two? D15 covers only later requests. |
| CVR sentence (S:334) | 241 (E12's last paragraph) | I | 16; 238 | |
| Cohorts (S:335–339) | 239; 232 | I | 147 ("One member's terms never describe the cohort") | |
| Dates (S:340–342) | 224 | I | 210 | |
| Examples table (S:344–360) | none | decide whether to include it | 220 (an unlabelled Heavy example; §9.1) | It names no deal [V]. |

## 2. Unmentioned conflicts

These are places where the draft's current text contradicts a V114 rule but §3 and §4 do not name the place. All were verified in the text; the fix direction is [I].

1. **55–64**: "on those rows", anchored to item 8, contradicts D18 once item 8 changes (Headline 1).
2. **208**: "Alternative structures in one communication are separate Bid rows" contradicts S:258 "One offer communication is one row". Astra kept the exception ("normally", ASTRA:170).
3. **210**: "as they stand at that date, updated by anything the filing reports by then" contradicts S:139 (an earlier row's value is not evidence) and D1's replacement of §3.3(a).
4. **230**: "including a bidder that stops when refused" contradicts S:331.
5. **160 (E5(b))**: the no-reported-contact break test contradicts S:213.
6. **257**: "not necessarily permanent", and **264**'s trigger and example, contradict D10 and S:207–208.
7. **255 and 265**: "refuses it the next stage" and the inferred Dropped by target contradict S:286 ("Selection for one stage does not exclude…") and S:282 (reserve status).
8. **256**: Withdrew's definition does not cover the switch that S:182 labels "usually Withdrew".
9. **260**: "Only participants that entered (E3) get exits". Under D7, partial-only parties never enter, so the close of their participation has no rule.
10. **262**: "Exit reason = Not stated", unconditional, contradicts the F.3 addition ("unless the filing reports one").
11. **24**: "one of three things" contradicts the four kinds of value (S:130).
12. **26**: "an exit label or reason the filing does not establish" treats inferred exit labels as false precision, while E14 assigns them by transition.
13. **28 and 68**: evidence and Note duties are written per row ("on an inferred row"), which does not fit field-level Inferred.
14. **173, lead sentence**: "begins soliciting buyers" does not fit S:223's "including substantive bilateral negotiation". Choosing the decision date (173) also sits badly with S:231 ("not the earlier board authorization").
15. **198**: the Sort date "decision day for an undated consequence of a dated decision" conflicts with S:231 when the outreach is undated.
16. **237**: Light's "expedited" does not match H2's defeat list (S:310).
17. **228**: Concern's "doubt about closing" against H3's "obstacle to completion … for this bid" (S:315–317). There is no stated boundary, so "Concern does not by itself trigger H3" is hard to apply.
18. **227**: the Contingent list (highly confident letter, "any part uncommitted") is not subordinated to D5, because S:325 amends only the last sentence.
19. **249**: Stock % "Varies on a cohort row whose members differ" lacks D16's partial-reporting case.
20. **57 and 251**: nothing says CVR/earnout value requires CVR/earnout = Y. With Varies now allowed, a cohort value would fail `bid.cvr_value_marker` (ck:630–631).
21. **245 and 247**: the price cells have no Other-scope exception (D18), and there is no rule for incompatible package bases (S:274).
22. **112, 153 and 163**: Bids received, E4 live units and the E5 closure Count are unscoped under D7.
23. **88**: Exclusivity changed ("requested, …") has no D15 exception for a request made with a material revision.
24. **220**: "record Formal with Conditions = Heavy" is a Heavy example that names no trigger (§9.1).
25. **129**: a second definition of Bid, next to E10's new one (§9.1 asks for one definition each). "Unresolved scope" is also unplaced under D7.
26. **224**: "the five condition columns" includes Exclusivity, which the new Part A calls "a term" and not a condition. This is terminology only [I].
27. **14 (Part A, verbatim)**: "an exit tells the model something about that bidder's valuation" sits beside S:288's "Do not infer a valuation … from a disappearance". There is no logical conflict, but E14's wording should keep the two roles apart [I].

## 3. Part A references

Every reference below resolves against the §2 text [V].

| Line | Reference | Resolves? |
|---|---|---|
| 20 (inside Part A) | "these five uses" | Yes: §2 keeps items 1–5. |
| 20 | "(Part F)" | Yes. |
| 125 (E preamble) | "use judgment from Part A for everything they leave open" | Yes: §2's last paragraph ("Where they are silent, make the call that serves these five uses best"). |
| 279 (F) | "matters for the five uses in Part A" | Yes. |
| §2 item 3 | "(E11)" | Yes. Part A summarizes only two of E11's three routes; route 3 (218, confirmation during finalization) is omitted, as it was before [V]. |
| §2 item 3 | "(E12)" | Yes. |
| §2 item 3 | "a later revision that changes them is a new bid (E10)" | **Only after E10 changes.** 208 today covers "price or material economic terms", not condition changes; S:256 fixes this. |
| §2 item 3 | "(item 5)" | Yes (18). |

There are no other occurrences of "Part A", "five uses", "judgment" or "Part A item" [V]. The other part references (Part B at 149 and 264; Part D and Part E at 34; Part F at 36 and 117) all resolve.

## 4. Value lists and columns against the checker

**Columns and fields: all match today [V].** Checked by script:
- the D1 29 columns (46–74) equal `LEDGER_COLUMNS_V114` (ck:74–104);
- the D3 10 columns equal `ROUND_COLUMNS`;
- the D4 7 columns equal `QUESTION_COLUMNS`;
- the D5 17 field labels (121), including their parentheticals, each match `FACT_FIELD_OPTIONS` (ck:131–169);
- `SHEETS` has four sheets (line 40).

V114 adds no column or field. D20's Source sheet is added only by the pipeline. Risks: an edit to 121's parentheticals, or a Question "issue type" that a model puts in a new column, would break the checker.

**Controlled lists:**

| List | Draft | Checker | Today | After V114 |
|---|---|---|---|---|
| Event labels | 80–98 (30 labels) | `EVENTS` | equal [V] | no label added (D10: "No new label") |
| Type | 49 | `TYPES` | equal | — |
| Acquirer type (D5) | **no list stated** (121) | prefix of `TYPES` (ck:1555–1564) | instruction silent; checker enforces | unchanged; [I] state it |
| Formality, Conditions | 58, 59 | `FORMALITY`, `CONDITIONS` | equal | — |
| Due diligence, Financing, Regulatory, Exclusivity | 60–62, 64 | ck:229–232 | equal | — |
| CVR/earnout, Antitrust | 56, 63: Y or blank | `MARKER` = {Y, Varies} | **mismatch** (the checker is wider) | fixed by S:152 |
| CVR/earnout value | 57, 251: stated amount | positive number, requires CVR = Y (ck:626–631) | implicit | **created**: Varies on the marker plus a value gives an error; the instruction must say "only with Y" |
| Antitrust prerequisite | 229: No concern, Concern or Varies | warning (ck:633) | severity differs | S1 makes it an error; the text is already mandatory |
| Stock % | 55, 249: number to one decimal, range "50–75", Part stock, Not stated, Varies | 0–100 number, `a-b` or `a–b` with a < b, `STOCK_CODES` (ck:589–619) | compatible; "one decimal" is not enforced (benign) | D16 wording only |
| Deadline outcome | 110: Enforced, Extended, Late bids accepted, Passed without action, Unclear; No deadline stated | `DEADLINE_OUTCOMES` plus special-cased "No deadline stated", paired with "none stated" (ck:1277–1334) | equal | **created**: `Extended (late bid accepted)` is an error until S1; `Late bids accepted` becomes a warning |
| Finality | 111 | `FINALITY` | equal | — |
| Initiation | 121 | `INITIATION` (prefix, case-insensitive) | equal | — |
| Exit reason | 273 (9 values) | `EXIT_REASONS` | equal [V] | — |
| Auction screen | 131 (Met, Not met or Uncertain, with a number or "count unknown") | regex (ck:1588–1605) | equal | meaning changes (D7); format unchanged |
| Whole-company bids | 121 | ck:1606–1616 | equal | — |
| Inferred, Flag, Round, Count, Quote | 67, 70, 52, 65, 69 | ck:943–1013 and 802–843 | equal | `exit.inferred_reason` (ck:924–932) gives false warnings under field-level Inferred and the F.3 addition (S1 lists it) |
| Round opened first | not stated | `round.opening_order` (ck:1171–1179) | **mismatch**: the checker enforces an unstated rule | fixed by S:240 |
| Other-scope price blanks | not stated | not checked | — | **created** (D18); S1 item 2 |

**Cockpit choices** (`workspace.py:349–357`, derived from checker constants) [V]:
- The "Deadline outcome" choices omit `No deadline stated`, which the draft allows. This is a mismatch today.
- "All cash" is offered whatever the schema (S2 already lists this).

## 5. Hygiene

- **Deal names:** none [V]. I searched for all 13 project deal names and the adviser and bidder names used in the spec. "Party A", "Sponsor 2" and "Unnamed financial bidder 1" (141) are generic.
- **Deal-derived figures:**
  - 247, "Ref: $12.10 close 08/08/2014; 49% premium", is Penford [V] (`raw_filing/penford_2014-12-29_DEFM14A.htm`: "Based on the $12.10 per share closing price … on August 8, 2014"; $18.00 / $12.10 = 1.488). It comes unchanged from v1.13.2 (frozen line 230). Replace it with neutral numbers.
  - 249, "50–75", is attributed to Pepco (a held-out deal) at TAXONOMY_DRAFT5:28 [V], but it is a bare format example [I]. The risk is low.
- **Header and version:** 3 → "**Revision of <date>, v1.14 (candidate).**". Line 4's research credit is unchanged from v1.13.2 and fine. `CHECKER_REVISION` (ck:40), the ck:73 comment and `_dev/tools/README.md:19` say "v1.14 (draft)"; this is S1's concern, not the instruction's.
- **Alex-facing, pilot or meta text:** none in the draft beyond line 4 [V]. Spec text that must not be copied:
  - S:245 "This follows Alex's convention";
  - S:240 "This fixes the recurring `round.opening_order` error";
  - S:290 "remain deferred";
  - D18's "applies to v1.14 only";
  - the §4 table caption ("the instruction and the reviewers must agree on");
  - **every decision ID from §1**: (D3), (D4), (D5), (D7), (D10), (D14)–(D18), "follow D17", "Varies follows D16 and the D1 sentence in §3". D3–D5 would resolve to the instruction's Rounds, Questions and Deal facts sections.
  - "H1–H3" are new instruction labels and fine.

## 6. Missing changes (implied by D1–D21, not listed in §3 or §4)

| D | Needed change | Draft line |
|---|---|---|
| D18 | Re-anchor "on those rows"; add the Other-scope exception to E13 price cells and the CVR value; tighten E1 | 55–64; 245, 247, 251; 129 |
| D16 | Partial reporting for Stock % Varies; CVR value only with Y | 249; 57, 251 |
| D10 | Rewrite the inferred Did not submit trigger and example; delete "not necessarily permanent"; name where a continuing bidder's missed submission is recorded | 264; 257; 110 or 202 |
| D7 | Scope E4 live units, the E5 closure Count and Bids received to the whole company; cover Withdrew for a switch; say how partial-only participation closes; place "unresolved scope" | 153, 163, 112; 256; 260; 129 |
| D7 | Scope the inferred-exit transitions to whole-company participants | 262–269 |
| D15 | Exclusivity changed label exception; the "stops when refused" clause; a request inside the bid letter | 88; 230 |
| D1 (express incorporation) | Remove the Bid reaffirmed state carry | 210 |
| D13 | Say which row's Note holds the target's termination fee; add reverse fee to the Note list | 208 (new); 68 |
| D5 | Subordinate the whole Contingent list, not only its last sentence | 227 |
| D14 | Align Light's "expedited" with H2's defeat | 237 |
| D3 | A boundary between Concern ("doubt about closing") and an H3 obstacle | 228, 238 |
| D8 | D8 cites "explicit final solicitation" as part of Astra's E6, but neither S:220–234 nor ASTRA:188–198 contains such a rule. Nothing to implement, or a gap. | 171, 177 |
| D8 | Round 1's lead sentence; decision date against outreach date | 173; 198 |
| D12 | No change (F kept) [V] | 277–279 |
| D2, D6, D19–D21 | No instruction change; line 40 stays "exactly four sheets" (D20) | — |

## 7. Errors in V114_SPEC §2–§4 and §9.1

1. **S:152 (D1 items 11 and 18).** "The draft text does not say this yet" is true of 56 and 63 [V]. But the sentence S:152 asks A1 to add is half present at 232 ("A Y on a cohort row means every member carries it"); only "if only some do, Varies" is new. 232's "In every column … Varies" arguably already reaches Antitrust, though not CVR (an E13 column). The cited source is itself inconsistent: TAXONOMY_DRAFT5 §3.2 (line 47) allows Varies, but its column tables say "`Y` or blank" (lines 29, 39).
2. **S:151.** It omits the "on those rows" anchor (Headline 1).
3. **S:259.** The quotation "copy the earlier row's values ('Terms: as #n')" is a paraphrase; 224 reads "then copy the earlier row's values and write “Terms: as #n” in the Note". It also leaves 210 (the §3.3(a) carry) unnamed, although S:95 says express incorporation replaces it.
4. **S:258.** "One offer communication is one row" is unqualified and contradicts retained text at 208; Astra's source said "normally" (ASTRA:170).
5. **S:269.** "Keep: a letter alone …" labels new text as kept. 220 lists the filing's words, a range, "an exclusivity request" and lateness, but not "a letter alone".
6. **S:146 and S:148** present existing text (35) and a non-issue (no checkpoint is promised) as changes.
7. **S:213** introduces a rule that contradicts 160(b) without naming it.
8. **S:325** amends only the last sentence of Financing; the Contingent definition list (227) also needs the precedence.
9. **S:310 against S:319 (D6)** leaves "expedited" (237) inconsistent with H2's defeat.
10. **S:182's "usually Withdrew"** conflicts with Withdrew's definition (256); nothing in §3 widens it.
11. **§9.1 "names no deal (check with grep)"**: a name grep misses 247's Penford figures.
12. **§9.1 "Every Heavy example names H1, H2 or H3"**: 220 is a Heavy example, and §3 and §4 never mention it.
13. **§9.1 "D18's reach D1 and F.4"** also needs E13 (245, 247, 251) and E1 (129). **"D7's … E3, E14 and F.1"** also needs E4 (153), E5 (163), D3 (112) and E14 (256, 260, 262–269). **"D10's reach D2 and E14"** must include 264 specifically.
14. **D8 (S:77)** cites an "explicit final solicitation" rule that neither §3 E6 nor Astra's §5 E6 contains.
15. **S:127** drops the header's bold and final period. This is trivial, but give the exact form.
16. Verified correct: §2's "four edits"; the S:222 and S:229 quotations (173, 171); S:160's "still being received, not admitted" (108); the S:329 quotation (230); the S:325 quotation (227); S:304's order (234); S:311's Unclear clause (239); F.4's first sentence (286); the D1 item numbers 8, 9, 11, 12, 18 and 22 (53, 54, 56, 57, 63, 67). The draft contains no in-text references to D1 item numbers [V].
17. Incidental, outside the requested sections: in S:457, `check_lean.py:922-930` is actually ck:924–932. `:633`, `:1526-1538`, `test_check_lean.py:510`, `workspace.py:349-357` and `:497` are correct [V].
