# Proposed v1.14 amendment after the blinded trial

> **Status note, 26 September 2026 (added after the v1.14.1 candidate; body unchanged).** Superseded by [V1141_SPEC](../2026-09-26-v1141-streamline/V1141_SPEC.md) §7 and the v1.14.1 candidate (`8bdb7c20…8a79`). A1–A4 were not adopted as drafted: R1 (Same offer) and R2 (evidence window, forecasts count) replace A1; R3 and H2/H3 replace A2; A3 survives inside v1.14.1 E12 H2 (R4); H4 and E10 replace A4. **P1 (§5) still stands** and is implemented under [PIPELINE_UPGRADE_SPEC](../2026-09-26-v1141-streamline/PIPELINE_UPGRADE_SPEC.md) WP3 item 1. The Astra-default engine choice described here was reversed the same day: Opus 5.5 medium is the default again (decided and built; live after the WP1 deploy).

**Status: proposed for Austin's approval. The instruction and analysis tool have not been amended.**

26 September 2026. Baseline: the tested instruction candidate, SHA-256 `c2d47a479d09eb46d0ab9fbf887568fcf13e972e2e11acbf08d5cdfab468ab27`, and the existing approved [V114_SPEC](../2026-09-24-bid-terms-taxonomy/V114_SPEC.md). Evidence: [verified Pro findings](PRO_FINDINGS_VERIFICATION.md).

## 1. Recommendation

Keep the worked-out taxonomy and the four-sheet, 29-column ledger. Make four short clarifications to the instruction and amend one part of the downstream analysis contract. Add the verified failures to the review checklist. Most observed errors already violate the candidate and do not justify extra categories or a longer decision tree.

The separate choice of **GPT-6-Astra high as the extraction default is approved and implemented**. That operational change does not publish this candidate or accept any trial workbook for research.

Approval of this amendment would authorize preparation and testing of the changes below in the isolated upgrade tree. It would not, by itself, authorize an extraction, a workbook correction pass, publishing an instruction, rebasing a working copy, deployment of v1.14, a commit or a push. Those remain the existing release actions; no new approval framework is introduced here.

## 2. Decisions this amendment preserves

- **Formality and Conditions remain separate.** A document-engaged bid may be Formal and Heavy. A late negotiation is not automatically Formal; retain E11's three routes and its price-only revision rule.
- **CVR/earnout remains consideration.** It does not itself make a bid Heavy or prevent None. Preserve the separation of upfront price, contingent value and the stated basis of that value (D4/E13).
- **Heavy remains H1, H2 or H3.** Preserve financing precedence including the express no-financing-condition rule (D5); substantive/at-least-two-week diligence with the confirmatory exception (D27); and an explicit material dependency for H3. Do not make every open diligence task, regulatory concern or exclusivity request Heavy.
- **Bidder commitment revisions remain Bid rows** under D13/E10, including a material change without a newly stated price. Separate exclusivity events remain as D15 requires. Do not add a new event label or a new extraction column.
- **Express incorporation remains limited in scope.** The instruction does not fill every later bid from the previous row. `Bid reaffirmed` retains its existing standing-price exception and qualifying conditions.
- **Inferred exits remain distinguishable from reported exits.** Preserve E14's bounded closure convention. A constructed closure is not a directly observed dropout decision.
- **Research choices remain explicit analysis alternatives with no primary default** under D22. This proposal does not pick a count estimate, a Formality reading, a treatment of Unclear, or a dropout/censoring assumption on Alex's behalf.

## 3. Proposed instruction edits

### A1. Distinguish offer terms from facts that can change over time

**Location:** E10, Express incorporation, with a short cross-reference in E12. Replace the current status-fact sentence with the following language; retain the surrounding missing-value rules and the existing reaffirmation exception.

> Carry only the offer terms within the filing's stated reference to an earlier proposal. A statement about an earlier state of affairs—such as unfinished diligence or financing documents that were not yet committed—is not itself a term that the bidder has agreed to keep unchanged. Code that state at the new bid date from evidence the filing dates to then or expressly says continues through then. An expressly carried financing condition or no-financing-condition term does carry. When current status is not established, use Not stated and retain any material earlier fact, with its date, in the Note; Not stated does not mean that the earlier issue was resolved.

