"""
Tests for Events CRUD Endpoints
"""

from fastapi.testclient import TestClient

from backend.app.models.event import Event


def test_create_event_success(client: TestClient):
    payload = {
        "name": "Cloud Native Summit Hackathon",
        "slug": "cloud-native-2026",
        "description": "Building next-gen distributed systems",
        "location": "Bengaluru / Virtual",
        "status": "active",
        "max_teams": 30,
    }
    response = client.post("/api/events", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["slug"] == payload["slug"]
    assert "id" in data


def test_create_event_duplicate_slug_conflict(client: TestClient, sample_event: Event):
    payload = {
        "name": "Conflicting Event",
        "slug": sample_event.slug,  # Duplicate slug
        "description": "Conflict test",
        "location": "Virtual",
        "status": "active",
        "max_teams": 10,
    }
    response = client.post("/api/events", json=payload)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_create_event_validation_error(client: TestClient):
    # Invalid slug with uppercase and spaces, missing name
    payload = {
        "slug": "INVALID SLUG!",
        "max_teams": -5,
    }
    response = client.post("/api/events", json=payload)
    assert response.status_code == 422


def test_list_events_pagination_and_search(client: TestClient, sample_event: Event):
    response = client.get("/api/events?page=1&page_size=5&search=Test")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1
    assert data["page"] == 1


def test_get_event_by_id(client: TestClient, sample_event: Event):
    response = client.get(f"/api/events/{sample_event.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_event.id
    assert data["name"] == sample_event.name


def test_get_event_not_found(client: TestClient):
    response = client.get("/api/events/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


def test_update_event(client: TestClient, sample_event: Event):
    update_payload = {"name": "Updated DevSecOps Arena Name", "max_teams": 75}
    response = client.put(f"/api/events/{sample_event.id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated DevSecOps Arena Name"
    assert response.json()["max_teams"] == 75


def test_delete_event(client: TestClient, sample_event: Event):
    response = client.delete(f"/api/events/{sample_event.id}")
    assert response.status_code == 204
    # Verify deletion
    check = client.get(f"/api/events/{sample_event.id}")
    assert check.status_code == 404
