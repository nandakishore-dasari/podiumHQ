"""
Judging Round Model for PodiumHQ
"""

import enum
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.app.database import Base


class RoundStatus(str, enum.Enum):
    PENDING = "pending"
    OPEN = "open"
    CLOSED = "closed"


class Round(Base):
    __tablename__ = "rounds"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    round_number = Column(Integer, nullable=False, default=1)
    name = Column(String(100), nullable=False)
    status = Column(Enum(RoundStatus), default=RoundStatus.OPEN, nullable=False)
    weight = Column(Float, default=1.0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    event = relationship("Event", back_populates="rounds")
    criteria = relationship("Criterion", back_populates="round", cascade="all, delete-orphan")
    scores = relationship("Score", back_populates="round", cascade="all, delete-orphan")