**Purpose:** prevent both unsupported copying and the opposite mistake of treating silence as an improvement. This directly addresses MG6 while preserving the supported sTec June 10/14 treatment in ST7. A “same offer” reference need not repeat every price term, but it does not mechanically update every historical condition fact.

**E12 addition after the opening date rule:**

> A later passage may establish an earlier fact only when it dates that fact to the bid or identifies it as applying then. A later assessment or improvement is not knowledge at the earlier bid date. Apply E10's distinction between incorporated terms and dated status facts.

This does not require evidence to appear in the bid paragraph. Source order and event time remain separate: later-written text can expressly describe an earlier state.

**Acceptance examples:**

| Generic source situation | Required treatment |
|---|---|
| An earlier offer depended on obtaining financing; a revision expressly retains all its conditions. | Carry the financing condition, cite the reference, apply H1 unless the existing precedence rule changes the result. |
| At an earlier date no commitment letter had been supplied; a later proposal repeats its price and is otherwise silent about financing status. | Do not convert the earlier document status into a confirmed current state. Financing Not stated; retain the dated earlier fact in the Note. |
| A later paragraph explicitly says diligence was still ongoing throughout an interval that includes the bid date. | That is usable evidence of Incomplete at the bid date; H2 still needs its own evidence. |
| Confirmatory diligence begins after an earlier bid, or a board assessment occurs later that day. | Do not use it to improve or newly characterize the earlier bid's condition state without a retrospective link. Record the later development where material. |

### A2. Make population uncertainty constrain the recorded event

**Location:** E14, immediately before the inferred-closure alternatives. Add one paragraph, without changing their order or labels.

> Apply each transition only to participants whose membership and timing fit that transition. A population reported over an interval is not automatically the group eligible for a deadline inside the interval. A residual subtraction does not establish invitation, non-submission or an exact departure date unless those premises are supported. If named parties may overlap a cohort, do not record them as additional disjoint entries; retain the supported bound or unresolved membership under E3. Carry the same uncertainty into the event label, date bounds and Rounds account. A caution in the Note or a Question does not make a conflicting exact cell supported.

**Purpose:** enforce existing E3/E14 consistently across cells and prose. This is supported by MG1–2 and PW1–3. It does not impose a universal residual such as PW's 16–24 and does not require guessing anonymous identities.

**Replace delivery check F.2 with:**

> Every stated population total reconciles to its rows as an exact count, a bound or an estimate, with no party counted twice. The recorded entries, exits and Rounds account use the same population and timing assumptions; a qualification in prose is reflected in the cells it qualifies.

**Acceptance:** an NDA cohort accumulated after an early deadline cannot all become Did not submit by that deadline. A complete later advancing set may bound closure under E14. An unknown overlap stays unknown in the main account, even when a nominal subtraction is shown for explanation.

### A3. Clarify what duration can trigger H2

**Location:** E12's existing paragraph explaining H2. Add one sentence after the exclusion of exclusivity, signing and negotiation periods.

> A single period requested jointly for diligence and agreement negotiations does not establish that diligence itself requires that period; apply H2 only if the filing separately supports substantive remaining diligence or a diligence period of at least two weeks.

**Purpose:** remove the tempting but invalid reading in PW4. This is a clarification of the current threshold, not a higher threshold or a new category. A stated three weeks of remaining diligence still triggers H2, subject to the existing express confirmatory/limited exception. Sixty days of exclusivity for diligence and drafting does not trigger H2 from duration alone.

### A4. Make the role of a non-price Bid explicit

**Location:** E10, after the material-revision paragraph. Add two sentences.

> A Bid row can record a material change in commitment without a newly stated price; its existence does not establish a new price observation. Describe what changed in the Note, and fill the price and condition fields only as the evidence for that communication and the rules below permit.

**Purpose:** preserve D13 while preventing either loss of the sTec standstill condition or invention of a fresh Mac-Gray price. Do not require a new Note tag whose wording a downstream script would mistake for authoritative classification. The analysis tool will expose the available price data mechanically (P1).

## 4. Items to enforce under existing rules, without new instruction clauses

These belong in a compact reviewer checklist and synthetic examples, not an additional taxonomy:

