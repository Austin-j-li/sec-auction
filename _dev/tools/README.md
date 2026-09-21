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

`sol` and `deepseek` are the other supported providers. `deepseek` runs `deepseek/deepseek-flash` at the max variant through OpenCode, inside the same sandbox; only the DeepSeek key is copied into the temporary provider state, never into the run directory. `prepare --instruction <path>` supplies a candidate instruction in place of the working one. The runner rejects a provider that differs from its prepared metadata. Prepare does not call a model; launch does. Only one instruction and filing enter a blind extraction. The legacy DeepSeek/OpenCode shell runners were removed; the `deepseek` provider replaces them.

Revision is a separate mode: pass both `--revise-from <workbook>` and `--report <findings.md>` to prepare. This deliberately exposes that workbook and report in addition to the instruction and filing. Never use a revision as a blind extraction. The completed revision experiment is at `407a6e4:_dev/revision_loop/RESULTS.md`.

When a run ends, `status.json` records its tokens and cost (`usage`), read from the provider's event log; Codex reports tokens but no cost. New run directories under `_dev/runs/` are ignored. Record the results you need, then delete the run. Full event logs from older experiments remain in their recorded git snapshots.

## Review helpers and filing inputs

```bash
python3 _dev/tools/findings_text.py <check.json> <findings.md>
python3 _dev/tools/diff_workbooks.py <before.xlsx> <after.xlsx>
python3 _dev/tools/fetch_filing.py --list <name>
```

Findings distinguish mechanical errors from review warnings and optional model judgments. Workbook diffs preserve cell types, so a number changed into text is visible, and detect added trailing columns.

`fetch_filing.py <deal>` fetches a filing from EDGAR. An existing filing must match its recorded local size/hash; `--verify` contacts EDGAR, while `--force` explicitly replaces a file. Writes are atomic per file. Set `SEC_USER_AGENT` for another operator; the default identifies Austin. SC TO-T exhibits and seed rows marked for review remain unsupported.

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

A read-only page for reviewing each `extraction/<deal>.xlsx` beside its filing (`raw_filing/`, matched through `MANIFEST.csv`): filing text on the left with every ledger quote highlighted and printed page numbers marked, and ledger, rounds, questions, deal facts and checker findings on the right. Iteration 1 is read-only. The server binds 127.0.0.1, answers GET only, makes no network calls and writes no files; workbooks are read from an in-memory copy. It runs `check_lean.py` in-process and keeps the report only in memory. It never reads `ref/`.

Quotes are located with the checker's own parsing and both of its filing renderings, so every quote the checker accepts is highlighted. A "page hint" (a quote found on a different printed page from the one cited) is a cockpit hint, not a checker finding, and is shown only when a filing's page numbers were detected reliably. A workbook or filing that cannot be read is listed as unreadable (HTTP 409 for that deal) without hiding the other deals.

Deployed since 21 September 2026 at https://lines.dealextract.org. The systemd user unit `ledger-cockpit.service` runs this server from the working tree on 127.0.0.1:8778. The unit `cloudflared.service` publishes that port through the dedicated tunnel, behind Cloudflare Access (one-time email code, Austin and Alex only). Both units are enabled, and lingering is on, so they start at boot. The server reads `Cf-Access-Authenticated-User-Email` only to display the reader (austin or alex, default austin); it never uses it for access control. Workbook changes show up on the next request. After changing cockpit code, run `systemctl --user restart ledger-cockpit`; the site returns an error for about 15 s while the server restarts and loads the deals. Logs: `journalctl _SYSTEMD_USER_UNIT=ledger-cockpit.service` (or `cloudflared.service`).
