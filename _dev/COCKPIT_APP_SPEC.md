# Ledger cockpit as a shared extraction app: specification

Approved by Austin on 23 September 2026, including the §13 defaults. It builds on the deployed cockpit (`https://lines.dealextract.org`, [review guide](cockpit/README.md), [build contract](COCKPIT_BUILD.md)) and the isolated runner (`tools/sandbox/run_model.py`, [tools README](tools/README.md)).

## 1. Goal

Austin and Alex each log in with their own identity and, without a terminal or an agent conversation, can:

1. add a deal by searching the seed list or pasting an EDGAR link;
2. start an extraction on their own Claude or ChatGPT subscription, choosing the engine, effort and instruction version (default: GPT-6-Astra, high, current default instruction; Austin's 26 September update);
3. edit instructions as new versions, never altering a frozen one;
4. review and edit the shared working copy, and see what the other person changed or said, without being flooded.

The research guarantees stay as they are: blind, isolated extraction; immutable originals; offline checking after the run; attributed, restorable edits.

## 2. Decisions taken (23 September)

| Topic | Decision |
|---|---|
| Who may extract | Austin and Alex, each on their own initiative. |
| Deal sources | Search `ref/seed.csv` by name, or paste any EDGAR filing or index link. |
| Re-extraction of an edited deal | Adds a new read-only version. The working copy keeps its edits and base; changing its base is a separate, deliberate action. |
| Engines | GPT-6-Astra (default, high; Austin’s 26 September update), Claude Opus 5.5, Claude Fable 5.1 and GPT-6-Sol, at every effort the runner allows. Claude engines use the starting user's Claude plan; GPT engines use the starting user's ChatGPT plan. |
| Instructions | Editable in the app as new versions. Either user may publish a version and make it the default. Drafts may be run: the exact text is frozen under its hash and the version is labelled "draft instruction". |
| Version labels | Every extraction version states its engine, effort, instruction, who ran it and when (§6.3). |
| Trace | Recommended design in §8: threaded comments, a per-deal "since your last visit" digest, and last-changed-by on hover. No email, no live notifications. |

## 3. Non-goals

- No API-key billing. Each person's runs use that person's own subscription; the app never lends one user's credential to the other.
- No access to `ref/` answers, Alex's hand-coded workbook or evaluation scoring in the app. The seed's identifying columns are the only `ref/` data read, and only by the server.
- No model ranking or automatic acceptance. Checker output is mechanical; research acceptance stays a human judgment.
- No git writes from the app. Repository commits remain a separate, requested step (§11).
- No new users beyond Austin and Alex.

## 4. Architecture

```
browser ──Cloudflare Access──▶ server.py (HTTP, SQLite, no model or network calls in requests)
                                   │ enqueue job rows
                                   ▼
                           worker.py  (new systemd user service)
                             ├─ EDGAR fetch (SEC user agent, ≤4 req/s)
                             ├─ run_model.py prepare / launch  (bubblewrap sandbox)
                             ├─ check_lean.py  (outside the sandbox)
                             └─ import result as immutable version
```

- **Server** keeps its current rule: request handling makes no remote calls. Anything slow or external is a job.
- **Worker** (`ledger-worker.service`) claims jobs from SQLite, one transaction per state change, and survives restarts: on start it marks jobs whose process is gone as `failed: worker_restart`.
- **Store**: the ignored `_dev/cockpit/state/` directory, alongside `workspace.sqlite3`:
  - `filings/<deal>/<file>` plus a manifest row per filing (source URL, document, fetched time, bytes, SHA-256), as in `raw_filing/MANIFEST.csv`;
  - `instructions/<sha256>.md` (content-addressed);
  - `versions/<deal>/<version-id>/` with `workbook.xlsx`, `check.json` and the run receipts (`metadata.json`, `command.json`, `status.json`, `provider-results.json`);
  - `secrets/` for credentials (§5).
  The nine existing deals keep their files in `raw_filing/` and `extraction/`, read through `catalog.json` as now.
- **Backups**: a nightly job copies the SQLite database (online backup API) and the store to `~/backups/ledger-cockpit/`, keeping 14 days. The database is the only copy of working revisions and comments.
- **Capacity**: the VM has 64 CPUs and 125 GB RAM. A run is mostly waiting on the model, so the cap is set by subscription limits, not the machine: at most 4 concurrent runs overall and 2 per user, with the rest queued.

## 5. Accounts: "Connect your Claude / ChatGPT account"

A **Settings → Accounts** page lists, per user: Claude (not connected / connected, expires *date*) and ChatGPT (same), with Connect, Reconnect and Disconnect.

### 5.1 Claude (Opus 5.5, Fable 5.1)

- The worker starts `claude setup-token` in a pseudo-terminal with a scratch home. The page shows the sign-in link; the user opens it, approves with their own claude.ai login and pastes back the code shown. The worker feeds the code in, captures the one-year token and stores it.
- Fallback if the pseudo-terminal flow proves unreliable: the page explains how to run `claude setup-token` once on any computer and has a box to paste the token.
- Runs pass the token as the runner already does, through an inherited pipe (`CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR`), never in a command line, the sandbox environment or the run directory. The runner's `SEC_CLAUDE_OAUTH_TOKEN_FILE` becomes a per-user path.

### 5.2 ChatGPT (GPT-6-Sol, GPT-6-Astra)

- The worker runs `codex login --device-auth` with a per-user `CODEX_HOME`. The page shows the verification link and code; the user approves in their own ChatGPT account; the worker waits for completion.
- Refresh tokens rotate. The runner currently mounts `~/.codex/auth.json` read-only and refuses a run with under seven hours of access-token life, because a refresh inside the sandbox cannot be written back. Per-user credentials keep that rule. The worker refreshes a user's credential outside the sandbox, under a per-user lock and never during that user's GPT run, when less than 24 hours remain. The exact refresh command is spike S2.

### 5.3 Credential handling

- Encrypted at rest (a key file readable only by the service user, outside the repository), never returned to the browser, never logged.
- Every run records `account: austin|alex` and the provider, so a version always says whose plan paid for it.
- An engine whose provider the starting user has not connected is disabled in the Run dialog, with a link to Settings.
- Disconnect deletes the stored credential. The page also tells the user where to revoke it on claude.ai or chatgpt.com.

## 6. Extractions

### 6.1 Run dialog

Opened from a deal's toolbar (**Extract**) or right after adding a deal.

- **Engine**: GPT-6-Astra (default, high), Claude Opus 5.5, Claude Fable 5.1 (marked *experimental*), GPT-6-Sol. Selecting Fable shows: "Fable's safety filter often blocks runs partway (6 of 11 test prompts); a blocked run fails and must be restarted."
- **Effort**: `low`, `medium`, `high`, `xhigh`, `max`, restricted to what the engine supports; default `high` for Astra and `medium` for other cockpit engines. `ultra` is not offered because it delegates to subagents, which breaks isolation.
- **Instruction**: the default published version, preselected. The list shows published versions, then drafts, each marked.
- **Time limit**: default 90 minutes (runner range 10–360).
- A one-line summary before the button, for example: "GPT-6-Astra · high · v1.13.2 · on Alex's ChatGPT plan."

### 6.2 Job lifecycle

`queued → preparing → running → checking → importing → completed`, or `failed`, `timed_out` or `cancelled`.

- *preparing*: `run_model.py prepare` with the chosen provider, model, effort, instruction file (a snapshot of the pinned text) and filing.
- *running*: `launch`. The runner's continuation logic (at most two resumes) is unchanged.
- *checking*: `check_lean.py` against the workbook and filing, outside the sandbox.
- *importing*: copy the workbook and receipts into the store, create the version and emit an activity event. A failed run creates no version, but its job record, failure reason and receipts are kept.
- New failure reason `usage_limit`, when the provider reports a plan limit, so the page says "Alex's Claude plan hit its usage limit; try again after *time*" instead of a generic error. The provider's error wording is found in spike S4.
- **Cancel** stops a queued or running job, killing its process group.
- The run folder under `_dev/runs/` is deleted after import, as the tools README already requires.

### 6.3 Versions and labels

Each completed run adds an immutable version:

```
id:         <engine>-<effort>-<yyyymmdd-hhmm>-<short hash>
label:      Opus 5.5 · medium · v1.13.2 — Alex, 23 Sep 14:05
kind:       raw
engine, model, effort, instruction {id, name or "draft", sha256},
filing sha256, runner sha256, CLI version, account, started_by,
started_at, finished_at, continuations, tokens, list-price cost (Claude only),
checker errors and warnings
```

- The dropdown groups them: the **Working copy** first, then originals newest first. The deal's current base is marked "base of working copy".
- A version made with a draft instruction reads "… · draft 3f2a9c1 (Alex) …".
- Versions are never deleted. **Hide** removes one from the dropdown for both users and can be undone. Hiding the working copy's base is refused.

### 6.4 Working copy and re-extraction

- The first version of a new deal becomes its working copy's base automatically.
- A later version never touches the working copy. To use it, **Rebase working copy** (with a reason) creates a new revision whose content is the chosen version. The previous working state stays in History and remains restorable.
- **Compare**: the Changes tab gains "compare any two versions", including the working copy, reusing its event-identity diff.

## 7. Adding deals

**Add deal** on the overview page opens a dialog with two tabs.

### 7.1 Search the seed

- Type-ahead over `target_name` and `deal` in `ref/seed.csv` (391 rows), showing form type, filing date and status. Rows already in the cockpit show "Open".
- Rows marked `review` (17 of them) show the reason, and the user picks the correct filing from the EDGAR index (§7.2) instead of an automatic choice.
- Behind the scenes the server reads only the seed's identifying columns (deal, name, form, date, index URL), never any other `ref/` file.

### 7.2 Paste a link

- Accepts an EDGAR filing index (`…-index.htm`), a full submission `.txt`, or a document URL on `www.sec.gov/Archives/`. Anything else is refused.
- A fetch job reads the index and lists its documents with their types. It preselects the main document by the existing rule (DEFM14A and PREM14A: the document whose type equals the form; SC TO-T: exhibit `EX-99.(A)(1)(A)`). The user confirms or changes the choice.
- The deal name comes from the filer or subject company and the slug from `make_seed.py`'s rule; both are editable before saving. A slug that already exists is refused.
- A warning, not a block, if the chosen document has no "Background of the Merger", "Background of the Offer" or similar heading.

### 7.3 Saving

- The filing is saved byte-for-byte, with a manifest row, through the logic of `fetch_filing.py` (refactored to accept an index URL as well as a seed row). SEC's named user agent and request pacing are kept.
- The dialog ends with **Add** or **Add and extract** (opens §6.1 with defaults).
- The deal records who added it and from which source (seed row or pasted link).

## 8. Trace and collaboration: recommended design

Principle: the other person's work should be easy to find when you look, but nothing should demand attention. Everything is pull-based and grouped.

### 8.1 Attribution everywhere, shown quietly

- **History** (exists): every saved revision shows its author, time and reason.
- **Last changed by**: hovering or focusing a field in the editor shows "Alex · 23 Sep 14:05 · revision 12", linking to that revision. It is computed from revision history, so nothing new is stored.
- In event lists, a small initials mark (AL, AG) appears on rows the *other* person changed since your last visit, and only then.

### 8.2 Comments

- Threads can be attached to an event, round, question, deal fact, finding, or the whole deal.
- A comment has an author, a time and text. Replies are one level deep. A thread can be **resolved** or reopened, and the thread records who did it.
- Comments are never overwritten. Editing your own comment keeps the previous text, shown as "edited". Deleting leaves "comment deleted by Alex".
- The existing single notes on row review and finding judgment become each object's first comment, with their original author and time. Review *status* stays a field, and each change to it is recorded as a thread event ("Austin marked reviewed").
- Comments follow event identities through inserts and moves, as references already do. A comment on a deleted event stays visible on the deal thread with "event removed in revision N".
- The row list shows a count only for open threads.

### 8.3 "Since your last visit"

- The overview has one line per deal with activity by the other person since you last opened that deal, for example: "Alex · 12 edits, 3 comments, 1 extraction". Nothing appears when there is nothing new.
- Opening a deal shows a collapsible **What's new** panel at the top of the workspace, grouped by person and session (a burst of activity within 30 minutes counts as one session). It lists revisions with their reasons, new comments and resolutions, runs started or finished, and instruction or base changes. Each item links to its place.
- Leaving a deal records that you have seen everything up to that point. You can also mark items unread again.
- An account-wide activity page lists everything, filterable by person, deal and type, for when you want the full record.

### 8.4 Deliberately left out

Email, browser notifications, live co-editing cursors and per-comment unread counts. They can be added later if the digest proves insufficient.

## 9. Instructions

An **Instructions** page lists every version: name (for example v1.13.2), status (published or draft), author, date, parent, a note, and which one is the default.

- **Published versions** are frozen. Their text can never change.
- **New draft from…** copies any version into an editor (Markdown, with a side-by-side diff against the parent). Saving a draft records the author and time; drafts keep a history of their own edits.
- **Run a draft**: a run freezes the draft's current text under its SHA-256. Later edits to the draft do not affect versions already made.
- **Publish**: freezes the draft under a name and a required change note. Names must be unique and cannot be reused.
- **Make default**: either user, logged in the activity feed and the Instructions page.
- The editor shows a short reminder of AGENTS.md's rule for instruction changes: a change should be general (objective, work process, honesty about uncertainty, a repaired contradiction, a deletion), never a rule justified by one reviewed deal. It is advisory, not enforced.
- v1.13.2 is imported as the first published version and the default, with the SHA-256 of the file currently in the repository.
- The in-app store is authoritative for runs made in the app. `SEC_Deal_Ledger_Extraction_Instruction.md` in the repository stays v1.13.2 until someone deliberately exports a newer version (§11).

## 10. Research integrity (unchanged guarantees, now enforced by the app)

- A run sees exactly one instruction text and one filing, in the existing bubblewrap sandbox, with the same tools and features switched off (web, subagents, connectors). Nothing else from the store, `ref/`, other deals, working copies, comments or earlier versions is mounted.
- The checker runs only after the provider exits, outside the sandbox.
- Every version records the full provenance in §6.3. Two versions are comparable only if their instruction hashes are the same, and the Compare view says when they are not.
- Revision mode (an agent seeing a workbook and findings) is **not** offered in the app. It stays a separate, explicitly requested step.
- The runner's model allow-list grows to Opus 5.5, Fable 5.1, GPT-6-Sol and GPT-6-Astra. Each addition gets the same checks (the served model must match the requested one; refusal fallback is disabled for Claude).

## 11. Documentation changes that follow approval

- **AGENTS.md** and **HANDOFF.md**: extractions may be started in the app by Austin or Alex; instructions may be versioned in the app; either may change the default. The rule that instruction changes must be general stays, as guidance.
- **Cockpit README**: accounts, adding deals, running, versions, comments, what's new, instructions.
- **Tools README**: per-user credentials, the new models and the worker.
- **Export to repository** (optional, admin-only script, not a button): write a chosen instruction version or deal version into `SEC_Deal_Ledger_Extraction_Instruction.md`, `raw_filing/` and `extraction/` for a commit Austin requests.

## 12. Build phases

Models are chosen per task (see HANDOFF). Phase 1 is Claude-only: Opus 5.5 builds it, with Fable 5.1 as an occasional second opinion.

| Phase | Content | Done when |
|---|---|---|
| S. Spikes | S1 `setup-token` in a pseudo-terminal; S2 Codex device login and refresh with a per-user `CODEX_HOME`; S3 Fable 5.1 on a Max plan, with its efforts; S4 usage-limit error wording for both providers. | Each has a short written result. Fallbacks are chosen where a spike fails. |
| 1. Trace | Comments, note migration, last-changed-by, What's new, activity page. No model work. | Two-user tests: Alex's edits and comments appear in Austin's digest and clear after viewing; old notes are preserved as comments. |
| 2. Accounts + runs on existing deals | Settings → Accounts, credential store, worker, job lifecycle, versions and labels, rebase, compare. Opus 5.5 only. | Austin and Alex each complete one run on their own plan (a real run, requiring Austin's go-ahead). Receipts show the right account. Cancel, timeout, restart and usage-limit paths are tested with a fake provider. |
| 3. Add deal | Seed search, link paste, document choice, fetch, **Add and extract**. | One seed deal and one pasted-link deal added and extracted end to end. |
| 4. Instructions + other engines | Instruction editor, drafts, publish, default; Fable, Sol and Astra in the runner and dialog. | A draft run and a published run on the same filing show different instruction hashes. Each engine completes one isolated run (requires Austin's go-ahead). |
| 5. Hardening | Backups, restore rehearsal, documentation (§11). | A restore from backup reproduces the working copies and comments. |

Every phase keeps the existing suites green (browser, resize, responsive, HTTP, vitest and Python unit tests) and adds its own.

## 13. Defaults (approved 23 September)

1. Identities stay Cloudflare Access emails: `junyu.li.24@ucl.ac.uk` → Austin, `a.gorbenko@ucl.ac.uk` → Alex.
2. Run caps: 4 concurrent overall, 2 per user.
3. Backups: nightly, local to the VM, 14 days. Nothing is copied off the VM.
4. A new deal's first completed version becomes its working-copy base automatically.
5. Versions and deals can be hidden, never deleted.
6. The digest's session gap is 30 minutes.
7. Fable 5.1 is offered as *experimental* (Austin, 23 September, after spike S3). A safeguard block is recorded as `provider_refusal` and shown as "blocked by Fable's safety filter".

## 14. Spike results (23 September)

Run on the VM with Claude Code 2.1.280 and Codex 0.156.1, using scratch homes so the host logins were untouched. Model calls: 11 Fable 5.1, 1 Opus 5.5 and 1 GPT-6-Sol one-word prompts on Austin's plans.

- **S1 Claude sign-in: works up to the code.** In a pseudo-terminal, `claude setup-token` prints an authorize link (`claude.com/cai/oauth/authorize`, scope `user:inference`, callback page on `platform.claude.com` that shows the code) and waits at "Paste code here if prompted". The PKCE verifier lives in that process, so the worker must keep the same process alive between showing the link and receiving the code (time out after 10 minutes). Give the terminal a wide size, or the link wraps at 80 columns. Capturing the token after a real approval is untested; it needs Austin or Alex to approve once.
- **S2 ChatGPT sign-in: works up to approval; refresh unconfirmed.** `codex login --device-auth` with a per-user `CODEX_HOME` prints `https://auth.openai.com/codex/device` and a one-time code (valid 15 minutes) on plain output, so no pseudo-terminal is needed. Access tokens last 10 days (the host token: issued 14 September, expires 24 September 11:38 UTC). A call nine days in did not refresh the token, so Codex refreshes lazily, near or after expiry. Plan: when a user's token is expired or has under 7 hours left, the worker runs a one-word `codex exec` outside the sandbox with that user's writable `CODEX_HOME` and confirms `last_refresh` advanced. Confirm this when the host token expires on 24 September. Until the host login refreshes, the runner's 7-hour rule refuses host Sol runs from about 04:38 UTC on 24 September.
- **S3 Fable 5.1: served on the Max plan, but its safeguards block unpredictably.** All five efforts (`low`–`max`) were accepted and served by `claude-fable-5-1`. Yet 6 of 11 one-word prompts failed with "Fable 5.1's safeguards flagged this message … Claude Code can't respond to this message with Fable 5.1", across efforts. With refusal fallback disabled (required for isolation), a long extraction would very likely fail as `provider_refusal`. Each one-word call cost about $0.09 at list price because of Claude Code's own prompt.
- **S4 Usage limits.** Claude: the stream reports a `rate_limit_event` with `status` (`allowed`, `allowed_warning`, `rejected`), the limit type (`five_hour`, `seven_day`, …), `resetsAt`, and each window's utilization (at the test: 10% of five-hour, 29% of weekly). The app can therefore show each user's plan usage before a run and classify `usage_limit` failures exactly. The CLI can also "wrap up the current step" when approaching the five-hour limit, which the runner's continuation logic treats as an unfinished run. Codex: `codex exec --json` reports token counts but no plan usage; the binary's limit message is "You've hit your usage limit … Try again at …", so `usage_limit` is detected by message until a real event is captured.
