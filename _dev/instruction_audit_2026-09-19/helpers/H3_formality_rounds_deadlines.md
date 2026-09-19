# H3 — Bids, formality, conditionality, prices, rounds, processes, deadlines

Audit of `SEC_Deal_Ledger_Extraction_Instruction_v2.md` §§4, 6.2–6.3, 8.3, 9.1–9.4, 11.3–11.5, 12, 13 against Alex's documents.
Sources: `alex_collection_instructions.txt` (CI §n), `alex_notes.txt` (VN = voice note, deal + item; SUM = "Alex's summary" items A–M), `alex_hand_collected_9deals.txt` (HC + Excel line), the 12 workbooks (`extraction/*.xlsx`, read-only), Pro's register (85 rows, not 83).

## Index

| # | Topic | Dir | Matters | Conf |
|---|---|---|---|---|
| F1 | Markup ⇒ Formal labels Providence G&W 7/21 and Party D Formal; Alex's sheet says Informal | F/B | High | High |
| F2 | Alex's legacy `bid_type` appears conditionality-contaminated; §9.2 is documentation-only | F | High | Med |
| F3 | Issues-list default (Party E) reproduces Alex's label exactly | E | Med | High |
| F4 | "Any range is informal" (CI 3.5) vs §9.2 "A final range … can be Formal"; Alex does both | F | Med | High |
| F5 | §9.1 + §12-C forbid the Providence Aug 4 / Penford Oct 14 formal-confirmation row Alex wants | A | High | High |
| F6 | Conditions level: **None 0/174, Heavy 129/174** — flag has almost no variation | A/D | High | High |
| F7 | §9.3 measures transaction readiness; Alex's flag measures bidder-imposed conditions | B/F | High | Med |
| F8 | Alex wants absence-of-financing recorded; coarse level cannot carry it (PS-DS-02) | C | Med | Med |
| F9 | CVR/earnout: Alex codes all_cash = 1; §9.4 forces "Not stated" | A | Med | High |
| F10 | §6.3's negative list denies a round to an announced final/best-and-final solicitation (Mac-Gray 9/11) | B | High | High |
| F11 | PetSmart R1 start: Alex Oct 3, models Aug 13/19; Alex's own SUM-A rule also says mid-Aug | F/A | Med | High |
| F12 | Alex's "Final Round (Inf) Ann" conflates round launch and deadline communication | F | Med | High |
| F13 | §6.3 finality vocabulary matches VN Providence 12 but is delivered only as Summary prose | C/D | Med | High |
| F14 | Deadline set / revised / due separation = exactly VN Providence 7 and PetSmart 6 | E | High | High |
| F15 | "Enforced requires positive support" makes the variable near-uncodeable; no value for STEC soft deadline | A/C | High | High |
| F16 | PetSmart Dec 10→12: Alex "Final Round Ext"; models new Deadline set, treatment Enforced/Unclear | C/F | High | High |
| F17 | Deadline treatment has no structured ledger field | C/D | Med | High |
| F18 | Group envelope X–Y: exact match | E | Med | High |
| F19 | "At least $80": §9.4 blanks both price cells; Alex records "80-" as a floor | A/B | Med | Med |
| F20 | EV→per-share conversion banned from price cells; Alex does the calculation | A | Med | High |
| F21 | Partial bids: §4 records + flags where CI 3.5 says don't record — better, and satisfies SUM-L/M | E | Med | High |
| F22 | Dual proposals: separate rows ✓, but no rule for which is the comparable bid | C | Low | High |
| F23 | §6.2 processes ≈ Synacor 1 / STEC 1 verbatim; participant continuity not named | E/C | Med | High |
| F24 | Formality/Conditions demanded on Offer update rows Alex does not collect | D | Low | High |
| F25 | Bid reversion and IOI=one-Bid: direct answers to VN Meredith 8 / SUM-K | E | Med | High |

---

### F1 — The markup test labels two Providence bids Formal that Alex's own sheet calls Informal (F/B, High, High)

