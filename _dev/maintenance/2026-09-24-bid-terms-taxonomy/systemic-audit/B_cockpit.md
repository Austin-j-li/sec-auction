# B. Cockpit: systemic audit for v1.14

25 September 2026. The slice is `_dev/tools/cockpit/`: the Python modules, `deploy/`, `acceptance/`, `frontend/src/` and `dist/`, plus `_dev/tools/test_cockpit*.py`.

The work was read-only:
- no service was restarted or sent a request;
- SQLite was opened only with `file:…?mode=ro`;
- no model, network or paid call was made.

Experiments ran on a scratch copy, `/tmp/b_cockpit_scratch`, now deleted. It held:
- the database, copied with the SQLite backup API from a `mode=ro` connection;
- `catalog.json`, `state/versions`, `state/instructions` and `state/filings`;
- `extraction/` and `raw_filing/`.

`git status --short` was the same before and after.

Evidence tags: **[V]** verified by reading the code; **[R]** verified by running (offline test or the scratch copy); **[I]** inference.

**What was run**
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s _dev/tools -p 'test_*.py'` gave `Ran 199 tests in 49.998s OK`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider _dev/tools/cockpit/acceptance/test_http.py` gave `14 passed in 13.17s`, on its synthetic temporary repository.
- vitest was not run: `npx vitest run` in the checkout writes `node_modules/.vite/vitest`. Instead the test cases were counted: 53 (api 3, deals 5, instructions 13, runs 23, trace 9).
- The browser suites were not run.

**Service state** (`systemctl --user show`)
- `ledger-cockpit` and `ledger-worker` started at 2026-09-24 22:02:00 UTC. That is after the last edits to `check_lean.py` (21:59:17) and `workspace.py` (21:59:31), so the live server already runs checker 1.6 and the current choice lists.
- `dist/` was built at 23 Sep 20:40:13, after the newest frontend source (20:39:58).

---

## 1. Claims

### Claim 1. Checker results are stored permanently: CONFIRMED, with one nuance

- **How the worker checks.** It runs `_dev/tools/check_lean.py` from the live checkout as a fresh subprocess for each job: `CHECKER` is defined at `worker.py:50`, and the call `[python, CHECKER, --workbook, --filing, --output run_dir/check.json]` is at `worker.py:311-312`. It keeps only the counts: `checker = {"errors": …, "warnings": …}` (`worker.py:318-319`).
- **Where results are stored.** Three places, each written once, at import:
  1. `jobs.result.checker` (`worker.py:320-321`);
  2. `versions.checker` (`worker.py:354-358`; the schema is at `runs.py:27`);
  3. the full receipt `_dev/cockpit/state/versions/<deal>/<id>/check.json` (`worker.py:342-344`).

  Nothing rewrites them. The only `UPDATE versions` in the cockpit is the hide flag (`runs.py:336`); `INSERT OR REPLACE` runs only on an import retry.
- **Nuance.** The receipt does record the checker version (and `ledger_schema` from 1.6 on). Only the two database copies lack it. Live receipts [R]:
  ```
  mac-gray/opus55-medium-20260924-2241-d7d267              1.6  v1.14  errors 1, warnings 16
  providence-worcester/opus55-medium-20260924-2241-38bc24  1.6  v1.14  errors 0, warnings 14
  imprivata, medivation, pepco-holdings, petsmart, zep     1.5  (no ledger_schema)
  ```
- **1.6 rejects the renamed value** [R]. In scratch copies of both pilots, replacing `Late bids accepted` with `Extended (late bid accepted)` on Rounds row 2 produced `controlled.deadline_outcome: Unallowed deadline outcome value(s): ['Extended (late bid accepted)']`. Mac-Gray went from 1 error to 2, P&W from 0 to 1. The value set is `DEADLINE_OUTCOMES` (`check_lean.py:261-267`); the test is at `:1296-1306`. Both pilots use `Late bids accepted` on Rounds rows 2 and 3.
- **What the UI shows: both, and neither is labelled with a checker version.**
  - **Live recheck.** It runs in the server process with the imported module, not as a subprocess.
    - An unedited copy uses a cached check (`data.py:733-743`, via `workspace.py:323`).
    - An edited working copy is rendered and rechecked on every request (`workspace.py:325-329`).
    - It is shown on All deals (`data.py:836-840`, then `Overview.jsx:9-17, 97`), in the Review tab's Mechanical check (`Review.jsx:28-60`) and as row issues.
  - **Stored counts** appear only in the Runs tab (`job.result.checker`, `Runs.jsx:45-50`). `versions[].checker` is sent (`workspace.py:29, :342`) but never displayed.
  - `check.checker_version` is in the payload (`data.py:984`), but no frontend file reads it (a grep for `checker_version` in `frontend/src` finds nothing).

### Claim 2. Choice lists need a restart: CONFIRMED. The editor is only partly restrictive.

