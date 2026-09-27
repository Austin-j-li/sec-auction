#!/usr/bin/env python3
"""Show operational progress only; never read workbook cells."""
from pathlib import Path
from collections import Counter
import datetime as dt
import json

packet = Path(__file__).resolve().parents[1]
root = packet.parents[2] / "_dev/runs" / packet.name
plan = json.loads((packet / "plan.json").read_text())
counts, terminal, saved = Counter(), [], 0
for cell in plan["cells"]:
    folder = root / cell["id"]
    if not (folder / "status.json").exists():
        folder = packet / "runs" / cell["id"]
    status_file = folder / "status.json"
    status = json.loads(status_file.read_text()) if status_file.exists() else {"state": "prepared"}
    counts[status["state"]] += 1
    saved += any(p.is_file() for p in (folder / "extraction" / f"{cell['deal']}.xlsx", folder / f"{cell['deal']}.xlsx"))
    if status["state"] not in ("running", "prepared"):
        terminal.append({"id": cell["id"], "state": status["state"],
                         "reason": status.get("failure_reason"), "error": status.get("error"),
                         "elapsed_seconds": status.get("elapsed_seconds")})
print(json.dumps({"at": dt.datetime.now(dt.timezone.utc).isoformat(), "counts": dict(counts),
                  "terminal": terminal, "workbooks_saved_so_far": saved,
                  "receipts": len(list((packet / "runs").glob("*/receipt.json")))}, indent=2))
