# Editable cockpit build contract and delivery record

This is a build contract and dated delivery record, not the current research queue or proof of laptop/VM equivalence. Start with [current status and decisions](RESEARCH_QUESTIONS.md); later VM changes are only partly recovered locally.

## Authorized objective and model roles

The original authorized build completed the nine-deal v1.13.2 set and delivered an editable cockpit. It reused Datalink and Mac-Gray's isolated v1.13.2 extractions and ran the seven remaining deals once using Opus 5 high. Originals were preserved, checked outside the provider sandbox and exposed alongside working copies and recorded findings. Austin's source review and adjudication remain separate work; the original delivery did not establish research acceptance.

The original build used Sol for code and Astra for design and review. Current model selection follows [AGENTS.md](../AGENTS.md). The original build did not authorize a commit, push or instruction edit. On 22 September Austin separately authorized consolidation and a local commit; see the [consolidation record](maintenance/2026-09-22-consolidation/README.md). New substantive audits and corrections to the fresh drafts still require a separate command.

**Original delivery, 22 September 2026:** all nine v1.13.2 raw versions were preserved and the editable cockpit was deployed. Datalink's verified correction pass and Mac-Gray's latest correction candidate (R01 pending) became the initial working bases for those deals. The [original verification evidence](reviews/2026-09-21-v1132-cockpit/cockpit-verification/VERIFICATION.md) describes that delivery and its limits. Since 22 September the catalog holds only the nine Opus 5.5 medium extractions, one version per deal, beside run versions started in the cockpit. All thirteen working copies still have v1.13.2 bases in the 27 September 10:55 UTC snapshot. The [review guide](cockpit/README.md), [current status and decisions](RESEARCH_QUESTIONS.md) and [re-extraction packet](reviews/2026-09-22-opus55-reextraction/README.md) describe the current state.

The 23 September build also added filing/workspace and sheet list/editor dividers, with mouse and keyboard resizing, browser-local size memory, and resizable multiline fields. The frontend source is in `tools/cockpit/frontend/src/`; the isolated synthetic browser check is `tools/cockpit/acceptance/test_resize.mjs`. These later changes are outside the original delivery and consolidation test receipts. The frontend was then visually redesigned and deployed on 23 September (see "Design" below); against that build, all suites passed: 46/46 synthetic browser assertions (rerun against the deployed `dist/`), resize, responsive, 11 HTTP, 3 vitest and 128 Python unit tests. The authenticated public route was checked only up to its Cloudflare Access redirect.

## Design

Reading this as an editable research workspace for Austin and Alex, with calm document-focused styling. Preserve `/`, `/deal/<slug>`, ledger `#row-n` and Question navigation, and the existing Ledger cockpit name. Dials: design variance 4, motion 3, visual density 8. Preserve blue control accents and yellow quotation highlights on a single light theme. Cabinet Grotesk is the seeded type choice; self-host the font. Use official Fluent UI React controls and one Phosphor icon family. GSAP is for restrained view/save feedback only, with reduced-motion handling and cleanup.

The requested design-taste-frontend skill explicitly excludes dense dashboards from its marketing patterns. Product editing and complete source text take precedence over the skills' hero, cinematic spacing, photo, carousel and scroll-hijacking recipes. Do not truncate or change research text to satisfy marketing copy rules. Retain full excerpts, including punctuation from sources.

Layout: restrained navigation, a compact nine-deal overview, a version-aware deal toolbar, filing and editable record panes. Ledger supports a compact event list and a full editor for the selected event. Tabs retain Rounds, Questions and Deal facts and add Review, Changes and History. Evidence navigation works both from rows and findings. On narrow screens switch Filing/Workspace without losing selections; do not stack two huge scrolling regions. Inputs have visible labels, error/saved/unsaved states, keyboard access and strong contrast.

Redesign of 22–23 September 2026 ("working papers"; brief, audit and progress in `_dev/maintenance/2026-09-22-cockpit-redesign/`). Hierarchy comes from hairline rules, alignment and weight. There are no cards, chips, tinted callout boxes or eyebrow labels. Colours use one stone-neutral family, with every token in a single `:root` block in `style.css` and mirrored into the Fluent theme in `src/theme.js`. The only accent is the control blue `#1f4f99`, used only where the user acts: links, the primary button, focus rings and selection. Quotes use three yellows: located, selected and search hit. The fonts are self-hosted: Cabinet Grotesk for the interface, IBM Plex Mono for figures, dates and ids, and Source Serif 4 for filing text. The favicon lives in `src/favicon.svg` and ships as a hashed `/assets/` file, because `server.py` serves only `/assets/` and the index; do not add a `public/` folder. Known inconsistency: on the Rounds, Questions and Facts sheets the section head spans both columns, while on the Ledger it sits in the list column. `test_resize` pins `.other-sheet > .section-head h2`.

## Original build ownership

