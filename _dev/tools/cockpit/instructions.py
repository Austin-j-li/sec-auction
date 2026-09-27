"""Instruction versions for the cockpit: drafts, published versions and the default.

Texts are stored by SHA-256 under `_dev/cockpit/state/instructions/` and never replaced, so a
run that names a hash always finds the exact text it was given. Published versions never
change; a draft keeps a history of its saves. The repository's working instruction is
imported once as the first published version and the default; nothing here writes it.
"""
from __future__ import annotations

import hashlib
import os
import re
import sqlite3
import uuid
from pathlib import Path
from typing import Any

from cockpit.workspace import Conflict, Missing, Workspace, WorkspaceError, _now

SCHEMA = (
    "CREATE TABLE IF NOT EXISTS instructions (id TEXT PRIMARY KEY, name TEXT UNIQUE, status TEXT NOT NULL, parent_id TEXT, sha256 TEXT NOT NULL, note TEXT, created_by TEXT NOT NULL, created_at TEXT NOT NULL, updated_by TEXT NOT NULL, updated_at TEXT NOT NULL, published_by TEXT, published_at TEXT)",
    "CREATE TABLE IF NOT EXISTS instruction_edits (instruction_id TEXT NOT NULL, seq INTEGER NOT NULL, sha256 TEXT NOT NULL, author TEXT NOT NULL, at TEXT NOT NULL, PRIMARY KEY (instruction_id, seq))",
    "CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL, updated_by TEXT NOT NULL, updated_at TEXT NOT NULL)",
)
REPOSITORY_INSTRUCTION = "SEC_Deal_Ledger_Extraction_Instruction.md"
NAME_RE = re.compile(r"[A-Za-z0-9._ -]{1,40}\Z")
ID_RE = re.compile(r"[0-9a-f]{12}\Z")
SHA_RE = re.compile(r"[0-9a-f]{64}\Z")
MAX_TEXT = 400 * 1024
MAX_NOTE = 2000
NAMES = {"austin": "Austin", "alex": "Alex", "local": "Local", "system": "System"}


def ensure_schema(conn: sqlite3.Connection) -> None:
    for statement in SCHEMA:
        conn.execute(statement)
    conn.commit()


def header_version(text: str) -> str | None:
    found = re.search(r"\bVersion\s+(\d+)\b", text[:600], re.I)
    if found:
        return f"Version {found.group(1)}"
    found = re.search(r"\bv(\d+\.\d+(?:\.\d+)?)\b", text[:600])
    return f"v{found.group(1)}" if found else None


def label(row: sqlite3.Row) -> str:
    if row["status"] == "published":
        return row["name"]
    return f"draft {row['sha256'][:7]} ({NAMES.get(row['created_by'], row['created_by'])})"


