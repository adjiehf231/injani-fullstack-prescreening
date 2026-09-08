"""
PT Injani Systems - Fullstack Developer Prescreening
Unit tests for Google Cloud Tasks Worker (Q3)
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_cloud_task_worker_execution_success(client):
    payload = {
        "workflow_id": "wf_2026_09",
        "action": "GENERATE_NIGHTLY_REPORT"
    }
    headers = {
        "X-CloudTasks-QueueName": "nightly-reports-queue",
        "X-CloudTasks-TaskName": "task-uuid-88912",
        "X-CloudTasks-TaskRetryCount": "0",
        "X-CloudTasks-TaskExecutionCount": "1",
    }

    res = client.post("/api/v1/tasks/worker", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()["data"]

    assert data["status"] == "SUCCESS"
    assert data["action"] == "GENERATE_NIGHTLY_REPORT"
    assert data["processed_items"] == 120


def test_cloud_task_worker_dead_letter_on_max_retries(client):
    payload = {
        "workflow_id": "wf_failing_01",
        "action": "SYNC_FAILED_LEDGER"
    }
    # Cloud Tasks retry count >= 4 indicates terminal failure attempt
    headers = {
        "X-CloudTasks-QueueName": "nightly-reports-queue",
        "X-CloudTasks-TaskName": "task-uuid-failing-99",
        "X-CloudTasks-TaskRetryCount": "4",
        "X-CloudTasks-TaskExecutionCount": "5",
    }

    res = client.post("/api/v1/tasks/worker", json=payload, headers=headers)
    assert res.status_code == 200
    body = res.json()

    assert body["success"] is False
    assert body["error"]["code"] == "TASK_DEAD_LETTERED"
    assert body["data"]["status"] == "DEAD_LETTERED"
