"""
Tests for Scoring, Rounds, Criteria, and Live Leaderboard
"""

from fastapi.testclient import TestClient

from backend.app.models.criterion import Criterion
from backend.app.models.event import Event
from backend.app.models.judge import Judge
from backend.app.models.round import Round, RoundStatus
from backend.app.models.team import Team


def test_judges_and_rounds_crud(client: TestClient, sample_event: Event):
    # Register judge
    j_payload = {
        "name": "Sarah Connor",
        "email": "sarah.connor@resistance.net",
        "organization": "Cyberdyne Defense",
        "title": "Threat Modeling Lead",
        "is_active": True,
    }
    j_res = client.post("/api/judges", json=j_payload)
    assert j_res.status_code == 201
    judge_id = j_res.json()["id"]

    # List judges
    list_res = client.get("/api/judges")
    assert list_res.status_code == 200
    assert any(j["id"] == judge_id for j in list_res.json())

    # Create Round
    r_payload = {
        "event_id": sample_event.id,
        "round_number": 2,
        "name": "Finals Demo Pitch",
        "status": "open",
        "weight": 1.5,
    }
    r_res = client.post("/api/rounds", json=r_payload)
    assert r_res.status_code == 201
    round_id = r_res.json()["id"]

    # Add Criterion
    c_payload = {
        "round_id": round_id,
        "name": "Live Resilience Demonstration",
        "max_score": 10.0,
        "weight": 0.4,
    }
    c_res = client.post("/api/criteria", json=c_payload)
    assert c_res.status_code == 201
    assert c_res.json()["name"] == c_payload["name"]


def test_submit_score_success(
    client: TestClient,
    sample_judge: Judge,
    sample_team: Team,
    sample_round: Round,
    sample_criterion: Criterion,
):
    score_payload = {
        "judge_id": sample_judge.id,
        "team_id": sample_team.id,
        "round_id": sample_round.id,
        "criterion_id": sample_criterion.id,
        "raw_score": 9.5,
        "feedback": "Outstanding Kubernetes PodDisruptionBudget setup.",
    }
    response = client.post("/api/scores", json=score_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["raw_score"] == 9.5
    assert data["team_id"] == sample_team.id


def test_submit_score_duplicate_conflict(
    client: TestClient,
    sample_judge: Judge,
    sample_team: Team,
    sample_round: Round,
    sample_criterion: Criterion,
):
    score_payload = {
        "judge_id": sample_judge.id,
        "team_id": sample_team.id,
        "round_id": sample_round.id,
        "criterion_id": sample_criterion.id,
        "raw_score": 9.0,
        "feedback": "Initial evaluation",
    }
    first_res = client.post("/api/scores", json=score_payload)
    assert first_res.status_code == 201

    # Second submission must trigger 409 Conflict (R1/M1 business rule)
    second_res = client.post("/api/scores", json=score_payload)
    assert second_res.status_code == 409
    assert "already submitted an evaluation" in second_res.json()["detail"]


def test_submit_score_when_round_closed(
    client: TestClient,
    db_session,
    sample_judge: Judge,
    sample_team: Team,
    sample_round: Round,
    sample_criterion: Criterion,
):
    # Lock the judging round
    sample_round.status = RoundStatus.CLOSED
    db_session.commit()

    score_payload = {
        "judge_id": sample_judge.id,
        "team_id": sample_team.id,
        "round_id": sample_round.id,
        "criterion_id": sample_criterion.id,
        "raw_score": 8.0,
    }
    response = client.post("/api/scores", json=score_payload)
    assert response.status_code == 422
    assert "Scoring is locked" in response.json()["detail"]


def test_submit_score_out_of_bounds(
    client: TestClient,
    sample_judge: Judge,
    sample_team: Team,
    sample_round: Round,
    sample_criterion: Criterion,
):
    # Exceeds max_score of 10.0
    score_payload = {
        "judge_id": sample_judge.id,
        "team_id": sample_team.id,
        "round_id": sample_round.id,
        "criterion_id": sample_criterion.id,
        "raw_score": 15.0,
    }
    response = client.post("/api/scores", json=score_payload)
    assert response.status_code == 422


def test_batch_score_submission(
    client: TestClient,
    sample_judge: Judge,
    sample_team: Team,
    sample_round: Round,
    sample_criterion: Criterion,
):
    batch_payload = {
        "judge_id": sample_judge.id,
        "team_id": sample_team.id,
        "round_id": sample_round.id,
        "scores": [
            {
                "criterion_id": sample_criterion.id,
                "raw_score": 8.7,
                "feedback": "Batch scored item",
            }
        ],
    }
    response = client.post("/api/scores/batch", json=batch_payload)
    assert response.status_code == 201
    assert len(response.json()) == 1


def test_leaderboard_endpoint(
    client: TestClient,
    sample_event: Event,
    sample_judge: Judge,
    sample_team: Team,
    sample_round: Round,
    sample_criterion: Criterion,
):
    # Submit score first
    client.post(
        "/api/scores",
        json={
            "judge_id": sample_judge.id,
            "team_id": sample_team.id,
            "round_id": sample_round.id,
            "criterion_id": sample_criterion.id,
            "raw_score": 9.2,
        },
    )

    response = client.get(f"/api/leaderboard?event_id={sample_event.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["event_name"] == sample_event.name
    assert data["total_ranked_teams"] >= 1
    top_entry = data["rankings"][0]
    assert top_entry["rank"] == 1
    assert top_entry["composite_score"] > 0
    assert "rank_delta" in top_entry
    assert len(top_entry["rounds_breakdown"]) >= 1
