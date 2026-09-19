"""One-command secure Schwab local setup (run on YOUR machine).

Prompts for the two keys at the terminal using getpass (no echo, no log), writes
them to a 0600 file you own, verifies the redirect URI, and hands you the
authorize URL. Nothing is committed, logged, or printed back. Run:

  python3 -m hedge_desk.schwab_setup
"""

from __future__ import annotations

import getpass
import os
import sys
from pathlib import Path

from hedge_desk.connect_local import build_authorize_url, load_env


DEFAULT_ENV_FILE = "~/.schwab/env.env"


def _yesno(prompt: str, default: bool = False) -> bool:
    suffix = " [y/N]" if not default else " [Y/n]"
    while True:
        val = input(prompt + suffix + " ").strip().lower()
        if not val:
            return default
        if val in ("y", "yes"):
            return True
        if val in ("n", "no"):
            return False
        print("please answer y or n")


def run(env_file: str | None = None, write: bool = True) -> dict:
    path = Path((env_file or DEFAULT_ENV_FILE)).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)

    existing = load_env(path)
    if existing:
        print(f"Env file already exists at {path} with:" +
              (" a client id" if existing.get("SCHWAB_CLIENT_ID") else "") +
              (", a secret" if existing.get("SCHWAB_CLIENT_SECRET") else "") +
              (".")
        )

    # Prompt for the two secrets at the terminal with getpass (no echo to the
    # terminal session or any transcript).
    client_id = input("Schwab App Key (client id): ").strip()
    if not client_id:
        print("No app key supplied; aborting.")
        sys.exit(1)
    client_secret = getpass.getpass("Schwab App Secret (not shown as you type): ").strip()
    if not client_secret:
        print("No app secret supplied; aborting.")
        sys.exit(1)
    redirect_uri = input("Redirect URI (Schwab callbacks URL, e.g. https://127.0.0.1): ").strip() or "https://127.0.0.1"

    content = "\n".join([
        f"SCHWAB_CLIENT_ID={client_id}",
        f"SCHWAB_CLIENT_SECRET={client_secret}",
        f"SCHWAB_REDIRECT_URI={redirect_uri}",
        "",
    ])
    if write:
        tmp = path.with_suffix(".tmp")
        tmp.write_text(content, encoding="utf-8")
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)  # atomic, 0600
        os.chmod(path, 0o600)

    env = load_env(path)
    auth = build_authorize_url(env)
    return {"env_file": str(path), "auth": auth}


def main() -> None:
    result = run()
    auth = result["auth"]
    if auth.get("status") != "ok":
        print("\n" + auth.get("hint", "not configured"))
        sys.exit(1)
    print("\n=== next step: open this URL in your browser and log in to Schwab ===")
    print(auth["authorize_url"])
    print("\nAfter you log in, Schwab redirects to your callback URL with")
    print("  ?code=...&state=...  in the address bar.")
    print("Copy BOTH values, then run:")
    print("  python3 -m hedge_desk.connect_local --env ~/.schwab/env.env --code <code> --state <state>")


if __name__ == "__main__":
    main()