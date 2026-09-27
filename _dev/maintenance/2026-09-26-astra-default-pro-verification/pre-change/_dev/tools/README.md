# Pipeline tools

Run commands from the repository root. Read [AGENTS.md](../../AGENTS.md) and [the current handoff](../HANDOFF.md) first. Extractors must see only their isolated inputs; run the checker after extraction, outside that sandbox. Extractions, model experiments and workbook revisions require Austin's explicit instruction. These examples do not authorize a run.

## Environment

Python 3.10+ with the dependencies pinned in [requirements.txt](requirements.txt): openpyxl, Beautiful Soup and lxml. Change a pin deliberately; a run records the installed versions in `metadata.json` (`library_versions`). Tests use `unittest` and mocks; no provider credentials or network are required.

The isolated runner requires Linux bubblewrap and a standalone Codex or native Claude installation. It resolves the executables on PATH; `SEC_CODEX_BIN` and `SEC_CLAUDE_BIN` can select explicit binaries. A Codex override must resolve to a standalone release's `bin/codex`, not a shell or Node wrapper.

Opus runs authenticate with a long-lived subscription token. Create it once with `claude setup-token` and save it to `~/.config/sec-extraction/claude-oauth-token`, readable only by you (`chmod 600`); `SEC_CLAUDE_OAUTH_TOKEN_FILE` selects another file. Each invocation receives the token through an inherited pipe (`CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR`), so it never appears in a command line, the sandbox environment or the run directory. The host's own Claude login is deliberately not shared: a sandboxed CLI that refreshed that login would rotate its refresh token, which a read-only sandbox cannot write back, and so log the host out. Codex credentials are bound read-only: the host's `~/.codex/auth.json`, or the file `SEC_CODEX_AUTH_FILE` names (the cockpit names each user's own login). A Sol-transport run refuses a login within 7 hours of expiry, because a refresh inside the sandbox could not be written back. Mutable provider state and the sandbox's scratch home and `/tmp` are temporary and deleted when the worker exits.

## Mechanical checking

```bash
python3 _dev/tools/check_lean.py --workbook extraction/<deal>.xlsx --filing raw_filing/<filing>.htm --output _dev/runs/<deal>/check.json
```

The checker is offline. It validates workbook structure, dates, labels, links, quotation occurrence and agreement between columns of the same row (an exact-day When against its three date cells; an inferred exit's reason). It does not establish the truth of classifications or live-bidder arithmetic. Required long Notes and documented uncertain Counts are review warnings. The ledger header selects the rules: a `Stock %` column marks a v1.14 (draft) workbook, whose bid-term columns get their value lists and the E12 consistency rules (Financing Contingent requires Heavy; None requires Complete diligence and committed or unneeded financing); any other header is checked as v1.13.2, unchanged. The report's `ledger_schema` says which applied.

## Isolated runs

```bash
python3 _dev/tools/sandbox/run_model.py prepare --provider opus --run-dir _dev/runs/<run> --deal <deal> --filing <bare-filing-name>.htm [--effort <level>] [--model <model>] [--timeout-minutes <n>] [--instruction <file>]
python3 _dev/tools/sandbox/run_model.py launch --provider opus --run-dir _dev/runs/<run>
python3 _dev/tools/sandbox/run_model.py status --runs-dir _dev/runs
```

The extraction engine is **Claude Opus 5.5** (`claude-opus-5-5`). Its effort level is chosen at prepare (`low`, `medium`, `high`, `xhigh` or `max`) and recorded in `metadata.json` with the model and the wall-clock limit (default 90 minutes; `--timeout-minutes` takes 10–360). The provider command is built from those recorded values, and launch refuses metadata whose model or effort is not allowed. Without `--effort` the runner uses `DEFAULT_EFFORT` in `run_model.py`: `medium`. The [22 September effort sweep](../reviews/2026-09-22-opus55-sol6-sweep/REPORT.md) found no reliable gain from high over medium, on three deals with one run each. Opus 5.5's own API default is `medium`, and its levels do not match Opus 5's, so always record the level used. `sol` remains an implemented transport, not an approved default; an alternative-model run requires Austin's explicit command. `sol` runs GPT-6-Sol (`gpt-6-sol`, or `gpt-5.6-sol`) through Codex at effort `low` to `max`. The `ultra` level is not offered, because it delegates to subagents automatically. By default `codex exec` offers the account's ChatGPT app connectors (mail, GitLab, site deploys, a remote shell), web browsing, image generation and subagents. Every Sol run switches those off (`CODEX_DISABLED_FEATURES`, plus `web_search="disabled"`), leaving shell commands and file patches. Code mode stays on because GPT-6-Sol calls every tool through it. Codex's login is bound read-only, and a sandboxed refresh would rotate its refresh token and log the host out, so preflight refuses a Sol run when the host Codex access token has less than seven hours left. `prepare --instruction <path>` supplies a candidate instruction in place of the working one. The runner rejects a provider that differs from its prepared metadata. Prepare does not call a model; launch does. Only one instruction and filing enter a blind extraction.

Launch and worker startup verify the prepared instruction, filing and prompt against their recorded SHA-256 hashes before starting a provider. A revision also verifies its starting workbook and findings report. Changed or missing inputs require a newly prepared run directory. Older extraction metadata with the required hashes remains usable; older revision metadata without a findings-report hash must be prepared again. Status inspection does not recheck the starting workbook, since a revision legitimately changes it.

Revision is a separate mode: pass both `--revise-from <workbook>` and `--report <findings.md>` to prepare. This deliberately exposes that workbook and report in addition to the instruction and filing. Never use a revision as a blind extraction. The completed revision experiment is at `407a6e4:_dev/revision_loop/RESULTS.md`.

Inside the sandbox every Opus run sees only the Bash, Read and Write tools (`--tools`), and sets three Claude Code variables (`CLAUDE_ENV` in the runner, also recorded in `command.json`). `CLAUDE_CODE_DISABLE_REFUSAL_FALLBACK=1` makes a safety-classifier refusal fail the run rather than silently continue on another model. `CLAUDE_CODE_PROMPT_CACHE_TTL=1h` holds the cache lifetime at the subscription default, so costs stay comparable. `CLAUDE_CODE_SILENT_TURN_REMINDER_TURNS=1000000` stops the "user hasn't heard from you" reminder, since no one reads a sandboxed run as it works. Opus 5.5 can end an unattended turn with a progress report before its work is done. If a run ends cleanly while its deliverable is still owed, the worker resumes the same session with a short continuation message naming it, at most twice (`MAX_CONTINUATIONS`). For an extraction the deliverable is a readable four-sheet workbook; for a revision it is `revision_notes.md`. The sandbox's scratch home and `/tmp` are kept for all of a run's invocations, so the resumed session still has the working files it made. The message carries no findings or other information. The session lives only in the temporary provider state. `command.json` records the first command, every continuation command, the runner's hash at worker start and the provider binary's hash. Pin the Claude Code binary for comparisons with `SEC_CLAUDE_BIN`, because the installed CLI updates itself.

When a run ends, `status.json` records its tokens and cost (`usage`), read from the provider's event log; Codex reports tokens but no cost. For Opus, usage is summed over the first invocation and any continuations, and cost is the session's cumulative figure. `status.json` also holds a `provider` summary: served models, Claude Code version, turns, API time, thinking tokens, cache writes by lifetime, refusal and stop reasons, permission denials and subagents. `provider-results.json` keeps the CLI's result events verbatim, including the agent's final report. New run directories under `_dev/runs/` are ignored. Record the results you need, then delete the run. Full event logs from older experiments remain in their recorded git snapshots.

For new runs, `state: completed` means all of the following hold:
- the provider exited with code zero;
- for Opus, the CLI reported success without a refusal, and the only model that served the run was the prepared one;
- the expected workbook can be read, including its worksheets, and has exactly the four sheets the instruction requires, in order;
- for a revision, `revision_notes.md` was written.

`--provider opus` is the Claude Code transport (models `claude-opus-5-5`, the default, and `claude-fable-5-1`); `--provider sol` is the Codex transport (`gpt-6-sol`, the default, and `gpt-6-astra`). Efforts are `low` to `max` for both. Fable 5.1's safeguard block ("…safeguards flagged this message…") counts as `provider_refusal`. A Codex run that stops with "You've hit your usage limit" is `usage_limit`, with the provider's sentence in `usage_limit_message`.

Otherwise the run is `failed`, with one of these `failure_reason`s: `provider_refusal`, `provider_exit`, `provider_error`, `model_mismatch`, `workbook_missing`, `workbook_unreadable`, `workbook_incomplete` or `revision_notes_missing`. A timeout yields `timed_out`. Worker startup errors also leave a failed status. The worker exits nonzero on failure, while `launch` only reports successful dispatch: inspect `status` for the outcome. Older saved statuses keep their original meaning. Workbook readability is not a mechanical-checker pass or substantive acceptance; both remain separate steps.

The cockpit importer (`cockpit/import_results.py`) builds the catalog with one version per deal: the Opus 5.5 medium extraction in `extraction/<deal>.xlsx`, confirmed from the receipts in `_dev/reviews/2026-09-22-opus55-reextraction/`, plus the Datalink F9 and Mac-Gray R01 case-level decisions. `cockpit/verify_catalog.py` is the read-only live check of that catalog; it writes its result to the same packet.

## Cockpit worker

`cockpit/worker.py` runs as the user service `ledger-worker.service` (unit in `~/.config/systemd/user/`, `KillMode=process`). It takes jobs the cockpit writes to its SQLite database: Claude sign-ins, which drive `claude setup-token` in a pseudo-terminal; ChatGPT sign-ins, which run `codex login --device-auth` with a fresh `CODEX_HOME` that becomes `~/.config/sec-extraction/users/<user>/codex/` (0700) on approval; and extractions, which call this runner's `prepare` (with the engine's provider and model and `--instruction` pointing at the frozen text in `_dev/cockpit/state/instructions/<sha256>.md`) and `worker` with the starting user's credential (`SEC_CLAUDE_OAUTH_TOKEN_FILE` pointing to `~/.config/sec-extraction/users/<user>/claude-oauth-token`, mode 0600, or `SEC_CODEX_AUTH_FILE` pointing to that user's `codex/auth.json`). When a ChatGPT login has under 24 hours left and its owner has no GPT run going, the worker renews it outside the sandbox with one short `codex exec` (GPT-6-Sol, low effort) under that user's writable `CODEX_HOME`, at most hourly; a queued GPT run within 7 hours of expiry waits for that and fails `login_expired` if it does not renew. It runs the checker outside the sandbox and imports the workbook and receipts into `_dev/cockpit/state/versions/<deal>/<version>/`; failed runs keep their receipts in `_dev/cockpit/state/jobs/<job>/`. The run folder under `_dev/runs/` is deleted either way. The runner's `worker` stops on SIGTERM with `state: cancelled`, records the last Claude rate-limit report as `plan_usage`, and names a rejected plan limit `usage_limit` with `usage_limit_resets_at`. Runner processes outlive a worker restart; the restarted worker reattaches by pid or finishes them from their `status.json`.

