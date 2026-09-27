"""Local-only filing integrity checks; all download operations are mocked."""

import hashlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import fetch_filing


def document_block(form_type, filename, body):
    return (
        b"<DOCUMENT>\n<TYPE>" + form_type.encode("ascii")
        + b"\n<SEQUENCE>1\n<FILENAME>" + filename.encode("ascii")
        + b"\n<TEXT>\n<html>" + body + b"</html>\n</TEXT>\n</DOCUMENT>\n"
    )


class FilingSelectionTests(unittest.TestCase):
    INDEX_URL = "https://www.sec.gov/Archives/edgar/data/1/0000000001-20-000001-index.htm"
    SUBMISSION_URL = "https://www.sec.gov/Archives/edgar/data/1/0000000001-20-000001.txt"
    PROXY = document_block("DEFM14A", "proxy.htm", b"Proxy terms: \xc2\xa310 per share")
    COVER = document_block("SC TO-T", "cover.htm", b"Cover form only")
    OFFER = document_block("EX-99.(A)(1)(A)", "offer.htm", b"Offer terms")

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.raw = Path(temporary.name)
        for name, value in (("RAW", self.raw), ("MANIFEST", self.raw / "MANIFEST.csv")):
            patcher = mock.patch.object(fetch_filing, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = mock.patch.object(fetch_filing, "get")
        self.download = patcher.start()
        self.addCleanup(patcher.stop)

    def fetch_fixture(self, form_type, submission):
        self.download.return_value = submission
        seed = {"deal": "sample", "status": "ok", "form_type": form_type,
                "date_filed": "2020-01-10", "index_url": self.INDEX_URL}
        manifest = []
        fetch_filing.fetch(seed, manifest, False)
        return fetch_filing.read_csv(fetch_filing.MANIFEST)

    def verify_quietly(self, manifest):
        with mock.patch("sys.stdout", new_callable=io.StringIO) as output:
            result = fetch_filing.verify(manifest)
        return result, output.getvalue()

    def test_fetch_and_verify_preserve_proxy_and_tender_exhibit_bytes(self):
        for form_type, submission, expected, filename in (
            ("DEFM14A", self.PROXY + self.OFFER, self.PROXY, "proxy.htm"),
            ("SC TO-T", self.COVER + self.OFFER, self.OFFER, "offer.htm"),
        ):
            with self.subTest(form_type=form_type):
                self.download.reset_mock()
                manifest = self.fetch_fixture(form_type, submission)
                row = manifest[0]
                self.assertEqual((self.raw / row["file"]).read_bytes(), expected)
                self.assertEqual(row["document"], filename)
                self.assertEqual(row["form_type"], form_type)
                self.assertEqual(row["source_url"], self.SUBMISSION_URL)
                self.assertEqual(int(row["bytes"]), len(expected))
                self.assertEqual(row["sha256"], hashlib.sha256(expected).hexdigest())
                result, output = self.verify_quietly(manifest)
                self.assertEqual(result, 0)
                self.assertIn("ok", output)
                self.assertEqual(self.download.call_args_list,
                                 [mock.call(self.SUBMISSION_URL), mock.call(self.SUBMISSION_URL)])

    def test_verify_selects_recorded_filename_when_type_is_ambiguous(self):
        manifest = self.fetch_fixture("SC TO-T", self.COVER + self.OFFER)
        self.download.return_value += document_block("EX-99.(A)(1)(A)", "other.htm", b"Other exhibit")
        self.assertEqual(self.verify_quietly(manifest)[0], 0)
        with self.assertRaisesRegex(fetch_filing.FetchError, "found 2"):
            fetch_filing.main_document(self.INDEX_URL, "SC TO-T")

    def test_verify_rejects_missing_or_wrong_type_recorded_document(self):
        manifest = self.fetch_fixture("SC TO-T", self.COVER + self.OFFER)
        for filename in ("missing.htm", "cover.htm"):
            with self.subTest(filename=filename):
                manifest[0]["document"] = filename
                with self.assertRaisesRegex(fetch_filing.FetchError, "found 0"):
                    self.verify_quietly(manifest)

    def test_verify_legacy_manifest_without_document_uses_same_selection(self):
        for form_type, submission in (("DEFM14A", self.PROXY), ("SC TO-T", self.COVER + self.OFFER)):
            with self.subTest(form_type=form_type):
                manifest = self.fetch_fixture(form_type, submission)
                del manifest[0]["document"]
                self.assertEqual(self.verify_quietly(manifest)[0], 0)

    def test_missing_offer_exhibit_cannot_fall_back_to_cover(self):
        self.download.return_value = self.COVER
        with self.assertRaisesRegex(fetch_filing.FetchError, "found 0"):
            fetch_filing.main_document(self.INDEX_URL, "SC TO-T")

    def test_verify_reports_local_remote_and_missing_file_mismatches(self):
        manifest = self.fetch_fixture("SC TO-T", self.COVER + self.OFFER)
        path = self.raw / manifest[0]["file"]
        for change in ("local", "remote", "missing"):
            with self.subTest(change=change):
                path.write_bytes(self.OFFER)
                self.download.return_value = self.COVER + self.OFFER
                if change == "local":
                    path.write_bytes(b"Changed local filing")
                elif change == "remote":
                    self.download.return_value = self.COVER + self.OFFER.replace(b"Offer terms", b"Changed terms")
                else:
                    path.unlink()
                result, output = self.verify_quietly(manifest)
                self.assertEqual(result, 1)
                self.assertIn("MISMATCH", output)
                self.assertIn({"local": "local changed", "remote": "EDGAR changed",
                               "missing": "local missing"}[change], output)


class FilingIntegrityTests(unittest.TestCase):
    def test_existing_corrupted_filing_is_rejected_without_network(self):
        seed = {"deal": "sample", "status": "ok", "form_type": "DEFM14A", "date_filed": "2020-01-10"}
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp)
            path = raw / "sample_2020-01-10_DEFM14A.htm"
            original = b"Original filing"
            manifest = [{"file": path.name, "sha256": hashlib.sha256(original).hexdigest(), "bytes": len(original)}]
            path.write_bytes(original)
            with mock.patch.object(fetch_filing, "RAW", raw), mock.patch.object(fetch_filing, "main_document") as download:
                self.assertIn("hash verified", fetch_filing.fetch(seed, manifest, False))
                path.write_bytes(b"Changed filing")
                with self.assertRaisesRegex(fetch_filing.FetchError, "differs from its manifest"):
                    fetch_filing.fetch(seed, manifest, False)
                download.assert_not_called()

    def test_failed_atomic_replace_keeps_original_and_cleans_temporary_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "filing.htm"
            path.write_bytes(b"Original filing")
            with mock.patch.object(Path, "replace", side_effect=OSError("synthetic replace failure")):
                with self.assertRaises(OSError):
                    fetch_filing.atomic_write(path, b"New filing")
            self.assertEqual(path.read_bytes(), b"Original filing")
            self.assertEqual(list(path.parent.iterdir()), [path])


