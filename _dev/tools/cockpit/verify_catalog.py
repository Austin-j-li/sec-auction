"""Read-only live integration check of the one-version nine-deal catalog."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
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


def state_files(root: Path) -> dict[str, str]:
    folder = root / "_dev/cockpit/state"
    return {str(path.relative_to(root)): imp.sha256(path)
            for path in folder.glob("*") if path.is_file()} if folder.exists() else {}


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


def rows_in_book(path: Path) -> dict[str, int]:
    book = openpyxl.load_workbook(path, read_only=True)
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
    before = state_files(root)
    cockpit = data.Cockpit(root)
    if not cockpit.workspace.available:
        raise RuntimeError("Workspace did not activate")
    rows = {}
    for slug in imp.DEALS:
        began = time.monotonic()
        item = catalog["deals"][slug]
        versions = {v["id"]: v for v in item["versions"]}
        if list(versions) != [imp.VERSION_ID] or item["default_base"] != imp.VERSION_ID:
            raise RuntimeError(f"Catalog is not the single current version: {slug}")
        if versions[imp.VERSION_ID]["path"] != f"extraction/{slug}.xlsx":
            raise RuntimeError(f"Current version path differs: {slug}")
        if any(record.get("source_version") is not None
               for record in item["findings"] + item["documents"]):
            raise RuntimeError(f"Review record is tied to a removed version: {slug}")
        payload = cockpit.deal(slug)
        if payload["workspace"]["base_version"] != item["default_base"]:
            raise RuntimeError(f"Wrong default base: {slug}")
        if payload["workspace"]["revision"] != 0:
            raise RuntimeError(f"Unexpected production revision: {slug}")
        api_ids = [v["id"] for v in payload["versions"]]
        if api_ids != ["working", *versions]:
            raise RuntimeError(f"API version list differs: {slug}")
        base = versions[item["default_base"]]
        base_path = root / base["path"]
        expected_counts = rows_in_book(base_path)
        shown_counts = {sheet: len(payload[key]["rows"]) for sheet, key in
                        (("Deal ledger", "ledger"), ("Rounds", "rounds"),
                         ("Questions", "questions"))}
        shown_counts["Deal facts"] = len(payload["facts"])
        if shown_counts != expected_counts:
            raise RuntimeError(f"Displayed row counts differ: {slug}")
        for ident, ver in versions.items():
            if digest(cockpit.workspace.export(slug, ident)) != ver["sha256"]:
                raise RuntimeError(f"Immutable export bytes differ: {slug}/{ident}")
        if digest(cockpit.workspace.export(slug)) != base["sha256"]:
            raise RuntimeError(f"Unedited working export differs: {slug}")
        filing = root / "raw_filing" / cockpit.manifest()[slug]["file"]
        fresh = check_lean.LeanChecker(base_path, filing).run()
        if payload["check"]["summary"] != fresh["summary"]:
            raise RuntimeError(f"Displayed check summary differs: {slug}")
        shown_issues = issues_from_payload(payload)
        if normalized_issues(shown_issues) != normalized_issues(fresh["issues"]):
            raise RuntimeError(f"Displayed checker findings differ: {slug}")
        rows[slug] = dict(default_base=item["default_base"],
                          versions=api_ids, counts=shown_counts,
                          check_summary=fresh["summary"],
                          checker_findings=len(fresh["issues"]),
                          sha256=base["sha256"],
                          findings=[f["id"] for f in payload["findings"]],
                          documents=[d["id"] for d in payload["documents"]],
                          seconds=round(time.monotonic() - began, 3))
    after = state_files(root)
    if before != after:
        raise RuntimeError("Production SQLite state files changed during read-only verification")
    return dict(verified_at=dt.datetime.now(dt.timezone.utc).isoformat(),
                deals=rows, production_state_before=before,
                production_state_after=after,
                production_state_unchanged=True,
                seconds=round(time.monotonic() - started, 3))


def main() -> None:
    root = imp.ROOT
    outcome = verify(root)
    output = root / imp.REEXTRACT / "catalog-verification.json"
    imp.atomic_json(output, outcome)
    print(f"Verified {len(outcome['deals'])} deals in {outcome['seconds']}s; no production state writes")


if __name__ == "__main__":
    main()
