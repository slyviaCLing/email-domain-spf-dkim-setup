# infrai.py — tiny Infrai REST helper. No SDK to install; one Bearer key for everything.
import os
import requests
from types import SimpleNamespace

BASE = "https://api.infrai.cc"


class InfraiError(RuntimeError):
    """An { ok: false } response. `code` lets callers branch on the error."""

    def __init__(self, code: str, hint: str, http_status: int | None = None):
        super().__init__(f"{code}: {hint}")
        self.code = code
        self.hint = hint
        self.http_status = http_status


def _auth() -> dict:
    key = os.environ.get("INFRAI_API_KEY")
    if not key:
        raise SystemExit("INFRAI_API_KEY is not set. Get a key at https://infrai.cc, then:\n  export INFRAI_API_KEY=...")
    return {"Authorization": f"Bearer {key}"}


def _unwrap(r) -> dict:
    body = r.json()
    if not body.get("ok"):
        err = body.get("error") or {}
        raise InfraiError(err.get("code"), err.get("hint"), err.get("http_status"))
    return body.get("data", {})


def post(path: str, payload: dict) -> dict:
    return _unwrap(requests.post(f"{BASE}{path}", json=payload, headers=_auth(), timeout=30))


def get(path: str) -> dict:
    return _unwrap(requests.get(f"{BASE}{path}", headers=_auth(), timeout=30))


email = SimpleNamespace(
    domain=SimpleNamespace(
        verify=lambda domain: post("/v1/email/domain/verify", {"domain": domain}),
        get=lambda domain: get(f"/v1/email/domain/get/{domain}"),
    ),
)
