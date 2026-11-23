# Comparison protocol

Recorded on 12 October 2026, before any completed output was examined.

## Design

- Draw three deals uniformly without replacement from the twelve active deals.
- Save the seed and population before the model calls. Make one draw.
- Run each selected deal once with each requested model and effort.
- Start all nine isolated runs together. Request Fast service for both GPT arms.
- Use the same v1.1 instruction and the same filing bytes for every arm within a deal.
- Keep the original output. Do not revise it or give checker feedback to an extractor.
- Run the checker and analytical export after extraction, outside its sandbox.

## Source review

An independent reviewer first reads the instruction and filing for one deal.
The reviewer records an event inventory before access to any new workbook.
The inventory covers every process, round, price proposal, deadline, admission, exit, and process closure.
It also records source ambiguity and the instruction clauses that govern difficult choices.

The reviewer then receives three workbooks under neutral labels A, B, and C.
The label mapping differs randomly across deals. The reviewer receives no engine metadata, runtime, or prior workbook.
Workbook prose or style could still reveal a model. This is label masking, not guaranteed blind identification.
The manager retains the identity map and reveals it only after each reviewer records a comparison.

## Judgments

For every material finding, record the source passage, source location, workbook sheet and row, and applicable rule.
Separate a confirmed error from a defensible interpretation and from unresolved source ambiguity.
Do not use agreement between models as proof. Do not use a prior hand-coded workbook as ground truth.
Do not reward extra rows unless the instruction requires those events.
Do not treat a checker warning as an established source error.

Use these dimensions:

| Dimension | What the review checks |
| --- | --- |
| Coverage | Required processes, stages, bids, deadlines, exits, and material events |
| Economic coding | Bid prices and types, Formality, conditions at communication, and initiation |
| Participation | Admissions, cohorts, bidder identity, non-submission, re-entry, and final closure |
| Traceability | Accurate quotes, useful source locations, explicit inference, and honest uncertainty |
| Operation | Completed original workbook, schema/checker findings, elapsed time, and available usage receipts |

Severity follows the consequence:

- **Major:** changes the process or round structure, the bidder population, or a material bid/exit observation.
- **Moderate:** wrong value in a required field with a narrower effect; material evidence or uncertainty is absent.
- **Minor:** local presentation or locator defect that does not change the economic observation.

One cause that affects many cells is one finding. Record its affected rows separately.
Reviewers report issue counts and a reasoned per-deal ranking. A tie is allowed.
They also state what they checked and what remains unresolved.
The manager verifies decisive claims against the source before the final recommendation.

## Limits

This is three deals and one run per model per deal. The cases come from the active development set.
The result measures this pilot. It cannot establish general accuracy or repeatability on unseen deals.
Equal effort names do not establish equal internal compute across providers.
Elapsed time includes provider delay under nine concurrent jobs.
Requested Fast service is verified through the command receipts. Actual provider service is reported only if the response exposes it.
Token counts across different tokenizers are not directly comparable.
Codex subscription runs do not expose a cash cost. Do not invent one from API list prices.
Any Claude cost field is a reported usage estimate, not proof of a subscription charge.