1. **Current evidence for every Heavy trigger.** Name H1/H2/H3 and the fact supporting it. Ongoing diligence alone is not H2; comparative funding risk alone is not H1; ordinary approvals alone are not H3.
2. **Material commitment changes appear in bid fields.** The sTec standstill condition must not disappear into a row whose condition columns are inapplicable. A new price need not be invented to create the row.
3. **Keep information events.** Check material differences in access, synergy discussions, forecasts supplied after price agreement, and the distinction between knowing a rival improved and knowing its exact price. Existing E2 covers these. Do not create an event for every routine contact.
4. **Keep offer bases.** Preserve costs, transaction-expense assumptions, upfront versus contingent components and the valuation basis. Do not compute unsupported comparable prices.
5. **Do not revise history from later scope.** Apply E1/E3 to a later asset-only proposal without asserting that earlier intentions were known.
6. **Check references and map boundaries.** Every “revises #n” points to the intended bidder/event; a rival's withdrawal does not itself create a new round. Source-context date inferences are disclosed when consequential rather than automatically rejected.

Mechanical checks may identify inconsistent cells and broken references. They must not certify membership, diligence progress or the meaning of a filing passage. The filing review remains necessary.

## 5. Pipeline amendment P1: price availability in the analysis output

**Existing implementation:** the upgrade already has `derive_analysis.py`, an analysis contract and D22 switches. This is an amendment to them, not a new analysis system.

**Reproduced problem:** Mac-Gray A #61/#62 have no stated price, yet both `price_obs__same_price_as_new` and `price_obs__same_price_as_terms` equal 1. See [diagnostic bids.csv](analysis-diagnostics/mac-gray/bids.csv) and the verification report. The current contract explicitly sets the first flag to 1 for every bid row and suppresses the second only when numeric prices match a previous row. Thus both versions can count a commitment event with no available upfront price.

**Proposed behavior:**

1. Preserve one `bids.csv` row for every current Bid/Bid reaffirmed event, including undisclosed-price and commitment-only events. Do not alter the workbook or fill missing prices.
2. Add `upfront_price_kind`, derived only from validated Price low/high: `point`, `range`, `lower_bound`, `upper_bound`, `not_available`, or `invalid`. A point requires two valid equal numbers; a range requires valid ordered unequal endpoints. Invalid types, nonpositive values and reversed ranges are invalid and generate a review item.
3. Both `price_obs__same_price_as_*` flags become 0 for `not_available` or `invalid`. For valid point/range/bound data, retain the existing same-price alternatives. The flags identify observations containing usable numeric upfront-price information; users of point-price models must also require `upfront_price_kind = point`.
4. Do not equate `not_available` with “no economic price” or “commitment-only.” It can also mean an undisclosed offer or an inseparable consideration package. Those events remain in the output with CVR, price-basis Notes and all other fields. A material non-price event remains valuable even though its price-observation flags are 0.
5. Keep `same_price_revision` as the existing comparison of recorded numeric price/CVR values, and explicitly document that equal recorded figures do not prove identical economic terms. Keep Bid reaffirmed distinguishable through Event. This amendment does not settle Alex's treatment of reaffirmations or repeated same-price commitments.
6. Bump the analysis contract and tool version for this semantic change (currently contract `0.1`, tool `0.2`), record those versions in the manifest, and list affected output fields in the change note. Old outputs remain interpretable under their old contract.

**Files, if approved:** isolated upgrade `_dev/tools/derive_analysis.py`, `test_derive_analysis.py`, relevant tool README; main maintenance `ANALYSIS_CONTRACT.md` as the contract source, with the spec's output-field table reconciled. Keep the publication instruction untouched until its separate version step. No cockpit schema, catalog migration or extraction workbook column change is needed for P1.

**Required offline tests:**

| Input case | Expected result |
|---|---|
| A Bid with both prices blank but a material commitment condition. | Event preserved; kind not_available; both price-observation flags 0; condition preserved. |
| A package whose compatible upfront component cannot be separated. | No invented upfront price; kind not_available; package basis and contingent data retained. |
| Valid equal endpoints, valid range, lower bound, upper bound. | Distinct kinds; numeric-price candidate flags retain the existing same-price alternatives. Only equal valid endpoints qualify as a point. |
| Invalid/nonpositive price or reversed range. | Kind invalid, no usable-price flag, review item. |
| A repeated numeric price, an intervening blank-price commitment event, and a Bid reaffirmed. | Preserve documented comparison behavior and Event; do not infer unseen price continuity. Test the exact intended semantics so a refactor cannot silently change them. |
| Existing v1.13.2 and v1.14 fixtures. | Existing supported fields/readings retained; new output fields and versions recorded; inputs byte-identical. |

