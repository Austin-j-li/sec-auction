# Alex's voice notes versus the current research conventions

27 September 2026. Detailed reconciliation, not an instruction amendment or acceptance of any workbook.

## Verdict and scope

**v1.14.1 does not fully implement Alex's stated research intentions.** Several differences concern the economic object being recorded, rather than extraction accuracy: what constitutes a new stage, what makes a stage final, how a dormant process restarts, whether activist presence implies initiation, and when the human must review an apparently determinate coding. Matching the instruction can therefore produce a ledger that disagrees with Alex.

Much of the instruction does agree with him. Separate formality and conditionality, preservation of substantive bid revisions, cohort reconciliation, distinct contact/NDA events, cash earnout separation, and distinct signing/announcement events are substantial improvements. They still need filing review; agreement in the rulebook is not evidence of flawless execution.

This audit reads all 187 direct body paragraphs of the [voice document](../ref/alex_voice_notes_2026-08.docx), the complete [v1.14.1 instruction](../SEC_Deal_Ledger_Extraction_Instruction.md), the nine-page [older collection instructions](../ref/CollectionInstructions_Alex_2026.pdf), and the [current status](STATUS.md). Three independent review lanes covered rounds/processes, bid terms/review flags, and participants/prices. Selected consequential examples were checked against the recovered filing text and saved runs. This is **not** a complete row-by-row audit of every deal, a new extraction, or a live VM check.

The saved run comparisons refer to the 27 September 10:55:33 UTC snapshot (git `9b4f178:_dev/recovery/2026-09-27-cockpit/INDEX.json`). Four original deals have no v1.14.1 run in that snapshot. Existing working-copy edits and newer raw versions must not be conflated.

### Attribution and priority

- **V¶n** below means direct Word body paragraph n, counting empty paragraphs. Paragraphs 129–166 are labelled “Claude's reading.” Alex broadly endorses that summary at ¶168, but a model's detailed reconstruction is not independently established as an explicit case ruling by Alex. His own closing requirements are ¶169–187.
- The voice document's colors have meaning: black is important/easier, red important/difficult, blue potentially less important/easier, magenta potentially less important/difficult. Color informs priority; it does not cancel a request. Several intricate Meredith alternatives and adviser details are lower priority than round boundaries and mandatory review.
- **Explicit disagreement** means the sources actually give different treatments. **Added convention** means v1.14.1 makes a more specific choice than Alex's document; that alone does not make it wrong or unapproved. Some such defaults already have Austin's approval. **Implementation work** means applying an agreed principle to source evidence. **Later analysis** means the extraction can proceed without selecting an estimator interpretation.
- Alex explicitly warns that his hand-coded dates are not perfect (V¶34). A spreadsheet cell is not an unquestionable fact. Source conflicts require separating the filing's event from the research convention used to represent it.

### Decisions already made

Austin's 27 September **13:48 UTC** direction supersedes his earlier two-round Kraton answer: follow Alex's three rounds, with July 6 opening the second informal round. The exact general amendment remains to be written and approved; the published instruction still implements the conflicting interpretation.

Meredith's economic partial scope and exclusion from structural estimation are settled. Retain descriptive/reduced-form use. Company H's target-driven exit by May 16, the agreed non-submitter accounting, and commitment-only rows without invented new prices are also recorded rulings. This audit does not reopen them.

## 1. What begins a new round?

**Explicit conflict; first general convention to resolve.** Sources: V¶25–28,42–44,71–72,82,124,173; E6.

Alex treats a meaningful target-selected transition as a stage even when it remains informal. The current E6 requires a selection **and** a request for new offers, postpones an offer-less selection until a later request, and says repeated improvement requests normally continue the existing round. The difficult cases lie where selection, diligence access and a renewed request form one stage but occur on different days.

### Kraton

Alex explicitly starts round 2 on **July 6**, after four of ten NDA signers are selected to continue submitting IOIs. The later formal stage is round 3 (V¶82,173). Filing p.35 records a request for revised IOIs from A, H, Parent and I by July 19 before choosing who proceeds to the banker's “second round.” The current two-round interpretation treats this as an improvement step and loses Alex's second informal round.

The saved older working copy is not an accepted substitute: it also has three rounds, but opens them on May 24, July 20 and after August 11. Correct total, incorrect map relative to Alex. His voice notes fix July 6 and the three-round interpretation; **they do not explicitly fix round 3's opening date**. July 20 advancement, August 11 approval of transaction documents and subsequent final letters need separate source/convention review.

### Mac-Gray

Alex starts the second informal round on **July 25** and distinguishes the **August 27** deadline communication (V¶44). The new v1.14.1 run starts round 2 on August 27. Filing pp.33–35 supports the July 25 authorization of a second stage involving management access followed by revised IOIs, the August 15 follow-up, and the August 27 letter. This is a concrete disagreement about when a reported stage begins, even though both maps have three rounds.

