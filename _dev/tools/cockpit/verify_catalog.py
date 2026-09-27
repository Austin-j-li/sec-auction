"""Read-only integration check of the nine-deal catalog and its working copies.

For every catalog deal: each catalog version's file exists and matches its SHA-256;
the deal is listed and its working copy renders at its latest revision, on the base
that revision records; the version list starts with the working copy and holds every
catalog and imported version; and an unedited working copy exports its base's bytes
and shows a fresh check of the base. The result goes to a new timestamped file; an
existing result is never overwritten.
"""

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
                for sheet in imp.SHEETS}
    finally:
        book.close()


def verify(root: Path) -> dict:
    started = time.monotonic()
    catalog = json.loads((root / "_dev/cockpit/catalog.json").read_text())
    if set(catalog["deals"]) != set(imp.DEALS):
        raise RuntimeError("Catalog does not have exactly nine deals")
    cockpit = data.Cockpit(root)
    if not cockpit.workspace.available:
        raise RuntimeError("Workspace did not activate")
    latest, imported = database_rows(cockpit.workspace.db_path)
    listed = cockpit.slugs()
    rows = {}
    for slug in imp.DEALS:
        began = time.monotonic()
        item = catalog["deals"][slug]
        versions = {v["id"]: v for v in item["versions"]}
        if list(versions) != [imp.VERSION_ID] or item["default_base"] != imp.VERSION_ID:
            raise RuntimeError(f"Catalog is not the single current version: {slug}")
        if any(record.get("source_version") is not None
               for record in item["findings"] + item["documents"]):
            raise RuntimeError(f"Review record is tied to a removed version: {slug}")
        for ident, ver in versions.items():
            path = root / ver["path"]
            if not path.is_file() or imp.sha256(path) != ver["sha256"]:
                raise RuntimeError(f"Catalog workbook is missing or differs from its hash: {slug}/{ident}")
            if digest(cockpit.workspace.export(slug, ident)) != ver["sha256"]:
                raise RuntimeError(f"Immutable export bytes differ: {slug}/{ident}")
        if slug not in listed:
            raise RuntimeError(f"Deal is not listed: {slug}")
        payload = cockpit.deal(slug)
        revision = latest.get(slug)
        base = versions[item["default_base"]]
        expected = ((revision["revision"], revision["base_id"], revision["base_sha256"]) if revision
                    else (0, base["id"], base["sha256"]))
        shown = payload["workspace"]
        if (shown["revision"], shown["base_version"], shown["base_sha256"]) != expected:
            raise RuntimeError(f"Working copy is not at its latest revision and recorded base: {slug}")
        api_ids = [v["id"] for v in payload["versions"]]
        if api_ids[:1] != ["working"] or not {*versions, *imported.get(slug, [])} <= set(api_ids[1:]):
            raise RuntimeError(f"API version list differs: {slug}")
        working = cockpit.workspace.export(slug)
        exported_counts = rows_in_book(io.BytesIO(working))
        shown_counts = {sheet: len(payload[key]["rows"]) for sheet, key in
                        (("Deal ledger", "ledger"), ("Rounds", "rounds"),
                         ("Questions", "questions"))}
        shown_counts["Deal facts"] = len(payload["facts"])
        fresh = None
        if revision is None:  # unedited: the working copy is the base itself
            base_path = root / base["path"]
            if shown_counts != rows_in_book(base_path):
                raise RuntimeError(f"Displayed row counts differ: {slug}")
            if digest(working) != base["sha256"]:
                raise RuntimeError(f"Unedited working export differs: {slug}")
            filing = root / "raw_filing" / cockpit.manifest()[slug]["file"]
            fresh = check_lean.LeanChecker(base_path, filing).run()
            if payload["check"]["summary"] != fresh["summary"]:
                raise RuntimeError(f"Displayed check summary differs: {slug}")
            if normalized_issues(issues_from_payload(payload)) != normalized_issues(fresh["issues"]):
                raise RuntimeError(f"Displayed checker findings differ: {slug}")
        rows[slug] = dict(default_base=item["default_base"], edited=revision is not None,
                          revision=shown["revision"], base_version=shown["base_version"],
                          base_sha256=shown["base_sha256"], path=base["path"],
                          versions=api_ids, counts=shown_counts, export_counts=exported_counts,
                          check_summary=payload["check"]["summary"],
                          fresh_check_summary=fresh["summary"] if fresh else None,
                          sha256=base["sha256"],
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
    output = args.output or root / imp.REEXTRACT / f"catalog-verification-{stamp}.json"
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
