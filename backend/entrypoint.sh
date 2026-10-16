#!/bin/sh
set -e

# ==============================================================================
# PodiumHQ Backend Container Entrypoint
# Conditionally executes database migrations, then launches Uvicorn server.
# ==============================================================================

echo "[PodiumHQ] Initializing backend container runtime..."

if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "[PodiumHQ] RUN_MIGRATIONS=true detected. Executing Alembic database migrations..."
    alembic upgrade head
    echo "[PodiumHQ] Database migrations completed successfully."
else
    echo "[PodiumHQ] RUN_MIGRATIONS is not set to true. Skipping in-container migration."
fi

# If SEED_DATABASE is true, run idempotent seed
if [ "$SEED_DATABASE" = "true" ]; then
    echo "[PodiumHQ] SEED_DATABASE=true detected. Seeding sample hackathon data..."
    python -m backend.app.services.seed_data || true
fi

echo "[PodiumHQ] Launching Uvicorn ASGI server on port 8000..."
exec uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --workers 2 --access-log
