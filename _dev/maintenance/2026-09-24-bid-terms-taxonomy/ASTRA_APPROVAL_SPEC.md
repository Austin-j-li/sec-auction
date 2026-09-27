# v1.14 approval specification

Prepared for Austin — 25 September 2026

**Status: proposed implementation specification, awaiting approval.** This consolidates the conversation, Alex’s written instructions, August voice notes and Q&A, the September 24 taxonomy, and the completed Astra source reviews. It specifies a coherent instruction and the accompanying pipeline work. It does not enact those changes.

The immediate recommendation is to finish v1.14 as a consistent account of **what happened, who was still participating, what each offer contained, and what remained uncertain at that time**. Keep analytical assumptions separate. Record consideration, procedural formality and conditions independently. A CVR or exclusivity requirement alone must not make an offer Heavy.

This document supersedes the earlier [instruction change plan](INSTRUCTION_CHANGE_PLAN.md) wherever recommendations differ, especially the now-accepted CVR rule. The [recommendation review](RECOMMENDATION_REVIEW.md) remains the evidence record; its suggestion to ask Alex about CVR-to-Heavy is superseded by Austin’s latest acceptance. Older review documents remain historical evidence.

## 1. Decisions carried forward and choices being submitted

| Status | Decision | Consequence |
| --- | --- | --- |
| Already agreed in the taxonomy work | Retain the approved consideration and condition columns. | Four workbook sheets; 29 Deal ledger columns. No additional Consideration, fee, or bidder-regulatory-risk column. |
| Already agreed | Price low/high contain upfront per-share consideration; contingent consideration is separate. | Keep the filing’s total package value and its basis in the Note. |
| Already agreed | Highly confident letters and explicitly uncommitted funding are Financing = Contingent. | They cannot support Committed merely because a funding source is named. |
| Accepted in this conversation | A CVR/earnout alone never triggers Heavy, regardless of its size. | No discretionary “material CVR” threshold. Independently supported financing, diligence or closing conditions still determine the grade. |
| Carried forward from Alex’s instructions | Exclusivity alone does not determine Formality or Conditions. | Record its status and period; assess associated diligence separately. |
| Proposed for approval | Every offer row describes the evidence applicable at its own date, including revisions and reaffirmations. | Remove the special permission to rewrite an earlier standing bid with a later exclusivity request. |
| Proposed for approval | Use one explicit Conditions decision sequence, with affirmative support for None/Light. | Unknown does not become low risk by default. See §4. |
| Proposed for approval | Preserve counts, timing and scope uncertainty; do not fill missing facts with a presumed ordinary auction sequence. | Bounds and alternatives remain visible. Any point assumption belongs to a separately declared analysis policy. |
| Proposed for approval, supported by Alex’s Q&A | Whole-company bidder counts exclude partial-only alternatives from the primary definition. | Retain those alternatives and scope changes; do not erase their possible competitive influence. |
| Proposed for approval | Count a solicitation stage once, and distinguish participation from admission to that stage. | Reconcile the existing round maps before changing historical data. |
| Still requiring a research decision before finalization | Specific round/finality conflicts, inferred document continuity, and the analysis treatment of incomplete participation evidence. | Use the short decision list in §6; no silent overwrite of prior adjudications. |

Approval of a specification is not evidence that a deal has been extracted correctly. Source review, researcher decisions and implementation checks have different roles.

## 2. Proposed polished opening for v1.14

The following replaces Part A and governs the wording of the later sections. It deliberately avoids calling a procedurally Formal offer legally binding or claiming that disappearance reveals a bidder’s valuation.

> **A. Purpose and approach**
>
> Reconstruct the sale process reported in the filing so that the researchers can study how bidders enter, compete, revise their proposals and leave. Follow the reported sequence, including bilateral negotiations, changes of scope, interrupted discussions and renewed outreach. Do not force the history into a standard informal-then-formal auction.
>
> The ledger must let a reader answer four questions: who was participating and in what capacity; what the target requested and when; what each bidder offered; and how the process changed after each offer or decision. Distinguish participation in the process from admission to a particular solicitation. Preserve uncertainty about identities, numbers, dates and scope instead of supplying an unsupported precise answer.
>
> Record an offer’s procedure, consideration and conditions separately. Formality describes the submission procedure and engagement with definitive documents under E11. The consideration columns describe the upfront payment and any contingent payment. The condition columns describe diligence, financing, regulatory concerns and exclusivity as supported at the offer date. Conditions summarizes the supported remaining diligence, funding and other closing or repricing obstacles under E12. A CVR or exclusivity alone does not increase that summary level, and no condition changes the Formality label.
>
> Record every communicated material change in price, consideration or bidder commitment, even when the shareholder price stays the same. Record material information and target feedback that explain later behavior. Distinguish failure to answer one solicitation from departure from the process. An exit establishes a valuation comparison only where the filing supplies the necessary evidence.
>
> First identify the act, its timing, actor and scope. Then determine its effect on participation and place it in a process and round. For an offer, record the evidence for each attribute before assigning its summary labels. Apply the fixed conventions consistently. Where a material choice remains unresolved, preserve the source facts, flag the choice and explain what another reading would change. The research purpose does not authorize an unsupported fact or an exception to a stated convention.

The final draft must use the same definitions in Parts D–F. The introduction must not become a second, competing rulebook.

## 3. Schema, evidence and reading workflow

### 3.1 Keep the approved workbook structure

Sheet order: **Deal ledger; Rounds; Questions; Deal facts**. Keep the ledger order:

`#; When; Who; Type; Event; Process; Round; Price low; Price high; Stock %; CVR/earnout; CVR/earnout value; Formality; Conditions; Due diligence; Financing; Regulatory; Antitrust; Exclusivity; Count; Exit reason; Inferred; Note; Quote and page; Flag; Reviewer note; Sort date; Date from; Date to`.

