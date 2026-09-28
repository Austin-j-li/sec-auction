"""Comments, activity and "since your last visit" on disposable fixtures."""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch

from cockpit import server
from cockpit.workspace import WorkspaceError
from test_cockpit_workspace import StubAccess, fixture

SLUG = "alpha-deal"


class TraceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.cockpit, original = fixture(self.root)
        self.ws, self.trace = self.cockpit.workspace, self.cockpit.trace
        self.base = hashlib.sha256(original).hexdigest()
        self.revision = 0

    def tearDown(self): self.temp.cleanup()

    def save(self, ops, actor="austin", reason="Review edit"):
        result = self.ws.edit(SLUG, {"revision": self.revision, "base_sha256": self.base, "reason": reason, "operations": ops}, actor)
        self.revision = result["workspace"]["revision"]
        return result

    def rows(self):
        return self.cockpit.deal(SLUG)["ledger"]["rows"]

    def post(self, actor="austin", **request):
        return self.trace.comment(SLUG, request, actor)

    def test_reads_do_not_create_the_database(self):
        self.assertEqual(self.trace.comments(SLUG), {"threads": []})
        self.assertEqual(self.trace.activity("austin", SLUG)["items"], [])
        self.assertEqual(self.trace.unseen(SLUG, "austin")["by"], {})
        extras = self.trace.deal_extras(SLUG, "austin")
        self.assertEqual((extras["field_authors"], extras["thread_counts"], extras["seen"]), ({}, {}, None))
        self.assertFalse(self.ws.db_path.exists())

    def test_thread_lifecycle_and_authorship(self):
        uid = self.rows()[0]["uid"]
        threads = self.post(action="create", target={"kind": "row", "sheet": "Deal ledger", "uid": uid}, body="  Is this dated right?  ")["threads"]
        thread = threads[0]
        self.assertEqual((thread["target"]["uid"], thread["created_by"], thread["comments"][0]["body"]), (uid, "austin", "Is this dated right?"))
        self.assertTrue(thread["target"]["label"].startswith("Event #1"))
        first = thread["comments"][0]["id"]
        thread = self.post("alex", action="reply", thread_id=thread["id"], body="Yes, page 27.")["threads"][0]
        self.assertEqual(thread["comments"][1]["parent_id"], first)
        with self.assertRaises(WorkspaceError) as caught:
            self.post("alex", action="edit", comment_id=first, body="changed")
        self.assertEqual(caught.exception.status, 403)
        thread = self.post(action="edit", comment_id=first, body="Is this date right?")["threads"][0]
        self.assertEqual((thread["comments"][0]["body"], thread["comments"][0]["edit_count"]), ("Is this date right?", 1))
        self.assertIsNotNone(thread["comments"][0]["edited_at"])
        thread = self.post("alex", action="resolve", thread_id=thread["id"])["threads"][0]
        self.assertEqual(thread["resolved"]["by"], "alex")
        with self.assertRaises(WorkspaceError): self.post(action="resolve", thread_id=thread["id"])
        thread = self.post(action="reply", thread_id=thread["id"], body="One more point")["threads"][0]
        self.assertIsNone(thread["resolved"])
        thread = self.post(action="delete", comment_id=first)["threads"][0]
        self.assertEqual((thread["comments"][0]["body"], thread["comments"][0]["deleted"]["by"]), ("", "austin"))
        kinds = [item["kind"] for item in reversed(self.trace.activity("austin", SLUG)["items"])]
        self.assertEqual(kinds, ["comment", "reply", "comment_edit", "resolve", "reopen", "reply", "comment_delete"])

    def test_targets_are_validated_and_deal_and_finding_threads_work(self):
        for request in ({"target": {"kind": "row", "sheet": "Deal ledger", "uid": "nope"}, "body": "x"},
                        {"target": {"kind": "finding", "uid": "F9"}, "body": "x"},
                        {"target": {"kind": "row", "sheet": "Bogus", "uid": "x"}, "body": "x"},
                        {"target": {"kind": "deal"}, "body": "   "}):
            with self.assertRaises(WorkspaceError): self.post(action="create", **request)
        self.post(action="create", target={"kind": "deal"}, body="Overall")
        self.post(action="create", target={"kind": "finding", "uid": "F1"}, body="Agree")
        counts = self.trace.deal_extras(SLUG, "austin")["thread_counts"]
        self.assertEqual(counts, {"deal": {"open": 1, "resolved": 0}, "F1": {"open": 1, "resolved": 0}})

    def test_deleted_row_thread_is_marked_missing(self):
        rows = self.rows()
        last = rows[-1]["uid"]
        self.post(action="create", target={"kind": "row", "sheet": "Deal ledger", "uid": last}, body="Duplicate?")
        self.save([{"type": "delete", "sheet": "Deal ledger", "uid": last}])
        thread = self.trace.comments(SLUG)["threads"][0]
        self.assertTrue(thread["target_missing"])
        self.assertTrue(thread["target"]["label"].startswith("Event #"))

    def test_saves_write_activity_and_field_authors(self):
        rows = self.rows()
        self.save([{"type": "update", "sheet": "Deal ledger", "uid": rows[0]["uid"], "values": {"Who": "Party A"}}], actor="alex", reason="Name the bidder")
        values = {k: v for k, v in rows[0]["cells"].items() if k != "#"}
        inserted = self.save([{"type": "insert", "sheet": "Deal ledger", "after_uid": rows[0]["uid"], "values": values}], actor="austin")
        new_uid = inserted["ledger"]["rows"][1]["uid"]
        authors = self.trace.deal_extras(SLUG, "austin")["field_authors"]
        self.assertEqual((authors[rows[0]["uid"]]["Who"]["actor"], authors[rows[0]["uid"]]["Who"]["revision"]), ("alex", 1))
        self.assertEqual(authors[new_uid]["Event"]["actor"], "austin")
        self.save([{"type": "restore", "target_revision": 0}], actor="alex", reason="Back to raw")
        authors = self.trace.deal_extras(SLUG, "austin")["field_authors"]
        self.assertEqual(authors[rows[0]["uid"]]["Who"]["revision"], 3)
        self.assertNotIn(new_uid, authors)
        self.assertEqual(self.trace.deal_extras(SLUG, "austin", "base-raw")["field_authors"], {})
        items = self.trace.activity("austin", SLUG)["items"]
        self.assertEqual([(i["kind"], i["revision"], i["actor"]) for i in items], [("restore", 3, "alex"), ("revision", 2, "austin"), ("revision", 1, "alex")])
        self.assertEqual(items[2]["summary"], "Name the bidder")

    def test_unseen_and_seen_markers(self):
        uid = self.rows()[0]["uid"]
        self.save([{"type": "update", "sheet": "Deal ledger", "uid": uid, "values": {"Who": "Party A"}}], actor="alex")
        self.post("alex", action="create", target={"kind": "deal"}, body="Look at round 2")
        self.post("austin", action="create", target={"kind": "deal"}, body="My own note")
        self.assertEqual(self.trace.unseen(SLUG, "austin")["by"], {"alex": {"edits": 1, "comments": 1, "runs": 0}})
        self.assertEqual(self.trace.unseen(SLUG, "alex")["by"], {"austin": {"edits": 0, "comments": 1, "runs": 0}})
        feed = self.trace.activity("austin", SLUG)
        self.assertEqual([i["unseen"] for i in feed["items"]], [False, True, True])
        latest = feed["items"][0]["id"]
        seen = self.trace.mark_seen(SLUG, {"activity_id": latest}, "austin")["seen"]
        self.assertEqual((seen["activity_id"], seen["revision"]), (latest, 1))
        self.assertEqual(self.trace.unseen(SLUG, "austin")["by"], {})
        self.assertEqual(self.trace.deal_extras(SLUG, "austin")["seen"]["activity_id"], latest)
        self.trace.mark_seen(SLUG, {"activity_id": 0}, "austin")
        self.assertEqual(self.trace.unseen(SLUG, "austin")["by"], {"alex": {"edits": 1, "comments": 1, "runs": 0}})
        for bad in ({"activity_id": 999}, {"activity_id": -1}, {"activity_id": "1"}, {}):
            with self.assertRaises(WorkspaceError): self.trace.mark_seen(SLUG, bad, "austin")
        account = self.trace.activity("austin", None, account=True, actor="alex")
        self.assertEqual({i["slug"] for i in account["items"]}, {SLUG})
        self.assertEqual({i["name"] for i in account["items"]}, {"Alpha Deal"})
        self.assertNotIn("seen", account)

    def test_legacy_notes_migrate_once(self):
        uid = self.rows()[0]["uid"]
        self.save([{"type": "review", "uid": uid, "status": "reviewed", "note": "Checked against page 27"},
                   {"type": "finding", "id": "F1", "judgment": "supported", "implementation": "not_applied", "verification": "unchecked", "note": "Agree with F1"}], actor="alex")
        conn = sqlite3.connect(self.ws.db_path)
        conn.execute("DELETE FROM migrations"); conn.commit(); conn.close()
        for _ in range(2):
            self.ws._connect(write=True).close()
        threads = self.trace.comments(SLUG)["threads"]
        self.assertEqual(sorted((t["target"]["kind"], t["comments"][0]["body"], t["comments"][0]["actor"]) for t in threads),
                         [("finding", "Agree with F1", "alex"), ("row", "Checked against page 27", "alex")])


class TraceHTTPTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.cockpit, _ = fixture(self.root)
        self.httpd = server.make_server(0, self.cockpit, quiet=True)
        self.httpd.RequestHandlerClass.access_verifier = StubAccess()  # the assertion header carries the email
        self.port = self.httpd.server_address[1]
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.env = patch.dict(os.environ, {"COCKPIT_PUBLIC_ORIGIN": "https://lines.dealextract.org"})
        self.env.start()

    def tearDown(self):
        self.env.stop(); self.httpd.shutdown(); self.httpd.server_close(); self.temp.cleanup()

    def request(self, path, body=None, headers=None):
        req = urllib.request.Request(f"http://127.0.0.1:{self.port}{path}", data=None if body is None else json.dumps(body).encode(), headers=headers or {})
        try:
            with urllib.request.urlopen(req, timeout=20) as response: return response.status, json.loads(response.read())
        except urllib.error.HTTPError as exc: return exc.code, json.loads(exc.read())

    def user(self, email):
        headers = {"Host": "lines.dealextract.org", "Cf-Access-Jwt-Assertion": email}
        session = self.request("/api/session", headers=headers)[1]
        return {**headers, "Content-Type": "application/json", "Origin": "https://lines.dealextract.org", "X-Cockpit-CSRF": session["csrf_token"] or ""}

    def test_two_users_see_each_others_trace(self):
        austin, alex = self.user("junyu.li.24@ucl.ac.uk"), self.user("a.gorbenko@ucl.ac.uk")
        status, _ = self.request(f"/api/deal/{SLUG}/comments", {"action": "create", "target": {"kind": "deal"}, "body": "x"}, {**alex, "X-Cockpit-CSRF": "bad"})
        self.assertEqual(status, 403)
        anonymous = {"Host": "lines.dealextract.org", "Content-Type": "application/json", "Origin": "https://lines.dealextract.org"}
        self.assertEqual(self.request(f"/api/deal/{SLUG}/seen", {"activity_id": 0}, anonymous)[0], 403)
        self.assertEqual(self.request(f"/api/deal/{SLUG}/seen", headers=austin)[0], 405)
        status, payload = self.request(f"/api/deal/{SLUG}/comments", {"action": "create", "target": {"kind": "deal"}, "body": "Please check round 2"}, alex)
        self.assertEqual((status, payload["threads"][0]["created_by"]), (200, "alex"))
        deals = self.request("/api/deals", headers=austin)[1]
        self.assertEqual(next(d for d in deals if d["slug"] == SLUG)["unseen"]["by"], {"alex": {"edits": 0, "comments": 1, "runs": 0}})
        self.assertNotIn("unseen", next(d for d in self.request("/api/deals", headers={"Host": "lines.dealextract.org"})[1] if d["slug"] == SLUG))
        feed = self.request(f"/api/deal/{SLUG}/activity", headers=austin)[1]
        self.assertTrue(feed["items"][0]["unseen"])
        status, seen = self.request(f"/api/deal/{SLUG}/seen", {"activity_id": feed["items"][0]["id"]}, austin)
        self.assertEqual(status, 200)
        deal = self.request(f"/api/deal/{SLUG}", headers=austin)[1]
        self.assertEqual((deal["seen"]["activity_id"], deal["thread_counts"]["deal"]["open"]), (seen["seen"]["activity_id"], 1))
        self.assertEqual(self.request("/api/deals", headers=austin)[1][0]["unseen"]["by"], {})
        status, account = self.request("/api/activity?actor=alex&limit=5", headers=austin)
        self.assertEqual((status, account["items"][0]["name"]), (200, "Alpha Deal"))
        self.assertEqual(self.request("/api/activity?before=x", headers=austin)[0], 400)


if __name__ == "__main__": unittest.main()
