# TypeSafe follow-up experiment plan — 19 September 2026

Scope: read-only, post-extraction research using the three public filings. No workbook generation, instruction changes, or production integration. Existing Jev experiments are development context, not independent validation. New outputs stay in this folder.

Before API results are observed:

1. **Price binding:** source-authored cases with correct prices and deliberately wrong prices that occur nearby (other bidder, earlier/later offer, or cash component). Compare the earlier actor-only Noul question with an event-specific three-way support question and source-candidate selection. Include missing-evidence controls. Candidate selection is a verification experiment, not a new deal extraction.
2. **Coverage:** source-authored target events and constructed candidate ledger rows: correct, paraphrased, absent, and plausible distractors. Compare a binary match question with selecting an actual matching row or none. This tests matching given a known event, not discovery of every event.
3. **Financing evidence:** distinguish explicitly committed financing, explicitly missing commitment, and silence. Compare a broad Heavy-condition classification with narrowly reading the financing evidence. Overall condition labels require wider context and are not scored as gold.

Use jev-1.13.0. Freeze cases and labels before calls; keep labels outside requests. Source labels are this assistant's reading, not Alex-approved gold. Fixed diagnostic thresholds: Noul 0.5; Choice argmax; separately show confidence >=0.9, without calling it calibrated. No tuning on results. Every request and response is saved without credentials. Report raw counts, failures, latency, token usage and documented-price estimate. Budget at most 200 requests in this run, concurrency 4, no unbounded retries. Cache subsequent replay; repeats must explicitly bypass cache. No third-party LLM control is authorized by the provided key.

Sources: live TypeSafe docs in `docs/`; raw SEC HTML in `raw_filing/`; working C14/C15 instructions for interpreting domain rules. The pre-existing `_dev/jev_experiments_2026-09-19/RESULTS.md` motivates harder controls but its figures are not new results.
