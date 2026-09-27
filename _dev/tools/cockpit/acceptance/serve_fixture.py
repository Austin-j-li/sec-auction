"""Serve the synthetic fixture for the isolated Playwright acceptance run."""

from __future__ import annotations

import json
import os
import signal
import sys
import tempfile
import threading
from pathlib import Path

from test_http import HttpFixture, add_pending_catalog_deal, synthetic_repo


def start_fake_worker(root: Path) -> None:
    """Run the real worker loop against the fake runner, Claude CLI and Codex CLI from the unit tests. No model is called.

    The fake Codex sign-in waits until `<root>/codex-flag` holds "approve" (or anything else, to fail).
    """
    import openpyxl
    from cockpit import worker
    from test_cockpit_phase4 import FAKE_CODEX
    from test_cockpit_runs import FAKE_CLAUDE, FAKE_RUNNER

    (root / "fake_runner.py").write_text(FAKE_RUNNER)
    (root / "fake_claude.py").write_text(FAKE_CLAUDE)
    claude = root / "claude"
    claude.write_text(f"#!/bin/sh\nexec {sys.executable} {root / 'fake_claude.py'}\n")
    claude.chmod(0o755)
    (root / "fake_codex.py").write_text(FAKE_CODEX)
    codex = root / "codex"
    codex.write_text(f"#!/bin/sh\nexport FAKE_CODEX_FLAG={root / 'codex-flag'} FAKE_CODEX_CALLS={root / 'codex-calls'}\nexec {sys.executable} {root / 'fake_codex.py'} \"$@\"\n")
    codex.chmod(0o755)
    # The fake run returns the fixture workbook with one bidder renamed, so Compare has a difference to show.
    workbook = openpyxl.load_workbook(root / "extraction/synthetic.xlsx")
    workbook["Deal ledger"]["C3"] = "Party A (new run)"
    workbook.save(root / "fake_run.xlsx")
    os.environ.update({"COCKPIT_TOKEN_ROOT": str(root / "tokens"), "FAKE_WORKBOOK": str(root / "fake_run.xlsx")})
    worker.RUNNER, worker.CLAUDE, worker.CODEX = root / "fake_runner.py", str(claude), str(codex)
    loop = worker.Worker(root)

    def forever() -> None:
        while True:
            try:
                loop.tick()
            except Exception as exc:  # noqa: BLE001
                print(f"fake worker: {exc}", file=sys.stderr, flush=True)
            threading.Event().wait(0.3)

    threading.Thread(target=forever, daemon=True).start()


SEED_INDEX = "https://www.sec.gov/Archives/edgar/data/77/0000000077-21-000001-index.htm"
PASTED_INDEX = "https://www.sec.gov/Archives/edgar/data/88/0000000088-22-000002-index.htm"


def stub_edgar(root: Path) -> None:
    """A two-row seed and a stubbed EDGAR, so adding deals needs no network."""
    import csv
    import fetch_filing

    def document(kind: str, name: str, body: str) -> bytes:
        return f"<DOCUMENT>\n<TYPE>{kind}\n<SEQUENCE>1\n<FILENAME>{name}\n<DESCRIPTION>{kind}\n<TEXT>\n<html><body>{body}</body></html>\n</TEXT>\n</DOCUMENT>\n".encode()

    story = "".join(f"<p>Delta filler paragraph {n}.</p>" for n in range(30))
    submissions = {
        SEED_INDEX.replace("-index.htm", ".txt"): b"<SEC-HEADER>\nCONFORMED SUBMISSION TYPE:\tDEFM14A\nFILED AS OF DATE:\t\t20210305\n\nFILER:\n\n\tCOMPANY DATA:\t\n\t\tCOMPANY CONFORMED NAME:\t\t\tDELTA SYSTEMS INC\n</SEC-HEADER>\n"
            + document("DEFM14A", "delta-proxy.htm", "<h1>Background of the Merger</h1><p>1</p><p>Delta met three bidders.</p>" + story)
            + document("EX-99.1", "delta-letter.htm", "<p>A letter</p>"),
        PASTED_INDEX.replace("-index.htm", ".txt"): b"<SEC-HEADER>\nCONFORMED SUBMISSION TYPE:\tSC TO-T\nFILED AS OF DATE:\t\t20220107\n\nSUBJECT COMPANY:\n\n\tCOMPANY DATA:\t\n\t\tCOMPANY CONFORMED NAME:\t\t\tEcho Labs, Inc.\n\nFILED BY:\n\n\tCOMPANY DATA:\t\n\t\tCOMPANY CONFORMED NAME:\t\t\tFoxtrot Merger Sub\n</SEC-HEADER>\n"
            + document("SC TO-T", "echo-cover.htm", "<p>Cover form</p>")
            + document("EX-99.(A)(1)(A)", "echo-offer.htm", "<h1>Background of the Offer</h1><p>Echo received an offer.</p>" + story),
    }

    def get(url: str) -> bytes:
        if url not in submissions:
            raise fetch_filing.FetchError(f"{url}: HTTP Error 404: Not Found")
        return submissions[url]

    fetch_filing.get = get
    (root / "ref").mkdir(exist_ok=True)
    with (root / "ref/seed.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["deal", "target_name", "deal_number", "form_type", "date_filed", "index_url", "status"])
        writer.writerow(["delta-systems", "DELTA SYSTEMS INC", "1", "DEFM14A", "2021-03-05", SEED_INDEX, "ok"])
        writer.writerow(["kilo", "KILO CORP", "2", "DEFM14A", "2020-02-02", "", "review: 0 usable of 1 links"])


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="cockpit-browser-") as folder:
        root = Path(folder)
        actual_catalog = "--actual-catalog-readonly" in sys.argv[1:]
        if actual_catalog:
            root = Path(__file__).resolve().parents[4]
            os.environ["COCKPIT_REQUIRE_ACCESS"] = "1"
        else:
            synthetic_repo(root)
            if "--catalog-pending" in sys.argv[1:]:
                add_pending_catalog_deal(root)
        fixture = HttpFixture(root)
        if "--two-users" in sys.argv[1:]:
            # Identities come from the Cloudflare Access email header, as on the public route.
            os.environ["COCKPIT_REQUIRE_ACCESS"] = "1"
            os.environ["COCKPIT_PUBLIC_ORIGIN"] = fixture.base
        if "--deals" in sys.argv[1:]:
            stub_edgar(root)
        if "--runs" in sys.argv[1:]:
            start_fake_worker(root)
        signal.signal(signal.SIGTERM, lambda *_: fixture.httpd.shutdown())
        print(json.dumps({"url": fixture.base, "root": str(root)}), flush=True)
        try:
            fixture.thread.join()
        finally:
            fixture.close()


if __name__ == "__main__":
    main()
