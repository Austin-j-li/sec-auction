# Proposed changes for a coherent v1.14 instruction

25 September 2026. Prepared for Austin. This is a change specification for review, not an adopted instruction. The frozen repository instruction, existing v1.14 draft, workbooks and cockpit have not been edited.

## What this plan changes

The existing draft adds useful bid-term columns, but preserves several older ambiguities about participation, rounds, inference and exits. A consistent v1.14 needs one evidence rule and one decision sequence across all of those sections. Better prose alone cannot establish source accuracy or provide the interactive review workflow Alex requested.

The baseline is the frozen v1.13.2 instruction, SHA-256 `513c8e3e8159e4a6bceccd6ffca32a246302736329a0c7137b64dd3b7ffcd304`, and the September 24 v1.14 draft, SHA-256 `f9595d7413149f86c074f1d4b9ef96a5a24b3d8dd9b6c11061b0bd6e889aea97`. Line references below refer to the [v1.14 draft](/home/uctpiaj/work/Projects/sec-extraction/_dev/maintenance/2026-09-24-bid-terms-taxonomy/SEC_Deal_Ledger_Extraction_Instruction_v1.14_draft.md).

The approved column set and upfront-price policy remain the starting point. Proposed research defaults are identified as proposals. A general rule must explain the cases; individual deals must not become exceptions embedded in the extraction prompt.

## 1 Purpose and decision order — Part A

**Current problem, lines 10–20:** the opening describes an informal-then-formal auction sequence, calls Formality how firmly a bidder is bound, and suggests an exit reveals valuation. Actual processes can depart from that sequence; procedural formality is not a legal-enforceability conclusion; many exits disclose no valuation.

**Change:** describe the task as reconstructing the reported process. State the separate purposes of the participation record, round map, bid procedure, conditions, consideration and chronology. A departing bidder’s valuation is recoverable only where the source supplies a relevant comparison.

Use this decision order throughout the document:

1. Identify the reported act and its supported date/order.
2. Identify the actor, economic scope and bidder unit.
3. Determine the act’s effect on participation and stage admission separately.
4. Place it in a process and solicitation round under the explicit conventions.
5. If it is an offer, classify formality, consideration and each condition independently.
6. Compute summary labels only after the underlying evidence is recorded.
7. Flag uncertainty and the consequence of a different interpretation.

**General instruction:** “Apply the fixed conventions below. Where they do not resolve a material ambiguity, preserve the source facts, identify the unresolved choice and provide a provisional reading only where the schema requires one. The research purpose does not authorize an unsupported fact or an exception to a stated convention.”

A polished proposed opening is already available in the [integration review](/home/uctpiaj/work/archive/tmp-cleanup-2026-09-25/handoffs/sec-v114-alex-integration-2026-09-25.md) (line 106; archived copy, moved from `/home/uctpiaj/work/tmp/` in the 25 September cleanup). It must be checked against the final operative rules before adoption.

## 2 One evidence standard — Part B, D1 and F

**Current problem:** B line 24 refers to inference in every cell, while D1 line 67 describes Inferred only as an inferred event. F line 285 demands that every exact exit label/date/reason be reported or exact arithmetic, although E14 explicitly mandates inferred closures and E8 applies date conventions.

**Change:** distinguish reported facts, exact calculations from reported inputs, classifications under fixed conventions, and additional inferences. Mark Inferred = Y when an event or material field depends on an additional inference. The Note names the field and explains its basis. Do not require every ordinary classification to be flagged merely because the filing uses different vocabulary.

Replace F’s contradictory universal test with two tests:

- Reported and calculated values must preserve the source’s precision and have valid inputs.
- Inferred events or values must obey the relevant convention, retain supported bounds and identify the inference. An inferred exit does not imply an inferred reason.

**Temporal rule:** use facts applicable to the event date, wherever the filing discloses them. A later-written passage may establish an earlier fact if it explicitly dates that fact. A later change in the deal must not rewrite the earlier state. Distinguish the date of disclosure from the date of the underlying fact.

The short row quotation anchors the event. Where other passages support individual fields, retain their separate page references in the Note. A located quotation is not proof that every coded field or omitted event is correct.

## 3 Reading and mapping — Part C

