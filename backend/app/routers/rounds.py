"""
Judging Rounds and Criteria Router
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.round import Round, RoundStatus
from backend.app.models.criterion import Criterion
from backend.app.schemas.round import RoundCreate, RoundResponse
from backend.app.schemas.criterion import CriterionCreate, CriterionResponse

router = APIRouter(tags=["Rounds & Criteria"])


@router.get("/rounds", response_model=List[RoundResponse], summary="List Judging Rounds")
def list_rounds(event_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Round)
    if event_id:
        query = query.filter(Round.event_id == event_id)
    return query.order_by(Round.round_number.asc()).all()


@router.post("/rounds", response_model=RoundResponse, status_code=status.HTTP_201_CREATED, summary="Create Round")
def create_round(payload: RoundCreate, db: Session = Depends(get_db)):
    round_obj = Round(**payload.model_dump())
    db.add(round_obj)
    db.commit()
    db.refresh(round_obj)
    return round_obj


@router.get("/rounds/{round_id}", response_model=RoundResponse, summary="Get Round Details")
def get_round(round_id: int, db: Session = Depends(get_db)):
    round_obj = db.query(Round).filter(Round.id == round_id).first()
    if not round_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Round not found")
    return round_obj


@router.get("/criteria", response_model=List[CriterionResponse], summary="List Evaluation Criteria")
def list_criteria(round_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Criterion)
    if round_id:
        query = query.filter(Criterion.round_id == round_id)
    return query.order_by(Criterion.id.asc()).all()


@router.post("/criteria", response_model=CriterionResponse, status_code=status.HTTP_201_CREATED, summary="Add Criterion")
def create_criterion(payload: CriterionCreate, db: Session = Depends(get_db)):
    round_obj = db.query(Round).filter(Round.id == payload.round_id).first()
    if not round_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Round does not exist")
    criterion = Criterion(**payload.model_dump())
    db.add(criterion)
    db.commit()
    db.refresh(criterion)
    return criterion
