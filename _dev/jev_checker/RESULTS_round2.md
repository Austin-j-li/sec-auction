# TypeSafe follow-up: proposed checker changes

**Recommendation: add event-specific price verification to a read-only post-extraction reviewer first.** The existing price experiment's question omits the bid date and event. In these harder controls it accepted 10 of 27 deliberately incorrect prices, usually a real price from another offer by the same bidder. Adding the event, time and price basis caught all 27, with no false flags on 27 correct controls. The same improvement occurred with a yes/no question, so the evidence supports better question scope, not a claim that Choice outperforms Noul.

I ran **184 new API calls** with `jev-1.13.0`, using the TypeSafe skill and the supplied credential: 114 first-phase cases and 70 adaptive diagnostic calls. They consumed **234,300 input tokens**, an estimated **$0.00984** at the documented $0.042 per million input tokens. There were no HTTP errors or retries. Combined API-run wall time was 190.4 seconds at concurrency four; median request elapsed time was 2.14 seconds and p95 was 12.40 seconds. Timing includes this Python client's connection overhead; it is not server-only inference latency. The cost is calculated from usage and the [official model price](https://docs.typesafe.ai/models.md), not an account invoice.

No extraction workbook, working instruction, or production checker was changed. The pre-existing Jev experiments and unrelated working-tree changes were left intact. Credentials are absent from saved experiment files.

## Evidence and limits

These are **development tests**, authored from the three existing public filings: Providence & Worcester, Mac-Gray and PetSmart. Expected answers were fixed before each phase's API calls and were excluded from requests. They reflect this assistant's source reading, not independent human adjudication. The API received public filing passages and, for coverage, constructed candidate ledger rows. This is not a new clean extraction or a blind test of unseen deals.

The first phase was specified in `PLAN.md`. The second phase was designed after observing the first phase, preserving the same labels. Its purpose was to diagnose the mechanism, not provide independent confirmation. All requests, responses, question text, source hashes, labels, usage and failures are saved. `summary.json` is generated from the raw responses by `analyze.py`.

## 1. Price verification: the strongest result

There are 27 distinct offer events. Each has a correct price and one incorrect price. Twenty-four of the 27 incorrect prices have all their endpoints somewhere in the supplied five-paragraph source window, making number occurrence an especially weak test.

| Check | Correct prices accepted | Incorrect prices rejected |
|---|---:|---:|
| Deterministic monetary-number presence | 27/27 | 3/27 |
| Earlier actor-only Noul question | 27/27 | 17/27 |
| Event-specific three-way Choice | 27/27 | 27/27 |
| Event-specific Noul, adaptive comparison | 27/27 | 27/27 |

The original Noul asks whether a party offered that price somewhere in the passage. For many wrong-date cases its answer is literally reasonable: the question never asked about the date. This is a **verification-design failure**, not evidence that Jev cannot understand dates. Increasing its probability threshold would not solve the design problem: several incorrect approvals have P(yes) of 0.98–0.99.

Concrete controls:

- Providence, paragraph 353: G&W offered $21.15 on July 21 and $22.15 on July 26. Swapping those prices passed the older question with P(yes) 0.98 and 0.99. Event-specific checks rejected both.
- PetSmart, paragraph 313: the Buyer Group's earlier oral $82.50 and later final $83 offers on December 12 must stay distinct. A calendar date alone is insufficient; the event description needs the within-day sequence.
- Mac-Gray, paragraph 256: Party B attributed $21.50 to its package, consisting of $19 cash and options valued at $2.50. Testing only the $19 cash component as the package price passed the older question; the total-price specification rejected it.

A separate candidate-selection question chose the correct low and high endpoints for all 27 events in both correct-claim and incorrect-claim request batches. Candidate amounts came from a regex over the source, with a `none` option. This avoids generating numeric strings, but source occurrence alone does not guarantee the chosen amount has the right meaning. The two batches reuse the same events and are not 54 independent observations of selection accuracy.

Four missing-evidence controls all returned `insufficient`, including Party B's August 4 returned draft without a quoted price. That distinction matters: the working instruction permits a standing price to be carried from an earlier row. A locally absent price must not become an alleged factual error.

**Proposed implementation:** supply bidder, event date/range, event description including sequence, and price basis to the checker. Return `supported`, `contradicted`, or `insufficient`, plus the source and model probabilities. Route a carried-forward price to its earlier evidence row. Keep unresolved date/event attribution for review. Do not automatically replace cells. Candidate selection can provide a suggested alternative amount for the reviewer, not an automatic repair.

