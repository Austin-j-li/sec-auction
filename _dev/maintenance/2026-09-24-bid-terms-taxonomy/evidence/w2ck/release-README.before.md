# D25 release patch (package S5)

`d25-tools.patch` carries the `_dev/tools/` code for D25: moving the nine v1.13.2 workbooks out of `extraction/` at gate 12 (spec §7.7, §13 gate 12). It is applied at gate 12 only, never at the deploy.

SHA-256 of `d25-tools.patch`: `299cee26f3be43a772785b79d419297291ef4e50fac3c5d972dbf7e988ece97d`.

## What the patch contains

The patch changes four files. It was taken with `git diff --no-index --binary` between two copies of S5's deploy-state tree, so its paths are `a/_dev/tools/…` and `b/_dev/tools/…` and it applies from the repository root with `git apply`.

- `_dev/tools/cockpit/import_results.py`:
  - adds `WORKBOOKS = "_dev/reviews/2026-09-22-opus55-reextraction/workbooks"`;
  - reads the nine workbooks from there when it checks them against their receipts (the old `extraction/{deal}.xlsx` at `:203`);
  - writes catalog paths there (the old `:216`);
  - updates the module docstring to match.
- `_dev/tools/cockpit/verify_catalog.py`: requires each catalog version's path to be `WORKBOOKS/<slug>.xlsx`. The deploy-state script has no path check (see below).
- `_dev/tools/cockpit/test_import_results.py`:
  - the synthetic receipts point at the relocated workbooks;
  - a new test shows that v1.14 workbooks in `extraction/` do not change the catalog the importer builds.
- `_dev/tools/test_cockpit_catalog.py`:
  - the deploy-state test "verify passes in place" becomes "verify requires the relocated paths" (it refuses `extraction/` paths and passes after relocation);
  - a new `ReleaseTests` class simulates gate 12 on a synthetic nine-deal repository. It sets up two edited working copies and an imported run version per deal. Before relocation, `export_repo.py` refuses `extraction/<slug>.xlsx`. After the workbooks move and the catalog is repointed, every working copy shows the same base id, hash, revision and cells, and `verify_catalog` passes. `export_repo.py deal <slug> --version run1 --write` is then accepted for all nine and writes the run's bytes. The working copies are unchanged afterwards, the nine deals are still listed, and `verify_catalog` passes again.

