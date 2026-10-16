"""
API Routers Export
"""

from backend.app.routers.ops import router as ops_router
from backend.app.routers.events import router as events_router
from backend.app.routers.teams import router as teams_router
from backend.app.routers.judges import router as judges_router
from backend.app.routers.rounds import router as rounds_router
from backend.app.routers.scores import router as scores_router
from backend.app.routers.leaderboard import router as leaderboard_router

__all__ = [
    "ops_router",
    "events_router",
    "teams_router",
    "judges_router",
    "rounds_router",
    "scores_router",
    "leaderboard_router",
]
