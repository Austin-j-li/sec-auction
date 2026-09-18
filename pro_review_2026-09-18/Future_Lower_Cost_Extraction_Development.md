# Future development of reliable lower-cost extraction
**Exploratory note — no change to the current quality-first policy**  
**Austin Li / Alex Gorbenko — 18 September 2026**

## Recommendation

There is enough evidence to justify a **bounded development experiment**, but not to replace the current extractor. Continue using the strongest demonstrated configuration for production-facing first passes and human review. Among these four Providence runs, Astra is my present choice; Fable is a close comparison candidate. Do not interpret this note as approval for a cheaper model, a cheaper first-pass/stronger-repair cascade or unattended batch extraction.

The most promising investment is not a longer list of deal-specific warnings. It is a small shared layer for source preparation, typed output, chronological/count checks and reproducible evaluation. That layer would also help the stronger extractor. It becomes a cost-saving system only if new tests demonstrate that a lower-cost candidate can meet the research-quality requirement with less **total** effort.

No actual run prices, token counts or times were supplied. “Lower-cost candidate” below is a hypothesis about a configuration to test, not a verified price ranking of these four models.

## 1. What these results demonstrate

The runs separate several failure mechanisms.

**Mechanical output failures exist.** Muse's `Deal!L2:M2` links point to the wrong events, and its `Bids!AA5:AA6` prior-offer links form a cycle. These are amenable to deterministic validation after extraction. They do not require a legal expert to detect. A fixed writer could eliminate classes of malformed links and column-placement errors without making the language model a better reader.

**Exact quotations do not certify interpretations.** DeepSeek's 194 nonempty Evidence quotations matched the normalized filing in the mechanical check, yet report dates become exact action dates and a deadline-setting event is used as a deadline reference. Correcting quote fidelity alone would not fix those errors. [Comparative assessment §3C and §5; BG-006–009 and BG-021.]

**The stronger output also needs ordinary engineering.** Astra's independently assigned representative dates produce a misleading chronology around selection/exclusion. A common interval/precedence display and a date-consistency checker would help it as well as a lower-ranked run. [Astra Events rows 49–50; BG-020.]

**Some disagreements are about research definitions.** Party E's issues summary can reasonably support different formality assessments under an incompletely calibrated threshold. An additional model call cannot resolve an unapproved convention merely by voting. The objective is to preserve the documentary facts and apply an agreed rule consistently. [BG-012, BG-015; Fable Bids row 6 versus Astra Bids row 6.]

**Some uncertainty is in the filing.** The early 25 NDA signers, new Party C and later overall 25 summary cannot be reconciled with certainty by better arithmetic. The result should retain the competing populations and a preferred qualified interpretation. [BG-004; BG-011; Reasons p.33.]

These are demonstrated properties of the supplied artifacts. The improvements below have not yet been tested.

## 2. Interventions worth testing

| Intervention | Concrete test suggested by Providence | What success could establish | What it would not establish |
|---|---|---|---|
| **One fixed workbook writer** | Feed unchanged reviewed records into the five-sheet layout; validate all keys, prior-version chains and native links. | Removal of formatting/link/serialization failures; lower navigation burden. | Better reading, correct prices, correct event existence, or correct research judgments. |
| **Clean, stable source preparation** | Preserve complete background paragraphs, bullets and printed pages; add the specific full-filing sections needed for parties, final terms and contradictions. | Fewer locator errors and easier access to premises. | That the model used all relevant text, or that a shortened excerpt contains every important fact. |
| **Typed date and precedence checks** | “Had approached” cannot silently become an exact reporting-day action; a representative exclusion date cannot precede its prerequisite selection. | Detection of inconsistent stored dates and suspicious date-basis claims. | The correct date when no date is disclosed; whether two partially ordered events truly precede one another. |
| **Proposal-history and population checks** | Reject forward/cyclic prior-offer links; distinguish E's restored offer, group envelopes, six bidding units and seven LOI versions. | Internally consistent representations and denominators. | Correct identity mappings or complete event coverage; a perfectly consistent invented population remains possible. |
| **Targeted contradiction review** | Compare `bidder_excluded` with a local note that continued diligence was permitted; compare B's “unconditional” label with ongoing diligence. | Detection of a defined class of claim/evidence tensions. | A guarantee that unflagged claims are correct or that one keyword determines the legal/economic interpretation. |
| **Whole-source coverage pass** | Check that the narrative's reversion, non-submissions, final refusal and signing/announcement all have usable records. | Measurable reduction in omissions on tested cases. | Complete recall merely because the model says it checked coverage. The pass needs independent grading. |
| **Small adjudicated example set** | Include positive and negative examples: actual withdrawal versus adverse notice with continued participation; markup versus target template; financing support versus joint bidding. | More consistent application of a settled definition on held-out cases. | That the system has learned a universal rule rather than copied the examples. |

The first, third and fourth interventions should be relatively contained engineering tasks because they operate on explicit structures. Their economic value still needs measurement. Do not build a large orchestration system before testing whether this smaller layer materially improves research-ready outputs.

