#!/usr/bin/env python3
"""Show what changed between two ledger workbooks, sheet by sheet.

    python3 _dev/tools/diff_workbooks.py before.xlsx after.xlsx

Rows are matched in order (difflib), so an inserted row shows as one added row,
not as every later row changing. For a changed row only the changed cells are
printed, under the column heading from the sheet's first row.
"""
import difflib
import sys

import openpyxl


def rows(ws):
    return [tuple("" if c is None else str(c) for c in r) for r in ws.iter_rows(values_only=True)]


def clip(text, n=160):
    text = text.replace("\n", " ")
    return text if len(text) <= n else text[:n] + "..."


def main(before, after):
    a_wb, b_wb = openpyxl.load_workbook(before), openpyxl.load_workbook(after)
    total = 0
    for name in dict.fromkeys(a_wb.sheetnames + b_wb.sheetnames):
        if name not in a_wb.sheetnames or name not in b_wb.sheetnames:
            print("## %s: sheet %s" % (name, "added" if name in b_wb.sheetnames else "removed"))
            total += 1
            continue
        a, b = rows(a_wb[name]), rows(b_wb[name])
        head = a[0] if a else ()
        out = []
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
            if op == "equal":
                continue
            if op == "replace" and i2 - i1 == j2 - j1:
                for i, j in zip(range(i1, i2), range(j1, j2)):
                    for k, (x, y) in enumerate(zip(a[i], b[j])):
                        if x != y:
                            col = head[k] if k < len(head) and head[k] else "col %d" % (k + 1)
                            out.append("  row %d -> %d, %s:\n      was: %s\n      now: %s" % (i + 1, j + 1, col, clip(x), clip(y)))
                continue
            for i in range(i1, i2):
                out.append("  removed row %d: %s" % (i + 1, clip(" | ".join(v for v in a[i] if v), 300)))
            for j in range(j1, j2):
                out.append("  added row %d: %s" % (j + 1, clip(" | ".join(v for v in b[j] if v), 300)))
        print("## %s: %s" % (name, "no change" if not out else "%d change(s)" % len(out)))
        print("\n".join(out)) if out else None
        total += len(out)
    print("\nTotal: %d change(s)" % total)


if __name__ == "__main__":
    main(*sys.argv[1:3])
