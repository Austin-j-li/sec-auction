"""A synthetic root for the S2/MIG-C UI smoke test: the fixture deal, a v1.14 run version, a reviewed revision,
a finding decision and a row thread. Local identity only; temporary root under TMPDIR."""
import json, os, signal, sys, tempfile
from pathlib import Path
TREE = Path("/home/uctpiaj/work/tmp/v114-scratch/tmp/s2/browser-tree/_dev/tools")
sys.path.insert(0, str(TREE)); sys.path.insert(0, str(TREE / "cockpit/acceptance"))
from test_http import HttpFixture, synthetic_repo, add_v114_version, deal, save, row  # noqa: E402

with tempfile.TemporaryDirectory(prefix="s2-ui-") as folder:
    root = Path(folder)
    os.environ["COCKPIT_TOKEN_ROOT"] = str(root / "tokens")
    synthetic_repo(root)
    http = HttpFixture(root)
    ident, _, _ = add_v114_version(http)
    initial = deal(http)
    first = row(initial, "Deal ledger")["uid"]
    assert save(http, initial, [{"type": "update", "sheet": "Deal ledger", "uid": first, "values": {"Note": "Reviewed wording"}},
                                {"type": "review", "uid": first, "status": "reviewed"},
                                {"type": "finding", "id": "F1", "judgment": "supported", "implementation": "applied", "verification": "verified", "note": ""}], "Review pass").status_code == 200
    assert http.post("/api/deal/synthetic/comments", {"action": "create", "target": {"kind": "row", "sheet": "Deal ledger", "uid": first}, "body": "Check the page"}).status_code == 200
    assert http.post("/api/account/claude", {"action": "token", "token": "sk-ant-oat01-" + "A" * 40}).status_code == 200
    signal.signal(signal.SIGTERM, lambda *_: http.httpd.shutdown())
    print(json.dumps({"url": http.base, "version": ident}), flush=True)
    try: http.thread.join()
    finally: http.close()
