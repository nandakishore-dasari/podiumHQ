"""
Criterion Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CriterionBase(BaseModel):
    round_id: int
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    max_score: float = Field(default=10.0, gt=0, le=100.0)
    weight: float = Field(default=0.25, gt=0.0, le=1.0)


class CriterionCreate(CriterionBase):
    pass


class CriterionResponse(CriterionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
