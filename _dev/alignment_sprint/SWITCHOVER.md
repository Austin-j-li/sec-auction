# Version 1 switch-over

This file is the dated record of the fresh-state cutover of 28 September 2026. The cutover is complete. Do not repeat it.
For a release, use [CLOUD_DEPLOYMENT.md](../CLOUD_DEPLOYMENT.md). For a repository export, see the [cockpit README](../cockpit/README.md#repository-export).
The step-by-step runbook and its rollback section were deleted on 13 October 2026. Git history keeps them. Line references to this file in the build records point to that runbook.

## Deployment record, 28 September 2026

Run on Austin's order ("hard switch and get rid of the old version").
- Deployed commit `4dd04c19c004e1e9b32a578e988a954702e52986` at `~/work/Projects/ledger-live` (detached worktree of `sec-auction`); root instruction SHA-256 `05d8668d…05de4`; committed `dist/` matched a fresh build of its source.
- Old app drained (no outstanding jobs or runners), then stopped. Final backup `~/backups/ledger-cockpit/version-1-20260928-123713/` (integrity ok) and state archive `~/backups/ledger-state-before-version-1-20260928-123713.tgz` (SHA-256 `ca3cc60b…fd82db`). The archive holds the eight edited working copies to carry into Version 1 reviews by hand.
- Fresh state: 3 accounts, 4 added deals, 4 filings; no old instructions, jobs or work. The app shows 13 deals; Version 1 is the only instruction and the default, seeded as "System".
- Drop-ins 40-version-1-deploy.conf installed for the cockpit, worker and backup units (tracked copies deleted 13 October 2026). Cloudflare Access: team domain `https://divine-flower-e89f.cloudflareaccess.com`, AUD `8050c359…51f049` (both read from the site's Access redirect), plus `COCKPIT_REQUIRE_ACCESS=1`.
- Checks: a forged email header and an unsigned loopback request both get `unknown`, `can_edit` false; Austin's browser session via Access gets `austin`, `can_edit` true. Alex's sign-in not yet observed.
- On Austin's order the old version was then deleted without the one-week wait: `~/work/Projects/sec-extraction`, `sec-extraction-v114`, `sec-extraction-archive` and the old nightlies in `~/backups/ledger-cockpit/`. Their Git history stays on GitLab (`vm-live-2026-09-26`, `vm-v114-2026-09-26`). **Rollback is no longer possible.** `~/backups/vm-checkouts-2026-09-27.tgz` is kept for now as the only copy of the untracked `lesson/` notes.

## Redeployment, 29 September 2026

On Austin's order ("make sol 6.1 selectable in the cockpit webapp"): no queued or active jobs; the deployment worktree moved from `4dd04c1` to `9f0750e` (GPT-6.1-Sol engine, rebuilt `dist/`, docs); `ledger-cockpit` and `ledger-worker` restarted, backup timer untouched. The served page loads the new bundle and the deployed `ENGINES` lists `sol61`.
