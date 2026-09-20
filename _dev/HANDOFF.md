# Current development handoff — 20 September 2026

The working instruction is **v1.11 lean**, with 22 ledger columns and four sheets: Deal ledger, Rounds, Questions, Deal facts. [Its decision record](DECISIONS_v1.11.md) explains the consistency pass. No extraction has tested v1.9–v1.11.

The three workbooks in `extraction/` are still the **Opus 5 high runs under v1.8**. They were selected by the blind comparison (`git show 407a6e4:_dev/model_comparison/COMPARISON.md`), and still need the corrections in its grading notes. They are not research-ready. Cleanup did not change the instruction, filings, reference data or workbooks.

## Current workflow

- Use [tools/README.md](tools/README.md) for the checker, isolated runner, filing fetcher and review helpers. Run results go under ignored `_dev/runs/`.
- `tools/check_lean.py` is the mechanical checker, version **1.4**. Its standard command is offline. It checks structure and source-quote occurrence, not substantive research correctness. A mechanical pass is not acceptance of the data.
- **Jev was deleted on 20 September 2026.** It caught planted price swaps but never a real error: no Jev finding changed a workbook in the five-deal trial, and Penford drew two false alarms. The code is in git history up to `407a6e4`.
- The checker/revision trial is **complete**, not waiting to be launched. Its results (`git show 407a6e4:_dev/revision_loop/RESULTS.md`) show mechanical cleanup, little substantive improvement, and all Jev findings rejected by the revising model. Those refusals are not independent human adjudication.
- [RESEARCH_QUESTIONS.md](RESEARCH_QUESTIONS.md) is the current question list. Prior recommendations remain provisional. Q3's one-sided-price change and Q7's Company H exit change remain unadopted.
- `tools/make_seed.py` builds identifying-only `ref/seed.csv` from Alex's workbook; it is a deliberate rebuild command. `tools/fetch_filing.py` downloads filings and records their source/hash. Existing files must match their local manifest before reuse. SC TO-T tender-offer exhibits remain unsupported.

## Next work

1. Ask Alex the current convention questions and adjudicate the disputed sTec findings against the source. The Astra grade was a model review under v1.8; several judgments were overtaken by later rules.
2. On Austin's explicit command, run isolated v1.11 extractions on sTec and Penford, then check and evaluate them outside the extractor's sandbox. These deals are useful regressions, not a clean unseen test of the instruction.
3. Update the lagging workbooks only after the validation decision. A genuinely unseen pilot would need new filings and human review.

Do not rerun the completed revision trial merely because a historical report calls it “next.” There is no archive folder: completed experiments live in git history, indexed in [CHRONOLOGY.md](CHRONOLOGY.md).