- Sol backend: `_dev/tools/cockpit/workspace.py`, `server.py`, necessary `data.py` integration, and backend tests.
- Sol frontend: `_dev/tools/cockpit/frontend/` including package/lock, source, self-hosted fonts in `src/fonts/`, Vite build, plus root `.gitignore` additions for its node_modules. Build output belongs in `_dev/tools/cockpit/dist/`.
- Sol import: version catalog, recorded findings/documents, extraction receipt administration and import tooling. Does not change existing raw workbooks, instruction, production runner or another task's revision.
- Astra: architecture, design decisions, review, acceptance checks, deployment and handoff documentation. Any required code fixes go back to Sol.

## Shared API contract

All existing GET routes remain. Backend serves Vite `dist/index.html` for the existing page routes and `/assets/*` safely from dist. If `dist/index.html` is absent, page routes return an explicit HTTP 503 error; the legacy read-only page was retired on 23 September. Source parsing/highlighting stays in the existing data layer. No remote calls in server request handling.

`GET /api/session` returns `{user, can_edit, csrf_token}`. Send `X-Cockpit-CSRF` on JSON write requests. Public writes require the existing trusted Cloudflare identity for Austin/Alex. Unknown public users must not default to Austin. Direct loopback development may use an explicitly labeled local actor. Verify Origin and content type, bound request sizes, and reject unsafe paths.

`GET /api/deals` remains an array, extending existing entries with `name`, `instruction_version`, `review_status`, `working_revision` and `base_label` as available. Counts and checks describe the displayed working version.

`GET /api/deal/<slug>?version=working` extends the existing payload:

- `versions`: array of `{id,label,instruction_version,kind,sha256,review_status}`. Include `working` and every immutable catalog version. The original build listed `v1132-raw`, any `v113-baseline` and separately recorded revisions; since 22 September the catalog holds one `opus55-medium` version per deal. Never silently overwrite a raw output.
- `workspace`: `{revision,base_version,base_sha256,updated_at,updated_by,editable,selected_version}`. Revision is an integer, initially zero. For an immutable version, `editable=false`.
- Each ledger, rounds and questions row gains `uid` (stable across inserts/moves/saves) and retains `cells`, `excel_row`, `id`, `issues` and source quote data. `cells` are display strings; the backend stores typed values separately.
- Facts gain `uid` while retaining `field` and `value`.
- `findings`: array of `{id,title,detail,rule,source_version,source_label,source_rows,evidence,proposed_change,needs_recheck,judgment,implementation,verification,note,actor,at}`. Evidence is an array of `{quote,page}`. A case-level decision that does not depend on any workbook's rows has a null `source_version`. Original source row numbers are not links to a different extraction. Existing lead judgments remain attributed; fresh drafts inherit no human acceptance.
- `documents`: array of `{id,label,source_version,kind}`. `GET /api/document/<slug>/<id>` returns `{title,text}` for an allowlisted recorded report.
- `row_review`: mapping stable uid to `{status,note,actor,at}`. Status is `unreviewed`, `reviewed`, or `needs_decision`.
- `choices`: mapping field names to allowed labels from `check_lean.choice_lists` for the displayed version's `ledger_schema`. A working copy uses its base's schema; a deal can hold versions of both schemas. A 29-column version uses v1.14.1 rules by default, or v1.14 when its instruction SHA-256 selects them. An unreadable header gives no choices. Preserve existing unusual values visibly; do not silently normalize old data.

`POST /api/deal/<slug>/edit` accepts `{revision,base_sha256,reason,operations}`. Writes are transactional; any failure leaves all changes unapplied. Reject stale revisions/base hashes with HTTP 409. Return the updated working deal payload.

Operations:

- `{type:'update',sheet,uid,values}` patches columns in one record. Facts use Field/Value. Preserve Excel numeric/date types; validate field names and primitive values. Never permit an injected formula in a text edit.
- `{type:'insert',sheet,after_uid,values,client_uid?}` inserts a row; null after_uid means start. Assign stable uid. An optional bounded `new-*` client UID lets later operations in the same save refer to this new row. Blank dates and uncertain counts remain blank. The frontend can clone a row into the insert form for splitting, but must not silently double-count a cohort.
- `{type:'delete',sheet,uid,replacement_uid?}` removes a row. For referenced ledger rows, require a chosen replacement or explicit reference cleanup. Deleting one row must not retarget its references to the next event.
- `{type:'move',sheet,uid,after_uid}` reorders a row without changing identity.
- `{type:'finding',id,judgment,implementation,verification,note}` records a user decision. Judgment: unreviewed/supported/rejected/deferred; implementation: unassessed/not_applied/applied; verification: unchecked/verified. Imported candidates start unassessed. Explicit earlier rulings and verified corrections are separately attributed in `recorded_decision` and `recorded_correction`; they do not become automatic human acceptance of the displayed version. Decision alone does not change workbook data or automatically mark a correction verified.
- `{type:'review',uid,status,note}` records review status.
- `{type:'bulk_update',sheet:'Deal ledger',uids,values}` sets Process and/or Round on distinct live rows or `new-*` client UIDs introduced in the same save. It counts as one of a save's 100 operations; Process must be a whole number of at least 1, and Round a whole number of at least 0 or `post`. Each row is recorded, diffed and attributed; row review marks remain. The editor stages this from **Select → Set Process/Round…** behind confirmation.
- `{type:'restore',target_revision}` restores a saved snapshot as a new revision with visible history. Do not erase historical changes.
- `{type:'rebase',target_version}` makes a version the working base as one new revision. Row marks and row threads remain attached to old rows; finding judgments carry over with a `carried_over` record, while implementation and verification reset. `GET /api/deal/<slug>/rebase?to=<id>` previews both schemas and counts that stop applying.

