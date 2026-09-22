"""Serve the synthetic fixture for the isolated Playwright acceptance run."""

from __future__ import annotations

import json
import os
import signal
import sys
import tempfile
from pathlib import Path

from test_http import HttpFixture, synthetic_repo


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
        signal.signal(signal.SIGTERM, lambda *_: fixture.httpd.shutdown())
        print(json.dumps({"url": fixture.base}), flush=True)
        try:
            fixture.thread.join()
        finally:
            fixture.close()


if __name__ == "__main__":
    main()
