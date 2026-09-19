"""Local-only Schwab connection test runner (never contacts my code path).

This is the SAFE "plug your keys" step: it runs entirely on YOUR machine and your
credentials never enter git, never enter a chat transcript, and are never exposed
to me. The pattern is OAuth 2.0 authorization-code flow:

  YOUR machine reads  SCHWAB_CLIENT_ID / SCHWAB_CLIENT_SECRET / SCHWAB_REDIRECT_URI
  from a local file you create  ->  builds the Schwab authorize URL  ->  you log in
  in your browser  ->  Schwab redirects with a one-time code  ->  this script
  exchanges it (on your machine) for an access token  ->  makes ONE read-only
  call (your balances / positions)  ->  prints whether the connection works.

Security posture (matches hedge_desk/brokers/schwab_oauth.py):
- The secret is read from a file you own and is never written, logged, or returned.
- State is generated per attempt and verified round-trip (CSRF).
- Only the read-only scope is requested; no order is ever placed by this script.
- Fail closed: any error returns a structured result, never a fabricated token.

This makes NO orders. It exists so the GP can prove his Schwab credentials work
end-to-end before any execution gate is released.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Optional

from hedge_desk.brokers.schwab_oauth import SchwabOAuth, SchwabOAuthConfig
from hedge_desk.brokers.schwab_readonly import SchwabReadOnlyBroker


def _read_env_file(path: Path) -> Dict[str, str]:
    """Read KEY=VALUE lines from a local env file the user owns."""
    result: Dict[str, str] = {}
    if not path.is_file():
        return result
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def _config(env: Dict[str, str]) -> Optional[SchwabOAuthConfig]:
    conf = SchwabOAuthConfig.from_environment(env)
    return conf if conf.configured else None


def build_authorize_url(env: Dict[str, str]) -> Dict[str, object]:
    """Return the browser URL for the GP to log in, plus the CSRF state to verify."""
    conf = _config(env)
    if conf is None:
        return {
            "status": "not_configured",
            "hint": "Set SCHWAB_CLIENT_ID, SCHWAB_CLIENT_SECRET, SCHWAB_REDIRECT_URI "
                    "in your local env file.",
        }
    oauth = SchwabOAuth(conf)
    state = oauth.new_state()
    return {"status": "ok", "state": state, "authorize_url": oauth.authorize_url(state)}


def exchange_and_probe(
    env: Dict[str, str],
    code: str,
    state_expected: str,
    state_provided: str,
) -> Dict[str, object]:
    """Exchange the one-time code for a token and make ONE read-only call."""
    if state_expected != state_provided:
        return {"status": "error", "error": "state_mismatch"}
    conf = _config(env)
    if conf is None:
        return {"status": "error", "error": "not_configured"}
    oauth = SchwabOAuth(conf)
    result = oauth.exchange_code(code)
    if result.get("status") != "ok":
        return {"status": "error", "error": result.get("error", "exchange_failed")}
    token = result["access_token"]
    broker = SchwabReadOnlyBroker()
    numbers = broker.account_numbers(token)
    accounts = numbers.get("account_numbers", []) if numbers.get("status") == "ok" else []
    summary = {
        "status": "ok",
        "token_type": result.get("token_type", "Bearer"),
        "scope": result.get("scope", "readonly"),
        "account_count": len(accounts),
        "accounts": accounts,
        "read_only": True,
        "note": "Connection validated with a single read-only call. No order placed.",
        # never return the token
    }
    if not accounts:
        summary["status"] = "ok_no_accounts"
        summary["note"] = "Token valid but no account numbers exposed; scope/perms may need review."
    return summary


def load_env(path: Path) -> Dict[str, str]:
    return _read_env_file(path)


def _state_file(env_file: Path) -> Path:
    return env_file.parent / ".schwab_state"


def _save_state(env_file: Path, state: str) -> None:
    """Persist the CSRF state until the exchange completes (0600, single value)."""
    sf = _state_file(env_file)
    sf.write_text(state, encoding="utf-8")
    os.chmod(sf, 0o600)


def _read_and_consume_state(env_file: Path) -> Optional[str]:
    """Read the expected state, then delete it (single-use, tamper-evident)."""
    sf = _state_file(env_file)
    if not sf.is_file():
        return None
    value = sf.read_text(encoding="utf-8").strip()
    try:
        sf.unlink()
    except OSError:
        pass
    return value or None


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--env",
        default="~/.schwab/env.env",
        help="path to your local Schwab KEY=VALUE env file (never committed)",
    )
    parser.add_argument(
        "--auth", action="store_true",
        help="print the authorize URL and save its CSRF state for the exchange step",
    )
    parser.add_argument(
        "--code", default="",
        help="the one-time code Schwab redirects back to your callback, to exchange",
    )
    parser.add_argument(
        "--state", default="",
        help="the state value Schwab echoed back (required; verified against the saved state)",
    )
    args = parser.parse_args()

    env_file = Path(args.env).expanduser()
    env_file.parent.mkdir(parents=True, exist_ok=True)
    # Hard requirement: the secrets directory must not be world/group readable.
    os.chmod(env_file.parent, 0o700)

    env = load_env(env_file)
    if args.auth:
        result = build_authorize_url(env)
        if result.get("status") == "ok" and result.get("state"):
            _save_state(env_file, str(result["state"]))
        print(json.dumps(result, indent=2))
        return
    if not args.code:
        parser.error("Use --auth to get the URL, log in, then pass --code <code> --state <state>")
        return

    # GENUINE round-trip CSRF: compare the provided state against the one SAVED at
    # --auth time (a value can never verify itself). Single-use: consumed after.
    expected = _read_and_consume_state(env_file)
    if expected is None:
        print(json.dumps(
            {"status": "error",
             "error": "no_saved_state",
             "detail": "Run --auth first so the expected CSRF state is stored."},
            indent=2))
        return
    print(json.dumps(
        exchange_and_probe(env, args.code, expected, args.state or ""), indent=2))


if __name__ == "__main__":
    main()