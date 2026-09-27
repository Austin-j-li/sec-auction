#!/usr/bin/env python3
"""Show what changed between two ledger workbooks, sheet by sheet.

    python3 _dev/tools/diff_workbooks.py before.xlsx after.xlsx [--crosswalk] [--by-quote] [--include-source]

Columns are aligned by their heading, and the columns only one workbook has are listed once
per sheet. Rows are matched by a key: Deal ledger rows by (Event, Who, Sort date), Rounds lines
by (Process, Round), Questions by Q and Deal facts by Field. `--by-quote` then pairs leftover
ledger rows whose quoted passages are the same. Other sheets are matched in order (difflib), so an
inserted row shows as one added row, not as every later row changing. For a matched row only the
changed cells are printed, with each value's type. A `Source` sheet (the provenance a cockpit
download adds) is skipped unless `--include-source` is given.

`--crosswalk` compares a v1.13.2 workbook with a v1.14 one: All cash is compared with Stock %,
and the other differences that come from the schema are labelled rather than equated
(`crosswalk()`). An event-count summary for both workbooks comes first.
"""
import argparse
from collections import Counter
import datetime as dt
import difflib
import re
import sys

import openpyxl

import check_lean

KEYS = {
    "Deal ledger": ("Event", "Who", "Sort date"),
    "Rounds": ("Process", "Round"),
    "Questions": ("Q",),
    "Deal facts": ("Field",),
}
SOURCE_SHEET = "Source"
# Deal ledger rows are identified by their key; "#" is renumbered by any insertion, so it labels rows only.
LABEL_ONLY = {"Deal ledger": {"#"}}
# Events whose counts show the v1.14 rule changes at a glance (D7, D10, D13, D15, E6).
SUMMARY_EVENTS = ("Bid", "Bid reaffirmed", "Other-scope bid", "Exclusivity changed", "Did not submit",
                  "Re-entered", "Round opened")
ADDED_IN_V114 = tuple(column for column in check_lean.TERM_COLUMNS_V114 if column != "Stock %")
LATE_V1132, LATE_V114 = "Late bids accepted", "Extended (late bid accepted)"


def blank(value):
    return value is None or (isinstance(value, str) and not value.strip())


def all_cash_for_stock(stock):
    """The v1.13.2 All cash value a v1.14 Stock % cell stands for; None where there is no equivalent.

    0 is Yes; a number above 0, a range or Part stock is No; Not stated is Not stated. Varies,
    a blank and an invalid value have no equivalent.
    """
    if isinstance(stock, bool) or blank(stock):
        return None
    if isinstance(stock, (int, float)):
        return "Yes" if stock == 0 else "No" if 0 < stock <= 100 else None
    text = str(stock).strip()
    if text == "Part stock":
        return "No"
    if text == "Not stated":
        return "Not stated"
    match = check_lean.STOCK_RANGE_RE.fullmatch(text)
    return "No" if match and float(match.group(2)) > 0 else None


def crosswalk(column, old, new, new_row):
    """The v1.13.2 -> v1.14 crosswalk for one pair of cells (spec §7.8).

    `column` is the v1.14 column; "Stock %" is compared with the v1.13.2 "All cash". `old` is the
    v1.13.2 value, `new` the v1.14 value, `new_row` the whole v1.14 row keyed by heading.
    Returns None where no crosswalk rule applies (compare the cells as they are), otherwise
    (verdict, label): "same" (equivalent, not a change), "shown" (a difference that comes from the
    schema, shown with its label and not equated) or "suppressed" (not shown, counted).
    """
    if column == "Stock %":
        if blank(old) and blank(new):
            return "same", None
        if isinstance(new, str) and new.strip() == "Varies":
            return "shown", "v1.14 Varies has no v1.13.2 equivalent"
        mapped = all_cash_for_stock(new)
        if mapped is not None and not blank(old) and str(old).strip() == mapped:
            return "same", None
        return "shown", "All cash vs Stock %: not equivalent (Yes = 0; No = above 0, a range or Part stock)"
    if column in ("Price low", "Price high"):
        if new_row.get("Event") == "Other-scope bid" and blank(new) and not blank(old):
            return "suppressed", "D18: v1.14 leaves Other-scope prices blank"
        marker, value = new_row.get("CVR/earnout"), new_row.get("CVR/earnout value")
        if not blank(marker) or not blank(value):
            return "shown", "E13 basis: v1.14 price with CVR/earnout %s, value %s; not equated with the v1.13.2 price" % (
                "blank" if blank(marker) else marker, "blank" if blank(value) else value)
        return None
    if column == "Deadline outcome":
        if LATE_V1132 in str(old or "") and LATE_V114 in str(new or ""):
            return "shown", "D11 (wider): shown, not equated"
        return None
    if column == "Conditions":
        if str(old or "").strip() == str(new or "").strip():
            return "same", None
        return "shown", "E12 rules changed"
    return None