Re-run the offline derivation on the already supplied Mac-Gray A and sTec B to show the relevant no-price commitment rows remain visible without becoming usable price observations. This invokes no extraction model.

## 6. Questions for Alex and the voice-note reconciliation

Do not ask Alex to determine what a filing already states or to re-answer settled instruction choices. Retain the current replacement questionnaire's decision numbers and reconcile its text after approval; this proposal does not generate a competing DOCX.

**Keep for research decisions:** which Formality reading to use for the primary analysis; how to handle Unclear and financing walk-away protection; whether repeated same-price commitments/reaffirmations count as observations; whether constructed exits are dropouts or censoring; how to use ranges/overlapping populations; upfront versus contingent-package price when comparison requires it. These largely already appear under D5/D9/D22 and Decision 3/3b. Present conditional alternatives where the source cannot identify one fact.

**Explain as resolved by evidence or current rules:** CVRs do not trigger Heavy by themselves; markup and conditionality are separate; a long exclusivity request is not automatically a long diligence requirement; later favorable information cannot be backdated; a price known to the reader was not necessarily disclosed to a rival.

**Show explicit disagreements without silently rewriting Alex:** PW's August 4 offer has document engagement but the filing does not establish unconditionality; sTec's May 28 markup likewise does not prove None. The exact November–February cessation interval is unresolved. These should be short source-backed notes in the existing questions/crosswalk, with a recommendation, rather than a request to supply absent filing facts.

**Still outside this amendment:** market-price history and broader research data linkage. Alex's voice concern remains real, but blind extraction must continue using only the supplied filing and instruction. Also, this three-deal verification does not certify that every concern in every voice-document deal has been closed.

## 7. Implementation order and acceptance

1. Incorporate approved A1–A4 into a new candidate copy; never overwrite the trial's hash-pinned candidate. Prepare a line diff, update the change log and reconcile the introduction with the unchanged taxonomy. No extra thesis or deal-specific rules are needed in the introduction.
2. Update the approved spec's affected prose and the existing Alex-question crosswalk so they agree with the candidate. Preserve explicitly provisional decisions as provisional. The trial baseline, voice source and Pro report remain intact.
3. Implement P1 and its focused offline tests; update the analysis contract, version and examples. Add the existing-rule reviewer checklist with the evidence links above.
4. Check the instruction for internal consistency: missing values, carry rules, H1–H3, CVR, Formality, E10 revisions, E14 exits and the final delivery checks must agree. Verify native output enums and column count remain unchanged. A checker pass is mechanical evidence only.
5. Reconcile the 25 September release/deploy patches against the now-live Astra-high default and the current upgrade tree. Preserve legacy Opus job labels, explicit engine choices and per-run model/effort provenance. Do not apply old patches blindly.
6. Present the resulting candidate, source verification and offline results for the existing release decision. A further blind model test, if Austin wants one, should be separately authorized and use an isolated filing/instruction environment. Do not automatically repeat the 15-run sweep.

**Completion standard:** the wording does not force uncertain history into precise cells; conditions are judged at the correct date; every material commitment remains extractable; no event with an absent/invalid upfront price is advertised as usable numeric price data; existing research switches remain visible; every approved default route selects Astra high without changing old provenance.

## 8. Changes already made versus still proposed

| Work | State |
|---|---|
| Astra-high default in cockpit and isolated runner, including matching upgrade code | Implemented and live for the main cockpit; upgrade remains undeployed. |
| Verification against supplied filings/workbooks and relevant Alex passages | Completed within the bounded scope in the verification report. |
| A1–A4 instruction wording | Proposed here only; no instruction changed. |
| P1 analysis contract/tool amendment | Reproduced and specified; not implemented. |
| Existing-rule workbook corrections | Identified; no corrections applied. |
| Updated questions-for-Alex DOCX | Reconciliation specified; not edited. |
| Additional extraction, v1.14 publication/deploy, commit/push | Not performed. |
