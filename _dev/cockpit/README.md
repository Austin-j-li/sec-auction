# Reviewing in the cockpit

Open [Ledger cockpit](https://lines.dealextract.org) using the existing Austin or Alex login. Choose a deal, then use its **Working copy** to make edits. The filing stays beside the selected record. On a narrow screen, switch between **Filing** and **Workspace**.

Drag the thin divider between the filing and workspace, or between a sheet's list and editor, to change their widths. When the right panel is narrow, the list moves above the editor; drag their horizontal divider to change the list height. Double-click a divider to reset it; when focused, use arrow keys for small steps or Home/End for the limits. Use the arrow buttons beside the workspace tabs to reach tabs that do not fit. Drag the lower-right corner of a multiline text box to change its width and height; if widened beyond the editor, use its horizontal scrollbar to reach the rest. Pane sizes are remembered in this browser and do not change the workbook or create an unsaved edit.

## Versions and review status

Each of the nine deals has one version: its Claude Opus 5.5 medium extraction under instruction v1.13.2 (22 September), which is also the working base. None has been reviewed. Earlier Opus 5 drafts, v1.13 baselines and the lead-verified Datalink and Mac-Gray correction passes are no longer selectable; their evidence remains in the review packets.

Review holds only case-level decisions that do not depend on an earlier workbook's rows. Datalink shows Austin's 21 September ruling to keep January's bilateral stage as round 1 (five rounds; January 29 inferred), to be checked against the displayed extraction. Mac-Gray shows Austin's 22 September R01 decision, with its research-decision document: bidder-commitment changes at an unchanged price are same-price Bids, and the target termination fee stays in a dated Note. The displayed extraction has not yet been revised to it. Audit findings and corrections keyed to earlier drafts' rows were removed from the cockpit. The Astra experiment is a historical side note and is not a selectable cockpit version.

## A review session

1. Select an event and use **Show in filing**, the filing search, or a printed page number to inspect its evidence. Selecting text in the filing can fill the selected event's quotation field. A located quotation is a navigation aid, not proof that the event is correctly coded or that no events are missing.
2. Edit the Ledger, Rounds, Questions or Deal facts. Changes remain staged until **Save changes**. Use a short reason to explain the revision. Add an event for an omission; **Clone to split** starts from an existing event and clears Count so a cohort is not silently counted twice.
3. Use **Review** for the mechanical report, recorded candidate findings, prior decisions and supporting documents. Finding judgment, correction implementation and verification are separate choices. Changing a finding's judgment does not change any workbook cell. Record an event's review status and note in its own editor.
4. Save, inspect **Changes**, then export Excel when needed. **History** preserves saved revisions and their attribution. Restoring any earlier revision, including the starting base, creates a new revision rather than erasing history.

When events are inserted, moved or deleted, explicit event references follow their identities. Until saving, refer to the numbers still displayed; new events receive numbers on save. Deleting a referenced event requires a replacement event or explicit cleanup of its references. Narrative references may require manual review. Renumbering cannot determine whether a round summary or bidder count is substantively correct.

If another editor has saved first, the cockpit keeps your staged edits and blocks overwriting that revision. Download those edits before choosing to discard them and load the current copy. Compare and reapply the intended changes to the current copy.

The mechanical checker runs again on saved working copies. Its errors and warnings remain visible; it does not certify source completeness or research acceptance.

## Storage and operation

Version and report paths are allowlisted in [catalog.json](catalog.json). Original workbooks are immutable inputs. Working revisions and decisions are stored in the ignored `_dev/cockpit/state/workspace.sqlite3`; this database must be preserved across deployments. GET requests do not create working revisions.

The existing `ledger-cockpit.service` serves the built frontend and API on loopback port 8778 behind the existing Cloudflare Access route. The public origin is `https://lines.dealextract.org`. Public edit attribution uses the configured access identities; loopback development is explicitly attributed to `local`. The application performs no model calls when viewing or saving a deal.

Build and verification scope: [COCKPIT_BUILD.md](../COCKPIT_BUILD.md). The original cockpit acceptance and deployment records predate the resize controls described above; their separate synthetic browser check is `_dev/tools/cockpit/acceptance/test_resize.mjs`. The "working papers" visual redesign was deployed on 23 September; its brief and test log are in [`maintenance/2026-09-22-cockpit-redesign/`](../maintenance/2026-09-22-cockpit-redesign/PROGRESS.md), and all acceptance suites passed against it. Extraction provenance: [re-extraction packet](../reviews/2026-09-22-opus55-reextraction/README.md). The role assignment for this development phase is **Astra for design, review and reasoning; GPT Sol for code implementation**.
