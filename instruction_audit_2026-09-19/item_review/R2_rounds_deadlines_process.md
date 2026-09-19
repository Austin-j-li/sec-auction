# R2 — rounds, deadlines, process: items 3, 7, 8, 10

Reviewer pass of 19 Sep 2026. Files read: `SEC_Deal_Ledger_Extraction_Instruction.md` (in full), `INSTRUCTION_CHANGELOG.md`, `QUESTIONS_evaluation.md` A4/A7, `helpers/H3_formality_rounds_deadlines.md`, Alex's voice notes (all eight deals + his own summary), his collection instructions §3.5/§3.7/§3.9, his hand-collected rows for nine deals, the three background sections, and the twelve old-instruction model dumps.

Evidence-source convention used below: **RULE** = Alex's own written rule (collection-instruction "Alex's addition", or his own summary section 2); **VN** = dictated per-deal voice note; **HC-red** = his own hand-collected row/comment; **HC-black** = an RA row he kept; **AI-sum** = the "Claude's reading" block in the notes file, which is *not* his words.

---

## Item 3 — Round-1 start (§6.3)

### (a) Current wording

> Round 1 opens when the target or its banker begins soliciting potential buyers: the first outreach wave, or the launch decision when outreach follows at once; in a bilateral case, the start of substantive sale negotiations. A sale-exploration decision or press release that defers outreach to a later date is not the opening, and a vague earlier authorization is insufficient. Inbound enquiries, earlier approaches and unsolicited proposals before the opening remain in round 0. On the round 1 `Round opened` row, state `R1 anchor:` with the event used and list the Row ids of the other candidate anchors, so that the boundary can be re-cut. Later evaluation of an unchanged early proposal is not resubmission.

### (b) Every statement Alex makes about when round 1 starts

| # | Source | Kind | What it says |
|---|---|---|---|
| 1 | Summary 2A | **RULE** (his own deliberate written summary) | "if there is no officially stated starting date of round 1 in the background, we should assume that this round starts **when the target's investment bank first starts contacting bidders**. The event of such contacts/NDAs should also be flagged." |
| 2 | VN II.2 (Mac-Gray) | dictated | "there is no clear indication that one of the bidding rounds starts, in this case round one. However, from the context, it is clear that **round one started on June 24 when the Transaction Committee met and decided to start the selling process**. And the deadline on round one is July 23." |
| 3 | VN III.1 (PetSmart) | dictated | "if there is also a meeting … that happens on October 3, and from the context, it is clear that the target will start contacting bidders after that meeting … such a meeting would also indicate that a new round or, in this case, **round one of bidding starts on October 3**." |
| 4 | VN IV.4 (Penford) | dictated | "unless the starting date is explicitly stated in the background, **round one of bidding starts at the point in time when a target starts the sale process**. So this makes some initial bids by Ingredion ($18.25-18.5, then $18.5, then $19) belong to round one." |
| 5 | AI-sum 1 and the row-level block | **not his words** | "a round starts when the target decides who advances or launches the next stage (typically a board or committee meeting and an invitation to re-bid)". Do not cite this to him as his rule. |

His hand-collected sheet has **no round-1-start marker at all**. Its round vocabulary (CI §3.7, his own addition) is only `Final Round Inf Ann` / `Final Round Inf` / `Final Round Ann` / `Final Round` / `Ext` variants — the *final* round's announcement and deadline. The only process-opening markers are `Target Sale`, `Bidder Sale`, `Target Sale Public`, `Activist Sale`:

- Providence HC 6026 `Target Sale` **03/14/2016** (the board meeting), red comment "No concrete offer from Party A and a large time gap, so perhaps this is Target Sale?" — not the week-of-28-March outreach.
- Mac-Gray HC 6931 `Bidder Sale` Party A **06/21/2013** (the unsolicited bid), preceded by HC 6928 `Target Interest` 04/08/2013 with the red comment "**Not an official sale, but T approached Party A**"; the 06/21 bid row (6932) sits *before* the 06/24 `Final Round Inf Ann` row.
- PetSmart HC 6410 `Target Sale Public` **08/13/2014**, HC 6411 `Sale Press Release` **08/19/2014**, NDAs all dated **10/07/2014**, `Final Round Inf Ann` 10/15.
- Penford: **no** `Target Sale`/`Bidder Sale` row at all; the 2007/2009 NDAs carry his red "[EVERYTHING IN GREY SHOULD NOT BE HERE]". `Final Round Ann` 10/03/2014 (= his VN IV.5 round 2).
- Kraton has no hand rows in the nine-deal file; only VN V.3 ("the second round starts on July 6").

