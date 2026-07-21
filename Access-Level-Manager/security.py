import hashlib
import os

ITERATIONS = 100_000
def hash_password(password, salt=None):
    if salt is None:
        salt_bytes = os.urandom(16)
    else:
        salt_bytes = bytes.fromhex(salt)

    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt_bytes,
        ITERATIONS
    )
    return salt_bytes.hex(), pwd_hash.hex()


def verify_password(password, salt_hex, stored_hash_hex):
    if not salt_hex or not stored_hash_hex:
        return False
    _, new_hash_hex = hash_password(password, salt_hex)
    return new_hash_hex == stored_hash_hex