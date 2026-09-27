"""Synthetic tests for building a pending catalog from filing evidence only."""
from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from cockpit import import_results as imp


class CatalogBuilderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        folder = self.root / "raw_filing"
        folder.mkdir()
        fields = ("file", "deal", "form_type", "date_filed", "source_url", "document", "fetched_utc", "bytes", "sha256")
        with (folder / "MANIFEST.csv").open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            for slug in imp.DEALS:
                path = folder / f"{slug}.htm"
                path.write_text(f"<html><body>Synthetic {slug}</body></html>")
                writer.writerow(dict(file=path.name, deal=slug, form_type="DEFM14A", date_filed="2020-01-01",
                                     source_url=f"https://example.invalid/{slug}.txt", document=path.name,
                                     fetched_utc="2026-09-27T00:00:00Z", bytes=path.stat().st_size, sha256=imp.sha256(path)))

    def tearDown(self):
        self.temp.cleanup()

    def test_builds_nine_pending_deals_without_workbook_dependencies(self):
        catalog = imp.build_catalog(self.root)
        self.assertEqual(set(catalog["deals"]), set(imp.DEALS))
        for slug, item in catalog["deals"].items():
            self.assertEqual((item["versions"], item["findings"], item["documents"]), ([], [], []))
            self.assertNotIn("default_base", item)
            self.assertEqual(item["filing"]["deal"], slug)
            self.assertEqual(item["filing"]["sha256"], imp.sha256(self.root / "raw_filing" / item["filing"]["file"]))
        self.assertNotIn("extraction/", json.dumps(catalog))

    def test_rejects_changed_or_missing_filing(self):
        (self.root / "raw_filing/stec.htm").write_text("changed")
        with self.assertRaisesRegex(imp.CatalogError, "differs"):
            imp.build_catalog(self.root)
        (self.root / "raw_filing/stec.htm").unlink()
        with self.assertRaisesRegex(imp.CatalogError, "missing"):
            imp.build_catalog(self.root)

    def test_rejects_incomplete_deal_set(self):
        path = self.root / "raw_filing/MANIFEST.csv"
        lines = path.read_text().splitlines()
        path.write_text("\n".join(lines[:-1]) + "\n")
        with self.assertRaisesRegex(imp.CatalogError, "exactly"):
            imp.build_catalog(self.root)

    def test_main_creates_once_and_never_overwrites(self):
        output = self.root / "_dev/cockpit/catalog.json"
        self.assertEqual(imp.main(["--root", str(self.root)]), 0)
        original = output.read_bytes()
        with self.assertRaises(FileExistsError):
            imp.main(["--root", str(self.root)])
        self.assertEqual(output.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
