# Reviewing in the cockpit

Open [Ledger cockpit](https://lines.dealextract.org) using the existing Austin or Alex login. Choose a deal, then use its **Working copy** to make edits. The filing stays beside the selected record. On a narrow screen, switch between **Filing** and **Workspace**.

## Versions and review status

Each of the nine deals has a preserved v1.13.2 raw extraction. The original eight also retain their v1.13 baselines. Datalink starts from its verified 68-event correction pass. Mac-Gray starts from the latest 58-event correction candidate, explicitly labeled **R01 pending**; the earlier 55-event correction pass and raw drafts remain selectable. Verification here means the documented development-lead checks of supported corrections. It is not a human approval of the complete deal.

Mac-Gray's R01 asks whether material termination-fee and guarantee changes should be separate same-price Bids or dated Notes. Its decision, acceptance, coverage and analytical-use documents are in Review. That choice remains Austin's; the candidate is not frozen or research-ready.

The seven fresh drafts await source review; retired Sol/Grok comparison findings and report links have been removed. Datalink and Mac-Gray retain their attributed review records. Source row numbers in earlier findings belong to their labeled version. Datalink's January-round convention is recorded separately as Austin's decision. The Astra experiment is a historical side note and is not a selectable cockpit version.

## A review session

1. Select an event and use **Show in filing**, the filing search, or a printed page number to inspect its evidence. Selecting text in the filing can fill the selected event's quotation field. A located quotation is a navigation aid, not proof that the event is correctly coded or that no events are missing.
2. Edit the Ledger, Rounds, Questions or Deal facts. Changes remain staged until **Save changes**. Use a short reason to explain the revision. Add an event for an omission; **Clone to split** starts from an existing event and clears Count so a cohort is not silently counted twice.
3. Use **Review** for the mechanical report, recorded candidate findings, prior decisions and supporting documents. Finding judgment, correction implementation and verification are separate choices. Changing a finding's judgment does not change any workbook cell. Record an event's review status and note in its own editor.
4. Save, inspect **Changes**, then export Excel when needed. **History** preserves saved revisions and their attribution. Restoring any earlier revision, including the starting base, creates a new revision rather than erasing history.

When events are inserted, moved or deleted, explicit event references follow their identities. Until saving, refer to the numbers still displayed; new events receive numbers on save. Deleting a referenced event requires a replacement event or explicit cleanup of its references. Narrative references may require manual review. Renumbering cannot determine whether a round summary or bidder count is substantively correct.

If another editor has saved first, the cockpit keeps your staged edits and blocks overwriting that revision. Download those edits before choosing to discard them and load the current copy. Compare and reapply the intended changes to the current copy.

The mechanical checker runs again on saved working copies. Its errors and warnings remain visible; it does not certify source completeness or research acceptance. Datalink's imported correction pass retains the documented page-break quotation exception in its checker result.

## Storage and operation

Version and report paths are allowlisted in [catalog.json](catalog.json). Original workbooks are immutable inputs. Working revisions and decisions are stored in the ignored `_dev/cockpit/state/workspace.sqlite3`; this database must be preserved across deployments. GET requests do not create working revisions.

The existing `ledger-cockpit.service` serves the built frontend and API on loopback port 8778 behind the existing Cloudflare Access route. The public origin is `https://lines.dealextract.org`. Public edit attribution uses the configured access identities; loopback development is explicitly attributed to `local`. The application performs no model calls when viewing or saving a deal.

Build and verification scope: [COCKPIT_BUILD.md](../COCKPIT_BUILD.md). Extraction provenance: [nine-deal import report](../reviews/2026-09-21-v1132-cockpit/REPORT.md). The role assignment for this development phase is **Astra for design, review and reasoning; GPT Sol for code implementation**.
