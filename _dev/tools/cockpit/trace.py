"""Comments, activity and "since your last visit" state for the shared working copies.

Everything lives in the workspace SQLite file beside the revisions. Reads tolerate a
missing database or missing tables and never create either; writes run in one
transaction with their activity row.
"""
from __future__ import annotations

import json
import sqlite3
import uuid
from typing import Any

from cockpit.workspace import SHEETS, Conflict, Missing, Workspace, WorkspaceError, _now, record_label

SCHEMA = (
    "CREATE TABLE IF NOT EXISTS threads (id TEXT PRIMARY KEY, slug TEXT NOT NULL, target_kind TEXT NOT NULL CHECK (target_kind IN ('deal','row','finding')), target_sheet TEXT, target_uid TEXT, target_label TEXT NOT NULL, created_by TEXT NOT NULL, created_at TEXT NOT NULL, resolved_by TEXT, resolved_at TEXT)",
    "CREATE TABLE IF NOT EXISTS comments (id TEXT PRIMARY KEY, thread_id TEXT NOT NULL REFERENCES threads(id), parent_id TEXT, actor TEXT NOT NULL, at TEXT NOT NULL, body TEXT NOT NULL, edited_at TEXT, deleted_by TEXT, deleted_at TEXT)",
    "CREATE TABLE IF NOT EXISTS comment_edits (comment_id TEXT NOT NULL, at TEXT NOT NULL, previous_body TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS activity (id INTEGER PRIMARY KEY AUTOINCREMENT, slug TEXT NOT NULL, at TEXT NOT NULL, actor TEXT NOT NULL, kind TEXT NOT NULL, revision INTEGER, thread_id TEXT, comment_id TEXT, summary TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS seen (user TEXT NOT NULL, slug TEXT NOT NULL, activity_id INTEGER NOT NULL, at TEXT NOT NULL, PRIMARY KEY (user, slug))",
    "CREATE TABLE IF NOT EXISTS migrations (key TEXT PRIMARY KEY)",
    "CREATE INDEX IF NOT EXISTS activity_slug ON activity (slug, id)",
    "CREATE INDEX IF NOT EXISTS threads_slug ON threads (slug)",
    "CREATE INDEX IF NOT EXISTS comments_thread ON comments (thread_id)",
)
EDIT_KINDS = ("revision", "restore")
COMMENT_KINDS = ("comment", "reply")
KINDS = EDIT_KINDS + COMMENT_KINDS + ("resolve", "reopen", "comment_edit", "comment_delete")
MAX_BODY = 20000


