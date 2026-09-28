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
The key set is fetched from `<team domain>/cdn-cgi/access/certs` and kept for an hour. A token that no cached key
verifies (as after Cloudflare rotates its keys) prompts an early fetch. Fetches, including failed ones, happen at
most once a minute.
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
import urllib.request
from typing import Any, Callable

try:
    from jwcrypto import jwk, jwt
except ImportError:  # the VM's python3-jwcrypto package provides it; without it nobody is signed in
    jwk = jwt = None

TEAM_ENV = "COCKPIT_ACCESS_TEAM_DOMAIN"
AUD_ENV = "COCKPIT_ACCESS_AUD"
KEYS_TTL = 3600
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


def configured() -> bool:
    return settings() is not None and jwt is not None


def fetch_keys(url: str) -> str:
    with urllib.request.urlopen(url, timeout=FETCH_TIMEOUT) as response:  # noqa: S310 - https URL from configuration
        return response.read(1 << 20).decode("utf-8")


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


class Verifier:
    """Verifies Access tokens against the team's key set, which it caches. Shared by the request threads."""

    def __init__(self, fetch: Callable[[str], str] = fetch_keys):
        self.fetch = fetch
        self.lock = threading.Lock()
        self.cache: dict[str, tuple[Any, float | None, float]] = {}  # url -> (key set or None, fetched, last attempt)

    def keys(self, url: str, stale: bool = False) -> Any:
        """The key set for url. stale=True asks for a new copy, subject to the once-a-minute limit."""
        with self.lock:
            keyset, fetched, attempted = self.cache.get(url, (None, None, None))
            now = time.monotonic()
            due = attempted is None or (now - attempted >= RETRY_AFTER and (keyset is None or stale or now - fetched >= KEYS_TTL))
            if due:
                try:
                    keyset, fetched = jwk.JWKSet.from_json(self.fetch(url)), now
                except Exception as exc:  # noqa: BLE001 - keep the last good set, if any
                    sys.stderr.write(f"cloudflare access: fetching the key set from {url} failed: {type(exc).__name__}: {exc}\n")
                self.cache[url] = (keyset, fetched, now)
            if keyset is None:
                raise LookupError("no Cloudflare Access key set")
            return keyset

    def email(self, assertion: str | None) -> str | None:
        """The lower-case email of a verified token, or None for a missing, invalid or unverifiable one."""
        config = settings()
        if not assertion or config is None or jwt is None:
            return None
        issuer, audience = config
        url = issuer + "/cdn-cgi/access/certs"
        try:
            try:
                claims = self._claims(assertion, self.keys(url))
            except jwt.JWTMissingKey:  # no cached key verifies it: the keys may have rotated
                claims = self._claims(assertion, self.keys(url, stale=True))
        except Exception:  # noqa: BLE001 - any failure means "not signed in"
            return None
        now = time.time()
        audiences = claims.get("aud") if isinstance(claims.get("aud"), list) else [claims.get("aud")]
        exp, nbf, email = claims.get("exp"), claims.get("nbf"), claims.get("email")
        if claims.get("iss") != issuer or audience not in audiences:
            return None
        if not _number(exp) or exp < now - LEEWAY:
            return None
        if nbf is not None and (not _number(nbf) or nbf > now + LEEWAY):
            return None
        return email.strip().lower() if isinstance(email, str) and email.strip() else None

    @staticmethod
    def _claims(assertion: str, keyset: Any) -> dict[str, Any]:
        """The claims of a token whose RS256 signature verifies against keyset; the caller checks the claims."""
        token = jwt.JWT(jwt=assertion, key=keyset, algs=["RS256"], expected_type="JWS", check_claims=False)
        claims = json.loads(token.claims)
        if not isinstance(claims, dict):
            raise ValueError("the token's claims are not an object")
        return claims