The three-way representation remains useful because it separates contradiction from missing evidence; it did not beat a properly scoped Noul on binary correctness here. Its distinction follows the [citation-check cookbook](https://docs.typesafe.ai/cookbooks/citation_check.md); source candidate selection follows the [pre-parsed value cookbook](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook.md).

## 2. Event-to-row matching: promising, but not an omission detector yet

Ten source events each had four candidate-row scenarios: exact representation, paraphrase with a distractor, distractor alone, and no rows. Both binary matching and selecting a row or `none` were correct in **40/40 scenarios**: 20 represented and 20 absent events. Selection confidence was at least 0.9 in 38/40, all correct; this is a descriptive count, not a validated deployment threshold.

Examples included an executed MacDonald voting agreement versus an earlier request for one; PetSmart's revised December 10 deadline versus its earlier December 5 deadline; and Party E's August 2 reversion versus its August 1 higher offer. Topic overlap was not enough to fool the matcher on these controls.

**Proposed implementation:** for a known source event, ask for the specific ledger row that represents it, or `none`. This makes review output more concrete than one paragraph-level coverage score. Search a sufficiently broad candidate set and display both the source event and candidate rows to the reviewer.

The material limitation is that **I supplied the target events**. These tests do not establish that Jev discovers all events in a filing, retrieves every relevant ledger row, or reduces reviewer minutes. An upstream source-event inventory and candidate-retrieval evaluation remain necessary. A `none` result can mean retrieval failed, not that the workbook omitted the event. This should initially be an experimental reading aid, behind price verification in priority.

## 3. Financing evidence: use a narrow question and a small source packet

The task has three answers: explicit commitment, explicit absence of commitment, and silence. There were six commitment cases, three missing-commitment cases and seven silent cases.

| Input design | Correct | Remaining concern |
|---|---:|---|
| Source plus the overall C14 conditions rule | 15/16 | Missed Bidder 2's commitment in an “each bidder” sentence |
| Same question, source only; adaptive comparison | 16/16 | Both “each bidder” answers remained below 0.9 confidence |

The failing first-phase case was PetSmart paragraph 313. It states that each bidder submitted financing commitment documents. Jev chose `silent` for Bidder 2 with confidence 0.26; for the Buyer Group it chose `committed` with confidence 0.40. Source-only input returned `committed` for both, at confidence 0.66 and 0.74. This is one observed improvement on the same cases, not proof that removing context always improves accuracy. There were no independent repeated runs to measure variability. The diagnostic also removed the companion overall-conditions question; the documented API evaluates questions independently, but that request-shape change was not separately isolated.

The seven silent passages were never mistaken for explicitly missing commitments. For example, an all-cash offer or a due-diligence condition does not by itself tell us whether financing was committed.

**Proposed implementation:** add a financing-evidence review field with those three outcomes. Use only relevant source context for this judgment. Treat explicit absence as evidence relevant to C14's Heavy trigger; treat silence as no financing conclusion. Do not infer `None` or `Light` solely from commitment, since diligence and other conditions still matter. Send shared/group references and uncertain judgments for review. The first-phase overall Conditions answers are saved but deliberately unscored because the packet lacks some stage and diligence history.

## Changes to prioritize

1. **First: a read-only price review pass outside the extraction sandbox.** Bind price to bidder, event and basis; preserve missing evidence and carry-forward handling. Run it on completed workbooks and output a separate review file with cell references and evidence.
2. **Second: a separate financing-evidence check.** Keep it independent of the complete Conditions judgment and preserve an explicit silent outcome.
3. **Experimental: known-event-to-row matching.** Require a matching row ID or `none`, and measure candidate retrieval before claiming omissions.
4. **Before adoption:** use untouched deals with human-reviewed labels, mixed real errors and correct rows, and measure false flags and reviewer time. Include difficult shared references, date ranges, within-day sequences, carried prices, numeric extraction gaps and actual missing rows. Pin the model and retain raw responses. This run neither calibrates a universal confidence cutoff nor compares TypeSafe against a generative-model control.

I propose these as checker changes. **No change to the extraction instruction is justified by these results:** C14 already distinguishes financing silence and missing commitments; C15 already distinguishes package values and components. The demonstrated defect is in how the verification question was asked.

## Reproduction and provenance

See `README.md` for commands. `experiment.py`, `build_ablation.py` and `analyze.py` are the experiment code. `cases.json` and `ablation_cases.json` contain the frozen designs. `raw/` and `ablation_raw/` contain all 184 credential-free API records. Source paragraph indices are harness-local, not official SEC references; the full quoted source packet is included in each request.

Official sources consulted: [HTTP API](https://docs.typesafe.ai/api.md), [state and independent questions](https://docs.typesafe.ai/concepts/state.md), [Choice](https://docs.typesafe.ai/primitives/choice.md), [Noul](https://docs.typesafe.ai/primitives/noul.md), [citation checking](https://docs.typesafe.ai/cookbooks/citation_check.md), [source-candidate selection](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook.md), and [model version, limits and pricing](https://docs.typesafe.ai/models.md). Snapshots are in `docs/`.
