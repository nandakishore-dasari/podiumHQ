#!/usr/bin/env bash
# ==============================================================================
# Out-of-band In-Cluster Secret Provisioner
# Creates PostgreSQL credentials secret directly in Kubernetes (Never in Git)
# ==============================================================================

set -euo pipefail

NAMESPACE=${1:-"podiumhq"}
DB_PASSWORD=${2:-"podium_secure_password_2026"}

echo "[PodiumHQ] Provisioning database secret in namespace: $NAMESPACE..."

kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic podiumhq-db-secret \
  --namespace="$NAMESPACE" \
  --from-literal=password="$DB_PASSWORD" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "[PodiumHQ] Secret 'podiumhq-db-secret' successfully created."
