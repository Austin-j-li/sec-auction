# Phase 1 (trace) build contract

Implements §8 of [the app spec](../../COCKPIT_APP_SPEC.md): comments, "since your last visit", last-changed-by, and an activity page. No model calls, no new dependencies. Read `_dev/COCKPIT_APP_SPEC.md` §8, `_dev/COCKPIT_BUILD.md` ("Design" and "Shared API contract") and `_dev/cockpit/README.md` first.

Claude-only build (Austin, 23 September): Opus 5.5 leads, writes the backend (`_dev/tools/cockpit/workspace.py`, `server.py`, tests), integrates, builds and deploys; an Opus 5.5 subagent writes the frontend (`_dev/tools/cockpit/frontend/src/`); Fable 5.1 is consulted only occasionally for a second opinion. Do not edit files owned by the other side. Do not read `ref/`, `extraction/` contents beyond what the cockpit already serves, or anything under `_dev/reviews/` or `_dev/side-notes/`.

## Identity

`server._identity()` already returns `(actor, can_edit)`: `austin`, `alex`, or `local` on loopback (writes allowed), else `unknown` (read-only). Every new write uses the same CSRF, Origin, content-type and body-size checks as `/edit`. `unknown` gets no `seen` state and cannot write.

## Storage (same SQLite file, `_dev/cockpit/state/workspace.sqlite3`)

Create tables idempotently in `_connect(write=True)`. Reads must tolerate a missing database or missing tables (return empty results), as `_latest` already does.

```sql
CREATE TABLE IF NOT EXISTS threads (
  id TEXT PRIMARY KEY, slug TEXT NOT NULL,
  target_kind TEXT NOT NULL CHECK (target_kind IN ('deal','row','finding')),
  target_sheet TEXT,            -- for 'row': 'Deal ledger' | 'Rounds' | 'Questions' | 'Deal facts'
  target_uid TEXT,              -- row uid, or finding id; NULL for 'deal'
  target_label TEXT NOT NULL,   -- label at creation, e.g. "Event #12 · 2016-06-06 · Party A · …"
  created_by TEXT NOT NULL, created_at TEXT NOT NULL,
  resolved_by TEXT, resolved_at TEXT);
CREATE TABLE IF NOT EXISTS comments (
  id TEXT PRIMARY KEY, thread_id TEXT NOT NULL REFERENCES threads(id),
  parent_id TEXT,               -- NULL for the thread's first comment and for replies (replies are one level)
  actor TEXT NOT NULL, at TEXT NOT NULL, body TEXT NOT NULL,
  edited_at TEXT, deleted_by TEXT, deleted_at TEXT);
CREATE TABLE IF NOT EXISTS comment_edits (
  comment_id TEXT NOT NULL, at TEXT NOT NULL, previous_body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS activity (
  id INTEGER PRIMARY KEY AUTOINCREMENT, slug TEXT NOT NULL, at TEXT NOT NULL, actor TEXT NOT NULL,
  kind TEXT NOT NULL,           -- revision | restore | comment | reply | resolve | reopen | comment_edit | comment_delete
  revision INTEGER,             -- for revision/restore: the saved revision number
  thread_id TEXT, comment_id TEXT,
  summary TEXT NOT NULL);       -- one line, e.g. the save reason, or the first 140 chars of a comment
CREATE TABLE IF NOT EXISTS seen (
  user TEXT NOT NULL, slug TEXT NOT NULL, activity_id INTEGER NOT NULL, at TEXT NOT NULL,
  PRIMARY KEY (user, slug));
```

- `edit()` inserts one `activity` row (`revision` or `restore`, `summary` = the save reason) in the same transaction as the revision.
- Comment writes insert their `activity` row in the same transaction.
- Replies are one level: `parent_id` of a reply is always the thread's first comment id. The first comment has `parent_id` NULL.
- Comment body: non-empty after trimming, at most 20 000 characters.
- Only the author may edit or delete a comment. Editing appends the old body to `comment_edits` and sets `edited_at`. Deleting sets `deleted_by`/`deleted_at` and keeps the row; the API returns `body: ""` and `deleted: {by, at}` for it.
- Either user may resolve or reopen a thread. Replying to a resolved thread reopens it (record both activity rows).
- A `row` target must exist in the current working state when the thread is created; a `finding` target must be a catalog finding id for the deal.

