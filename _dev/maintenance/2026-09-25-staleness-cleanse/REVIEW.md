# Review of the revised v1.14 specification and staleness cleanup

25 September 2026. This pass is separate from the Opus upgrade. It reviews the specification and adds evidence-navigation repairs; it does not change the specification, instruction, pipeline code, workbooks, app state or deployment.

Reviewed specification: [V114_SPEC.md](../2026-09-24-bid-terms-taxonomy/V114_SPEC.md), SHA-256 `9ba2283084b7be28da0ff86a67a58fd8afca862a7985015087dab2c1aa89412c`. Findings below apply to that snapshot. Opus is actively changing the documentation; re-read it before treating a stale statement listed here as still present.

## Overall assessment

The revised spec is a better implementation handoff than the earlier Astra proposal. In particular, it accounts for the live-checker/deployment boundary, schema-specific editor behavior, immutable download semantics, preservation of working-copy review history, and the catalog dependencies of a later workbook relocation. These are concrete corrections to gaps in the earlier proposal.

I agree with keeping Regulatory Concern separate from an automatic Heavy result under the confirmed taxonomy. The old Astra proposal's Concern-to-Heavy rule was a proposed policy change, not something already authorized by the column set. D3/D27 now resolve it explicitly. I also agree with preserving existing working copies, treating the pilots as regression evidence, and preparing migration rather than rebasing onto a superseded pilot.

D5, D6, D9, D12 and D27 intentionally settle choices differently from the earlier proposal. They should be implemented as the decisions now recorded, with the provisional ones identified for Alex. In particular, Committed under D5 is the project's classification of the stated financing condition; it must not be casually described downstream as proof that funding documents were signed or cash was available. The Note preserves that distinction.

The early human checkpoint and full market-price series are expressly deferred. That is a scope choice, not a completed response to those parts of Alex's request. Likewise, D12 keeps material-ambiguity judgment instead of making every A–M item a mandatory model Question. Future status reports should say so plainly.

## Specific implementation concerns to resolve

These are targeted additions to the implementation/acceptance contract, not requests to reopen the adopted taxonomy.

