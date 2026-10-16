"""
Scores Router for PodiumHQ
Validates round openness, uniqueness constraints, max score limits,
and triggers Prometheus score metrics.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.metrics import record_score_submission
from backend.app.models.criterion import Criterion
from backend.app.models.judge import Judge
from backend.app.models.round import Round, RoundStatus
from backend.app.models.score import Score
from backend.app.models.team import Team, TeamStatus
from backend.app.schemas.score import (
    BatchScoreSubmission,
    ScoreCreate,
    ScoreResponse,
)

router = APIRouter(prefix="/scores", tags=["Scores"])


@router.get("", response_model=List[ScoreResponse], summary="List Evaluations")
def list_scores(
    team_id: Optional[int] = Query(None),
    judge_id: Optional[int] = Query(None),
    round_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Score)
    if team_id:
        query = query.filter(Score.team_id == team_id)
    if judge_id:
        query = query.filter(Score.judge_id == judge_id)
    if round_id:
        query = query.filter(Score.round_id == round_id)
    return query.order_by(Score.created_at.desc()).all()


@router.post("", response_model=ScoreResponse, status_code=status.HTTP_201_CREATED, summary="Submit Judge Evaluation")
def submit_score(payload: ScoreCreate, db: Session = Depends(get_db)):
    # 1. Validate round is OPEN
    round_obj = db.query(Round).filter(Round.id == payload.round_id).first()
    if not round_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Round not found")
    if round_obj.status != RoundStatus.OPEN:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Judging round '{round_obj.name}' is currently {round_obj.status.value}. Scoring is locked.",
        )

    # 2. Validate judge exists and is active
    judge = db.query(Judge).filter(Judge.id == payload.judge_id).first()
    if not judge or not judge.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Active judge not found")

    # 3. Validate team exists
    team = db.query(Team).filter(Team.id == payload.team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    if team.status == TeamStatus.DISQUALIFIED:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Cannot submit scores for a disqualified team.",
        )

    # 4. Validate criterion exists and matches round
    criterion = db.query(Criterion).filter(Criterion.id == payload.criterion_id).first()
    if not criterion or criterion.round_id != payload.round_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Criterion does not belong to the specified judging round.",
        )

    # 5. Check raw score bounds
    if payload.raw_score < 0.0 or payload.raw_score > criterion.max_score:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Score must be between 0.0 and maximum {criterion.max_score}.",
        )

    # 6. Check unique constraint (no duplicate score by same judge on same criterion)
    existing = (
        db.query(Score)
        .filter(
            Score.judge_id == payload.judge_id,
            Score.team_id == payload.team_id,
            Score.round_id == payload.round_id,
            Score.criterion_id == payload.criterion_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Judge has already submitted an evaluation for this criterion and team in this round.",
        )

    score_entry = Score(**payload.model_dump())
    db.add(score_entry)

    # If team was registered or submitted, advance to under_review or scored
    if team.status in [TeamStatus.REGISTERED, TeamStatus.SUBMITTED]:
        team.status = TeamStatus.SCORED

    try:
        db.commit()
        db.refresh(score_entry)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Duplicate score conflict detected.",
        )

    # Record Prometheus metrics
    record_score_submission(payload.round_id, criterion.name, payload.raw_score)

    return score_entry


@router.post(
    "/batch",
    response_model=List[ScoreResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Submit Batch Criteria Scores",
)
def submit_batch_scores(payload: BatchScoreSubmission, db: Session = Depends(get_db)):
    """Allows a judge to submit scores for all criteria of a round at once."""
    round_obj = db.query(Round).filter(Round.id == payload.round_id).first()
    if not round_obj or round_obj.status != RoundStatus.OPEN:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Judging round is not currently open.",
        )

    created_scores: List[Score] = []
    for item in payload.scores:
        score_input = ScoreCreate(
            judge_id=payload.judge_id,
            team_id=payload.team_id,
            round_id=payload.round_id,
            criterion_id=item.criterion_id,
            raw_score=item.raw_score,
            feedback=item.feedback,
        )
        score_res = submit_score(score_input, db)
        created_scores.append(score_res)

    return created_scores