```bash
systemctl --user restart ledger-worker
journalctl --user -u ledger-worker -f
```

## Backups and restore

`cockpit/backup.py` copies the cockpit's state. The working-state database is the only copy of working revisions and comments.

```bash
python3 _dev/tools/cockpit/backup.py create                      # -> ~/backups/ledger-cockpit/<YYYYMMDD-HHMMSS>Z/
python3 _dev/tools/cockpit/backup.py rehearse                    # back up, restore to a temporary root, compare
python3 _dev/tools/cockpit/backup.py restore <backup> --state <dir> [--replace]
```

- **What `create` copies:**
  - The database, with SQLite's online backup API, integrity-checked and stored in rollback-journal mode.
  - `filings/`, `instructions/`, `versions/` and `jobs/`.
  - It leaves out `lookups/` (EDGAR caches), `worker.lock` and credentials (`~/.config/sec-extraction/users/`, never backed up; users reconnect after a restore).
- **`manifest.json`:**
  - every file's size and SHA-256;
  - the database's hash and its per-table row counts;
  - the git HEAD;
  - a per-deal summary: the working revision, a hash of the working sheets, and thread and comment counts and hashes.
- **Writing and pruning:**
  - A backup is written under `.partial-*` and renamed when complete.
  - Pruning keeps 14 days (`--keep-days`) and always the newest, and touches nothing else in the folder.
