# Review after the 9 October merges

**The checkout is current. The merged work makes real progress, but PR #11 needs a small correction before merge.**

The live cockpit and its original workbooks remain unchanged. The project still needs data corrections and source review before research use.

This report updates the earlier review at `2e78102`. It preserves that review as a dated record.

## Scope and snapshot

The team comprised two Astra reviewers and two Sol reviewers. Astra reviewed the rules and analysis semantics. Sol reviewed engineering standards and deployment state.

| Layer | Reviewed state |
|---|---|
| GitHub and the main VM checkout | `0707d3e066a9f024c523a3a8c5279dafc1f3a801`; clean `extraction-v2` |
| Open PR #11 | Base `0707d3e`; head `f894aeb67f1956f6d4109aee7d0c14c6ba94634d` |
| Live deployment | `9f0750e`; clean; separate deployment checkout |
| Main instruction SHA-256 | `87f4efdca62395a1a19ceb034c4ec61a4b1688705fa93683ce7739cec9761054` |
| PR #11 instruction SHA-256 | `3f67be55ca9eecaefd70d123d582888c8fb5fec48320f0a226f67b1644701252` |
| Live instruction SHA-256 | `05d8668d7778eb3e985599fec0a42c62fd4e41575e542af935d2d4ff8af05de4` |

The main checkout received a fetch and a fast-forward update before this review. A later remote check confirmed both reviewed heads.

Live verification occurred at 17:29–17:31 BST on 9 October. The database contains 13 raw versions and 13 completed extractions. It contains no revisions or review decisions. No extraction job is active.

## What the merges accomplish

