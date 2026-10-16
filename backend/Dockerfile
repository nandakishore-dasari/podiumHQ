# ==============================================================================
# Stage 1: Dependency Builder
# ==============================================================================
FROM python:3.12.6-slim AS builder

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ==============================================================================
# Stage 2: Hardened Non-Root Production Runtime
# ==============================================================================
FROM python:3.12.6-slim AS runtime

LABEL org.opencontainers.image.title="PodiumHQ Backend" \
      org.opencontainers.image.description="FastAPI Backend for PodiumHQ Hackathon & Event Judging Platform" \
      org.opencontainers.image.vendor="PodiumHQ" \
      org.opencontainers.image.authors="nandakishore-dasari" \
      org.opencontainers.image.source="https://github.com/nandakishore-dasari/podiumHQ"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:$PATH" \
    PYTHONPATH="/app:$PYTHONPATH"

# Install curl for HEALTHCHECK and ca-certificates
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user and group with explicit UID/GID
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/sh -m appuser

WORKDIR /app
RUN chown -R appuser:appgroup /app

# Copy installed python dependencies from builder
COPY --from=builder --chown=appuser:appgroup /root/.local /home/appuser/.local

# Copy application code, configuration, tests and migrations
COPY --chown=appuser:appgroup alembic.ini .
COPY --chown=appuser:appgroup pytest.ini .
COPY --chown=appuser:appgroup alembic/ ./alembic/
COPY --chown=appuser:appgroup app/ ./backend/app/
COPY --chown=appuser:appgroup tests/ ./tests/
COPY --chown=appuser:appgroup entrypoint.sh .

RUN touch ./backend/__init__.py && \
    ln -s /app/backend/app /app/app && \
    chmod +x entrypoint.sh && \
    chown -R appuser:appgroup /app

USER appuser:appgroup

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["./entrypoint.sh"]