Reading: `Target Sale` is his **initiation** marker — the instruction's `Target sale decision` label, not a round boundary. So Providence 03/14 is not strictly a counter-example to the rule; it is a different object. But it is the nearest thing to a round-1 anchor he ever wrote down for that deal, and it is the board decision, not the outreach.

### (c) Applying the current wording by hand

**Providence.** Mar 14 board "concluded … to proceed with the transaction strategy" and appointed the Transaction Committee (p.27); Mar 24 the Committee "authorized GHF to contact Party A as well as other potential buyers"; "During the week of March 28, 2016, in accordance with the Transaction Committee's directives, representatives of GHF contacted 11 potential strategic buyers … and 18 potential financial buyers."
Rule gives: week of Mar 28 (outreach wave), or Mar 24 if "outreach follows at once" is read to cover a 4–10-day lag. Mar 14 is excluded ("a vague earlier authorization is insufficient" — arguably too harsh a description of Mar 14, which is a concluded decision, but the deferral of outreach by 14 days does the work). All four old-instruction models landed here: ds/glm/sol "week of 03/28" (ds and sol with Working date 03/24), opus 03/24. **No bid moves** under any of 03/14 / 03/24 / week-of-03/28; only the Mar 22–23 management meetings with Party A and the Mar 24 committee row change round label.

**Mac-Gray.** Apr 5 board "authorized … management to work with BofA Merrill Lynch to explore transactional opportunities … including opportunities with … Party A"; Apr 8 "representatives of BofA Merrill Lynch, as instructed by the Board, telephoned a representative of Party A to discuss generally a possible business combination"; Jun 21 Party A's unsolicited $17–19; Jun 24 Special Committee "determined to approach a total of 50 parties"; "**During the next several weeks** … BofA Merrill Lynch contacted the strategic and financial parties identified at the June 24th Special Committee meeting"; Jun 28 call at which "BofA Merrill Lynch summarized the contacts they had had with certain of the potential bidders"; IOIs due Jul 23.
Rule gives Jun 24 (launch decision, outreach begun by Jun 28) = Alex's answer, **provided** Apr 8 is not read as the opening. It can be: a banker instructed by the board telephoning a potential buyer is literally "its banker begins soliciting potential buyers", and the new clause "in a bilateral case, the start of substantive sale negotiations" points the same way. "Wave" is the only word resisting it, and it is undefined. If Apr 8 opened round 1, **Party A's Jun 21 proposal moves from round 0 into round 1** — the only place in the three deals where an anchor choice moves a bid. All three models that emitted a `Round opened` row chose 06/24 under the old text, so this is a prospective risk created by the new "bilateral case" clause, not an observed one.

**PetSmart — the rule does not give Alex's Oct 3.** Aug 13 board "determined to explore strategic alternatives … and determined that at the appropriate time, which was expected to be **during the second half of September or early October**, J.P. Morgan should contact financial and strategic parties"; Aug 19 press release; then, decisively (background para 16): "During the period from the middle of August through the end of October … **J.P. Morgan was contacted by 27 potential participants** in a sale process". The 27 are **inbound**; the press release was designed to produce them ("would ensure that interested parties not contacted would become aware of the process and could contact J.P. Morgan on their own initiative"). Oct 3: board receives "an update on communications with the 27 potentially interested parties … that had occurred **since the August 13 board meeting**" and is told "approximately 15 parties had expressed interest". First week of October: NDAs with 15 financial buyers. "During October": IOI due date of Oct 30 communicated.
So **PetSmart has no reported target outreach wave**. Under the current text: Aug 13 excluded, Aug 19 excluded, and the positive test has no referent. §7.1 expressly separates contacts from NDAs, so a model cannot legitimately read the NDA wave as "the first outreach wave" — which is exactly the equation `QUESTIONS_evaluation.md` A4 relies on when it claims "window 10/03–10/07, Working date 10/03 … which is Alex's date". The changelog line "Gives Alex's Oct 3 for PetSmart" is **not true of the text as written** and must be corrected before this is shown to Alex.
Empirically the old text scattered: ds 08/13, glm 08/13, opus 08/19 ("inferred operative launch"), sol first-week-of-October NDAs. The new text removes two of those four answers and leaves the remaining choice unguided.
Is the Aug 19 press release a solicitation? Functionally yes — it is the only mechanism by which any participant entered, and every one of the 27 came through it. The instruction's exclusion is nevertheless right for the *round* variable: the press release produced two and a half months of unstructured inbound enquiries with no target requirement, no information stage and no deadline, which is not a round in the sense the estimation uses. But the reason should be the absence of an organized stage, not "it defers outreach" — in PetSmart outreach never happened at all.
Alex's Oct 3 is best defended not as "outreach followed the meeting" (the filing says the reverse) but as *the dated board meeting immediately preceding the organized stage* — the last board review before the NDA wave, the management presentations and the Oct 30 due date. VN III.1's phrasing is hypothetical ("let's say, that happens on October 3") and is primarily about narrowing the NDA window; his own sheet then dates the NDAs 10/07, not 10/03.

