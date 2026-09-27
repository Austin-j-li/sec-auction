# Ledger cockpit on the Version 1 build

This is the cockpit bundled with the Version 1 candidate. It remains a build artifact until Austin approves the switch-over in `_dev/alignment_sprint/SWITCHOVER.md`; the current public service keeps its existing checkout and state until then.

The catalog contains nine deals with verified filing metadata and no workbook version. A fresh state keeps the four deals added in the earlier app, their filings and Austin's and Alex's account records. All thirteen deals initially show **No extraction yet**. A deal's first successful run becomes its immutable base version and opens an editable working copy. Runs made later become selectable versions without replacing the working copy. Earlier runs, revisions, comments and instruction versions stay in the archived state.

The app seeds its instruction table from the repository instruction when a fresh state first starts. In this build that file says Version 0; at the approved switch-over the deployed file will be Version 1. The checker and editor choices use the Version 1 ledger format only. The **Questions** sheet accepts Q ids for extraction questions and R ids for review items. A linked R item can be renamed; its references update with it. Remove its references before deleting it.

## Reviewing a deal

Open a deal and use the filing pane, search or printed page links to inspect evidence. A located quotation helps navigate; it does not establish that the row is accurate or that the ledger is complete. Stage edits in the Deal ledger, Rounds, Questions and Deal facts tabs, then save them with a reason. Process and Round can be changed across selected events in one save. A referenced event needs a replacement or its references cleared before deletion.

The Review tab shows the current mechanical check and row review marks. The checker reports format and consistency problems; a clean report is not research acceptance. Comments, history, comparisons and attribution remain in the state database. Export Excel adds a Source sheet with recorded provenance; select **Four sheets only (checker format)** for a file to pass to the checker.

## Runs and instructions

Austin and Alex connect their Claude or ChatGPT accounts in Settings and may run on their own subscriptions. Extract freezes the selected published instruction or draft when the job is submitted. The default engine is Opus 5.5 at medium effort; GPT-6-Sol, GPT-6-Astra and Fable 5.1 are also selectable. The Runs tab shows progress, checker counts and receipts. A run is never started by viewing or saving a deal.

Instructions lists published versions and drafts. Published text is immutable. Publishing or changing the default affects future runs only. The app does not change `SEC_Deal_Ledger_Extraction_Instruction.md`; repository export requires a separate command at Austin's request.

## Adding and operating deals

Add Deal accepts a seed entry or an EDGAR filing link. It fetches the filing, shows its documents and saves the chosen document with source metadata. The new deal remains pending until a run succeeds. A whole deal or individual version can be hidden without deleting its state.

The database and file store are under ignored `_dev/cockpit/state/`. Account tokens live outside that folder and must not be copied into Git. The deployed services and nightly backup timer are described in the switch-over runbook. The Version 1 catalog is `_dev/cockpit/catalog.json`; `import_results.py` builds a new pending catalog from the filing manifest, and `verify_catalog.py` checks pending filings and any imported bases without historical review packets.