### What we need to decide

Define whether a selected stage opens at authorization/communication of advancement, at access to its diligence, or only at its solicitation of offers. Also distinguish selection that changes who remains from a request that merely improves existing offers. A board meeting alone is not automatically a new round: Alex says relevant meetings should be flagged because they may reveal a transition.

**Recommendation for discussion:** recognize a documented selection-and-continuation stage even when its later bid deadline has not yet been communicated. Require evidence of the stage's purpose and participants; do not equate every board meeting, negotiating call or price improvement with a new round. This is proposed general wording direction, not an approved rule.

## 2. What does “final” mean, and how does it relate to Formality?

**Explicit sTec conflict plus an unresolved general definition.** Sources: V¶19–20,26–28,48,72–74,124–125; older collection PDF p.8; E6/E11.

There are at least three distinct objects: the numbered stage, whether that stage is final in the relevant process, and whether an individual proposal is Formal. Alex clearly allows a Formal proposal in a non-final stage: WDC on May 28. Conversely, the older collection document explicitly provides categories for a **final round of informal bids**, alongside final-round announcements and deadlines. “Final,” “Formal” and “last observed offer” cannot be synonyms.

### sTec

The filing calls the May 16 letters “final round process letters.” E6 accordingly labels the new run's May 16 stage Announced as final. But Alex calls it **round 2 of informal bidding** (V¶124) and explicitly says the May 28 Formal proposal is **not in the final round** (V¶125).

The filing's May 29 best-and-final request is real. Treating May 29 as round 3 is a plausible reconstruction represented in the questionnaire, **not an explicit dated ruling in Alex's own sTec voice notes**. The embedded Claude summary's reference to a third-round call should be traced to the original spreadsheet before being attributed more strongly.

My earlier recommendation of May 16 as research-final has been withdrawn. It used compliance with the current wording to override Alex's stated interpretation.

### What remains

Decide whether finality follows the target's words or a substantive change in commitment, definitive negotiation or opportunity to remain in contention. If the research needs both the announced label and substantive assessment, preserve both concepts rather than overloading one field. This is a possible schema direction, not authority to add columns now.

Resolve this general definition before assigning sTec's later final opening. Also review P&W's inferred definitive-negotiation stage and Penford's October 3 opening. Do not automatically label every bid in an inferred-final stage Formal without resolving section 8 below.

## 3. Round 1, preliminary approaches and bilateral negotiations

**Added operational defaults; one concrete saved-map disagreement.** Sources: V¶38–42,55,68–71,173; E6.

Alex's fallback is the banker's first contacts when no official opening is given. The current instruction adds a two-or-more-buyer outreach test, a seven-day backdating convention to a board launch, a first-NDA/price-negotiation rule for inbound/bilateral cases, and round 0 for earlier approaches. These are useful operational decisions but are not all directly specified by Alex.

- **PetSmart:** Alex uses October 3. The saved v1.13.2 working copy uses August 19, the announcement date. Filing p.23 records inbound contacts during August–October and October's substantive NDA process. An announcement does not by itself establish that a bidding round began. There is no v1.14.1 PetSmart run in the snapshot.
- **Penford:** Alex puts the initial Ingredion proposals into round 1 once the target starts selling; a historical stock-price reference on July 17 is interest, not a bid.
- **Datalink:** the new run starts January 28 at a price response in bilateral discussion, then opens another stage on June 6. Datalink has no section in this voice document. Neither map may be called Alex-approved on this source alone.

Work through how the same stage definition covers a marketed auction, an inbound bid followed by negotiation, and an earlier bilateral attempt that later expands. Avoid different economic definitions solely because one filing uses the word “process.”

## 4. When is there a new process rather than another round?

**Direct sTec mismatch; exact current-rule violation not established.** Sources: V¶108–110,118,186; E5.

Alex identifies two sTec processes separated by the November 2012–February 2013 gap. The v1.14.1 run records one process and no process Question. E5 requires all of: no outstanding offer/negotiation, an explicit end or at least 90 days without reported sale contact, and a fresh target step.

November 14 to February 13 is 91 days, but the filing reports undated follow-up and cancellation after November 14. Therefore November 14 is not demonstrably the last contact. It would be too strong to say that the model clearly violated E5's exact 90-day test. It **does** disagree with Alex's case interpretation.

Synacor gives two useful controls. Alex wants the October 2019–July 2020 break recognized as a new process. He rejects a new process merely because exclusivity ended October 23 and contacts resumed October 27 while Company E remained active. The new run agrees with those two points.

**Work needed:** define dormancy in a way that handles approximate contact dates and a genuine abandoned attempt, rather than making a one-day threshold decisive where the chronology is imprecise. Preserve uncertainty in the boundary. The exact 90-day conjunction is a current convention, not a number Alex prescribes in the voice notes.

