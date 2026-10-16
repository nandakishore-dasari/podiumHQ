"""
Judges Router for PodiumHQ
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.judge import Judge
from backend.app.schemas.judge import JudgeCreate, JudgeResponse

router = APIRouter(prefix="/judges", tags=["Judges"])


@router.get("", response_model=List[JudgeResponse], summary="List All Evaluators")
def list_judges(active_only: bool = Query(True), db: Session = Depends(get_db)):
    query = db.query(Judge)
    if active_only:
        query = query.filter(Judge.is_active.is_(True))
    return query.order_by(Judge.name.asc()).all()


@router.post("", response_model=JudgeResponse, status_code=status.HTTP_201_CREATED, summary="Register Judge")
def create_judge(payload: JudgeCreate, db: Session = Depends(get_db)):
    existing = db.query(Judge).filter(Judge.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Judge with email '{payload.email}' already exists.",
        )
    judge = Judge(**payload.model_dump())
    db.add(judge)
    db.commit()
    db.refresh(judge)
    return judge


@router.get("/{judge_id}", response_model=JudgeResponse, summary="Get Judge Profile")
def get_judge(judge_id: int, db: Session = Depends(get_db)):
    judge = db.query(Judge).filter(Judge.id == judge_id).first()
    if not judge:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Judge not found")
    return judge