### Source preparation should preserve context, not replace it with a model summary

A useful source pack would contain the complete background, stable locators and a small source index to additional filing sections. It should retain the original HTML or PDF for verification. An excerpt-only workflow would have missed the overall 25-NDA statement outside Providence's background. A summary-first workflow might silently reconcile that conflict before the extractor sees it.

There is primary research showing that performance on some long-context tasks depended on where relevant information appeared. That work studied earlier models and tasks, not these four September 2026 configurations. It supports **testing position and source-layout sensitivity**, not a claim that any particular current model must fail on long filings. [Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*, 2023, arXiv:2307.03172.]

### Checks need external evidence, not just “think again”

Asking the same model to review everything again may sometimes help, but that has not been demonstrated here. A better experiment supplies a specific detected conflict, the relevant source paragraphs and a requirement to preserve or revise the field with an explicit reason. Check whether the repair fixes the targeted issue **and introduces no new errors**.

Research on intrinsic self-correction found limitations, including deterioration in some tested reasoning settings without external feedback. Those experiments do not establish a timeless inability of language models, or measure the present models. They are a reason not to treat an unaudited second answer as an independent certificate. [Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, 2023, arXiv:2310.01798.]

### An automatic critic is an experiment, not a replacement for Alex

A model-based critic may help detect scope, identity, event-agency and evidence problems that are difficult to encode. It may also agree with an incorrect extraction, prefer its own style or collapse a legitimate ambiguity into a false consensus.

A practical evaluation should combine deterministic checks, coverage/groundedness review and expert adjudication; the critic's results themselves must be calibrated. Anthropic's January 2026 engineering discussion makes this distinction between code-based, model-based and human graders, and emphasizes repeated trials and examination of actual outcomes rather than success claims. That is useful methodological guidance, not evidence that this project is ready for automatic approval. [Anthropic, *Demystifying evals for AI agents*, 9 January 2026.]

## 3. Which candidates deserve development attention?

**DeepSeek is the most interesting lower-ranked research candidate in this comparison**, subject to obtaining actual economic records. It already preserved many core facts, coherent proposal histories and exact quotations. Its date-basis errors, a deadline-link mistake and some missing final offer-state representation are sufficiently concrete to support a focused intervention. Whether the model can repair them reliably when given better source structure and checks remains untested.

**Muse is not my first optimization target.** A shared writer may fix some of its linkage failures, so those should not be taken as proof of an intrinsic reading limitation. But its inconsistent NDA population, broad event bundles, sparse/nonverbatim evidence and unsupported CVR cash coding mean that formatting repairs alone would leave substantive concerns. Test it after establishing the shared writer rather than building a special rescue architecture around this one output.

**Fable is a useful near-quality comparator, not automatically a cheap option.** Its local explanation correctly preserves G&W's continuation while its event code does not. That suggests an intervention aimed at categorical/narrative consistency could help this run. Its E formality and prior-response-round choices should not be “corrected” by rote; they depend on the approved coding policy. Nothing supplied proves that Fable is cheaper than Astra or that either has lower total review cost.

**Astra should receive the shared improvements too.** A stronger reading configuration is not a reason to tolerate poor dates, excessive tables or stale export mechanics. Comparing a carefully engineered cheap workflow against an unassisted strong model would confound engineering and model quality. The stronger baseline should use the same source preparation, writer and deterministic checks.

## 4. A staged experiment, without changing extraction now

### Stage A — separate writer errors from reading errors

Freeze the current source files and original outputs. Create a canonical, reviewed representation of Providence that explicitly includes uncertainty and alternative conventions. Feed that **unchanged content** to the writer and test table integrity, numeric types, source access, correction workflow and reading order.

This establishes whether presentation and serialization can be made reliable independently of extraction. It does not test a model's ability to extract the content.

The supplied demonstration starts this separation, but it is not a locked human-adjudicated gold standard. Alex/Austin still need to approve its policy-dependent decisions.

### Stage B — a matched Providence diagnostic rerun

Run the stronger baseline and candidate with identical complete sources, policy version, writer and permitted tools. Preserve full prompts, model build, reasoning settings, sampling/output settings, tool traces, retries, repairs, costs and elapsed times.

Compare: unassisted extraction; extraction plus deterministic checks; extraction plus a narrowly targeted repair pass. Change one support component at a time where feasible. Include repeated independent runs, not only a best-of-several example.

This could show that a specific intervention remedies a Providence failure class. It cannot establish generalization. The current base instruction itself contains Providence, Mac-Gray and PetSmart calibration facts, so none of those is an untouched blind holdout.

### Stage C — new, diverse, independently adjudicated deals

Use a development set for rule refinement and a genuinely held-out set that is not used to revise prompts. A pilot might begin with a few dozen deliberately varied new cases, but that is a development scale suggestion, **not a validated sample-size threshold**.

Include structured and loosely narrated processes, anonymous cohorts, late entrants, repeat processes, consortium changes, price ranges/alternative structures, contingent consideration, downward revisions, weak/strong deadlines, price-to-value conversion problems and partial-asset scope issues. Test ordinary cases too: an edge-case-only set cannot measure routine overflagging or ordinary review burden.