- **Why a restart is needed.** `workspace.py:20` imports `check_lean` when the module loads, and every payload builds its choices from that module's constants (`workspace.py:349-357`). New lists therefore appear only after `ledger-cockpit` restarts. The live service's start time (22:02, after the 21:59 file edits) shows it already serves the 1.6 lists.
- **How the editor uses the lists** (`Records.jsx:123-152`; the citation 117-130 is the component's head). If a field has a list and its value is blank or on the list, the editor shows a `<Select>` offering only "Blank" and the listed values. Otherwise it shows free text: a `Textarea` (Deadline outcome is in `LONG_FIELDS`, `:10`) or an `Input`. So:
  - A blank field can only be set to a listed value.
  - A stored value that is not on the list (for example `Extended; Enforced`, or `Extended (late bid accepted)` under the current lists) is editable as free text. As soon as the typed text equals a listed value, the control switches to the Select.
  - A multi-deadline outcome `A; B`, which the checker requires with one part per Deadline row (`check_lean.py:1297`), cannot be built from a blank or single-valued cell. Such values are common today: `Extended; Enforced` appears in the working copies of Kraton, Meredith, PetSmart and sTec, and in the `extraction/` workbooks of Datalink, Kraton, Meredith, PetSmart and sTec [R].
- **The server does not enforce the lists.** `_coerce` (`workspace.py:515-549`) only types dates and numbers. [R] On the scratch copy, the edit API accepted `Extended (late bid accepted); Enforced`.

### Claim 3. The payload and diff gaps in S2: CONFIRMED, all three

1. **`ledger_schema` is missing.** The payload's `check` object holds only `{status, summary, scope_note, checker_version, other_issues}` (`data.py:980-986`), so the checker report's `ledger_schema` (`check_lean.py:1676`) is dropped. [R] `"ledger_schema" in payload` was `False` for Mac-Gray's working copy and for its v1.14 pilot.
2. **`_diff` walks only the new version's columns** (`workspace.py:497`). [R] Comparing Mac-Gray versions on the scratch copy:
   ```
   working -> pilot : All cash updates 0,  Stock % updates 13, Financing updates 13
   pilot -> working : All cash updates 16, Stock % updates 0,  Financing updates 0
   ```
   In practice only `compare` is affected. Edits within one base share its columns. A rebase or restore across bases changes every uid, so it shows as whole-row deletes and inserts that carry all values.
3. **One list per field, whatever the schema** (`workspace.py:349-357`). [R] The v1.13.2 working copy and the v1.14 pilot both get `Deadline outcome = [Enforced, Extended, Late bids accepted, Passed without action, Unclear]`.

### Claim 4. S3 facts: CONFIRMED

- **The download route** is `server.py:176-178`: `content = self.cockpit.workspace.export(slug, version)`, served as `{slug}-{version}.xlsx`.
- **`Workspace.export` is shared.** It is defined at `workspace.py:409-418` and used by `export_repo.py:131` and `verify_catalog.py:98, :100`. `test_cockpit_export.py:130` asserts that the repository export equals `ws.export` and calls those "the server's download bytes".
- **The HTTP test expects four sheets.** `acceptance/test_http.py:252` asserts the four sheet names. `:200` and `:206` assert that a raw-version download is byte-identical to the original.
- **`added_deals` has an `index_url` column** (`deals.py:27`), filled for the four live added deals (medivation, zep, pepco-holdings, imprivata). It is itself derived from the submission link: `submission_url[:-len(".txt")] + "-index.htm"` (`deals.py:240`), the same rule `fetch_filing.verify` uses (`fetch_filing.py:237`).
- **`MANIFEST.csv` stores complete-submission `.txt` URLs.** Worked example, Kraton (CIK 1321646, accession 0001193125-21-320389):
  - `source_url`: `https://www.sec.gov/Archives/edgar/data/1321646/0001193125-21-320389.txt`
  - EDGAR index: `https://www.sec.gov/Archives/edgar/data/1321646/0001193125-21-320389-index.htm`
  - saved document (the `document` column): `https://www.sec.gov/Archives/edgar/data/1321646/000119312521320389/d210874ddefm14a.htm`

  [R] For all nine manifest rows, `fetch_filing.submission_link()` maps both the derived index URL and the document URL back to the manifest's `.txt`. This was checked offline; no URL was fetched.

### Claim 5. S5 facts: CONFIRMED, with line corrections

- **`verify_catalog.py`:**
  - `revision != 0` is at `:83-84`, as cited.
  - The one-version check on the API list is at `:85-87`, not 86-88.
  - More assertions are now stale:
    - `:97-101`: an unedited working export must equal the base;
    - `:103-108`: the displayed check must equal a fresh check of the base, which is false for any edited deal;
    - `:117-119`: the top-level state files must be byte-identical before and after, which the live services can break by writing.
  - What `main()` overwrites: `main()` (`:127-132`) writes `_dev/reviews/2026-09-22-opus55-reextraction/catalog-verification.json` only after `verify()` returns. [R] On the scratch copy, `verify()` first raises `RuntimeError: Unexpected production revision: kraton`, so today it writes nothing. Updating the assertions would make it overwrite the 22 September evidence.
- **`export_repo.py:148-153`** refuses any path that `catalog.json` names anywhere (`catalog_paths`, `:46-58`). That includes `extraction/<slug>.xlsx` for all nine deals.
- **`import_results.py`** hard-codes:
  - `DEALS` (`:23-26`);
  - `VERSION_ID = "opus55-medium"` (`:36`);
  - `INSTRUCTION_HASH = 513c8e…` (`:32`);
  - `NAMES`.

  Its `main()` rewrites `catalog.json` and `import-verification.json` (`:232-243`).

### Claim 6. Default instruction: CONFIRMED. The fallback cannot be reached by new jobs.

- **The fallback.** At `worker.py:253-260`, a job with no `params["instruction"]` gets `self.repo / "SEC_Deal_Ledger_Extraction_Instruction.md"`.
- **When it happens.** Since phase 4, `runs.job_action` always freezes an instruction: `Instructions.resolve(request.get("instruction_id"))` (`runs.py:288-292, :307-308`). Without an id it takes the default (`instructions.py:169-181`); with no default it returns 409 "no default instruction" instead of falling back.
- **Live database (read-only).**
  - Three extraction jobs have no instruction, all queued on 23 Sep before phase 4 and all finished: petsmart 15:28, providence-worcester 16:19 (cancelled), medivation 16:30.
  - The five later jobs carry one.

  So the fallback would run only for a pre-phase-4 job still waiting in the queue, and there is none.
- **Other reads of the repository file:**
  - `worker.instruction_version()` (`worker.py:75-77`) labels those old jobs in `describe` (`:329`) and `import_version` (`:348`).
  - `Instructions._seed` (`instructions.py:88-109`) imports the file only when the `instructions` table is empty.
- **How the two relate.** The cockpit default is `settings.default_instruction = 513c8e3e8159`, named "v1.13.2". `system` seeded it from the repository file at 16:58 on 23 Sep, taking the name from the first 600 characters with `header_version`. Since then the two are independent:
  - Make default never writes the repository file.
  - Only `export_repo.py instruction <name> --write` does, and only for a published version (`export_repo.py:72-96`).

  Live instruction rows:
  - `v1.13.2`: published, the default;
  - draft `73f21eb8c09a`: text identical to v1.13.2;
  - draft `a4ca26ecfa92`: text `f9595d74…`, the 24 September draft, which both pilots used.

---

## 2. Findings

Each finding gives:
- **Where:** file and line;
- **Now:** what happens today, tagged [V] or [R];
- **Needs:** what v1.14 needs, with a proposed change;
- **Severity** and whether V114_SPEC covers it.

### B1. The gate order checks and reviews candidate runs with checker 1.6 (worker, server, editor)

- **Where:** V114_SPEC §7 gates 4, 5 and 7; `worker.py:311`; `workspace.py:20, :349-357`.
- **Now** [R]: the bounded blind runs (gate 4) and their review (gate 5) come before the deploy (gate 7). As a result:
  - The runs are checked by the live 1.6 file and keep 1.6 counts and receipts permanently (Claim 1).
  - The server's live recheck stays 1.6, so reviewers see a `controlled.deadline_outcome` error on every correct `Extended (late bid accepted)`.
  - The editor cannot offer that value for a blank cell (Claim 2).
- **Needs:** deploy S1 (checker 1.7) and S2 (schema-aware payload and choices) before gate 4. Both leave v1.13.2 behaviour unchanged, so an early deploy is safe. If the order stays, add B2 and state in the review notes that gate-4 results are checker 1.6.
- **Severity:** release blocker for the gate plan. **Spec:** no.

### B2. No screen shows a checker version (worker, API, frontend)

- **Where:** `worker.py:318-321`; `runs.py:123-129`; `data.py:984`; `Review.jsx:28-60`; `Runs.jsx:45-50`; `Overview.jsx:9-17`.
- **Now** [V]: the stored counts appear only in the Runs tab, the live recheck elsewhere, and no version label appears anywhere. After 1.7 is deployed, the pilots' Runs tab (1.6) and their live Review tab (1.7) will disagree without explanation.
- **Needs:**
  1. S1: store `checker_version` and `ledger_schema` in `versions.checker` and `jobs.result.checker`.
  2. For existing versions, read both from the receipt `check.json` (in the folder named by `versions.receipts`) when serving, and never rewrite it.
  3. Review, Mechanical check: show "Live check: checker 1.7, v1.14 rules" and, for run versions, "At import: checker 1.6, 1 error, 16 warnings".
  4. Runs tab and version picker: append "checker 1.6".
  5. All deals: a tooltip with the version.
- **Severity:** needed for v1.14. **Spec:** partly; §7 S1 stores the version but plans no display.

### B3. The payload has no schema and one choice list per field (API)

- **Where:** `data.py:968-989`; `workspace.py:349-357`.
- **Now** [R]: see Claim 3.
- **Needs:**
  - Set `payload["ledger_schema"]` from the report. If the check fails fatally, fall back to one helper in `check_lean` that reads the header, not a second detector.
  - Serve choices from a checker function keyed by schema.
  - Key them by the displayed version's schema (for the working copy, its base's), not "the deal's", because one deal can hold both schemas.
  - The v1.14 Deadline outcome list must not offer `Late bids accepted`. Stored legacy values still display, as free text.
