#!/usr/bin/env python3
"""Mechanical validator for the lean deal-ledger workbook (instruction v1.12).

This checker intentionally does not decide whether events, bidders, rounds, or
classifications are substantively correct. In particular, it does not sum
``Count`` into a bidder population. It checks workbook structure and internal
consistency, then tests each quoted passage as one contiguous normalized
substring of the full filing parsed by BeautifulSoup.

Usage:
    python3 check_lean.py --workbook candidate.xlsx --filing filing.htm \
        --output mechanical_report.json

Exit status is 0 when there are no errors, 1 when validation errors are found,
and 2 when an input cannot be opened or the JSON report cannot be written.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import openpyxl
from bs4 import BeautifulSoup
from openpyxl.utils.cell import coordinate_to_tuple, range_boundaries


CHECKER_VERSION = "1.5"
CHECKER_REVISION = (
    "Adds two cross-column checks: an exact-day When must equal Date from, Date to and "
    "Sort date (C10), and an inferred exit carries Exit reason 'Not stated' (C16). "
    "Checks instruction v1.12."
)

SHEETS = ["Deal ledger", "Rounds", "Questions", "Deal facts"]

LEDGER_COLUMNS = [
    "#",
    "When",
    "Who",
    "Type",
    "Event",
    "Process",
    "Round",
    "Price low",
    "Price high",
    "All cash",
    "Formality",
    "Conditions",
    "Count",
    "Exit reason",
    "Inferred",
    "Note",
    "Quote and page",
    "Flag",
    "Reviewer note",
    "Sort date",
    "Date from",
    "Date to",
]

ROUND_COLUMNS = [
    "Process",
    "Round",
    "Opened",
    "How opened",
    "Who was in",
    "Due dates",
    "Deadline outcome",
    "Finality",
    "Bids received",
    "How it ended",
]

QUESTION_COLUMNS = [
    "Q",
    "Question",
    "Recommended answer",
    "Why, with page",
    "Rows affected",
    "What changes if answered differently",
    "Reviewer note",
]

FACT_COLUMNS = ["Field", "Value"]

FACT_FIELDS = [
    "Target",
    "Acquirer",
    "Acquirer type",
    "Agreed price and consideration",
    "Merger agreement signed",
    "Merger announced",
    "Filing type and date",
    "Background pages",
    "Initiation",
    "Number of processes",
    "Auction screen",
    "Whole-company bids",
    "Currency and units of bid prices",
    "Target financial advisers",
    "Target legal advisers",
    "Account (five or six plain sentences)",
]
ACCOUNT_FIELDS = {"Account", "Account (five or six plain sentences)"}
INITIATION_FIELDS = {
    "Initiation",
    "Initiation (target-led, bidder-led, activist-influenced, mixed or unclear)",
}
AUCTION_SCREEN_FIELDS = {"Auction screen", "Auction screen (C1)"}
EARLIER_APPROACHES_FIELDS = {"Earlier approaches", "Earlier approaches (C7)"}
WHOLE_COMPANY_FIELDS = {
    "Whole-company bids",
    "Whole-company bids (Yes, or No with what was bid for)",
}
FACT_FIELD_OPTIONS = [{field} for field in FACT_FIELDS]
FACT_FIELD_OPTIONS[8] = INITIATION_FIELDS
FACT_FIELD_OPTIONS[10] = AUCTION_SCREEN_FIELDS
FACT_FIELD_OPTIONS[11] = WHOLE_COMPANY_FIELDS
FACT_FIELD_OPTIONS[15] = ACCOUNT_FIELDS

EVENTS = {
    "Target interest",
    "Bidder interest",
    "Target sale decision",
    "Activist",
    "Adviser",
    "Adviser ended",
    "Contact",
    "NDA signed",
    "Round opened",
    "Deadline set",
    "Deadline revised",
    "Deadline",
    "Exclusivity changed",
    "Other material event",
    "Bid",
    "Bid reaffirmed",
    "Other-scope bid",
    "Bidding group changed",
    "Dropped by target",
    "Withdrew",
    "Did not submit",
    "Not selected at signing",
    "Re-entered",
    "Sale process announced",
    "Bid announced",
    "Merger announced",
    "Merger agreement signed",
    "Go-shop changed",
    "Process terminated",
    "Process restarted",
}

TYPES = {"Strategic", "Financial", "Mixed", "Unknown"}
BID_EVENTS = {"Bid", "Bid reaffirmed", "Other-scope bid"}
EXIT_EVENTS = {
    "Dropped by target",
    "Withdrew",
    "Did not submit",
    "Not selected at signing",
}
NO_BIDDER_COUNT_EVENTS = {
    "Adviser",
    "Adviser ended",
    "Round opened",
    "Deadline set",
    "Deadline revised",
    "Deadline",
    "Sale process announced",
    "Bid announced",
    "Merger announced",
}
ALL_CASH = {"Yes", "No", "Not stated"}
FORMALITY = {"Formal", "Informal", "Unclear"}
CONDITIONS = {"None", "Light", "Heavy", "Unclear"}
EXIT_REASONS = {
    "Value below market price",
    "Value at or below market price",
    "Value below earlier offer",
    "Value at earlier offer",
    "Would not improve earlier offer",
    "Lower offer than rivals",
    "Terms or process",
    "Other stated reason",
    "Not stated",
}
FINALITY = {"Announced as final", "Inferred final", "Not final"}
DEADLINE_OUTCOMES = {
    "Enforced",
    "Extended",
    "Late bids accepted",
    "Passed without action",
    "Unclear",
}
INITIATION = {
    "target-led",
    "bidder-led",
    "activist-influenced",
    "mixed",
    "unclear",
}

DATE_COLUMNS = ("Sort date", "Date from", "Date to")
PAGE_REF_RE = re.compile(
    r"(?:\(\s*pp?\.\s*(?P<paren>[^()]+?)\s*\)|pp?\.\s*(?P<bare>[A-Za-z0-9]+(?:\s*[-\u2013,]\s*[A-Za-z0-9]+)*))\s*$",
    re.IGNORECASE,
)
QID_RE = re.compile(r"Q[1-9]\d*")


def normalize_contiguous(value: Any) -> str:
    """Normalize Unicode and whitespace without splitting or joining excerpts."""

    text = unicodedata.normalize("NFC", str(value)).replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text).strip()


def word_count(value: Any) -> int:
    text = normalize_contiguous(value)
    return len(text.split()) if text else 0


def strip_outer_quotes(value: str) -> str:
    text = value.strip()
    if len(text) >= 2 and ((text[0], text[-1]) in {("\u201c", "\u201d"), ('"', '"')}):
        return text[1:-1].strip()
    return text


def parse_quote_and_page(value: Any) -> tuple[str, str] | None:
    """Separate one passage from its terminal p./pp. reference.

    Outer quotation marks are optional and may surround the passage alone or
    the passage plus its page reference. The returned passage remains whole;
    no ellipsis/bracket splitting or piecewise matching is performed.
    """

    if is_blank(value):
        return None
    text = normalize_contiguous(value)
    text_without_outer_quotes = strip_outer_quotes(text)
    match = PAGE_REF_RE.search(text_without_outer_quotes)
    if match is None:
        return None
    passage = strip_outer_quotes(text_without_outer_quotes[: match.start()].strip())
    page = normalize_contiguous(match.group("paren") or match.group("bare"))
    return passage, page


def is_blank(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def is_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) or (
        isinstance(value, float) and math.isfinite(value) and value.is_integer()
    )


def as_integer(value: Any) -> int | None:
    return int(value) if is_integer(value) else None


def as_integer_or_text(value: Any) -> int | None:
    integer = as_integer(value)
    if integer is not None:
        return integer
    if isinstance(value, str) and re.fullmatch(r"[+-]?\d+", value.strip()):
        return int(value.strip())
    return None


def starts_with_canonical(value: Any, allowed: set[str]) -> bool:
    text = normalize_contiguous(value)
    folded = text.casefold()
    return any(
        folded == label.casefold()
        or (
            folded.startswith(label.casefold())
            and len(text) > len(label)
            and not text[len(label)].isalnum()
        )
        for label in allowed
    )


def parse_flag_ids(value: Any) -> set[str] | None:
    """Parse one or more Q ids; return None if any other content is present."""

    if is_blank(value):
        return set()
    text = normalize_contiguous(value)
    ids = QID_RE.findall(text)
    remainder = QID_RE.sub("", text)
    remainder = re.sub(r"\band\b", "", remainder, flags=re.IGNORECASE)
    if not ids or re.fullmatch(r"[\s,;/&]*", remainder) is None:
        return None
    return set(ids)


def as_date(value: Any) -> dt.date | None:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    return None


def date_has_time(value: Any) -> bool:
    return isinstance(value, dt.datetime) and value.time() != dt.time()


def has_mmddyyyy_format(cell: Any) -> bool:
    return str(cell.number_format or "").strip().lower() == "mm/dd/yyyy"


def nonempty_rows(ws: Any, width: int) -> list[int]:
    scan_width = max(width, ws.max_column)
    return [
        row
        for row in range(2, ws.max_row + 1)
        if any(not is_blank(ws.cell(row, col).value) for col in range(1, scan_width + 1))
    ]


def parse_affected_rows(value: Any) -> tuple[set[int], bool]:
    """Return explicit ledger row references and whether the syntax was parseable.

    Accepted forms include ``#2, #4-#6`` and ``Rows 2, 4-6``. Narrative/global
    descriptions are left unparsed so the checker does not invent references.
    """

    if is_blank(value):
        return set(), False
    text = normalize_contiguous(value).replace("\u2013", "-").replace("\u2014", "-")
    hash_refs = {int(number) for number in re.findall(r"#\s*(\d+)", text)}
    for start, end in re.findall(r"#\s*(\d+)\s*-\s*#?\s*(\d+)", text):
        lo, hi = sorted((int(start), int(end)))
        hash_refs.update(range(lo, hi + 1))
    if "#" in text:
        return hash_refs, bool(hash_refs)

    stripped = re.sub(r"(?i)^\s*rows?\s*:?\s*", "", text)
    if not re.fullmatch(r"\d+(?:\s*-\s*\d+)?(?:\s*[,;]\s*\d+(?:\s*-\s*\d+)?)*", stripped):
        return set(), False
    refs: set[int] = set()
    for token in re.split(r"\s*[,;]\s*", stripped):
        if "-" in token:
            start, end = (int(part.strip()) for part in token.split("-", 1))
            lo, hi = sorted((start, end))
            refs.update(range(lo, hi + 1))
        else:
            refs.add(int(token))
    return refs, True


class LeanChecker:
    def __init__(self, workbook_path: Path, filing_path: Path) -> None:
        self.workbook_path = workbook_path
        self.filing_path = filing_path
        self.issues: list[dict[str, Any]] = []
        self.fatal = False
        self.wb: Any = None
        self.filing_texts: tuple[str, ...] = ()

    def add(
        self,
        severity: str,
        code: str,
        message: str,
        *,
        sheet: str | None = None,
        row: int | None = None,
        column: str | None = None,
    ) -> None:
        self.issues.append(
            {
                "severity": severity,
                "code": code,
                "sheet": sheet,
                "row": row,
                "column": column,
                "message": message,
            }
        )

    def load_inputs(self) -> bool:
        try:
            self.wb = openpyxl.load_workbook(self.workbook_path, data_only=False)
        except Exception as exc:  # openpyxl exposes several format/XML exceptions
            self.fatal = True
            self.add(
                "error",
                "input.workbook_unreadable",
                f"Could not open workbook: {type(exc).__name__}: {exc}",
            )
            return False

        try:
            raw = self.filing_path.read_bytes()
            soup = BeautifulSoup(raw, "html.parser")
            for element in soup(["script", "style", "noscript"]):
                element.decompose()
            # SEC HTML frequently divides a visually contiguous phrase among
            # inline FONT/SPAN nodes. Both renderings preserve DOM order and
            # contiguous matching; neither permits excerpt-by-excerpt splicing.
            renderings = (
                normalize_contiguous(soup.get_text(" ")),
                normalize_contiguous(soup.get_text("")),
            )
            self.filing_texts = tuple(dict.fromkeys(text for text in renderings if text))
            if not self.filing_texts:
                raise ValueError("parsed filing contains no text")
        except Exception as exc:
            self.fatal = True
            self.add(
                "error",
                "input.filing_unreadable",
                f"Could not parse filing: {type(exc).__name__}: {exc}",
            )
            return False
        return True

    def check_schema(self, ws: Any, expected: list[str]) -> bool:
        width = max(ws.max_column, len(expected))
        actual = [ws.cell(1, col).value for col in range(1, width + 1)]
        while actual and is_blank(actual[-1]):
            actual.pop()
        if actual != expected:
            self.add(
                "error",
                "schema.columns",
                f"Expected columns {expected!r}; found {actual!r}.",
                sheet=ws.title,
                row=1,
            )
            return False
        return True

    def check_presentation(self, ws: Any, expected_width: int) -> None:
        if ws.sheet_state != "visible":
            self.add(
                "error",
                "presentation.hidden_sheet",
                "Required sheet is not visible.",
                sheet=ws.title,
            )

        if ws.merged_cells.ranges:
            self.add(
                "error",
                "presentation.merged_cells",
                "Merged cells are prohibited: "
                + ", ".join(str(item) for item in list(ws.merged_cells.ranges)[:10]),
                sheet=ws.title,
            )

        freeze = ws.freeze_panes
        try:
            coordinate = freeze.coordinate if hasattr(freeze, "coordinate") else str(freeze)
            freeze_row, _ = coordinate_to_tuple(coordinate)
        except Exception:
            freeze_row = None
        if freeze_row != 2:
            self.add(
                "error",
                "presentation.freeze_header",
                f"Header row is not frozen at row 1 (freeze_panes={freeze!r}).",
                sheet=ws.title,
                row=1,
            )

        filter_refs: list[str] = []
        if ws.auto_filter.ref:
            filter_refs.append(str(ws.auto_filter.ref))
        filter_refs.extend(str(table.ref) for table in ws.tables.values())
        covered = False
        for ref in filter_refs:
            try:
                min_col, min_row, max_col, _ = range_boundaries(ref)
                covered = covered or (min_col == 1 and min_row == 1 and max_col >= expected_width)
            except ValueError:
                continue
        if not covered:
            self.add(
                "error",
                "presentation.filters",
                "No filter range starts at A1 and covers every prescribed column.",
                sheet=ws.title,
                row=1,
            )

        unwrapped: list[str] = []
        for row in range(1, ws.max_row + 1):
            for col in range(1, expected_width + 1):
                cell = ws.cell(row, col)
                if not is_blank(cell.value) and cell.alignment.wrap_text is not True:
                    unwrapped.append(cell.coordinate)
        if unwrapped:
            self.add(
                "error",
                "presentation.wrap_text",
                f"{len(unwrapped)} nonempty prescribed cells do not have wrap text enabled; "
                f"first: {', '.join(unwrapped[:12])}.",
                sheet=ws.title,
                row=ws[unwrapped[0]].row,
            )

    def check_ledger(self) -> dict[str, Any]:
        ws = self.wb["Deal ledger"]
        schema_ok = self.check_schema(ws, LEDGER_COLUMNS)
        self.check_presentation(ws, len(LEDGER_COLUMNS))
        if not schema_ok:
            return {
                "rows": [],
                "by_number": {},
                "rounds": defaultdict(list),
                "round_openings": defaultdict(list),
                "deadlines": Counter(),
                "flags": {},
                "processes": set(),
            }

        columns = {name: index + 1 for index, name in enumerate(LEDGER_COLUMNS)}
        rows = nonempty_rows(ws, len(LEDGER_COLUMNS))
        records: list[dict[str, Any]] = []
        by_number: dict[int, int] = {}
        round_rows: dict[tuple[int, int], list[int]] = defaultdict(list)
        round_openings: dict[tuple[int, int], list[tuple[int, dt.date | None]]] = defaultdict(list)
        deadline_counts: Counter[tuple[int, int]] = Counter()
        flags: dict[int, set[str]] = {}
        processes: set[int] = set()
        previous_sort: tuple[dt.date, int] | None = None

        def value(row: int, column: str) -> Any:
            return ws.cell(row, columns[column]).value

        for ordinal, excel_row in enumerate(rows, start=1):
            record = {name: value(excel_row, name) for name in LEDGER_COLUMNS}
            records.append(record)
            row_number = as_integer(record["#"])
            if row_number != ordinal:
                self.add(
                    "error",
                    "ledger.sequence",
                    f"Event number must be {ordinal}; found {record['#']!r}.",
                    sheet=ws.title,
                    row=excel_row,
                    column="#",
                )
            elif row_number in by_number:
                self.add(
                    "error",
                    "ledger.duplicate_number",
                    f"Duplicate event number {row_number}.",
                    sheet=ws.title,
                    row=excel_row,
                    column="#",
                )
            else:
                by_number[row_number] = excel_row

            if is_blank(record["Who"]):
                self.add(
                    "error",
                    "ledger.who_blank",
                    "Who must never be blank.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Who",
                )

            type_value = record["Type"]
            if not is_blank(type_value) and type_value not in TYPES:
                self.add(
                    "error",
                    "controlled.type",
                    f"Type {type_value!r} is not allowed.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Type",
                )

            event = record["Event"]
            if event not in EVENTS:
                self.add(
                    "error",
                    "controlled.event",
                    f"Event {event!r} is not an allowed label.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Event",
                )

            process = as_integer(record["Process"])
            if process is None or process < 1:
                self.add(
                    "error",
                    "ledger.process",
                    f"Process must be a positive integer; found {record['Process']!r}.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Process",
                )
            else:
                processes.add(process)

            round_value = record["Round"]
            numbered_round = as_integer(round_value)
            if round_value == "post":
                numbered_round = None
            elif numbered_round is None or numbered_round < 0:
                self.add(
                    "error",
                    "ledger.round",
                    f"Round must be a nonnegative integer or 'post'; found {round_value!r}.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Round",
                )

            if process is not None and process >= 1 and numbered_round is not None and numbered_round > 0:
                key = (process, numbered_round)
                round_rows[key].append(excel_row)
                if event == "Round opened":
                    round_openings[key].append((excel_row, as_date(record["Sort date"])))
                if event == "Deadline":
                    deadline_counts[key] += 1
            elif event == "Round opened":
                self.add(
                    "error",
                    "round.opening_key",
                    "Round opened must carry a positive numbered round.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Round",
                )

            count = record["Count"]
            if not is_blank(count) and (not is_integer(count) or int(count) <= 0):
                self.add(
                    "error",
                    "ledger.count",
                    f"Count must be a positive integer or blank; found {count!r}.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Count",
                )
            if event in NO_BIDDER_COUNT_EVENTS and not is_blank(count):
                self.add(
                    "error",
                    "ledger.count_nonbidder",
                    f"Count must be blank on {event} rows.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Count",
                )
            if event in BID_EVENTS | {"Re-entered"} and is_blank(count):
                count_note = normalize_contiguous(record["Note"])
                documented_count = re.search(
                    r"\bCount:\s*(?:at least\b|more than\b|at most\b|fewer than\b|"
                    r"less than\b|approximately\b|about\b|unknown\b|not stated\b|"
                    r"\d+\s*[-–—]\s*\d+)",
                    count_note,
                    re.IGNORECASE,
                )
                self.add(
                    "warning" if documented_count else "error",
                    "ledger.count_uncertain" if documented_count else "ledger.count_bidder",
                    (
                        "Count is blank with a documented bound, estimate or unknown population; "
                        "review the source and do not use it as an exact count."
                        if documented_count
                        else f"Count is required on {event} rows unless the Note explains the "
                        "qualified or unknown population with 'Count: ...'."
                    ),
                    sheet=ws.title,
                    row=excel_row,
                    column="Count",
                )

            for price_column in ("Price low", "Price high"):
                price = record[price_column]
                if not is_blank(price) and (
                    isinstance(price, bool)
                    or not isinstance(price, (int, float))
                    or not math.isfinite(float(price))
                    or float(price) <= 0
                ):
                    self.add(
                        "error",
                        "bid.price_type",
                        f"{price_column} must be a positive number or blank; found {price!r}.",
                        sheet=ws.title,
                        row=excel_row,
                        column=price_column,
                    )
            low, high = record["Price low"], record["Price high"]
            if isinstance(low, (int, float)) and not isinstance(low, bool) and isinstance(high, (int, float)) and not isinstance(high, bool) and low > high:
                self.add(
                    "error",
                    "bid.price_order",
                    f"Price low {low!r} exceeds Price high {high!r}.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Price low",
                )
            if event in BID_EVENTS:
                for field, allowed in (
                    ("All cash", ALL_CASH),
                    ("Formality", FORMALITY),
                    ("Conditions", CONDITIONS),
                ):
                    field_value = record[field]
                    if field_value not in allowed:
                        self.add(
                            "error",
                            f"controlled.{field.lower().replace(' ', '_')}",
                            f"{field} must be filled with an allowed value on {event} rows; found {field_value!r}.",
                            sheet=ws.title,
                            row=excel_row,
                            column=field,
                        )
                if is_blank(low) != is_blank(high):
                    note = normalize_contiguous(record["Note"]).lower()
                    markers = ("at least", "no more than", "floor", "ceiling", "\u2265", "\u2264")
                    if not any(marker in note for marker in markers):
                        self.add(
                            "warning",
                            "bid.one_sided_price",
                            "Only one price endpoint is filled, but the Note does not visibly identify a floor or ceiling.",
                            sheet=ws.title,
                            row=excel_row,
                            column="Note",
                        )
            else:
                for field in ("Price low", "Price high", "All cash", "Formality", "Conditions"):
                    if not is_blank(record[field]):
                        self.add(
                            "error",
                            "bid.fields_on_nonbid",
                            f"{field} must be blank because {event!r} is not a bid row.",
                            sheet=ws.title,
                            row=excel_row,
                            column=field,
                        )

            exit_reason = record["Exit reason"]
            if event in EXIT_EVENTS:
                if exit_reason not in EXIT_REASONS:
                    self.add(
                        "error",
                        "controlled.exit_reason",
                        f"Exit reason must be filled with an allowed value on {event} rows; found {exit_reason!r}.",
                        sheet=ws.title,
                        row=excel_row,
                        column="Exit reason",
                    )
                elif record["Inferred"] == "Y" and exit_reason != "Not stated":
                    self.add(
                        "warning",
                        "exit.inferred_reason",
                        f"An inferred exit carries Exit reason 'Not stated' (C16); found {exit_reason!r}.",
                        sheet=ws.title,
                        row=excel_row,
                        column="Exit reason",
                    )
            elif not is_blank(exit_reason):
                self.add(
                    "error",
                    "ledger.exit_reason_nonexit",
                    "Exit reason is permitted only on exit rows.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Exit reason",
                )

            inferred = record["Inferred"]
            if inferred not in (None, "", "Y"):
                self.add(
                    "error",
                    "controlled.inferred",
                    f"Inferred must be 'Y' or blank; found {inferred!r}.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Inferred",
                )
            if inferred == "Y" and is_blank(record["Note"]):
                self.add(
                    "error",
                    "ledger.inference_note",
                    "An inferred row needs a Note explaining how the inference is known.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Note",
                )

            if word_count(record["Note"]) > 40:
                self.add(
                    "warning",
                    "ledger.note_length",
                    f"Note has {word_count(record['Note'])} words; aim for 40. "
                    "Retain the excess only for required facts that cannot be shortened.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Note",
                )

            quote_cell = record["Quote and page"]
            parsed_quote = parse_quote_and_page(quote_cell)
            if parsed_quote is None:
                self.add(
                    "error",
                    "quote.format",
                    "Quote and page must end with a p. or pp. printed-page reference.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Quote and page",
                )
            else:
                quote, _ = parsed_quote
                if not quote:
                    self.add(
                        "error",
                        "quote.empty",
                        "The quoted passage is empty.",
                        sheet=ws.title,
                        row=excel_row,
                        column="Quote and page",
                    )
                elif word_count(quote) > 30:
                    self.add(
                        "error",
                        "quote.length",
                        f"Quotation has {word_count(quote)} words; maximum is 30.",
                        sheet=ws.title,
                        row=excel_row,
                        column="Quote and page",
                    )
                if quote and not any(quote in filing_text for filing_text in self.filing_texts):
                    self.add(
                        "error",
                        "quote.not_contiguous_in_filing",
                        "Normalized quotation does not occur as one contiguous passage in the parsed full filing.",
                        sheet=ws.title,
                        row=excel_row,
                        column="Quote and page",
                    )

            flag = record["Flag"]
            if not is_blank(flag):
                flag_ids = parse_flag_ids(flag)
                if flag_ids is None:
                    self.add(
                        "error",
                        "controlled.flag",
                        f"Flag must contain only question ids such as Q1 or Q1, Q2; found {flag!r}.",
                        sheet=ws.title,
                        row=excel_row,
                        column="Flag",
                    )
                elif row_number is not None:
                    flags[row_number] = flag_ids

            if not is_blank(record["Reviewer note"]):
                self.add(
                    "error",
                    "reviewer_note.not_empty",
                    "Reviewer note must be empty.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Reviewer note",
                )

            parsed_dates: dict[str, dt.date | None] = {}
            for date_column in DATE_COLUMNS:
                date_value = record[date_column]
                parsed = as_date(date_value)
                parsed_dates[date_column] = parsed
                cell = ws.cell(excel_row, columns[date_column])
                if date_column == "Sort date" and is_blank(date_value):
                    self.add(
                        "error",
                        "date.sort_blank",
                        "Sort date must always be filled.",
                        sheet=ws.title,
                        row=excel_row,
                        column=date_column,
                    )
                elif not is_blank(date_value) and parsed is None:
                    self.add(
                        "error",
                        "date.not_excel_date",
                        f"{date_column} must be a real Excel date; found {date_value!r}.",
                        sheet=ws.title,
                        row=excel_row,
                        column=date_column,
                    )
                elif parsed is not None:
                    if date_has_time(date_value):
                        self.add(
                            "error",
                            "date.has_time",
                            f"{date_column} contains a time component.",
                            sheet=ws.title,
                            row=excel_row,
                            column=date_column,
                        )
                    if not has_mmddyyyy_format(cell):
                        self.add(
                            "error",
                            "date.format",
                            f"{date_column} must use Excel format MM/DD/YYYY; found {cell.number_format!r}.",
                            sheet=ws.title,
                            row=excel_row,
                            column=date_column,
                        )

            sort_date = parsed_dates["Sort date"]
            date_from = parsed_dates["Date from"]
            date_to = parsed_dates["Date to"]
            if date_from and date_to and date_from > date_to:
                self.add(
                    "error",
                    "date.window_reversed",
                    "Date from is later than Date to.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Date from",
                )
            when = record["When"]
            if isinstance(when, str) and re.fullmatch(r"\d{2}/\d{2}/\d{4}", when.strip()):
                try:
                    reported_day = dt.datetime.strptime(when.strip(), "%m/%d/%Y").date()
                except ValueError:
                    reported_day = None
                for date_column in DATE_COLUMNS:
                    if reported_day and parsed_dates[date_column] not in (None, reported_day):
                        self.add(
                            "error",
                            "date.exact_day_mismatch",
                            f"When reports the day {when.strip()}, so {date_column} must equal it (C10).",
                            sheet=ws.title,
                            row=excel_row,
                            column=date_column,
                        )
            if sort_date and date_from and sort_date < date_from:
                self.add(
                    "error",
                    "date.sort_outside_window",
                    "Sort date falls before Date from.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Sort date",
                )
            if sort_date and date_to and sort_date > date_to:
                self.add(
                    "error",
                    "date.sort_outside_window",
                    "Sort date falls after Date to.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Sort date",
                )
            if sort_date and previous_sort and sort_date < previous_sort[0]:
                self.add(
                    "error",
                    "date.sort_decreases",
                    f"Sort date {sort_date:%m/%d/%Y} is earlier than the prior populated row's "
                    f"{previous_sort[0]:%m/%d/%Y} (Excel row {previous_sort[1]}).",
                    sheet=ws.title,
                    row=excel_row,
                    column="Sort date",
                )
            if sort_date:
                previous_sort = (sort_date, excel_row)

        expected_processes = list(range(1, max(processes) + 1)) if processes else []
        if sorted(processes) != expected_processes:
            self.add(
                "error",
                "ledger.process_sequence",
                f"Processes must be consecutive from 1; found {sorted(processes)}.",
                sheet=ws.title,
            )
        for process in sorted(processes):
            used = sorted(round_number for proc, round_number in round_rows if proc == process)
            if used and used != list(range(1, max(used) + 1)):
                self.add(
                    "error",
                    "round.sequence",
                    f"Numbered rounds for Process {process} must be consecutive from 1; found {used}.",
                    sheet=ws.title,
                )
        for key, key_rows in round_rows.items():
            openings = round_openings.get(key, [])
            if len(openings) != 1:
                self.add(
                    "error",
                    "round.opening_count",
                    f"Process {key[0]} Round {key[1]} has {len(openings)} Round opened rows; expected exactly one.",
                    sheet=ws.title,
                    row=key_rows[0],
                    column="Event",
                )
            elif openings[0][0] != min(key_rows):
                self.add(
                    "error",
                    "round.opening_order",
                    f"Round opened is not the first ledger row assigned to Process {key[0]} Round {key[1]}.",
                    sheet=ws.title,
                    row=openings[0][0],
                    column="Event",
                )

        return {
            "rows": rows,
            "by_number": by_number,
            "rounds": round_rows,
            "round_openings": round_openings,
            "deadlines": deadline_counts,
            "flags": flags,
            "processes": processes,
        }

    def check_rounds(self, ledger: dict[str, Any]) -> None:
        ws = self.wb["Rounds"]
        schema_ok = self.check_schema(ws, ROUND_COLUMNS)
        self.check_presentation(ws, len(ROUND_COLUMNS))
        if not schema_ok:
            return

        rows = nonempty_rows(ws, len(ROUND_COLUMNS))
        keys: list[tuple[int, int]] = []
        opened: dict[tuple[int, int], tuple[int, dt.date | None]] = {}
        for excel_row in rows:
            values = {name: ws.cell(excel_row, col + 1).value for col, name in enumerate(ROUND_COLUMNS)}
            process, round_number = as_integer(values["Process"]), as_integer(values["Round"])
            if process is None or process < 1 or round_number is None or round_number < 1:
                self.add(
                    "error",
                    "rounds.key",
                    f"Process and Round must be positive integers; found {values['Process']!r}, {values['Round']!r}.",
                    sheet=ws.title,
                    row=excel_row,
                )
                continue
            key = (process, round_number)
            keys.append(key)
            if key in opened:
                self.add(
                    "error",
                    "rounds.duplicate",
                    f"Duplicate Process {process} Round {round_number} summary row.",
                    sheet=ws.title,
                    row=excel_row,
                )

            for field in ROUND_COLUMNS[2:]:
                if field == "Deadline outcome":
                    # Future or superseded deadlines can leave this cell blank;
                    # validate it against the reached Deadline rows below.
                    continue
                if is_blank(values[field]):
                    self.add(
                        "error",
                        "rounds.required",
                        f"{field} must be filled on every Rounds row.",
                        sheet=ws.title,
                        row=excel_row,
                        column=field,
                    )

            opened_date = as_date(values["Opened"])
            opened[key] = (excel_row, opened_date)
            opened_cell = ws.cell(excel_row, ROUND_COLUMNS.index("Opened") + 1)
            if opened_date is None and not is_blank(values["Opened"]):
                self.add(
                    "error",
                    "rounds.opened_type",
                    f"Opened must be a real Excel date; found {values['Opened']!r}.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Opened",
                )
            elif opened_date is not None and not has_mmddyyyy_format(opened_cell):
                self.add(
                    "error",
                    "date.format",
                    f"Opened must use Excel format MM/DD/YYYY; found {opened_cell.number_format!r}.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Opened",
                )

            if values["Finality"] not in FINALITY:
                self.add(
                    "error",
                    "controlled.finality",
                    f"Finality {values['Finality']!r} is not allowed.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Finality",
                )

            due_dates = normalize_contiguous(values["Due dates"])
            outcome = (
                "" if is_blank(values["Deadline outcome"])
                else normalize_contiguous(values["Deadline outcome"])
            )
            deadline_count = ledger["deadlines"].get(key, 0)
            if outcome == "No deadline stated":
                if due_dates.lower() != "none stated":
                    self.add(
                        "error",
                        "rounds.no_deadline_pair",
                        "Deadline outcome is 'No deadline stated' but Due dates is not 'none stated'.",
                        sheet=ws.title,
                        row=excel_row,
                        column="Due dates",
                    )
                if deadline_count:
                    self.add(
                        "error",
                        "rounds.deadline_count",
                        f"Rounds says no deadline, but the ledger has {deadline_count} Deadline row(s) for this round.",
                        sheet=ws.title,
                        row=excel_row,
                        column="Deadline outcome",
                    )
            elif outcome:
                outcomes = [part.strip() for part in outcome.split(";")]
                bad = [part for part in outcomes if part not in DEADLINE_OUTCOMES]
                if bad:
                    self.add(
                        "error",
                        "controlled.deadline_outcome",
                        f"Unallowed deadline outcome value(s): {bad!r}.",
                        sheet=ws.title,
                        row=excel_row,
                        column="Deadline outcome",
                    )
                if deadline_count != len(outcomes):
                    self.add(
                        "error",
                        "rounds.deadline_count",
                        f"Ledger has {deadline_count} Deadline row(s), but Rounds lists {len(outcomes)} outcome(s).",
                        sheet=ws.title,
                        row=excel_row,
                        column="Deadline outcome",
                    )
            elif deadline_count:
                self.add(
                    "error",
                    "rounds.deadline_count",
                    f"Ledger has {deadline_count} Deadline row(s), but Deadline outcome is blank.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Deadline outcome",
                )
            elif due_dates.lower() == "none stated":
                self.add(
                    "error",
                    "rounds.no_deadline_pair",
                    "Due dates is 'none stated', so Deadline outcome must be 'No deadline stated'.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Deadline outcome",
                )

        if keys != sorted(keys):
            self.add(
                "error",
                "rounds.order",
                "Rounds rows must be ordered by Process and Round.",
                sheet=ws.title,
            )
        ledger_keys = set(ledger["rounds"])
        sheet_keys = set(keys)
        for key in sorted(ledger_keys - sheet_keys):
            self.add(
                "error",
                "rounds.missing_summary",
                f"Process {key[0]} Round {key[1]} appears in the ledger but not in Rounds.",
                sheet=ws.title,
            )
        for key in sorted(sheet_keys - ledger_keys):
            row = opened[key][0] if key in opened else None
            self.add(
                "error",
                "rounds.orphan_summary",
                f"Process {key[0]} Round {key[1]} appears in Rounds but not in the ledger.",
                sheet=ws.title,
                row=row,
            )
        for key in sorted(ledger_keys & sheet_keys):
            ledger_openings = ledger["round_openings"].get(key, [])
            if len(ledger_openings) == 1 and key in opened:
                ledger_date = ledger_openings[0][1]
                summary_date = opened[key][1]
                if ledger_date is not None and summary_date is not None and ledger_date != summary_date:
                    self.add(
                        "error",
                        "rounds.opened_mismatch",
                        f"Opened {summary_date:%m/%d/%Y} does not equal the Round opened row's Sort date "
                        f"{ledger_date:%m/%d/%Y}.",
                        sheet=ws.title,
                        row=opened[key][0],
                        column="Opened",
                    )

    def check_questions(self, ledger: dict[str, Any]) -> None:
        ws = self.wb["Questions"]
        schema_ok = self.check_schema(ws, QUESTION_COLUMNS)
        self.check_presentation(ws, len(QUESTION_COLUMNS))
        if not schema_ok:
            return

        rows = nonempty_rows(ws, len(QUESTION_COLUMNS))
        q_rows: dict[str, int] = {}
        affected_by_q: dict[str, tuple[set[int], bool]] = {}
        question_texts: list[str] = []
        for ordinal, excel_row in enumerate(rows, start=1):
            values = {name: ws.cell(excel_row, col + 1).value for col, name in enumerate(QUESTION_COLUMNS)}
            qid = str(values["Q"]).strip() if not is_blank(values["Q"]) else ""
            expected = f"Q{ordinal}"
            if qid != expected:
                self.add(
                    "error",
                    "questions.sequence",
                    f"Question id must be {expected}; found {values['Q']!r}.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Q",
                )
            if qid in q_rows:
                self.add(
                    "error",
                    "questions.duplicate",
                    f"Duplicate question id {qid!r}.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Q",
                )
            elif QID_RE.fullmatch(qid):
                q_rows[qid] = excel_row

            for field in QUESTION_COLUMNS[1:-1]:
                if is_blank(values[field]):
                    self.add(
                        "error",
                        "questions.required",
                        f"{field} must be filled.",
                        sheet=ws.title,
                        row=excel_row,
                        column=field,
                    )
            if not is_blank(values["Reviewer note"]):
                self.add(
                    "error",
                    "reviewer_note.not_empty",
                    "Reviewer note must be empty.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Reviewer note",
                )

            refs, parseable = parse_affected_rows(values["Rows affected"])
            if qid:
                affected_by_q[qid] = (refs, parseable)
            if not is_blank(values["Rows affected"]) and not parseable:
                self.add(
                    "warning",
                    "questions.rows_unparsed",
                    "Rows affected is narrative/global, so its row links could not be checked mechanically.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Rows affected",
                )
            for ref in sorted(refs):
                if ref not in ledger["by_number"]:
                    self.add(
                        "error",
                        "questions.unknown_row",
                        f"Rows affected cites nonexistent ledger row #{ref}.",
                        sheet=ws.title,
                        row=excel_row,
                        column="Rows affected",
                    )
                elif qid not in ledger["flags"].get(ref, set()):
                    self.add(
                        "warning",
                        "questions.flag_mismatch",
                        f"Rows affected cites #{ref}, but that ledger row's focused Flag does not include {qid!r}.",
                        sheet=ws.title,
                        row=excel_row,
                        column="Rows affected",
                    )

            text = normalize_contiguous(values["Question"]).lower()
            question_texts.append(text)
            total_words = sum(word_count(values[field]) for field in QUESTION_COLUMNS[1:-1])
            if total_words > 90:
                self.add(
                    "warning",
                    "questions.length",
                    f"Question entry has about {total_words} words across its review fields; the instruction asks for about 60.",
                    sheet=ws.title,
                    row=excel_row,
                )

        for row_number, qids in ledger["flags"].items():
            excel_row = ledger["by_number"].get(row_number)
            for qid in sorted(qids):
                if qid not in q_rows:
                    self.add(
                        "error",
                        "questions.unknown_flag",
                        f"Flag {qid} has no Questions row.",
                        sheet="Deal ledger",
                        row=excel_row,
                        column="Flag",
                    )
                    continue
                refs, parseable = affected_by_q.get(qid, (set(), False))
                if parseable and row_number not in refs:
                    self.add(
                        "warning",
                        "questions.reverse_link",
                        f"Ledger row #{row_number} is flagged {qid}, but {qid}'s broad Rows affected range does not cite it.",
                        sheet="Deal ledger",
                        row=excel_row,
                        column="Flag",
                    )

        if not any("process" in text and "round" in text for text in question_texts):
            self.add(
                "warning",
                "questions.process_round_map",
                "No Question visibly mentions both the process and round map; wording may need manual review.",
                sheet=ws.title,
            )
        if sum(ledger["deadlines"].values()) and not any(
            "deadline" in text and "outcome" in text for text in question_texts
        ):
            self.add(
                "warning",
                "questions.deadline_outcomes",
                "The ledger has a reached Deadline, but no Question visibly mentions deadline outcomes.",
                sheet=ws.title,
            )

    def check_facts(self, ledger: dict[str, Any]) -> None:
        ws = self.wb["Deal facts"]
        schema_ok = self.check_schema(ws, FACT_COLUMNS)
        self.check_presentation(ws, len(FACT_COLUMNS))
        if not schema_ok:
            return

        rows = nonempty_rows(ws, len(FACT_COLUMNS))
        actual_fields = [ws.cell(row, 1).value for row in rows]
        # "Earlier approaches" (v1.9, C7) follows Number of processes; workbooks made under v1.8 lack it.
        required_fields = [
            field
            for index, field in enumerate(actual_fields)
            if not (
                field in EARLIER_APPROACHES_FIELDS
                and index > 0
                and actual_fields[index - 1] == "Number of processes"
            )
        ]
        fields_match = len(required_fields) == len(FACT_FIELD_OPTIONS) and all(
            actual in allowed for actual, allowed in zip(required_fields, FACT_FIELD_OPTIONS, strict=True)
        )
        if not fields_match:
            self.add(
                "error",
                "facts.fields",
                f"Deal facts fields must appear exactly in the prescribed order; found {actual_fields!r}.",
                sheet=ws.title,
                row=rows[0] if rows else 2,
                column="Field",
            )
        values: dict[str, Any] = {}
        for excel_row in rows:
            field = ws.cell(excel_row, 1).value
            value = ws.cell(excel_row, 2).value
            if isinstance(field, str):
                values[field] = value
            if is_blank(value):
                self.add(
                    "error",
                    "facts.value_blank",
                    f"Value is blank for field {field!r}.",
                    sheet=ws.title,
                    row=excel_row,
                    column="Value",
                )

        acquirer_type = values.get("Acquirer type")
        if not is_blank(acquirer_type) and not starts_with_canonical(acquirer_type, TYPES):
            self.add(
                "error",
                "controlled.acquirer_type",
                f"Acquirer type {acquirer_type!r} is not allowed.",
                sheet=ws.title,
                row=self._fact_row(rows, ws, "Acquirer type"),
                column="Value",
            )
        initiation_field = next((field for field in INITIATION_FIELDS if field in values), None)
        initiation = values.get(initiation_field) if initiation_field else None
        if not is_blank(initiation) and not starts_with_canonical(initiation, INITIATION):
            self.add(
                "error",
                "controlled.initiation",
                f"Initiation {initiation!r} is not allowed.",
                sheet=ws.title,
                row=self._fact_row(rows, ws, initiation_field),
                column="Value",
            )
        process_count = values.get("Number of processes")
        expected_process_count = len(ledger["processes"])
        parsed_process_count = as_integer_or_text(process_count)
        if not is_blank(process_count) and parsed_process_count != expected_process_count:
            self.add(
                "error",
                "facts.process_count",
                f"Number of processes must equal the ledger's {expected_process_count}; found {process_count!r}.",
                sheet=ws.title,
                row=self._fact_row(rows, ws, "Number of processes"),
                column="Value",
            )
        auction_field = next((field for field in AUCTION_SCREEN_FIELDS if field in values), None)
        auction = normalize_contiguous(values.get(auction_field)) if auction_field else ""
        if auction and (
            re.match(r"^(Met|Not met|Uncertain)(?:\b|:)", auction) is None
            or (
                re.search(r"\b\d+\b", auction) is None
                and re.search(r"\bcount unknown\b", auction, re.IGNORECASE) is None
            )
        ):
            self.add(
                "error",
                "facts.auction_screen",
                "Auction screen must start with Met, Not met, or Uncertain and include "
                "a supported number or 'count unknown'.",
                sheet=ws.title,
                row=self._fact_row(rows, ws, auction_field),
                column="Value",
            )
        whole_company_field = next((field for field in WHOLE_COMPANY_FIELDS if field in values), None)
        whole_company = normalize_contiguous(values.get(whole_company_field)) if whole_company_field else ""
        if whole_company and not starts_with_canonical(whole_company, {"Yes", "No"}):
            self.add(
                "error",
                "facts.whole_company_bids",
                "Whole-company bids must be 'Yes', or start with 'No' and say what was bid for.",
                sheet=ws.title,
                row=self._fact_row(rows, ws, whole_company_field),
                column="Value",
            )
        account_field = next((field for field in ACCOUNT_FIELDS if field in values), None)
        account = normalize_contiguous(values.get(account_field)) if account_field else ""
        if account:
            sentence_count = len(re.findall(r"(?:[.!?](?:[\"\u201d']*)\s+|[.!?](?:[\"\u201d']*)$)", account))
            if sentence_count not in (5, 6):
                self.add(
                    "warning",
                    "facts.account_sentences",
                    f"Account appears to have {sentence_count} sentences; the instruction asks for five or six.",
                    sheet=ws.title,
                    row=self._fact_row(rows, ws, account_field),
                    column="Value",
                )

    @staticmethod
    def _fact_row(rows: list[int], ws: Any, field: str) -> int | None:
        return next((row for row in rows if ws.cell(row, 1).value == field), None)

    def run(self) -> dict[str, Any]:
        if self.load_inputs():
            actual_sheets = self.wb.sheetnames
            if actual_sheets != SHEETS:
                self.add(
                    "error",
                    "schema.sheets",
                    f"Workbook must contain exactly {SHEETS!r} in that order; found {actual_sheets!r}.",
                )
            available = set(actual_sheets)
            ledger: dict[str, Any] = {
                "rows": [],
                "by_number": {},
                "rounds": defaultdict(list),
                "round_openings": defaultdict(list),
                "deadlines": Counter(),
                "flags": {},
                "processes": set(),
            }
            if "Deal ledger" in available:
                ledger = self.check_ledger()
            if "Rounds" in available:
                self.check_rounds(ledger)
            if "Questions" in available:
                self.check_questions(ledger)
            if "Deal facts" in available:
                self.check_facts(ledger)

        counts = Counter(issue["severity"] for issue in self.issues)
        if self.fatal:
            status = "error"
        elif counts["error"]:
            status = "fail"
        elif counts["warning"]:
            status = "pass_with_warnings"
        else:
            status = "pass"
        return {
            "checker": "lean-mechanical",
            "checker_version": CHECKER_VERSION,
            "checker_revision": CHECKER_REVISION,
            "workbook": str(self.workbook_path),
            "filing": str(self.filing_path),
            "status": status,
            "scope_note": (
                "Mechanical checks only. Quote occurrence proves source occurrence, not semantic support. "
                "No bidder-population arithmetic or substantive extraction grading is performed."
            ),
            "summary": {
                "errors": counts["error"],
                "warnings": counts["warning"],
                "information": counts["info"],
                "total_issues": len(self.issues),
            },
            "issues": [{**issue, "basis": "mechanical"} for issue in self.issues],
        }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workbook", required=True, type=Path, help="Workbook to check")
    parser.add_argument("--filing", required=True, type=Path, help="Full SEC filing in HTML")
    parser.add_argument("--output", required=True, type=Path, help="JSON report path")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    checker = LeanChecker(args.workbook, args.filing)
    report = checker.run()
    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"Could not write JSON report {args.output}: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print(
        f"{report['status']}: {report['summary']['errors']} error(s), "
        f"{report['summary']['warnings']} warning(s)"
        + f"; report={args.output}"
    )
    if report["status"] == "error":
        return 2
    return 1 if report["summary"]["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