Instruction §9.2: "Strong formal signals are: 1. **Bidder-returned acquisition agreement markups**, a full proposed agreement, or relevant voting/transaction-document markups showing engagement with definitive terms."
Filing (providence bg, p.29): "Party B, G&W and another bidder ("Party D") **also provided mark-ups of the draft merger agreement and voting agreement**."
Alex CI 3.5: "Record a formal bid if the bidder also submits/returns a draft or the marked-up copy of a merger agreement." — i.e. the instruction copies Alex's written rule.
Alex HC 6035 (Party B $24, 07/20): `Formal`; HC 6041 (G&W $21.15, 07/21): **`Informal`**; HC 6037 (Party D $21, 07/20): **`Informal`**; HC 6044 (G&W $22.15, 07/26): `Formal`.
Workbooks: all four models code G&W 7/21 **Formal** and Party D **Formal** (ds R029/R033, glm R031/R034, opus R032/R036, sol R029/R031). Pro flagged none of these — it treats them as correct.
So the instruction and Alex's *written* rule agree, and both disagree with Alex's *data* on 2 of 6 late-July bids. Alex himself flags the doubt on the same block of rows (HC 6035 comments_3: "expedited DD; **what is the threshold for "formal"?**").
**Fix / question for Alex:** "Your CI says a returned markup makes a bid formal, but G&W's 7/21 LOI and Party D's LOI (both with markups, per p.29) are Informal in your sheet while Party B is Formal. Which is the rule?" Until answered, keep §9.2 as written and make every markup-based Formal a review item (§11.5 already does).

### F2 — Alex's legacy label looks conditionality-adjusted; §9.2 is deliberately documentation-only (F, High, Med)

Instruction §9.2: "**Formality** is an analytical documentation/solicitation assessment… Heavy conditions do not change that label." VN Providence 10 wants exactly that separation ("even though the offer seems formal because it comes in with all the markups… we can look at conditionality, and THEN make a decision whether to treat this bid as formal or informal").
But his hand-collected labels track the diligence/financing burden, not the documents. Providence late July: B "expedited diligence review" → Formal; G&W "three-week exclusive diligence" → Informal; D "four-week diligence" → Informal; E 60-day → Informal; C 30-day → Informal; F 30-day → Informal (HC 6035–6041, comments_3 column). Saks HC 7009 Hudson's Bay $15.25 `Formal` "formal, with committed debt and equity financing" vs HC 7010 Sponsor A/E $14.5–15.5 `Informal` "Several weeks of DD required, no availability of financing" — same final round, same day, split by conditions. STEC HC 7164 WDC $9.15 `Formal` (VN STEC 6: "This offer has a markup. It has no conditions").
Counter-example: Mac-Gray HC 6954 Party B $21.50 `Formal` with "No firm financing commitment" — so the pattern is not a rule, and the G&W 7/21→7/26 flip has no stated basis.
**Matters because** if v2 output is pooled with the legacy `bid_type` column the two vintages measure different constructs (documentation vs documentation-net-of-conditions), which is precisely the robustness exercise Alex wants to run *ex post*.
**Question for Alex:** "Does the legacy bid_type already fold conditionality in? If so, should new Formal be documentation-only (as §9.2), with the legacy-style label reconstructed at estimation from Formality × Conditions level?"

### F3 — Issues-list default matches Alex's actual label (E, Med, High)

§9.2: "**Working default for an issues list:** comments or a summary of issues are not automatically a returned agreement markup. Without another formal signal, classify Informal."
Filing p.29: "One bidder ("Party E") provided a summary of material issues and proposed changes to the merger agreement". Alex HC 6036: Party E `Informal`. All four models: Informal. Clean match; keep.

### F4 — The range rule (E/F, Med, High)

Alex CI 3.5: "any bid expressed as a range is also to be classified as informal bid."
Alex VN Mac-Gray 6: "party A makes an indication of interest between $18 and $19/share. And it says that this is their best and final offer… This bid is currently recorded as formal. **And I think I want to keep it this way.**"
§9.2 sides with the voice note: "A final range or non-binding LOI can be Formal", plus signal 2 "A response on the requested basis to a genuine final, binding or best-and-final solicitation."
All four models code Mac-Gray Party A 09/18 `Bid reaffirmed / Formal`; Alex HC 6953 also `Formal`. But Saks HC 7010 keeps a final-round range Informal. So the legacy data contains both behaviours.
**Fix:** state in §9.2 that CI 3.5's range rule is superseded for final-round responses (it already is, implicitly) and add a one-line note that ranges are retained in Price low/high so the "range ⇒ informal" recode remains available at estimation.

### F5 — The formal-confirmation row Alex explicitly asks for is forbidden (A, High, High)

