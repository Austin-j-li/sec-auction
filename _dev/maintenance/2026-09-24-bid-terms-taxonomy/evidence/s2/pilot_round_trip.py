"""S2.6 evidence: the two v1.14 pilots, copied into a temporary workspace, through import, rebase, edit, save,
reload and export. Reads only copies; writes only under the temporary root and the named output file."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import json
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

SANDBOX = Path("/home/uctpiaj/work/tmp/v114-scratch/pkg/s2")
COPIES = Path("/home/uctpiaj/work/tmp/v114-scratch/tmp/s2/pilot-copies")
sys.path.insert(0, str(SANDBOX / "_dev/tools"))

import openpyxl  # noqa: E402
import check_lean  # noqa: E402
from cockpit import data  # noqa: E402

PILOTS = {"mac-gray": ("opus55-medium-20260924-2241-d7d267", "mac-gray_2013-12-04_DEFM14A.htm"),
          "providence-worcester": ("opus55-medium-20260924-2241-38bc24", "providence-worcester_2016-09-20_DEFM14A.htm")}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cells(source) -> dict:
    wb = openpyxl.load_workbook(source)
    out = {}
    for sheet in ("Deal ledger", "Rounds", "Questions", "Deal facts"):
        rows = [[cell.value for cell in row] for row in wb[sheet].iter_rows()]
        out[sheet] = [row for index, row in enumerate(rows) if index == 0 or any(value is not None and value != "" for value in row)]
    wb.close()
    return out


def same(a, b) -> bool:
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        return float(a) == float(b)
    return a == b


def run(slug: str, ident: str, filing: str, folder: Path) -> dict:
    root = folder / slug
    (root / "extraction").mkdir(parents=True)
    (root / "raw_filing").mkdir()
    (root / "_dev/cockpit").mkdir(parents=True)
    base = root / "extraction" / f"{slug}.xlsx"
    shutil.copy2(SANDBOX / "extraction" / f"{slug}.xlsx", base)
    shutil.copy2(COPIES / filing, root / "raw_filing" / filing)
    with (COPIES / "manifest-rows.csv").open(newline="", encoding="utf-8") as handle:
        header = ["file", "deal", "form_type", "date_filed", "source_url", "document", "fetched_utc", "bytes", "sha256"]
        rows = [dict(zip(header, row)) for row in csv.reader(handle) if row[1] == slug]
    with (root / "raw_filing/MANIFEST.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
    catalog = {"schema_version": 1, "deals": {slug: {"name": slug, "default_base": "opus55-medium", "findings": [], "documents": [],
               "versions": [{"id": "opus55-medium", "label": "Opus 5.5 medium extraction", "path": f"extraction/{slug}.xlsx", "sha256": sha(base),
                             "instruction_version": "v1.13.2", "kind": "raw", "review_status": "unreviewed"}]}}}
    (root / "_dev/cockpit/catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
    cockpit = data.Cockpit(root)
    ws = cockpit.workspace
    # "Import": the pilot becomes a run version with its stored receipt, as the worker leaves it.
    receipts = root / "_dev/cockpit/state/versions" / slug / ident
    receipts.mkdir(parents=True)
    pilot = receipts / f"{slug}.xlsx"
    shutil.copy2(COPIES / f"{slug}.xlsx", pilot)
    shutil.copy2(COPIES / f"{slug}-check.json", receipts / "check.json")
    receipt_hash = sha(receipts / "check.json")
    conn = ws._connect(write=True)
    conn.execute("INSERT INTO versions (slug, id, label, path, sha256, kind, engine, model, effort, instruction_version, instruction_sha256, filing_sha256, started_by, started_at, finished_at, receipts, checker) VALUES (?,?,?,?,?,'raw','Opus 5.5','claude-opus-5-5','medium',NULL,?,?,'austin',?,?,?,?)",
                 (slug, ident, f"Opus 5.5 · medium · draft f9595d7 (Austin) — Austin, 24 Sep 22:41", str(pilot.relative_to(root)), sha(pilot), "f9595d74" + "0" * 56, rows[0]["sha256"],
                  "2026-09-24T22:41:00+00:00", "2026-09-24T22:52:00+00:00", str(receipts.relative_to(root)), json.dumps(json.loads((receipts / "check.json").read_text())["summary"])))
    conn.commit(); conn.close()
    pilot_hash = sha(pilot)

    working = ws.deal(slug)
    shown = ws.deal(slug, ident)
    compared = ws.compare(slug, "working", ident)["changes"]
    compared_fields = sorted({c["field"] for c in compared if c["type"] == "update"})
    preview = ws.rebase_preview(slug, ident)
    rebased = ws.edit(slug, {"revision": 0, "base_sha256": working["workspace"]["base_sha256"], "reason": "Round trip: rebase onto the pilot", "operations": [{"type": "rebase", "target_version": ident}]}, "local")
    first = rebased["ledger"]["rows"][0]
    edited = ws.edit(slug, {"revision": 1, "base_sha256": rebased["workspace"]["base_sha256"], "reason": "Round trip: one edit",
                            "operations": [{"type": "update", "sheet": "Deal ledger", "uid": first["uid"], "values": {"Note": (first["cells"].get("Note") or "") + " [round-trip probe]"}}]}, "local")
    reloaded = data.Cockpit(root)
    exported = reloaded.workspace.export(slug)
    got, want = cells(io.BytesIO(exported)), cells(pilot)
    column = want["Deal ledger"][0].index("Note")
    want["Deal ledger"][1][column] = (want["Deal ledger"][1][column] or "") + " [round-trip probe]"
    differences = []
    for sheet in want:
        if len(got[sheet]) != len(want[sheet]):
            differences.append({"sheet": sheet, "rows": [len(want[sheet]), len(got[sheet])]})
        for r, (a, b) in enumerate(zip(want[sheet], got[sheet]), 1):
            for c, (x, y) in enumerate(zip(a, b), 1):
                if not same(x, y):
                    differences.append({"sheet": sheet, "row": r, "column": c, "want": repr(x), "got": repr(y)})
            if len(a) != len(b) and any(v is not None for v in (a[len(b):] + b[len(a):])):
                differences.append({"sheet": sheet, "row": r, "width": [len(a), len(b)]})
    with tempfile.NamedTemporaryFile(suffix=".xlsx", dir=folder) as out:
        out.write(exported); out.flush()
        exported_check = check_lean.LeanChecker(Path(out.name), root / "raw_filing" / filing).run()
    raw_check = check_lean.LeanChecker(pilot, root / "raw_filing" / filing).run()
    kinds = {}
    for row in want["Deal ledger"][1:]:
        for header, value in zip(want["Deal ledger"][0], row):
            key = type(value).__name__
            kinds[key] = kinds.get(key, 0) + 1
    return {
        "deal": slug, "pilot_version": ident,
        "working_copy_schema": working["ledger_schema"], "pilot_schema": shown["ledger_schema"],
        "pilot_deadline_choices": shown["choices"].get("Deadline outcome"), "working_has_all_cash_choice": "All cash" in working["choices"],
        "pilot_at_import": next(v for v in shown["versions"] if v["id"] == ident)["checker"],
        "live_check": {"checker_version": shown["check"]["checker_version"], "summary": shown["check"]["summary"]},
        "compare_working_to_pilot_fields": compared_fields,
        "rebase_preview": preview["stops_applying"],
        "export_differences": differences,
        "ledger_value_types": kinds,
        "raw_check_summary": raw_check["summary"], "exported_check_summary": exported_check["summary"],
        "exported_schema": exported_check["ledger_schema"],
        "pilot_bytes_unchanged": sha(pilot) == pilot_hash == sha(COPIES / f"{slug}.xlsx"),
        "version_download_hash_equals": hashlib.sha256(reloaded.workspace.export(slug, ident)).hexdigest() == pilot_hash,
        "receipt_unchanged": sha(receipts / "check.json") == receipt_hash,
        "revisions": [h["revision"] for h in reloaded.workspace.history(slug)["history"]],
    }


def main() -> int:
    output = Path(sys.argv[1])
    with tempfile.TemporaryDirectory(prefix="s2-pilot-round-trip-") as folder:
        results = [run(slug, ident, filing, Path(folder)) for slug, (ident, filing) in PILOTS.items()]
    document = {"run_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "checker_version": check_lean.CHECKER_VERSION,
                "note": "Copies of the two v1.14 pilot workbooks, receipts and filings in a temporary workspace; the live state was only read (copied).",
                "results": results}
    output.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    ok = all(not r["export_differences"] and r["pilot_bytes_unchanged"] and r["version_download_hash_equals"] and r["receipt_unchanged"] for r in results)
    print(json.dumps({"ok": ok, "output": str(output)}))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