| Field | Values and interpretation |
| --- | --- |
| Stock % | Numeric 0–100; a source-supported range; Part stock; Not stated; Varies. It is the stock share of upfront consideration, not ownership of the combined company. Keep the existing disclosed convention for other non-contingent securities, identifying their nature in the Note. |
| CVR/earnout | Y, Varies, or blank. A payment after closing whose amount depends on future events. Blank means none reported, not proven absent. A pre-closing price contingency is not automatically a CVR. |
| CVR/earnout value | Reported positive per-share amount, or blank; only with Y. Identify maximum, face amount or attributed valuation in the Note. Do not interchange these bases. |
| Formality | Formal, Informal, Unclear, under the procedural rule in E11. |
| Conditions | None, Light, Heavy, Unclear, under §4. There is no Conditions = Varies value. |
| Due diligence | Complete, Incomplete, Not begun, Not stated, Varies. Progress and severity are separate: Incomplete does not always mean Heavy. |
| Financing | Not needed, Committed, Contingent, Not stated, Varies. Define the reported basis, not a general legal guarantee. |
| Regulatory | No concern, Concern, Not stated, Varies. Routine required approval alone is Not stated. |
| Antitrust | Y, Varies, or blank, qualifying a Regulatory value of No concern, Concern or Varies. Keep a bare approval requirement in the Note when that prerequisite is unmet. |
| Exclusivity | Required, Requested, Not stated, Varies. No new “No” or “Not required” code. Preserve an express negative statement in the Note. |

Explicitly document Varies in D1, E12 and E13. Proposed cohort convention: use it for disclosed differences or partial reporting, and say which in the Note. Do not use it for one bidder. If all members are unreported, use Not stated or blank as appropriate; if only two of five have disclosed financing, do not give all five those terms.

Whole-company price cells remain blank on Other-scope bid rows. Put that proposal’s amount, units and scope in the Note. Other applicable bid attributes can still be populated. This resolves D1’s broad price wording against E1 without manufacturing comparable prices.

Do not add ledger columns for review convenience. Source URL and provenance can be appended as named Deal facts metadata in a **derived delivery copy**, described in §7; preserve the raw workbook separately.

### 3.2 One evidence rule

Separate four things: reported facts; exact calculations from reported inputs; classifications under an adopted convention; and additional inferences. Mark Inferred = Y for an inferred event or material inferred field, and name that field in the Note. Ordinary application of a fixed classification does not by itself require Y.

Use evidence applicable to the event date. A passage disclosed later can establish an earlier fact if it explicitly dates that fact. A later development cannot be projected backward. An earlier row’s value is not itself evidence that the value still applied to a later offer.

For every initial offer, revision and reaffirmation:

1. Use the current communication and background evidence that applies at that date.
2. Carry proposal terms expressly incorporated from an earlier offer, within the stated scope of that incorporation.
3. Assess status facts, such as diligence progress, separately. Incorporating transaction terms does not freeze an earlier diligence state.
4. Otherwise use Not stated/blank or the prescribed classification default. If a permitted inference supplies a material field, identify it.
5. Recompute the summary from the supported attributes.

If narrative evidence expressly covers a period, use it for offers within that period; do not mechanically reset a known applicable fact merely because the price changed. Conversely, silence is not an unrestricted inheritance rule.

Each short quotation anchors the event. Additional passages supporting different fields need their own page references in the Note or review evidence record. A quotation match is not proof that every field is supported.

### 3.3 Reading sequence

Require: read the complete background; inspect relevant filing/annex material; build a source-event inventory; map processes, solicitations and participant/cohort relationships; draft rows; reread from sources to rows and rows to sources; reconcile dependencies.

The map is provisional until reviewed. Part C must not promise a human checkpoint that the runner does not provide. The separate assisted workflow in §7 implements that part of Alex’s request.

## 4. Exact condition-classification design

### 4.1 Grade an individual offer before aggregating a cohort

Apply this order: **supported Heavy trigger → positively supported None → positively supported Light → Unclear**. Never use “not Heavy” as a synonym for Light. Apply the common-level rule for cohorts only after the individual evidence can support it.

| Grade | Proposed operative test |
| --- | --- |
| Heavy | At least one supported trigger H1–H3 below applies to this offer. The Note names the trigger and its evidence. |
| None | Affirmative evidence of readiness to sign with no unresolved material condition, Due diligence = Complete, Financing = Committed or Not needed, and no reported regulatory or other material obstacle. The field combination alone is insufficient. |
| Light | Affirmative evidence that the remaining matters are only confirmatory/limited diligence or final documentation, with no supported Heavy trigger. The limiting statement must describe what remains overall, or other applicable evidence must establish that limitation. Merely mentioning confirmatory diligence while other necessary matters remain unknown is insufficient. |
| Unclear | The evidence does not establish Heavy, None or Light. Keep the known components; do not fill their gaps to force a grade. |

Regulatory = Not stated remains unknown. It does not assert No concern. It can coexist with None or Light when affirmative overall evidence supports the summary and no material obstacle is reported; an explicit clean-regulatory statement in every case is not introduced as a new universal requirement.

**Heavy triggers, for approval:**

- **H1 — Financing = Contingent.** This includes explicit uncommitted funding and highly confident/non-binding lender support.
- **H2 — substantive remaining diligence, or a stated required multi-week diligence period.** Make the retained duration convention precise: two weeks or longer, expressly describing remaining required diligence. Do not substitute an exclusivity period, time until signing or generic negotiation period. An explicit statement that only confirmatory/limited diligence remains defeats the duration shortcut; another Heavy trigger can still apply.
- **H3 — another expressly stated substantial closing or repricing obstacle.** Require an identifiable basis: a bidder right to revise the upfront price; an unresolved transaction-specific prerequisite on which proceeding depends; or an identified material regulatory obstacle to completion. Record the stated dependency or obstacle. Ordinary approvals, routine documentation, generic risk language, and the size of a CVR do not qualify by themselves. If the source does not establish that character, flag the ambiguity instead of inventing a heavy condition.

This preserves a route for uncommon conditions without asking the model to decide whether a deal merely “feels risky.” Do not turn H3 into a second CVR or exclusivity test. A routine approval requirement is not automatically a transaction-specific obstacle.

### 4.2 Component definitions and precedence

