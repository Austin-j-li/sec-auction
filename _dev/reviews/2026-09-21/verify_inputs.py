#!/usr/bin/env python3
"""Verify review provenance and reuse checks only for byte-identical workbooks."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SCRATCH = Path("/tmp/sec-extraction-review-20260921")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads((SCRATCH / "manifest.json").read_text())
    changed = [name for name, info in manifest["sources"].items() if digest(ROOT / name) != info["sha256"]]
    if changed:
        raise SystemExit(f"Review inputs changed: {changed}")
    checks = []
    for deal, sheets in manifest["workbooks"].items():
        run = ROOT / "_dev/runs" / f"v1.11_{deal}"
        validation = json.loads((run / "validation.json").read_text())
        check = json.loads((run / "check.json").read_text())
        status = json.loads((run / "status.json").read_text())
        source_hash = manifest["sources"][f"extraction/{deal}.xlsx"]["sha256"]
        if source_hash != validation["sha256"] or source_hash != digest(run / "extraction" / f"{deal}.xlsx"):
            raise SystemExit(f"Stored checker workbook differs: {deal}")
        checks.append({
            "deal": deal,
            "ledger_events": sheets["Deal ledger"] - 1,
            "rounds": sheets["Rounds"] - 1,
            "questions": sheets["Questions"] - 1,
            "workbook_sha256": source_hash,
            "original_run_completed": status["state"] == "completed" and status["exit_code"] == 0,
            "checker_status": check["status"],
            "checker_version": check["checker_version"],
            "errors": check["summary"]["errors"],
            "warnings": check["summary"]["warnings"],
            "warning_codes": sorted({issue["code"] for issue in check["issues"]}),
        })
    result = {
        "input_files_unchanged": True,
        "mechanical_reports_reused_for_identical_workbooks": True,
        "mechanical_scope": "Structure and quotation occurrence only; not substantive truth or completeness.",
        "totals": {key: sum(row[key] for row in checks) for key in ["ledger_events", "rounds", "questions", "errors", "warnings"]},
        "cases": checks,
        "sources": manifest["sources"],
    }
    (OUT / "input_verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key not in {"cases", "sources"}}, indent=2))


if __name__ == "__main__":
    main()
