# Opus 5.5 medium re-extraction of the nine deals — 22 September 2026

Austin authorized replacing the nine workbooks in `extraction/` with new blind extractions by Claude Opus 5.5 at medium effort, and updating the cockpit to show them. All nine runs completed once, with no continuations, failures or retries.

## Setup

| Item | Value |
|---|---|
| Model and effort | `claude-opus-5-5`, `medium` |
| Claude Code | 2.1.280, pinned binary `_dev/runs/.pinned/claude-2.1.280` (SHA-256 `1e08503dbdf3c2cb0d706d32f3408277388d1c76ef108673e8fe42c1b322925b`), the same binary as the [effort sweep](../2026-09-22-opus55-sol6-sweep/REPORT.md) |
| Instruction | `SEC_Deal_Ledger_Extraction_Instruction.md` v1.13.2, unchanged, SHA-256 `513c8e3e8159e4a6bceccd6ffca32a246302736329a0c7137b64dd3b7ffcd304` |
| Runner | `_dev/tools/sandbox/run_model.py`, SHA-256 `b74fc6b74eec6a3061a5ac809610fdcb48c0793ac90cabd925132f5531c2f485` at prepare |
| Isolation | One instruction and one filing per bubblewrap sandbox; each worker had its own temporary home, `/tmp` and provider state, and its own output directory. Tools: Bash, Read, Write |
| Timeout | 150 minutes, as in the sweep |
| Timing | All nine launched together at 21:21:57 UTC; the last finished after 932 seconds |

The checker (`check_lean.py`) ran after each run, outside the sandbox. A scan of the event logs found no network commands; the only matches were the word "curly" and filing text quoting the SEC's website.

## Results

Costs are the CLI's list-price figures, not account billing. Rows are non-empty data rows. "Old" is the workbook previously in `extraction/`: for Datalink this was the Opus 5 high v1.13.2 raw draft; for the other eight, the Opus 5 high v1.13 baselines. Old and new row counts therefore compare different instruction versions for eight deals.

| Deal | State | Continuations | Seconds | Input | Cache write | Cache read | Output | Cost | Checker errors | Warnings | Ledger rows | Rounds | Questions |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| datalink | completed | 0 | 725 | 50 | 135,638 | 1,413,782 | 83,167 | $3.031 | 0 | 21 | 67 → 71 | 5 → 4 | 10 → 8 |
| kraton | completed | 0 | 781 | 68 | 169,685 | 2,568,640 | 85,122 | $3.574 | 0 | 20 | 74 → 73 | 4 → 3 | 9 → 8 |
| mac-gray | completed | 0 | 584 | 66 | 135,235 | 2,359,483 | 65,375 | $2.862 | 1 | 26 | 54 → 53 | 3 → 3 | 9 → 9 |
| meredith | completed | 0 | 794 | 72 | 174,173 | 2,622,088 | 87,618 | $3.670 | 0 | 16 | 79 → 85 | 3 → 3 | 9 → 11 |
| penford | completed | 0 | 443 | 44 | 119,370 | 948,028 | 49,940 | $2.144 | 0 | 15 | 52 → 50 | 2 → 2 | 7 → 7 |
| petsmart | completed | 0 | 594 | 42 | 130,500 | 998,487 | 67,469 | $2.593 | 1 | 22 | 44 → 47 | 3 → 2 | 8 → 9 |
| providence-worcester | completed | 0 | 668 | 42 | 145,330 | 1,186,322 | 76,444 | $2.929 | 0 | 12 | 62 → 63 | 3 → 3 | 9 → 8 |
| stec | completed | 0 | 611 | 58 | 137,988 | 1,691,316 | 69,819 | $2.839 | 0 | 21 | 67 → 61 | 3 → 3 | 8 → 9 |
| synacor | completed | 0 | 932 | 60 | 182,222 | 2,375,417 | 105,748 | $4.048 | 1 | 8 | 78 → 77 | 6 → 6 | 10 → 9 |

Total: $27.690 and 690,702 output tokens. Every run was served only by `claude-opus-5-5`, with no refusal, subagent or permission denial. There were 3 checker errors and 161 warnings in total:

- Mac-Gray, ledger row 10: `round.opening_order` (Round opened is not the first row assigned to Process 1 Round 1).
- PetSmart, ledger row 11: `round.opening_order` (same check).
- Synacor, Deal facts row 11: `facts.process_count` (the value is "3 (2018; 2019; July 2020–February 2021)" rather than the bare number 3).

These are mechanical findings. They do not establish substantive accuracy, and the new drafts have not been reviewed.

## Workbook hashes

