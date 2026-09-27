# D25 release patch (package S5)

> **Status, 26 September, about 20:45 UTC.** `deploy-tools-v1141.patch` was applied to the live checkout at 19:41 UTC by Austin's order (gate 3 done; [receipt](../../2026-09-26-v1141-streamline/deployment-v1141.json)), so the WP1 engine note below is out of date: Opus 5.5 medium is the live default. Austin published the edited v1.14.1 candidate in the cockpit as v1.14.1 at 20:18 UTC (id `08caed447f7d`, SHA-256 `8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98`, the reviewed `8bdb7c20…8a79` plus eight approved wording fixes) and made it the cockpit default. The release notes below name `8bdb7c20…`; the published text is `8a93df3c…6c98`, and `check_lean.RULES_BY_INSTRUCTION` maps both to v1.14.1. Gate 12 (this folder's `release-gate12.patch`), the repository export and the unit-file changes are still GATEs.

**26 September, evening: retargeted to v1.14.1** ([PIPELINE_UPGRADE_SPEC](../../2026-09-26-v1141-streamline/PIPELINE_UPGRADE_SPEC.md) WP7). This supersedes the integration update below.
- **The release is v1.14.1**, the candidate `SEC_Deal_Ledger_Extraction_Instruction_v1.14.1_candidate.md` (SHA-256 `8bdb7c205512c9bcf55ffa7623fba0a8bb4aabaed23c99845fa88b4a80cc8a79`) in [2026-09-26-v1141-streamline](../../2026-09-26-v1141-streamline/). The v1.14 candidate (`c2d47a47…ab27`) was trialled and will not be released as the default. The runs exported at gate 12 are v1.14.1 runs.
- **The default extraction engine is Opus 5.5 at medium effort again** (WP1, built in both trees, not yet deployed). The GPT-6-Astra-high default described below is superseded; until the WP1 restart the live cockpit still preselects Astra high.
- **The deploy patch for gate 3 is `deploy-tools-v1141.patch`**, in this folder, regenerated from `~/work/Projects/sec-extraction-v114` against main after WP1–WP6. It deploys checker 1.8, which checks a 29-column ledger under the v1.14.1 rules by default and under the v1.14 rules with `--rules v1.14`; the cockpit picks the rules from the instruction version's SHA-256. The 25 September `deploy-tools.patch` is superseded and kept for the record only: `git apply --check` fails on `runs.js`, `runs.test.js`, `run_model.py` and `test_cockpit_phase4.py`, because the Astra-default change touched the same lines.
- **The gate 12 patches** (`d25-tools.patch`, `tools-readme-release.patch` and their concatenation `release-gate12.patch`) had their added comments, docstrings and README lines retargeted from "v1.14" to "v1.14.1". No code or hunk line count changed. The 25 September versions are kept as `*.patch.pre-v1141`. See "Retarget check (26 September)" at the end.

**26 September integration update (superseded by the note above):** Austin approved GPT-6-Astra high as the extraction default after the 15-run trial. That narrow change is live and has been merged into the upgrade code. These 25 September deploy/release patches predate it: reconcile and regenerate affected patches against the new baseline before use; preserve explicit engine choices and legacy Opus job provenance. The trial is complete; its findings and the proposed, unapproved instruction amendment are in [the current packet](../../2026-09-26-astra-default-pro-verification/README.md). The instruction candidate remains unpublished.

`d25-tools.patch` carries the `_dev/tools/` code for D25: moving the nine v1.13.2 workbooks out of `extraction/` at gate 12 (spec §7.7, §13 gate 12). It is applied at gate 12 only, never at the deploy.

SHA-256 of `d25-tools.patch`: `e6576c63ed5490fac64cda718639cbd3a5901f1e3a2878249108bd59a96a4bbc` since its comments were retargeted to v1.14.1 on 26 September; before that it was `5bc4a5cae0c176e6b9f8ebb0447d522ab6275dae4c65b8a622e1110313e8ef4f`, kept as `d25-tools.patch.pre-v1141`. That version was regenerated on 25 September against the integrated worktree after wave 2, which added a relocation test to `test_cockpit_catalog.py`; the wave-1 version (`299cee26…e97d`), made against S5's own tree, is kept as `d25-tools-wave1.patch` for the record and no longer applies. Checked on 25 September: the deploy tree plus this patch passes 294 unit tests and 20 HTTP tests. The 26 September retarget changed only comments, docstrings and README text, and the tests were not rerun.

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
  - a new test shows that v1.14.1 workbooks in `extraction/` do not change the catalog the importer builds.
- `_dev/tools/test_cockpit_catalog.py`:
  - the deploy-state test "verify passes in place" becomes "verify requires the relocated paths" (it refuses `extraction/` paths and passes after relocation);
  - a new `ReleaseTests` class simulates gate 12 on a synthetic nine-deal repository. It sets up two edited working copies and an imported run version per deal. Before relocation, `export_repo.py` refuses `extraction/<slug>.xlsx`. After the workbooks move and the catalog is repointed, every working copy shows the same base id, hash, revision and cells, and `verify_catalog` passes. `export_repo.py deal <slug> --version run1 --write` is then accepted for all nine and writes the run's bytes. The working copies are unchanged afterwards, the nine deals are still listed, and `verify_catalog` passes again.

