# Three-model extraction comparison — 12 October 2026

**Astra xhigh performs best in this pilot. Sol 6.1 xhigh ranks second; Opus 5.5 xhigh ranks third.**
Astra ties Sol on Medivation and leads on Penford and Synacor. It also finishes first on every deal.
Its Penford financing omission prevents a clean accuracy verdict.

For a choice among these three tested settings, I recommend **Astra xhigh with source review**.
This is a recommendation from three development deals, not a change to the live default.
The comparison does not evaluate Sol at high or Opus at medium.

**One further pipeline repair is needed.** The exporter ignores explicit stage admissions in both GPT Medivation workbooks.
It then reports zero live bidders at Pfizer's final bid. Do not use those participation exports for research until this is repaired.

Austin requested three random deals, each extracted once by Astra xhigh, Sol 6.1 xhigh, and Opus xhigh.
He confirmed that all nine runs should start together. All six GPT runs requested Fast service.
The sample is **Synacor, Penford, and Medivation**. The Opus model is **Opus 5.5**.

## Final quality comparison

| Model at xhigh | Major causes | Moderate causes | Minor causes | Mean minutes |
| --- | ---: | ---: | ---: | ---: |
| Astra | 0 | 1 | 0 | 10.91 |
| Sol 6.1 | 1 | 3 | 1 | 12.68 |
| Opus 5.5 | 3 | 6 | 4 | 22.78 |

These are adjudicated causes across three outputs per model, not error rates or statistical estimates.
A source error that affects several cells counts once. The exporter defect does not count against either GPT model.
The [findings record](adjudicated_findings.json) gives every cause, location, source report, and manager adjustment.

| Deal | Astra: major / moderate / minor | Sol: major / moderate / minor | Opus: major / moderate / minor | Source result |
| --- | ---: | ---: | ---: | --- |
| Medivation | 0 / 0 / 0 | 0 / 0 / 0 | 1 / 0 / 1 | Astra = Sol > Opus |
| Penford | 0 / 1 / 0 | 0 / 1 / 1 | 1 / 1 / 2 | Astra > Sol > Opus |
| Synacor | 0 / 0 / 0 | 1 / 2 / 0 | 1 / 5 / 1 | Astra > Sol > Opus |

Two proposed penalties leave the final counts after adjudication: Medivation financing and Synacor calculated price endpoints.
Synacor cohort allocation also remains unresolved. The manager adds one Synacor Questions-length cause for consistent treatment across deals.
The original reports remain available; their provisional counts do not override this final table.

## Design and evidence

The random draw used seed `3947230645779240231`, without replacement, from the twelve active deals.
The [selection receipt](selection.json) records the population and result before the calls.
Each model received the same instruction and filing bytes for its deal, in a separate sandbox.
The extractor could see no prior workbook, reference answer, checker result, or other model output.

All nine workers started between **16:10:13.605523 and 16:10:13.866541 UTC**: a spread of **0.261 seconds**.
This was one concurrent batch. The comparison includes one original run per model and deal.
The [dispatch receipt](dispatch.json) and [execution context](execution_context.json) record the launch.

The run used the latest fetched `extraction-v2` commit, `58675c97fc9bc3018bd7bea21e7691ae484fc8bd`, after PR #18.
A small runner change added an explicit per-run Fast override for both GPT models.
The code and frozen plan were committed as `cb7bfba4f11624cd2984c86fd4d4f93a60574dd5`.
The instruction stayed unchanged. Its SHA-256 is `e6e1e2f3b53378bdb6770762d33fe9b84090c2ae27301d5bf725e0c3f629eb13`.

