#!/usr/bin/env python3
"""Show what changed between two v0 ledger workbooks, sheet by sheet.

    python3 _dev/tools/diff_workbooks.py before.xlsx after.xlsx [--by-quote] [--include-source]

Rows are matched in order (difflib), so an inserted row shows as one added row,
not as every later row changing. For a changed row only the changed cells are
printed, under the column heading from the sheet's first row.
"""
import argparse
from collections import Counter
import sys

import openpyxl


def rows(ws):
    return [
        tuple(("blank", "") if c.value is None else (c.data_type, c.value) for c in row)
        for row in ws.iter_rows()
    ]


def display(cell):
    kind, value = cell
    label = {"n": "number", "s": "text", "d": "date", "b": "boolean", "f": "formula"}.get(kind, kind)
    return f"{value} [{label}]" if kind != "blank" else "[blank]"


def clip(text, n=160):
    text = text.replace("\n", " ")
    return text if len(text) <= n else text[:n] + "..."


KEYS = {"Deal ledger": ("Event", "Who", "Sort date"), "Rounds": ("Process", "Round"),
        "Questions": ("Q",), "Deal facts": ("Field",)}


def records(ws, by_quote=False):
    table = rows(ws)
    if not table:
        return [], {}
    headings = [cell[1] for cell in table[0]]
    counts = Counter()
    result = {}
    for index, cells in enumerate(table[1:], 2):
        if not any(cell[0] != "blank" for cell in cells):
            continue
        record = dict(zip(headings, cells))
        fields = KEYS.get(ws.title)
        key = tuple(record[field][1] for field in fields) if fields and all(field in record for field in fields) else (index,)
        counts[key] += 1
        result[(key, counts[key])] = (index, record)
    return headings, result


def quote_matches(a, b, pairs):
    """Pair leftover ledger rows by a unique quoted passage, then unique containment."""
    unused_a = [key for key in a if key not in pairs]
    unused_b = [key for key in b if key not in pairs.values()]

    def passage(record):
        cell = record.get("Quote and page", ("blank", ""))
        return " ".join(str(cell[1]).split()) if cell[0] != "blank" else ""

    quotes_a = {key: passage(a[key][1]) for key in unused_a}
    quotes_b = {key: passage(b[key][1]) for key in unused_b}
    counts_a, counts_b = Counter(quotes_a.values()), Counter(quotes_b.values())
    for key, quote in quotes_a.items():
        if quote and counts_a[quote] == counts_b[quote] == 1:
            pairs[key] = next(other for other, value in quotes_b.items() if value == quote)

    unused_a = [key for key in unused_a if key not in pairs]
    unused_b = [key for key in unused_b if key not in pairs.values()]
    candidates = {key: [other for other in unused_b if quotes_a[key] and quotes_b[other]
                        and len(min(quotes_a[key], quotes_b[other], key=len)) >= 20
                        and (quotes_a[key] in quotes_b[other] or quotes_b[other] in quotes_a[key])]
                  for key in unused_a}
    claimed = Counter(other for found in candidates.values() for other in found)
    pairs.update((key, found[0]) for key, found in candidates.items()
                 if len(found) == 1 and claimed[found[0]] == 1)


def compare_sheet(a_ws, b_ws, by_quote=False):
    a_head, a = records(a_ws)
    b_head, b = records(b_ws)
    out = []
    added = [column for column in b_head if column not in a_head]
    removed = [column for column in a_head if column not in b_head]
    if added:
        out.append("  added column(s): " + ", ".join(display(("s", column)) for column in added))
    if removed:
        out.append("  removed column(s): " + ", ".join(removed))
    pairs = {key: key for key in a if key in b}
    if by_quote and a_ws.title == "Deal ledger":
        quote_matches(a, b, pairs)
    for key in a:
        if key not in pairs:
            index, record = a[key]
            out.append(f"  removed row {index}: " + clip(" | ".join(
                f"{column}={display(cell)}" for column, cell in record.items() if cell[0] != "blank"), 300))
            continue
        i, old = a[key]
        j, new = b[pairs[key]]
        for column in dict.fromkeys([*a_head, *b_head]):
            x = old.get(column, ("blank", ""))
            y = new.get(column, ("blank", ""))
            if column not in old and y[0] == "blank" or column not in new and x[0] == "blank":
                continue
            if x == y:
                continue
            out.append(f"  row {i} -> {j}, {column}:\n      was: {clip(display(x))}\n      now: {clip(display(y))}")
    for key in b:
        if key not in pairs.values():
            index, record = b[key]
            out.append(f"  added row {index}: " + clip(" | ".join(
                f"{column}={display(cell)}" for column, cell in record.items() if cell[0] != "blank"), 300))
    return out


def main(before, after, include_source=False, by_quote=False):
    a_wb, b_wb = openpyxl.load_workbook(before), openpyxl.load_workbook(after)
    total = 0
    if "Deal ledger" in a_wb and "Deal ledger" in b_wb:
        print("Events: %d -> %d" % (a_wb["Deal ledger"].max_row - 1, b_wb["Deal ledger"].max_row - 1))
    for name in dict.fromkeys(a_wb.sheetnames + b_wb.sheetnames):
        if name == "Source" and not include_source:
            continue
        if name not in a_wb.sheetnames or name not in b_wb.sheetnames:
            print("## %s: sheet %s" % (name, "added" if name in b_wb.sheetnames else "removed"))
            total += 1
            continue
        out = compare_sheet(a_wb[name], b_wb[name], by_quote)
        print("## %s: %s" % (name, "no change" if not out else "%d change(s)" % len(out)))
        print("\n".join(out)) if out else None
        total += len(out)
    print("\nTotal: %d change(s)" % total)
    a_wb.close()
    b_wb.close()


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("before")
    cli.add_argument("after")
    cli.add_argument("--by-quote", action="store_true")
    cli.add_argument("--include-source", action="store_true")
    args = cli.parse_args()
    main(args.before, args.after, args.include_source, args.by_quote)