## 5. The additional 30-day/expired-exclusivity round trigger

**Added convention with important dependent maps.** Sources: E6(d); V¶109 does not establish this rule.

E6(d) opens a new round when the target solicits offers after at least 30 solicitation-free days or after exclusivity ends. Alex's statement that Synacor remained in the same **process** does not decide whether it entered another **round**. No direct voice-note authority establishes either automatic trigger.

Datalink's v1.14.1 map depends on this rule for June 6 after a pause and October 1 after Insight's exclusivity. It also waits until the August 16 final letter after a July 27 selection of five participants. A stage-selection amendment could move or add the latter boundary, while a change to trigger (d) could remove other boundaries.

Austin previously approved four rounds under v1.14.1. His later Alex-alignment direction requires rechecking the general convention and its consequences. **Neither four nor the old five follows automatically from “follow Alex.”** Confirm, modify or remove this added trigger deliberately after resolving what a stage is.

## 6. Deadline records versus actual enforcement

**Definitional mismatch; some underlying events already captured.** Sources: V¶15,18,61–63,75,122–124,174; E9.

Alex wants to learn how firmly the target enforces deadlines. The current single Outcome field mixes explicit extensions, late acceptance and action on submissions. It prioritizes a later due date for any bidder, then acceptance of a late bid, then action/evaluation of submitted bids, then no action. These can describe different dimensions of the same episode.

- **sTec May 3:** Alex calls it soft because no decisive selection/exclusion follows and bidding continues until May 16. The saved run says Extended (late bid accepted). Company D's May 2 request for another week and May 10 offer support late acceptance, but that observation does not fully represent Alex's soft-deadline concept.
- **P&W:** Alex treats the July 27 committee decision as an effective round ending. The run's stated due date is July 20. A communicated bid deadline and the later date at which the target actually acts are different facts. Do not replace either with the other.
- **PetSmart:** December 10 moving to December 12 is an extension within the round, not a new round. Both Alex and the instruction agree.
- **Penford:** no invented deadline where none is given. Agreement.

**Recommendation for discussion:** preserve announced due date, communicated revision, late acceptance and actual selection/enforcement as distinguishable evidence. Decide whether the existing events/notes suffice or a separate analytical classification is needed. A mere meeting or feedback should not be called economically decisive without support. Alex requests human review of extensions **and their absence** after a due date.

## 7. Mandatory human review is a substantive missing requirement

**Direct workflow conflict; high priority.** Sources: V¶169–187; C, D1 Flag, F.

Alex requests interactive review while the process is being constructed, particularly before a wrong round map propagates across the ledger. His closing list uses “always” and “must,” while allowing some checks to be retired after demonstrated reliability. The current instruction caps ordinary Questions at five, permits them only for unresolved alternative codings, says a default is never a Question, and flags only Question-linked rows. The special process Question provides partial coverage but does not solve the general mismatch.

| Alex's requested verification | Current gap |
|---|---|
| Possible stage endings/openings and relevant deadline-adjacent selection meetings, ¶173 | A default-decided boundary need not be flagged; only certain inferred/trigger-(d) openings force a Question |
| Extensions or lack of action/extension after a due date, ¶174 | Outcomes can be coded without human review |
| Unknown winner or Formal bidder type, ¶175–176 | Search is required, but unresolved Unknown does not force a flag |
| Uncertain NDA count/type split, ¶177 | Qualified/unknown count can remain without a flag |
| Uncertain reason for exit, ¶178 | Not stated is permitted without a flag |
| Suggested conditionality verification on initial deals until reliable, ¶179 | Fields exist, but no initial verification gate; Alex phrases this as something that might make sense |
| Unclear adviser representation, ¶182 | No universal review requirement |
| Formal IOI based on markup/context, ¶183 | Alex suggests verification; classification currently proceeds automatically |
| Deals with only partial bids, ¶184 | Scope fields do not themselves create a flag |
| Ambiguous units/currency or EV/equity basis, ¶185 | Notes do not themselves create a flag |
| Multiple/uncertain processes, ¶110,186 | Recognized multiple processes get a Question; a missed candidate split can remain invisible |

A determinately applied convention can still require verification. “The instruction tells me to write Unknown” and “Alex does not need to inspect this” are different statements.

**Recommendation:** separate mandatory verification items from genuinely unresolved coding Questions. A five-question ceiling need not limit a checklist of important facts. For the initial reviewed deals, settle the process/round map early, then review conditionality and participation. Whether to pause live or deliver a staged review packet is a workflow decision; Alex's preferred interaction is real time. Do not claim the conditions for retiring these checks have been met: this audit establishes no such validation.

## 8. Bid Formality: agreed architecture, more specific unconfirmed boundaries

