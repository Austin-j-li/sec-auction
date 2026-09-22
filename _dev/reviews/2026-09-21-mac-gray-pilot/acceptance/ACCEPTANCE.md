# Mac-Gray acceptance review — 22 September 2026

**Source review and supported corrections are complete. Final research acceptance is pending one consequential convention decision, R01.** The candidate is not frozen or labelled research-ready. The user was asked whether material fee/guarantee changes should become separate same-price bids or remain dated terms in existing Notes; no answer has yet arrived.

Current candidate: [extraction/mac-gray.xlsx](extraction/mac-gray.xlsx), SHA-256 `db85a39b00bb98702e73ad3e891cb4ab50202f2e032fcb3278ef0e6e45f351e1`.

## Review completed

- Complete background read in order and two-way reconciliation of all **87 narrative paragraph fragments**, all **55 starting ledger events**, three Rounds rows, nine Questions and 17 Deal facts fields. [Coverage and its boundary](FILING_COVERAGE.md) distinguishes full narrative review from section-level screening of excluded procedural/legal material.
- Supporting sections and annexes checked for missed events, buyer identity, financing, adviser engagements, projections, final consideration and post-signing developments. Annex A §5.11 supplied **three omitted named buyer intermediaries**: Morgan Stanley, Deutsche Bank and Evercore. Their specific roles and appointment dates remain undisclosed; the new rows say so.
- Additional precision/application repairs: Kirkland's first involvement is bounded; two bid delivery media were unstated; Party C's August29 diligence was in person; instructions and potential recusals are distinguished from completed actions; full-access timing preserved; exit price comparison dated; unsupported deadline-tolerance alternatives removed; cohort closure described as a conservative bound; non-submission distinguished from withdrawal in the account.
- Earlier representation questions were adjudicated under existing rules: April5 qualified exploration remains permissible under D2; Party A's information-access lag is preserved by dated NDA/package rows; full access after exclusivity can remain on that row under E2; frozen E12 continues to govern Heavy conditions. Unknown outreach units and anonymous timing remain qualified rather than guessed.

The lead's original candidate-row rulings are in [candidate-row-review.json](candidate-row-review.json), all other sheets in [other-sheets-review.json](other-sheets-review.json), and paragraph dispositions in [background-coverage.json](background-coverage.json). This is a familiar-case lead/model review, not a new blind reader or a human benchmark.

## Controlled correction and independent verification

One isolated native **Claude Opus 5 high** revision implemented only [A01–A11](ACCEPTED_CORRECTIONS.md), using the supplied instruction, filing, selected workbook and correction packet. The generic checker-oriented transport prompt was adapted and its hash pinned before launch. Production runner code was unchanged. Preflight showed exactly the four authorized input/workbook files; neither `_dev/` nor `ref/` was visible. Research choice R01 was expressly excluded.

Run: September21, 23:52:22–23:54:30 UTC; runner elapsed **127.520 seconds**, provider-reported list cost **$1.421771**. Requested and reported model match. Provider result success; no provider web-search/fetch requests; empty stderr. Provenance is preserved in `provenance/`. The total reported cost of the Mac-Gray extraction/audit/revision workflow through this pass is **$11.773043**, not a claim about actual account billing. No human active-review-time saving was measured.

Independent verification, transcribed from the correction packet rather than inferred from provider output:

| Check | Result |
| --- | --- |
| Complete comparison across four sheets | 1,378 existing cells checked; **19 changed cells**, all authorized (16 substantive/precision cells, two event numbers, one reference) |
| Added rows | Three Adviser rows, **all 66 fields checked** against the packet and source context |
| Final structure | **58 events, 13 Bid rows, 3 rounds, 9 Questions** |
| Existing bids | Core fields of all 13 unchanged; no economic-term bids added |
| Source quotation checks | All 58 exact quotations located on cited printed pages, at most 30 words; semantic support separately reviewed |
| Internal links | All 74 event-reference occurrences valid; Question row lists equal ledger flags |
| Mechanical checker v1.5 | **0 errors, 13 warnings**: five necessary long Notes, seven long Questions, one false-positive deadline-question warning |
| Formatting/controls | Resolved styles of matched cells unchanged; new rows match Adviser style; four-sheet controls preserved; only required ledger filter expansion |
| Package comparison | Only intended worksheet contents/dimensions, filter name/range and modified timestamp differ; styles/theme unchanged |
| Protected inputs | Instruction, filing, canonical raw v1.13, raw v1.13.2, previous revised candidate and runner hashes unchanged |

Evidence: [complete diff](verification/CELL_DIFF.md), [comparison](verification/comparison.json), [all added cells](verification/added-rows.json), [mechanical report](mechanical-check.json), and [reproducible read-only verifier](verify_correction_pass.py). Two wrapped content previews were inspected for readability; these are explicitly **not native Excel renders**. Artifact-tool/native spreadsheet rendering was unavailable, so no native-application display certification is claimed. A temporary verifier mismatch used object identity for empty conditional-formatting collections; corrected to compare serialized rules, without changing the workbook.

Raw outputs and earlier evidence remain intact. Owned run scaffolding is removed after provenance capture; `cleanup.json` and `EVIDENCE_MANIFEST.json` record cleanup and the preserved snapshot. No instruction edit, canonical workbook overwrite, production-code change, commit or push.

## Remaining decision and acceptance gate

[R01](RESEARCH_DECISION.md) provides the passages, dates, applicable rules and concrete proposed event treatment. **E2 folds routine legal negotiation into Notes; E10 requires material economic changes to receive their own Bid.** Whether these fee/guarantee changes cross that boundary is the remaining research choice reserved for Austin. It affects the record of commitment and the number of offer revisions, so the lead has not silently chosen it.

Recommendation: record material fee/guarantee changes separately, carrying the unchanged $21.25 cash price. Target counterproposals/requirements are separate target events, not bids. Routine unspecified drafting remains in Notes. The alternative keeps 13 Bid rows and preserves these developments as dated terms in Notes. Neither option changes the core price sequence or three-round map. After Austin chooses, implement only that convention's concrete corrections through Opus, verify the complete diff, and then freeze the accepted version with its hash and [analytical-use restrictions](ANALYTICAL_USE.md).

The most consequential unavoidable restriction is the anonymous cohort: exact early entry/exit dates and live counts are unavailable. Acceptance cannot turn sorting keys or conservative bounds into observations. Any estimation design needing exact early competition must explicitly handle missingness/bounds or exclude those observations.
