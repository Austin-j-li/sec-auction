"""Backups, restores and the restore rehearsal, on a fixture repository with a real workspace."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from openpyxl import load_workbook

from cockpit import backup, data
from test_cockpit_workspace import fixture

SLUG = "alpha-deal"
ADDED = "beta-holdings"
NOW = dt.datetime(2026, 9, 23, 3, 30, tzinfo=dt.timezone.utc)
SCRIPT = Path(backup.__file__)


def tree(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob("*")) if p.is_file()}


class BackupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        self.cockpit, original = fixture(self.root)
        self.ws, self.trace = self.cockpit.workspace, self.cockpit.trace
        self.state = self.root / "_dev/cockpit/state"
        self.dest = self.base / "backups"
        sha = hashlib.sha256(original).hexdigest()
        row = self.cockpit.deal(SLUG)["ledger"]["rows"][0]
        self.ws.edit(SLUG, {"revision": 0, "base_sha256": sha, "reason": "Fix price", "operations": [{"type": "update", "sheet": "Deal ledger", "uid": row["uid"], "values": {"Price low": "12.5"}}]}, "austin")
        threads = self.trace.comment(SLUG, {"action": "create", "target": {"kind": "deal"}, "body": "Check the price"}, "austin")["threads"]
        thread = threads[0]["id"]
        self.trace.comment(SLUG, {"action": "reply", "thread_id": thread, "body": "Agreed"}, "alex")
        self.comment = threads[0]["comments"][0]["id"]
        self.trace.comment(SLUG, {"action": "edit", "comment_id": self.comment, "body": "Check the low price"}, "austin")
        self.trace.comment(SLUG, {"action": "resolve", "thread_id": thread}, "alex")
        self.trace.comment(SLUG, {"action": "create", "target": {"kind": "row", "sheet": "Deal ledger", "uid": row["uid"]}, "body": "Row note"}, "alex")
        # A version made in the cockpit, then hidden.
        folder = self.state / "versions" / SLUG / "opus55-medium-x"
        folder.mkdir(parents=True)
        wb = load_workbook(self.root / "extraction/alpha-deal.xlsx")
        wb["Deal ledger"]["C2"] = "Changed who"
        wb.save(folder / f"{SLUG}.xlsx")
        (folder / "metadata.json").write_text("{}")
        conn = self.ws._connect(write=True)
        conn.execute("INSERT INTO versions (slug, id, label, path, sha256, kind, engine, model, effort, instruction_version, instruction_sha256, filing_sha256, started_by, started_at, finished_at, receipts, checker) VALUES (?,?,?,?,?,'raw','Opus 5.5','claude-opus-5-5','medium','v1.13.2','i','f','alex','2026-09-23T10:00:00+00:00','2026-09-23T10:10:00+00:00',?,'{}')",
                     (SLUG, "opus55-medium-x", "Opus 5.5 · medium", str((folder / f"{SLUG}.xlsx").relative_to(self.root)), hashlib.sha256((folder / f"{SLUG}.xlsx").read_bytes()).hexdigest(), str(folder.relative_to(self.root))))
        # A deal added in the cockpit (no run yet), and one hidden deal.
        filing = (self.root / "raw_filing/alpha-deal_2020-04-01_DEFM14A.htm").read_bytes()
        (self.state / "filings" / ADDED).mkdir(parents=True)
        (self.state / "filings" / ADDED / "beta.htm").write_bytes(filing)
        conn.execute("INSERT INTO added_deals VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (ADDED, "Beta Holdings", "DEFM14A", "2021-03-04", "beta.htm", "link", None, None, "https://example.invalid/b.txt", "beta.htm", "2026-09-23T10:00:00+00:00", len(filing), hashlib.sha256(filing).hexdigest(), "alex", "2026-09-23T10:00:00+00:00"))
        conn.execute("CREATE TABLE IF NOT EXISTS hidden_deals (slug TEXT PRIMARY KEY, hidden_by TEXT NOT NULL, hidden_at TEXT NOT NULL)")
        conn.execute("INSERT INTO hidden_deals VALUES (?, 'alex', '2026-09-23T11:00:00+00:00')", (ADDED,))
        conn.commit(); conn.close()
        self.cockpit.runs.version_action(SLUG, "austin", {"action": "hide", "version_id": "opus55-medium-x"})
        # A draft instruction with a saved edit.
        published = self.cockpit.instructions.list()["items"][0]
        draft = self.cockpit.instructions.request("alex", {"action": "draft", "from": published["id"]})
        self.cockpit.instructions.request("alex", {"action": "save", "id": draft["item"]["id"], "text": draft["text"] + "More.\n", "base_sha256": draft["item"]["sha256"]})
        # Left out of backups.
        (self.state / "jobs/job1").mkdir(parents=True)
        (self.state / "jobs/job1/status.json").write_text('{"state": "completed"}')
        (self.state / "lookups").mkdir()
        (self.state / "lookups/cache.txt").write_text("cache")
        (self.state / "worker.lock").write_text("")

    def tearDown(self):
        self.temp.cleanup()

    def fake_systemctl(self, status: str) -> dict[str, str]:
        folder = self.base / "bin"
        folder.mkdir(exist_ok=True)
        tool = folder / "systemctl"
        tool.write_text(f"#!/bin/sh\necho {status}\necho {status}\n")
        tool.chmod(0o755)
        return {"PATH": f"{folder}:{os.environ['PATH']}"}

    def test_create_restore_and_rehearse_are_equal(self):
        made = backup.create(self.root, self.dest, now=NOW)
        self.assertEqual(made.name, "20260923-033000Z")
        self.assertEqual(self.dest.stat().st_mode & 0o777, 0o700)
        manifest = json.loads((made / "manifest.json").read_text())
        paths = {entry["path"] for entry in manifest["files"]}
        self.assertIn("instructions", {p.split("/")[0] for p in paths})
        self.assertIn(f"versions/{SLUG}/opus55-medium-x/{SLUG}.xlsx", paths)
        self.assertIn(f"filings/{ADDED}/beta.htm", paths)
        self.assertIn("jobs/job1/status.json", paths)
        self.assertFalse({p for p in paths if p.startswith("lookups") or "worker.lock" in p or p.endswith(("-wal", "-shm"))})
        self.assertEqual(sorted(p.name for p in made.iterdir()), ["filings", "instructions", "jobs", "manifest.json", "versions", "workspace.sqlite3"])
        self.assertEqual((manifest["database"]["tables"]["comments"], manifest["database"]["tables"]["revisions"], manifest["database"]["tables"]["hidden_deals"]), (3, 1, 1))
        self.assertEqual(manifest["summary"][SLUG] | {"content_sha256": None, "comments_sha256": None},
                         {"revision": 1, "base": "v1132-raw", "content_sha256": None, "threads": 2, "comments": 3, "comments_sha256": None})
        self.assertEqual(manifest["summary"][ADDED]["revision"], 0)
        self.assertEqual(manifest["state"], str(self.state.resolve()))

        target = self.base / "restored/state"
        backup.restore(made, target)
        self.assertEqual(sorted(p.name for p in target.iterdir()), ["filings", "instructions", "jobs", "lookups", "versions", "workspace.sqlite3"])
        self.assertEqual(list((target / "lookups").iterdir()), [])
        for name in ("filings", "instructions", "versions", "jobs"):
            self.assertEqual(tree(target / name), tree(self.state / name))

        report = backup.rehearse(self.root, self.dest, keep_days=None)
        self.assertEqual(report["differences"], [])
        self.assertEqual((report["deals"], report["working_copies_equal"], report["comments_equal"]), (2, True, True))
        self.assertTrue(Path(report["backup"]).is_dir())
        self.assertEqual([p.name for p in self.dest.iterdir() if p.name.startswith(".")], [])  # the temporary root is gone
        # The restored root reads through the same code as the server: working copy, comments, hidden version, draft.
        staged = self.base / "staged"
        staged.mkdir()
        restored = backup.stage_root(self.root, made, staged)
        self.assertEqual(restored.deal(SLUG)["workspace"]["revision"], 1)
        self.assertEqual(restored.deal(SLUG)["ledger"]["rows"][0]["cells"]["Price low"], "12.5")
        self.assertEqual(restored.trace.comments(SLUG), self.trace.comments(SLUG))
        self.assertTrue(next(v for v in restored.deal(SLUG)["versions"] if v["id"] == "opus55-medium-x")["hidden"])
        self.assertEqual([i["status"] for i in restored.instructions.list()["items"]], ["published", "draft"])

    def test_cli_create_and_rehearse(self):
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        made = subprocess.run([sys.executable, str(SCRIPT), "create", "--repo-root", str(self.root), "--dest", str(self.dest)], capture_output=True, text=True, env=env)
        self.assertEqual(made.returncode, 0, made.stderr)
        self.assertTrue(Path(made.stdout.strip()).is_dir())
        checked = subprocess.run([sys.executable, str(SCRIPT), "rehearse", "--repo-root", str(self.root), "--dest", str(self.base / "other")], capture_output=True, text=True, env=env)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertEqual(json.loads(checked.stdout)["differences"], [])
        failed = subprocess.run([sys.executable, str(SCRIPT), "create", "--repo-root", str(self.base), "--dest", str(self.dest)], capture_output=True, text=True, env=env)
        self.assertEqual((failed.returncode, failed.stdout, len(failed.stderr.strip().splitlines())), (1, "", 1))
        self.assertIn("no workspace database", failed.stderr)

    def test_backup_while_a_writer_holds_the_database_is_consistent(self):
        stop = threading.Event()
        errors: list[BaseException] = []
        commits = []

        def churn():  # another writer committing while the backup runs
            try:
                while not stop.is_set():
                    other = sqlite3.connect(self.ws.db_path, timeout=30)
                    other.execute("INSERT INTO activity (slug, at, actor, kind, summary) VALUES ('alpha-deal', 'x', 'alex', 'comment', 'churn')")
                    other.commit(); other.close()
                    commits.append(1)
            except BaseException as exc:  # noqa: BLE001
                errors.append(exc)
        thread = threading.Thread(target=churn)
        thread.start()
        try:
            during = backup.create(self.root, self.dest, now=NOW)
        finally:
            stop.set(); thread.join()
        self.assertEqual(errors, [])
        self.assertTrue(commits)
        writer = sqlite3.connect(self.ws.db_path, timeout=30)
        writer.execute("BEGIN IMMEDIATE")
        writer.execute("INSERT INTO activity (slug, at, actor, kind, summary) VALUES ('alpha-deal', 'x', 'alex', 'comment', 'uncommitted')")
        try:
            held = backup.create(self.root, self.dest, now=NOW + dt.timedelta(seconds=1))
        finally:
            writer.rollback(); writer.close()
        for made in (during, held):
            backup.verify(made)
            conn = sqlite3.connect(made / "workspace.sqlite3")
            self.assertEqual(conn.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            self.assertEqual(conn.execute("PRAGMA journal_mode").fetchone()[0], "delete")
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM activity WHERE summary='uncommitted'").fetchone()[0], 0)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM comments").fetchone()[0], 3)
            counts = json.loads((made / "manifest.json").read_text())["database"]["tables"]
            self.assertEqual(counts["activity"], conn.execute("SELECT COUNT(*) FROM activity").fetchone()[0])
            conn.close()
            self.assertEqual(sorted(p.name for p in made.iterdir() if p.name.endswith(("-wal", "-shm", "-journal"))), [])

    def test_tampered_file_fails_restore_and_leaves_the_target_untouched(self):
        made = backup.create(self.root, self.dest, now=NOW)
        target = self.base / "target"
        (target / "versions").mkdir(parents=True)
        (target / "versions/keep.txt").write_text("old")
        before = tree(target)
        instruction = next((made / "instructions").iterdir())
        instruction.write_text(instruction.read_text() + "tampered")
        with self.assertRaisesRegex(backup.BackupError, "does not match the manifest"):
            backup.restore(made, target, replace=True)
        self.assertEqual(tree(target), before)
        self.assertEqual(sorted(p.name for p in self.base.iterdir()), ["backups", "repo", "target"])
        # A manifest that names a path outside the store is refused too.
        other = backup.create(self.root, self.dest, now=NOW + dt.timedelta(seconds=1))
        manifest = json.loads((other / "manifest.json").read_text())
        manifest["files"][0]["path"] = "../escape"
        (other / "manifest.json").write_text(json.dumps(manifest))
        with self.assertRaisesRegex(backup.BackupError, "unsafe path"):
            backup.restore(other, self.base / "new")
        self.assertFalse((self.base / "new").exists())

    def test_pruning(self):
        self.dest.mkdir()
        for days in (20, 15, 13, 1):
            old = self.dest / (NOW - dt.timedelta(days=days)).strftime(backup.STAMP)
            old.mkdir()
            (old / "manifest.json").write_text("{}")
        foreign = [self.dest / "notes", self.dest / "20200101-000000Z-copy", self.dest / "20200101-000001Z"]  # the last has no manifest
        for path in foreign: path.mkdir()
        (self.dest / "README.txt").write_text("mine")
        (self.dest / ".partial-20260101-000000Z").mkdir()
        made = backup.create(self.root, self.dest, now=NOW)
        names = sorted(p.name for p in self.dest.iterdir())
        kept = sorted((NOW - dt.timedelta(days=d)).strftime(backup.STAMP) for d in (13, 1))
        self.assertEqual(names, sorted([*kept, made.name, "notes", "20200101-000000Z-copy", "20200101-000001Z", "README.txt"]))
        # Long after the last backup, the newest is still kept.
        backup.prune(self.dest, 14, NOW + dt.timedelta(days=100))
        self.assertEqual([p.name for p in backup.backups(self.dest)], [made.name])
        self.assertTrue(all(path.exists() for path in foreign))

    def test_replace_moves_the_old_directory_aside(self):
        made = backup.create(self.root, self.dest, now=NOW)
        target = self.base / "target"
        target.mkdir()
        (target / "old.txt").write_text("old")
        with self.assertRaisesRegex(backup.BackupError, "not empty"):
            backup.restore(made, target)
        backup.restore(made, target, replace=True, now=NOW)
        aside = self.base / "target.before-restore-20260923-033000Z"
        self.assertEqual((aside / "old.txt").read_text(), "old")
        self.assertTrue((target / "workspace.sqlite3").is_file())
        self.assertFalse((target / "old.txt").exists())
        empty = self.base / "empty"
        empty.mkdir()
        backup.restore(made, empty)  # an existing empty directory needs no --replace
        self.assertTrue((empty / "workspace.sqlite3").is_file())
        self.assertEqual(backup.create(self.root, self.dest, now=NOW).name, "20260923-033001Z")  # same second: the next free stamp

    def test_restore_is_refused_on_the_live_state_while_services_run(self):
        made = backup.create(self.root, self.dest, now=NOW)
        before = tree(self.state)
        with patch.dict(os.environ, self.fake_systemctl("active")):
            with self.assertRaisesRegex(backup.BackupError, "live state"):
                backup.restore(made, self.state, replace=True, repo_root=self.root)
        self.assertEqual(tree(self.state), before)
        with patch.dict(os.environ, self.fake_systemctl("inactive")):
            backup.restore(made, self.state, replace=True, repo_root=self.root, now=NOW)
        self.assertTrue((self.root / "_dev/cockpit/state.before-restore-20260923-033000Z/lookups/cache.txt").is_file())
        self.assertEqual(data.Cockpit(self.root).deal(SLUG)["workspace"]["revision"], 1)

    def test_changed_comment_after_the_backup_is_a_difference(self):
        made = backup.create(self.root, self.dest, now=NOW)
        staged = self.base / "staged"
        staged.mkdir()
        restored = backup.stage_root(self.root, made, staged)
        self.assertEqual(backup.compare(self.cockpit, restored), [])
        self.trace.comment(SLUG, {"action": "edit", "comment_id": self.comment, "body": "Check the high price"}, "austin")
        differences = backup.compare(self.cockpit, restored)
        self.assertEqual({(d["deal"], d["part"]) for d in differences}, {(SLUG, "comments")})
        self.assertEqual(backup.compare_tables(made / "workspace.sqlite3", self.ws.db_path)[0]["part"], "tables")


if __name__ == "__main__":
    unittest.main()