**Strong broad agreement; consequential added defaults.** Sources: V¶19–20,26–31,47–49,74,125; E10–E12.

Alex wants procedural Formality recorded separately from conditions. A marked-up merger/voting agreement can make a bid Formal despite heavy conditions. Mac-Gray's $18–19 final range stays Formal in the ledger. Exclusivity does not downgrade it in the ledger or estimation. Those principles are implemented and should be preserved.

E11 then makes more precise decisions that Alex does not fully specify:

1. A commitment letter can qualify as definitive-document support; an issues list cannot.
2. Every new revision, even price-only, must independently meet a Formal route. This can reset a later bid to Informal without evidence that commitment weakened.
3. An unsolicited offer within a final round does not qualify simply from being in that round.
4. A new bid in an inferred-final definitive-negotiation stage can remain Informal unless it has qualifying documents or is a same-offer reaffirmation. Alex's P&W discussion suggests bids seriously considered at that stage should be Formal, possibly with conditions.
5. Individual uncertainty does not have its own Formality=Unclear treatment; the instruction reserves that value for heterogeneous cohorts.

These are existing defaults, not proof of model error. Prioritize confirming the revision-reset rule and inferred-final treatment because they directly affect the intended formal-bid series. A procedural label should not silently become a measure of completion probability.

### The examples do not all match

| Example | Alex versus checked evidence/current treatment |
|---|---|
| P&W Party B, August 4 | V¶30 requests an additional Formal, unconditional $24 bid. The inspected filing passage reports counsel sending a revised merger draft, without restating $24 or saying diligence is complete. The v1.14.1 run has no Party B Bid that day. E2/E10 can omit an unchanged document exchange. This requires source/convention reconciliation, not automatic insertion of Alex's expected price. |
| sTec WDC, May 28 | V¶125 calls the $9.15 offer Formal with no conditions. The markup supports Formal. The new run records Formal/Unclear with diligence and financing Not stated. It matches formality but not his conditionality assessment. |
| Mac-Gray Party A, September 18 | V¶48 keeps the $18–19 range Formal. The new run does too, but records Heavy from contingent financing, with incomplete diligence separately recorded. Alex's range observation does not independently establish that diagnosis. |
| Penford Ingredion, October 14 | V¶74's Formal $19 confirmation fits the filing and current Bid reaffirmed rule. No v1.14.1 Penford run exists here, so this is rule/source agreement, not a verified new-run success. |

The August 4 case also raises which revised legal documents represent a new economic offer. “Document supplied” can be evidence of formality without every routine draft becoming a new Bid event.

## 9. Conditions: economic meaning, thresholds and evidence time

**Added specification needing targeted confirmation, not wholesale rejection.** Sources: V¶19,30,46–49,125,179; B, E10, E12.

Alex proposes None/Light/Heavy as a summary of economically relevant uncertainty and lets estimation reinterpret Formal bids. He does not supply the exact H1–H3 thresholds. The current implementation has several implications that should be discussed explicitly:

- A financing source named without a commitment is Contingent and therefore Heavy. Silence is Not stated. This measures disclosed commitment evidence, not only an expressly stated financing contingency.
- A bid stated to have no financing condition is Committed. Full sponsor/parent coverage also qualifies. Cash on hand, existing facilities or all-stock consideration becomes Not needed. These categories combine contractual conditionality and sources of funds.
- H2 requires at least two weeks tied to remaining diligence **alone**, excludes confirmatory diligence, and excludes a combined negotiation/exclusivity period. Extensive undated diligence need not produce Heavy.
- H3 covers an explicit repricing right or condition without which the bidder will not or may not proceed, except diligence, financing, exclusivity and ordinary approvals, which are handled separately.
- Regulatory Concern alone does not trigger Heavy. Complete diligence plus regulatory risk can lead to Light. Internal bidder approvals also do not trigger H3.
- None requires complete diligence and committed/not-needed financing, but only that Regulatory is not Concern. Regulatory Not stated can therefore coexist with None. **None is not a literal assertion that every possible condition has been explicitly ruled out.**
- Not begun diligence is defined by being pre-NDA, a proxy rather than an explicit observation of diligence activity. Only-documentation-remains is Incomplete but normally Light.

Part B does not mark convention-based classifications as Inferred. The pre-NDA diligence proxy and financing classifications can therefore appear without an inference flag. A reviewer must distinguish a directly reported condition from a classification obtained by applying these conventions; the current Inferred column does not make that distinction visible.

Some of these operational choices have already been approved by Austin. Their absence from the voice notes does not undo that approval. The work is to identify which describe Alex's intended economic variable, document their limits, and propose a targeted change only where the latest alignment direction requires it.

### Evidence window and forecasts

