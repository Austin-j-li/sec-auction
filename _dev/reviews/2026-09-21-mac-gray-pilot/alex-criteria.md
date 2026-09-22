# Mac-Gray: what the voice comments test

Source: `ref/alex_voice_notes_2026-08.docx`, section II, Word document paragraphs 36–52 (paragraphs counted in document XML). Alex discussed an older AI database, not the current v1.13 workbook. These comments select evaluation dimensions; the filing and frozen instruction determine whether current rows are errors.

| Criterion | Alex comment | Source / current-rule check |
| --- | --- | --- |
| A01 | Target approached A first, then A returned with an unsolicited bid; initiation is mixed. | April 8 target-directed call (p.27); June 21 bid (p.30). Keep both and the sequence. |
| A02 | Record the outreach, rather than only a participation total. | Decision June 24; 50 contacts during following weeks, 15 strategic and 35 financial (pp.31–32). The decision date is not automatically every contact's exact date. |
| A03 | Do not double-count named NDA signers or invent unnamed strategic signers. | 20 overall = A + CSC/Pamplona + B + C + 16 other financial. B June 28, C June 30, CSC July 11, A August 5 (pp.32–34). |
| A04 | Round 1 and its deadline must be identifiable. | June 24 decision launching outreach; July 23 due date (pp.31–33). B/C late submissions were accepted. |
| A05 | Second informal stage opens July 25; its September 9 deadline is announced August 27. | Four parties advance to management meetings, staged disclosure and revised offers (pp.33–35). |
| A06 | Store financing and diligence conditions with bids. | CSC/Pamplona financing commitment vs B's missing commitment September 9; A and C similarly lack commitments September 10 (p.35). |
| A07 | The final-stage A range can be Formal. | September 11 final solicitation, September 18 best-and-final reiteration (p.36); E11 and current Conditions convention assessed separately. |
| A08 | Exclusivity does not itself make a Formal bid Informal. | E11 preserves Formality; E12 separately classifies reported conditions. A disagreement over Heavy/Light is not an error in Formality. |
| A09 | Avoid invented or wrongly dated exits. | Party C did not submit September 18 (p.36); A and B remain rival bidders displaced by executed exclusivity September 24 (p.38). Alex's paragraph 50 says B and C were dropped at exclusivity; this conflicts with the source's reported C non-submission. Do not reproduce it as ground truth. |
| A10 | Goodwin's adviser row should start at earliest reported action, not at signing. | May 9 (p.27). BofA's earlier acquisition mandate was expressly terminated and a new mandate engaged (pp.27–30); D2 uses one row per relationship, not an unconditional one-row-per-firm rule. |

## Pre-output baseline assessment

The current v1.13 workbook already satisfies most of these broad checks: April target interest, three stages, the named NDA dates and total, per-bid Conditions, Formal final-stage offers, C's September 18 non-submission, A/B's September 24 inferred exits, and signing separately from announcement. Those cannot be counted as improvements from this new run.

The baseline's 16-person anonymous NDA cohort has a June 24–August 24 window (#19), but all 16 are closed by July 23 (#22) and Rounds describes 19 first-stage signers while admitting some could sign later (Q3). The new extraction must be judged on how it represents that temporal uncertainty, not just whether its eventual total adds to 20.

This case can reveal residual errors and whether a fresh audit helps. It cannot measure generalization, isolate the effect of the E6 wording repair from run variation, or establish human review time saved.
