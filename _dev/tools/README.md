# Pipeline tools

Run commands from the repository root. Read [AGENTS.md](../../AGENTS.md) and [the current handoff](../HANDOFF.md) first. Extractors must see only their isolated inputs; run the checker after extraction, outside that sandbox. Extractions, model experiments and workbook revisions require Austin's explicit instruction. These examples do not authorize a run.

## Environment

Python 3.10+ with the existing dependencies listed in [requirements.txt](requirements.txt): openpyxl, Beautiful Soup and lxml. Tests use `unittest` and mocks; no provider credentials or network are required.

The isolated runner requires Linux bubblewrap and an authenticated standalone Codex or native Claude installation. It resolves the executables on PATH; `SEC_CODEX_BIN` and `SEC_CLAUDE_BIN` can select explicit binaries. A Codex override must resolve to a standalone release's `bin/codex`, not a shell or Node wrapper. Credentials are bound read-only from the host; mutable provider state is temporary and deleted when the worker exits.

## Mechanical checking

```bash
python3 _dev/tools/check_lean.py --workbook extraction/<deal>.xlsx --filing raw_filing/<filing>.htm --output _dev/runs/<deal>/check.json
```

The checker is offline. It validates workbook structure, dates, labels, links and quotation occurrence. It does not establish the truth of classifications or live-bidder arithmetic. Required long Notes and documented uncertain Counts are review warnings.

## Isolated runs

```bash
python3 _dev/tools/sandbox/run_model.py prepare --provider opus --run-dir _dev/runs/<run> --deal <deal> --filing <bare-filing-name>.htm
python3 _dev/tools/sandbox/run_model.py launch --provider opus --run-dir _dev/runs/<run>
python3 _dev/tools/sandbox/run_model.py status --runs-dir _dev/runs
```

`sol` is the other supported provider. The runner rejects a provider that differs from its prepared metadata. Prepare does not call a model; launch does. Only one instruction and filing enter a blind extraction. The legacy DeepSeek/OpenCode shell runners were removed; restore their historical tree only for deliberate reproduction.

Revision is a separate mode: pass both `--revise-from <workbook>` and `--report <findings.md>` to prepare. This deliberately exposes that workbook and report in addition to the instruction and filing. Never use a revision as a blind extraction. The completed revision experiment is at `407a6e4:_dev/revision_loop/RESULTS.md`.

New run directories under `_dev/runs/` are ignored. Record the results you need, then delete the run. Full event logs from older experiments remain in their recorded git snapshots.

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
