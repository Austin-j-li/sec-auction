# SEC merger-auction extraction instruction

**Research:** Informal bids, information, selection and competition in corporate takeover processes — Austin Li and Alex Gorbenko  
**Version:** 1.0 — proposed pilot specification, 18 September 2026  
**Use:** Attach this instruction and a new deal filing to an interactive model session. This document is sufficient to perform the extraction; its development materials and companion decision note are not required.

## 1. Your assignment and the deliverable

Read the supplied filing and produce a complete, evidence-linked first-pass reconstruction of the target's sale process. Make the best-supported assessment of every judgment-dependent field. Do not substitute a list of questions for an extraction, and do not fill disclosure gaps with invented facts. A reviewer must be able to see **what happened, who was involved, when it happened, what you concluded, why, and what remains uncertain**.

The research concerns how potential acquirers enter, obtain information, submit and revise informal and formal proposals, advance or cease participating, and ultimately agree a transaction. Preserve the target's choices about admission, disclosure, deadlines and negotiation, and the bidders' stated reasons for their actions. These features matter independently of the winning price.

Deliver one Excel workbook with the ten tables in Section 12, or an equivalent set of UTF-8 CSV files. The main review surfaces are **Deal, Events, Bids and Review**; the other tables support them. Also provide a short plain-language process summary and a validation report. When file-generation tools are unavailable, provide complete, separately labelled CSV blocks with the same schemas. Do not claim to have created a file without actually creating it. Never silently truncate a table: declare the remaining records and continue in a labelled subsequent part.

Read the entire background before finalizing local interpretations. Where available, also inspect the filing's descriptions of the merger parties, transaction summary, agreement terms and other sections needed to resolve the acquirer, consideration or transaction dates. Do not require external databases or unrelated filings. If only an excerpt is supplied, identify that limitation and distinguish **not available in the supplied source** from **not disclosed anywhere in a complete filing**.

**Terminology:** an NDA is a non-disclosure/confidentiality agreement; an IOI is an indication of interest; an LOI is a letter of intent. Due diligence is the bidder's investigation of the target. A markup is a party's proposed edits to draft transaction documents, not necessarily an executed agreement. A standstill restricts specified acquisition-related actions under its terms; its existence is distinct from confidentiality. Equity value concerns shareholders' interests; enterprise value concerns the business before the relevant debt/cash and other equity-bridge adjustments. A go-shop is a supported post-signing opportunity for solicitation of competing proposals. These terms describe different actions and rights; their mere appearance does not determine the research coding.

### 1.1 Authority and working conventions

This specification carries forward the research requirements to collect initiation, advisers, executed bidder confidentiality agreements, whole-company proposals, bidder characteristics, selection and exits, analytical rounds and deadlines, conditionality, earlier sale attempts, execution and public announcements. Later clarifications allow a formal offer to have conditions or a price range; formality is not a synonym for legal enforceability.

Some operational choices below are recommendations, not previously approved instructions from Alex. Use them for a **provisional pilot extraction** unless the researcher supplies an override. Record the policy version. Do not represent the use of this document as approval for estimation or production deployment.

| Policy | Working default in this version | Status |
|---|---|---|
| C1 — Anonymous groups and prices | Preserve unidentified cohorts and group price envelopes without manufacturing individual bid ranges or persistent identities. A legacy expansion, if requested, must distinguish inferred bounds from actual bidder-submitted ranges. | Proposed replacement for the older literal expansion/copy-the-range convention; requires research approval before treating the new representation as final. |
| C2 — Dates | Store ISO dates, retain source wording, supply a U.S. date display, and distinguish representative dates from reported dates. Use the approximate-date rules in Section 7. | Recommended implementation of the requirement to preserve chronology without false precision. |
| C3 — Conditionality | Assess material completion/repricing exposure as none, light, heavy or not assessable, separately from consideration uncertainty and exclusivity. | Alex requested a compact conditionality classification; the operational thresholds here are recommended. |
| C4 — Identity and bidder type | Use business, ownership and acquisition-role evidence, not a CEO title alone; private-equity ownership does not automatically make an operating-company acquisition financial. | Proposed replacement for the older CEO-based shortcut; retain unresolved classifications for review. |
| C5 — Coverage versus analytical inclusion | Retain genuine whole-company proposals made before an NDA; keep partial proposals and rejected preliminary approaches in clearly excluded context records where necessary to explain the process. | Recommended clarification. Do not infer a universal exclusion rule from one historical deletion comment. Confirm the estimation sample separately. |
| C6 — Exclusivity and exits | Record target-driven displacement or suspension separately from a bidder's permanent withdrawal. Do not erase a prior non-submission or infer an exit date from the eventual signing alone. | Recommended evidentiary refinement of target-driven dropout coding. |
| C7 — Review delivery | Preserve mandatory verification categories, but group related flags into decision packets and complete the provisional first pass. | Recommended review arrangement; not permission to waive Alex's required checks. |

Create at most one policy-confirmation item for the relevant proposed defaults, rather than asking for the same convention on every affected row. Subsequent explicit researcher decisions override these defaults and must be recorded, not silently retrofitted into the original model assessment.

## 2. Evidence, uncertainty and judgment

### 2.1 Separate four different things

| Evidence basis | Meaning | Example |
|---|---|---|
| `reported` | The filing expressly states the fact, including any qualification. | A bidder submitted a $20 offer on a stated date. |
| `contextual_inference` | The conclusion follows from identified contextual evidence, but is not expressly stated. | An unlabelled final negotiation phase began when the board selected a bidder and directed finalization of a definitive agreement. |
| `calculated` | Arithmetic or a transparent transformation of sourced inputs. | Twenty executed bidder NDAs minus four identified signers leaves sixteen unidentified signers in the same population. |
| `research_convention` | An analytical label or assigned value under this instruction. | A non-binding proposal with bidder-submitted merger markups is assessed as formal; an approximate interval receives a representative date. |

A single row may contain a reported price, an inferred round assignment and a convention-based formality assessment. **Do not give the entire row one evidentiary status or one confidence score.** Use field-specific entries in Evidence. A reported statement is evidence that a party said something, not proof that its economic claim is true: an assertion about financing, synergies or valuation remains attributed to its speaker.

For every nontrivial judgment record the assessed value, a concise reason, supporting locations, confidence (`high`, `medium`, `low`) and any consequential alternative. High confidence means strong support, not immunity from verification. These are qualitative assessments, not calibrated probabilities.

Reasonable inference is expected. For example, substantive diligence plus unsecured funding needs can support heavy conditionality even when the text does not use that label. Conversely, silence about financing does not establish that financing is assured. Use `indeterminate` or `not_assessable` only when the evidence genuinely cannot sustain the required classification; explain the remaining uncertainty and give a preferred interpretation where one is defensible.

### 2.2 Source locators and quotations

Use the supplied paragraph identifiers. If none exist, assign stable identifiers to the complete supplied background in source order, including short numbered paragraphs and bullet items. Record the printed filing page separately from the PDF page index. Do not invent an SEC accession number, URL, page number or paragraph identifier that cannot be established from the supplied material.

Each substantive record must link to Evidence entries containing: source filename or document identifier; section; printed page, if available; paragraph or line locator; and a short exact supporting quotation. For cross-paragraph inferences, include every material premise and explain the inference. A quote must support the particular field being claimed, not merely mention the same bidder. Use separate evidence entries for different quotations; do not splice passages into a purported single quotation.

Verify quotations against the source. Preserve errors in quoted text, while recording a proposed correction separately. Do not cite a later summary as proof of an earlier precise event date. Links should lead to the actual filing or local source; when a page anchor cannot be verified, provide the document link and an explicit page/paragraph locator rather than a fabricated deep link.

### 2.3 Missingness

Use empty numeric/date cells with a corresponding status; never use zero to mean unknown. Use these status values where relevant: `known`, `not_disclosed`, `not_in_supplied_material`, `ambiguous`, `conflicting`, `not_applicable`. `Not_disclosed` does not mean no. For a categorical judgment, a best-supported inferred value may be present even though a directly reported value is unavailable.

Absence of a later named mention does not prove a bidder's identity, withdrawal, or round of exit. A document's general incompleteness is not a reason to withhold clear facts that it does disclose.

## 3. Coverage and analytical eligibility

### 3.1 Target and transaction scope

The core bid dataset covers proposals to acquire the whole target company, not a business segment, selected assets, a minority stake, or an unrelated company that the target considered buying. A bid for all equity can remain a whole-company proposal despite share rollover: rollover changes how some owners are paid, not necessarily the scope acquired.

Distinguish `whole_company_equity`, `whole_business_assets`, `segment_or_selected_assets`, `minority_or_partial_equity`, `combination_scope_unclear`, and `not_an_acquisition`. Whole-business asset transactions require a comparability assessment; they are not automatically equivalent to an offer for the listed target's common shares. Keep excluded-context records only when useful for explaining initiation, exclusion, alternatives or the transaction's scope. Clearly set `core_bid_eligible=false` and explain why; never combine them with comparable whole-company bids in totals.

