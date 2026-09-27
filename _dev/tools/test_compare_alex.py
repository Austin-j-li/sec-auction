"""The side-by-side with Alex's coding, on a synthetic ledger and a synthetic copy of his workbook."""
from __future__ import annotations

import contextlib
import csv
import datetime as dt
import io
import json
import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

import compare_alex
import derive_analysis as derive
from test_derive_analysis import D, FACTS, bid, row, rounds_line, write

ALEX_HEADER = [None, "TargetName", "gvkeyT", "DealNumber", "Acquirer", "gvkeyA", "DateAnnounced", "DateEffective", "DateFiled",
               "FormType", "URL", "Auction", "BidderID", "BidderName", "bidder_type_financial", "bidder_type_strategic",
               "bidder_type_mixed", "bidder_type_nonUS", "bidder_type_note", "bid_value", "bid_value_pershare", "bid_value_lower",
               "bid_value_upper", "bid_value_unit", "multiplier", "bid_type", "bid_date_precise", "bid_date_rough", "bid_note",
               "all_cash", "additional_note", "cshoc", "comments_1", "comments_2", "comments_3"]


def day(n):
    return dt.datetime.combine(D + dt.timedelta(days=n), dt.time())


def alex_row(number, bidder, when, note="NA", kind="NA", lo="NA", hi="NA", cash="NA", red=()):
    values = {"DealNumber": number, "BidderName": bidder, "bid_date_precise": when, "bid_date_rough": when, "bid_note": note,
              "bid_type": kind, "bid_value_lower": lo, "bid_value_upper": hi, "bid_value_pershare": lo, "all_cash": cash}
    return [values.get(h, "NA") for h in ALEX_HEADER], red


def alex_workbook(path: Path, rows) -> Path:
    wb = Workbook()
    ws = wb.active
    ws.title = "deal_details"
    ws.append(ALEX_HEADER)
    for values, red in rows:
        ws.append(values)
        for column in (ALEX_HEADER if red == "all" else red):
            ws.cell(ws.max_row, ALEX_HEADER.index(column) + 1).font = Font(color="FFFF0000")
    wb.save(path)
    return path


class CompareAlexTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.dir = Path(self.temp.name)
        ledger = [
            row(1, "Bank", "Adviser", rnd=0),
            bid(2, "Party A", 10, 12, day=1),
            bid(3, "5 IOI bidders", 8, 9, day=1, Count=5),
            row(4, "Party C", "Did not submit", day=2, Type="Financial", Count=1, **{"Exit reason": "Not stated"}),
            row(5, "Target", "Deadline", rnd=2, day=10),
            bid(6, "Party B", 19, rnd=2, day=10, formality="Formal", conditions="Heavy", **{"CVR/earnout": "Y", "CVR/earnout value": 2.5}),
            bid(7, "Party E", 23.81, rnd=2, day=11, conditions="Heavy"),
            row(8, "Party D", "Withdrew", rnd=2, day=12, Type="Financial", Count=1, **{"Exit reason": "Value below market price"}),
            row(9, "Party A", "Merger agreement signed", rnd=2, day=20, Type="Financial", Count=1),
        ]
        self.workbook = write(self.dir / "alpha.xlsx", ledger,
                              [rounds_line(1, "Enforced"), rounds_line(2, "Enforced", finality="Announced as final")], facts=FACTS)
        self.alex = alex_workbook(self.dir / "alex.xlsx", [
            alex_row(111, "Party A", day(1), kind="Informal", lo=10, hi=12, cash=1),
            alex_row(111, "Party B", day(10), kind="Formal", lo=21.5, hi=21.5, cash=0, red=("bid_type",)),
            alex_row(111, "Party E/F", day(11), kind="Informsl", lo=23.81, hi=23.81),
            alex_row(111, "5 parties", day(1), kind="Informal", lo=8, hi=9),
            alex_row(111, "Party Z", day(5), kind="Formal", lo=99, hi=99, red="all"),
            alex_row(111, "Bank", day(0), note="IB"),
            alex_row(111, "Party C", day(2), note="Drop", red=("comments_1",)),
            alex_row(111, "Party D", day(12), note="DropM"),
            alex_row(111, "NA", day(10), note="Final Round"),
            alex_row(111, "NA", day(10), note="Final Round Inf"),
            alex_row(111, "Party A", day(20), note="Executed"),
            alex_row(111, "Party Q", day(3), note="NDA"),
            alex_row(222, "Party A", day(1), kind="Formal", lo=10, hi=12),  # another deal
        ])
        self.seed = self.dir / "seed.csv"
        self.seed.write_text("deal,target_name,deal_number,form_type,date_filed,index_url,status\n"
                             "alpha,ALPHA,111,DEFM14A,2020-02-01,https://example.invalid,ok\n", encoding="utf-8")

    def tearDown(self): self.temp.cleanup()

    def test_bids_align_and_agreement_is_counted_per_reading(self):
        result = compare_alex.compare(self.workbook, "alpha", self.alex, self.seed, rules="v1.14")
        bids = {r["bidder_name"]: r for r in result["bids"]}
        self.assertEqual({k: (v.get("ledger_row"), v["alignment"], v.get("price_basis")) for k, v in bids.items()}, {
            "Party A": (2, "bidder, price, date", "upfront"),
            "Party B": (6, "bidder, price, date", "package"),
            "Party E/F": (7, "bidder (part of name), price, date", "upfront"),
            "5 parties": (3, "cohort size, price, date", "upfront"),
            "Party Z": (None, "unaligned", None)})
        summary = result["summary"]
        self.assertEqual((summary["alex_labelled_bids"], summary["aligned"]), (5, 4))
        self.assertEqual(summary["readings"]["T0"], {"agree": 4, "compared": 4, "missing": 0})
        self.assertEqual(summary["readings"]["T1"], {"agree": 3, "compared": 4, "missing": 0})
        self.assertEqual(bids["Party B"]["agree_all_cash"], "N")  # a CVR does not change all_cash in the ledger
        self.assertEqual(bids["Party B"]["per_share_match"], "package")
        self.assertEqual(bids["Party B"]["ledger_package_basis"], "upfront + CVR/earnout value (basis not stated in the Note)")
        # Under the v1.14.1 rules (the default for a 29-column workbook) E13 fixes the basis; nothing else here changes.
        default = compare_alex.compare(self.workbook, "alpha", self.alex, self.seed)
        self.assertEqual(default["summary"]["ledger_schema"], "v1.14.1")
        self.assertEqual(next(r for r in default["bids"] if r["bidder_name"] == "Party B")["ledger_package_basis"],
                         "upfront + CVR/earnout value (the stated per-share amount, the maximum where several; E13)")
        self.assertEqual(default["summary"]["readings"], summary["readings"])
        self.assertEqual(bids["Party E/F"]["bid_type"], "Informal")  # the "Informsl" typo
        self.assertEqual(bids["Party B"]["provenance"], "Alex: red-font correction")
        self.assertEqual(bids["Party Z"]["provenance"], "Alex: whole row in red (added or rewritten)")
        self.assertEqual(bids["Party A"]["provenance"], "Chicago coding (deal has no corrections)")
        self.assertEqual(summary["labelled_bids_with_red_bid_type"], 2)  # Party B, and Party Z's whole row
        party_c = next(r for r in result["events"] if r["bidder_name"] == "Party C")
        self.assertEqual(party_c["provenance"], "Alex: red comments only (coding as Chicago)")

    def test_bid_note_codes_follow_the_code_map(self):
        events = {(r["bidder_name"], r["bid_note"]): r for r in compare_alex.compare(self.workbook, "alpha", self.alex, self.seed)["events"]}
        status = {k: (v["status"], v.get("ledger_row")) for k, v in events.items() if k[1] != "NA"}
        self.assertEqual(status, {
            ("Bank", "IB"): ("agree", 1),
            ("Party C", "Drop"): ("exit, other label or reason", 4),
            ("Party D", "DropM"): ("agree", 8),
            ("", "Final Round"): ("agree", 5),
            ("", "Final Round Inf"): ("event agrees, round finality differs", 5),
            ("Party A", "Executed"): ("agree", 9),
            ("Party Q", "NDA"): ("unaligned", None)})
        self.assertEqual(events[("Party A", "NA")]["status"], "agree")

    def test_the_deal_is_joined_through_the_seed(self):
        with self.assertRaisesRegex(derive.DeriveError, "not in"):
            compare_alex.compare(self.workbook, "beta", self.alex, self.seed)

    def test_main_writes_only_its_three_files_into_a_new_folder(self):
        out = self.dir / "out"
        args = [str(self.workbook), "--deal", "alpha", "--out", str(out), "--alex", str(self.alex), "--seed", str(self.seed)]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(compare_alex.main(args), 0)
        self.assertEqual(sorted(p.name for p in out.iterdir()), ["alex_bids.csv", "alex_events.csv", "summary.json"])
        self.assertIn("never a target", json.loads((out / "summary.json").read_text())["note"])
        with (out / "alex_bids.csv").open(newline="", encoding="utf-8") as handle:
            self.assertEqual(len(list(csv.DictReader(handle))), 5)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(compare_alex.main(args), 2)  # refuses to overwrite


if __name__ == "__main__":
    unittest.main()
