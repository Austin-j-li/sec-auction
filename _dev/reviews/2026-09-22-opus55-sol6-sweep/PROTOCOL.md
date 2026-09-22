# Opus 5.5 and GPT-6-Sol extraction sweep: protocol

Written 22 September 2026, before any sweep output existed. Austin authorized the design in this session: "a lean ladder of 3 deals, and we try only opus med and opus high, and then sol high and sol xhigh", with no Opus 5 control arm.

## Question

Which of four extraction configurations gives the best v1.13.2 workbooks for its cost and time?

| Arm | Provider | Model | Effort |
|---|---|---|---|
| `opus-5-5-medium` | Claude Code (`opus`) | `claude-opus-5-5` | medium |
| `opus-5-5-high` | Claude Code (`opus`) | `claude-opus-5-5` | high |
| `gpt-6-sol-high` | Codex (`sol`) | `gpt-6-sol` | high |
| `gpt-6-sol-xhigh` | Codex (`sol`) | `gpt-6-sol` | xhigh |

## Fixed for every cell

- **Inputs.** The frozen instruction v1.13.2 (SHA-256 `513c8e3e…`), one filing from `raw_filing/` (hashes in `MANIFEST.csv`) and the unchanged launch prompt. `pin.json` records the runner, instruction and both provider binaries at the first launch, and the driver refuses any change after that.
- **Binaries.** Claude Code 2.1.280 is a pinned copy (`_dev/runs/.pinned/claude-2.1.280`, SHA-256 `1e08503d…`). Codex is 0.155.1, as a versioned standalone release.
- **Sandbox.** Bubblewrap with fresh provider state, one instruction, one filing and one output directory. The scratch home and `/tmp` last only for the run.
  - **Opus** sees only Bash, Read and Write. Refusal fallback is off, the one-hour cache lifetime is pinned, and the silent-turn reminder is off. If a session ends before a readable four-sheet workbook exists, it is resumed at most twice.
  - **Sol** sees shell commands and file patches only. Codex's app connectors, web search, browser, computer use, image generation and subagents are disabled; code mode stays on because GPT-6-Sol requires it. Codex has no continuation, so the two providers differ here. Continuations are counted and reported.
- **Authentication.** Opus uses a long-lived subscription token passed through an inherited pipe. Sol uses the host Codex login, bound read-only; preflight refuses a Sol run when that login's access token has less than seven hours left.
- **Scoring instruments.** The checker `_dev/tools/check_lean.py` runs outside the sandbox after each run. The reference tests are `reference/<deal>.json`. `protocol-freeze.json` records the hashes of the checker, the references and this protocol, and none of them changes during the sweep.

## Design

- **Deals:** Mac-Gray, Datalink and Synacor. Mac-Gray and Datalink have the strongest lead-verified references. Synacor has the hardest process and round map.
- **Size:** 4 arms × 3 deals × 2 replicates = 24 cells.
- **Order:** `effort_sweep.py plan` with seed `20260922`. Each replicate block runs every deal-arm pair once in a seeded random order, so the arms share the same time window.
- **Execution:** at most 4 cells at once, with a 150-minute limit per cell. Three consecutive provider or worker failures stop new launches. Such failures can be retried and are reported, never scored.

## Measures

1. **Primary: reference-test score, 0–100 per workbook.**
   - Each deal's frozen tests carry weights: participation 30, rounds 25, formality and conditions 20, chronology 10, bids and prices 10, deal facts 5.
   - Each test is graded pass (1), partial (0.5) or fail (0), with the ledger rows cited.
   - Grading is blind. Graders get a copy of the workbook with its document properties cleared under an opaque label, plus the filing, the instruction and the tests. They get no logs, costs, times, final reports or arm labels.
   - Each workbook gets three independent graders: two fresh Claude Opus 5.5 agents and one GPT-6-Astra agent. Astra runs through Codex in read-only mode with web, connectors and subagents disabled; Austin approved this grader on 22 September.
   - The primary score is family-balanced: the mean of the two Claude scores, averaged with the Astra score.
   - Each family's scores, the Claude–Claude and Claude–Astra agreement, and every item where graders differ by a full credit level are reported.
   - Scores are frozen with a hash before unblinding.
2. **Secondary:**
   - checker errors by code, with warnings reported separately (known false-positive classes noted);
   - agreement between replicates of the same arm and deal: bid multiset Jaccard, same round count, event-count gap;
   - run health: failures, continuations, and network, web, connector or subagent use found in the event logs.
3. **Cost and time:**
   - Opus: list-price cost repriced by one formula at $4/$20 per million input/output tokens, $0.20 per million cache reads and $8 per million one-hour cache writes.
   - Sol: tokens and reasoning tokens only, since Codex reports no cost.
   - Both: wall time. Subscription usage is not billed per token, so costs across the two providers are not directly comparable.

## Decision rule

The report gives each arm's mean score, per-deal scores and the range across replicates. Within a provider, the higher effort is preferred only if its mean score exceeds the lower effort's by more than the larger of 2 points and the pooled replicate spread, on at least two of the three deals. Otherwise the lower effort is recommended. Across providers the report states the evidence (score, stability, failures, time and tokens); the choice is Austin's. With six workbooks per arm, differences of a few points are not distinguishable.

## Limits stated in advance

- **Familiar deals.** The three deals are development deals, and the instruction was developed on them. This is a comparison between arms, not an estimate of accuracy on unseen filings.
- **Model-built references.** The references were written by Claude Opus 5.5 agents from the filing, the lead-verified corrections and earlier reviews. Each was checked by three independent verifier lenses, but none has been human-adjudicated. Some items rest on conventions that are still open; these carry accepted alternatives or are left unscored.
- **Grader families.** Claude graders could favour Claude-written workbooks, and a GPT grader could favour GPT-written ones. The primary score gives each family equal weight. Each family's scores are reported, so any bias shows as a family-by-arm pattern. The references were built by Claude agents, which is a further limitation on the Sol arms.
- **Early and late failures:**
  - A Sol run that stops early is not resumed, while an Opus run is resumed at most twice.
  - A run killed at its time limit counts as a failure of its arm, not as a missing value.