Flag a deal with only partial bids or a contemporaneous spin-off that prevents observing a comparable whole-company price. Do not manufacture a market price for an unlisted segment, sum-of-parts equity price or acquisition premium. Retain descriptive information, and classify estimation eligibility as excluded or requiring a research decision. A spin-off completed materially before a subsequent acquisition is a different question: establish which company and shares each offer concerns rather than imposing a universal rule.

A historical effort by the target to acquire another firm is context, not an earlier attempt to sell the target.

### 3.2 Auction status is not the same as extraction scope

Apply the research screening criterion: **multiple distinct potential acquiring bidder units executed confidentiality agreements for the relevant sale process**. Exclude adviser, lender-only and rollover-holder agreements and agreements belonging solely to stale processes. Record the supporting count and whether it is reported, inferred or uncertain.

Use `auction_screen=meets_criterion|does_not_meet_criterion|uncertain`. Do not infer multiple NDA signers merely from multiple bids or multiple consortium members. If an old agreement was expressly relied upon in the current process, record that reuse and flag the treatment of current NDA participation; do not silently count it as a newly executed agreement.

Continue extracting a supplied case that fails or cannot establish the screen, marking its eligibility. Do not discard initiating offers, genuine pre-NDA proposals or diagnostic context merely to force the case to fit the screen. Extraction is not sample approval.

## 4. Parties, bidder units and relationships

### 4.1 Stable identities and types

Create stable IDs for the target, relevant boards/committees, bidders, bidding groups, financial and legal advisers, relevant shareholders/activists, financing providers and material acquisition vehicles. Do not enumerate every director or lawyer unless their individual role matters. Keep the exact disclosed name and aliases. “Parent,” “Merger Sub,” the operating acquirer and the sponsor may be different legal entities within one economic acquisition; identify their relationships rather than blindly merging every name or counting each as a competitor.

A **bidder unit** is the economic participant submitting a proposal independently at that point in time. Several financial sponsors submitting one joint proposal constitute one bidding unit, not several competing bids. A sponsor-backed operating company pursuing an industry acquisition can be strategic. Preserve both the operating-company role and sponsor backing. `Strategic`, `financial` and `mixed` are not substitutes for public/private status, domicile or transaction vehicle type.

Assess `bidder_type=strategic|financial|mixed|unknown`, with reason and source. Use `mixed` only for a genuinely joint strategic/financial acquisition role, not simply because a strategic buyer has a lender or a private-equity owner. Record ownership status (`public`, `private`, `unknown`), country if disclosed, and `non_us` only when determinable. A CEO title or a reference to “strategic alternatives” alone is insufficient. Do not infer cash consideration from financial-bidder status.

Resolve the winner and formal bidders using the rest of the supplied filing where necessary. Always flag an unknown winner or formal-bidder type after that search. Do not guess the identities of anonymized losing bidders using outside memory.

### 4.2 Anonymous individuals and cohorts

A disclosed “Party A” is a stable actor even when its real name is unknown. An unnamed but distinguishable individual may receive an ID such as `U001`. A group whose members cannot be individually distinguished must receive a **cohort ID**, not invented individual histories. Cohorts belong to a defined population and time/stage; they are not themselves one bidder.

For “20 NDA signers, including A, B, C and D,” the total already includes those named parties. Record the identified members and the residual cohort. If two signers are strategic and those two are identified, do not also create two anonymous strategic signers. Never link an anonymous early bidder to a later anonymous bidder solely because the numbers fit or the filing stops naming someone.

Keep alternative identity mappings when they affect selection, bidder type or round participation. An exact aggregate count may coexist with uncertain identities. Conversely, exact identities at a later stage do not establish an earlier total when population overlap is unclear.

### 4.3 Relationships and adviser engagements

Record who advises whom, who sponsors or controls an acquisition vehicle, who belongs to a bidding group, who supplies financing, and who proposes or agrees to roll over existing shares. Date material relationship changes and distinguish requested, authorized, executed, withdrawn and merely discussed arrangements.

An equity rollover is **not automatically consortium formation**. Nor are a shareholder NDA, a financing-support letter, shared counsel or a board appointment. A statement that bidder F supports bidder E's financing does not, without more, establish a jointly controlled E/F bid. Record financing support first; assess joint bidding separately.

Preserve changes in bidding partners over time. Do not rewrite earlier bids under the name of a later consortium. When former bidders join a group, retain their individual early histories, link them to the later group, and avoid counting group members again as additional independent competitors at the same stage.

For advisers, use one actor identity but retain genuinely different engagements. Separate earliest observed service, selection/authorization, and execution of an engagement letter. A long-standing lawyer's first appearance is not a newly observed retention. A bank's acquisition or renaming does not automatically create a second advisory relationship. Conversely, an old mandate's termination and a new mandate's execution are real changes, not duplicate mentions to delete. Record the primary target financial adviser if identified, otherwise all, and collect disclosed legal advisers with their clients. An unclear client affiliation requires review.

## 5. Initiation, information and process structure

### 5.1 Reconstruct the initiation chain

Do not force the entire deal into a single target-initiated/bidder-initiated label prematurely. Distinguish a target's preliminary approach; a bidder's unsolicited interest without an acquisition proposal; a submitted proposal that helps trigger active sale exploration; board authorization to explore a sale; authorization to announce that exploration; the actual public announcement; and activist pressure or more qualified activist involvement.

A board can authorize exploring a sale while retaining the option to remain independent. Describe that accurately, not as an irrevocable decision to sell. A subsequent proposal described as “unsolicited” may follow earlier target outreach; preserve both facts. A shareholder that merely supports considering a sale is not necessarily the cause of the sale process. Record `initiation_assessment=target_led|bidder_led|activist_influenced|mixed|uncertain` as a summary of the documented sequence, with reasons and alternatives rather than replacing the sequence.

Capture the first sale-related contact and its direction. If a first contact includes a proposal, one proposal event may carry the initial-contact and initiation roles; do not create two supposed submissions. A view corresponding to the legacy “Bidder Sale” label can reference that same proposal. Keep a public disclosure of the proposal as a separate event.

### 5.2 Earlier processes and resumed discussions

A process is a continuing attempt to sell the relevant target, potentially containing several rounds. Identify earlier attempts where the filing describes them. Separate cessation of an entire process from a single bidder's withdrawal or termination of a signed merger agreement.

An explicit abandonment followed by a fresh launch can support a new process. A substantial dormant interval plus renewed acquisition activity can also support that interpretation, with contextual reasoning. There is **no fixed three-month, nine-month or other gap rule**. Renewed contacts immediately after exclusivity expires, with the incumbent still active, usually represent continuation, not automatic restart. Do not infer that every historical NDA belongs to the current process. Every proposed multi-process segmentation receives a grouped review item.

### 5.3 Analytical rounds

A round is a target-organized solicitation, evaluation or negotiation phase with a reasonably coherent participation set and submission objective. It need not be called a round in the filing. Use one consecutive `round_number` within each process and a stable `round_id`. Keep the filing's own stage name separately. Do not introduce a competing `round_count` label on event rows.

Assess a new round when the target makes a substantive transition: selects parties to advance and requests updated proposals; opens a distinct information/diligence stage linked to new offers; or moves from preliminary evaluation to final definitive-agreement negotiation, even with only one bidder. Multiple informal rounds can precede a formal round. The banker's “second round” need not be analytical round 2.

Do **not** create a round solely because another bid arrives, a board meets, a deadline passes, one bidder gets more time, the same finalists are asked to improve their prices, or exclusivity follows an already established final round. These are boundary candidates to assess and flag, not mechanical triggers. A price-improvement extension can remain within the same final round. Explain why a borderline transition is or is not a new round.

Record both the decision authorizing a stage and the observed implementation where they differ. For round 1, use an explicit operative launch if present; otherwise use the first actual target/adviser sale-directed outreach as the working default. A definite board authorization of an organized solicitation can establish its operative launch even when the contacts are implemented afterward; explain that launch assessment rather than redating the contacts. A vague strategic review or authorization for contacts months later is not automatically the operational start. In a bilateral case with no outreach campaign, use the first substantive sale negotiation and explain the adaptation. Retain meaningful pre-launch approaches and proposals with `round_assignment=pre_round` rather than altering their dates to fit round 1. An initial proposal may later be considered in round 1: record that evaluation link without falsely redating or resubmitting it.

