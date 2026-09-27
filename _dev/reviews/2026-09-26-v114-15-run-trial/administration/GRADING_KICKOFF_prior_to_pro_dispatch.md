# Independent grading kickoff

> **Status, 26 September 2026 (20:45 UTC):** superseded rubric, kept as a record. It rewards "dates and bounds"; v1.14.1 codes these differently, so it must not be used to grade v1.14.1 output ([`RETEST_PLAN.md`, Acceptance](../../../maintenance/2026-09-26-v1141-streamline/retest/RETEST_PLAN.md)). The worktree path below no longer exists; the packet now lives in the main checkout.

You are the independent grader of a fresh v1.14 extraction trial. The administrator ran the models and preserved their outputs; the administrator did not grade, correct or rank them.

## Location and scope

Worktree: `/home/uctpiaj/work/Projects/sec-extraction-v114-trial-20260926`

Packet: `_dev/reviews/2026-09-26-v114-15-run-trial/`

There are three deals: Mac-Gray, Providence & Worcester, and sTec. Each was assigned to five model/effort settings, one fresh extraction per setting: Opus 5.5 medium, Opus 5.5 xhigh, GPT-6-Astra high, GPT-6-Astra xhigh, and GPT-6-Sol xhigh. This is a small pilot, with no repeated trials within a setting/deal.

Read `COMPLETION.json` first for administrative completion only. Grade available original outputs; report any missing/failed runs separately. Do not infer extraction quality from administrative completion, a readable workbook, mechanical checks, number of rows, or agreement among models.

## Boundaries

- Do not change instructions, original workbooks, live application state, working copies, or the catalog. Do not run another extraction, perform a correction pass, deploy, commit or push.
- Write grading artifacts only under a new `grading/` folder in this packet. Preserve source and workbook hashes.
- The extraction rulebook is the exact frozen instruction in `inputs/SEC_Deal_Ledger_Extraction_Instruction.md`, SHA-256 `c2d47a479d09eb46d0ab9fbf887568fcf13e972e2e11acbf08d5cdfab468ab27`. Judge rule compliance against this version, not the older instruction at the worktree root or an earlier v1.14 draft.
- Use the three complete filings in `inputs/raw_filing/` as primary factual evidence. No outside information or identification of anonymous bidders.
- Keep instruction compliance, source accuracy, unresolved research conventions, and operational reliability separate. A provisional but explicit instruction rule is the rule for this test; its research desirability is a separate question.

## First pass: source review without model identities

Read `blinded/manifest.json`, then the A–E workbooks inside each deal's folder. Letter labels are randomized separately for each deal and do not identify the same model across deals. Copies are byte-identical to the originals; internal workbook metadata has not been rewritten, so blinding is best effort.

Do not open `administration/blind-key.json`, `runs/`, model event logs, or model-specific plan/receipt files until the source findings and rubric are written. Do not use previous reviews as an answer key on this first pass.

1. Read the instruction and each filing's whole background. Build a source-based inventory of material events, bids and revisions, participant entries/exits, scope changes, stage boundaries, deadlines and counts. Consult other filing sections wherever necessary.
2. Establish one consistent rubric before unblinding. Prioritize material data over prose polish: bidder identity and units, participation/counts, rounds, dates and bounds, prices and consideration, formality, financing, diligence, regulatory/antitrust conditions, exclusivity, and the resulting Conditions classification.
3. Audit in both directions: every substantive extracted claim against its evidence, and every required source event against the workbook. Check omissions, invented events, duplicates, unsupported precision, retrospective backfilling and inconsistent dependent fields. Check all four sheets and their references.
4. Assess whether the new condition taxonomy is applied consistently and whether the instruction itself leads careful readers into ambiguity or contradiction. Distinguish an extractor's mistake from a rule-design problem. Pay particular attention to CVRs versus bid conditions, exclusivity, Heavy triggers, scope changes and continuing participation after missed deadlines.
5. For each finding give deal, anonymous workbook label, sheet/row/cell, extracted value, supported reading, exact filing page/passage and instruction section, severity, and downstream consequences. Accept multiple readings where the evidence or instruction genuinely permits them. Do not penalize an honest blank or range simply for being less precise.
6. Resolve disputed findings independently against the source before ranking. If using a Codex review team, use Astra for substantive source judgment with effort adapted to difficulty, read the applicable Codex team skill, use at most six direct workers, and do not allow nested delegation. Reviewers must not edit extraction files.

## Second pass: context and comparison

After freezing the first-pass findings, open `administration/blind-key.json` and the run receipts. Mechanical `check.json` reports are supporting evidence only; they were generated after extraction and never shown to the extracting models. Inspect `ISOLATION_PREFLIGHT.json`, receipts, and logs as needed to assess protocol adherence without treating shell-network pattern matches as proved external access.

Then consult existing research context in `/home/uctpiaj/work/Projects/sec-extraction/`: `ref/alex_voice_notes_2026-08.docx`, `ref/CollectionInstructions_Alex_2026.pdf`, `ref/deal_details_Alex_2026.xlsx`, the current taxonomy package under `_dev/maintenance/2026-09-24-bid-terms-taxonomy/`, and relevant `lesson/` records. Treat previous extractions, human edits, Alex's examples and earlier recommendations as claims to reconcile with the filing and explicit conventions, not automatic ground truth. Clearly identify any pending decision that changes the comparison.

## Deliverables

- A source-backed findings ledger and a coverage record for each deal.
- A model-by-deal comparison of material errors, omissions, unsupported precision, condition-taxonomy consistency and practical correction burden. State denominators and avoid double-counting one root mistake as many independent errors.
- Separate conclusions on (a) which model/effort is most useful in this pilot, (b) whether v1.14 needs general instruction changes, and (c) what genuinely remains for Alex. Include proposed wording only as recommendations, with each change tied to evidence and general applicability.
- Runtime and token/cost information only where receipts support it. Do not invent subscription costs or claim statistically reliable model superiority from three deals and one run per cell.
- A concise answer for Austin: whether to adopt v1.14, revise and retest it, or hold it; what to change first; and the few remaining research decisions. Keep supported findings separate from uncertainty.

Finish with links to your reports. Do not implement the recommendations.
