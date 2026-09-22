# Development handoff — 22 September 2026

## Current direction

**Use the main `extraction-v2` checkout and the editable [Ledger cockpit](https://lines.dealextract.org). Claude Opus 5.5 at medium effort is the extraction model.** The [22 September effort sweep](reviews/2026-09-22-opus55-sol6-sweep/REPORT.md) found no reliable gain from high effort. GPT-6-Sol at xhigh was not distinguishable from it on quality; Austin chose Opus for now (22 September). The current workbooks in `extraction/` are Opus 5.5 medium extractions of all nine deals ([re-extraction packet](reviews/2026-09-22-opus55-reextraction/README.md)); the replaced Opus 5 high originals are archived outside the checkout and recoverable from Git at `03d59b1`. The working instruction is **v1.13.2, frozen**. Austin authorized consolidation, deletion of the retired Grok/Sol extraction results, and a local commit on 22 September. This maintenance does not authorize another model run or a research-convention change.

For engineering, **Astra designs, reasons and reviews; GPT Sol subagents write code and execute the implementation**. Removing Sol's extraction experiment does not change that engineering assignment.

## What is ready for Austin

The cockpit contains nine deals, each with one immutable version: its Opus 5.5 medium v1.13.2 extraction in `extraction/` (22 September), which is also the working base. None has been reviewed. Earlier Opus 5 drafts, the v1.13 baselines and the lead-verified Datalink and Mac-Gray correction passes are no longer in the cockpit; their evidence stays in the review packets. Working edits, decisions and revision history are separate from the preserved workbooks.

| Deal | Current result | Review boundary |
|---|---|---|
| Datalink | 71 events, 4 rounds, 8 Questions; checker 0 errors / 21 warnings | Austin's source review is pending. Review shows Austin's 21 September F9 ruling (January's bilateral stage is round 1; five rounds) as a case-level decision to check against this extraction. |
| Mac-Gray | 53 events, 3 rounds, 9 Questions; checker 1 error / 26 warnings | Austin's source review is pending. Checker error: round-opening order (ledger row 10). **R01 decided by Austin, 22 September**: bidder-commitment changes (reverse fee, sponsor cap, conditions) are same-price Bids, the target termination fee a dated Note; the current draft is not yet revised to it. Review shows the decision document. |
| Kraton, Meredith, Penford, PetSmart, Providence & Worcester, sTec and Synacor | One draft each | Austin's source review is pending. Checker errors: PetSmart round-opening order (ledger row 11) and Synacor Deal facts process count (row 11). |

The nine workbooks total **3 mechanical errors and 161 warnings**. Those are checker occurrences, not an accuracy score. The row-keyed audit findings and corrections for the earlier Datalink and Mac-Gray drafts were removed from the cockpit and remain in their packets. No saved production SQLite database was present when the catalog was reduced to one version per deal.

- [Review guide](cockpit/README.md): filing navigation, editing all four sheets, inserting/deleting/moving events, recording decisions, saving, comparing, restoring and exporting Excel.
- [Datalink packet entry point](reviews/2026-09-21-datalink-pilot/README.md): the earlier raw-draft review, F9 ruling and verified 68-event revision, with its full diff and retained uncertainty. That revision is no longer a cockpit version.
- [Mac-Gray packet entry point](reviews/2026-09-21-mac-gray-pilot/README.md): the earlier raw audit, 55-event revision and 58-event candidate, source coverage, analytical restrictions and the R01 decision. Those workbooks are no longer cockpit versions.
- [Re-extraction packet](reviews/2026-09-22-opus55-reextraction/README.md): receipts, checker results and hashes for the nine current workbooks, and the catalog's import and live verification. The earlier [nine-deal import report](reviews/2026-09-21-v1132-cockpit/REPORT.md) describes the retired Opus 5 v1.13.2 set.

## Consolidated layout

| Location | Purpose |
|---|---|
| `SEC_Deal_Ledger_Extraction_Instruction.md` | The only working extraction instruction; v1.13.2. |
| `raw_filing/` and `MANIFEST.csv` | Nine supplied filings, source links, sizes and hashes. |
| `extraction/` | Current Opus 5.5 medium v1.13.2 extractions of all nine deals; the cockpit's only versions. |
| `_dev/reviews/2026-09-21-datalink-pilot/` and `_dev/reviews/2026-09-21-mac-gray-pilot/` | Active Opus review, correction and verification evidence. Keep source outputs and their provenance immutable. |
| `_dev/reviews/2026-09-22-opus55-reextraction/` | Receipts, checker results and hashes for the nine Opus 5.5 medium extractions, and the catalog's import and live verification. |
| `_dev/reviews/2026-09-21-v1132-cockpit/` | Extraction receipts, checks and import evidence for seven retired Opus 5 v1.13.2 raw outputs (the workbooks left the checkout on 22 September; recoverable from Git at `03d59b1`), and original cockpit acceptance evidence. |
| `_dev/cockpit/catalog.json` | Allowlisted version and review-document catalog. Imported originals are never edited in place. |
| `_dev/cockpit/state/workspace.sqlite3` | Ignored working revisions and decisions, created on the first save. Preserve it across deployments. |
| `_dev/tools/cockpit/` | Python API/storage/import tools, React frontend source, built assets and tests. |
| `_dev/maintenance/2026-09-22-consolidation/` | Exact deletion inventory, preservation checks and consolidation verification. |
| `_dev/maintenance/2026-09-22-doc-refresh/` | Documentation inventory, protected-file baseline, link audit and current-navigation refresh. |

The Grok and Sol comparison worktrees, their local branches, their raw results, the derived three-model packet and the superseded pre-build pipeline proposal are retired. Their contents are hard-deleted, not archived as a competing development tree. Deletion records contain paths and hashes rather than workbook cells or report copies. The former detached `7877` checkout is unregistered and retains only a relocation note: live tool processes still use its directory, so its directory inode is retained without stale project files. The main checkout is the sole development worktree.

**Historical side note only:** the [Astra/Mac-Gray experiment](side-notes/2026-09-21-astra-mac-gray/README.md) and its evidence are retained separately. Austin rejected Astra as the normal extraction model because of cost. It is excluded from the cockpit and current development plan; the old report's suggested follow-up experiment is not an active task.

## Engineering status and operation

The cockpit supports four-sheet editing, event operations, explicit reference maintenance, filing search/evidence navigation, findings and decisions, saved history, changes, restore and XLSX export. Stale saves preserve the user's draft and require reconciliation. A finding judgment does not itself change workbook cells. Original files and native Excel cell types/formatting are preserved by the working-copy/export layer. [Build contract](COCKPIT_BUILD.md).

The existing `ledger-cockpit.service` runs from this checkout on `127.0.0.1:8778`, through Cloudflare Access at `https://lines.dealextract.org`. Public writes use the configured Austin/Alex identity, Origin and CSRF checks; loopback development is attributed to `local`. Viewing or saving does not invoke a model. [Tool and operation guide](tools/README.md).

Filing fetch/verification share the selected document and verification pins its recorded filename. The runner verifies prepared input hashes, including revision evidence, and distinguishes provider failure, missing/unreadable output, timeout and successful production. Checking remains mechanical and offline. The existing alternative transport implementations in the runner are not authorization to use an alternative extractor.

The delivered build passed 110 Python tests and 38 subtests, three frontend tests, and 46 synthetic browser assertions. The original [acceptance record](reviews/2026-09-21-v1132-cockpit/cockpit-verification/VERIFICATION.md), [deployment receipt](reviews/2026-09-21-v1132-cockpit/cockpit-verification/deployment.json), and [VM review](reviews/2026-09-21-v1132-cockpit/cockpit-verification/VM_REVIEW.md) state their exact boundaries. The later [consolidation verification](maintenance/2026-09-22-consolidation/README.md) reran 99 Python unit tests, 11 HTTP acceptance tests, three frontend tests, the build and post-deletion catalog/live-document checks; all passed. An existing authenticated public session was verified; a fresh sign-in/OTP challenge, real production save and live EDGAR re-verification remain outside that evidence.

The current frontend source and built assets add mouse/keyboard split-pane resizing, mobile list-height resizing, localStorage persistence and two-dimensional multiline-field resizing. On 22 September a read-only loopback check confirmed the running service served the current built HTML, JavaScript and CSS byte-for-byte. The earlier acceptance and consolidation test counts predate these changes; browser resize interaction and the authenticated public route were not retested in this documentation pass. The [cockpit guide](cockpit/README.md) and [build contract](COCKPIT_BUILD.md) describe the current controls and their verification limits.

## Next work

1. Austin reviews the nine current workbooks in the cockpit, including applying the Mac-Gray R01 decision. Check Datalink against the accepted January-round ruling.
2. Check both directions: ledger rows against source support, and bounded source passages against events that should appear. Mechanical cleanliness, matching models and located quotations do not establish complete extraction.
3. Separate mistakes under existing rules, research choices requiring Austin, and unsupported reviewer claims. Only an explicitly authorized correction pass should receive an accepted correction brief. Verify its entire diff and dependent references afterward.
4. Keep [research questions](RESEARCH_QUESTIONS.md) explicit. Austin confirmed on 22 September that Q3 and Q7 are no longer withheld; do not repeat the earlier approval holds. Remaining deal decisions and provisional conventions for Alex are tracked separately from that status correction. No automatic revision loops, new provider comparisons or instruction tuning are part of this maintenance. Human review-time savings and whole-filing accuracy remain unmeasured.

Instruction edits require Austin's approval and must be general, not a new rule justified by one reviewed deal. Extract only on command in an isolated one-instruction/one-filing session; run the checker afterward. Commit and push only when asked. Historical instruction evidence remains in Git and is indexed in [CHRONOLOGY.md](CHRONOLOGY.md); never restore an old instruction into the working checkout.