- **Nightly job:**
  - `ledger-backup.timer` runs `ledger-backup.service` at 03:30 UTC (`Persistent=true`, so a missed night runs at the next boot).
  - The unit files are in `cockpit/deploy/`; install them with `cp _dev/tools/cockpit/deploy/ledger-backup.* ~/.config/systemd/user/ && systemctl --user daemon-reload && systemctl --user enable --now ledger-backup.timer`.
- **`rehearse`** is the restore check. It:
  1. backs up the live state;
  2. restores the backup into a temporary repository root that links the checkout's catalog, filings and instruction;
  3. compares the two through the cockpit's own data layer: working copies, revision history, comments with their edits, versions, added and hidden deals, and instructions. It also compares every database table row by row.

  It prints a JSON report and exits 0 only with no differences.
- **`restore`:**
  - It checks every hash before writing anything.
  - It restores into a new or empty directory; `--replace` moves an existing one aside to `<dir>.before-restore-<stamp>`.
  - It refuses the live `_dev/cockpit/state/` while `ledger-cockpit` or `ledger-worker` is running.
  - To replace the live state:
    1. stop both services;
    2. run `restore <backup> --state _dev/cockpit/state --replace`;
    3. start both services.

If `systemctl --user` fails with "Failed to connect to user scope bus via local transport", the user manager's private socket file has been replaced (on 23 September this happened while unit files were being checked with `systemd-analyze`). The manager is still reachable over D-Bus. Re-execute it, and running services carry on:

