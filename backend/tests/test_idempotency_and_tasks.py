"""
Unit tests for Idempotency and Async Background Job Tracking (Q6)
"""

import asyncio
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import idempotency_store
from app.services.task_manager import global_task_manager, TaskStatus
from app.core.errors import ConflictException


@pytest.fixture
def client():
    idempotency_store.clear()
    return TestClient(app)


def test_idempotent_order_submission_prevents_duplicate_runs(client):
    payload = {
        "customer_id": "cust_8821",
        "items": [{"item_name": "cement", "quantity": 10}],
        "delivery_address": "Jl. Sudirman No. 45, Jakarta"
    }
    headers = {"Idempotency-Key": "req_unique_abc_123"}

    # First request
    res1 = client.post("/api/v1/orders/submit", json=payload, headers=headers)
    assert res1.status_code == 202
    data1 = res1.json()["data"]
    order_id = data1["order_id"]
    task_id = data1["task_id"]

    # Second request with identical Idempotency-Key (simulating network retry)
    res2 = client.post("/api/v1/orders/submit", json=payload, headers=headers)
    assert res2.status_code in [200, 202]
    assert res2.headers.get("X-Cache-Lookup") == "HIT-IDEMPOTENT"
    data2 = res2.json()["data"]

    # Verify identical order_id and task_id were returned, not newly generated
    assert data2["order_id"] == order_id
    assert data2["task_id"] == task_id


def test_concurrent_idempotency_request_conflict():
    idempotency_store.clear()
    key = "concurrent_key_777"
    
    # First request locks the key as IN_PROGRESS
    res = idempotency_store.check_or_lock(key)
    assert res is None  # Locked

    # Concurrent request attempting to use the same key before completion must raise ConflictException
    with pytest.raises(ConflictException) as exc_info:
        idempotency_store.check_or_lock(key)
    assert exc_info.value.status_code == 409
    assert exc_info.value.code == "IDEMPOTENCY_CONCURRENT_REQUEST"


@pytest.mark.anyio
async def test_async_task_progress_lifecycle():
    task_id = global_task_manager.create_task(task_type="pdf_report")
    
    # Initial status
    initial = global_task_manager.get_task_status(task_id)
    assert initial.status == TaskStatus.PENDING
    assert initial.progress_percent == 0

    # Execute simulation
    await global_task_manager.execute_mock_pdf_generation(task_id, "ord_test_99")

    # Completed status
    final_status = global_task_manager.get_task_status(task_id)
    assert final_status.status == TaskStatus.COMPLETED
    assert final_status.progress_percent == 100
    assert "download_url" in final_status.result