**Penford (from his notes only; no filing, no `Target Sale` row).** VN IV.4 puts Ingredion's $18.25–18.5 (17 Sep), $18.5 and $19 (2 Oct) in round 1 and, by omission, its $17 (6 Aug) and $18 (10 Aug) in round 0 — the target began contacting others between those dates (Party C NDA 15 Sep, Party D 23 Sep, Party A 30 Sep). This is the clearest support anywhere in his material for the instruction's round-0 treatment of pre-opening unsolicited bids, and it is the one case where an early *bid* stays in round 0 by his own reckoning. The inference rests on his omitting the August bids from the round-1 list; not independently checked.

**Kraton.** VN V.3 concerns the round-1→2 boundary (Jul 6), not the round-1 start; it confirms only that the boundary is the target's advancement decision and that the banker's vocabulary is ignored. Nothing about R1.

### (d) Ambiguities, collisions, downstream risk

1. **"when outreach follows at once" is unoperationalized.** Mac-Gray's outreach is reported as "during the next several weeks"; Providence's as "during the week of March 28". Both are *the direct execution of the decision*, but neither is "at once" on a plain reading. Without a tolerance, models will split between decision day and outreach on identical facts.
2. **No fallback for the inbound-driven deal.** PetSmart above. This shape (press release, inbound enquiries, then an NDA wave and a process letter) is common in large-cap sales; the rule must cover it or it will silently drift.
3. **Single early bilateral call.** Mac-Gray Apr 8. "Wave" and Alex's own "Not an official sale" comment resolve it, but the text should say so.
4. **Pre-round-1 inbound bids and standing proposals.** Round 0 is the right home (Penford confirms), but Mac-Gray exposes a downstream gap: Party A is a live round-1 participant whose **only bid sits in round 0**, and whose June 21 proposal is reviewed by the committee alongside the Jul 23 IOIs ("reviewed the preliminary indications of interest received from Party B, Party C and CSC/Pamplona **as well as the Party A June 21 proposal**"). §6.3's "Later evaluation of an unchanged early proposal is not resubmission" correctly suppresses a duplicate Bid row, but then neither §7.2 (Count on Bid/Bid reaffirmed) nor §10.2 (Party A did not exit) records Party A as a round-1 bidder. A naive round-1 bidder tally reads 3 where the target had 4 live proposals. This must be handled in the Summary round map via Related rows, and it is worth one explicit sentence.
5. **`R1 anchor:` reversibility.** The device is sound and cheap, and it is the single most valuable thing in this item: it makes the boundary re-cuttable without re-extraction, which is what Alex's #1 complaint actually needs. Two defects: (i) it does not say *where* in the cell it goes, while item 7's finality phrase claims "the start of Terms or outcome" on the same row — no hard collision, but say the order; (ii) listing "Row ids of the other candidate anchors" is only re-cuttable if those candidate rows exist, which for PetSmart means the Aug 13 decision, the Aug 19 press release, the inbound-contact cohort, the NDA wave and the "during October" deadline communication must all be rows. They are, under §4/§7.1/§8.3 — worth stating so the model does not drop the losing candidates.

### (e) Verdict

**KEEP WITH REWORDING.** The rule's direction (solicitation, not decision; unsolicited bids in round 0) is right and is the only reading that reconciles his written RULE with Penford. What it lacks is a tolerance for "at once", a fallback for the inbound case, and a guard on the single bilateral call. Minimal replacement for the first three sentences of that paragraph:

