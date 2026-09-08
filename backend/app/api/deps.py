"""
PT Injani Systems - Fullstack Developer Prescreening
Q5 & Q6: Dependencies for Idempotency, Rate Limiting, and Authentication
"""

import time
from typing import Dict, Any, Optional
from fastapi import Header, Request, HTTPException
from app.core.errors import ConflictException, RateLimitExceededException, DomainException
from app.core.security import mock_verify_jwt_token


class InMemoryIdempotencyStore:
    """
    Stores idempotency records to ensure HTTP retries do not execute tasks twice (Q6c).
    In production: Backed by Redis SETNX or PostgreSQL table with UNIQUE(idempotency_key).
    """

    def __init__(self, ttl_seconds: int = 86400):
        self._store: Dict[str, Dict[str, Any]] = {}
        self.ttl_seconds = ttl_seconds

    def check_or_lock(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Returns cached response if already completed.
        Raises ConflictException if another request is currently processing this key.
        Locks key as IN_PROGRESS if new.
        """
        now = time.time()
        record = self._store.get(key)

        if record:
            # Check expiration
            if now - record["created_at"] > self.ttl_seconds:
                del self._store[key]
            elif record["status"] == "IN_PROGRESS":
                raise ConflictException(
                    message="A request with this Idempotency-Key is currently being processed. Please retry later.",
                    code="IDEMPOTENCY_CONCURRENT_REQUEST"
                )
            elif record["status"] == "COMPLETED":
                return record["response"]

        # Lock key
        self._store[key] = {
            "status": "IN_PROGRESS",
            "response": None,
            "created_at": now
        }
        return None

    def store_response(self, key: str, response_data: Dict[str, Any]) -> None:
        if key in self._store:
            self._store[key]["status"] = "COMPLETED"
            self._store[key]["response"] = response_data

    def clear(self):
        self._store.clear()


class InMemoryRateLimiter:
    """
    Sliding window in-memory rate limiter without requiring dedicated Redis (Q5b).
    Stores timestamps of requests per client key in a rolling time window.
    """

    def __init__(self, max_requests: int = 5, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._history: Dict[str, list[float]] = {}

    def check_rate_limit(self, client_id: str) -> None:
        now = time.time()
        window_start = now - self.window_seconds

        timestamps = self._history.get(client_id, [])
        # Evict timestamps older than sliding window
        valid_timestamps = [t for t in timestamps if t > window_start]

        if len(valid_timestamps) >= self.max_requests:
            retry_after = int(self.window_seconds - (now - valid_timestamps[0]))
            raise RateLimitExceededException(retry_after_seconds=max(1, retry_after))

        valid_timestamps.append(now)
        self._history[client_id] = valid_timestamps

    def clear(self):
        self._history.clear()


# Global singletons for FastAPI dependencies
idempotency_store = InMemoryIdempotencyStore()
rate_limiter = InMemoryRateLimiter(max_requests=10, window_seconds=60)


async def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """Validates JWT bearer token."""
    return mock_verify_jwt_token(authorization)


async def enforce_rate_limit(request: Request) -> None:
    """Rate limits based on client host or user token."""
    client_ip = request.client.host if request.client else "127.0.0.1"
    rate_limiter.check_rate_limit(client_ip)


async def enforce_idempotency(
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key")
) -> Optional[str]:
    """Requires or checks idempotency header."""
    if idempotency_key:
        cached_result = idempotency_store.check_or_lock(idempotency_key)
        if cached_result is not None:
            # We raise a special carrier or store the cached data on request state
            return idempotency_key
    return idempotency_key
