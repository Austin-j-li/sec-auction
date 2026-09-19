# How JEV could help SEC auction extraction

Research date: 19 September 2026. This is a research assessment and proposed experiment, not an implemented pipeline or an acceptance result. Primary-source detail is in [PRIMARY_RESEARCH.md](PRIMARY_RESEARCH.md).

## Judgment

JEV merits a bounded trial as a fast reader for narrowly specified questions: locating candidate events, checking individual fields against evidence, and deciding which cases deserve attention. Its value to this project would be more complete and cheaper review. Whole-deal reconstruction, research definitions, source completeness and acceptance remain separate responsibilities.

The strongest design implication is to split a broad judgment such as “is this ledger row correct?” into questions about actor, action, scope, timing, terms and evidentiary basis. Then apply the extraction conventions in ordinary code. A single favourable verdict can conceal one wrong component of an otherwise plausible row.

This assessment uses the current [extraction instruction](../SEC_Deal_Ledger_Extraction_Instruction.md), revised 19 September. That instruction remains untested and unreviewed by Alex, according to its own status note. Its date and outcome policies differ from the earlier instruction used in the Providence pilot.

## What the model offers

The interface takes supplied text and predefined questions, and returns typed decisions. Choice selects among supplied alternatives; Noul estimates a yes/no proposition; Score rates an ordered rubric. It does not produce open-ended narrative, code, quotations or workbooks. A surrounding program must supply candidates and preserve the original evidence. [TypeSafe quick start](https://docs.typesafe.ai/introduction/quickstart)

Many questions can share one state and be evaluated together. This makes a checklist over the same short source packet an appealing use: the vendor says extra questions typically add little latency, though they still consume input and context. [Fan-out documentation](https://docs.typesafe.ai/patterns/fan-out)

The supplier describes a new architecture, parallel sampling and Reinforcement Learning for Calibrated Decisions. These are supplier descriptions; the material reviewed does not establish a reproducible independent architecture/training audit. Its schema guarantee constrains the form of an answer, not whether the selected answer is true. [Launch announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev)

## Where it fits in this project

| Job | Proposed use of JEV | Responsibility elsewhere |
|---|---|---|
| Find possible omissions | Tag passages for offers, outcomes, access to information, changed forecasts, deadlines and bidder relationships | Compare with the ledger; audit passage recall against the complete source |
| Check existing entries | Ask separately whether actor, price, condition, event and evidence basis are supported | Assemble sufficient evidence and adjudicate ambiguous flags |
| Distinguish financing from bidding | Select among financing support, joint bidding, separate bids and insufficient evidence | Resolve identities across the filing and maintain bidder units |
| Classify an outcome | Identify what ended: proposal, diligence, negotiation or participation | Apply the research definition and current closeout policy |
| Interpret date evidence | Identify whether a date explicitly applies to the action, only to a meeting, or is inferred | Calculate intervals, working dates and ordering constraints |
| Reconcile counts | Judge whether descriptions refer to the same population and period | Compute arithmetic, enforce disjointness and expose assumptions |
| Produce the workbook | Supply candidate classifications and review flags | Write cells, formulas, links, provenance and formatting deterministically |

These are hypotheses about fit, not demonstrated capabilities on unseen auction filings.

### An intuitive example

Consider a hypothetical passage: a bidder withdraws its revised proposal but confirms that its earlier offer remains available. A single “withdrawal” classifier risks closing the bidder out.

Instead ask three separate questions:

1. Does the passage withdraw the revised proposal?
2. Does it explicitly keep an earlier offer available?
3. Does it explicitly end participation in the process?

The supplied choices should include insufficient evidence. A program can use those answers to propose a bid reversion while leaving participation open. A reviewer can inspect the relevant source and the competing interpretations. No probabilities in this example are actual JEV results.

The same approach helps distinguish “financing commitment obtained” from “financing condition removed,” or “diligence completed” from “all material conditions removed.” Each distinction needs its own definition and evidence.

### Coverage matters as much as verification

A verifier sees only entries that already exist. It cannot flag an omitted information-access event if no candidate or source passage is presented to it.

A useful experiment therefore needs two directions: source-to-ledger coverage checks and ledger-to-source support checks. Scan the complete relevant filing, including tables and relevant material outside Background. Identify candidate passages independently of the existing extraction. Compare them with ledger entries and give reviewers a queue of unmatched material.

Initially, low-scoring passages should remain available for audit. Using an unmeasured relevance threshold to discard them could make the pipeline cheaper by silently worsening completeness. Measure passage/event recall before treating any filter as a safe exclusion rule.

### The current instruction gives code a larger role

Section 8.1 now requires every Working date to be filled, while preserving honest source timing and distinguishing reported, inferred and assigned dates. JEV could help recognise which evidence applies. Calendar arithmetic, priority rules and sequence constraints belong in deterministic logic. An assigned decision-day sort key must never become a claim that the source reported the event on that day.

Section 10.2 requires every participant to be closed out, sometimes through an explicitly inferred residual or silent-exit row. That means “the source does not expressly report an exit” is not sufficient to reject a row. Check the population and transition evidence, then check that the inference follows the policy and is labelled honestly.

This separation is critical: source support, analytical inference and compliance with a convention are different questions. Researcher corrections should retain their scope; one deal-specific judgment should not automatically become a universal rule.

## Evidence and limitations

TypeSafe's current limitations page explicitly flags counting, numerical precision, date comparison, multi-step reasoning and distraction by irrelevant context. Independent answers may conflict logically; finite choices can force a bad selection when none is appropriate. [JEV 1.13 limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13)

The direct implication for this project is to avoid a whole-filing, whole-instruction mega-question. Supply a focused evidence packet with enough neighbouring context to resolve identities and references. Include “not stated,” “unclear” or “conflicting evidence” where appropriate. A candidate selector cannot recover an answer missing from its candidate list, and a checker cannot repair missing evidence by confidence alone.

Confidence is a statistic of the returned probability distribution, rather than an independent verification of truth. Thresholds require validation on the actual task. [Confidence documentation](https://docs.typesafe.ai/confidence)

An especially relevant example uses JEV **1.12** for SEC industry classification. It demonstrates useful confidence ranking alongside confidently wrong answers; the companion report gives the sample and results. [SEC classification cookbook](https://docs.typesafe.ai/cookbooks/classification_using_confidence)

The workflow benchmark uses reference answers derived from Astra and Fable, assumes its harness is correct, and covers four vendor-selected workflows. Agreement with those references is not adjudicated historical truth. It does not measure missing auction events, correction time or workbook acceptance. [Evaluation methodology](https://evals.typesafe.ai/)

The companion primary-source report records the benchmark chart values and their substantial variation by task. The engineering pattern itself can benefit other models too: a fair comparison must give competitors the same source packets, question definitions and deterministic rules.

## What the earlier Providence run tells us

The earlier session recorded 20 original checks and four deliberately corrupted claims through OpenCode's typed System One endpoint. Calls succeeded; the original checks had a median latency around 0.57 seconds, and the four planted errors were flagged. A questionable “reported day” designation was accepted with high confidence. Some other judgments depended on incomplete evidence packets or debatable labels.

These are historical session-reported observations. The prior pilot directory is absent from the current workspace, so raw outputs were not re-audited for this research note and no model calls were repeated. The instruction has also changed. Treat this as an integration smoke test and a source of failure cases; do not turn the accept/reject counts into an accuracy estimate.

The date example is especially instructive: a plausible date can still have the wrong evidentiary status. The next test should ask separately whether the event occurred by that date, whether the exact day is explicitly reported, and whether the chosen Working date follows the current assignment rule.

## Economics, access and learning from corrections

OpenCode lists paid and free JEV 1.13 IDs on its `/systemone` endpoint. The paid rate is $0.042 per million input tokens with free output; the free offer is temporary. No separate quality advantage for the paid alias is established by those listings. [OpenCode Zen](https://opencode.ai/docs/zen/)

At that paid rate, 100,000 requests averaging 2,000 total input tokens cost about **$8.40** in JEV input charges. This is arithmetic from an assumed workload, not a measured project budget. Preparation, retrieval, other models, retries, engineering and human review are additional. A cheap checker saves little if expensive preparation dominates; noisy flags can increase review time.

Customer fine-tuning/LoRA is unavailable. Prompt criteria and examples can change behaviour; accumulated corrections do not automatically change its weights. Native service limits and data-handling commitments must not be assumed to transfer unchanged to a gateway. [Model reference](https://docs.typesafe.ai/models)

Later, a separately trained classifier or calibrator could learn how JEV's outputs map to researcher judgments. TypeSafe demonstrates the general idea with JEV-derived features and CatBoost on wine reviews, using JEV 1.12. That is a design example, not evidence that it will work for bidder histories. [AutoResearch cookbook](https://docs.typesafe.ai/cookbooks/autoresearch_feature_discovery)

For this project, any such learning should use versioned, human-adjudicated decisions, with entire deals held out. Randomly splitting similar rows from the same filing can leak the same facts and wording across development and evaluation.

## A test that would answer the useful question

Recommended first experiment: **review assistance**, under the current frozen instruction, on several fresh deals. Around five to ten deals and 200–300 adjudicated field checks would be a practical feasibility study, not a precise certification of rare-error rates. Deliberately sample ambiguous dates, inferred closeouts, bidder groups, changing terms and information-access events, alongside routine cases. Separately review the full source to establish material-event coverage.

Compare the existing extraction-and-review process with the same process plus JEV flags. Also compare JEV with an inexpensive generative model on identical narrow questions. Keep evidence preparation and deterministic checks common. Record any benefit of decomposition separately from the benefit of changing models.

Measure:

- **Missed material events:** source events absent from the ledger, including events the initial extractor never proposed.
- **Errors among accepted entries:** especially mistakes receiving high confidence or no review flag.
- **Useful-alert rate:** how often a flag leads to a justified correction.
- **Human correction time:** including false alarms, evidence retrieval and propagation of edits.
- **Accepted deal cost:** all model and review costs per workbook meeting the researcher's bar.

Preserve raw source blocks, candidate inputs, model/version, question and instruction versions, complete outputs, reviewer judgments and subsequent corrections. Do not overwrite the original result when a human changes it.

The adoption decision should be conditional: keep JEV where it saves review effort while preserving coverage and accepted quality. If it reliably handles only passage tagging or a few easy fields, that can still be useful. Automating entire accepted workbooks would require a much stronger result than a fast series of plausible classifications.