**Due diligence.** Complete requires support that none remains. Incomplete requires reported unfinished work, whether substantive or confirmatory. “Substantially all completed” maps to Incomplete under the proposed convention, without assuming what remains. “Substantive diligence completed” alone leaves overall completion unresolved: use Not stated unless other evidence establishes completion or remaining work. Not begun requires affirmative support; an absent data-room reference is insufficient, and an NDA alone does not prove work began. Neither Not begun nor Incomplete by itself establishes H2; the evidence must also establish the required character or duration of the remaining work.

**Financing.** Not needed retains the adopted cash-on-hand/existing-facility/all-stock meaning. Committed retains the project’s reported-evidence bucket: commitment letters, a full sponsor/parent commitment, or an offer expressly not subject to a financing condition. State which basis applies; remove the blanket claim that this proves the bidder cannot walk away. Proposed overlap rule: expressly unarranged/uncommitted funding takes precedence and yields Contingent even if the offer also disclaims a financing condition; preserve both facts. A draft letter, debt use, or silence alone establishes neither Committed nor Contingent.

**Regulatory and Antitrust.** No concern requires a reported assessment supporting a clean or prompt path. Concern requires a reported material risk such as difficult clearance, divestitures, delay or doubt about completion. Under this proposed definition, Concern supplies the regulatory obstacle in H3 and entails Heavy; do not put a routine approval requirement in Concern. A generic requirement for approval is Not stated. Record the jurisdiction, authority, relevant commitment and timing in the Note; do not backfill a later agreement’s risk allocation.

**Exclusivity.** Required means the bid or willingness to proceed is expressly conditional on it. Requested means a request, assumption or draft without that supported condition. Record a later request at its own date. If it materially revises the offer, use Bid and describe the change; otherwise use Exclusivity changed linked to the standing offer. Do not create duplicate substantive rows for the same act merely to use both labels. A separate grant, extension or termination is its own event. A later refusal or departure does not retrospectively establish that an earlier request was conditional unless the source makes that connection.

**Cohorts.** Use a common Conditions grade only when supported for every represented member. If grades differ, or partial evidence prevents a common grade, use Unclear and describe the composition. One known Heavy bidder does not make the whole cohort Heavy. A cohort-wide Financing = Contingent, however, still entails Heavy because the code asserts that condition for all represented members.

### 4.3 Examples the final instruction and evaluation must agree on

| Reported evidence | Required behavior |
| --- | --- |
| An otherwise unchanged offer adds a CVR. | Record its payment feature and value basis. The Conditions grade stays the same. |
| CVR; other closing-condition evidence absent. | CVR = Y; relevant components Not stated; Conditions = Unclear. |
| CVR; expressly only confirmatory work remains overall. | Light, unless another supported Heavy trigger contradicts that description. |
| CVR; financing expressly uncommitted. | Financing = Contingent; Conditions = Heavy because of financing. |
| Five weeks of requested exclusivity; diligence and documents mentioned, without a required substantive-diligence period. | Exclusivity recorded. Duration alone does not establish Heavy; normally Unclear without further support. |
| Thirty days expressly required for remaining diligence, without a limiting confirmatory description. | Heavy under the retained multi-week diligence convention; name that basis. |
| Diligence complete, funds supported, affirmative readiness, CVR still present. | None can be correct. It means no supported remaining condition under E12, not a guaranteed total CVR payout. |
| Signed financing evidence arises after the bid. | Do not recode the earlier offer as Committed unless the filing expressly establishes the commitment at that earlier time. |

These are rule checks, not a claim that future model outputs will always obey them. Human/source verification remains necessary.

## 5. Section-by-section changes to the rest of the instruction

### B, D1 and F — evidence and inference

Replace the conflict between “every cell is evidence-based,” “Inferred concerns only the event,” and F’s demand that every exit detail be reported. A reported act can have an inferred material date or attribute. An inferred closure can have an unknown reason. Apply §3.2 everywhere and make source precision, inference justification and cross-field consistency separate checks.

Do not require an invented point estimate in Recommended answer when the correct recommendation is to retain an unknown or a range. Questions must distinguish a source gap, permitted inference, convention choice and researcher decision.

### E1 — scope and auction screen

Use whole-company acquisition participation as the primary scope; preserve partial alternatives separately. Mark a supported change of scope at the date it occurs. Ending a whole-company proposal is not necessarily leaving every discussion. A later partial proposal does not retrospectively prove that the bidder’s earlier involvement was partial-only.

For merger-of-equals discussions, preserve the dated approach and disclosed roles. Do not introduce the unsupported “control surrendered or premium paid” screen from the current questions document. When acquirer/target sale roles remain unclear, flag the scope and its effect on process continuity. Do not infer exclusion from missing ownership terms.

Define the screen’s units as independent prospective acquirers pursuing the relevant scope, with uncertainty retained. A count of all NDA signers, including financing/supporting parties or unrelated scopes, is not automatically that number. Partial-only deals must be flagged for the research sample; retain the existing Meredith scope concern rather than treating a clean extraction as estimation eligibility.

### D2 and E2 — what deserves a row

Resolve “an approach naming a price is a Bid” against E10’s exclusion of non-offer valuations. A Bid requires a communicated acquisition proposal, including an oral, conditional or non-binding proposal. A market reference, hypothetical ceiling, or refusal to pay above a threshold is not automatically an offer. Ambiguous valuation/proposal language needs a source-backed question.

The material-change rule takes priority over the routine-legal-negotiation exclusion. Capture changes in economic terms, bidder commitments, target requirements, information supplied and price feedback. Keep routine unchanged document circulation out. Distinguish a target’s new requirement from a bidder accepting or countering it.

One offer communication normally has one row; IOI and offer are not duplicate events. Record genuinely separate alternatives or materially different proposals as prescribed by E10/E13. Process/round marker rows remain explicit representation exceptions.

### E3, E4 and D3 — who counts, and when

Distinguish process participation, eligibility for a particular solicitation, admission to that stage, and continuing reserve/alternative status. Rounds.Who was in must identify those categories rather than label all lifetime NDA signers as admitted.

