#!/usr/bin/env python3
"""Show what changed between two ledger workbooks, sheet by sheet.

    python3 _dev/tools/diff_workbooks.py before.xlsx after.xlsx

Rows are matched in order (difflib), so an inserted row shows as one added row,
not as every later row changing. For a changed row only the changed cells are
printed, under the column heading from the sheet's first row.
"""
import argparse
from collections import Counter
import sys

import openpyxl
import check_lean


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


def blank(value):
    return value is None or isinstance(value, str) and not value.strip()


def all_cash_for_stock(stock):
    """The old All cash choice represented by a 29-column Stock % value."""
    if isinstance(stock, bool) or blank(stock):
        return None
    if isinstance(stock, (int, float)):
        return "Yes" if stock == 0 else "No" if 0 < stock <= 100 else None
    value = str(stock).strip()
    if value == "Part stock":
        return "No"
    if value == "Not stated":
        return "Not stated"
    match = check_lean.STOCK_RANGE_RE.fullmatch(value)
    return "No" if match and float(match.group(2)) > 0 else None


def crosswalk(column, old, new, new_row):
    """Return a v1.13.2 to 29-column comparison verdict and its explanation."""
    if column == "Stock %":
        if new == "Varies":
            return "shown", "Varies has no v1.13.2 equivalent"
        if blank(old) and blank(new):
            return "same", "both blank"
        if old == all_cash_for_stock(new):
            return "same", "All cash and Stock % agree"
        return "shown", "All cash and Stock % differ"
    if column in ("Price low", "Price high") and not (blank(old) and blank(new)) and (
        not blank(new_row.get("CVR/earnout")) or not blank(new_row.get("CVR/earnout value"))
    ):
        return "shown", "price basis may exclude separately reported contingent value"
    if column == "Conditions":
        return ("shown", "E12 condition rules changed") if old != new else None
    if column == "Deadline outcome":
        if old == new:
            return None
        if (old, new) == ("Late bids accepted", "Extended (late bid accepted)"):
            return "shown", "D11 (wider)"
        return "shown", "deadline outcome choices changed"
    return None


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


def compare_sheet(a_ws, b_ws, crosswalk_on=False, by_quote=False, schema_direction=None):
    a_head, a = records(a_ws)
    b_head, b = records(b_ws)
    out = []
    added = [column for column in b_head if column not in a_head]
    removed = [column for column in a_head if column not in b_head]
    if added:
        out.append("  added column(s): " + ", ".join(display(("s", column)) for column in added))
    if removed:
        out.append("  removed column(s): " + ", ".join(removed))
    old_to_new = a_ws.title == "Deal ledger" and "All cash" in a_head and "Stock %" in b_head
    new_to_old = a_ws.title == "Deal ledger" and "Stock %" in a_head and "All cash" in b_head
    schema_direction = schema_direction or ("old_to_new" if old_to_new else "new_to_old" if new_to_old else None)
    pairs = {key: key for key in a if key in b}
    if by_quote and a_ws.title == "Deal ledger":
        quote_matches(a, b, pairs)
    d18_blanks = 0
    for key in a:
        if key not in pairs:
            index, record = a[key]
            out.append(f"  removed row {index}: " + clip(" | ".join(
                f"{column}={display(cell)}" for column, cell in record.items() if cell[0] != "blank"), 300))
            continue
        i, old = a[key]
        j, new = b[pairs[key]]
        for column in dict.fromkeys([*a_head, *b_head]):
            if old_to_new and column == "All cash" or new_to_old and column == "Stock %":
                continue
            old_column = ("All cash" if old_to_new and column == "Stock %" else
                          "Stock %" if new_to_old and column == "All cash" else column)
            new_column = column
            x = old.get(old_column, ("blank", ""))
            y = new.get(new_column, ("blank", ""))
            if old_column not in old and y[0] == "blank" or new_column not in new and x[0] == "blank":
                continue
            if (crosswalk_on and a_ws.title == "Deal ledger" and column in ("Price low", "Price high")
                    and schema_direction in ("old_to_new", "new_to_old")):
                legacy, modern = (old, new) if schema_direction == "old_to_new" else (new, old)
                legacy_price = legacy.get(column, ("blank", ""))[1]
                modern_price = modern.get(column, ("blank", ""))[1]
                if (modern.get("Event", ("blank", ""))[1] == "Other-scope bid"
                        and not blank(legacy_price) and blank(modern_price)):
                    d18_blanks += 1
                    continue
            note = ""
            verdict = None
            if crosswalk_on and schema_direction:
                v114_column = "Stock %" if column in ("All cash", "Stock %") else column
                v114_row = new if schema_direction == "old_to_new" else old
                legacy_value, modern_value = (x[1], y[1]) if schema_direction == "old_to_new" else (y[1], x[1])
                verdict = crosswalk(v114_column, legacy_value, modern_value,
                                    {name: cell[1] for name, cell in v114_row.items()})
                if verdict:
                    if verdict[0] == "same":
                        continue
                    note = "\n      crosswalk: " + verdict[1]
            if x == y and not verdict:
                continue
            out.append(f"  row {i} -> {j}, {column}:\n      was: {clip(display(x))}\n      now: {clip(display(y))}{note}")
    for key in b:
        if key not in pairs.values():
            index, record = b[key]
            out.append(f"  added row {index}: " + clip(" | ".join(
                f"{column}={display(cell)}" for column, cell in record.items() if cell[0] != "blank"), 300))
    if d18_blanks:
        out.append(f"  D18: {d18_blanks} blank Other-scope price cell(s) counted, not listed")
    return out


def main(before, after, crosswalk_on=False, include_source=False, by_quote=False):
    a_wb, b_wb = openpyxl.load_workbook(before), openpyxl.load_workbook(after)
    total = 0
    a_ledger = [cell.value for cell in a_wb["Deal ledger"][1]] if "Deal ledger" in a_wb else []
    b_ledger = [cell.value for cell in b_wb["Deal ledger"][1]] if "Deal ledger" in b_wb else []
    schema_direction = ("old_to_new" if "All cash" in a_ledger and "Stock %" in b_ledger else
                        "new_to_old" if "Stock %" in a_ledger and "All cash" in b_ledger else None)
    if "Deal ledger" in a_wb and "Deal ledger" in b_wb:
        print("Events: %d -> %d" % (a_wb["Deal ledger"].max_row - 1, b_wb["Deal ledger"].max_row - 1))
    for name in dict.fromkeys(a_wb.sheetnames + b_wb.sheetnames):
        if name == "Source" and not include_source:
            continue
        if name not in a_wb.sheetnames or name not in b_wb.sheetnames:
            print("## %s: sheet %s" % (name, "added" if name in b_wb.sheetnames else "removed"))
            total += 1
            continue
        out = compare_sheet(a_wb[name], b_wb[name], crosswalk_on, by_quote, schema_direction)
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
    cli.add_argument("--crosswalk", action="store_true")
    cli.add_argument("--by-quote", action="store_true")
    cli.add_argument("--include-source", action="store_true")
    args = cli.parse_args()
    main(args.before, args.after, args.crosswalk, args.include_source, args.by_quote)
