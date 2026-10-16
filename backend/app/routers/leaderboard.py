"""
Leaderboard Router for PodiumHQ
Provides real-time ranked results, round breakdowns, and rank delta indicators.
"""

from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.event import Event
from backend.app.models.round import Round, RoundStatus
from backend.app.schemas.leaderboard import LeaderboardResponse
from backend.app.services.scoring_engine import ScoringEngine
from backend.app.metrics import LEADERBOARD_REQUESTS_TOTAL

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("", response_model=LeaderboardResponse, summary="Get Live Event Leaderboard")
def get_leaderboard(
    event_id: Optional[int] = Query(None),
    event_slug: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Event)
    if event_id:
        event = query.filter(Event.id == event_id).first()
    elif event_slug:
        event = query.filter(Event.slug == event_slug).first()
    else:
        event = query.order_by(Event.created_at.desc()).first()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found for leaderboard generation.",
        )

    # Increment custom Prometheus metric
    LEADERBOARD_REQUESTS_TOTAL.labels(event_slug=event.slug).inc()

    # Determine current active round name
    active_round_obj = (
        db.query(Round)
        .filter(Round.event_id == event.id, Round.status == RoundStatus.OPEN)
        .order_by(Round.round_number.desc())
        .first()
    )
    active_round_label = active_round_obj.name if active_round_obj else "Evaluations Finalized"

    # Compute ranked leaderboard items
    rankings = ScoringEngine.compute_team_scores(db, event.id)

    return LeaderboardResponse(
        event_id=event.id,
        event_name=event.name,
        generated_at=datetime.now(timezone.utc),
        active_round=active_round_label,
        total_ranked_teams=len(rankings),
        rankings=rankings,
    )