Keep exact counts only when reported or exactly derivable. Preserve bounds and the missing premise otherwise. An NDA sometime in a two-month interval does not prove eligibility at an intervening deadline. Never calculate an exact non-submitter total by subtracting bids from an inapplicable eventual cohort.

Reconcile named members with anonymous cohorts before adding them; avoid a second entry when a previously anonymous member is named. Distinguish real joint bidding from financing support, rollover holders, common advisers and board changes. Rounds.Bids received counts distinct bidder units, not revised-offer rows. Do not sum Count over all events to obtain participants.

### E5 — processes

Keep the existing continuity/break/fresh-start framework, but make its evidence requirements consistent. Silence about contacts does not prove inactivity. An existing NDA alone does not prove ongoing negotiations. Use supported dates and bounds; do not round an uncertain gap up to the threshold.

Separate reported termination from inferred lapse, and close each earlier participation interval once. If a group/process closure and individual exits describe the same departures, reconcile them rather than double-subtracting. Returning participants enter the new process only if a new process is actually supported.

An uncertain merger-of-equals episode may affect continuity, but does not automatically determine the process count. Preserve an alternative map when the convention or evidence remains unresolved.

### E6 — rounds and finality

Round 1 starts at the earliest supported target-organized sale stage, including substantive bilateral negotiation. A preliminary unsolicited approach alone does not open it. Later broad outreach must not demote a genuine earlier requested-bid stage to round 0.

Count a target-organized solicitation stage once. Admission, common diligence and a later letter specifying that stage’s submission can be steps in one round. Another round requires evidence of a distinct solicitation/selection or materially changed submission basis, rather than merely another document or meeting.

Deliberate effective reopening of rival solicitation after suspension can open another round in the same process. Routine follow-up and an unsolicited individual return do not automatically do so. Use the effective outreach date, distinguishing it from an earlier board authorization.

Keep extensions and repeated bargaining within the round unless a distinct stage is supported. Finality describes the target’s announced or demonstrably instituted procedure. It is separate from which bid was eventually last, and from whether an individual offer satisfies E11.

**Before this rule is finalized:** reconcile Datalink’s retained July/August split, Kraton’s admission/procedure-letter sequence, and Alex’s sTec finality reading. The earlier Datalink adjudication retains January bilateral negotiations; it does not separately settle whether the later admission and letter constitute two rounds. Do not silently revise an accepted map while claiming merely to clarify prose.

### E7 and E8 — dates and ordering

Distinguish initial contact, sending an NDA, executing it, supplying information and reusing an earlier agreement. Inspect annexes for dated execution evidence; reconcile named parties with cohorts.

Keep Date from/Date to as supported source bounds and Sort date as an ordering device. Explain interval/date conventions explicitly. A bid deadline does not prove a response arrived on time. Preserve supported sequence across paragraphs; flag a conflict with reported exact dates rather than moving those dates.

Make Round opened the first row assigned to its new round, sharing the trigger’s supported date where appropriate. This is marker ordering, not evidence that a separate administrative act occurred earlier. It resolves the recurring checker disagreement without fabricating chronology.

### E9 — deadlines

Define a late response as an overdue **required response to the specified solicitation** that the target considered. That may be a first, revised or final response. A negotiated improvement to an on-time submission is not late merely because it follows the original deadline.

Record due dates, bidder-specific extensions, actual response timing, invitations and subsequent decisions before assigning an outcome. Do not infer an invitation solely because banker conversations preceded an increase.

Retain one outcome per reached operative due date. Proposed decision order: explicit extension for that cutoff; otherwise accepted overdue required responses; otherwise a supported Enforced finding; otherwise Passed without action or Unclear. If different bidders have different extensions or responses, preserve the distinction in Notes/Questions. A deadline superseded before arrival is identified as such rather than treated as reached.

Enforced means the target used the specified submission cutoff in taking its next step. It does not claim that all bargaining ended. A missed response and an exit are separate questions.

### E10 and E11 — bids, reaffirmations and formality

Every communicated material revision of price, consideration or bidder commitment is a Bid. Include substantive changes in conditions, funding commitments, reverse termination fees and bidder/sponsor liability even at the same shareholder price. A same-price material revision takes priority over the narrower reaffirmation label. Do not add a price row merely because the agreement was signed.

Bid reaffirmed requires actual bidder confirmation or its own document submission satisfying the existing substantive gate; a target’s assumptions are insufficient. State the supported carried price and classify all other fields with the same date/linkage rule used for revisions.

Retain procedural formality: a priced proposal engaging with a definitive-agreement markup, a response to a genuine final solicitation, or a qualifying bidder confirmation during finalization. A written letter alone, a price range, non-binding language, exclusivity, a condition, or lateness does not decide the label. A final-round label does not make every unsolicited communication a response to that solicitation.

Distinguish express incorporation from inferred continuity. Express readoption can link an offer after a withdrawal to its earlier terms. Later document work alone cannot prove engagement at an earlier bid date. Proposed conservative default: no silent inheritance of Formal without a supported link; if Alex wants a broader document-continuity convention, adopt and flag it explicitly. Penford’s October markup/formality conflict must be reconciled under a general rule.

### E12 and E13 — conditions and consideration

Implement §4 as the single source of the grading definitions; cross-reference rather than restating divergent shortcuts elsewhere. Remove any suggestion in Part A, examples or review guidance that a contingent payment itself causes Heavy or that all Formal bids are ready to close.

Keep upfront-only price, attributed CVR values and filing-reported currency/units. Subtract contingent consideration from a package only when the filing supplies compatible figures and their relationship. Do not subtract a maximum from a package based on a different valuation basis.

Keep separate alternative structures, actual revisions, reversions and same-day order. Preserve market-price/premium references with their own dates and basis. A complete historical stock-price series is a downstream task, not permission for the filing-only extractor to obtain outside data.

### E14 — exits

Check for continuing solicitation, a still-active offer, ongoing diligence or explicit reserve status before inferring departure. Record supported withdrawals/exclusions. Infer closure only when the adopted eligibility/transition conditions hold and the narrative does not carry the bidder forward.