Keep full-background reading, whole-filing supplementation, and the two-way reread. Make the intermediate work concrete:

- Build a source-event inventory before deciding the final row set.
- Map process boundaries and solicitations, recording the selection, requested submission, deadline and subsequent decision for each proposed round.
- Reconcile named parties and cohorts before using their counts to infer exits.
- Record ambiguity in the map before propagating it into every bid and exit.

Do not promise that “fix the map before writing rows” supplies human approval. In the current batch worker it remains the extractor’s provisional map. Actual human adjudication before completion requires the separate workflow extension below.

## 4 Workbook definitions — Part D

**Align the schema and definitions:**

- D1’s CVR/earnout and Antitrust definitions must state the cohort value Varies if it remains permitted by the checker; their headings currently describe only Y/blank.
- Define blank Y markers as “not reported,” not a confirmed negative.
- D1 prices on Other-scope bid rows must agree with E1. Proposed default: whole-company price cells remain empty on other-scope offers; retain that offer’s amount, units and scope in the Note. Do not normalize a partial price into a whole-company price.
- D3 Who was in should distinguish admitted bidders from other continuing participants/reserves and from uncertain eligibility. Bids received counts distinct bidder units, not revision rows. Neither field is the lifetime number of NDA signers.
- D4 must accommodate mandatory review items as well as unsettled conventions. A reported uncertainty may deserve review even when it has no sensible alternative numerical answer.
- Preserve source URL and run provenance in the standalone deliverable. The runner/exporter should obtain these deterministically from existing filing metadata; the extracting model should not guess a URL or gain access to other analyses. Any added Deal facts fields require a schema/checker/export update and preserved raw-output provenance.

## 5 Transaction scope and the auction screen — E1

**Current gap, lines 129–131:** a partial offer gets Other-scope bid, but participation and the NDA screen do not consistently distinguish the transaction being pursued.

**Proposed research default:** keep whole-company participation separate from partial-sale alternatives, consistent with Alex’s written instructions and Q&A. Retain partial offers and their competitive relevance descriptively; do not add them to one undifferentiated whole-company rival count.

Record when a bidder changes scope. Close its whole-company participation only when the filing shows that the whole-company offer/interest was abandoned or excluded. Continued pursuit of a division is not necessarily a withdrawal from every transaction discussion. Do not retrospectively recode earlier NDA participation just because a narrower interest is disclosed later.

For merger-of-equals talks, retain the dated history and flag which party’s sale, if any, is being pursued. Do not invent a control-or-premium test. Scope uncertainty must be resolved or explicitly branched before those contacts are used to join sale processes.

Define the auction screen’s unit explicitly: relevant independent prospective acquirers, with scope known or uncertain, rather than every NDA involving the company. This is an analysis convention that needs adoption, not a source fact.

## 6 Material events take precedence — D2 and E2

**Current conflict, lines 81, 135 and 208:** D2 says an approach naming a price is a Bid, whereas E10 excludes valuations without offers. E2’s list of routine legal negotiation can also swallow changes that E10 requires.

**Replacement rules:**

“An approach is a Bid only when the filing reports an acquisition proposal, including an oral, non-binding or conditional proposal. A quoted market price, a valuation statement or a refusal to offer above a threshold is not by itself a proposal.”

“The material-change test takes precedence over the routine-event exclusions. A document exchange that changes a bidder’s economic terms or commitment, target requirements, participation or information is material even if it occurs during legal negotiations.”

Preserve substantive price feedback and asymmetric information as events. Keep routine repeated calls, unchanged drafts and board acknowledgment out of the ledger. A target fee or process requirement is not automatically a bidder’s new offer.

## 7 Entry, eligibility, admission and participation — E3, E4, D3 and E14

Keep four concepts distinct:

- **Process participation:** the bidder has entered and has not left that relevant process/scope.
- **Solicitation eligibility:** the bidder was entitled to answer this specific request by its deadline.
- **Round admission:** the target selected it for that stage.
- **Continuing reserve/alternative:** the target continues considering it despite its not being admitted to the selected solicitation.

An NDA signed at some time during a two-month period does not establish eligibility by a deadline inside that period. A live participant not selected for updated bids need not have been excluded from every continuing discussion. Kraton’s July 6 partial proposals and Penford’s reserve participants are useful checks.

