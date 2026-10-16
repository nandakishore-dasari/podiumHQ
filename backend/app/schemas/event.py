"""
Event Schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from backend.app.models.event import EventStatus


class EventBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    slug: str = Field(..., min_length=2, max_length=120, pattern=r"^[a-z0-9\-]+$")
    description: Optional[str] = None
    location: str = Field(default="Virtual / Hybrid")
    status: EventStatus = Field(default=EventStatus.ACTIVE)
    max_teams: int = Field(default=50, ge=1, le=500)


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=120)
    description: Optional[str] = None
    location: Optional[str] = None
    status: Optional[EventStatus] = None
    max_teams: Optional[int] = Field(None, ge=1, le=500)


class EventResponse(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
