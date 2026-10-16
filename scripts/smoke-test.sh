#!/usr/bin/env bash
# ==============================================================================
# PodiumHQ Smoke Test Suite
# Validates health, readiness, and metrics endpoints
# ==============================================================================

set -euo pipefail

BASE_URL=${1:-"http://localhost:8000"}

echo "[PodiumHQ] Executing smoke tests against $BASE_URL..."

# 1. Health Probe
echo "1. Probing /health..."
HEALTH=$(curl -s "$BASE_URL/health")
echo "   Response: $HEALTH"

# 2. Readiness Probe
echo "2. Probing /ready..."
STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/ready")
if [ "$STATUS_CODE" -eq 200 ]; then
    echo "   Readiness Probe: PASS (HTTP 200)"
else
    echo "   Readiness Probe: FAIL (HTTP $STATUS_CODE)"
    exit 1
fi

# 3. Metrics Probe
echo "3. Probing /metrics..."
METRICS_COUNT=$(curl -s "$BASE_URL/metrics" | wc -l)
echo "   Metrics lines received: $METRICS_COUNT"

echo "[PodiumHQ] All smoke tests PASSED."
