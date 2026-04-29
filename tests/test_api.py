from fastapi.testclient import TestClient

from src.cli import app
from src.api import endpoints


client = TestClient(app)


def test_health_endpoint_returns_alive_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "alive"
    assert "X-Process-Time" in response.headers


def test_tasks_endpoint_requires_api_key(valid_task_payload):
    response = client.post("/api/v1/tasks", json=valid_task_payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "API Key missing"


def test_tasks_endpoint_rejects_invalid_api_key(valid_task_payload, monkeypatch):
    monkeypatch.setattr(endpoints.settings, "API_KEY_SECRET", "correct-secret")

    response = client.post(
        "/api/v1/tasks",
        json=valid_task_payload,
        headers={"X-API-Key": "wrong-secret"},
    )

    assert response.status_code == 403


def test_tasks_endpoint_accepts_valid_payload_and_key(valid_task_payload, monkeypatch):
    monkeypatch.setattr(endpoints.settings, "API_KEY_SECRET", "test-secret")
    monkeypatch.setattr(endpoints.kafka_service, "send_task", lambda task: True)

    response = client.post(
        "/api/v1/tasks",
        json=valid_task_payload,
        headers={"X-API-Key": "test-secret"},
    )

    assert response.status_code == 202
    assert response.json() == {"status": "accepted", "id": valid_task_payload["order_id"]}


def test_tasks_endpoint_returns_500_when_kafka_fails(valid_task_payload, monkeypatch):
    monkeypatch.setattr(endpoints.settings, "API_KEY_SECRET", "test-secret")
    monkeypatch.setattr(endpoints.kafka_service, "send_task", lambda task: False)

    response = client.post(
        "/api/v1/tasks",
        json=valid_task_payload,
        headers={"X-API-Key": "test-secret"},
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "Internal Broker Error"
