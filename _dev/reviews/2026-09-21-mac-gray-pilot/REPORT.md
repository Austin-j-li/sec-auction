# Mac-Gray: fresh extraction and audit under v1.13.2

**The rerun did not demonstrate meaningful improvement over the current v1.13 workbook. The fresh audit found useful corrections, but missed material problems and produced a false cell claim.** This supports a source-backed adjudication step; it does not yet establish a reliable automatic review pipeline.

Mac-Gray was selected because Alex's voice notes explicitly identify it as a useful test of multiple bidders and stages, NDA counts, conditions and exits. The selection and evaluation dimensions were recorded before the new output. This familiar-case trial accompanies the separately administered Datalink trial; it is not an unseen-case test.

## What ran

| | Existing baseline | Fresh extraction |
| --- | --- | --- |
| Instruction | v1.13 | v1.13.2, unchanged |
| Extractor | Recorded Opus run | Claude Opus 5, high |
| Ledger events | 54 | 53 |
| Rounds | 3 | 3 |
| Bid events | 13 | 13 |
| Mechanical checker 1.5 | 0 errors, 11 warnings | 1 error, 8 warnings |

All thirteen bids match on bidder, date, round, price endpoints, cash classification, Formality and Conditions. Both drafts open rounds on June 24, July 25 and September 11, retain the same deadlines/outcomes, and separate October 14 signing from October 15 announcement. These broad successes were already present in v1.13 and cannot be credited as improvements from this rerun.

The fresh extraction took 473.448 seconds and reported $3.0989005. A new isolated Opus 5 high session audited it in 535.525 seconds for $4.002606. **Total reported provider cost: $7.1015065; total sequential model time: 16.8 minutes.** Reported cost is not a claim about the account's billed charge. Human review time was not measured.

The reviewer saw only the frozen instruction, the filing and the read-only new workbook. The sandbox was checked before launch. It did not see Alex's notes, the old workbook, checker output, the lead's source inventory, or earlier reports. Both sessions completed successfully; success here means execution and artifact production, not substantive acceptance.

## What improved, what did not

- **One limited correction:** the baseline says A's September 10 $18–19 range equals its June 21 $17–19 proposal. The new Note correctly calls it a narrowing. The numeric prices were already right.
- **Main participation defect persists:** both drafts close all sixteen unnamed financial NDA signers by July 23 while admitting their signing dates are unknown. The filing gives an eventual total across roughly two months. A Question does not justify an exact earlier live population or exit count.
- **Some detail regressed:** the new ledger omits the separate September 27 execution of bidder-requested MacDonald voting agreements and drops material option-vesting terms from Party B's September 18 bid Note. A few new quotation/chronology defects and a round-opening order error also appear. No meaningful improvement in the main auction variables was established.
- **Do not overcount losses:** the lead initially queried the folded full-access event during exclusivity. Because no rival remained live and the access change is retained in a Note, a separate row is not clearly required. It is not counted as a confirmed regression.

## What the fresh audit contributed

The reviewer returned ten candidate findings. The lead checked every one against the filing, workbook and instruction:

- **Five support limited corrections:** Q9's incorrect counterfactual, two quotations that support the wrong part of a row, outreach wording that is too precise, and the account of Party C's written bid after the selection meeting. One of these findings also suggests deleting adviser rows; only its quotation correction is accepted.
- **Three require judgment:** whether later reverse-fee/commitment terms are a new economic bid; whether A's delayed package needs an additional information-state row; and how to label the April authorization. They are not three established extraction mistakes.
- **Two are not accepted as stated:** F05 criticizes the discussion of late NDAs but approves retaining the unsupported exact July 23 closure. F09 says the winner's Type is blank, although the exact audit input has **Strategic in D53**.

The audit did not resolve the principal cohort-timing defect. It also did not flag the omitted voting-agreement event, the missing option terms, or the extension request folded into a later event. Its no-missing-bid finding is consistent with the inspected price series; it does not establish complete material-event coverage.

