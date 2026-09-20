"""Local-only filing integrity checks; all download operations are mocked."""

import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import fetch_filing


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


if __name__ == "__main__":
    unittest.main()
