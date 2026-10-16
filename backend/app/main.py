"""
PodiumHQ FastAPI Application Entrypoint
Configures CORS, Request ID middleware, Prometheus instrumentation,
structured logging, and routers.
"""

import uuid
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from backend.app.config import settings
from backend.app.logging import setup_logging, request_id_ctx
from backend.app.database import engine, Base
from backend.app.routers import (
    ops_router,
    events_router,
    teams_router,
    judges_router,
    rounds_router,
    scores_router,
    leaderboard_router,
)

# Initialize structured logging
logger = setup_logging(settings.LOG_LEVEL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        f"Starting {settings.PROJECT_NAME} v{settings.APP_VERSION} in {settings.ENVIRONMENT} mode"
    )
    # Create tables if not running Alembic migrations
    Base.metadata.create_all(bind=engine)
    yield
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


app = FastAPI(
    title="PodiumHQ API",
    description="Production-grade Hackathon & Event Judging Platform Backend with DevSecOps telemetry.",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request ID and Latency Tracing Middleware
@app.middleware("http")
async def request_id_and_logging_middleware(request: Request, call_next):
    req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    token = request_id_ctx.set(req_id)
    start_time = time.perf_counter()

    try:
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Request-ID"] = req_id
        response.headers["X-Process-Time-Sec"] = f"{process_time:.4f}"

        logger.info(
            f"{request.method} {request.url.path} responded {response.status_code} in {process_time * 1000:.2f}ms"
        )
        return response
    except Exception as exc:
        process_time = time.perf_counter() - start_time
        logger.error(
            f"Unhandled exception on {request.method} {request.url.path}: {str(exc)}",
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "An internal server error occurred.",
                "request_id": req_id,
            },
            headers={"X-Request-ID": req_id},
        )
    finally:
        request_id_ctx.reset(token)


# Prometheus Instrumentator (exposes metrics and instruments endpoints)
Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    excluded_handlers=["/metrics", "/health"],
).instrument(app)

# Include Operations router at root
app.include_router(ops_router)

# Include Domain routers under /api prefix
app.include_router(events_router, prefix=settings.API_V1_PREFIX)
app.include_router(teams_router, prefix=settings.API_V1_PREFIX)
app.include_router(judges_router, prefix=settings.API_V1_PREFIX)
app.include_router(rounds_router, prefix=settings.API_V1_PREFIX)
app.include_router(scores_router, prefix=settings.API_V1_PREFIX)
app.include_router(leaderboard_router, prefix=settings.API_V1_PREFIX)
