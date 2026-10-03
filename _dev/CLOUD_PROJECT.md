# The Claude Code project

Development of sec-auction happens in one Claude Code project at claude.ai/code (also in the desktop app's Code tab and the mobile app). This page records how the project is set up, so it can be rebuilt. Docs: [Projects](https://code.claude.com/docs/en/claude-projects), [cloud environments](https://code.claude.com/docs/en/cloud-environments), [Remote Control](https://code.claude.com/docs/en/remote-control).

## How the parts fit

- **Project conversation:** Austin sends tasks there. Claude starts a thread for each task and tracks it in the **Overview** pane.
- **Cloud threads:** each thread is a fresh clone of `extraction-v2` on an Anthropic machine. It works on its own branch and opens a pull request. Austin merges. Nothing outside git survives the thread.
- **VM threads:** for a task that needs the VM (Codex, paid runs, the live cockpit), choose **Work locally** in the project. The thread then runs on the VM through Remote Control, with the VM's files, tools and logins.
- **What every thread reads:** [AGENTS.md](../AGENTS.md), [CLAUDE.md](../CLAUDE.md), the project instructions below and, in cloud threads, project memory.

## 1. GitHub

1. Install the Claude GitHub App on `Austin-j-li/sec-auction`: https://github.com/apps/claude. A `/web-setup` token is not enough for a project.
2. Check the repository under **Repository access** at https://github.com/settings/installations.

## 2. Cloud environment

Create it at claude.ai/code from the environment selector, then **New environment**.

- **Name:** `sec-auction`
- **Network access:** **Custom**. Check **Also include default list of common package managers**. Allowed domains:

  ```text
  www.sec.gov
  ```

  `fetch_filing.py` needs this domain to download filings from EDGAR.
- **Environment variables:** none. Values here are readable by anyone who uses the environment, so never put a token here.
- **Setup script** (it runs before the clone, so it names the packages in [requirements.txt](tools/requirements.txt); keep the two in step):

  ```bash
  #!/bin/bash
  python3 -m pip install --break-system-packages openpyxl==3.1.5 beautifulsoup4==4.15.0 lxml==5.2.1 \
    || python3 -m pip install openpyxl==3.1.5 beautifulsoup4==4.15.0 lxml==5.2.1
  ```

## 3. The project

1. Open **Projects** in the sidebar, then **New project**.
2. **Name:** `sec-auction`. **Goal:** `Build and check the Version 1 deal-ledger pipeline for Austin and Alex's takeover-auction research.`
3. **Context:** add the repository `Austin-j-li/sec-auction`. Add nothing else.
4. Click **Create project**. If Claude posts **Setup recommendations**, switch off every routine and thread it suggests.
5. **Project settings > Environment:** choose the `sec-auction` environment.
6. **Project settings > General:** thread model Opus 5.5 at high effort, coordinator Opus 5.5 at low effort. Extraction runs choose their own model through the runner, so these settings do not change Version 1 results.
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
- Any paid model run: run_model.py launch, effort_sweep.py run, codex exec or claude -p. Launch only the runs he names.
- Any change to SEC_Deal_Ledger_Extraction_Instruction.md.
- Anything that touches the live cockpit or its deployment folder on the VM.

Where things run
- Cloud threads cannot reach the VM. Paid runs, Codex (Astra and Sol) and the cockpit live on the VM. When a task needs them, stop and ask Austin for a "Work locally" thread on the VM.
- Extraction must stay blind. Never put Alex's hand-coded answers from ref/, or codings from reviews and comparisons, into project memory or into the instructions.

When something is missing
- If you cannot reach something you need (a domain, a secret, a tool, a file), say exactly what is missing in your first message and stop. Do not substitute, mock or guess.

Reports
- Write for Austin in the plain style of CLAUDE.md. Start with what changed for the deal ledger.
```

## 4. Remote Control on the VM

The VM runs `claude remote-control` as the user service `sec-auction-remote.service`, in `~/work/Projects/sec-auction`, with `--spawn worktree`. Each VM thread gets its own git worktree, so threads do not overwrite each other or the checkout. The live deployment folder `~/work/Projects/ledger-live` is not part of it.

First start, once:

1. Log in to the VM: `ssh condenser-vm`.
2. Accept the workspace trust prompt: `cd ~/work/Projects/sec-auction && claude`, accept, then type `/exit`.
3. Start the service: `systemctl --user enable --now sec-auction-remote.service`.
4. Check it: `systemctl --user status sec-auction-remote.service` and `journalctl --user -u sec-auction-remote.service -n 30`.

Then, in the project, choose **Work locally** from the **+** menu, write the task and click **Allow once** on the card. A VM thread starts with the project instructions but not with project memory.

Anyone signed in to Austin's claude.ai account can then run commands on the VM. Turn the service off with `systemctl --user disable --now sec-auction-remote.service` when it is not needed. A project cannot run VM threads while **Require trusted devices** is on.

The bastion certificate (`~/.ssh/id_condenser.signed` on the Mac) still expires every 7 days. Remote Control does not need it, because the VM connects out to claude.ai.