> Round 1 opens when the target or its banker begins soliciting potential buyers. Use, in order: the first outreach wave; or the decision that launched it, where the filing reports the outreach as that decision's direct execution beginning within about a week; or, where the filing reports no target outreach and the participants came to the target instead, the first target-organized step that admits participants to a stage — the confidentiality-agreement wave or the process letter, whichever is earlier; or, in a bilateral case, the start of substantive sale negotiations. A single exploratory approach to one party, a sale-exploration decision or press release that defers or replaces outreach, and a vague earlier authorization are not the opening. Inbound enquiries, earlier approaches and unsolicited proposals before the opening remain in round 0; where such a proposal is still standing when round 1 is evaluated, the round map and Related rows must show the bidder as a round-1 participant even though its bid row sits in round 0.

And add to the `R1 anchor:` sentence: "Place it after the finality phrase on that row, and keep every rejected candidate as its own row so the boundary can actually be moved."

Under this text: Providence → week of Mar 28 / Mar 24 (unchanged); Mac-Gray → Jun 24, with Apr 8 explicitly out; PetSmart → the first-week-of-October NDA wave, Working date Oct 3 by §8.1 rule 5 with the Oct 3 board meeting ("approximately 15 parties had expressed interest" = the 15 signers) as the lower bound, flagged as a cross-paragraph inference — Alex's date reached by an honest route; Penford → unchanged.

**Confidence: high** on the diagnosis (the PetSmart paragraph is dispositive), **medium-high** on the exact replacement wording.
**Not checked:** the Penford, Kraton, Synacor and STEC filings; whether any *other* deal type breaks the inbound fallback; whether models actually obey a four-branch ordered rule (nothing has been run on the revised instruction).

---

## Item 7 — Round finality phrase (§6.3)

### (a) Current wording

> For each round, Summary records the opening, objective, relevant participants, deadline history, contemporaneous finality, observed ending and submitting-bidder tally. Distinguish **announced as final**, **inferred final negotiation**, and merely **last observed**. State the same finality at the start of Terms or outcome on the round's `Round opened` row — `Announced as final`, `Inferred final` or `Not final` — so that it can be filtered.

### (b) Evidence

The variable is Alex's, and it is red (important and hard): VN I.12, "how do we learn if a bidding round is final or not? Or **viewed as final in the moment**? Sometimes, the background does not tell this information even if it declares the start of the new bidding round … if we are lucky then we will see the target saying, this is the final round of bidding, or that everybody must submit formal committing bids. If we are less lucky, the target can say that it is interested in completing the negotiation of the merger agreement with one of the bidders left in the process … **For Providence, this happened after round two (which was announced) and during round three (which was not announced).** … This, again, will require us scanning all paragraphs pertaining to a round of bidding for these words to assess finality of the round." That maps exactly onto Announced / Inferred / Not.

It is also **an input to his legacy formality variable**: CI §3.5 (Chicago black text, i.e. the inherited RA rule he kept) — "Record a formal bid if **the company announced a final round of bidding** that only a subset of bidders is invited to." And CI §3.7 is an entire section of his own ("Alex's addition") devoted to `Final Round Ann` / `Final Round` / `Final Round Inf Ann` / `Final Round Inf` / `Ext` — finality is a first-class object in his schema, not prose. Every one of his nine hand-collected deals carries these rows.

### (c) Applying it to the eight rounds in the three deals

| Round | Contemporaneous evidence | Value |
|---|---|---|
| Providence R1 (Mar, IOIs due May 19) | preliminary IOIs, management presentations to follow | Not final |
| Providence R2 (mid-June, LOIs due Jul 20) | non-binding LOIs with mark-ups; Alex's `Final Round Inf Ann` 06/15 | Not final |
| Providence R3 (Jul 27) | committee "should proceed with confirmatory due diligence and negotiations with G&W and Party B"; VN I.12 says the finality signal falls here and was "not announced" | **Inferred final** |
| Mac-Gray R1 (Jun 24, IOIs due Jul 23) | "preliminary indication of interest" | Not final |
| Mac-Gray R2 (Jul 25, revised proposals due Sep 9) | "revised written proposals … if such bidders wished to proceed further" | Not final |
| Mac-Gray R3 (Sep 11, due Sep 18) | letter requesting "**final indications of interest** by September 18, 2013" plus possible exclusivity | **Announced as final** |
| PetSmart R1 (Oct, IOIs due Oct 30) | "non-binding preliminary indications of interest" | Not final |
| PetSmart R2 (Nov 3) | board "determined to allow the four bidders … to proceed to the **final round** of the sale process"; bidders instructed to submit comments "together with their **final bids**". The Dec 10→12 request for improved bids does not change the value — VN III.6: "This doesn't look like a new round of bidding, just a continuation of round two" | **Announced as final** |