| Deal | Old SHA-256 | New SHA-256 |
|---|---|---|
| datalink | `499d2f2259f10bcb3895a08538bcbf4f686c55a4d568c0a6ded9096ee9449358` | `f28c711cf1ffdcc4b7f35ffd160719ed712c1dc022a89ed3ab878e557ea8217b` |
| kraton | `b1388206612abde5df19564951c3a897673fb5c7b2a6eb8b3d8e26f75c27a7d2` | `20cc6986afb8b301e2a38a8d06e2c191c0cf7d3621d7dcf84121d9265b3d780c` |
| mac-gray | `6c8b583bd9b948cd8e6dee6aa2f7fba43acc5598c5bf73c6f55ae7efab13a852` | `407615092e6dc33be22a8f80ab41d365083de0813f93b48897cbd7605a68ec0e` |
| meredith | `dbcca62b71624101fb17698736cf4faee112bca09d59223de780e77ce4fdf8ac` | `fae16e4a2ba8b6c6a233b9d029f94dacbfaacdabd4771b6b62fffdbaf4609c9e` |
| penford | `b2a25f75d3334e70962cf4782157aa42fb85bc6055ec0ef6410125a44d91758c` | `14f6c9c8e7c697b477e98f8f163c9180a236d1210e226cc0fdaeac98d50380d5` |
| petsmart | `05073372db646a9a219f893de8dabac90218ef3b7621315cf63bb366ca1f7c94` | `04c7d952864f1a122bb72bf489712cc0434465cc1b3957d8a686f15e174ec20c` |
| providence-worcester | `fa7c8f382a9931e649cb402043618b19da73eed0a623a5bf1deddad11b9f9f22` | `394a8cea099340df499697247c68430fef2010177ce91aae3930608d95cc3d00` |
| stec | `6e97cd3ad27116387cd7348f413f317a1173b1cd7c6a9190a776a73e7b2fbc62` | `467f739dea7b540eec2d3fb664ec1a4bb6479394820fc66b750e6ec3821fbc1d` |
| synacor | `13703aed7f4ae51dbef3b40bdc12c36b935e283a056adce93fd9c813d0e4dda9` | `4d2610753b2b6a06d6a4a4408306cc094999ddb8be1c5904e5f9eab3b2e025af` |

The old hashes equal the protected hashes in `../2026-09-21-v1132-cockpit/protected-inputs.json`.

## Cockpit

Before replacement, no cockpit working state existed (`_dev/cockpit/state/workspace.sqlite3` was absent, and no copy exists elsewhere). The catalog's findings, decisions and documents are all regenerated by `import_results.py` from committed packet evidence, and the importer reproduced the existing catalog byte for byte. No human-entered review data was at risk.

The replaced workbooks are archived outside the checkout at `/home/uctpiaj/work/Projects/sec-extraction-archive/2026-09-22-replaced-workbooks/` and are recoverable from Git at `03d59b1`.

The first import added each new extraction as an `opus55-medium` version beside the 20 earlier versions. Austin then asked for the cockpit to show only the new extractions. `import_results.py` now builds a catalog with one version per deal: `opus55-medium` ("Opus 5.5 medium extraction"), pointing at `extraction/<deal>.xlsx` and serving as the default working base. The Opus 5 v1.13 baselines, the v1.13.2 raw drafts and the lead-verified Datalink and Mac-Gray corrections are no longer cockpit versions.

Findings and documents keyed to those earlier workbooks' rows were removed from the catalog; their evidence stays in the Datalink, Mac-Gray and 21 September cockpit packets (that packet's seven raw workbooks have since left the checkout and are recoverable from Git at `03d59b1`). Two case-level decisions do not depend on any workbook's rows, so each remains as a deal-level finding with no source version. Datalink shows Austin's F9 ruling (January's bilateral stage is round 1; five rounds). The new Datalink draft has four rounds, so the ruling needs checking against it. *(Status, 26 September 2026: settled. Austin decided that Datalink follows the v1.14.1 text, which gives four rounds; F9 is superseded for Datalink. See the [v1.14.1 retest](../2026-09-26-v1141-retest/README.md).)* Mac-Gray shows the pending R01 decision and its research-decision document.

`import-verification.json` records the importer's verification of these receipts. `catalog-verification.json` is a read-only live check of the one-version catalog. For each deal it confirms that the version exports byte-identically, the displayed row counts and checker findings match fresh runs, and production state was unchanged. The frontend loads the catalog through the API at run time, so neither a rebuild nor a service restart was needed.

## Files

- `reextraction.json`: per-deal state, usage, checker summary, old and new hashes, and row counts for all four sheets.
- `receipts/<deal>/`: `metadata.json`, `status.json`, `command.json`, `check.json` and `provider-results.json` from each run. The paths in `check.json` refer to the deleted run directory; the workbook is byte-identical to `extraction/<deal>.xlsx`.

The run directories `_dev/runs/opus55-*` were deleted after these receipts were recorded. Their full event logs were not kept.