- **Severity:** needed. **Spec:** §7 S2; its phrase "the deal's `ledger_schema`" should be corrected.

### B4. Cross-schema compare drops columns (backend)

- **Where:** `workspace.py:497`.
- **Now** [R]: see Claim 3.
- **Needs:** iterate over the after-version's columns, then the columns only the before-version has. Test with a v1.13.2 and v1.14 pair.
- **Severity:** needed. **Spec:** §7 S2.

### B5. The editor cannot enter multi-part or not-yet-listed values (frontend)

- **Where:** `Records.jsx:123-152`.
- **Now** [V, R]: see Claim 2. D11 adds a value and asks for more coding per deadline.
- **Needs:**
  - Deadline outcome, whose value lists one outcome per deadline separated by semicolons, needs a free-text input with suggestions (a `datalist`), or a picker that builds `A; B`.
  - Other single-value fields keep the Select but gain an "Other…" free-text option, so reviewers are not blocked when the lists lag behind the checker.
- **Severity:** needed for the v1.14 review. **Spec:** no.

### B6. Rebasing drops reviewed work without warning, and past revisions cannot be compared or downloaded (backend, frontend)

- **Where:** `workspace.py:766-773` (rebase), `:243` (uids are `sha256(slug|version sha|sheet|row)`), `:409-418` (export), `:441-471` (compare); `trace.py:233-235`; `Comments.jsx:66`; `main.jsx:682, :848-864`.
- **Now** [R], Mac-Gray revision 8 rebased onto its pilot in the scratch copy:
  - The rebase saved one revision, 9, with 87 deletes, 85 inserts and 59 decision changes.
  - `row_review` went from 58 marks to 0.
  - The finding `mac-gray-r01` went from supported/applied to unreviewed/unassessed.
  - A row thread became `target_missing` and is labelled "Record removed".
  - `deal_review` reads "edited since".
  - The Changes tab showed 0 changes against the new base.
  - Restoring revision 8 brings back the v1.13.2 base and all 58 marks.
  - Restoring revision 0 returns to the catalog base, not to the rebased one.
  - The dialog says only "The working copy is replaced by this version in one new revision."
  - Compare offers the current working copy and the versions (`main.jsx:682`), and Excel export takes only the working copy or a version id, so a past revision cannot be compared or downloaded without restoring it.
