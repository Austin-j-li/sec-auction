# SEC auction project review — 9 October 2026

**The project has a substantial Version 1 instruction and an operational app. It does not yet have an accepted research dataset.**

Version 1 addresses most of Alex's collection requests. Several detailed rules reflect Austin's approved conventions. Four themes remain deferred. The live outputs contain material departures from both the instruction and adopted decisions.

**Assessment: needs revision before research use.** This assessment applies to the data and derived tables. The report itself supplies evidence for the next decisions.

## What exists now

The review separates the repository, deployment, raw outputs, and research acceptance. These states differ.

| Layer | Verified state | Consequence |
|---|---|---|
| GitHub `extraction-v2` | `2e78102`, merged 8 October | Contains the recent count, price-mask, and review-panel changes. |
| Original VM checkout | `e0f73ee`, nine commits behind GitHub | Its status file incorrectly says no extractions exist. |
| Live cockpit | `9f0750e`, deployed 29 September | Does not contain the new mandatory-review panel or analysis fixes. |
| Instruction | Same approved 28 September Version 1 in all three states | Hash `05d8668d7778eb3e985599fec0a42c62fd4e41575e542af935d2d4ff8af05de4`. |
| Raw live outputs | 13 Opus 5.5 medium workbooks, all from 28 September | 696 ledger events and 37 round rows across the files. |
| Recorded human review | No revisions, review decisions, comments, or threads | All 13 show revision zero and Unreviewed. |
| Repository exports | `extraction/` contains only `.gitkeep` | The live outputs exist, but no repository export records acceptance. |
| Model comparison | 16 separate workbooks; two deals; one run per setup | Limited evidence for the default model, not a general accuracy estimate. |

The live inventory began at 15:35 BST on 9 October. Its technical receipts retain UTC timestamps. All 13 live files match their recorded hashes. The cockpit and worker run from the separate deployment checkout. No extraction job is active or failed. [Inventory and exact commands](live_inventory.md).

The browser confirms 13 Unreviewed deals. The sTec Review tab shows zero recorded findings and the mechanical result. It has no mandatory-review panel. Ordinary browser use can update view markers; no workbook or review-status edit occurred.

## Does the state address Alex's voice note?

**Largely at the rule level; partly at the workflow level; insufficiently at the verified-data level.**

The team compared all 187 original Word paragraphs with the saved transcript. They match after removal of labels and color markers. The paragraph count includes empty paragraphs. Paragraphs 129–166 contain an embedded Claude summary; Alex endorses that summary at paragraph 168.

The rulebook now separates Formality from conditions. It also distinguishes process boundaries, round boundaries, contacts, NDAs, partial scope, exits, and announcement events. These changes address central concerns in the voice note.

| Alex's concern | Current response | Assessment |
|---|---|---|
| Infer rounds from the actual process, not its labels | Selection and renewed-request rules in E6 | Implemented in the instruction; live Datalink violates the rule. |
| Separate Formality and conditionality | Separate columns and T0–T3 variants | Implemented. No primary estimation variant is selected. |
| Reconcile contacts, NDA signers, cohorts, and exits | E3, E7, E14 and analysis tools | Substantial implementation; residual-count defects remain. |
| Preserve substantive price and commitment changes | E10 and price-observation masks | Implemented in principle; a real backward price revision disappears from current analysis. |
| Record later confirmation and changed commitment | Same-offer and document-confirmation rules | Approved differences remain: Providence August 4 is Light; Penford confirmation starts October 8 rather than Alex's October 14 example. |
| Flag important cases for human review | Uncapped model Review items plus 14 script categories | New GitHub adapter returns 193 prompts. Live users lack that adapter. |
| Consult the human before an incorrect round map propagates | Unattended extraction, then cockpit review | Explicitly deferred by Austin under O2. This does not deliver real-time intervention. |
| Measure deadline discipline | Dates, extensions, outcomes, and review prompts | Recorded, but the current Enforced definition differs from Alex's soft-deadline example. |
| Keep partial deals separate | Other-scope bids; Meredith excluded from structural estimation | Implemented and settled. Descriptive use remains. |
| Link the reviewer directly to source pages | Quotes, pages, cockpit navigation | Partly delivered. The runner-written filing link remains deferred under O7. |
| Capture price-normalization inputs | Limited filing reference values | Deferred under O5. No complete market-price series follows from these workbooks. |
| Address regulatory risk in Heavy | Regulatory column exists | The additional Heavy convention remains deferred under F8. |

