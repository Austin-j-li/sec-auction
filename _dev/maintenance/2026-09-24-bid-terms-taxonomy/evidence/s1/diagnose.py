#!/usr/bin/env python3
"""Diagnostic only: apply the conditions of the v1.14 review warnings and of
bid.other_scope_per_share to every workbook, the v1.13.2 ones included, where the
checker does not run them, to see how they would behave.

Usage:
    python3 diagnose.py --inputs DIR --checker CHECKER --output FILE

DIR has the layout reproduce.py uses (extraction/*.xlsx and versions/<deal>/<id>/*.xlsx).
The workbooks are only read, and an existing FILE is never overwritten.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--inputs", required=True, type=Path, help="Folder of copied inputs")
    parser.add_argument("--checker", required=True, type=Path, help="check_lean.py whose sequence rules are applied")
    parser.add_argument("--output", required=True, type=Path, help="JSON result; must not exist yet")
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f"{args.output} exists; choose a new output path")
    if not args.output.parent.is_dir():
        parser.error(f"{args.output.parent} is not a folder")
    workbooks = sorted([*(args.inputs / "extraction").glob("*.xlsx"), *(args.inputs / "versions").glob("*/*/*.xlsx")])
    if not workbooks:
        parser.error(f"no workbooks under {args.inputs}")

    spec = importlib.util.spec_from_file_location("check_lean_diagnosed", args.checker)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    out = {}
    for path in workbooks:
        wb = cl.openpyxl.load_workbook(path)
        ws = wb["Deal ledger"]
        header = [c.value for c in ws[1]]
        rows = [(i, dict(zip(header, r))) for i, r in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2)
                if any(v is not None for v in r)]
        for _, r in rows:
            r.setdefault("Exclusivity", None)  # v1.13.2 has no Exclusivity column
        checker = cl.LeanChecker(path, path)
        checker.check_v114_sequences(ws, rows)
        found = [[i["code"], i["row"], i["message"][:90]] for i in checker.issues]
        # Extended outcomes with no Deadline set or Deadline revised on or after the matching Deadline row.
        deadlines: dict = {}
        for _, r in rows:
            p, rd = cl.as_integer(r["Process"]), cl.as_integer(r["Round"])
            if p and rd and r["Event"] in {"Deadline", "Deadline set", "Deadline revised"}:
                deadlines.setdefault((p, rd), []).append((r["Event"], cl.as_date(r["Sort date"])))
        for row in wb["Rounds"].iter_rows(min_row=2, values_only=True):
            if not row[0] or not row[6]:
                continue
            parts = [x.strip() for x in str(row[6]).split(";")]
            events = deadlines.get((row[0], row[1]), [])
            reached = [d for e, d in events if e == "Deadline"]
            new = [d for e, d in events if e != "Deadline" and d]
            if len(reached) == len(parts):
                for pos, (part, day) in enumerate(zip(parts, reached), 1):
                    if part == "Extended" and day and not any(n >= day for n in new):
                        found.append(["rounds.extended_without_new_date", [row[0], row[1], pos], ""])
            if "Extended" in parts:
                found.append(["info.extended_present", [row[0], row[1]], str(row[6])])
        other_scope = [r for _, r in rows if r["Event"] == "Other-scope bid"]
        blank_note = [r["#"] for r in other_scope if cl.is_blank(r["Note"])]
        per_share = [[r["#"], column] for r in other_scope for column in ("Price low", "Price high", "CVR/earnout value")
                     if not cl.is_blank(r.get(column))]
        found.append(["info.other_scope_rows", len(other_scope), f"blank Note: {blank_note}"])
        found.append(["info.other_scope_per_share", per_share, "filled per-share cells on Other-scope bid rows"])
        name = str(path.relative_to(args.inputs))
        out[name] = found
        print(name)
        for f in found:
            print("   ", f)
    with args.output.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps({"checker": str(args.checker), "checker_version": cl.CHECKER_VERSION,
                                 "inputs": str(args.inputs), "workbooks": out}, indent=2, ensure_ascii=False, default=str) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