Part B permits evidence from the offer through the next bid, exclusivity change, exit or signing, including forecasts. New revisions reset most cells unless the bidder expressly says the same offer stands. Alex supports reading the full context but does not specify this exact time window/reset mechanism.

Decide whether the variable represents the condition **at submission**, the later best description of that same offer, or everything learned before the next event. An expected future diligence completion must not silently become achieved completion at the original bid date. Conversely, silence on a price revision does not economically prove that a previously reported condition disappeared. Retain source timing when assessing these cases.

### Exclusivity and contingent value

Exclusivity should remain a separate field and must not alone downgrade Formality; that is explicit Alex guidance. Required versus Requested and separate process-request events are additional mechanics. Likewise, Kraton's cash earnout stays separate from cash upfront consideration. The extension from that example to all contingent securities, maximum payouts and performance-vesting equity options is a normalization choice, not something his cash example fully decides. A Mac-Gray raw row represents contingent equity options as Stock %=0 plus a CVR/earnout value; its instrument description must remain visible if this convention is retained.

## 10. Activation, participation, non-invitation and exits

**Mostly implemented bookkeeping, with a consequential boundary question.** Sources: V¶12–16,21–24,41–45,50,60,70,72,76,83,121,177–178; E1/E3/E7/E14.

Alex says participation is constructed from source events, not separately extracted as another count. The instruction correctly does not sum contacts, NDAs and bids as if they were different people. Contact alone is not entry. Repeated NDA mentions do not duplicate participation within a continuous process; later-process entry and genuine re-entry are recorded separately. Named bidders must be reconciled with cumulative cohorts and type totals. These are implementation requirements, not fresh decisions.

### Non-invitation does not have one unambiguous meaning across the sources

E14 closes a participant as Dropped by target when not invited into the next stage, regardless of the possibility of return. Alex's Penford V¶72 says Ingredion enters the October 3 stage while earlier NDA signers are **not explicitly excluded**. That distinction may be lost under an automatic exit.

However, the older collection PDF p.8 explicitly includes DropTarget when a bidder is not invited to the final round. Thus it would be wrong to say Alex never supported invitation-based exclusion. The question is how to reconcile that generic instruction with the later Penford reading, a stage involving one selected negotiator, and the difference between actual exclusion and a filing's silence about invitations.

**Decision needed:** is non-invitation an observed exclusion, an explicit ledger inference, or insufficient evidence in some stages? Preserve the distinction between live in the whole-company contest and admitted to a particular stage. This does not reverse the settled Company H case.

### Cohort closures and valuation information

The P&W 16 non-submitters and Mac-Gray 16 unnamed financial signers have settled ledger treatment. Do not ask again merely because the estimator treatment is open. An inferred exit date can close the bookkeeping without proving voluntary withdrawal or revealing a valuation threshold.

Alex explicitly distinguishes value below market, value at/below an earlier offer and refusal to improve. E14 already preserves those categories and exact comparisons. The remaining task is to use the correct category and benchmark. A refusal to improve is not automatically an assertion that value equals the old price. Constructing numerical bounds belongs to analysis and must handle prior price ranges and contingent consideration carefully.

## 11. Initiation and activist influence

**Explicit sTec conflict; broader issue of attributing causation.** Sources: V¶38–39,118–120; D2/D5.

Alex wants sTec's activist presence recorded but explicitly does **not** think the sale was driven by activist pressure: sale was one among several suggestions. The v1.14.1 run says Activist-influenced because the December 6 event precedes round 1. D5 makes that precedence mechanically decisive, while D2 defines Activist as pressing for a sale.

Mac-Gray has a different mixed sequence: the target initially sounds out a buyer, becomes passive, and later receives unsolicited interest. Alex says it is a bit of both and asks to keep the interactions for reinterpretation. A target-led label based on the first event is reproducible, but is not the full economic judgment he expresses.

**Recommendation:** preserve the observable sequence, including activist involvement, separately from an assertion that it caused the sale. Confirm whether the headline field should mean first mover, sale initiator, or activist influence. These are different concepts. Do not infer causation solely from chronological precedence, and do not omit activist facts merely because the sale is not activist-driven.

## 12. Scope: settled Meredith decision and remaining general boundaries

**Meredith principle settled; implementation and other extensions remain.** Sources: V¶89–105,184; E1/E10/E13.

Alex explicitly excludes Meredith from structural estimation because the acquired segment has no separately observed market price. A simultaneous spin-off followed by acquisition does not create a clean unaffected market value for that segment. An earlier, independently completed spin-off can be different. Austin has reaffirmed this economic scope.

The current Meredith working copy still has 26 LMG Bid rows using provisional legal-entity scope and ten station Other-scope rows. Correct implementation means reviewing all scope-dependent fields together: event type, amounts/units, live participation, bids received, auction screen and exits/re-entry. Under current D2/E1, partial amounts belong in Notes and price/CVR-value cells stay blank. Do not blindly apply an older proposal to a changed schema, or mutate the recovered snapshot as though it were the live working copy.

