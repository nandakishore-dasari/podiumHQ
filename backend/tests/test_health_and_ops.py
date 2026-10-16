"""
Tests for Operations Endpoints (/health, /ready, /metrics, /)
"""

from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from backend.app.database import get_db
from backend.app.main import app


def test_root_metadata(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "PodiumHQ"
    assert data["status"] == "online"
    assert "/health" in data["health"]
    assert "/metrics" in data["metrics"]


def test_health_probe(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_readiness_probe_healthy(client: TestClient):
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["database"] == "connected"


def test_readiness_probe_db_failure(client: TestClient):
    mock_db = MagicMock()
    mock_db.execute.side_effect = OperationalError("connection refused", {}, None)

    app.dependency_overrides[get_db] = lambda: mock_db
    try:
        response = client.get("/ready")
        assert response.status_code == 503
        data = response.json()
        assert "Database connectivity check failed" in data["detail"]
    finally:
        app.dependency_overrides.pop(get_db, None)


def test_metrics_endpoint(client: TestClient):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers.get("content-type", "")
    content = response.text
    # Verify custom domain metrics are present in telemetry
    assert "podiumhq_scores_submitted_total" in content
    assert "podiumhq_teams_by_status" in content
    assert "podiumhq_score_value" in content
    assert "podiumhq_leaderboard_requests_total" in content
