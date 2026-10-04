# The Claude Code project

Development of sec-auction happens in one Claude Code project at claude.ai/code (also in the desktop app's Code tab and the mobile app). This page records how the project is set up, so it can be rebuilt. Docs: [Projects](https://code.claude.com/docs/en/claude-projects), [cloud environments](https://code.claude.com/docs/en/cloud-environments), [Remote Control](https://code.claude.com/docs/en/remote-control).

## How the parts fit

- **Project conversation:** Austin sends tasks there. Claude starts a thread for each task and tracks it in the **Overview** pane.
- **Cloud threads:** each thread is a fresh clone of `extraction-v2` on an Anthropic machine. It works on its own branch and opens a pull request. Austin merges. Nothing outside git survives the thread.
- **VM access from cloud threads:** use the installed `arc` client and protected credential for `arc.dealextract.org`. Deployment stays in the cloud task. Follow [CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md).
- **VM threads:** Remote Control through **Work locally** remains optional.
- **What every thread reads:** [AGENTS.md](../AGENTS.md), [CLAUDE.md](../CLAUDE.md), the project instructions below and, in cloud threads, project memory.

## 1. GitHub

1. Install the Claude GitHub App on `Austin-j-li/sec-auction`: https://github.com/apps/claude. A `/web-setup` token is not enough for a project.
2. Check the repository under **Repository access** at https://github.com/settings/installations.

## 2. Cloud environment

Create it at claude.ai/code from the environment selector, then **New environment**.

- **Name:** `sec-auction`
- **Network access:** Full, as configured on 4 October 2026.
- **Protected API credential:** Condenser and Myriad, host `arc.dealextract.org`.
- **Setup script:** preserve the pinned project dependencies and the shared research setup.
  The shared setup installs `/usr/local/bin/arc` and `/usr/local/bin/claude-gpt`.
  It also installs the research tools under `/opt/claude-research`.
- **Credentials:** reuse the protected ARC credential. Never copy it to the setup script or plain variables.
- **Deployment:** no Cloudflare token is needed for an ordinary release of the VM app.

Setup changes apply to new cloud sessions. Existing sessions with ARC access can use the deployment route directly.
Verify access from the actual project environment with `arc health` and the commands in [CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md).

## 3. The project

1. Open **Projects** in the sidebar, then **New project**.
2. **Name:** `sec-auction`. **Goal:** `Build and check the Version 1 deal-ledger pipeline for Austin and Alex's takeover-auction research.`
3. **Context:** add the repository `Austin-j-li/sec-auction`. Add nothing else.
4. Click **Create project**. If Claude posts **Setup recommendations**, switch off every routine and thread it suggests.
5. **Project settings > Environment:** choose the `sec-auction` environment, and turn on **Use worktrees in local folders**.
6. **Project settings > General:** thread model Opus 5.5 at medium effort, coordinator Opus 5.5 at low effort (both defaults). Extraction runs choose their own model through the runner, so these settings do not change Version 1 results.
7. **Project settings > Memory > Project instructions:** paste the text below.

### Project instructions

```text
This project develops the sec-auction pipeline. It turns the "Background of the Merger" section of an SEC merger filing into an Excel deal ledger, for Austin Li and Alex Gorbenko's research on informal and formal bidding in takeover auctions. Repository: Austin-j-li/sec-auction. Read AGENTS.md, CLAUDE.md and _dev/STATUS.md before you change anything.

Branches and pull requests
- Start from extraction-v2. Open one pull request for each thread into extraction-v2. Do not merge it; Austin merges.
- On a long task, commit and push work in progress. A cloud sandbox can restart from a fresh clone.

Checks
- Verify a change by running the tool on real files, for example check_lean.py on a real workbook and filing. Report what you ran and what you saw. Do not write or run tests.

What needs Austin's word first
- Paid extraction runs: run_model.py launch, effort_sweep.py run, or direct extraction calls. Launch only the runs Austin names.
- GPT advice and development delegation follow Austin's shared GPT policy.
- Any change to SEC_Deal_Ledger_Extraction_Instruction.md.
- A release of the live cockpit requires a deployment request. That request covers the release steps in the same cloud task.
- Follow _dev/CLOUD_DEPLOYMENT.md. Do not request another approval for the same release.

Where things run
- Cloud threads reach the VM through arc exec condenser and the protected credential for arc.dealextract.org.
- Keep requested deployments in the same cloud task. Work locally is optional.
- Use claude-gpt for GPT help under Austin's shared GPT policy. Paid extraction runs retain their separate authorization rule.
- Extraction must stay blind. Never put Alex's hand-coded answers from ref/, or codings from reviews and comparisons, into project memory or into the instructions.

When something is missing
- If you cannot reach something you need (a domain, a secret, a tool, a file), say exactly what is missing in your first message and stop. Do not substitute, mock or guess.

Reports
- Write for Austin in the plain style of CLAUDE.md. Start with what changed for the deal ledger.
```

## 4. Optional Remote Control on the VM

The VM runs `claude remote-control` as the user service `sec-auction-remote.service`, in `~/work/Projects/sec-auction`, with `--spawn worktree`. Each VM thread gets its own git worktree, so threads do not overwrite each other or the checkout. The live deployment folder `~/work/Projects/ledger-live` is not part of it.

First start, once:

1. Log in to the VM: `ssh condenser-vm`.
2. Accept the workspace trust prompt: `cd ~/work/Projects/sec-auction && claude`, accept, then type `/exit`.
3. Start the service: `systemctl --user enable --now sec-auction-remote.service`.
4. Check it: `systemctl --user status sec-auction-remote.service` and `journalctl --user -u sec-auction-remote.service -n 30`.

Then, in the project, choose **Work locally** from the **+** menu, write the task and click **Allow once** on the card. A VM thread starts with the project instructions but not with project memory.

Anyone signed in to Austin's claude.ai account can then run commands on the VM. Turn the service off with `systemctl --user disable --now sec-auction-remote.service` when it is not needed. A project cannot run VM threads while **Require trusted devices** is on.

The bastion certificate (`~/.ssh/id_condenser.signed` on the Mac) still expires every 7 days. Remote Control does not need it, because the VM connects out to claude.ai.
