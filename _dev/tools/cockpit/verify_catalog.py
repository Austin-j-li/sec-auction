"""Read-only verification of pending catalog filings and imported run bases."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import os
from pathlib import Path
import sqlite3
import sys
import time

import openpyxl

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import check_lean
from cockpit import data
from cockpit import import_results as imp


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def database_rows(db_path: Path) -> tuple[dict[str, dict], dict[str, list[str]]]:
    """Each deal's latest revision and its imported version ids, through a read-only connection."""
    if not db_path.is_file():
        return {}, {}
    conn = sqlite3.connect(f"{db_path.as_uri()}?mode=ro", uri=True)
    try:
        def rows(sql: str) -> list[tuple]:
            try:
                return conn.execute(sql).fetchall()
            except sqlite3.OperationalError:  # a table no save or run has created yet
                return []
        latest = {slug: dict(revision=revision, base_id=base_id, base_sha256=base_sha256)
                  for slug, revision, base_id, base_sha256 in rows(
                      "SELECT slug, revision, base_id, base_sha256 FROM revisions ORDER BY slug, revision")}
        imported: dict[str, list[str]] = {}
        for slug, ident in rows("SELECT slug, id FROM versions ORDER BY started_at, id"):
            imported.setdefault(slug, []).append(ident)
        return latest, imported
    finally:
        conn.close()


def issues_from_payload(payload: dict) -> list[dict]:
    issues = list(payload["check"]["other_issues"])
    for sheet, key in (("Deal ledger", "ledger"), ("Rounds", "rounds"),
                       ("Questions", "questions")):
        for row in payload[key]["rows"]:
            issues.extend({**issue, "sheet": sheet, "row": row["excel_row"]}
                          for issue in row["issues"])
    return issues


def normalized_issues(issues: list[dict]) -> list[str]:
    keys = ("severity", "code", "column", "message", "sheet", "row")
    return sorted(json.dumps({key: issue.get(key) for key in keys},
                             sort_keys=True, ensure_ascii=False) for issue in issues)


def rows_in_book(source: Path | io.BytesIO) -> dict[str, int]:
    book = openpyxl.load_workbook(source, read_only=True)
    try:
        return {sheet: sum(1 for row in book[sheet].iter_rows(min_row=2, values_only=True)
                           if any(value is not None and str(value).strip() for value in row))
                for sheet in check_lean.SHEETS}
    finally:
        book.close()