def display(cell):
    kind, value = cell[:2]
    label = {"n": "number", "s": "text", "d": "date", "b": "boolean", "f": "formula"}.get(kind, kind)
    return f"{value} [{label}]" if kind != "blank" else "[blank]"


def clip(text, n=160):
    text = text.replace("\n", " ")
    return text if len(text) <= n else text[:n] + "..."


def read_sheet(ws):
    """(headings, rows): each row is a dict of heading -> (type, text, value), with its Excel row number."""
    raw = [
        [("blank", "", None) if c.value is None else (c.data_type, str(c.value), c.value) for c in row]
        for row in ws.iter_rows()
    ]
    if not raw:
        return [], []
    names = []
    for k, (_, text, _) in enumerate(raw[0]):
        name = text.strip() or "col %d" % (k + 1)
        names.append(name if name not in names else "%s (%d)" % (name, k + 1))
    rows = []
    for number, cells in enumerate(raw[1:], 2):
        rows.append((number, dict(zip(names, cells))))
    return names, rows


def key_text(value):
    if isinstance(value, dt.datetime):
        value = value.date()
    return value.isoformat() if isinstance(value, dt.date) else str(value).strip() if value is not None else ""


def quote_text(value):
    """A quoted passage without its page reference, outer quotation marks or spacing."""
    text = check_lean.normalize_contiguous(value or "")
    text = check_lean.PAGE_REF_RE.sub("", text).strip()
    return re.sub(r"^[\"'\u201c\u201d]+|[\"'\u201c\u201d]+$", "", text).strip()


def pair_rows(a_rows, b_rows, key, shared):
    """Match rows with equal keys; several rows under one key pair by the most equal cells."""
    groups = {}
    for side, rows in ((0, a_rows), (1, b_rows)):
        for index, (_, row) in enumerate(rows):
            groups.setdefault(key(row), ([], []))[side].append(index)
    pairs = []
    for left, right in groups.values():
        if len(left) == 1 and len(right) == 1:
            pairs.append((left[0], right[0]))
            continue
        scored = sorted((-sum(a_rows[i][1][c][:2] == b_rows[j][1][c][:2] for c in shared), i, j)
                        for i in left for j in right)
        used_a, used_b = set(), set()
        for _, i, j in scored:
            if i not in used_a and j not in used_b:
                pairs.append((i, j))
                used_a.add(i)
                used_b.add(j)
    return pairs


def pair_by_quote(a_rows, b_rows, pairs):
    """Pair leftover ledger rows whose quoted passages are equal, or one contains the other; unique pairs only."""
    done_a, done_b = {i for i, _ in pairs}, {j for _, j in pairs}
    quotes_a = {i: quote_text(row.get("Quote and page", ("", "", None))[2]) for i, (_, row) in enumerate(a_rows) if i not in done_a}
    quotes_b = {j: quote_text(row.get("Quote and page", ("", "", None))[2]) for j, (_, row) in enumerate(b_rows) if j not in done_b}
    candidates = {i: [j for j, q in quotes_b.items() if len(min(p, q, key=len)) >= 20 and (p in q or q in p)]
                  for i, p in quotes_a.items() if p}
    claimed = Counter(j for found in candidates.values() for j in found)
    return [(i, found[0]) for i, found in candidates.items() if len(found) == 1 and claimed[found[0]] == 1]


def row_line(row, names):
    return " | ".join(display(row[n]) for n in names if n in row and row[n][0] != "blank")


