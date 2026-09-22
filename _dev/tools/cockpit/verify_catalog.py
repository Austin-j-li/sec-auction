"""Read-only live integration check of the completed nine-deal catalog."""

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
    for slug in imp.NEW_DEALS:
        item = catalog["deals"][slug]
        if item["findings"] or item["documents"]:
            raise RuntimeError(f"Fresh draft has imported prior review material: {slug}")
    if "2026-09-21-three-models" in json.dumps(catalog):
        raise RuntimeError("Catalog still references the retired comparison")
    before = state_files(root)
    cockpit = data.Cockpit(root)
    if not cockpit.workspace.available:
        raise RuntimeError("Workspace did not activate")
    rows = {}
    for slug in imp.DEALS:
        began = time.monotonic()
        item = catalog["deals"][slug]
        versions = {v["id"]: v for v in item["versions"]}
        required = {"v1132-raw"} if slug == "datalink" else {"v1132-raw", "v113-baseline"}
        if not required.issubset(versions) or item["default_base"] not in versions:
            raise RuntimeError(f"Version list incomplete: {slug}")
        payload = cockpit.deal(slug)
        if payload["workspace"]["base_version"] != item["default_base"]:
            raise RuntimeError(f"Wrong default base: {slug}")
        if payload["workspace"]["revision"] != 0:
            raise RuntimeError(f"Unexpected production revision: {slug}")
        api_ids = [v["id"] for v in payload["versions"]]
        if api_ids != ["working", *versions]:
            raise RuntimeError(f"API version list differs: {slug}")
        if slug == "mac-gray":
            r01 = [f for f in payload["findings"] if f["id"] == "mac-gray-r01"]
            docs = {d["id"] for d in payload["documents"]}
            if (item["default_base"] != "mac-gray-candidate"
                    or "mac-gray-verified" not in versions
                    or len(r01) != 1 or r01[0]["source_version"] != "mac-gray-candidate"
                    or r01[0]["judgment"] != "unreviewed"
                    or r01[0]["implementation"] != "unassessed"
                    or "recorded_correction" in r01[0]
                    or not {"mac-gray-acceptance", "mac-gray-r01", "mac-gray-analytical-use",
                            "mac-gray-filing-coverage"}.issubset(docs)):
                raise RuntimeError("Mac-Gray candidate or pending R01 record differs")
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
                          raw_sha256=versions["v1132-raw"]["sha256"],
                          pending_r01=(slug == "mac-gray"),
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
    output = root / imp.REVIEW / "catalog-verification.json"
    imp.atomic_json(output, outcome)
    print(f"Verified {len(outcome['deals'])} deals in {outcome['seconds']}s; no production state writes")


if __name__ == "__main__":
    main()
