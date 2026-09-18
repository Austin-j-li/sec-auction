# Readable Excel output for SEC merger-auction extraction
**Version 2.0 — presentation override, 18 September 2026**  
**Research: Austin Li and Alex Gorbenko**

## 1. How to use this instruction, and what it supersedes

Supply this document **together with** `SEC_Merger_Auction_Extraction_Instruction.md` and the new deal filing. The base instruction supplies the research definitions, event terminology, scope and interpretive rules. This document replaces its workbook-delivery design.

**Precedence:** this document controls whenever an output requirement conflicts with the base instruction. In particular, it replaces the ten-table mandate in base §1, the mandatory physical schemas and table names in §12, the requirement for a separate field-level Evidence table, and conflicting presentation, validation-report and final-delivery requirements in §§14–15. Do not create ten mandatory tabs and then add a dashboard. Do not reproduce every legacy column merely to claim compliance.

Keep the substantive requirements in the base instruction, including the distinctions among reported facts, inference, calculation and research convention; scope and eligibility; bidder units and cohorts; process and round assessment; dates; formality; conditionality; prices; exits; and required review categories. Translate those concepts into the arrangement below. A field no longer having a mandatory dedicated column is **not permission to omit its information**.

This is an output override, not an approval of the base instruction's proposed C1–C7 research policies. Continue to label those policies provisional unless the researcher has approved or replaced them. Identify any additional proposed substantive change separately, with its consequence and recommended resolution. Do not let a layout decision silently change what counts as a bidder, proposal, round, condition or exit.

The companion decision note and old example workbooks are not needed by a future extracting model. Do not copy historical example facts into the new deal.

## 2. Produce a complete first pass, not an assignment for the reviewer

Read the entire background and the other supplied filing sections needed to resolve transaction identity, consideration, source conflicts and final terms. Make your best-supported judgment on every relevant interpretive field.

A researcher should be able to read the deal from beginning to end and understand who did what, the proposals, changes and outcomes **without looking up an ID or joining tables**. Technical identifiers are for sorting, updating and export, not the ordinary reading interface.

Use short, professional sentences. Explain a legal term at first use when understanding it matters. “Party E restored its earlier $21.26 proposal” is better than “proposal reversion event”; the machine code can remain in a collapsed technical column.

When the filing supports an inference, give the inference and explain it. When it does not disclose a fact, state that limitation. Avoid both confident invention and indiscriminate “unknown” answers. A price may be reported while its formality is assessed and its date is approximate; do not attach a single evidentiary status to the whole row.

## 3. Workbook arrangement: five sheets, two principal reading surfaces

Use these five visible sheets, in this order:

| Sheet | Purpose | Ordinary review |
|---|---|---|
| **Deal guide** | Commercial summary, transaction facts, short process/round map, participants/advisers, scoped participation counts and a plain glossary. | Read first; consult later as needed. |
| **Timeline** | A continuous chronological account of material events. Names, prices and outcomes are readable locally. | Principal chronology surface. |
| **Offers** | Proposal histories and necessary document/condition checkpoints, with assessments and evidence beside each observation. | Principal bid-quality surface. |
| **Review decisions** | A small set of grouped decisions with complete model recommendations; separate human responses and correction history. | Resolve consequential issues, not every blank cell. |
| **Sources** | Locatable source passages and filing metadata; preferably the full background, plus the supplementary passages used. | Inspect evidence without leaving the workbook. |

Do not add separate Parties, Relationships, Processes, Rounds, Counts or Evidence sheets by default. Their research content has a home in the five sheets above. Small labelled tables within Deal guide are appropriate; do not force unrelated sections into one enormous filter range. Earlier processes belong in the same Timeline with a clear process label.

For an unusually complex case, do not multiply tabs automatically. First improve grouping, source access and the distinction between the principal view and its technical columns. An optional machine-readable companion is permitted, but it must not become necessary to understand or correct the workbook.

## 4. Deal guide

Put the transaction and a short commercial account at the top. Cover initiation, who organized the process, the main admission/information transitions, important price changes, the selection rationale, and signing/announcement/completion status. This should explain the deal, not describe the database.

Include compact, separately labelled sections:

**Transaction facts.** Target, acquiring economic bidder, relevant acquisition vehicle, agreed consideration and share basis, currency, signing date, public-announcement date, closing date/status, auction screen, scope/eligibility assessment, filing identity and source coverage. Distinguish the proxy's document date, the filing date established from available metadata, and dates appearing only in a filename.

