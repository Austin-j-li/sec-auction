# Phase 3 (add deals): build record

Contract: [CONTRACT.md](CONTRACT.md). Built by Opus 5.5 on 23 September 2026 (Austin: "commit and run phase 3 now", after phase 2 was committed as `c28f150`). Deployed at 16:24 UTC; committed at Austin's request (commit "Cockpit phase 3: add deals from the seed or an EDGAR link").

## What was built

- **Fetcher** (`fetch_filing.py`): `submission_link`, `parse_submission`, `default_document` and `document_bytes`; `main_document` now uses the shared document pattern. The CLI is unchanged. Checked against EDGAR: for PetSmart (DEFM14A) and Synacor (SC TO-T), the parser picks the recorded document, and the cut bytes match `raw_filing/MANIFEST.csv`'s SHA-256 exactly.
- **Runner** (`run_model.py prepare --filing-dir`): default `raw_filing/`; otherwise only a deal folder directly under `_dev/cockpit/state/filings/`.
- **Backend** (`cockpit/deals.py`, new): seed search over the six identifying columns, lookup jobs, and `add` (local only: cut from the cached submission, atomic write, `added_deals` row and `deal_added` activity in one transaction, with the folder removed if anything fails). `workspace.item` serves added deals, and their oldest imported version is `default_base`. A deal with no version returns a pending payload; edit, export, changes and comments refuse it with 409. `data.Cockpit` merges added deals into the manifest and deal list.
- **Worker**: runs lookups one at a time in a thread, fails interrupted lookups on restart, prunes cached submissions after 24 hours, and passes `--filing-dir` for every run.
- **Server**: `GET /api/seed`, `GET /api/lookup/<id>`, `POST /api/deals` (CSRF and a known user, like other writes).
- **Frontend**: `AddDeal.jsx` (seed search, paste link, document choice with Background warning, names, Add / Add and extract), `deals.js` helpers, an **Add deal** button on the overview, pending rows, and a pending deal page (filing, "No extraction yet", Extract, run badge, Runs list) that reloads into the workspace when the first run finishes.

## Decisions made in the build

- Form types become file-name-safe (`SC TO-T/A` → `SCTO-T-A`), found in self-review before deploy.
- Suggested names drop the seed's suffix words (`MAC-GRAY CORP` → `Mac-Gray`); both names stay editable. A pasted link's short name gets the filing year when the plain one is taken.
- Seed rows marked `review` with a usable link are looked up without preselection; those without one ask for a pasted link, and the seed row still supplies the names.
- Hiding deals (spec §13.5) is left for phase 5.

## Tests

- Python: 174 pass (`python3 -m pytest -q _dev/tools`), including the new `test_cockpit_deals.py` (9), link and parse tests in `test_fetch_filing.py`, and the runner `--filing-dir` test. The fake runner now asserts the filing is in `--filing-dir`.
- `test_http.py`: 11 pass. Vitest: 31 pass (new `deals.test.js`).
- Browser: `test_browser`, `test_resize`, `test_responsive` and the new `test_deals.mjs` (seed add, review row, refused link, pasted link with document choice, Add and extract to an imported base, Alex's feed) passed on the staged build. `test_runs` and `test_trace` passed on the deployed `dist/` after the swap, since they do not honour `COCKPIT_TEST_DIST`. (The phase 2 run-badge note said all five suites ran on the staged build; those two had in fact used the then-live `dist/`.)
- Live, after the restart: nine deals listed and unchanged (PetSmart working copy revision 0, 1 error / 22 warnings as before); seed search returns only identifying columns; a real EDGAR lookup of `8point3-energy-partners` completed with `d553814ddefm14a.htm` preselected. No deal was added.

## Not yet done

> **Status, 26 September 2026:** this list is as of 23 September. The [development handoff](../../HANDOFF.md) tracks which acceptance items remain.

- **Acceptance (spec §12):** one seed deal and one pasted-link deal added and extracted end to end. Adding fetches from EDGAR; each extraction is a real Opus 5.5 run and needs Austin's go-ahead.
