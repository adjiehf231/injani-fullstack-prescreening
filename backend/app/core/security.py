"""
PT Injani Systems - Fullstack Developer Prescreening
Q5: Cryptographically Verified Authentication & Webhook Security Utilities
"""

import hmac
import hashlib
import base64
import json
import time
from typing import Dict, Any, Optional
from app.core.errors import DomainException
from app.core.config import settings


def verify_webhook_hmac_sha256(
    payload_bytes: bytes,
    signature_header: str,
    secret_key: Optional[str] = None
) -> bool:
    """
    Verifies incoming webhook requests against an HMAC-SHA256 signature.
    Prevents tampering and spoofing from unauthorized callers.
    """
    secret = secret_key or settings.webhook_secret
    if not signature_header or not secret:
        return False

    expected_prefix = "sha256="
    if signature_header.startswith(expected_prefix):
        received_sig = signature_header[len(expected_prefix):]
    else:
        received_sig = signature_header

    mac = hmac.new(secret.encode("utf-8"), msg=payload_bytes, digestmod=hashlib.sha256)
    computed_sig = mac.hexdigest()

    return hmac.compare_digest(computed_sig, received_sig)


def _base64url_decode(input_str: str) -> bytes:
    rem = len(input_str) % 4
    if rem > 0:
        input_str += "=" * (4 - rem)
    return base64.urlsafe_b64decode(input_str)


def _base64url_encode(input_bytes: bytes) -> str:
    return base64.urlsafe_b64encode(input_bytes).rstrip(b"=").decode("utf-8")


def create_signed_jwt(
    payload: Dict[str, Any],
    secret_key: Optional[str] = None,
    expires_in_seconds: int = 3600
) -> str:
    """Creates a genuine cryptographically signed JWT with HMAC-SHA256 (HS256)."""
    secret = secret_key or settings.jwt_secret
    header = {"alg": "HS256", "typ": "JWT"}
    body = {
        **payload,
        "exp": int(time.time()) + expires_in_seconds,
        "iat": int(time.time())
    }

    header_b64 = _base64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    body_b64 = _base64url_encode(json.dumps(body, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_b64}.{body_b64}".encode("utf-8")

    signature = hmac.new(secret.encode("utf-8"), msg=signing_input, digestmod=hashlib.sha256).digest()
    sig_b64 = _base64url_encode(signature)

    return f"{header_b64}.{body_b64}.{sig_b64}"


def verify_jwt_token(
    token: str,
    secret_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Cryptographically verifies JWT signature, expiration, and formatting.
    Fails closed if signature is invalid, payload is forged, or token is expired.
    """
    secret = secret_key or settings.jwt_secret
    if not token or not isinstance(token, str):
        raise DomainException(
            message="Token is missing or empty.",
            code="UNAUTHORIZED",
            status_code=401
        )

    parts = token.strip().split(".")
    if len(parts) != 3:
        raise DomainException(
            message="Malformed JWT token structure. Expected 3 segments.",
            code="INVALID_TOKEN",
            status_code=401
        )

    header_b64, body_b64, signature_b64 = parts

    # 1. Cryptographic Signature Verification
    signing_input = f"{header_b64}.{body_b64}".encode("utf-8")
    expected_signature = hmac.new(secret.encode("utf-8"), msg=signing_input, digestmod=hashlib.sha256).digest()
    expected_sig_b64 = _base64url_encode(expected_signature)

    if not hmac.compare_digest(expected_sig_b64, signature_b64):
        raise DomainException(
            message="Invalid JWT signature. The token has been forged, tampered with, or signed by an untrusted key.",
            code="INVALID_SIGNATURE",
            status_code=401
        )

    # 2. Decode and Validate Claims
    try:
        payload = json.loads(_base64url_decode(body_b64).decode("utf-8"))
    except Exception:
        raise DomainException(
            message="Corrupted JWT payload.",
            code="INVALID_TOKEN",
            status_code=401
        )

    # 3. Check Expiration
    exp = payload.get("exp")
    if exp is not None and isinstance(exp, (int, float)):
        if time.time() > exp:
            raise DomainException(
                message="Token has expired. Please refresh your credentials.",
                code="TOKEN_EXPIRED",
                status_code=401
            )

    return payload