```bash
busctl --user call org.freedesktop.systemd1 /org/freedesktop/systemd1 org.freedesktop.systemd1.Manager Reexecute
```

## Export to the repository

`cockpit/export_repo.py` copies a cockpit version into the repository for a commit Austin requests. It is an admin script, not a button. It never commits, and it never calls a model or the network.

```bash
python3 _dev/tools/cockpit/export_repo.py instruction v1.14                     # dry run: target, current hash -> new hash
python3 _dev/tools/cockpit/export_repo.py instruction v1.14 --write             # writes SEC_Deal_Ledger_Extraction_Instruction.md
python3 _dev/tools/cockpit/export_repo.py deal <slug> --version <id>|working [--write]
```

- **Instructions:** only published versions can be exported, and the stored text must match its content hash.
- **Deals:**
  - A deal export writes `extraction/<slug>.xlsx`, using the same bytes as the cockpit's Excel download.
  - For a deal added in the cockpit, it also writes the filing to `raw_filing/` and adds or updates its `MANIFEST.csv` row.
  - It refuses any path that `catalog.json` names as an immutable original, so in practice only added deals can be exported. Changing the catalog is a separate, requested edit.
  - Once an exported added deal is committed, the cockpit reads its filing from `raw_filing/` like the original nine.
- **Without `--write`** it is a dry run that writes nothing.

## Effort sweeps

`effort_sweep.py` runs the same filings under several arms through the isolated runner. An arm is `provider:model:effort`. It requires Austin's authorization, as any extraction does.

```bash
python3 _dev/tools/effort_sweep.py plan --packet _dev/reviews/<date>-<name> --deals <deal,...> --arms opus:claude-opus-5-5:medium sol:gpt-6-sol:high --replicates 2 --seed <n> [--timeout-minutes 120]
SEC_CLAUDE_BIN=<pinned claude> SEC_CODEX_BIN=<pinned codex> python3 _dev/tools/effort_sweep.py run --packet _dev/reviews/<date>-<name> --concurrency 3 [--only <cell ids, arms, deals or providers>]
python3 _dev/tools/effort_sweep.py summarize --packet _dev/reviews/<date>-<name>
```

`plan` writes `plan.json`. Each replicate block covers every deal and arm pair once, in a seeded random order, so the arms are interleaved over the same period rather than run one after another.

`run` works as follows:
- On its first call it records the hashes of each provider's binary, the instruction and the runner in `pin.json`. Later calls refuse any difference, it stops before a launch if any of them has changed, and every run it starts uses the pinned binaries.
- It prepares and launches each cell as an ordinary run, at most `--concurrency` at a time. It refuses a run folder whose metadata does not match its planned cell.
- It can be restarted: recorded cells are skipped, and cells an interrupted driver had already launched are counted first.
- For each finished cell it copies the receipts, the workbook and the compressed event log into `runs/<cell>/`. It runs the checker outside the sandbox and lists any shell command that looks able to reach the network, and any web, connector or subagent tool use, for both providers.
- After three provider or worker failures in a row (a usage limit, an outage, expired credentials) it starts no new cells. `--retry-failed` moves such failures aside under `retried/` and runs those cells again.

