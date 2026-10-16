"""
Teams Router for PodiumHQ
Provides full CRUD, lifecycle status state-machine transitions,
KPI statistics, pagination, and multi-field search.
"""

from datetime import datetime, timezone
from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.metrics import update_team_status_gauge
from backend.app.models.event import Event
from backend.app.models.score import Score
from backend.app.models.team import Team, TeamStatus
from backend.app.schemas.common import PaginatedResponse
from backend.app.schemas.team import (
    TeamCreate,
    TeamResponse,
    TeamStatsResponse,
    TeamStatusUpdate,
    TeamUpdate,
)
from backend.app.services.scoring_engine import ScoringEngine

router = APIRouter(prefix="/teams", tags=["Teams"])

# Valid state machine transitions
ALLOWED_TRANSITIONS = {
    TeamStatus.REGISTERED: [TeamStatus.SUBMITTED, TeamStatus.DISQUALIFIED],
    TeamStatus.SUBMITTED: [TeamStatus.UNDER_REVIEW, TeamStatus.DISQUALIFIED],
    TeamStatus.UNDER_REVIEW: [TeamStatus.SCORED, TeamStatus.DISQUALIFIED],
    TeamStatus.SCORED: [TeamStatus.UNDER_REVIEW, TeamStatus.DISQUALIFIED],
    TeamStatus.DISQUALIFIED: [TeamStatus.REGISTERED, TeamStatus.SUBMITTED],
}


@router.get("/stats", response_model=TeamStatsResponse, summary="Get Team Evaluation KPI Stats")
def get_team_stats(event_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """Computes summary KPI metrics for the executive dashboard."""
    query = db.query(Team)
    if event_id:
        query = query.filter(Team.event_id == event_id)

    teams = query.all()
    total_teams = len(teams)

    by_status: Dict[str, int] = {s.value: 0 for s in TeamStatus}
    for t in teams:
        by_status[t.status.value] = by_status.get(t.status.value, 0) + 1

    # Update metric gauge
    update_team_status_gauge(by_status)

    # Average score across all evaluations
    score_query = db.query(func.avg(Score.raw_score))
    if event_id:
        score_query = score_query.join(Team, Team.id == Score.team_id).filter(Team.event_id == event_id)
    avg_score_raw = score_query.scalar() or 0.0

    # Judge agreement / consensus index
    effective_event_id = event_id if event_id else (teams[0].event_id if teams else 1)
    consensus_index = ScoringEngine.calculate_judge_agreement_index(db, effective_event_id)

    return TeamStatsResponse(
        total_teams=total_teams,
        by_status=by_status,
        submitted_count=by_status.get(TeamStatus.SUBMITTED.value, 0),
        under_review_count=by_status.get(TeamStatus.UNDER_REVIEW.value, 0),
        scored_count=by_status.get(TeamStatus.SCORED.value, 0),
        disqualified_count=by_status.get(TeamStatus.DISQUALIFIED.value, 0),
        registered_count=by_status.get(TeamStatus.REGISTERED.value, 0),
        average_score=round(float(avg_score_raw), 2),
        judge_agreement_index=consensus_index,
    )


@router.get("", response_model=PaginatedResponse[TeamResponse], summary="List Teams")
def list_teams(
    event_id: Optional[int] = Query(None),
    status_filter: Optional[TeamStatus] = Query(None, alias="status"),
    track: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Team)
    if event_id:
        query = query.filter(Team.event_id == event_id)
    if status_filter:
        query = query.filter(Team.status == status_filter)
    if track:
        query = query.filter(Team.track.ilike(f"%{track}%"))
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Team.name.ilike(pattern),
                Team.project_title.ilike(pattern),
                Team.track.ilike(pattern),
            )
        )

    total = query.count()
    items = query.order_by(Team.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    pages = (total + page_size - 1) // page_size if total > 0 else 1

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED, summary="Register Team")
def register_team(payload: TeamCreate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == payload.event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target event ID {payload.event_id} does not exist.",
        )

    # Check team capacity
    current_count = db.query(Team).filter(Team.event_id == payload.event_id).count()
    if current_count >= event.max_teams:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Event has reached maximum team capacity of {event.max_teams}.",
        )

    # Check unique team name within event
    duplicate = db.query(Team).filter(Team.event_id == payload.event_id, Team.name.ilike(payload.name)).first()
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A team named '{payload.name}' is already registered in this event.",
        )

    team = Team(**payload.model_dump())
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


@router.get("/{team_id}", response_model=TeamResponse, summary="Get Team by ID")
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team


@router.put("/{team_id}", response_model=TeamResponse, summary="Update Team Information")
def update_team(team_id: int, payload: TeamUpdate, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    update_dict = payload.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(team, key, value)

    # If submitting repo or demo, conditionally update submitted_at
    if (payload.project_repo_url or payload.demo_url) and not team.submitted_at:
        team.submitted_at = datetime.now(timezone.utc)
        if team.status == TeamStatus.REGISTERED:
            team.status = TeamStatus.SUBMITTED

    db.commit()
    db.refresh(team)
    return team


@router.patch("/{team_id}/status", response_model=TeamResponse, summary="Transition Team Lifecycle Status")
def update_team_status(team_id: int, payload: TeamStatusUpdate, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    new_status = payload.status
    current_status = team.status

    if new_status == current_status:
        return team

    allowed = ALLOWED_TRANSITIONS.get(current_status, [])
    if new_status not in allowed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid lifecycle transition from '{current_status.value}' to '{new_status.value}'.",
        )

    team.status = new_status
    if new_status == TeamStatus.SUBMITTED and not team.submitted_at:
        team.submitted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(team)
    return team


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Team")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    db.delete(team)
    db.commit()
    return None