Alex VN Providence 14: "what used to be informal or a "formal conditional" offer becomes properly formal… **In the case of Providence, an additional row on August 4 stating that party B has submitted a formal unconditional offer for $24.00/share should be included.**" His sheet has it: HC 6054 `Party B | 24 | 24-24 | Formal | date_precise 07/20/2016 | date_rough 08/04/2016 | comments "Confirm 7/20/2016 bid after DD"`. Penford VN 7: "**We know that a deal cannot finish without a formal offer**… on October 14, Ingredion has been contacted to confirm the proposed price of $19/share and to finalize the draft merger agreement… The AI did not record $19/share on October 14 as a formal offer, but I think it should" (HC 6481 records it, Formal).
Instruction §9.1: "A further draft is not automatically a bid or reduced conditionality… Never fabricate a "missing formal offer"." §12-C is built on this very event: "Providence's Party B returned a further merger-agreement draft on August 4… **Do not create a new $24 price quotation** or infer Light/None from the draft alone."
Consequence in the 12 workbooks: all four models emit an unpriced `Offer update / Formal / Heavy` on 08/04 (ds #45, glm #51, opus #57, sol #46). Nobody produced Alex's row; nobody was penalised for not producing it.
Note the instruction's own tension: §9.2 signal 3 is "**An actual price confirmation while a definitive agreement is being finalized with the bidder**" — a signal that presupposes a row §9.1 forbids creating.
**Smallest fix:** allow, as a flagged convention, a `Bid reaffirmed` row with Formality = Formal, Price origin = **Carried forward** (§9.4 already provides this), Date basis = Inferred day, when the filing shows the earlier price treated as operative *and* definitive-agreement finalisation with that bidder. That gives Alex the row without asserting a new stated price, and Count rules (§7.2) keep it out of submission tallies.
**Quirk Austin should know:** the convention makes "the winner made a formal offer" true by construction in every completed deal, so formality of the last bid carries no information about the winner; and it dates an event by inference on a day with no reported bidder communication. Also ask what `bid_note = "Executed"` on HC 6054 means — it is unexplained and may be an artefact.

### F6 — The conditionality flag has almost no variation (A/D, High, High)

§9.3: "**None and Light require affirmative support, not silence or the mere passage of time.**"
Measured over all 12 workbooks (Deal ledger, all classified rows): **Heavy 129, Light 32, Insufficient evidence 11, Varies 2, None 0** (n = 174). `None` was never used by any model on any deal; Heavy is 74%. Formality never used Insufficient evidence or Varies at all (0/174).
Alex VN Providence 10 wants the flag to do work: "some kind of a flag that says, this deal has heavy conditionality or light conditionality or non conditionality at all… we can look at conditionality, and THEN make a decision whether to treat this bid as formal or informal." A flag that is Heavy for three quarters of bids — including every pre-signing final bid — demotes essentially all formal bids and cannot support that reinterpretation.
**Fix:** anchor the levels to the *bidder's stated conditions* (F7), and allow None where the filing states committed financing and no outstanding diligence request, rather than requiring evidence of overall readiness to sign.

### F7 — The two documents mean different things by "conditions" (B/F, High, Med)

§9.3: "**Conditions level** measures unresolved material diligence, funding, commercial or completion/repricing exposure at the time of the offer."
Alex VN Mac-Gray 5: "CSC/Pamplona submitting an indication of interest, and they claim that **financing is 100% guaranteed**… I would rather record the lack of financing guarantees than their presence… Party B therefore gets an additional row saying that they don't have financing." VN Mac-Gray 7: exclusivity conditions recorded "the same way we record… financing or due diligence conditionalities."
i.e. Alex's flag = conditions the *bidder attaches* (financing / diligence period / exclusivity). §9.3's flag = the state of the *transaction*. Because any pre-signing bid has unfinished diligence, §9.3 collapses to Heavy (F6).
Evidence in Pro's register: **MG-GLM-03** (Major) — GLM coded CSC/Pamplona 09/18 Light; Pro: "do not infer Light solely from the capital commitment", because "subsequent full diligence and material documentation/liability negotiations" followed. That is a correct application of §9.3 and the opposite of Alex's reading ("financing is 100% guaranteed" ⇒ unconditional on financing). **PS-GLM-07** (Major) — Bidder 2's 12/10 final bid Light: Pro requires an absolute readiness scale; Alex's scale would read "final bid letter + revised documents + financing commitments" as light.
**Fix is definitional, not a reversal of Pro:** rename/redefine the column as *bidder-imposed conditionality* (None / Light / Heavy over financing, diligence, exclusivity, repricing), and keep "transaction readiness" out of it. Then MG-GLM-03 and PS-GLM-07 become acceptable calls and the Heavy monoculture breaks.

### F8 — Recording the *absence* of financing (C, Med, Med)

Alex VN Mac-Gray 5: "I would rather record the lack of financing guarantees than their presence. Their presence keeps the informal bid informal and the formal bid formal. But their lack may prompt us to drop the formal bid to informal."
§9.3 supports this in prose — "Distinguish committed funding, represented availability, **explicit absence of commitment** and silence" — but only in Terms or outcome; the structured flag cannot express "financing not evidenced".
Pro **PS-DS-02** (Major): DS wrote "no financing commitment documents provided" for Bidder 2 on 12/06 where the filing only says the Buyer Group provided its documents. Pro is right that this is an omission, not a negative fact — Alex's own Mac-Gray case rests on an *explicit* statement ("no firm financing commitment", HC 6947/6949/6950). Keep Pro's correction, but add a structured marker (e.g. Terms prefix "Financing: committed / represented / explicitly absent / not evidenced") so the distinction survives into the dataset rather than being flattened into "Insufficient evidence".

### F9 — CVR/earnout and All cash (A, Med, High)

Alex VN Kraton 5: "when a bidder… submits a bid with an earnout, this is not a mixed offer. This still seems to me like a cash offer with an extra contingent payment". His data follows: HC 6041 G&W $21.15 = "20.02 cash + 1.13 CVR", `all_cash = 1`; HC 6044 $22.15 with CVR, `all_cash = 1`.
§9.4: "Cash plus an expressly cash-settled earnout or CVR can be Yes; **the term "CVR" alone does not establish settlement**", reinforced by §12-D. All four models therefore set All cash = **Not stated** for G&W's 7/21 and 7/26 LOIs.
Direction A (stricter than Alex). Materially this changes an `all_cash` dummy from 1 to missing on a bid Alex has already coded 1. Alex's Mac-Gray options case (HC 6954 `all_cash = 0`) agrees with the instruction, so only the CVR branch is in dispute.
**Question for Alex:** "Default a CVR with no stated settlement form to all-cash = 1 (your Providence coding) or to missing (v2)?"

### F10 — §6.3 gives no round trigger for an announced final solicitation to unchanged participants (B, High, High)

Filing (mac-gray bg): "the Special Committee instructed BofA Merrill Lynch to call each of Party A, Party B, Party C and CSC/Pamplona to **request final indications of interest by September 18, 2013**… representatives of BofA Merrill Lynch called each… on September 11, 2013".
Alex HC 6951: 09/11 `Final Round Ann`; HC 6956: 09/18 `Final Round`. CI 3.5 makes this the formality trigger: "Record a formal bid if the company announced a final round of bidding that only a subset of bidders is invited to."
§6.3: "Another bid, a board meeting, a passing or revised deadline, bidder-specific extra time, or **another price-improvement request to the same finalists does not by itself create a round**… Prefer the smallest round map." Sept 11 is precisely a price-improvement request to the same four finalists.
Outcome: ds, opus, sol opened R3 on 09/11 (matching Alex); **glm did not** — it left the 09/18 final bids in R2 and opened R3 at the 09/21 exclusivity, i.e. the map Alex's rule forbids twice over. Pro's register contains no finding on this; the only Mac-Gray round finding is **MG-SOL-06** ("Interpretive"), about Sol's extra exclusivity round. So the single round-map error that matters most to Alex went unscored.
**Fix:** add to §6.3's positive list: "a target-communicated final, binding or best-and-final solicitation opens a new round even when the participant set is unchanged" — this also aligns §6.3 with §9.2 signal 2, which already treats that solicitation as a state change.

### F11 — PetSmart round 1 start (F/A, Med, High)

Alex VN PetSmart 1: "if there is also a meeting, let's say, that happens on October 3, and from the context, it is clear that the target will start contacting bidders after that meeting… such a meeting would also indicate that a new round or, in this case, **round one of bidding starts on October 3**."
Alex SUM-A, same document: "if there is no officially stated starting date of round 1 in the background, we should assume that this round starts **when the target's investment bank first starts contacting bidders**."
Filing: the Oct 3 board meeting received "an update on communications with the 27 potentially interested parties… that had occurred **since the August 13 board meeting**" — so first contact is mid-August, and SUM-A points to August, not October 3.
§6.3: "Round 1 starts at an established operative launch; otherwise use actual outreach launching solicitation… A vague earlier authorization is insufficient." Models: ds R1 = 08/13, glm R1 = 08/13, opus R1 = 08/19 ("inferred operative"), sol R1 = "First week of October 2014". Only Sol lands near Alex's stated answer, and for a different reason (NDAs + diligence start).
This is an Alex-internal conflict (F) more than an instruction defect; the instruction is faithful to SUM-A. **Question for Alex:** "Does round 1 start at first outreach (SUM-A) or at the board meeting that reviews interest and precedes the NDA wave (VN PetSmart 1)? PetSmart splits these by seven weeks."

### F12 — Vocabulary mapping: Alex's "Final Round … Ann" is not a round-start marker (F, Med, High)

CI 3.7 defines only: "Final Round Ann" (announcement of the final round), "Final Round" (the deadline to submit bids in the final round), plus Inf and Ext variants. There is no generic round-open label and no round number, so a three-or-more-round process cannot be expressed: Mac-Gray HC uses `Final Round Inf Ann` 06/24 (a committee launch), `Final Round Inf Ext Ann` 07/25 (which VN Mac-Gray 3 calls "round two of informal bidding"), `Final Round Ann` 09/11. Providence HC 6032 puts `Final Round Inf Ann` at 06/15 (the mid-June LOI instruction = a *deadline communication*), while VN Providence 12 / SUM-A would start the round at the 06/01 committee decision to advance seven bidders.
§6.3 + §8.3 separate the two ("A **Round opened** row can carry a deadline set in the same instruction, without another redundant Deadline set row") and number rounds — richer than the legacy vocabulary and consistent with VN Kraton 3 ("the formal round of bidding… is gonna be round three").
**Consequence for merging:** legacy rows cannot be mapped 1:1 to v2 rounds; `Final Round Inf Ann` maps sometimes to Round opened, sometimes to Deadline set. Worth a written crosswalk before any pooling. For Providence R2 specifically the choice (06/01 vs mid-June) is immaterial — no bid falls in between — and models split (glm 06/01; ds/sol mid-June; opus "05/23 or 06/01").

### F13 — Finality vocabulary exists but arrives as prose (C/D, Med, High)

§6.3: "Distinguish **announced as final**, **inferred final negotiation**, and merely **last observed**." This answers VN Providence 12 ("how do we learn if a bidding round is final or not? Or viewed as final in the moment?… For Providence, this happened after round two (which was announced) and during round three (which was not announced)").
Delivery is inconsistent: grepping the 12 dumps, the three terms appear 0 times in ds_providence, 3 times in sol_providence, 1 in sol_mac-gray, none in sol_petsmart's deadline map; opus uses them most. There is no ledger field for it, so the flag Alex wants per round lives in variable-quality Summary sentences.
**Fix:** put finality on the `Round opened` row itself (one of the three values in Terms or outcome, first token), which costs nothing and makes it extractable.

### F14 — Deadline set / revised / due: a clean match (E, High, High)

VN Providence 7: "the AI seems to be having difficulties distinguishing between the date on which a round deadline has been set and the date on which it has expired. Those are two different dates." VN PetSmart 6: "when round two was announced, the deadline was set at December 10, on December 10, this deadline has changed to December 12, and this is a separate row… it costs us very little to collect these deadline revisions."
§8.3: "**Deadline set**… **Deadline revised**: when an existing due date was changed. Preserve old and new due dates… **Deadline**: the scheduled due date itself… Preserve every stated deadline version."
All four workbooks produce the full Providence chain (set 05/10 → revised 05/19 → due 05/19) and the PetSmart chain (set 12/05 → revised 12/10), including the 12/05 original that Alex's own sheet omits (HC has no Dec 5 row). This is the instruction doing better than the legacy data on something Alex asked for. Keep unchanged.

### F15 — "Enforced" is set so high the variable stops discriminating, and Alex's soft-deadline state has no value (A/C, High, High)

§8.3: "For each relevant deadline, the Summary map states **Enforced**, **Extended**, **Late bids accepted**, **Unclear**, or **No deadline stated**… **Enforced requires positive support for an actual cutoff, not merely absence of disclosed later bids.**"
Alex VN STEC 5: "a deadline for round one… has been announced as May 3, and then some bids came by that deadline, but it doesn't look like the target has done anything decisive on this day or following this day. And the bidders continued making offers without an announcement of the next round. So we have the case of **soft deadlines**… I am wondering if it will be useful for us to record when round deadlines have been enforced and when they haven't been. I feel like this is something that is **critical for the analysis of sale processes and their optimality**." SUM-B: "any bidding round extension **OR the lack thereof** following a stated bidding round deadline should be flagged."
Two problems:
1. Since filings essentially never report a rejected late bid, positive support is unobtainable, so the honest value is always Unclear. Pro enforced this in **MG-DS-03**, **MG-GLM-01** ("timeliness of observed submissions does not demonstrate rejection of late submissions") and **PS-GLM-06**. Observed split on Mac-Gray 09/18: ds "enforced", glm "Enforced reading", opus "Treatment: unclear rather than enforced", sol "Party C did not submit or reaffirm" (unlabelled). On PetSmart 12/10: glm "Enforced", ds "Unclear", opus "unclear rather than enforced".
2. No value expresses STEC's soft deadline — a due date that passes with **no decisive target action and no extension while bidding continues**. "Unclear" (evidence problem) and "Late bids accepted" (a different fact) both mis-describe it.
**Fix:** redefine **Enforced** as "the due date passed and the target acted on the bids received without extending it or accepting a later submission" (observable), and add **Passed without action** for the STEC case. Then Mac-Gray 09/18 = Enforced (bids reviewed 09/19, selection 09/21, no extension) — which is what Alex's data implies — and STEC round 1 = Passed without action.
**What Alex would code on the two cases asked:** Mac-Gray 09/18 → deadline held, no extension (his HC 6956 `Final Round` on 09/18, with no Ext row) ⇒ Enforced. PetSmart 12/10 → **extended** (F16).

### F16 — PetSmart Dec 10 → Dec 12: Alex codes an extension, the instruction produces a new deadline (C/F, High, High)

Filing: "the ad hoc committee instructed J.P. Morgan to inform each bidder that it would need to increase its bid, and to instruct the bidders to **submit improved bids on December 12, 2014**."
Alex VN PetSmart 6: "the final round, round two, **ended up being extended by two days**. The original deadline was December 10, the new deadline became December 12. This doesn't look like a new round of bidding, just a continuation of round two." His sheet: HC 6453 `Final Round Ext Ann` 12/10, HC 6457 `Final Round Ext` 12/12.
Instruction: §8.3 defines Deadline revised as "when an **existing** due date was changed" and requires a Deadline row for "a due date reached while still operative" — the 12/10 date *was* reached, so all four models emit a met Deadline on 12/10 plus a fresh **Deadline set** for 12/12 (ds #43, opus #51, sol #40; glm emits a second Deadline row). §6.3 correctly keeps it inside round 2 ("another price-improvement request to the same finalists does not by itself create a round"), matching Alex.
Net: on the deadline-treatment variable, instruction-compliant output says PetSmart's final deadline was *Enforced* (glm) or *Unclear* (ds, opus) where Alex says *Extended*. §8.3 offers "Extended" as a value but never defines it for this shape.
**Question for Alex:** "Does 'extension' mean only (a) a due date moved before it arrives, or also (b) any further solicited bidding step after the announced final deadline (PetSmart 12/10→12/12; and your Providence 'July 27 is a fair assessment of the deadline')? Your codings suggest (b)."

### F17 — Deadline treatment is not a field (C/D, Med, High)

§8.3 puts treatment in "the Summary map"; §11.2's expandable fields contain "Due date | Submission due date only" and nothing for treatment. Models improvised a "Treatment:" prefix inside Terms or outcome text. For a variable Alex calls critical (VN STEC 5, SUM-B), Summary prose is the wrong home.
**Fix:** one expandable field `Deadline treatment` on Deadline / Deadline revised rows, values as in F15.

### F18/F19/F20 — Prices (E; A/B; A)

**F18 (E):** CI 3.5 "If it is only specified that six bidders made offers in the range between X and Y and there is no individual bid information for a bidder of that group record the indicated range as bid, i.e., X-Y" vs §9.4 "An envelope across several offers belongs only to its described group". All four workbooks record the nine Providence IOIs as one row, Price kind = **Group envelope**, 17.93–26.50, Count 9 — identical to HC 6029 (`9 parties | 17.93 | 17.93-26.5 | Informal`). Keep.
**F19 (A/B, Med):** §9.4: ""A range reached at least $80" constrains its upper endpoint, not its lower endpoint. **Leave both numeric price cells blank**, set Bound only". All four models did exactly that for the third PetSmart bidder. Alex HC 6428 records `80-` in the lower-upper field and VN PetSmart 3 uses it as a floor: "they will allow **the four bidders who had indicated a price or range at or above $80/share** to proceed" — which is the filing's own Nov 3 sentence. So for these four bidders the filing supplies a floor, and Pro's **PS-DS-03** (which penalises DS for calling $80 a lower bound) is a finding Alex would reject. **Fix:** allow Price low = 80 with Price kind = Bound only where a later passage restates the same indications as "at or above" a figure.
**F20 (A, Med/Low):** VN Meredith 4: "the background says that the remaining segments… will be allocated 1.975 billion of the company's net debt. And so this allows us to subtract the value of the net debt from the enterprise value of each of the offers in order to get their equity values. And then if we divide that by the number of shares outstanding… we get the price per share." §9.4: "Do not assume net debt, shares, dilution… Any optional conversion is a separately labelled calculation there [Summary], with its formula and sources, **not an invented observed per-share bid**." Defensible, but it means EV-quoted deals arrive with empty price cells. Low-cost fix: keep the cells blank but require the labelled conversion in Summary *with the same Row id*, so estimation can join it. SUM-M (flag unclear currency / non-per-share / EV bids) is already met by §9.4 and §11.5.

### F21/F22 — Scope (E; C)

CI 3.5: "Only collect bids to acquire the entire company… Don't record the information for those bids." VN Meredith 2 / SUM-L: "a deal like that, that does not have bids for the entire company, should be flagged by the AI."
§4: "Use **Other-scope bid** for segments, selected assets, minority stakes… Retain material alternatives outside core bid counts. Flag non-comparability", with §7.2 keeping the tally separate. This records what Alex discards while protecting the whole-company counts, and §11.5 requires an "Other-scope or partial-only cases" review item — better than CI 3.5 and it satisfies SUM-L. Also correct on rollover: §4 "An existing shareholder's rollover does not by itself make an otherwise whole-company offer partial" = VN PetSmart 7.
**F22 (C, Low):** VN Meredith 6 wants dual proposals as separate bids *and* a selection rule ("we should record the 2.76 billion, which gives target shareholders a better out"). §9.1 gives the rows ("Alternative structures get separate cross-referenced rows marked **one communication, one bidder**") but no guidance on which alternative is the comparable one. Add one sentence: identify the alternative the target treated as the operative proposal, or flag.

### F23 — Processes (E, with one gap) (Med, High)

VN Synacor 1: a 9-month gap between the end of C's negotiations and E's approach "indicates that these are indeed different processes", while resuming contacts 4 days after E's exclusivity lapsed with E still active "is not the start of the new process… a standard situation in which many contacts in the same process are renewed upon the expiration of exclusivity". VN STEC 1: a 3-month contact gap "clearly identifies two separate processes". "it will be useful to flag all deals in which the AI thinks there are multiple sequential processes for human review."
§6.2: "A supported abandonment followed by a fresh start, or substantial dormancy together with evidence of a renewed attempt, can establish a new process. **There is no fixed gap length.** Resuming contacts shortly after exclusivity expires, with negotiations still alive, normally remains the same process… **Explain every multi-process assessment in Questions.**" Near-verbatim agreement, including the flagging requirement; §11.3 has Process terminated / Process restarted matching CI 3.9 (Zep). Untested by these three deals (all Process 1 in all 12 workbooks).
**Gap (C, low):** Alex's test is gap **plus participant continuity** ("a long dormancy with new actors is a new process"); §6.2 never mentions participant turnover. One clause would close it.

### F24/F25 — Two smaller items

**F24 (D, Low):** §11.2 requires Formality and Conditions level on "relevant Offer update" rows. That manufactures classification work — and model disagreement — on events Alex does not collect at all: PetSmart 12/06 comments are Formal in ds/glm, Informal in opus/sol, and Pro scored the latter two as defects (**PS-OPUS-01**, **PS-SOL-02**) although Alex's sheet has no 12/06 row. Cheap fix: make formality optional on Offer update rows unless the update is the evidence for a later formal call.
**F25 (E, Med):** §9.1's Bid definition includes "reverting to an earlier offer", and "Withdrawal of a higher proposal while confirming an older one is a Bid reversion, not necessarily process withdrawal" — a direct answer to VN Meredith 8 ("the bid reverts back to 16.99. The AI does not record this bouncing back and forth"). All four models recorded Providence Party E's 08/02 reversion as a Bid (matching HC 6052). Likewise §9.1 "An IOI and its offer are one Bid; later board review is not another" answers SUM-K ("indications of interest and bids are recorded as separate rows. Why is this necessary?"), and §11.5 "Formal IOIs/LOIs, borderline formality, and **all conditionality assessments during the pilot**" is SUM-K/SUM-G verbatim. Keep all three.

---

## Answers to the seven questions

**1. Formality.** The three strong signals reproduce Alex's *written* CI 3.5 almost exactly (markup, final-round solicitation, price confirmation), and the issues-list default reproduces his Party E label. They diverge from his *data* on Providence G&W 7/21 and Party D (markups, yet Informal in HC 6041/6037) — all four models say Formal, Pro flagged nothing (F1). Mac-Gray 09/18 best-and-final range: instruction, models and HC 6953 all say Formal, against CI 3.5's "any range is informal" (F4). PetSmart 12/06 comments: instruction prefers Formal (final-solicitation response), models split, Alex has no row (F24); PetSmart 12/10 final bids Formal everywhere including HC 6447/6448 ✓. Alex's cross-document inconsistency (F1/F2/F4) implies one question: *is your legacy bid_type documentation-based or conditionality-adjusted?* — his Providence late-July split, Saks 7009/7010 and STEC 7164 point to the latter.

**2. Aug 4 / Oct 14.** §9.1 + §12-C forbid exactly the row Alex wants; no model produced it (all four: unpriced Offer update). Signal 3 in §9.2 presupposes such a record, so the instruction is internally inconsistent. It can be satisfied without fabricating a price: `Bid reaffirmed`, Formality Formal, Price origin **Carried forward**, Date basis Inferred day, Count 0, review-flagged. Penford Oct 14 probably already qualifies under §9.1's Bid reaffirmed if the filing reports Ingredion confirming (I could not read the Penford filing); the true residual case is target-side finalisation with no reported bidder communication. Quirk: it makes "the winner made a formal offer" true by construction and dates an event by inference.

**3. Conditionality.** §9.3 gives Alex the coarse flag on the bid row (VN Mac-Gray 5's preferred layout) and gets exclusivity (§9.3 "Exclusivity alone changes neither formality nor the conditions level" = VN Mac-Gray 7) and earnout components right. But it measures transaction readiness, not bidder-imposed conditions, so **None was used 0 times and Heavy 129/174 (74%)** across the 12 workbooks; Insufficient evidence 11 (10 of them PetSmart), Varies 2 (F6/F7). Pro penalised three calls Alex would plausibly accept — MG-GLM-03 and PS-GLM-07 (Light) and, more weakly, PS-DS-02 (absent financing). Pro applied §9.3 correctly; the variable needs redefining, not the review overruling.

**4. Rounds.** §6.3's substantive-transition test reproduces Alex's board/committee rule and his "naming inferred from process not banker vocabulary" (VN Kraton 3), and its negative list correctly keeps PetSmart 12/12 inside round 2. Observed maps: Providence R1 week of 03/28 (ds, glm, sol; opus 03/24), R2 06/01 (glm) or mid-June (ds, sol; opus "05/23 or 06/01"), R3 07/27 (all four) — Alex-compatible (F12). Mac-Gray R1 06/24, R2 07/25 (all four ✓ VN Mac-Gray 2/3); final round 09/11 in ds/opus/sol ✓ HC 6951, **but glm collapsed it** and Pro did not flag it — caused by §6.3's "another price-improvement request to the same finalists" (F10). PetSmart R1: Alex Oct 3, models Aug 13/19 + sol first week of Oct (F11), though Alex's own SUM-A rule points to August. Finality vocabulary exists (§6.3) and answers VN Providence 12, but is unstructured and unevenly delivered (F13). SUM-A's always-flag list is covered by §11.5's round-map item except the "board meets at/just after a deadline" trigger, which is implicit only.

**5. Deadlines.** Set vs revised vs due is exactly what Alex asked for and the models deliver it, including the Dec 5 row his own sheet lacks (F14). The weak point is treatment: "Enforced requires positive support" makes Enforced practically uncodeable (Pro: MG-DS-03, MG-GLM-01, PS-GLM-06), and there is no value for STEC's soft deadline (F15). Alex would code Mac-Gray 09/18 Enforced (deadline held, no extension) and PetSmart 12/10 Extended (HC 6453/6457) — neither is what §8.3 produces (Unclear/Enforced, plus a fresh Deadline set) (F16). The five values are the right *shape*; two need redefining, and the field must move into the ledger (F17).

**6. Prices/scope.** Group envelopes X–Y: exact match (F18). Whole-company-only + flag partial deals: §4 is better than CI 3.5 and meets SUM-L/M (F21). "At least $80": §9.4's blank-cells rule loses information Alex keeps, and its "upper endpoint only" reading is contradicted by the filing's own "at or above $80.00 per share"; Pro's PS-DS-03 is a finding Alex would reject (F19). Per-share vs EV: §9.4 blocks the net-debt conversion Alex performs (F20). Dual proposals: separate rows ✓, no comparability rule (F22). CVR ⇒ All cash "Not stated" contradicts his `all_cash = 1` coding (F9).

**7. Processes.** §6.2 matches Synacor 1 and STEC 1 almost clause for clause — no fixed gap length, dormancy plus renewed attempt, post-exclusivity resumption stays the same process — and §6.2/§11.5 require every multi-process assessment to be flagged, which is Alex's request. Only omission: participant continuity ("new actors") is not named as part of the test (F23). Untested here: all 12 workbooks are single-process.
