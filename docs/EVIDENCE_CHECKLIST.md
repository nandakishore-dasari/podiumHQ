# PodiumHQ — Rubric Evidence Checklist (`EVIDENCE_CHECKLIST.md`)

This document catalogs every item of evidence required by the 100-point Capstone Grading Rubric, specifying the command used to generate it, its location in the repository, and whether it was executed locally or requires cloud access.

---

## 📁 Evidence Files Inventory (`docs/evidence/`)

| Deliverable | Description | Command / Source | Target File | Verification Status |
|---|---|---|---|---|
| **Health Probe** | Backend `/health` liveness endpoint response | `curl.exe -s http://localhost:8000/health` | [`docs/evidence/health.txt`](file:///c:/Users/nandu/OneDrive/Desktop/devsecops-proj/docs/evidence/health.txt) | ✅ **Executed & Verified** (`{"status":"healthy",...}`) |
| **Readiness Probe** | Backend `/ready` readiness probe status code | `curl.exe -s -o NUL -w "%{http_code}" http://localhost:8000/ready` | [`docs/evidence/ready.txt`](file:///c:/Users/nandu/OneDrive/Desktop/devsecops-proj/docs/evidence/ready.txt) | ✅ **Executed & Verified** (`200 OK`) |
| **Prometheus Metrics** | Full `/metrics` Prometheus exposition stream | `curl.exe -s http://localhost:8000/metrics` | [`docs/evidence/metrics.txt`](file:///c:/Users/nandu/OneDrive/Desktop/devsecops-proj/docs/evidence/metrics.txt) | ✅ **Executed & Verified** (HTTP + Custom Domain Metrics) |
| **Non-Root Check** | In-container UID/GID security validation | `docker compose exec backend id` | [`docs/evidence/nonroot.txt`](file:///c:/Users/nandu/OneDrive/Desktop/devsecops-proj/docs/evidence/nonroot.txt) | ✅ **Executed & Verified** (`uid=10001(appuser)`) |
| **Test Suite & Coverage** | Pytest 31 tests execution and 91% coverage report | `docker compose exec backend pytest -v --cov=app` | [`docs/evidence/pytest-output.txt`](file:///c:/Users/nandu/OneDrive/Desktop/devsecops-proj/docs/evidence/pytest-output.txt) | ✅ **Executed & Verified** (31 passed in 1.32s, 91% cov) |
| **Web UI Dashboard** | PodiumHQ live leaderboard & scoring form | Browser at `http://localhost:3000` | Optional screenshot (`ui-screenshot.png`) | ✅ **Live in Container** |
| **Terraform Plan / Apply** | AWS VPC and EKS infrastructure plan | `terraform -chdir=terraform plan` | `docs/evidence/terraform-plan.txt` | 🟡 Human-only (Requires AWS Credentials) |
| **GitHub Actions Run** | Green CI/CD pipeline execution with Trivy | GitHub Actions web interface | GitHub Actions URL | 🟡 Human-only (Requires GitHub Remote Push) |
| **ArgoCD Sync Status** | GitOps Application Healthy & Synced state | `kubectl get application -n argocd` | `docs/evidence/argocd-sync.txt` | 🟡 Human-only (Requires Live Cluster) |
| **Grafana Dashboard** | Live telemetry panels and Prometheus graphs | Browser at `http://localhost:3000` (Grafana) | Optional screenshot (`grafana.png`) | 🟡 Human-only (Requires Prometheus Stack) |

---

## 🛠️ Step-by-Step Commands to Recreate Evidence

To regenerate all local evidence files in one pass:

```powershell
# 1. Start full Docker Compose stack
docker compose up --build -d

# 2. Capture backend health probe
curl.exe -s http://localhost:8000/health | Set-Content -Encoding utf8 docs/evidence/health.txt

# 3. Capture backend readiness probe HTTP code
curl.exe -s -o NUL -w "%{http_code}" http://localhost:8000/ready | Set-Content -Encoding utf8 docs/evidence/ready.txt

# 4. Capture Prometheus metrics
curl.exe -s http://localhost:8000/metrics | Set-Content -Encoding utf8 docs/evidence/metrics.txt

# 5. Capture non-root UID/GID verification
docker compose exec backend id | Set-Content -Encoding utf8 docs/evidence/nonroot.txt

# 6. Capture Pytest execution and coverage table
docker compose exec backend pytest -v --cov=app | Set-Content -Encoding utf8 docs/evidence/pytest-output.txt
```