class Comparison:
    """Cell comparison for matched rows, with the crosswalk when one workbook is v1.13.2 and the other v1.14."""

    def __init__(self, a_schema, b_schema, crosswalk_on):
        self.xw = crosswalk_on and a_schema != b_schema and None not in (a_schema, b_schema)
        # The v1.13.2 side is "old" for the crosswalk, whichever of the two it is.
        self.a_is_old = a_schema == check_lean.SCHEMA_V1132
        self.suppressed = 0

    def cells(self, sheet, a, b, shared, label):
        out = []
        new_row = {c: v[2] for c, v in (b if self.a_is_old else a).items()} if self.xw else {}
        columns = [(c, c) for c in shared if c not in LABEL_ONLY.get(sheet, ())]
        if self.xw and sheet == "Deal ledger":
            columns.append(("All cash", "Stock %") if self.a_is_old else ("Stock %", "All cash"))
        for ca, cb in columns:
            if ca not in a or cb not in b:
                continue
            x, y = a[ca], b[cb]
            verdict = None
            if self.xw:
                old, new = (x, y) if self.a_is_old else (y, x)
                v114_column = cb if self.a_is_old else ca
                verdict = crosswalk(v114_column, old[2], new[2], new_row)
            if verdict is None:
                if x[:2] == y[:2]:
                    continue
                note = None
            elif verdict[0] == "same":
                continue
            elif verdict[0] == "suppressed":
                self.suppressed += 1
                continue
            else:
                note = verdict[1]
            col = ca if ca == cb else "%s -> %s" % (ca, cb)
            out.append("  %s, %s:\n      was: %s\n      now: %s%s" % (
                label, col, clip(display(x)), clip(display(y)), "\n      crosswalk: %s" % note if note else ""))
        return out


def column_notes(sheet, only_a, only_b, comparison):
    lines = []
    for side, cols in (("before", only_a), ("after", only_b)):
        for col in cols:
            note = ""
            if comparison.xw and sheet == "Deal ledger":
                if col == "All cash":
                    note = " [crosswalk: compared with Stock %]"
                elif col == "Stock %":
                    note = " [crosswalk: replaces All cash]"
                elif col in ADDED_IN_V114:
                    note = " [added in v1.14]"
            lines.append("  column only in %s: %s%s" % (side, col, note))
    if comparison.xw and sheet == "Deal ledger":
        lines.append("  Conditions: compared [crosswalk: E12 rules changed]")
    return lines


def diff_sheet(name, a_ws, b_ws, comparison, by_quote):
    a_names, a_rows = read_sheet(a_ws)
    b_names, b_rows = read_sheet(b_ws)
    shared = [n for n in a_names if n in b_names]
    only_a = [n for n in a_names if n not in b_names]
    only_b = [n for n in b_names if n not in a_names]
    out, matching = [], ""
    key_cols = KEYS.get(name)
    if key_cols and all(c in a_names and c in b_names for c in key_cols):
        a_rows = [r for r in a_rows if any(v[0] != "blank" for v in r[1].values())]
        b_rows = [r for r in b_rows if any(v[0] != "blank" for v in r[1].values())]

        def key(row):
            return tuple(key_text(row[c][2]) for c in key_cols)

        pairs = pair_rows(a_rows, b_rows, key, shared)
        by_quote_pairs = pair_by_quote(a_rows, b_rows, pairs) if by_quote and name == "Deal ledger" else []
        for i, j in sorted(pairs + by_quote_pairs):
            (na, ra), (nb, rb) = a_rows[i], b_rows[j]
            label = "row %d -> %d [%s]" % (na, nb, " | ".join(key(ra)))
            if (i, j) in by_quote_pairs:
                label += " (matched by quote; key now %s)" % " | ".join(key(rb))
            out += comparison.cells(name, ra, rb, shared, label)
        matched_a, matched_b = {i for i, _ in pairs + by_quote_pairs}, {j for _, j in pairs + by_quote_pairs}
        matching = "; rows by %s: %d matched%s, %d removed, %d added" % (
            ", ".join(key_cols), len(pairs), " (+%d by quote)" % len(by_quote_pairs) if by_quote_pairs else "",
            len(a_rows) - len(matched_a), len(b_rows) - len(matched_b))
        for i, (number, row) in enumerate(a_rows):
            if i not in matched_a:
                out.append("  removed row %d [%s]: %s" % (number, " | ".join(key(row)), clip(row_line(row, a_names), 300)))
        for j, (number, row) in enumerate(b_rows):
            if j not in matched_b:
                out.append("  added row %d [%s]: %s" % (number, " | ".join(key(row)), clip(row_line(row, b_names), 300)))
    else:
        # No key: match rows in order on the shared columns.
        a_seq = [tuple(row[c][:2] for c in shared) for _, row in a_rows]
        b_seq = [tuple(row[c][:2] for c in shared) for _, row in b_rows]
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a_seq, b=b_seq, autojunk=False).get_opcodes():
            if op == "equal":
                continue
            if op == "replace" and i2 - i1 == j2 - j1:
                for i, j in zip(range(i1, i2), range(j1, j2)):
                    out += comparison.cells(name, a_rows[i][1], b_rows[j][1], shared,
                                            "row %d -> %d" % (a_rows[i][0], b_rows[j][0]))
                continue
            for i in range(i1, i2):
                out.append("  removed row %d: %s" % (a_rows[i][0], clip(row_line(a_rows[i][1], a_names), 300)))
            for j in range(j1, j2):
                out.append("  added row %d: %s" % (b_rows[j][0], clip(row_line(b_rows[j][1], b_names), 300)))
    return column_notes(name, only_a, only_b, comparison), out, len(only_a) + len(only_b), matching