Assign proposals to the phase they actually respond to, using process letters, invitations, information access and substantive purpose. Submission date alone does not settle assignment near a boundary. The primary `round_id` is the phase to which the proposal substantively belongs; use `receipt_round_id` only when the phase active on receipt differs, and `evaluated_in_round_ids` for later consideration of an unchanged earlier offer. Explain any difference and do not count later evaluation as resubmission. A late entrant can submit a preliminary informal proposal within the current later round; do not invent a separate personal round counter or force formality from the calendar.

Distinguish **contemporaneously announced finality**, **inferred final-negotiation status**, and **the last round observed retrospectively**. The last observed bid does not prove that the target had announced a final round. A process can end without an announced deadline.

### 5.4 Information allocation and decision rationales

Record material differences in access to management, customer information, a data room, site visits or confirmatory diligence when they define a phase or differentiate bidders. Capture delays in NDA execution that affect access. Do not log every routine conversation or document upload after entry.

Retain stated target rationales: management capacity, bid levels or closeness, strategic synergies, financing capability, confidentiality/leakage risk, antitrust concerns, management conflicts, an alternative of remaining independent, or a desire to limit disruption. Attribute each rationale to the decision-maker. Capture material financial/projection updates or business developments that the narrative links to price revisions or continued participation. Do not transform a research hypothesis about these mechanisms into an established causal explanation.

This is not a comprehensive legal-terms project. Capture legal or commercial terms to the extent needed for formality, conditionality, consideration, participation, timing or a stated selection rationale; omit routine drafting minutiae.

## 6. Contacts, confidentiality agreements and counting

An authorization to contact 50 firms is not evidence that all 50 were contacted that day. When later prose confirms the contacts occurred over several weeks, record the actual contact activity with that timing and the authorization separately. Preserve whether contacts were inbound, outbound or mixed, who communicated, and whom the communicator represented.

Record initial unsolicited or sale-solicitation contacts before NDA execution, with the response if disclosed. Do not inflate counts with recontacts, conventions, routine post-NDA meetings or repeated reports to the board. Material re-entry after a pause is worth recording but does not create a new unique firm.

Record executed/signed confidentiality agreements, not merely drafts, invitations or negotiations. A memorandum sent to existing NDA signers is not another NDA. Neither are separate labels such as “NDA” and “NDA signed” two events. An amendment or stronger standstill agreement can be a real contract update without adding a new distinct NDA participant. Record the agreement's purpose and parties; a bidder-target confidentiality agreement, adviser agreement and bidder-rollover-holder agreement are different populations.

### 6.1 Count assertions versus calculated participation

In Counts, preserve each consequential source assertion with its population, unit, timing, type split and qualifier. In Events, preserve the underlying contact, NDA, submission or admission activity. A count assertion linked to that activity is **not another participant event**. Do not emit a standalone `participation_count` event and then add it to the events that generated it.

Calculate unique participation from identified parties, genuinely disjoint residual cohorts and time-varying groups. Record the calculation and reconcile it against disclosed summaries. State unresolved overlap; do not force all totals to balance with invented bidders or exits.

Respect exact, approximate and inequality language. “Fifteen signed” is exact; “approximately fifteen expressed interest” is a different, approximate claim. “More than six” implies a lower bound of seven for an integer count, not an exact seven. “Several” stays a qualitative quantifier without an invented exact number. Do not convert a filing's literal “at least” to an exact count unless other evidence establishes the total.

The counting unit is essential: interested organizations, lead buyers, equity providers, executed contracts, unique NDA-signing bidder units, proposal submissions, and unique submitting bidders are not interchangeable. Six bidders can submit seven proposal versions. Four invited bidders can later participate through a different number of bidding groups. Preserve source counts even when an individual-level history cannot be recovered.

## 7. Dates, order and deadlines

### 7.1 Date record

For each event retain the original date expression; an exact reported date when one exists; lower and upper bounds for the best-supported window; the basis of those bounds; and any representative date used for display. Numeric date fields use `YYYY-MM-DD`; provide a U.S. `MM/DD/YYYY` display column in the review workbook. Never display a representative date as an exact reported date.

| Expression | Working interpretation | Evidentiary qualification |
|---|---|---|
| Exact day | That day. | Reported date, unless the day/year requires inference or correction. |
| A stated inclusive date range | Preserve its endpoints. | Reported interval. Do not collapse it to one day. |
| Quarter | Actual first and last calendar dates of the quarter. | Calendar translation, not a year-wide interval. |
| “Week of [date]” | That date through six days later, absent a contrary source convention. | Recommended seven-day interpretation; qualify if “week of” is ambiguous. |
| “First week of [month]” | Days 1–7. | Calendar translation. A meeting on the 3rd narrows it only if the text establishes that the event followed the meeting. |
| “Early,” “mid,” “late” month | Initially 1–10, 11–19, and 20–month-end, respectively. | **Proposed soft lexical bands**, not reported hard bounds. Override or widen when better contextual evidence requires it. |
| Month only | Entire month. | No precision beyond the month without additional evidence. |
| “Over the next few weeks” | Retain relative wording and any supported before/after constraints. | Do not silently translate “few” into an exact number of days. |
| “By [date]” / “after [event]” | A one-sided date bound or sequence constraint, with inclusivity stated. | Do not fabricate the missing endpoint. |

Tighten bounds using cross-paragraph evidence only when the logical sequence warrants it. A July 22 committee meeting followed by a July 27 review does not prove that every offer reviewed across those meetings arrived by July 22. A published July 20 deadline does not prove all offers arrived on July 20; explicitly late offers defeat that assumption.

For a bounded approximate window, use the calendar midpoint, rounding toward the earlier day, as the default representative date. An exact inferred day can be used when context actually pins it down. Adjust a representative date within its admissible window if needed to respect a supported sequence, recording the method. If bounds are one-sided or unknown, leave the representative date empty unless a specific, explained convention is supplied. Never move a real submission date to its deadline merely to simplify sorting.

Use stable `event_order` values for reading order, plus explicit `after_event_ids` for supported precedence. Same-day initial and revised bids by the same bidder must retain their known sequence. Independent overlapping events may be unordered; use a deterministic display order but label it `display_only`, not an inferred historical ordering. A source paragraph's position alone is not reliable when it contains retrospective summaries.

### 7.2 Deadline history

Keep separate records for **when a submission deadline was set or changed** and **the scheduled deadline itself**. A scheduled deadline is a milestone, not proof that a meeting, submission or enforcement action occurred then. Distinguish target-wide and bidder-specific deadlines.

Preserve the original deadline, every disclosed change, who initiated the change, when it was communicated, and the replacement deadline. Superseded milestones remain in the history with their status. An instruction to submit improved final offers two days later can be a final-round extension, not a new round.

Distinguish a formal deadline extension from the observed acceptance of late bids without a disclosed extension. Assess deadline enforcement as `observed_cutoff`, `extended`, `late_submissions_accepted`, `not_assessable`, or `not_applicable`, with evidence. Timely submissions alone do not prove a hard commitment; silence alone does not prove a soft deadline. Flag the lack of disclosed enforcement/extension when a stated deadline passes and the narrative leaves the outcome unclear.

Do not substitute any of the following for a bid-submission deadline: the last committee meeting, the last observed bid, the end of exclusivity, a bidder's offer-expiry time, a hoped-for signing date, or the date of agreement execution. These have their own fields or event types. The observed end of a round can be recorded even when no deadline was announced.

## 8. Proposals, formality, conditionality and value

### 8.1 What is a bid, and what is a revision?

A proposal is a communicated acquisition offer or indication addressing the acquisition of the relevant target. It can be oral, written, non-binding, conditional, a point value, a range, or a genuine proposal whose price is not disclosed in the narrative. Preserve all economically distinct submitted proposals in scope. Do not create an offer from a historical stock-price quotation, general interest, a target's asking price, an adviser's valuation or a bidder's statement that its valuation cannot exceed a threshold.

One IOI and the bid represented by that IOI are **one proposal**, not two submissions. A later board discussion of the same offer is not another bid. A target's request to confirm a price is not proof that the bidder confirmed it; seek the bidder response or other evidence of continued agreement.

Create a new proposal version for a new price or range, a meaningful change in consideration or material conditions, a substantive transition in commitment/documentation, or an actual final reaffirmation of the same offer. Link it to the preceding version. An oral offer followed by a revised oral or written offer is a sequence, not one averaged bid. Preserve downward revisions and reversions to a previous price. Withdrawal of a revised proposal while reaffirming an older proposal is not necessarily withdrawal from the process.

A bidder's submission of revised agreement documents is at least a document-update event. Create a linked proposal version when it materially clarifies the live offer, commitment or assessed formality. Carry a price forward only when continuity of the same proposal is supported, marking `price_origin=carried_forward`; do not present it as newly quoted. Never assume that an unspecified markup removed conditions. Routine legal drafting with no research-relevant change need not generate another proposal row.

If one communication offers mutually exclusive transaction structures, create separate alternative proposal records under one `alternative_bundle_id` and the same submission event. Do not turn two structures into a price range or count them as two independent bidder arrivals. Preserve which, if any, the target preferred.

