# v1.14 extraction trial — 26 September 2026

> **Status, 26 September 2026 (20:45 UTC):** historical evidence for v1.14. The v1.14.1 text has since been published in the cockpit as the default and retested on five deals ([retest](../2026-09-26-v1141-retest/README.md)), and Opus 5.5 medium is the live default engine. This packet's grading materials do not apply to v1.14.1: `administration/GRADING_KICKOFF_prior_to_pro_dispatch.md` rewards "dates and bounds", `grading/README.md` and `grading/03_instruction_and_research_decisions.md` close non-submitters "with a bound", and `grading/mechanical_check.py` has no Note cap. Each would score v1.14.1 behaviour as wrong ([`RETEST_PLAN.md`, Acceptance](../../maintenance/2026-09-26-v1141-streamline/retest/RETEST_PLAN.md)). Current state: [development handoff](../../HANDOFF.md).

**Completed: 15 of 15 runs produced readable workbooks.** Final packaging and preservation checks completed at 10:10 UTC on 26 September 2026. No outputs were graded or corrected. See `COMPLETION.json` and `administration/VERIFICATION.json`. Give the separate grader `GRADING_KICKOFF.md`.

Austin authorized 15 fresh blind extractions: Mac-Gray, Providence & Worcester and sTec, each on Opus 5.5 medium, Opus 5.5 xhigh, GPT-6-Astra high, GPT-6-Astra xhigh and GPT-6-Sol xhigh. One run per deal/setting; all 15 dispatched concurrently, with a common 120-minute wall-clock allowance.

This worktree administers the experiment. It does not deploy the upgrade or replace the live instruction. The frozen candidate is under `inputs/`, and every prepared run pins its bytes and its filing. The root instruction in this worktree remains the older checked-in version and is not used by the trial.

Each extractor sees a fresh filesystem environment with one read-only instruction, one read-only filing, and its own initially empty writable output folder. Project history, reference answers, previous outputs, reviews and sibling runs are not mounted. Web, connector and delegation tools are disabled. Network remains available for provider transport; post-run logs are checked mechanically for possible shell network use. `ISOLATION_PREFLIGHT.json` records actual filesystem tests of all 15 environments.

The existing upgraded runner, checker and sweep tools were copied from the undeployed v1.14 worktree. Binaries, inputs and runner hashes are recorded. No extraction rule was edited. Automatic schema checks occur after each model finishes, outside its sandbox; no feedback or correction pass is sent to the model. The standard runner may resume a cleanly ended Opus session if it has not yet saved its required workbook, using only a neutral completion reminder.

No substantive grading, ranking, workbook correction or model comparison is performed by the administrator. The sweep's grading/summary command is not run.

## Files

- `SETUP.json`, `plan.json`, `pin.json`: input and run configuration.
- `parallel-start.json`: evidence that all 15 were running concurrently.
- `ISOLATION_PREFLIGHT.json`: filesystem isolation checks for every run.
- `runs/<cell>/`: original workbook, provider records, compressed event log, automatic checker report and archived raw workspace.
- `COMPLETION.json`: administrative completion totals, safe to read before unblinding.
- `administration/VERIFICATION.json`: final input, isolation, configuration and preservation checks.
- `administration/outcomes.json`: per-run operational outcomes; contains model identities.
- `blinded/<deal>/A.xlsx` through `E.xlsx`: randomized labels with author/document and timestamp metadata normalized; all non-property workbook parts remain byte-identical to the originals.
- `administration/blind-key.json`: identities, withheld from the grader's first pass.
- `GRADING_KICKOFF.md`: instructions for the separate grading agent.

The stale Astra audit worktree was archived with every file verified before removal. Its archive and manifest are under `/home/uctpiaj/work/archive/sec-extraction-worktrees/2026-09-26/`. The v1.14 implementation worktree remains because it holds the undeployed upgrade and release base.

The main checkout, published instruction, live services, catalog and reviewed workbooks are outside this experiment. No commit or push is part of the authorization.

## GPT Pro review

Austin requested a lighter research-focused brief and dispatch to GPT Pro. `pro-review/REQUEST.md` supersedes the previous detailed grading rubric. The anonymous upload package excludes model identities, logs and prior evaluations. `administration/anonymization-v2.json` records the metadata-only changes; original run outputs remain unchanged. Do not rerun the earlier finalizer over these metadata-normalized copies.

## Relocation note (26 September 2026)

This packet was moved here from the `sec-extraction-v114-trial-20260926` worktree when that worktree was removed. All 296 files were verified by SHA-256. The absolute paths inside the JSON receipts and the logs are historical and still name the old location.