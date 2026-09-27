#!/usr/bin/env python3
"""Re-check the 15 v1.14 trial workbooks with a checker tree and compare with their stored check.json.

Read-only on the trial packet. Usage:
    python3 recheck_trial.py --tools ~/work/Projects/sec-extraction-v114/_dev/tools --rules v1.14 --output result.json
"""
import argparse, json, sys
from pathlib import Path

MAIN = Path(__file__).resolve().parents[4]
TRIAL = MAIN / "_dev/reviews/2026-09-26-v114-15-run-trial/runs"

def key(issue):
    return (issue["severity"], issue["code"], issue.get("sheet"), issue.get("row"), issue.get("column"), issue["message"])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tools", required=True, type=Path)
    ap.add_argument("--rules", default=None)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    sys.path.insert(0, str(args.tools))
    import check_lean
    results, same = [], 0
    for run in sorted(p for p in TRIAL.iterdir() if (p / "check.json").is_file()):
        stored = json.loads((run / "check.json").read_text())
        workbook = next(run.glob("*.xlsx"))
        filing = MAIN / "raw_filing" / Path(stored["filing"]).name
        report = check_lean.LeanChecker(workbook, filing, rules=args.rules).run()
        old, new = sorted(map(key, stored["issues"])), sorted(map(key, report["issues"]))
        match = old == new and stored["status"] == report["status"]
        same += match
        results.append({"run": run.name, "stored": stored["summary"], "stored_schema": stored["ledger_schema"],
                        "now": report["summary"], "now_schema": report["ledger_schema"], "checker_version": report["checker_version"],
                        "identical_issues": match, "only_stored": [list(k) for k in old if k not in new],
                        "only_now": [list(k) for k in new if k not in old]})
    args.output.write_text(json.dumps({"rules": args.rules, "identical": same, "runs": len(results), "results": results}, indent=2) + "\n")
    print(f"{same}/{len(results)} identical under rules={args.rules}")
    return 0 if same == len(results) else 1

if __name__ == "__main__":
    raise SystemExit(main())
