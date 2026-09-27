"""Synthetic regression checks for workbook comparisons and revision findings."""

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from openpyxl import Workbook

import diff_workbooks
import findings_text


class ReviewHelperTests(unittest.TestCase):
    def test_workbook_diff_reports_number_to_text_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            before, after = Path(tmp) / "before.xlsx", Path(tmp) / "after.xlsx"
            wb = Workbook()
            wb.active.append(["Round"])
            wb.active.append([1])
            wb.save(before)
            wb.active["A2"] = "1"
            wb.save(after)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                diff_workbooks.main(before, after)
            self.assertIn("1 [number]", output.getvalue())
            self.assertIn("1 [text]", output.getvalue())
            self.assertIn("Total: 1 change(s)", output.getvalue())

    def test_workbook_diff_reports_an_added_trailing_column(self):
        with tempfile.TemporaryDirectory() as tmp:
            before, after = Path(tmp) / "before.xlsx", Path(tmp) / "after.xlsx"
            wb = Workbook()
            wb.active.append(["Round"])
            wb.active.append([1])
            wb.save(before)
            wb.active["B1"] = "New field"
            wb.active["B2"] = "New value"
            wb.save(after)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                diff_workbooks.main(before, after)
            self.assertIn("New field [text]", output.getvalue())
            self.assertIn("New value [text]", output.getvalue())

    def test_findings_keep_warnings_as_review_leads(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / "report.json", Path(tmp) / "findings.md"
            source.write_text(json.dumps({"issues": [
                {"severity": "warning", "basis": "mechanical", "message": "Required note may exceed target"},
                {"severity": "error", "basis": "mechanical", "message": "Invalid event label"},
            ]}))
            with contextlib.redirect_stdout(io.StringIO()):
                findings_text.main(source, output)
            text = output.read_text()
            self.assertLess(text.index("Invalid event label"), text.index("Required note"))
            self.assertIn("warning; mechanical review lead", text)
            self.assertIn("Checker version not recorded; ledger rules not recorded", text)
            self.assertNotIn("certain", text)

    def test_crosswalk_aligns_old_cash_with_new_stock(self):
        with tempfile.TemporaryDirectory() as tmp:
            before, after = Path(tmp) / "old.xlsx", Path(tmp) / "new.xlsx"
            wb = Workbook()
            ws = wb.active
            ws.title = "Deal ledger"
            ws.append(["#", "Event", "Who", "Sort date", "All cash"])
            ws.append([1, "Bid", "A", "2020-01-01", "Yes"])
            wb.save(before)
            ws["E1"] = "Stock %"
            ws["E2"] = 0
            ws["F1"] = "Financing"
            ws["F2"] = "Contingent"
            wb.save(after)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                diff_workbooks.main(before, after, crosswalk_on=True)
            result = output.getvalue()
            self.assertIn("Financing", result)
            self.assertNotIn("row 2 -> 2, Stock %", result)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                diff_workbooks.main(after, before, crosswalk_on=True)
            self.assertNotIn("row 2 -> 2, All cash", output.getvalue())

    def test_crosswalk_shows_equal_price_with_new_cvr_basis(self):
        with tempfile.TemporaryDirectory() as tmp:
            before, after = Path(tmp) / "old.xlsx", Path(tmp) / "new.xlsx"
            wb = Workbook()
            ws = wb.active
            ws.title = "Deal ledger"
            ws.append(["Event", "Who", "Sort date", "Price low", "Price high", "All cash"])
            ws.append(["Bid", "A", "2020-01-01", 10, 10, "Yes"])
            wb.save(before)
            ws["F1"] = "Stock %"
            ws["F2"] = 0
            ws["G1"] = "CVR/earnout"
            ws["G2"] = "Y"
            wb.save(after)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                diff_workbooks.main(before, after, crosswalk_on=True)
            result = output.getvalue()
            self.assertIn("row 2 -> 2, Price low", result)
            self.assertIn("row 2 -> 2, Price high", result)
            self.assertIn("price basis may exclude separately reported contingent value", result)

    def test_crosswalk_counts_blank_other_scope_prices_in_both_directions(self):
        with tempfile.TemporaryDirectory() as tmp:
            before, after = Path(tmp) / "old.xlsx", Path(tmp) / "new.xlsx"
            wb = Workbook()
            ws = wb.active
            ws.title = "Deal ledger"
            ws.append(["Event", "Who", "Sort date", "Price low", "Price high", "All cash"])
            ws.append(["Other-scope bid", "A", "2020-01-01", 10, 10, "Yes"])
            wb.save(before)
            ws["F1"] = "Stock %"
            ws["F2"] = None
            ws["D2"] = None
            ws["E2"] = None
            wb.save(after)
            for first, second in ((before, after), (after, before)):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    diff_workbooks.main(first, second, crosswalk_on=True)
                result = output.getvalue()
                self.assertIn("D18: 2 blank Other-scope price cell(s) counted, not listed", result)
                self.assertNotIn("row 2 -> 2, Price low", result)
                self.assertNotIn("row 2 -> 2, Price high", result)

    def test_crosswalk_marks_wider_deadline_choice_in_both_directions(self):
        with tempfile.TemporaryDirectory() as tmp:
            before, after = Path(tmp) / "old.xlsx", Path(tmp) / "new.xlsx"
            wb = Workbook()
            ledger = wb.active
            ledger.title = "Deal ledger"
            ledger.append(["Event", "All cash"])
            rounds = wb.create_sheet("Rounds")
            rounds.append(["Process", "Round", "Deadline outcome"])
            rounds.append([1, 1, "Late bids accepted"])
            rounds.append([1, 2, "Enforced"])
            wb.save(before)
            ledger["B1"] = "Stock %"
            rounds["C2"] = "Extended (late bid accepted)"
            wb.save(after)
            for first, second in ((before, after), (after, before)):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    diff_workbooks.main(first, second, crosswalk_on=True)
                self.assertIn("crosswalk: D11 (wider)", output.getvalue())
                self.assertNotIn("row 3 -> 3, Deadline outcome", output.getvalue())

    def test_by_quote_uses_primary_key_then_unique_passage(self):
        with tempfile.TemporaryDirectory() as tmp:
            before, after = Path(tmp) / "before.xlsx", Path(tmp) / "after.xlsx"
            wb = Workbook()
            ws = wb.active
            ws.title = "Deal ledger"
            ws.append(["Event", "Who", "Sort date", "Quote and page"])
            ws.append(["Bid", "A", "2020-01-01", "The bidder sent a cash proposal. Page 3"])
            ws.append(["Contact", "B", "2020-01-02", "The board held a meeting about the sale. Page 4"])
            ws.append(["Contact", "C", "2020-01-03", "Repeated passage. Page 5"])
            ws.append(["Contact", "D", "2020-01-04", "Repeated passage. Page 5"])
            wb.save(before)
            ws["D2"] = "The bidder sent a revised cash proposal. Page 3"
            ws["A3"] = "Meeting"
            ws["D3"] = "The board held a meeting about the sale. Page 4, later corrected"
            ws["A4"] = "Meeting"
            ws["A5"] = "Meeting"
            wb.save(after)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                diff_workbooks.main(before, after, by_quote=True)
            result = output.getvalue()
            self.assertIn("row 2 -> 2, Quote and page", result)
            self.assertIn("row 3 -> 3, Event", result)
            self.assertIn("removed row 4", result)
            self.assertIn("removed row 5", result)
            self.assertIn("added row 4", result)
            self.assertIn("added row 5", result)

    def test_findings_name_rules_when_report_records_them(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / "report.json", Path(tmp) / "findings.md"
            source.write_text(json.dumps({"ledger_schema": "v1.14.1", "checker_version": "1.8", "issues": []}))
            with contextlib.redirect_stdout(io.StringIO()):
                findings_text.main(source, output)
            self.assertIn("Checker 1.8; v1.14.1 ledger rules", output.read_text())


if __name__ == "__main__":
    unittest.main()