### Migration of existing notes (idempotent, on first write connection)

Existing working states may hold notes in `row_review[uid].note` and `findings[id].note` (the production database does not exist yet, so this is for completeness). For each non-empty note in the latest revision of each deal that has no migrated thread yet, create a thread on that target with one comment: author and time from the note's `actor`/`at`, body = the note, and an `activity` row of kind `comment`. Record migrated targets in a table `migrations(key TEXT PRIMARY KEY)` (key `note:<slug>:<kind>:<uid>`) so it never runs twice. Do not change revisions.

After this phase the frontend stops sending `note` in `review` and `finding` operations (it sends `""`). The backend keeps accepting `note` for compatibility.

## API

All JSON. Times are ISO-8601 UTC strings as `_now()` produces.

### `GET /api/deal/<slug>` (existing), additions

```json
"field_authors": { "<uid>": { "<field>": {"actor": "alex", "at": "…", "revision": 12} } },
"thread_counts": { "<uid or finding id or 'deal'>": {"open": 2, "resolved": 1} },
"seen": {"activity_id": 41, "revision": 11, "at": "…"}
```

- `field_authors` is computed from all revisions' stored `changes` for the working copy, in revision order: `update` sets `[uid][field]`; `insert` sets every field of the inserted row; `restore` revisions clear and recompute from the restored revision's history (simplest correct approach: when a restore to revision R is saved, attribute each field changed by the restore diff to the restorer; fields unchanged keep their earlier author). Only for `version=working`; `{}` for immutable versions.
- `seen` is the current user's row for this deal (`null` if none or user is `unknown`). `revision` is the highest revision whose activity id ≤ `seen.activity_id`.

### `GET /api/deals` (existing), additions per deal

```json
"unseen": {"since": "<seen.at or null>", "by": {"alex": {"edits": 12, "comments": 3}}, "latest_activity_id": 57}
```

Counts only activity by *other* actors with `id > seen.activity_id` (all activity if never seen). `edits` counts `revision` and `restore` rows; `comments` counts `comment` and `reply`. `by` is `{}` when nothing is new. Omitted for `unknown`.

### `GET /api/deal/<slug>/comments`

```json
{"threads": [{
  "id": "…", "target": {"kind": "row", "sheet": "Deal ledger", "uid": "…", "label": "Event #12 · …"},
  "target_missing": false,
  "created_by": "austin", "created_at": "…",
  "resolved": null,
  "comments": [{"id": "…", "parent_id": null, "actor": "austin", "at": "…", "body": "…",
                "edited_at": null, "deleted": null, "edit_count": 0}]
}]}
```

Threads ordered by `created_at`; comments by `at`. `target_missing` is true when a row target no longer exists in the working state. For a missing row, `label` is the stored creation label.

### `POST /api/deal/<slug>/comments`

Body is one action; response is the full `GET …/comments` payload.

```json
{"action": "create", "target": {"kind": "row", "sheet": "Deal ledger", "uid": "…"}, "body": "…"}
{"action": "create", "target": {"kind": "deal"}, "body": "…"}
{"action": "create", "target": {"kind": "finding", "uid": "datalink-f9"}, "body": "…"}
{"action": "reply",  "thread_id": "…", "body": "…"}
{"action": "edit",   "comment_id": "…", "body": "…"}
{"action": "delete", "comment_id": "…"}
{"action": "resolve", "thread_id": "…"}
{"action": "reopen",  "thread_id": "…"}
```

Errors use the existing `WorkspaceError` statuses (400 invalid, 403 not the author, 404 unknown thread/comment/target).

### `GET /api/deal/<slug>/activity?limit=200`

```json
{"items": [{"id": 57, "at": "…", "actor": "alex", "kind": "reply", "summary": "…",
            "revision": null, "thread_id": "…", "comment_id": "…",
            "target": {"kind": "row", "sheet": "Deal ledger", "uid": "…", "label": "…"},
            "unseen": true}],
 "seen": {"activity_id": 41, "revision": 11, "at": "…"}}
```