**Process and round map.** One row per phase: readable phase name, source stage label where different, working start/end, date precision, submission objective, admitted population, information/access change, deadline history, announced versus inferred finality, and the short reason for the boundary. Show consequential alternative boundaries in the corresponding review decision, not on every downstream event. Do not replace an unknown deadline with the last observed offer or a committee meeting.

**Participants and relationships.** One understandable entry per relevant named party or population. Record bidder type and its basis, ownership/country when supported, aliases, adviser and client, acquisition vehicles, group membership, financing support, shareholder voting support/rollover, first observed participation and final observed status. These may be concise labelled phrases rather than many mostly empty columns. Distinguish a bank's renaming from a new mandate; an adviser’s first appearance from retention; a funding relationship from a consortium; and an unnamed cohort from one bidder. Separate individual histories when a relationship changes.

**Participation checks.** For each consequential number, show the population, counting unit, reported value and qualifier, derivation if applicable, overlap/exclusions, and reconciliation status. The source's aggregate assertion and an independently calculated total are not the same thing. A residual added back to the total from which it was calculated is not independent validation. Never sum parent totals and their component populations.

**Glossary and review instructions.** Explain NDA, IOI, LOI, markup, due diligence, exclusivity, conditionality, contingent consideration, signing and closing in ordinary language. State where human corrections go, how to restore the chronological view after sorting, and how technical columns are revealed.

A numerical total that is genuinely calculated must use a transparent formula with identifiable inputs when the workbook supports formulas. Do not let a formula impose a disputed identity mapping or erase a source conflict. Qualifiers such as “at least,” “approximately,” and “conditional on this interpretation” must remain visible.

## 5. Timeline: the deal can be read without joins

Use the following visible columns. Equivalent wording is acceptable; the meaning is not optional.

| Visible column | Required content |
|---|---|
| **Order** | Stable reading order. Sorting back to it restores the narrative. It is not automatically a claim of strict historical precedence. |
| **When** | Exact reported date, actual interval, “by” date, or source wording with an honest qualification. Use U.S. date display and a four-digit year. |
| **Stage** | Readable process and analytical round label. Include “before bidding,” “post-signing” or another appropriate context label. |
| **Participant** | Actor and affected party/recipient in words; preserve adviser-mediated direction, such as “GHF, for PWRR → bidders.” |
| **What happened** | Professional event label plus an independently understandable account, including the important price, change, count, request or outcome. |
| **Model assessment — why / limits** | Field-labelled interpretation, concise reason, uncertainty and consequential alternative. Do not repeat the factual description instead of explaining the assessment. |
| **Evidence** | Printed page/section and paragraph locator, with a short exact supporting quotation. Provide a working source link when possible. |
| **Review** | A short issue label or “no material flag,” linking to a grouped decision when applicable. |
| **Human correction / note** | Initially blank. A human can enter the corrected fact/interpretation and reason without overwriting the model answer. |

Keep names and prices in Timeline even though a focused version is also in Offers. This is a readable mirror, not a second submission. A proposal’s canonical offer record must remain identifiable technically.

### Granularity

Keep distinct submissions, price revisions, meaningful commitment changes, participation changes, deadline changes and signing/public-announcement events independently inspectable. A broad row containing a bidder's re-entry, two parties' revised bids, a reversion and a withdrawal is too compressed.

Do not log every routine post-NDA call or every draft exchange. Related administrative context may be summarized, but explicitly retain any component dates that matter. Such a context summary must not pretend that several actions happened on one date. Material actions affecting different bidders or a later participation outcome should normally be separate rows.

Preserve the difference between:
- a deadline being set, changed and reached as a scheduled milestone;
- target authorization and its implementation;
- an offer, a target asking price, a valuation statement and a document update;
- a bidder's withdrawal, target exclusion, non-submission, a proposal reversion and an unsuccessful outcome;
- signing, public announcement and closing.

No event code should contradict its local explanation. For example, a bidder allowed to continue diligence is not coded as excluded merely because the target warns that another bidder is preferred.

### Honest chronology

Do not make the model select a fictitious exact day merely to fill the visible date column. “After August 1; exact day not disclosed” is usable output.

Show literal intervals and qualified inferred dates first. Retain the base instruction's representative-date convention only in a separate technical field where applicable; never replace the reported window with it. Distinguish a preferred working boundary from an exact date pinned down by the evidence.

Respect known within-day sequences and explicit before/after relations. Overlapping independent windows can appear in a deterministic display order, but that order must be labelled as display-only technically. A representative date must not place a dependent event before its prerequisite. In a source paragraph summarizing multiple meetings, do not infer that every proposal arrived before the first meeting.