The six GPT commands record `service_tier="priority"`, Fast mode, and `xhigh`.
OpenAI identifies priority requests with Fast mode in its [official changelog](https://developers.openai.com/api/docs/changelog).
The CLI receipts prove the requested setting. They do not independently expose the delivered GPT service tier.
Equal effort names across providers do not establish equal internal compute.

The live cockpit, its default engine, and its saved workbooks did not change.
These outputs belong to this separate comparison packet. No workbook received a revision pass.

## Completed runs

All nine finished successfully. No runner continuation, retry, or revision was needed.
The checker found zero errors in every workbook. The source review remains a separate requirement.

| Deal | Model at xhigh | Minutes | Checker warnings | Whole-company bid rows | Original workbook |
| --- | --- | ---: | ---: | ---: | --- |
| Medivation | Astra | 8.04 | 0 | 4 | [Workbook](runs/medivation-gpt-6-astra-xhigh-r1/medivation.xlsx) |
| Medivation | Sol 6.1 | 9.91 | 0 | 4 | [Workbook](runs/medivation-gpt-6.1-sol-xhigh-r1/medivation.xlsx) |
| Medivation | Opus 5.5 | 13.83 | 5 | 4 | [Workbook](runs/medivation-opus-5-5-xhigh-r1/medivation.xlsx) |
| Penford | Astra | 10.38 | 0 | 10 | [Workbook](runs/penford-gpt-6-astra-xhigh-r1/penford.xlsx) |
| Penford | Sol 6.1 | 13.43 | 1 | 10 | [Workbook](runs/penford-gpt-6.1-sol-xhigh-r1/penford.xlsx) |
| Penford | Opus 5.5 | 17.55 | 2 | 10 | [Workbook](runs/penford-opus-5-5-xhigh-r1/penford.xlsx) |
| Synacor | Astra | 14.30 | 2 | 13 | [Workbook](runs/synacor-gpt-6-astra-xhigh-r1/synacor.xlsx) |
| Synacor | Sol 6.1 | 14.71 | 2 | 13 | [Workbook](runs/synacor-gpt-6.1-sol-xhigh-r1/synacor.xlsx) |
| Synacor | Opus 5.5 | 36.95 | 4 | 12 | [Workbook](runs/synacor-opus-5-5-xhigh-r1/synacor.xlsx) |

Astra averaged **10.91 minutes**, Sol **12.68 minutes**, and Opus **22.78 minutes** per deal.
Astra finished first on each deal. These are observed times from this batch, not general speed guarantees.
The full batch ran for **36.95 minutes**, dominated by Opus on Synacor.
Bid-row counts describe the outputs; a larger count is not an accuracy score.

## Source review

The [protocol](evaluation/PROTOCOL.md) preceded review of any completed output.
An Astra xhigh reviewer first built an event inventory from each filing and the instruction.
The [inventory receipts](evaluation/inventory_receipts.json) record those files before candidate access.
Reviewers then received complete cell dumps under neutral A/B/C labels. Labels differed across deals.
They received no model identity, runtime, usage receipt, or prior extraction.

The review covered all four sheets and the material source events, including events all candidates might omit.
Source accuracy, ambiguity, mechanical checks, and runtime received separate judgments.
Extra rows and model agreement were not evidence of better accuracy.
The manager checked decisive claims against the source and requested separate financing and price adjudications.

Some candidates arrived before others. Their reviewers received them in stages; final ranks waited for all three.
A replacement reviewer completed Penford because the original reviewer thread could not resume.
That reviewer read the filing and instruction, then all candidates, and checked the interim claims.
The [original Penford report](evaluation/penford_candidate_review.md) remains beside the [final report](evaluation/penford_final_review.md).

The manager knew the identity map. The deal reviewers did not receive it before their reports.
All deal reviewers used Astra, so reviewer-model bias remains possible despite labels and source citations.
Workbook prose could also reveal its origin. This method masks labels; it cannot guarantee hidden identity.

## What a finding means

- **Major:** changes a process, stage, bidder population, or material offer or exit observation.
- **Moderate:** gives a narrower required field the wrong value, or omits material field evidence.
- **Minor:** a local evidence or presentation defect leaves the economic observation intact.

One cause counts once for each affected candidate. Several affected rows do not create several independent findings.
Unresolved source readings do not enter the confirmed counts. A zero means no confirmed defect from this review, not proven perfection.

## Penford: Astra narrowly ahead of Sol; Opus third

All three preserve the core $17, $18, $18.25–$18.50, $18.50, and $19 offer sequence.
They preserve the required reaffirmations, Party A's later offers, four entrants, two stages, and the absence of bid deadlines.

Astra and Sol miss a financing fact on Ingredion's final $19 reaffirmation.
The board's reasons state that the transaction has no financing condition before the agreement is executed.
Both models leave the bid's Financing cell as `Not stated`, although they retain financing facts in later Notes.
The [independent adjudication](evaluation/financing_adjudication.md) upholds this omission. It does not backdate financing facts to earlier offers.

Opus records a supported final financing state. However, it assigns the inferred exits of Parties C and D to round 2.
Those bidders leave round 1 when round 2 opens. The instruction expressly assigns exits to the round left.
Opus's Rounds sheet has the correct populations, but its exit rows put two losses in the wrong stage.
That conflict matters when the researcher estimates bidder losses by stage.

Opus also turns the NDA's effective date into its exact execution date.
The filing gives an agreement effective on July 20, not a proven execution day of July 20.
Both Sol and Opus omit the negation from a price-feedback quotation across a page break.
Their Notes retain the negative assessment, so this is a minor evidence defect.
Opus also exceeds the Questions word limit.

The Astra/Sol difference is narrow: their main economic record is similar, and they share the financing omission.
See the [final Penford review](evaluation/penford_final_review.md) for cells, filing pages, instruction clauses, and unscored alternatives.

## Medivation: Astra and Sol tie; Opus third

All three preserve the four reported prices and the principal deal facts.
The filing is Pfizer's tender-offer account. It does not supply a complete rival-bid history or an exact anonymous-party count.

Opus keeps the unnamed NDA cohort continuously active through the August 8 bid deadline.
The instruction requires an inferred closure for unnamed entrants with no reported offer at that first deadline.
The later anonymous invitation does not cancel that convention. Its identity link to the earlier cohort remains uncertain.
The missing closure changes the participation history, even though the final offer prices remain correct.

The original reviewer also proposed a financing error on Opus's final $81.50 bid.
The independent adjudication found a date-window problem: the financing disclosure describes the later filing date without a clear bid-date anchor.
The final comparison excludes that proposed Moderate finding from confirmed counts.
It remains unresolved; the report does not certify either `Committed` or a mandatory `Contingent` replacement.

Opus exceeds the Questions word limit. Its two-round interpretation, against the GPT models' three rounds, receives no confirmed-error penalty.
The precise effect of the target's “definitive proposal” request allows more than one defensible reading.
See the [original Medivation review](evaluation/medivation_candidate_review.md) and [later adjudication](evaluation/financing_adjudication.md).

## Synacor: Astra first, Sol second, Opus third

All three preserve the main three-process history and the $2.20 final price.
The filing contains earlier sale efforts, partial-business proposals, changing exclusivity, and ambiguous anonymous-party totals.
It creates more opportunities for a plausible narrative to hide a wrong research field.

Sol opens the first competitive round too early in both earlier processes.
It applies the first-NDA exception even though the target later approaches multiple buyers.
That moves three early offers from preliminary round 0 into round 1.
It also loses source information in two exit-reason fields and treats a January 6 report as an exact bid date.

Opus combines CLP's reverse-fee refusal and its later stockholder-support requirement into one bid.
Those are separate commitment responses under E10. The combination loses an observation and its separate condition window.
Opus also misses prospective financing evidence for the January document confirmation.
Its later `Committed` values require caution because the exact February transition remains unclear.

Other confirmed Opus issues are narrower:

- It labels three Company D acquisition events as merger-of-equals events without source support for that classification.
- It loses Company A's earlier-value benchmark from the exit reason.
- It leaves Company H's information request only in a round-marker Note, without the required event row.
- It omits the required review of the December 18–21 possible round boundary.
- Two Questions entries exceed the word limit; this is one minor presentation cause.

The final comparison excludes Opus's calculated September dollar endpoints as a confirmed error.
Its products are exact outer bounds from a reported percentage revision and the referenced earlier per-share range.
The instruction permits exact calculations but also reserves price cells for the bidder's own range.
The [independent price adjudication](evaluation/price_adjudication.md) finds that conflict unresolved.
The comparison also excludes the uncertain whole-company allocation of the fourteen mixed-scope NDA parties.

Astra has no confirmed finding in this source pass. That does not settle every source ambiguity.
Its clearer treatment of the scope uncertainty also helps the reader distinguish an assumption from a secure minimum.
See the [full Synacor review](evaluation/synacor_candidate_review.md) for source locations, affected cells, and the competing interpretations.

## Mechanical checks and analytical exports

The checker verifies structure and selected local rules. It does not establish correct source interpretation.
Every workbook has zero checker errors. There are sixteen warnings across the nine files; warnings still require review.

Several warnings are false positives:

- Synacor's restart rows close zero remaining participants. Their blank Count cells follow E5.
- Sol's Penford Note explicitly says “Below” and “upper bound.” Its one-sided-price warning misses that wording.
- Opus's Medivation Account contains six sentences. The sentence heuristic splits the abbreviation “J.P. Morgan.”

Seven Questions length warnings identify real presentation defects, grouped into one cause per Opus workbook.
Eight warnings are false positives: six empty restart counts, the Penford upper-bound Note, and the Medivation sentence count.
The Medivation deadline warning concerns the alternative two-round map and does not establish a confirmed error by itself.
No warning total serves as an accuracy score.

Analytical exports and their provenance manifests sit in [analysis/](analysis/).
Their review flags require separate interpretation. A complete export is not proof of correct extracted events or participant counts.
The [diagnostic review](evaluation/analysis_diagnostics.md) identifies a further program defect in Medivation.
Astra and Sol explicitly record admission of several anonymous rivals on August 10.
The exporter ignores these `Other material event` / `Admit` rows, then subtracts their later exits from Pfizer alone.
It exports zero live bidders at Pfizer's final bid, although the workbook correctly records Pfizer's participation.

This defect also understates competition at Pfizer's earlier $77 bid.
Its exported live count is one; the workbook supports Pfizer plus several admitted rivals.
The defect produces false round-population and terminal-state warnings. It is one program cause, with several symptoms.
These diagnostics do not lower Astra's or Sol's source scores.

**The affected Medivation participation exports need a repair before analytical use.**
The repair must recognize explicit target admission and avoid duplicate entry for a party already active.
This comparison records the defect; it does not change derivation code or revise the frozen outputs.
The evidence does not show that PR #18 introduced the defect.

Opus's unknown terminal population has a different cause: its unmatched anonymous-cohort count bases.
That belongs with its existing cohort-continuity finding, without a second penalty for the downstream warning.

## Limits and next decision

This is a comparison on three active development deals, with one run per model per deal.
These deals are not an unseen holdout. The result cannot establish broad accuracy or repeatability.
Only `xhigh` was compared. It does not answer whether Sol at `high` offers a better tradeoff.

Runtime includes provider delay and local resource competition under nine concurrent jobs.
Codex subscription runs expose no cash cost. Claude's usage estimate uses list rates and does not prove a subscription charge.
This packet therefore supports an observed quality/time comparison, not a cost-effectiveness claim.
The three Claude CLI estimates total $15.41 at list rates. This is not a measured bill and has no comparable GPT cash figure.

A research default still needs source review for difficult participation, date, and condition decisions.
Any later revision, instruction change, live default change, or deployment is a separate action.

## Read the evidence

- [Frozen plan](plan.json), [binary and instruction pins](pin.json), and [source receipts](source_receipts.json).
- [Run receipts and original workbooks](runs/), plus compressed event and network logs.
- [Measured results](metrics.json), including available provider usage receipts.
- [Operational audit](operational_audit.json) and [temporary-folder cleanup receipt](cleanup_receipt.json).
- [Final findings and adjustments](adjudicated_findings.json), including the separate exporter defect.
- [Medivation source inventory](evaluation/medivation_source_inventory.md).
- [Penford source inventory](evaluation/penford_source_inventory.md).
- [Synacor source inventory](evaluation/synacor_source_inventory.md).
- [Masked cell dumps](evaluation/candidates/) and the [identity map](identity_map.json).

The Medivation filing remains on RDSS through the recorded local alias; its live source remains unchanged.
[Storage details](data_storage.json) record the path and hash. No filing bytes were added to this packet.

All nine original workbooks, compressed logs, and analysis input hashes matched before temporary-folder removal.
No receipt mismatch, web/delegation event, or incomplete analysis output was recorded.
The GPT clients made background requests to `ab.chatgpt.com`; the allowlist denied them. Only provider API traffic was allowed.
