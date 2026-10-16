"""
Tests for Teams CRUD, Lifecycle State Machine, and Stats
"""

from fastapi.testclient import TestClient

from backend.app.models.event import Event
from backend.app.models.team import Team


def test_register_team_success(client: TestClient, sample_event: Event):
    payload = {
        "event_id": sample_event.id,
        "name": "Quantum Defenders",
        "project_title": "Quantum Key Distribution Controller",
        "project_repo_url": "https://github.com/quantum/qkd",
        "demo_url": "https://qkd.podiumhq.local",
        "track": "Cryptography",
    }
    response = client.post("/api/teams", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Quantum Defenders"
    assert data["status"] == "registered"


def test_register_team_duplicate_name_conflict(client: TestClient, sample_team: Team):
    payload = {
        "event_id": sample_team.event_id,
        "name": sample_team.name,  # Duplicate name
        "project_title": "Another Project",
        "track": "General",
    }
    response = client.post("/api/teams", json=payload)
    assert response.status_code == 409
    assert "already registered" in response.json()["detail"]


def test_register_team_event_not_found(client: TestClient):
    payload = {
        "event_id": 999999,
        "name": "Orphan Team",
        "project_title": "No Event",
    }
    response = client.post("/api/teams", json=payload)
    assert response.status_code == 404


def test_list_teams_filter_and_search(client: TestClient, sample_team: Team):
    response = client.get(f"/api/teams?event_id={sample_team.event_id}&status=registered&search=CyberShield")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert data["items"][0]["name"] == sample_team.name


def test_get_team_by_id(client: TestClient, sample_team: Team):
    response = client.get(f"/api/teams/{sample_team.id}")
    assert response.status_code == 200
    assert response.json()["id"] == sample_team.id


def test_get_team_not_found(client: TestClient):
    response = client.get("/api/teams/999999")
    assert response.status_code == 404


def test_update_team(client: TestClient, sample_team: Team):
    payload = {
        "project_title": "Enhanced Container Security Scanner",
        "demo_url": "https://updated-demo.local",
    }
    response = client.put(f"/api/teams/{sample_team.id}", json=payload)
    assert response.status_code == 200
    assert response.json()["project_title"] == "Enhanced Container Security Scanner"
    assert response.json()["status"] == "submitted"  # Auto-transitioned on demo submission


def test_team_status_transition_valid(client: TestClient, sample_team: Team):
    # Transition registered -> submitted
    response = client.patch(f"/api/teams/{sample_team.id}/status", json={"status": "submitted"})
    assert response.status_code == 200
    assert response.json()["status"] == "submitted"

    # Transition submitted -> under_review
    response2 = client.patch(f"/api/teams/{sample_team.id}/status", json={"status": "under_review"})
    assert response2.status_code == 200
    assert response2.json()["status"] == "under_review"


def test_team_status_transition_invalid(client: TestClient, sample_team: Team):
    # Cannot jump directly registered -> scored
    response = client.patch(f"/api/teams/{sample_team.id}/status", json={"status": "scored"})
    assert response.status_code == 422
    assert "Invalid lifecycle transition" in response.json()["detail"]


def test_team_stats_endpoint(client: TestClient, sample_team: Team):
    response = client.get(f"/api/teams/stats?event_id={sample_team.event_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["total_teams"] >= 1
    assert "by_status" in data
    assert "average_score" in data
    assert "judge_agreement_index" in data


def test_delete_team(client: TestClient, sample_team: Team):
    response = client.delete(f"/api/teams/{sample_team.id}")
    assert response.status_code == 204
    check = client.get(f"/api/teams/{sample_team.id}")
    assert check.status_code == 404
