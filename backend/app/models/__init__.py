"""
SQLAlchemy Domain Models for PodiumHQ
"""

from backend.app.models.event import Event, EventStatus
from backend.app.models.team import Team, TeamStatus
from backend.app.models.judge import Judge
from backend.app.models.round import Round, RoundStatus
from backend.app.models.criterion import Criterion
from backend.app.models.score import Score

__all__ = [
    "Event",
    "EventStatus",
    "Team",
    "TeamStatus",
    "Judge",
    "Round",
    "RoundStatus",
    "Criterion",
    "Score",
]
