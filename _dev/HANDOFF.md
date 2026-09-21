# Current development handoff — 21 September 2026

The working instruction is **v1.12**, with 22 ledger columns and four sheets: Deal ledger, Rounds, Questions, Deal facts. [Its decision record](DECISIONS_v1.12.md) lists the seven general edits made to v1.11. v1.12 and the candidate v1.12.1 were run on the eight reviewed deals on 21 September (results below); neither has been run on an unseen filing.

The eight workbooks in `extraction/` (kraton, mac-gray, meredith, penford, petsmart, providence-worcester, stec, synacor) are blind **Opus 5 high runs under v1.11**. They pass the mechanical checker and are not research-ready: see the review below. `extraction/archive/v1.8/` holds three older workbooks. Older instructions, decision records and handoffs exist only in git history ([CHRONOLOGY.md](CHRONOLOGY.md)); keep it that way so no agent reads a past version by mistake.

## How Austin wants the instruction changed

Change the instruction only where the change is general: the research objective, the work process, honesty about uncertainty, a repaired contradiction, a deletion. Never add a rule whose only justification is one reviewed deal; that overfits, and a capable agent should reach such calls by judgment from the objective. Alex Gorbenko is out of reach for now, so conventions are Austin's to set provisionally. Every instruction edit still needs Austin's approval.

## What the 21 September review found

A model review of the eight v1.11 workbooks is in `reviews/2026-09-21/`, with a research note proposing a staged, evidence-first pipeline (`pipeline_research.md`). Five further model audits checked both. No human has adjudicated more than 6 of the review's 43 findings, so treat it as leads, not ground truth.

- Every bid price and bid date in all eight deals is correct.
- About 2–8% of ledger rows per deal carry a consequential error (Meredith 12–15%, mostly one round-label question). The errors sit in cohort counts, exit labels and reasons, round boundaries and conditionality: values stated more exactly than the filing supports.
- The extracting agents grepped narrow slices of the filing, never opened annexes, and ran the mandated reread as a quote-matching script. v1.12 addresses all three.
- Verdict: the staged pipeline is not being built now. v1.12 and an objective-led candidate come first.
- The eight reviewed deals shaped v1.12 and cannot test it. `ref/seed.csv` lists 390 deals; all but these eight are unseen.

## What the 21 September instruction comparison found

Thirty isolated runs: DeepSeek flash (max) under v1.11, v1.12 and v1.12.1 on all eight deals, and Opus high under v1.12 and v1.12.1 on Meredith, Synacor and sTec. The record is `reviews/2026-09-21/instruction_comparison.md`; the run folders are `_dev/runs/dsf_*` and `_dev/runs/opus_*`.

- On Opus, both new instructions beat v1.11: most over-exact counts, conditions and exit reasons the review found are gone, and no bid price, bidder or date is wrong.
- Neither beats the other. v1.12 is better on sTec, v1.12.1 on Meredith (the only run to split the December stage from the January final round) and slightly on Synacor. Round maps stay unstable under both.
- DeepSeek costs about $0.13 a deal against $4–6 and gets prices and bidders right, but is unreliable on processes, rounds, closures and Conditions. It is a cheap signal about an instruction, not the extractor. Its one clear signal: the shorter v1.12.1 cuts its checker errors from 42 to 11.
- These judgments come from model readers, not a human, and all eight deals shaped both instructions.

## Current workflow

- The isolated runner takes `--provider opus`, `sol` or `deepseek` (opencode, `deepseek/deepseek-flash`, max variant) and `--instruction <path>` to run a candidate instruction. Use [tools/README.md](tools/README.md) for the checker, isolated runner, filing fetcher, review helpers and cockpit. Run results go under ignored `_dev/runs/`.
- Review the workbooks in `extraction/` beside their filings in the read-only cockpit at https://lines.dealextract.org (Cloudflare Access: Austin and Alex). Service details are in the "Review cockpit" section of [tools/README.md](tools/README.md).
- `tools/check_lean.py` is the mechanical checker, version **1.5**, offline. It checks structure, quotation occurrence and agreement between columns of a row, not research correctness. A mechanical pass is not acceptance of the data. On the eight workbooks its new inferred-exit check raises five warnings (kraton #35; meredith #33, #34, #35, #56) and no errors.
- The runner writes tokens and cost to `status.json` and library versions to `metadata.json`; `tools/requirements.txt` is pinned. The eight v1.11 runs cost about $31 in total (about $4 a deal).
- `raw_filing/MANIFEST.csv` is the filing index: one line per filing with its EDGAR link and SHA-256, and each run's `metadata.json` records the hash it used. `tools/fetch_filing.py` maintains it; for an SC TO-T tender offer it saves the offer to purchase, exhibit (a)(1)(A). `tools/make_seed.py` is a deliberate rebuild command for `ref/seed.csv`.
- [RESEARCH_QUESTIONS.md](RESEARCH_QUESTIONS.md) is the current question list. Q3 needs no text change (C1, C12 and C15 already give its result). Q7 stays unadopted; the current C16 rule matches Alex's written §3.6.
- The `_dev/runs/v1.11_*` folders have been reviewed; their instruction copies are deleted. Delete the folders once nothing more is needed from their logs.

## Next work

1. **Objective-led candidate instruction ("Option A").** Austin approved drafting it as a separate candidate, not a replacement: objective and reasoning first, a work process with clear finish conditions, a short list of fixed conventions kept for cross-deal consistency, deal-born sub-rules deleted. His rulings: C12's late-reconfirmation rule shrinks to two sentences; C7 keeps its three tests and drops most of the case list. **Drafted 21 September as v1.12.1** (5,500 words) in the git worktree `../sec-extraction-v1.12.1`, branch `instruction-v1.12.1`, uncommitted. That worktree was cut from `59e2325`, so its tools are the older ones: run any test with this checkout's runner and checker, pointing at the candidate instruction. Austin has not yet read the draft. It has been run on the eight reviewed deals (comparison above).
2. **Blind comparison protocol**, then, **only on Austin's explicit command**, a head-to-head of v1.12 against the candidate on the same unseen filings (four deals under both is about $30). Unseen deals have no ground truth, so the protocol must say who judges the two ledgers and how.
3. Open design question, not approved: supplying runs with a committed HTML-to-text conversion of the filing with stable paragraph numbers, so agents stop writing throwaway converters. This changes the extraction input and needs Austin's decision.
4. When Alex is reachable: the convention questions in RESEARCH_QUESTIONS.md and Q7.

Uncommitted at the time of writing: everything from 20–21 September after `59e2325` (the v1.11 workbooks, three filings, the reviews, the cockpit, v1.12 and the tool changes). `extraction-v2` is also two commits ahead of GitLab. Commit and push only when Austin asks.
