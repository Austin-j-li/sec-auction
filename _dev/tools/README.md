# Pipeline tools

Run commands from the repository root. Read [AGENTS.md](../../AGENTS.md) first. The checker and analysis tools enforce Version 1 only, using the current 29-column Deal ledger. The Version 1 instruction is a draft in `_dev/alignment_sprint/draft/`; the root instruction remains Version 0 until Austin approves it. A workbook with any other ledger header is an error, not a fallback. Extractions, model experiments and workbook revisions need Austin's explicit instruction; these examples do not authorize a run.

## Environment

Python 3.10+ with the dependencies pinned in [requirements.txt](requirements.txt): openpyxl, Beautiful Soup and lxml. A run records the installed versions in `metadata.json` (`library_versions`).

The isolated runner needs Linux bubblewrap and a standalone Codex or native Claude installation, found on PATH or named by `SEC_CODEX_BIN` and `SEC_CLAUDE_BIN`. A Codex override must be a standalone release's `bin/codex`, not a wrapper.

Opus runs use a long-lived subscription token made once with `claude setup-token` and saved to `~/.config/sec-extraction/claude-oauth-token` (mode 600); `SEC_CLAUDE_OAUTH_TOKEN_FILE` names another file. The token reaches the sandbox through an inherited pipe, never a command line, environment variable or file in the run. The host's own Claude login is never shared, because a refresh inside the read-only sandbox would log the host out. Codex runs bind `~/.codex/auth.json`, or the file `SEC_CODEX_AUTH_FILE` names, read-only, and refuse a login within 7 hours of expiry.

## Mechanical checking

```bash
python3 _dev/tools/check_lean.py --workbook extraction/<deal>.xlsx --filing raw_filing/<filing>.htm --output _dev/runs/<deal>/check.json
```

The checker is offline. It checks workbook structure, dates, labels, links, that each quotation occurs in the filing, and agreement between columns of a row. It does not judge whether a classification is right or count live bidders. Its report gives `checker_version` and `ledger_schema`, both `Version 1`. Exit status is 0 with no errors, 1 with errors, 2 when an input cannot be read.

## Isolated runs

```bash
python3 _dev/tools/sandbox/run_model.py prepare --provider opus --run-dir _dev/runs/<run> --deal <deal> --filing <filing>.htm [--model <model>] [--effort <level>] [--timeout-minutes <n>] [--instruction <file>]
python3 _dev/tools/sandbox/run_model.py launch --provider opus --run-dir _dev/runs/<run>
python3 _dev/tools/sandbox/run_model.py status --runs-dir _dev/runs
```

The default is Claude Opus 5.5 (`claude-opus-5-5`) at medium effort. `--provider opus` also runs `claude-fable-5-1`; `--provider sol` runs `gpt-6-sol` by default (xhigh) or `gpt-6-astra` (high) through Codex. Efforts are `low` to `max`. The model, effort and time limit (default 90 minutes, 10–360 allowed) are recorded in `metadata.json`, and launch refuses metadata with a model or effort that is not allowed. Prepare calls no model; launch does. `--instruction` supplies another instruction file in place of the root one. `--filing-dir` takes `raw_filing/` (the default) or a deal folder the cockpit added under `_dev/cockpit/state/filings/`.

Launch and worker startup check the prepared instruction, filing and prompt against their recorded SHA-256 hashes. A changed or missing input needs a newly prepared run directory.

Revision is a separate mode: pass both `--revise-from <workbook>` and `--report <findings.md>`. The workbook must be a four-sheet Version 1 workbook. A revision deliberately shows the agent that workbook and the findings, so it is never a blind extraction.

Every Opus run sees only the Bash, Read and Write tools and sets the variables in `CLAUDE_ENV`: a refusal fails the run instead of switching models, the prompt cache keeps the subscription lifetime, and the "user hasn't heard from you" reminder never fires. If a run ends while its deliverable is still owed, the worker resumes the same session at most twice (`MAX_CONTINUATIONS`) with a short message naming the deliverable. Sol runs disable connectors, web, image generation and subagents. Pin the Claude binary with `SEC_CLAUDE_BIN` for comparisons, because the installed CLI updates itself.

