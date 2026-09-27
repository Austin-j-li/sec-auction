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
            source.write_text(json.dumps({"ledger_schema": "v0", "checker_version": "v0", "issues": []}))
            with contextlib.redirect_stdout(io.StringIO()):
                findings_text.main(source, output)
            self.assertIn("Checker v0; v0 ledger rules", output.read_text())


if __name__ == "__main__":
    unittest.main()
