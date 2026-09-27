# Recovery team brief (shared by every agent)

## Situation
Repo: `/Users/austinli/Projects/sec-auction`, branch `local-recovery-2026-09-27` (off `679d4fc`, 23 Sep, "Cockpit phase 5").
The real development tree lives on a remote VM (`/home/uctpiaj/work/Projects/sec-extraction`, plus worktrees
`sec-extraction-v114` and `sec-extraction-v114-trial-20260926`) that is unreachable. 24–26 Sep work there was never
committed. We are rebuilding what we can on the laptop from evidence. Read `AGENTS.md` and `_dev/recovery/GAP.md` first.

## Evidence (read-only; never modify)
- `/tmp/recov/evidence/<repo-relative-path>.json` — per file: every Read/Write/Edit tool call on that file in the VM
  Claude transcripts, chronological (`events[]`: ts, tree = which VM checkout, tool, input, result), plus
  `bash_mentions[]` (Bash commands after 23 Sep 17:00 that mention the file's basename, with output).
  `INDEX.json` lists all paths. Read results carry `cat -n` style line prefixes (`   12→text` or `12\ttext`); strip them.
  An Edit's `input` has `old_string`/`new_string`/`replace_all`. A Read with `offset`/`limit` is partial.
- `/tmp/recov/all_calls_since_0924.jsonl` — every tool call (any tool) from 24 Sep onwards, chronological
  (ts, name, cwd, input, result, session). Use for heredoc writes (`cat > file <<`), `python - <<` edits, diffs, test output.
- `/tmp/calib/*.md` — digests of each VM session (user and assistant messages); `/tmp/calib/astra_report.md` — status report.
- `_dev/recovery/2026-09-27-cockpit/` — snapshot of the live cockpit API (hash-indexed in `INDEX.json`):
  published instructions in `instructions/`, and in `raw/` per-deal JSON including every stored version with the
  cockpit's own checker output (`check`, checker_version 1.8 on the 26 Sep v1.14.1 reruns) and `.xlsx` exports.
- Original transcripts: `~/.claude/projects/ssh-*/**/*.jsonl` (if the digests are not enough).

## Reconstruction rules
1. Tree precedence: the final state is the **main** checkout (`/home/uctpiaj/work/Projects/sec-extraction/`) as of
   26 Sep ~20:50 UTC. Work done in `sec-extraction-v114` was merged into main around 19:00–19:40 on 26 Sep; check the
   evidence for the merge before assuming.
2. Replay: start from the last full snapshot (a Write, or a Read that covers the whole file with no gaps), then apply
   every later Edit to that file in the relevant tree, in order. An Edit whose `old_string` does not occur is a signal
   that an intermediate unseen change exists — record it, do not guess silently.
3. Where content is not in evidence, rebuild from specs/descriptions/tests in evidence. Mark each rebuilt file's
   provenance in your report (EXACT / REPLAYED / REBUILT) — never in the file itself unless it is a doc.
4. Tests decide. Recovered tests are ground truth over reconstructed code when they disagree.

## Hard limits
- Touch only the files your slice names. Other agents are editing other files concurrently.
- No git commit/push/reset/checkout/stash. No network. No real model runs (no `run_model.py` live, no API calls).
- Do not edit `raw_filing/`, `extraction/`, `ref/`, `_dev/recovery/2026-09-27-cockpit/`.
- `lesson/` is dropped; never recreate it.
- Run only your slice's tests (`python3 -m pytest _dev/tools/<your tests> -q`), not the whole suite.

## Report (final message, also write to `/tmp/recov/reports/<slice>.md`)
Per file: provenance class, evidence used (ts of snapshot + number of replayed edits), anything unresolved.
Then test commands run and their exact outcome. Be concrete; no summary prose.

## Proportionality (added by the orchestrator, 27 Sep 12:50)
- The goal is a faithful, working copy of the VM state, not a better design. Do the smallest change the evidence supports.
  No new abstractions, options, helpers, tests beyond what a fix needs, or defensive code the VM did not have.
- A reviewer's job on a fix round is to confirm the named findings are fixed and nothing important broke. Do not reopen
  accepted work, re-audit the whole slice, or raise style, wording, or hypothetical concerns. "Minor" findings that do not
  change behaviour or recovered content should normally be left out.
- Uncertainty is recorded once in the report, plainly. Do not pad reports with caveats.
- Reviewers: the read-only sandbox cannot create temp dirs, so do not try to run pytest; the orchestrator runs the tests.
