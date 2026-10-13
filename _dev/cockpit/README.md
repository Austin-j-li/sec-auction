# Ledger cockpit

The cockpit is the shared extraction app on the VM. It is live at https://lines.dealextract.org since the switch-over of 28 September 2026 ([record](../alignment_sprint/SWITCHOVER.md)). The live service runs from its own deployment worktree and state. [STATUS.md](../STATUS.md) records the live commit, the listed deals and their versions. The product specification is [COCKPIT_APP_SPEC.md](../COCKPIT_APP_SPEC.md).

The catalog (`_dev/cockpit/catalog.json`) names the eight deals that have a filing in `raw_filing/`, with verified filing metadata. It holds no workbook version. A deal added through the app lives only in the state. A deal shows **No extraction yet** until its first run succeeds. That run becomes the deal's immutable base version and opens an editable working copy. A later run becomes a selectable version and does not replace the working copy. **Use as working-copy base…** moves the working copy to another version and records a reason.

The app seeds its instruction table from the repository instruction when a fresh state first starts. Later instruction versions are published in the app. The checker and the editor choices use the Version 1 ledger format only. The **Questions** sheet accepts Q ids for extraction questions and R ids for review items. A linked R item can be renamed; its references update with it. Remove its references before you delete it.

## Reviewing a deal

Open a deal and use the filing pane, search or printed page links to inspect evidence. A located quotation helps navigate; it does not establish that the row is accurate or that the ledger is complete. Stage edits in the Deal ledger, Rounds, Questions and Deal facts tabs, then save them with a reason. Process and Round can be changed across selected events in one save. A referenced event needs a replacement or its references cleared before deletion.

The Review tab shows the current mechanical check, the must-flag list and the row review marks. The must-flag list is `review_list.py`'s queue of cells Alex asked a person to look at; each ledger item links to its row. A row review mark holds a status only; write a note as a comment on the row. The checker reports format and consistency problems; a clean report is not research acceptance. Comments, history, comparisons and attribution remain in the state database. Export Excel adds a Source sheet with recorded provenance; select **Four sheets only (checker format)** for a file to pass to the checker.

## Runs and instructions

Austin and Alex connect their Claude or ChatGPT accounts in Settings and may run on their own subscriptions. Extract freezes the selected published instruction or draft when the job is submitted. The default engine is Opus 5.5 at medium effort; Fable 5.1, GPT-6.1-Sol and GPT-6-Astra are also selectable. GPT-6.1-Sol always runs on the Fast tier. GPT-6-Astra has an optional **Fast service** checkbox. By default, four runs can be active in total and two for each user; extra runs wait. The Runs tab shows progress, checker counts and receipts. A run is never started by viewing or saving a deal.

Instructions lists published versions and drafts. Published text is immutable. Publishing or changing the default affects future runs only. The app does not change `SEC_Deal_Ledger_Extraction_Instruction.md`; repository export requires a separate command at Austin's request.

## Adding and operating deals

Add Deal accepts a seed entry or an EDGAR filing link. It fetches the filing, shows its documents and saves the chosen document with source metadata. The new deal remains pending until a run succeeds. A whole deal or individual version can be hidden without deleting its state.

The database and file store are under ignored `_dev/cockpit/state/`, in the deployment worktree. Account tokens live outside that folder and must not be copied into Git. On the public site the server knows a reader only from the signed Cloudflare Access token it verifies (`_dev/tools/cockpit/access.py`); the plain email header is ignored.

## Services and releases

Three systemd user units run the app: `ledger-cockpit.service`, `ledger-worker.service` and `ledger-backup.timer` (which starts `ledger-backup.service`). The tracked copies in `_dev/tools/cockpit/deploy/` are the installed units. They start in `~/work/Projects/ledger-live`. The cockpit and worker units set `TMPDIR`. The tracked drop-in `20-public-origin.conf` sets the public origin.

One installed drop-in exists only on the VM: `~/.config/systemd/user/ledger-cockpit.service.d/30-access.conf`. It sets the Cloudflare Access team domain, the audience tag and `COCKPIT_REQUIRE_ACCESS=1`. It is not tracked, because the repository is public.

The nightly backups go to `~/backups/ledger-live/`. To release a new commit, follow [CLOUD_DEPLOYMENT.md](../CLOUD_DEPLOYMENT.md).

## Repository export

`_dev/tools/cockpit/export_repo.py` writes a published instruction or a deal version into a checkout, for a commit Austin requests. Run the deployment's own script. Write into the development clone with `--out-root`, never into the deployment folder. First run the command without `--write` and examine the dry run. Then repeat the command with `--write`:

```bash
python3 -B ~/work/Projects/ledger-live/_dev/tools/cockpit/export_repo.py \
  --out-root ~/work/Projects/sec-auction deal SLUG --version VERSION_ID
```

The same applies to `instruction NAME`. The script refuses `--write` without `--out-root`.