**Prerequisite: the deploy patch from gate 3.** Since 26 September that is `deploy-tools-v1141.patch`, which replaces the superseded `deploy-tools.patch`. The patch's context is S5's deploy state, which introduced three things:
- the catalog lookup in `data.py` (`Cockpit.slugs()` and `resolve()` find a catalog deal from `catalog.json` and `raw_filing/MANIFEST.csv`, with its workbook taken from the catalog base's `path`);
- the rewritten `verify_catalog.py`;
- `test_cockpit_catalog.py`.

The patch does not apply to a tree without them. If anyone edits these four files after this patch was made, regenerate it.

**Not in this patch:**
- **The release lines of `_dev/tools/README.md`.** §12 step 5 puts them in the release patch: they are in `tools-readme-release.patch`, and `release-gate12.patch` is this patch followed by that one, the file to apply at gate 12. The deploy patch for gate 3 is `deploy-tools-v1141.patch`, which replaces the 25 September `deploy-tools.patch` (superseded; it no longer applies).
- **Repointing `catalog.json`.**
- **The `git mv` of the nine workbooks.**
- **The export of the v1.14.1 runs.**

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
5. **Export the v1.14.1 runs** (gate 12.4). For each deal, first a dry run, then the write:
   ```
   python3 _dev/tools/cockpit/export_repo.py deal <slug> --version <v1.14.1 run id>
   python3 _dev/tools/cockpit/export_repo.py deal <slug> --version <v1.14.1 run id> --write
   ```
   `export_repo.py` now accepts `extraction/<slug>.xlsx`, because the catalog no longer names it.
6. **Test, verify, back up and restart** (gate 12.5):
   - run the §9.4 suites;
   - run `python3 _dev/tools/cockpit/verify_catalog.py`. It writes `_dev/reviews/2026-09-22-opus55-reextraction/catalog-verification-<UTC timestamp>.json` and never overwrites an existing file, including the 22 September `catalog-verification.json`. It exits 1 with "Verification failed: …" on any failed check;
   - run `python3 _dev/tools/cockpit/backup.py create`;
   - start `ledger-cockpit.service`, then `ledger-worker.service`.
7. Gate 12.6 and 12.7 (whether the repository copies become catalog entries, and the release documentation lines) are Austin's and S6's. If Austin makes the repository copies catalog entries, `verify_catalog.py` needs a change first: it still requires exactly one catalog version per deal.

**Rollback before the commit,** in this order, from `$LIVE` with `W` set as in step 2. Skip a step whose forward step did not run (for example, `git apply -R` fails if step 4 did not run).
1. If step 6 restarted the services, stop them again: `systemctl --user stop ledger-worker.service ledger-cockpit.service`. They read `catalog.json` and the workbooks.
2. **Remove the exported v1.14.1 files first.** Once step 5 has run, `extraction/<slug>.xlsx` holds a v1.14.1 run, and `git mv` refuses to move a v1.13.2 workbook onto an existing file. For the nine deals the export writes only `extraction/<slug>.xlsx`, which git sees as untracked because step 2 staged the old file's move. Move them aside rather than deleting them:
   ```
   mkdir -p /home/uctpiaj/work/tmp/d25-rollback
   for d in datalink kraton mac-gray meredith penford petsmart providence-worcester stec synacor; do [ -e extraction/$d.xlsx ] && mv extraction/$d.xlsx /home/uctpiaj/work/tmp/d25-rollback/; done
   ```
3. `git mv` the nine back: `mkdir -p extraction; for d in datalink kraton mac-gray meredith penford petsmart providence-worcester stec synacor; do git mv $W/$d.xlsx extraction/$d.xlsx; done`, then `rmdir $W`.
4. Restore the catalog from the commit, not the index, in case it was staged: `git checkout HEAD -- _dev/cockpit/catalog.json`.
5. `git apply -R` the patch, and reverse S6's release lines of `_dev/tools/README.md` the way they were applied.
6. Check: `git status --short -- extraction _dev/cockpit/catalog.json $W _dev/tools` shows none of the release changes, and `git diff --stat HEAD -- extraction _dev/cockpit/catalog.json` prints nothing. A `catalog-verification-<timestamp>.json` written in step 6 may stay as evidence.
7. Start `ledger-cockpit.service`, then `ledger-worker.service`, if they were running before.

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

## Retarget check (26 September, in a scratch copy, never in the live checkout)

Each patch was checked with `git apply --check` before and after the retarget, against scratch copies of the six files it touches or depends on, taken from main and from the v114 worktree:
- **Against main:** all three patches fail before and after, with the same errors. `verify_catalog.py:101` does not match and `test_cockpit_catalog.py` does not exist (d25-tools); `_dev/tools/README.md:46` does not match (tools-readme-release). Main lacks the deploy state these patches need: `data.py` has no `catalog_deals`, and neither the rewritten `verify_catalog.py`, `test_cockpit_catalog.py` nor the deploy-class README lines are there. This is the prerequisite above, not a defect: apply them only after `deploy-tools-v1141.patch`.
- **Against main after the deploy patch:** in a scratch copy of main's `_dev/tools/`, `deploy-tools-v1141.patch` as written at 19:25 UTC passed `git apply --check` and applied. `release-gate12.patch` then passes `git apply --check`, before the retarget and after it. Repeat this check if the deploy patch is regenerated.
- **Against the v114 worktree (the deploy state):** all three pass before and after. `release-gate12.patch` was also applied in full to a throwaway copy, and the four Python files it changes compile.
- The concatenation `d25-tools.patch` + `tools-readme-release.patch` is still byte-identical to `release-gate12.patch`. The new SHA-256s are `e6576c63…4bbc` (d25-tools), `59d44598ef31a10e51583dd8694defe726f5f9a9b4616fa71c820c764b532dad` (tools-readme-release) and `727c9cac3fb300164cb9f152da5f87b01a4772d5da4e69907f8a1ae36eac63ed` (release-gate12). The `index` lines of the git patch still carry the 25 September blob ids. `git apply` uses them only for a three-way fallback.
- The test fixture's sheet title `"v1.14 export"` in `test_import_results.py` was left unchanged. It is a string literal, not a comment, and any title works.