`summarize` reports each Claude run's list-price cost, repriced by one formula. A Claude run killed at its time limit is costed from its per-message usage and marked partial. Codex reports tokens but no cost, so Sol runs carry tokens and time only. It also reports tokens, turns, time, checker counts and ledger size. For each arm it adds:
- total spend and spend per completed workbook;
- agreement between replicates;
- the mean graded score, when the packet has a `grades.json`.

A run that does not match its planned cell or the pin is listed but never averaged. Delete the run folders once their cells are recorded.

## Review helpers and filing inputs

```bash
python3 _dev/tools/findings_text.py <check.json> <findings.md>
python3 _dev/tools/diff_workbooks.py <before.xlsx> <after.xlsx>
python3 _dev/tools/fetch_filing.py --list <name>
```

Findings distinguish mechanical errors from review warnings and optional model judgments. Workbook diffs preserve cell types, so a number changed into text is visible, and detect added trailing columns.

`fetch_filing.py <deal>` fetches a filing from EDGAR. An existing filing must match its recorded local size/hash; `--verify` contacts EDGAR, while `--force` explicitly replaces a file. Fetch and verification select the same document type: for SC TO-T, the offer-to-purchase exhibit `EX-99.(A)(1)(A)`, rather than the cover form. Verification also requires the manifest's recorded document filename when present; legacy rows without one require an unambiguous match by type. Writes are atomic per file. Set `SEC_USER_AGENT` for another operator; the default identifies Austin. Seed rows marked for review remain unsupported. The cockpit's Add deal uses the same module (`submission_link`, `parse_submission`, `default_document`, `document_bytes`) and so saves identical bytes.

`make_seed.py` deliberately rebuilds `ref/seed.csv` from Alex's workbook using identifying fields only. Do not run it merely to inspect or tidy the repo. Reference data and canonical workbooks are research inputs, not disposable development output.

## Offline validation

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s _dev/tools -p 'test_*.py'
```

The tests use synthetic fixtures. Runner tests construct commands and mock execution; they never launch an extractor.

## Review cockpit

```bash
python3 _dev/tools/cockpit/server.py            # http://127.0.0.1:8778 (or $COCKPIT_PORT)
python3 _dev/tools/cockpit/server.py --port 8791  # a second copy while the service holds 8778
```

The second command changes only the port: it reads the same catalog and working-state database from this checkout. Use a synthetic fixture or a separate checkout for disposable edit tests.

The editable cockpit uses the allowlisted version catalog at `_dev/cockpit/catalog.json`, displaying each workbook beside its filing (`raw_filing/`, matched through `MANIFEST.csv`). The built React interface supports Ledger, Rounds, Questions and Deal facts editing, event insertion/deletion/movement, source navigation, findings, changes, history/restore and Excel export. Preserved source versions are immutable; saved working revisions live in the ignored `_dev/cockpit/state/workspace.sqlite3`. Preserve that database across deployments. Deals added in the app (phase 3) are rows in its `added_deals` table with their filings in `_dev/cockpit/state/filings/<slug>/`; the worker fetches them from EDGAR as `lookup` jobs (cached 24 hours in `state/lookups/`), and passes the folder to `run_model.py prepare --filing-dir`, which accepts only `raw_filing/` or such a folder. The server reads only the seed's identifying columns. Viewing a deal does not create a revision. The server binds 127.0.0.1, makes no network or model calls, runs the mechanical checker in-process and never reads `ref/`. If `dist/index.html` is missing, page routes return HTTP 503 naming the missing build; there is no fallback interface. See the [review guide](../cockpit/README.md) and [build contract](../COCKPIT_BUILD.md).

Quotes are located with the checker's own parsing and both of its filing renderings, so every quote the checker accepts is highlighted. A "page hint" (a quote found on a different printed page from the one cited) is a cockpit hint, not a checker finding, and is shown only when a filing's page numbers were detected reliably. A workbook or filing that cannot be read is listed as unreadable (HTTP 409 for that deal) without hiding the other deals.

The editable build was deployed on 22 September 2026 at https://lines.dealextract.org. The systemd user unit `ledger-cockpit.service` runs the server from the working tree on 127.0.0.1:8778, and `cloudflared.service` publishes that port behind the existing Cloudflare Access route for Austin and Alex. Public writes require a configured trusted identity, matching Origin and a session CSRF token. Unknown users do not default to Austin. Direct loopback development uses the explicit `local` actor. The service drop-in sets `COCKPIT_PUBLIC_ORIGIN=https://lines.dealextract.org`; do not expose the loopback development server directly to the network.

