#!/usr/bin/env python3
"""Loopback HTTP service for the editable ledger cockpit."""
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import secrets
import sys
import threading
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse, parse_qs

HERE = Path(__file__).resolve().parent
TOOLS_DIR = HERE.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))
from cockpit import access, data  # noqa: E402
from cockpit import provenance  # noqa: E402
from cockpit.workspace import WorkspaceError  # noqa: E402

DEFAULT_PORT = 8778
READER_EMAILS = {"junyu.li.24@ucl.ac.uk": "austin", "a.gorbenko@ucl.ac.uk": "alex"}
SLUG_PATH_RE = re.compile(r"/api/(deal|filing)/([^/]*)")
DEAL_ACTION_RE = re.compile(r"/api/deal/([^/]*)/(history|changes|export|edit|comments|activity|seen|jobs|versions|compare|review|rebase)")
DOCUMENT_RE = re.compile(r"/api/document/([^/]*)/([^/]*)")
LOOKUP_RE = re.compile(r"/api/lookup/([0-9a-f]{32})")
DEAL_VISIBILITY_RE = re.compile(r"/api/deals/([^/]*)/visibility")
INSTRUCTION_RE = re.compile(r"/api/instructions/([0-9a-f]{12})")
PAGE_PATH_RE = re.compile(r"/deal/[^/]*/?|/activity/?|/settings/?|/instructions/?")
MAX_JSON = 1024 * 1024