Two general current extensions deserve targeted confirmation:

- A bidder that **switches** from whole-company to partial is recorded as Withdrew from the whole-company contest. Alex does not explicitly specify that label. A simultaneous additional partial alternative is not necessarily abandonment of the whole-company offer.
- A merger-of-equals counterparty is excluded from the modeled acquisition contest unless the target is being sold to it. Alex's Synacor comments establish process relevance, not a complete rule for whether those talks count as bids or satisfy the auction NDA screen.

These are confirmations of existing modeling boundaries, not newly discovered proof that their implementation is wrong.

## 13. Alternatives, price normalization and market-price paths

**A mixture of a lower-priority observation choice and unfulfilled data requirements.** Sources: V¶98–105,117,185; E10/E13.

### Alternative structures

For Meredith's $2.66bn/50.2%-retained and $2.76bn/34%-retained proposals, Alex says they are separate bids, not a range, then favors recording the latter because the target wanted cash-out. E10 retains both alternatives as separate rows. Both agree that the amounts cannot be collapsed into a price interval, but the instruction has no preferred-alternative designation.

**Recommendation:** preserve both source alternatives and select the relevant economic observation during analysis, unless Alex explicitly wants a narrower collected dataset. This retains information while accommodating his target-preference reading. Do not generalize one cash-out example into “always pick the largest dollar amount.” This voice passage is magenta-coded and lower priority than rounds/review.

### Enterprise value to equity/per-share

Alex wants net debt and share counts to convert enterprise offers into comparable equity/per-share amounts. He identifies Meredith's segment net debt and the need to match valuation scope. E13 deliberately fills numeric price cells only when the filing supplies a per-share amount; otherwise amounts and basis stay in Notes. The schema has no dedicated debt, shares or conversion-input dates.

This is an unfulfilled research-data step, not a reason to let the blind extractor invent a normalized price. Decide where a source-linked normalization table belongs. It needs raw value, currency, units, enterprise/equity basis, asset scope, relevant net debt, share count, source/date and the conversion. Historical accounting inputs must not be silently mixed across scopes or dates. Meredith's estimation exclusion remains even after arithmetic conversion because the market-price benchmark is still missing.

### Stock-price path

Alex explicitly requests the target's stock price throughout the sale process (V¶117), since a lower dollar offer can have a larger premium after the stock falls. E13 stores reference prices/premiums mentioned in the filing; this is not a market-data series.

Create a separately specified enrichment step: source, sampling dates, event-time convention, corporate-action adjustments, and treatment of announcement contamination or trading interruptions. External market-data collection is not authorized merely by this audit. Choosing the exact estimator benchmark can wait, but the data requirement should be visible now.

## 14. Event preservation, source quotes and chronology

**Mostly aligned; review must test omissions as well as false rows.** Sources: V¶9–18,29–35,51,55,59,68,73,85,103–104,111–113,126,170,180–183; B–E.

The instruction correctly preserves separate Contact/NDA events, substantive same-day revisions, returns to an old price, signing and public announcement, and meaningful target/bidder actions. It avoids duplicate IOI/Bid rows, routine post-NDA calls and fake exits for parties that were merely contacted. Longview's rollover and sTec's board appointment are not consortium formation. These are not new policy questions.

Review nonetheless needs two directions: every row must have support, and every material source event must have a row. The P&W August 4 example shows why looking only at existing rows misses a substantive disagreement. Synacor's incorrectly imagined go-shop would be a source-reading problem: post-signing contact is not automatically organized solicitation.

### Date windows and display dates

Alex prioritizes order over false day-level precision. E8 supports bounds and narrative ordering, but its Sort date can be raised to preserve order. D3 copies that value into the displayed round opening. In P&W, the new run's round 3 displays July 26 while its own opening event has a July 22–27 interval. That point date is partly a sorting artifact. Do not treat it as a reported July 26 board decision or silently use it as an exact econometric event date.

Cross-paragraph timing intersections matter: first-week contacts after an October 3 meeting can narrow a window; later narrative can distinguish an earlier contact from a later NDA. Keep the original bounds and explanation when a display date is constructed.

### Evidence capacity

Part B asks for one short quote; Notes and Questions have tight word limits. These constraints aid readability but cannot always display all premises of a cross-paragraph inference, a financing window or cohort reconciliation. The audit does not prove they have caused every omission. It does show that verification should have an accessible source trail beyond a single cropped excerpt. Alex specifically requests a direct link to the relevant background/page (V¶170). Use the cockpit's available source navigation and inspect that it leads to the evidence used; do not assume a quote alone verifies a multi-source conclusion.

### Advisers

