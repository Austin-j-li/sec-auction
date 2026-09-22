# Consolidation — 22 September 2026

Austin authorized deletion of the Grok and GPT-5.6-Sol extraction results, removal of stale copies, consolidation around the main Opus workflow, retention of the Astra experiment only as a side note, and a local commit. No new extraction, audit, correction pass or instruction edit was part of this maintenance.

## Removed

The exact five targets are recorded in [deletion-inventory.json](deletion-inventory.json) and [cleanup-result.json](cleanup-result.json): both model-comparison worktrees, the old detached checkout's project contents, the derived three-model review packet, and the superseded pre-build pipeline proposal. This removed **524 inventoried files / 81,042,428 bytes**. The two local comparison branches were deleted. No report/workbook backup of the retired results was created; the inventory retains paths, sizes and hashes only. Earlier committed Git history and remote archive branches were not rewritten.

The main checkout is the sole registered Git worktree. Four live MCP/advisor processes still used the former detached directory as their current working directory. Its inode was therefore preserved with only `RELOCATED.md`, pointing to the main checkout and Astra side note. Its stale files and Git registration are gone; those processes and the public cockpit service were not stopped.

## Preserved and reconciled

- All twenty catalogued Opus workbook versions, nine filings plus their manifest, the frozen instruction and production runner retain their pre-cleanup hashes. [Before](protected-inputs-before.json) and [after](protected-inputs-after.json) records cover 33 files including the already-updated catalog.
- The Astra experiment's 22 manifested evidence files and original manifest were copied byte-for-byte into the [historical side note](../../side-notes/2026-09-21-astra-mac-gray/README.md). Austin's cost constraint supersedes the historical report's proposed follow-up. The original extractor-response file keeps one historical sandbox-local link; use the preserved workbook link in the side-note README.
- The cockpit importer no longer depends on the deleted comparison report. Its seven fresh drafts have no inherited comparison findings or documents. Datalink retains thirteen findings and Mac-Gray fifteen, including the pending R01 decision. All twenty versions and working defaults remain unchanged.
- The handoff, repository guidance, instruction-decision status and research-question index now describe the current workflow. No deleted report remains a live catalog document.

## Verification

[Engineering verification](engineering-verification.json) records 99 Python unit tests, 11 disposable HTTP acceptance tests, three frontend tests and a successful production build. The post-deletion importer and nine-deal catalog checks passed, including exact version/export hashes. Live HTTP returned all sixteen catalog documents matching source text and served the built HTML/assets byte-for-byte. The service required no restart; production working state remained absent and all working versions remained at revision zero.

These checks establish preservation and software behavior, not substantive acceptance of the extracted data. At consolidation, the defaults retained 2 checker errors / 125 warnings, Datalink's documented quotation exception, and Mac-Gray's pending R01 decision. Human source review remains next. The [handoff](../../HANDOFF.md) is the current entry point.
