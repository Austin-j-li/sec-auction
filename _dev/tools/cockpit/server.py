#!/usr/bin/env python3
"""Local read-only HTTP server for the ledger review cockpit.

Run from the repository root:

    python3 _dev/tools/cockpit/server.py [--port N]

The port defaults to $COCKPIT_PORT, else 8778. The server binds 127.0.0.1,
answers GET only, makes no outbound calls and writes nothing.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

HERE = Path(__file__).resolve().parent
TOOLS_DIR = HERE.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from cockpit import data  # noqa: E402

DEFAULT_PORT = 8778
READER_EMAILS = {
    "junyu.li.24@ucl.ac.uk": "austin",
    "a.gorbenko@ucl.ac.uk": "alex",
}
DEFAULT_READER = "austin"
STATIC_FILES = {
    "app.js": "text/javascript; charset=utf-8",
    "style.css": "text/css; charset=utf-8",
    "index.html": "text/html; charset=utf-8",
}
SLUG_PATH_RE = re.compile(r"/api/(deal|filing)/([^/]*)")
PAGE_PATH_RE = re.compile(r"/deal/[^/]*/?")


def reader_for(email: str | None) -> str:
    return READER_EMAILS.get((email or "").strip().lower(), DEFAULT_READER)


class Handler(BaseHTTPRequestHandler):
    cockpit: data.Cockpit = data.default()
    server_version = "LedgerCockpit/1"
    quiet = False

    def log_message(self, fmt: str, *args: Any) -> None:
        if not self.quiet:
            sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))

    def __getattr__(self, name: str) -> Any:
        # Any method other than GET (TRACE, CONNECT, PROPFIND, ...) is refused
        # with the same JSON 405 instead of the library's HTML 501 page.
        if name.startswith("do_") and name != "do_GET":
            return self._not_allowed
        raise AttributeError(name)

    def send_error(self, code: int, message: str | None = None, explain: str | None = None) -> None:
        """Protocol errors (bad request line, oversized header) as JSON, never cached."""

        self.close_connection = True
        short = self.responses.get(code, ("error",))[0]
        body = json.dumps({"error": message or short}).encode("utf-8")
        self._send(body, "application/json; charset=utf-8", code, Connection="close")

    def _send(self, body: bytes, content_type: str, status: int = 200, **headers: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        for name, value in headers.items():
            self.send_header(name.replace("_", "-"), value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, value: Any, status: int = 200) -> None:
        body = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self._send(body, "application/json; charset=utf-8", status)

    def do_GET(self) -> None:
        try:
            self._route()
        except (BrokenPipeError, ConnectionResetError):
            pass  # the client went away mid-response; nothing left to send

    def _route(self) -> None:
        path = urlparse(self.path).path
        try:
            if path == "/api/deals":
                return self._json(self.cockpit.list_deals())
            match = SLUG_PATH_RE.fullmatch(path)
            if match:
                kind, slug = match.group(1), unquote(match.group(2))
                if kind == "deal":
                    payload = self.cockpit.deal(slug)
                    reader = reader_for(self.headers.get("Cf-Access-Authenticated-User-Email"))
                    return self._json({**payload, "reader": reader})
                return self._json(self.cockpit.filing_payload(slug))
            if path.startswith("/api/"):
                return self._json({"error": "not found"}, 404)
            if path.startswith("/static/"):
                name = path.removeprefix("/static/")
                file = HERE / name
                if name not in STATIC_FILES or not file.is_file():
                    return self._json({"error": "not found"}, 404)
                return self._send(file.read_bytes(), STATIC_FILES[name])
            if path in ("/", "/index.html") or PAGE_PATH_RE.fullmatch(path):
                return self._send((HERE / "index.html").read_bytes(), STATIC_FILES["index.html"])
            return self._json({"error": "not found"}, 404)
        except data.DealNotFound as exc:
            return self._json({"error": str(exc)}, 404)
        except data.DealUnavailable as exc:
            return self._json({"error": str(exc)}, 409)
        except (BrokenPipeError, ConnectionResetError):
            raise
        except Exception as exc:  # report, never crash the server thread
            # The full error (with paths) goes to the server log only.
            traceback.print_exc(file=sys.stderr)
            return self._json({"error": f"internal error ({type(exc).__name__}); see the server log"}, 500)

    def _not_allowed(self) -> None:
        body = json.dumps({"error": "method not allowed; the cockpit is read-only"}).encode("utf-8")
        self._send(body, "application/json; charset=utf-8", 405, Allow="GET")


def make_server(port: int, cockpit: data.Cockpit | None = None, quiet: bool = False) -> ThreadingHTTPServer:
    handler = Handler
    if cockpit is not None or quiet:
        handler = type("BoundHandler", (Handler,), {"cockpit": cockpit or Handler.cockpit, "quiet": quiet})
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    server.daemon_threads = True
    return server


def _warm(cockpit: data.Cockpit) -> None:
    try:
        cockpit.list_deals()
    except Exception as exc:  # warming is best effort
        sys.stderr.write(f"cockpit warm-up failed: {type(exc).__name__}: {exc}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only ledger review cockpit")
    parser.add_argument("--port", type=int, default=int(os.environ.get("COCKPIT_PORT") or DEFAULT_PORT))
    parser.add_argument("--no-warm", action="store_true", help="skip parsing every deal at start-up")
    args = parser.parse_args(argv)
    cockpit = data.default()
    httpd = make_server(args.port, cockpit)
    if not args.no_warm:
        threading.Thread(target=_warm, args=(cockpit,), daemon=True).start()
    print(f"ledger cockpit (read-only) -> http://127.0.0.1:{args.port}", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
