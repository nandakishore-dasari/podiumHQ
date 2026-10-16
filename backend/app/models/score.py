"""
Judge Score Model for PodiumHQ
Records individual criterion scores submitted by judges.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    Integer,
    Float,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    judge_id = Column(Integer, ForeignKey("judges.id", ondelete="CASCADE"), nullable=False, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)
    round_id = Column(Integer, ForeignKey("rounds.id", ondelete="CASCADE"), nullable=False, index=True)
    criterion_id = Column(Integer, ForeignKey("criteria.id", ondelete="CASCADE"), nullable=False, index=True)
    raw_score = Column(Float, nullable=False)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        UniqueConstraint(
            "judge_id",
            "team_id",
            "round_id",
            "criterion_id",
            name="uq_judge_team_round_criterion",
        ),
        Index("ix_scores_team_round", "team_id", "round_id"),
    )

    # Relationships
    judge = relationship("Judge", back_populates="scores")
    team = relationship("Team", back_populates="scores")
    round = relationship("Round", back_populates="scores")
    criterion = relationship("Criterion", back_populates="scores")
