# Astra default, verified Pro findings and proposed amendment

26 September 2026. Austin authorized the Astra default switch, source verification of Pro's findings and an amendment proposal. This packet records those three distinct outcomes.

## Read first

> **Status note, 26 September 2026 (after the v1.14.1 candidate).** This packet is history. The amendment spec is superseded by [V1141_SPEC](../2026-09-26-v1141-streamline/V1141_SPEC.md) §7, except P1, which [PIPELINE_UPGRADE_SPEC](../2026-09-26-v1141-streamline/PIPELINE_UPGRADE_SPEC.md) WP3 implements. [DECISION_BRIEF_2026-09-26.md](DECISION_BRIEF_2026-09-26.md) §§1–4, §6 and §7 are resolved (R1–R6). The Astra-high default below was reversed the same day: Opus 5.5 at medium effort is the default extractor again, decided and built in both trees, and live after the WP1 deploy (a GATE); until then the live services still default to Astra high.

> **Status, 26 September, about 20:45 UTC.** The reversal is live: the WP7 deploy at 19:41 UTC made Opus 5.5 at medium effort the default extractor ([receipt](../2026-09-26-v1141-streamline/deployment-v1141.json)). GPT-6-Astra stays selectable, with high effort as its own default. The Astra-high default described below is history.

1. [Amendment spec for approval](AMENDMENT_SPEC.md): retain the v1.14 taxonomy; four small wording clarifications, an analysis-output amendment and focused acceptance checks. **Proposed only.**
2. [Source verification](PRO_FINDINGS_VERIFICATION.md): 26 deal-level findings, important qualifications to Pro's preferred readings, relevant Alex voice passages and a reproduced analysis-tool gap.
3. [Pro's original PDF](/home/uctpiaj/work/Projects/sec-extraction/_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/SEC_Anonymous_Extraction_Review.pdf) and [unblinded scores](/home/uctpiaj/work/Projects/sec-extraction/_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/UNBLINDED_RESULTS.md). The verification does not change those scores.

## Implemented: Astra high as the default

The live cockpit defaults to GPT-6-Astra high when the user's ChatGPT account is connected. Explicit choices remain available; the existing behavior chooses a connected engine if the preferred account is unavailable. The isolated runner's `prepare` command also defaults to Astra high when provider/model/effort are omitted. Historical jobs without an engine selection remain Opus jobs, not retroactively relabelled Astra jobs.

The backend, worker's legacy fallback, frontend and runner were changed narrowly, with routing/history tests. Matching changes were merged into the separate v1.14 upgrade worktree while retaining its other work. Its documentation now points to this update. The old release/deploy patches have a reconciliation notice; they must be regenerated against the new baseline before use.

Both main services restarted at **12:02:33 UTC on 26 September** after checking that no jobs were active. The new main frontend build was deployed, with old available assets retained for open tabs. The authenticated live extraction dialog displayed **GPT-6-Astra · high · v1.13.2 · on Austin's ChatGPT plan**. It was closed without starting a run. See [deployment receipt](deployment.json) and [live dialog verification](live-dialog-verification.json).

**The instruction default is still v1.13.2.** Changing the model default did not publish v1.14, deploy its upgrade code or alter an extraction.

## Validation

| Check | Evidence |
|---|---|
| Main backend/runner focused tests | [73 passed](python-tests.log), using fixture transports. |
| Main frontend routing tests | [23 passed](frontend-tests.log). |
| Main frontend build | [Build passed](build.log); existing bundle-size warning. |
| Upgrade backend/runner focused tests | [68 passed in the final run](upgrade-final-tests.log). An earlier fixture relied on implicit Opus selection; it now selects its intended engine explicitly. The original failure and targeted rerun are retained in `upgrade-tests.log` and `upgrade-retest.log`. |
| Upgrade frontend routing tests | [27 passed](upgrade-frontend-tests.log). |
| Production smoke check | Authenticated default selection verified; no extraction invoked. |
| Preservation | [Receipt](preservation-verification.json): main frozen instruction, catalog and all nine raw workbooks unchanged; all 22 manifest-listed Pro inputs unchanged; no new extraction jobs since work began. |
| Analysis diagnostic | Offline derivation of Mac-Gray A reproduced two blank-price Bid rows marked as price observations; [output](analysis-diagnostics/mac-gray/bids.csv). The analysis tool itself was not edited. |

The tests establish routing, fallback and fixture behavior. Source verification, not test counts, supports the extraction findings. This work does not certify any workbook as research-ready, revalidate all 1,024 quotation matches or settle the remaining analysis choices for Alex.

## Scope and provenance

- Main checkout: `/home/uctpiaj/work/Projects/sec-extraction`, branch `extraction-v2`. It already contained uncommitted work; the default delta was applied without reverting it.
- Upgrade checkout: `/home/uctpiaj/work/Projects/sec-extraction-v114`, still undeployed.
- Trial raw/anonymous outputs: `_dev/reviews/2026-09-26-v114-15-run-trial/` in the main checkout. They were moved there from the `sec-extraction-v114-trial-20260926` worktree, which was removed on 26 September. Its code duplicated `sec-extraction-v114` before the Astra-default change.
- Pre-change snapshots: `before.json`, `pre-change/`, `upgrade-pre-change/`. These isolate this task's changes from the pre-existing dirty trees.
- `astra-default.patch` is the initial main code/test delta, not a complete release patch. [task-delta.json](task-delta.json), [main delta](task-delta-main.patch) and [upgrade delta](task-delta-upgrade.patch) record the completed source/document changes against their pre-task snapshots. The historical release patches are not refreshed or applied in this task.
- Reading evidence is under `evidence/`. Copied text and cell dumps support review; the original filings and workbooks remain authoritative.

No instruction or workbook was edited, no new model extraction was launched, and no commit or push was made. Instruction/analysis changes and questionnaire reconciliation are proposed in the amendment spec, not implemented.