- **Needs:** see §4. The minimum:
  - a past revision (`rev:N`) as a read-only compare source and download;
  - a rebase dialog that lists what stops applying (revisions, row marks, finding decisions, row threads);
  - case-level finding judgments kept across a rebase (reset only implementation and verification), or an explicit prompt;
  - orphaned threads labelled "on an earlier base (revision N)".
- **Severity:** needed before any reviewed deal is rebased. **Spec:** no; §7 (D21) only forbids rebasing onto a pilot.

### B7. A working copy's columns are fixed by its base (backend constraint)

- **Where:** `workspace.py:618-621, :265-316`.
- **Now** [V]:
  - An edit may use only the base's columns, so a v1.13.2 working copy can never gain the v1.14 columns.
  - `_render_xlsx` writes values under the base workbook's own header, so the state's columns must equal the base's.
- **Needs:** no change now. Any port or migration tool must keep this invariant.
- **Severity:** nice to have (a constraint to record). **Spec:** no.

### B8. The five-sheet download fails the checker, and the docs say downloads and exports are identical (S3)

- **Where:** `check_lean.py:1637-1643`; `_dev/tools/README.md:118`; `test_cockpit_export.py:130`.
- **Now** [V]:
  - The checker reports `schema.sheets` for any sheet set other than the four, so a downloaded working copy with a `Source` sheet is not checker-valid.
  - README line 118 says a deal export uses "the same bytes as the cockpit's Excel download", and the test comment says the same. S3 makes both false for the working copy.
- **Needs:**
  - Keep S3 in the download route, as specified.
  - Add a four-sheet option for the working copy (`?source=0`).
  - Fix README line 118 and the test comment.
  - Put the revision in the file name: `{slug}-working-r{N}.xlsx`.
- **Severity:** needed. **Spec:** §7 S3, partly.

### B9. Sources for the S3 provenance sheet (API)

- **Where:** `data.py:970-975`; `workspace.py:366-368, :473-484`; `deals.py:240`; `fetch_filing.py:237`; `trace.py:126-134`.
- **Now** [V]:
  - Every payload has `filing.source_url`, the `.txt` link.
  - `added.index_url` appears only in the payload of a pending added deal.
  - Catalog versions carry `instruction_version` but no `instruction_sha256`; `_instruction_hash` resolves the hash through the published name (giving `513c8e…`).
  - Filing hashes come from `MANIFEST.csv` or `added_deals.sha256`; run versions also record `filing_sha256`.
- **Needs:**
  - One derivation of the index URL for every deal, with the `.txt` and index links both shown and labelled.
  - The instruction hash from `_instruction_hash`.
  - The revision number from the latest row in `revisions`.
  - A decision on review status: the uncommitted feature added a `deal_review` table, which is now one authoritative working-copy status with its revision. S3 may include it, or keep leaving it out.
- **Severity:** needed (S3 detail). **Spec:** §7 S3, partly.

### B10. Writing v1.14 workbooks to `extraction/` would break eight working copies (release)

- **Where:** `export_repo.py:148-153`; `data.py:686-711`; `workspace.py:162-169`.
- **Now** [V]:
  - The cockpit lists and resolves a catalog deal only if `extraction/<slug>.xlsx` exists (`data.py:686-694, :709`).
  - It hash-checks every catalog version's path (`workspace.py:166-168`).
  - Overwriting `extraction/<slug>.xlsx` with v1.14 bytes, by any means, would make every revision based on `opus55-medium` fail with 409 "catalog workbook hash does not match": the eight working copies.
