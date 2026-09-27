# S2 with MIG-C: payload and API changes

Package S2 (cockpit schema awareness, V114_SPEC §7.4) with MIG-C (safe rebase, §7.9). Everything is additive: no
field was removed or renamed, no route changed method, and no database table or column was added (the new data
lives in existing JSON columns or is computed when serving). The old code reads a database written by the new code.

## Deal payload (`GET /api/deal/<slug>?version=…`, and the payload returned by `POST …/edit`)

| Field | Shape | Meaning |
|---|---|---|
| `ledger_schema` (new, top level) | `"v1.14"` \| `"v1.13.2"` \| `null` | Schema of the displayed version, from the checker report. When the check failed fatally (`status == "error"`), `check_lean.ledger_schema(path)` on the version's workbook (for a working copy, its base's; same columns). `null` for a pending added deal or an unreadable workbook. `data.report_schema(report, path)` holds the rule. |
| `choices` (changed) | `{field: [values]}` | Now `check_lean.choice_lists(ledger_schema)`: the displayed version's lists (a working copy has its base's). v1.13.2 gets `All cash` and no v1.14 columns; v1.14 gets CVR/earnout, Antitrust and the four condition columns and no `All cash`. Both get `Deadline outcome` with `No deadline stated`. `{}` when the schema is unknown (the editor then shows free text). The server still does not enforce any list. |
| `versions[].checker` (changed) | `{checker_version, ledger_schema, errors, warnings}` \| `null` | Was the raw `versions.checker` (`{errors, warnings}`) or absent. Now the check recorded at import: stored values for new imports; else read (never written) from the run's receipt `<versions.receipts>/check.json`; for catalog versions from `_dev/reviews/2026-09-22-opus55-reextraction/receipts/<slug>/check.json` when that packet's `reextraction.json` gives the version's SHA-256 as `new_sha256` (checker 1.5, `ledger_schema: null`). `null` = "At import: not recorded". |
| `workspace.revision`, `updated_at`, `updated_by` (fixed) | as before | While an original is shown (`?version=<id>`), these now give the **working copy's** latest revision, not 0. Before, the rebase dialog, which saves from that view, got 409 "stale revision" on any edited working copy (all eight reviewed deals). |
| `workspace.base_ledger_schema` (new) | schema \| `null` | The working copy's schema (its base's), whichever version is shown. |
| `workspace.base_instruction_version` (new) | string \| `null` | The working base's `instruction_version`. |
| `workspace.base_instruction_sha256` (new) | string \| `null` | The working base's instruction hash (`Workspace._instruction_hash`). |
| `findings[].carried_over` (new, optional) | `{revision, from_base, actor}` | Set on a finding decision a rebase carried over; a later decision on that finding drops it. |

`versions[0]` (the working entry) is unchanged except that its `review_status` also reflects the working revision while an original is shown.

## Other endpoints

