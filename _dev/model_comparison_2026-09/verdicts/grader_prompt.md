You are grading three extractions of the same SEC merger filing. Work only with the files in this folder; do not open any other path.

- `INSTRUCTION.md` is the extraction instruction the three extractors were given. It defines the workbook, the evidence standard and every coding convention.
- `FILING.txt` is the filing, converted from HTML to text. The "Background of the Merger" section is the main source.
- `WORKBOOK_A.txt`, `WORKBOOK_B.txt`, `WORKBOOK_C.txt` are the three workbooks, one sheet after another, each row tab-separated with its row number first.
- `CHECKER_A.json` etc. are the offline mechanical checker's reports. The checker tests structure, dates, labels and that quotes occur in the filing; it does not judge whether a coding is right.

The three workbooks were produced independently, under the same instruction, by different extraction setups. You are not told which setup produced which, and nothing about the setups matters: judge only the work.

Your job is to decide which workbook a researcher should trust most, and how far apart they are.

1. Read the instruction in full, then the Background section of the filing in full, before judging any workbook. Build your own understanding of the process: the parties, contacts and confidentiality agreements, each bid with its date, price, form and conditions, the rounds and deadlines, and how and when each party left.
2. Compare the three workbooks against the filing and the instruction. Where they disagree, go to the filing text and decide which (if any) is right under the instruction. Where all three agree, spot-check against the filing anyway.
3. Count only errors you have verified against the filing text, and quote the passage that settles each one. When the instruction leaves a reading genuinely open and a workbook records that in its Questions sheet, that is not an error. Where you are unsure, say so rather than counting it.
4. Weigh errors by what they would do to research on informal and formal bidding: a missing or invented bid, a wrong price, a wrong Formality, a wrong exit date or reason, or a wrong bidder count matters more than wording in a Note or a slightly different quote.

Write your report to `VERDICT.md` in this folder with these parts:

- **Ranking**: best to worst, with a one-line reason each, and whether the gap between each pair is large, small or negligible.
- **Scores** for each workbook, 1–10: completeness (every event and party the instruction requires), accuracy of codings (dates, prices, Formality, conditions, rounds, exits, counts), evidence (quotes support what the row claims), handling of uncertainty (Questions sheet: real open readings flagged, nothing invented, nothing overclaimed), and instruction compliance.
- **Verified errors** per workbook: a table with sheet and row, what it says, what it should say, the filing passage, and severity (high / medium / low).
- **Where they differ**: the material disagreements between workbooks and which is right.
- **Fit for research**: for each workbook, whether a researcher could use it after light review, after substantial correction, or not at all.

Be concrete and brief. Do not rewrite the workbooks.