The frontend source is in `_dev/tools/cockpit/frontend/src/`: `main.jsx` (shell and routing), `Overview.jsx`, `Records.jsx`, `Review.jsx`, `ui.jsx` (shared controls), `theme.js` (Fluent theme mirroring the CSS tokens), `Filing.jsx`, `SplitPane.jsx` (draggable dividers with keyboard control and browser-local size memory) and `TabScroller.jsx`, with self-hosted fonts in `src/fonts/`. Vite bundles the fonts and favicon into hashed files under `dist/assets/`, the only static path the server serves besides the index. The "working papers" redesign was built into `dist/` and deployed on 23 September; its brief, audit and progress log are in `_dev/maintenance/2026-09-22-cockpit-redesign/`. The public route was checked only up to its Cloudflare Access redirect.

Never run `npm run build` against the live checkout. The service serves `dist/` straight from this working tree and reads files per request, and the build empties `../dist` first (`emptyOutDir`), so the live site breaks while it builds and changes the moment it finishes. Build beside it and swap:

```bash
cd _dev/tools/cockpit/frontend && npm ci
npx vite build --outDir ../dist.new --emptyOutDir
cd .. && mv dist dist.old && mv dist.new dist
systemctl --user restart ledger-cockpit.service   # also needed after any Python cockpit or checker change
```

Remove `dist.old` once the site checks out. After a restart, verify `/api/session`, `/api/deals` and `/api/deal/<deal>?version=working`, compare checker findings with a fresh run, and preserve source hashes and working state. Catalog updates are read on later requests; changing a default base must not silently replace a saved working revision. Logs: `journalctl _SYSTEMD_USER_UNIT=ledger-cockpit.service` (or `cloudflared.service`). Verification evidence is linked from [HANDOFF.md](../HANDOFF.md).

Acceptance suites run against a synthetic fixture (`acceptance/serve_fixture.py`; `--two-users` makes it take identities from the Cloudflare Access email header, for `test_trace.mjs`; `--runs` adds the real worker loop driving the fake runner and fake `claude` from `test_cockpit_runs.py` and the fake `codex` from `test_cockpit_phase4.py` (its sign-in waits for `<root>/codex-flag`; the fixture prints `root`), for `test_runs.mjs` and `test_instructions.mjs`; `--deals` adds a two-row seed and a stubbed EDGAR, for `test_deals.mjs`) on a private port and a private headless Chrome; they never touch production workbooks, the catalog, working state or the live service. Run from the repository root:

```bash
COCKPIT_BROWSER_EVIDENCE=/tmp/cockpit-browser node _dev/tools/cockpit/acceptance/test_browser.mjs
COCKPIT_RESIZE_EVIDENCE=/tmp/cockpit-resize node _dev/tools/cockpit/acceptance/test_resize.mjs
COCKPIT_RESPONSIVE_EVIDENCE=/tmp/cockpit-responsive node _dev/tools/cockpit/acceptance/test_responsive.mjs
COCKPIT_TRACE_EVIDENCE=/tmp/cockpit-trace node _dev/tools/cockpit/acceptance/test_trace.mjs
COCKPIT_RUNS_EVIDENCE=/tmp/cockpit-runs node _dev/tools/cockpit/acceptance/test_runs.mjs
COCKPIT_DEALS_EVIDENCE=/tmp/cockpit-deals node _dev/tools/cockpit/acceptance/test_deals.mjs
COCKPIT_INSTRUCTIONS_EVIDENCE=/tmp/cockpit-instructions node _dev/tools/cockpit/acceptance/test_instructions.mjs
python3 -m pytest -q _dev/tools/cockpit/acceptance/test_http.py
(cd _dev/tools/cockpit/frontend && npx vitest run)
```

The browser suites use the repository `dist/` read-only; set `COCKPIT_TEST_DIST` to test a staged build such as `dist.new` before swapping. Only `test_browser.mjs`, `test_resize.mjs`, `test_responsive.mjs`, `test_deals.mjs` and `test_instructions.mjs` honour it; `test_runs.mjs` and `test_trace.mjs` always use `dist/`, so run them again after the swap. Screenshots go to `/tmp/cockpit-*-acceptance` unless a `COCKPIT_*_EVIDENCE` variable says otherwise; keep them outside the repository. `test_http.py` needs `pytest` and `requests`, which are not in `requirements.txt`.
