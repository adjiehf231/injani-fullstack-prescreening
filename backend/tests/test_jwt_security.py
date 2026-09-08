"""
PT Injani Systems - Fullstack Developer Prescreening
Unit tests for Cryptographic JWT Verification (Q5)
"""

import time
import pytest
from app.core.security import create_signed_jwt, verify_jwt_token
from app.core.errors import DomainException


SECRET_KEY = "test-secret-key-32-characters-minimum!!"


def test_valid_jwt_token_verification():
    claims = {
        "sub": "usr_adjie_01",
        "email": "adjie@injani.co.id",
        "role": "lead_developer",
        "departmentId": "dept_eng_01"
    }
    token = create_signed_jwt(claims, secret_key=SECRET_KEY, expires_in_seconds=3600)
    decoded = verify_jwt_token(token, secret_key=SECRET_KEY)

    assert decoded["sub"] == "usr_adjie_01"
    assert decoded["email"] == "adjie@injani.co.id"
    assert decoded["role"] == "lead_developer"
    assert decoded["departmentId"] == "dept_eng_01"
    assert decoded["exp"] > time.time()


def test_forged_jwt_signature_rejected():
    claims = {"sub": "attacker", "role": "admin"}
    # Token signed with an attacker's key
    forged_token = create_signed_jwt(claims, secret_key="attacker-untrusted-private-key")

    # Verifying with server secret must raise INVALID_SIGNATURE
    with pytest.raises(DomainException) as exc_info:
        verify_jwt_token(forged_token, secret_key=SECRET_KEY)

    assert exc_info.value.status_code == 401
    assert exc_info.value.code == "INVALID_SIGNATURE"


def test_tampered_payload_rejected():
    claims = {"sub": "user_normal", "role": "user"}
    valid_token = create_signed_jwt(claims, secret_key=SECRET_KEY)

    parts = valid_token.split(".")
    # Attacker alters the body segment to claim role: admin without resigning
    tampered_body = "eyJzdWIiOiAidXNlcl9ub3JtYWwiLCAicm9sZSI6ICJhZG1pbiJ9"
    tampered_token = f"{parts[0]}.{tampered_body}.{parts[2]}"

    with pytest.raises(DomainException) as exc_info:
        verify_jwt_token(tampered_token, secret_key=SECRET_KEY)

    assert exc_info.value.status_code == 401
    assert exc_info.value.code == "INVALID_SIGNATURE"


def test_expired_jwt_token_rejected():
    claims = {"sub": "usr_expired"}
    # Expired 10 seconds ago
    expired_token = create_signed_jwt(claims, secret_key=SECRET_KEY, expires_in_seconds=-10)

    with pytest.raises(DomainException) as exc_info:
        verify_jwt_token(expired_token, secret_key=SECRET_KEY)

    assert exc_info.value.status_code == 401
    assert exc_info.value.code == "TOKEN_EXPIRED"


def test_malformed_jwt_token_rejected():
    with pytest.raises(DomainException) as exc_info:
        verify_jwt_token("not-a-jwt-token", secret_key=SECRET_KEY)

    assert exc_info.value.status_code == 401
    assert exc_info.value.code == "INVALID_TOKEN"


def test_empty_jwt_token_rejected():
    with pytest.raises(DomainException) as exc_info:
        verify_jwt_token("", secret_key=SECRET_KEY)

    assert exc_info.value.status_code == 401
    assert exc_info.value.code == "UNAUTHORIZED"


def test_unsupported_algorithm_rejected():
    import json
    from app.core.security import _base64url_encode
    header = _base64url_encode(json.dumps({"alg": "none", "typ": "JWT"}).encode())
    body = _base64url_encode(json.dumps({"sub": "usr_none", "exp": int(time.time()) + 3600}).encode())
    token = f"{header}.{body}.invalidsig"

    with pytest.raises(DomainException) as exc_info:
        verify_jwt_token(token, secret_key=SECRET_KEY)

    assert exc_info.value.status_code == 401
    assert exc_info.value.code == "UNSUPPORTED_ALGORITHM"


def test_missing_exp_claim_rejected():
    import json
    import hmac
    import hashlib
    from app.core.security import _base64url_encode
    header = _base64url_encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    body = _base64url_encode(json.dumps({"sub": "usr_no_exp"}).encode())
    signing_input = f"{header}.{body}".encode("utf-8")
    sig = _base64url_encode(hmac.new(SECRET_KEY.encode("utf-8"), msg=signing_input, digestmod=hashlib.sha256).digest())
    token = f"{header}.{body}.{sig}"

    with pytest.raises(DomainException) as exc_info:
        verify_jwt_token(token, secret_key=SECRET_KEY)

    assert exc_info.value.status_code == 401
    assert exc_info.value.code == "INVALID_TOKEN"
    assert "Missing or invalid mandatory 'exp'" in exc_info.value.message
