"""
Pytest configuration and test environment setup.
Injects isolated, test-only secrets so application runtime does not require
or use insecure fallback defaults.
"""
import os
import pytest

# Inject deterministic test-only secrets for pytest runs
TEST_JWT_SECRET = "test-deterministic-jwt-secret-at-least-32-chars-long!!"
TEST_WEBHOOK_SECRET = "test-deterministic-webhook-secret-token"

os.environ["JWT_SECRET"] = TEST_JWT_SECRET
os.environ["WEBHOOK_SECRET"] = TEST_WEBHOOK_SECRET

from app.core.config import settings

# Bind test secrets to current settings instance for test run
settings.jwt_secret = TEST_JWT_SECRET
settings.webhook_secret = TEST_WEBHOOK_SECRET
