#!/usr/bin/env python3
"""Turn a check_lean.py JSON report into the plain-text findings handed to a revision pass.

    python3 _dev/tools/findings_text.py report.json findings.md

Every finding in the report is listed, most serious first, each marked "certain"
(an exact rule) or "model judgment" (Jev, with its confidence). Nothing is added
from the grading notes or any other source.
"""
import json
import sys

ORDER = {"error": 0, "review": 1, "warning": 2, "information": 3}


def main(report_path, out_path):
    report = json.load(open(report_path, encoding="utf-8"))
    issues = sorted(report["issues"], key=lambda i: (ORDER.get(i.get("severity"), 9), i.get("basis") != "jev", -(i.get("confidence") or 0)))
    lines = ["# Checker findings", "", "%d finding(s). Numbered for reference in revision_notes.md." % len(issues), ""]
    for n, i in enumerate(issues, 1):
        where = i.get("sheet") or ""
        if i.get("row"):
            where += ", row %s" % i["row"]
        if i.get("column"):
            where += ", column %s" % i["column"]
        if i.get("basis") == "jev":
            basis = "model judgment, confidence %.2f" % i.get("confidence", 0)
        else:
            basis = "certain"
        lines.append("%d. [%s; %s] %s%s" % (n, i.get("severity"), basis, (where + ": ") if where else "", i["message"]))
    open(out_path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("%d findings written to %s" % (len(issues), out_path))


if __name__ == "__main__":
    main(*sys.argv[1:3])
