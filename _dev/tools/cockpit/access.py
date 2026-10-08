"""Who is signed in on the public route: the email in a verified Cloudflare Access token.

Cloudflare Access adds a signed token (a JWT) in the `Cf-Access-Jwt-Assertion` header to every request it lets
through to the app. The server takes a reader's email only from a token that verifies: RS256, signed by a key in
the team's published key set, issued by the team domain, for this app's audience tag and not expired. The plain
`Cf-Access-Authenticated-User-Email` header is never trusted, because any local process can send it.

Configuration, in the environment of ledger-cockpit.service (SWITCHOVER.md, "Point services at the approved
deployment"):

    COCKPIT_ACCESS_TEAM_DOMAIN  the Zero Trust team domain, https://<team>.cloudflareaccess.com
    COCKPIT_ACCESS_AUD          the Access application's Application Audience (AUD) tag

Without both, no public request is signed in: the site stays readable through Access, and nobody can edit.
Both are read once, when the verifier is made (at server start). jwcrypto checks the signature and the iss, aud,
exp and nbf claims, with a minute of clock skew allowed. The key set is fetched from
`<team domain>/cdn-cgi/access/certs` on first use and kept; a token whose key id the cached set lacks (as after
Cloudflare rotates its keys) prompts a new fetch. Fetches, including failed ones, happen at most once a minute.
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
import urllib.request
from time import time as wall_clock  # token times are wall-clock times, kept apart from the monotonic clock
from typing import Any, Callable

try:
    from jwcrypto import jwk, jwt
except ImportError:  # the VM's python3-jwcrypto package provides it; without it nobody is signed in
    jwk = jwt = None

TEAM_ENV = "COCKPIT_ACCESS_TEAM_DOMAIN"
AUD_ENV = "COCKPIT_ACCESS_AUD"
RETRY_AFTER = 60
FETCH_TIMEOUT = 5
LEEWAY = 60  # seconds of clock skew allowed on exp and nbf


def settings() -> tuple[str, str] | None:
    """(issuer, audience) from the environment, or None when verification is not configured."""
    team = os.environ.get(TEAM_ENV, "").strip().rstrip("/")
    audience = os.environ.get(AUD_ENV, "").strip()
    team = team if "://" in team else "https://" + team
    if not audience or not team.startswith("https://") or team == "https://":
        return None  # the key set is fetched from the team domain, so only over https
    return team, audience


def fetch_keys(url: str) -> str:
    with urllib.request.urlopen(url, timeout=FETCH_TIMEOUT) as response:  # noqa: S310 - https URL from configuration
        return response.read(1 << 20).decode("utf-8")


class Verifier:
    """Verifies Access tokens against the team's key set, which it caches. Shared by the request threads."""

    def __init__(self, fetch: Callable[[str], str] = fetch_keys):
        self.fetch = fetch
        self.settings = settings()
        self.configured = self.settings is not None and jwt is not None
        self.lock = threading.Lock()
        self.keyset: Any = None
        self.attempted: float | None = None  # time.monotonic() of the last fetch, successful or not

    def keys(self, kid: Any) -> Any:
        """The cached key set, fetched again when it lacks kid (subject to the once-a-minute limit)."""
        with self.lock:
            now = time.monotonic()
            unknown = self.keyset is None or not self.keyset.get_keys(kid)
            if unknown and (self.attempted is None or now - self.attempted >= RETRY_AFTER):
                self.attempted = now
                url = self.settings[0] + "/cdn-cgi/access/certs"
                try:
                    self.keyset = jwk.JWKSet.from_json(self.fetch(url))
                except Exception as exc:  # noqa: BLE001 - keep the last good set, if any
                    sys.stderr.write(f"cloudflare access: fetching the key set from {url} failed: {type(exc).__name__}: {exc}\n")
            if self.keyset is None:
                raise LookupError("no Cloudflare Access key set")
            return self.keyset

    def email(self, assertion: str | None) -> str | None:
        """The lower-case email of a verified token, or None for a missing, invalid or unverifiable one."""
        if not assertion or not self.configured:
            return None
        issuer, audience = self.settings
        try:
            token = jwt.JWT(jwt=assertion, algs=["RS256"], expected_type="JWS",
                            check_claims={"iss": issuer, "aud": audience, "exp": None})
            token.leeway = LEEWAY
            token.validate(self.keys(token.token.jose_header.get("kid")))  # the signature, then the claims
            claims = json.loads(token.claims)
            # nbf is optional; listing it in check_claims would reject tokens without it
            if isinstance(claims.get("nbf"), (int, float)) and claims["nbf"] > wall_clock() + LEEWAY:
                return None
            email = claims.get("email")
        except Exception:  # noqa: BLE001 - any failure means "not signed in"
            return None
        return email.strip().lower() if isinstance(email, str) and email.strip() else None
