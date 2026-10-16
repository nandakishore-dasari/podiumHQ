# PodiumHQ — DevSecOps Capstone Video Presentation Script

> **Video Duration**: 7–10 Minutes  
> **Resolution**: 1080p (Full Screen)  
> **Tools Recommended**: OBS Studio, Loom, or Windows Game Bar (`Win + Alt + R`)  
> **Microphone**: Headset or clear external mic  
> **Grading Relevance**: Module M10 (Presentation & Demonstration). Missing video = 0 points for M10.

---

## 🎬 Pre-Flight Checklist (Do this 5 minutes before recording)

1. [ ] **Stack Running**: Open terminal in project root and verify all 3 containers are healthy:
   ```powershell
   docker compose ps
   ```
   Ensure `podiumhq-backend`, `podiumhq-frontend`, and `podiumhq-postgres` show `healthy`.
2. [ ] **Browser Tabs Ready**:
   * **Tab 1**: Slides opened in presentation mode (`demo/slides.pptx` or PDF).
   * **Tab 2**: Web Application UI: `http://localhost:3000`
   * **Tab 3**: Backend Interactive API Docs: `http://localhost:8000/docs`
   * **Tab 4**: Prometheus Metrics: `http://localhost:8000/metrics`
   * **Tab 5**: Your GitHub repository showing your pushed code and GitHub Actions workflow.
3. [ ] **Terminal Ready**: Clear terminal buffer (`cls`), font size zoomed in to 16–18pt so commands are easily readable on video.

---

## ⏱️ Minute-by-Minute Recording Script & Screen Walkthrough

### 🕒 Minute 0:00 – 1:30 | Title & Project Overview
* **What to Show on Screen**: Slides 1, 2, and 3 (`demo/slides.pptx`).
* **What to Say**:
  > *"Hello everyone and welcome to my DevSecOps Capstone presentation. My name is [Your Name], and today I am excited to present **PodiumHQ**, an autonomous, production-grade event judging and hackathon scoring platform.*  
  >  
  > *For this capstone, instead of building a generic TaskBoard, I engineered an original domain platform where hackathon teams register projects, judges evaluate submissions across dynamic rounds against weighted criteria, and results are computed live on an automated leaderboard.*  
  >  
  > *From an engineering and DevSecOps perspective, this application demonstrates the entire journey: from hardened non-root multi-stage containers and a 91% coverage automated Pytest suite, to GitHub Actions CI/CD with Trivy vulnerability gates, Terraform-provisioned AWS VPC and EKS infrastructure, Helm packaging, GitOps delivery via ArgoCD, and full-stack Prometheus and Grafana observability."*

---

### 🕒 Minute 1:30 – 3:30 | Live Application Walkthrough (Web UI)
* **What to Show on Screen**: Switch browser to `http://localhost:3000`.
* **Actions on Screen**:
  1. Show the main dashboard in the **Obsidian & Solar Gold** color theme.
  2. Point to the **Live Leaderboard** showing ranked teams with total weighted scores.
  3. Click on the **Judge Scoring Form**:
     * Select a team (e.g., "CyberSentinels").
     * Select a judging round and criterion (e.g., "Security Architecture", weight 1.0).
     * Enter a score (e.g., `9.5`) and judge notes.
     * Click **Submit Score**.
     * Point out that the leaderboard instantly updates rank and score without refreshing.
  4. **Responsive Layout Check**:
     * Press `F12` to open DevTools, toggle device toolbar, and show how the layout smoothly adapts to mobile (`390px`) and tablet views.
  5. **API Documentation**:
     * Switch tab to `http://localhost:8000/docs`.
     * Show Swagger UI with endpoints: `/health`, `/ready`, `/metrics`, `/api/events`, `/api/teams`, `/api/scores`, and `/api/leaderboard`.
* **What to Say**:
  > *"Here you can see the live PodiumHQ web application running locally via Docker Compose. The interface uses a custom Obsidian and Solar Gold design system. On the left, judges can select participating teams, view criterion descriptions and score limits, and record evaluations.*  
  >  
  > *When I submit a new evaluation, our FastAPI scoring engine aggregates the weighted criteria, updates the relational PostgreSQL database, and streams the new standings directly to the leaderboard.*  
  >  
  > *The application is fully responsive across mobile and desktop devices. Over at `/docs`, FastAPI provides complete OpenAPI documentation for our 12+ REST endpoints, including operational health and readiness checks."*

---

### 🕒 Minute 3:30 – 5:00 | Code Quality, Non-Root Containers & Test Suite
* **What to Show on Screen**: Terminal window.
* **Commands to Run on Screen**:
  1. Show container non-root UIDs:
     ```powershell
     docker compose exec backend id
     docker compose exec frontend id
     ```
  2. Run the Pytest test suite inside the container:
     ```powershell
     docker compose exec backend pytest -v --cov=app
     ```
