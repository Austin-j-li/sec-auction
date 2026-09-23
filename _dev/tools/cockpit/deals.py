"""Deals added in the cockpit: seed search, EDGAR lookups and saved filings.

The server reads only the seed's identifying columns and never touches the network:
a lookup is a job the worker runs (`run_lookup`), which fetches the filing's complete
submission from EDGAR and caches it. Adding a deal cuts the chosen document from that
cached submission, byte for byte, into `_dev/cockpit/state/filings/<slug>/`.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import re
import shutil
import sqlite3
import uuid
from pathlib import Path
from typing import Any

import fetch_filing
import make_seed
from cockpit import data
from cockpit.workspace import Conflict, Missing, Workspace, WorkspaceError, _now

SCHEMA = (
    "CREATE TABLE IF NOT EXISTS added_deals (slug TEXT PRIMARY KEY, name TEXT NOT NULL, form_type TEXT NOT NULL, date_filed TEXT NOT NULL, file TEXT NOT NULL, source_kind TEXT NOT NULL, seed_deal TEXT, index_url TEXT, source_url TEXT NOT NULL, document TEXT NOT NULL, fetched_utc TEXT NOT NULL, bytes INTEGER NOT NULL, sha256 TEXT NOT NULL, added_by TEXT NOT NULL, added_at TEXT NOT NULL)",
)
SEED_COLUMNS = ("deal", "target_name", "form_type", "date_filed", "index_url", "status")
LOOKUP_TTL = dt.timedelta(hours=24)
FORMS = ("DEFM14A", "PREM14A", "SC TO-T")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
LOOKUP_ACTIVE = ("queued", "running")


def ensure_schema(conn: sqlite3.Connection) -> None:
    for statement in SCHEMA:
        conn.execute(statement)


def display_name(name: str) -> str:
    """"MAC-GRAY CORP" -> "Mac-Gray": the seed's slug rule's suffixes dropped, words capitalised."""
    words = (name or "").split()
    while len(words) > 1 and re.sub(r"[^A-Z0-9]", "", words[-1].upper()) in make_seed.SUFFIXES:
        words.pop()
    return " ".join("-".join(part[:1].upper() + part[1:].lower() for part in word.split("-")) for word in words).strip(" ,.")


def _old(stamp: str | None) -> bool:
    try:
        return dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(stamp or "") > LOOKUP_TTL
    except ValueError:
        return True


def lookup_json(row: sqlite3.Row) -> dict[str, Any]:
    params = json.loads(row["params"])
    return {"id": row["id"], "state": row["state"], "actor": row["actor"], "created_at": row["created_at"], "ended_at": row["ended_at"],
            "url": params.get("url"), "seed_deal": params.get("seed_deal"), "error": row["error"],
            "result": json.loads(row["result"]) if row["state"] == "completed" and row["result"] else None}


class Deals:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.root = workspace.root
        self.state = self.root / "_dev/cockpit/state"
        self._seed: tuple[tuple[int, int], list[dict[str, str]]] | None = None

    # ---- paths and reads -------------------------------------------------------

    def filing_path(self, row: dict[str, Any] | sqlite3.Row) -> Path:
        return self.state / "filings" / row["slug"] / row["file"]

    def lookup_path(self, job_id: str) -> Path:
        return self.state / "lookups" / f"{job_id}.txt"

    def added(self, slug: str | None = None) -> list[dict[str, Any]]:
        """Added deals, oldest first (or the one named). Reads never create the database."""
        conn = self.workspace._connect()
        if conn is None:
            return []
        try:
            query, params = ("SELECT * FROM added_deals WHERE slug=?", (slug,)) if slug else ("SELECT * FROM added_deals ORDER BY added_at, slug", ())
            try:
                return [dict(row) for row in conn.execute(query, params)]
            except sqlite3.OperationalError:
                return []
        finally:
            conn.close()

    def in_use(self, slug: str) -> bool:
        return slug in self.workspace.catalog()["deals"] or bool(self.added(slug))

    def seed(self) -> list[dict[str, str]]:
        """The seed's identifying columns only; nothing else under ref/ is read."""
        path = self.root / "ref/seed.csv"
        try:
            stat = path.stat()
        except OSError:
            return []
        key = (stat.st_mtime_ns, stat.st_size)
        if self._seed is None or self._seed[0] != key:
            with path.open(newline="", encoding="utf-8") as handle:
                rows = [{column: (row.get(column) or "").strip() for column in SEED_COLUMNS} for row in csv.DictReader(handle)]
            self._seed = (key, rows)
        return self._seed[1]

    def seed_search(self, text: str) -> dict[str, Any]:
        needle = (text or "").strip().lower()
        if not needle:
            return {"rows": []}
        rows = [row for row in self.seed() if needle in row["deal"] or needle in row["target_name"].lower()][:25]
        return {"rows": [{**row, "in_cockpit": self.in_use(row["deal"])} for row in rows]}

    # ---- lookups ---------------------------------------------------------------

    def lookup(self, job_id: str) -> dict[str, Any]:
        conn = self.workspace._connect()
        try:
            row = conn.execute("SELECT * FROM jobs WHERE id=? AND kind='lookup'", (job_id,)).fetchone() if conn else None
        finally:
            if conn: conn.close()
        if row is None:
            raise Missing("unknown lookup")
        return lookup_json(row)

    def request(self, user: str, body: dict[str, Any]) -> dict[str, Any]:
        action = body.get("action") if isinstance(body, dict) else None
        if action == "lookup":
            return {"lookup": self.start_lookup(user, body)}
        if action == "add":
            return self.add(user, body)
        raise WorkspaceError("unknown deal action")

    def start_lookup(self, user: str, body: dict[str, Any]) -> dict[str, Any]:
        url, seed_deal = body.get("url"), body.get("seed_deal")
        if not isinstance(url, str) or len(url) > 500:
            raise WorkspaceError("a filing link is required")
        try:
            submission, document = fetch_filing.submission_link(url)
        except fetch_filing.FetchError as exc:
            raise WorkspaceError(str(exc)) from exc
        if seed_deal is not None and not any(row["deal"] == seed_deal for row in self.seed()):
            raise WorkspaceError("unknown seed row")
        ident = uuid.uuid4().hex
        params = {"url": url.strip(), "submission_url": submission, "document": document, "seed_deal": seed_deal}
        conn = self.workspace._connect(write=True)
        try:
            conn.execute("INSERT INTO jobs (id, kind, slug, actor, created_at, state, params) VALUES (?, 'lookup', NULL, ?, ?, 'queued', ?)",
                         (ident, user, _now(), json.dumps(params)))
            conn.commit()
        finally:
            conn.close()
        return self.lookup(ident)

    def run_lookup(self, job: sqlite3.Row) -> dict[str, Any]:
        """Worker side: fetch the submission, cache it, and describe its documents. Raises FetchError."""
        params = json.loads(job["params"])
        submission = fetch_filing.get(params["submission_url"])
        path = self.lookup_path(job["id"])
        path.parent.mkdir(parents=True, exist_ok=True)
        fetch_filing.atomic_write(path, submission)
        parsed = fetch_filing.parse_submission(submission)
        documents = parsed["documents"]
        if not documents:
            raise fetch_filing.FetchError("the submission has no documents")
        seed = next((row for row in self.seed() if row["deal"] == params.get("seed_deal")), None)
        warnings = []
        if seed:
            form, date, name, slug = seed["form_type"], seed["date_filed"], display_name(seed["target_name"]), seed["deal"]
            if seed["status"] != "ok":
                warnings.append(f"The seed marks this deal for review ({seed['status'].removeprefix('review: ')}); choose the document yourself.")
            if parsed["form_type"] and parsed["form_type"] != form:
                warnings.append(f"The seed says {form}, but EDGAR files this as {parsed['form_type']}.")
            if parsed["date_filed"] and parsed["date_filed"] != date:
                warnings.append(f"The seed says filed {date}, but EDGAR says {parsed['date_filed']}.")
        else:
            form, date = parsed["form_type"], parsed["date_filed"]
            name = display_name(parsed["subject_company"] or parsed["filer"])
            slug = make_seed.slug(name.upper()) if name else ""
            if slug and self.in_use(slug):
                slug = f"{slug}-{date[:4]}"
        if form not in FORMS:
            warnings.append(f"This is a {form or 'filing of unknown form'}; the instruction was written for DEFM14A, PREM14A and SC TO-T filings.")
        hinted = params.get("document")
        if hinted and not any(d["filename"] == hinted and d["html"] for d in documents):
            warnings.append(f"The linked document {hinted} is not an HTML document of this filing.")
            hinted = None
        preselected = hinted or (fetch_filing.default_document(documents, form) if not seed or seed["status"] == "ok" else None)
        index = params["submission_url"][:-len(".txt")] + "-index.htm"
        return {"form_type": form, "date_filed": date, "header": {key: parsed[key] for key in ("form_type", "date_filed", "subject_company", "filer")},
                "documents": documents, "preselected": preselected, "suggested": {"slug": slug, "name": name},
                "source_url": params["submission_url"], "index_url": index, "seed": seed, "warnings": warnings,
                "sha256": hashlib.sha256(submission).hexdigest(), "bytes": len(submission)}

    def prune_lookups(self) -> None:
        folder = self.state / "lookups"
        if not folder.is_dir():
            return
        for path in folder.glob("*.txt"):
            if _old(dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc).isoformat()):
                path.unlink(missing_ok=True)

    # ---- adding ----------------------------------------------------------------

    def add(self, user: str, body: dict[str, Any]) -> dict[str, Any]:
        found = self.lookup(body.get("lookup_id") if isinstance(body.get("lookup_id"), str) else "")
        result = found["result"]
        if found["state"] != "completed" or not result:
            raise Conflict("the lookup has not finished")
        if _old(found["ended_at"]):
            raise Conflict("this lookup is more than a day old; look the filing up again")
        cache = self.lookup_path(found["id"])
        submission = cache.read_bytes() if cache.is_file() else b""
        if hashlib.sha256(submission).hexdigest() != result["sha256"]:
            raise Conflict("the fetched filing is no longer available; look it up again")
        document = body.get("document")
        if not any(d["filename"] == document and d["html"] for d in result["documents"]):
            raise WorkspaceError("choose one of the filing's HTML documents")
        slug, name = body.get("slug"), body.get("name")
        if not isinstance(slug, str) or not data.SLUG_RE.fullmatch(slug) or len(slug) > 60:
            raise WorkspaceError("the short name may use lower-case letters, digits and hyphens")
        if not isinstance(name, str) or not name.strip() or len(name.strip()) > 120 or any(ord(c) < 32 for c in name):
            raise WorkspaceError("the deal name must be 1 to 120 characters")
        form, date = result["form_type"], result["date_filed"]
        if not form or not DATE_RE.fullmatch(date or ""):
            raise WorkspaceError("the filing's form or date could not be read")
        try:
            content = fetch_filing.document_bytes(submission, document)
        except fetch_filing.FetchError as exc:
            raise WorkspaceError(str(exc)) from exc
        seed = result.get("seed")
        row = {"slug": slug, "name": name.strip(), "form_type": form, "date_filed": date,
               "file": f"{slug}_{date}_{re.sub(r'[^A-Za-z0-9-]', '', form.replace('/', '-'))}.htm", "source_kind": "seed" if seed else "link",
               "seed_deal": seed["deal"] if seed else None, "index_url": result["index_url"], "source_url": result["source_url"],
               "document": document, "fetched_utc": (found["ended_at"] or _now()), "bytes": len(content),
               "sha256": hashlib.sha256(content).hexdigest(), "added_by": user, "added_at": _now()}
        path = self.filing_path(row)
        conn = self.workspace._connect(write=True)
        created = False
        try:
            conn.execute("BEGIN IMMEDIATE")
            if slug in self.workspace.catalog()["deals"] or conn.execute("SELECT 1 FROM added_deals WHERE slug=?", (slug,)).fetchone():
                raise Conflict(f"a deal named {slug} is already in the cockpit")
            if path.parent.exists():
                raise Conflict(f"a filing folder for {slug} already exists")
            path.parent.mkdir(parents=True)
            created = True
            fetch_filing.atomic_write(path, content)
            conn.execute(f"INSERT INTO added_deals ({', '.join(row)}) VALUES ({', '.join('?' * len(row))})", tuple(row.values()))
            from cockpit import trace
            source = f"the seed ({seed['deal']})" if seed else "a pasted link"
            trace._activity(conn, slug, user, "deal_added", summary=f"Added {row['name']} ({form}, filed {date}) from {source}", at=row["added_at"])
            conn.commit()
        except Exception:
            conn.rollback()
            if created:
                shutil.rmtree(path.parent, ignore_errors=True)
            raise
        finally:
            conn.close()
        return {"slug": slug}