class Handler(BaseHTTPRequestHandler):
    cockpit: data.Cockpit = data.default()
    access_verifier = access.Verifier()  # shared by all servers in the process; tests replace it per server
    server_version = "LedgerCockpit/2"
    quiet = False
    csrf_token = secrets.token_urlsafe(32)

    def log_message(self, fmt: str, *args: Any) -> None:
        if not self.quiet:
            sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))

    def __getattr__(self, name: str) -> Any:
        if name.startswith("do_") and name not in ("do_GET", "do_POST"):
            return self._not_allowed
        raise AttributeError(name)

    def send_error(self, code: int, message: str | None = None, explain: str | None = None) -> None:
        self.close_connection = True
        body = json.dumps({"error": message or self.responses.get(code, ("error",))[0]}).encode()
        self._send(body, "application/json; charset=utf-8", code, Connection="close")

    def _send(self, body: bytes, content_type: str, status: int = 200, **headers: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        for name, value in headers.items(): self.send_header(name.replace("_", "-"), value)
        self.end_headers()
        if self.command != "HEAD": self.wfile.write(body)

    def _json(self, value: Any, status: int = 200) -> None:
        self._send(json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode(), "application/json; charset=utf-8", status)

    def _identity(self) -> tuple[str, bool]:
        """(reader, may edit). On the public host the reader comes only from a verified Cloudflare Access token
        (access.py); the plain email header, which any local process can forge, is ignored."""
        host = (self.headers.get("Host") or "").lower()
        local_hosts = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
        if host in local_hosts and self.client_address[0] in ("127.0.0.1", "::1") and os.environ.get("COCKPIT_REQUIRE_ACCESS") != "1":
            proxied = self.headers.get("Cf-Access-Jwt-Assertion") or self.headers.get("Cf-Access-Authenticated-User-Email")
            return ("local", not proxied)
        expected = os.environ.get("COCKPIT_PUBLIC_ORIGIN", "").rstrip("/").lower()
        if not expected or host != urlparse(expected).netloc.lower():
            return ("unknown", False)
        actor = READER_EMAILS.get(self.access_verifier.email(self.headers.get("Cf-Access-Jwt-Assertion")) or "")
        return (actor or "unknown", actor is not None)

    def _origin_ok(self) -> bool:
        origin = self.headers.get("Origin")
        if not origin or origin == "null": return False
        parsed = urlparse(origin)
        if parsed.scheme not in ("http", "https") or parsed.path not in ("", "/") or parsed.query or parsed.fragment or parsed.username or parsed.password: return False
        host = (self.headers.get("Host") or "").lower()
        local = host == f"127.0.0.1:{self.server.server_port}" or host == f"localhost:{self.server.server_port}"
        if local:
            return origin.lower() == f"http://{host}"
        expected = os.environ.get("COCKPIT_PUBLIC_ORIGIN", "").rstrip("/").lower()
        return bool(expected and origin.lower() == expected and parsed.netloc.lower() == host)

    def do_GET(self) -> None:
        try: self._route_get()
        except (BrokenPipeError, ConnectionResetError): pass

    def _route_get(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        try:
            if path == "/api/session":
                actor, can_edit = self._identity()
                return self._json({"user": actor, "can_edit": can_edit, "csrf_token": self.csrf_token if can_edit else None})
            if path == "/api/deals":
                actor, _ = self._identity()
                deals = self.cockpit.list_deals()
                if self.cockpit.workspace.available and actor != "unknown":
                    for deal in deals: deal["unseen"] = self.cockpit.trace.unseen(deal["slug"], actor)
                if self.cockpit.workspace.available:
                    for deal in deals: deal["active_jobs"] = self.cockpit.runs.active_jobs(deal["slug"])
                    for deal in deals:
                        if not deal.get("pending"): deal["deal_review"] = self.cockpit.trace.deal_review(deal["slug"])
                return self._json(deals)
            if path == "/api/account":
                actor, _ = self._identity()
                if actor == "unknown": return self._json({"user": actor, "claude": {"connected": False}, "connect": None, "chatgpt": {"connected": False}, "chatgpt_connect": None, "engines": []})
                return self._json(self.cockpit.runs.account(actor))
            if path == "/api/instructions":
                if not self.cockpit.workspace.available: return self._json({"error": "workspace unavailable"}, 404)
                return self._json(self.cockpit.instructions.list())
            match = INSTRUCTION_RE.fullmatch(path)
            if match:
                if not self.cockpit.workspace.available: return self._json({"error": "workspace unavailable"}, 404)
                seq = (query.get("seq") or [None])[0]
                if seq is not None and not seq.isdigit(): return self._json({"error": "invalid seq"}, 400)
                return self._json(self.cockpit.instructions.detail(match.group(1), int(seq) if seq else None))
            if path == "/api/seed":
                if not self.cockpit.workspace.available: return self._json({"error": "workspace unavailable"}, 404)
                return self._json(self.cockpit.deals.seed_search((query.get("q") or [""])[0][:100]))
            match = LOOKUP_RE.fullmatch(path)
            if match:
                if not self.cockpit.workspace.available: return self._json({"error": "workspace unavailable"}, 404)
                return self._json(self.cockpit.deals.lookup(match.group(1)))
            if path == "/api/activity":
                if not self.cockpit.workspace.available: return self._json({"error": "workspace unavailable"}, 404)
                actor, _ = self._identity()
                one = lambda key: (query.get(key) or [None])[0] or None
                try: before, limit = (int(one("before")) if one("before") else None), int(one("limit") or 100)
                except ValueError: return self._json({"error": "invalid paging"}, 400)
                if before is not None and not 0 <= before < 2**63: return self._json({"error": "invalid paging"}, 400)
                return self._json(self.cockpit.trace.activity(actor, one("slug"), actor=one("actor"), kind=one("kind"), before=before, limit=limit, account=True))
            match = SLUG_PATH_RE.fullmatch(path)
            if match:
                kind, slug = match.group(1), unquote(match.group(2))
                if kind == "deal":
                    version = query.get("version", ["working"])[0]
                    payload = self.cockpit.deal(slug, version=version)
                    actor, _ = self._identity()
                    if self.cockpit.workspace.available: payload.update(self._deal_extras(slug, actor, version))
                    return self._json({**payload, "reader": actor})
                return self._json(self.cockpit.filing_payload(slug))
            match = DEAL_ACTION_RE.fullmatch(path)
            if match:
                slug, action = unquote(match.group(1)), match.group(2)
                if not self.cockpit.workspace.available: return self._json({"error": "workspace unavailable"}, 404)
                if action == "history": return self._json(self.cockpit.workspace.history(slug))
                if action == "changes": return self._json(self.cockpit.workspace.changes(slug))
                if action in ("edit", "seen", "versions"): return self._not_allowed()
                if action == "jobs": return self._json(self.cockpit.runs.jobs(slug))
                if action == "compare":
                    workspace = self.cockpit.workspace
                    left, right = (query.get("from") or ["base"])[0], (query.get("to") or ["working"])[0]
                    if left == "base": left = workspace.working_base(slug, workspace.item(slug))["id"]
                    return self._json(workspace.compare(slug, left, right))
                if action == "comments": return self._json(self.cockpit.trace.comments(slug))
                if action == "review": return self._json({"deal_review": self.cockpit.trace.deal_review(slug)})
                if action == "rebase": return self._json(self.cockpit.workspace.rebase_preview(slug, (query.get("to") or [""])[0]))
                if action == "activity":
                    actor, _ = self._identity()
                    try: limit = int(query.get("limit", ["200"])[0])
                    except ValueError: return self._json({"error": "invalid limit"}, 400)
                    return self._json(self.cockpit.trace.activity(actor, slug, limit=limit))
                version = query.get("version", ["working"])[0]
                source = (query.get("source") or [""])[0]  # "0": the working copy's (or a past revision's) four sheets; "1": a version with the Source sheet
                if source not in ("", "0", "1"): return self._json({"error": "invalid source"}, 400)
                content, name = provenance.download(self.cockpit, slug, version, source == "1" if source else None)
                return self._send(content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", Content_Disposition=f'attachment; filename="{name}"')
            if DEAL_VISIBILITY_RE.fullmatch(path): return self._not_allowed()
            match = DOCUMENT_RE.fullmatch(path)
            if match:
                if not self.cockpit.workspace.available: return self._json({"error": "workspace unavailable"}, 404)
                return self._json(self.cockpit.workspace.document(unquote(match.group(1)), unquote(match.group(2))))
            if path.startswith("/api/"): return self._json({"error": "not found"}, 404)
            if path.startswith("/assets/"):
                relative = unquote(path.removeprefix("/assets/"))
                dist = HERE / "dist" / "assets"
                file = (dist / relative).resolve()
                if dist.resolve() not in file.parents or not file.is_file(): return self._json({"error": "not found"}, 404)
                return self._send(file.read_bytes(), mimetypes.guess_type(file.name)[0] or "application/octet-stream")
            if path in ("/", "/index.html") or PAGE_PATH_RE.fullmatch(path):
                index = HERE / "dist/index.html"
                if not index.is_file(): return self._json({"error": "frontend not built: _dev/tools/cockpit/dist/index.html is missing"}, 503)
                return self._send(index.read_bytes(), "text/html; charset=utf-8")
            return self._json({"error": "not found"}, 404)
        except data.DealNotFound as exc: return self._json({"error": str(exc)}, 404)
        except data.DealUnavailable as exc: return self._json({"error": str(exc)}, 409)
        except WorkspaceError as exc: return self._json({"error": str(exc)}, exc.status)
        except (BrokenPipeError, ConnectionResetError): raise
        except Exception as exc:
            traceback.print_exc(file=sys.stderr)
            return self._json({"error": f"internal error ({type(exc).__name__}); see the server log"}, 500)

    def do_POST(self) -> None:
        try:
            self._route_post()
        except (BrokenPipeError, ConnectionResetError): pass

    def _route_post(self) -> None:
        path = urlparse(self.path).path
        match = DEAL_ACTION_RE.fullmatch(path)
        visibility = DEAL_VISIBILITY_RE.fullmatch(path)
        if path not in ("/api/account/claude", "/api/account/chatgpt", "/api/deals", "/api/instructions") and not visibility and (not match or match.group(2) not in ("edit", "comments", "seen", "jobs", "versions", "review")): return self._not_allowed()
        if not self.cockpit.workspace.available: return self._json({"error": "workspace unavailable"}, 404)
        actor, can_edit = self._identity()
        if not can_edit or not self._origin_ok() or not secrets.compare_digest(self.headers.get("X-Cockpit-CSRF") or "", self.csrf_token):
            return self._json({"error": "write authorization failed"}, 403)
        if self.headers.get_content_type() != "application/json": return self._json({"error": "JSON content type required"}, 415)
        try: length = int(self.headers.get("Content-Length") or "")
        except ValueError: return self._json({"error": "content length required"}, 411)
        if length <= 0 or length > MAX_JSON: return self._json({"error": "request body size out of range"}, 413)
        try:
            body = json.loads(self.rfile.read(length))
            if path == "/api/deals": return self._json(self.cockpit.deals.request(actor, body))
            if path == "/api/instructions": return self._json(self.cockpit.instructions.request(actor, body))
            if path == "/api/account/chatgpt": return self._json(self.cockpit.runs.chatgpt_action(actor, body))
            if visibility: return self._json(self.cockpit.deals.visibility(unquote(visibility.group(1)), actor, body))
            if match is None: return self._json(self.cockpit.runs.account_action(actor, body))
            slug, action = unquote(match.group(1)), match.group(2)
            if action == "jobs": return self._json(self.cockpit.runs.job_action(slug, actor, body))
            if action == "versions": return self._json(self.cockpit.runs.version_action(slug, actor, body))
            if action == "comments": return self._json(self.cockpit.trace.comment(slug, body, actor))
            if action == "seen": return self._json(self.cockpit.trace.mark_seen(slug, body, actor))
            if action == "review": return self._json(self.cockpit.trace.set_deal_review(slug, body, actor))
            payload = self.cockpit.workspace.edit(slug, body, actor)
            payload.update(self._deal_extras(slug, actor))
            return self._json({**payload, "reader": actor})
        except (UnicodeDecodeError, json.JSONDecodeError): return self._json({"error": "invalid JSON"}, 400)
        except data.DealNotFound as exc: return self._json({"error": str(exc)}, 404)
        except WorkspaceError as exc: return self._json({"error": str(exc)}, exc.status)
        except Exception as exc:
            traceback.print_exc(file=sys.stderr)
            return self._json({"error": f"internal error ({type(exc).__name__}); see the server log"}, 500)

    def _deal_extras(self, slug: str, actor: str, version: str = "working") -> dict[str, Any]:
        """Additions to a deal payload: trace extras plus whether the deal is hidden (and by whom, when)."""
        return {**self.cockpit.trace.deal_extras(slug, actor, version), **self.cockpit.deals.visibility_of(slug)}

    def _not_allowed(self) -> None:
        return self._json({"error": "method not allowed"}, 405)


def make_server(port: int, cockpit: data.Cockpit | None = None, quiet: bool = False) -> ThreadingHTTPServer:
    handler = Handler
    if cockpit is not None or quiet:
        handler = type("BoundHandler", (Handler,), {"cockpit": cockpit or Handler.cockpit, "quiet": quiet, "csrf_token": secrets.token_urlsafe(32)})
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    server.daemon_threads = True
    return server


def _warm(cockpit: data.Cockpit) -> None:
    try: cockpit.list_deals()
    except Exception as exc: sys.stderr.write(f"cockpit warm-up failed: {type(exc).__name__}: {exc}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Editable ledger review cockpit")
    parser.add_argument("--port", type=int, default=int(os.environ.get("COCKPIT_PORT") or DEFAULT_PORT))
    parser.add_argument("--repo-root", type=Path, default=data.REPO_ROOT, help="repository root (fixture/testing)")
    parser.add_argument("--no-warm", action="store_true")
    args = parser.parse_args(argv)
    cockpit = data.Cockpit(args.repo_root)
    if os.environ.get("COCKPIT_PUBLIC_ORIGIN") and not access.configured():
        print(f"warning: COCKPIT_PUBLIC_ORIGIN is set but {access.TEAM_ENV} and {access.AUD_ENV} are not (or jwcrypto is missing); "
              "nobody can sign in on the public site, so it is read-only", file=sys.stderr, flush=True)
    httpd = make_server(args.port, cockpit)
    if not args.no_warm: threading.Thread(target=_warm, args=(cockpit,), daemon=True).start()
    print(f"ledger cockpit -> http://127.0.0.1:{args.port}", flush=True)
    try: httpd.serve_forever()
    except KeyboardInterrupt: pass
    finally: httpd.server_close()
    return 0

if __name__ == "__main__": raise SystemExit(main())