| Priority | Location | Concern and concrete resolution |
| --- | --- | --- |
| High | [Package P, price derivation](../2026-09-24-bid-terms-taxonomy/V114_SPEC.md:755) | `package = upfront + CVR/earnout value` is too broad without a basis guard. The extraction intentionally preserves CVR maxima, face amounts and attributed valuations as different kinds of amount. Calculate only compatible reported bases; retain a basis label, both bounds for ranges, and missing when the package cannot be supported. A maximum can support a labelled maximum package, not an unlabeled comparable value. This is the same restraint E13 already requires. |
| High | [Package P, partial-only parties](../2026-09-24-bid-terms-taxonomy/V114_SPEC.md:783) | “A Who whose every bid row is an Other-scope bid” does not establish that its earlier participation was partial-only. Example: a bidder enters whole-company discussions, makes no priced whole-company offer, then switches to a division offer. All its bid rows can be Other-scope even though it was previously a whole-company participant. Use supported scope intervals/entry and exit evidence. The whole-history heuristic may identify a review candidate; it must not remove earlier participation mechanically. |
| Medium | [Package P, T2](../2026-09-24-bid-terms-taxonomy/V114_SPEC.md:760) | Equal price cells must mean two present, valid numeric values. Two blank cells must not establish a point offer merely because they compare equal. Preserve missingness for an unavailable price, and test the unsplittable-package case explicitly. |
| Medium | [Field-level inference](../2026-09-24-bid-terms-taxonomy/V114_SPEC.md:185) and [D22's inferred-exit switch](../2026-09-24-bid-terms-taxonomy/V114_SPEC.md:129) | Inferred = Y can describe the date or another material field of an expressly reported exit. Package P must not automatically interpret every Y exit row as an inferred departure. Preserve/identify the field being inferred; when the Note cannot resolve that mechanically, emit a review requirement rather than a false dropout classification. S1 already acknowledges this distinction when removing its old inferred-reason check. |
| Medium | [MIG triage](../2026-09-24-bid-terms-taxonomy/V114_SPEC.md:731) | “Agrees: accept, with a seeded spot-check” needs a status guard. A new result agreeing with an old Needs decision or unsupported fact does not resolve it. Only unchanged, supported facts can qualify for the agreement/spot-check path; unresolved, reverted or disputed facts remain review items, and new columns have no inherited acceptance. The reviewer still authorizes the port batch. |
| Low | [Acceptance wording](../2026-09-24-bid-terms-taxonomy/V114_SPEC.md:914) | Add “by itself” after Regulatory Concern in the prohibition on Concern making a bid Heavy. D3/D27 correctly allow an explicitly stated regulatory dependency to establish H3. The current absolute wording could make R reject that valid explanation. |

Suggested focused fixtures: incompatible CVR value bases; an unsplittable package with both price cells blank; whole-company entry followed by the first priced offer being partial; a reported exit with only its timing inferred; and a repeated unresolved fact in MIG. These test consequences of the rules rather than duplicate their wording. No tests or model runs were launched in this review pass.

## Live state used to distinguish current from stale

Read from SQLite through `mode=ro` in a read transaction; no live HTTP requests or service actions.

| Item | Observation at this pass |
| --- | --- |
| Repository instruction | v1.13.2, SHA-256 `513c8e3e8159e4a6bceccd6ffca32a246302736329a0c7137b64dd3b7ffcd304`. |
| Cockpit default | Published `v1.13.2`, id `513c8e3e8159`. |
| Other cockpit instructions | Two drafts: an unchanged v1.13.2 copy and the September 24 taxonomy draft `a4ca26ecfa92`. No published v1.14. |
| Checker on disk in the live checkout | 1.6. This pass did not make an HTTP claim about what a running process has loaded. |
| Deals and versions | Nine catalog deals plus four added deals; seven imported run versions across the catalog/added deals. |
| Edited working copies | Mac-Gray 8; P&W 16; Kraton 4; Meredith 4; PetSmart 2; Penford 2; sTec 1; Synacor 1. Datalink has no saved revision. |
| Deal-level acceptance | `deal_review` has no rows. Row review labels and saved edits do not establish deal-level acceptance. |
| Extraction jobs | Seven completed, one cancelled; no extraction job in an active state in the queried snapshot. This is not permission to deploy. |
| Root disk | `df -h` showed 82% used and 1.7 GB available; `/home/uctpiaj/work` had 324 GB available. The spec's 97%/341 MB figure is an earlier snapshot, not the present cleanup justification. |

## Cleanup performed without overlapping S6

1. Added [RECOMMENDATION_REVIEW.md](../2026-09-24-bid-terms-taxonomy/RECOMMENDATION_REVIEW.md) as a short redirect to the renamed historical review and the current specification. This repairs two relative links in the byte-preserved Astra approval document without modifying that document.
2. Added [sources/README.md](../2026-09-24-bid-terms-taxonomy/sources/README.md), identifying the Q&A's new location and verified hash. The original manifest is preserved as a capture record, including its historical temporary path.
3. Recorded this review and a bounded verification inventory beside it. Opus retains ownership of S6's current-state documents and all upgrade implementation.

The before-scan examined 20 Markdown documents: the top-level taxonomy packet and eight selected project/lesson entry points. It found five broken link occurrences. The two renamed-review occurrences are repaired by the pointer. The other targets below need disposition; the scan is not a whole-repository broken-link audit.

## Remaining staleness register and ownership

| Item | Correct treatment | Owner/timing |
| --- | --- | --- |
| README, HANDOFF, research register, cockpit guide, chronology and pilot navigation | Refresh current claims, with distinct now/deploy/release wording. S6 already specifies this. Edits appeared during this review, so do not overwrite its work. | Opus S6, now or at the stated gate. |
| `ASTRA_APPROVAL_SPEC.md` still says awaiting approval and contains rejected recommendations | Historical proposal, subordinate to V114_SPEC. Preserve the pinned bytes. Link to the current decision record at navigation points; do not treat old Package A as the active scope. | Navigation cleanup; no rewrite of the preserved source. |
| Old integration memo at `/home/uctpiaj/work/tmp/sec-v114-alex-integration-2026-09-25.md` | Two references remain, in ASTRA_APPROVAL_SPEC and INSTRUCTION_CHANGE_PLAN. The original file is absent from the checked location. If an exact preserved copy is found, link to it; otherwise mark the reference unavailable in a location/disposition note. Do not pretend the memo was relocated or recreate a new document under its historical identity. The preserved approval spec contains its own concern mapping. | Historical-reference follow-up. |
| CHRONOLOGY link to deleted `2026-09-22-doc-refresh/README.md` | Replace the dead current-path link with a historical Git reference: `6980189^:_dev/maintenance/2026-09-22-doc-refresh/README.md` exists. Preserve the dated event. | Opus S6; do not restore a retired current-looking packet. |
| `sources/manifest.json` old `qa.source` | Capture metadata with a now-obsolete location. Use the new sources README; the relocated DOCX matches the recorded SHA-256. | Location note added; original manifest retained. |
| Decision count in V114_SPEC table of contents and release-row template | D27 exists; the two D1–D26 references should read D1–D27. Older audit snapshots mentioning D1–D21 can stay historical. | Spec owner, small editorial repair. |
| `lesson/README.md` pre-revert revisions and broad review claims | Read alongside the independent audit and September 24 reverts. A current navigation pointer should lead there; do not rewrite historical lesson verdicts as if they were new findings. | S6/lesson navigation. |
| Q identifiers reused across documents | Qualify the document/date, especially historical Q3/Q7 versus the September 24 questionnaire. “Already answered” must identify which question, not just its number. | S6 and A2. |
| Old taxonomy drafts, pilot XLSX files, receipts and review packets | Retain: they are baseline, regression or provenance inputs. Superseded policy is not the same as disposable evidence. | No deletion in this cleanup. |
| `v114-scratch`, package copies, builds and pre-existing patches | Active upgrade workspace. Remove only after its owner has preserved deliverables and release/rollback evidence. | Opus after completion. |
| `extraction/`, catalog paths and raw versions | Relocation is D25 at the release gate. Doing it as a staleness cleanup would break existing resolution/provenance assumptions. | Release only. |

A staleness pass should make it obvious which document is authoritative and which artifact is historical. It should not globally replace v1.13.2 with v1.14, erase unresolved decisions, delete the test baselines, or describe unshipped code as deployed.

## Completion boundary

Only additive navigation/review files were created by this pass. Existing specification/source bytes are protected, and the active Opus-owned documents and code were not edited here. The implementation concerns above are supplied for review; they are not silently applied to Austin's decisions. No model run, deployment, publication, database mutation, external message, commit or push was performed.