Ledger sequence numbers and explicit references (`#n`, Questions' parseable Rows affected ranges) follow stable event identity when inserting/moving/deleting. Staged text uses the displayed pre-save numbers; renumber and remap once after the entire batch. New rows are labeled New until saved. Preserve exact membership of referenced ranges. Treat narrative/global references conservatively and flag affected summaries. Question IDs must remain unique; maintain references when changed or block an unsafe edit. Review status/checker success must never certify source completeness.

`GET /api/deal/<slug>/history` returns `{history:[{revision,at,actor,reason,summary,changes}]}` newest first, including the restorable base at revision zero. `changes` contain `{sheet,uid,field,before,after,type}` with full text.

`GET /api/deal/<slug>/changes` returns `{base_label,changes}` comparing the working version with its actual base, matching records by stable uid.

`GET /api/deal/<slug>/export?version=working` returns `<slug>-working-r<N>.xlsx`: the four workbook sheets plus a cockpit-written **Source** sheet with EDGAR filing-index and complete-submission links, Background pages, filing/instruction/raw-workbook hashes, base version, revision, deal review status and export time. `&source=0` returns the four sheets alone for checker use. `?version=rev:N` downloads a past revision similarly, read only, without changing state. Raw version exports preserve the original bytes; `&source=1` adds Source as `<slug>-<version>-with-source.xlsx`. Any other `source` value returns HTTP 400. `Workspace.export`, used by `export_repo.py` and `verify_catalog.py`, remains four-sheet. Preserve typed dates/numbers, formats, row references and filters. No model writes the Source sheet.

## Storage/catalog contract

Catalog path: `_dev/cockpit/catalog.json`. Format: `{schema_version:1,deals:{slug:{name,default_base,versions:[{id,label,path,sha256,instruction_version,kind,review_status}],findings:[],documents:[]}}}`. Document entries also contain an allowlisted relative `path`. Paths resolve inside the repository, never `ref/`. In the original build `v1132-raw` existed for every deal, and Datalink's verified correction pass was its default base on the strength of its separate review record. Since 22 September each catalog deal has one `opus55-medium` version; cockpit-started runs add separate versions without changing its base. Earlier workbooks remain only as packet evidence.

Working state: SQLite under `_dev/cockpit/state/` (ignored), with an original base hash, stable record identifiers, transactional revision snapshots and audit metadata. State survives process restart and browser/device changes. Keep GETs read-only where possible, and initialize or write only when necessary. Never write back to catalog source workbooks.

## Original acceptance requirements

The numbered checks below governed the original build. The [verification evidence](reviews/2026-09-21-v1132-cockpit/cockpit-verification/VERIFICATION.md) records what was exercised; the [consolidation record](maintenance/2026-09-22-consolidation/README.md) covers later maintenance. Neither record is a test receipt for subsequent interface changes.

1. Seven successful isolated Opus outputs plus the two reused v1.13.2 originals, with recorded instruction/source/output hashes and separate mechanical reports. No substantive revision of these seven.
2. All nine appear in the deployed cockpit with correct versions, counts, evidence links and honest review states.
3. Editing all four sheets, adding/deleting/moving events, preserving references, restoring/undoing changes, recording decisions and exporting are tested end to end on disposable fixtures. Production research state remains untouched by test edits.
4. Tests exercise numeric/date preservation, missing/uncertain fields, deleted references, atomic batches, stale saves, attribution, forbidden writes/path traversal and restart persistence.
5. Browser checks cover desktop and narrow widths, all tabs, source search/links, full field editing, save errors, unsaved navigation, history and Excel download. No placeholder controls or unexplained dead buttons.
6. Original files and frozen instruction retain their initial hashes; all required checks pass. Deploy through the existing localhost service and Cloudflare route, preserve existing access boundaries, record final version and restart behavior.
7. Keep a concise handoff with the cockpit URL and how Austin resumes tomorrow. Stop at the built cockpit; do not adjudicate on his behalf or launch new audit/revision passes.
