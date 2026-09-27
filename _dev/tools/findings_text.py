#!/usr/bin/env python3
"""Turn a check_lean.py JSON report into the plain-text findings handed to a revision pass.

    python3 _dev/tools/findings_text.py report.json findings.md

Every finding is listed, errors first. Warnings remain review leads, not
certain errors. Nothing is added from grading notes or other sources.
"""
import json
import sys

ORDER = {"error": 0, "warning": 1, "review": 2, "info": 3, "information": 3}


def main(report_path, out_path):
    with open(report_path, encoding="utf-8") as handle:
        report = json.load(handle)
    issues = sorted(report["issues"], key=lambda i: ORDER.get(i.get("severity"), 9))
    checker = "Checker %s" % report["checker_version"] if report.get("checker_version") else "Checker version not recorded"
    rules = "%s ledger rules" % report["ledger_schema"] if report.get("ledger_schema") else "ledger rules not recorded"
    lines = ["# Checker findings (%s; %s)" % (checker, rules), "",
             "%d finding(s). Numbered for reference in revision_notes.md." % len(issues), ""]
    for n, i in enumerate(issues, 1):
        where = i.get("sheet") or ""
        if i.get("row"):
            where += ", row %s" % i["row"]
        if i.get("column"):
            where += ", column %s" % i["column"]
        basis = "mechanical error" if i.get("severity") == "error" else "mechanical review lead"
        lines.append("%d. [%s; %s] %s%s" % (n, i.get("severity"), basis, (where + ": ") if where else "", i["message"]))
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print("%d findings written to %s" % (len(issues), out_path))


if __name__ == "__main__":
    main(*sys.argv[1:3])