def verify(root: Path) -> dict:
    started = time.monotonic()
    catalog = json.loads((root / "_dev/cockpit/catalog.json").read_text())
    if catalog.get("schema_version") != 1 or set(catalog.get("deals", {})) != set(imp.DEALS):
        raise RuntimeError("Catalog must contain exactly the filed deals")
    filings = imp.manifest(root)
    cockpit = data.Cockpit(root)
    if not cockpit.workspace.available:
        raise RuntimeError("Workspace did not activate")
    latest, imported = database_rows(cockpit.workspace.db_path)
    listed = set(cockpit.slugs())
    rows = {}
    for slug in imp.DEALS:
        began = time.monotonic()
        entry = catalog["deals"][slug]
        if entry.get("filing") != filings[slug]:
            raise RuntimeError(f"Catalog filing metadata differs from manifest: {slug}")
        if slug not in listed:
            raise RuntimeError(f"Deal is not listed: {slug}")
        versions = cockpit.workspace.item(slug).get("versions", [])
        pending = not versions
        if pending:
            if entry.get("default_base") or latest.get(slug) or entry.get("findings") or entry.get("documents"):
                raise RuntimeError(f"Pending catalog deal has old state: {slug}")
            payload = cockpit.deal(slug)
            summary = next(item for item in cockpit.list_deals() if item["slug"] == slug)
            if not payload.get("pending") or not summary.get("pending") or payload["workspace"]["base_version"] is not None:
                raise RuntimeError(f"Pending deal is not displayed as pending: {slug}")
            rows[slug] = dict(pending=True, filing=filings[slug]["file"], default_base=None, revision=0,
                              versions=[], check_summary=None, seconds=round(time.monotonic() - began, 3))
            continue
        for version in versions:
            path = cockpit.workspace._path(version["path"])
            if not path.is_file() or imp.sha256(path) != version["sha256"]:
                raise RuntimeError(f"Version workbook is missing or differs from its hash: {slug}/{version['id']}")
            if digest(cockpit.workspace.export(slug, version["id"])) != version["sha256"]:
                raise RuntimeError(f"Immutable export bytes differ: {slug}/{version['id']}")
        payload = cockpit.deal(slug)
        shown = payload["workspace"]
        base = cockpit.workspace.base(cockpit.workspace.item(slug))
        revision = latest.get(slug)
        expected = ((revision["revision"], revision["base_id"], revision["base_sha256"]) if revision
                    else (0, base["id"], base["sha256"]))
        if (shown["revision"], shown["base_version"], shown["base_sha256"]) != expected:
            raise RuntimeError(f"Working base differs from recorded revision: {slug}")
        api_ids = [v["id"] for v in payload["versions"]]
        if api_ids[:1] != ["working"] or not {v["id"] for v in versions} <= set(api_ids[1:]):
            raise RuntimeError(f"API version list differs: {slug}")
        working = cockpit.workspace.export(slug)
        export_counts = rows_in_book(io.BytesIO(working))
        shown_counts = {sheet: len(payload[key]["rows"]) for sheet, key in
                        (("Deal ledger", "ledger"), ("Rounds", "rounds"), ("Questions", "questions"))}
        shown_counts["Deal facts"] = len(payload["facts"])
        if export_counts != shown_counts:
            raise RuntimeError(f"Displayed row counts differ from export: {slug}")
        fresh = None
        if revision is None:
            base_path = cockpit.workspace._path(base["path"])
            if digest(working) != base["sha256"]:
                raise RuntimeError(f"Unedited working export differs: {slug}")
            filing_path = root / "raw_filing" / filings[slug]["file"]
            fresh = check_lean.LeanChecker(base_path, filing_path).run()
            if payload["check"]["summary"] != fresh["summary"]:
                raise RuntimeError(f"Displayed check summary differs: {slug}")
            if normalized_issues(issues_from_payload(payload)) != normalized_issues(fresh["issues"]):
                raise RuntimeError(f"Displayed checker findings differ: {slug}")
        rows[slug] = dict(pending=False, filing=filings[slug]["file"], default_base=base["id"],
                          edited=revision is not None, revision=shown["revision"], base_version=shown["base_version"],
                          base_sha256=shown["base_sha256"], path=base["path"], versions=api_ids,
                          counts=shown_counts, export_counts=export_counts, check_summary=payload["check"]["summary"],
                          fresh_check_summary=fresh["summary"] if fresh else None, sha256=base["sha256"],
                          findings=[f["id"] for f in payload["findings"]],
                          documents=[d["id"] for d in payload["documents"]],
                          seconds=round(time.monotonic() - began, 3))
    return dict(verified_at=dt.datetime.now(dt.timezone.utc).isoformat(),
                deals=rows, seconds=round(time.monotonic() - started, 3))


def write_new(path: Path, value: dict) -> None:
    """Write JSON to a new file, atomically; FileExistsError if the file exists."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        os.link(temporary, path)
    finally:
        temporary.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=imp.ROOT)
    parser.add_argument("--output", type=Path,
                        help="a new file (default: a timestamped file in the re-extraction packet)")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = args.output or root / "_dev/alignment_sprint" / f"catalog-verification-{stamp}.json"
    if output.exists():
        print(f"Refused: {output} exists; a verification never overwrites an earlier result", file=sys.stderr)
        return 2
    outcome = verify(root)
    try:
        write_new(output, outcome)
    except FileExistsError:
        print(f"Refused: {output} exists; a verification never overwrites an earlier result", file=sys.stderr)
        return 2
    print(f"Verified {len(outcome['deals'])} deals in {outcome['seconds']}s; wrote {output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"Verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