Keep Count as a reported/exactly derived integer or blank with supported bounds. Do not encode an ordinary-sequence assumption as a fact. Any estimation point assumption belongs in an explicit analysis policy or reviewed decision.

Clarify cohort bookkeeping: an individual later identified as belonging to a cohort is not another entrant. Individual detail and the residual must reconcile for the same step; subsequent bids by that individual remain their own events. Count must never be summed across all event rows.

Keep E4’s existing distinction between real joint bidding and rollover, financing support, shared advisers or board changes. Reconcile independent units when a genuine group forms.

## 8 Separate sale attempts — E5

Keep continuity, evidence of a break and a fresh start as distinct tests. Make clear that no reported contact is not proof no contact occurred. Apply supported date bounds rather than rounding a gap up to the threshold. An existing NDA document alone is not proof that active negotiations continued.

Where transaction scope or an undated interval affects the conclusion, retain an alternative process map in Questions. Do not promise a new process count merely from including/excluding an ambiguous merger-of-equals episode.

Distinguish a reported termination from an inferred lapse. Close an earlier process once and enter returning parties afresh, without double-counting both group/process closures and individual exits.

The detailed threshold/continuity interpretation remains a research convention. Alex’s sTec and Synacor readings are acceptance cases to discuss, not permission to write a universal “three months always means a new process” rule.

## 9 Count each solicitation stage once — E6

**Current conflicts, lines 169–177:** one clause opens a round for a distinct information stage, another for the first final-offer request, and another says repeated requests merely continue the round. The Round 1 hierarchy can also move genuine earlier bilateral negotiations into round 0 when broad outreach appears later.

**Proposed general wording:**

“Round 1 opens at the earliest supported target-organized sale stage, whether substantive bilateral negotiation or broader solicitation. Later expansion does not move earlier requested bids into round 0. A preliminary unsolicited approach alone does not open a round.”

“Count one target-organized bidding stage once. Admission, common diligence and the letter specifying that stage’s submission may be steps in one round. Open another round when the target establishes a distinct competitive solicitation, selection or materially changed submission basis. Identify the evidence distinguishing it from preparation or negotiation within the existing round.”

“Deliberate reopening of rival solicitation after other discussions were suspended may open another round of the same process. Use its effective reopening date. Routine follow-up or one participant’s unsolicited return does not alone open a round.”

Keep deadline extensions, repeated bargaining and a bidder’s own ‘last and best’ language from automatically creating rounds. Finality describes what the target communicated or demonstrably instituted; it is not the eventual historical last bid and does not determine the formality of every offer.

**Decision needed:** this rule can coalesce Kraton’s July 20 admission and August 11 procedures into one round. It can also change the July/August split in Datalink’s retained five-round map. Austin’s earlier F9 specifically addressed January versus June, not a separate adjudication of that later split. Preserve January under the accepted ruling and surface the later split for explicit reconciliation. Also resolve Alex’s sTec ‘not final’ reading against the filing’s final-round procedure language; do not silently override either.

## 10 Dates and marker ordering — E7 and E8

Keep initial contact, NDA execution, information delivery and later reuse separate. Read annexes for executed NDA dates and reconcile any resulting named member with the earlier cohort.

Preserve the distinction between source date bounds and Sort date. Explain which interval conventions are coding rules, rather than literally reported day ranges. Never use the due date to assert timely submission. If exact dates and source sequence conflict, flag the conflict rather than moving a reported date.

Add a deterministic representation rule for Round opened: it is the first row assigned to the new round, with the same supported date as the triggering act where appropriate. Its display position is a marker convention, not a claim that the administrative marker occurred earlier in real time. This aligns the text with the existing opening-order checker.

## 11 Deadline outcomes — E9

**Current problem, line 204:** accepting a post-deadline negotiated revision can satisfy Late bids accepted while the same target decision satisfies Enforced. The latest question’s ‘first response’ language is also too broad if a later solicitation requests a required written or final response from someone who bid earlier.

**Proposed definition:** “A late response is the required submission for the specified solicitation, received after the due date given to that bidder and considered by the target. A later improvement to an on-time response is not late solely because its date follows that deadline. Record the subsequent invitation and revision separately.”

