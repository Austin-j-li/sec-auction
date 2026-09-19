# Proposed nine-run model comparison

19 September 2026. Preparation and connectivity probes only; extraction has not started.

Connectivity findings: a direct DeepSeek API request with `model=deepseek-flash`, thinking enabled and `reasoning_effort=max` succeeded in 3.71 seconds and returned `model=deepseek-flash`. Safe response metadata and its short experiment-design consultation are saved in `deepseek_direct_probe.json`. Claude also completed its sandbox workbook probe in 10.6 seconds: `--model opus --effort high` resolved to `claude-opus-5`, with no web searches or permission denials reported. Both models independently warned about identity leakage through workbook metadata and recommended fresh runs and neutral grading copies. Two fresh-state OpenCode attempts returned a model-routing error despite successful direct API access. Sol completed an API turn under the requested model/effort, but could not create the workbook because its shell launcher reported a missing executable. These are infrastructure preflight failures, not extraction scores. Resolve the Sol shell runtime and DeepSeek client route and require all three to pass the toy workbook test before dispatching the nine extraction jobs. See the probe artifacts for exact results; later checks may refine these diagnoses.

## Run matrix

One fresh session per model and filing, nine workbooks total:

| Model | Effort | Deals |
|---|---|---|
| GPT-5.6-Sol | xhigh | Mac-Gray, PetSmart, Providence & Worcester |
| Claude Opus 5 (`claude-opus-5`, the installed `opus` alias's verified resolution) | high | Same three |
| DeepSeek V4.1 Flash (`deepseek/deepseek-flash`) | max | Same three |

Freeze the root instruction, not the earlier unpatched comparison copy. Its SHA-256 at planning time is `f7e73a6673166597f2bd7c8c0457f72ba996585f1351595d00cd653f7a37009d`. Record full instruction and filing hashes, CLI versions, launch arguments, resolved model identifiers, and timestamps in a manifest before launching. Never substitute another model after a failure.

## Extraction isolation and administration

Create a new comparison directory, preserving all earlier experiments. Each bubblewrap session sees exactly one instruction, one original full HTML filing, its empty output directory, and a common installed Python/tool runtime. It gets a fresh home, client state and temporary directory. No reference answers, development material, repository history, assistant memory, previous outputs, cross-run folders, checker or grading rubric are mounted. Provider authentication is narrowly provisioned outside the working input directory; credentials never appear in published logs or artifacts. User/project custom instructions, skills, hooks and external connectors are disabled or absent.

Use the same short task prompt and output name `<deal>.xlsx` in every run. Do not add deal-specific hints. Expose equivalent file/shell capabilities and the same Python packages. Use the installed native clients for Sol and Opus and OpenCode for DeepSeek; record this client difference as part of the experiment rather than claiming to isolate model weights alone.

The existing sandbox shares network access for the model API. A filesystem sandbox plus disabled web tools does not physically block shell HTTP requests. For extraction, block browsing tools and require filing-only use; audit tool commands for external retrieval. If stronger network enforcement is implemented, test API-only egress in preflight. Do not claim complete network isolation without verifying it. Any outside evidence access invalidates that run.

Start all nine independent jobs with a small launch stagger, then monitor them outside their sandboxes. Preserve stdout/stderr, tool events, exit status, elapsed time and available usage/cost. Allow equal 90-minute initial ceilings; a harness interruption can resume the same isolated session with no content hints, recorded separately. Do not silently select the best retry or provide checker-driven repairs. Preserve failed attempts and report incomplete jobs explicitly.

## Blind evaluation

1. Before opening candidate workbooks, have fresh isolated evaluators prepare references for each deal from the full filing and the frozen instruction. Their first stage has no candidate workbooks or earlier comparisons mounted. Lock the event inventory, supported alternatives, round transitions, bidder accounting and scoring definitions before admitting neutral candidates for the second stage. Do not reuse old candidate scores or accept the old reference mechanically.
2. Use the filing for source facts and the frozen instruction for required conventions. Evaluate agreement with Alex's primary hand coding and voice notes separately. Example: the older PetSmart rubric penalized a valuation statement for not being a Bid; that is not automatically an error under current C12. Keep this example out of extractor prompts.
3. Preserve original workbook bytes. Randomize opaque candidate IDs independently for each deal. Keep the model-to-ID map in the administrator area, outside all grader sandboxes. Produce neutral content dumps and copies with identifying document metadata removed; preserve content, values, formulas and formatting. Audit filenames, properties, comments, sheet content and dump headers for model identifiers. Disclose any unavoidable clues instead of calling this perfect blinding.
4. Dispatch one fresh independent grader per deal, with no inherited conversation. Each receives only the full filing, current instruction, locked reference/rubric, and that deal's three neutral candidates. The administrator who knows identities does not assign blind grades. Grade all three against the same reference and record evidence for every charged error.
5. Run a new schema-appropriate mechanical checker after extraction, outside the extractor environment: required four sheets and 22 columns, controlled values, dates/windows/order, price cells, row/question links, per-round consistency and source quotation occurrence. Quote occurrence and arithmetic checks are not semantic adjudication. Report these separately from factual grades.
6. Assess core research outcomes: live-bidder counts at fixed transitions; processes, rounds and bid placement; formality and conditions; event order and supported date bounds; proposal coverage and prices. Separately list omitted material events, unsupported additions, internal inconsistencies, workbook compliance and review-text burden. Record denominators and specific affected rows; avoid treating one shared upstream mistake as many independent failures.
7. Send material disputed judgments or proposed changes to the locked reference to a fresh identity-blind adjudicator. Apply any justified reference amendment to every candidate, preserving the original reference and an amendment log. Freeze scores and evidence before revealing the identity map.

## Reporting

Deliver nine original workbooks in model-specific folders, the frozen manifest and inputs, redacted execution logs, mechanical reports, blind grades with source evidence, the subsequently revealed mapping, and one comparison report. Compare models within each deal before summarizing across deals. Separate extraction/API cost from unavailable subscription marginal cost; do not invent dollar prices. Report output size and estimated review burden as proxies, not measured human correction time.

This is one run per model per deal. It can identify practical strengths, failures and a provisional model preference on these three development deals. It does not estimate within-model variability or demonstrate performance on unseen deals. The working instruction remains unchanged, and no commit or push is part of this plan.
