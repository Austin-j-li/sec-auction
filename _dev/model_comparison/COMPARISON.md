# Blind model comparison — patched v1.8 lean

> Note (20 Sep 2026): this folder is a slimmed record. Links below to `grading/<deal>/work/output/...` now resolve to `grading/<deal>/`; run logs, the Sol and DeepSeek workbooks and admin scripts are in git history (see `_dev/CHRONOLOGY.md`).

All nine requested extractions and blind grading are complete. **Claude Opus 5 high has the highest mean score in this three-deal experiment: 96.42/100.** This is a small development-set result, not a general model ranking or acceptance of the workbooks as research-ready.

| Model / effort | Mac-Gray | PetSmart | Providence–Worcester | Mean / 100 | Critical root causes |
|---|---:|---:|---:|---:|---:|
| Claude Opus 5 high | 93.25 | 96.00 | 100.00 | **96.42** | 0 |
| GPT-5.6-Sol xhigh | 87.25 | 91.00 | 83.00 | **87.08** | 3 |
| DeepSeek V4.1 Flash max | 90.75 | 78.50 | 90.50 | **86.58** | 2 |

Scores measure the frozen weighted tests. Critical errors are separate source-reviewed root causes, not extra score deductions. The same root cause may affect several research fields. In particular, 100/100 on Providence means passing its 33 weighted tests; its unscored notes and Questions still contain errors.

## Concrete findings

### mac-gray

- **Claude Opus 5 high (Candidate-B):** Highest Mac-Gray score; preserves the three-round structure, all 13 bids/reaffirmations and explicit contact cohorts. Still omits buyer-bank adviser events and September 27 voting-agreement formation; some conditions/date judgments need qualification.
- **GPT-5.6-Sol xhigh (Candidate-C):** Adds an extra August 27 round where the grader finds a deadline announcement within the July 25 stage. This shifts later round labels (ledger rows 29-50, Rounds rows 3-5). All 13 economic bid/reaffirmation events and numeric prices remain intact.
- **DeepSeek V4.1 Flash max (Candidate-A):** Preserves the three-round structure and all 13 bid/reaffirmation events. Missing aggregate Contact and several adviser/access events; Party A NDA is assigned to the wrong round. No critical error under the frozen rubric.

Evidence: [full scoring notes](grading/mac-gray/scoring_notes.md), [test-by-test scores](grading/mac-gray/scores.json), [source reference](grading/mac-gray/reference.md). Row numbers above are worksheet rows unless stated otherwise.

### petsmart

- **Claude Opus 5 high (Candidate-C):** Highest PetSmart score; retains the separate third initial qualifying indication, net one-unit group reduction and deadline extension. Still over-links anonymous price histories, needs tighter date bounds and contains some unsupported adviser/financing qualifiers.
- **GPT-5.6-Sol xhigh (Candidate-A):** Correct main participation path and separate third qualifying initial indication. Uses constituent Count 2 at joint-unit formation with a clarifying Question; normalize the net reduction to 1. Anonymous price-slot links and deadline consistency still need correction.
- **DeepSeek V4.1 Flash max (Candidate-B):** Records Count 2 when the single Bidder 3 group exits on December 10 (ledger row 31), corrupting the live-bidder arithmetic. Also misses a separate initially qualifying indication and part of the December deadline history.

Evidence: [full scoring notes](grading/petsmart/scoring_notes.md), [test-by-test scores](grading/petsmart/scores.json), [source reference](grading/petsmart/reference.md). Row numbers above are worksheet rows unless stated otherwise.

### providence-worcester

- **Claude Opus 5 high (Candidate-C):** Passes all 33 frozen weighted tests, including re-entry and late-stage competition. Still needs corrections to Party A statements in Questions, a catch-up-access date bound, the unscored transaction-expense caveat and an ambiguous final-signing note. A 100 score does not mean an error-free workbook.
- **GPT-5.6-Sol xhigh (Candidate-A):** Codes the July CVR packages as noncash without settlement support and Party B as Dropped by target rather than Not selected at signing (ledger rows 34-35 and 53). Also misses Party B August 4 reaffirmation.
- **DeepSeek V4.1 Flash max (Candidate-B):** Keeps Party E live until signing despite an earlier named continuation set, overstating late competition (ledger rows 43,45,51; Rounds row 4). Also leaves several LOI upper bounds too late.

Evidence: [full scoring notes](grading/providence-worcester/scoring_notes.md), [test-by-test scores](grading/providence-worcester/scores.json), [source reference](grading/providence-worcester/reference.md). Row numbers above are worksheet rows unless stated otherwise.

## What this says about the new instruction

The project now has a compact 22-column ledger with four sheets, and explicit rules for re-entry and target-organized rounds. This experiment tested the patched instruction verbatim. The current instruction and full filing governed scoring; Alex’s hand rows and voice notes were assessed separately for compatibility. Earlier hand-coded conventions were not treated as automatic ground truth.

The outputs generally preserve major prices and bid sequences. The remaining differences concentrate on reconstruction of competition: group counts, round boundaries, closing out bidders, and distinguishing reported dates from inferred bounds. The Mac-Gray extra-round error shows that the round patch does not eliminate all interpretation differences. PetSmart still exposes the difference between constituent firms and one joint bidding unit. Providence still exposes the need to close a bidder at an earlier named continuation set rather than defaulting to signing.