## 6. Offers: prices and judgments remain together

Use one row per economically distinct proposal version or alternative under the base definitions. Include a clearly labelled **checkpoint** when preserving a document or condition development is useful but a new submission or substantive commitment revision is not established. This is a presentation device; it does not redefine every draft exchange as a bid.

Use these visible columns:

| Visible column | Required content |
|---|---|
| **When** | Same date/precision as the canonical Timeline event. |
| **Bidder** | The economic submitting unit, not an adviser, financing source or later group retroactively substituted for it. |
| **Offer and change** | Observation kind, original price expression, units/basis, important cash/contingent components, and change from the previous proposal. |
| **Formality — model assessment** | Formal/informal/indeterminate, confidence, short reason, source terminology/document state and any consequential alternative. |
| **Completion conditions — assessment** | None/light/heavy/not assessable, confidence and material condition evidence as of this observation. |
| **Other terms / interpretation** | Relevant financing, diligence, exclusivity, consideration uncertainty, expiry, target response and normalization limits not already visible. |
| **Evidence** | Exact main quotation and actual source locators; identify additional premises for a cross-paragraph judgment. |
| **Review** | Grouped issue reference, with local meaning. |
| **Human correction / note** | Initially blank; preserve the AI baseline. |

Put the required categorical judgments in their own typed technical columns too. The visible explanation can combine the label and reason to save width; the underlying label must still be exportable without text mining.

**Assessments are as-of observations.** A next-day withdrawal does not itself establish a condition in today's offer. A financing representation in the signed agreement does not establish that an earlier LOI lacked a financing contingency. Expedited diligence is not automatically completed diligence; substantially executable documents are stronger evidence than silence.

**Separate dimensions.** Formality, legal bindingness, completion conditionality, consideration uncertainty and round membership remain distinct. A formal range is possible. Exclusivity alone neither makes an offer informal nor proves heavy completion conditionality. A contingent cash payment can still be cash-settled; a CVR's name alone does not establish its settlement medium.

**Prices.** Keep point offers, actual individual ranges, group-wide envelopes, partial endpoint constraints, target requests, valuation bounds and mutually exclusive structures distinct. Do not put a group envelope into individual-range columns. Do not turn an unknown value into zero or use a midpoint as an observed offer. Record carried-forward and calculated amounts as such, with the inputs and reasoning. A participant's refusal to increase a price is not direct observation of its private value.

**Checkpoints and counts.** Include `observation_kind` and separate flags for an individual proposal/reaffirmation, a newly stated price, a context/checkpoint and a group envelope. Checkpoints and mirrors do not add bidders or new priced submissions. Reaffirmation may be a legitimate proposal observation without a new price. State the counting unit before reporting a bid total.

## 7. Field coverage and technical columns

Use hidden or collapsed columns on the relevant sheet, not ten reader-facing tables. Keep enough fields for unambiguous sorting, filtering, correction propagation and export. Reveal instructions belong in Deal guide. A user must not need these fields to understand the deal.

At minimum preserve:

**For Timeline:** stable record key; process/round key or number; controlled event code and event role; exact reported date, lower/upper bounds and their basis; representative date/method only when used; reported source wording; known predecessor relation and whether order is historical or display-only; participant identity links; canonical offer link; source locators; review state.

**For Offers:** stable offer key and Timeline key; bidder unit; process/round; prior offer/alternative bundle; observation/revision kind; reported bindingness and document state; scope; price form/origin; currency and valuation/share basis; actual point/range values, separately named envelope values or explicit bounds; fixed cash and contingent components; settlement/all-cash status; normalization inputs/formula when relevant; categorical formality and conditionality; condition/financing/diligence/exclusivity facts; individual-observation and new-submission flags; evidence and review references.

**For applicable event-specific facts:** retain deadline scope/replacement/expiry type; admission destination; exit agency/reason/valuation reference; information change; decision-maker's rationale; publicity type; participant-count scope and overlap. Preserve these either in a typed field where used repeatedly or in a labelled detail field that is fully visible locally. Do not create hundreds of blank fields for inapplicable concepts.

Field-specific evidence, reasons and confidence remain mandatory for nontrivial judgments. They may live in the relevant judgement cell and a short labelled technical detail, rather than a separate normalized Evidence table. Different bases must be distinguishable: “Price: reported; formality: convention applied to submitted markups; financing: not disclosed.” A single confidence flag does not cover all three.

If a rare source fact does not fit the standard schema, retain it in a clearly named extra field or labelled detail, explain it, and flag only a consequential interpretation. Do not drop the fact to keep a table narrow.

