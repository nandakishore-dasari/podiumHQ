# PodiumHQ — Screenshot Evidence Guide (`SCREENSHOT-EVIDENCE-GUIDE.md`)

This guide provides the exact list of screenshots needed to prove compliance with each section of the grading rubric. Follow the numbered checklist below.

---

## 📸 Master Screenshot Checklist

| # | Screenshot Name | File Name Suggestion | What to Open / Command to Run | What Must Be Visible | Environment |
|---|---|---|---|---|---|
| **1** | **Application UI & Live Leaderboard** | `01-application-leaderboard.png` | Open browser: `http://localhost:3000` | Hackathon title, live team ranking table, score podium, judge filter dropdown | Local (`docker compose` or K8s) |
| **2** | **Judge Scoring Modal** | `02-judge-scoring-modal.png` | In `http://localhost:3000`, click "Score Project" on any team | Multi-criteria scoring sliders (Architecture, Security, Innovation), judge selection, dynamic score total | Local |
| **3** | **FastAPI Swagger Docs & Health** | `03-swagger-api-health.png` | Open browser: `http://localhost:8000/docs` | FastAPI Swagger UI showing `/health`, `/ready`, `/metrics`, and `/api/v1/scores` endpoints | Local |
| **4** | **Automated Tests & 91% Coverage** | `04-pytest-coverage-terminal.png` | Terminal: `docker compose exec backend python -m pytest -v --cov=app --cov-fail-under=80` | All 31 tests passing, green coverage table showing `TOTAL: 91%` | Local Terminal |
| **5** | **Non-Root Container Security** | `05-nonroot-containers.png` | Terminal: `docker compose exec backend id; docker compose exec frontend id` | `uid=10001(appuser)` for backend and `uid=101(nginx)` for frontend | Local Terminal |
| **6** | **GitHub Actions Green CI/CD Pipeline** | `06-github-actions-pipeline.png` | Open browser: `https://github.com/nandakishore-dasari/podiumHQ/actions` | All 4 jobs with green checkmarks: `Lint & Test Suite`, `Secret & Dependency Audits`, `Build, Scan & Push`, and `GitOps Bump` | GitHub Web UI |
| **7** | **Prometheus Scraped Metrics Stream** | `07-prometheus-metrics-endpoint.png` | Open browser: `http://localhost:8000/metrics` | Raw Prometheus exposition format showing `podiumhq_scores_submitted_total` and `http_requests_total` | Local Browser |
| **8** | **Grafana Dashboard Visualization** | `08-grafana-dashboard-monitoring.png` | Open `monitoring/grafana-dashboard.json` or Grafana UI | Visual panels showing HTTP Request Rate, 5xx Error Rate, P95 Latency, and Active Judges | Local / File |
| **9** | **Terraform Plan Execution (AWS)** | `09-terraform-plan-output.png` | Terminal in `terraform/`: `terraform plan` | `Plan: 30 to add, 0 to change, 0 to destroy.` showing AWS VPC, subnets, and EKS resources | Local Terminal (AWS authenticated) |
| **10** | **Live Kubernetes & Helm Deployment** | `10-kubernetes-helm-workloads.png` | Terminal: `kubectl get all,pvc -n podiumhq` | `podiumhq-backend` (1/1 Running), `podiumhq-frontend` (1/1 Running), `podiumhq-postgres-0` (1/1 Running), and PVC `Bound` | Local Kubernetes Cluster |
| **11** | **Git Commit History (>= 12 Commits)** | `11-git-commit-history.png` | Terminal: `git log --oneline -n 15` | Conventional commits list (`feat:`, `fix:`, `chore:`, `ci:`) showing $\ge 12$ atomic commits | Local Terminal |
| **12** | **Presentation Slide Deck Title Slide** | `12-presentation-deck.png` | Open `demo/slides.pdf` (Slide 1 or Slide 3 Architecture) | Clean dark-theme presentation slide with architecture diagram and author details | PDF Viewer |

---

## 📝 Step-by-Step Instructions to Capture Each Screenshot

### Screenshot 1 & 2: Application UI & Scoring Modal
1. Make sure Docker Compose or Kubernetes is running.
2. Open Google Chrome or Edge to `http://localhost:3000`.
3. Capture the full window showing the dark-gold dashboard (`01-application-leaderboard.png`).
4. Click the golden **"Score Project"** button on team "ZeroTrust Guard".
5. Capture the open modal with the scoring sliders (`02-judge-scoring-modal.png`).

### Screenshot 3: Swagger REST API Documentation
1. Navigate to `http://localhost:8000/docs`.
2. Expand the `GET /health` and `GET /ready` endpoints.
3. Capture the screen showing the interactive OpenAPI documentation (`03-swagger-api-health.png`).

### Screenshot 4 & 5: Pytest Coverage and Non-Root Verification
1. Open PowerShell in the project directory:
   ```powershell
   docker compose exec backend python -m pytest -v --cov=app --cov-report=term-missing --cov-fail-under=80
   ```
2. Take a screenshot showing `31 passed in ...` and `TOTAL ... 91%` (`04-pytest-coverage-terminal.png`).
3. Run the user identity checks:
   ```powershell
   docker compose exec backend id
   docker compose exec frontend id
   ```
4. Capture the terminal showing non-root UIDs `10001` and `101` (`05-nonroot-containers.png`).

### Screenshot 6: GitHub Actions Workflow
1. Visit `https://github.com/nandakishore-dasari/podiumHQ/actions`.
2. Click into the latest commit run.
3. Capture the workflow graph showing the sequential stages (`06-github-actions-pipeline.png`).

### Screenshot 7 & 8: Observability (Prometheus & Grafana)
1. In your browser, open `http://localhost:8000/metrics`.
2. Scroll to `podiumhq_scores_submitted_total` and capture (`07-prometheus-metrics-endpoint.png`).
3. Open `monitoring/grafana-dashboard.json` in VS Code or Grafana to show the dashboard schema (`08-grafana-dashboard-monitoring.png`).

### Screenshot 9: Terraform Infrastructure Plan
1. Open PowerShell and run:
   ```powershell
   cd terraform
   terraform plan
   ```
2. Capture the bottom summary block showing:
   ```text
   Plan: 30 to add, 0 to change, 0 to destroy.
   Changes to Outputs:
     + cluster_name = "podiumhq-eks"
     + vpc_id       = (known after apply)
   ```
   Save as `09-terraform-plan-output.png`.

### Screenshot 10: Kubernetes Workloads via Helm
1. Run in PowerShell:
   ```powershell
   kubectl get all,pvc -n podiumhq
   ```
2. Capture the output showing all pods `1/1 Running` and PVC `Bound` (`10-kubernetes-helm-workloads.png`).