Resolve the conflict between “Did not submit is not necessarily permanent” and a formula that subtracts every such row as an exit. Under the present vocabulary, reserve the exit label for supported closure. Put a missed submission by a continuing participant in the deadline/round account or a material event, without invented exit/re-entry. A dedicated machine-readable non-exit non-submission event would be a separate schema change, not silently introduced here.

Selection for one stage is not necessarily exclusion from every continuing discussion. A whole-company scope exit is not necessarily withdrawal from a partial transaction. Signing closure is not a voluntary withdrawal.

Treat exit actor, timing and reason independently. Preserve the source’s price comparison in the Note even when the inferred exit uses Exit reason = Not stated. Do not infer valuation or an exact exclusion date from disappearance. The previously deferred regulatory-exit taxonomy is not added to this version without a separate decision.

### D4 and F — mandatory review

Keep Alex’s mandatory review items even where the model has a recommended interpretation. Group related rows when that keeps the questions readable; do not create a duplicate question for every repeated instance. Require candidate round/process boundaries, deadline exceptions, unresolved winner/Formal-bidder type, uncertain NDA counts, uncertain exits, adviser affiliation, surprising Formal IOIs, partial-only scope and non-comparable prices to be visible for review.

For the initial v1.14 acceptance exercise, every offer’s condition coding must appear in the review checklist. A grouped review item can cover straightforward rows; material ambiguity requires a specific question. Completion of this checklist by a model is not Alex’s requested researcher verification.

After a correction, reconcile dependent participation counts, round membership, prices, references, deadline outcomes and process totals. The final audit must find omitted source events as well as incorrect existing rows.

## 6. Replacement scope for Questions for Alex

### 6.1 What should stop being an open question

| Current document item | Disposition in the replacement |
| --- | --- |
| Q1: ordinary sequence/count imputation | Extract bounds and uncertainty now. Retain only the analysis-policy question below; do not ask Alex to certify an undisclosed NDA date. |
| Q2: partial-company bidders | Record the whole-company primary definition supported by his Q&A. Ask only if the research intentionally wants an additional alternative-sale measure. |
| Q3: reopened outreach | Adopt deliberate effective reopening as distinct from routine contact. Put the remaining stage-boundary conflicts in Decision 1. |
| Q4: merger of equals | Remove the invented control/premium screen. Retain scope uncertainty; discuss analytical sample treatment only if needed. |
| Q5: revised-offer inheritance | Adopt the common evidence/date rule and express incorporation. Keep only the disputed formality-continuity convention in Decision 2. |
| Q6a: five weeks of exclusivity | Correct the inference: exclusivity duration does not establish required substantive diligence. No need to ask whether an unreported fact occurred. |
| Q6b: financing/Kraton | Replace blanket Light/Heavy recommendations with offer-specific source coding. Draft letters and later signed terms are not enough. |
| Q7: deadline enforcement | Adopt the required-response definition in §5, preserving later bargaining. Escalate only a genuinely different research definition. |
| sTec H confirmation | Record supported target-side nonadvancement with bounded timing and preserved price feedback; keep the uncertainty. |
| sTec D confirmation | Continuous participation is supported through the express withdrawal. Treat as a correction, not an unanswered convention. |
| Penford A confirmation | October 4 threshold is not a bid; October 14 is a definite offer. Keep October 13 as a small case-adjudication item because the wording supports competing readings. |
| CVR-to-Heavy | Remove from the proposed open list: Austin has accepted no automatic Heavy trigger. Show the adopted rule in the settled-decisions section. |

### 6.2 Three decision groups worth putting in front of Alex

**Decision 1 — one solicitation stage versus another round, and the meaning of finality.** Present the exact Kraton and Datalink admission/letter sequences and the sTec final-round language alongside Alex’s reading. Recommended general rule: count one organized stage once; let explicit target-announced final solicitation establish Announced as final, while preserving later deviations. Ask which general distinction justifies any different map. This needs resolution before presenting the new round convention as jointly settled.

**Decision 2 — how much documentary linkage is enough for Formal.** Recommended: current procedural evidence or express incorporation supports the label; unsupported continuity does not. If Alex wants continuity inferred from an established document track, define the required evidence and mark the inference. Use the Penford earlier-markup/October 14 conflict and the G&W July revision/August document sequence as the concrete tests. This is a convention question, not a request to change source dates.

**Decision 3 — what the analysis needs when the source cannot supply a point or a clean scope.** Determine whether the intended estimator can use bounds/unresolved membership. If a point is required, specify separate assumptions for membership, timing and independent bidder units. Also declare how it treats partial alternatives, ambiguous mutual-combination talks, Formal/Heavy and Unclear. Recommended extraction policy remains unchanged; recommended analysis output preserves alternative results rather than hides assumptions in the ledger. This does not block producing the instruction candidate, but it does block claiming an agreed estimation input.

Keep Penford October 13 and any remaining deal-specific ambiguities in a short source-review appendix. Do not turn every unknown into a policy question. Austin can approve the conservative defaults without a new question to Alex; discrepancies with Alex’s explicit prior readings should still be shown transparently before calling the integration jointly reconciled.

The proposed replacement DOCX should contain: adopted decisions; the three decision groups with source excerpts and consequences; a short case appendix. Preserve the September 24 original. Preparation of the replacement can follow approval; uploading it to Dropbox or sending it to Alex is a separate action.

## 7. Pipeline work beyond the instruction

### 7.1 What already exists

The September 24 v1.14 draft and two pilot extractions exist. The checker already recognizes the 29-column schema using Stock %, validates the new codes and enforces some cross-field rules. The cockpit already offers the new choices and converts numeric Stock % and CVR values. These are additions to refine, not components to rebuild.

Current code inspection confirms:

- [check_lean.py](/home/uctpiaj/work/Projects/sec-extraction/_dev/tools/check_lean.py:584) checks bid terms, forces Contingent financing to Heavy, and checks necessary None combinations. Antitrust paired with an incompatible Regulatory value is currently only a warning.
- [workspace.py](/home/uctpiaj/work/Projects/sec-extraction/_dev/tools/cockpit/workspace.py:409) returns immutable version bytes unchanged; a working export renders changed state. Preserve that raw-download contract.
- [test_cockpit_workspace.py](/home/uctpiaj/work/Projects/sec-extraction/_dev/tools/test_cockpit_workspace.py:118) covers new-field coercion and choices, but that focused test is not a complete v1.14 import/edit/export exercise.
- [worker.py](/home/uctpiaj/work/Projects/sec-extraction/_dev/tools/cockpit/worker.py:307) proceeds from completed extraction to checking and import. Its import preserves run receipts and instruction/filing hashes. It does not stop for a researcher to approve the process map.

The earlier handoff’s test and deployment results describe that earlier build. This document does not claim a fresh full test run or current live-service acceptance.

### 7.2 Required work, in priority order

| Priority / component | Concrete work | Completion evidence |
| --- | --- | --- |
| **P0 — instruction/checker agreement** | Update the candidate and checker together for adopted codes, Other-scope price handling, metadata allowance and true cross-field contradictions. Make the explicit Antitrust/Regulatory prerequisite an error. Enforce Concern-to-Heavy if its narrowed definition above is adopted. Preserve v1.13.2 compatibility. Do not add a CVR-to-Heavy check. | Positive/negative fixtures for contradictions; both schemas still load. Necessary None conditions must not be advertised as sufficient source proof. |
| **P0 — cockpit round trip** | Verify import, edit, save, reload and export of all new columns, dates, blanks, Varies, ranges and numeric values. Preserve review attribution, references and raw versions. Change code only where this exercise reveals an actual gap. | A representative v1.14 fixture survives the complete path with semantic equality; editing a working copy leaves original bytes and hash unchanged. |
| **P0 — source review and pilot repair** | Apply separately approved corrections in new controlled versions; adjudicate convention-dependent rows first. Inspect all changed and dependent rows, plus omitted material source events. | Source-backed correction ledger, full cell/event diff, count/round/reference reconciliation, mechanical check, researcher condition review and explicit remaining issues. |
| **P1 — usable delivery provenance** | Add a derived review export/package containing the original SEC URL and run provenance. Obtain them from existing catalog/manifest/run metadata, never a model guess. Preserve the existing raw download. | Source link resolves to the recorded filing; file/instruction/raw-output hashes match receipts; enriched workbook and its manifest identify the base version and working revision. |
| **P1 — Alex’s early review checkpoint** | Implement the staged assisted workflow below. Existing after-the-run review cannot meet this request on its own. | Durable review state, attributed decisions, resumable jobs, cancellation/restart tests, clear assisted labels and source access. |
| **P1 — analysis contract** | Define counts and bounds, independent bidder units, partial scopes, eligibility versus admission, treatment of Unclear, and the chosen formality/condition transformation. | Same ledger reproduces each declared analysis policy; assumptions are inspectable and do not replace source fields. |
| **P2 — market-data supplement** | Supply the changing target-price series Alex requested through a separate authorized downstream data join. Keep filing-reported price references in the extraction. | Named source, identifier/date/currency/adjustment conventions, reproducible join and clear separation from the filing evidence. |
| **Rollout — documentation and production verification** | Refresh current handoff, questions register and version status; after a requested deployment, verify the loaded checker/UI against the tested artifact and confirm required account/published-version flows. | Current navigation no longer describes obsolete questions as pending or a draft as adopted; any service restart waits for no active jobs. |

P0 items are needed before claiming the new instruction works with the pipeline. P1 provenance and review workflow are needed to fulfill Alex’s broader usability and collaboration requests. The market-data supplement is part of his research request but need not block a correctly scoped filing-only v1.14 release.

Preserve historical checker receipts. A recheck under revised rules is a new result, identified by checker version and the workbook’s instruction hash; it must not silently replace the earlier validation record or rewrite the raw values. A new finding on an older draft is a review item, not automatic permission to alter it.

**Provenance design to implement:** append delivery-only Deal facts fields named Source SEC URL, Source filing SHA-256, Instruction version, Instruction SHA-256, Raw workbook SHA-256, Run/version ID, Working revision, and Review status. Unknown metadata stays explicitly unavailable; do not infer it from a filename. A sidecar manifest records the derived export’s own hash, avoiding a workbook containing its own hash. Update validators/readers for these reserved delivery fields while allowing historical raw workbooks. Do not rewrite an immutable model output to add them.

**Likely files:** `_dev/tools/check_lean.py`, `_dev/tools/test_check_lean.py`, `_dev/tools/cockpit/workspace.py`, `_dev/tools/test_cockpit_workspace.py`, and the relevant export/data/HTTP tests. The assisted workflow additionally affects worker/job state, API and frontend review screens. Resolve exact implementation locations against the current tree before editing; unrelated existing changes must be preserved.

### 7.3 Assisted map review: a separate workflow deliverable

Use two completed stages rather than parking an active model call while waiting for a person:

1. Produce the event inventory, proposed process/round map, cohort reconciliation and material ambiguities from the filing and frozen instruction.
2. Persist that artifact and enter an explicit awaiting-review state. Show relevant source passages with each decision.
3. Record Austin/Alex’s accept/reject/alternative decisions, actor and time. Preserve unresolved choices; do not let “approve map” silently answer them.
4. Start a completion stage with the frozen instruction, filing, map and explicit reviewed decisions. Record each input and its hash.
5. Check, import and review the completed ledger, including whether the accepted decisions were followed and what new uncertainty arose.

Label this output assisted, with its actual inputs. Keep ordinary blind evaluation restricted to one instruction and one filing; do not compare an assisted result against a blind result as if both measured blind accuracy. Test state transitions with fixtures/stubs before any authorized paid model run.

### 7.4 Existing extractions need their own correction pass

Improving v1.14 cannot repair an existing workbook. The reviewed pilot findings include the following concrete work; this is a correction scope, not a claim it has been applied:

| Pilot | Source-backed correction or decision required |
| --- | --- |
| Mac-Gray | Remove the unsupported use of an eventual 16-party non-submitter cohort as exact July-deadline eligibility. Preserve the evidence and bounds. |
| Mac-Gray | Add the omitted material same-price commitment packages: September reverse-fee/financing terms and October sponsor-liability changes. Distinguish the target’s later exclusivity requirement from a bidder’s proposal. |
| Mac-Gray | Remove backward use of later diligence/financing evidence in earlier offer rows; reassess Party B’s September financing under the common evidence rule. Keep its CVR and attributed value without using the CVR itself as Heavy. |
| Mac-Gray | Correct unsupported specific reasons on inferred exits; repair same-day round-marker order; reconcile affected Questions and Rounds. |
| Providence & Worcester | Add the April 3 G&W NDA supported by the annex, without assuming unproven cohort membership or double-counting entry. |
| Providence & Worcester | Preserve material price/CVR feedback and assess July revised-offer/document linkage under the approved formality rule. |
| Providence & Worcester | Remove the use of later signed financing evidence in the earlier August 12 offer unless earlier applicability is established. |

Pilot identifiers are `mac-gray/opus55-medium-20260924-2241-d7d267` and `providence-worcester/opus55-medium-20260924-2241-38bc24`. Preserve both raw versions. Earlier wider-review findings, including Meredith’s scope treatment and other outstanding adjudications, remain a separate backlog; correcting these two pilots does not certify every deal.

## 8. Coverage of Alex’s voice notes and related instructions

“Specified” below means this plan provides a route to satisfy the concern. It does not mean the implementation or researcher review is complete.

| Concern | v1.14 or pipeline response | What still establishes completion |
| --- | --- | --- |
| Real-time collaboration | Persisted map-review checkpoint before completion (§7.3). | Working assisted flow and actual reviewer decisions. |
| A: possible round boundaries | Candidate boundaries, selection meetings and alternative maps visible under E5/E6/F. | Reconcile the specific convention conflicts and inspect source coverage. |
| B: deadline extension/non-enforcement | E9’s required-response rule, operative due dates and preserved later bargaining. | Review source timing, especially uncertain arrival/invitation evidence. |
| C/D: unknown winner or Formal-bidder type | Whole-filing search and mandatory flag if unresolved. | No unsupported type assignment; review the remaining unknowns. |
| E: uncertain NDA counts/type splits | Bounds, cohort membership checks and separate eligibility/admission. | No fabricated point count or duplicated named cohort member. |
| F: uncertain exit actor/reason | Independent actor/time/reason treatment; continuing-participation check. | Source-supported exits and visible unresolved interpretations. |
| G: initial verification of conditions | Every pilot offer enters the condition-review checklist; new taxonomy and explicit grading. | Austin/Alex review, beyond model agreement. |
| H: order before artificial precision | Source bounds, separate Sort date, deterministic marker order. | Date/order conflicts remain visible rather than invented away. |
| I: signing and announcements | Preserve separate reported events and dates. | Verify both against sources; no automatic duplication or inferred announcement. |
| J: adviser duplication/affiliation | One relationship/event as appropriate; name continuity and uncertain-client flags. | Resolve or retain affiliation uncertainty; distinguish genuinely different clients. |
| K: IOI versus offer | One offer communication; procedural formality; flag surprising Formal IOIs. | No duplicate IOI/Bid and no letter/range shortcut. |
| L: partial-only transactions | Explicit scope and sample flag; partial alternatives retained separately. | Research sample policy and source-supported scope intervals. |
| M: incomparable prices/currencies | Preserve units, EV/equity distinctions, upfront/CVR bases and Questions. | No invented conversion or comparable per-share value. |
| Contacts, NDAs and annexes | Separate acts and full-filing supplementation. | Source-to-ledger review catches omitted dates/events. |
| Groups and distinct bidder counts | Reconcile economic bidder units, actual consortium formation and repeated bids. | Analysis never sums bid revisions as distinct bidders. |
| Feedback and information differences | Material target feedback/information events survive routine-event exclusions. | Check omissions, not merely quotations on existing rows. |
| Revisions with unchanged prices | Commitment changes count as bids; one evidence rule for revisions/reaffirmations. | Same-price funding, fee and liability changes retained with supported timing. |
| Failed/restarted processes and go-shop | Separate continuity, termination, restart and post-signing activity. | Scope/time evidence supports the maps; analysis separates post-signing competition. |
| Market prices across the process | Keep filing references and add a separate downstream series if authorized. | Reproducible external-data join, not invented filing facts. |
| Direct access to original evidence | Source passages plus SEC URL and provenance in the derived delivery. | Export remains usable outside the cockpit and identifies its source/version. |

## 9. Acceptance criteria

### 9.1 Instruction consistency

Before calling the candidate ready:

- Check A–F for one definition of Formality, Conditions, scope, participation and date applicability. Remove the replaced shortcuts rather than adding exceptions around them.
- Ensure D1 choices, E12/E13 prose, examples, checker values and cockpit choices agree.
- Verify that unknown is never used as a negative, regulatory silence as No concern, or not-Heavy as Light.
- Confirm every Heavy example names H1, H2 or H3; CVR and exclusivity cannot slip back through a general catch-all.
- Confirm the same evidence rule applies to price changes, same-price commitment revisions and reaffirmations.
- Document each research decision or explicitly unresolved choice. No hidden deal-specific exceptions in the instruction.

### 9.2 Source cases and software checks

Keep source cases in the evaluation packet, outside blind extraction inputs. The detailed source citations are in [RECOMMENDATION_REVIEW.md](RECOMMENDATION_REVIEW.md).