Reference labels must be checked against actual filings. Alex's nine annotated deals are valuable calibration material but not automatic ground truth; the remaining Chicago-RA spreadsheet is not a trustworthy label set. A reviewed correction must be tagged as a filing fact, reasonable inference, approved convention or unresolved question.

Where reasonable conventions differ, grade whether the system represents and applies the chosen policy, not whether it happens to match one evaluator's unapproved preference.

### Stage D — judge readiness, not cosmetic improvement

Evaluate at least five separate outcomes:

1. **Material factual precision and coverage:** unsupported assertions and missed economically important events.
2. **Judgment fidelity:** scope, identity, phase, formality, conditions, agency and price meaning, graded against explicit rubrics.
3. **Consistency and chronology:** complete key chains, correct denominators, no impossible precedence and honest date precision.
4. **Human work:** time to review and correct, number and severity of edits, repeated questions, and need to reopen the source.
5. **Operational reliability:** failure/retry rate, output truncation, repair regressions, total model calls and run-to-run variation.

Audit both flagged items and a sample of unflagged/high-confidence items. Otherwise a system can appear reliable by failing to flag its mistakes. Do not use a workbook's own “pass” declaration as an outcome.

Use paired deal-level comparisons against the stronger workflow; do not treat hundreds of correlated cells as hundreds of independent trials. Specify acceptable margins and unacceptable error classes before reviewing the final holdout. Report uncertainty and case-level failures, rather than a single pooled accuracy number that hides catastrophic mistakes.

Only after those tests should Austin and Alex decide whether to try a restricted shadow deployment, a reviewed subset or broader adoption. Success on Providence alone cannot authorize that decision.

## 5. What code cannot solve by itself

A checker can prove that a referenced key exists. It cannot prove that the key points to the right event unless the semantic relationship has also been validated.

It can reject a date outside stored bounds. It cannot prove the stored bounds came from the right sentence.

It can verify that quoted words occur in the filing. It cannot infer that “had advised by April 27” means “advised on April 27”—indeed, that inference is the problem.

It can add seven and one. It cannot resolve whether an unidentified later consortium member belongs to an earlier invitation population.

It can preserve every candidate event. It cannot decide automatically that an issues summary is a formal bid when the research team has not fixed that threshold.

These limits point toward a mixed system with a small deterministic core and substantive model/human judgment, not a code-only parser. The same warning applies to model voting: agreement among models is evidence of agreement, not independent proof from the filing.

## 6. Economic assessment and stopping rule

The relevant unit is **cost per acceptably reviewed deal**, not the price of one model call. A useful accounting identity is:

\[
C_{\text{reviewed deal}}
= C_{\text{initial extraction}}
+ C_{\text{checks and extra calls}}
+ C_{\text{retries and repair}}
+ C_{\text{human review and correction}}
+ \frac{C_{\text{development and maintenance}}}{N}.
\]

Each term must be measured under comparable quality requirements. If a repair workflow calls the strongest model on most deals, the nominally cheaper first call may simply add cost and delay. If it creates difficult-to-detect errors, those are a research-validity constraint, not merely another inexpensive correction.

For this project, I would start with the **shared writer, source preparation and deterministic checks** because they address observed defects and improve the quality-first baseline as well. I would then time-box a DeepSeek diagnostic experiment rather than committing to model-specific fine-tuning or a many-agent pipeline.

Proceed only if the candidate meaningfully reduces total reviewed-deal effort while meeting the pre-agreed quality bar on new cases. Stop or defer if gains disappear once human correction, retries and stronger-model rescue are counted, or if material unflagged errors remain hard to detect. No numerical break-even claim is justified by the data supplied.

Fine-tuning may become worth considering once there is a sufficiently varied, source-adjudicated training set and a locked evaluation protocol. At present, rules, examples and feedback histories are cheaper hypotheses to test than training a specialized system—but even that relative development judgment needs actual effort records. Do not train disputed annotations as settled labels.

## Bottom line

**Worthwhile now:** improve the shared review/writing infrastructure and establish a reproducible evaluation protocol.

**Worth testing later:** whether a lower-cost candidate, with that same support, can match the stronger workflow's substantive quality and lower total human-plus-model effort.

**Not established:** that Providence repairs generalize, that extra model calls create independence, that any supplied model is economically cheaper in this workflow, or that human verification can be reduced.

Continue the current strongest-model policy until a mature alternative has been demonstrated and you explicitly approve adoption.

## Primary sources used for methodological context

These sources were not used to decide Providence's transaction facts or rank the supplied workbooks.

- Nelson F. Liu et al. (2023), *Lost in the Middle: How Language Models Use Long Contexts*. https://arxiv.org/abs/2307.03172
- Jie Huang et al. (2023), *Large Language Models Cannot Self-Correct Reasoning Yet*. https://arxiv.org/abs/2310.01798
- Anthropic (9 January 2026), *Demystifying evals for AI agents*. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