This experiment does not identify the causal effect of the patch: there is no matched unpatched control or repeated sampling here. It supplies a clean baseline for the next unseen filings. No instruction edits were made.

## Isolation and blind evaluation

1. Each extractor had a fresh bubblewrap session, one identical instruction and one full filing, plus runtime tools and minimal provider authentication. No researcher answers, project history, previous outputs, personal memory or shared agent context were supplied. All nine used identical prompt bytes within each deal.
2. The actual clients were Codex 0.155.1 (gpt-5.6-sol, xhigh), Claude Code 2.1.278 (claude-opus-5, high), and OpenCode 2.0.9 (deepseek/deepseek-flash, max). Claude and DeepSeek connectivity and tool execution were tested before the experiment. The API networking path remained available; isolation was not an OS-enforced API-only egress firewall. Command-log review found no outside-source retrieval.
3. Fresh GPT-6-Astra high sessions built source-only references before seeing candidates: 45 Mac-Gray tests, 40 PetSmart tests, 33 Providence tests. A separate fresh session per deal graded all three candidates against that locked reference.
4. Candidate identities were independently randomized for each deal. Workbook creator/application metadata and archive timestamps were neutralized; cell data, formulas and styles were preserved. Original workbooks were kept byte-for-byte. The graders could see neutral candidates, filings and source references, but not model maps or extraction logs. Writing style could still provide clues, so this is identity masking rather than a guarantee against inference.
5. All 354 candidate/test credits were recomputed. Source references, scores and notes were hashed before model identities were revealed. A fresh identity-blind adjudicator resolved the one reference amendment before unblinding. The administrator did not revise scores after revealing identities.

Each deal has 100 points: participation 30; rounds 25; formality and conditions 20; chronology 10; bids/prices 10; other material coverage 5. Credits are 0, 0.5 or 1 per fixed test. The three deals have equal weight in the model mean. No points are awarded for verbosity, formatting or question count.

The lean-schema mechanical checker runs outside the extracting sandbox. Version 1.1 was applied uniformly to all nine candidates; it corrects overly strict parsing of explanatory labels and treats broad Question links as review leads. Its quote matches and counts are diagnostic leads, not semantic judgments. Original version-1 reports remain archived.

## Reference correction

AM01 corrects the Providence reference: Annex A-48 explicitly describes the Company–Parent confidentiality agreement as dated April 3, 2016. The original inventory overgeneralized that individual NDA dates were absent. A fresh blind adjudicator checked the parties, passage, relevant rows and T01 treatment. The amendment changes no candidate score and adds no new weighted test. “Dated” does not independently establish when signatures were delivered; the exact-date note should cite the annex.

The original reference is preserved. See the [independent adjudication](grading/providence-worcester/work/output/adjudicate/adjudication.md), [original blind score lock](admin/blind_score_validation.json), [final blind lock](admin/final_blind_lock.json), and [timestamped identity reveal](admin/unblinding.json).

## Execution and review burden

| Model | Mean extraction time | Ledger rows, all 3 | Words per ledger row | Questions, all 3 |
|---|---:|---:|---:|---:|
| Claude Opus 5 high | 8.13 min | 145 | 63.8 | 19 |
| GPT-5.6-Sol xhigh | 13.08 min | 152 | 50.7 | 13 |
| DeepSeek V4.1 Flash max | 10.62 min | 139 | 57.7 | 16 |

Times are observed wall-clock extraction times under concurrent local runs, excluding preflight, reference building and grading. Counts and text volume are review-burden proxies; no human correction minutes were measured. Detailed per-candidate review and compatibility observations are in the scoring notes.

DeepSeek’s client reported approximately $0.348 for its three extractions. Claude’s CLI reported approximately $9.045 at list-rate valuation for its three extractions; this is not the marginal subscription charge. Sol billing was unavailable. These are client estimates, not verified invoices, and should not be treated as a complete comparable cost study. Token accounting differs across clients.

## Deliverables and limitations

- [All nine original workbooks](nine_workbooks.zip), organized by model and deal, with SHA256 checksums.
- [Machine-readable results](comparison_scores.json) and [CSV scores](comparison_scores.csv).
- [Input/model manifest](MANIFEST.json), [execution inventory](admin/run_inventory.json), [integrity verification](admin/final_integrity.json), and [frozen rubric](admin/RUBRIC.md).
- Per-deal source references, detailed row-level scoring notes, Questions and Alex-compatibility assessments are linked above.

All nine sessions exited successfully and produced readable four-sheet workbooks. Input hashes match the frozen manifest; collected workbooks and archive entries match original run outputs. The experiment did not visually render the workbooks. No commits or pushes were made.

There is one run per model per deal, only three development filings, one grader model family, and no human adjudication of all 118 tests. Reference construction itself can miss facts, as AM01 illustrates. The ranking therefore supports choosing the next validation run; it does not establish statistical superiority or readiness for unattended production. Fix the listed substantive errors before accepting these rows into the research dataset.
