# Astra Fast batch: release packet

Prepared on 12 October 2026. No live deployment, extraction, or replacement took place during these checks.

## Request and current state

Austin requested fresh Astra xhigh extractions for all listed deals, with Fast service and parallel execution. He authorized replacement of their working copies through the browser. He first required confirmation that the cockpit was current.

The cockpit was not current. The clean live checkout used `a8ecea3d35e57a8c1f6201753f82022318da2ecb`. GitHub's merged branch used `58675c97fc9bc3018bd7bea21e7691ae484fc8bd`, which includes PR #18. This release starts from that merged commit.

The live cockpit, worker, and backup timer were active. The live queue had no unfinished jobs. The browser showed Austin with edit access.

The 12 listed deals were Datalink, Kraton, Mac-Gray, Penford, PetSmart, Providence & Worcester, sTec, Synacor, Medivation, Zep, Pepco Holdings, and Imprivata. Each working copy used its 28 September Opus 5.5 medium original at revision 0. Meredith was absent from the list.

The default instruction was v1.1, ID `e77059e96146`, SHA-256 `e6e1e2f3b53378bdb6770762d33fe9b84090c2ae27301d5bf725e0c3f629eb13`.

## Change

- The Astra dialog offers a Fast service checkbox.
- The job records the selected tier. The worker passes it to the sandbox runner.
- The runner records `priority` and passes the Fast settings to Codex.
- Job and original-version labels include Fast when the receipt requests it.
- Environment variables control the queue limits. Defaults remain four total and two per user.
- The dialog shows the account's per-user limit.

No database migration or instruction change is required. The runner change is identical to the corresponding change in PR #19. This release does not depend on the comparison report or sweep tool in that PR.

## Consumer verification

No tests or test suites ran. No live extraction was submitted.

1. Built the frontend with `npm run build`. The build completed. It reported the existing large-bundle warning.
2. Used the real job interface with Datalink and a separate copy of the live database. The queued job recorded Astra, xhigh, priority, and the exact v1.1 identity. No worker ran against that copy. See [queued_job.json](queued_job.json).
3. Prepared the real Datalink filing through the sandbox CLI. The metadata recorded Astra, xhigh, priority, and the expected instruction and filing hashes. The generated provider command included `service_tier="priority"` and `fast_mode`. Preparation made no model call. See [prepared_runner.json](prepared_runner.json).
4. Read the actual queue configuration with both limits set to 12. It returned 12 total and 12 per user.
5. Opened a separate authenticated browser tab with the proposed frontend bundle. The tab blocked all API writes. Selected Astra, xhigh, and Fast. The dialog showed v1.1 and “Fast service requested.” The Start button was not used. See [dialog.png](dialog.png).
6. Closed the preview tab and its temporary routes. Closed the extraction dialog in the original live tab.

The preview used the old live account response, so it could not display the new limit field. The backend queue configuration was checked separately. The worker-to-provider path still requires observation during the authorized batch.

Fast receipts show the requested service tier. They do not prove the provider's delivered tier. This release does not repair the separate Medivation admission-count defect identified in the comparison review.

## Proposed release and batch

The release remains subject to Austin's deployment order under AGENTS.md and CLOUD_DEPLOYMENT.md. His extraction and replacement authorization already covers all 12 deals.

The prescribed ARC route also needs its protected credential in the release session. Here, `arc health` returned: `Set ARC_BRIDGE_TOKEN or supply --token-file`. No credential was displayed or copied. Local browser and read-only VM access worked; ARC access remains unverified.

1. Select the full release commit after the branch and PR exist.
2. Recheck the live queue and runner processes.
3. Follow the release lock, backup, checkout, and service steps in [CLOUD_DEPLOYMENT.md](../CLOUD_DEPLOYMENT.md).
4. Set both concurrency limits to 12 for this batch. Preserve the previous service configuration.
5. Confirm the deployed commit and the authenticated browser controls.
6. Submit one fresh Astra xhigh Fast extraction for each of the 12 listed deals, with v1.1.
7. Record job IDs and verify the model, effort, tier request, and instruction in their receipts.
8. Use each completed original as the base of that deal's working copy through the browser.
9. Verify all 12 replacements. Preserve the old originals and revision history.
10. Restore the earlier concurrency limits after the jobs finish.

The app's “Use as base” action creates a new revision. It preserves the prior original and working-copy history.