Signing establishes agreed transaction terms, but it does not retrospectively establish a separately submitted formal bid on an invented earlier date. If no final proposal is separately identifiable, record the execution and agreed consideration with that limitation rather than fabricating a missing bid.

### 8.2 Formality: an analytical assessment, not a legal conclusion

Record the filing's actual terminology and binding/non-binding wording separately from `assessed_formality=formal|informal|indeterminate`. Use the complete context, including the bidder's documents and the target's solicitation objective.

| Evidence | Recommended interpretation |
|---|---|
| Preliminary interest, exploratory IOI or early price range with further evaluation expected and no stronger commitment evidence | Normally informal. A numerical range alone is not decisive. |
| Bidder submits a markup of the merger agreement, relevant voting agreement or a substantive transaction-document package with its offer | Strong evidence of a formal proposal, even if called an IOI/LOI or described as non-binding. Assess conditions separately. |
| Target requests final executable/binding proposals and bidder responds on that basis | Strong evidence of formality, even when the narrative abbreviates the document description. |
| Explicit best-and-final reaffirmation in an established final solicitation | Can be formal even if oral or expressed as a range. Explain the contextual basis. |
| Bidder submits substantially executable documents or confirms price while finalizing a definitive agreement | Strong evidence of a formal offer/reaffirmation when a bidder response or agreement is actually supported. |
| Only a target template was posted, an offer was written on legal letterhead, or the phrase “strategic discussions” appears | Insufficient by itself to establish formality. |
| Late preliminary approach by an unprepared new or returning bidder | Do not classify automatically as formal solely because other bidders are in a final round. |

A final stage, a markup, a point price, a range, and the words “non-binding” each convey different information. Make one best-supported formality assessment, record the competing evidence and flag material conflicts. Do not let heavy conditionality mechanically change the stored formality assessment to informal. Do not automatically make every bid in an informal round informal either. These variables must remain separately usable in estimation.

Always flag cases where an IOI/LOI is assessed as formal on stronger documentation/context, and any other material conflict between labels and evidence. Record the basis once; do not solve the problem by duplicating the bid.

### 8.3 Conditionality and economic uncertainty

Assess the offer **as it stood at that event**, not using information learned only from the eventual signed agreement. Record financing, diligence, regulatory/completion issues, material repricing exposure and exclusivity in the bid row, with compact evidence and reasons. Preserve later changes as linked revisions when material.

| `completion_conditionality` | Operational test |
|---|---|
| `none` | Affirmative evidence supports no material unresolved diligence, funding or other completion/repricing condition in the offer at that time. Use sparingly; silence and a bare markup are insufficient. |
| `light` | Substantially negotiated or executable offer; remaining steps appear limited, confirmatory or routine, with no evidenced material unresolved funding or repricing issue. Explain the positive contextual support. |
| `heavy` | Identified unresolved conditions can materially affect price or completion: substantive diligence, uncommitted financing, material contingent repricing, significant identified regulatory obstacles, indispensable third-party support, or important unresolved commercial terms. |
| `not_assessable` | Disclosures are too thin, comparative only, or conflicting to sustain an absolute classification. Record any known conditions and the preferred interpretation if supported. |

“Less conditional than bidder B” supports a **relative comparison**, not automatically `none` or `light`. A funding commitment, a representation that funding will be supplied, and an express absence of a financing contingency are distinct facts. Record them separately. Silence about a commitment is not the same as an expressly missing commitment. A financing commitment does not itself remove all diligence or other conditions.

Use concise condition tags where supported: `uncommitted_financing`, `substantive_diligence`, `confirmatory_diligence`, `material_regulatory_risk`, `material_price_adjustment`, `required_shareholder_support`, `material_terms_open`, `other`. Explain rather than tag every ordinary contract provision.

**Exclusivity is separate.** Record a bidder's request or requirement, duration and whether the target granted it. Exclusivity alone must not downgrade a formal offer to informal. Nor should its mere presence automatically make completion conditionality heavy. The substantive diligence or financing condition associated with exclusivity may independently justify heavy conditionality.

**Consideration uncertainty is also separate.** A cash earnout, a cash-settled contingent value right (CVR), equity options or a price range can make the payoff uncertain without establishing uncertainty about whether the transaction closes. Record the instrument, settlement medium, fixed cash component, contingent component and the source of any value estimate. Do not attempt detailed option valuation or legal-risk modelling unless explicitly requested.

### 8.4 Prices and normalization

Preserve the original amount, currency, scale, valuation basis, share class, consideration structure and price qualification before normalizing anything.

| Price observation | Required treatment |
|---|---|
| Actual individual point offer | Record the stated point and whether it is cash, package value or another measure. |
| Actual individual offered range | Record lower and upper endpoints; no midpoint as an observed offer. |
| Range across several bidders' offers | Record a group envelope and its population. It is not evidence that each bidder offered that range. |
| A bidder's range “reached at least $80” | The **upper endpoint** is at least $80. Do not fill the bidder's lower endpoint with $80. |
| A valuation “not above” approximately $78 | A weak upper bound relative to an approximate benchmark, not an exact $78 submitted bid and not a strict below-market inequality. |
| A proposal valued at $21.50, including $19 cash and options assigned $2.50 by the bidder | Preserve $19 cash and the attributed option valuation. Do not treat $21.50 as certain cash or call equity options a cash earnout. |
| An enterprise value or total equity value | Keep the original basis and scale. Convert only with sufficiently supported, economically compatible inputs. |

If converting enterprise value to equity value, identify the actual debt/cash and other adjustments implied by the proposal; do not assume an arbitrary net-debt number. If dividing equity value by shares, establish the relevant share count, date, dilution and treatment of preferred shares/rollover. Show the formula and sourced inputs. Otherwise leave normalized per-share fields empty and flag comparability. Do not infer a share count from an approximate transaction-value/price pair and then present the resulting conversion as independently observed.

A cash-settled contingent component can coexist with cash-only settlement; cash plus equity options is not simply all cash. When settlement is unclear, preserve that uncertainty. Do not identify a cash-settled instrument solely from the letters “CVR.” Store the nominal/stated package amount separately from fixed cash payable at closing and any attributed contingent valuation.

Collect disclosed market-price benchmarks and their dates when relevant to an offer comparison or withdrawal statement. Do not mistake them for offer prices. Do not calculate a premium when numerator and denominator refer to different assets, share classes or times without an explicitly justified comparison. External market-price enrichment is a separate task; missing external data must not be guessed.

## 9. Admission, exits and unsuccessful participation

Separate the following outcomes; they can occur at different times for the same bidder.

| Outcome | Meaning and recording rule |
|---|---|
| Initial interest declined | A contacted firm declines a potential transaction. Preserve the initial contact and response; do not invent an exit from a round it never entered. |
| Pre-entry exclusion | Target declines to invite a known interested party, for example because of regulatory or information concerns. Record the target decision, not a fictitious NDA-stage withdrawal. |
| Target exclusion/non-admission | Target removes a participant or does not invite it to continue after a genuine selection decision. Record the originating and destination rounds and stated reason. |
| Bidder withdrawal | Bidder communicates that it will not proceed. Preserve date bounds and reason; retain the record if the bidder later returns. |
| Non-submission | An expected or potential bidder does not submit an offer. Distinguish an explicit report of no submission from a merely missing later mention. Do not infer a voluntary exit date or motivation. |
| Target-driven exclusivity displacement | Another bidder receives exclusivity that suspends the target's discussions with remaining competitors. Record the effect and its potentially temporary character; do not invent permanent withdrawals. |
| Proposal withdrawal/reversion | A particular proposal is withdrawn or superseded, possibly while an earlier offer remains live. This is not necessarily an actor-level exit. |
| Unsuccessful at signing | A participant is not the chosen buyer. This is an outcome, not proof of an earlier voluntary withdrawal or a particular private valuation. |

For each meaningful exit or exclusion assess agency (`bidder`, `target`, `joint_or_mixed`, `unknown`), participation status and reason. Attribute valuation statements carefully. Preserve whether the bidder reported its valuation or willingness to pay as below market, at its previous IOI, below its previous IOI, or unable to increase a prior range. Keep the reference proposal, market benchmark and strict/weak inequality. These are reported constraints on willingness/valuation, not directly observed latent auction values.

A refusal to raise a price is not necessarily an announcement of withdrawal. A target's advice that a valuation is uncompetitive followed by no bid may involve both target selection and bidder non-participation; make a supported agency assessment rather than forcing one party to be the sole cause.

Do not infer the identity of a missing strategic bidder from the fact that a named strategic bidder disappears from the narrative. Do not add dropout rows for parties never contacted. Do not fill an apparent count gap with fictitious dropouts when consortium formation or incomplete disclosure may explain it. Unknown exit reasons must be flagged, but can be reviewed together for a homogeneous cohort.

