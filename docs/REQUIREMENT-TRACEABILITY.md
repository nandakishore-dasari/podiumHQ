# PodiumHQ — Requirement Traceability Matrix (`REQUIREMENT-TRACEABILITY.md`)

This matrix maps every grading rubric requirement to its concrete codebase implementation, verification procedure, and corresponding evidence artifact.

---

| Rubric ID | Rubric Requirement | Codebase Implementation | Verification Command | Evidence Artifact |
|---|---|---|---|---|
| **M1.1** | Original Non-TaskBoard domain | `backend/app/models/` (Events, Rounds, Criteria, Teams, Judges, Scores) | `curl -f http://localhost:8000/api/v1/events` | `docs/evidence/ready.txt` |
| **M1.2** | Relational DB with $\ge 3$ tables | PostgreSQL 16 schema with 6 relational tables and foreign keys | `docker compose exec postgres psql -U podium_user -d podiumhq_db -c "\dt"` | Container runtime logs |
| **M1.3** | Automated schema migrations | `backend/alembic/` (001 initial, 002 constraints) | Run at container startup via `entrypoint.sh` | Container stdout |
| **M1.4** | REST API with $\ge 8$ endpoints | `backend/app/routers/` (15 REST endpoints) | Open `http://localhost:8000/docs` | Screenshot `03-swagger-api-health.png` |
| **M1.5** | Liveness & readiness probes | `backend/app/routers/ops.py` (`/health`, `/ready`) | `curl -f http://localhost:8000/health; curl -f http://localhost:8000/ready` | `docs/evidence/health.txt`, `ready.txt` |
| **M1.6** | Responsive frontend UI | `frontend/src/` (React 18, Tailwind, Leaderboard, Modals) | Open `http://localhost:3000` in browser | Screenshot `01-application-leaderboard.png` |
| **M2.1** | Pytest suite ($\ge 15$ tests) | `backend/tests/` (31 tests across all domains) | `python -m pytest -v` | `docs/evidence/pytest-output.txt` |
| **M2.2** | Test coverage $\ge 80\%$ | `backend/pytest.ini` (`--cov-fail-under=80`) | `pytest --cov=app` (achieved 91.22%) | `docs/evidence/pytest-output.txt` |
| **M2.3** | Isolated test database | `backend/tests/conftest.py` (SQLite `StaticPool`) | Pytest session execution | `docs/evidence/pytest-output.txt` |
| **M2.4** | Static code linters | `backend/ruff.toml`, `backend/mypy.ini` | `ruff check backend` | Terminal stdout (0 errors) |
| **M3.1** | Clean commit history | 19 Conventional Commits on `main` branch | `git log --oneline` | Screenshot `11-git-commit-history.png` |
| **M3.2** | Zero committed secrets | `.gitignore`, `.env.example`, `terraform.tfvars.example` | Gitleaks scan via `.gitleaks.toml` | CI Gitleaks step log |
| **M3.3** | PR template & branch strategy | `.github/pull_request_template.md`, protected `main` | Review GitHub repo settings | `.github/pull_request_template.md` |
| **M4.1** | Multi-stage Docker builds | `backend/Dockerfile`, `frontend/Dockerfile` | `docker compose build` | Docker build logs |
| **M4.2** | Non-root containers | `appuser` (10001) in backend, `nginx` (101) in frontend | `docker compose exec backend id; docker compose exec frontend id` | `docs/evidence/nonroot.txt` |
| **M4.3** | Docker Compose orchestration | `docker-compose.yml` (backend, frontend, postgres) | `docker compose ps` | `docs/evidence/nonroot.txt` |
| **M4.4** | Immutable tagging | Commit SHA tagging in `.github/workflows/ci-cd.yml` | Review workflow artifact tags | GitHub Actions logs |
| **M5.1** | Automated CI quality gates | `.github/workflows/ci-cd.yml` (Lint, Test, Build, Push) | Trigger push to GitHub `main` | Screenshot `06-github-actions-pipeline.png` |
| **M5.2** | Native container build | Docker build within GitHub Actions runner | CI runner execution | GitHub Actions logs |
| **M5.3** | GHCR image push | Pushed to `ghcr.io/nandakishore-dasari/...` with commit SHA | Check GHCR package registry | GitHub Packages |
| **M5.4** | GitOps tag bump | `gitops-bump` job updates `values-prod.yaml` | Git log check on `main` | Git commit history |
| **M6.1** | Trivy vulnerability scan | Aqua Security Trivy image scan with SARIF export | Workflow step `Trivy Vulnerability Scan` | GitHub Security tab |
| **M6.2** | Secret detection | Gitleaks scanner running in CI | Workflow step `Run Gitleaks Secret Scanner` | GitHub Actions logs |
| **M7.1** | AWS VPC across $\ge 2$ AZs | `terraform/vpc.tf` (3 AZs: `ap-south-1a, b, c`) | `terraform plan` | `docs/evidence/terraform-plan.txt` |
| **M7.2** | Managed AWS EKS Cluster | `terraform/eks.tf` (Kubernetes 1.30 control plane) | `terraform plan` | `docs/evidence/terraform-plan.txt` |
| **M7.3** | EKS Add-ons | `terraform/addons.tf` (EBS CSI Driver, VPC CNI) | `terraform plan` | `docs/evidence/terraform-plan.txt` |
| **M7.4** | Teardown runbook | `terraform/README.md` (clean `terraform destroy` guide) | Code review | `terraform/README.md` |
| **M8.1** | Production Helm chart | `helm/podiumhq/` (Chart.yaml, templates, values) | `helm lint helm/podiumhq` | Helm lint output (0 errors) |
| **M8.2** | High-availability manifests | `helm/podiumhq/templates/` (Deployments, HPA, PDB) | `helm template podiumhq helm/podiumhq` | `docs/evidence/helm-rendered.yaml` |
| **M8.3** | In-Cluster DB StatefulSet | `helm/podiumhq/templates/postgres.yaml` (PVC Bound) | `kubectl get pvc -n podiumhq` | `docs/evidence/k8s-workloads.txt` |
| **M8.4** | Live cluster deployment | Deployed into local Kubernetes cluster via Helm | `kubectl get all -n podiumhq` | `docs/evidence/k8s-workloads.txt` |
| **M8.5** | ArgoCD GitOps manifest | `argocd/application.yaml` (automated self-healing) | Manifest inspection | `argocd/application.yaml` |
| **M9.1** | Prometheus `/metrics` | `backend/app/metrics.py` (HTTP duration, counts) | `curl -f http://localhost:8000/metrics` | `docs/evidence/metrics.txt` |
| **M9.2** | Custom business metrics | `podiumhq_scores_submitted_total`, `active_judges` | `curl -f http://localhost:8000/metrics` | `docs/evidence/metrics.txt` |
| **M9.3** | Custom Grafana dashboard | `monitoring/grafana-dashboard.json` (6 panels) | File inspection / Grafana import | `monitoring/grafana-dashboard.json` |
| **M9.4** | Alerting rules | `monitoring/alerts.yaml` (HighLatency, PodDown) | PrometheusRule inspection | `monitoring/alerts.yaml` |
| **M10.1** | Master README | `README.md` (Architecture, Quickstart, Runbooks) | Markdown view | `README.md` |
| **M10.2** | Presentation deck | `demo/presentation.pptx` and `demo/slides.pdf` | View presentation | `demo/slides.pdf` |
| **M10.3** | Video recording script | `docs/VIDEO_SCRIPT.md` (Minute-by-minute transcript) | Markdown review | `docs/VIDEO_SCRIPT.md` |
| **M10.4** | Verification evidence | `docs/evidence/` (Raw logs from actual runs) | File review | `docs/evidence/` directory |
