"""Synthetic, offline checks for the one-way fresh-state builder."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import sqlite3
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from cockpit import data, fresh_state


NAMES = ("medivation", "zep", "pepco-holdings", "imprivata")
SECRET = b"synthetic-token\x00with-binary-bytes"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FreshStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / "old-state"
        self.source.mkdir()
        self.db = self.source / fresh_state.DATABASE
        self.conn = sqlite3.connect(self.db)
        self.addCleanup(self.conn.close)
        self.conn.execute("PRAGMA journal_mode=WAL")
        # An extra BLOB column proves opaque account values survive byte for byte.
        self.conn.execute("CREATE TABLE accounts (user TEXT NOT NULL, provider TEXT NOT NULL, connected_at TEXT NOT NULL, expires_at TEXT, synthetic_token BLOB, PRIMARY KEY(user, provider))")
        self.conn.execute("CREATE TABLE added_deals (slug TEXT PRIMARY KEY, name TEXT NOT NULL, form_type TEXT NOT NULL, date_filed TEXT NOT NULL, file TEXT NOT NULL, source_kind TEXT NOT NULL, seed_deal TEXT, index_url TEXT, source_url TEXT NOT NULL, document TEXT NOT NULL, fetched_utc TEXT NOT NULL, bytes INTEGER NOT NULL, sha256 TEXT NOT NULL, added_by TEXT NOT NULL, added_at TEXT NOT NULL)")
        for name in ("instructions", "settings", "versions", "revisions", "jobs", "comments", "activity"):
            self.conn.execute(f"CREATE TABLE {name} (value TEXT)")
            self.conn.execute(f"INSERT INTO {name} VALUES ('old state only')")
        self.conn.execute("INSERT INTO accounts VALUES ('austin','claude','2026-09-01',NULL,?)", (SECRET,))
        self.conn.commit()
        for index, slug in enumerate(NAMES):
            filing = self.source / "filings" / slug / f"{slug}.htm"
            filing.parent.mkdir(parents=True)
            content = f"<html>synthetic filing {index}</html>".encode()
            filing.write_bytes(content)
            self.conn.execute("INSERT INTO added_deals VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                              (slug, slug.title(), "DEFM14A", "2026-09-01", filing.name, "link", None, None,
                               "https://example.invalid/filing", filing.name, "2026-09-01T00:00:00Z",
                               len(content), hashlib.sha256(content).hexdigest(), "alex", "2026-09-01T00:00:00Z"))
        # This row is committed in WAL while the writer remains open.
        self.conn.execute("INSERT INTO accounts VALUES ('alex','chatgpt','2026-09-02',NULL,?)", (SECRET[::-1],))
        self.conn.commit()
        self.assertTrue((self.source / "workspace.sqlite3-wal").is_file())
        (self.source / "instructions").mkdir()
        (self.source / "instructions/old.txt").write_text("Do not copy")

    def test_copies_only_required_tables_and_verified_files_from_wal_snapshot(self) -> None:
        source_data = {str(path.relative_to(self.source)): digest(path) for path in self.source.rglob("*")
                       if path.is_file() and not path.name.endswith("-shm")}
        target = self.base / "new-state"
        summary = fresh_state.create(self.source, target)
        self.assertEqual(summary, {"accounts": 2, "added_deals": 4, "filings": 4})
        self.assertEqual(target.stat().st_mode & 0o777, 0o700)
        self.assertEqual({str(path.relative_to(target)) for path in target.rglob("*") if path.is_file()},
                         {"workspace.sqlite3", *(f"filings/{slug}/{slug}.htm" for slug in NAMES)})
        with sqlite3.connect(target / fresh_state.DATABASE) as copied:
            tables = {row[0] for row in copied.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")}
            self.assertEqual(tables, {"accounts", "added_deals"})
            self.assertEqual(copied.execute("SELECT synthetic_token FROM accounts WHERE user='austin'").fetchone()[0], SECRET)
            self.assertEqual(copied.execute("SELECT synthetic_token FROM accounts WHERE user='alex'").fetchone()[0], SECRET[::-1])
            self.assertEqual(copied.execute("SELECT count(*) FROM added_deals").fetchone()[0], 4)
            self.assertEqual(copied.execute("PRAGMA quick_check").fetchone()[0], "ok")
        for slug in NAMES:
            self.assertEqual(digest(target / "filings" / slug / f"{slug}.htm"),
                             digest(self.source / "filings" / slug / f"{slug}.htm"))
        self.assertEqual(source_data, {str(path.relative_to(self.source)): digest(path) for path in self.source.rglob("*")
                                       if path.is_file() and not path.name.endswith("-shm")})
        self.assertEqual(self.conn.execute("SELECT count(*) FROM instructions").fetchone()[0], 1)

    def test_app_reads_nine_catalog_and_four_added_deals_then_seeds_root_instruction(self) -> None:
        root = self.base / "repo"
        cockpit_dir = root / "_dev/cockpit"
        cockpit_dir.mkdir(parents=True)
        raw = root / "raw_filing"
        raw.mkdir()
        fields = ("deal", "file", "form_type", "date_filed", "source_url", "document", "fetched_utc", "bytes", "sha256")
        catalog = {}
        with (raw / "MANIFEST.csv").open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for index in range(9):
                slug = f"catalog-{index}"
                name = f"{slug}.htm"
                content = b"<html>synthetic catalog filing</html>"
                (raw / name).write_bytes(content)
                entry = {"deal": slug, "file": name, "form_type": "DEFM14A", "date_filed": "2026-09-01",
                         "source_url": "https://example.invalid/catalog", "document": name, "fetched_utc": "2026-09-01T00:00:00Z",
                         "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
                writer.writerow(entry)
                catalog[slug] = {"name": slug, "versions": [], "default_base": None, "filing": entry,
                                 "findings": [], "documents": []}
        (cockpit_dir / "catalog.json").write_text(json.dumps({"schema_version": 1, "deals": catalog}))
        instruction = "# Version 0\n\nSynthetic repository instruction.\n"
        (root / "SEC_Deal_Ledger_Extraction_Instruction.md").write_text(instruction)
        state = cockpit_dir / "state"
        fresh_state.create(self.source, state)
        with sqlite3.connect(state / fresh_state.DATABASE) as conn:
            self.assertEqual({row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")},
                             {"accounts", "added_deals"})
        cockpit = data.Cockpit(root)
        listed = cockpit.list_deals()
        self.assertEqual(len(listed), 13)
        self.assertEqual({row["slug"] for row in listed}, set(catalog) | set(NAMES))
        self.assertTrue(all(row["pending"] for row in listed))
        versions = cockpit.instructions.list()
        self.assertEqual(len(versions["items"]), 1)
        self.assertEqual(versions["items"][0]["id"], versions["default_id"])
        self.assertEqual(cockpit.instructions.text(versions["items"][0]["sha256"]), instruction)

    def test_refuses_existing_and_overlapping_destinations_without_writing(self) -> None:
        existing = self.base / "existing"
        existing.mkdir()
        marker = existing / "marker"
        marker.write_text("keep")
        for target in (existing, self.source, self.source / "nested", self.base):
            with self.subTest(target=target), self.assertRaises(fresh_state.FreshStateError):
                fresh_state.create(self.source, target)
        self.assertEqual(marker.read_text(), "keep")
        self.assertEqual(list(self.base.glob(".fresh-state-*")), [])

    def test_rejects_unsafe_paths_and_symlinks_without_partial_destination(self) -> None:
        row = self.conn.execute("SELECT slug, file FROM added_deals LIMIT 1").fetchone()
        slug, filename = row
        for unsafe in ("../escape.htm", "/absolute.htm", "..\\escape.htm", ".hidden"):
            self.conn.execute("UPDATE added_deals SET file=? WHERE slug=?", (unsafe, slug))
            self.conn.commit()
            with self.subTest(file=unsafe), self.assertRaises(fresh_state.FreshStateError):
                fresh_state.create(self.source, self.base / "new-state")
            self.assertFalse((self.base / "new-state").exists())
        self.conn.execute("UPDATE added_deals SET file=? WHERE slug=?", (filename, slug))
        self.conn.commit()
        filing = self.source / "filings" / slug / filename
        filing.unlink()
        filing.symlink_to(self.source / "instructions/old.txt")
        with self.assertRaises(fresh_state.FreshStateError):
            fresh_state.create(self.source, self.base / "new-state")
        self.assertFalse((self.base / "new-state").exists())
        self.assertEqual(list(self.base.glob(".fresh-state-*")), [])

    def test_rejects_incomplete_or_changed_filing_and_cleans_stage(self) -> None:
        bad = self.source / "filings" / NAMES[-1] / f"{NAMES[-1]}.htm"
        bad.write_bytes(b"incomplete")
        with self.assertRaises(fresh_state.FreshStateError):
            fresh_state.create(self.source, self.base / "new-state")
        self.assertFalse((self.base / "new-state").exists())
        self.assertEqual(list(self.base.glob(".fresh-state-*")), [])

    def test_rejects_missing_filing_and_database_symlink(self) -> None:
        missing = self.source / "filings" / NAMES[0] / f"{NAMES[0]}.htm"
        missing.unlink()
        with self.assertRaises(fresh_state.FreshStateError):
            fresh_state.create(self.source, self.base / "new-state")
        self.assertFalse((self.base / "new-state").exists())
        self.db.unlink()
        self.db.symlink_to(self.source / "instructions/old.txt")
        with self.assertRaises(fresh_state.FreshStateError):
            fresh_state.create(self.source, self.base / "new-state")
        self.assertFalse((self.base / "new-state").exists())

    def test_rejects_destination_symlink(self) -> None:
        destination = self.base / "new-state"
        destination.symlink_to(self.source)
        with self.assertRaises(fresh_state.FreshStateError):
            fresh_state.create(self.source, destination)
        self.assertTrue(destination.is_symlink())

    def test_destination_created_during_copy_is_not_replaced(self) -> None:
        destination = self.base / "new-state"
        copy_filings = fresh_state._copy_filings

        def racing_copy(source: Path, stage: Path, added: list[tuple[str, str, int, str]]) -> None:
            copy_filings(source, stage, added)
            destination.mkdir()

        with patch.object(fresh_state, "_copy_filings", side_effect=racing_copy):
            with self.assertRaises(fresh_state.FreshStateError):
                fresh_state.create(self.source, destination)
        self.assertTrue(destination.is_dir())
        self.assertEqual(list(destination.iterdir()), [])
        self.assertEqual(list(self.base.glob(".fresh-state-*")), [])

    def test_cli_reports_counts_without_account_contents(self) -> None:
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            code = fresh_state.main([str(self.source), str(self.base / "new-state")])
        self.assertEqual(code, 0)
        self.assertIn("2 accounts, 4 added deals, 4 filings", output.getvalue())
        self.assertNotIn(SECRET.decode("latin-1"), output.getvalue() + errors.getvalue())


if __name__ == "__main__":
    unittest.main()
