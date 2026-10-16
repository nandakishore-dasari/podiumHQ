"""
Pydantic Schemas Export
"""

from backend.app.schemas.common import MessageResponse, PaginatedResponse
from backend.app.schemas.event import EventBase, EventCreate, EventUpdate, EventResponse
from backend.app.schemas.team import (
    TeamBase,
    TeamCreate,
    TeamUpdate,
    TeamStatusUpdate,
    TeamResponse,
    TeamStatsResponse,
)
from backend.app.schemas.judge import JudgeBase, JudgeCreate, JudgeResponse
from backend.app.schemas.round import RoundBase, RoundCreate, RoundResponse
from backend.app.schemas.criterion import CriterionBase, CriterionCreate, CriterionResponse
from backend.app.schemas.score import (
    ScoreBase,
    ScoreCreate,
    ScoreResponse,
    BatchScoreSubmission,
    SingleCriterionScore,
)
from backend.app.schemas.leaderboard import (
    LeaderboardEntry,
    LeaderboardResponse,
    RoundScoreBreakdown,
)

__all__ = [
    "MessageResponse",
    "PaginatedResponse",
    "EventBase",
    "EventCreate",
    "EventUpdate",
    "EventResponse",
    "TeamBase",
    "TeamCreate",
    "TeamUpdate",
    "TeamStatusUpdate",
    "TeamResponse",
    "TeamStatsResponse",
    "JudgeBase",
    "JudgeCreate",
    "JudgeResponse",
    "RoundBase",
    "RoundCreate",
    "RoundResponse",
    "CriterionBase",
    "CriterionCreate",
    "CriterionResponse",
    "ScoreBase",
    "ScoreCreate",
    "ScoreResponse",
    "BatchScoreSubmission",
    "SingleCriterionScore",
    "LeaderboardEntry",
    "LeaderboardResponse",
    "RoundScoreBreakdown",
]