| Case/check | Required invariant |
| --- | --- |
| Mac-Gray NDA interval | Eventual membership is not exact deadline eligibility. |
| Kraton July 6 | Exclusion from a selected solicitation does not erase an alternative still under consideration. |
| Synacor E’s scope change | Whole-company withdrawal differs from continued partial-stake negotiation. |
| Synacor/Datalink renewed outreach | Effective reopening is distinct from board authorization and routine contact. |
| Kraton and Datalink admission/letter sequences | One stage is not counted twice without an adopted basis. |
| WDC June readoption | Express linkage carries applicable terms, not stale diligence progress. |
| G&W July/August document sequence | Later work does not silently become earlier contemporaneous proof. |
| Penford later exclusivity request | Earlier offer remains a snapshot at its date. |
| Synacor five-week request | Exclusivity duration is not required substantive-diligence duration. |
| Kraton financing sequence | Draft documents and subsequent signed terms do not decide all earlier offers. |
| Mac-Gray same-price packages | Material commitment changes survive legal-negotiation exclusions. |
| sTec D and H | Continuing participation prevents fabricated exits; uncertain actor/date/reason remain distinct. |
| Penford October 4/13/14 | Negative threshold, ambiguous proposal and definite offer are distinguished. |
| Otherwise identical offers with/without CVR | Same Conditions result; the consideration fields change. Test all supported grades, not just Light. |
| Otherwise identical offers with/without exclusivity | Same Conditions/Formality unless a separately supported substantive fact changed. |
| Cohort with two contingent and three unreported | Partial evidence is not assigned to all five; no false common Heavy or Committed value. |
| Temporal evidence check | Moving the commitment’s applicability to after the bid removes support for Committed at that bid. |
| Full workbook round trip | Numbers, ranges, blanks, unknowns, dates, flags and references survive import/edit/export. |
| Backward compatibility and provenance | Old raw workbooks remain readable; immutable bytes and receipt hashes remain unchanged. |

Mechanical checks validate structure and explicit cross-field implications. Source judgments require source review; a regex in a Note cannot certify them. A clean checker report, exact quotation, label match or agreement among reviewers is not research acceptance.

Fresh blind runs, if later requested, must use an approved frozen candidate and record the precise inputs, model and requested effort. Use a bounded set containing both known difficult cases and a held-out case before making a claim about general extraction quality. Do not use an assisted correction as evidence of blind improvement. No such runs are launched by this specification.

### 9.3 Research acceptance of corrected data

Require a complete diff against the preserved raw version, evidence for every material correction, reconciliation of dependent fields, an account of remaining/new material issues, and the intended researcher review of condition coding. Keep execution status, mechanical validation, source review and researcher acceptance separate in the record.

## 10. Concrete approval scope and order of work

**Recommended first approval: Package A — prepare the revised local candidate and align its supporting software.** This covers:

1. Revise the separate v1.14 candidate under `_dev/maintenance/2026-09-24-bid-terms-taxonomy/`, preserving the reviewed September 24 baseline and a full diff. Keep unresolved researcher decisions identified; do not silently overwrite an earlier adjudication.
2. Prepare the replacement Questions for Alex DOCX locally, with the settled list, three decision groups and case appendix. Render and inspect it before delivery.
3. Implement the bounded checker/schema and cockpit round-trip fixes, plus the derived provenance export described in §7. Preserve existing unrelated work and raw-download behavior.
4. Run the targeted mechanical/round-trip tests and perform the document/source-case consistency review. Record failures, outstanding decisions and the candidate hash.
5. Refresh the current local handoff/questions register to describe candidate status and the actual remaining work.

Package A produces a reviewable candidate and tested local support. It does not claim that the unresolved choices have been answered, deploy the changes, or replace the frozen repository instruction.

**Package B — controlled data corrections and researcher review.** Apply the approved rule/source corrections to separate versions of the two pilots, perform complete change verification and obtain the intended condition review. Scope any wider-deal corrections explicitly. This remains necessary even if the next blind run performs well.

**Package C — assisted review workflow.** Build and test §7.3 as a distinct app feature. It is required to fulfill the early-collaboration request, but does not have to be mixed into the instruction rewrite or its first offline tests.

**Package D — analysis and market-data work.** Resolve Decision 3 and implement only the declared downstream transformations/data join. This is not a request to build an unspecified estimator.

**Release actions, once separately requested:** deploy tested software with active-job protection; run the authorized evaluation set; publish the approved instruction and change the default if requested; export to the repository through the project’s prescribed route for a requested commit; re-extract only the specified deals. Dropbox replacement, sending material to Alex, root frozen-instruction replacement, real model runs, publication/default changes, commits and pushes are not performed by this document or bundled into Package A.

The order is: **resolve the instruction’s internal conflicts → test its local software contract → correct/review the evidence cases → evaluate requested runs → adopt the release**. The assisted workflow and analysis work can proceed as separately authorized packages. This keeps “v1.14 written,” “pipeline supports it,” and “research data accepted” as concrete, different milestones.

## 11. Sources, review record and boundaries

Primary material: the frozen instruction; September 24 v1.14 draft; Alex’s collection instructions, voice notes and August Q&A; the September 24 Questions for Alex file from Austin’s September 22 Dropbox submission; and the relevant local SEC filings. The [source manifest](sources/manifest.json) records the captured document hashes. The [earlier integration memo](/home/uctpiaj/work/tmp/sec-v114-alex-integration-2026-09-25.md) provides the broader concern mapping.

Five focused Astra reviews in this conversation examined counts/scope, rounds, inheritance/formality, conditions, and deadlines/case confirmations, using higher effort for difficult source judgments. Their findings were reconciled against sources rather than treated as votes. Earlier pilot/code reviews inform §7.4. This specification is a consolidation, not a fresh extraction or proof that all filings have now passed a complete acceptance audit.

Pinned baselines:

| Artifact | SHA-256 |
| --- | --- |
| Frozen repository instruction v1.13.2 | `513c8e3e8159e4a6bceccd6ffca32a246302736329a0c7137b64dd3b7ffcd304` |
| September 24 v1.14 draft | `f9595d7413149f86c074f1d4b9ef96a5a24b3d8dd9b6c11061b0bd6e889aea97` |
| Current September 24 Questions for Alex DOCX | `faab1d66d13a1053c2816a8aaed371c3caf49b6733a9005a4e0e949e12ed5220` |
| Alex August voice notes DOCX | `9ddb0a38f3ffcabdbf7693ced379df3aa8b53a1c4d065990d09d57978af220fb` |

No operative instruction, extraction workbook, cockpit state, pipeline code or Dropbox content was changed to prepare this specification. No extraction, deployment, publication, default change, commit or push was performed. The concrete artifact produced here is this approval specification.
