"""Instruction versions, engines and ChatGPT accounts, with a fake runner and a fake Codex CLI."""
from __future__ import annotations

import base64
import hashlib
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from cockpit import runs, worker
from cockpit.workspace import Conflict, Missing, WorkspaceError
import check_lean
from test_cockpit_runs import FAKE_RUNNER, SLUG, TOKEN
from test_cockpit_workspace import fixture


def access_token(hours: float) -> str:
    claims = base64.urlsafe_b64encode(json.dumps({"exp": int(time.time() + hours * 3600)}).encode()).decode().rstrip("=")
    return f"header.{claims}.signature"


def auth_json(hours: float, refreshed: str = "2026-09-14T11:38:08Z") -> str:
    return json.dumps({"auth_mode": "chatgpt", "tokens": {"access_token": access_token(hours), "refresh_token": "r", "id_token": "i"}, "last_refresh": refreshed})


FAKE_CODEX = r'''
import base64, json, os, sys, time
from pathlib import Path
home = Path(os.environ["CODEX_HOME"])
def token(hours):
    claims = base64.urlsafe_b64encode(json.dumps({"exp": int(time.time() + hours * 3600)}).encode()).decode().rstrip("=")
    return f"h.{claims}.s"
if sys.argv[1:3] == ["login", "--device-auth"]:
    print("\x1b[90mWelcome to Codex\x1b[0m\nFollow these steps to sign in with ChatGPT using device code authorization:\n")
    print("1. Open this link in your browser and sign in to your account\n   \x1b[94mhttps://auth.openai.com/codex/device\x1b[0m\n")
    print("2. Enter this one-time code \x1b[90m(expires in 15 minutes)\x1b[0m\n   \x1b[94mTSTB-IOSMS\x1b[0m\n", flush=True)
    flag = Path(os.environ["FAKE_CODEX_FLAG"])
    while not flag.exists():
        time.sleep(0.05)
    if flag.read_text() != "approve":
        print("Error logging in: device code expired", flush=True)
        sys.exit(1)
    (home / "auth.json").write_text(json.dumps({"tokens": {"access_token": token(240)}, "last_refresh": "2026-09-23T10:00:00Z"}))
    print("Successfully logged in", flush=True)
    sys.exit(0)
if sys.argv[1] == "exec":
    Path(os.environ["FAKE_CODEX_CALLS"]).open("a").write(" ".join(sys.argv[1:]) + "\n")
    if Path(os.environ["FAKE_CODEX_FLAG"] + "-renew").exists():
        (home / "auth.json").write_text(json.dumps({"tokens": {"access_token": token(240)}, "last_refresh": "2026-09-24T11:00:00Z"}))
    print("OK")
    sys.exit(0)
sys.exit(2)
'''