Record announced/revised due dates, actual response timing and what the target then did before assigning an outcome. Enforced means the defined submission cutoff was used to take the next step; it does not promise an end to bargaining.

Specify one outcome precedence if the existing single-value-per-date design is retained: an explicit extension is recorded as such; accepted overdue required responses take precedence over a generic Enforced inference; otherwise distinguish acting on the responses from merely continuing negotiations. Keep multiple observed actions and unclear timing in the Notes/Questions. Do not infer an invitation to improve solely because a later increase followed banker conversations.

Missing a deadline is not itself a bidder’s exit. Cross-reference the continuation test in E14.

## 12 Offers and reaffirmations share one evidence rule — E10 and E11

**Current problem, lines 208–224:** same-price reaffirmations carry standing conditions, while a silent price change resets them. A prior Formal label can also obscure a later material commitment change.

“Every communicated material change in price, consideration or bidder commitment is a Bid, including a change in conditions, funding commitment, reverse termination fee or bidder/sponsor liability. This applies even when shareholder price is unchanged.”

“A Bid reaffirmed requires an actual bidder confirmation or its own document submission that makes a substantive difference to the record. Carry the supported standing price; classify every other field under the same evidence rules as a revised Bid.”

Use three linkage cases:

1. **Express incorporation:** the offer expressly adopts earlier terms. Carry the disclosed proposal terms within that reference’s scope, subject to reported changes.
2. **Inferred continuity:** the filing supports a continuous document track but does not expressly link the new offer. Permit a Formal classification only under an adopted continuity convention; identify the documents, offer and applicable dates, and mark the inference.
3. **No supported link:** use the current offer’s evidence and the normal classification default. A return after withdrawal needs renewed linkage; express readoption can provide it.

Later document negotiations do not by themselves establish engagement at an earlier date. Historical diligence status is not copied merely because transaction terms were incorporated. Recompute Conditions after filling all supported components.

Penford’s October 8 markup versus Alex’s October 14 formal date requires a general decision about formality, not a Penford exception. Record both material communications if supported, and decide which criteria produce their labels. Likewise, do not make an offer unconditional solely because Alex’s illustrative description uses that word where the filing still discusses diligence.

## 13 Conditions, missingness and time — E12

### One rule for every offer row

“Use facts the filing makes applicable to the offer at its event date, wherever reported. Express incorporation carries disclosed proposal terms within its scope. Assess dated status facts separately. Without applicable evidence or incorporation, use Not stated. The rule is identical for initial offers, revisions and reaffirmations.”

### Diligence

Reserve Incomplete for reported unfinished work or work still underway, including confirmatory work. State explicitly that ‘substantially all completed’ maps to Incomplete while leaving the character of the remainder unknown. This differs from ‘substantive diligence completed’: that describes the kind of work completed and does not, by itself, establish either all work complete or affirmative remaining work. Preserve that wording and use Not stated for the unresolved overall status unless other evidence resolves it. Neither expression by itself establishes that only confirmatory work remains or warrants Light.

Reserve Not begun for evidence that the relevant diligence has not begun. Access need not mean a named virtual data room if confidential memoranda or other actual diligence are shown. If an earlier NDA/information-access account conflicts with a later statement that diligence was commencing, preserve both and ask which activity the passage describes instead of assigning a confident no-access status.

A multi-week period drives Heavy only when the source connects it to substantive remaining diligence or a required diligence period under an explicitly adopted duration convention. A long exclusive negotiation period does not establish that fact. Proposed precedence: an express description of only confirmatory/limited work overrides the duration heuristic, unless another Heavy trigger applies.

### Financing

Retain Austin’s selected codes, but define Committed by its reported evidence rather than the universal claim ‘cannot walk away.’ Preserve its basis in the Note: commitment letters, full sponsor/parent commitment, or no-financing-condition language are distinct evidence.

Explicitly resolve the overlap: proposed precedence is that reported unarranged/uncommitted funding produces Contingent even if the offer also disclaims a financing condition, with both facts retained. A draft letter, the use of debt, or silence does not on its own prove an absence of commitments. Apply the evidence at each bid date; do not backfill the signed agreement’s terms into earlier offers.

This precedence is a proposed clarification to adopt, not a claim that every historical draft already implemented it. Kraton’s September rows need individual treatment, not one label inferred from the final signed package.

