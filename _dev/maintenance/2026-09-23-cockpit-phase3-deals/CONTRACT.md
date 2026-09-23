# Phase 3 (add deals) build contract

Implements §7 of [the app spec](../../COCKPIT_APP_SPEC.md): add a deal from `ref/seed.csv` or a pasted EDGAR link, choose the document, save the filing, and optionally go straight to an extraction. Phase 2's runs, versions and base rules apply unchanged to added deals. Engines other than Opus 5.5 and instruction editing stay in phase 4; hiding deals is left for phase 5.

Claude-only build (Austin, 23 September): Opus 5.5 builds and integrates. Do not read `ref/` beyond the seed's identifying columns, `_dev/reviews/` or `_dev/side-notes/`.

## Research guarantees (unchanged)

- A filing is saved byte for byte, cut from EDGAR's complete submission text file exactly as `fetch_filing.py` does, with SEC's named user agent and at most 4 requests a second.
- The server reads only the seed's `deal`, `target_name`, `form_type`, `date_filed`, `index_url` and `status` columns. No other `ref/` file is read by the app.
- A run of an added deal sees one instruction and that deal's one filing in the same sandbox.
- HTTP requests make no network calls. The EDGAR fetch is a worker job.

## Fetch (`_dev/tools/fetch_filing.py`, refactored)

- `submission_link(url)` accepts, on `https://www.sec.gov/Archives/edgar/data/<cik>/…`: a filing index (`…-index.htm(l)`), a complete submission (`<accession>.txt`), or a document in the accession folder (`<cik>/<18 digits>/<file>`). It returns the submission `.txt` link and, for a document link, that document's name. Anything else raises `FetchError`.
- `parse_submission(bytes)` returns the header (submission type, filed date, subject company and filer names) and each document's type, filename, description, size, whether it is HTML, and whether it contains a "Background of the Merger/Offer/Transaction" heading.
- `default_document(documents, form)` applies the existing rule: DEFM14A and PREM14A take the document whose type equals the form; SC TO-T takes `EX-99.(A)(1)(A)`; otherwise no preselection. Exactly one match is required.
- `document_bytes(submission, filename)` returns the saved bytes (`<DOCUMENT>…</DOCUMENT>` block plus a newline), as today.
- `main_document()` and the CLI keep their behaviour and tests.

## Storage

Same SQLite file, created idempotently:

```sql
CREATE TABLE IF NOT EXISTS added_deals (
  slug TEXT PRIMARY KEY, name TEXT NOT NULL, form_type TEXT NOT NULL, date_filed TEXT NOT NULL,
  file TEXT NOT NULL,                 -- <slug>_<date>_<FORM without spaces>.htm
  source_kind TEXT NOT NULL,          -- 'seed' | 'link'
  seed_deal TEXT, index_url TEXT, source_url TEXT NOT NULL, document TEXT NOT NULL,
  fetched_utc TEXT NOT NULL, bytes INTEGER NOT NULL, sha256 TEXT NOT NULL,
  added_by TEXT NOT NULL, added_at TEXT NOT NULL);
```

- Filings: `_dev/cockpit/state/filings/<slug>/<file>`, written atomically, never replaced.
- Lookups are `jobs` rows with `kind='lookup'` (`queued → running → completed | failed`). The fetched submission is cached at `_dev/cockpit/state/lookups/<job-id>.txt` with its SHA-256 in the job result, so the saved document is cut from the bytes the user chose from. Cached lookups are deleted after 24 hours.

## Deals in the cockpit

- A deal is a catalog deal or an added deal. Slugs must be unique across both, the seed's other rows excluded; a slug in use is refused (409).
- An added deal's versions are its imported runs. Its `default_base` is its oldest imported version, so the first finished run becomes the working copy's base automatically (spec §13.4). Later runs never move it; rebase does, as in phase 2.
- An added deal with no version is **pending**. `/api/deal/<slug>` returns `pending: true`, the filing header, empty sheets, no versions and a read-only workspace. Edit, export, history, changes and compare refuse it with 409 "no extraction yet". Comments are not offered until there is a working copy.
- `/api/deals` lists added deals after catalog deals; a pending one shows `pending: true`, the form and date, and any active run.
- Adding a deal writes an activity item `deal_added` ("Added from the seed" or "Added from a pasted link").

## Runner

`run_model.py prepare` gains `--filing-dir`, default `raw_filing/`. It must resolve to `raw_filing/` or a folder directly under `_dev/cockpit/state/filings/`; anything else is refused. The worker passes the deal's filing folder.

## API

- `GET /api/seed?q=<text>` → up to 25 seed rows matching `deal` or `target_name` (case-insensitive), each with `in_cockpit`. An empty query returns nothing.
- `POST /api/deals` (CSRF, known users only):
  - `{action: "lookup", url, seed_deal?}` → `{lookup: <job>}`. `url` is validated by `submission_link`; `seed_deal` must be a seed row and fixes the suggested slug, name, form and date.
  - `{action: "add", lookup_id, document, slug, name}` → `{slug}`. Requires a completed lookup under 24 hours old by any user, an HTML document in it, a valid unused slug and a name of 1–120 characters.
- `GET /api/lookup/<job-id>` → the lookup: state, error, and when complete `{header, documents, preselected, suggested: {slug, name, form_type, date_filed}, source_url, index_url, warnings}`.

## Frontend

- **Add deal** on the overview (signed-in users) opens a dialog with **Search the seed** and **Paste a link**.
- Seed search is type-ahead. Rows already in the cockpit say "Open". Rows marked `review` show their reason; one with a usable index link is looked up without preselection, and one without asks for a pasted link.
- After a lookup: documents as a choice list (type, name, description, size), the preselected one checked, a warning (not a block) on a document without a Background heading, editable name and slug, then **Add** or **Add and extract**. The latter opens the deal and its Extract dialog.
- A pending deal page shows the filing, "No extraction yet", the Extract button, the run badge and the Runs list. When its first run finishes, the page reloads into the normal workspace.

## Tests

- Python: `submission_link`, `parse_submission`, `default_document`; seed search columns; lookup through the worker with a stubbed `get`; add (file bytes, manifest fields, activity, slug and document refusals); pending payload and refusals; extraction of an added deal through the fake runner with `--filing-dir`, and automatic base. Runner `--filing-dir` restriction.
- Browser: a new `test_deals.mjs` on the fixture with the fake worker and a stubbed EDGAR, covering seed add, pasted-link add with document choice, and Add and extract to an imported version.
- All earlier suites stay green.

## Acceptance (spec §12)

One seed deal and one pasted-link deal added and extracted end to end. Adding fetches from EDGAR; each extraction is a real model run and needs Austin's go-ahead.
