"""
Team Model for PodiumHQ
"""

import enum
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.app.database import Base


class TeamStatus(str, enum.Enum):
    REGISTERED = "registered"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    SCORED = "scored"
    DISQUALIFIED = "disqualified"


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    project_title = Column(String(150), nullable=False)
    project_repo_url = Column(String(255), nullable=True)
    demo_url = Column(String(255), nullable=True)
    track = Column(String(80), default="Open Innovation")
    status = Column(Enum(TeamStatus), default=TeamStatus.REGISTERED, nullable=False, index=True)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    event = relationship("Event", back_populates="teams")
    scores = relationship("Score", back_populates="team", cascade="all, delete-orphan")