## 8. Review decisions and human corrections

Create one decision packet for each underlying consequential question, not one per dependent row. For example, one round-boundary decision can cover ten affected bids; one bidder-history review can cover recurring condition assessments.

Each packet must contain the topic, priority and mandatory category; complete model recommendation; evidence and concise reasoning; meaningful alternative; specific affected entries; research consequence; and suggested human action.

Keep all mandatory review categories from the base instruction. Grouping is not waiving them. In the initial pilot, all conditionality assessments remain reviewable, but they do not require separate repetitive questions. A required verification is not automatically a blocker for the entire deal. State precisely which analytical use remains provisional.

Use human-only fields: **Pending / Accepted / Corrected / Deferred**, corrected value or interpretation, reason, reviewer and date. Leave them blank or Pending until a human acts. A model must not approve its own work.

Preserve an immutable AI baseline. A human note does not silently change another sheet. Either implement and test an explicit correction mechanism or explain that an accepted correction requires regenerating a versioned reviewed view. Update dependent phase labels, counts and mirrored prices together and repeat validation. Do not claim automatic propagation from free-text notes.

When demonstrating or repairing an earlier extraction, include a distinct **AI adjudication change log** on this sheet: original file/cell, former value or problem, new assessment, filing basis, affected demo records and whether the change is factual, mechanical or a proposed convention. Do not enter these changes as Alex's corrections.

## 9. Source access and spreadsheet engineering

Display the important quote and page beside the claim. Where practical, make the evidence cell a native hyperlink to the corresponding Sources passage. Use more than one premise when needed; never let a nearby but irrelevant quote stand in for support.

Sources should preserve paragraph identifiers, section, printed page, exact text, original filename and the source URL if established. Splitting a long passage into labelled continuation rows is acceptable if the text is lossless. Include the full supplied background when practical, so the source reader is not restricted to passages chosen by the extractor. Do not invent a deep link or accession number.

Use a single header row and Excel tables for each sortable section. No merged data cells, embedded subtotal rows inside data tables, empty spacer rows inside filter ranges, or multi-row “cards” that break sorting. Titles above tables can be merged.

Default to nine or fewer visible columns on the principal sheets, readable 10–11-point text, wrapped cells, restrained row heights, frozen headers and date/participant columns, and sensible widths at ordinary laptop zoom. Keep long prose bounded; use short field-labelled explanations and source access rather than tiny fonts or 300-character column headers. Do not solve width by shrinking a 70-column table onto one page.

Color may identify human-input cells or flags, but meanings must also be written. Validate human status categories. Store prices/counts as numbers and dates as actual Excel dates in technical fields; preserve display intervals as text. Use blanks plus meaningful status for unknown numerics, never “NA” mixed into numeric cells or zero-as-missing. Neutralize formula-leading source text; do not turn genuine negative numeric values into text.

No macros or unrequested external connections. Verify hyperlinks actually target the intended local passage and survive export. A converter's successful file save is not evidence that freeze panes, formulas or links survived. If a feature is unavailable, use a working transparent fallback and state the limitation.

## 10. Validation and final delivery

Before handing over the workbook, verify **substance and presentation separately**:

**Substance:** every relevant proposal, material revision, NDA/contact/admission/exit, round/deadline transition, rationale, relationship and focal date is covered; source quotes support their claims; cohort counts and identities are not double-counted; chronology respects supported precedence; formality/conditions are assessed independently; remaining source conflicts are visible.

**Engineering:** no broken or semantically stale references; no prior-offer cycles; typed columns travel with their rows when sorted; no formula errors or placeholder values; hidden fields are recoverable; mirror values agree; links, frozen headers and human-input fields work; no clipped consequential text.

**Review burden:** the deal can be understood from Timeline and Offers; every issue contains a recommended answer; repeated flags are grouped; difficult judgments have not been omitted to produce a cleaner appearance.

Report checks as passed, qualified or failed with a short reason. Do not claim scientific validation from spreadsheet consistency tests. Do not claim complete quotations were checked if only selected ones were compared.

Deliver the actual `.xlsx`, a short commercial summary, and the few consequential outstanding decisions. When actual file creation is unavailable, provide separate complete UTF-8 CSVs for the five-sheet content, with a source/comment convention and an explicit limitation about Excel formatting. Do not pretend plain CSV provides working workbook navigation.

The result should be a **complete, readable, evidence-supported and correctable first pass**. It should reduce the reviewer's navigation burden without taking away substantive information or the extracting model's responsibility to judge.
