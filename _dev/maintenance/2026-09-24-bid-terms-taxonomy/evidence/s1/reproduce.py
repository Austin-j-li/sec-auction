#!/usr/bin/env python3
"""Reproduce stored checker results with two versions of check_lean.py.

Usage:
    python3 reproduce.py --inputs DIR --before CHECKER --after CHECKER --output FILE

DIR holds copies of the inputs, never the live files:
    extraction/<deal>.xlsx                     the extraction/ workbooks
    receipts/<deal>/{check.json,metadata.json} their stored results
    versions/<deal>/<id>/{<deal>.xlsx,check.json,metadata.json}  cockpit run versions
    filings/<filing_name>                      each filing named in a metadata.json

Both checkers run in-process on each workbook. Each result is compared with the stored
check.json on the issue multiset, summary and status. Nothing in DIR is written, and an
existing FILE is never overwritten.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path

FIELDS = ("severity", "code", "sheet", "row", "column", "message")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def key(issue: dict) -> tuple:
    return tuple(issue.get(field) for field in FIELDS)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def delta(before: list[dict], after: list[dict]) -> dict:
    b, a = Counter(map(key, before)), Counter(map(key, after))
    return {
        "added": [dict(zip(FIELDS, item)) for item in sorted((a - b).elements(), key=repr)],
        "removed": [dict(zip(FIELDS, item)) for item in sorted((b - a).elements(), key=repr)],
    }


def same(report: dict, stored: dict) -> bool:
    return (Counter(map(key, report["issues"])) == Counter(map(key, stored["issues"]))
            and report["summary"] == stored["summary"] and report["status"] == stored["status"])


def cases(inputs: Path) -> list[dict]:
    out = []
    for workbook in sorted((inputs / "extraction").glob("*.xlsx")):
        receipt = inputs / "receipts" / workbook.stem
        out.append({"group": "extraction", "id": workbook.stem, "workbook": workbook,
                    "stored": receipt / "check.json", "meta": json.loads((receipt / "metadata.json").read_text())})
    for folder in sorted((inputs / "versions").glob("*/*")):
        out.append({"group": "version", "id": f"{folder.parent.name}/{folder.name}",
                    "workbook": next(folder.glob("*.xlsx")), "stored": folder / "check.json",
                    "meta": json.loads((folder / "metadata.json").read_text())})
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--inputs", required=True, type=Path, help="Folder of copied inputs (layout above)")
    parser.add_argument("--before", required=True, type=Path, help="Earlier check_lean.py")
    parser.add_argument("--after", required=True, type=Path, help="New check_lean.py")
    parser.add_argument("--output", required=True, type=Path, help="JSON result; must not exist yet")
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f"{args.output} exists; choose a new output path")
    if not args.output.parent.is_dir():
        parser.error(f"{args.output.parent} is not a folder")
    found = cases(args.inputs)
    if not found:
        parser.error(f"no workbooks under {args.inputs}")

    before_checker, after_checker = load("check_lean_before", args.before), load("check_lean_after", args.after)
    results = []
    for case in found:
        filing = args.inputs / "filings" / case["meta"]["filing_name"]
        assert sha(filing) == case["meta"]["filing_sha256"], filing
        stored = json.loads(case["stored"].read_text())
        before = before_checker.LeanChecker(case["workbook"], filing).run()
        after = after_checker.LeanChecker(case["workbook"], filing).run()
        row = {
            "group": case["group"],
            "id": case["id"],
            "workbook_sha256": sha(case["workbook"]),
            "filing": case["meta"]["filing_name"],
            "instruction_sha256": case["meta"].get("instruction_sha256"),
            "ledger_schema": after["ledger_schema"],
            "ledger_schema_helper": after_checker.ledger_schema(case["workbook"]),
            "stored": {"checker_version": stored.get("checker_version"), "status": stored["status"],
                       "summary": stored["summary"]},
            "before": {"status": before["status"], "summary": before["summary"], "identical_to_stored": same(before, stored)},
            "after": {"status": after["status"], "summary": after["summary"], "identical_to_stored": same(after, stored)},
            "delta_after_vs_stored": delta(stored["issues"], after["issues"]),
            "delta_after_vs_before": delta(before["issues"], after["issues"]),
        }
        results.append(row)
        d = row["delta_after_vs_stored"]
        print(f"{row['id']:55} {row['ledger_schema']:8} stored {stored['summary']['errors']}e/{stored['summary']['warnings']}w "
              f"before same={row['before']['identical_to_stored']} after same={row['after']['identical_to_stored']} "
              f"+{dict(Counter(i['code'] for i in d['added']))} -{dict(Counter(i['code'] for i in d['removed']))}")

    with args.output.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps({
            "checker_before": {"version": before_checker.CHECKER_VERSION, "path": str(args.before), "sha256": sha(args.before)},
            "checker_after": {"version": after_checker.CHECKER_VERSION, "path": str(args.after), "sha256": sha(args.after)},
            "inputs": str(args.inputs),
            "compared_fields": list(FIELDS),
            "ignored_fields": ["checker_version", "checker_revision", "ledger_schema", "workbook", "filing", "basis"],
            "results": results,
        }, indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
