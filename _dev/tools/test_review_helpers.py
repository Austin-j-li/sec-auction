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
            self.assertNotIn("certain", text)


if __name__ == "__main__":
    unittest.main()
