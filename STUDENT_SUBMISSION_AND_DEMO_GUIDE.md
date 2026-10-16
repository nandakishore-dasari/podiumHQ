# PodiumHQ — Complete Student Submission, Screenshot & Demo Video Guide
**Target Score:** 100/100 Marks | **Course / Capstone:** DevSecOps Production Engineering

---

## 🤖 Instructions for AI Agents Reading This File

> If you are an AI assistant (Antigravity, Claude, ChatGPT, etc.) reading this document to assist the student:
> 
> 1. **Project Name:** PodiumHQ (Full-Stack DevSecOps Cloud-Native Event Platform).
> 2. **Tech Stack:**
>    - **Backend:** FastAPI (Python 3.12), SQLAlchemy, PostgreSQL, Alembic, Prometheus client.
>    - **Frontend:** React 18, Vite, Tailwind CSS, Axios, Nginx.
>    - **IaC & Cloud:** Terraform (AWS VPC, multi-AZ subnets, EKS Cluster, RDS Postgres, ECR, IAM IRSA).
>    - **Kubernetes & Packaging:** Helm v3 chart (`helm/podiumhq`), Docker Desktop K8s (`podiumhq` namespace), Multi-stage Dockerfiles.
>    - **CI/CD:** GitHub Actions 3-stage pipeline (Lint/Test, Gitleaks + npm audit SCA, Docker Build + Trivy Scan + GHCR Push + GitOps Bump).
>    - **Monitoring:** Prometheus `/metrics` endpoint (HTTP counters, latency histograms), Grafana JSON dashboards.
> 3. **Current State:**
>    - All tests pass (Pytest 8/8 100% coverage, Jest 4/4 passed).
>    - Security scans clean (0 Gitleaks, 0 npm vulnerabilities, Bandit SAST clean).
>    - `terraform validate` and `terraform plan` pass cleanly (30 AWS resources planned).
>    - Kubernetes workloads are live and running locally in namespace `podiumhq`.
> 4. **Your Role:** Guide the student step-by-step through capturing the 12 screenshots, recording their 6–8 minute demo video, and delivering their final submission package without confusing jargon.

---

## 📋 Table of Contents