- **Needs:** a release decision (S5). Either:
  - first copy the v1.13.2 workbooks to an archive path and repoint the catalog versions' `path` (same SHA-256, so revisions still resolve), then write the v1.14 files; or
  - add v1.14 as new catalog versions under new paths.
- **Severity:** needed for release. **Spec:** §7 S5 records the refusal, not this breakage.

### B11. Publishing keeps the text's hash; editing the header at publish time does not (instructions)

- **Where:** `instructions.py:45-48, :226-246`; `worker.py:345-351`.
- **Now** [V, live database]:
  - Publishing names the draft and freezes its text unchanged, so the hash stays the same.
  - Runs made on a draft keep `instruction_version = NULL` and the label "draft <sha7> (Austin)"; both pilots do.
  - Compare matches runs by `instruction_sha256`.
  - Editing the text, for example the header "v1.14 (candidate)" to "v1.14", makes a new hash. Gate-4 runs and runs after publication would then be marked "made under different instructions".
  - Nothing parses the header except `header_version` at seeding and the worker's fallback.
  - The 24 September draft (40 KB) is well under the 400 KB limit.
- **Needs:**
  - Settle the header before the draft is run, or accept that the published text is a new instruction.
  - Decide the new draft's parent:
    - the 24 September draft, `a4ca26ecfa92`, makes the editor's side-by-side diff match A1's diff;
    - v1.13.2 gives a cleaner published lineage.
- **Severity:** needed for gates 3–6. **Spec:** no.

### B12. A restart invalidates the write token in open tabs (server, frontend)

- **Where:** `server.py:42`; `main.jsx:121`; `api.js:13`.
- **Now** [V]: the CSRF token is created when the server starts, and the page reads it once. After a restart, every save from an open tab fails with 403 until the page is reloaded.
- **Needs:** in the deploy, ask users to save and reload. Optionally, fetch `/api/session` again on a 403 and retry once.
- **Severity:** a deploy step now; the code change is nice to have. **Spec:** no.

### B13. The root disk is nearly full (operations)

- **Where:** the root filesystem.
- **Now** [R]:
  - `/`, which holds `/tmp` and `~/backups`, is at 97%, with 299–345 MB free.
  - Neither service sets `TMPDIR`, so the server's per-request check files (`workspace.py:326`) and the nightly backups land there.
  - `/home/uctpiaj/work` has 327 GB free.
- **Needs:**
  - Check with `df -h` before deploying.
  - Optionally add `Environment=TMPDIR=%h/work/tmp` to both units.
  - Build the worktree and its `node_modules` (491 MB) under `/home/uctpiaj/work`, never `/tmp`.
- **Severity:** needed (operations). **Spec:** no.

### B14. The server and worker unit files are not in the repository (deploy)

- **Where:** `_dev/tools/cockpit/deploy/`, which has only `ledger-backup.*`.
- **Now** [V]: `ledger-cockpit.service` (with `.d/20-public-origin.conf`) and `ledger-worker.service` exist only in `~/.config/systemd/user`.
- **Needs:** copy them into `deploy/`, so they are reviewed and rolled back with the code.
- **Severity:** nice to have. **Spec:** no.

### B15. Backups: coverage is complete; the manifest does not identify the running code (backup)

- **Where:** `backup.py:40, :151-156, :332`.
- **Now** [V]:
  - A backup copies the whole database: instructions, instruction edits, settings, versions, jobs, deal review and every other table.
  - It copies the file store, including `instructions/<sha>.md`; the rehearsal compares every table.
  - v1.14 adds no stored artifact if S3 builds the sheet at download time and S1 keeps the version inside the database.
  - The manifest records only `git_head`, but the services run a tree with uncommitted changes.
- **Needs:**
  - A manual `backup.py create` just before the deploy.
  - Optionally, record `CHECKER_VERSION` and a hash of `dist/index.html` (or of `git diff`) in the manifest.
  - Keep database changes additive (`add_column`), so the old code can read the new database on rollback.
- **Severity:** nice to have. **Spec:** no.

### B16. One save is capped at 100 operations (backend; affects S4)

- **Where:** `workspace.py:742`.
- **Now** [V]: a Process or Round change across a whole deal needs one update per row. The largest ledger today has 85 rows (Meredith), and v1.14 runs may be larger.
- **Needs:** one bulk operation, or a higher cap for S4.
- **Severity:** needed if S4 is built. **Spec:** no.

### B17. One acceptance mode points at the live checkout (tests)

- **Where:** `acceptance/serve_fixture.py:93-95`.
- **Now** [V]:
  - `--actual-catalog-readonly` serves the live checkout, and `GET /api/instructions` opens a write connection (`instructions.py:82-86, :144`).
  - Browser evidence goes to `/tmp` by default (see B13).
- **Needs:** never use that mode for v1.14 tests, and set `COCKPIT_*_EVIDENCE` under `/home/uctpiaj/work/tmp`.
- **Severity:** nice to have. **Spec:** no.

### B18. Field formatting sets omit `CVR/earnout value` (frontend)

- **Where:** `Records.jsx:12-13`.
- **Now** [V]: `NUMERIC_FIELDS` and `MONO_FIELDS` omit it. This affects only the numeric keypad and the font; the server already stores it as a number (`workspace.py:24`).
- **Needs:** add it to both sets.
- **Severity:** nice to have. **Spec:** §7 S2, optional.