class Phase4Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.cockpit, _ = fixture(self.root)
        self.ws, self.runs, self.instructions = self.cockpit.workspace, self.cockpit.runs, self.cockpit.instructions
        self.flag = self.root / "codex-flag"
        self.calls = self.root / "codex-calls"
        self.env = patch.dict(os.environ, {"COCKPIT_TOKEN_ROOT": str(self.root / "tokens"), "FAKE_WORKBOOK": str(self.root / "extraction/alpha-deal.xlsx"),
                                           "FAKE_CODEX_FLAG": str(self.flag), "FAKE_CODEX_CALLS": str(self.calls)})
        self.env.start()
        (self.root / "fake_runner.py").write_text(FAKE_RUNNER)
        (self.root / "fake_codex.py").write_text(FAKE_CODEX)
        codex = self.root / "codex"
        # The worker gives Codex a minimal environment, so the fake's settings are fixed in its wrapper.
        codex.write_text(f"#!/bin/sh\nexport FAKE_CODEX_FLAG={self.flag} FAKE_CODEX_CALLS={self.calls}\nexec {sys.executable} {self.root / 'fake_codex.py'} \"$@\"\n")
        codex.chmod(0o755)
        self.patches = [patch.object(worker, "RUNNER", self.root / "fake_runner.py"), patch.object(worker, "CODEX", str(codex))]
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
            time.sleep(0.05)
        self.fail("condition not reached")

    def gpt_login(self, user="austin", hours=240.0):
        home = runs.codex_home(user)
        home.mkdir(parents=True, exist_ok=True)
        (home / "auth.json").write_text(auth_json(hours))
        conn = self.ws._connect(write=True)
        conn.execute("INSERT OR REPLACE INTO accounts VALUES (?, 'chatgpt', '2026-09-23T10:00:00+00:00', NULL)", (user,))
        conn.commit(); conn.close()

    def jobs(self):
        return self.runs.jobs(SLUG)["jobs"]

    # ---- instructions -----------------------------------------------------------------

    def test_repository_instruction_is_imported_as_the_published_default(self):
        listing = self.instructions.list()
        [item] = listing["items"]
        text = (self.root / "SEC_Deal_Ledger_Extraction_Instruction.md").read_text()
        self.assertEqual((item["name"], item["status"], item["is_default"], listing["default_id"]), ("Version 0", "published", True, item["id"]))
        self.assertEqual(item["sha256"], hashlib.sha256(text.encode()).hexdigest())
        self.assertEqual(self.instructions.detail(item["id"])["text"], text)
        self.assertEqual(len(self.instructions.list()["items"]), 1)  # imported once

    def test_repository_instruction_seeds_version_number_label(self):
        from cockpit.instructions import header_version
        self.assertEqual(header_version("# Synthetic instruction\n\n**Version 0, 27 September 2026.**"), "Version 0")
        self.assertEqual(header_version("# Synthetic instruction\n\n**Version 1, 27 September 2026.**"), "Version 1")

    def test_draft_save_publish_and_default(self):
        base = self.instructions.list()["items"][0]
        draft = self.instructions.request("alex", {"action": "draft", "from": base["id"]})
        ident, first = draft["item"]["id"], draft["item"]["sha256"]
        self.assertEqual((draft["item"]["status"], draft["item"]["parent_label"], draft["parent_text"]), ("draft", "Version 0", draft["text"]))
        self.assertEqual(draft["item"]["label"], f"draft {first[:7]} (Alex)")
        saved = self.instructions.request("austin", {"action": "save", "id": ident, "text": draft["text"] + "Be honest about uncertainty.\n", "base_sha256": first})
        self.assertNotEqual(saved["item"]["sha256"], first)
        self.assertEqual([edit["author"] for edit in saved["history"]], ["alex", "austin"])
        with self.assertRaisesRegex(Conflict, "saved this draft"):  # a stale save is refused
            self.instructions.request("alex", {"action": "save", "id": ident, "text": "other", "base_sha256": first})
        self.assertEqual(self.instructions.detail(ident, seq=1)["text"], draft["text"])
        unchanged = self.instructions.request("austin", {"action": "save", "id": ident, "text": saved["text"], "base_sha256": saved["item"]["sha256"]})
        self.assertEqual(len(unchanged["history"]), 2)
        with self.assertRaisesRegex(Conflict, "only a published"):
            self.instructions.request("alex", {"action": "default", "id": ident})
        for bad in ({"name": "", "note": "x"}, {"name": "Version/1", "note": "x"}, {"name": "Version 1", "note": " "}):
            with self.assertRaises(WorkspaceError):
                self.instructions.request("alex", {"action": "publish", "id": ident, **bad})
        with self.assertRaisesRegex(Conflict, "already used"):
            self.instructions.request("alex", {"action": "publish", "id": ident, "name": "Version 0", "note": "x"})
        published = self.instructions.request("alex", {"action": "publish", "id": ident, "name": "Version 1", "note": "States the uncertainty rule."})
        self.assertEqual((published["item"]["status"], published["item"]["label"], published["item"]["published_by"]), ("published", "Version 1", "alex"))
        for action in ({"action": "save", "id": ident, "text": "x", "base_sha256": published["item"]["sha256"]}, {"action": "publish", "id": ident, "name": "v1.15", "note": "x"}):
            with self.assertRaises(Conflict):
                self.instructions.request("austin", action)
        listing = self.instructions.request("austin", {"action": "default", "id": ident})
        self.assertEqual(listing["default_id"], ident)
        self.assertEqual([item["name"] for item in listing["items"]], ["Version 1", "Version 0"])
        kinds = [item["kind"] for item in self.cockpit.trace.activity("austin", account=True)["items"]]
        self.assertEqual(kinds, ["instruction_default", "instruction_published", "instruction_draft"])
        with self.assertRaises(Missing):
            self.instructions.detail("0" * 12)

    def test_stored_texts_are_content_addressed_and_checked(self):
        sha = self.instructions.put("text one")
        self.assertEqual(self.instructions.put("text one"), sha)
        self.instructions.path(sha).write_text("tampered")
        with self.assertRaisesRegex(WorkspaceError, "does not match"):
            self.instructions.text(sha)

    # ---- engines and runs -----------------------------------------------------------------

    def test_new_default_uses_opus_medium_without_relabelling_legacy_jobs(self):
        self.runs.account_action("austin", {"action": "token", "token": TOKEN})
        self.runs.job_action(SLUG, "austin", {"action": "extract"})
        self.settle(lambda: self.jobs()[0]["state"] == "completed")
        job = self.jobs()[0]
        self.assertEqual((job["params"]["engine"], job["params"]["model"], job["params"]["effort"], job["params"]["account"]),
                         ("opus55", "claude-opus-5-5", "medium", "claude"))
        version = next(v for v in self.ws.item(SLUG)["versions"] if v["id"] == job["version_id"])
        self.assertEqual((version["model"], version["effort"]), ("claude-opus-5-5", "medium"))
        # Astra chosen explicitly keeps its own default effort.
        self.gpt_login()
        astra = self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "astra6"})["jobs"][0]
        self.assertEqual((astra["params"]["engine"], astra["params"]["effort"]), ("astra6", "high"))
        self.assertEqual(worker.engine_of({})[0], "opus55")
        self.assertEqual(runs.job_account({}), "claude")
        self.assertEqual(worker.engine_of({"engine": "sol6"})[0], "sol6")
        defaults = {e["id"]: e["default_effort"] for e in self.runs.account("austin")["engines"]}
        self.assertEqual(defaults, {"astra6": "high", "opus55": "medium", "fable51": "medium", "sol6": "medium", "sol61": "medium"})

    def test_extract_checks_the_engines_account_and_freezes_the_instruction(self):
        with self.assertRaisesRegex(Conflict, "ChatGPT"):
            self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "astra6"})
        with self.assertRaisesRegex(Conflict, "Claude"):
            self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "fable51"})
        with self.assertRaisesRegex(WorkspaceError, "unknown engine"):
            self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "gpt-4"})
        self.gpt_login()
        base = self.instructions.list()["items"][0]
        draft = self.instructions.request("alex", {"action": "draft", "from": base["id"]})
        self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "astra6", "effort": "high", "instruction_id": draft["item"]["id"]})
        self.instructions.request("alex", {"action": "save", "id": draft["item"]["id"], "text": "edited later", "base_sha256": draft["item"]["sha256"]})
        [job] = self.jobs()
        self.assertEqual({key: job["params"][key] for key in ("engine", "engine_label", "model", "provider", "account", "effort")},
                         {"engine": "astra6", "engine_label": "GPT-6-Astra", "model": "gpt-6-astra", "provider": "sol", "account": "chatgpt", "effort": "high"})
        self.assertEqual(job["params"]["instruction"], {"id": draft["item"]["id"], "label": draft["item"]["label"], "name": None, "status": "draft", "sha256": draft["item"]["sha256"]})
        account = self.runs.account("austin")
        self.assertEqual({engine["id"]: engine["connected"] for engine in account["engines"]}, {"opus55": False, "fable51": False, "sol6": True, "sol61": True, "astra6": True})
        self.assertTrue(account["chatgpt"]["connected"])

    def test_runs_under_distinct_instructions_use_the_version1_checker(self):
        """Distinct frozen instructions use the same current ledger format and checker."""
        from test_cockpit_workspace import build_version1_workbook
        self.runs.account_action("austin", {"action": "token", "token": TOKEN})
        base = self.instructions.list()["items"][0]
        drafts = []
        for text in ("Rules A stand-in.\n", "Rules B stand-in.\n"):
            draft = self.instructions.request("alex", {"action": "draft", "from": base["id"]})
            drafts.append(self.instructions.request("alex", {"action": "save", "id": draft["item"]["id"], "text": text, "base_sha256": draft["item"]["sha256"]})["item"])
        for number, draft in enumerate(drafts):
            workbook = build_version1_workbook(self.root / f"version1-run-{number}.xlsx")
            book = check_lean.openpyxl.load_workbook(workbook)
            book["Deal ledger"].cell(2, check_lean.LEDGER_COLUMNS.index("Note") + 1).value = f"Run {number}."
            book.save(workbook)
            with patch.dict(os.environ, {"FAKE_WORKBOOK": str(workbook)}):
                self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "opus55", "instruction_id": draft["id"]})
                self.settle(lambda: all(job["state"] == "completed" for job in self.jobs()))
        jobs = self.jobs()
        self.assertEqual({job["params"]["instruction"]["sha256"] for job in jobs}, {draft["sha256"] for draft in drafts})
        self.assertEqual({job["result"]["checker"]["ledger_schema"] for job in jobs}, {"Version 1"})
        self.assertEqual({self.ws.deal(SLUG, job["version_id"])["ledger_schema"] for job in jobs}, {"Version 1"})

    def test_a_draft_run_and_a_published_run_differ_in_instruction(self):
        self.runs.account_action("austin", {"action": "token", "token": TOKEN})
        self.gpt_login()
        base = self.instructions.list()["items"][0]
        draft = self.instructions.request("alex", {"action": "draft", "from": base["id"]})
        draft = self.instructions.request("alex", {"action": "save", "id": draft["item"]["id"], "text": draft["text"] + "A general change.\n", "base_sha256": draft["item"]["sha256"]})
        self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "fable51", "effort": "low"})
        self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "sol6", "effort": "xhigh", "instruction_id": draft["item"]["id"]})
        self.settle(lambda: all(job["state"] == "completed" for job in self.jobs()))
        versions = {version["id"].split("-")[0]: version for version in self.ws.item(SLUG)["versions"] if version.get("started_by")}
        fable, sol = versions["fable51"], versions["sol6"]
        self.assertEqual((fable["engine"], fable["instruction_version"], fable["instruction_sha256"], fable["instruction_id"]), ("Fable 5.1", "Version 0", base["sha256"], base["id"]))
        self.assertEqual((sol["engine"], sol["instruction_version"], sol["instruction_sha256"]), ("GPT-6-Sol", None, draft["item"]["sha256"]))
        self.assertRegex(fable["label"], r"^Fable 5\.1 · low · Version 0 — Austin, ")
        self.assertIn(f"GPT-6-Sol · xhigh · draft {draft['item']['sha256'][:7]} (Alex) — Austin", sol["label"])
        self.assertFalse(self.ws.compare(SLUG, fable["id"], sol["id"])["same_instruction"])
        # An unmatched catalog instruction name has no hash; the published name resolves it.
        catalog = self.ws.catalog()
        catalog["deals"][SLUG]["versions"][0]["instruction_version"] = "Unmatched"
        self.ws.catalog_path.write_text(json.dumps(catalog))
        self.assertIsNone(self.ws.compare(SLUG, "base-raw", fable["id"])["same_instruction"])
        catalog["deals"][SLUG]["versions"][0]["instruction_version"] = "Version 0"
        self.ws.catalog_path.write_text(json.dumps(catalog))
        self.assertTrue(self.ws.compare(SLUG, "base-raw", fable["id"])["same_instruction"])
        self.assertFalse(self.ws.compare(SLUG, "base-raw", sol["id"])["same_instruction"])
        summaries = [item["summary"] for item in self.cockpit.trace.activity("austin", SLUG)["items"] if item["kind"] == "extraction"]
        self.assertTrue(any(summary.startswith("GPT-6-Sol · xhigh · draft ") for summary in summaries))

    def test_an_altered_stored_instruction_fails_the_run(self):
        self.runs.account_action("austin", {"action": "token", "token": TOKEN})
        self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "opus55"})
        sha = self.jobs()[0]["params"]["instruction"]["sha256"]
        self.instructions.path(sha).write_text("tampered")
        self.settle(lambda: self.jobs()[0]["state"] == "failed")
        self.assertEqual(self.jobs()[0]["failure_reason"], "instruction_missing")

    def test_a_job_without_an_instruction_fails_instead_of_using_the_repository_text(self):
        self.runs.account_action("austin", {"action": "token", "token": TOKEN})
        job = self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "opus55"})["jobs"][0]
        params = {key: value for key, value in job["params"].items() if key != "instruction"}
        conn = self.ws._connect(write=True)
        conn.execute("UPDATE jobs SET params=? WHERE id=?", (json.dumps(params), job["id"]))
        conn.commit(); conn.close()
        self.settle(lambda: self.jobs()[0]["state"] == "failed")
        self.assertEqual((self.jobs()[0]["failure_reason"], self.jobs()[0]["error"]), ("instruction_missing", "The job names no instruction version."))
        self.assertFalse((self.root / "_dev/runs" / f"cockpit-{job['id']}").exists())

    # ---- ChatGPT sign-in and refresh -------------------------------------------------------

    def test_chatgpt_sign_in_shows_link_and_code_then_saves_the_login(self):
        account = self.runs.chatgpt_action("alex", {"action": "connect"})
        job = account["chatgpt_connect"]["job_id"]
        self.settle(lambda: (self.runs.account("alex")["chatgpt_connect"] or {}).get("state") == "waiting_for_approval")
        shown = self.runs.account("alex")["chatgpt_connect"]
        self.assertEqual((shown["link"], shown["code"]), ("https://auth.openai.com/codex/device", "TSTB-IOSMS"))
        self.flag.write_text("approve")
        self.settle(lambda: self.runs.account("alex")["chatgpt"]["connected"])
        home = runs.codex_home("alex")
        self.assertEqual(oct(home.stat().st_mode & 0o777), "0o700")
        self.assertEqual(oct((home / "auth.json").stat().st_mode & 0o777), "0o600")
        self.assertEqual(self.runs.account("alex")["chatgpt_connect"]["state"], "completed")
        self.assertFalse(self.runs.account("austin")["chatgpt"]["connected"])
        self.assertEqual([p.name for p in home.parent.iterdir()], ["codex"])  # no staging folder left
        self.runs.chatgpt_action("alex", {"action": "disconnect"})
        self.assertFalse(home.exists())
        self.assertFalse(self.runs.account("alex")["chatgpt"]["connected"])
        self.assertTrue(job)

    def test_chatgpt_sign_in_failure_and_cancel_keep_an_existing_login(self):
        self.gpt_login("alex")
        before = (runs.codex_home("alex") / "auth.json").read_text()
        self.runs.chatgpt_action("alex", {"action": "connect"})
        self.settle(lambda: (self.runs.account("alex")["chatgpt_connect"] or {}).get("state") == "waiting_for_approval")
        self.flag.write_text("deny")
        self.settle(lambda: self.runs.account("alex")["chatgpt_connect"]["state"] == "failed")
        self.assertIn("device code expired", self.runs.account("alex")["chatgpt_connect"]["error"])
        self.flag.unlink()
        account = self.runs.chatgpt_action("alex", {"action": "connect"})
        self.settle(lambda: (self.runs.account("alex")["chatgpt_connect"] or {}).get("state") == "waiting_for_approval")
        self.runs.chatgpt_action("alex", {"action": "cancel", "job_id": account["chatgpt_connect"]["job_id"]})
        self.settle(lambda: self.runs.account("alex")["chatgpt_connect"]["state"] == "cancelled")
        self.assertEqual((runs.codex_home("alex") / "auth.json").read_text(), before)

    def test_a_login_near_expiry_is_refreshed_before_a_gpt_run(self):
        self.gpt_login("austin", hours=3)
        self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "sol6"})
        Path(f"{self.flag}-renew").write_text("")
        self.settle(lambda: self.jobs()[0]["state"] == "completed")
        self.assertIn("-m gpt-6-sol", self.calls.read_text())
        self.assertGreater(runs.codex_login(runs.codex_home("austin") / "auth.json")["hours_left"], 200)

    def test_a_login_that_does_not_renew_fails_the_run_as_login_expired(self):
        self.gpt_login("austin", hours=3)
        self.runs.job_action(SLUG, "austin", {"action": "extract", "engine": "astra6"})
        self.settle(lambda: self.jobs()[0]["state"] == "failed")
        self.assertEqual(self.jobs()[0]["failure_reason"], "login_expired")
        self.assertEqual(len(self.calls.read_text().splitlines()), 1)

    def test_logins_within_a_day_are_refreshed_at_most_hourly(self):
        self.gpt_login("alex", hours=20)
        self.gpt_login("austin", hours=100)
        for _ in range(5):
            self.worker.tick()
            for thread in list(self.worker.refreshing.values()): thread.join(10)
        self.assertEqual(len(self.calls.read_text().splitlines()), 1)
        self.assertIn("alex", self.worker.refreshed)
        self.assertNotIn("austin", self.worker.refreshed)


if __name__ == "__main__":
    unittest.main()
