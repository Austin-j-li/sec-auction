# Model comparison runs, 28–29 September 2026

This folder records the isolated comparison runs made on the VM under Version 1. The run folders in `_dev/runs/` were deleted on 3 October 2026, after this record was made. Event logs, prompts and sandbox inputs are not kept.

## What was run

- **Deals:** Imprivata (DEFM14A, 2016) and sTec (DEFM14A, 2013). One run for each deal and setup.
- **Runner:** `_dev/tools/sandbox/run_model.py`, root instruction (Version 1), one filing in each sandbox.
- **Claude Code:** Opus runs on 2.1.281, Sonnet runs on 2.1.284. Sol and Astra runs used Codex.
- **Checker:** `check_lean.py`, run again on 3 October 2026 on each kept workbook.

| Setup | Deal | Minutes | Cost (USD) | Output tokens | Checker | Grader rank |
|---|---|---|---|---|---|---|
| Opus 5.5 medium | Imprivata | 9.9 | 2.47 | 65,711 | pass, 7 warnings | 1st of 3, twice |
| Opus 5.5 medium | sTec | 11.2 | 2.88 | 73,942 | pass, 5 warnings | 1st of 3, twice |
| Opus 5.5 high | Imprivata | 11.7 | 2.97 | 77,154 | pass, 5 warnings | not graded |
| Opus 5.5 high | sTec | 14.5 | 3.61 | 96,834 | pass, 5 warnings | not graded |
| Sonnet 5.5 high | Imprivata | 8.8 | 1.42 | — | **fail**, 1 error | 3rd |
| Sonnet 5.5 high | sTec | 10.8 | 1.79 | — | **fail**, 1 error | 3rd |
| Sonnet 5.5 xhigh | Imprivata | 17.5 | 3.21 | — | pass, 11 warnings | 2nd |
| Sonnet 5.5 xhigh | sTec | 19.6 | 3.62 | — | pass, 7 warnings | 2nd |
| GPT-6.1-Sol high | Imprivata | 16.3 | — | 26,203 | pass, 1 warning | 3rd |
| GPT-6.1-Sol high | sTec | 14.3 | — | 24,682 | pass, 3 warnings | 3rd |
| GPT-6.1-Sol xhigh | Imprivata | 23.6 | — | 40,268 | pass, 1 warning | 2nd |
| GPT-6.1-Sol xhigh | sTec | 18.4 | — | 32,396 | pass, 2 warnings | 2nd |
| GPT-6 Astra medium | Imprivata | 9.3 | — | 15,307 | pass, 1 warning | not graded |
| GPT-6 Astra medium | sTec | 7.8 | — | 13,953 | pass, 3 warnings | not graded |
| GPT-6 Astra high | Imprivata | 10.5 | — | 17,155 | pass, 1 warning | not graded |
| GPT-6 Astra high | sTec | 10.0 | — | 17,403 | pass, 1 warning | not graded |

Codex reports no cost, so the Sol and Astra cells are empty. Checker warnings count review leads, not errors.

## Blind grading

Opus 5.5 graded each deal twice, each time with three workbooks labelled A, B and C. The grader saw only the instruction, the filing text, the three workbooks and their checker reports. The prompt for the Sol grading is [verdicts/grader_prompt.md](verdicts/grader_prompt.md); the Sonnet grading prompt was not kept.

1. **Sonnet 5.5 against Opus medium** (28 September). Opus medium came 1st on both deals, Sonnet xhigh 2nd and Sonnet high 3rd. On Imprivata, both Sonnet workbooks treated the deal as one sale process. The grader held that the 90-day rule (E5) gives two processes, so Initiation is bidder-led. Verdicts: [Imprivata](verdicts/sonnet55_imprivata.md), [sTec](verdicts/sonnet55_stec.md); labels in [sonnet55_mapping.json](verdicts/sonnet55_mapping.json).
2. **GPT-6.1-Sol against Opus medium** (29 September). Opus medium came 1st on both deals and Sol xhigh 2nd. On Imprivata the gap was about four rows, but they decide the round count, the final-round Formal bidders and Sponsor B's exit. On sTec the gaps were negligible to small. Verdicts: [Imprivata](verdicts/sol61_imprivata.md), [sTec](verdicts/sol61_stec.md); labels in [sol61_mapping.json](verdicts/sol61_mapping.json).

The Opus high and Astra runs of 28 September were never graded. Their workbooks are kept in [workbooks/](workbooks/), named `<deal>-<setup>-r1.xlsx`.

## Limits

- Two deals and one run for each setup cannot separate model differences from run-to-run noise.
- The grader is an Opus model. It may prefer Opus's style even when it does not know the source.
- Imprivata is not in `raw_filing/`. Its filing reached the runs as a packet input.

## Conclusion at the time

Opus 5.5 at medium effort stayed the default extraction model (AGENTS.md).