### B19. The Extract dialog does not warn about schemas (frontend)

- **Where:** `Runs.jsx` (the Extract dialog).
- **Now** [V]: once v1.14 is the default, it is preselected for every deal. Nothing tells the user that the new version cannot be merged into a v1.13.2 working copy.
- **Needs:** one line in the dialog when the working copy has revisions under another instruction or schema.
- **Severity:** nice to have. **Spec:** no.

### B20. The instruction fallback and a hard-coded label are dead paths (worker, frontend)

- **Where:** `worker.py:75-77, :253-260`; `runs.js:6, :51`.
- **Now** [V]: only pre-phase-4 jobs lack an instruction. The `'v1.13.2'` fallback label in `runs.js` labels only those old jobs; the Extract dialog passes its own label.
- **Needs:** keep them for old rows, or make a new job without an instruction fail explicitly.
- **Severity:** nice to have. **Spec:** no.

### B21. The deal list rechecks every edited deal on every request (performance)

- **Where:** `data.py:799-848`; `workspace.py:324-329`.
- **Now** [R]: every `GET /api/deals` renders and rechecks each edited deal with no cache. On the scratch copy it took 17.9 s cold and 5.9 s warm.
- **Needs:** cache by slug, revision and checker version. Expect a slow first load after the deploy restart.
- **Severity:** nice to have. **Spec:** no.

### Mixed-schema deals: what assumes one column set

| Area | Finding |
|---|---|
| `compare` / `_diff` | Assumes one set: B4. |
| Choices, and `ledger_schema` in the payload | Assume one set: B3. |
| Row review keys (`row_review`), comment threads, field authors | Keyed by uid, which is tied to the version, not the schema. Nothing carries over between versions of either schema (B6). |
| `record_label`, `trace.py`, `trace.js`, the digest, the review status | Use only When, Who, Event, Q, Process, Round and Field, which both schemas have. No change needed. |
| All deals list | Takes its counts from the live recheck; will change when the checker does (B2). |
| `DATE_FIELDS` / `NUMBER_FIELDS` in `workspace.py` | Name-based unions; no collision between schemas. No change needed. |
| `Records.jsx` field sets | Cosmetic only (B18). |
| Sorting and filtering | None in the ledger or sheet lists, which show sheet order. Nothing to change. |
| Compare row keys (`#`, Process/Round, Q, Field) | Schema-agnostic, but noisy across independent runs. |

---

## 3. Deploy checklist (v1.14 code, on Austin's order)

### Before the window: in the separate worktree on `/home/uctpiaj/work`

1. **Record the baseline.** When the worktree is created, copy the live tree:
   ```
   rsync -a --exclude node_modules --exclude dist <live>/_dev/tools/ <baseline>/
   ```
   Just before the deploy, confirm the live tree has not moved:
   ```
   diff -r --exclude node_modules --exclude __pycache__ --exclude dist <baseline> <live>/_dev/tools
   ```
   This must print nothing.
2. **Run the tests,** with `TMPDIR=/home/uctpiaj/work/tmp`. Every suite builds its own temporary repository root, so none touches the live state.
   - Unit tests: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s _dev/tools -p 'test_*.py'`. Baseline: 199.
   - HTTP: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider _dev/tools/cockpit/acceptance/test_http.py`. Baseline: 14. Update line 252 for S3.
   - vitest: `(cd _dev/tools/cockpit/frontend && npx vitest run)`. Baseline: 53.
   - Build:
     1. Copy `node_modules` (491 MB, work volume) or run `npm ci`, which needs the network.
     2. Run `npx vite build`, which writes to the worktree's own `dist`.
   - Browser: seven suites through `serve_fixture.py` (temporary root, fake worker, stubbed EDGAR), with each `COCKPIT_*_EVIDENCE` under `/home/uctpiaj/work/tmp`. Never use `--actual-catalog-readonly`.
   - The S1 fixtures, the S2 round trip and the S3 download tests.
   - Stored receipts reproduce under v1.13.2 rules.
   - For reference, `server.py --repo-root <dir>` and `worker.Worker(<dir>)` also accept a temporary root.
3. **Make the patch:** `diff -ruN <baseline> <worktree>/_dev/tools`, excluding `node_modules` and `dist`. The built `dist` travels separately.

### The window (away from 03:30 UTC, when `ledger-backup.timer` runs the checkout's `backup.py`)

1. **Confirm nothing is running.** The VM has no `sqlite3` command-line tool, so use Python, read-only:
   ```
   python3 -c "import sqlite3; c=sqlite3.connect('file:/home/uctpiaj/work/Projects/sec-extraction/_dev/cockpit/state/workspace.sqlite3?mode=ro', uri=True); print(c.execute(\"SELECT kind, state, COUNT(*) FROM jobs WHERE state IN ('queued','preparing','running','checking','importing','waiting_for_code','completing','waiting_for_approval') GROUP BY kind, state\").fetchall())"
   ```
   It must print `[]`; it did on 25 September. `pgrep -af run_model.py` must print nothing. Ask Alex and Austin to save and close their cockpit tabs.
