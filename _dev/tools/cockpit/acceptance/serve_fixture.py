"""Serve the synthetic fixture for the isolated Playwright acceptance run."""

from __future__ import annotations

import json
import csv
import hashlib
import os
import shutil
import signal
import sys
import tempfile
from pathlib import Path

from test_http import HttpFixture, synthetic_repo


def real_readonly_copy(root: Path) -> None:
    """Copy one real raw deal into a disposable catalog for visual load checks."""
    repository = Path(__file__).resolve().parents[4]
    with (repository / "raw_filing/MANIFEST.csv").open(newline="", encoding="utf-8") as handle:
        source = next(row for row in csv.DictReader(handle) if row["deal"] == "datalink")
    for name in ("extraction", "raw_filing", "_dev/cockpit"):
        (root / name).mkdir(parents=True, exist_ok=True)
    workbook = root / "extraction/datalink.xlsx"
    shutil.copyfile(repository / "extraction/datalink.xlsx", workbook)
    shutil.copyfile(repository / "raw_filing" / source["file"], root / "raw_filing" / source["file"])
    with (root / "raw_filing/MANIFEST.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=source.keys())
        writer.writeheader()
        writer.writerow(source)
    digest = hashlib.sha256(workbook.read_bytes()).hexdigest()
    catalog = {"schema_version": 1, "deals": {"datalink": {"name": "Datalink", "default_base": "v1132-raw", "versions": [{"id": "v1132-raw", "label": "Datalink raw v1.13.2", "path": "extraction/datalink.xlsx", "sha256": digest, "instruction_version": "v1.13.2", "kind": "raw", "review_status": "unreviewed"}], "findings": [], "documents": []}}}
    (root / "_dev/cockpit/catalog.json").write_text(json.dumps(catalog), encoding="utf-8")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="cockpit-browser-") as folder:
        root = Path(folder)
        real = "--real-readonly" in sys.argv[1:]
        actual_catalog = "--actual-catalog-readonly" in sys.argv[1:]
        if actual_catalog:
            root = Path(__file__).resolve().parents[4]
            os.environ["COCKPIT_REQUIRE_ACCESS"] = "1"
        elif real:
            real_readonly_copy(root)
            os.environ["COCKPIT_REQUIRE_ACCESS"] = "1"
        else:
            synthetic_repo(root)
        fixture = HttpFixture(root)
        signal.signal(signal.SIGTERM, lambda *_: fixture.httpd.shutdown())
        print(json.dumps({"url": fixture.base}), flush=True)
        try:
            fixture.thread.join()
        finally:
            fixture.close()


if __name__ == "__main__":
    main()
