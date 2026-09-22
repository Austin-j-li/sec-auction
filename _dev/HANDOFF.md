# Development handoff — 22 September 2026

## Current direction

**Use the main `extraction-v2` checkout and the editable [Ledger cockpit](https://lines.dealextract.org). Claude Opus 5 high remains the extraction model.** The working instruction is **v1.13.2, frozen**. Austin authorized consolidation, deletion of the retired Grok/Sol extraction results, and a local commit on 22 September. This maintenance does not authorize another model run or a research-convention change.

For engineering, **Astra designs, reasons and reviews; GPT Sol subagents write code and execute the implementation**. Removing Sol's extraction experiment does not change that engineering assignment.

## What is ready for Austin

The cockpit contains nine deals and twenty immutable Opus workbook versions. All nine have a v1.13.2 raw extraction. The original eight v1.13 baselines, Datalink's controlled revision, and both later Mac-Gray correction versions remain selectable. Working edits, decisions and revision history are separate from the preserved workbooks.

| Working base | Current result | Review boundary |
|---|---|---|
| Datalink, verified correction pass | 68 events, 5 rounds, 10 Questions; checker 1 error / 24 warnings | Accepted corrections and the complete change diff were lead-verified. January remains round 1 under Austin's F9 ruling. The checker error is a documented page-break quotation false positive; September Conditions interpretations remain qualified. Whole-deal human acceptance is pending. |
| Mac-Gray, latest correction candidate | 58 events, 13 bids, 3 rounds, 9 Questions; checker 0 errors / 13 warnings | Supported corrections and source coverage were lead-verified. **R01 remains pending:** separate same-price Bids for material fee/guarantee changes versus dated Notes. The candidate is not frozen or research-ready. |
| Kraton, Meredith, Penford, PetSmart, Providence & Worcester, sTec and Synacor | One fresh v1.13.2 Opus draft each | Austin's source review is pending. Synacor retains a round-opening-order error at ledger Excel row 7. No inherited Sol/Grok comparison findings or document links remain on these drafts. |

Current default workbooks total **2 mechanical errors and 125 warnings**. Those are checker occurrences, not an accuracy score. All working copies were still at revision zero at consolidation; no saved production SQLite database was present.

- [Review guide](cockpit/README.md): filing navigation, editing all four sheets, inserting/deleting/moving events, recording decisions, saving, comparing, restoring and exporting Excel.
- [Datalink verification](reviews/2026-09-21-datalink-pilot/revision/VERIFICATION.md): corrected workbook, full diff, references, bounded source inventory, provenance and retained uncertainty. The original [adjudication](reviews/2026-09-21-datalink-pilot/ADJUDICATION.md) preserves the findings and Austin's ruling.
- [Mac-Gray acceptance packet](reviews/2026-09-21-mac-gray-pilot/acceptance/ACCEPTANCE.md): latest candidate, complete verified correction set, source coverage and analytical restrictions. [R01 decision context](reviews/2026-09-21-mac-gray-pilot/acceptance/RESEARCH_DECISION.md).
- [Nine-deal import report](reviews/2026-09-21-v1132-cockpit/REPORT.md): seven new runs, two reused raw runs, protected input hashes and separate checker receipts. The seven new runs report $27.436 in provider list-price cost, not account billing.

## Consolidated layout

| Location | Purpose |
|---|---|
| `SEC_Deal_Ledger_Extraction_Instruction.md` | The only working extraction instruction; v1.13.2. |
| `raw_filing/` and `MANIFEST.csv` | Nine supplied filings, source links, sizes and hashes. |
| `extraction/` | Preserved canonical originals: eight v1.13 Opus drafts and Datalink's v1.13.2 raw draft. The cockpit catalog selects newer versions where available. |
| `_dev/reviews/2026-09-21-datalink-pilot/` and `_dev/reviews/2026-09-21-mac-gray-pilot/` | Active Opus review, correction and verification evidence. Keep source outputs and their provenance immutable. |
| `_dev/reviews/2026-09-21-v1132-cockpit/` | Seven newer raw Opus outputs, extraction receipts, import evidence and original cockpit acceptance evidence. |
| `_dev/cockpit/catalog.json` | Allowlisted version and review-document catalog. Imported originals are never edited in place. |
| `_dev/cockpit/state/workspace.sqlite3` | Ignored working revisions and decisions, created on the first save. Preserve it across deployments. |
| `_dev/tools/cockpit/` | Python API/storage/import tools, React frontend source, built assets and tests. |
| `_dev/maintenance/2026-09-22-consolidation/` | Exact deletion inventory, preservation checks and consolidation verification. |

The Grok and Sol comparison worktrees, their local branches, their raw results, the derived three-model packet and the superseded pre-build pipeline proposal are retired. Their contents are hard-deleted, not archived as a competing development tree. Deletion records contain paths and hashes rather than workbook cells or report copies. The former detached `7877` checkout is unregistered and retains only a relocation note: live tool processes still use its directory, so its directory inode is retained without stale project files. The main checkout is the sole development worktree.

**Historical side note only:** the [Astra/Mac-Gray experiment](side-notes/2026-09-21-astra-mac-gray/README.md) and its evidence are retained separately. Austin rejected Astra as the normal extraction model because of cost. It is excluded from the cockpit and current development plan; the old report's suggested follow-up experiment is not an active task.

## Engineering status and operation

The cockpit supports four-sheet editing, event operations, explicit reference maintenance, filing search/evidence navigation, findings and decisions, saved history, changes, restore and XLSX export. Stale saves preserve the user's draft and require reconciliation. A finding judgment does not itself change workbook cells. Original files and native Excel cell types/formatting are preserved by the working-copy/export layer. [Build contract](COCKPIT_BUILD.md).

The existing `ledger-cockpit.service` runs from this checkout on `127.0.0.1:8778`, through Cloudflare Access at `https://lines.dealextract.org`. Public writes use the configured Austin/Alex identity, Origin and CSRF checks; loopback development is attributed to `local`. Viewing or saving does not invoke a model. [Tool and operation guide](tools/README.md).

Filing fetch/verification share the selected document and verification pins its recorded filename. The runner verifies prepared input hashes, including revision evidence, and distinguishes provider failure, missing/unreadable output, timeout and successful production. Checking remains mechanical and offline. The existing alternative transport implementations in the runner are not authorization to use an alternative extractor.

The delivered build passed 110 Python tests and 38 subtests, three frontend tests, and 46 synthetic browser assertions. The original [acceptance record](reviews/2026-09-21-v1132-cockpit/cockpit-verification/VERIFICATION.md), [deployment receipt](reviews/2026-09-21-v1132-cockpit/cockpit-verification/deployment.json), and [VM review](reviews/2026-09-21-v1132-cockpit/cockpit-verification/VM_REVIEW.md) state their exact boundaries. The later [consolidation verification](maintenance/2026-09-22-consolidation/README.md) reran 99 Python unit tests, 11 HTTP acceptance tests, three frontend tests, the build and post-deletion catalog/live-document checks; all passed. An existing authenticated public session was verified; a fresh sign-in/OTP challenge, real production save and live EDGAR re-verification remain outside that evidence.

## Next work

1. Austin reviews the current workbooks in the cockpit, beginning with the pending Mac-Gray R01 decision and the fresh drafts. Preserve the accepted Datalink January-round ruling.
2. Check both directions: ledger rows against source support, and bounded source passages against events that should appear. Mechanical cleanliness, matching models and located quotations do not establish complete extraction.
3. Separate mistakes under existing rules, research choices requiring Austin, and unsupported reviewer claims. Only an explicitly authorized correction pass should receive an accepted correction brief. Verify its entire diff and dependent references afterward.
4. Keep [research questions](RESEARCH_QUESTIONS.md) explicit. No automatic revision loops, new provider comparisons or instruction tuning are part of this maintenance. Human review-time savings and whole-filing accuracy remain unmeasured.

Instruction edits require Austin's approval and must be general, not a new rule justified by one reviewed deal. Extract only on command in an isolated one-instruction/one-filing session; run the checker afterward. Commit and push only when asked. Historical instruction evidence remains in Git and is indexed in [CHRONOLOGY.md](CHRONOLOGY.md); never restore an old instruction into the working checkout.
