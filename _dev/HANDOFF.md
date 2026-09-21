# Current development handoff — 21 September 2026

The working instruction is **v1.13**: the objective-led rewrite (5,600 words, tested as "v1.12.1") plus a definition of a round as one request for offers. The workbook format is unchanged: 22 ledger columns and four sheets (Deal ledger, Rounds, Questions, Deal facts). [Its decision record](DECISIONS_v1.13.md) lists what changed. Its conventions are sections E1–E14; v1.12 and earlier called them C1–C16. **No extraction has run under v1.13 as it now reads, and none under any version on an unseen filing.**

The eight workbooks in `extraction/` (kraton, mac-gray, meredith, penford, petsmart, providence-worcester, stec, synacor) are blind **Opus 5 high runs under v1.11**. They pass the mechanical checker and are not research-ready: see the review below. `extraction/archive/v1.8/` holds three older workbooks. Older instructions, decision records and handoffs exist only in git history ([CHRONOLOGY.md](CHRONOLOGY.md)); keep it that way so no agent reads a past version by mistake.

## How Austin wants the instruction changed

Change the instruction only where the change is general: the research objective, the work process, honesty about uncertainty, a repaired contradiction, a deletion. Never add a rule whose only justification is one reviewed deal; that overfits, and a capable agent should reach such calls by judgment from the objective. Alex Gorbenko is out of reach for now, so conventions are Austin's to set provisionally. Every instruction edit still needs Austin's approval.

## What the 21 September review found

A model review of the eight v1.11 workbooks is in `reviews/2026-09-21/`, with a research note proposing a staged, evidence-first pipeline (`pipeline_research.md`). Five further model audits checked both. No human has adjudicated more than 6 of the review's 43 findings, so treat it as leads, not ground truth.

- Every bid price and bid date in all eight deals is correct.
- About 2–8% of ledger rows per deal carry a consequential error (Meredith 12–15%, mostly one round-label question). The errors sit in cohort counts, exit labels and reasons, round boundaries and conditionality: values stated more exactly than the filing supports.
- The extracting agents grepped narrow slices of the filing, never opened annexes, and ran the mandated reread as a quote-matching script. v1.12 and v1.13 address all three.
- Verdict: the staged pipeline is not being built now.
- The eight reviewed deals shaped v1.12 and v1.13 and cannot test them. `ref/seed.csv` lists 390 deals; all but these eight are unseen.

## What the 21 September instruction comparison found

Thirty isolated runs: DeepSeek flash (max) under v1.11, v1.12 and v1.12.1 on all eight deals, and Opus high under v1.12 and v1.12.1 on Meredith, Synacor and sTec. The record is `reviews/2026-09-21/instruction_comparison.md`; the run folders `_dev/runs/dsf_*` and `_dev/runs/opus_*` keep the workbooks and logs, without their instruction copies; delete them once nothing more is needed.

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
- [RESEARCH_QUESTIONS.md](RESEARCH_QUESTIONS.md) is the current question list. Q3 needs no text change. Q7 stays unadopted; the current exit rule (E14) matches Alex's written §3.6.
- The `_dev/runs/v1.11_*` folders have been reviewed; their instruction copies are deleted. Delete the folders once nothing more is needed from their logs.

## Next work

1. **Test v1.13 on unseen filings, only on Austin's explicit command.** Three or four Opus runs cost about $15–20. Unseen deals have no ground truth; the method that worked on 21 September is one fresh reader agent per deal checking the workbook against the filing, with Austin spot-checking its findings in the cockpit. Watch round maps first: they were the unstable part under every earlier version.
2. Open design question from Austin: DeepSeek as a cheap first pass with Opus reviewing. Not decided.
3. Not approved, do not build: extra checker rules, an "Unclear" finality value, paragraph-indexed filing text, the staged pipeline.
4. When Alex is reachable: the convention questions in RESEARCH_QUESTIONS.md and Q7.

Commit and push only when Austin asks.
