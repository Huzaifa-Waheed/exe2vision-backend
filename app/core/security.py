import os
import hashlib
import hmac
import base64

# PBKDF2 settings (uses only Python stdlib)
SALT_SIZE = 16
ITERATIONS = 200_000
HASH_NAME = "sha256"


def hash_password(password: str) -> str:
    """Return a string containing algorithm, iterations, salt and derived key.

    Format: pbkdf2_sha256$<iterations>$<salt_b64>$<dk_b64>
    """
    salt = os.urandom(SALT_SIZE)
    dk = hashlib.pbkdf2_hmac(HASH_NAME, password.encode("utf-8"), salt, ITERATIONS)
    return f"pbkdf2_sha256${ITERATIONS}${base64.b64encode(salt).decode()}${base64.b64encode(dk).decode()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algo, iter_s, salt_b64, dk_b64 = stored_hash.split("$", 3)
    except Exception:
        return False
    if algo != "pbkdf2_sha256":
        # unknown format
        return False
    iterations = int(iter_s)
    salt = base64.b64decode(salt_b64)
    dk = base64.b64decode(dk_b64)
    new_dk = hashlib.pbkdf2_hmac(HASH_NAME, password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(new_dk, dk)