def ensure_schema(conn: sqlite3.Connection) -> None:
    """Create the trace tables and migrate legacy notes once. Called on every write connection."""
    for statement in SCHEMA:
        conn.execute(statement)
    conn.commit()
    if conn.execute("SELECT 1 FROM migrations WHERE key='notes-v1'").fetchone():
        return
    conn.execute("BEGIN IMMEDIATE")
    try:
        if not conn.execute("SELECT 1 FROM migrations WHERE key='notes-v1'").fetchone():
            _migrate_notes(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def _migrate_notes(conn: sqlite3.Connection) -> None:
    latest = conn.execute("SELECT r.slug, r.snapshot FROM revisions r JOIN (SELECT slug, MAX(revision) AS revision FROM revisions GROUP BY slug) m ON r.slug=m.slug AND r.revision=m.revision").fetchall()
    for row in latest:
        slug, state = row[0], json.loads(row[1])
        records = {r["uid"]: (sheet, r) for sheet in SHEETS for r in state["sheets"][sheet]["rows"]}
        for kind, notes in (("row", state.get("row_review", {})), ("finding", state.get("findings", {}))):
            for uid, entry in notes.items():
                note = (entry or {}).get("note") or ""
                if not note.strip():
                    continue
                key = f"note:{slug}:{kind}:{uid}"
                if conn.execute("SELECT 1 FROM migrations WHERE key=?", (key,)).fetchone():
                    continue
                if kind == "row":
                    sheet, record = records.get(uid, (None, None))
                    label = record_label(sheet, record, record) if record else f"Row {uid}"
                else:
                    sheet, label = None, f"Finding {uid}"
                actor, at = entry.get("actor") or "unknown", entry.get("at") or _now()
                thread = _insert_thread(conn, slug, kind, sheet, uid, label, actor, at)
                comment = _insert_comment(conn, thread, None, actor, at, note)
                _activity(conn, slug, actor, "comment", summary=_summary(note), thread_id=thread, comment_id=comment, at=at)
                conn.execute("INSERT INTO migrations VALUES (?)", (key,))
    conn.execute("INSERT INTO migrations VALUES ('notes-v1')")


def record_revision(conn: sqlite3.Connection, slug: str, actor: str, revision: int, reason: str, restore: bool, at: str) -> None:
    """Called by Workspace.edit inside its transaction, with the revision's own timestamp."""
    _activity(conn, slug, actor, "restore" if restore else "revision", revision=revision, summary=_summary(reason), at=at)


def _summary(text: str) -> str:
    line = " ".join(text.split())
    return line if len(line) <= 140 else line[:139] + "…"


def _activity(conn: sqlite3.Connection, slug: str, actor: str, kind: str, *, revision: int | None = None, thread_id: str | None = None, comment_id: str | None = None, summary: str = "", at: str | None = None) -> int:
    cursor = conn.execute("INSERT INTO activity (slug, at, actor, kind, revision, thread_id, comment_id, summary) VALUES (?,?,?,?,?,?,?,?)", (slug, at or _now(), actor, kind, revision, thread_id, comment_id, summary))
    return int(cursor.lastrowid)


def _insert_thread(conn: sqlite3.Connection, slug: str, kind: str, sheet: str | None, uid: str | None, label: str, actor: str, at: str) -> str:
    ident = uuid.uuid4().hex
    conn.execute("INSERT INTO threads (id, slug, target_kind, target_sheet, target_uid, target_label, created_by, created_at) VALUES (?,?,?,?,?,?,?,?)", (ident, slug, kind, sheet, uid, label, actor, at))
    return ident


def _insert_comment(conn: sqlite3.Connection, thread: str, parent: str | None, actor: str, at: str, body: str) -> str:
    ident = uuid.uuid4().hex
    conn.execute("INSERT INTO comments (id, thread_id, parent_id, actor, at, body) VALUES (?,?,?,?,?,?)", (ident, thread, parent, actor, at, body))
    return ident


def _body(value: Any) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > MAX_BODY:
        raise WorkspaceError(f"comment must be 1 to {MAX_BODY} characters")
    return value.strip()


def _rows(conn: sqlite3.Connection | None, query: str, params: tuple = ()) -> list[sqlite3.Row]:
    if conn is None:
        return []
    try:
        return conn.execute(query, params).fetchall()
    except sqlite3.OperationalError:
        return []


class Trace:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace

    # ---- reads ---------------------------------------------------------------

    def _seen(self, conn: sqlite3.Connection | None, user: str, slug: str) -> dict[str, Any] | None:
        if user == "unknown":
            return None
        found = _rows(conn, "SELECT activity_id, at FROM seen WHERE user=? AND slug=?", (user, slug))
        if not found:
            return None
        activity_id = found[0]["activity_id"]
        revision = _rows(conn, "SELECT MAX(revision) AS r FROM activity WHERE slug=? AND id<=? AND revision IS NOT NULL", (slug, activity_id))
        return {"activity_id": activity_id, "revision": (revision[0]["r"] if revision else None) or 0, "at": found[0]["at"]}

    def deal_extras(self, slug: str, user: str, version: str = "working") -> dict[str, Any]:
        """Additions to GET /api/deal: field authors, thread counts and the reader's seen marker."""
        conn = self.workspace._connect()
        try:
            authors: dict[str, dict[str, Any]] = {}
            if version == "working":
                for row in _rows(conn, "SELECT revision, at, actor, changes FROM revisions WHERE slug=? ORDER BY revision", (slug,)):
                    for change in json.loads(row["changes"]):
                        uid, kind = change.get("uid"), change.get("type")
                        stamp = {"actor": row["actor"], "at": row["at"], "revision": row["revision"]}
                        if kind == "update" and change.get("sheet") in SHEETS:
                            authors.setdefault(uid, {})[change["field"]] = stamp
                        elif kind == "insert":
                            authors[uid] = {field: stamp for field in (change.get("after") or {})}
                        elif kind == "delete":
                            authors.pop(uid, None)
            counts: dict[str, dict[str, int]] = {}
            for row in _rows(conn, "SELECT target_kind, target_uid, resolved_at FROM threads WHERE slug=?", (slug,)):
                key = row["target_uid"] if row["target_kind"] != "deal" else "deal"
                entry = counts.setdefault(key, {"open": 0, "resolved": 0})
                entry["resolved" if row["resolved_at"] else "open"] += 1
            return {"field_authors": authors, "thread_counts": counts, "seen": self._seen(conn, user, slug)}
        finally:
            if conn: conn.close()

    def unseen(self, slug: str, user: str) -> dict[str, Any] | None:
        """The per-deal summary for GET /api/deals: other people's activity since the reader last looked."""
        if user == "unknown":
            return None
        conn = self.workspace._connect()
        try:
            seen = self._seen(conn, user, slug)
            after = seen["activity_id"] if seen else 0
            by: dict[str, dict[str, int]] = {}
            for row in _rows(conn, "SELECT actor, kind, COUNT(*) AS n FROM activity WHERE slug=? AND id>? AND actor<>? GROUP BY actor, kind", (slug, after, user)):
                entry = by.setdefault(row["actor"], {"edits": 0, "comments": 0})
                if row["kind"] in EDIT_KINDS: entry["edits"] += row["n"]
                elif row["kind"] in COMMENT_KINDS: entry["comments"] += row["n"]
            by = {actor: counts for actor, counts in by.items() if counts["edits"] or counts["comments"]}
            latest = _rows(conn, "SELECT MAX(id) AS id FROM activity WHERE slug=?", (slug,))
            return {"since": seen["at"] if seen else None, "by": by, "latest_activity_id": (latest[0]["id"] if latest else None) or 0}
        finally:
            if conn: conn.close()

    def comments(self, slug: str) -> dict[str, Any]:
        item = self.workspace.item(slug)
        conn = self.workspace._connect()
        try:
            return self._threads(conn, slug, item)
        finally:
            if conn: conn.close()

    def _threads(self, conn: sqlite3.Connection | None, slug: str, item: dict[str, Any]) -> dict[str, Any]:
        threads = _rows(conn, "SELECT * FROM threads WHERE slug=? ORDER BY created_at, rowid", (slug,))
        if not threads:
            return {"threads": []}
        state, _, _ = self.workspace._state(slug, item, conn)
        live = {r["uid"] for sheet in SHEETS for r in state["sheets"][sheet]["rows"]}
        edits = {row["comment_id"]: row["n"] for row in _rows(conn, "SELECT comment_id, COUNT(*) AS n FROM comment_edits GROUP BY comment_id")}
        comments: dict[str, list[dict[str, Any]]] = {}
        for c in _rows(conn, "SELECT c.* FROM comments c JOIN threads t ON c.thread_id=t.id WHERE t.slug=? ORDER BY c.at, c.rowid", (slug,)):
            deleted = {"by": c["deleted_by"], "at": c["deleted_at"]} if c["deleted_at"] else None
            comments.setdefault(c["thread_id"], []).append({"id": c["id"], "parent_id": c["parent_id"], "actor": c["actor"], "at": c["at"], "body": "" if deleted else c["body"], "edited_at": c["edited_at"], "deleted": deleted, "edit_count": edits.get(c["id"], 0)})
        return {"threads": [self._thread_json(t, comments.get(t["id"], []), live) for t in threads]}

    @staticmethod
    def _target(t: sqlite3.Row) -> dict[str, Any]:
        target: dict[str, Any] = {"kind": t["target_kind"], "label": t["target_label"]}
        if t["target_kind"] == "row": target["sheet"] = t["target_sheet"]
        if t["target_kind"] != "deal": target["uid"] = t["target_uid"]
        return target

    def _thread_json(self, t: sqlite3.Row, comments: list[dict[str, Any]], live: set[str]) -> dict[str, Any]:
        return {"id": t["id"], "target": self._target(t), "target_missing": t["target_kind"] == "row" and t["target_uid"] not in live,
                "created_by": t["created_by"], "created_at": t["created_at"],
                "resolved": {"by": t["resolved_by"], "at": t["resolved_at"]} if t["resolved_at"] else None,
                "comments": comments}

    def activity(self, user: str, slug: str | None = None, *, actor: str | None = None, kind: str | None = None, before: int | None = None, limit: int = 200, account: bool = False) -> dict[str, Any]:
        """A deal's feed, or with account=True the account-wide feed (optionally filtered to one deal), newest first."""
        catalog = self.workspace.catalog()["deals"]
        if slug is not None:
            self.workspace.item(slug)
        conn = self.workspace._connect()
        try:
            clauses, params = [], []
            for column, value in (("a.slug", slug), ("a.actor", actor), ("a.kind", kind)):
                if value:
                    clauses.append(f"{column}=?"); params.append(value)
            if before is not None:
                clauses.append("a.id<?"); params.append(before)
            where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
            rows = _rows(conn, f"SELECT a.*, t.target_kind, t.target_sheet, t.target_uid, t.target_label FROM activity a LEFT JOIN threads t ON a.thread_id=t.id {where} ORDER BY a.id DESC LIMIT ?", (*params, max(1, min(limit, 500))))
            seen_cache: dict[str, dict[str, Any] | None] = {}
            items = []
            for row in rows:
                if row["slug"] not in seen_cache:
                    seen_cache[row["slug"]] = self._seen(conn, user, row["slug"])
                seen = seen_cache[row["slug"]]
                entry = {"id": row["id"], "at": row["at"], "actor": row["actor"], "kind": row["kind"], "summary": row["summary"], "revision": row["revision"], "thread_id": row["thread_id"], "comment_id": row["comment_id"],
                         "unseen": user != "unknown" and row["actor"] != user and row["id"] > (seen["activity_id"] if seen else 0)}
                if row["target_kind"]:
                    entry["target"] = self._target(row)
                if account:
                    entry["slug"] = row["slug"]; entry["name"] = catalog.get(row["slug"], {}).get("name", row["slug"])
                items.append(entry)
            result: dict[str, Any] = {"items": items}
            if not account:
                result["seen"] = self._seen(conn, user, slug)
            return result
        finally:
            if conn: conn.close()

    # ---- writes --------------------------------------------------------------

    def _write(self):
        conn = self.workspace._connect(write=True)
        assert conn is not None
        conn.execute("BEGIN IMMEDIATE")
        return conn

    def comment(self, slug: str, request: dict[str, Any], actor: str) -> dict[str, Any]:
        item = self.workspace.item(slug)
        if not isinstance(request, dict):
            raise WorkspaceError("comment action required")
        action = request.get("action")
        conn = self._write()
        try:
            now = _now()
            if action == "create":
                target = request.get("target")
                if not isinstance(target, dict): raise WorkspaceError("target required")
                kind, body = target.get("kind"), _body(request.get("body"))
                sheet = uid = None
                if kind == "deal":
                    label = "Whole deal"
                elif kind == "finding":
                    uid = target.get("uid")
                    finding = next((f for f in item.get("findings", []) if f.get("id") == uid), None)
                    if finding is None: raise Missing("unknown finding")
                    label = f"Finding {uid}" + (f" · {finding['title']}" if finding.get("title") else "")
                elif kind == "row":
                    sheet, uid = target.get("sheet"), target.get("uid")
                    if sheet not in SHEETS: raise WorkspaceError("unknown sheet")
                    state, _, _ = self.workspace._state(slug, item, conn)
                    record = next((r for r in state["sheets"][sheet]["rows"] if r["uid"] == uid), None)
                    if record is None: raise Missing("unknown row uid")
                    label = record_label(sheet, record, record)
                else:
                    raise WorkspaceError("invalid target kind")
                thread = _insert_thread(conn, slug, kind, sheet, uid, label, actor, now)
                comment = _insert_comment(conn, thread, None, actor, now, body)
                _activity(conn, slug, actor, "comment", thread_id=thread, comment_id=comment, summary=_summary(body), at=now)
            elif action in ("reply", "resolve", "reopen"):
                thread = conn.execute("SELECT * FROM threads WHERE id=? AND slug=?", (request.get("thread_id"), slug)).fetchone()
                if thread is None: raise Missing("unknown thread")
                if action == "reply":
                    body = _body(request.get("body"))
                    first = conn.execute("SELECT id FROM comments WHERE thread_id=? AND parent_id IS NULL ORDER BY at, rowid LIMIT 1", (thread["id"],)).fetchone()
                    if thread["resolved_at"]:
                        conn.execute("UPDATE threads SET resolved_by=NULL, resolved_at=NULL WHERE id=?", (thread["id"],))
                        _activity(conn, slug, actor, "reopen", thread_id=thread["id"], summary="Reopened by reply", at=now)
                    comment = _insert_comment(conn, thread["id"], first["id"] if first else None, actor, now, body)
                    _activity(conn, slug, actor, "reply", thread_id=thread["id"], comment_id=comment, summary=_summary(body), at=now)
                elif action == "resolve":
                    if thread["resolved_at"]: raise Conflict("thread already resolved")
                    conn.execute("UPDATE threads SET resolved_by=?, resolved_at=? WHERE id=?", (actor, now, thread["id"]))
                    _activity(conn, slug, actor, "resolve", thread_id=thread["id"], summary="Resolved", at=now)
                else:
                    if not thread["resolved_at"]: raise Conflict("thread is open")
                    conn.execute("UPDATE threads SET resolved_by=NULL, resolved_at=NULL WHERE id=?", (thread["id"],))
                    _activity(conn, slug, actor, "reopen", thread_id=thread["id"], summary="Reopened", at=now)
            elif action in ("edit", "delete"):
                comment = conn.execute("SELECT c.* FROM comments c JOIN threads t ON c.thread_id=t.id WHERE c.id=? AND t.slug=?", (request.get("comment_id"), slug)).fetchone()
                if comment is None: raise Missing("unknown comment")
                if comment["actor"] != actor:
                    error = WorkspaceError("only the author may change a comment"); error.status = 403; raise error
                if comment["deleted_at"]: raise Conflict("comment already deleted")
                if action == "edit":
                    body = _body(request.get("body"))
                    if body == comment["body"]: raise WorkspaceError("no changes to save")
                    conn.execute("INSERT INTO comment_edits VALUES (?,?,?)", (comment["id"], now, comment["body"]))
                    conn.execute("UPDATE comments SET body=?, edited_at=? WHERE id=?", (body, now, comment["id"]))
                    _activity(conn, slug, actor, "comment_edit", thread_id=comment["thread_id"], comment_id=comment["id"], summary=_summary(body), at=now)
                else:
                    conn.execute("UPDATE comments SET deleted_by=?, deleted_at=? WHERE id=?", (actor, now, comment["id"]))
                    _activity(conn, slug, actor, "comment_delete", thread_id=comment["thread_id"], comment_id=comment["id"], summary="Comment deleted", at=now)
            else:
                raise WorkspaceError("unknown comment action")
            payload = self._threads(conn, slug, item)
            conn.commit()
            return payload
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def mark_seen(self, slug: str, request: dict[str, Any], user: str) -> dict[str, Any]:
        self.workspace.item(slug)
        activity_id = request.get("activity_id") if isinstance(request, dict) else None
        if type(activity_id) is not int or not 0 <= activity_id < 2**63: raise WorkspaceError("activity_id required")
        conn = self._write()
        try:
            if activity_id and not conn.execute("SELECT 1 FROM activity WHERE id=? AND slug=?", (activity_id, slug)).fetchone():
                raise Missing("unknown activity id")
            conn.execute("INSERT INTO seen VALUES (?,?,?,?) ON CONFLICT(user, slug) DO UPDATE SET activity_id=excluded.activity_id, at=excluded.at", (user, slug, activity_id, _now()))
            seen = self._seen(conn, user, slug)
            conn.commit()
            return {"seen": seen}
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
