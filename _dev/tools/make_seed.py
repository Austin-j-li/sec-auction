#!/usr/bin/env python3
"""Build ref/seed.csv from Alex's workbook: one row per deal, identifying columns only.

The seed says which filing belongs to which deal (name, form type, filing date,
EDGAR index link). It carries no bidders, prices or other hand-coded answers.
Rebuild it with this script; do not edit it by hand.

    python3 _dev/tools/make_seed.py
"""
import csv
import re
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
WORKBOOK = ROOT / "ref" / "deal_details_Alex_2026.xlsx"
SEED = ROOT / "ref" / "seed.csv"

FIELDS = ["deal", "target_name", "deal_number", "form_type", "date_filed", "index_url", "status"]
INDEX_URL = re.compile(r"^https://www\.sec\.gov/Archives/edgar/data/\d+/[\d-]+-index\.html?$")
SUFFIXES = {"INC", "CORP", "CO", "LTD", "PLC", "LP", "LLC", "NV", "SA", "CL", "A", "B", "OLD", "NEW"}
# Short names already in use that the slug rule would not produce.
SLUG_OVERRIDES = {"PROVIDENCE & WORCESTER RR CO": "providence-worcester"}


def slug(name):
    if name in SLUG_OVERRIDES:
        return SLUG_OVERRIDES[name]
    words = re.sub(r"[^A-Z0-9 ]", " ", name.upper()).split()
    while len(words) > 1 and words[-1] in SUFFIXES:
        words.pop()
    out = []
    for w in words:  # "S T E C" -> "stec"
        if len(w) == 1 and out and out[-1][1]:
            out[-1] = (out[-1][0] + w, True)
        else:
            out.append((w, len(w) == 1))
    return "-".join(w for w, _ in out).lower()


def main():
    ws = openpyxl.load_workbook(WORKBOOK, read_only=True).worksheets[0]
    rows = ws.iter_rows(values_only=True)
    col = {name: i for i, name in enumerate(next(rows))}
    deals = {}
    for r in rows:
        d = deals.setdefault(str(r[col["DealNumber"]]), {"names": [], "forms": [], "dates": [], "urls": []})
        for key, column in (("names", "TargetName"), ("forms", "FormType"), ("dates", "DateFiled"), ("urls", "URL")):
            v = r[col[column]]
            v = v.date().isoformat() if hasattr(v, "date") else str(v).strip() if v is not None else ""
            if v and v != "NA" and v not in d[key]:
                d[key].append(v)

    out = []
    for number, d in deals.items():
        good = [u for u in d["urls"] if INDEX_URL.match(u)]
        problems = []
        if len(good) != 1 or len(d["urls"]) != 1:
            problems.append("%d usable of %d links" % (len(good), len(d["urls"])))
        for key, label in (("names", "target names"), ("forms", "form types"), ("dates", "filing dates")):
            if len(d[key]) != 1:
                problems.append("%d %s" % (len(d[key]), label))
        out.append({
            "deal": slug(d["names"][0]) if d["names"] else "",
            "target_name": d["names"][0] if d["names"] else "",
            "deal_number": number,
            "form_type": d["forms"][0] if d["forms"] else "",
            "date_filed": d["dates"][0][:10] if d["dates"] else "",
            "index_url": good[0] if len(good) == 1 else "",
            "status": "ok" if not problems else "review: " + "; ".join(problems),
        })

    seen = {}
    for row in out:
        seen.setdefault(row["deal"], []).append(row)
    for name, same in seen.items():  # same target in two deals: tell them apart by filing year
        if len(same) > 1:
            for row in same:
                row["deal"] = "%s-%s" % (name, row["date_filed"][:4])
    names = [row["deal"] for row in out]
    assert len(names) == len(set(names)), "short names are not unique"

    out.sort(key=lambda row: row["deal"])
    with open(SEED, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(out)
    print("%d deals written to %s; %d need review" % (len(out), SEED.relative_to(ROOT), sum(r["status"] != "ok" for r in out)))


if __name__ == "__main__":
    main()
