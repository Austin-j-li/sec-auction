# Current development handoff — 21 September 2026

**Settled on 21 September:** the working instruction is **v1.13** and **Claude Opus 5 high is the single extractor**. The checkout holds only current material. Every earlier instruction, decision record, review, run folder and old workbook lives in git history only ([CHRONOLOGY.md](CHRONOLOGY.md) gives the commits); keep it that way so no agent reads a past version by mistake.

v1.13 is an objective-led text of 5,600 words: what the ledger is for, the evidence standard, a work process with finish conditions, the workbook, fourteen fixed conventions (E1–E14), questions and delivery. The workbook format is unchanged from v1.11: 22 ledger columns and four sheets (Deal ledger, Rounds, Questions, Deal facts). [DECISIONS_v1.13.md](DECISIONS_v1.13.md) lists what changed. **No extraction has run under v1.13 as it now reads, and none under any version on a filing nobody has studied.**

The eight workbooks in `extraction/` (kraton, mac-gray, meredith, penford, petsmart, providence-worcester, stec, synacor) are Opus 5 high runs under **v1.11**. They pass the mechanical checker and are not research-ready. They stay because the review cockpit serves them; replace them when Austin orders a v1.13 run of the eight.

## How Austin wants the instruction changed

Change the instruction only where the change is general: the research objective, the work process, honesty about uncertainty, a repaired contradiction, a deletion. Never add a rule whose only justification is one reviewed deal; that overfits, and a capable agent should reach such calls by judgment from the objective. Prefer fewer moving parts: Austin declined extra checker rules, an "Unclear" finality value, paragraph-indexed filing text and the staged pipeline. Alex Gorbenko is out of reach for now, so conventions are Austin's to set provisionally. Every instruction edit still needs Austin's approval.

## What 21 September established

All of it rests on model readers checking workbooks against filings; no human has adjudicated more than a handful of findings. The eight deals shaped v1.12 and v1.13 and cannot test them. The records are in git: `git show acc9986:_dev/reviews/2026-09-21/README.md` (review of the v1.11 workbooks) and `git show acc9986:_dev/reviews/2026-09-21/instruction_comparison.md` (the runs below). They cite v1.12-and-earlier rule numbers, C1–C16.

- **The v1.11 workbooks.** Every bid price and bid date is correct. About 2–8% of rows per deal carry a consequential error (Meredith 12–15%), in cohort counts, exit labels and reasons, round boundaries and conditionality: values stated more exactly than the filing supports. The agents grepped slices of the filing, skipped annexes and ran the reread as a quote-matching script.
- **Instructions.** v1.12 (v1.11 plus seven general edits) and v1.12.1 (the objective-led rewrite) both beat v1.11 on Opus on Meredith, Synacor and sTec, and tied each other. Round maps were unstable under all three, which is why v1.13 defines a round as one request for offers.
- **Still wrong under every version:** Meredith's whole-company scope flag and its missing 13 April structure revision; sTec's 30 May deadline marked Enforced although later bids were taken; Synacor's 29 December "CLP's offer" with no Question raised.
- **DeepSeek flash** costs about $0.13 a deal against $4–6. It gets prices and bidders right and is unreliable on processes, rounds, closures and Conditions. Its only use is a cheap check that an instruction draft is easy to follow (its checker errors fell from 42 to 11 under the shorter text).
- **DeepSeek drafting with Opus reviewing** was tried on two deals: the same cost as a fresh Opus extraction, and the reviewer inherited the draft's round and process skeleton. Dropped.
- A second look did add something on Synacor. The open idea is the reverse order, a fresh Opus reader auditing an Opus workbook, at about double the cost. Not approved; decide after v1.13's first unseen-filing results.

## Current workflow

- [tools/README.md](tools/README.md) covers the checker, isolated runner, filing fetcher, review helpers and cockpit. The runner takes `--provider opus`, `sol` or `deepseek` and `--instruction <path>` for a candidate text. Run results go under ignored `_dev/runs/`; record what you need, then delete the folder, including its instruction copy.
- Review the workbooks in `extraction/` beside their filings in the read-only cockpit at https://lines.dealextract.org (Cloudflare Access: Austin and Alex). Service details are in the "Review cockpit" section of [tools/README.md](tools/README.md).
- `tools/check_lean.py` is the mechanical checker, version **1.5**, offline. It checks structure, quotation occurrence and agreement between columns of a row, not research correctness. A mechanical pass is not acceptance of the data.
- The runner writes tokens and cost to `status.json` and library versions to `metadata.json`; `tools/requirements.txt` is pinned.
- `raw_filing/MANIFEST.csv` is the filing index: one line per filing with its EDGAR link and SHA-256. `tools/fetch_filing.py` maintains it; for an SC TO-T tender offer it saves the offer to purchase, exhibit (a)(1)(A). `tools/make_seed.py` is a deliberate rebuild command for `ref/seed.csv`, which lists 390 deals; all but the eight here are unseen.
- [RESEARCH_QUESTIONS.md](RESEARCH_QUESTIONS.md) is the current question list. Q3 needs no text change. Q7 stays unadopted; the current exit rule (E14) matches Alex's written §3.6.

## Next work

1. **Test v1.13 on three or four unseen filings, only on Austin's explicit command** (about $15–20 on Opus). Unseen deals have no ground truth; the method that worked on 21 September is one fresh reader agent per deal checking the workbook against the filing, with Austin spot-checking its findings in the cockpit. Watch round maps first.
2. Then decide on the second Opus reader, and on re-running the eight deals under v1.13 to replace the v1.11 workbooks.
3. When Alex is reachable: the convention questions in RESEARCH_QUESTIONS.md and Q7.

Commit and push only when Austin asks.
