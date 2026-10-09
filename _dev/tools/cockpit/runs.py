"""Claude and ChatGPT accounts, extraction jobs and imported versions for the cockpit.

The HTTP server only reads and writes these rows; `worker.py` starts processes, runs
the isolated extraction, checks and imports the result. Credentials live outside the
repository, readable only by their owner, and never leave the server.
"""
from __future__ import annotations

import base64
import datetime as dt
import json
import os
import re
import shutil
import sqlite3
import uuid
from pathlib import Path
from typing import Any

from cockpit.workspace import SAFE_ID, Conflict, Missing, Workspace, WorkspaceError, _now, add_column

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
# Extraction engines. "provider" is the runner's transport: "opus" drives Claude Code, "sol" Codex.
# "account" is whose plan pays: the starting user's Claude or ChatGPT subscription.
FABLE_NOTE = "Fable's safety filter often blocks runs partway (6 of 11 test prompts); a blocked run fails and must be restarted."
# Austin, 8 Oct 2026: GPT-6-Sol is no longer offered, and GPT-6.1-Sol runs on the Fast (priority) tier.
SOL_FAST_NOTE = "Runs on the Fast (priority) tier: about twice as fast, and it uses more of your ChatGPT plan."
ENGINES = {
    "opus55": {"label": "Opus 5.5", "name": "Claude Opus 5.5", "provider": "opus", "model": "claude-opus-5-5", "account": "claude", "experimental": False, "note": None},
    "fable51": {"label": "Fable 5.1", "name": "Claude Fable 5.1", "provider": "opus", "model": "claude-fable-5-1", "account": "claude", "experimental": True, "note": FABLE_NOTE},
    "sol61": {"label": "GPT-6.1-Sol", "name": "GPT-6.1-Sol", "provider": "sol", "model": "gpt-6.1-sol", "account": "chatgpt", "experimental": False, "note": SOL_FAST_NOTE},
    "astra6": {"label": "GPT-6-Astra", "name": "GPT-6-Astra", "provider": "sol", "model": "gpt-6-astra", "account": "chatgpt", "experimental": False, "note": None},
}
DEFAULT_ENGINE = "opus55"  # Austin, 26 Sep 2026: Opus 5.5 medium is the main extractor again.
LEGACY_ENGINE = "opus55"  # Jobs recorded before engine selection existed remain Claude jobs.
DEFAULT_EFFORT = {ident: "high" if ident == "astra6" else "medium" for ident in ENGINES}
ACTIVE = ("queued", "preparing", "running", "checking", "importing")
CONNECT_ACTIVE = ("queued", "waiting_for_code", "completing")
CHATGPT_CONNECT_ACTIVE = ("queued", "waiting_for_approval")
TOKEN_RE = re.compile(r"sk-ant-oat\d\d-[A-Za-z0-9_-]{20,}")
CAPS = {"total": 4, "per_user": 2}


def ensure_schema(conn: sqlite3.Connection) -> None:
    for statement in SCHEMA:
        conn.execute(statement)
    add_column(conn, "jobs", "cancelled_by", "TEXT")
    add_column(conn, "versions", "instruction_id", "TEXT")
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


def codex_home(user: str) -> Path:
    """The user's own Codex login folder (CODEX_HOME), holding auth.json."""
    if user not in USERS:
        raise WorkspaceError("unknown user")
    return token_root() / user / "codex"


def codex_login(auth: Path) -> dict[str, Any] | None:
    """Expiry, hours left and last refresh of a Codex login; None if there is no readable login."""
    try:
        document = json.loads(auth.read_text(encoding="utf-8"))
        payload = document["tokens"]["access_token"].split(".")[1]
        claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
        expires = dt.datetime.fromtimestamp(claims["exp"], dt.timezone.utc)
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError):
        return None
    return {"expires_at": expires.isoformat(timespec="seconds"), "last_refresh": document.get("last_refresh"),
            "hours_left": (expires - dt.datetime.now(dt.timezone.utc)).total_seconds() / 3600}


def job_account(params: dict[str, Any] | None) -> str:
    """Whose plan a job uses; jobs from before phase 4 are Opus 5.5 on Claude."""
    return ENGINES.get((params or {}).get("engine"), ENGINES[LEGACY_ENGINE])["account"]


