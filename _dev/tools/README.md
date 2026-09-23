# Pipeline tools

Run commands from the repository root. Read [AGENTS.md](../../AGENTS.md) and [the current handoff](../HANDOFF.md) first. Extractors must see only their isolated inputs; run the checker after extraction, outside that sandbox. Extractions, model experiments and workbook revisions require Austin's explicit instruction. These examples do not authorize a run.

## Environment

Python 3.10+ with the dependencies pinned in [requirements.txt](requirements.txt): openpyxl, Beautiful Soup and lxml. Change a pin deliberately; a run records the installed versions in `metadata.json` (`library_versions`). Tests use `unittest` and mocks; no provider credentials or network are required.

The isolated runner requires Linux bubblewrap and a standalone Codex or native Claude installation. It resolves the executables on PATH; `SEC_CODEX_BIN` and `SEC_CLAUDE_BIN` can select explicit binaries. A Codex override must resolve to a standalone release's `bin/codex`, not a shell or Node wrapper.

Opus runs authenticate with a long-lived subscription token. Create it once with `claude setup-token` and save it to `~/.config/sec-extraction/claude-oauth-token`, readable only by you (`chmod 600`); `SEC_CLAUDE_OAUTH_TOKEN_FILE` selects another file. Each invocation receives the token through an inherited pipe (`CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR`), so it never appears in a command line, the sandbox environment or the run directory. The host's own Claude login is deliberately not shared: a sandboxed CLI that refreshed that login would rotate its refresh token, which a read-only sandbox cannot write back, and so log the host out. Codex and DeepSeek credentials are bound read-only from the host. Mutable provider state and the sandbox's scratch home and `/tmp` are temporary and deleted when the worker exits.

## Mechanical checking

```bash
python3 _dev/tools/check_lean.py --workbook extraction/<deal>.xlsx --filing raw_filing/<filing>.htm --output _dev/runs/<deal>/check.json
```

