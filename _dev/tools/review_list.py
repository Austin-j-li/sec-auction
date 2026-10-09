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
    "non_dollar_price", "round_opened", "multi_process", "conditions_unclear", "none_on_silence",
    "initiation_differs",
)
# E12's condition columns that a Conditions None reading rests on.
CONDITION_COLUMNS = ("Due diligence", "Financing", "Regulatory")
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
        if event == "Round opened":
            key = (check_lean.as_integer_or_text(r.get("Process")), check_lean.as_integer_or_text(r.get("Round")))
            add("round_opened", "Deal ledger", number, who, f"Round trigger: {round_triggers.get(key, '(missing)')}")
        # E12 on Formal whole-company bids, where Conditions decides the T1 and T1u readings.
        if event in derive_analysis.WHOLE_BIDS and r.get("Formality") == "Formal":
            if r.get("Conditions") == "Unclear":
                add("conditions_unclear", "Deal ledger", number, who, "Formal bid with Conditions Unclear")
            elif r.get("Conditions") == "None" and all(r.get(c) == "Not stated" for c in CONDITION_COLUMNS):
                add("none_on_silence", "Deal ledger", number, who,
                    "Formal bid with Conditions None, but Due diligence, Financing and Regulatory are all Not stated")

    # Currency and price basis: one deal-level item each, from Deal facts and the bid rows' Notes.
    units = derive_analysis.text(facts.get("Currency and units of bid prices"))
    bid_notes = [(derive_analysis.cell(r.get("#")), derive_analysis.text(r.get("Note"))) for r in rows
                 if derive_analysis.text(r.get("Event")) in bid_events]
    for category, pattern, label in (("non_per_share_price", NON_SHARE_BASIS_RE, "Price basis needs review"),
                                     ("non_dollar_price", NON_DOLLAR_RE, "Currency needs review")):
        in_notes = [f"#{number}" for number, note in bid_notes if pattern.search(note)]
        if bid_notes and (pattern.search(units) or in_notes):
            add(category, "Deal facts", "Currency and units of bid prices", "",
                f"{label}: Deal facts gives {units!r}"
                + (f"; bid Notes at {', '.join(in_notes)}" if in_notes else ""))

    for line in ledger["rounds"]:
        outcome = derive_analysis.text(line.get("Deadline outcome"))
        if outcome and outcome != check_lean.NO_DEADLINE:
            add("deadline_outcome", "Rounds", f"{line.get('Process')}/{line.get('Round')}", "", outcome)
    processes = {check_lean.as_integer_or_text(r.get("Process")) for r in rows}
    processes.discard(None)
    if len(processes) > 1:
        add("multi_process", "Deal facts", "Number of processes", "", f"{len(processes)} processes")
    if "initiation_differs" not in disabled:
        for line in derive_analysis.derive(ledger, "")["deal"]:
            if line["initiation_check"] == "differs":
                add("initiation_differs", "Deal facts", "Initiation", "",
                    f"Initiation is {line['initiation_recorded']!r}, but D5's rule gives {line['initiation_first_event']} "
                    f"from {line['initiation_first_row']}")
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
