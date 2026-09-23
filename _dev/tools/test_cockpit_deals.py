"""Adding deals: seed search, EDGAR lookups (stubbed), saved filings, pending deals and their first run."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import fetch_filing
from cockpit import worker
from cockpit.workspace import Conflict, Missing, WorkspaceError
from test_cockpit_runs import FAKE_RUNNER, TOKEN
from test_cockpit_workspace import fixture
from test_fetch_filing import document_block

INDEX = "https://www.sec.gov/Archives/edgar/data/42/0000000042-21-000007-index.htm"
SUBMISSION_URL = "https://www.sec.gov/Archives/edgar/data/42/0000000042-21-000007.txt"
HEADER = (b"<SEC-DOCUMENT>0000000042-21-000007.txt : 20210304\n<SEC-HEADER>\nCONFORMED SUBMISSION TYPE:\tDEFM14A\n"
          b"FILED AS OF DATE:\t\t20210304\n\nFILER:\n\n\tCOMPANY DATA:\t\n\t\tCOMPANY CONFORMED NAME:\t\t\tBETA HOLDINGS CORP\n</SEC-HEADER>\n")
PROXY = document_block("DEFM14A", "beta-proxy.htm", b"<h2>Background of the Merger</h2><p>Beta met Party A.</p>")
LETTER = document_block("EX-99.1", "letter.htm", b"<p>A letter</p>")
IMAGE = document_block("GRAPHIC", "logo.jpg", b"binary")
SUBMISSION = HEADER + PROXY + LETTER + IMAGE
SEED = [
    {"deal": "beta-holdings", "target_name": "BETA HOLDINGS CORP", "deal_number": "1", "form_type": "DEFM14A", "date_filed": "2021-03-04", "index_url": INDEX, "status": "ok", "secret": "do not return"},
    {"deal": "gamma", "target_name": "GAMMA INC", "deal_number": "2", "form_type": "DEFM14A", "date_filed": "2021-03-04", "index_url": INDEX, "status": "review: 2 target names", "secret": "x"},
    {"deal": "alpha-deal", "target_name": "ALPHA DEAL INC", "deal_number": "3", "form_type": "DEFM14A", "date_filed": "2020-01-01", "index_url": "", "status": "review: 0 usable of 1 links", "secret": "x"},
]


class DealsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.cockpit, _ = fixture(self.root)
        self.ws, self.deals, self.runs = self.cockpit.workspace, self.cockpit.deals, self.cockpit.runs
        (self.root / "ref").mkdir()
        with (self.root / "ref/seed.csv").open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(SEED[0]))
            writer.writeheader()
            writer.writerows(SEED)
        self.fetched = []
        self.patches = [patch.object(fetch_filing, "get", side_effect=lambda url: self.fetched.append(url) or SUBMISSION),
                        patch.object(worker, "RUNNER", self.root / "fake_runner.py"),
                        patch.dict(os.environ, {"COCKPIT_TOKEN_ROOT": str(self.root / "tokens"), "FAKE_WORKBOOK": str(self.root / "extraction/alpha-deal.xlsx")})]
        for item in self.patches: item.start()
        (self.root / "fake_runner.py").write_text(FAKE_RUNNER)
        self.worker = worker.Worker(self.root)

    def tearDown(self):
        for child in self.worker.children.values():
            if child.poll() is None: child.kill()
        for item in self.patches: item.stop()
        self.temp.cleanup()

    def settle(self, predicate, seconds=20):
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            self.worker.tick()
            if predicate(): return
            time.sleep(0.05)
        self.fail("condition not reached")

    def looked_up(self, url=INDEX, seed=None, user="austin"):
        lookup = self.deals.request(user, {"action": "lookup", "url": url, **({"seed_deal": seed} if seed else {})})["lookup"]
        self.settle(lambda: self.deals.lookup(lookup["id"])["state"] in ("completed", "failed"))
        return self.deals.lookup(lookup["id"])

    def add(self, lookup, **overrides):
        body = {"action": "add", "lookup_id": lookup["id"], "document": lookup["result"]["preselected"],
                "slug": lookup["result"]["suggested"]["slug"], "name": lookup["result"]["suggested"]["name"], **overrides}
        return self.deals.request("alex", body)

    # ---- seed ------------------------------------------------------------------------

    def test_seed_search_returns_identifying_columns_only(self):
        self.assertEqual(self.deals.seed_search("")["rows"], [])
        rows = self.deals.seed_search("ALPHA")["rows"]
        self.assertEqual([row["deal"] for row in rows], ["alpha-deal"])
        self.assertEqual(set(rows[0]), {"deal", "target_name", "form_type", "date_filed", "index_url", "status", "in_cockpit"})
        self.assertTrue(rows[0]["in_cockpit"])
        self.assertFalse(self.deals.seed_search("beta")["rows"][0]["in_cockpit"])

    # ---- lookups -------------------------------------------------------------------------

    def test_seed_lookup_preselects_the_main_document(self):
        lookup = self.looked_up(seed="beta-holdings")
        self.assertEqual(self.fetched, [SUBMISSION_URL])
        result = lookup["result"]
        self.assertEqual((lookup["state"], result["preselected"], result["suggested"]), ("completed", "beta-proxy.htm", {"slug": "beta-holdings", "name": "Beta Holdings"}))
        self.assertEqual((result["form_type"], result["date_filed"], result["warnings"]), ("DEFM14A", "2021-03-04", []))
        self.assertEqual([(d["filename"], d["html"], d["background"]) for d in result["documents"]],
                         [("beta-proxy.htm", True, True), ("letter.htm", True, False), ("logo.jpg", False, False)])
        self.assertNotIn("secret", json.dumps(result))
        self.assertEqual(hashlib.sha256(self.deals.lookup_path(lookup["id"]).read_bytes()).hexdigest(), result["sha256"])

    def test_review_rows_and_pasted_links(self):
        review = self.looked_up(seed="gamma")["result"]
        self.assertIsNone(review["preselected"])
        self.assertIn("marks this deal for review (2 target names)", review["warnings"][0])
        pasted = self.looked_up(url="https://www.sec.gov/Archives/edgar/data/42/000000004221000007/letter.htm")["result"]
        self.assertEqual((pasted["preselected"], pasted["suggested"], pasted["seed"]), ("letter.htm", {"slug": "beta-holdings", "name": "Beta Holdings"}, None))
        for bad in ({"url": "https://example.com/filing-index.htm"}, {"url": INDEX, "seed_deal": "nope"}, {"url": None}):
            with self.assertRaises(WorkspaceError): self.deals.request("austin", {"action": "lookup", **bad})

    def test_failed_fetch_is_reported(self):
        with patch.object(fetch_filing, "get", side_effect=fetch_filing.FetchError("404 Not Found")):
            lookup = self.looked_up()
        self.assertEqual((lookup["state"], lookup["error"], lookup["result"]), ("failed", "404 Not Found", None))

    # ---- adding --------------------------------------------------------------------------

    def test_add_saves_the_document_bytes_and_lists_a_pending_deal(self):
        lookup = self.looked_up(seed="beta-holdings")
        self.assertEqual(self.add(lookup), {"slug": "beta-holdings"})
        path = self.root / "_dev/cockpit/state/filings/beta-holdings/beta-holdings_2021-03-04_DEFM14A.htm"
        self.assertEqual(path.read_bytes(), PROXY)
        row = self.deals.added("beta-holdings")[0]
        self.assertEqual((row["source_kind"], row["seed_deal"], row["source_url"], row["document"], row["added_by"], row["sha256"], row["bytes"]),
                         ("seed", "beta-holdings", SUBMISSION_URL, "beta-proxy.htm", "alex", hashlib.sha256(PROXY).hexdigest(), len(PROXY)))
        listed = next(d for d in self.cockpit.list_deals() if d["slug"] == "beta-holdings")
        self.assertEqual((listed["pending"], listed["name"], listed["form_type"]), (True, "Beta Holdings", "DEFM14A"))
        deal = self.cockpit.deal("beta-holdings")
        self.assertEqual((deal["pending"], deal["versions"], deal["ledger"]["rows"], deal["workspace"]["editable"]), (True, [], [], False))
        self.assertIn("Background of the Merger", json.dumps(self.cockpit.filing_payload("beta-holdings")))
        self.assertTrue(self.deals.seed_search("beta")["rows"][0]["in_cockpit"])
        activity = self.cockpit.trace.activity("austin", "beta-holdings")["items"]
        self.assertEqual((activity[0]["kind"], activity[0]["actor"]), ("deal_added", "alex"))
        self.assertIn("from the seed (beta-holdings)", activity[0]["summary"])
        with self.assertRaises(Conflict): self.ws.export("beta-holdings")
        with self.assertRaises(Conflict): self.ws.changes("beta-holdings")
        with self.assertRaises(Conflict): self.cockpit.trace.comment("beta-holdings", {"action": "create", "target": {"kind": "deal"}, "body": "x"}, "austin")
        with self.assertRaises(Missing): self.cockpit.deal("beta-holdings", version="v1132-raw")

    def test_add_refusals(self):
        lookup = self.looked_up(seed="beta-holdings")
        for overrides, error in (({"slug": "alpha-deal"}, Conflict), ({"slug": "Bad Slug"}, WorkspaceError), ({"name": " "}, WorkspaceError),
                                 ({"document": "logo.jpg"}, WorkspaceError), ({"document": "absent.htm"}, WorkspaceError)):
            with self.subTest(overrides=overrides), self.assertRaises(error):
                self.add(lookup, **overrides)
        self.assertFalse((self.root / "_dev/cockpit/state/filings").exists())
        self.add(lookup)
        with self.assertRaises(Conflict): self.add(lookup)  # the same slug twice
        # A lookup whose cached submission changed, or that is a day old, is refused.
        other = self.looked_up(seed="gamma")
        self.deals.lookup_path(other["id"]).write_bytes(b"changed")
        with self.assertRaises(Conflict): self.add(other, document="beta-proxy.htm", slug="gamma")
        stale = self.looked_up()
        conn = sqlite3.connect(self.ws.db_path)
        conn.execute("UPDATE jobs SET ended_at='2020-01-01T00:00:00+00:00' WHERE id=?", (stale["id"],)); conn.commit(); conn.close()
        with self.assertRaises(Conflict): self.add(stale, slug="beta-2021")

    def test_amended_form_types_make_safe_file_names(self):
        amended = SUBMISSION.replace(b"CONFORMED SUBMISSION TYPE:\tDEFM14A", b"CONFORMED SUBMISSION TYPE:\tSC TO-T/A")
        with patch.object(fetch_filing, "get", return_value=amended):
            lookup = self.looked_up()
        self.add(lookup, document="beta-proxy.htm", slug="beta-amended")
        self.assertEqual(self.deals.added("beta-amended")[0]["file"], "beta-amended_2021-03-04_SCTO-T-A.htm")
        self.assertTrue((self.root / "_dev/cockpit/state/filings/beta-amended/beta-amended_2021-03-04_SCTO-T-A.htm").is_file())

    # ---- first run -------------------------------------------------------------------------

    def test_first_run_of_an_added_deal_becomes_its_base(self):
        self.add(self.looked_up(seed="beta-holdings"))
        self.runs.account_action("austin", {"action": "token", "token": TOKEN})
        for _ in range(2):
            self.runs.job_action("beta-holdings", "austin", {"action": "extract"})
            self.settle(lambda: all(job["state"] in worker.TERMINAL for job in self.runs.jobs("beta-holdings")["jobs"]))
        jobs = self.runs.jobs("beta-holdings")["jobs"]
        self.assertEqual([job["state"] for job in jobs], ["completed", "completed"], jobs)
        first = jobs[-1]["version_id"]
        deal = self.cockpit.deal("beta-holdings")
        self.assertNotIn("pending", deal)
        self.assertEqual(deal["workspace"]["base_version"], first)
        self.assertEqual([v["id"] for v in deal["versions"] if v.get("is_base")], [first])
        self.assertEqual(deal["filing"]["file"], "beta-holdings_2021-03-04_DEFM14A.htm")
        listed = next(d for d in self.cockpit.list_deals() if d["slug"] == "beta-holdings")
        self.assertNotIn("pending", listed)
        self.assertTrue(self.ws.export("beta-holdings").startswith(b"PK"))

    # ---- hiding deals --------------------------------------------------------------------

    def test_hide_and_unhide_deals(self):
        added = self.add(self.looked_up(seed="beta-holdings"))["slug"]
        listed = lambda: {d["slug"]: d for d in self.cockpit.list_deals()}
        self.assertEqual({slug: d["hidden"] for slug, d in listed().items()}, {"alpha-deal": False, added: False})
        from cockpit import data
        with self.assertRaises(data.DealNotFound): self.deals.visibility("nosuch", "austin", {"action": "hide"})
        with self.assertRaises(WorkspaceError): self.deals.visibility("alpha-deal", "austin", {"action": "remove"})
        with self.assertRaises(Conflict): self.deals.visibility("alpha-deal", "austin", {"action": "unhide"})
        # A queued or running job on the deal blocks hiding.
        self.runs.account_action("austin", {"action": "token", "token": TOKEN})
        job = self.runs.job_action("alpha-deal", "austin", {"action": "extract"})["jobs"][0]
        with self.assertRaises(Conflict) as caught: self.deals.visibility("alpha-deal", "alex", {"action": "hide"})
        self.assertIn("still going", str(caught.exception))
        conn = sqlite3.connect(self.ws.db_path)
        conn.execute("UPDATE jobs SET state='failed' WHERE id=?", (job["id"],)); conn.commit(); conn.close()
        revision = self.ws.deal("alpha-deal")["workspace"]["revision"]
        result = self.deals.visibility("alpha-deal", "alex", {"action": "hide"})
        self.assertEqual((result["hidden"], result["hidden_by"]), (True, "alex"))
        self.deals.visibility(added, "austin", {"action": "hide"})
        with self.assertRaises(Conflict): self.deals.visibility("alpha-deal", "austin", {"action": "hide"})
        with self.assertRaises(Conflict) as caught: self.runs.job_action("alpha-deal", "austin", {"action": "extract"})
        self.assertIn("unhide the deal first", str(caught.exception))
        # Nothing else changes, the flag survives a new process, and the deal still opens.
        fresh = data.Cockpit(self.root)
        self.assertEqual({slug: (d["hidden"], d["hidden_by"]) for slug, d in {d["slug"]: d for d in fresh.list_deals()}.items()},
                         {"alpha-deal": (True, "alex"), added: (True, "austin")})
        self.assertEqual(fresh.workspace.deal("alpha-deal")["workspace"]["revision"], revision)
        self.assertTrue(fresh.workspace.item(added)["pending"])
        feed = self.cockpit.trace.activity("austin", "alpha-deal")["items"]
        self.assertEqual((feed[0]["kind"], feed[0]["actor"], feed[0]["summary"]), ("hide_deal", "alex", "Hid the deal"))
        self.assertTrue(feed[0]["unseen"])
        result = self.deals.visibility("alpha-deal", "austin", {"action": "unhide"})
        self.assertEqual((result["hidden"], result["hidden_by"], result["hidden_at"]), (False, None, None))
        self.assertEqual(self.cockpit.trace.activity("alex", "alpha-deal")["items"][0]["summary"], "Unhid the deal")
        self.assertEqual({slug: d["hidden"] for slug, d in listed().items()}, {"alpha-deal": False, added: True})
        self.assertEqual(self.runs.job_action("alpha-deal", "austin", {"action": "extract"})["jobs"][0]["state"], "queued")

    # ---- HTTP ------------------------------------------------------------------------------

    def test_routes_and_write_guards(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent / "cockpit/acceptance"))
        from test_http import HttpFixture
        http = HttpFixture(self.root)
        try:
            self.assertEqual([r["deal"] for r in http.get("/api/seed?q=beta").json()["rows"]], ["beta-holdings"])
            self.assertEqual(http.post("/api/deals", {"action": "lookup", "url": INDEX}, csrf="wrong").status_code, 403)
            self.assertEqual(http.post("/api/deals", {"action": "lookup", "url": "https://example.com/x"}).status_code, 400)
            lookup = http.post("/api/deals", {"action": "lookup", "url": INDEX, "seed_deal": "beta-holdings"}).json()["lookup"]
            self.assertEqual(lookup["state"], "queued")
            self.settle(lambda: http.get(f"/api/lookup/{lookup['id']}").json()["state"] == "completed")
            self.assertEqual(http.get("/api/lookup/" + "0" * 32).status_code, 404)
            added = http.post("/api/deals", {"action": "add", "lookup_id": lookup["id"], "document": "beta-proxy.htm", "slug": "beta-holdings", "name": "Beta"})
            self.assertEqual((added.status_code, added.json()), (200, {"slug": "beta-holdings"}))
            self.assertTrue(http.get("/api/deal/beta-holdings").json()["pending"])
            self.assertEqual(http.get("/api/deal/beta-holdings/export").status_code, 409)
        finally:
            http.close()


if __name__ == "__main__":
    unittest.main()