Eight for eight, no strain. Mac-Gray's exclusivity (Sep 24) sits inside R3 and opens no round, as §6.3 requires; PetSmart's Dec 12 extension sits inside R2. Nothing in the three deals needs a fourth value.

### (d) Defects and risk

1. **Internal inconsistency inside the same paragraph.** The Summary triple is {announced as final, inferred final negotiation, **merely last observed**}; the row triple is {Announced as final, Inferred final, **Not final**}. "State the same finality" is then impossible for the third value: a last round of an abandoned process is "merely last observed", which is not the same claim as "Not final". This will produce inconsistent workbooks. It is the one thing in the item that must change.
2. **`Inferred final` is undefined.** Nowhere does the instruction say what evidence supports it, though §6.3 already supplies the trigger one paragraph above ("moves to definitive negotiation with selected bidders").
3. **Prefix vs field.** Prefixes now compete for the start of Terms on different labels: `R1 anchor:` (Round opened, R1 only), `Treatment:` (Deadline), `Bound: ≥ X` (Bid), the Outcome-basis words (exit rows), "the precise action" (Material process update). No two collide on the same label except finality and `R1 anchor:` — fix by ordering, not by removing either. The real objection to a prefix is reliability: the twelve old-instruction dumps show models already improvising these prefixes in free text, and across them the finality words appear 7× "announced as final", 7× "inferred final", 15× "last observed" in prose, with no consistent position. Given that CI §3.5 makes round finality an input to the formality variable that will be computed across hundreds of deals, this deserves the treatment Austin already approved for `Date method` and `Outcome basis`: a controlled field *plus* the same words at the start of Terms. It costs nothing in review width — the expandable groups are collapsed, and `Due date` already sits alone in one of them, populated only on the same handful of rows.

### (e) Verdict

**KEEP WITH REWORDING** (and add the field). Replacement for the two sentences:

> Distinguish **Announced as final** (the target told the bidders this was the final, binding or best-and-final stage), **Inferred final** (no such announcement, but the target moved to definitive negotiation with selected bidders or stated an intention to conclude an agreement) and **Not final** (neither, including a round for which no finality signal is found — say which in the reason). State that value in the expandable **Round finality** field and repeat it at the start of Terms or outcome on the round's `Round opened` row, before any `R1 anchor:` text, so that it can be filtered.

and in §11.2, extend the existing collapsed group to `Due date; Deadline treatment; Round finality`.

