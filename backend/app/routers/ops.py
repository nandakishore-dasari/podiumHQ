"""
Operational Endpoints Router
Exposes root metadata, liveness (/health), database readiness (/ready), and Prometheus metrics (/metrics).
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import text
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from backend.app.config import settings
from backend.app.database import get_db

router = APIRouter(tags=["Operations & Health"])


@router.get("/", summary="Service Information & Metadata")
def root_info():
    """Returns application name, semantic version, and operational links."""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "online",
        "documentation": "/docs",
        "health": "/health",
        "readiness": "/ready",
        "metrics": "/metrics",
    }


@router.get("/health", summary="Liveness Probe")
def liveness_probe():
    """Cheap probe returning 200 OK if the application process is running."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.APP_VERSION,
    }


@router.get("/ready", summary="Readiness Probe")
def readiness_probe(db: Session = Depends(get_db)):
    """
    Executes a SELECT 1 query on the database.
    Returns 200 OK when the database is accessible.
    Returns 503 Service Unavailable when the database connection fails.
    """
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ready",
            "database": "connected",
            "service": settings.PROJECT_NAME,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connectivity check failed: {str(exc)}",
        )


@router.get("/metrics", summary="Prometheus Telemetry Metrics")
def prometheus_metrics():
    """Outputs Prometheus metric telemetry for scraping by Prometheus Agent/Server."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
