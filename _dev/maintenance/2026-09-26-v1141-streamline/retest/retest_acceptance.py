#!/usr/bin/env python3
"""Offline acceptance check for the v1.14.1 retest (V1141_SPEC.md §10 step 6).

Run it after the five runs, outside their sandboxes, never where an extracting agent can see it.
It re-checks each workbook with checker 1.8 under the v1.14.1 rules and tests the behaviours §10
step 6 pins. Items a script cannot judge are marked REVIEW with the rows to look at. It does not
reuse the v1.14 trial's rubric, which rewards the dates, bounds and long Notes v1.14.1 removed.

Usage:
    python3 retest_acceptance.py --tools ~/work/Projects/sec-extraction-v114/_dev/tools \
        --workbook mac-gray=PATH --workbook providence-worcester=PATH --workbook stec=PATH \
        --workbook synacor=PATH --workbook datalink=PATH --output acceptance.json

Exit status 0 when no item FAILs (REVIEW items still need a person), 1 otherwise.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

MAIN = Path(__file__).resolve().parents[4]
# Rows in the trial's Opus 5.5 medium workbooks (v1.14 trial packet): the retest should not exceed them.
TRIAL_ROWS = {"mac-gray": 64, "providence-worcester": 63, "stec": 66}
# Recorded round maps (MAP_RECHECK.md): Synacor three processes and six rounds; Datalink F9 five rounds.
RECORDED_MAPS = {"synacor": {"processes": 3, "rounds": 6}, "datalink": {"processes": 1, "rounds": 5}}
SAME_AS = re.compile(r"^\s*Same as #\s*\d+\b\.?\s*", re.IGNORECASE)


def rows_of(ws):
    header = [cell.value for cell in ws[1]]
    return [dict(zip(header, row)) for row in ws.iter_rows(min_row=2, values_only=True) if any(v not in (None, "") for v in row)]


def day(value):
    return value.date() if isinstance(value, dt.datetime) else value if isinstance(value, dt.date) else None


def on(record, month, dom, column="Sort date"):
    d = day(record.get(column))
    return bool(d and (d.month, d.day) == (month, dom))


def who(record, pattern):
    return bool(re.search(pattern, str(record.get("Who") or ""), re.IGNORECASE))


def trigger(record):
    return SAME_AS.sub("", str(record.get("Note") or ""), count=1)[:3]


def blank(value):
    return value in (None, "")


def item(results, deal, key, status, text, rows=()):
    results.append({"deal": deal, "item": key, "status": status, "text": text, "rows": [r.get("#") for r in rows]})


def check_deal(check_lean, deal, path, results):
    manifest = {row["deal"]: row["file"] for row in csv.DictReader((MAIN / "raw_filing/MANIFEST.csv").open())}
    report = check_lean.LeanChecker(path, MAIN / "raw_filing" / manifest[deal], rules="v1.14.1").run()
    book = check_lean.openpyxl.load_workbook(path, data_only=True)
    ledger, rounds, questions = rows_of(book["Deal ledger"]), rows_of(book["Rounds"]), rows_of(book["Questions"])
    bids = [r for r in ledger if r.get("Event") in check_lean.BID_EVENTS]

    # All five: no Note-length error; at most five Questions plus the process Question; row counts.
    long_notes = [i for i in report["issues"] if i["code"] == "ledger.note_length"]
    item(results, deal, "checker", "PASS" if report["summary"]["errors"] == 0 else "REVIEW",
         f"checker {report['checker_version']} ({report['ledger_schema']}): {report['summary']['errors']} errors, {report['summary']['warnings']} warnings")
    item(results, deal, "note_length", "PASS" if not long_notes else "FAIL", f"{len(long_notes)} Notes over 40 words")
    markers = {r.get("#") for r in ledger if r.get("Event") in check_lean.PROCESS_MARKERS}
    process = [q for q in questions if check_lean.is_process_question(q.get("Question"), q.get("Rows affected"), markers)][:1]
    counted = len(questions) - len(process)
    item(results, deal, "questions", "PASS" if counted <= 5 else "FAIL", f"{counted} Questions besides the process Question ({'present' if process else 'none'})")
    if deal in TRIAL_ROWS:
        item(results, deal, "rows", "PASS" if len(ledger) <= TRIAL_ROWS[deal] else "FAIL",
             f"{len(ledger)} ledger rows; the trial's Opus 5.5 medium workbook had {TRIAL_ROWS[deal]}")

    if deal == "mac-gray":
        cohort = [r for r in ledger if r.get("Event") == "Did not submit" and r.get("Count") == 16 and on(r, 7, 23)]
        item(results, deal, "16 by 23 July", "PASS" if cohort else "FAIL", "16 unnamed signers Did not submit, dated 23 July, Count 16", cohort)
        october = [r for r in bids if r.get("Event") == "Bid" and day(r.get("Sort date")) and day(r.get("Sort date")).month == 10]
        liability = [r for r in october if re.search(r"liab|reverse|termination fee|cap\b", str(r.get("Note") or ""), re.IGNORECASE)]
        ok = liability and all(blank(r.get("Price low")) and blank(r.get("Price high")) for r in liability)
        item(results, deal, "October liability rows", "PASS" if ok else "REVIEW",
             "October liability revisions are Bid rows with blank prices (H4); confirm the rows listed are those revisions", liability or october)
        party_a = [r for r in bids if who(r, r"\bParty A\b") and on(r, 9, 18)]
        ok = party_a and all(r.get("Conditions") == "Heavy" and trigger(r) == "H1:" and r.get("Formality") == "Formal" for r in party_a)
        item(results, deal, "Party A 18 September", "PASS" if ok else "FAIL", "Party A's 18 September bid is Heavy (H1) and Formal", party_a)

    if deal == "providence-worcester":
        cohort = [r for r in ledger if r.get("Event") == "Did not submit" and r.get("Count") == 16]
        item(results, deal, "16 non-submitters", "PASS" if cohort else "FAIL", "16 non-submitters, Count 16", cohort)
        entrants = [r for r in ledger if r.get("Event") == "NDA signed"]
        item(results, deal, "no extra entrant", "REVIEW", "No named party is entered beside the 25 signers; check the NDA signed rows", entrants)
        e_h2 = [r for r in bids if who(r, r"\bParty E\b") and trigger(r) == "H2:"]
        item(results, deal, "Party E not H2", "PASS" if not e_h2 else "FAIL", "No Party E bid is coded H2", e_h2)
        gw = [r for r in bids if who(r, r"G&W|Genesee") and on(r, 8, 12)]
        ok = gw and all(r.get("Regulatory") == "Concern" for r in gw)
        item(results, deal, "G&W 12 August", "PASS" if ok else "FAIL", "G&W's 12 August bid has Regulatory Concern", gw)
        party_c = [r for r in bids if who(r, r"\bParty C\b") and on(r, 7, 12)]
        ok = party_c and all(r.get("Due diligence") != "Not begun" for r in party_c)
        item(results, deal, "Party C 12 July", "PASS" if ok else "FAIL", "Party C's 12 July diligence is not Not begun", party_c)

    if deal == "stec":
        h = [r for r in ledger if who(r, r"Company H") and r.get("Event") == "Dropped by target"]
        ok = h and all((on(r, 5, 16) or on(r, 5, 16, "Date to")) and r.get("Exit reason") == "Would not improve earlier offer" for r in h)
        item(results, deal, "Company H", "PASS" if ok else "FAIL", "Company H Dropped by target by 16 May, Would not improve earlier offer", h)
        standstill = [r for r in bids if who(r, r"WDC|Western Digital") and day(r.get("Sort date")) and day(r.get("Sort date")).month == 6
                      and trigger(r) == "H3:" and blank(r.get("Price low")) and blank(r.get("Price high"))]
        item(results, deal, "standstill warning", "PASS" if standstill else "FAIL", "WDC's June standstill warning is a Bid with H3 and no price", standstill)
        count = len([r for r in rounds if r.get("Process") == 1])
        item(results, deal, "two rounds", "PASS" if count == 2 else "FAIL", f"{count} rounds (expected 2)")

    if deal in RECORDED_MAPS:
        processes = len({r.get("Process") for r in rounds})
        mapped = [(r.get("Process"), r.get("Round"), day(r.get("Opened")).isoformat() if day(r.get("Opened")) else None, r.get("How opened"), r.get("Finality")) for r in rounds]
        expected = RECORDED_MAPS[deal]
        same = processes == expected["processes"] and len(rounds) == expected["rounds"]
        item(results, deal, "round map", "PASS" if same else "REVIEW",
             f"{processes} processes, {len(rounds)} rounds; recorded {expected['processes']} and {expected['rounds']}. "
             "A change must be explained by trigger (d) and shown to Austin: " + json.dumps(mapped, default=str))
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tools", required=True, type=Path, help="the _dev/tools folder holding checker 1.8")
    ap.add_argument("--workbook", action="append", required=True, help="deal=path, once per retest workbook")
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    sys.path.insert(0, str(args.tools))
    import check_lean
    if check_lean.CHECKER_VERSION != "1.8":
        raise SystemExit(f"needs checker 1.8; {args.tools} has {check_lean.CHECKER_VERSION}")
    results: list[dict] = []
    for pair in args.workbook:
        deal, path = pair.split("=", 1)
        check_deal(check_lean, deal, Path(path), results)
    args.output.write_text(json.dumps({"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "results": results}, indent=2) + "\n")
    for r in results:
        print(f"{r['status']:6} {r['deal']:22} {r['item']:24} {r['text']}" + (f" rows {r['rows']}" if r["rows"] else ""))
    return 1 if any(r["status"] == "FAIL" for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