Newest first. `unseen` is true when `id > seen.activity_id` and `actor` is not the current user. `target` is present for comment kinds (from the thread).

### `POST /api/deal/<slug>/seen`

`{"activity_id": 57}` sets the current user's seen marker to exactly that id (it may move backwards, which is how "mark unread" works). The id must be 0 or an existing activity id of this deal. Response: `{"seen": {...}}`.

### `GET /api/activity?actor=&slug=&kind=&before=&limit=100`

Account-wide feed across deals, newest first, with the same item shape plus `slug` and the deal `name`. `before` is an activity id for paging. Filters are optional and exact-match.

## Frontend behaviour

Follow the "working papers" design in `_dev/COCKPIT_BUILD.md`: hairlines, alignment and weight; no cards, chips or tinted boxes; the only accent is the control blue; Fluent UI controls and Phosphor icons already in use; tokens in the single `:root` block of `style.css`.

1. **Overview** (`Overview.jsx`): under each deal with non-empty `unseen.by`, one muted line: "Alex · 12 edits, 3 comments since you last looked". Nothing otherwise.
2. **What's new** panel at the top of the deal workspace, collapsible, shown only when the activity has unseen items. Group unseen items by actor and session (a new session starts after a 30-minute gap). Each group: "Alex · 23 Sep 14:05–14:40 · 5 edits, 2 comments", expandable to its items. Items link: revisions open the History tab at that revision; comment kinds select the target row and open its thread (deal and finding threads open the Review tab). Buttons: "Mark as read" (POST seen with the newest activity id) and, after marking, "Mark unread" (restore the previous id). Leaving the deal (route change or `pagehide`) marks as read with `fetch(…, {keepalive: true})` and the CSRF header, but only if the panel was shown.
3. **Comments** component used in the Ledger, Rounds, Questions and Deal facts editors (below the fields) and in the Review tab (a "Discussion" section for deal-level threads, and a thread under each finding). Shows threads for that target, newest thread last; a "New comment" box; reply, resolve/reopen, and edit/delete on your own comments ("edited" marker; deleted shows "Comment deleted by Alex"). Resolved threads are collapsed to one line. Comments do not use the unsaved-edits dock: each action posts immediately.
4. **Remove the note textareas** from row review and finding judgment; statuses stay. Send `note: ""`.
5. **Last changed by**: in the editors, each field label gets a tooltip "Alex · 23 Sep 14:05 · revision 12" from `field_authors`, linking to History. No visible text unless focused or hovered.
6. **Row marks**: in the event and record lists, a small mono initials mark (`AL` for Austin, `AG` for Alex) on rows with any field changed by the other user in a revision greater than `seen.revision`, and an open-thread count from `thread_counts` (e.g. a speech-bubble icon with "2"). Nothing when zero.
7. **Activity page** at `/activity`, linked from the header: the account-wide feed with filters (person, deal, type) and "Load more".
8. Unknown users see comments read-only and no What's new.

## Tests and acceptance

- Backend unit tests (extend `_dev/tools/test_cockpit_workspace.py` or add `_dev/tools/test_cockpit_trace.py`, `unittest`, temporary copies): thread create/reply/edit/delete/resolve/reopen, authorship enforcement, reply reopening, activity rows written atomically with saves and comments, `unseen` counts exclude own activity, `seen` can move backwards, `field_authors` for update/insert/restore, note migration idempotence, missing-DB reads, `target_missing` after a row delete.
- HTTP tests (`_dev/tools/cockpit/acceptance/test_http.py`): new routes require CSRF/Origin for writes; `unknown` cannot write.
- Frontend: `npm test` and `npm run build` pass; add vitest for session grouping (30-minute gap) and initials.
- Existing suites stay green: `python3 -m pytest -q _dev/tools/test_cockpit.py _dev/tools/test_cockpit_workspace.py _dev/tools/cockpit/`, vitest, and the browser acceptance scripts in `_dev/tools/cockpit/acceptance/`.
- Two-user acceptance (Opus): with a loopback server on a scratch database and the `Cf-Access-Authenticated-User-Email` header set to each user in turn under `COCKPIT_REQUIRE_ACCESS=1`, Alex saves edits and comments, Austin's overview and What's new show them, marking read clears them, and marking unread restores them.