### Exclusivity

Preferred proposal: delete the rule that a later request codes the earlier standing bid. Record the later request at its own supported date, link it to the standing offer, and use a new Bid if the bidder communicates a material revision. An earlier request also must not be recoded Required merely because the bidder later stops after refusal, unless the source makes the condition applicable to that earlier request.

The conditions reviewer proposed retaining a clearly labelled standing-offer exception instead. That preserves the current special rule but means the bid row is no longer uniformly a snapshot at its date; downstream consumers must consult the separate request date. I recommend the snapshot approach for coherent as-of analysis. This is an explicit choice between two temporal designs, not a claim that the prior approved column set itself was defective.

Exclusivity alone does not change Formality or the Conditions level. Substantive diligence associated with it is assessed on its own evidence.

### Summary Conditions

Compute the summary after the components and other material conditions. None requires affirmative readiness/no unresolved material-condition support; passing the checker's necessary combinations is not sufficient evidence. Regulatory Not stated must remain unknown rather than supplying a No concern assertion. Requiring an explicit Regulatory No concern in every None row would be a new, stricter convention, not an already-established checker requirement.

Light needs supported limited/confirmatory remaining matters or the explicitly adopted equivalent test. Heavy needs a supported heavy trigger. Unclear remains a real unresolved category: it must not become Light merely because an analyst filters out Heavy.

State how contingent consideration relates to this summary. A CVR is recorded payment uncertainty; it is not automatically a financing contingency or a right to abandon closing. The current text does not establish a universal CVR-to-Heavy rule. My proposed default is to keep its value uncertainty in the consideration fields and treat a separately supported material closing/repricing condition under E12; if the researchers want CVRs themselves to drive Heavy, specify that decision explicitly.

For cohorts, Varies must distinguish known differences from partial reporting in its Note. “Two of five contingent; three not stated” does not identify five contingent or three committed bidders. Mixed/partly reported components do not license copying a single participant’s summary to the whole cohort.

## 14 Price and consideration — E13

Keep the approved upfront-only policy, the attributed CVR value and the source's currency/units. Deduct a contingent component from a package value only when the filing supplies the relevant compatible figures and their relationship. A face maximum, a bidder valuation and guaranteed cash are not interchangeable amounts.

Keep alternative transaction structures separate, even in one communication; a range of prices for one proposal is different. Record reversions to earlier prices and same-day order. Preserve market-price references from the filing with their dates, but do not manufacture the complete stock-price series Alex requested. That series belongs in a separate downstream data task.

Keep the approved Stock % definition consistent across D1, E13, code and export. Its project convention for other securities must be explicit in the Note; analysts must not mistake it for an ownership percentage. Resolve E1/D1 on partial-offer price cells as stated above.

## 15 Exits and closure — E14

**Current conflict, lines 257–269:** Did not submit is ‘not necessarily permanent’ but participates in a formula that subtracts all exits; a complete advancing set implies exclusion even where other parties remain under consideration; deadline inference precedes evidence of continued participation.

Apply this order:

1. Look for explicit continued solicitation, active offer, pending diligence or other participation after the apparent missed deadline/selection.
2. Record reported withdrawals and exclusions with their supported timing.
3. Distinguish failure to submit to one solicitation from ending participation in the process.
4. Infer closure only when the convention’s eligibility and transition conditions hold and the filing does not carry the participant forward.

With the current schema, reserve the Did not submit exit label for cases where a closure is supported under the adopted rule. Record a missed submission by a continuing bidder in the deadline/round account or a material event, without subtracting the bidder and inventing a later re-entry. If the researchers need all non-submissions as machine-readable non-exit events, that is an explicit event-vocabulary/schema change.

An unselected bidder is dropped only where the target's action establishes exclusion from further relevant participation, not merely exclusion from one solicitation. Signing closure remains distinct from a bidder's voluntary withdrawal.

Separate exit actor, exit timing and stated reason. Target price feedback followed by inability to improve can support a price reason without proving an exact date of target exclusion. Preserve an inferred closure and reported comparison separately; apply the adopted inferred-reason convention consistently rather than inferring valuation from disappearance.

## 16 Mandatory review and acceptance — Part F

