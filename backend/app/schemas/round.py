"""
Round Schemas
"""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from backend.app.models.round import RoundStatus


class RoundBase(BaseModel):
    event_id: int
    round_number: int = Field(default=1, ge=1)
    name: str = Field(..., min_length=2, max_length=100)
    status: RoundStatus = Field(default=RoundStatus.OPEN)
    weight: float = Field(default=1.0, ge=0.0, le=5.0)


class RoundCreate(RoundBase):
    pass


class RoundResponse(RoundBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