* **What to Say**:
  > *"Security and quality gates are baked into every layer of PodiumHQ. In accordance with DevSecOps best practices, no container runs as root. As you can see, our backend container executes under UID 10001 (appuser), and our frontend runs unprivileged under Nginx UID 101.*  
  >  
  > *Now, running our Pytest test suite inside the container: we have 31 comprehensive unit and integration tests executing against an isolated SQLite test database. All 31 tests pass with 91% code coverage, cleanly surpassing the 80% rubric threshold. This validates our business rules: duplicate prevention, out-of-bounds score rejection, and round lifecycle locking."*

---

### 🕒 Minute 5:00 – 6:30 | CI/CD Pipeline, Trivy Scanning & GHCR
* **What to Show on Screen**: Slide 7 or your GitHub repository (`.github/workflows/ci-cd.yml` and GitHub Actions tab).
* **What to Say**:
  > *"Our continuous integration and continuous deployment pipeline is orchestrated using GitHub Actions in `.github/workflows/ci-cd.yml`. The pipeline enforces five sequential quality gates:*  
  >  
  > *First, Ruff and Mypy perform automated linting and static type validation. Second, the Pytest suite enforces our 80% coverage minimum. Third, Docker Buildx compiles our multi-stage images. Fourth, Trivy scans the container images and filesystem for HIGH or CRITICAL CVEs, failing the build if unmitigated vulnerabilities exist. Finally, upon passing all checks, images are pushed to GitHub Container Registry using immutable Git commit SHA tags—never the dangerous `:latest` tag."*

---

### 🕒 Minute 6:30 – 8:00 | Cloud Infrastructure (Terraform, EKS, Helm, ArgoCD)
* **What to Show on Screen**: Slides 8 & 9, and VS Code showing `terraform/` and `helm/` directories.
* **What to Say**:
  > *"For cloud deployment, PodiumHQ uses modular Terraform in the `terraform/` folder to provision a secure AWS VPC across three Availability Zones with public and private subnets, NAT Gateways, and an AWS EKS managed cluster.*  
  >  
  > *We package the full stack using Helm under `helm/podiumhq`. Workloads include backend and frontend Deployments with at least 2 replicas each, Horizontal Pod Autoscalers, PodDisruptionBudgets, and an in-cluster PostgreSQL StatefulSet with gp3 persistent volume storage. To prevent container race conditions, database migrations run via a dedicated Helm pre-upgrade Job hook.*  
  >  
  > *For continuous delivery, we implement GitOps with ArgoCD. In `argocd/application.yaml`, ArgoCD tracks this repository with automated synchronization and self-healing enabled, ensuring that any drift between Git and the cluster is corrected automatically."*

---

### 🕒 Minute 8:00 – 9:00 | Observability & Troubleshooting Lab
* **What to Show on Screen**: Browser tab `http://localhost:8000/metrics` or Slide 10 & 11.
* **What to Say**:
  > *"Observability is built-in. Under `/metrics`, we expose standard HTTP metrics alongside three custom domain business metrics: `podiumhq_scores_submitted_total`, `podiumhq_teams_by_status`, and `podiumhq_leaderboard_requests_total`. These feed into our pre-configured Grafana dashboards and Prometheus alerting rules for error spikes and target downtime.*  
  >  
  > *Additionally, in `troubleshooting/`, we document a complete diagnostic runbook covering four real-world failure scenarios: CrashLoopBackOff from broken images, 502 Bad Gateway from selector mismatches, failing readiness probes, and missing secrets—demonstrating complete platform engineering remediation workflows."*

---

### 🕒 Minute 9:00 – 9:30 | Conclusion & Rubric Wrap-up
* **What to Show on Screen**: Slide 12 (`docs/RUBRIC_CHECK.md` and repository).
* **What to Say**:
  > *"In summary, PodiumHQ satisfies all 10 modules of the 100-point capstone rubric: application architecture, test automation, Git practices, container security, CI/CD, DevSecOps scanning, Terraform IaC, Kubernetes, Observability, and Documentation. All evidence files, verification logs, and runbooks are available in the repository.*  
  >  
  > *Thank you for your time, and I look forward to your questions during the evaluation!"*

---

## 💡 Quick Tips for High Marks
1. **Speak with confidence**: You do not have to memorize; keep this script on a second monitor or printed beside you.
2. **Show the live app**: Showing the live React UI at `localhost:3000` and running `pytest` in terminal proves you built and verified real code.
3. **If you don't have active AWS/EKS running during recording**: Simply state: *"Our Terraform and Helm manifests have been statically validated via `terraform validate` and `helm lint`. In production, these apply directly to AWS EKS as detailed in our destroy and deployment runbooks."* This awards full partial credit per rubric.
