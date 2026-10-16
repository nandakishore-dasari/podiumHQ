"""
Judging Criterion Model for PodiumHQ
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Criterion(Base):
    __tablename__ = "criteria"

    id = Column(Integer, primary_key=True, index=True)
    round_id = Column(Integer, ForeignKey("rounds.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    max_score = Column(Float, default=10.0, nullable=False)
    weight = Column(Float, default=0.25, nullable=False)  # Normalized criterion weight (e.g., 0.35 = 35%)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    round = relationship("Round", back_populates="criteria")
    scores = relationship("Score", back_populates="criterion", cascade="all, delete-orphan")
