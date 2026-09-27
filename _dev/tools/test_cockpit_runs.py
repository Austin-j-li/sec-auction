"""Accounts, extraction jobs, the worker and imported versions, with a fake runner and a fake Claude CLI."""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import stat
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from openpyxl import load_workbook

import check_lean
from cockpit import runs, worker
from cockpit.workspace import Conflict, WorkspaceError
from test_cockpit_workspace import fixture

SLUG = "alpha-deal"
TOKEN = "sk-ant-oat01-" + "A" * 40

FAKE_RUNNER = r'''
import hashlib, json, os, shutil, signal, sys, time
from pathlib import Path
command, args = sys.argv[1], sys.argv[2:]
value = lambda flag: args[args.index(flag) + 1]
run = Path(value("--run-dir"))
if command == "prepare":
    # The worker names the deal's filing folder; the filing must be there.
    assert (Path(value("--filing-dir")) / value("--filing")).is_file(), "filing not in --filing-dir"
    run.mkdir(parents=True)
    (run / "extraction").mkdir()
    instruction = hashlib.sha256(open(value("--instruction"), "rb").read()).hexdigest()
    json.dump({"effort": value("--effort"), "model": value("--model"), "provider": value("--provider"), "instruction_sha256": instruction,
               "filing_sha256": "f" * 64, "deal": value("--deal")}, open(run / "metadata.json", "w"))
    sys.exit(0)
metadata = json.load(open(run / "metadata.json"))
deal = metadata["deal"]
outcome = os.environ.get("FAKE_OUTCOME", "completed")
assert value("--provider") == metadata["provider"]
if metadata["provider"] == "opus":
    assert os.environ["SEC_CLAUDE_OAUTH_TOKEN_FILE"].endswith("claude-oauth-token") and "SEC_CODEX_AUTH_FILE" not in os.environ
else:
    assert os.environ["SEC_CODEX_AUTH_FILE"].endswith("codex/auth.json") and "SEC_CLAUDE_OAUTH_TOKEN_FILE" not in os.environ
status = {"started_at": "2026-09-23T10:00:00+00:00", "ended_at": "2026-09-23T10:12:00+00:00", "continuations": 0,
          "usage": {"tokens": {"output_tokens": 5}, "cost_usd": 3.0},
          "plan_usage": {"status": "allowed", "unifiedWindows": {"five_hour": {"utilization": 0.4, "resetsAt": 1}, "seven_day": {"utilization": 0.5, "resetsAt": 2}}}}
if outcome == "wait":
    signal.signal(signal.SIGTERM, lambda *_: (json.dump({**status, "state": "cancelled", "failure_reason": "cancelled"}, open(run / "status.json", "w")), sys.exit(1)))
    json.dump({"state": "running"}, open(run / "status.json", "w"))
    time.sleep(60)
if outcome == "usage_limit":
    json.dump({**status, "state": "failed", "failure_reason": "usage_limit", "usage_limit_resets_at": "2026-09-23T15:00:00+00:00"}, open(run / "status.json", "w"))
    sys.exit(1)
shutil.copy2(os.environ["FAKE_WORKBOOK"], run / "extraction" / f"{deal}.xlsx")
json.dump({**status, "state": "completed", "failure_reason": None}, open(run / "status.json", "w"))
'''

FAKE_CLAUDE = r'''
import sys
print("Welcome. Browser didn't open? Use the url below to sign in")
print("https://claude.com/cai/oauth/authorize?code=true&client_id=x&state=y")
print("Paste code here if prompted >", end="", flush=True)
# Like the real Claude input: a multi-character write is a paste, so only an Enter
# arriving on its own submits.
import os, tty
tty.setraw(0)
code = ""
while True:
    chunk = os.read(0, 4096).decode()
    if chunk in ("\r", "\n"):
        break
    code += chunk.replace("\r", "").replace("\n", "")
if code != "good-code":
    print("OAuth error: Request failed with status code 400\nPress Enter to retry.", flush=True); sys.stdin.readline(); sys.exit(1)
print("\nYour OAuth token (valid for 1 year):\n\n''' + TOKEN + r'''\n", flush=True)
'''


class RunsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.cockpit, self.original = fixture(self.root)
        self.ws, self.runs = self.cockpit.workspace, self.cockpit.runs
        self.base = hashlib.sha256(self.original).hexdigest()
        self.env = patch.dict(os.environ, {"COCKPIT_TOKEN_ROOT": str(self.root / "tokens"), "FAKE_WORKBOOK": str(self.root / "extraction/alpha-deal.xlsx")})
        self.env.start()
        (self.root / "fake_runner.py").write_text(FAKE_RUNNER)
        (self.root / "fake_claude.py").write_text(FAKE_CLAUDE)
        claude = self.root / "claude"
        claude.write_text(f"#!/bin/sh\nexec {sys.executable} {self.root / 'fake_claude.py'}\n")
        claude.chmod(0o755)
        self.patches = [patch.object(worker, "RUNNER", self.root / "fake_runner.py"), patch.object(worker, "CLAUDE", str(claude))]
        for item in self.patches: item.start()
        self.worker = worker.Worker(self.root)

    def tearDown(self):
        for child in self.worker.children.values():
            if child.poll() is None: child.kill()
        for item in self.patches: item.stop()
        self.env.stop()
        self.temp.cleanup()

    def settle(self, predicate, seconds=20):
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            self.worker.tick()
            if predicate(): return
            time.sleep(0.1)
        self.fail("condition not reached")

    def jobs(self):
        return self.runs.jobs(SLUG)["jobs"]

    def connect(self, user="austin"):
        self.runs.account_action(user, {"action": "token", "token": TOKEN})

    def add_version(self, ident="opus55-medium-x", change=None):
        folder = self.root / "_dev/cockpit/state/versions" / SLUG / ident
        folder.mkdir(parents=True)
        path = folder / f"{SLUG}.xlsx"
        wb = load_workbook(self.root / "extraction/alpha-deal.xlsx")
        if change: wb["Deal ledger"][change[0]] = change[1]
        wb.save(path)
        conn = self.ws._connect(write=True)
        conn.execute("INSERT INTO versions (slug, id, label, path, sha256, kind, engine, model, effort, instruction_version, instruction_sha256, filing_sha256, started_by, started_at, finished_at, receipts, checker) VALUES (?,?,?,?,?,'raw','Opus 5.5','claude-opus-5-5','medium','Version 0','i','f','alex','2026-09-23T10:00:00+00:00','2026-09-23T10:10:00+00:00',?,'{}')",
                     (SLUG, ident, f"Opus 5.5 · medium · Version 0 — Alex", str(path.relative_to(self.root)), hashlib.sha256(path.read_bytes()).hexdigest(), str(folder.relative_to(self.root))))
        conn.commit(); conn.close()
        return ident

    # ---- accounts ------------------------------------------------------------------

    def test_token_paste_and_disconnect(self):
        self.assertFalse(self.runs.account("austin")["claude"]["connected"])
        with self.assertRaises(WorkspaceError): self.runs.account_action("austin", {"action": "token", "token": "nope"})
        account = self.runs.account_action("austin", {"action": "token", "token": TOKEN})
        path = runs.token_path("austin")
        self.assertTrue(account["claude"]["connected"])
        self.assertEqual((stat.S_IMODE(path.stat().st_mode), stat.S_IMODE(path.parent.stat().st_mode)), (0o600, 0o700))
        self.assertNotIn(TOKEN, json.dumps(account))
        self.assertFalse(self.runs.account("alex")["claude"]["connected"])
        self.assertFalse(self.runs.account_action("austin", {"action": "disconnect"})["claude"]["connected"])
        self.assertFalse(path.exists())

    def test_sign_in_through_the_worker(self):
        self.runs.account_action("alex", {"action": "connect"})
        self.settle(lambda: (self.runs.account("alex")["connect"] or {}).get("state") == "waiting_for_code")
        connect = self.runs.account("alex")["connect"]
        self.assertTrue(connect["link"].startswith("https://claude.com/cai/oauth/authorize"))
        self.runs.account_action("alex", {"action": "code", "job_id": connect["job_id"], "code": "good-code"})
        self.settle(lambda: self.runs.account("alex")["claude"]["connected"])
        self.assertEqual(runs.token_path("alex").read_text().strip(), TOKEN)
        self.assertEqual(self.runs.account("alex")["connect"]["state"], "completed")
        # A wrong code fails with a readable error and saves nothing new.
        self.runs.account_action("austin", {"action": "connect"})
        self.settle(lambda: (self.runs.account("austin")["connect"] or {}).get("state") == "waiting_for_code")
        self.runs.account_action("austin", {"action": "code", "job_id": self.runs.account("austin")["connect"]["job_id"], "code": "bad"})
        self.settle(lambda: self.runs.account("austin")["connect"]["state"] == "failed")
        self.assertIn("Claude refused the code (OAuth error: Request failed with status code 400)", self.runs.account("austin")["connect"]["error"])
        self.assertFalse(runs.token_path("austin").exists())

    # ---- jobs and worker -------------------------------------------------------------

    def test_extract_requires_an_account_and_valid_settings(self):
        with self.assertRaises(Conflict): self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "opus55"})
        self.connect()
        for bad in ({"effort": "ultra"}, {"timeout_minutes": 5}, {"timeout_minutes": "90"}):
            with self.assertRaises(WorkspaceError): self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "opus55", **bad})
        job = self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "opus55", "effort": "high"})["jobs"][0]
        self.assertEqual((job["state"], job["params"]["effort"], job["params"]["model"]), ("queued", "high", "claude-opus-5-5"))
        self.runs.job_action(SLUG, "alex", {"action": "cancel", "job_id": job["id"]})
        self.worker.tick()
        self.assertEqual((self.jobs()[0]["state"], self.jobs()[0]["failure_reason"], self.jobs()[0]["cancelled_by"]), ("cancelled", "cancelled", "alex"))

    def test_completed_run_is_checked_and_imported(self):
        self.connect()
        self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "opus55"})
        self.settle(lambda: self.jobs()[0]["state"] in worker.TERMINAL)
        job = self.jobs()[0]
        self.assertEqual(job["state"], "completed", job)
        self.assertIn("errors", job["result"]["checker"])
        # The checker version and the rules it applied are stored with the counts, in the job and the version.
        self.assertEqual((job["result"]["checker"]["checker_version"], job["result"]["checker"]["ledger_schema"]), ("Version 1", "Version 1"))
        stored = json.loads(self.ws._connect().execute("SELECT checker FROM versions WHERE id=?", (job["version_id"],)).fetchone()["checker"])
        self.assertEqual((stored["checker_version"], stored["ledger_schema"]), ("Version 1", "Version 1"))
        version = next(v for v in self.cockpit.deal(SLUG)["versions"] if v["id"] == job["version_id"])
        self.assertEqual(version["checker"]["checker_version"], check_lean.CHECKER_VERSION)
        self.assertTrue(version["label"].startswith("Opus 5.5 · medium · Version 0 — Austin, "))
        self.assertEqual((version["engine"], version["started_by"], version["is_base"], version["hidden"]), ("Opus 5.5", "austin", False, False))
        receipts = self.root / "_dev/cockpit/state/versions" / SLUG / job["version_id"]
        self.assertTrue((receipts / "check.json").is_file() and (receipts / "status.json").is_file())
        self.assertEqual(self.ws.export(SLUG, job["version_id"]), self.original)
        self.assertFalse(Path(self.worker.job(job["id"])["run_dir"]).exists())
        self.assertEqual(self.runs.account("austin")["claude"]["plan_usage"]["seven_day"]["utilization"], 0.5)
        feed = self.cockpit.trace.activity("alex", SLUG)["items"]
        self.assertEqual((feed[0]["kind"], feed[0]["actor"], feed[0]["version_id"]), ("extraction", "austin", job["version_id"]))
        self.assertEqual(self.cockpit.trace.unseen(SLUG, "alex")["by"], {"austin": {"edits": 0, "comments": 0, "runs": 1}})

    def test_usage_limit_failure_keeps_receipts(self):
        self.connect()
        with patch.dict(os.environ, {"FAKE_OUTCOME": "usage_limit"}):
            self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "opus55"})
            self.settle(lambda: self.jobs()[0]["state"] in worker.TERMINAL)
        job = self.jobs()[0]
        self.assertEqual((job["state"], job["failure_reason"], job["result"]["usage_limit_resets_at"]), ("failed", "usage_limit", "2026-09-23T15:00:00+00:00"))
        self.assertTrue((self.root / "_dev/cockpit/state/jobs" / job["id"] / "status.json").is_file())
        self.assertIsNone(job["version_id"])

    def test_running_job_can_be_cancelled(self):
        self.connect()
        with patch.dict(os.environ, {"FAKE_OUTCOME": "wait"}):
            self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "opus55"})
            self.settle(lambda: self.jobs()[0]["state"] == "running" and (Path(self.worker.job(self.jobs()[0]["id"])["run_dir"]) / "status.json").is_file())
            time.sleep(0.3)
            self.runs.job_action(SLUG, "alex", {"action": "cancel", "job_id": self.jobs()[0]["id"]})
            self.settle(lambda: self.jobs()[0]["state"] in worker.TERMINAL)
        self.assertEqual((self.jobs()[0]["state"], self.jobs()[0]["failure_reason"]), ("cancelled", "cancelled"))

    def test_caps_limit_concurrent_runs_per_user(self):
        self.connect()
        with patch.dict(os.environ, {"FAKE_OUTCOME": "wait"}):
            for _ in range(3): self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "opus55"})
            self.worker.tick()
        states = sorted(job["state"] for job in self.jobs())
        self.assertEqual(states, ["queued", "running", "running"])

    def test_restarted_worker_finishes_orphaned_runs(self):
        self.connect()
        self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "opus55"})
        self.worker.tick()
        job = self.jobs()[0]
        self.worker.children[job["id"]].wait(timeout=20)
        restarted = worker.Worker(self.root)  # knows nothing about the child; the pid is dead
        restarted.recover(); restarted.tick()
        self.assertEqual(self.jobs()[0]["state"], "completed")
        conn = sqlite3.connect(self.ws.db_path)
        conn.execute("UPDATE jobs SET state='preparing' WHERE id=?", (job["id"],)); conn.commit(); conn.close()
        worker.Worker(self.root).recover()
        self.assertEqual(self.jobs()[0]["failure_reason"], "worker_restart")

    def test_import_crash_is_retried_once_and_a_broken_job_does_not_block_others(self):
        self.connect()
        self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "opus55"})
        self.worker.tick()
        job = self.jobs()[0]
        self.worker.children[job["id"]].wait(timeout=20)
        real = worker.Worker.import_version

        def crash_after_insert(this, *args):
            ident = real(this, *args)
            conn = sqlite3.connect(self.ws.db_path)  # as if the worker died before recording completion
            conn.execute("UPDATE jobs SET state='importing', version_id=NULL WHERE id=?", (job["id"],)); conn.commit(); conn.close()
            raise KeyboardInterrupt
        with patch.object(worker.Worker, "import_version", crash_after_insert), self.assertRaises(KeyboardInterrupt):
            self.worker.tick()
        worker.Worker(self.root).recover()  # the version row exists already; the retry must not collide
        done = self.jobs()[0]
        self.assertEqual(done["state"], "completed")
        self.assertEqual(sum(v["id"] == done["version_id"] for v in self.cockpit.deal(SLUG)["versions"]), 1)

        self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "opus55"})
        self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "opus55"})
        with patch.object(worker.Worker, "start", side_effect=[RuntimeError("disk full"), True], autospec=True):
            self.worker.tick()
        states = sorted((j["state"], j["failure_reason"]) for j in self.jobs() if j["id"] != done["id"])
        self.assertIn(("failed", "worker_error"), states)

    def test_a_job_is_started_once_and_a_foreign_pid_is_not_the_runner(self):
        self.connect()
        with patch.dict(os.environ, {"FAKE_OUTCOME": "wait"}):
            self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "opus55"})
            job = self.jobs()[0]
            row = self.worker.job(job["id"])
            self.assertTrue(self.worker.start(row))
            self.assertFalse(worker.Worker(self.root).start(row))  # a second worker loses the claim
        running = self.worker.job(job["id"])
        self.assertTrue(worker.alive(running["pid"], running["run_dir"]))
        self.assertFalse(worker.alive(os.getpid(), running["run_dir"]))
        with self.assertRaises(Conflict):
            self.runs.account_action("austin", {"action": "disconnect"})

    # ---- versions: rebase, restore, hide, compare ----------------------------------------

    def test_rebase_restore_and_hide(self):
        ident = self.add_version(change=("C2", "Changed who"))
        deal = self.cockpit.deal(SLUG)
        self.assertIn(ident, [v["id"] for v in deal["versions"]])
        rebased = self.ws.edit(SLUG, {"revision": 0, "base_sha256": self.base, "reason": "Use the new run", "operations": [{"type": "rebase", "target_version": ident}]}, "alex")
        self.assertEqual(rebased["workspace"]["base_version"], ident)
        self.assertTrue(next(v for v in rebased["versions"] if v["id"] == ident)["is_base"])
        latest = self.cockpit.trace.activity("austin", SLUG)["items"][0]
        self.assertEqual((latest["kind"], latest["revision"]), ("rebase", 1))
        with self.assertRaises(Conflict): self.runs.version_action(SLUG, "austin", {"action": "hide", "version_id": ident})
        new_base = rebased["workspace"]["base_sha256"]
        with self.assertRaises(WorkspaceError):
            self.ws.edit(SLUG, {"revision": 1, "base_sha256": new_base, "reason": "again", "operations": [{"type": "rebase", "target_version": ident}]}, "alex")
        restored = self.ws.edit(SLUG, {"revision": 1, "base_sha256": new_base, "reason": "Back", "operations": [{"type": "restore", "target_revision": 0}]}, "austin")
        self.assertEqual(restored["workspace"]["base_version"], "base-raw")
        self.assertTrue(self.runs.version_action(SLUG, "austin", {"action": "hide", "version_id": ident})["versions"][0]["hidden"])
        with self.assertRaises(WorkspaceError):
            self.ws.edit(SLUG, {"revision": 2, "base_sha256": self.base, "reason": "x", "operations": [{"type": "rebase", "target_version": ident}]}, "alex")
        with self.assertRaises(WorkspaceError): self.runs.version_action(SLUG, "austin", {"action": "hide", "version_id": "base-raw"})
        self.assertFalse(self.runs.version_action(SLUG, "alex", {"action": "unhide", "version_id": ident})["versions"][0]["hidden"])
        catalog = next(v for v in self.cockpit.deal(SLUG)["versions"] if v["id"] == "base-raw")
        self.assertTrue(catalog["is_base"])

    def test_a_run_imported_before_versions_were_stored_reads_its_receipt(self):
        ident = self.add_version()
        folder = self.root / "_dev/cockpit/state/versions" / SLUG / ident
        (folder / "check.json").write_text(json.dumps({"checker_version": "1.6", "ledger_schema": "Version 1", "summary": {"errors": 1, "warnings": 16}}))
        conn = self.ws._connect(write=True)
        conn.execute("INSERT INTO jobs (id, kind, slug, actor, created_at, state, params, result, version_id) VALUES ('old', 'extract', ?, 'alex', '2026-09-24T22:41:00+00:00', 'completed', '{}', ?, ?)",
                     (SLUG, json.dumps({"checker": {"errors": 1, "warnings": 16}}), ident))
        conn.commit(); conn.close()
        receipt = (folder / "check.json").read_bytes()
        checker = self.jobs()[0]["result"]["checker"]
        self.assertEqual(checker, {"errors": 1, "warnings": 16, "checker_version": "1.6", "ledger_schema": "Version 1"})
        version = next(v for v in self.cockpit.deal(SLUG)["versions"] if v["id"] == ident)
        self.assertEqual(version["checker"], {"checker_version": "1.6", "ledger_schema": "Version 1", "errors": 1, "warnings": 16})
        self.assertEqual((folder / "check.json").read_bytes(), receipt)
        self.assertEqual(json.loads(self.ws._connect().execute("SELECT result FROM jobs WHERE id='old'").fetchone()["result"]), {"checker": {"errors": 1, "warnings": 16}})

    def test_compare_matches_rows_by_key(self):
        ident = self.add_version(change=("C2", "Changed who"))
        who = self.cockpit.deal(SLUG)["ledger"]["columns"].index("Who")
        self.assertEqual(who, 2)  # column C, as changed above
        result = self.ws.compare(SLUG, "base-raw", ident)
        self.assertEqual([(c["type"], c["field"], c["after"]) for c in result["changes"]], [("update", "Who", "Changed who")])
        self.assertIsNone(result["same_instruction"])
        self.assertEqual(self.ws.compare(SLUG, "base-raw", "working")["changes"], [])
        first = self.cockpit.deal(SLUG)["ledger"]["rows"][0]["uid"]
        self.ws.edit(SLUG, {"revision": 0, "base_sha256": self.base, "reason": "Edit", "operations": [{"type": "update", "sheet": "Deal ledger", "uid": first, "values": {"Who": "Working who"}}]}, "austin")
        self.assertEqual([c["after"] for c in self.ws.compare(SLUG, ident, "working")["changes"]], ["Working who"])


if __name__ == "__main__": unittest.main()