The phrase **“no questions for Alex”** records a decision-log status. It means Austin resolved the listed conventions or decided on Alex's behalf. It does not establish Alex's personal approval of every rule, source certainty, or dataset acceptance.

The 41 themes each have a recorded disposition. Four dispositions are deferrals. The full request map separates direct alignment, added conventions, deferrals, and source ambiguities. [Voice-note assessment](voice_alignment.md).

## Material data findings

### Datalink loses a round and retains two bidders too long

The live workbook has four rounds. The approved map requires five.

The filing admits five parties on July 27. Its August 16 final letters name only Insight, Party B, and Party C. The instruction makes that narrower common request a new round.

The workbook instead records August 16 as a deadline event within round 2. Its Question assumes that the two unnamed parties were implicitly invited. It closes them on August 30.

That unsupported assumption removes a stage and retains two competitors for 14 extra days. The October 26 opening already exists. Its number becomes five after the missing August stage is restored.

Evidence: live Datalink `Rounds!B2:B5`; `Deal ledger!E38/G38`, `B42/E42/T42`, `E70/G70`; `Questions!C4`. Filing lines 3305 and 3332; instruction lines 193–197 and 328–336; decision log line 267. [Detailed source findings](technical_findings.md#datalink-round-and-participation-error).

### A backward price revision disappears from current analysis

Providence Party E offers $21.26, raises it to $23.81, then returns to $21.26. The source confirms that sequence.

The workbook labels the last row `Same as #33`. Current code suppresses every such row from both price-observation variants. It therefore removes this real downward revision. E10 expressly preserves a return to an older price as a revision.

The underlying ledger label requires review. The checker also needs to detect the intervening price change. Ordinary exclusion of a copied, unchanged price remains correct.

Evidence: Providence ledger events #33, #50, #52; filing page 30; `derive_analysis.py:713–772`. [Technical finding](technical_findings.md#price-reversion-and-observation-masks).

### An uncertain total becomes an unsupported competitor minimum

Medivation reports several NDA signers, including named parties. The residual cohort Note subtracts Sanofi and perhaps Pfizer from that total.

The current parser reads “several” but ignores that subtraction. It assigns at least two additional parties and at least four live bidders. The source does not establish that residual minimum.

Evidence: Medivation ledger #9; filing page 22; `derive_analysis.py:257–262`. This affects a core competition measure. [Technical finding](technical_findings.md#qualified-total-versus-residual-count).

### The sTec evaluation preserves a shared error

The preferred comparison workbook and the live workbook call May 3 “Extended (late bid accepted).” Both saved model grades endorse that result.

The approved correction says **Enforced**. Company D already gave a qualifying verbal offer on April 23; its May 10 document confirms that offer. Model agreement therefore does not establish compliance with the approved rule.

There is also a separate measurement limitation. Alex calls this deadline soft because activity continues before the May 15–16 selection. The approved Enforced label follows that later selection. It must not serve as an unqualified measure of timely deadline discipline.

These are two different issues: an output-rule conflict and a rule-research interpretation limit. [Source evidence and exact cells](technical_findings.md#stec-deadline-outcome-and-grader-conflict).

### Other recorded discrepancies need bounded source review

The comparison also exposes these differences from adopted anchors:

- PetSmart opens its first round on August 13. The adopted anchor is October 3.
- Synacor's third process opens its first round on July 19. The adopted anchor is July 13.
- Penford's ledger event #35 leaves price cells blank but quotes $17.50–18 in its Note.

The first two are verified workbook-versus-decision differences. They are not fresh authority to alter the adopted conventions. The third needs source review of the proposal and its price bounds. These observations are review leads, not an exhaustive source audit of those deals.

Synacor's six total round rows are not themselves an error. The approved structure has one round in each earlier process and four in the last process.

## What the completed comparisons establish

Today the team ran the existing comparator on all nine original live workbooks. Each command completed through its normal CLI. No new extraction or revision occurred.

| Deal | Reference labelled bids | Automatically aligned | Equal recorded Formality / aligned |
|---|---:|---:|---:|
| Datalink | 21 | 15 | 14 / 15 |
| Kraton | 15 | 13 | 8 / 13 |
| Mac-Gray | 13 | 13 | 13 / 13 |
| Meredith | 20 | 0 | 0 / 0 |
| Penford | 9 | 8 | 8 / 8 |
| PetSmart | 13 | 12 | 11 / 12 |
| Providence & Worcester | 14 | 13 | 11 / 13 |
| sTec | 7 | 7 | 7 / 7 |
| Synacor | 11 | 9 | 9 / 9 |
| **Total** | **123** | **90** | **81 / 90** |

The comparator processed 321 reference rows. Its 81 equal labels among 90 aligned bids are **not an accuracy rate**.

The limits materially affect interpretation:

- Seven bid matches use only price and date. One maps an individual to a two-bidder cohort.
- The comparator prefers the old precise-date column AA. The inherited comparison uses Alex's edited rough-date column AB.
- Event matches can accept dates 31 days apart. An “agree” result can conceal a material timing difference.
- The comparator omits unmatched ledger events from a separate coverage denominator.
- Meredith's 20 unaligned bids reflect the whole-company filter. They do not establish 20 missing events.
- Alex's reference mixes original Chicago entries and later corrections. Only seven labelled bids in this comparison carry a red `bid_type` correction.
- The reference lacks equivalent Process, Round, Conditions, and participation-total fields.

Alternative Formality equality counts are T1 78/90, T1u 69/90, T2 81/90, and T3 80/90. These are descriptive comparisons. They must not select the estimator variant by fit to hand coding.

The complete CSVs and hash receipts are in [alex_comparison_outputs](alex_comparison_outputs/). [Comparator assessment](alex_comparison.md).

Alex's reference also contains source conflicts. The team verified Meredith's $16.51 versus $15.51, Kraton's $42–45 versus $42, and Datalink's price/signature dates. The filing governs those facts. A reference match can be wrong, and a reference disagreement can be right.

## The model evidence supports only a provisional default

The retained comparison covers Imprivata and sTec, with one run per setup. Opus medium ranks first in two separate three-way comparisons per deal. Those comparisons reuse the same Opus output.

The Imprivata source supports an important Opus advantage. Competing Sol and Astra workbooks turn Sponsor B's hypothetical price statement into a Formal bid. The source later says only Thoma Bravo submitted. Opus medium preserves that distinction and the appropriate non-submission event.

But Opus supplies all four saved grades. Opus high and Astra have no saved grades. The sTec shared error shows why this evidence cannot establish general accuracy.

**The graded Opus workbooks differ from the live Opus workbooks.** The sTec comparison has 66 events; the live file has 63. The Imprivata comparison has two processes and bidder-led initiation; the live file has one process and mixed initiation.

The comparison rank cannot transfer to those live files. Deleted prompts, event logs, and sandbox inputs also limit retrospective provenance checks. The retained Imprivata filing supports factual review but does not restore the original packet.

Ruling 9 requires separate reporting for codings that depend on rules developed from individual deals. No accepted evaluation on unseen deals establishes generalization. [Saved comparison record](../../model_comparison_2026-09/README.md).

## Pipeline and operational findings

**The isolation gap needs repair before further blind runs.** The sandbox shares the host network, while the model retains shell access. A benign request with those network flags reached the live deal API.

This proves access capability. It does not prove that any saved extraction used outside evidence. The instruction's prohibition remains clear, but the technical barrier does not enforce it.

The current implementation also has these bounded concerns:

| Finding | Effect | Evidence status |
|---|---|---|
| New review queue absent from live app | Users lack 193 cell-derived prompts available in current GitHub code | Code, real workbook adapter use, and browser verified. |
| Publish action omits displayed instruction hash | A stale browser can publish another user's later draft | Latent defect from source review; no claim it occurred. |
| Row Reviewed mark survives content edits | A changed row can retain an obsolete review mark | Latent defect; whole-deal edited-since notice partly mitigates it. |
| Round check compares cumulative and simultaneous participants | Valid histories receive false inconsistency warnings | Verified with Synacor, Mac-Gray, and Imprivata. |
| Download paths still target the work disk | Next download would miss the supplied RDSS storage rule | Source and resolved paths verified; no post-rule download alleged. |
| Backup schedule has a gap | Scheduled continuity is unproved | Latest backup hashes match; gap cause unknown. |

The latest backup is from 14:42:50 BST today. All 110 recorded file and database hashes match. A restore did not occur. No manifest exists for 8 October or today's scheduled 04:30 BST run. The available journal does not explain the gap.

The retained external filings predate the storage rule. Future downloads still use the old paths. A migration must preserve hashes and leave links for frozen inputs. No migration occurred in this review.

[Technical findings and verification limits](technical_findings.md). [Operational inventory](live_inventory.md).

## Mechanical checks are useful but insufficient

The current checker ran on all 13 live workbooks and their real filing paths. It reports 51 errors and 42 warnings. The stored receipts report 52 errors and 40 warnings.

The change removes one Medivation quoted-count error and adds two deadline warnings. Current errors comprise 41 Meredith Count errors, eight Synacor quote errors, one Datalink inferred-event error, and one Providence date error.

These are mechanical diagnostics. Their totals neither count all research errors nor measure severity. Datalink's omitted stage and Providence's lost price revision require substantive review beyond these counts.

The recent code makes useful improvements. It avoids duplicate entries from known cohort members, suppresses ordinary copied prices, cancels equal inexact entry/exit counts, and repairs round maxima. The defects above remain after those improvements.

## Completed, pending, and proposed

**Completed in the project:** Version 1 approval; traceable decisions; live cockpit; 13 raw runs; retained comparison artifacts; merged 8 October tool changes.

**Completed in this review:** three-state inventory; original voice-note verification; code review by Astra and Sol; current checker use; nine live/reference comparisons; selected filing checks; browser inspection; backup integrity checks.

**Pending in GitHub at review time:**

| Pull request | State | Meaning |
|---|---|---|
| [#7: Mixed initiation](https://github.com/Austin-j-li/sec-auction/pull/7) | Open; mergeable | Records Austin's 8 October sequence correction. Not in the reviewed base or live instruction. |
| [#5: Sol engine and priority tier](https://github.com/Austin-j-li/sec-auction/pull/5) | Open; conflicts | Needs integration with the current branch. |
| [#3: Cloud deployment route](https://github.com/Austin-j-li/sec-auction/pull/3) | Open; mergeable | Proposed route and release guidance; not a completed app release. |

PR #7 changes the mixed rule so the target must move first. Its author reports effects on Datalink, Imprivata, Penford, and Pepco. This review inspected the proposal; it did not rerun or adopt that branch.

**Proposed next steps, in order:**

1. Repair extraction isolation and the confirmed analysis/comparison defects in a separate change.
2. Resolve the open PRs and select an exact release commit. Deploy only on Austin's order.
3. Review the existing 13 originals against their filings. Preserve each original; record any correction as a separate authorized revision.
4. Start with rounds, live participants, price revisions, and Formality. Use the current report as a review queue.
5. Reconcile the nine original deals with Alex's reference and approved decisions. Separate source facts, conventions, and remaining ambiguities.
6. Obtain research acceptance before export for estimation. Choose Formality and inferred-exit treatments as research assumptions.
7. Evaluate unseen deals under the approved isolated process. Keep results from rule-development cases separate.

No new extraction, instruction amendment, workbook correction, deployment, or merge is authorized by this report. The review creates only reports and derived comparison evidence. Tests and test suites were neither added nor run.

## Scope and reading guide

Three Astra reviewers covered voice alignment, source quality, and analysis semantics. Three Sol reviewers covered implementation, live inventory, and the nine-deal comparison. The root agent reconciled their evidence and inspected the live browser.

This is a thorough project review, not a cell-by-cell semantic certification of all 696 events. The selected filing checks establish real defects. They do not establish the complete defect count.

- [Voice-note assessment](voice_alignment.md): requests, conventions, mandatory review, deferrals, and unresolved source readings.
- [Technical findings](technical_findings.md): source examples, code defects, comparison limits, and verification steps.
- [Live inventory](live_inventory.md): exact states, counts, paths, hashes, services, and backups.
- [Alex comparison](alex_comparison.md): interpretation of the nine CLI outputs.
- [Comparison evidence](alex_comparison_outputs/): per-deal CSVs and input hashes.

All source line references refer to `2e781023289eab42b7a3ead0b8d5977525450211`, unless explicitly marked live or proposed. This is a dated audit record. `_dev/STATUS.md` remains the project's canonical status document.
