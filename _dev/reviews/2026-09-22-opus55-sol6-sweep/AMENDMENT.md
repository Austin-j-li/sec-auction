# Amendment to the sweep protocol

Written 22 September 2026 at about 20:00 UTC, while the first replicate was running and before any workbook had been graded. `PROTOCOL.md` is unchanged and still matches `protocol-freeze.json`. This file records how the sweep departed from it and why.

## One replicate instead of two

At about 19:58 UTC Austin cut the sweep to 12 cells: "make it 12".

- **What runs.** Replicate 1 only: every deal-arm pair once, 3 deals × 4 arms. The 12 replicate-2 cells in `plan.json` were never launched.
- **How it was stopped.** The plan runs all of replicate 1 before replicate 2, and 7 of the 12 replicate-1 cells had launched. I stopped the driver, leaving its detached workers running, and restarted it with `--only` limited to the replicate-1 cell ids. It picked up the four runs in flight and launched only the remaining replicate-1 cells. `driver.log` marks the restart.
- **All at once.** At about 20:02 UTC Austin asked for "a big parallel of 12, just make sure they don't see each other". I restarted the driver again with a limit of 12, so the last five cells launched together and eight ran at the same time. Before the restart I checked the live sandboxes. Each had its own `/tmp`, home and provider-state directories, only its own instruction copy, filing and output directory, and its own process namespace. The runs share only network access, which the model APIs need.
- **Effect on the decision rule.** The rule compared effort levels against the larger of 2 points and the pooled replicate spread. With one run per cell there is no replicate spread, so the threshold is 2 points. Run-to-run variation is not measured, so a difference that clears 2 points on two of three deals could still be run noise. The report therefore treats every effort comparison as direction only. It also states the grader noise measured by the duplicate controls, which sets a floor on what one score can resolve.
- **Effect on the secondary measures.** Agreement between replicates (bid multiset Jaccard, same round count, event-count gap) cannot be computed and is not reported.

## Grading details the protocol left open or described differently

These were settled during two dry runs on the calibration workbooks (Providence & Worcester, not a sweep deal), before any sweep workbook was graded.

- **What graders see.** The protocol says graders get "a copy of the workbook with its document properties cleared". They instead get a JSON dump of the four sheets, with each row's Excel row number. No file properties survive at all, and Claude and Codex agents can read it without a spreadsheet library.
- **Where graders work.** Graders work in a self-contained grading directory outside the repository. It holds the blinded bundles and copies of the reference tests, filings and instruction. `inputs.json` records the copies' SHA-256 hashes, which match the frozen files. The first dry run pointed graders at the repository, where run receipts sit next to the references and name each arm. It also showed Claude graders writing scratch files under generic names into a shared folder, where one grader could have read another's files. Each grader now has a private work directory, and the label key is kept outside the grading directory.
- **Access audit.** After grading, `access-audit.json` lists every path each grader session touched. It flags any path outside that grader's own bundle, the shared inputs and its own work directory, and any mention of another bundle's label. Flagged sessions are reported.
- **Astra's settings.** GPT-6-Astra runs at reasoning effort `high` through `codex exec` in a read-only sandbox. Web search is disabled, the same Codex features as the extraction runs are disabled, and a JSON schema is enforced on the output. A session that misses any test id is retried once.
- **Claude graders.** Two fresh Claude Opus 5.5 subagents per bundle, run through a workflow, with the grade schema enforced as structured output.
- **Dry-run agreement, as a sanity check only.** On the Sol calibration workbook, Claude graders scored 87.25–89.0 across six grades. Astra scored 85.5 and 83.75 in two separate sessions. On the Opus calibration workbook, every grader scored 98.75. These numbers are not part of the sweep results.

## Addendum written after grading (22 September 2026, about 20:40 UTC)

Everything above was written before any sweep workbook was graded. This section was added after unblinding, following independent checks of the draft report.

- **Load differed by arm.** The concurrency note above does not state the timing effect. The cut to 12 cells and the restart with a limit of 12 ran the Datalink and Mac-Gray cells of the higher-effort arms early, with about 4 runs going at once. The lower-effort arms ran later, under 6 to 8. The seeded order no longer gave the arms a shared time window. Wall-time comparisons are therefore confounded with load, and the report compares token counts instead.
- **Disputed grades.** The checks found three grades that the frozen rubric decides differently from the graders, plus contested reference items. The frozen grades remain the primary result, because changing grades once the arms are known would bias it. The report shows the disputes as sensitivity scenarios and states whether any verdict changes. None does.
- **Grader noise.** The duplicate controls only show that each grader gives the same answer twice. They do not measure disagreement between grader families, which reaches 5.5 points on one workbook. The report states that spread as the resolution limit for single-score comparisons, rather than the duplicate gap.
