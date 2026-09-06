"""Encrypt lab solutions for the password-gated pages.

Plaintext lives in files/data-612/lab-*-solutions.md (gitignored).
Only the ciphertext JSON is published.

  python scripts/encrypt_lab_solutions.py --lab 2
  python scripts/encrypt_lab_solutions.py --lab 1 --password "your-passphrase"

If --password is omitted, the script uses files/data-612/.lab1-solutions-password
or LAB_SOLUTIONS_PASSWORD. Keep the passphrase off the public site.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import pathlib
import secrets
import subprocess
import sys

try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ROOT = pathlib.Path(__file__).resolve().parents[1]
PASSWORD_FILE = ROOT / "files" / "data-612" / ".lab1-solutions-password"
ITERATIONS = 210_000


def markdown_to_html(text: str) -> str:
    try:
        import markdown
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])
        import markdown

    html = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
    html = html.replace("<table>", '<div class="table-wrap"><table>').replace(
        "</table>", "</table></div>"
    )
    return html


def encrypt(plaintext: bytes, password: str) -> dict:
    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    key = kdf.derive(password.encode("utf-8"))
    ct = AESGCM(key).encrypt(nonce, plaintext, None)
    b64 = lambda b: base64.b64encode(b).decode("ascii")
    return {
        "v": 1,
        "kdf": "PBKDF2",
        "hash": "SHA-256",
        "iter": ITERATIONS,
        "salt": b64(salt),
        "iv": b64(nonce),
        "ct": b64(ct),
    }


def default_password() -> str | None:
    env = os.environ.get("LAB_SOLUTIONS_PASSWORD") or os.environ.get(
        "LAB1_SOLUTIONS_PASSWORD"
    )
    if env:
        return env
    if PASSWORD_FILE.exists():
        return PASSWORD_FILE.read_text(encoding="utf-8").strip()
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lab", default="1", help="Lab number, for example 1 or 2.")
    parser.add_argument(
        "--password",
        default=default_password(),
        help="Passphrase students will type. Or set LAB_SOLUTIONS_PASSWORD.",
    )
    args = parser.parse_args()
    if not args.password:
        sys.exit("Provide --password, LAB_SOLUTIONS_PASSWORD, or the password file.")

    md_path = ROOT / "files" / "data-612" / f"lab-{args.lab}-solutions.md"
    out_path = ROOT / "files" / "data-612" / f"lab-{args.lab}-solutions.enc.json"
    if not md_path.exists():
        sys.exit(f"Missing {md_path}")

    html = markdown_to_html(md_path.read_text(encoding="utf-8"))
    payload = encrypt(html.encode("utf-8"), args.password)
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