## 10. Event terminology

Use the following professional labels and machine codes. A row records a distinct action, communication, state observation or scheduled milestone; it is not simply a sentence in the filing. Split materially distinct actions even when they share a paragraph or date. Link complementary tables rather than counting their representations as additional events.

| Code | Display label and meaning |
|---|---|
| `strategic_alternatives_review` | Strategic alternatives reviewed — include only a material review needed to explain initiation or a subsequent decision. |
| `sale_exploration_authorized` | Sale exploration authorized — board/committee approves active consideration of a target sale. |
| `public_sale_announcement_authorized` | Public sale-process announcement authorized — distinct from its eventual publication. |
| `initial_sale_contact` | Initial sale-related contact — record initiator, recipient, represented party and response; not routine recontact. |
| `acquisition_interest_expressed` | Acquisition interest expressed — no separately supported acquisition proposal. |
| `activist_sale_advocacy` | Activist sale advocacy — pressure or advocacy for sale, with its strength and source. |
| `activist_involvement` | Other material activist involvement — support, alternative suggestions or involvement not established as sale pressure. |
| `financial_adviser_engagement` | Financial adviser engaged — clarify whether approval, service commencement or contract execution. |
| `advisory_engagement_ended` | Advisory engagement ended — not termination of the target's sale process. |
| `confidentiality_agreement_executed` | Confidentiality agreement executed — include agreement purpose and participant-count treatment. |
| `confidentiality_agreement_updated` | Confidentiality arrangement updated or reused — no automatic new participant. |
| `due_diligence_access_changed` | Due-diligence access granted or changed — material information access/staging only. |
| `management_presentation` | Material management presentation — retain individual timing when relevant to admission, information or preparation. |
| `round_opened` | Bidding/negotiation round opened — a distinct launch or inferred transition, not a duplicate of an already recorded operative decision. |
| `bid_deadline_set` | Bid-submission deadline set — event date is when the target set/communicated it. |
| `bid_deadline_revised` | Bid-submission deadline revised — link old and new scheduled milestones. |
| `bid_submission_deadline` | Scheduled bid-submission deadline — mark whether superseded, reached, cancelled or uncertain. |
| `bidder_admitted` | Bidder admitted to a phase — with destination round and access conditions. |
| `bidder_excluded` | Bidder excluded or not admitted — with agency, stage and reason; distinguish temporary exclusivity displacement. |
| `bidder_withdrew` | Bidder withdrew from participation — distinguish withdrawal of a proposal alone. |
| `bid_not_submitted` | Proposal not submitted — observed nonresponse/non-submission, not an invented bid. |
| `bidder_valuation_statement` | Bidder valuation/willingness statement — an economic bound or assessment not itself an offer. |
| `acquisition_proposal_submitted` | Acquisition proposal submitted, revised or reaffirmed — link proposal versions in Bids. |
| `proposal_withdrawn` | Acquisition proposal withdrawn — identify the proposal and any surviving/restored offer. |
| `proposal_document_update` | Material proposal-document update — no invented new price or removal of conditions. |
| `target_price_request` | Target requests a price or improvement — not a bidder's submitted offer. |
| `exclusivity_requested` | Exclusivity requested — only a separate event if distinct from the proposal already carrying this condition. |
| `exclusivity_granted` | Exclusive negotiations agreed — distinguish authorization from executed agreement. |
| `exclusivity_extended` | Exclusive-negotiation period extended — not a bid-deadline extension. |
| `exclusivity_ended` | Exclusive-negotiation period ended — does not itself end the sale process. |
| `bidding_group_changed` | Bidding-group formation or membership change — requires acquisition-participation evidence. |
| `equity_rollover_arrangement` | Equity-rollover arrangement discussed, authorized or agreed — not automatically a new bidding group. |
| `material_information_update` | Material business/financial information updated — where relevant to bids, selection or process design. |
| `sale_process_suspended` | Sale process suspended — continued sale effort is paused, not necessarily abandoned. |
| `sale_process_terminated` | Sale process abandoned/terminated — distinguish a failed sale effort from successful execution. |
| `sale_process_restarted` | Sale process restarted — link the prior process and the evidence supporting a new attempt. |
| `sale_process_publicly_announced` | Sale exploration publicly announced — not announcement of a signed transaction. |
| `acquisition_proposal_publicly_announced` | Acquisition proposal publicly announced — identify issuer, proposal and publicity type. |
| `transaction_approved` | Transaction approved — board/committee decision, including unresolved qualifications. |
| `merger_agreement_executed` | Merger agreement executed — signing, not closing. |
| `merger_agreement_publicly_announced` | Executed merger agreement publicly announced — separate even when signing occurs the same day. |
| `post_signing_solicitation_started` | Post-signing solicitation/go-shop started — must follow agreement execution and be supported, not inferred from ordinary renewed contacts. |
| `post_signing_solicitation_ended` | Post-signing solicitation/go-shop ended — distinguish its deadline from a pre-signing bid deadline. |
| `merger_agreement_terminated` | Signed merger agreement terminated — distinguish termination of an unsigned sale effort. |
| `transaction_completed` | Transaction legally completed/closed — only when disclosed in the supplied material. |
| `other_material_process_event` | Other material process event — explain a genuinely necessary event not covered above; do not use as a dumping ground. |

A media report or rumor is not an issuer press release; record it as a material publicity event with `publicity_kind=media_report` when consequential. Legal-adviser names and first observed service normally belong in Parties/Relationships, not fabricated retention events.

A board decision that opens a round and selects bidders may support multiple distinct decisions, but do not emit duplicate `round_opened` rows just because the same decision is also linked from Rounds. Likewise, setting a deadline, reaching its scheduled date and receiving a late offer are distinct records, not alternative labels for one action.

Legacy labels map to the definitions above, not to unexplained fragments: “Target Sale” → sale exploration authorized; “Bidder Interest” → acquisition interest expressed; “IB” → financial-adviser engagement; “NDA” → executed bidder confidentiality agreement; “Final Round Ann/Inf Ann” → round launch/deadline-setting events with round finality and solicitation objective; “Final Round/Inf/Ext” → scheduled deadline and its revision history; “Drop/DropBelowM/DropBelowInf/DropAtInf/DropTarget” → participation outcome plus agency and valuation-reference fields; “Executed” → merger-agreement execution; “Terminated/Restarted” → process termination/restart. An old event index called `BidderID` must never become the new stable bidder identifier.

## 11. Interactive review without offloading the extraction

Read the whole supplied background, form a provisional process/round map, and surface consequential structural issues early when the session allows progress messages. Give the proposed answer and evidence, not “please tell me the rounds.” Continue with a complete provisional extraction unless a missing source or irreconcilable structural problem actually prevents meaningful completion. Mark dependent assignments provisional and group them under stable issue IDs so a correction can propagate coherently.

The following verification categories remain mandatory in this pilot:

| Category | Required review treatment |
|---|---|
| Possible round ending/start, including board meetings near deadlines and unlabelled first-round starts | Review the proposed boundary map and the material candidates rejected as non-boundaries. Group by transition, not by every downstream bid. |
| Deadline revisions and continuation after a deadline without a disclosed revision/enforcement decision | Review the complete deadline history for that round, including the recommended interpretation. |
| More than one sequential sale process | Review segmentation and the treatment of earlier NDAs/participants. |
| Uncertain NDA totals, identity overlap or strategic/financial splits | Review one reconciliation packet per related population problem. |
| Unknown winner or formal-bidder type | Review after checking relevant sections of the supplied filing. |
| Uncertain withdrawal/exclusion reason or agency | Review individually when economically distinct; combine genuinely homogeneous unidentified cases. |
| Formal assessment despite IOI/LOI terminology, or other consequential formality conflict | Show source label, documents, solicitation context and the model's assessment. |
| Conditionality | Review all bid conditionality assessments during the initial pilot, grouped by bidder history or recurring condition pattern where useful. Do not silently waive this pilot check. |
| Unclear adviser affiliation | Review the proposed client link rather than each appearance of the adviser. |
| Partial-only transactions, ambiguous units/currency, enterprise-versus-equity confusion or non-comparable consideration | Review scope and normalization before claiming estimation readiness. |
| Unsupported quotation, source contradiction, material date/identity ambiguity, or another high-impact uncertainty | Repair what can be repaired; otherwise supply a recommended resolution and the unresolved evidence. |

A required verification is not automatically a blocker. Use `priority=blocking|material|routine` and explain the downstream consequence. `Blocking` means that a specific analytical output cannot be relied on without resolution, not that the entire extraction should be withheld. A narrow uncertainty about the exact day can be routine if event order and round assignment are secure. Several mandatory items can be handled in one coherent decision packet, but their coverage must remain visible.