Rejected alternative: a fourth value `Unclear` / `Last observed`. It is defensible for abandoned processes, but no round in the three deals needs it, the reason cell already carries the distinction, and one more category per round is not worth it until a deal demands it. **Confidence: high** on the inconsistency fix and the definition, **medium** on field-vs-prefix (it is a judgment about export reliability, and adding two fields cuts against Alex's dislike of bloat — though both are in collapsed groups he never has to look at).
**Not checked:** how a round in a process that ends without signing (Zep process 1, Synacor's early attempts) reads under `Not final` — no such process appears in the three deals.

---

## Item 8 — `Treatment:` prefix on Deadline rows (§8.3)

### (a) Current wording

> For each relevant deadline, the Summary map states **Enforced**, **Extended**, **Late bids accepted**, **Passed without action**, **Unclear**, or **No deadline stated**, with evidence. Begin Terms or outcome on each Deadline row with the same value (`Treatment: Extended`, and so on) so that it can be filtered. Decide the treatment from what followed in the same round. **Extended:** a `Deadline revised` row moves this due date, whenever it was issued. **Late bids accepted:** the target considered a bid dated after the due date without any revision. **Enforced:** the date passed with neither of these, and the target took its next step — selection, exclusion, next round or exclusivity — on the bids in hand. **Passed without action:** the date passed with no extension and no selection step, and bidding or negotiation simply continued. **Unclear:** the filing does not say what followed. Values can combine; record both extension and later acceptance when both occurred.

(The five definitions themselves are confirmed. Under review: the `Treatment:` prefix mechanism and the combination rule.)

### (b) Evidence

The variable is Alex's and he calls it critical: VN VIII.5 (red, STEC) — "a deadline for round one, the informal round, has been announced as May 3, and then some bids came by that deadline, but it doesn't look like the target has done anything decisive … So we have the case of soft deadlines … I am wondering if it will be useful for us to record when round deadlines have been enforced and when they haven't been. I feel like this is something that is critical for the analysis of sale processes and their optimality." Summary 2B (**RULE**) — "any bidding round extension **OR the lack thereof** following a stated bidding round deadline should be flagged, and the information about extensions or the lack thereof should be recorded, as these are informative about how the target runs the sale process." VN III.6 (PetSmart) — "the final round, round two, ended up being extended by two days. The original deadline was December 10, the new deadline became December 12 … we can record deadline revisions … this can be an indication that the target is unhappy with bids and it has limited committing power". CI §3.7 gives `Final Round Ext Ann` / `Final Round Ext` their own rows.
*Note on attribution:* the frequently quoted "Providence, PetSmart — Dec 5 to 10 to 12, Mac-Gray" extension list is in the **AI-sum** block, not his words. Alex himself only ever names Dec 10→12. His hand sheet has no Dec 5 row and no Providence May 10/19 row at all.

### (c) Applying the definitions by hand

| Deadline | What followed | Treatment |
|---|---|---|
| Providence May 10 | postponed to May 19 before it arrived; no `Deadline` row (§8.3) | — (lives on `Deadline set`/`Deadline revised`) |
| Providence **May 19** | nine IOIs received "Between May 19, 2016 and June 1, 2016" (Date from = May 19 for all nine; none *known* late); committee met May 23 and Jun 1; two low bidders excluded Jun 1 | **Enforced** — but see defect 2 |
| Providence **Jul 20** | G&W's LOI dated Jul 21 considered; §12.B already calls this "late acceptance, not a fabricated formal extension"; the committee reviewed the LOIs on Jul 22 and Jul 27 and selected G&W and Party B, GHF "subsequently contacted the remaining bidders to inform them that they were no longer involved" (the filing dates no exclusion; HC 6042/6043 put the first two on 07/22) | **Late bids accepted** |
| Mac-Gray **Jul 23** | CSC/Pamplona on Jul 23; Party B and Party C on Jul 24; Party C revised Jul 25; all considered | **Late bids accepted** |
| Mac-Gray **Sep 9** | CSC/Pamplona and Party B on Sep 9; Party A and Party C on Sep 10; all considered | **Late bids accepted** |
| Mac-Gray **Sep 18** | three proposals on the date; committee Sep 19; on Sep 21 the Transaction Committee *itself called* CSC/Pamplona and obtained $21.25; exclusivity Sep 24 | **Enforced** — but only with defect 3 fixed |
| PetSmart **Oct 30** | six IOIs on the date; JPM then spoke to all parties Oct 30–Nov 2 and Bidder 2 raised $78 → $81–84; board selected four on Nov 3 | **Enforced** — but only with defect 3 fixed |
| PetSmart Dec 5 | moved to Dec 10 on Dec 4–5, before arrival; no `Deadline` row | — |
| PetSmart **Dec 10** | bids received; the ad hoc committee instructed bidders to resubmit improved bids on Dec 12 (§8.3's own post-deadline-call case) | **Extended** |
| PetSmart **Dec 12** | best-and-finals received; board Dec 13; signing | **Enforced** |

### (d) Defects

1. **Mechanism.** The twelve old-instruction dumps already show models improvising this prefix — and improvising it inconsistently: `Treatment: late submissions accepted`, `Treatment: late indications accepted`, `Treatment: late bids accepted`, `Treatment: LATE BIDS ACCEPTED`, `Treatment: Late bids accepted`, `Treatment: unclear`, `Treatment: UNCLEAR`, `Treatment: qualified`, `Treatment: Enforced reading`. Nine spellings of at most four values. A free-text prefix is empirically **not** a filterable variable. The audit helper H3 (F17) recommended a field; the instruction implemented only the prefix. For a variable Alex calls critical to the analysis, take the approved `Outcome basis` pattern: a controlled field in the collapsed group beside `Due date`, with Terms beginning with the same words.
2. **"a bid dated after the due date" is ambiguous between the honest window and the assigned Working date.** Providence's nine IOIs arrived "between May 19 and June 1" and every one takes Working date May 19 under §8.1 rule 2, so on a Working-date test nothing is late; on a Date-to test some are. The same convention that makes the ledger sortable can silently flip this variable. Discriminate explicitly on `Date from`.
3. **A target-solicited improvement from an on-time submitter is being scored as late acceptance.** PetSmart Bidder 2's Nov 2 increase came out of JPM's own post-deadline calls; Mac-Gray's Sep 21 $21.25 came when the Transaction Committee telephoned CSC/Pamplona to propose moving forward. Both are `Bid` rows dated after the due date that the target considered — literally "Late bids accepted", which would be wrong and would read, to a reviewer filtering the variable, as two targets failing to hold their own deadlines when in fact both held them and then negotiated. Alex's hand sheet backs the Enforced reading on both: Mac-Gray HC 6956 `Final Round` 09/18 with **no** `Ext` row, and he keeps Bidder 2's 11/02 revision inside the same round (HC 6435) without an `Ext` marker.
4. **The extension can disappear.** Providence's only IOI-stage extension (May 10 → May 19) is real, and Summary 2B says the extension "OR the lack thereof" must be recorded — but §8.3 gives May 10 no `Deadline` row and the literal reading of `Extended` ("a Deadline revised row moves **this** due date") does not attach to May 19 either. So no `Deadline` row in Providence carries `Extended`. One model under the old text improvised around it ("Treatment: Extended (postponed from 05/10) and late receipts accepted"). Do **not** repair this by redefining Extended to mean "this date is the product of a revision" — that would make PetSmart Dec 12 `Extended` when it is plainly Enforced. The extension belongs on the `Deadline revised` row, which is where a cross-deal filter should look; say so, so the reader is not misled by the surviving milestone row. Consequence to state in the Summary map: the two mechanisms record **different subsets** — a post-arrival extension lands on the milestone row's treatment (PetSmart Dec 10 = `Extended`) while a pre-arrival move lands only on `Deadline revised` (Providence May 10→19), so "how many targets extended a deadline" must be computed as the union of the two, not from `Deadline treatment = Extended` alone.
5. **Combination syntax undefined.** "Values can combine" but no format is given. Note also that only one pair can legitimately combine: Enforced, Passed without action and Unclear are each defined residually ("with neither of these" / "no extension and no selection step" / "does not say"), so the only real combination is Extended + Late bids accepted.

### (e) Verdict

**KEEP WITH REWORDING** (prefix retained, field added). Replace the sentence after the value list and append three clarifiers:

> State that value in the expandable **Deadline treatment** field and repeat it at the start of Terms or outcome on each `Deadline` row (`Treatment: Extended`, and so on), so that it can be filtered.

and after "Values can combine; record both extension and later acceptance when both occurred", add:

> Only Extended and Late bids accepted can combine; write them as `Treatment: Extended; Late bids accepted`. Enforced, Passed without action and Unclear are residual and never combine. A bid is late only where its `Date from` falls after the due date: a window that merely straddles the due date, and an assigned Working date, do not make a submission late. A price revision that the target itself solicited after the due date from a bidder that had already submitted on time belongs to the round's continuing negotiation and is not late acceptance. Where this due date replaced an earlier one, the extension is recorded on the `Deadline revised` row and in the Summary map; this row's treatment describes only what followed this date.

With these, the ten deadlines above resolve as in the table, and every one matches Alex's hand-collected `Ext`/no-`Ext` pattern where he recorded the deadline at all.
**Confidence: high** on defects 2, 3 and 5 (each changes a value in a real deal); **medium-high** on the field; **medium** on defect 4, where I am recommending a disclosure rather than a definition change and Alex has said nothing directly about pre-arrival moves.
**Not checked:** STEC's May 3 (`Passed without action`, his own case) against the filing — no STEC filing available; whether `No deadline stated` needs a row at all (Penford VN IV.8 suggests he would like one).

---

## Item 10 — New-process test (§6.2)

### (a) Current wording

> A process is one continuing target-sale attempt. Number processes 1, 2 and so on. A supported abandonment followed by a fresh start, or substantial dormancy together with evidence of a renewed attempt, can establish a new process. There is no fixed gap length. **A largely new set of participants after the dormancy supports a new process; the same participants resuming supports the same process.**
>
> Resuming contacts shortly after exclusivity expires, with negotiations still alive, normally remains the same process.

### (b) Evidence

VN VII.1 Synacor (red): "There is a 9 month gap between this event and the event of company E approaching the targets in July 2020. This large gap indicates that these are indeed different processes." And, on the over-segmentation: "There is only a 4 day gap … On top of that, **company E is still in the game**. This to me is not the start of the new process. This is instead a standard situation in which many contacts in the same process are renewed upon the expiration of exclusivity for one contact."
VN VIII.1 STEC: "There seems to be a gap between contacts of the target with potential acquirers from November 2012 to February 2013. This is a 3 month gap. I think this deal background clearly identifies two separate processes." **Gap only — he names no participant test.**
CI §3.9 (**RULE**, his own addition): `Terminated` = "the deal was terminated by the target due to the lack of interest [as an example, see Zep Inc in the database]"; `Restarted` = "the sale process (by the same target) was restarted later on (**it is possible that it will have an entirely different set of bidders**)". The parenthesis *permits* new bidders in a restart; it does not make them the criterion.
AI-sum 2 is where "The test is gap length plus continuity of participants" comes from — again, not his words.

### (c) The decisive counter-example: Zep, his own §3.9 example

His hand rows: `Target Sale` 01/31/2014 → 24 NDAs → **New Mountain Capital NDA 03/19/2014**, dropped 04/14/2014 → remaining bidders drop through May → **HC 6401 `Terminated` 06/26/2014** with his red comment "[THIS IS THE EXAMPLE OF THE EARLIER AUCTION THAT WAS TERMINATED! CAN USE]" → **HC 6402 `Restarted` 02/19/2015, bidder = New Mountain Capital** → NMC bids, gets exclusivity, signs.

The only participant recorded in the restarted process is **the same firm that participated in the terminated one** (CI §3.9 forces a bidder name onto a `Restarted` marker row, so this is not a claim that process 2 had no other participants — but the returning firm is unambiguously the same). Alex codes it as a new process anyway. The added clause's second half — "the same participants resuming supports the same process" — points the opposite way on his own canonical example. It is defeated in Zep by the first clause ("a supported abandonment followed by a fresh start"), so the outcome survives; but the sentence reads as a free-standing two-way test and a model that reaches it first will merge exactly the case §3.9 exists to split.

Second risk: participant continuity is the *normal* condition for a restart. A target that fails and tries again usually runs back to the same strategic universe. Making continuity affirmative evidence of one process will systematically under-segment.

Third risk, the other direction: the first half can over-segment where there was never an earlier *attempt*. Providence has Party A's Q4 2015 unpriced interest, then a gap to March 2016 and 25 new parties — "largely new set of participants after dormancy". Only "one continuing target-**sale attempt**" stops a model from calling that process 1 → process 2. Tying the test to a *prior attempt* removes the risk at no cost.

STEC is the case where the sentence could contradict him directly: his call rests on the gap alone, so if the November 2012 and February 2013 contact sets overlap, the second half argues for one process where he says two. **Not checked** — no STEC filing, and his hand sheet simply omits the November 2012 attempt (as Penford's omits the 2007/2009 NDAs, flagged "[EVERYTHING IN GREY SHOULD NOT BE HERE]"). Worth knowing: for earlier attempts he mostly *drops* rather than codes them, so the new-process test will bite less often in his own practice than the instruction implies.

### (d) Consistency with the rest of §6.2

The added sentence is partly redundant: Synacor's false split is already handled by the next sentence ("Resuming contacts shortly after exclusivity expires, with negotiations still alive, normally remains the same process"), which is closer to his reasoning ("company E is still in the game") than a participant count. What the sentence adds that is genuinely useful is the *positive* signal — new actors after a dormancy — which is the Synacor 9-month case.

### (e) Verdict

**KEEP WITH REWORDING** — make it asymmetric and subordinate. Replace the added sentence with:

> After a dormancy that follows an earlier sale attempt, a largely new set of participants supports a new process. Continuity of participants does not by itself establish one process: a restarted attempt often returns to the same buyers, and a supported abandonment followed by a fresh start is a new process even when the same bidder returns. It supports one process only together with continuing negotiations or an unresolved earlier stage.

This keeps Synacor's 9-month split and its 4-day merge, keeps STEC's 3-month split on gap grounds, leaves Zep's `Terminated` → `Restarted` pair intact, and removes the Providence over-segmentation route.
**Confidence: high** (Zep is his own designated example and it falsifies the clause as written).
**Not checked:** the Synacor and STEC filings; whether the November-2012 STEC contact set overlaps the February-2013 one; whether Alex wants ancient one-off NDAs (Penford 2007/2009) recorded as earlier processes at all — his grey marking suggests not, which is a §4 scope question rather than a §6.2 one, but it bounds how much this rule will ever be exercised.

---

## Cross-item note for whoever patches

- The changelog line for the round-1 start ("Gives Alex's Oct 3 for PetSmart; no bid changes round") is wrong on the first half as the instruction is written, and the second half is only true if Mac-Gray's April 8 call is excluded. Both need correcting before this is shown to Alex.
- Items 7 and 8 both end in the same recommendation: one controlled field each, in the collapsed group that already holds `Due date`, with the Terms prefix retained. If Austin declines the fields, the prefixes should at least be added to the §13.6 structure check so the exact strings are verified.
