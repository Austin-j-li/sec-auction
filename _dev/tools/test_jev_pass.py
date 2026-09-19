#!/usr/bin/env python3
"""Tests for jev_pass.py with the model stubbed out (no network, no cached answers)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from openpyxl import Workbook

import check_lean
import jev_pass
from test_check_lean import build_valid_fixture

BODY = [
    "On January 2, the board of the target met and decided to request proposals from buyers.",
    "On January 3, Alpha submitted an offer of $10.00 per share in cash for all of the shares.",
    "On January 5, Beta signed a confidentiality agreement with the target. Beta later received access to the data room.",
    "On January 6, the target and Alpha continued to negotiate the draft merger agreement terms.",
    "On January 7, the board of the target met again with its advisers to review the process.",
    "On January 8, the target and Alpha signed the merger agreement and announced it publicly.",
]


def fixture(directory: Path) -> tuple[Path, Path]:
    filing = directory / "filing.htm"
    filing.write_text(
        "<html><body><p>Background of the Merger</p>"
        + "".join(f"<p>{t}</p>" for t in BODY)
        + "<p>Reasons for the Merger</p></body></html>",
        encoding="utf-8",
    )
    wb = Workbook()
    ws = wb.active
    ws.title = "Deal ledger"
    ws.append(["#", "When", "Who", "Event", "Price low", "Price high", "Note", "Quote and page", "Sort date"])
    ws.append([1, "January 3", "Alpha", "Bid", 12, None, None, "“Alpha submitted an offer of $10.00 per share” (p. 1)", "2020-01-03"])
    workbook = directory / "ledger.xlsx"
    wb.save(workbook)
    return workbook, filing


def fake_answers(state, questions):
    if "scoped" in questions:
        return {"scoped": {"choice": "contradicted", "confidence": 0.93}}
    if "match" in questions:
        beta = "Beta signed" in state["target_sentence"]
        return {"match": {"choice": "none" if beta else "row_2", "confidence": 0.95}}
    text = state.get("sentence") or state["paragraph"]
    return {k: {"noul": 0.9 if (k == "nda_access" and "Beta signed" in text) else 0.1} for k in questions}


class JevPassTests(unittest.TestCase):
    def test_flags_wrong_price_and_missing_event(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(jev_pass.Asker, "__call__", side_effect=fake_answers, autospec=False):
            workbook, filing = fixture(Path(tmp))
            result = jev_pass.run(workbook, filing, cache_dir=Path(tmp) / "cache", api_key="x")
        tiers = [i.get("tier") for i in result["issues"]]
        self.assertEqual(tiers, ["price_contradicted", "missing_top"])
        self.assertEqual(result["issues"][0]["row"], 2)
        self.assertIn("Beta signed", result["issues"][1]["message"])

    def test_no_key_and_empty_cache_skips_quietly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = fixture(Path(tmp))
            result = jev_pass.run(workbook, filing, cache_dir=Path(tmp) / "cache", api_key="")
        self.assertEqual({i["code"] for i in result["issues"]}, {"jev.skipped"})
        self.assertEqual(result["summary"]["new_api_calls"], 0)

    def test_filing_without_background_heading_skips(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = fixture(Path(tmp))
            filing.write_text("<html><body><p>" + BODY[0] + "</p></body></html>", encoding="utf-8")
            result = jev_pass.run(workbook, filing, cache_dir=Path(tmp) / "cache", api_key="")
        self.assertEqual([i["code"] for i in result["issues"]], ["jev.skipped"])

    def test_model_judgments_do_not_change_status_or_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_valid_fixture(Path(tmp))
            output = Path(tmp) / "report.json"
            lead = {"severity": "review", "code": "jev.price_contradicted", "sheet": "Deal ledger", "row": 2, "column": "Price low",
                    "message": "x", "basis": "jev", "confidence": 0.9, "tier": "price_contradicted"}
            with mock.patch.object(jev_pass, "run", return_value={"issues": [lead], "summary": {"model_judgments": 1}}):
                code = check_lean.main(["--workbook", str(workbook), "--filing", str(filing), "--output", str(output), "--jev", "on"])
            report = json.loads(output.read_text())
        self.assertEqual(code, 0)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["issues"][0]["basis"], "jev")

    def test_broken_jev_module_still_writes_the_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_valid_fixture(Path(tmp))
            output = Path(tmp) / "report.json"
            with mock.patch.dict("sys.modules", {"jev_pass": None}):
                code = check_lean.main(["--workbook", str(workbook), "--filing", str(filing), "--output", str(output), "--jev", "on"])
            report = json.loads(output.read_text())
        self.assertEqual(code, 0)
        self.assertEqual([i["code"] for i in report["issues"]], ["jev.skipped"])
        self.assertEqual(report["summary"]["total_issues"], 1)


if __name__ == "__main__":
    unittest.main()
