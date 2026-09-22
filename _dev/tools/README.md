# Pipeline tools

Run commands from the repository root. Read [AGENTS.md](../../AGENTS.md) and [the current handoff](../HANDOFF.md) first. Extractors must see only their isolated inputs; run the checker after extraction, outside that sandbox. Extractions, model experiments and workbook revisions require Austin's explicit instruction. These examples do not authorize a run.

## Environment

Python 3.10+ with the dependencies pinned in [requirements.txt](requirements.txt): openpyxl, Beautiful Soup and lxml. Change a pin deliberately; a run records the installed versions in `metadata.json` (`library_versions`). Tests use `unittest` and mocks; no provider credentials or network are required.

The isolated runner requires Linux bubblewrap and an authenticated standalone Codex or native Claude installation. It resolves the executables on PATH; `SEC_CODEX_BIN` and `SEC_CLAUDE_BIN` can select explicit binaries. A Codex override must resolve to a standalone release's `bin/codex`, not a shell or Node wrapper. Credentials are bound read-only from the host; mutable provider state is temporary and deleted when the worker exits.

## Mechanical checking

```bash
python3 _dev/tools/check_lean.py --workbook extraction/<deal>.xlsx --filing raw_filing/<filing>.htm --output _dev/runs/<deal>/check.json
```

The checker is offline. It validates workbook structure, dates, labels, links, quotation occurrence and agreement between columns of the same row (an exact-day When against its three date cells; an inferred exit's reason). It does not establish the truth of classifications or live-bidder arithmetic. Required long Notes and documented uncertain Counts are review warnings.

## Isolated runs

```bash
python3 _dev/tools/sandbox/run_model.py prepare --provider opus --run-dir _dev/runs/<run> --deal <deal> --filing <bare-filing-name>.htm
python3 _dev/tools/sandbox/run_model.py launch --provider opus --run-dir _dev/runs/<run>
python3 _dev/tools/sandbox/run_model.py status --runs-dir _dev/runs
```

The current extraction workflow uses **Opus 5 high**. `sol` and `deepseek` remain implemented transports, not approved defaults; an alternative-model run requires Austin's explicit command. `deepseek` runs `deepseek/deepseek-flash` at the max variant through OpenCode, inside the same sandbox; only the DeepSeek key is copied into the temporary provider state, never into the run directory. `prepare --instruction <path>` supplies a candidate instruction in place of the working one. The runner rejects a provider that differs from its prepared metadata. Prepare does not call a model; launch does. Only one instruction and filing enter a blind extraction. The legacy DeepSeek/OpenCode shell runners were removed; the `deepseek` provider replaces them.

Launch and worker startup verify the prepared instruction, filing and prompt against their recorded SHA-256 hashes before starting a provider. A revision also verifies its starting workbook and findings report. Changed or missing inputs require a newly prepared run directory. Older extraction metadata with the required hashes remains usable; older revision metadata without a findings-report hash must be prepared again. Status inspection does not recheck the starting workbook, since a revision legitimately changes it.

Revision is a separate mode: pass both `--revise-from <workbook>` and `--report <findings.md>` to prepare. This deliberately exposes that workbook and report in addition to the instruction and filing. Never use a revision as a blind extraction. The completed revision experiment is at `407a6e4:_dev/revision_loop/RESULTS.md`.

When a run ends, `status.json` records its tokens and cost (`usage`), read from the provider's event log; Codex reports tokens but no cost. New run directories under `_dev/runs/` are ignored. Record the results you need, then delete the run. Full event logs from older experiments remain in their recorded git snapshots.

For new runs, `state: completed` means the provider exited with code zero and the expected workbook can be read, including its worksheets. A nonzero provider exit or missing/unreadable workbook yields `failed`, with a `failure_reason`; a timeout yields `timed_out`. Worker startup errors also leave a failed status. The worker exits nonzero on failure, while `launch` only reports successful dispatch: inspect `status` for the outcome. Older saved statuses keep their original meaning. Workbook readability is not a mechanical-checker pass or substantive acceptance; both remain separate steps.

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

The editable cockpit uses the allowlisted version catalog at `_dev/cockpit/catalog.json`, displaying each workbook beside its filing (`raw_filing/`, matched through `MANIFEST.csv`). The built React interface supports Ledger, Rounds, Questions and Deal facts editing, event insertion/deletion/movement, source navigation, findings, changes, history/restore and Excel export. Preserved source versions are immutable; saved working revisions live in the ignored `_dev/cockpit/state/workspace.sqlite3`. Preserve that database across deployments. Viewing a deal does not create a revision. The server binds 127.0.0.1, makes no network or model calls, runs the mechanical checker in-process and never reads `ref/`. If the catalog or built frontend is absent, the legacy read-only interface remains available. See the [review guide](../cockpit/README.md) and [build contract](../COCKPIT_BUILD.md).

Quotes are located with the checker's own parsing and both of its filing renderings, so every quote the checker accepts is highlighted. A "page hint" (a quote found on a different printed page from the one cited) is a cockpit hint, not a checker finding, and is shown only when a filing's page numbers were detected reliably. A workbook or filing that cannot be read is listed as unreadable (HTTP 409 for that deal) without hiding the other deals.

The editable build was deployed on 22 September 2026 at https://lines.dealextract.org. The systemd user unit `ledger-cockpit.service` runs the server from the working tree on 127.0.0.1:8778, and `cloudflared.service` publishes that port behind the existing Cloudflare Access route for Austin and Alex. Public writes require a configured trusted identity, matching Origin and a session CSRF token. Unknown users do not default to Austin. Direct loopback development uses the explicit `local` actor. The service drop-in sets `COCKPIT_PUBLIC_ORIGIN=https://lines.dealextract.org`; do not expose the loopback development server directly to the network.

Build frontend changes with `npm ci` and `npm run build` from `_dev/tools/cockpit/frontend/`; assets are written to `../dist/`. After changing Python server/checker code, restart `ledger-cockpit.service`. Verify `/api/session`, `/api/deals` and `/api/deal/<deal>?version=working`, compare checker findings with a fresh run, and preserve source hashes and working state. Catalog updates are read on later requests; changing a default base must not silently replace a saved working revision. Logs: `journalctl _SYSTEMD_USER_UNIT=ledger-cockpit.service` (or `cloudflared.service`). Verification evidence is linked from [HANDOFF.md](../HANDOFF.md).
