"""
Team Schemas
"""

from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.team import TeamStatus


class TeamBase(BaseModel):
    event_id: int
    name: str = Field(..., min_length=2, max_length=100)
    project_title: str = Field(..., min_length=2, max_length=150)
    project_repo_url: Optional[str] = None
    demo_url: Optional[str] = None
    track: str = Field(default="Open Innovation", max_length=80)


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    project_title: Optional[str] = Field(None, min_length=2, max_length=150)
    project_repo_url: Optional[str] = None
    demo_url: Optional[str] = None
    track: Optional[str] = None


class TeamStatusUpdate(BaseModel):
    status: TeamStatus


class TeamResponse(TeamBase):
    id: int
    status: TeamStatus
    submitted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TeamStatsResponse(BaseModel):
    total_teams: int
    by_status: Dict[str, int]
    submitted_count: int
    under_review_count: int
    scored_count: int
    disqualified_count: int
    registered_count: int
    average_score: float
    judge_agreement_index: float  # Scale 0.0 - 1.0 (variance-based consensus metric)
