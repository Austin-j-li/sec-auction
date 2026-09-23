# Reviewing in the cockpit

Open [Ledger cockpit](https://lines.dealextract.org) using the existing Austin or Alex login. Choose a deal, then use its **Working copy** to make edits. The filing stays beside the selected record. On a narrow screen, switch between **Filing** and **Workspace**.

Drag the thin divider between the filing and workspace, or between a sheet's list and editor, to change their widths. When the right panel is narrow, the list moves above the editor; drag their horizontal divider to change the list height. Double-click a divider to reset it; when focused, use arrow keys for small steps or Home/End for the limits. Use the arrow buttons beside the workspace tabs to reach tabs that do not fit. Drag the lower-right corner of a multiline text box to change its width and height; if widened beyond the editor, use its horizontal scrollbar to reach the rest. Pane sizes are remembered in this browser and do not change the workbook or create an unsaved edit.

## Versions and review status

Each of the nine deals has one version: its Claude Opus 5.5 medium extraction under instruction v1.13.2 (22 September), which is also the working base. None has been reviewed. Earlier Opus 5 drafts, v1.13 baselines and the lead-verified Datalink and Mac-Gray correction passes are no longer selectable; their evidence remains in the review packets.

Review holds only case-level decisions that do not depend on an earlier workbook's rows. Datalink shows Austin's 21 September ruling to keep January's bilateral stage as round 1 (five rounds; January 29 inferred), to be checked against the displayed extraction. Mac-Gray shows Austin's 22 September R01 decision, with its research-decision document: bidder-commitment changes at an unchanged price are same-price Bids, and the target termination fee stays in a dated Note. The displayed extraction has not yet been revised to it. Audit findings and corrections keyed to earlier drafts' rows were removed from the cockpit. The Astra experiment is a historical side note and is not a selectable cockpit version.

## A review session

1. Select an event and use **Show in filing**, the filing search, or a printed page number to inspect its evidence. Selecting text in the filing can fill the selected event's quotation field. A located quotation is a navigation aid, not proof that the event is correctly coded or that no events are missing.
2. Edit the Ledger, Rounds, Questions or Deal facts. Changes remain staged until **Save changes**. Use a short reason to explain the revision. Add an event for an omission; **Clone to split** starts from an existing event and clears Count so a cohort is not silently counted twice.
3. Use **Review** for the mechanical report, recorded candidate findings, prior decisions and supporting documents. Finding judgment, correction implementation and verification are separate choices. Changing a finding's judgment does not change any workbook cell. Record an event's review status in its own editor; discuss it in the comments below the fields.
4. Save, inspect **Changes**, then export Excel when needed. **History** preserves saved revisions and their attribution. Restoring any earlier revision, including the starting base, creates a new revision rather than erasing history.

When events are inserted, moved or deleted, explicit event references follow their identities. Until saving, refer to the numbers still displayed; new events receive numbers on save. Deleting a referenced event requires a replacement event or explicit cleanup of its references. Narrative references may require manual review. Renumbering cannot determine whether a round summary or bidder count is substantively correct.

If another editor has saved first, the cockpit keeps your staged edits and blocks overwriting that revision. Download those edits before choosing to discard them and load the current copy. Compare and reapply the intended changes to the current copy.

The mechanical checker runs again on saved working copies. Its errors and warnings remain visible; it does not certify source completeness or research acceptance.

## Connecting your Claude and ChatGPT accounts and running extractions

Each person runs extractions on their own Claude plan. Open **Settings** (your name in the header), choose **Connect Claude account**, open the link, approve with your claude.ai login and paste the code it shows. The connection lasts a year; Settings shows when it expires and how much of your plan's 5-hour and weekly limits the last run reported. If the link flow fails, run `claude setup-token` on any computer and paste the token under "Paste a token instead". **Disconnect** deletes the stored token; you can also revoke it on claude.ai.

GPT engines run on your ChatGPT plan. In **Settings**, **Connect ChatGPT account** shows a link and a one-time code: open the link, sign in to ChatGPT and enter the code; the page notices the approval by itself. The ChatGPT login lasts about ten days and the cockpit renews it in the background (a one-word GPT-6-Sol call on your plan) when it has less than a day left; a run that would start within seven hours of expiry waits for that renewal, and fails as "login expired" if it cannot be renewed, in which case connect again. **Disconnect** deletes the stored login; revoke it at chatgpt.com → Settings → Security.

In a deal, **Extract** starts an isolated run. Choose the engine (Claude Opus 5.5 by default; Claude Fable 5.1, marked experimental because its safety filter often blocks a run partway; GPT-6-Sol; GPT-6-Astra), the effort (default medium) and the instruction (the default published version, or any other version or draft). An engine whose account you have not connected is greyed out. The run sees only the instruction and the filing, exactly as in the command-line runner, and the instruction text is frozen when you press Start: editing a draft later does not change a run already requested. The **Runs** tab shows queued, running and finished runs, who started them, time, cost at list price and checker counts; **Cancel** stops a run. At most four runs go at once, two per person; others wait in the queue. A run that hits your plan's usage limit says so and when the limit resets.

A finished run becomes a new read-only version, labelled with engine, effort, instruction, who ran it and when. It never changes the working copy. To work from it, open that version and choose **Use as working-copy base…** with a reason; the previous working state stays in History and can be restored. The Changes tab compares any two versions, or a version and the working copy, matching events by number. **Hide** removes a version you no longer need from the list (it is never deleted; "Show hidden versions" brings it back).

## Instructions

**Instructions** in the header lists every instruction version: published versions (frozen; their text never changes) and drafts, with author, date, parent and which one is the default. v1.13.2, the repository's working instruction, was imported as the first published version and the default. **New draft from this** copies any version into an editor; the editor can show a side-by-side diff against its parent, and each **Save draft** is kept in the draft's history. If the other person saved the same draft since you opened it, your save is refused and you reload. **Publish…** freezes a draft under a new name with a required change note; **Make default** changes which version Extract preselects, for both of you. Drafts can be run; their versions read "draft 3f2a9c1 (Alex)". Compare says when two versions were made with different instructions. The repository file `SEC_Deal_Ledger_Extraction_Instruction.md` is not changed by any of this. As AGENTS.md advises, an instruction change should be general (objective, work process, honesty about uncertainty, a repaired contradiction, a deletion), never a rule justified by one reviewed deal.

## Adding a deal

**Add deal** on the overview adds a filing without a terminal. **Search the seed** finds a deal in `ref/seed.csv` by name; **Paste a link** takes an EDGAR filing index (`…-index.htm`), a complete submission (`.txt`) or a document under `www.sec.gov/Archives/edgar/data/`. The cockpit fetches the filing from EDGAR (a few seconds) and lists its documents with the main one preselected: the proxy for DEFM14A and PREM14A, the offer to purchase (`EX-99.(A)(1)(A)`) for SC TO-T. Seed rows marked for review preselect nothing, and one without a usable link asks you to paste it. A document without a "Background of the Merger" or similar heading is flagged but can still be added. Check the deal name and short name (the short name is permanent), then **Add**, or **Add and extract** to open the Extract dialog at once.

The chosen document is saved byte for byte, exactly as the command-line fetcher saves it, with its source link and SHA-256. Until its first run finishes, the deal shows only its filing and "No extraction yet"; the first finished run becomes its working copy's base, and later runs are added as versions like any other. The activity feed records who added which deal and from where.

## Seeing each other's work

Everything you save or comment is signed with your login, so Austin and Alex can each see what the other did. None of it pushes notifications; look when you want to.

- **Comments.** Every event, round, question and deal fact has a comment thread below its fields; the Review tab has a Discussion for the whole deal and a thread under each finding. Reply, resolve or reopen; replying to a resolved thread reopens it. You can edit or delete only your own comments; edits keep the earlier text, and a deleted comment leaves a marker. Comments post immediately and are not part of **Save changes**. A thread on an event that is later deleted stays visible, marked as such.
- **Since your last visit.** The overview shows one line under a deal when the other person has edited or commented since you last opened it. Inside the deal, **What's new** groups their activity by person and sitting, with links to the revision or thread. Leaving the deal marks it as read; **Mark unread** undoes that.
- **Who changed a field.** Hover or focus a field label to see who last changed it, when, and in which revision. Events the other person changed since your last visit carry their initials in the list, and events with open threads show a count.
- **Activity.** The Activity page lists every save and comment across deals, filterable by person, deal and type.

## Storage and operation

Version and report paths are allowlisted in [catalog.json](catalog.json). Original workbooks are immutable inputs. Working revisions, decisions, comments, activity and read markers are stored in the ignored `_dev/cockpit/state/workspace.sqlite3`; this database must be preserved across deployments. GET requests do not create working revisions or the database.

The existing `ledger-cockpit.service` serves the built frontend and API on loopback port 8778 behind the existing Cloudflare Access route. The public origin is `https://lines.dealextract.org`. Public edit attribution uses the configured access identities; loopback development is explicitly attributed to `local`. The application performs no model calls when viewing or saving a deal.

Build and verification scope: [COCKPIT_BUILD.md](../COCKPIT_BUILD.md). The original cockpit acceptance and deployment records predate the resize controls described above; their separate synthetic browser check is `_dev/tools/cockpit/acceptance/test_resize.mjs`. The "working papers" visual redesign was deployed on 23 September; its brief and test log are in [`maintenance/2026-09-22-cockpit-redesign/`](../maintenance/2026-09-22-cockpit-redesign/PROGRESS.md), and all acceptance suites passed against it. Extraction provenance: [re-extraction packet](../reviews/2026-09-22-opus55-reextraction/README.md). The role assignment for this development phase is **Astra for design, review and reasoning; GPT Sol for code implementation**.
