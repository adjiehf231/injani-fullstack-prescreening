"""
Unit tests for Error Handling, Rate Limiting, and Security (Q5)
"""

import hmac
import hashlib
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import rate_limiter
from app.core.config import settings
from app.core.security import verify_webhook_hmac_sha256


@pytest.fixture
def client():
    rate_limiter.clear()
    return TestClient(app)


def test_standardized_validation_error_format(client):
    # Send empty payload to trigger Pydantic validation error
    res = client.post("/api/v1/extract-order", json={})
    assert res.status_code == 422
    body = res.json()

    assert body["success"] is False
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert "trace_id" in body["error"]
    assert len(body["error"]["details"]) > 0


def test_standardized_not_found_error_format(client):
    res = client.get("/api/v1/tasks/non-existent-task-id-123/progress")
    assert res.status_code == 404
    body = res.json()

    assert body["success"] is False
    assert body["error"]["code"] == "RESOURCE_NOT_FOUND"
    assert "trace_id" in body["error"]


def test_hmac_webhook_verification_success_and_tampering(client):
    secret = settings.webhook_secret
    payload = b'{"event":"message_received","text":"hello"}'

    # Valid signature
    valid_sig = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    assert verify_webhook_hmac_sha256(payload, valid_sig, secret) is True
    assert verify_webhook_hmac_sha256(payload, f"sha256={valid_sig}", secret) is True

    # Tampered payload
    tampered = b'{"event":"message_received","text":"tampered!"}'
    assert verify_webhook_hmac_sha256(tampered, valid_sig, secret) is False

    # Invalid secret
    assert verify_webhook_hmac_sha256(payload, valid_sig, "wrong-secret") is False

    # Webhook endpoint integration test
    res_valid = client.post(
        "/api/v1/webhooks/whatsapp",
        content=payload,
        headers={"X-Hub-Signature-256": f"sha256={valid_sig}"}
    )
    assert res_valid.status_code == 200
    assert res_valid.json()["success"] is True

    res_invalid = client.post(
        "/api/v1/webhooks/whatsapp",
        content=payload,
        headers={"X-Hub-Signature-256": "sha256=invalidhexsignature"}
    )
    assert res_invalid.status_code == 401
    assert res_invalid.json()["error"]["code"] == "INVALID_WEBHOOK_SIGNATURE"


def test_rate_limiter_exceeded(client):
    # Rate limiter configured with limit=10 requests/window
    endpoint = "/api/v1/extract-order"
    payload = {
        "sender_phone": "+6281234567890",
        "message_text": "Ping test",
        "timestamp": "2026-09-08T11:00:00Z"
    }

    # Exhaust rate limit
    for _ in range(10):
        r = client.post(endpoint, json=payload)
        assert r.status_code == 200

    # 11th request must be rejected with 429
    r_exceeded = client.post(endpoint, json=payload)
    assert r_exceeded.status_code == 429
    body = r_exceeded.json()
    assert body["success"] is False
    assert body["error"]["code"] == "RATE_LIMIT_EXCEEDED"
