"""
Pytest Test Fixtures and In-Memory Database Configuration
Uses SQLite with StaticPool to ensure test isolation with zero dependencies on real databases.
"""

import sys
from pathlib import Path
from typing import Generator

# Ensure both repo root and backend directory are in sys.path
_conftest_path = Path(__file__).resolve()
_backend_dir = _conftest_path.parent.parent
_repo_root = _backend_dir.parent
for _p in [str(_repo_root), str(_backend_dir)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Also ensure 'backend' can be resolved if executed directly from inside backend dir
if "backend" not in sys.modules and (_backend_dir / "app").exists():
    try:
        import backend  # noqa: F401
    except ImportError:
        import types
        _pkg = types.ModuleType("backend")
        _pkg.__path__ = [str(_backend_dir)]
        sys.modules["backend"] = _pkg

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.database import Base, get_db
from backend.app.main import app
from backend.app.models.criterion import Criterion
from backend.app.models.event import Event, EventStatus
from backend.app.models.judge import Judge
from backend.app.models.round import Round, RoundStatus
from backend.app.models.team import Team, TeamStatus

# In-memory SQLite engine with StaticPool for thread-safe test isolation
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Provides a transactional database session per test function."""
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """FastAPI TestClient with overridden get_db dependency."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_event(db_session: Session) -> Event:
    event = Event(
        name="Test DevSecOps Arena",
        slug="test-arena-2026",
        description="Integration testing arena for automated scoring",
        location="Virtual",
        status=EventStatus.ACTIVE,
        max_teams=20,
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)
    return event


@pytest.fixture
def sample_round(db_session: Session, sample_event: Event) -> Round:
    round_obj = Round(
        event_id=sample_event.id,
        round_number=1,
        name="Security Architecture",
        status=RoundStatus.OPEN,
        weight=1.0,
    )
    db_session.add(round_obj)
    db_session.commit()
    db_session.refresh(round_obj)
    return round_obj


@pytest.fixture
def sample_criterion(db_session: Session, sample_round: Round) -> Criterion:
    criterion = Criterion(
        round_id=sample_round.id,
        name="Non-Root & Hardening",
        description="Tests compliance with non-root security",
        max_score=10.0,
        weight=0.5,
    )
    db_session.add(criterion)
    db_session.commit()
    db_session.refresh(criterion)
    return criterion


@pytest.fixture
def sample_judge(db_session: Session) -> Judge:
    judge = Judge(
        name="Judge Dredd",
        email="judge.dredd@mega-city.gov",
        organization="Mega-City One Security",
        title="High Arbiter",
        is_active=True,
    )
    db_session.add(judge)
    db_session.commit()
    db_session.refresh(judge)
    return judge


@pytest.fixture
def sample_team(db_session: Session, sample_event: Event) -> Team:
    team = Team(
        event_id=sample_event.id,
        name="CyberShield Alpha",
        project_title="Container Security Scanner",
        project_repo_url="https://github.com/test/cybershield",
        demo_url="https://cybershield.local",
        track="DevSecOps",
        status=TeamStatus.REGISTERED,
    )
    db_session.add(team)
    db_session.commit()
    db_session.refresh(team)
    return team