Each Review item must contain the model's conclusion, short reasons, source locations, affected IDs/fields, a consequential alternative if any, and an explicit suggested reviewer action. Avoid repetitive questions whose answer is simply “the filing does not disclose this.” Keep such missingness in the data; flag it once when it affects a required research judgment.

Preserve the original AI assessment and record reviewer corrections separately with reviewer, date and reason. Update derived counts, displays and dependent round assignments after an accepted correction, retaining the prior version. A correction in one deal is not a new universal rule unless the researcher explicitly makes it one. Do not claim cross-session learning without an updated instruction or supplied decision history.

## 12. Output tables and field dictionary

### 12.1 Common contract

Use the exact table names below. Each table has its own stable primary key; every record also has `deal_id`. Do not derive a party ID from an event number. Suggested prefixes are `D`, `P`, `R`, `A`, `L`, `E`, `B`, `C`, `V` and `Q` for deal, process, round, actor, relationship, event, bid, count, evidence and review IDs. IDs must survive re-sorting and correction.

Except Evidence and Review, append these common columns: `evidence_ids`, `review_issue_ids`, `record_status`. The first two are lists of linked IDs; `record_status` is `ai_first_pass`, `reviewed` or `superseded`. These are record-review states, not claims that an event occurred. Keep one key per row. If a table has no applicable records, provide its headers and explain that it is empty.

For CSV, separate list-valued ID or tag fields with `|` inside a properly quoted cell; never embed an unescaped delimiter in an ID. Such fields become junction tables if loaded into a relational database. Keep numbers numeric and dates standardized. Free text must not occupy numeric price or count fields. For genuine missing values, use a companion `<field>_status` column where ambiguity would otherwise arise; Evidence can carry the detailed reason. Do not create hundreds of separate review questions for structurally inapplicable fields.

**Evidence is the field-level audit trail.** An interpretation must have its own Evidence entry naming the table, record and field assessed. A short reason in the Bids or Events sheet is a readable mirror of that entry, not a second independent judgment. Reported facts that share the same passage and evidentiary basis can share one Evidence entry; distinct judgments cannot hide behind a blanket row-level confidence score.

### 12.2 Deal — one row for the focal transaction

| Field | Meaning |
|---|---|
| `deal_id`, `target_party_id`, `target_name` | Stable deal identifier, target actor link and readable target name. |
| `acquirer_party_id`, `acquirer_name` | Focal acquiring bidder unit and readable name; distinguish its legal vehicles in Relationships. |
| `source_filename`, `filing_type`, `filing_date`, `accession_number`, `source_url`, `source_coverage` | Available source identity and whether the full filing or only an excerpt was supplied. Unsupported metadata remains empty. |
| `signing_event_id`, `announcement_event_id`, `completion_event_id` | Links to focal execution, public transaction announcement and closing. Closing may be unavailable in a pre-closing proxy. |
| `date_announced`, `date_effective` | Readable mirrors of the merger-announcement and closing dates, respectively; not sale-exploration or signing dates. |
| `agreed_consideration_text`, `agreed_price_per_share`, `agreed_price_basis` | Actual agreed consideration, numeric per-share amount when meaningful, and whether cash or stated package value. Do not substitute the highest bid. |
| `auction_screen`, `auction_screen_reason` | Section 3 screening result and basis, linked to the relevant NDA population. |
| `inclusion_assessment`, `inclusion_reason` | `core_candidate`, `descriptive_only`, `excluded`, or `research_decision_required`; recommendation, not final estimation approval. |
| `initiation_assessment`, `initiation_reason` | Section 5 initiation summary, retaining links to the underlying sequence. |
| `process_summary`, `source_limitations`, `policy_version`, `extraction_version` | Short commercial narrative, actual limitations and reproducible policy/extraction identifiers. |

### 12.3 Processes — one row per distinct target-sale attempt

| Field | Meaning |
|---|---|
| `process_id`, `process_number`, `previous_process_id` | Stable episode ID, chronological display number and predecessor if relevant. |
| `process_scope`, `is_focal_process` | Asset/target scope and whether this is the focal attempt. An earlier acquisition by the target is not a sale-process row. |
| `start_event_id`, `end_event_id` | Supported beginning and observed ending; their Events records carry date uncertainty. |
| `outcome` | `agreement_signed`, `abandoned`, `suspended`, `ongoing`, or `not_observed`. Preserve later post-signing competition in Events rather than discarding it. |
| `segmentation_reason`, `continuity_evidence`, `alternative_segmentation` | Why this is one process or several; participants, cessation/renewal and timing evidence; consequential alternative. |
| `nda_scope_note` | Treatment of historical, reused and current-process agreements. |

### 12.4 Rounds — one row per analytical phase

| Field | Meaning |
|---|---|
| `round_id`, `process_id`, `round_number` | Stable phase ID and consecutive number within its process. |
| `source_stage_label`, `stage_objective` | Filing's wording and assessed objective: `preliminary_indications`, `updated_indications`, `final_proposals`, `definitive_negotiation`, or `other_explained`. |
| `authorization_event_id`, `start_event_id`, `end_event_id` | Distinguish authorization, operative start and observed end. These may refer to the same event when justified. |
| `latest_general_deadline_event_id`, `last_submission_event_id` | Latest target-wide scheduled deadline and last observed submission. These are not necessarily the same date. Bidder-specific deadlines remain in Events. |
| `admitted_population`, `information_stage` | Readable admitted party/cohort IDs and material access or preparation expected in this phase. |
| `finality_at_time`, `last_observed_round` | `announced_final`, `inferred_final`, `explicitly_intermediate`, or `not_stated`; separate Boolean identifying the retrospectively last observed phase. |
| `boundary_reason`, `deadline_enforcement`, `enforcement_reason` | Supported phase definition and Section 7 enforcement assessment. |

### 12.5 Parties — one row per actor or clearly defined anonymous cohort

| Field | Meaning |
|---|---|
| `party_id`, `display_name`, `disclosed_name`, `aliases` | Stable actor/cohort identity and source names. |
| `entity_kind` | `organization`, `person`, `board_or_committee`, `bidding_group`, `acquisition_vehicle`, `unidentified_individual`, or `unidentified_cohort`. |
| `research_roles` | Applicable roles: target, bidder, adviser, activist, shareholder, sponsor, lender, equity provider or acquisition vehicle. Role is not bidder type. |
| `bidder_type`, `type_reason` | Strategic/financial/mixed/unknown assessment and rationale. Empty as not applicable for non-bidders. |
| `ownership_status`, `country`, `non_us`, `sponsor_backed` | Separate attributes with support; unknown is not false. Identify the entity level to which they apply in Evidence. |
| `identity_status`, `identity_reason` | `identified`, `anonymous_distinct`, `cohort_only`, or `mapping_uncertain`; basis for linking names or keeping them separate. |
| `cohort_definition`, `cohort_count_id` | Population definition and cardinality link for a cohort; not an invented single bidder or a mutable basket of unrelated unknowns. |
| `first_observed_event_id`, `final_participation_status` | Earliest supported role/event and last observed participation state, not a fabricated exit. |

### 12.6 Relationships — one row per relationship episode or material change

| Field | Meaning |
|---|---|
| `relationship_id`, `from_party_id`, `to_party_id`, `process_id` | Directed actor links and applicable episode. |
| `relationship_type` | `advises`, `sponsors_or_controls`, `vehicle_for`, `member_of_bidder_group`, `financing_supports`, `rollover_into`, `cohort_member`, `cohort_subset`, or `other_explained`. |
| `relationship_status` | `discussed`, `requested`, `authorized`, `executed_or_active`, `ended`, `rejected`, or `uncertain`. |
| `start_event_id`, `end_event_id` | Supported temporal scope; leave unobserved endpoints empty. |
| `role_detail`, `economic_role_assessment`, `relationship_reason` | Client/mandate, ownership/funding/rollover distinctions and why a relationship does or does not constitute joint bidding. |
| `first_service_event_id`, `first_service_date_text`, `approval_event_id`, `contract_event_id`, `primary_adviser` | Advising-specific fields separating first observed service, authorization and contract signature. Preserve the source date expression directly when first observed service has no separate material event; do not fabricate a retention event merely to populate a link. Others are not applicable. |

### 12.7 Events — the chronological ledger

