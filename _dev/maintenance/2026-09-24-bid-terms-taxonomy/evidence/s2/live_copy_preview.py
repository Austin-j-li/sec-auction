"""S2/MIG-C evidence on a copy of the live cockpit state: the rebase preview for the two pilot deals, the checker
shown for every version, and the thread labels. The live database is opened only through a mode=ro URI and copied
with the SQLite backup API; version files are copied. Nothing in the live checkout is written."""
from __future__ import annotations

import datetime as dt
import json
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

LIVE = Path("/home/uctpiaj/work/Projects/sec-extraction")
SANDBOX = Path("/home/uctpiaj/work/tmp/v114-scratch/pkg/s2")
sys.path.insert(0, str(SANDBOX / "_dev/tools"))

from cockpit import data  # noqa: E402


def main() -> int:
    output = Path(sys.argv[1])
    with tempfile.TemporaryDirectory(prefix="s2-live-copy-") as folder:
        root = Path(folder)
        for part in ("extraction", "raw_filing"):
            shutil.copytree(SANDBOX / part, root / part)
        (root / "_dev/cockpit/state").mkdir(parents=True)
        shutil.copy2(LIVE / "_dev/cockpit/catalog.json", root / "_dev/cockpit/catalog.json")
        shutil.copytree(LIVE / "_dev/cockpit/state/versions", root / "_dev/cockpit/state/versions")
        shutil.copytree(LIVE / "_dev/cockpit/state/filings", root / "_dev/cockpit/state/filings")
        shutil.copytree(LIVE / "_dev/cockpit/state/instructions", root / "_dev/cockpit/state/instructions")
        packet = "_dev/reviews/2026-09-22-opus55-reextraction"
        (root / packet).mkdir(parents=True)
        shutil.copy2(LIVE / packet / "reextraction.json", root / packet / "reextraction.json")
        shutil.copytree(LIVE / packet / "receipts", root / packet / "receipts")
        source = sqlite3.connect(f"file:{LIVE / '_dev/cockpit/state/workspace.sqlite3'}?mode=ro", uri=True)
        target = sqlite3.connect(root / "_dev/cockpit/state/workspace.sqlite3")
        source.backup(target)
        source.close(); target.close()

        cockpit = data.Cockpit(root)
        ws = cockpit.workspace
        report = {"run_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "deals": {}}
        for slug in sorted(ws.catalog()["deals"]):
            payload = ws.deal(slug)
            entry = {"ledger_schema": payload["ledger_schema"], "revision": payload["workspace"]["revision"],
                     "live_check": payload["check"]["checker_version"],
                     "versions": {v["id"]: v.get("checker") for v in payload["versions"] if v["id"] != "working"},
                     "row_marks": len(payload["row_review"]),
                     "threads": [(t["target"]["kind"], t["target_missing"], t.get("target_context")) for t in cockpit.trace.comments(slug)["threads"]]}
            pilots = [v["id"] for v in payload["versions"] if v.get("started_at") and v["id"] != payload["workspace"]["base_version"]]
            if pilots:
                entry["rebase_preview"] = {ident: ws.rebase_preview(slug, ident) for ident in pilots}
            report["deals"][slug] = entry
        jobs = cockpit.runs
        report["jobs"] = {slug: [((j.get("result") or {}).get("checker"), j["version_id"]) for j in jobs.jobs(slug)["jobs"]]
                          for slug in ("mac-gray", "providence-worcester", "petsmart", "medivation")}
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
