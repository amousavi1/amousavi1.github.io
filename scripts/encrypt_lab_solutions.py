"""Encrypt Lab 1 solutions for the password-gated page.

Plaintext lives in files/data-612/lab-1-solutions.md (gitignored).
Only the ciphertext JSON is published.

  python scripts/encrypt_lab_solutions.py --password "your-passphrase"

Keep the passphrase off the public site. Share it with students when you want
them to open data-612-lab-1-solutions.html.
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
MD_PATH = ROOT / "files" / "data-612" / "lab-1-solutions.md"
OUT_PATH = ROOT / "files" / "data-612" / "lab-1-solutions.enc.json"
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--password",
        default=os.environ.get("LAB1_SOLUTIONS_PASSWORD"),
        help="Passphrase students will type. Or set LAB1_SOLUTIONS_PASSWORD.",
    )
    args = parser.parse_args()
    if not args.password:
        sys.exit("Provide --password or LAB1_SOLUTIONS_PASSWORD.")
    if not MD_PATH.exists():
        sys.exit(f"Missing {MD_PATH}")

    html = markdown_to_html(MD_PATH.read_text(encoding="utf-8"))
    payload = encrypt(html.encode("utf-8"), args.password)
    OUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