| Field | Meaning |
|---|---|
| `event_id`, `process_id`, `round_id`, `event_order` | Stable event and applicable episode/phase; integer display order. A pre-round/context event may have no round. |
| `event_code`, `event_role`, `event_phase` | Section 10 code; `action`, `communication`, `state_observation` or `scheduled_milestone`; `background_context`, `pre_round`, `round`, or `post_signing`. |
| `event_summary` | Independently understandable factual description; identify the action, subject and relevant change. |
| `actor_party_id`, `acting_for_party_id`, `recipient_party_id`, `subject_party_id` | Speaker/decision-maker, represented principal, recipient and affected participant/cohort. This preserves adviser-mediated direction of contact. |
| `actor_name`, `subject_name`, `round_label` | Readable mirrors of the linked entities/round. These are not independent identities. |
| `date_text`, `date_reported`, `date_lower`, `date_upper` | Original expression, exact literal event date where available, and supported/assigned window endpoints. |
| `date_precision`, `date_bounds_basis` | Precision: `exact_reported`, `exact_inferred`, `reported_range`, `approximate_window`, `relative_only`, `undated`; basis: reported interval, calendar translation, cross-reference, soft lexical convention or explained combination. |
| `date_assigned`, `date_assignment_method`, `date_display_us` | Exact or representative display date; method (`reported`, `inferred_exact`, `midpoint`, `order_constrained`, `unassigned`); readable U.S. display with approximation visibly marked. |
| `after_event_ids`, `order_basis` | Supported preceding events; `reported_sequence`, `contextual_sequence`, or `display_only` for unresolved ties. |
| `related_event_ids`, `bid_ids`, `count_ids`, `relationship_ids` | Links to connected actions, proposal records, scoped quantities and relationship changes. |
| `contact_direction`, `contact_response`, `agreement_purpose` | Inbound/outbound/mixed, disclosed initial response, and acquisition/advisory/funding/rollover/other confidentiality purpose where applicable. |
| `admission_status`, `origin_round_id`, `destination_round_id` | Whether admitted, excluded, conditionally admitted or not determined; distinguish the selection stage from the phase entered or denied. |
| `exit_agency`, `exit_reason`, `participation_effect` | Section 9 agency and attributed reason; withdrawal, non-submission, non-admission, temporary displacement, re-entry or unsuccessful outcome. |
| `valuation_reference`, `reference_bid_id`, `reference_value`, `reference_date`, `valuation_relation` | Bidder's stated valuation/willingness relative to own earlier IOI, market price or another identified benchmark; relation `below`, `at`, `not_above`, `not_below`, `unable_to_increase`, `other`, `unknown`. |
| `target_requested_price`, `target_price_relation`, `target_price_basis`, `target_price_scope`, `price_currency`, `price_unit` | Numeric target asking/admission threshold when disclosed, its operator (`at_least`, `above`, `exactly`, or `other_explained`), basis (point price, range upper endpoint, or other), and general/bidder-specific applicability and units. A source criterion satisfied by a range reaching a threshold does not require every point in that range to exceed it. |
| `deadline_scope`, `deadline_for_party_id`, `old_deadline_event_id`, `new_deadline_event_id`, `milestone_status` | General versus bidder-specific submission deadline, affected unit, revision links and status (`scheduled`, `superseded`, `reached`, `cancelled`, `uncertain`). |
| `other_expiry_date`, `other_expiry_kind`, `time_text` | Exclusivity or offer expiry and verbatim time/timezone; not a bid deadline. Preserve approximate precision through Evidence where necessary. |
| `decision_rationale`, `rationale_speaker_id`, `information_change`, `publicity_kind` | Attributed process rationale, information/access changes, and issuer release, public filing, media report or other publicity. |
| `judgment_note`, `source_locator`, `supporting_quote` | Brief readable interpretation and main source support. Field-level reasons and additional premises belong in Evidence. |

Only applicable event-specific columns need be populated. Do not create irrelevant data for every event merely because the schema permits it. A cohort event can reference its exact or bounded count without occupying a fictitious bidder row.

### 12.8 Bids — one economically distinct proposal version or alternative

| Field | Meaning |
|---|---|
| `bid_id`, `event_id`, `process_id`, `round_id`, `bidder_party_id` | Proposal key, canonical submission/reaffirmation event, phase and bidding unit. |
| `bidder_name`, `round_label`, `event_order`, `date_display_us` | Readable mirrors from Parties/Rounds/Events. A repeated mirror is not a new event. |
| `receipt_round_id`, `evaluated_in_round_ids` | Optional different phase active when an earlier-stage response arrived, or later phases evaluating an unchanged earlier proposal. No second numbering system; do not count evaluation as resubmission. |
| `previous_bid_id`, `revision_kind`, `alternative_bundle_id` | Version chain; `initial`, `price_revision`, `terms_revision`, `commitment_revision`, `reaffirmation`, or `reversion`; mutually exclusive structures share a bundle. |
| `submission_channel`, `source_bid_label`, `binding_status_as_reported`, `document_state` | Oral/written/both; IOI/LOI/proposal wording; binding/non-binding/not stated/mixed wording; target template only, bidder comments, bidder markup, substantially executable or not disclosed. |
| `acquisition_scope`, `core_bid_eligible`, `scope_reason` | Section 3 asset/equity scope, Boolean core-coverage status and reason. |
| `price_text`, `price_form`, `price_origin` | Exact source expression; `point`, `bidder_range`, `partially_known_bidder_range`, `group_envelope`, or `undisclosed`; `newly_stated`, `carried_forward`, `source_implied`, or `calculated`. |
| `price_per_share`, `price_lower`, `price_upper`, `price_constraint` | Individual point or actual range endpoints. Other information such as `range_upper >= 80` goes in the explicit constraint field, not an invented endpoint. |
| `currency`, `original_amount`, `original_lower`, `original_upper`, `original_scale`, `valuation_basis`, `share_class` | Original units, numeric amounts/endpoints, scale (1, thousand, million, billion), equity/enterprise/asset/other basis and affected shares. |
| `per_share_value_basis`, `cash_at_closing_per_share`, `consideration_medium`, `contingent_component`, `contingent_value`, `contingent_value_source` | Cash versus package/attributed value; fixed closing cash; cash/stock/mixed equity instruments/other/unknown settlement; instrument and attributed component value. Explain its units. |
| `all_cash` | Derived flag for the consideration payable on cashed-out target shares: 1 if all components settle in cash, 0 if a non-cash component is present, empty if unknown. Record a shareholder rollover separately. Cash-settled contingent consideration can be all cash without being a fixed or certain amount. |
| `normalization_formula`, `normalization_input_evidence_ids`, `comparability_assessment` | Calculation and actual inputs, or reason the proposal cannot be compared on a common per-share basis. |
| `assessed_formality`, `formality_reason` | Required assessment and concise reason; field-specific basis/confidence in Evidence. |
| `completion_conditionality`, `conditionality_reason`, `condition_tags` | Required Section 8 assessment, reasons and compact material-condition categories. |
| `financing_commitment_status`, `financing_contingency_as_reported`, `diligence_status` | Commitment: committed, represented available, explicitly uncommitted or not disclosed; financing contingency: yes/no/not disclosed; diligence: substantive, confirmatory, ongoing unspecified, reported complete, explicitly not required or not disclosed. |
| `exclusivity_status`, `exclusivity_duration_text`, `value_uncertainty_description`, `relative_conditionality` | Exclusivity requested/required/granted/explicitly not required/not disclosed; duration; uncertain payoff components; explicit comparisons with another bid. |
| `offer_expiry_text`, `target_response`, `response_event_id` | Bidder's expiry terms and source-supported target action. An asking-price request is not an additional bid. |
| `source_locator`, `supporting_quote` | Main evidence immediately readable beside the proposal; link all additional premise-specific evidence. |

Normally one Bids row links to one proposal event. Alternative structures submitted together share an event, so count submission events separately from the number of alternatives. A source-only group envelope can occupy a clearly labelled cohort record, but never masquerade as one individual's offer or enter individual bid statistics without an explicit analytical treatment.

### 12.9 Counts — disclosed assertions and reproducible reconciliation

| Field | Meaning |
|---|---|
| `count_id`, `process_id`, `round_id`, `as_of_event_id` | Scope identifiers and temporal reference. |
| `claim_role`, `metric`, `count_unit`, `population_definition`, `cohort_party_id` | `reported_summary` or `derived_result`; contacts, executed bidder NDAs, submitting bidders, submissions, invitees, independent bidding groups or another explained metric; exact unit and population. |
| `source_count_text`, `count_qualifier`, `count_exact`, `count_lower`, `count_upper` | Literal claim, exact/approximate/at least/more than/at most/range/qualitative classification and compatible numeric values. |
| `bidder_type_scope`, `known_member_ids`, `overlap_or_exclusions` | Type split/subpopulation, established members, overlap and explicit exclusions. A split component is not added to its parent total. |
| `input_event_ids`, `input_count_ids`, `calculation` | Transparent derivation with unique-unit and residual-cohort treatment. |
| `reconciliation_group_id`, `reconciliation_status`, `reconciliation_reason` | Link assertions to calculations; `independently_supported`, `partitioned_from_reported_total`, `partial`, `conflict`, or `unresolved_overlap`, with explanation. |

