#!/usr/bin/env python3
"""Build the switchable, cell-derived Version 1 human review queue.

This queue points a reviewer to ledger cells. It does not validate a coding against the filing.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import check_lean
import derive_analysis


CATEGORIES = (
    "unknown_type", "qualified_count", "type_unsplit_count", "inferred_exit",
    "unexplained_exit", "deadline_outcome", "partial_only", "non_per_share_price",
    "non_dollar_price", "round_opened", "multi_process",
)
NON_DOLLAR_RE = re.compile(
    r"\b(?:EUR|GBP|CAD|CNY|JPY|CHF|AUD|NZD|MXN|INR|BRL|SEK|NOK|DKK|HKD|SGD|ZAR|KRW|TWD|ILS|"
    r"euros?|pounds?|francs?|yen|yuan|rupees?|Canadian dollars?|Australian dollars?|"
    r"currency (?:not stated|unknown))\b|[€£¥]", re.I)
NON_SHARE_BASIS_RE = re.compile(
    r"\b(?:enterprise value|equity value|aggregate|total price|per unit|exchange ratio|"
    r"buyer shares? per target share|share exchange)\b", re.I)


def build_review_list(ledger: dict[str, Any], disabled: set[str] | None = None) -> list[dict[str, Any]]:
    """Return review items for enabled categories, using only workbook cells."""
    disabled = set(disabled or ())
    unknown = disabled - set(CATEGORIES)
    if unknown:
        raise ValueError(f"unknown review categories: {', '.join(sorted(unknown))}")
    rows = ledger["ledger"]
    facts = ledger["facts"]
    items: list[dict[str, Any]] = []

    def add(category: str, sheet: str, row: Any, who: Any, detail: str) -> None:
        if category not in disabled:
            items.append({"category": category, "sheet": sheet, "row": row or "",
                          "who": derive_analysis.text(who), "detail": detail})

    bid_events = check_lean.BID_EVENTS
    all_bid_events = {r.get("Event") for r in rows if r.get("Event") in bid_events}
    partial_only = "Other-scope bid" in all_bid_events and (
        derive_analysis.text(facts.get("Whole-company bids")).startswith("No")
        or all_bid_events == {"Other-scope bid"})
    round_triggers = {(check_lean.as_integer_or_text(r.get("Process")), check_lean.as_integer_or_text(r.get("Round"))):
                      derive_analysis.text(r.get("How opened")) for r in ledger["rounds"]}
    units = derive_analysis.text(facts.get("Currency and units of bid prices"))
    non_dollar = bool(NON_DOLLAR_RE.search(units))
    non_per_share = bool(NON_SHARE_BASIS_RE.search(units))
    if derive_analysis.text(facts.get("Acquirer type")).startswith("Unknown"):
        add("unknown_type", "Deal facts", "Acquirer type", facts.get("Acquirer"), "Winner type is Unknown")
    if partial_only:
        add("partial_only", "Deal facts", "Whole-company bids", "", "Deal has only Other-scope bids")
    for r in rows:
        number, event, who = r.get("#"), derive_analysis.text(r.get("Event")), r.get("Who")
        note = derive_analysis.text(r.get("Note"))
        if (r.get("Type") == "Unknown" and
                (event == "Merger agreement signed" and check_lean.as_integer(r.get("Count")) == 1
                 or event in bid_events and r.get("Formality") == "Formal")):
            add("unknown_type", "Deal ledger", number, who, "Unknown type for a winner or Formal bidder")
        if check_lean.is_blank(r.get("Count")) and (check_lean.COUNT_QUALIFIER_RE.search(note)
                or check_lean.COUNT_RANGE_RE.search(note) or check_lean.COUNT_UNKNOWN_RE.search(note)):
            add("qualified_count", "Deal ledger", number, who, "Count is qualified or unsized in the Note")
        if r.get("Type") == "Unknown" and (check_lean.is_cohort(r) or "at least" in note.casefold()):
            add("type_unsplit_count", "Deal ledger", number, who, "Bidder types are not split in this count")
        if event in check_lean.EXIT_EVENTS:
            if r.get("Inferred") == "Y":
                add("inferred_exit", "Deal ledger", number, who, "Exit is inferred")
            if r.get("Exit reason") == "Not stated":
                add("unexplained_exit", "Deal ledger", number, who, "Exit reason is Not stated")
        if event in bid_events:
            if non_per_share or NON_SHARE_BASIS_RE.search(note):
                add("non_per_share_price", "Deal ledger", number, who, "Price basis needs review")
            if non_dollar or NON_DOLLAR_RE.search(note):
                add("non_dollar_price", "Deal ledger", number, who, "Currency needs review")
        if event == "Round opened":
            key = (check_lean.as_integer_or_text(r.get("Process")), check_lean.as_integer_or_text(r.get("Round")))
            add("round_opened", "Deal ledger", number, who, f"Round trigger: {round_triggers.get(key, '(missing)')}")

    for line in ledger["rounds"]:
        outcome = derive_analysis.text(line.get("Deadline outcome"))
        if outcome and outcome != check_lean.NO_DEADLINE:
            add("deadline_outcome", "Rounds", f"{line.get('Process')}/{line.get('Round')}", "", outcome)
    processes = {check_lean.as_integer_or_text(r.get("Process")) for r in rows}
    processes.discard(None)
    if len(processes) > 1:
        add("multi_process", "Deal facts", "Number of processes", "", f"{len(processes)} processes")
    return items


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--disable", action="append", choices=CATEGORIES, default=[], metavar="CATEGORY")
    parser.add_argument("--output", type=Path, help="JSON file; stdout when omitted")
    args = parser.parse_args(argv)
    try:
        if args.output:
            # As derive_analysis.py guards --out: never write into the data folders or over the input.
            derive_analysis.check_outside_data(args.output, "--output")
            if args.output.resolve() == args.workbook.resolve():
                raise derive_analysis.DeriveError("--output must not be the input workbook")
        items = build_review_list(derive_analysis.load(args.workbook), set(args.disable))
        result = json.dumps({"categories": list(CATEGORIES), "disabled": args.disable, "items": items}, indent=2) + "\n"
        if args.output:
            args.output.write_text(result, encoding="utf-8")
        else:
            print(result, end="")
    except (OSError, derive_analysis.DeriveError) as exc:
        parser.exit(2, f"review_list: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