Replace ‘only material calls that could go either way’ with two categories:

- **Mandatory checks from Alex:** candidate round/process boundaries; deadline extension/non-enforcement; unknown winner/Formal-bidder type after whole-filing reading; uncertain NDA counts/type splits; uncertain exit actor/reason; initial condition coding; uncertain adviser affiliation; surprising Formal IOIs; partial-only transactions; non-comparable prices/currency/bases.
- **Additional material ambiguities:** questions affecting the main research uses that the conventions have not settled.

Require each Question to separate a source gap, a proposed inference, an instruction convention or a researcher decision. Give the evidence and consequence; do not require a confident fabricated answer to an undisclosed fact.

Reconcile the consequences of every accepted correction: entry/exit totals, round admission, offer references, deadline outcomes and process counts. Review from rows to sources and from source events to rows. A valid schema, matching quotations or agreement between models does not establish research acceptance.

## Implementation outside the instruction

| Component | Concrete change | Verification |
| --- | --- | --- |
| Checker | Align exact new schema values, inference rules, deadline outcomes and required metadata with the adopted instruction. Make Antitrust with an incompatible Regulatory code an error, as the stated prerequisite requires. | Positive/negative fixtures for real cross-field contradictions; v1.13.2 backward compatibility; avoid tests that only repeat wording. |
| Cockpit/import/export | Preserve new metadata, codes and field attribution; expose relevant source passages and dependencies. If scope intervals need additional structured fields, design and approve them explicitly rather than burying an unparseable assumption in live counts. | v1.14 import-edit-export round trip, numeric/unknown preservation and immutable-original comparison. |
| Worker/review workflow | Current lifecycle has no mid-run human pause. Design a map-review stage followed by ledger completion in an assisted workflow, preserving the map, reviewer decisions and subsequent version. | Exercise pause, review, resume, cancellation and provenance without a real model extraction first. |
| Blind extraction versus assisted revision | Preserve the blind one-instruction/one-filing baseline. A continuation given human deal-specific decisions must be labelled assisted/revision, with those decisions preserved as inputs. | Verify input manifests and labels; do not report assisted results as blind accuracy. |
| Analysis | Specify how ranges, partial alternatives, conditional Formal bids, Unclear and cohorts are handled. Keep the choice separate from reported facts. | Reproduce the resulting counts/labels from the same ledger under each declared policy. |

## Acceptance cases before calling v1.14 coherent

Use these as source-backed review cases, not names or answers embedded in the extraction instruction:

| Case | Required invariant |
| --- | --- |
| Mac-Gray two-month NDA window | Eventual cohort membership does not prove July deadline eligibility. |
| Kraton July 6 | A new selected solicitation does not automatically eliminate partial alternatives still being evaluated. |
| Synacor E December 14 | Ending whole-company interest is distinguished from continued partial-stake negotiation. |
| Synacor October 27 / Datalink October 1 | Reopening is dated to the effective action and stays in the continuing process. |
| Kraton July/August; Datalink July/August | Preparatory steps are not counted twice without an adjudicated distinct-round basis. |
| WDC June 10 | Express readoption carries linked proposal terms, not stale diligence status. |
| G&W July 26 / August 3 | Later document use does not silently become contemporaneous proof. |
| Penford August 10 / August 14 | A later exclusivity request does not rewrite the earlier bid. |
| Synacor E five-week request | Exclusivity duration alone does not establish substantive-diligence duration. |
| Kraton financing rows | A draft letter is not automatic proof of uncommitted financing; later contract terms do not silently backfill earlier bids. |
| Mac-Gray same-price sponsor commitments | Material commitment changes survive the routine-document exclusion. |
| sTec D missed deadlines | Explicit continued participation prevents fabricated exit/re-entry. |
| sTec H | Refusing to improve does not by itself identify an exact target-drop date. |
| Penford Party A October 4 / October 13 | Clear negative threshold and ambiguous valuation/proposal wording are not conflated. |
| All final exports | Source links, raw provenance, uncertainties and remaining researcher decisions remain inspectable. |

After the general conventions are adopted, apply controlled corrections to existing drafts and inspect the complete diff. New blind extraction tests, publication, changing the default instruction and repository commits remain separate actions; this specification does not perform them.
