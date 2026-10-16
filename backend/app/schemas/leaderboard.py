"""
Leaderboard Schemas
"""

from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel


class RoundScoreBreakdown(BaseModel):
    round_name: str
    round_number: int
    score: float
    weight: float


class LeaderboardEntry(BaseModel):
    rank: int
    previous_rank: int
    rank_delta: int  # Positive means climbed up, negative dropped
    team_id: int
    team_name: str
    project_title: str
    track: str
    status: str
    composite_score: float
    rounds_breakdown: List[RoundScoreBreakdown] = []
    criteria_scores: Dict[str, float] = {}
    total_evaluations: int
    submission_time: Optional[datetime] = None


class LeaderboardResponse(BaseModel):
    event_id: int
    event_name: str
    generated_at: datetime
    active_round: str
    total_ranked_teams: int
    rankings: List[LeaderboardEntry]