class Instructions:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.store = workspace.db_path.parent / "instructions"

    # ---- storage ------------------------------------------------------------------

    def path(self, sha: str) -> Path:
        if not SHA_RE.fullmatch(sha or ""):
            raise WorkspaceError("invalid instruction hash")
        return self.store / f"{sha}.md"

    def put(self, text: str) -> str:
        """Store a text under its hash (atomically, never replacing an existing copy)."""
        data = text.encode("utf-8")
        sha = hashlib.sha256(data).hexdigest()
        target = self.path(sha)
        if not target.is_file():
            self.store.mkdir(parents=True, exist_ok=True)
            temporary = target.with_suffix(f".{uuid.uuid4().hex}.tmp")
            temporary.write_bytes(data)
            os.replace(temporary, target)
        return sha

    def text(self, sha: str) -> str:
        path = self.path(sha)
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != sha:
            raise WorkspaceError(f"stored instruction {sha[:7]} does not match its hash")
        return data.decode("utf-8")

    def _connect(self) -> sqlite3.Connection:
        conn = self.workspace._connect(write=True)
        assert conn is not None
        self._seed(conn)
        return conn

    def _seed(self, conn: sqlite3.Connection) -> None:
        """Import the repository instruction as the first published version and the default."""
        if conn.execute("SELECT 1 FROM instructions LIMIT 1").fetchone():
            return
        source = self.workspace.root / REPOSITORY_INSTRUCTION
        if not source.is_file():
            return
        text = source.read_text(encoding="utf-8")
        sha = self.put(text)
        now = _now()
        ident = sha[:12]
        conn.execute("BEGIN IMMEDIATE")
        try:
            if not conn.execute("SELECT 1 FROM instructions LIMIT 1").fetchone():
                conn.execute("INSERT INTO instructions VALUES (?,?,'published',NULL,?,?,'system',?,'system',?,'system',?)",
                             (ident, header_version(text) or "imported", sha, f"Imported from {REPOSITORY_INSTRUCTION} in the repository.", now, now, now))
                conn.execute("INSERT INTO instruction_edits VALUES (?,1,?,'system',?)", (ident, sha, now))
                conn.execute("INSERT OR IGNORE INTO settings VALUES ('default_instruction', ?, 'system', ?)", (ident, now))
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def _transaction(self, action):
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            value = action(conn)
            conn.commit()
            return value
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # ---- reads --------------------------------------------------------------------

    def default_id(self, conn: sqlite3.Connection) -> str | None:
        row = conn.execute("SELECT value FROM settings WHERE key='default_instruction'").fetchone()
        return row["value"] if row else None

    def _row(self, conn: sqlite3.Connection, ident: Any) -> sqlite3.Row:
        if not isinstance(ident, str) or not ID_RE.fullmatch(ident):
            raise WorkspaceError("invalid instruction id")
        row = conn.execute("SELECT * FROM instructions WHERE id=?", (ident,)).fetchone()
        if row is None:
            raise Missing("unknown instruction")
        return row

    def _item(self, conn: sqlite3.Connection, row: sqlite3.Row, default: str | None) -> dict[str, Any]:
        parent = conn.execute("SELECT * FROM instructions WHERE id=?", (row["parent_id"],)).fetchone() if row["parent_id"] else None
        edits = conn.execute("SELECT COUNT(*) AS n FROM instruction_edits WHERE instruction_id=?", (row["id"],)).fetchone()["n"]
        return {key: row[key] for key in ("id", "name", "status", "parent_id", "sha256", "note", "created_by", "created_at", "updated_by", "updated_at", "published_by", "published_at")} | {
            "label": label(row), "parent_label": label(parent) if parent else None, "is_default": row["id"] == default, "edits": edits}

    def list(self) -> dict[str, Any]:
        conn = self._connect()
        try:
            default = self.default_id(conn)
            rows = conn.execute("SELECT * FROM instructions ORDER BY status='draft', COALESCE(published_at, updated_at) DESC, rowid DESC").fetchall()
            return {"default_id": default, "items": [self._item(conn, row, default) for row in rows]}
        finally:
            conn.close()

    def detail(self, ident: str, seq: int | None = None) -> dict[str, Any]:
        conn = self._connect()
        try:
            row = self._row(conn, ident)
            history = [dict(edit) for edit in conn.execute("SELECT seq, sha256, author, at FROM instruction_edits WHERE instruction_id=? ORDER BY seq", (ident,))]
            sha = row["sha256"]
            if seq is not None:
                sha = next((edit["sha256"] for edit in history if edit["seq"] == seq), None)
                if sha is None:
                    raise Missing("unknown edit")
            parent = conn.execute("SELECT sha256 FROM instructions WHERE id=?", (row["parent_id"],)).fetchone() if row["parent_id"] else None
            return {"item": self._item(conn, row, self.default_id(conn)), "seq": seq, "text": self.text(sha),
                    "parent_text": self.text(parent["sha256"]) if parent else None, "history": history}
        finally:
            conn.close()

    def resolve(self, ident: Any) -> dict[str, Any]:
        """The instruction a run will get, frozen now: id, label, published name and text hash."""
        conn = self._connect()
        try:
            if ident is None:
                ident = self.default_id(conn)
                if ident is None:
                    raise Conflict("no default instruction")
            row = self._row(conn, ident)
            self.text(row["sha256"])  # the stored copy must exist and match
            return {"id": row["id"], "label": label(row), "name": row["name"], "status": row["status"], "sha256": row["sha256"]}
        finally:
            conn.close()

    # ---- writes -------------------------------------------------------------------

    def request(self, user: str, body: Any) -> dict[str, Any]:
        if not isinstance(body, dict):
            raise WorkspaceError("invalid request")
        action = body.get("action")
        from cockpit import trace

        if action == "draft":
            source = body.get("from")

            def create(conn: sqlite3.Connection) -> str:
                parent = self._row(conn, source)
                ident = uuid.uuid4().hex[:12]
                now = _now()
                conn.execute("INSERT INTO instructions VALUES (?,NULL,'draft',?,?,NULL,?,?,?,?,NULL,NULL)", (ident, parent["id"], parent["sha256"], user, now, user, now))
                conn.execute("INSERT INTO instruction_edits VALUES (?,1,?,?,?)", (ident, parent["sha256"], user, now))
                draft = conn.execute("SELECT * FROM instructions WHERE id=?", (ident,)).fetchone()
                trace._activity(conn, "", user, "instruction_draft", summary=f"Started {label(draft)} from {label(parent)}", at=now)
                return ident
            return self.detail(self._transaction(create))

        if action == "save":
            text, base = body.get("text"), body.get("base_sha256")
            if not isinstance(text, str) or not text or len(text.encode("utf-8")) > MAX_TEXT:
                raise WorkspaceError(f"instruction text must be 1 character to {MAX_TEXT // 1024} KB")
            sha = self.put(text)

            def save(conn: sqlite3.Connection) -> None:
                row = self._row(conn, body.get("id"))
                if row["status"] != "draft":
                    raise Conflict("published instructions cannot be changed; start a draft from it")
                if base != row["sha256"]:
                    raise Conflict("someone saved this draft since you opened it")
                if sha == row["sha256"]:
                    return
                now = _now()
                seq = conn.execute("SELECT MAX(seq) AS n FROM instruction_edits WHERE instruction_id=?", (row["id"],)).fetchone()["n"] + 1
                conn.execute("UPDATE instructions SET sha256=?, updated_by=?, updated_at=? WHERE id=?", (sha, user, now, row["id"]))
                conn.execute("INSERT INTO instruction_edits VALUES (?,?,?,?,?)", (row["id"], seq, sha, user, now))
            self._transaction(save)
            return self.detail(body["id"])

        if action == "publish":
            name, note = body.get("name"), body.get("note")
            name = name.strip() if isinstance(name, str) else ""
            note = note.strip() if isinstance(note, str) else ""
            if not NAME_RE.fullmatch(name):
                raise WorkspaceError("name must be 1 to 40 letters, digits, spaces, dots, dashes or underscores")
            if not 1 <= len(note) <= MAX_NOTE:
                raise WorkspaceError(f"a change note of 1 to {MAX_NOTE} characters is required")

            def publish(conn: sqlite3.Connection) -> None:
                row = self._row(conn, body.get("id"))
                if row["status"] != "draft":
                    raise Conflict("already published")
                if conn.execute("SELECT 1 FROM instructions WHERE lower(name)=lower(?)", (name,)).fetchone():
                    raise Conflict(f"the name {name} is already used")
                now = _now()
                conn.execute("UPDATE instructions SET name=?, status='published', note=?, published_by=?, published_at=?, updated_by=?, updated_at=? WHERE id=?",
                             (name, note, user, now, user, now, row["id"]))
                trace._activity(conn, "", user, "instruction_published", summary=f"Published {name}: {note}"[:500], at=now)
            self._transaction(publish)
            return self.detail(body["id"])

        if action == "default":
            def make_default(conn: sqlite3.Connection) -> None:
                row = self._row(conn, body.get("id"))
                if row["status"] != "published":
                    raise Conflict("only a published instruction can be the default; publish the draft first")
                if self.default_id(conn) == row["id"]:
                    raise Conflict(f"{row['name']} is already the default")
                now = _now()
                conn.execute("INSERT INTO settings VALUES ('default_instruction', ?, ?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_by=excluded.updated_by, updated_at=excluded.updated_at",
                             (row["id"], user, now))
                trace._activity(conn, "", user, "instruction_default", summary=f"Made {row['name']} the default instruction", at=now)
            self._transaction(make_default)
            return self.list()

        raise WorkspaceError("unknown instruction action")
