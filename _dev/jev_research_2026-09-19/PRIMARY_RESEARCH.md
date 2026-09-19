# JEV primary-source research

Researched 19 September 2026. Scope: TypeSafe's documented model/interface, vendor evaluations and gateway access. No inference API calls were made. All performance numbers below are published vendor results, not independently reproduced measurements. This report does not re-audit the earlier Providence pilot.

## Assessment

Jev is a plausible inexpensive semantic decision component in an extraction pipeline. Its strongest design feature is making many bounded judgments over shared evidence with typed outputs. Its interface prevents invented output labels or malformed generated structures; it does not establish that the selected interpretation is true. The evidence supports testing narrow checks, candidate selection and review routing. It does not establish reliable unattended SEC deal reconstruction.

## Documented interface

The direct endpoint is `POST https://api.typesafe.ai/v1/systemone`, with a bearer key and `model`, `state`, and `questions`. A question identifier is only a response lookup key: the underlying model does **not** see it. The meaningful question must therefore be in `instructions` and `criteria`. This matters if a developer assumes an identifier such as `bidder_withdrew` explains an otherwise vague question. [HTTP API](https://docs.typesafe.ai/api)

`state` is supplied evidence: text, an object or an array. Every question in a request sees this same state independently. Objects can preserve named records and relationships; the request is not a stateful conversation. Related passages should be supplied together when the judgment requires comparing them. [State](https://docs.typesafe.ai/concepts/state)

| Primitive | What it returns | Useful extraction interpretation |
|---|---|---|
| Choice | One supplied option, distribution over options, confidence | Which event category or candidate source span fits? |
| Score | Position on an ordered rubric, distribution over levels, confidence | How relevant is this passage to a particular field? |
| Noul | Probability that a yes/no proposition is true | Does this passage explicitly state that the bidder withdrew? |

These are bounded judgments, not prose-generation requests. TypeSafe recommends decomposing questions that combine independent factors or require extended reasoning. [Introduction](https://docs.typesafe.ai/introduction)

Choice permits up to 255 options. The selected option is the highest-probability one and the option probabilities sum to one. Option names and descriptions are visible to the model. An explicit none/other/unknown option is necessary when the supplied alternatives may omit the truth. [Choice](https://docs.typesafe.ai/primitives/choice)

Score supports 2–10 ordered descriptions, numbered by their array positions. It is a rubric position, not an arbitrary numeric extractor. [Score](https://docs.typesafe.ai/primitives/score)

Questions sharing evidence can be batched, including conditional questions whose answers code later ignores. The documented advantage is approximately constant latency as questions are added; added question text still consumes tokens. Independent evaluation does not mean later questions can consume earlier answers in the same call. [Fan-out](https://docs.typesafe.ai/patterns/fan-out), [Choice](https://docs.typesafe.ai/primitives/choice)

## Versions, capacity and specialization

The documented direct model is `jev-1.13.0`; both `jev-latest` and `jev-preview` currently resolve to it. Log the returned model version and pin versions when thresholds are tuned. Direct limits are 64k tokens for the complete request, **32k for the state plus the longest question**. Thus 64k does not mean a 64k document can be passed as state. Only text is supported; English is strongest. Published direct limits are 250,000 tokens/second and 1,200 requests/minute, explicitly subject to change. Jev is not customer-fine-tuned or LoRA-adapted: all accounts share weights, and domain behavior comes from supplied evidence, instructions and criteria. [Models](https://docs.typesafe.ai/models)

## What confidence does and does not mean

Choice/Score `confidence` is computed from the returned probability distribution's concentration. It is not a second independent prediction of whether the answer is correct. Noul has no separate confidence property. The reviewed confidence page describes this conceptually without specifying a complete mathematical formula. It explicitly says thresholds depend on domain and measured performance. A displayed confidence of 0.95 should therefore not be read as an established 95% SEC-field accuracy. [Confidence](https://docs.typesafe.ai/confidence)

TypeSafe describes its training as Reinforcement Learning for Calibrated Decisions (RLCD). Calibration means that, across a relevant population, events assigned probability 0.8 should occur approximately 80% of the time. It is a population property, not proof of an individual answer. The primer describes the training objective, not a reproducible training algorithm or a domain-specific calibration certificate. [AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer)

The launch article attributes performance to a new architecture, parallel sampling and RLCD. Its zero-hallucination argument is a **schema-matching guarantee**, and the article says its zero figure is not an empirical semantic-error measurement. Its headline speed/cost comparisons come from the workflows discussed below. The authors acknowledge favorable short inputs in a demo, possible team-design bias, and higher LLM cost from returning probabilities. [Launch article](https://typesafe.ai/blog/introducing-system-one-models-and-jev)

Research boundary: the reviewed official docs, launch article and public repositories did not provide an independently auditable RLCD training specification, model weights or broad SEC-auction calibration study. This is a bounded search finding, not proof that no such material exists. The public organization principally exposes SDKs, integration skills and an LLM comparison adapter. [Official repositories](https://github.com/typesafe-ai)

## Documented failure modes relevant to this project

TypeSafe's version-specific warning page, reviewed 17 September, lists: literal interpretation; unreliable counting/arithmetic and numeric precision; unreliable date ordering and intervals; multi-hop indirection; declining accuracy with irrelevant long context; adversarial state; conflicting criteria; and failures of logical consistency between separate questions. It recommends counting and date arithmetic in code, precise boundary definitions, and small relevant evidence packets.

Two separate questions need not satisfy `P(A) + P(not A) = 1`; a Noul and an equivalent yes/no Choice can disagree. Do not transfer thresholds between primitives. Likewise, independent question execution does not make errors statistically independent.

It is not trained for free-text generation. TypeSafe recommends finding candidate values with regex or a generative model and having Jev choose among them. Relevant evidence omitted during retrieval cannot be recovered by this interface. These limitations directly constrain counts of bidders, inferred dates, nested conditionality and reconstruction of a long auction history. [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13)

## What the primary evaluations actually show

### Workflow comparison

The published evaluation uses four developer-written workflows. Reference labels derive from averaged GPT-6 Astra and Claude Fable 5.1 responses at high thinking; other models run at provider-default reasoning. The harness is assumed correct. This is agreement with a model consensus under a particular decomposition, not agreement with human-adjudicated truth. The overview equally weights the four workflows. [Evaluation method](https://evals.typesafe.ai/)

The following numbers were read directly from the inline SVG chart titles in the official overview HTML on the research date. Prices/time are vendor-reported means, rounded as displayed, not locally measured.

| Model, workflow mode | Consensus agreement | Cost per workflow | Time |
|---|---:|---:|---:|
| Jev | 67.8% | $0.0004 | 0.4 s |
| Terra | 67.9% | $0.0304 | 10.1 s |
| Sol | 74.1% | $0.0836 | 23.3 s |
| Opus 5 | 73.1% | $0.1761 | 37.8 s |
| DeepSeek v4 Flash | 64.4% | $0.0059 | 51.9 s |

[Official aggregate chart](https://evals.typesafe.ai/)

| Workflow | Jev agreement | Sol agreement | Terra agreement | Primary chart |
|---|---:|---:|---:|---|
| Security incidents | 61.7% | 62.5% | 51.2% | [Security](https://evals.typesafe.ai/security_incidents) |
| Agent traces | 71.6% | 76.6% | 73.0% | [Agent traces](https://evals.typesafe.ai/agent_trace_observability) |
| Invoice processing | 61.8% | 79.1% | 74.7% | [Invoices](https://evals.typesafe.ai/invoice_processing) |
| Customer service | 76.0% | 78.3% | 72.7% | [Customer service](https://evals.typesafe.ai/customer_service) |

The invoice gap is particularly relevant: its harness already handles sums, dates, account numbers and statuses in code, yet Jev has substantially lower agreement. This is evidence against assuming all business-document reasoning is equally suitable. [Invoice workflow](https://evals.typesafe.ai/invoice_processing)

The official LLM adapter can request probabilities or discrete decisions, with structured outputs and probability normalization configurable. It exposes latency, retry counts and total token usage. This makes a common-interface comparison possible, but an LLM asked for every probability is a more expensive baseline than one asked for a single answer. [Adapter source and README](https://github.com/typesafe-ai/system-one-adapter-python)

Interpretation: the strong result is low cost and latency at useful agreement. The shown numbers do not imply parity with the strongest models, universal 100-fold end-to-end savings, or correctness of the reference consensus. Evidence retrieval, schema design, generative extraction and human correction remain outside a simple Jev-call comparison. The reviewed workflow pages did not disclose enough sample-construction, sample-size and uncertainty detail to independently reconstruct the full statistical evaluation.

### Official citation-checking example

This is unusually close to the proposed SEC verifier. Code first checks whether a quotation exists; Jev then judges whether its context supports the claim. The demonstration contains eight RFC 7519 citations: four accurate and four deliberately faulty. It reports catching all planted failures, but uses cached `jev-1.12` outputs from 16 August. Eight selected cases demonstrate an integration pattern, not an error-rate estimate for Jev 1.13. Exact quotation matching and semantic entailment are explicitly separate steps. [Citation checker](https://docs.typesafe.ai/cookbooks/citation_check)

### Official extraction-cascade example

The recipe extracts with GPT-5.4 Mini, asks Jev per-field error questions, and sends flagged records to GPT-5.5 reasoning. It uses `jev-1.12`. Its internal comparison covers 100 scrapegraphai prompts and sweeps an escalation threshold; its chart is historical and not repriced at current Jev rates. The illustrative bad Mini extraction is deliberately hard-coded because live outputs vary. The page does not adequately define the chart's approximately 0.81 top-end “quality” measure or document a separate threshold-selection/held-out split. The sensible transferable idea is narrowly targeted error signals, with escalation if any relevant signal fires; the reported savings cannot be assumed for SEC extraction. [SDE cascade](https://docs.typesafe.ai/cookbooks/sde_cascade)

### Official SEC confidence example

The SEC cookbook uses `jev-1.12` (12 August) on 60 selected Item 1 excerpts whose text supports their SIC labels. Specific-group correctness is 39/60: 27/30 above the 0.9 confidence cutoff, 12/30 below. Coarsening uncertain answers to divisions yields 48/60, changing the target granularity. This supports prioritisation while retaining confident errors; it does not validate an auction-extraction threshold. [SEC classification cookbook](https://docs.typesafe.ai/cookbooks/classification_using_confidence)

### Consistency is separate from correctness

The Choice consistency cookbook repeats eight moderation questions on one borderline post 15 times, adding a fresh irrelevant identifier each run. Jev's raw majority-label agreement is 90.8%; requiring top probability at least 0.60 raises agreement to 99.2%, with automatic labels on 74.2% of answers. It explicitly acknowledges that this setup cannot distinguish sensitivity to that changed field from variability on identical requests. It has no adjudicated gold labels. Neither 99.2% consistency nor repeatable probabilities establish 99.2% correctness. [Consistency cookbook](https://docs.typesafe.ai/cookbooks/consistency_choice_cookbook)

## Can human corrections improve the system?

Yes, through the surrounding workflow; that is different from training Jev itself. An official example has another LLM propose and revise semantic feature questions, Jev compute their outputs, and CatBoost learn from labels. Its wine-rating task uses 1,200 development and 800 held-out rows. Five rounds produce 38 questions; held-out RMSE improves from 1.869 after round one to 1.772, with a reported paired-bootstrap interval of -0.147 to -0.050 for the difference. It compares against direct Jev scoring and a word-count CatBoost baseline, while listing embeddings and additional baselines as future work. [Autoresearch cookbook](https://docs.typesafe.ai/cookbooks/autoresearch_feature_discovery)

Inference for SEC: saved human corrections could improve coding definitions, evidence retrieval, question phrasing and a downstream review-priority predictor. They do not automatically update Jev's weights. Any learned reviewer should be evaluated on unseen deals, because dozens of fields from one filing share narrative and coding ambiguities. A model trained to reproduce earlier reviewers may also reproduce their inconsistent conventions.

## Access, price and privacy

Direct pricing is $0.042 per million input tokens, output free. As an arithmetic illustration, 1,000 requests averaging 5,000 input tokens cost $0.21 for Jev inference alone, excluding retrieval, extraction, hosting, gateways and human review. [Model pricing](https://docs.typesafe.ai/models)

OpenCode Zen documents `jev-1.13` and `jev-1.13-free`, both on `https://opencode.ai/zen/v1/systemone`. Paid input is $0.042/million and Free is a limited-time offer. It does not document a quality downgrade, but does not provide a formal equivalence guarantee, separate Free limits or a Free end date. Its privacy section says providers generally have zero retention and no training, with named exceptions; Jev is not listed among them. This is the gateway's published policy, not an independently audited claim. [OpenCode Zen](https://opencode.ai/docs/zen/)

Vercel lists `typesafe-ai/jev`, with an experimental evaluation API, currently promotional free pricing ending 25 September 2026, and a displayed 32K context. Its wrapper calls a yes/no question `boolean`, whereas the native API calls it `noul`; do not mix schemas. That expiry date belongs to Vercel and should not be transferred to OpenCode. [Vercel listing](https://vercel.com/ai-gateway/models/jev)

Direct TypeSafe privacy is a distinct policy: it says it will not train or fine-tune models on customer inputs but permits personal-data retention for service/business needs, without a fixed universal duration in the reviewed privacy page. The docs separately offer enterprise zero-data retention. Thus no-training does not by itself imply zero retention; gateway and direct service terms must be kept separate. [Privacy policy](https://typesafe.ai/legal/privacy-policy), [Legal documentation](https://docs.typesafe.ai/legal)

## Practical research conclusion

The first useful question is not whether Jev can approve an entire workbook. It is whether a small set of well-defined Jev decisions reduces the total effort needed to deliver a correct ledger. Candidate selection, per-field evidence checks, source-paragraph classification and selective escalation fit the documented interface. Counts, date arithmetic, free-form explanations, open-ended event discovery and final adjudication require other components.

A sound comparison should hold retrieval and evidence constant, compare Jev with the existing checker and with deterministic checks, and report error recall, false flags, confidently missed errors, accepted-case error rates, omission coverage and human correction time. It should include source-driven cases, not only already-extracted claims. This is an experimental recommendation inferred from the interface and evidence above, not a published validation result.
