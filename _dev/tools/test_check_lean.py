#!/usr/bin/env python3
"""Small synthetic-fixture tests for check_lean.py (no candidate workbooks)."""

from __future__ import annotations

import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment

import check_lean


QUOTES = [
    "On January 2, the target requested proposals.",
    "On January 3, Alpha submitted an offer of $10 per share.",
    "On January 4, the target signed the merger agreement.",
]


def finish_sheet(ws, width: int) -> None:
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{ws.cell(1, width).column_letter}{max(ws.max_row, 1)}"
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=width):
        for cell in row:
            if cell.value is not None:
                cell.alignment = Alignment(wrap_text=True)


def build_valid_fixture(directory: Path) -> tuple[Path, Path]:
    filing = directory / "filing.htm"
    filing.write_text(
        "<html><body>"
        f"<p>{QUOTES[0]}</p>"
        "<p>On January 3, Alpha submitted an offer of $<b>10</b> per share.</p>"
        f"<p>{QUOTES[2]}</p>"
        "</body></html>",
        encoding="utf-8",
    )

    workbook = directory / "valid.xlsx"
    wb = Workbook()
    ledger = wb.active
    ledger.title = "Deal ledger"
    ledger.append(check_lean.LEDGER_COLUMNS)
    rows = [
        [
            1,
            "01/02/2020",
            "Target",
            None,
            "Round opened",
            1,
            1,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "Requested proposals from Alpha.",
            f"\u201c{QUOTES[0]}\u201d (p. 10)",
            "Q1",
            None,
            dt.date(2020, 1, 2),
            dt.date(2020, 1, 2),
            dt.date(2020, 1, 2),
        ],
        [
            2,
            "01/03/2020",
            "Alpha",
            "Strategic",
            "Bid",
            1,
            1,
            10,
            10,
            "Yes",
            "Informal",
            "Unclear",
            1,
            None,
            None,
            "Preliminary bid before an NDA.",
            f"\u201c{QUOTES[1]}\u201d (p. 10)",
            "Q1",
            None,
            dt.date(2020, 1, 3),
            dt.date(2020, 1, 3),
            dt.date(2020, 1, 3),
        ],
        [
            3,
            "01/04/2020",
            "Target",
            None,
            "Merger agreement signed",
            1,
            1,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "$10 per share, all cash.",
            f"\u201c{QUOTES[2]}\u201d (p. 10)",
            "Q1",
            None,
            dt.date(2020, 1, 4),
            dt.date(2020, 1, 4),
            dt.date(2020, 1, 4),
        ],
    ]
    for row in rows:
        ledger.append(row)
    for row in range(2, 5):
        for column in (20, 21, 22):
            ledger.cell(row, column).number_format = "MM/DD/YYYY"
    finish_sheet(ledger, len(check_lean.LEDGER_COLUMNS))

    rounds = wb.create_sheet("Rounds")
    rounds.append(check_lean.ROUND_COLUMNS)
    rounds.append(
        [
            1,
            1,
            dt.date(2020, 1, 2),
            "Target requested proposals.",
            "1 strategic: Alpha",
            "none stated",
            "No deadline stated",
            "Not final",
            "1: Alpha",
            "Signing",
        ]
    )
    rounds["C2"].number_format = "MM/DD/YYYY"
    finish_sheet(rounds, len(check_lean.ROUND_COLUMNS))

    questions = wb.create_sheet("Questions")
    questions.append(check_lean.QUESTION_COLUMNS)
    questions.append(
        [
            "Q1",
            "Is one process and one round the best map?",
            "Yes; retain one process and one round.",
            "The target requested proposals once before signing (p. 10).",
            "Rows 1-3",
            "A different answer would move all three rows.",
            None,
        ]
    )
    finish_sheet(questions, len(check_lean.QUESTION_COLUMNS))

    facts = wb.create_sheet("Deal facts")
    facts.append(check_lean.FACT_COLUMNS)
    fact_values = [
        "Target",
        "Alpha",
        "Strategic",
        "$10 per share in cash",
        "01/04/2020",
        "01/04/2020",
        "DEFM14A filed 01/10/2020",
        "10",
        "target-led",
        1,
        "None reported",
        "Not met: 0 qualifying NDAs",
        "Yes",
        "US dollars per share",
        "Bank",
        "Law Firm",
        "The target opened one round. Alpha submitted one bid. The offer was all cash. The target selected Alpha. The parties signed on January 4.",
    ]
    for field, value in zip(check_lean.FACT_FIELDS, fact_values, strict=True):
        facts.append([field, value])
    finish_sheet(facts, len(check_lean.FACT_COLUMNS))

    wb.save(workbook)
    return workbook, filing


V114_BID_TERMS = {
    "Stock %": 0,
    "Due diligence": "Not begun",  # the bid came before an NDA (E12)
    "Financing": "Not stated",
    "Regulatory": "Not stated",
    "Exclusivity": "Not stated",
}


def build_v114_fixture(directory: Path) -> tuple[Path, Path]:
    """The valid fixture with its ledger rewritten in the v1.14 column order."""
    workbook, filing = build_valid_fixture(directory)
    wb = check_lean.openpyxl.load_workbook(workbook)
    old = wb["Deal ledger"]
    records = [dict(zip(check_lean.LEDGER_COLUMNS, row)) for row in old.iter_rows(min_row=2, values_only=True)]
    index = wb.sheetnames.index("Deal ledger")
    wb.remove(old)
    ledger = wb.create_sheet("Deal ledger", index)
    ledger.append(check_lean.LEDGER_COLUMNS_V114)
    for record in records:
        if record["Event"] in check_lean.BID_EVENTS:
            record.update(V114_BID_TERMS)
        ledger.append([record.get(column) for column in check_lean.LEDGER_COLUMNS_V114])
    dates = [check_lean.LEDGER_COLUMNS_V114.index(name) + 1 for name in check_lean.DATE_COLUMNS]
    for row in range(2, ledger.max_row + 1):
        for column in dates:
            ledger.cell(row, column).number_format = "MM/DD/YYYY"
    finish_sheet(ledger, len(check_lean.LEDGER_COLUMNS_V114))
    wb.save(workbook)
    return workbook, filing


def set_ledger(workbook: Path, row: int, values: dict) -> None:
    wb = check_lean.openpyxl.load_workbook(workbook)
    ws = wb["Deal ledger"]
    header = [cell.value for cell in ws[1]]
    for column, value in values.items():
        cell = ws.cell(row, header.index(column) + 1)
        cell.value = value
        cell.alignment = Alignment(wrap_text=True)
    wb.save(workbook)


def append_ledger(workbook: Path, records: list[dict]) -> None:
    """Append ledger rows (quoting a passage the fixture filing contains) with dated cells formatted."""
    wb = check_lean.openpyxl.load_workbook(workbook)
    ws = wb["Deal ledger"]
    header = [cell.value for cell in ws[1]]
    for values in records:
        day = values.pop("day")
        row = {"#": ws.max_row, "When": f"{day:%m/%d/%Y}", "Process": 1, "Round": 1, "Note": "Synthetic row.",
               "Quote and page": f"\u201c{QUOTES[2]}\u201d (p. 10)", **{name: day for name in check_lean.DATE_COLUMNS}, **values}
        ws.append([row.get(name) for name in header])
        for name in check_lean.DATE_COLUMNS:
            ws.cell(ws.max_row, header.index(name) + 1).number_format = "MM/DD/YYYY"
    finish_sheet(ws, len(header))
    wb.save(workbook)


def set_rounds(workbook: Path, values: dict) -> None:
    wb = check_lean.openpyxl.load_workbook(workbook)
    ws = wb["Rounds"]
    for column, value in values.items():
        cell = ws.cell(2, check_lean.ROUND_COLUMNS.index(column) + 1)
        cell.value = value
        cell.alignment = Alignment(wrap_text=True)
    wb.save(workbook)


def issue_set(workbook: Path, filing: Path, rules: str = "v1.14") -> set[tuple[str, str]]:
    return {(issue["code"], issue["severity"]) for issue in check_lean.LeanChecker(workbook, filing, rules=rules).run()["issues"]}