The current target-adviser row uses first shown selected/acting, agreeing with Alex's early Goodwin example. Renamed/acquired banks should remain one economic adviser where the filing establishes continuity. Bidder adviser affiliation can be noted, but shareholder advisers have no equally explicit location, and tax advisers fall outside target financial/legal categories. Alex's Deloitte remark is exploratory/blue-coded; confirm usefulness before expanding the schema. Unclear representation still belongs in his mandatory review queue.

## 15. What belongs to estimation rather than the extraction discussion?

Alex deliberately wants some interpretations postponed. Preserve that separation.

1. **Primary Formality mapping.** Recorded Formality, Formal excluding Heavy, Formal restricted to None/Light, single-price Formal, and final-stage-only Formal are possible analysis readings already exposed by the analysis tool. They are not interchangeable. No primary mapping is selected. Exclusivity alone should not downgrade, consistent with Alex's explicit instruction.
2. **Inferred exits.** A closure convention is not evidence of voluntary dropout or a bidder-value inequality. Specify censoring/uncertainty treatment separately.
3. **Inferred counts.** Separate reported totals, arithmetic residuals and inferred timings; robustness decisions do not undo settled arithmetic.
4. **Alternative proposals and repeated communications.** A preserved event row is not necessarily a new independent price observation. Commitment-only blank-price rows and copied same-offer prices already have settled handling.
5. **Contingent value and price normalization.** Upfront price, maximum contractual payout and expected package value differ. Market-adjusted premiums need the separate enrichment inputs above.

These choices do not block reviewing the filing or repairing the process map. They do block claiming that the ledger is ready for a particular structural estimator without an analysis specification.

## 16. Recommended order of work and concrete completion criteria

The audit should not become thirty unrelated approval questions. Work through these six connected discussions, followed by source review.

| Order | Discussion | Concrete result needed |
|---|---|---|
| 1 | Stage opening, finality and invitation/exit meaning | A general rule that explains Kraton July 6 and Mac-Gray July 25; an explicit distinction between numbered stage, announced finality and bid Formality; a resolved interpretation of non-invitation |
| 2 | Process dormancy and the additional restart triggers | A justified sTec two-process treatment under an agreed general convention; a deliberate decision on E6(d); a re-evaluated Datalink map |
| 3 | Mandatory human verification | A checklist separate from discretionary questions, a first-deal review sequence, and criteria for later removing checks |
| 4 | Initiation and deadline enforcement | Definitions that preserve sTec's activist fact without unsupported causation, and distinguish due dates/late acceptance from decisive target action |
| 5 | Formality revisions and condition measurement | Resolution of the P&W August 4 and sTec May 28 interpretations; confirmation of the economically consequential E11/E12 defaults and the evidence-time meaning |
| 6 | Collection versus enrichment/estimation | Placement of market prices and EV normalization; treatment of alternative structures; explicit deferred estimator choices |

After agreement, write one general instruction amendment with a decision-to-clause map. It should not contain deal-specific exceptions. Amendments require Austin's approval. Then review affected deals against the agreed definitions, preserving old raw outputs and distinguishing corrected working copies from new blind runs. New model runs require Austin's command.

Suggested review sequence: **Kraton and Mac-Gray** for selection-stage boundaries; **sTec** for finality/processes/activism/deadlines; **Penford and P&W** for inferred-final stages, invitation and formal reaffirmation; **Datalink and Synacor** for restart rules; **Meredith and PetSmart** for scope, alternatives, cohorts and price-event preservation. This order tests interactions rather than choosing a rule that only fixes one example.

A completed review should show filing support for each opening/closure, evidence bounds for uncertain dates, correct named/cohort reconciliation, bid-event coverage, condition source timing and resolved mandatory flags. Mechanical checker success is necessary for schema integrity but does not establish any of these substantive claims.

No fresh extraction, deployment, instruction edit, rebase or workbook amendment was performed for this report. The old handoff remains deleted. VM reconciliation and backup recovery are separate operational work; this report does not assert local/live equivalence.

## Appendix A. Coverage map of Alex's own deal notes

This maps the full original deal-note sections and closing summary to the work above. Repeated themes are consolidated rather than counted as separate decisions.