The full [adjudication packet](/home/uctpiaj/Projects/sec-extraction/_dev/reviews/2026-09-21-mac-gray-pilot/ADJUDICATION.md) gives passages, pages, affected rows, rules and proposed corrections, including the limits of each claim.

## Check against Alex's voice comments

Most broad issues Alex described in an older AI database were already addressed in the v1.13 baseline: target-first contact, separate contact/NDA events, two named strategic signers, three stages, bid-level conditions, final-range formality, and signing versus announcement. They remain largely stable here.

The voice notes are not an infallible answer key. Alex's Mac-Gray paragraph 50 names B and C as displaced at exclusivity; the filing says C did not submit on September 18, leaving A and B to be displaced on September 24. Both modern workbooks follow the filing correctly. The [criterion mapping](/home/uctpiaj/Projects/sec-extraction/_dev/reviews/2026-09-21-mac-gray-pilot/alex-criteria.md) records this distinction.

## Independent source coverage and limits

Before opening either comparison workbook, the lead froze an inventory for June 24–August 5 (pp.30–34), covering the first outreach, NDAs, first bids and July stage change. Both workbooks represent the main event obligations in that passage; the main defect is the precision of the anonymous cohort's timing. No wholly absent event was established within that predeclared passage, so there is no positive omitted-event denominator for estimating audit recall there.

Additional omissions were checked outside the passage but do not constitute an exhaustive, independently adjudicated whole-filing benchmark. The lead had seen Alex's comments; the fresh Opus reader had not. One run per condition cannot separate an instruction effect from run variation. No workbook revision or human review-time comparison was performed.

## Development decision

Keep the instruction frozen. Do not treat either re-extraction or an unadjudicated audit as sufficient to improve the dataset. The next useful test is a controlled revision using only accepted findings, followed by a full change review: confirm the cohort uncertainty is represented honestly, recover the supported missing events/terms, and check for new errors. Resolve the reverse-fee/economic-terms convention separately if it affects that pass. No revision, commit or push was performed in this trial.

## Preserved artifacts

- [Raw v1.13.2 workbook](/home/uctpiaj/Projects/sec-extraction/_dev/reviews/2026-09-21-mac-gray-pilot/raw/extraction/mac-gray.xlsx), byte-identical to the extractor's output.
- Existing v1.13 baseline, unchanged: the 54-event v1.13 baseline (SHA-256 `6c8b583bd9b948cd8e6dee6aa2f7fba43acc5598c5bf73c6f55ae7efab13a852`, archived; git `03d59b1:extraction/mac-gray.xlsx`). Since 22 September the current `extraction/mac-gray.xlsx` is a different, newer Opus 5.5 medium draft.
- [Original independent audit](/home/uctpiaj/Projects/sec-extraction/_dev/reviews/2026-09-21-mac-gray-pilot/audit/review.md) and [structured findings](/home/uctpiaj/Projects/sec-extraction/_dev/reviews/2026-09-21-mac-gray-pilot/audit/findings.json), unchanged.
- [Adjudication](/home/uctpiaj/Projects/sec-extraction/_dev/reviews/2026-09-21-mac-gray-pilot/ADJUDICATION.md), [source inventory](/home/uctpiaj/Projects/sec-extraction/_dev/reviews/2026-09-21-mac-gray-pilot/source-inventory.md), and [inventory comparison](/home/uctpiaj/Projects/sec-extraction/_dev/reviews/2026-09-21-mac-gray-pilot/inventory-comparison.md).
- `selection.json`, protocol and lead-finding freeze records, both mechanical reports, and `provenance/` retain hashes, prompts, statuses, model/usage evidence and the audit isolation check. Disposable run directories and provider state are removed after recording the results.

Raw new workbook SHA-256: `9422bc6b0d14c19033771a51bb6432e2054f16ba55e9b07df02c73c3d28ac279`.

Baseline SHA-256: `6c8b583bd9b948cd8e6dee6aa2f7fba43acc5598c5bf73c6f55ae7efab13a852`.

Instruction SHA-256: `513c8e3e8159e4a6bceccd6ffca32a246302736329a0c7137b64dd3b7ffcd304`.