def active_jobs_on(conn: sqlite3.Connection, user: str, account: str) -> bool:
    rows = conn.execute(f"SELECT params FROM jobs WHERE kind='extract' AND actor=? AND state IN ({','.join('?' * len(ACTIVE))})", (user, *ACTIVE)).fetchall()
    return any(job_account(_json(row["params"])) == account for row in rows)


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
            "receipts": row["receipts"], "checker": _json(row["checker"]), "hidden": bool(row["hidden"]),
            "instruction_id": row["instruction_id"] if "instruction_id" in row.keys() else None}


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
            chatgpt = _rows(conn, "SELECT * FROM accounts WHERE user=? AND provider='chatgpt'", (user,))
            login = codex_login(codex_home(user) / "auth.json") if user in USERS and chatgpt else None
            gpt = {"connected": bool(login), "connected_at": chatgpt[0]["connected_at"] if login else None,
                   "expires_at": login["expires_at"] if login else None, "last_refresh": login["last_refresh"] if login else None}
            job = _rows(conn, "SELECT * FROM jobs WHERE kind='connect_chatgpt' AND actor=? ORDER BY created_at DESC, rowid DESC LIMIT 1", (user,))
            gpt_connect = None
            if job and (job[0]["state"] != "completed" or (job[0]["ended_at"] or "") >= _minutes_ago(10)):
                shown = _json(job[0]["result"]) or {}
                gpt_connect = {"job_id": job[0]["id"], "state": job[0]["state"], "link": shown.get("link"), "code": shown.get("code"), "error": job[0]["error"]}
            accounts = {"claude": connected, "chatgpt": gpt["connected"]}
            engines = [{"id": ident, "label": engine["label"], "name": engine["name"], "account": engine["account"], "efforts": list(EFFORTS),
                        "default_effort": DEFAULT_EFFORT[ident], "experimental": engine["experimental"], "note": engine["note"], "connected": accounts[engine["account"]]}
                       for ident, engine in ENGINES.items()]
            return {"user": user, "claude": {"connected": connected, "connected_at": found[0]["connected_at"] if connected else None,
                                              "expires_at": found[0]["expires_at"] if connected else None, "plan_usage": plan}, "connect": connect,
                    "chatgpt": gpt, "chatgpt_connect": gpt_connect, "engines": engines}
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
                if active_jobs_on(conn, user, "claude"):
                    raise Conflict("your runs are still using this account; wait for them or cancel them first")
                token_path(user).unlink(missing_ok=True)
                conn.execute("DELETE FROM accounts WHERE user=? AND provider='claude'", (user,))
            else:
                raise WorkspaceError("unknown account action")
        self._transaction(run)
        return self.account(user)

    def chatgpt_action(self, user: str, request: dict[str, Any]) -> dict[str, Any]:
        if user not in USERS:
            raise WorkspaceError("unknown user")
        action = request.get("action") if isinstance(request, dict) else None

        def run(conn: sqlite3.Connection) -> None:
            if action == "connect":
                conn.execute("UPDATE jobs SET cancel_requested=1 WHERE kind='connect_chatgpt' AND actor=? AND state IN ('queued','waiting_for_approval')", (user,))
                conn.execute("INSERT INTO jobs (id, kind, slug, actor, created_at, state, params) VALUES (?, 'connect_chatgpt', NULL, ?, ?, 'queued', '{}')", (uuid.uuid4().hex, user, _now()))
            elif action == "cancel":
                job = conn.execute("SELECT * FROM jobs WHERE id=? AND kind='connect_chatgpt' AND actor=?", (request.get("job_id"), user)).fetchone()
                if job is None: raise Missing("unknown connect job")
                if job["state"] not in CHATGPT_CONNECT_ACTIVE: raise Conflict("connect is not in progress")
                conn.execute("UPDATE jobs SET cancel_requested=1 WHERE id=?", (job["id"],))
            elif action == "disconnect":
                if active_jobs_on(conn, user, "chatgpt"):
                    raise Conflict("your GPT runs are still using this account; wait for them or cancel them first")
                shutil.rmtree(codex_home(user), ignore_errors=True)
                conn.execute("DELETE FROM accounts WHERE user=? AND provider='chatgpt'", (user,))
            else:
                raise WorkspaceError("unknown account action")
        self._transaction(run)
        return self.account(user)

    # ---- jobs ------------------------------------------------------------------

    def jobs(self, slug: str) -> dict[str, Any]:
        self.workspace.item(slug)
        conn = self.workspace._connect()
        try:
            jobs = [job_json(row) for row in _rows(conn, "SELECT * FROM jobs WHERE slug=? AND kind='extract' ORDER BY created_at DESC, rowid DESC LIMIT 30", (slug,))]
        finally:
            if conn: conn.close()
        # Runs imported before the checker version was stored: read it from the version's receipt, never rewriting either.
        versions = None
        for job in jobs:
            checker = (job["result"] or {}).get("checker")
            if isinstance(checker, dict) and not checker.get("checker_version") and job["version_id"]:
                if versions is None:
                    versions = {version["id"]: version for version in imported_versions(self.workspace, slug)}
                recorded = self.workspace.import_check(slug, versions[job["version_id"]]) if job["version_id"] in versions else None
                if recorded:
                    job["result"]["checker"] = {**checker, "checker_version": recorded["checker_version"], "ledger_schema": recorded["ledger_schema"]}
        return {"jobs": jobs}

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
        instruction = None
        if action == "extract":
            # The run's instruction is frozen now: its text hash, whatever later happens to a draft.
            from cockpit.instructions import Instructions
            instruction = Instructions(self.workspace).resolve(request.get("instruction_id"))

        def run(conn: sqlite3.Connection) -> None:
            if action == "extract":
                if conn.execute("SELECT 1 FROM hidden_deals WHERE slug=?", (slug,)).fetchone(): raise Conflict("unhide the deal first")
                engine_id = request.get("engine", DEFAULT_ENGINE)
                if engine_id not in ENGINES: raise WorkspaceError("unknown engine")
                engine = ENGINES[engine_id]
                effort, minutes = request.get("effort", DEFAULT_EFFORT[engine_id]), request.get("timeout_minutes", 90)
                if effort not in EFFORTS: raise WorkspaceError("invalid effort")
                if type(minutes) is not int or not 10 <= minutes <= 360: raise WorkspaceError("time limit must be 10 to 360 minutes")
                if engine["account"] == "claude" and (not conn.execute("SELECT 1 FROM accounts WHERE user=? AND provider='claude'", (user,)).fetchone() or not token_path(user).is_file()):
                    raise Conflict("connect your Claude account in Settings first")
                if engine["account"] == "chatgpt" and (not conn.execute("SELECT 1 FROM accounts WHERE user=? AND provider='chatgpt'", (user,)).fetchone() or not (codex_home(user) / "auth.json").is_file()):
                    raise Conflict("connect your ChatGPT account in Settings first")
                params = {"engine": engine_id, "engine_label": engine["label"], "model": engine["model"], "provider": engine["provider"], "account": engine["account"],
                          "effort": effort, "timeout_minutes": minutes, "instruction": instruction}
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