| Voice section | Main requirements and where handled |
|---|---|
| Legend/title, ¶1–6 | Priority and color interpretation; attribution section |
| P&W, ¶7–35 | Date precision/order, contact/NDA separation, constructed counts and routine-contact suppression (§10,14); deadline and stage boundaries (§1,2,6); Formality/conditions and Aug 4 bid (§8,9); uncertain dropout (§10); advisers/signing/reference fallibility (§14, attribution) |
| Mac-Gray, ¶36–52 | Mixed initiation (§11); contact and NDA cohort/type timing (§10); July 25 stage (§1); conditions, ranges and exclusivity (§8,9); delayed target-driven exits (§10); earliest acting adviser (§14) |
| PetSmart, ¶53–65 | October 3 stage (§3); exact counts and initial/revised-offer arithmetic (§10); same-day order (§14); target drops versus unexplained non-submission (§10); December extension (§6); rollover not consortium (§14) |
| Penford, ¶66–77 | Reference price versus offer (§3,14); winner type/flags (§7); contact-only nonparticipants (§10); definitive negotiation and invitation ambiguity (§2,10); adviser affiliation (§14); Formal confirmation (§8); absent deadline (§6) |
| Kraton, ¶78–86 | Contact/NDA arithmetic and types (§10); three-stage interpretation (§1); valuation-related exits (§10); cash earnout (§9); signing versus announcement (§14) |
| Meredith, ¶87–105 | Economic scope/market benchmark and exclusion (§12); lower-priority tax adviser (§14); EV conversion (§13); detailed legal provisions as lower-priority other-project material, not automatic schema expansion (§9,13); alternative structures (§13); bid reversions/public bidding/signing (§14) |
| Synacor, ¶106–114 | Genuine process break versus continuing exclusivity episode (§4,5); multiple-process flags (§7); public-process/merger announcement distinction, bidder type and false go-shop (§7,14) |
| sTec, ¶115–127 | Dollar versus market-adjusted price path (§13); two processes (§4); activist presence versus initiation (§11); no board-appointment consortium (§14); repeat contact/NDA counts (§10); soft due date (§6); May 16 and May 28 (§2,8,9); signing/announcement (§14) |
| Embedded Claude synthesis, ¶129–166 | Broadly endorsed at ¶168, but not used as independent proof of dates/counts or direct Alex quotations |
| Alex closing summary, ¶167–187 | Mandatory interactive verification, source navigation, event order, types, NDA counts, exit reasons, conditionality, advisers, formal IOIs, partial-only deals, units and process uncertainty (§7,14) |

## Appendix B. Evidence pointers and reproducibility

Instruction section references identify the unchanged text hashed below. Word paragraph numbers use the direct `w:body/w:p` sequence, including empty paragraphs; no headings/tables are silently removed when counting.

| Source | SHA-256 |
|---|---|
| `ref/alex_voice_notes_2026-08.docx` | `9ddb0a38f3ffcabdbf7693ced379df3aa8b53a1c4d065990d09d57978af220fb` |
| `ref/CollectionInstructions_Alex_2026.pdf` | `0dd72b0ab97801cb7cf8bb2a635965a6b4de883399f738968c9985d7f7b56e37` |
| `SEC_Deal_Ledger_Extraction_Instruction.md` | `8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98` |

Selected raw-run checks are reproducible in these unmodified snapshot files:

- Mac-Gray v1.14.1 (git `9b4f178:_dev/recovery/2026-09-27-cockpit/raw/deal__mac-gray_version_opus55-medium-20260926-2019-1d1d60.json`): round 2 opening; events 37–38 for the range and contingent consideration.
- P&W v1.14.1 (git `9b4f178:_dev/recovery/2026-09-27-cockpit/raw/deal__providence-worcester_version_opus55-medium-20260926-2019-366a73.json`): round 3 opening interval; no August 4 Party B Bid; event 49 is the preferred-bidder decision.
- sTec v1.14.1 (git `9b4f178:_dev/recovery/2026-09-27-cockpit/raw/deal__stec_version_opus55-medium-20260926-2027-0643aa.json`): single process, Activist-influenced initiation, May 16 Announced as final, May 3 outcome; event 38 WDC Formal/Unclear.
- Datalink v1.14.1 (git `9b4f178:_dev/recovery/2026-09-27-cockpit/raw/deal__datalink_version_opus55-medium-20260926-2032-350a91.json`): January 28, June 6, August 16 and October 1 round map.
- Synacor v1.14.1 (git `9b4f178:_dev/recovery/2026-09-27-cockpit/raw/deal__synacor_version_opus55-medium-20260926-2028-342883.json`): July 2020 process boundary; no new October 27 process.
- PetSmart older working copy (git `9b4f178:_dev/recovery/2026-09-27-cockpit/raw/deal__petsmart.json`): August 19 round 1 opening; not a v1.14.1 result.

Filing checks use the printed filing pages: Kraton pp.35–37; Mac-Gray pp.33–36; P&W pp.30–31; sTec pp.24–25 and 29–30; Datalink pp.27–29 and 32; PetSmart p.23. The snapshot's `filing__<deal>.json` preserves paragraph blocks and page labels; original filings remain in [raw_filing](../raw_filing). Penford's October 14 confirmation was checked against its dated paragraph in the original filing. The older collection PDF's page 8 was also visually inspected to verify the “Alex's addition” attribution of the informal-final and DropTarget instructions.
