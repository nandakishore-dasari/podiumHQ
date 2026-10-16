#!/usr/bin/env bash
# ==============================================================================
# PodiumHQ HPA Load Generator
# Sends concurrent requests to simulate high judging traffic and trigger HPA scaling
# ==============================================================================

TARGET_URL=${1:-"http://localhost:8000/api/leaderboard"}
CONCURRENCY=${2:-10}
REQUESTS=${3:-1000}

echo "[PodiumHQ] Starting load test against $TARGET_URL..."
echo "[PodiumHQ] Concurrency: $CONCURRENCY | Total Requests: $REQUESTS"

if command -v hey &> /dev/null; then
    hey -n "$REQUESTS" -c "$CONCURRENCY" "$TARGET_URL"
elif command -v ab &> /dev/null; then
    ab -n "$REQUESTS" -c "$CONCURRENCY" "$TARGET_URL"
else
    echo "Running lightweight curl load loop..."
    for i in $(seq 1 "$REQUESTS"); do
        curl -s -o /dev/null "$TARGET_URL" &
        if (( i % CONCURRENCY == 0 )); then
            wait
        fi
    done
    wait
fi

echo "[PodiumHQ] Load test complete. Check 'kubectl get hpa -w' to view pod autoscaling."
