"""
Score Schemas
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ScoreBase(BaseModel):
    judge_id: int
    team_id: int
    round_id: int
    criterion_id: int
    raw_score: float = Field(..., ge=0.0, le=10.0)
    feedback: Optional[str] = None


class ScoreCreate(ScoreBase):
    pass


class SingleCriterionScore(BaseModel):
    criterion_id: int
    raw_score: float = Field(..., ge=0.0, le=10.0)
    feedback: Optional[str] = None


class BatchScoreSubmission(BaseModel):
    judge_id: int
    team_id: int
    round_id: int
    scores: List[SingleCriterionScore]


class ScoreResponse(ScoreBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
