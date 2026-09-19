# Scoring rubric: one deal, several candidate ledgers

You are scoring AI-made "deal ledgers" of one merger against (a) the filing's Background section, which is the ground truth, and (b) Alex Gorbenko's hand-coded rows and voice notes, which say what the researcher wants. The candidates carry neutral labels. They come from different instructions and have different column layouts. Score content, not layout. Do not guess which instruction produced which candidate and do not reward or punish length as such.

Files (all under this deal's folder): `filing_background.txt`, `alex_hand_rows.txt`, `alex_voice_notes.txt`, `../alex_closing_summary.txt`, and one `<label>.txt` dump per candidate (the full workbook is `<label>.xlsx` if you need it).

Rules of adjudication
- Where a candidate disagrees with Alex's hand rows, check the filing before scoring. If the filing supports the candidate, the candidate is right and you note "hand data differs". Alex's hand rows contain some errors and some legitimate alternative conventions.
- Build the reference list ONCE, before looking at any candidate: every priced proposal in the filing (bidder, date, low, high, per-share or not, stated formality signals), the rounds (what opened each, when, deadline, who was invited, who submitted), the NDA and contact counts by type, every exit the filing states, signing and announcement dates, advisers. Save it as `reference.md`. Then score every candidate against the same reference.
- Use the same strictness for every candidate. A tolerance of 3 days applies to assigned dates of events the filing dates only roughly; exact dates must match exactly.

Score these items for each candidate
1. **Priced bids.** For each reference priced proposal: present as its own row? bidder right? low and high right? formality as Alex would label it (raw), and formality after mapping "Formal with Heavy conditions" to Informal (mapped)? List misses, merged bids, wrong prices, and extra bid rows that are not real proposals.
2. **Rounds and processes.** Number of processes and rounds versus the reference and Alex. For each round: opening date, deadline, finality. Is each bid placed in the right round? Is the ledger's own round numbering coherent when read top to bottom?
3. **Live bidders.** Number of live bidders at each round boundary and at signing, as implied by the ledger's entry and exit rows, versus the reference. Does every confidentiality-agreement signer who did not win get accounted for exactly once? Any double close-out, any bidder left open, any exit before entry?
4. **Order.** Count pairs of bid or exit rows whose ledger order contradicts the filing's chronology.
5. **Counts.** Contacted and NDA totals, by strategic/financial where the filing gives it. Any "at least" where the filing is exact, any double counting.
6. **Alex's checklist.** Go through the numbered points of Alex's voice notes for this deal. For each: satisfied, violated, partly, or not applicable, with one line of evidence.
7. **Factual errors.** Statements in the ledger that the filing contradicts or does not support (invented facts, wrong date, wrong price, wrong party). Count and list. Separate "serious" (changes a first-order variable: price, formality, round, live-bidder count, order of bids) from "minor".
8. **Omissions Alex would want** (adviser, target or bidder initiation, sale announcement, signing and announcement as separate events, deadline set versus reached) and **rows Alex would delete** (count, with two or three examples).
9. **Review burden.** Would a researcher reading this ledger beside the filing be able to verify it quickly? Note anything that helps or hinders (flag column that flags everything, long cells, questions that bury the open calls, a clear rounds overview).

Output
- `scores.json`: `{"deal": ..., "reference": {"priced_bids": N, "rounds": N, "nda_total": N, "live_at_signing": N}, "candidates": {"<label>": {"bids_present": n, "bids_price_right": n, "bids_formality_raw_right": n, "bids_formality_mapped_right": n, "bids_missed": n, "bids_spurious": n, "rounds_count_right": true/false, "round_opening_dates_right": "k of N", "bids_in_right_round": "k of N", "live_bidder_counts_right": "k of N boundaries", "signers_accounted_once": true/false, "double_closeouts": n, "order_inversions": n, "counts_right": "k of N", "checklist_satisfied": n, "checklist_partly": n, "checklist_violated": n, "checklist_na": n, "factual_errors_serious": n, "factual_errors_minor": n, "omissions": n, "rows_alex_would_delete": n, "overall_0_to_10_for_alex": x}}}`
- `scoring_notes.md`: the evidence behind every number, candidate by candidate, short. End with a ranking for this deal and the two or three differences that actually matter for the research.
Be exact and even-handed. Do not read anything outside this deal's folder and its parent's `alex_closing_summary.txt`. No internet.