Emit either one aggregate activity with established membership links, **or** disjoint individual and residual-cohort activities; do not make both additive. Keep the source total in Counts. If an aggregate event is later decomposed into better-supported individual/residual events, mark the old representation superseded rather than counting it again.

A residual calculated as “20 minus four known signers” preserves the disclosed twenty; adding that residual back to the four is not independent validation of twenty. Label this arithmetic partition honestly. Count reconciliation must never create unsupported identity links, submission dates or exit reasons.

### 12.10 Evidence — field-level claims, facts and judgments

| Field | Meaning |
|---|---|
| `evidence_id`, `subject_table`, `subject_id`, `field_name` | Exact record/field supported. For directly reported facts with identical basis, a short list of fields is allowed; interpretive assessments get separate entries. |
| `claim_value`, `evidence_basis`, `confidence`, `reason` | Supported or assessed value, Section 2 basis, qualitative confidence and concise rationale. |
| `source_filename`, `section`, `printed_page`, `pdf_page`, `paragraph_or_line`, `source_url`, `verbatim_quote` | Verifiable source location and exact supporting text. Missing locator components stay empty. |
| `premise_evidence_ids`, `policy_id`, `alternative_value`, `uncertainty` | Additional premises for cross-source inference/calculation, applicable convention, consequential alternative and remaining limitation. |

An assessment using multiple passages should have a conclusion entry linked to premise entries, each with its actual quote. Convention-only assignments cite their policy and the factual premises; do not invent a quotation from the filing that supposedly states the convention. Judgments about scope, identities, bidder type, initiation, process/round structure, chronology, formality, conditionality, exit attribution and price normalization are all subject to this requirement.

### 12.11 Review — grouped decisions and correction record

| Field | Meaning |
|---|---|
| `issue_id`, `issue_group`, `priority`, `mandatory_category` | Stable decision packet, grouping, downstream priority and Section 11 category or policy confirmation. |
| `affected_records`, `affected_fields`, `question_or_check` | Specific linked record IDs and fields; one coherent question/check, not an open-ended research assignment. |
| `model_recommendation`, `reason`, `evidence_ids`, `source_locators`, `alternative` | Complete suggested resolution and its support. |
| `research_impact`, `suggested_action`, `review_status` | Consequence, recommended reviewer action, and `pending`, `accepted`, `corrected`, or `deferred`. |
| `original_ai_value`, `reviewer_value`, `reviewer_reason`, `reviewer`, `reviewed_at`, `dependent_records_updated` | Correction history. Preserve original values; do not overwrite them when populating a reviewed view. |

### 12.12 Human-readable presentation

Do not make the reviewer navigate IDs to understand an offer. In Bids, put the date, bidder name, round, price/consideration, formality and reason, conditionality and reason, main source locator/quote and review flag first. In Events, put sequence, displayed date/precision, event label, actor/subject, summary, phase and evidence first. Keep the fuller technical columns to the right; do not silently omit them from exported data.

Use Excel filters and frozen headers; preserve numeric types and legible wrapped text. Avoid merged data cells and color-only meanings. For CSV imports, protect free-text cells beginning with spreadsheet formula characters so filing text cannot execute as a formula; retain the unmodified source quote in a documented text representation. Do not prefix genuine negative numeric values as text. Explain list delimiters and missingness in the accompanying summary.

## 13. Worked calibration examples

These examples restate their factual premises and illustrate distinctions, not rules tied to a particular company. **Do not insert these historical facts into a new extraction.**

| Evidence pattern | Correct extraction consequence |
|---|---|
| Providence & Worcester: an offer called a non-binding LOI includes bidder-submitted merger/voting markups and requests substantive diligence. | Assess formality using the markup evidence; assess conditionality separately. “Non-binding,” “formal” and “conditional” can coexist. |
| Providence & Worcester: Party B's counsel sends a revised agreement on August 4 while the narrative also describes ongoing diligence into August. | Record the document update or a supported linked proposal version. Do not infer that every condition was removed on August 4, or call that date merger execution. |
| Providence & Worcester: six late-July LOIs are discussed across July 22 and 27 meetings; a specific revision is dated July 26. | Preserve the dated revision and uncertain dates of other offers. July 27 can support a phase-end assessment but is not automatically an announced July 27 deadline. |
| Mac-Gray: twenty NDA signers comprise two strategic firms identified as A and CSC/Pamplona and eighteen financial firms, including B and C. Individual NDA dates for those four firms are disclosed later. | Four individual records plus sixteen unidentified financial signers partition the total. No additional unnamed strategic signers; no extra twenty-signature event. |
| Mac-Gray: Party A reiterates an $18–19 range as best and final in an established final solicitation. | A defensible formal assessment retains the actual range; it does not invent an exact price or automatically downgrade the offer. |
| Mac-Gray: Party C explicitly does not submit/reaffirm on September 18; later comparison concerns A, B and the eventual winner before exclusivity. | Record C's non-submission with unknown reason; assess A/B's later displacement separately. Do not identify B/C as the two continuing rivals displaced merely because a secondary annotation says so. |
| PetSmart: three initial ranges reach at least $80; two are described; Bidder 2 initially offers $78 and later increases its range. | Preserve a third, initially high-range bidder distinct from Bidder 2, with an upper-endpoint constraint. Do not set that bidder's lower endpoint to $80. |
| PetSmart: four parties are invited; two parties later form a group, but only one member's invitation is explicit; three final bidding units are subsequently described. | Preserve both reported stage counts and group formation. Do not force the second member to have been an invitee or invent a fourth finalist's dropout to make the arithmetic neat. |
| PetSmart: bidder documents arrive December 6; priced final offers December 10; improved offers are requested for December 12; on December 12 a buyer offers $82.50 and then $83. | Documents alone are not another priced offer. Preserve the deadline extension and the order of the two December 12 proposal versions; no new round is required solely by the improvement request. |
| PetSmart: a group's valuation would not be above a current market price of approximately $78; it does not submit a written offer. | Record the reported weak valuation bound and participation outcome. Do not enter an exact $78 informal bid. |
| PetSmart: a shareholder may roll existing shares into the buyer and signs confidentiality arrangements. | Record rollover/funding-economics relationships without automatically creating a new competing bidder, acquisition NDA or consortium. |

## 14. Completion checks

Before delivering, verify the following against the actual source and report failures honestly.

**Coverage:** Every disclosed core proposal and meaningful revision, all material NDA/contact/admission/exit activity, initiation steps, relevant advisers and their clients, process/round transitions, deadline changes, material information/selection rationales, execution and public announcement are accounted for. Earlier processes and excluded-scope activity are labelled rather than mixed into the focal process. Relevant post-signing competition is not silently dropped.

**Evidence:** Quotes are exact and support the stated fields. Cross-paragraph assessments cite their premises. No confidence label conceals a guess. Source language, inference, calculation and convention remain distinguishable. No facts were copied from calibration examples or outside memory.

**Identity and quantities:** Names and aliases are reconciled without unjustified identity merges. Group membership is time-specific. Contacts, contracts, unique NDA bidders, proposal versions and independent bidding units have distinct denominators. Totals do not add named members to their own cohorts, parent totals to their splits, repeated mentions to original events, or group members to their joint bidder at the same stage.

**Chronology:** Reported dates, inferred dates, representative dates, interval bounds and scheduled milestones remain distinct. Representative dates respect valid bounds and supported ordering. Known same-day revisions are ordered correctly. Deadline announcements, scheduled dates, offer expiry, exclusivity and signing are not interchanged. A source typo has not been silently converted into a historical fact.

**Bids:** Only actual proposals populate individual proposal observations. Ranges, envelopes, bounds, alternative structures, cash components and attributed instrument values are distinguished. Every bid has a supported formality and conditionality assessment or a justified non-assessment. A markup does not by itself prove unconditionality. No transaction price or valuation conversion was fabricated.

**Structure and review:** All IDs resolve; each numbered round belongs to one process; no duplicate numbering scheme exists. Each mandatory verification category is either covered by a review packet or explicitly inapplicable. Material hypotheses have recommended resolutions and linked affected records. The model has not marked its own first pass as human-approved.

Report `pass`, `qualified` or `failed` for these six check groups, with the affected IDs and consequences. Fix a detected extraction error before delivery when the source resolves it. A passing internal check does not certify that all interpretations are correct.

## 15. Final response in the extracting session

Provide the actual workbook/CSV files, then a short commercial account of the process: initiation, principal participants, stage transitions, price evolution, selection rationale and outcome. State the most consequential outstanding decisions with your recommendations and the validation results. Separate incomplete source coverage from genuine source ambiguity. Do not call a provisional extraction estimation-ready merely because the files were generated successfully.

The desired end product is a **complete, reasoned and correctable first pass**: sufficiently detailed that Alex can review specific facts and judgments directly, without having to reconstruct the whole narrative himself or answer questions the model could already resolve.