class LeanCheckerTests(unittest.TestCase):
    def test_valid_minimal_fixture_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_valid_fixture(Path(tmp))
            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            self.assertEqual(report["status"], "pass", report["issues"])
            self.assertEqual(report["summary"]["errors"], 0)

    def test_qualified_bid_cohort_keeps_count_blank_without_hiding_omissions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_valid_fixture(Path(tmp))
            cases = [
                ("Count: at least 11; the filing supplies only a lower bound.", "warning"),
                ("Count: approximately 20.", "warning"),
                ("Count: 11–14.", "warning"),
                ("Count: unknown; the filing does not number these bidders.", "warning"),
                ("The price was approximately $10 per share.", "error"),
                ("", "error"),
            ]
            for note, expected_severity in cases:
                with self.subTest(note=note):
                    wb = check_lean.openpyxl.load_workbook(workbook)
                    wb["Deal ledger"]["C3"] = "Financial bidder cohort"
                    wb["Deal ledger"]["M3"] = None
                    wb["Deal ledger"]["P3"] = note
                    wb.save(workbook)
                    report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
                    count_issues = [
                        issue for issue in report["issues"]
                        if issue["code"] in {"ledger.count_bidder", "ledger.count_uncertain"}
                    ]
                    self.assertEqual(len(count_issues), 1, report["issues"])
                    self.assertEqual(count_issues[0]["severity"], expected_severity)
                    if expected_severity == "warning":
                        self.assertEqual(report["summary"]["errors"], 0, report["issues"])

    def test_required_bid_details_over_note_target_are_a_review_lead(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_valid_fixture(Path(tmp))
            wb = check_lean.openpyxl.load_workbook(workbook)
            wb["Deal ledger"]["P3"] = (
                "Six-week diligence period; financing not committed. The proposal requested "
                "exclusive negotiations through February 14 and a management presentation "
                "before final approval. Price carried from #1; reaffirmed by returned draft. "
                "The filing reports a reference closing price of $8 on January 2 and a "
                "25 percent premium to that price."
            )
            wb.save(workbook)
            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            issues = {issue["code"]: issue["severity"] for issue in report["issues"]}
            self.assertEqual(issues["ledger.note_length"], "warning")
            self.assertEqual(report["summary"]["errors"], 0, report["issues"])

    def test_future_deadline_has_no_outcome_but_reached_deadline_requires_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_valid_fixture(Path(tmp))
            wb = check_lean.openpyxl.load_workbook(workbook)
            wb["Rounds"]["F2"] = "01/20/2020 (future at filing)"
            wb["Rounds"]["G2"] = None
            wb["Rounds"]["J2"] = "Bidding remains open at filing."
            wb.save(workbook)
            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            self.assertEqual(report["summary"]["errors"], 0, report["issues"])

            wb["Deal ledger"]["E4"] = "Deadline"
            wb.save(workbook)
            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            self.assertIn("rounds.deadline_count", {issue["code"] for issue in report["issues"]})

    def test_unknown_auction_count_and_no_deadline_pair(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_valid_fixture(Path(tmp))
            wb = check_lean.openpyxl.load_workbook(workbook)
            wb["Deal facts"]["B13"] = "Uncertain: count unknown"
            wb.save(workbook)
            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            self.assertEqual(report["summary"]["errors"], 0, report["issues"])

            wb["Rounds"]["G2"] = None
            wb.save(workbook)
            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            self.assertIn("rounds.no_deadline_pair", {issue["code"] for issue in report["issues"]})

    def test_exact_day_and_inferred_exit_cross_checks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_valid_fixture(Path(tmp))
            wb = check_lean.openpyxl.load_workbook(workbook)
            ledger = wb["Deal ledger"]
            header = [cell.value for cell in ledger[1]]
            col = {name: index + 1 for index, name in enumerate(header)}
            target = next(
                row for row in range(2, ledger.max_row + 1)
                if isinstance(ledger.cell(row, col["When"]).value, str)
                and check_lean.re.fullmatch(r"\d{2}/\d{2}/\d{4}", ledger.cell(row, col["When"]).value)
            )
            sort_day = ledger.cell(target, col["Sort date"]).value
            ledger.cell(target, col["Date from"]).value = sort_day - dt.timedelta(days=1)
            ledger.cell(target, col["Event"]).value = "Withdrew"
            ledger.cell(target, col["Inferred"]).value = "Y"
            ledger.cell(target, col["Exit reason"]).value = "Terms or process"
            wb.save(workbook)
            issues = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()["issues"]
            found = {(issue["code"], issue["severity"]) for issue in issues}
            self.assertIn(("date.exact_day_mismatch", "error"), found)
            self.assertIn(("exit.inferred_reason", "warning"), found)

    def test_v114_inferred_exit_may_carry_a_reported_reason(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v114_fixture(Path(tmp))
            day = dt.date(2020, 1, 4)
            set_ledger(workbook, 4, {
                "Who": "Alpha", "Event": "Withdrew", "Inferred": "Y", "Exit reason": "Terms or process",
                "Date from": day - dt.timedelta(days=1),
            })
            found = issue_set(workbook, filing)
            self.assertIn(("date.exact_day_mismatch", "error"), found)
            self.assertNotIn("exit.inferred_reason", {code for code, _ in found})

    def test_important_failures_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_valid_fixture(Path(tmp))
            wb = check_lean.openpyxl.load_workbook(workbook)
            ledger = wb["Deal ledger"]
            ledger["E3"] = "Invented event"
            ledger["T3"] = "01/03/2020"
            ledger["T4"] = dt.date(2020, 1, 1)
            ledger["Q4"] = "\u201cOn January 4 ... merger agreement.\u201d (p. 10)"
            wb["Questions"]["E2"] = "Rows 1-99"
            wb.save(workbook)

            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            codes = {issue["code"] for issue in report["issues"]}
            self.assertEqual(report["status"], "fail")
            self.assertIn("controlled.event", codes)
            self.assertIn("date.not_excel_date", codes)
            self.assertIn("date.sort_outside_window", codes)
            self.assertIn("date.sort_decreases", codes)
            self.assertIn("quote.not_contiguous_in_filing", codes)
            self.assertIn("questions.unknown_row", codes)

    def test_malformed_required_sheet_fails_gracefully(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_valid_fixture(Path(tmp))
            wb = check_lean.openpyxl.load_workbook(workbook)
            wb["Deal ledger"]["A1"] = "Wrong header"
            wb.save(workbook)

            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            self.assertEqual(report["status"], "fail")
            self.assertIn("schema.columns", {issue["code"] for issue in report["issues"]})

    def test_account_and_quote_wrapper_variants_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_valid_fixture(Path(tmp))
            wb = check_lean.openpyxl.load_workbook(workbook)
            ledger = wb["Deal ledger"]
            ledger["Q2"] = f"{QUOTES[0]} (p. 10)"
            ledger["Q3"] = f"\u201c{QUOTES[1]} (pp. 10\u201311)\u201d"
            ledger["Q4"] = f'"{QUOTES[2]}" p. 10'
            wb["Deal facts"]["A18"] = "Account (five or six plain sentences)"
            wb.save(workbook)

            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            self.assertEqual(report["status"], "pass", report["issues"])

    def test_deal_fact_guidance_labels_and_explanations_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_valid_fixture(Path(tmp))
            wb = check_lean.openpyxl.load_workbook(workbook)
            facts = wb["Deal facts"]
            facts["B4"] = "Strategic - operating-company acquirer"
            facts["A10"] = "Initiation (target-led, bidder-led, activist-influenced, mixed or unclear)"
            facts["B10"] = "Target-led - the board initiated outreach"
            facts["B11"] = 1
            facts["A12"] = "Earlier approaches (E5; “None reported” if none)"
            facts["A13"] = "Auction screen (E1)"
            facts["A14"] = "Whole-company bids (Yes, or No with what was bid for)"
            wb.save(workbook)

            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            self.assertEqual(report["status"], "pass", report["issues"])

    def test_superseded_deal_fact_labels_are_rejected(self) -> None:
        for cell, label in (("A13", "Auction screen (C1)"), ("A12", "Earlier approaches (C7)")):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                workbook, filing = build_valid_fixture(Path(tmp))
                wb = check_lean.openpyxl.load_workbook(workbook)
                wb["Deal facts"][cell] = label
                wb.save(workbook)
                report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
                self.assertEqual(report["status"], "fail")
                self.assertIn("facts.fields", {issue["code"] for issue in report["issues"]})

    def test_missing_earlier_approaches_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_valid_fixture(Path(tmp))
            wb = check_lean.openpyxl.load_workbook(workbook)
            wb["Deal facts"].delete_rows(12)
            wb.save(workbook)
            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            self.assertEqual(report["status"], "fail")
            self.assertIn("facts.fields", {issue["code"] for issue in report["issues"]})

    def test_date_formatted_process_count_is_not_silently_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_valid_fixture(Path(tmp))
            wb = check_lean.openpyxl.load_workbook(workbook)
            wb["Deal facts"]["B11"] = 1
            wb["Deal facts"]["B11"].number_format = "MM/DD/YYYY"
            wb.save(workbook)
            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            self.assertEqual(report["status"], "fail")
            self.assertIn("facts.process_count", {issue["code"] for issue in report["issues"]})

    def test_multiple_flags_and_link_mismatches_are_review_leads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_valid_fixture(Path(tmp))
            wb = check_lean.openpyxl.load_workbook(workbook)
            wb["Deal ledger"]["R3"] = "Q1, Q2"
            questions = wb["Questions"]
            questions.append(
                [
                    "Q2",
                    "Is Alpha's classification supported?",
                    "Yes; retain the classification.",
                    "The filing describes Alpha as an operating company (p. 10).",
                    "Rows 1",
                    "A different answer would change Alpha's Type.",
                    None,
                ]
            )
            finish_sheet(questions, len(check_lean.QUESTION_COLUMNS))
            wb.save(workbook)

            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            issues = {issue["code"]: issue["severity"] for issue in report["issues"]}
            self.assertEqual(report["status"], "pass_with_warnings", report["issues"])
            self.assertEqual(issues["questions.flag_mismatch"], "warning")
            self.assertEqual(issues["questions.reverse_link"], "warning")
            self.assertNotIn("controlled.flag", issues)

            wb = check_lean.openpyxl.load_workbook(workbook)
            wb["Deal ledger"]["R3"] = "Q1, Q9"
            wb.save(workbook)
            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            errors = {
                issue["code"] for issue in report["issues"] if issue["severity"] == "error"
            }
            self.assertIn("questions.unknown_flag", errors)

    def test_missing_sheets_fail_gracefully(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            filing = directory / "filing.htm"
            filing.write_text("<p>Source text.</p>", encoding="utf-8")
            workbook = directory / "malformed.xlsx"
            Workbook().save(workbook)

            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            self.assertEqual(report["status"], "fail")
            self.assertEqual(report["issues"][0]["code"], "schema.sheets")

    def test_v114_fixture_passes_and_reports_its_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v114_fixture(Path(tmp))
            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            self.assertEqual(report["status"], "pass", report["issues"])
            self.assertEqual(report["ledger_schema"], "v1.14")
            workbook, filing = build_valid_fixture(Path(tmp))
            self.assertEqual(check_lean.LeanChecker(workbook, filing, rules="v1.14").run()["ledger_schema"], "v1.13.2")

    def test_v114_value_lists_and_consistency_rules(self) -> None:
        cases = [
            ({"Stock %": "abc"}, "controlled.stock_pct", "error"),
            ({"Stock %": "40"}, "controlled.stock_pct", "error"),
            ({"Stock %": 120}, "controlled.stock_pct", "error"),
            ({"Stock %": "75-50"}, "controlled.stock_pct", "error"),
            ({"Stock %": None}, "controlled.stock_pct", "error"),
            ({"Due diligence": None}, "controlled.due_diligence", "error"),
            ({"Financing": "Highly confident"}, "controlled.financing", "error"),
            ({"CVR/earnout": "Yes"}, "controlled.cvr_earnout", "error"),
            ({"CVR/earnout value": 1.13}, "bid.cvr_value_marker", "error"),
            ({"CVR/earnout": "Varies", "CVR/earnout value": 1.13}, "bid.cvr_value_marker", "error"),
            ({"Financing": "Contingent", "Conditions": "Light"}, "conditions.financing_heavy", "error"),
            ({"Conditions": "None", "Due diligence": "Incomplete", "Financing": "Committed"}, "conditions.none_support", "error"),
            ({"Exclusivity": "Varies"}, "bid.varies_single", "error"),
            ({"Antitrust": "Y"}, "conditions.antitrust_regulatory", "error"),
            ({"Regulatory": "Concern", "Conditions": "None", "Due diligence": "Complete", "Financing": "Committed"}, "conditions.none_support", "error"),
            ({"Event": "Other-scope bid"}, "bid.other_scope_per_share", "error"),
            ({"Event": "Other-scope bid", "Price low": None, "Price high": None, "CVR/earnout": "Y", "CVR/earnout value": 1.13}, "bid.other_scope_per_share", "error"),
            ({"Event": "Other-scope bid", "Price low": None, "Price high": None, "Note": None}, "bid.other_scope_note", "warning"),
            ({"Due diligence": "Not stated", "Conditions": "Heavy"}, "conditions.level_unsupported", "warning"),
        ]
        for values, code, severity in cases:
            with self.subTest(values=values):
                with tempfile.TemporaryDirectory() as tmp:
                    workbook, filing = build_v114_fixture(Path(tmp))
                    set_ledger(workbook, 3, values)
                    report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
                    found = {(issue["code"], issue["severity"]) for issue in report["issues"]}
                    self.assertIn((code, severity), found, report["issues"])

    def test_v114_accepts_ranges_codes_and_contingent_payments(self) -> None:
        accepted = [
            {"Stock %": "50\u201375"},
            {"Stock %": 33.3},
            {"Stock %": "Part stock"},
            {"CVR/earnout": "Y", "CVR/earnout value": 1.13},
            {"Regulatory": "Concern", "Antitrust": "Y"},
            {"Financing": "Contingent", "Conditions": "Heavy"},
            {"Conditions": "None", "Due diligence": "Complete", "Financing": "Not needed", "Regulatory": "No concern"},
        ]
        for values in accepted:
            with self.subTest(values=values):
                with tempfile.TemporaryDirectory() as tmp:
                    workbook, filing = build_v114_fixture(Path(tmp))
                    set_ledger(workbook, 3, values)
                    report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
                    self.assertEqual(report["status"], "pass", report["issues"])

    def test_v114_terms_must_be_blank_on_other_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v114_fixture(Path(tmp))
            set_ledger(workbook, 4, {"Financing": "Committed"})
            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            codes = {(issue["code"], issue["column"]) for issue in report["issues"]}
            self.assertIn(("bid.fields_on_nonbid", "Financing"), codes, report["issues"])

    def test_v114_markers_and_exclusivity_add_no_issue_at_any_level(self) -> None:
        levels = {
            "None": {"Conditions": "None", "Due diligence": "Complete", "Financing": "Committed", "Regulatory": "No concern"},
            "Light": {"Conditions": "Light"},
            "Heavy": {"Conditions": "Heavy"},
            "Unclear": {"Conditions": "Unclear"},
        }
        extras = [
            {"CVR/earnout": "Y", "CVR/earnout value": 1.13},
            *({"Exclusivity": value} for value in ("Required", "Requested", "Not stated")),
        ]
        for level, base in levels.items():
            for extra in extras:
                with self.subTest(level=level, extra=extra), tempfile.TemporaryDirectory() as tmp:
                    workbook, filing = build_v114_fixture(Path(tmp))
                    set_ledger(workbook, 3, base)
                    before = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()["issues"]
                    set_ledger(workbook, 3, extra)
                    after = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()["issues"]
                    self.assertEqual(before, after)
                    self.assertEqual(after, [], after)

    def test_v114_concern_and_cohort_financing_pass_where_allowed(self) -> None:
        accepted = [
            *({"Regulatory": "Concern", "Conditions": level} for level in ("Light", "Heavy", "Unclear")),
            {"Who": "Two financial bidders", "Count": 2, "Financing": "Varies", "Conditions": "Unclear"},
        ]
        for values in accepted:
            with self.subTest(values=values), tempfile.TemporaryDirectory() as tmp:
                workbook, filing = build_v114_fixture(Path(tmp))
                set_ledger(workbook, 3, values)
                report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
                self.assertEqual(report["status"], "pass", report["issues"])

    def test_other_scope_per_share_cells_are_v114_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v114_fixture(Path(tmp))
            set_ledger(workbook, 3, {"Event": "Other-scope bid", "Price low": None, "Price high": None})
            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            self.assertEqual(report["status"], "pass", report["issues"])
            workbook, filing = build_valid_fixture(Path(tmp))
            wb = check_lean.openpyxl.load_workbook(workbook)
            wb["Deal ledger"]["E3"] = "Other-scope bid"
            wb.save(workbook)
            report = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()
            self.assertEqual(report["status"], "pass", report["issues"])

    def test_other_scope_price_high_alone_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v114_fixture(Path(tmp))
            set_ledger(workbook, 3, {"Event": "Other-scope bid", "Price low": None, "Price high": 10, "Note": "Ceiling of $10 for the segment."})
            issues = check_lean.LeanChecker(workbook, filing, rules="v1.14").run()["issues"]
            found = [(issue["code"], issue["severity"], issue["column"]) for issue in issues if issue["code"] == "bid.other_scope_per_share"]
            self.assertEqual(found, [("bid.other_scope_per_share", "error", "Price high")], issues)

    def test_deadline_outcome_sets_follow_the_schema(self) -> None:
        cases = [
            (build_v114_fixture, "Extended (late bid accepted)", set(), {"controlled.deadline_outcome", "rounds.deadline_outcome_legacy"}),
            (build_v114_fixture, "Late bids accepted", {("rounds.deadline_outcome_legacy", "warning")}, {"controlled.deadline_outcome", "rounds.deadline_count"}),
            (build_v114_fixture, "Enforced", set(), {"controlled.deadline_outcome", "rounds.deadline_outcome_legacy"}),
            (build_valid_fixture, "Late bids accepted", set(), {"controlled.deadline_outcome", "rounds.deadline_outcome_legacy"}),
            (build_valid_fixture, "Extended (late bid accepted)", {("controlled.deadline_outcome", "error")}, {"rounds.deadline_outcome_legacy"}),
        ]
        for build, outcome, present, absent in cases:
            with self.subTest(build=build.__name__, outcome=outcome), tempfile.TemporaryDirectory() as tmp:
                workbook, filing = build(Path(tmp))
                set_ledger(workbook, 4, {"Event": "Deadline"})
                set_rounds(workbook, {"Due dates": "01/04/2020", "Deadline outcome": outcome})
                found = issue_set(workbook, filing)
                self.assertTrue(present <= found, found)
                self.assertFalse(absent & {code for code, _ in found}, found)

    def test_v114_review_warning_extended_without_new_date(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v114_fixture(Path(tmp))
            set_ledger(workbook, 4, {"Event": "Deadline", "Who": "Target"})
            set_rounds(workbook, {"Due dates": "01/04/2020", "Deadline outcome": "Extended"})
            self.assertIn(("rounds.extended_without_new_date", "warning"), issue_set(workbook, filing))
            append_ledger(workbook, [{"day": dt.date(2020, 1, 4), "Who": "Target", "Event": "Deadline revised"}])
            self.assertNotIn("rounds.extended_without_new_date", {code for code, _ in issue_set(workbook, filing)})
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_valid_fixture(Path(tmp))
            set_ledger(workbook, 4, {"Event": "Deadline"})
            set_rounds(workbook, {"Due dates": "01/04/2020", "Deadline outcome": "Extended"})
            self.assertNotIn("rounds.extended_without_new_date", {code for code, _ in issue_set(workbook, filing)})

    def test_v114_review_warning_exclusivity_repeating_a_bid_request(self) -> None:
        day = dt.date(2020, 1, 3)
        repeat = {"Who": "Alpha", "Event": "Exclusivity changed", "When": "01/03/2020", "Sort date": day, "Date from": day, "Date to": day}
        cases = [
            ({"Exclusivity": "Requested"}, repeat, True),
            ({"Exclusivity": "Required", "Event": "Bid reaffirmed"}, repeat, True),
            ({"Exclusivity": "Requested", "Event": "Other-scope bid", "Price low": None, "Price high": None}, repeat, True),
            ({"Exclusivity": "Not stated"}, repeat, False),
            ({"Exclusivity": "Requested"}, {**repeat, "Who": "Beta"}, False),
            ({"Exclusivity": "Requested"}, {"Who": "Alpha", "Event": "Exclusivity changed"}, False),
        ]
        for bid, row, expected in cases:
            with self.subTest(bid=bid, row=row), tempfile.TemporaryDirectory() as tmp:
                workbook, filing = build_v114_fixture(Path(tmp))
                set_ledger(workbook, 3, bid)
                set_ledger(workbook, 4, row)
                codes = {code for code, _ in issue_set(workbook, filing)}
                self.assertEqual("ledger.exclusivity_duplicate" in codes, expected, codes)

    def test_v114_review_warning_activity_after_exit(self) -> None:
        day = dt.date(2020, 1, 4)
        bid = {"day": day, "Who": "Alpha", "Type": "Strategic", "Event": "Bid", "Count": 1, "Formality": "Informal",
               "Conditions": "Heavy", **V114_BID_TERMS}
        exit_row = {"day": day, "Who": "Alpha", "Type": "Strategic", "Event": "Withdrew", "Count": 1, "Exit reason": "Not stated"}
        cases = [
            ([exit_row, bid], True),
            ([exit_row, {"day": day, "Who": "Alpha", "Type": "Strategic", "Event": "NDA signed", "Count": 1}], True),
            ([exit_row, {"day": day, "Who": "Alpha", "Type": "Strategic", "Event": "Re-entered", "Count": 1}, bid], False),
            ([exit_row, {**bid, "Event": "Other-scope bid"}], False),
            ([exit_row, {**bid, "Who": "Beta"}], False),
        ]
        for rows, expected in cases:
            with self.subTest(rows=[row["Event"] for row in rows]), tempfile.TemporaryDirectory() as tmp:
                workbook, filing = build_v114_fixture(Path(tmp))
                append_ledger(workbook, [dict(row) for row in rows])
                found = issue_set(workbook, filing)
                self.assertEqual(("exit.activity_without_reentry", "warning") in found, expected, found)
                self.assertNotIn("error", {severity for _, severity in found}, found)

    def test_v114_messages_name_the_rule_without_changing_v1132(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for build, expected in (
                (build_valid_fixture, "An inferred row needs a Note explaining how the inference is known."),
                (build_v114_fixture, "An inferred row needs a Note explaining how the inference is known, or naming the inferred field."),
            ):
                workbook, filing = build(Path(tmp))
                set_ledger(workbook, 2, {"Inferred": "Y", "Note": None})
                messages = {issue["code"]: issue["message"] for issue in check_lean.LeanChecker(workbook, filing, rules="v1.14").run()["issues"]}
                self.assertEqual(messages["ledger.inference_note"], expected)
            set_ledger(workbook, 3, {"Financing": "Contingent", "Conditions": "Light"})
            messages = {issue["code"]: issue["message"] for issue in check_lean.LeanChecker(workbook, filing, rules="v1.14").run()["issues"]}
            self.assertIn("(E12, H1)", messages["conditions.financing_heavy"])
            set_ledger(workbook, 3, {"Stock %": "abc"})
            messages = {issue["code"]: issue["message"] for issue in check_lean.LeanChecker(workbook, filing, rules="v1.14").run()["issues"]}
            self.assertIn("a stated range such as '40-60'", messages["controlled.stock_pct"])

    def test_schema_helpers_for_other_tools(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "v114").mkdir()
            v114, _ = build_v114_fixture(directory / "v114")
            v1132, _ = build_valid_fixture(directory)
            self.assertEqual(check_lean.ledger_schema(v114, "v1.14"), check_lean.SCHEMA_V114)
            self.assertEqual(check_lean.ledger_schema(v114), check_lean.SCHEMA_V1141)
            self.assertEqual(check_lean.ledger_schema(v1132), check_lean.SCHEMA_V1132)
            self.assertEqual(check_lean.ledger_schema(v1132, "v1.14.1"), check_lean.SCHEMA_V1132)
            broken = directory / "broken.xlsx"
            broken.write_text("not an xlsx", encoding="utf-8")
            self.assertIsNone(check_lean.ledger_schema(broken))
            empty = directory / "empty.xlsx"
            Workbook().save(empty)
            self.assertIsNone(check_lean.ledger_schema(empty))
        self.assertEqual(check_lean.schema_for_header(check_lean.LEDGER_COLUMNS_V114), "v1.14.1")
        self.assertEqual(check_lean.schema_for_header(check_lean.LEDGER_COLUMNS_V114, "v1.14"), "v1.14")
        self.assertEqual(check_lean.schema_for_header(check_lean.LEDGER_COLUMNS), "v1.13.2")
        self.assertIn("Late bids accepted", check_lean.DEADLINE_OUTCOMES)
        self.assertEqual(check_lean.deadline_outcomes("v1.13.2"), check_lean.DEADLINE_OUTCOMES)
        new, old = check_lean.choice_lists("v1.14"), check_lean.choice_lists("v1.13.2")
        self.assertIn("Extended (late bid accepted)", new["Deadline outcome"])
        self.assertNotIn("Late bids accepted", new["Deadline outcome"])
        self.assertIn("No deadline stated", new["Deadline outcome"])
        self.assertIn("Late bids accepted", old["Deadline outcome"])
        self.assertIn("No deadline stated", old["Deadline outcome"])
        self.assertEqual(new["Antitrust"], ["Varies", "Y"])
        self.assertNotIn("All cash", new)
        self.assertNotIn("CVR/earnout", old)
        self.assertEqual(old["All cash"], ["No", "Not stated", "Yes"])

    def test_cli_writes_json_for_unreadable_workbook(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            workbook = directory / "broken.xlsx"
            workbook.write_text("not an xlsx", encoding="utf-8")
            filing = directory / "filing.htm"
            filing.write_text("<p>Source text.</p>", encoding="utf-8")
            output = directory / "report.json"

            status = check_lean.main(
                ["--workbook", str(workbook), "--filing", str(filing), "--output", str(output)]
            )
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(status, 2)
            self.assertEqual(report["status"], "error")
            self.assertEqual(report["issues"][0]["code"], "input.workbook_unreadable")


# ---- v1.14.1 --------------------------------------------------------------------------------


def build_v1141_fixture(directory: Path) -> tuple[Path, Path]:
    """The v1.14 fixture as a v1.14.1 workbook: no Question, since one process needs none."""
    workbook, filing = build_v114_fixture(directory)
    wb = check_lean.openpyxl.load_workbook(workbook)
    ledger = wb["Deal ledger"]
    flag = check_lean.LEDGER_COLUMNS_V114.index("Flag") + 1
    for row in range(2, ledger.max_row + 1):
        ledger.cell(row, flag).value = None
    wb["Questions"].delete_rows(2, wb["Questions"].max_row)
    wb.save(workbook)
    return workbook, filing


def add_questions(workbook: Path, questions: list[list]) -> None:
    wb = check_lean.openpyxl.load_workbook(workbook)
    ws = wb["Questions"]
    for values in questions:
        ws.append(values)
    finish_sheet(ws, len(check_lean.QUESTION_COLUMNS))
    wb.save(workbook)


def question(number: int, text: str = "Is Alpha's Type Strategic?", rows: str = "Rows 2") -> list:
    return [f"Q{number}", text, "Yes.", "The filing calls Alpha an operating company (p. 10).", rows, "Row 2's Type changes.", None]


def v1141(workbook: Path, filing: Path) -> dict:
    return check_lean.LeanChecker(workbook, filing, rules="v1.14.1").run()


def codes_of(report: dict) -> set[tuple[str, str]]:
    return {(issue["code"], issue["severity"]) for issue in report["issues"]}


EXAMPLE_PASSAGES = [
    "On January 10, 2021, the board decided to explore a sale of the Company.",
    "Over the following six weeks, 14 parties, including Party A and Party B, signed confidentiality agreements and were asked to submit indications by March 3, 2021.",
    "On March 3, 2021, Party A submitted an indication of $25.00 per share in cash.",
    "On March 3, 2021, Party B submitted an indication of $24.00 per share in cash.",
    "On March 3, 2021, Party C submitted an indication of $30.00 per share in cash, with financing not committed.",
    "On March 3, 2021, Party D submitted the lowest indication, $20.00 per share in cash.",
    "On March 3, 2021, Party E submitted an indication of $28.00 per share in cash.",
    "On March 3, 2021, Party G submitted an indication of $27.00 per share in cash.",
    "The Company informed Party D its proposal was insufficient but that it could submit a revised proposal.",
    "On March 15, 2021, final-round letters asking for best and final offers by March 29, 2021 went to Parties C, E and G.",
    "Party C confirmed its prior proposal remained its best and final offer.",
    "Party G, which had signed a confidentiality agreement, made a proposal subject to a 45-day exclusivity period to complete due diligence and negotiate the merger agreement.",
    "On March 29, 2021, Party E submitted a best and final offer of $29.00 per share in cash with a markup of the merger agreement and committed financing.",
    "On April 2, 2021, Parent's counsel proposed that the sponsor's liability be capped at $40 million.",
    "On April 9, 2021, the Company and Party E signed the merger agreement.",
]


def build_examples_fixture(directory: Path) -> tuple[Path, Path]:
    """The candidate's five synthetic Examples, entered as one small v1.14.1 deal.

    Example 1 is row 9 (the cohort closure), Example 2 row 14 (Same as #5), Example 3 row 10
    (Party D not invited), Example 4 row 15 (Party G's exclusivity period) and Example 5 row 18
    (the sponsor liability cap with no price).
    """
    directory.mkdir(parents=True, exist_ok=True)
    filing = directory / "examples.htm"
    filing.write_text("<html><body>" + "".join(f"<p>{text}</p>" for text in EXAMPLE_PASSAGES) + "</body></html>", encoding="utf-8")
    day = dt.date
    cash = {"Stock %": 0, "Due diligence": "Incomplete", "Financing": "Not stated", "Regulatory": "Not stated", "Exclusivity": "Not stated"}

    def bid(who, when, price, quote, **extra):
        return {"Who": who, "Type": "Financial", "Event": "Bid", "Round": 1, "Price low": price, "Price high": price, "Formality": "Informal",
                "Conditions": "Unclear", "Count": 1, "day": when, "q": quote, **cash, **extra}

    def exit_(who, event, when, quote, round_=1, **extra):
        return {"Who": who, "Type": "Financial", "Event": event, "Round": round_, "Count": 1, "Exit reason": "Not stated", "Inferred": "Y",
                "When": f"by {when:%m/%d/%Y}", "day": when, "from": None, "q": quote, **extra}

    rows = [
        {"Who": "Target", "Event": "Target sale decision", "Round": 0, "day": day(2021, 1, 10), "q": 0, "Note": "Board to explore a sale."},
        {"Who": "Target", "Event": "Round opened", "Round": 1, "day": day(2021, 1, 20), "q": 1, "When": "late January 2021",
         "from": day(2021, 1, 20), "to": day(2021, 1, 31), "Note": "Outreach; indications due 03/03/2021."},
        bid("Party A", day(2021, 3, 3), 25, 2),
        bid("Party B", day(2021, 3, 3), 24, 3),
        bid("Party C", day(2021, 3, 3), 30, 4, Financing="Contingent", Conditions="Heavy", Note="H1: financing not committed."),
        bid("Party D", day(2021, 3, 3), 20, 5),
        bid("Party E", day(2021, 3, 3), 28, 6),
        bid("Party G", day(2021, 3, 3), 27, 7),
        # Example 1: unnamed members of a reported total with no reported offer.
        {"Who": "7 other NDA signers", "Type": "Unknown", "Event": "Did not submit", "Round": 1, "Count": 7, "Exit reason": "Not stated",
         "Inferred": "Y", "When": "by 03/03/2021", "day": day(2021, 3, 3), "from": None, "q": 1, "Note": "Count: 14 signers less Parties A to G."},
        # Example 3: not invited into the stage when it opens.
        exit_("Party D", "Dropped by target", day(2021, 3, 15), 8),
        exit_("Party A", "Dropped by target", day(2021, 3, 15), 9),
        exit_("Party B", "Dropped by target", day(2021, 3, 15), 9),
        {"Who": "Target", "Event": "Round opened", "Round": 2, "day": day(2021, 3, 15), "q": 9, "Note": "Best and final offers due 03/29/2021."},
        # Example 2: the same offer, restated in answer to the final-round letter.
        bid("Party C", day(2021, 3, 29), 30, 10, Round=2, When="by 03/29/2021", Formality="Formal", Financing="Contingent", Conditions="Heavy",
            **{"Due diligence": "Incomplete"}, Note="Same as #5. H1: financing not committed.", **{"from": None}),
        # Example 4: a period that also covers negotiation is not H2.
        bid("Party G", day(2021, 3, 29), None, 11, Round=2, When="by 03/29/2021", Formality="Formal", Exclusivity="Required",
            **{"Stock %": "Not stated"}, Note="45 days' exclusivity.", **{"from": None}),
        bid("Party E", day(2021, 3, 29), 29, 12, Round=2, Formality="Formal", Financing="Committed", Conditions="Unclear"),
        {"Who": "Target", "Event": "Deadline", "Round": 2, "day": day(2021, 3, 29), "q": 9, "Note": "Final bids due."},
        # Example 5: a commitment-only revision; no price, not a price observation.
        bid("Party E", day(2021, 4, 2), None, 13, Round=2, **{"Stock %": "Not stated", "Due diligence": "Not stated"}, Note="Sponsor liability cap $40m proposed."),
        {"Who": "Target", "Event": "Merger agreement signed", "Round": 2, "day": day(2021, 4, 9), "q": 14, "Note": "$29.00 per share in cash with Party E."},
        exit_("Party C", "Not selected at signing", day(2021, 4, 9), 14, round_=2),
        exit_("Party G", "Not selected at signing", day(2021, 4, 9), 14, round_=2),
    ]
    workbook = directory / "examples.xlsx"
    wb = Workbook()
    ledger = wb.active
    ledger.title = "Deal ledger"
    ledger.append(check_lean.LEDGER_COLUMNS_V114)
    for number, values in enumerate(rows, start=1):
        values = dict(values)
        when_day, quote = values.pop("day"), EXAMPLE_PASSAGES[values.pop("q")]
        start, end = values.pop("from", when_day), values.pop("to", when_day)
        # A quotation holds at most 30 words (B).
        quote = " ".join(quote.split()[:30])
        record = {"#": number, "When": f"{when_day:%m/%d/%Y}", "Process": 1, "Quote and page": f"“{quote}” (p. 20)",
                  "Sort date": when_day, "Date from": start, "Date to": end, **values}
        ledger.append([record.get(column) for column in check_lean.LEDGER_COLUMNS_V114])
    for row in range(2, ledger.max_row + 1):
        for name in check_lean.DATE_COLUMNS:
            ledger.cell(row, check_lean.LEDGER_COLUMNS_V114.index(name) + 1).number_format = "MM/DD/YYYY"
    finish_sheet(ledger, len(check_lean.LEDGER_COLUMNS_V114))

    rounds = wb.create_sheet("Rounds")
    rounds.append(check_lean.ROUND_COLUMNS)
    rounds.append([1, 1, day(2021, 1, 20), "Outreach to prospective buyers", "14 NDA signers, including Parties A to G", "03/03/2021", None,
                   "Not final", "6: Parties A, B, C, D, E and G", "Three advanced; eleven out"])
    rounds.append([1, 2, day(2021, 3, 15), "Final-round letters", "3: Parties C, E and G", "03/29/2021", "Enforced",
                   "Announced as final", "3: Parties C, E and G", "Signing with Party E"])
    for row in (2, 3):
        rounds.cell(row, 3).number_format = "MM/DD/YYYY"
    finish_sheet(rounds, len(check_lean.ROUND_COLUMNS))

    questions = wb.create_sheet("Questions")
    questions.append(check_lean.QUESTION_COLUMNS)
    finish_sheet(questions, len(check_lean.QUESTION_COLUMNS))

    facts = wb.create_sheet("Deal facts")
    facts.append(check_lean.FACT_COLUMNS)
    values = ["Example Co", "Party E", "Financial", "$29.00 per share in cash", "04/09/2021", "not reported", "Synthetic, 2021", "20",
              "target-led", 1, "None reported", "Met (process 1): 14 parties", "Yes", "US dollars per share", "Bank", "Law Firm",
              "The board decided to sell in January. Fourteen parties signed agreements. Six bid in March. Three were invited to a final round. "
              "Party E won and signed in April."]
    for field, value in zip(check_lean.FACT_FIELDS, values, strict=True):
        facts.append([field, value])
    finish_sheet(facts, len(check_lean.FACT_COLUMNS))
    wb.save(workbook)
    return workbook, filing


class LeanCheckerV1141Tests(unittest.TestCase):
    """Each v1.14.1 rule under the v1.14.1 rules, and the v1.14 behaviour it replaces."""

    def check_both(self, values: dict, code: str, v1141_severity: str | None, v114_severity: str | None, row: int = 3) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v1141_fixture(Path(tmp))
            set_ledger(workbook, row, values)
            for rules, severity in (("v1.14.1", v1141_severity), ("v1.14", v114_severity)):
                found = {sev for c, sev in issue_set(workbook, filing, rules) if c == code}
                self.assertEqual(found, {severity} if severity else set(), (rules, values, issue_set(workbook, filing, rules)))

    def test_fixture_passes_and_default_rules_are_v1141(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v1141_fixture(Path(tmp))
            report = check_lean.LeanChecker(workbook, filing).run()
            self.assertEqual((report["status"], report["ledger_schema"], report["checker_version"]), ("pass", "v1.14.1", "1.8"), report["issues"])
            # Under v1.14 the same workbook wants the process-map Question the v1.14.1 text deleted.
            self.assertIn(("questions.process_round_map", "warning"), issue_set(workbook, filing, "v1.14"))
        with self.assertRaises(ValueError):
            check_lean.LeanChecker(Path("x.xlsx"), Path("x.htm"), rules="v1.13.2")

    def test_five_examples_pass_with_no_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_examples_fixture(Path(tmp))
            report = v1141(workbook, filing)
            self.assertEqual(report["summary"]["errors"], 0, report["issues"])
            self.assertEqual(report["status"], "pass", report["issues"])

    def test_rules_for_instruction_and_cli(self) -> None:
        self.assertEqual(check_lean.rules_for_instruction("8bdb7c205512c9bcf55ffa7623fba0a8bb4aabaed23c99845fa88b4a80cc8a79"), "v1.14.1")
        self.assertEqual(check_lean.rules_for_instruction("8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98"), "v1.14.1")
        self.assertEqual(check_lean.rules_for_instruction("C2D47A479D09EB46D0AB9FBF887568FCF13E972E2E11ACBF08D5CDFAB468AB27"), "v1.14")
        self.assertIsNone(check_lean.rules_for_instruction("0" * 64))
        self.assertIsNone(check_lean.rules_for_instruction(None))
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v1141_fixture(Path(tmp))
            set_ledger(workbook, 3, {"Stock %": "40-60"})
            for rules, status, schema in (("v1.14", 0, "v1.14"), ("v1.14.1", 1, "v1.14.1"), (None, 1, "v1.14.1")):
                output = Path(tmp) / f"{rules}.json"
                argv = ["--workbook", str(workbook), "--filing", str(filing), "--output", str(output)] + (["--rules", rules] if rules else [])
                self.assertEqual(check_lean.main(argv), status)
                self.assertEqual(json.loads(output.read_text())["ledger_schema"], schema)

    def test_note_over_40_words_is_an_error(self) -> None:
        self.check_both({"Note": " ".join(["word"] * 41)}, "ledger.note_length", "error", "warning")
        self.check_both({"Note": " ".join(["word"] * 40)}, "ledger.note_length", None, None)

    def test_inferred_only_on_exit_round_opened_and_process_restarted(self) -> None:
        self.check_both({"Inferred": "Y"}, "ledger.inferred_event", "error", None)
        self.check_both({"Inferred": "Y"}, "ledger.inferred_event", None, None, row=2)  # Round opened
        self.check_both({"Event": "Withdrew", "Inferred": "Y", "Exit reason": "Not stated", "Who": "Alpha", "Note": None,
                         "Price low": None, "Price high": None, "Formality": None, "Conditions": None, "Stock %": None,
                         **{c: None for c in check_lean.CONDITION_COLUMNS}}, "ledger.inferred_event", None, None)

    def test_formality_unclear_only_on_cohort_rows(self) -> None:
        self.check_both({"Formality": "Unclear"}, "bid.formality_unclear", "error", None)
        self.check_both({"Formality": "Unclear", "Count": 2}, "bid.formality_unclear", None, None)
        self.check_both({"Formality": "Unclear", "Who": "Two financial bidders"}, "bid.formality_unclear", None, None)

    def test_antitrust_needs_regulatory_concern(self) -> None:
        self.check_both({"Antitrust": "Y", "Regulatory": "No concern"}, "conditions.antitrust_regulatory", "error", None)
        self.check_both({"Antitrust": "Y", "Regulatory": "Concern"}, "conditions.antitrust_regulatory", None, None)
        self.check_both({"Antitrust": "Y"}, "conditions.antitrust_regulatory", "error", "error")

    def test_stock_range_is_an_error_under_v1141(self) -> None:
        self.check_both({"Stock %": "40-60"}, "controlled.stock_pct", "error", None)
        self.check_both({"Stock %": "50–75"}, "controlled.stock_pct", "error", None)
        self.check_both({"Stock %": "Part stock", "Note": "Stock 40-60% of value."}, "controlled.stock_pct", None, None)
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v1141_fixture(Path(tmp))
            set_ledger(workbook, 3, {"Stock %": "40-60"})
            message = next(i["message"] for i in v1141(workbook, filing)["issues"] if i["code"] == "controlled.stock_pct")
            self.assertIn("Part stock", message)

    def test_markers_take_y_or_blank_only(self) -> None:
        cohort = {"Who": "Two financial bidders", "Count": 2}
        self.check_both({**cohort, "CVR/earnout": "Varies"}, "controlled.cvr_earnout", "error", None)
        self.check_both({**cohort, "Regulatory": "Varies", "Antitrust": "Varies"}, "controlled.antitrust", "error", None)
        self.assertEqual(check_lean.choice_lists("v1.14.1")["CVR/earnout"], ["Y"])
        self.assertEqual(check_lean.choice_lists("v1.14.1")["Antitrust"], ["Y"])
        self.assertEqual(check_lean.choice_lists("v1.14")["Antitrust"], ["Varies", "Y"])

    def test_initiation_takes_three_values(self) -> None:
        self.assertEqual(check_lean.choice_lists("v1.14.1")["Initiation"], ["activist-influenced", "bidder-led", "target-led"])
        self.assertIn("mixed", check_lean.choice_lists("v1.14")["Initiation"])
        for value, v1141_codes in (("mixed", {"controlled.initiation"}), ("unclear", {"controlled.initiation"}), ("bidder-led", set())):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as tmp:
                workbook, filing = build_v1141_fixture(Path(tmp))
                wb = check_lean.openpyxl.load_workbook(workbook)
                wb["Deal facts"]["B10"] = value
                wb.save(workbook)
                self.assertEqual({c for c, _ in issue_set(workbook, filing, "v1.14.1")} & {"controlled.initiation"}, v1141_codes)
                self.assertNotIn("controlled.initiation", {c for c, _ in issue_set(workbook, filing, "v1.14")})
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v1141_fixture(Path(tmp))
            wb = check_lean.openpyxl.load_workbook(workbook)
            wb["Deal facts"]["A10"] = "Initiation (target-led, bidder-led, activist-influenced, mixed or unclear)"
            wb.save(workbook)
            self.assertIn(("facts.fields", "error"), issue_set(workbook, filing, "v1.14.1"))
            self.assertNotIn("facts.fields", {c for c, _ in issue_set(workbook, filing, "v1.14")})

    def test_auction_screen_is_met_or_not_met_with_a_number(self) -> None:
        cases = [("Uncertain: count unknown", True, False), ("Met: count unknown", True, False), ("Met (process 1): 3 parties", False, False),
                 ("Not met (process 1): 1 party; Met (process 2): 4 parties", False, False)]
        for value, v1141_error, v114_error in cases:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as tmp:
                workbook, filing = build_v1141_fixture(Path(tmp))
                wb = check_lean.openpyxl.load_workbook(workbook)
                wb["Deal facts"]["B13"] = value
                wb.save(workbook)
                self.assertEqual(("facts.auction_screen", "error") in issue_set(workbook, filing, "v1.14.1"), v1141_error)
                self.assertEqual(("facts.auction_screen", "error") in issue_set(workbook, filing, "v1.14"), v114_error)

    def test_question_count_excludes_the_process_question(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v1141_fixture(Path(tmp))
            add_questions(workbook, [question(n) for n in range(1, 6)])
            set_ledger(workbook, 3, {"Flag": "Q1; Q2; Q3; Q4; Q5"})
            self.assertNotIn("questions.count", {c for c, _ in issue_set(workbook, filing, "v1.14.1")})
            add_questions(workbook, [question(6, "Process: is this one process with one round?", "Rows 1")])
            set_ledger(workbook, 2, {"Flag": "Q6"})
            self.assertNotIn("questions.count", {c for c, _ in issue_set(workbook, filing, "v1.14.1")})
            add_questions(workbook, [question(7)])
            set_ledger(workbook, 3, {"Flag": "Q1; Q2; Q3; Q4; Q5; Q7"})
            self.assertIn(("questions.count", "warning"), issue_set(workbook, filing, "v1.14.1"))
            self.assertNotIn("questions.count", {c for c, _ in issue_set(workbook, filing, "v1.14")})

    def test_process_question_is_recognised_and_expected_for_two_processes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v1141_fixture(Path(tmp))
            day = dt.date(2020, 1, 4)
            append_ledger(workbook, [{"day": day, "Who": "Target", "Event": "Process restarted", "Process": 2, "Round": 0, "Count": 1,
                                      "Inferred": "Y", "Note": "Last reported contact 01/03/2020."}])
            wb = check_lean.openpyxl.load_workbook(workbook)
            wb["Deal facts"]["B11"] = 2
            wb.save(workbook)
            self.assertIn(("questions.process_missing", "warning"), issue_set(workbook, filing, "v1.14.1"))
            add_questions(workbook, [question(n) for n in range(1, 6)] + [question(6, "Is the break a new process?", "#4")])
            set_ledger(workbook, 3, {"Flag": "Q1; Q2; Q3; Q4; Q5"})
            set_ledger(workbook, 5, {"Flag": "Q6"})
            found = {c for c, _ in issue_set(workbook, filing, "v1.14.1")}
            self.assertNotIn("questions.process_missing", found)
            self.assertNotIn("questions.count", found)

    def test_mandatory_map_and_deadline_questions_are_gone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v1141_fixture(Path(tmp))
            set_ledger(workbook, 4, {"Event": "Deadline"})
            set_rounds(workbook, {"Due dates": "01/04/2020", "Deadline outcome": "Enforced"})
            found = {c for c, _ in issue_set(workbook, filing, "v1.14.1")}
            self.assertFalse(found & {"questions.process_round_map", "questions.deadline_outcomes"}, found)
            found = {c for c, _ in issue_set(workbook, filing, "v1.14")}
            self.assertTrue({"questions.process_round_map", "questions.deadline_outcomes"} <= found, found)

    def test_question_entry_is_at_most_60_words(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v1141_fixture(Path(tmp))
            long = question(1, "Is Alpha " + " ".join(["really"] * 50) + " Strategic?")
            add_questions(workbook, [long])
            set_ledger(workbook, 3, {"Flag": "Q1"})
            self.assertIn(("questions.length", "warning"), issue_set(workbook, filing, "v1.14.1"))
            self.assertNotIn("questions.length", {c for c, _ in issue_set(workbook, filing, "v1.14")})

    def test_rounds_due_dates_compare_by_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v1141_fixture(Path(tmp))
            set_rounds(workbook, {"Due dates": "none stated (the letter set no date)"})
            self.assertNotIn("rounds.no_deadline_pair", {c for c, _ in issue_set(workbook, filing, "v1.14.1")})
            self.assertIn(("rounds.no_deadline_pair", "error"), issue_set(workbook, filing, "v1.14"))

    def test_legacy_deadline_outcome_is_not_a_v1141_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v1141_fixture(Path(tmp))
            set_ledger(workbook, 4, {"Event": "Deadline"})
            set_rounds(workbook, {"Due dates": "01/04/2020", "Deadline outcome": "Late bids accepted"})
            self.assertIn(("controlled.deadline_outcome", "error"), issue_set(workbook, filing, "v1.14.1"))
            self.assertIn(("rounds.deadline_outcome_legacy", "warning"), issue_set(workbook, filing, "v1.14"))

    def test_inference_note_is_a_warning_for_restarts_and_cohort_closures(self) -> None:
        day = dt.date(2020, 1, 4)
        cases = [
            ({"Who": "Target", "Event": "Process restarted", "Process": 2, "Round": 0, "Count": 1}, "warning"),
            ({"Who": "5 other NDA signers", "Type": "Unknown", "Event": "Did not submit", "Count": 5, "Exit reason": "Not stated"}, "warning"),
            ({"Who": "Beta", "Type": "Unknown", "Event": "Did not submit", "Count": 1, "Exit reason": "Not stated"}, None),
        ]
        for values, severity in cases:
            with self.subTest(event=values["Event"], who=values["Who"]), tempfile.TemporaryDirectory() as tmp:
                workbook, filing = build_v1141_fixture(Path(tmp))
                append_ledger(workbook, [{"day": day, "Inferred": "Y", "Note": None, **values}])
                found = {sev for c, sev in issue_set(workbook, filing, "v1.14.1") if c == "ledger.inference_note"}
                self.assertEqual(found, {severity} if severity else set())
                self.assertIn(("ledger.inference_note", "error"), issue_set(workbook, filing, "v1.14"))

    def test_count_on_process_markers_and_group_changes(self) -> None:
        day = dt.date(2020, 1, 4)
        cases = [
            ({"Who": "Alpha and Beta", "Event": "Bidding group changed", "Count": None}, ("ledger.count_bidder", "error")),
            ({"Who": "Alpha and Beta", "Event": "Bidding group changed", "Count": 1}, None),
            ({"Who": "Target", "Event": "Process terminated", "Count": None}, ("ledger.count_marker", "warning")),
            ({"Who": "Target", "Event": "Process terminated", "Count": 1}, None),
        ]
        for values, expected in cases:
            with self.subTest(values=values), tempfile.TemporaryDirectory() as tmp:
                workbook, filing = build_v1141_fixture(Path(tmp))
                append_ledger(workbook, [{"day": day, **values}])
                found = {(c, sev) for c, sev in issue_set(workbook, filing, "v1.14.1") if c in {"ledger.count_bidder", "ledger.count_marker"}}
                self.assertEqual(found, {expected} if expected else set())
                self.assertFalse({c for c, _ in issue_set(workbook, filing, "v1.14")} & {"ledger.count_bidder", "ledger.count_marker"})

    def test_count_note_accepts_a_qualifier_and_warns_on_a_range(self) -> None:
        cases = [("Count: more than ten.", None), ("Count: approximately 20.", None), ("Count: 11–14.", ("ledger.count_range", "warning")),
                 ("Count: unknown.", ("ledger.count_range", "warning")), ("", ("ledger.count_bidder", "error"))]
        for note, expected in cases:
            with self.subTest(note=note), tempfile.TemporaryDirectory() as tmp:
                workbook, filing = build_v1141_fixture(Path(tmp))
                set_ledger(workbook, 3, {"Who": "Financial bidders", "Count": None, "Note": note})
                found = {(c, s) for c, s in issue_set(workbook, filing, "v1.14.1") if c in {"ledger.count_range", "ledger.count_bidder", "ledger.count_uncertain"}}
                self.assertEqual(found, {expected} if expected else set())
                self.assertTrue({c for c, _ in issue_set(workbook, filing, "v1.14")} & {"ledger.count_uncertain", "ledger.count_bidder"})

    def test_round_zero_after_round_one_opens_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v1141_fixture(Path(tmp))
            set_ledger(workbook, 4, {"Round": 0})
            self.assertIn(("round.zero_after_opening", "error"), issue_set(workbook, filing, "v1.14.1"))
            self.assertNotIn("round.zero_after_opening", {c for c, _ in issue_set(workbook, filing, "v1.14")})

    def test_same_as_points_to_an_earlier_bid_of_the_same_bidder(self) -> None:
        day = dt.date(2020, 1, 4)
        again = {"day": day, "Who": "Alpha", "Type": "Strategic", "Event": "Bid", "Count": 1, "Price low": 10, "Price high": 10,
                 "Formality": "Informal", "Conditions": "Unclear", **V114_BID_TERMS}
        cases = [("Same as #2.", False), ("Same as #1.", True), ("Same as #9.", True), ("Same as #5.", True)]
        for note, error in cases:
            with self.subTest(note=note), tempfile.TemporaryDirectory() as tmp:
                workbook, filing = build_v1141_fixture(Path(tmp))
                append_ledger(workbook, [{**again, "Note": note}])
                self.assertEqual(("ledger.same_as", "error") in issue_set(workbook, filing, "v1.14.1"), error)
                self.assertNotIn("ledger.same_as", {c for c, _ in issue_set(workbook, filing, "v1.14")})
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v1141_fixture(Path(tmp))
            append_ledger(workbook, [{**again, "Who": "Beta", "Note": "Same as #2."}])
            self.assertIn(("ledger.same_as", "error"), issue_set(workbook, filing, "v1.14.1"))

    def test_heavy_note_begins_with_its_trigger(self) -> None:
        self.check_both({"Conditions": "Heavy", "Note": "Financing not committed."}, "conditions.heavy_trigger", "warning", None)
        self.check_both({"Conditions": "Heavy", "Note": "H3: may reprice after diligence."}, "conditions.heavy_trigger", None, None)
        self.check_both({"Conditions": "Heavy", "Note": "Same as #2. H1: financing not committed."}, "conditions.heavy_trigger", None, None)
        self.check_both({"Conditions": "Heavy", "Note": "Financing not committed.", "Due diligence": "Not stated"}, "conditions.level_unsupported", None, "warning")

    def test_bid_reaffirmed_is_formal_and_a_same_offer_row(self) -> None:
        day = dt.date(2020, 1, 4)
        base = {"day": day, "Who": "Alpha", "Type": "Strategic", "Event": "Bid reaffirmed", "Count": 1, "Price low": 10, "Price high": 10,
                "Conditions": "Unclear", **V114_BID_TERMS}
        cases = [({"Formality": "Formal", "Note": "Same as #2."}, set()),
                 ({"Formality": "Informal", "Note": "Same as #2."}, {"bid.reaffirmed_formal"}),
                 ({"Formality": "Formal", "Note": "Reaffirmed."}, {"bid.reaffirmed_same_as"})]
        for values, expected in cases:
            with self.subTest(values=values), tempfile.TemporaryDirectory() as tmp:
                workbook, filing = build_v1141_fixture(Path(tmp))
                append_ledger(workbook, [{**base, **values}])
                found = {c for c, _ in issue_set(workbook, filing, "v1.14.1")} & {"bid.reaffirmed_formal", "bid.reaffirmed_same_as"}
                self.assertEqual(found, expected)
                self.assertFalse({c for c, _ in issue_set(workbook, filing, "v1.14")} & {"bid.reaffirmed_formal", "bid.reaffirmed_same_as"})

    def test_light_needs_diligence_complete_or_incomplete(self) -> None:
        self.check_both({"Conditions": "Light", "Due diligence": "Not stated", "Financing": "Committed"}, "conditions.light_support", "warning", None)
        self.check_both({"Conditions": "Light", "Due diligence": "Incomplete"}, "conditions.light_support", None, None)

    def test_other_scope_message_cites_the_current_part(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook, filing = build_v1141_fixture(Path(tmp))
            set_ledger(workbook, 3, {"Event": "Other-scope bid"})
            message = next(i["message"] for i in v1141(workbook, filing)["issues"] if i["code"] == "bid.other_scope_per_share")
            self.assertIn("(D2)", message)
            self.assertNotIn("F.4", message)


if __name__ == "__main__":
    unittest.main()