class SubmissionTests(unittest.TestCase):
    HEADER = (b"<SEC-DOCUMENT>0000000002-21-000009.txt : 20210303\n<SEC-HEADER>\nACCESSION NUMBER:\t\t0000000002-21-000009\n"
              b"CONFORMED SUBMISSION TYPE:\tSC TO-T\nFILED AS OF DATE:\t\t20210303\n\nSUBJECT COMPANY:\t\n\n\tCOMPANY DATA:\t\n"
              b"\t\tCOMPANY CONFORMED NAME:\t\t\tTarget Co, Inc.\n\nFILED BY:\t\t\n\n\tCOMPANY DATA:\t\n"
              b"\t\tCOMPANY CONFORMED NAME:\t\t\tBuyer Merger Sub\n</SEC-HEADER>\n")

    def test_links_resolve_to_the_complete_submission(self):
        base = "https://www.sec.gov/Archives/edgar/data/1635581/"
        for url, expected in (
            (base + "0001193125-18-110072-index.htm", (base + "0001193125-18-110072.txt", None)),
            (base + "000119312518110072/0001193125-18-110072-index.html", (base + "0001193125-18-110072.txt", None)),
            ("http://www.sec.gov/Archives/edgar/data/1635581/0001193125-18-110072.txt", (base + "0001193125-18-110072.txt", None)),
            (base + "000119312518110072/d527171ddefm14a.htm#toc", (base + "0001193125-18-110072.txt", "d527171ddefm14a.htm")),
        ):
            with self.subTest(url=url):
                self.assertEqual(fetch_filing.submission_link(url), expected)
        for url in ("https://example.com/x-index.htm", base + "../../secret", "https://www.sec.gov/cgi-bin/browse-edgar?CIK=1", ""):
            with self.subTest(url=url), self.assertRaises(fetch_filing.FetchError):
                fetch_filing.submission_link(url)

    def test_index_link_is_derived_from_the_complete_submission(self):
        base = "https://www.sec.gov/Archives/edgar/data/1635581/"
        for url in (base + "0001193125-18-110072.txt", base + "000119312518110072/0001193125-18-110072.txt"):
            with self.subTest(url=url):
                self.assertEqual(fetch_filing.index_link(url), base + "0001193125-18-110072-index.htm")
                self.assertEqual(fetch_filing.submission_link(fetch_filing.index_link(url)), (base + "0001193125-18-110072.txt", None))
        for url in (base + "0001193125-18-110072-index.htm", base + "000119312518110072/d527171ddefm14a.htm",
                    "https://example.invalid/0001193125-18-110072.txt", "http://www.sec.gov/Archives/edgar/data/1635581/0001193125-18-110072.txt", "", None):
            with self.subTest(url=url), self.assertRaises(fetch_filing.FetchError):
                fetch_filing.index_link(url)

    def test_parse_submission_lists_documents_and_finds_the_background(self):
        cover = document_block("SC TO-T", "cover.htm", b"Cover form")
        offer = document_block("EX-99.(A)(1)(A)", "offer.htm", b"<p>BACKGROUND OF</p><p>THE&nbsp;OFFER</p>")
        image = document_block("GRAPHIC", "logo.jpg", b"binary")
        submission = self.HEADER + cover + offer + image
        parsed = fetch_filing.parse_submission(submission)
        self.assertEqual({k: parsed[k] for k in ("form_type", "date_filed", "subject_company", "filer")},
                         {"form_type": "SC TO-T", "date_filed": "2021-03-03", "subject_company": "Target Co, Inc.", "filer": "Buyer Merger Sub"})
        self.assertEqual([(d["type"], d["filename"], d["html"], d["background"]) for d in parsed["documents"]],
                         [("SC TO-T", "cover.htm", True, False), ("EX-99.(A)(1)(A)", "offer.htm", True, True), ("GRAPHIC", "logo.jpg", False, False)])
        self.assertEqual(fetch_filing.default_document(parsed["documents"], "SC TO-T"), "offer.htm")
        self.assertIsNone(fetch_filing.default_document(parsed["documents"], "S-4"))
        self.assertEqual(fetch_filing.document_bytes(submission, "offer.htm"), offer)
        self.assertEqual(parsed["documents"][1]["bytes"], len(offer))
        with self.assertRaises(fetch_filing.FetchError):
            fetch_filing.document_bytes(submission, "missing.htm")


if __name__ == "__main__":
    unittest.main()