def event_counts(wb):
    if "Deal ledger" not in wb.sheetnames:
        return Counter()
    _, rows = read_sheet(wb["Deal ledger"])
    return Counter(row["Event"][1].strip() for _, row in rows if "Event" in row and row["Event"][0] != "blank")


def main(before, after, crosswalk_on=False, include_source=False, by_quote=False):
    a_wb, b_wb = openpyxl.load_workbook(before), openpyxl.load_workbook(after)
    schemas = []
    for wb in (a_wb, b_wb):
        head = next(wb["Deal ledger"].iter_rows(min_row=1, max_row=1, values_only=True), ()) if "Deal ledger" in wb.sheetnames else None
        schemas.append(check_lean.schema_for_header(head) if head is not None else None)
    comparison = Comparison(schemas[0], schemas[1], crosswalk_on)
    print("Before: %s (%s)\nAfter: %s (%s)" % (before, schemas[0] or "no Deal ledger", after, schemas[1] or "no Deal ledger"))
    if crosswalk_on:
        print("Crosswalk: %s" % ("v1.13.2 -> v1.14 differences are labelled" if comparison.xw
                                 else "not applied: it needs one v1.13.2 and one v1.14 workbook"))
    a_events, b_events = event_counts(a_wb), event_counts(b_wb)
    if a_events or b_events:
        print("\n## Event counts (before -> after)")
        others = sorted((set(a_events) | set(b_events)) - set(SUMMARY_EVENTS))
        for event in (*SUMMARY_EVENTS, *others):
            print("  %s: %d -> %d" % (event, a_events[event], b_events[event]))
        print("  All rows: %d -> %d" % (sum(a_events.values()), sum(b_events.values())))
    total = columns = 0
    for name in dict.fromkeys(a_wb.sheetnames + b_wb.sheetnames):
        if name == SOURCE_SHEET and not include_source:
            print("\n## %s: skipped (--include-source compares it)" % name)
            continue
        if name not in a_wb.sheetnames or name not in b_wb.sheetnames:
            print("\n## %s: sheet %s" % (name, "added" if name in b_wb.sheetnames else "removed"))
            total += 1
            continue
        notes, out, only, matching = diff_sheet(name, a_wb[name], b_wb[name], comparison, by_quote)
        print("\n## %s: %s%s" % (name, "no change" if not out else "%d change(s)" % len(out), matching))
        print("\n".join(notes + out)) if notes or out else None
        total += len(out)
        columns += only
    if comparison.suppressed:
        print("\n%d Other-scope price cell(s) blank in v1.14 not shown (D18)" % comparison.suppressed)
    print("\nTotal: %d change(s) in rows; %d column(s) in one workbook only" % (total, columns))
    a_wb.close()
    b_wb.close()


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    cli.add_argument("before")
    cli.add_argument("after")
    cli.add_argument("--crosswalk", action="store_true", help="label v1.13.2 -> v1.14 schema differences")
    cli.add_argument("--by-quote", action="store_true", help="pair leftover ledger rows by their quoted passage")
    cli.add_argument("--include-source", action="store_true", help="also compare a Source sheet")
    args = cli.parse_args()
    main(args.before, args.after, args.crosswalk, args.include_source, args.by_quote)
