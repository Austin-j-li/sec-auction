# Astra batch: 12 October 2026

All 12 listed deals completed a fresh GPT-6-Astra xhigh extraction with Fast service requested. All 12 working copies now use those results at revision 1. The old originals remain unchanged.

The mechanical checker reported zero errors and 12 warnings. The cockpit located all 712 ledger quotes in their filings. These checks do not establish substantive accuracy.

## Release and authority

Austin authorized the extraction batch and replacement of all listed working copies. He then authorized the merge and deployment. PR #20 merged as `357bef89a494c8f009aa621db45cf547dd986448`. The live cockpit moved from `a8ecea3d35e57a8c1f6201753f82022318da2ecb` to that commit.

The release used direct VM access after the prescribed ARC route reported no credential. The release held the deployment lock and checked the empty queue before and after the server stop. It took a backup before the checkout change. The database copy passed its integrity check. No dependency, instruction, or database migration was required.

The cockpit, worker, and backup timer returned to active state. Unsigned requests still reported an unknown reader with no edit permission; the deals endpoint returned 401. The authenticated browser displayed the new Fast control and the temporary 12-run limit before submission.

## Batch

All times below use Europe/London. Machine receipts retain UTC.

- Instruction: v1.1, ID `e77059e96146`, SHA-256 `e6e1e2f3b53378bdb6770762d33fe9b84090c2ae27301d5bf725e0c3f629eb13`.
- Model: `gpt-6-astra`; effort: `xhigh`; service tier request: `priority`.
- Each browser submission used Austin's connected ChatGPT account and a 90-minute limit.
- One isolated instruction and filing per run. No previous workbook was supplied to an extraction.
- All 12 runs were active together. Starts spanned 20 seconds, from 20:24:55 to 20:25:15.
- The final extraction completed at 20:35:48. The final replacement completed at 20:36:05.
- Each browser “Use as base” action recorded a reason and created revision 1.
- Both temporary service overrides were removed after the queue emptied. Limits returned to four total and two per user.
- Model requests and receipts record Fast service. They do not independently prove the provider's delivered tier.

| Deal | Minutes | Events | Rounds | Questions | Errors | Warnings |
|---|---:|---:|---:|---:|---:|---:|
| Datalink | 10.01 | 85 | 5 | 22 | 0 | 1 |
| Kraton | 9.29 | 71 | 3 | 20 | 0 | 0 |
| Mac-Gray | 6.91 | 59 | 3 | 15 | 0 | 0 |
| Penford | 6.96 | 47 | 2 | 14 | 0 | 0 |
| PetSmart | 9.84 | 62 | 2 | 20 | 0 | 1 |
| Providence & Worcester | 10.25 | 64 | 3 | 20 | 0 | 0 |
| sTec | 7.12 | 65 | 3 | 19 | 0 | 2 |
| Synacor | 7.89 | 72 | 6 | 23 | 0 | 2 |
| Medivation | 6.47 | 30 | 2 | 14 | 0 | 0 |
| Zep | 10.11 | 56 | 5 | 20 | 0 | 3 |
| Pepco Holdings | 7.29 | 49 | 2 | 16 | 0 | 2 |
| Imprivata | 10.50 | 52 | 3 | 21 | 0 | 1 |

## Final observations

The browser overview showed all 12 Astra Fast xhigh v1.1 bases at revision 1. Each new workbook matched its stored hash. Each working base matched its new version and hash. The 12 previous originals still existed and matched their earlier hashes. The cockpit marked each new working copy “In review.”

The warnings are review leads, not confirmed source errors. No warning was repaired during this extraction pass. The separate analytical admission issue from the earlier comparison is outside this batch.

| Deal | Sheet | Row | Warning |
|---|---|---:|---|
| Datalink | Deal ledger | 80 | Exclusivity changed has the same Who and Sort date as bid row #78, which codes an exclusivity request; if this row repeats the bid's own request, remove it (E10); a grant, execution or extension is its own event. |
| PetSmart | Rounds | 3 | Outcome 1 is Passed without action, but the ledger sets a later due date in this round on or after that deadline (12/10/2014) and reaches it; check whether the outcome is Extended (E9, item 1). |
| sTec | Deal ledger | 6 | Count is blank on a Process restarted row; it holds the number of open participations the marker closes, and stays blank only when it closes none (E5). |
| sTec | Deal ledger | 27 | Only one price endpoint is filled, but the Note does not visibly identify a floor or ceiling. |
| Synacor | Deal ledger | 14 | Count is blank on a Process restarted row; it holds the number of open participations the marker closes, and stays blank only when it closes none (E5). |
| Synacor | Deal ledger | 22 | Count is blank on a Process restarted row; it holds the number of open participations the marker closes, and stays blank only when it closes none (E5). |
| Zep | Deal ledger | 4 | Count is blank on a Process terminated row; it holds the number of open participations the marker closes, and stays blank only when it closes none (E5). |
| Zep | Deal ledger | 5 | Count is blank on a Process restarted row; it holds the number of open participations the marker closes, and stays blank only when it closes none (E5). |
| Zep | Deal ledger | 32 | Count is blank on a Process restarted row; it holds the number of open participations the marker closes, and stays blank only when it closes none (E5). |
| Pepco Holdings | Deal ledger | 22 | Only one price endpoint is filled, but the Note does not visibly identify a floor or ceiling. |
| Pepco Holdings | Deal ledger | 23 | Only one price endpoint is filled, but the Note does not visibly identify a floor or ceiling. |
| Imprivata | Deal ledger | 3 | Count is blank on a Process restarted row; it holds the number of open participations the marker closes, and stays blank only when it closes none (E5). |

## Receipts

- [Release and backup receipt](release.json).
- [Job IDs, versions, timings, hashes, and checks](results.json).
- [Mechanical warnings](warnings.json).
- [Final browser overview](overview.png).
- VM release record: `/home/uctpiaj/work/sec-auction-deployment/releases/20261012-192326Z-astra-fast/`.
- Backup before release: `/home/uctpiaj/backups/ledger-live/releases/20261012-192326Z-before-357bef8/20261012-192356Z`.
- Backup after replacement: `/home/uctpiaj/backups/ledger-live/releases/20261012-1936Z-after-astra-batch/20261012-193652Z`.

This packet contains operational receipts. Workbooks remain in the cockpit; no app version or workbook was exported to the repository. No tests or test suites ran.