When a run ends, `status.json` records its tokens and cost (Codex reports no cost) and a `provider` summary; `provider-results.json` keeps the CLI's result events. `state: completed` means the provider exited with code zero; for Opus, the CLI reported success without a refusal and only the prepared model served the run; the workbook reads and has exactly the four required sheets in order; and a revision wrote `revision_notes.md`. Otherwise the run is `failed` with a `failure_reason` (`provider_refusal`, `provider_exit`, `provider_error`, `model_mismatch`, `usage_limit`, `workbook_missing`, `workbook_unreadable`, `workbook_incomplete`, `revision_notes_missing`) or `timed_out`. `launch` reports only the dispatch; read `status` for the outcome. A readable workbook is not a checker pass. Record the results you need, then delete the run folder.

## Effort sweeps

`effort_sweep.py` runs the same filings under several arms (`provider:model:effort`) through the isolated runner. It needs Austin's authorization, as any extraction does.

```bash
python3 _dev/tools/effort_sweep.py plan --packet <packet dir> --deals <deal,...> --arms opus:claude-opus-5-5:medium sol:gpt-6-sol:high --replicates 2 --seed <n>
SEC_CLAUDE_BIN=<pinned claude> SEC_CODEX_BIN=<pinned codex> python3 _dev/tools/effort_sweep.py run --packet <packet dir> --concurrency 3
python3 _dev/tools/effort_sweep.py summarize --packet <packet dir>
```

`plan` writes a seeded, interleaved run order. `run` pins the provider binaries, instruction and runner by hash, launches each cell as an ordinary run, runs the checker outside the sandbox, copies receipts, workbook and compressed event log into the packet, and stops after three provider or worker failures in a row (`--retry-failed` runs those cells again). It can be restarted. `summarize` reports cost, tokens, time, checker counts, ledger size and agreement between replicates per arm.

## Review and analysis helpers

```bash
python3 _dev/tools/findings_text.py <check.json> <findings.md>
python3 _dev/tools/diff_workbooks.py <before.xlsx> <after.xlsx> [--by-quote]
python3 _dev/tools/derive_analysis.py <ledger.xlsx> --out <new dir> [--deal <deal>]
python3 _dev/tools/review_list.py <ledger.xlsx> [--disable CATEGORY] [--output <review.json>]
python3 _dev/tools/compare_alex.py <ledger.xlsx> --out <new dir> [--deal <deal>]
```

`findings_text.py` turns a checker report into numbered findings for a revision pass, errors first; warnings stay review leads. `diff_workbooks.py` compares two Version 1 workbooks sheet by sheet and keeps cell types, so a number changed into text shows. `derive_analysis.py` turns a Version 1 ledger into estimation tables (bids, other-scope bids, rounds, participation, deal) with the T0–T3 Formality readings side by side and every open research choice listed as a switch with no default; it writes only into a new or empty folder outside `extraction/`, `raw_filing/` and `ref/`. `compare_alex.py` sets a ledger beside Alex's hand coding as a review aid; it reads `ref/`, so never run it where an extraction can see the output.

`review_list.py` builds a review queue from workbook cells without changing the ledger. Repeat `--disable` to omit categories: `unknown_type`, `qualified_count`, `type_unsplit_count`, `inferred_exit`, `unexplained_exit`, `deadline_outcome`, `partial_only`, `non_per_share_price`, `non_dollar_price`, `round_opened`, `multi_process`. The queue is a set of review leads, not a source-accuracy verdict. Like `derive_analysis.py`, it refuses an `--output` under `extraction/`, `raw_filing/` or `ref/`, or over the input workbook.

## Filing inputs

```bash
python3 _dev/tools/fetch_filing.py <deal> [--verify] [--force]
python3 _dev/tools/fetch_filing.py --list <name>
```

`fetch_filing.py` fetches a filing from EDGAR into `raw_filing/` and records it in `MANIFEST.csv`. An existing file must match its recorded size and hash; `--verify` checks against EDGAR and `--force` replaces the file. For SC TO-T it takes the offer-to-purchase exhibit, not the cover form. Set `SEC_USER_AGENT` for another operator.

`make_seed.py` rebuilds `ref/seed.csv` from Alex's workbook using identifying fields only. Do not run it merely to tidy the repository.

## Tests

```bash
cd _dev/tools && python3 -m pytest -q
```

The tests use synthetic fixtures and mocks. Runner tests build commands but never launch a model.
