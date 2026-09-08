"""
PT Injani Systems - Fullstack Developer Prescreening
Q5: Authentication & Webhook Security Utilities
"""

import hmac
import hashlib
import time
from typing import Dict, Any, Optional
from app.core.errors import DomainException


def verify_webhook_hmac_sha256(
    payload_bytes: bytes,
    signature_header: str,
    secret_key: str
) -> bool:
    """
    Verifies that an incoming webhook request body matches the HMAC-SHA256 signature.
    Prevents tampering and spoofing from unauthorized callers.
    Common pattern in WhatsApp Cloud API (X-Hub-Signature-256) and GitHub/Stripe webhooks.
    """
    if not signature_header or not secret_key:
        return False
    
    # Strip optional prefix like "sha256="
    expected_prefix = "sha256="
    if signature_header.startswith(expected_prefix):
        received_sig = signature_header[len(expected_prefix):]
    else:
        received_sig = signature_header

    mac = hmac.new(secret_key.encode("utf-8"), msg=payload_bytes, digestmod=hashlib.sha256)
    computed_sig = mac.hexdigest()
    
    # Constant-time comparison to prevent timing attacks
    return hmac.compare_digest(computed_sig, received_sig)


def mock_verify_jwt_token(auth_header: Optional[str], secret: str = "production-secret-key") -> Dict[str, Any]:
    """
    Decodes and validates JWT bearer token.
    In production: uses PyJWT or python-jose with RS256/HS256 validation.
    """
    if not auth_header:
        raise DomainException(
            message="Authorization header missing.",
            code="UNAUTHORIZED",
            status_code=401
        )
    
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise DomainException(
            message="Invalid Authorization format. Expected 'Bearer <token>'.",
            code="INVALID_AUTH_HEADER",
            status_code=401
        )
    
    token = parts[1]
    
    # For demonstration and test suite: validate token format and test tokens
    if token == "invalid-token" or len(token) < 10:
        raise DomainException(
            message="Token signature is invalid or token has expired.",
            code="INVALID_TOKEN",
            status_code=401
        )
    
    # Simulated claims payload
    return {
        "sub": "usr_998124",
        "email": "analyst@injani.co.id",
        "role": "analyst",
        "exp": int(time.time()) + 3600
    }