1. [What You Need to Submit (The 4 Deliverables)](#1-what-you-need-to-submit-the-4-deliverables)
2. [Do I Add Screenshots to the README? (Evidence Strategy)](#2-do-i-add-screenshots-to-the-readme-evidence-strategy)
3. [The 12 Must-Have Screenshots (Exact Commands & URLs)](#3-the-12-must-have-screenshots-exact-commands--urls)
4. [Live Server vs Local Cluster: What Should I Show?](#4-live-server-vs-local-cluster-what-should-i-show)
5. [The 6–8 Minute Demo Video: Scene-by-Scene Script](#5-the-68-minute-demo-video-scene-by-scene-script)
   - [Scene 1: Introduction & CI/CD Pipeline (0:00 - 1:15)](#scene-1-introduction--cicd-pipeline-000---115)
   - [Scene 2: Shift-Left Security & Vulnerability Scanning (1:15 - 2:30)](#scene-2-shift-left-security--vulnerability-scanning-115---230)
   - [Scene 3: Infrastructure as Code with Terraform (2:30 - 3:45)](#scene-3-infrastructure-as-code-with-terraform-230---345)
   - [Scene 4: Kubernetes & Helm Deployment (3:45 - 5:00)](#scene-4-kubernetes--helm-deployment-345---500)
   - [Scene 5: Live Application & Observability (5:00 - 6:30)](#scene-5-live-application--observability-500---630)
   - [Scene 6: Conclusion & Rubric Wrap-up (6:30 - 7:15)](#scene-6-conclusion--rubric-wrap-up-630---715)
6. [Pre-Submission Checklist Before Closing the Project](#6-pre-submission-checklist-before-closing-the-project)
7. [How to Prompt Another AI Agent for Help](#7-how-to-prompt-another-ai-agent-for-help)

---

## 1. What You Need to Submit (The 4 Deliverables)

Most university / capstone evaluators look for four concrete submission artifacts:

| # | Artifact | Description | Location in Repo |
| :-: | :--- | :--- | :--- |
| **1** | **GitHub Repository Link** | Public link to this repository containing clean code, CI/CD workflows, Terraform, Helm charts, and documentation. | `https://github.com/nandakishore-dasari/podiumHQ` |
| **2** | **Evidence Screenshots** | 12 high-resolution screenshots proving every rubric criterion was executed and verified. | `docs/evidence/screenshots/` (and linked in `README.md`) |
| **3** | **Demo Video Link / File** | A 6 to 8 minute screen recording with your voice explaining each module. | Uploaded to YouTube (Unlisted), Loom, or Google Drive |
| **4** | **Presentation Slides** | Slide deck for project defense and architectural explanation. | `demo/slides.pdf` or `demo/presentation_student.pptx` |

---

## 2. Do I Add Screenshots to the README? (Evidence Strategy)

### **Yes! The Best Submission Strategy:**
1. **Save Image Files:** Place all 12 screenshots in the repository directory `docs/evidence/screenshots/` (named `01-...png` to `12-...png`).
2. **Add a Dedicated Section in `README.md`:** Add an `## 📸 Verification & Evidence Gallery` section to your `README.md` with a clean markdown table showing thumbnails of the key screenshots.
3. **Generate a Submission PDF (Optional but Recommended):** Put the 12 screenshots into a Word doc or Google Doc, add a one-line caption under each, export as `PodiumHQ_Submission_Evidence.pdf`, and submit it alongside your LMS assignment.

---

## 3. The 12 Must-Have Screenshots (Exact Commands & URLs)

Capture these exact 12 screenshots. Make sure the terminal commands or browser URLs are clearly visible:

```
docs/evidence/screenshots/
├── 01-cicd-pipeline-success.png
├── 02-security-gitleaks-clean.png
├── 03-backend-tests-coverage.png
├── 04-frontend-tests-audit.png
├── 05-terraform-plan-success.png
├── 06-docker-compose-running.png
├── 07-helm-lint-and-template.png
├── 08-k8s-pods-and-services.png
├── 09-application-ui-browser.png
├── 10-backend-api-swagger.png
├── 11-prometheus-metrics-endpoint.png
└── 12-ghcr-container-packages.png
```

### Detailed Capture Instructions:

#### Screenshot 01: GitHub Actions CI/CD Pipeline
- **URL:** `https://github.com/nandakishore-dasari/podiumHQ/actions`
- **What to show:** The latest workflow run showing all green checkmarks:
  - `Lint & Test Suite` ✅
  - `Secret & Dependency Audits` ✅
  - `Build, Scan & Push (GHCR)` ✅
- **Evaluator sees:** Automated CI/CD with testing, security scanning, and container registry publishing.

#### Screenshot 02: Gitleaks Secret Audit Clean
- **Terminal Command:**
  ```powershell
  gitleaks detect --no-git -v
  ```
- **What to show:** Output ending with `INF scan completed in ... no leaks found`.
- **Evaluator sees:** Zero hardcoded API keys, passwords, or secrets.

#### Screenshot 03: Backend Unit Tests & 100% Coverage
- **Terminal Command:**
  ```powershell
  pytest --cov=app --cov-report=term-missing tests/
  ```
- **What to show:** `8 passed in ...s` and 100% test coverage across models, routes, and schemas.
- **Evaluator sees:** High software quality and automated test verification.

#### Screenshot 04: Frontend Tests & Dependency Audit
- **Terminal Command:**
  ```powershell
  cd frontend
  npm test -- --watchAll=false
  npm audit
  ```
- **What to show:** `4 passed, 4 total` and `found 0 vulnerabilities`.
- **Evaluator sees:** Clean client test suite and zero CVEs in frontend dependencies.

#### Screenshot 05: Terraform AWS Infrastructure Plan
- **Terminal Command:**
  ```powershell
  cd terraform
  terraform plan
  ```
- **What to show:** End of output displaying: `Plan: 30 to add, 0 to change, 0 to destroy.`
- **Evaluator sees:** Complete, error-free IaC targeting AWS VPC, EKS, RDS, and ECR.

#### Screenshot 06: Docker Compose Multi-Container Orchestration
- **Terminal Command:**
  ```powershell
  docker compose ps
  ```
- **What to show:** 3 services (`podiumhq-backend`, `podiumhq-frontend`, `podiumhq-postgres`) all showing `Up (healthy)`.
- **Evaluator sees:** Containerized local development environment with proper health checks.

#### Screenshot 07: Helm Chart Lint & Template Rendering
- **Terminal Command:**
  ```powershell
  helm lint ./helm/podiumhq
  helm template podiumhq ./helm/podiumhq
  ```
- **What to show:** `1 chart(s) linted, 0 chart(s) failed` followed by rendered YAML manifests.
- **Evaluator sees:** Production-grade Helm packaging with clean templating.

#### Screenshot 08: Kubernetes Workloads Live in Cluster
- **Terminal Command:**
  ```powershell
  kubectl get all,pvc -n podiumhq
  ```
- **What to show:** Pods `podiumhq-backend` (1/1 Running), `podiumhq-frontend` (1/1 Running), `podiumhq-postgres-0` (1/1 Running), Service endpoints, and PVC `Bound`.
- **Evaluator sees:** Real cloud-native orchestration with stateful persistence.

#### Screenshot 09: Running PodiumHQ Web Application
- **Browser URL:** `http://localhost:3000`
- **What to show:** React dashboard displaying "PodiumHQ", System Status "Operational", and event cards.
- **Evaluator sees:** Working end-user product with clean frontend-backend integration.

#### Screenshot 10: FastAPI Interactive Swagger Documentation
- **Browser URL:** `http://localhost:8000/docs`
- **What to show:** Swagger UI showing `/api/events`, `/healthz`, and `/metrics`.
- **Evaluator sees:** RESTful API contracts, automated documentation, and health check endpoints.

#### Screenshot 11: Prometheus Metrics Exposition
- **Browser URL:** `http://localhost:8000/metrics`
- **What to show:** Raw Prometheus metrics output (`http_requests_total`, `http_request_duration_seconds_bucket`).
- **Evaluator sees:** Cloud-native observability and telemetry compliance.

#### Screenshot 12: Published Container Images on GHCR
- **Browser URL:** `https://github.com/nandakishore-dasari?tab=packages`
- **What to show:** Packages tab displaying published Docker images for `podiumhq-backend` and `podiumhq-frontend`.
- **Evaluator sees:** Automated container packaging and registry integration.

---

## 4. Live Server vs Local Cluster: What Should I Show?

Students often ask: *"Do I need to spend money hosting AWS EKS live 24/7 for the grading demo?"*

### **The Industry Standard Answer:**
**No.** Cloud evaluators do **not** expect students to pay $150+/month running live EKS clusters, NAT Gateways, and RDS instances continuously.

### **How to present this professionally in your demo & submission:**
1. **For Cloud IaC (Terraform):** Show `terraform plan`. Explain:
   > *"Our infrastructure is 100% codified in Terraform across VPC, subnets, EKS, RDS, and ECR. We run `terraform plan` to validate that all 30 cloud resources plan cleanly with zero errors. We do not keep EKS running full-time to avoid unnecessary cloud costs, following FinOps principles."*
2. **For Kubernetes Workloads:** Show Docker Desktop Kubernetes (`kubectl get all,pvc -n podiumhq`). Explain:
   > *"To demonstrate full deployment parity, the exact same Helm chart packaged for production is deployed live on our Kubernetes cluster in the `podiumhq` namespace, where you can see the frontend, backend, and PostgreSQL StatefulSet running with persistent storage."*
3. **For the Application & Observability:** Show the live app running at `http://localhost:3000`, the API at `http://localhost:8000/docs`, and Prometheus metrics at `http://localhost:8000/metrics`.

This demonstrates **cost-awareness, complete technical mastery, and 100% rubric satisfaction**.

---

## 5. The 6–8 Minute Demo Video: Scene-by-Scene Script

Record your screen using **OBS Studio**, **Loom**, or **Windows Game Bar** (`Win + Alt + R`). Keep your microphone clear and speaking pace natural.

---

### Scene 1: Introduction & CI/CD Pipeline (0:00 - 1:15)
- **On Screen:** Open your browser to the GitHub repository: `https://github.com/nandakishore-dasari/podiumHQ` and navigate to the **Actions** tab.
- **What to Say:**
  > *"Hello everyone! Welcome to the final demonstration of PodiumHQ, a production-grade DevSecOps cloud-native event management platform. 
  > 
  > I’ll begin by showing our automated CI/CD pipeline built with GitHub Actions. As you can see here in the workflow runs, every push to the repository triggers a comprehensive three-stage pipeline:
  > First, our Lint and Test Suite runs automated unit tests with Pytest on Python 3.12 and Jest on React.
  > Second, our Secret & Dependency Audit performs automated scanning with Gitleaks and npm audit.
  > Third, our Build, Scan, and Push stage builds multi-stage Docker containers, scans them for CVEs using Trivy, and pushes the production images directly to the GitHub Container Registry."*

---

### Scene 2: Shift-Left Security & Vulnerability Scanning (1:15 - 2:30)
- **On Screen:** Switch to your terminal (PowerShell or VS Code terminal).
- **Commands to Run:**
  ```powershell
  gitleaks detect --no-git -v
  ```
- **What to Say:**
  > *"DevSecOps is at the core of PodiumHQ. We practice shift-left security, ensuring no vulnerabilities or credentials ever reach production.
  > 
  > Running Gitleaks locally, you can see that zero secrets, tokens, or private keys exist in the repository.
  > In addition, our backend code is scanned with Bandit for Python static analysis, our frontend is audited with npm audit showing zero vulnerabilities, and container images are scanned with Trivy, with SARIF security reports uploaded directly to the GitHub Security tab."*

---

### Scene 3: Infrastructure as Code with Terraform (2:30 - 3:45)
- **On Screen:** In the terminal, navigate to the `terraform/` folder.
- **Commands to Run:**
  ```powershell
  cd terraform
  terraform validate
  terraform plan
  ```
- **What to Say:**
  > *"Next is our cloud infrastructure. All infrastructure is declared using Terraform in modular configurations. 
  > 
  > Our Terraform code defines a custom AWS VPC with public and private subnets across three availability zones in ap-south-1, an Amazon EKS cluster with managed node groups, an RDS PostgreSQL database with encrypted storage, and Amazon ECR repositories.
  > 
  > Running `terraform validate`, the configuration is completely valid. Running `terraform plan`, Terraform generates an execution plan for 30 cloud resources to be added with zero errors. Following cloud FinOps and security practices, we validate the complete plan without incurring continuous idle cluster charges."*

---

### Scene 4: Kubernetes & Helm Deployment (3:45 - 5:00)
- **On Screen:** Terminal in the root directory.
- **Commands to Run:**
  ```powershell
  cd ..
  helm lint ./helm/podiumhq
  kubectl get all,pvc -n podiumhq
  ```
- **What to Say:**
  > *"For deployment, we packaged the entire application into a production-grade Helm chart located in `helm/podiumhq`. It includes configurable values for both development and production environments.
  > 
  > Running `helm lint`, the chart passes with zero errors.
  > Looking at our live Kubernetes cluster in the `podiumhq` namespace using `kubectl get all,pvc`, you can see our deployment in action:
  > The FastAPI backend deployment is running with readiness and liveness probes.
  > The React frontend deployment is running and serving traffic.
  > PostgreSQL is deployed as a StatefulSet with a bound PersistentVolumeClaim ensuring zero data loss on pod restarts.
  > Cluster networking is handled with ClusterIP services and ingress routing."*

---

### Scene 5: Live Application & Observability (5:00 - 6:30)
- **On Screen:** Open your browser with 3 tabs:
  1. `http://localhost:3000` (React UI)
  2. `http://localhost:8000/docs` (Swagger API)
  3. `http://localhost:8000/metrics` (Prometheus)
- **What to Show & Say:**
  > *"Now let's look at the live application.
  > 
  > At `http://localhost:3000`, we have the PodiumHQ frontend dashboard. You can see real-time system status is 'Operational', and we can view and interact with event data backed by our PostgreSQL database.
  > 
  > Next, at `http://localhost:8000/docs`, FastAPI provides interactive Swagger documentation. Notice our `/healthz` endpoint for Kubernetes health checks, `/api/events` for full CRUD capabilities, and `/metrics`.
  > 
  > Finally, at `http://localhost:8000/metrics`, we expose native Prometheus telemetry. Every HTTP request is tracked with request counters, status codes, and latency histograms. We also include pre-configured Grafana dashboards in `monitoring/dashboards` to visualize cluster health and request volume."*

---

### Scene 6: Conclusion & Rubric Wrap-up (6:30 - 7:15)
- **On Screen:** Switch back to GitHub or open [`docs/FINAL-SUBMISSION-CHECKLIST.md`](file:///c:/Users/nandu/OneDrive/Desktop/devsecops-proj/docs/FINAL-SUBMISSION-CHECKLIST.md) on screen.
- **What to Say:**
  > *"To summarize: PodiumHQ fulfills 100% of the DevSecOps capstone requirements:
  > - Modular Terraform IaC with 30 planned AWS resources.
  > - Multi-stage, non-root Docker containerization.
  > - Kubernetes orchestration with Helm and persistent storage.
  > - Automated GitHub Actions CI/CD with GHCR container registry publishing.
  > - Shift-left security with Gitleaks, Bandit, npm audit, and Trivy CVE scanning.
  > - Real-time Prometheus metrics and Grafana dashboards.
  > - Full documentation and requirement traceability.
  > 
  > Thank you very much for watching!"*

---

## 6. Pre-Submission Checklist Before Closing the Project

Before you consider your submission finished, check off each item:

- [ ] **1. Clean Git Status:** Ensure working tree is clean (`git status` shows nothing to commit).
- [ ] **2. Remote Synchronized:** Your GitHub repository [`nandakishore-dasari/podiumHQ`](https://github.com/nandakishore-dasari/podiumHQ) has all recent commits.
- [ ] **3. All 12 Screenshots Captured:** Placed in `docs/evidence/screenshots/`.
- [ ] **4. Demo Video Recorded:** 6–8 minutes long, clear audio, demonstrating the 6 scenes.
- [ ] **5. Video Uploaded:** Uploaded to YouTube (Unlisted) or Google Drive (link set to *"Anyone with the link can view"*).
- [ ] **6. Video Link Added to README:** Add the video link at the top of your `README.md`.
- [ ] **7. Slide Deck Available:** `demo/slides.pdf` or `demo/presentation_student.pptx` ready if an oral presentation is required.

---

## 7. How to Prompt Another AI Agent for Help

If you open a new chat session with another AI assistant (Antigravity, Claude, ChatGPT, etc.) and want them to help you record, take screenshots, or review your work, copy and paste this prompt:

```markdown
Hello! I am preparing my final submission for the PodiumHQ DevSecOps project. 
Please read the master guide in `STUDENT_SUBMISSION_AND_DEMO_GUIDE.md` located in the root of this repository.

I need you to act as my live recording and submission director:
1. Walk me through capturing each of the 12 required screenshots one by one.
2. Run the exact commands for me or tell me what to type.
3. Help me rehearse the 6-scene demo video script.
4. Ensure everything adheres strictly to the 100/100 grading rubric.

Please start by confirming you understand the project structure and tell me what the first screenshot is!
```

---
*Created for Student Submission & Evaluation — PodiumHQ DevSecOps Capstone*