**Prerequisite: the deploy patch from gate 3.** The patch's context is S5's deploy state, which introduced three things:
- the catalog lookup in `data.py` (`Cockpit.slugs()` and `resolve()` find a catalog deal from `catalog.json` and `raw_filing/MANIFEST.csv`, with its workbook taken from the catalog base's `path`);
- the rewritten `verify_catalog.py`;
- `test_cockpit_catalog.py`.

The patch does not apply to a tree without them. If anyone edits these four files after this patch was made, regenerate it.

**Not in this patch:**
- **The release lines of `_dev/tools/README.md`.** §12 step 5 puts them in the release patch. They belong to S6, so the lead appends them or ships them beside this patch. In particular, line 49 still says the importer uses `extraction/<deal>.xlsx`.
- **Repointing `catalog.json`.**
- **The `git mv` of the nine workbooks.**
- **The export of the v1.14 runs.**

None of these was done now. S5 did not touch `catalog.json`, `extraction/` or any cockpit state. They are gate 12 steps, carried out at a commit Austin requests, as below.

## Applying it at gate 12

`$LIVE` is `/home/uctpiaj/work/Projects/sec-extraction`. Run everything from `$LIVE`, on Austin's command, after S5's lookup change is deployed (gate 3). To check that it is deployed: `grep -n "def catalog_deals" _dev/tools/cockpit/data.py` must print a line.

1. **Check that nothing is running** with the jobs query and `pgrep -af run_model.py` from §12 ("The window", step 1). Then stop both services for steps 2–6:
   `systemctl --user stop ledger-worker.service ledger-cockpit.service`.
2. **Move the nine workbooks, bytes unchanged** (gate 12.1):
   ```
   W=_dev/reviews/2026-09-22-opus55-reextraction/workbooks
   mkdir -p $W
   for d in datalink kraton mac-gray meredith penford petsmart providence-worcester stec synacor; do git mv extraction/$d.xlsx $W/$d.xlsx; done
   ```
3. **Repoint only their catalog paths** (gate 12.2). This keeps the id `opus55-medium`, the SHA-256 and `instruction_version: v1.13.2`. The committed `catalog.json` round-trips byte for byte through this formatting, so the diff is exactly nine `path` lines:
   ```
   python3 - <<'EOF'
   import json
   from pathlib import Path
   path = Path("_dev/cockpit/catalog.json")
   catalog = json.loads(path.read_text(encoding="utf-8"))
   for slug, item in catalog["deals"].items():
       for version in item["versions"]:
           if version["id"] == "opus55-medium" and version["path"] == f"extraction/{slug}.xlsx":
               version["path"] = f"_dev/reviews/2026-09-22-opus55-reextraction/workbooks/{slug}.xlsx"
   path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
   EOF
   git diff --stat _dev/cockpit/catalog.json   # 9 insertions, 9 deletions
   ```
4. **Apply the release patch** (gate 12.3):
   ```
   git apply --check _dev/maintenance/2026-09-24-bid-terms-taxonomy/release/d25-tools.patch
   git apply _dev/maintenance/2026-09-24-bid-terms-taxonomy/release/d25-tools.patch
   ```
   Also apply S6's release lines of `_dev/tools/README.md`.

   Optional cross-check, which writes only the named output: `python3 _dev/tools/cockpit/import_results.py --output /home/uctpiaj/work/tmp/d25-catalog-check.json`. It must equal the repointed `catalog.json` as JSON. It refuses if `raw_filing/MANIFEST.csv` holds more than the nine deals, for example after an added deal has been exported.
5. **Export the v1.14 runs** (gate 12.4). For each deal, first a dry run, then the write:
   ```
   python3 _dev/tools/cockpit/export_repo.py deal <slug> --version <v1.14 run id>
   python3 _dev/tools/cockpit/export_repo.py deal <slug> --version <v1.14 run id> --write
   ```
   `export_repo.py` now accepts `extraction/<slug>.xlsx`, because the catalog no longer names it.
6. **Test, verify, back up and restart** (gate 12.5):
   - run the §9.4 suites;
   - run `python3 _dev/tools/cockpit/verify_catalog.py`. It writes `_dev/reviews/2026-09-22-opus55-reextraction/catalog-verification-<UTC timestamp>.json` and never overwrites an existing file, including the 22 September `catalog-verification.json`. It exits 1 with "Verification failed: …" on any failed check;
   - run `python3 _dev/tools/cockpit/backup.py create`;
   - start `ledger-cockpit.service`, then `ledger-worker.service`.
7. Gate 12.6 and 12.7 (whether the repository copies become catalog entries, and the release documentation lines) are Austin's and S6's. If Austin makes the repository copies catalog entries, `verify_catalog.py` needs a change first: it still requires exactly one catalog version per deal.

**Rollback before the commit:**
- `git apply -R` the patch;
- `git mv` the nine back;
- `git checkout -- _dev/cockpit/catalog.json`;
- remove any exported `extraction/` files.

The working copies resolve in both states, because the lookup change finds them through the catalog.

## Verification done (25 September, in `/home/uctpiaj/work/tmp/v114-scratch/tmp/s5`, never in the live checkout)

- **Patch check.** `git apply --check` and `git apply` succeeded on a third fresh copy of the deploy-state tree, and the result was identical (`diff -r`) to the hand-edited release copy.
- **Deploy state (the S5 sandbox):**
  - unit tests: 206 passed (199 + 7 new);
  - HTTP: 14 passed;
  - vitest: 53 passed.
- **Deploy state plus this patch:**
  - unit tests: 208 passed;
  - HTTP: 14 passed;
  - vitest: 53 passed.
- **Rehearsal of steps 2–6** on a temporary copy of the tree with the real nine v1.13.2 workbooks and the committed `catalog.json`. There was no cockpit state, so every deal was unedited.
  - The deploy-state `verify_catalog` passed in place, and refused to overwrite its output on a second run.
  - After the move and the repoint, the catalog diff was nine lines, and the deploy-state lookup listed all nine deals with `extraction/` empty.
  - The patch applied, and `import_results.py --output` produced a catalog JSON-equal to the repointed one.
  - `export_repo.py deal kraton --version working` (dry run) was accepted.
  - The patched `verify_catalog.py` passed and wrote a new timestamped file beside the untouched 22 September one.

Logs are in `../evidence/s5/`.