The checker is offline. It validates workbook structure, dates, labels, links, quotation occurrence and agreement between columns of the same row (an exact-day When against its three date cells; an inferred exit's reason). It does not establish the truth of classifications or live-bidder arithmetic. Required long Notes and documented uncertain Counts are review warnings.

## Isolated runs

```bash
python3 _dev/tools/sandbox/run_model.py prepare --provider opus --run-dir _dev/runs/<run> --deal <deal> --filing <bare-filing-name>.htm [--effort <level>] [--model <model>] [--timeout-minutes <n>]
python3 _dev/tools/sandbox/run_model.py launch --provider opus --run-dir _dev/runs/<run>
python3 _dev/tools/sandbox/run_model.py status --runs-dir _dev/runs
```

The extraction engine is **Claude Opus 5.5** (`claude-opus-5-5`). Its effort level is chosen at prepare (`low`, `medium`, `high`, `xhigh` or `max`) and recorded in `metadata.json` with the model and the wall-clock limit (default 90 minutes; `--timeout-minutes` takes 10–360). The provider command is built from those recorded values, and launch refuses metadata whose model or effort is not allowed. Without `--effort` the runner uses `DEFAULT_EFFORT` in `run_model.py`: `medium`. The [22 September effort sweep](../reviews/2026-09-22-opus55-sol6-sweep/REPORT.md) found no reliable gain from high over medium, on three deals with one run each. Opus 5.5's own API default is `medium`, and its levels do not match Opus 5's, so always record the level used. `sol` and `deepseek` remain implemented transports, not approved defaults; an alternative-model run requires Austin's explicit command. `sol` runs GPT-6-Sol (`gpt-6-sol`, or `gpt-5.6-sol`) through Codex at effort `low` to `max`. The `ultra` level is not offered, because it delegates to subagents automatically. By default `codex exec` offers the account's ChatGPT app connectors (mail, GitLab, site deploys, a remote shell), web browsing, image generation and subagents. Every Sol run switches those off (`CODEX_DISABLED_FEATURES`, plus `web_search="disabled"`), leaving shell commands and file patches. Code mode stays on because GPT-6-Sol calls every tool through it. Codex's login is bound read-only, and a sandboxed refresh would rotate its refresh token and log the host out, so preflight refuses a Sol run when the host Codex access token has less than seven hours left. `deepseek` runs `deepseek/deepseek-flash` at the max variant through OpenCode, inside the same sandbox; only the DeepSeek key is copied into the temporary provider state, never into the run directory. `prepare --instruction <path>` supplies a candidate instruction in place of the working one. The runner rejects a provider that differs from its prepared metadata. Prepare does not call a model; launch does. Only one instruction and filing enter a blind extraction.

Launch and worker startup verify the prepared instruction, filing and prompt against their recorded SHA-256 hashes before starting a provider. A revision also verifies its starting workbook and findings report. Changed or missing inputs require a newly prepared run directory. Older extraction metadata with the required hashes remains usable; older revision metadata without a findings-report hash must be prepared again. Status inspection does not recheck the starting workbook, since a revision legitimately changes it.

Revision is a separate mode: pass both `--revise-from <workbook>` and `--report <findings.md>` to prepare. This deliberately exposes that workbook and report in addition to the instruction and filing. Never use a revision as a blind extraction. The completed revision experiment is at `407a6e4:_dev/revision_loop/RESULTS.md`.

Inside the sandbox every Opus run sees only the Bash, Read and Write tools (`--tools`), and sets three Claude Code variables (`CLAUDE_ENV` in the runner, also recorded in `command.json`). `CLAUDE_CODE_DISABLE_REFUSAL_FALLBACK=1` makes a safety-classifier refusal fail the run rather than silently continue on another model. `CLAUDE_CODE_PROMPT_CACHE_TTL=1h` holds the cache lifetime at the subscription default, so costs stay comparable. `CLAUDE_CODE_SILENT_TURN_REMINDER_TURNS=1000000` stops the "user hasn't heard from you" reminder, since no one reads a sandboxed run as it works. Opus 5.5 can end an unattended turn with a progress report before its work is done. If a run ends cleanly while its deliverable is still owed, the worker resumes the same session with a short continuation message naming it, at most twice (`MAX_CONTINUATIONS`). For an extraction the deliverable is a readable four-sheet workbook; for a revision it is `revision_notes.md`. The sandbox's scratch home and `/tmp` are kept for all of a run's invocations, so the resumed session still has the working files it made. The message carries no findings or other information. The session lives only in the temporary provider state. `command.json` records the first command, every continuation command, the runner's hash at worker start and the provider binary's hash. Pin the Claude Code binary for comparisons with `SEC_CLAUDE_BIN`, because the installed CLI updates itself.

When a run ends, `status.json` records its tokens and cost (`usage`), read from the provider's event log; Codex reports tokens but no cost. For Opus, usage is summed over the first invocation and any continuations, and cost is the session's cumulative figure. `status.json` also holds a `provider` summary: served models, Claude Code version, turns, API time, thinking tokens, cache writes by lifetime, refusal and stop reasons, permission denials and subagents. `provider-results.json` keeps the CLI's result events verbatim, including the agent's final report. New run directories under `_dev/runs/` are ignored. Record the results you need, then delete the run. Full event logs from older experiments remain in their recorded git snapshots.

For new runs, `state: completed` means all of the following hold:
- the provider exited with code zero;
- for Opus, the CLI reported success without a refusal, and the only model that served the run was the prepared one;
- the expected workbook can be read, including its worksheets, and has exactly the four sheets the instruction requires, in order;
- for a revision, `revision_notes.md` was written.

Otherwise the run is `failed`, with one of these `failure_reason`s: `provider_refusal`, `provider_exit`, `provider_error`, `model_mismatch`, `workbook_missing`, `workbook_unreadable`, `workbook_incomplete` or `revision_notes_missing`. A timeout yields `timed_out`. Worker startup errors also leave a failed status. The worker exits nonzero on failure, while `launch` only reports successful dispatch: inspect `status` for the outcome. Older saved statuses keep their original meaning. Workbook readability is not a mechanical-checker pass or substantive acceptance; both remain separate steps.

The cockpit importer (`cockpit/import_results.py`) builds the catalog with one version per deal: the Opus 5.5 medium extraction in `extraction/<deal>.xlsx`, confirmed from the receipts in `_dev/reviews/2026-09-22-opus55-reextraction/`, plus the Datalink F9 and Mac-Gray R01 case-level decisions. `cockpit/verify_catalog.py` is the read-only live check of that catalog; it writes its result to the same packet.

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

`fetch_filing.py <deal>` fetches a filing from EDGAR. An existing filing must match its recorded local size/hash; `--verify` contacts EDGAR, while `--force` explicitly replaces a file. Fetch and verification select the same document type: for SC TO-T, the offer-to-purchase exhibit `EX-99.(A)(1)(A)`, rather than the cover form. Verification also requires the manifest's recorded document filename when present; legacy rows without one require an unambiguous match by type. Writes are atomic per file. Set `SEC_USER_AGENT` for another operator; the default identifies Austin. Seed rows marked for review remain unsupported.

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

The editable cockpit uses the allowlisted version catalog at `_dev/cockpit/catalog.json`, displaying each workbook beside its filing (`raw_filing/`, matched through `MANIFEST.csv`). The built React interface supports Ledger, Rounds, Questions and Deal facts editing, event insertion/deletion/movement, source navigation, findings, changes, history/restore and Excel export. Preserved source versions are immutable; saved working revisions live in the ignored `_dev/cockpit/state/workspace.sqlite3`. Preserve that database across deployments. Viewing a deal does not create a revision. The server binds 127.0.0.1, makes no network or model calls, runs the mechanical checker in-process and never reads `ref/`. If `dist/index.html` is missing, page routes return HTTP 503 naming the missing build; there is no fallback interface. See the [review guide](../cockpit/README.md) and [build contract](../COCKPIT_BUILD.md).

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

Acceptance suites run against a synthetic fixture (`acceptance/serve_fixture.py`) on a private port and a private headless Chrome; they never touch production workbooks, the catalog, working state or the live service. Run from the repository root:

```bash
COCKPIT_BROWSER_EVIDENCE=/tmp/cockpit-browser node _dev/tools/cockpit/acceptance/test_browser.mjs
COCKPIT_RESIZE_EVIDENCE=/tmp/cockpit-resize node _dev/tools/cockpit/acceptance/test_resize.mjs
COCKPIT_RESPONSIVE_EVIDENCE=/tmp/cockpit-responsive node _dev/tools/cockpit/acceptance/test_responsive.mjs
python3 -m pytest -q _dev/tools/cockpit/acceptance/test_http.py
(cd _dev/tools/cockpit/frontend && npx vitest run)
```

The browser suites use the repository `dist/` read-only; set `COCKPIT_TEST_DIST` to test a staged build such as `dist.new` before swapping. Screenshots go to `/tmp/cockpit-*-acceptance` unless a `COCKPIT_*_EVIDENCE` variable says otherwise; keep them outside the repository. `test_http.py` needs `pytest` and `requests`, which are not in `requirements.txt`.
