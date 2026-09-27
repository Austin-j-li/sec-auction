You are reviewing a proposed change to a research data-extraction instruction. Work only from the files in this folder. Do not write or edit any file; reply in text.

Files:
- `SEC_Deal_Ledger_Extraction_Instruction.md`: the current frozen instruction (v1.13.2). Part A states what the ledger is for; E11 (Formality), E12 (Conditions) and E13 (Price and consideration) are the rules this proposal touches; D1 lists the ledger columns.
- `TAXONOMY_DRAFT2.md`: the proposal under review. It adds coded columns for a bid's consideration mix and conditions.
- `filings/`: plain-text versions of twelve SEC merger filings. The bids are described in each filing's "Background of the Merger" (or "of the Offer") section.

Context: the researchers (Austin Li and Alex Gorbenko) estimate takeover auctions in which targets first collect informal bids and then formal bids. An LLM will fill these columns from one filing at a time, and an expert will check the workbook by hand. The researchers have already decided the following; do not argue against them, but do point out edge cases they create:
1. There is no separate cash/stock Consideration column; Stock % carries the consideration mix.
2. In Financing, highly confident letters and uncommitted financing are both coded Contingent.
3. Termination fees and reverse termination fees are out of scope.

Review the proposal for:
1. **Codability.** Search the Background sections of several filings for how bids describe diligence, financing, regulatory/antitrust approval, exclusivity, CVRs/earnouts and cash/stock consideration. Try coding real bids. Report bids where no value fits, where two values fit, or where the value would need outside knowledge. Cite the file and a short exact quote.
2. **Definitions.** Ambiguous boundaries between values, precedence gaps, values that will be over- or under-used, and whether the Not stated / negative distinction and the no-carry-forward rule will work in practice.
3. **Research fit.** Whether the columns serve Part A, especially use 3 (reinterpreting a formal but heavily conditional bid as informal), and whether any condition the researchers named is poorly captured.
4. **Consistency** with E11–E13 and the rest of the instruction, including the proposed checker rules in section 4, and whether the two open decisions in section 5 have a better answer.
5. **Data design.** Column types (e.g. Stock % mixing numbers and text codes), marker columns (Y or blank), cohort rows, and evidence.

Output, at most 1,500 words:
- A one-paragraph verdict.
- Issues ranked by importance. For each: the problem, a filing example if you found one, and the exact replacement wording you propose.
- A short list of parts that work as drafted.
