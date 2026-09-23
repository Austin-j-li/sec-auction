"""Claude accounts, extraction jobs and imported versions for the cockpit.

The HTTP server only reads and writes these rows; `worker.py` starts processes, runs
the isolated extraction, checks and imports the result. Tokens live outside the
repository, readable only by their owner, and never leave the server.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sqlite3
import uuid
from pathlib import Path
from typing import Any

from cockpit.workspace import SAFE_ID, Conflict, Missing, Workspace, WorkspaceError, _now

SCHEMA = (
    "CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, kind TEXT NOT NULL, slug TEXT, actor TEXT NOT NULL, created_at TEXT NOT NULL, state TEXT NOT NULL, params TEXT NOT NULL, cancel_requested INTEGER NOT NULL DEFAULT 0, input TEXT, pid INTEGER, run_dir TEXT, started_at TEXT, ended_at TEXT, failure_reason TEXT, error TEXT, result TEXT, version_id TEXT, cancelled_by TEXT)",
    "CREATE INDEX IF NOT EXISTS jobs_state ON jobs (state, created_at)",
    "CREATE TABLE IF NOT EXISTS accounts (user TEXT NOT NULL, provider TEXT NOT NULL, connected_at TEXT NOT NULL, expires_at TEXT, PRIMARY KEY (user, provider))",
    "CREATE TABLE IF NOT EXISTS plan_usage (user TEXT NOT NULL, provider TEXT NOT NULL, at TEXT NOT NULL, info TEXT NOT NULL, PRIMARY KEY (user, provider))",
    "CREATE TABLE IF NOT EXISTS versions (slug TEXT NOT NULL, id TEXT NOT NULL, label TEXT NOT NULL, path TEXT NOT NULL, sha256 TEXT NOT NULL, kind TEXT NOT NULL, engine TEXT NOT NULL, model TEXT NOT NULL, effort TEXT NOT NULL, instruction_version TEXT, instruction_sha256 TEXT NOT NULL, filing_sha256 TEXT NOT NULL, started_by TEXT NOT NULL, started_at TEXT NOT NULL, finished_at TEXT NOT NULL, receipts TEXT NOT NULL, checker TEXT NOT NULL, hidden INTEGER NOT NULL DEFAULT 0, hidden_by TEXT, hidden_at TEXT, PRIMARY KEY (slug, id))",
)
USERS = ("austin", "alex", "local")
NAMES = {"austin": "Austin", "alex": "Alex", "local": "Local"}
EFFORTS = ("low", "medium", "high", "xhigh", "max")
MODEL = "claude-opus-5-5"
ENGINE = "Opus 5.5"
ACTIVE = ("queued", "preparing", "running", "checking", "importing")
CONNECT_ACTIVE = ("queued", "waiting_for_code", "completing")
TOKEN_RE = re.compile(r"sk-ant-oat\d\d-[A-Za-z0-9_-]{20,}")
CAPS = {"total": 4, "per_user": 2}


def ensure_schema(conn: sqlite3.Connection) -> None:
    for statement in SCHEMA:
        conn.execute(statement)
    if "cancelled_by" not in {row[1] for row in conn.execute("PRAGMA table_info(jobs)")}:
        conn.execute("ALTER TABLE jobs ADD COLUMN cancelled_by TEXT")
    conn.commit()


def token_root() -> Path:
    return Path(os.environ.get("COCKPIT_TOKEN_ROOT") or Path.home() / ".config/sec-extraction/users")


def token_path(user: str) -> Path:
    if user not in USERS:
        raise WorkspaceError("unknown user")
    return token_root() / user / "claude-oauth-token"


def save_token(user: str, token: str) -> None:
    """Write a token readable only by the service user (the runner refuses anything looser)."""
    path = token_path(user)
    path.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "w") as handle:
        handle.write(token.strip() + "\n")
    os.chmod(path, 0o600)


def _json(value: str | None) -> Any:
    return json.loads(value) if value else None


def _rows(conn: sqlite3.Connection | None, query: str, params: tuple = ()) -> list[sqlite3.Row]:
    if conn is None:
        return []
    try:
        return conn.execute(query, params).fetchall()
    except sqlite3.OperationalError:
        return []


def version_json(row: sqlite3.Row) -> dict[str, Any]:
    return {"id": row["id"], "label": row["label"], "path": row["path"], "sha256": row["sha256"], "kind": row["kind"],
            "instruction_version": row["instruction_version"], "instruction_sha256": row["instruction_sha256"],
            "filing_sha256": row["filing_sha256"], "review_status": "unreviewed", "engine": row["engine"], "model": row["model"],
            "effort": row["effort"], "started_by": row["started_by"], "started_at": row["started_at"], "finished_at": row["finished_at"],
            "receipts": row["receipts"], "checker": _json(row["checker"]), "hidden": bool(row["hidden"])}


def imported_versions(workspace: Workspace, slug: str) -> list[dict[str, Any]]:
    """Versions imported from cockpit runs, oldest first. Reads never create the database."""
    conn = workspace._connect()
    try:
        return [version_json(row) for row in _rows(conn, "SELECT * FROM versions WHERE slug=? ORDER BY started_at, id", (slug,))]
    finally:
        if conn: conn.close()


def job_json(row: sqlite3.Row) -> dict[str, Any]:
    return {"id": row["id"], "kind": row["kind"], "slug": row["slug"], "state": row["state"], "actor": row["actor"],
            "created_at": row["created_at"], "started_at": row["started_at"], "ended_at": row["ended_at"],
            "params": _json(row["params"]), "failure_reason": row["failure_reason"], "error": row["error"],
            "result": _json(row["result"]), "version_id": row["version_id"], "cancel_requested": bool(row["cancel_requested"]), "cancelled_by": row["cancelled_by"]}


class Runs:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace

    def _write(self) -> sqlite3.Connection:
        conn = self.workspace._connect(write=True)
        assert conn is not None
        conn.execute("BEGIN IMMEDIATE")
        return conn

    def _transaction(self, action):
        conn = self._write()
        try:
            value = action(conn)
            conn.commit()
            return value
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # ---- accounts --------------------------------------------------------------

    def account(self, user: str) -> dict[str, Any]:
        conn = self.workspace._connect()
        try:
            found = _rows(conn, "SELECT * FROM accounts WHERE user=? AND provider='claude'", (user,))
            connected = bool(found) and token_path(user).is_file() if user in USERS else False
            usage = _rows(conn, "SELECT at, info FROM plan_usage WHERE user=? AND provider='claude'", (user,))
            plan = None
            if usage:
                windows = (json.loads(usage[0]["info"]).get("unifiedWindows") or {})
                plan = {"at": usage[0]["at"], **{name: {"utilization": (windows.get(name) or {}).get("utilization"), "resets_at": (windows.get(name) or {}).get("resetsAt")} for name in ("five_hour", "seven_day")}}
            job = _rows(conn, "SELECT * FROM jobs WHERE kind='connect_claude' AND actor=? ORDER BY created_at DESC, rowid DESC LIMIT 1", (user,))
            connect = None
            if job and (job[0]["state"] != "completed" or (job[0]["ended_at"] or "") >= _minutes_ago(10)):
                connect = {"job_id": job[0]["id"], "state": job[0]["state"], "link": (_json(job[0]["result"]) or {}).get("link"), "error": job[0]["error"]}
            return {"user": user, "claude": {"connected": connected, "connected_at": found[0]["connected_at"] if connected else None,
                                              "expires_at": found[0]["expires_at"] if connected else None, "plan_usage": plan}, "connect": connect}
        finally:
            if conn: conn.close()

    def account_action(self, user: str, request: dict[str, Any]) -> dict[str, Any]:
        if user not in USERS:
            raise WorkspaceError("unknown user")
        action = request.get("action") if isinstance(request, dict) else None

        def run(conn: sqlite3.Connection) -> None:
            now = _now()
            if action == "connect":
                conn.execute("UPDATE jobs SET cancel_requested=1 WHERE kind='connect_claude' AND actor=? AND state IN ('queued','waiting_for_code','completing')", (user,))
                conn.execute("INSERT INTO jobs (id, kind, slug, actor, created_at, state, params) VALUES (?, 'connect_claude', NULL, ?, ?, 'queued', '{}')", (uuid.uuid4().hex, user, now))
            elif action in ("code", "cancel"):
                job = conn.execute("SELECT * FROM jobs WHERE id=? AND kind='connect_claude' AND actor=?", (request.get("job_id"), user)).fetchone()
                if job is None: raise Missing("unknown connect job")
                if action == "cancel":
                    if job["state"] not in CONNECT_ACTIVE: raise Conflict("connect is not in progress")
                    conn.execute("UPDATE jobs SET cancel_requested=1 WHERE id=?", (job["id"],))
                else:
                    code = request.get("code")
                    if job["state"] != "waiting_for_code": raise Conflict("not waiting for a code")
                    if not isinstance(code, str) or not code.strip() or len(code) > 500 or any(c in code for c in "\r\n\x00"):
                        raise WorkspaceError("invalid code")
                    conn.execute("UPDATE jobs SET input=? WHERE id=?", (code.strip(), job["id"]))
            elif action == "token":
                token = request.get("token")
                if not isinstance(token, str) or not TOKEN_RE.fullmatch(token.strip()):
                    raise WorkspaceError("that does not look like a token from `claude setup-token`")
                save_token(user, token)
                connected(conn, user)
            elif action == "disconnect":
                if conn.execute(f"SELECT 1 FROM jobs WHERE kind='extract' AND actor=? AND state IN ({','.join('?' * len(ACTIVE))})", (user, *ACTIVE)).fetchone():
                    raise Conflict("your runs are still using this account; wait for them or cancel them first")
                token_path(user).unlink(missing_ok=True)
                conn.execute("DELETE FROM accounts WHERE user=? AND provider='claude'", (user,))
            else:
                raise WorkspaceError("unknown account action")
        self._transaction(run)
        return self.account(user)

    # ---- jobs ------------------------------------------------------------------

    def jobs(self, slug: str) -> dict[str, Any]:
        self.workspace.item(slug)
        conn = self.workspace._connect()
        try:
            return {"jobs": [job_json(row) for row in _rows(conn, "SELECT * FROM jobs WHERE slug=? AND kind='extract' ORDER BY created_at DESC, rowid DESC LIMIT 30", (slug,))]}
        finally:
            if conn: conn.close()

    def active_jobs(self, slug: str) -> int:
        conn = self.workspace._connect()
        try:
            found = _rows(conn, f"SELECT COUNT(*) AS n FROM jobs WHERE slug=? AND kind='extract' AND state IN ({','.join('?' * len(ACTIVE))})", (slug, *ACTIVE))
            return found[0]["n"] if found else 0
        finally:
            if conn: conn.close()

    def job_action(self, slug: str, user: str, request: dict[str, Any]) -> dict[str, Any]:
        self.workspace.item(slug)
        action = request.get("action") if isinstance(request, dict) else None

        def run(conn: sqlite3.Connection) -> None:
            if action == "extract":
                effort, minutes = request.get("effort", "medium"), request.get("timeout_minutes", 90)
                if effort not in EFFORTS: raise WorkspaceError("invalid effort")
                if type(minutes) is not int or not 10 <= minutes <= 360: raise WorkspaceError("time limit must be 10 to 360 minutes")
                if not conn.execute("SELECT 1 FROM accounts WHERE user=? AND provider='claude'", (user,)).fetchone() or not token_path(user).is_file():
                    raise Conflict("connect your Claude account in Settings first")
                params = {"engine": ENGINE, "model": MODEL, "effort": effort, "timeout_minutes": minutes}
                conn.execute("INSERT INTO jobs (id, kind, slug, actor, created_at, state, params) VALUES (?, 'extract', ?, ?, ?, 'queued', ?)", (uuid.uuid4().hex, slug, user, _now(), json.dumps(params)))
            elif action == "cancel":
                job = conn.execute("SELECT * FROM jobs WHERE id=? AND slug=? AND kind='extract'", (request.get("job_id"), slug)).fetchone()
                if job is None: raise Missing("unknown job")
                if job["state"] not in ACTIVE: raise Conflict("job is not active")
                conn.execute("UPDATE jobs SET cancel_requested=1, cancelled_by=COALESCE(cancelled_by, ?) WHERE id=?", (user, job["id"]))
            else:
                raise WorkspaceError("unknown job action")
        self._transaction(run)
        return self.jobs(slug)

    # ---- versions --------------------------------------------------------------

    def version_action(self, slug: str, user: str, request: dict[str, Any]) -> dict[str, Any]:
        item = self.workspace.item(slug)
        action = request.get("action") if isinstance(request, dict) else None
        ident = request.get("version_id") if isinstance(request, dict) else None
        if action not in ("hide", "unhide"): raise WorkspaceError("unknown version action")
        if not isinstance(ident, str) or not SAFE_ID.fullmatch(ident): raise WorkspaceError("invalid version_id")
        if action == "hide" and self.workspace.working_base(slug, item)["id"] == ident:
            raise Conflict("the working copy's base cannot be hidden")

        def run(conn: sqlite3.Connection) -> None:
            row = conn.execute("SELECT * FROM versions WHERE slug=? AND id=?", (slug, ident)).fetchone()
            if row is None: raise Missing("only versions made in the cockpit can be hidden")
            if bool(row["hidden"]) == (action == "hide"): raise Conflict(f"version already {'hidden' if row['hidden'] else 'shown'}")
            now = _now()
            conn.execute("UPDATE versions SET hidden=?, hidden_by=?, hidden_at=? WHERE slug=? AND id=?", (1 if action == "hide" else 0, user, now, slug, ident))
            from cockpit import trace
            trace._activity(conn, slug, user, action, summary=f"{'Hid' if action == 'hide' else 'Unhid'} {row['label']}", at=now)
        self._transaction(run)
        return {"versions": imported_versions(self.workspace, slug)}


def connected(conn: sqlite3.Connection, user: str) -> None:
    """Record a newly saved Claude token (valid for a year from setup-token)."""
    now = _now()
    expires = _days_ahead(365)
    conn.execute("INSERT INTO accounts VALUES (?, 'claude', ?, ?) ON CONFLICT(user, provider) DO UPDATE SET connected_at=excluded.connected_at, expires_at=excluded.expires_at", (user, now, expires))


def _minutes_ago(minutes: int) -> str:
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=minutes)).isoformat(timespec="seconds")


def _days_ahead(days: int) -> str:
    return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=days)).isoformat(timespec="seconds")
