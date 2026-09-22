import hashlib
import hmac
import secrets

from app.config import settings


def generate_verification_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_verification_code(code: str) -> str:
    return hmac.new(
        settings.verification_code_secret.encode(),
        code.encode(),
        hashlib.sha256,
    ).hexdigest()


def verify_verification_code(
    code: str,
    code_hash: str,
) -> bool:
    expected_hash = hash_verification_code(code)

    return hmac.compare_digest(
        expected_hash,
        code_hash,
    )