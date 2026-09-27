#!/usr/bin/env python3
"""Compare check_lean.py's column lists and value lists with an instruction's text.

Usage:
    python3 compare_lists.py --checker CHECKER --instruction INSTRUCTION

Reads both files and prints one line per comparison; writes nothing. Exit status 1 if any
comparison fails.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--checker", required=True, type=Path, help="check_lean.py")
    parser.add_argument("--instruction", required=True, type=Path, help="v1.14 instruction text")
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("check_lean_compared", args.checker)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    text = args.instruction.read_text(encoding="utf-8")
    lines = text.splitlines()

    def section(start: str, stop: str) -> list[str]:
        i = next(n for n, line in enumerate(lines) if line.startswith(start))
        return lines[i:next(n for n, line in enumerate(lines) if n > i and line.startswith(stop))]

    def numbered(start: str, stop: str) -> list[str]:
        return [m.group(1) for line in section(start, stop) if (m := re.match(r"\d+\. \*\*(.+?)\*\*", line))]

    def split(values: str) -> set[str]:
        return {part.strip() for part in re.split(r",\s*(?:or\s+)?|\s+or\s+|;\s*", values) if part.strip()}

    def column(name: str) -> str:
        line = next(line for line in section("### D1.", "### D2.") if f"**{name}** — " in line)
        return line.split(" — ", 1)[1]

    labels = [label.strip() for line in section("### D2.", "### D3.")
              if (m := re.match(r"- \*\*(.+?)\*\*", line)) for label in m.group(1).split(";")]
    facts = next(line for line in section("### D5.", "## E.") if line.startswith("Two columns"))
    facts = [part.strip().split(" (")[0] for part in re.split(r";\s*(?![^()]*\))", facts.split("fields in this order: ")[1].rstrip("."))]
    outcomes = re.search(r"separated by semicolons: (.+?)\. Blank", text).group(1)
    e9 = [m.group(1) for line in section("### E9.", "### E10.") if (m := re.match(r"\d\. \*\*(.+?)\*\*", line))]
    reasons = re.search(r"\*\*Exit reason\*\* — one of: (.+?)\. The first four", text).group(1)
    stock = next(line for line in section("### E13.", "### E14.") if line.startswith("**Stock %**"))
    checks = [
        ("Deal ledger columns (D1)", numbered("### D1.", "### D2.") == cl.LEDGER_COLUMNS_V114),
        ("Rounds columns (D3)", numbered("### D3.", "### D4.") == cl.ROUND_COLUMNS),
        ("Questions columns (D4)", re.findall(r"\*\*(.+?)\*\*", next(line for line in section("### D4.", "### D5.") if line.startswith("Columns:"))) == cl.QUESTION_COLUMNS),
        ("Event labels (D2)", len(labels) == len(set(labels)) and set(labels) == cl.EVENTS),
        ("Deal facts fields (D5)", facts == cl.FACT_FIELDS),
        ("Deadline outcome (D3)", {part.strip() for part in re.split(r", (?![^()]*\))", outcomes)} == cl.deadline_outcomes(cl.SCHEMA_V114)),
        ("Deadline outcome (E9 list)", set(e9) == cl.deadline_outcomes(cl.SCHEMA_V114)),
        ("No deadline stated (D3)", f"{cl.NO_DEADLINE} only when none was set" in text),
        ("Late bids accepted absent", cl.LEGACY_DEADLINE_OUTCOME not in text),
        ("Exit reason (E14)", {part.strip() for part in reasons.split(";")} == cl.EXIT_REASONS),
        ("Finality (D3)", split(re.search(r"\*\*Finality\*\* — (.+?) \(E6\)", text).group(1)) == cl.FINALITY),
        ("Type (D1)", split(column("Type").split(" for bidders")[0]) == cl.TYPES),
        ("Formality (D1)", split(column("Formality").split(", on those rows")[0]) == cl.FORMALITY),
        ("Conditions (D1)", split(column("Conditions").split(", on those rows")[0]) == cl.CONDITIONS),
        *((f"{name} (D1)", split(column(name).split(", on those rows")[0]) == allowed) for name, allowed in cl.CONDITION_COLUMNS.items()),
        ("CVR/earnout and Antitrust take Y or Varies (D1)", all("Y where" in column(n) and "Varies on a cohort row" in column(n) for n in ("CVR/earnout", "Antitrust")) and cl.MARKER == {"Y", "Varies"}),
        ("Stock % codes (E13)", all(f"**{code}**" in stock for code in cl.STOCK_CODES) and cl.STOCK_CODES == {"Part stock", "Not stated", "Varies"}),
        ("Stock % range example (E13)", "(“40–60”)" in stock and bool(cl.STOCK_RANGE_RE.fullmatch("40–60"))),
        ("Initiation (D5)", split(re.search(r"Initiation \((.+?)\)", text).group(1)) == cl.INITIATION),
        ("Acquirer type (D5)", "Acquirer type begins with Strategic, Financial, Mixed or Unknown" in text),
    ]
    for name, ok in checks:
        print(f"{'equal' if ok else 'DIFFERS':8} {name}")
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
