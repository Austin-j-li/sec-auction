# Medivation participation diagnostics

Reviewed at commit `cb7bfba4f11624cd2984c86fd4d4f93a60574dd5` on 12 October 2026.

**The Astra and Sol diagnostics expose a program defect. They do not show missing admissions or exits in those workbooks.** Opus has a separate cohort-mapping issue. Do not rank these extractions by their manifest review counts.

I read the three completed Medivation workbooks and their saved analysis files. I called the current program's `load()` and `derive()` functions on each original workbook. The reported diagnostics match the saved manifests. I used no assertions, test suite, model calls, or revised inputs. Only this report was added.

Workbook references below use the ledger's `#`. The Excel row number is one greater.

| Model | Original workbook | Manifest review items | Final exported `(live_lo, live_hi, live_point)` |
| --- | --- | ---: | --- |
| Astra | [Workbook](../runs/medivation-gpt-6-astra-xhigh-r1/medivation.xlsx) | 5 | `(0, 0, blank)` |
| Sol | [Workbook](../runs/medivation-gpt-6.1-sol-xhigh-r1/medivation.xlsx) | 5 | `(0, 0, blank)` |
| Opus | [Workbook](../runs/medivation-opus-5-5-xhigh-r1/medivation.xlsx) | 2 | `(0, blank, blank)` |

In these exports, a blank upper bound means unbounded; a blank point means unknown. Neither means zero.

## 1. P1 program defect: explicit stage admissions never enter the population

**Location:** [derive_analysis.py:49](../../tools/derive_analysis.py#L49), entry dispatch at lines 572–614, and exit subtraction at lines 623–640.

`ENTRY_EVENTS` includes NDA and bid events. It excludes an `Other material event` that records target admission. E3 expressly makes target admission an entry: [instruction, line 161](../../../SEC_Deal_Ledger_Extraction_Instruction.md#L161).

The source states that Pfizer advances with several other interested parties on August 10. It does not identify those parties as the earlier NDA cohort. See [filing, lines 1495–1496](../../cockpit/state/filings/medivation/medivation_2016-08-30_SCTO-T.htm#L1495).

The relevant raw rows are:

| Model | Row | Raw event and Who | Raw Count and Note |
| --- | ---: | --- | --- |
| Astra | 19 | Other material event; Other August 10 invitees | Blank. `Admit. Count: several other interested parties; identities and overlap with earlier NDA signers unreported.` |
| Astra | 25 | Dropped by target; Other August 10 invitees | Blank. `Count: several other interested parties. not invited; only Pfizer is identified in the best-and-final request. Also p. 23.` Inferred = Y. |
| Sol | 18 | Other material event; Several other round-2 parties | Blank. `Admit; Count: several other interested parties; individual identities not reported.` |
| Sol | 24 | Dropped by target; Several other round-2 parties | Blank. `Count: several other interested parties; not invited to the best-and-final stage; no later offer or continued admission reported. Also p. 23.` Inferred = Y. |

Both workbooks close the earlier NDA residual at #15 and Sanofi at #17. The later admission therefore records an active cohort absent from the remaining population. Unknown historical overlap does not justify ignoring its current admission. Neither workbook asserts an identity that would require a named re-entry row.

The program omits Astra #19 and Sol #18 from `participation.csv`. It later subtracts their exits because an earlier cohort once existed in the process. At those exits, its population contains only Pfizer.

For both exits, the exported count bounds are `(2, unbounded)`. The deltas are `(unknown, -2, unknown)`. The population changes from `(1,1,1)` to `(0,0,unknown)` after zero-clamping. Lines 536–542 retain an unknown point marker despite the exact zero bounds. The same-day opening adjustment transfers this state to round 3.

| Exported observation | Astra row | Sol row | Current output | Required by these workbooks' own sequence |
| --- | ---: | ---: | --- | --- |
| Pfizer $77 bid | 23 | 22 | Live `(1,1,1)` | Live lower bound 3; upper bound and point unknown |
| Round 3 | Rounds row 4 | Rounds row 4 | Opening `(0,0,unknown)`; `admitted_hi=0` | One live and admitted bidder: Pfizer |
| Pfizer $81.50 bid | 27 | 26 | Live `(0,0,unknown)` | Live `(1,1,1)` |
| Pfizer signs | 28 | 27 | Live `(0,0,unknown)` | Live `(0,0,0)` |

The lower bound of three uses the program's existing `several >= 2` convention, plus Pfizer. It is not an exact rival count. The source separately confirms Pfizer's final bid and signature: [lines 1519–1521](../../cockpit/state/filings/medivation/medivation_2016-08-30_SCTO-T.htm#L1519).

This causes three downstream review items: exit without entry, final unknown population with bounds 0–0, and one reported round-3 bidder exceeding `admitted_hi=0`. Treat them as one program cause. The two residual-count review items are expected uncertainty notices.

**Impact:** The export removes real competitors at the $77 bid and even removes the bidder that submits the final bid. These fields cannot support a competition measure as exported.

**Smallest verification:** Run the real derive functions on either unchanged workbook. Inspect the admission row, its paired exit, and the two later bid populations. A repair must recognize target admissions without duplicating already-live parties. This report changes no code or input.

This is a newly demonstrated defect in the existing entry logic. The evidence does not establish that PR18 introduced it.

## 2. P2 workbook issue: Opus equates cohorts that the source does not identify

Opus #9 records `Other NDA signers`, with blank Count and Note `Count: ‘several parties, including Sanofi’, less Pfizer and Sanofi.` It derives as `(0, unbounded, unknown)`.

Opus omits an August 8 closure for that cohort. Its round-2 opening, #15, records the August 10 invitation. Questions Q1 expressly recommends uninterrupted participation by the same cohort.

Opus #21 closes `Other NDA signers` on August 19. Its Note instead uses `Count: ‘several other interested parties’ invited 08/10/2016 with Pfizer; no reported offer. Also p. 22`. This derives as `(2, unbounded, unknown)`.

The source establishes both groups, but supplies no identity match: [earlier NDAs, lines 1467–1468](../../cockpit/state/filings/medivation/medivation_2016-08-30_SCTO-T.htm#L1467), and [later invitees, lines 1495–1496](../../cockpit/state/filings/medivation/medivation_2016-08-30_SCTO-T.htm#L1495). E14(4) closes the unnamed initial cohort at its first due date. The exception in E14 line 336 names closing events 1 and 3, not event 4.

The code cancels an inexact entry only when its bounds equal the exit's bounds, at lines 635–640. Here `(0,None,None)` differs from `(2,None,None)`. The program therefore preserves uncertainty and exports final bounds `0–open`, with an unknown point. Its final warning is not the same zero-bound contradiction seen for Astra and Sol.

The wide Opus bound is conservative given the conflicting population bases. It is not proof that an actual rival remains after signing. Automatic cancellation would silently accept the workbook's unsupported identity assumption. Repair the cohort history before assigning an exact terminal count. This evidence does not establish a separate program regression for Opus.

**Smallest verification:** Compare Opus #9, #15, #21, and Questions Q1 with the two source passages and E14. Retain this as one continuity finding, not separate penalties for the warning and changed bounds.

## Ranking consequence

Astra and Sol record the admission and later exit that the program fails to consume. Give neither a source-accuracy penalty for these three downstream diagnostics. Their five review items do not make them worse than Opus with two.

Opus's unsupported cohort continuity belongs in its source review. Its unknown terminal export is not an additional independent extraction error. This diagnosis supports keeping the existing source-based comparison separate from program acceptance. It does not decide the models' overall ranking, other deals, financing, or final-stage interpretation.