- `GET /api/deals`: each entry's `check` gains `checker_version` and `ledger_schema` (of the live recheck), for the All deals tooltip.
- `GET /api/deal/<slug>/jobs`: `result.checker` gains `checker_version` and `ledger_schema`. New imports store them; for older completed jobs they are read from the imported version's receipt when serving (the stored row is not rewritten).
- `GET /api/deal/<slug>/comments`: each thread gains `target_context`: `null` while the target is live or not a row; `"on an earlier base (revision N)"` when a rebase or a restore across bases replaced the row (N = the last revision that held it; 0 = the starting catalog base); `"record removed"` when an ordinary edit deleted it. `target_missing` is unchanged.
- `GET /api/deal/<slug>/compare?from=…&to=…`: either side may be `rev:N` (read only; `rev:0` is the catalog's starting base, `rev:N` the snapshot saved as revision N; label "Revision N" / "Revision 0 (starting base)"). Unknown N → 404. Compare now walks the after-version's columns and then the before-only columns, so a v1.13.2 ↔ v1.14 compare shows `All cash` and the v1.14 columns in both directions.
- `GET /api/deal/<slug>/export?version=rev:N` (new value): `rev:0` returns the starting base's raw bytes; `rev:N` renders that snapshot on its own base. No revision is saved. The server's filename stays `{slug}-{version}.xlsx` (so `…-rev:3.xlsx`); the History tab's link sets `download="{slug}-revision-{N}.xlsx"`. **S3 owns the download route**: when it adds the Source sheet and `{slug}-working-r{N}.xlsx`, it should decide the name (suggest `{slug}-r{N}.xlsx`) and whether `rev:N` gets a Source sheet. `Workspace.export(slug, "rev:N")` is the hook.
- `GET /api/deal/<slug>/rebase?to=<version id>` (new, GET only; POST → 405): the rebase dialog's payload. Nothing is saved.
  ```
  {"current": {"id", "label", "instruction_version", "ledger_schema", "revision"},
   "target":  {"id", "label", "instruction_version", "ledger_schema"},
   "deal_review": {… as GET …/review …},
   "stops_applying": {"revisions": n,            # revisions saved on the current base since it became the base
                      "edits": n,                # cell and row changes from the base (not decisions)
                      "row_marks": {"total", "reviewed", "needs_decision", "unreviewed"},
                      "row_threads": {"total", "open", "resolved"},   # threads on rows now live
                      "finding_decisions": {"total", "judgments_kept", "reset"}}}
  ```
  400 for an invalid id, the current base or a hidden version (same messages as the rebase itself); 404 for an unknown version.

## Behaviour changes in saves

- **Rebase** (`operations: [{type: "rebase", …}]`): finding decisions with a judgment other than `unreviewed` (or a note) carry over with `implementation: "unassessed"`, `verification: "unchecked"` and `carried_over`; the decision's `actor`/`at` stay the judge's. Row marks and row threads stay with the old rows, as before. Restoring the pre-rebase revision brings everything back (unchanged).
- The working copy's columns still equal its base's: an update naming a column the base lacks is still refused (`invalid columns`); tested both ways.

## Worker

`versions.checker` and `jobs.result.checker` now store `{"errors", "warnings", "checker_version", "ledger_schema"}` from the run's `check.json` (`worker.py`, `finish`). Receipts are unchanged.

## Frontend

- `choices.js` (new): `MULTI_FIELDS`, `OTHER`, `valueParts`, `addPart`, `listControl`. Records.jsx: Deadline outcome is free text with an "Add an outcome…" picker that appends `; ` parts (the picker sits outside the Fluent Field so the text box keeps the label); other listed fields keep the drop-down with `Other…`, which switches to free text ("Choose from the list" switches back); a stored value off the list shows as text with the hint "Not on this version's list". `CVR/earnout value` joined `NUMERIC_FIELDS` and `MONO_FIELDS`.
- runs.js: `INSTRUCTION_VERSION` renamed `LEGACY_INSTRUCTION_LABEL` (only `jobInstructionLabel`'s fallback for the three pre-phase-4 jobs); `runSummary`'s default label is now "default instruction" (the dialog passes the chosen instruction, which starts as the default). New `checkerLabel`, `liveCheckText`, `importCheckText`, `extractNotice`, `rebaseLines`; `versionOptionLabel` appends `· checker X`.
- Review tab mechanical check: "Live check: checker 1.7, v1.14 rules" and, for an original, "At import: checker 1.6, 1 error, 16 warnings" or "At import: not recorded"; a carried finding shows "Judgment carried over from <base> at revision N; implementation and verification reset".
- Runs tab: "checker 1.6 · 1 error · 16 warnings". Version picker: "… · checker 1.6". All deals: tooltip on the check line.
- History tab: per revision, "Download" (`export?version=rev:N`) and "Compare with working copy" (sets Compare to `rev:N` → working, opens Changes). Compare's From/To lists also offer "Revision k · read only" for k < the working revision.
- Rebase dialog: fetches `GET …/rebase?to=` and lists the lines from `rebaseLines`; "Use as base" waits for the list (or its error).
- Threads: `threadContext(thread)` in trace.js shows "On an earlier base (revision N)" or "Record removed"; threads are re-read after a rebase or restore.
- Extract dialog: gets `working={deal.workspace}` and shows one warning line when the chosen instruction's hash differs from the working base's (names compared when a hash is unknown).
- style.css: `.add-part`, `.history-actions`, `.mechanical-content > p.checker-lines`, `.modal .rebase-list` (inserted beside related rules, not at the end).

## Merge notes

- `server.py`: only `DEAL_ACTION_RE` (adds `rebase`) and one GET line after `review`; the export lines (S3) are untouched.
- `data.py`: `build_deal_payload` gains an optional `workbook_path`; `report_schema` is new; `list_deals` adds two keys to `check`. `slugs()`/`resolve()` (S5) untouched.
- `worker.py`: only the checker summary in `finish` and a type hint; the instruction fallback (OPS) untouched.
- `api.js` untouched (OPS). The rebase preview is fetched with `json()` in main.jsx.
- `dist/` not built into the sandbox; a check build went to the temp dir.