| Merged PR | Result | Limit |
|---|---|---|
| [#3](https://github.com/Austin-j-li/sec-auction/pull/3) | Adds the cloud deployment route through ARC. | A runbook does not establish deployment. Austin retains release authority. |
| [#8](https://github.com/Austin-j-li/sec-auction/pull/8) | Preserves the first review and its comparison evidence. | Its statements describe the earlier snapshot. |
| [#7](https://github.com/Austin-j-li/sec-auction/pull/7) | Requires the target to move first for `mixed` initiation. | Original workbook values remain unchanged. |
| [#9](https://github.com/Austin-j-li/sec-auction/pull/9) | Repairs the principal price masks and detects residual count language. | Two analysis issues remain below. |
| [#5](https://github.com/Austin-j-li/sec-auction/pull/5), [#10](https://github.com/Austin-j-li/sec-auction/pull/10) | Remove GPT-6-Sol from the cockpit and add Fast arguments for Sol. The integrated frontend retains the review panel. | No model execution or deployment occurred in this review. |

The initiation change produces `bidder-led` for Datalink, Imprivata, Penford, and Pepco. Mac-Gray remains `mixed`.

Datalink, Imprivata, and Penford therefore disagree with their recorded `mixed` values. Pepco's recorded value now agrees. This is the intended effect of the approved rule.

The merged Sol command adds `-c service_tier="priority" --enable fast_mode`. Astra receives neither argument. The review confirms command construction, not provider execution or billing.

The referenced frontend bundle contains both the mandatory-review panel and extraction information. The live bundle contains neither feature.

## PR #11: Standards

**No actionable hard-rule or heuristic violation was verified.**

- The decision log records Austin's authority to remove Meredith.
- The catalog, manifest, seed, import list, and verification list consistently exclude Meredith.
- The seed builder preserves this exclusion on a rebuild.
- The backup path still retains the full database and stored files.
- The deleted frontend assets are absent from the current HTML references.
- The diff adds no tests, credentials, model runs, or external data paths.
- `git diff --check` passes.

Sol also independently confirmed the activity defect in the Spec review below. That corroboration does not add a separate standards finding.

## PR #11: Spec

**The instruction changes match the recorded rulings. Two issues remain.**

### P2: the activity filter hides instruction history

At `_dev/tools/cockpit/trace.py:255–258`, the new account feed accepts only listed deal slugs. Instruction events use an empty slug.

`instructions.py:204,247,261` records instruction draft, publication, and default changes with that empty slug. The new query therefore excludes all three event types.

The app specification requires the account feed to show all activity. It specifically requires a record of default changes. See `_dev/COCKPIT_APP_SPEC.md:176,190`.

The filter removes more than Meredith. It removes the shared instruction audit trail from the feed.

**Required correction:** preserve global instruction events while excluding removed deals. This defect follows directly from the query and its callers. The review did not create a live event.

### P3: current counts anticipate the release

`_dev/STATUS.md:8` and `README.md:14` describe 12 cockpit runs. The live database still contains 13 originals.

The approved removal takes effect in the deal list after the next release. It retains Meredith's database rows and backups.

**Required correction:** distinguish 13 retained originals from 12 listed deals after release. `_dev/STATUS.md:9` already makes the release boundary clear.

Standards: zero findings. Spec: two findings; the worst is P2, loss of instruction events from the account feed.

## The new rulings and the remaining data work

These are accepted rulings in PR #11's decision log, lines 279–283. This review does not reopen them.

| Ruling | PR #11 implementation | Separate data action |
|---|---|---|
| An offer time limit does not trigger H3 | E12 excludes it and retains the time limit in the Note. | Change Synacor #61 Conditions to None. Providence #60 already agrees. |
| A return to an older price is a revision | E10 distinguishes it from a Same offer. | Correct Providence #52 and remove its `Same as` reference. |
| Kraton Parent financing is Committed | Records the source ruling without a new general rule. | Correct Kraton #49. Preserve #41 and #43 as recorded. |
| Meredith leaves the project | Removes current inputs and catalog entries; preserves dated records. | Release the catalog change. Preserve the stored original and backups. |
| Sponsor B withdrew on 29 June | Records the Imprivata ruling and its separate evaluation treatment. | Replace #34 with Withdrew, reason Value below earlier offer. Remove #40. |

The Imprivata ruling supersedes the first review's preference for July 8 non-submission. Report agreement on this case separately from generalization evidence.

The Meredith ruling supersedes its earlier descriptive-only status. After release, the active list contains eight reference deals and four added deals.

These workbook changes are a separate revision pass. Their absence is not missing implementation within PR #11's stated scope.

## Two analysis issues survive PR #9

### P2: the residual minimum remains unsupported

The Medivation fix reduces event #9's residual minimum from two to one. The derived live minimum at #9 and Pfizer's bid #13 falls from four to three.

The filing reports Pfizer's NDA, then agreements with several parties, including Sanofi. The code interprets `several` as at least two.

Those two named parties can exhaust that lower bound. A positive residual does not follow from this convention. Later August language cannot establish the July residual.

`derive_analysis.py:263` still returns a residual minimum of one. The review message at line 700 repeats that assumption.

**Required correction:** permit zero unless separate evidence establishes another signer. An explicit approved convention could instead support a positive minimum.

Source: the saved Medivation filing, lines 1466–1467. Consumer evidence: saved workbook #9 and #13, under both exact Git revisions.

### P2: a documented filter still drops the price reversion

Providence #52 now receives `1` in both price masks. Ordinary restatements #57 and #64 still receive `0`. The principal mask fix works.

However, #52 retains `same_offer_of=33`. The manifest's `same_offer_restatements=dropped` variant selects rows only when that field is blank.

A consumer who follows that instruction still loses the $23.81 to $21.26 revision. The internal reversion flag is absent from the exported row.

**Required correction:** expose the reversion classification and exempt it from that filter, or correct the documented selection rule.

References: `derive_analysis.py:114,783–788`. The separate workbook correction would resolve this instance, but it does not repair the current exported contract.

## What remains from the first review

The new merges do not establish research acceptance. In particular:

- Datalink still lacks the August 16 round and retains two bidders for 14 extra days.
- The saved sTec outcome still conflicts with the approved Enforced correction.
- The PetSmart and Synacor round anchors still need the recorded corrections.
- The analysis still compares cumulative participants with maximum simultaneous participation. Synacor process 3, round 3 produces a false discrepancy.
- The model comparison still covers two deals, with one run per setup. It does not establish a general accuracy rate.
- The earlier isolation, instruction publication, review-status, date-comparison, and data-path findings remain open. The reviewed changes do not address them.

See the [first report](README.md) and [technical evidence](technical_findings.md) for the unchanged findings. The price-mask, initiation, Meredith, and Imprivata statements above replace the corresponding earlier assessments.

## Answer to the voice-note question

**The rules are closer to Alex's requests. The live evidence is not yet an accepted research dataset.**

The changes clarify initiation, genuine price revisions, and time limits. The adopted Imprivata exit also follows Alex's coding.

The remaining distinction is practical. Rules in GitHub, deployed tools, corrected workbooks, and accepted research data are separate states. Only the first state advances in these merges.

The earlier deferred items remain deferred. The remaining workbook defects still affect round structure, participation, and deadline interpretation.

## Verification and next decision

The team read the merged diff and all 16 changed PR #11 files. It used exact Git revisions for the analysis comparison.

Astra compared analysis outputs for seven saved workbooks at both exact Git revisions. It also derived current Synacor outputs. It ran the checker only on Providence and Medivation.

Providence returns one error and two warnings. Medivation returns zero errors and three warnings.

The new Providence warning identifies a Same-offer reference after an intervening revision. A clean checker result would still not establish source accuracy.

Sol inspected the deployment checkout, service state, instruction record, database counts, and referenced frontend assets. The services retain their earlier process IDs and start times.

The review did not repeat PR #11's scratch-browser demonstration. It did not execute a provider call. It wrote no tests and ran no test suite.

**Recommended next step:** repair PR #11's feed filter and count descriptions before merge. Keep the two residual analysis defects open. Then authorize deployment, instruction publication, and bounded data revisions as separate actions.

This report changes no instruction, program code, workbook, or live state.