2. **Check disk space:** `df -h / /home/uctpiaj/work`.
3. **Back up:** `python3 _dev/tools/cockpit/backup.py create` and note the path. Optionally run `backup.py rehearse`, which must exit 0.
4. **Record the smoke-test baseline:**
   ```
   curl -s http://127.0.0.1:8778/api/deals > ~/work/tmp/pre-v114-deals.json
   sha256sum _dev/cockpit/state/versions/*/*/check.json _dev/cockpit/state/versions/*/*/*.xlsx extraction/*.xlsx _dev/cockpit/catalog.json SEC_Deal_Ledger_Extraction_Instruction.md > ~/work/tmp/pre-v114-hashes.txt
   ```
5. **Keep a rollback copy of the code:**
   ```
   tar czf ~/work/tmp/pre-v114-tools.tgz --exclude=node_modules --exclude=dist _dev/tools
   ```
6. **Apply the patch** to the live checkout, with a dry run first. Nothing changes live until a restart, with two exceptions: the checker subprocess of a job (there are none) and the 03:30 backup.
7. **Restart the server:** `systemctl --user restart ledger-cockpit.service`. Then `journalctl --user -u ledger-cockpit -n 20 --no-pager` must show `ledger cockpit -> http://127.0.0.1:8778` and no traceback.
8. **Swap `dist`.** The server reads it from disk on every request, so this is live at once. It goes after the server restart so that the new frontend never talks to the old API.
   ```
   rsync -a <worktree>/_dev/tools/cockpit/dist/ _dev/tools/cockpit/dist.new/
   cd _dev/tools/cockpit && mv dist dist.old && mv dist.new dist
   ```
9. **Restart the worker:** `systemctl --user restart ledger-worker.service`. The journal must show "cockpit worker started". With `KillMode=process` and no jobs, there is nothing to reattach.
10. **Smoke tests,** over loopback with GET requests only. They are attributed to `local`; do not POST.
    - `curl -s 127.0.0.1:8778/api/session` returns `"user":"local"`.
    - `/api/deals`: the first call takes about 20 s. The same deals are listed. Every v1.13.2 base shows the same errors and warnings as the saved file; the pilots differ only by the documented new warnings.
    - `/api/deal/mac-gray?version=working`: `ledger_schema` is `v1.13.2` and `check.checker_version` is `1.7`.
    - The same with `?version=opus55-medium-20260924-2241-d7d267`: `ledger_schema` is `v1.14`, and the Deadline outcome choices include `Extended (late bid accepted)` but not `Late bids accepted`.
    - `/api/deal/mac-gray/export?version=working`: five sheets and a correct `Source` sheet.
    - `export?version=<id>`: its SHA-256 equals the version's.
    - `/api/deal/mac-gray/compare?from=working&to=<pilot>`: both `All cash` and the v1.14 columns appear.
    - `sha256sum -c ~/work/tmp/pre-v114-hashes.txt`: every line OK (receipts, workbooks, catalog and instruction unchanged).
    - Austin, on the public URL after a hard reload: the Review tab shows the checker version, and the pilots' runs show "checker 1.6".
11. **Tell both users to reload** any open tab (the write token has changed; B12).
12. **After acceptance,** remove `dist.old`. Keep the backup and the tarball for at least 14 days.

### Rollback

- **Code:**
  ```
  cd _dev/tools/cockpit && mv dist dist.bad && mv dist.old dist
  cd <live> && tar xzf ~/work/tmp/pre-v114-tools.tgz
  ```
  Then restart `ledger-cockpit`, then `ledger-worker`. Versions imported under 1.7 keep their 1.7 receipts, which is correct: they are immutable.
- **Data,** only if a migration damaged the state:
  1. stop both services;
  2. run `python3 _dev/tools/cockpit/backup.py restore <pre-deploy backup> --state _dev/cockpit/state --replace`, which moves the current state aside to `state.before-restore-<stamp>`;
  3. start both services.

  This loses anything saved after the backup. With additive schema changes, the old code reads the new database, so a data restore should not be needed for a code rollback.

---

## 4. Moving reviewed work to v1.14

### What is at stake (live database, read-only)

- **Eight deals have reviewed v1.13.2 working copies,** all based on `opus55-medium`, with these revision counts:

  | Deal | Revisions |
  |---|---|
  | Mac-Gray | 8 |
  | P&W | 16 |
  | PetSmart | 2 |
  | sTec | 1 |
  | Penford | 2 |
  | Synacor | 1 |
  | Kraton | 4 |
  | Meredith | 4 |
- **Row marks:** every ledger row of those deals is marked, 434 "reviewed" and 66 "needs decision".
- **Finding decisions:** one; Mac-Gray R01 is supported and applied.
- **Threads:** three (two deal-level, one on a P&W row).
- **Datalink:** no edits.

### What the code supports today

- **Keep:** a new run becomes a read-only version, and the working copy is untouched.
- **Rebase:** replace the working copy with the new version, losing its marks and decisions (B6).
- **Restore:** bring back any past revision, together with its own base.
- **Compare:** any two of the current working copy and the versions, matching rows by `#`.
- **History:** the full before and after of every past revision, as a list.
- **What it cannot do** (B6, B7):
  - view, compare or download a past revision without restoring it;
  - add v1.14 columns to a v1.13.2 working copy;
  - carry marks or comments from one version to another.

### Options

