import base64
import hashlib
import os
import secrets

ALGORITHM = "sha256"
ITERATIONS = 310_000


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(ALGORITHM, password.encode("utf-8"), salt, ITERATIONS)
    return f"{ALGORITHM}${ITERATIONS}${base64.b64encode(salt).decode()}${base64.b64encode(digest).decode()}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations, salt_b64, digest_b64 = password_hash.split("$")
        salt = base64.b64decode(salt_b64)
        digest = base64.b64decode(digest_b64)
        test_digest = hashlib.pbkdf2_hmac(algorithm, password.encode("utf-8"), salt, int(iterations))
        return secrets.compare_digest(test_digest, digest)
    except Exception:
        return False
