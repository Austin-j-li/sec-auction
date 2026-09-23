"""Serve the synthetic fixture for the isolated Playwright acceptance run."""

from __future__ import annotations

import json
import os
import signal
import sys
import tempfile
import threading
from pathlib import Path

from test_http import HttpFixture, synthetic_repo


def start_fake_worker(root: Path) -> None:
    """Run the real worker loop against the fake runner and fake Claude CLI from the unit tests. No model is called."""
    import openpyxl
    from cockpit import worker
    from test_cockpit_runs import FAKE_CLAUDE, FAKE_RUNNER

    (root / "fake_runner.py").write_text(FAKE_RUNNER)
    (root / "fake_claude.py").write_text(FAKE_CLAUDE)
    claude = root / "claude"
    claude.write_text(f"#!/bin/sh\nexec {sys.executable} {root / 'fake_claude.py'}\n")
    claude.chmod(0o755)
    # The fake run returns the fixture workbook with one bidder renamed, so Compare has a difference to show.
    workbook = openpyxl.load_workbook(root / "extraction/synthetic.xlsx")
    workbook["Deal ledger"]["C3"] = "Party A (new run)"
    workbook.save(root / "fake_run.xlsx")
    os.environ.update({"COCKPIT_TOKEN_ROOT": str(root / "tokens"), "FAKE_WORKBOOK": str(root / "fake_run.xlsx")})
    worker.RUNNER, worker.CLAUDE = root / "fake_runner.py", str(claude)
    loop = worker.Worker(root)

    def forever() -> None:
        while True:
            try:
                loop.tick()
            except Exception as exc:  # noqa: BLE001
                print(f"fake worker: {exc}", file=sys.stderr, flush=True)
            threading.Event().wait(0.3)

    threading.Thread(target=forever, daemon=True).start()


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="cockpit-browser-") as folder:
        root = Path(folder)
        actual_catalog = "--actual-catalog-readonly" in sys.argv[1:]
        if actual_catalog:
            root = Path(__file__).resolve().parents[4]
            os.environ["COCKPIT_REQUIRE_ACCESS"] = "1"
        else:
            synthetic_repo(root)
        fixture = HttpFixture(root)
        if "--two-users" in sys.argv[1:]:
            # Identities come from the Cloudflare Access email header, as on the public route.
            os.environ["COCKPIT_REQUIRE_ACCESS"] = "1"
            os.environ["COCKPIT_PUBLIC_ORIGIN"] = fixture.base
        if "--runs" in sys.argv[1:]:
            start_fake_worker(root)
        signal.signal(signal.SIGTERM, lambda *_: fixture.httpd.shutdown())
        print(json.dumps({"url": fixture.base}), flush=True)
        try:
            fixture.thread.join()
        finally:
            fixture.close()


if __name__ == "__main__":
    main()
