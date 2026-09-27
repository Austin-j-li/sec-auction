#!/usr/bin/env python3
"""Recompute the questionnaire's 3.3(a) Formality-reading agreement table from the v1.14.1 retest.

Review aid only (V114_SPEC §9.5): never a target for the instruction, never shown to an extraction run.

It runs the live derive_analysis (0.3, --rules v1.14.1) on the Mac-Gray and P&W retest workbooks and aligns
Alex's labelled bids to their Bid rows with compare_alex.align, exactly as compare_alex.py does. Alex's labels are
not read from ref/: they are the alex_bids.csv tables that compare_alex.py wrote for the 24 September pilots
(bidder name, date, price, bid_type; ../../../maintenance/2026-09-24-bid-terms-taxonomy/analysis/compare-alex-*).
Those tables carry one date per bid (precise, else rough), so compare_alex's tie-break on the rough date is lost.
Writes formality_agreement.json and formality_agreement.csv next to this script.

    python3 _dev/reviews/2026-09-26-v1141-retest/analysis/formality_agreement.py
"""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "_dev/tools"))
import derive_analysis as derive  # noqa: E402
import compare_alex  # noqa: E402

HERE = Path(__file__).resolve().parent
PILOTS = ROOT / "_dev/maintenance/2026-09-24-bid-terms-taxonomy/analysis"
RUNS = {
    "mac-gray": ("opus55-medium-20260926-2019-1d1d60", "compare-alex-mac-gray-pilot-d7d267"),
    "providence-worcester": ("opus55-medium-20260926-2019-366a73", "compare-alex-providence-worcester-pilot-38bc24"),
}
READINGS = ("T0", "T1", "T1u", "T2", "T3")

summary, rows_out = {"note": __doc__.splitlines()[2], "derive_analysis": derive.TOOL_VERSION, "contract": derive.CONTRACT_VERSION, "deals": {}}, []
for deal, (version, pilot) in RUNS.items():
    workbook = ROOT / "_dev/cockpit/state/versions" / deal / version / f"{deal}.xlsx"
    ledger = derive.load(workbook, "v1.14.1")
    bids = derive.derive(ledger, deal)["bids"]
    with (PILOTS / pilot / "alex_bids.csv").open(newline="", encoding="utf-8") as handle:
        alex = [{"BidderName": r["bidder_name"], "bid_date_precise": r["alex_date"], "bid_date_rough": None,
                 "bid_value_lower": r["bid_value_lower"] or None, "bid_value_upper": r["bid_value_upper"] or None,
                 "bid_value_pershare": r["bid_value_pershare"] or None, "bid_type": r["bid_type"], "alex_row": r["alex_row"]}
                for r in csv.DictReader(handle)]
    aligned = compare_alex.align(bids, alex)
    tally = {t: {"agree": 0, "compared": 0} for t in READINGS}
    for i, row in enumerate(alex):
        out = {"deal": deal, "alex_row": row["alex_row"], "bidder_name": row["BidderName"], "alex_date": row["bid_date_precise"],
               "bid_type": row["bid_type"], "alignment": "unaligned"}
        if i in aligned:
            bid, how, basis, days = aligned[i]
            out.update(ledger_row=bid["row"], ledger_who=bid["who"], ledger_event=bid["event"], alignment=how,
                       price_basis=basis, date_gap_days=days, formality=bid.get("formality"), conditions=bid.get("conditions"))
            for t in READINGS:
                out[t] = bid[t]
                if bid[t]:
                    tally[t]["compared"] += 1
                    tally[t]["agree"] += bid[t] == row["bid_type"]
        rows_out.append(out)
    summary["deals"][deal] = {"workbook": str(workbook.relative_to(ROOT)), "workbook_sha256": derive.sha256(workbook),
                              "alex_labelled_bids": len(alex), "aligned": len(aligned), "readings": tally}

(HERE / "formality_agreement.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
fields = list(dict.fromkeys(k for r in rows_out for k in r))
with (HERE / "formality_agreement.csv").open("w", newline="", encoding="utf-8") as handle:
    w = csv.DictWriter(handle, fieldnames=fields); w.writeheader(); w.writerows(rows_out)
for deal, s in summary["deals"].items():
    print(deal, f"aligned {s['aligned']}/{s['alex_labelled_bids']}", {t: f"{v['agree']}/{v['compared']}" for t, v in s["readings"].items()})