| Option | Supported today? | For | Against |
|---|---|---|---|
| **O1. Keep the v1.13.2 working copies.** v1.14 runs stay as read-only versions. | Yes | Nothing is lost. The reviewed record stays authoritative. | The reviewed deals stay on the v1.13.2 schema (All cash, no condition columns), so the dataset mixes schemas. D-rule changes (D8, D10, D11, D13) never reach those deals. |
| **O2. Rebase onto a reviewed v1.14 run and re-review,** using the old working copy as the checklist. | Rebase, yes. The checklist view, no. | A clean lineage: a blind v1.14 run plus attributed edits. The old work stays in History and can be restored. | The 500 row marks, the R01 decision and the row-thread anchors stop applying. Reviewers redo the row-level review. Without the B6 tooling they cannot see the old reviewed state beside the new one. |
| **O3. Replay the old edits onto the v1.14 run** (a port tool). | No | Less manual work. | The runs are independent extractions with different rows, numbering and schema, so matching is heuristic. v1.14 deliberately changes rows (D8, D10, D13), so replay would reimport v1.13.2 rulings that v1.14 reverses, such as PetSmart's Unclear deadline under the v1.13.2 rule. High risk of silent errors. |
| **O4. Convert the reviewed copy to the v1.14 schema** (All cash to Stock % and CVR; condition columns set to Not stated) as a derived base. | No | Keeps the marks, if uids are remapped. | A derived base is not a blind, immutable run. The new columns would be filled with placeholders instead of evidence. It contradicts the reason §7 (D21) gives for not rebasing onto pilots. |
| **O5. A second working copy per deal.** | No | Both lines stay live. | Contradicts the approved spec (one working copy per deal, `COCKPIT_APP_SPEC.md` §6.4). Needs large changes to the revisions table, trace and review status. |

### Recommendation [I]

1. Use **O1 by default** until a v1.14 run of a deal passes review.
2. Then use **O2, deal by deal,** with small additions:
   - a past revision (`rev:N`) as a read-only compare source and download;
   - the cross-schema diff fix (B4);
   - a rebase dialog that states what stops applying;
   - finding judgments kept across a rebase (implementation reset);
   - orphaned threads relabelled.
3. Before each rebase:
   - set the review status, which records "Reviewed at revision N";
   - download the working copy (with the S3 `Source` sheet, which records the revision);
   - note the revision in HANDOFF.
4. Rebase Datalink freely: it has nothing to lose.

---

## 5. Errors in V114_SPEC (§7 and §9, cockpit slice)

1. **§7 gates 4, 5 and 7: the order is wrong.** Candidate runs and their review happen under checker 1.6 and 1.6 choice lists, and their stored results stay 1.6. Deploy S1 and S2 before gate 4 (B1).
2. **§7 gate 7: the idle check is too narrow.** "Nothing queued or running" should cover every active state: `queued, preparing, running, checking, importing` for extractions, and `waiting_for_code, completing, waiting_for_approval` and queued or running lookups for sign-ins and deal lookups. It should also check `pgrep run_model.py`. Use the query in §3; there is no `sqlite3` command-line tool.
3. **§7 S5: stale citations and fix.**
   - The one-version check is at `verify_catalog.py:85-87`, not 86-88.
   - Lines 97-101, 103-108 and 117-119 are also stale.
   - `main()` overwrites its output only after `verify()` passes, and today `verify()` raises first. "Update the assertions" alone would therefore cause the overwrite. The safe fix is a new output path, or a refusal to overwrite.
   - The S5 note on `export_repo.py` omits that writing `extraction/<slug>.xlsx` would break eight working copies (B10).
4. **§7 S2:**
   - "the deal's `ledger_schema`" should be the displayed version's schema (B3).
   - S2 omits the editor's Select restriction and the multi-part Deadline outcome problem (B5).
   - The round trip itself already works in the backend [R]. In the scratch copy, the Mac-Gray pilot was rebased, edited, saved and exported:
     - numbers kept their type (`Price low` 21.25 and `CVR/earnout value` 1.25 as numbers);
     - `Stock %` `50-75` and `Varies` stayed text;
     - dates stayed dates;
     - the header matched the pilot's;
     - the raw bytes were unchanged.
5. **§7 S3:**
   - It omits that the five-sheet download fails the checker's four-sheet rule, and that `_dev/tools/README.md:118` and `test_cockpit_export.py:130` would become false (B8).
   - "Review status lives in four places" predates the uncommitted `deal_review` table, which gives one working-copy status.
   - `added_deals.index_url` is derived by the same rule as for the nine seed deals (`deals.py:240`, `fetch_filing.py:237`), so one derivation serves all deals.
6. **§7 S1 and §0: the server side is missing.**
   - "Store the checker version in the worker's summary (`worker.py:318-319`)" also needs `jobs.result` (`:320`) and a display (B2).
   - `data.py:984` is served but not shown.
   - §0 warns only that checker edits take effect early in the worker. It misses the opposite hazard: the server runs `check_lean` in-process, for the live recheck and the choice lists, and stays stale until it is restarted.
7. **§0: minor citation.** `server.py:185-193` should be 185-194.
8. **§9.4: baselines.**
   - The HTTP suite baseline, 14, is not stated.
   - The 199 unit-test baseline was confirmed [R].
   - The 53 vitest cases were confirmed by count only.
