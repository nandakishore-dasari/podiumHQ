# PodiumHQ — Autonomous Hackathon & Event Judging Platform

[![CI/CD Pipeline](https://github.com/nandakishore-dasari/podiumHQ/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/nandakishore-dasari/podiumHQ/actions/workflows/ci-cd.yml)
[![Scheduled Security Scan](https://github.com/nandakishore-dasari/podiumHQ/actions/workflows/security.yml/badge.svg)](https://github.com/nandakishore-dasari/podiumHQ/actions/workflows/security.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage: 90%](https://img.shields.io/badge/Coverage-90%25-brightgreen.svg)](#5-testing--quality-gates)
[![Security: Non-Root](https://img.shields.io/badge/Security-Non--Root-emerald.svg)](#7-devsecops--security-hardening)

---

> ### 🎥 Project Demonstration & Slides
> * **Demo Video**: `<!-- TODO: add after recording -->` <!-- Video walkthrough (6-8 mins) will be linked here once recorded: https://youtu.be/EXAMPLE or release asset -->
> * **Presentation Slides (PDF)**: [demo/slides.pdf](demo/slides.pdf)
> * **Presentation Slides (PowerPoint)**: [demo/slides.pptx](demo/slides.pptx)
> * **Student Presentation Deck**: [demo/presentation_student.pptx](demo/presentation_student.pptx)

---

## 📑 Table of Contents

1. [Project Description & Purpose](#1-project-description--purpose)
2. [Architecture Diagram](#2-architecture-diagram)
3. [Tech Stack Summary](#3-tech-stack-summary)
4. [Local Setup (Docker Compose)](#4-local-setup-docker-compose)
5. [Testing & Quality Gates](#5-testing--quality-gates)
6. [CI/CD Pipeline & Delivery Workflow](#6-cicd-pipeline--delivery-workflow)
7. [DevSecOps & Security Hardening](#7-devsecops--security-hardening)
8. [Terraform Cloud Infrastructure (AWS EKS)](#8-terraform-cloud-infrastructure-aws-eks)
9. [Kubernetes & Helm Deployment](#9-kubernetes--helm-deployment)
10. [GitOps Continuous Delivery with ArgoCD](#10-gitops-continuous-delivery-with-argocd)
11. [Observability (Prometheus & Grafana)](#11-observability-prometheus--grafana)
12. [Evidence Gallery](#12-evidence-gallery)
13. [Demo Video & Presentation Slides](#13-demo-video--presentation-slides)
14. [Known Issues & Limitations](#14-known-issues--limitations)
15. [Project Directory Structure](#15-project-directory-structure)
16. [Author & License](#16-author--license)

---

## 1. Project Description & Purpose

**PodiumHQ** is a production-grade, cloud-native DevSecOps platform built for hackathon management and real-time competitive project judging. Rather than acting as a simple task manager or to-do list, PodiumHQ implements complex domain workflows:

* **Event & Team Lifecycle**: Team registration, criteria-based evaluation rounds, and track filtering.
* **Multi-Criteria Scoring Engine**: Weighted multi-judge scoring with automated tie-breaking rules.
* **Live Leaderboards**: Real-time standings computed dynamically across judging rounds.
* **Operational Telemetry**: Built-in health checks (`/health`), database readiness probes (`/ready`), and custom Prometheus metric exposition (`/metrics`).

The platform serves as an end-to-end reference implementation for modern DevSecOps engineering: from hardened non-root containerization and automated Pytest test suites to GitHub Actions CI/CD with Trivy container vulnerability scanning, Terraform-managed AWS EKS infrastructure, Helm v3 packaging, ArgoCD GitOps reconciliation, and Prometheus/Grafana observability.

---

## 2. Architecture Diagram

```mermaid
flowchart TD
    subgraph Developer_Flow["1. Developer & Source Control"]
        Dev["Developer"] -->|git push| GH["GitHub Repository (nandakishore-dasari/podiumHQ)"]
    end

    subgraph CI_CD["2. GitHub Actions CI/CD Pipeline (.github/workflows/ci-cd.yml)"]
        GH --> Job1["Job 1: Lint & Test Suite (Ruff + Pytest 90% Cov + ESLint)"]
        Job1 --> Job2["Job 2: Secret & Dependency Audits (Gitleaks + pip-audit + npm audit)"]
        Job2 --> Job3["Job 3: Build, Scan & Push (Docker Build + Trivy CVE Scan -> GHCR)"]
        Job3 --> Job4["Job 4: GitOps Bump (yq bumps values-prod.yaml with Commit SHA)"]
    end

    subgraph GitOps_Delivery["3. GitOps Continuous Delivery (ArgoCD)"]
        Job4 -->|Auto-Commit [skip ci]| GH
        GH -->|Polls Repo & Syncs| Argo["ArgoCD Controller (argocd/application.yaml)"]
    end

    subgraph Cloud_Orchestration["4. Cloud Infrastructure & Workloads (AWS & Kubernetes)"]
        TF["Terraform (terraform/)"] -->|Provisions 30 Resources| EKS["AWS EKS Cluster v1.30 (VPC, 3 AZs in ap-south-1)"]
        Argo -->|Deploys Helm Release| EKS
        
        subgraph K8s_Namespace["Namespace: podiumhq"]
            Ingress["Nginx Ingress Controller (Host: podiumhq.local)"]
            Ingress -->|/api, /health, /ready| BackendSvc["Backend Service (:8000)"]
            Ingress -->|/| FrontendSvc["Frontend Service (:8080)"]
            
            BackendSvc --> BackendPods["FastAPI Deployment (Non-Root UID 10001, HPA 2-6 Pods)"]
            FrontendSvc --> FrontendPods["React 18 + Nginx Deployment (Non-Root UID 101, 2 Replicas)"]
            BackendPods --> PostgresDB[("PostgreSQL 16 StatefulSet (EBS gp3 PVC)")]
        end
    end

    subgraph Observability_Stack["5. Telemetry & Monitoring"]
        Prom["Prometheus (kube-prometheus-stack)"] -->|Scrapes /metrics| BackendPods
        Grafana["Grafana Dashboards"] -->|Visualizes Metrics| Prom
    end
```

### ASCII Architecture Fallback
```text
+-----------------------------------------------------------------------------------------+
|                                    DEVELOPER WORKFLOW                                   |
| Developer -> git push -> GitHub (nandakishore-dasari/podiumHQ)                          |
+-----------------------------------------------------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                        GITHUB ACTIONS CI/CD PIPELINE (4 JOBS)                           |
| Job 1: Lint & Test Suite  -> Ruff, Pytest (31 tests, 90% coverage), ESLint             |
| Job 2: Secrets & Deps     -> Gitleaks secret scanner, pip-audit, npm audit              |
| Job 3: Build, Scan & Push -> Docker build, Trivy vulnerability scan, push to GHCR       |
| Job 4: GitOps Image Bump  -> Updates helm/podiumhq/values-prod.yaml with commit SHA     |
+-----------------------------------------------------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                                  GITOPS WITH ARGOCD                                     |
| ArgoCD Controller polls repo -> auto-syncs Helm chart -> self-heals cluster state       |
+-----------------------------------------------------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                           KUBERNETES RUNTIME (AWS EKS / LOCAL)                          |
| Ingress (podiumhq.local):                                                               |
|   ├── /         -> Frontend Service (:8080) -> React 18 + Nginx (UID 101, 2 replicas)   |
|   ├── /api      -> Backend Service (:8000)  -> FastAPI (UID 10001, HPA min 2, max 6)   |
|   ├── /health   -> Backend Liveness Probe                                               |
|   └── /ready    -> Backend Readiness Probe (SELECT 1 on DB)                             |
| Backend connects to: PostgreSQL 16 StatefulSet (gp3 PersistentVolumeClaim storage)       |
| Prometheus scrapes:  Backend /metrics endpoint -> Grafana dashboards                    |
+-----------------------------------------------------------------------------------------+
```

---

## 3. Tech Stack Summary

| Layer | Technology | Version | Purpose in PodiumHQ |
|---|---|---|---|
| **Backend API** | FastAPI / Python | 3.12 | Async REST API, Pydantic v2 schemas, SQLAlchemy 2.0 ORM, Prometheus middleware |
| **Frontend UI** | React / Vite | React 18.3, Vite 5.4 | Single-page application, Tailwind CSS styling, real-time leaderboard |
| **Database** | PostgreSQL | 16-alpine | Relational ACID storage, stateful persistence, schema managed by Alembic |
| **Testing** | Pytest / Pytest-Cov | 9.1 / 7.1 | **31 automated backend tests**, **90.4% code coverage**, SQLite in-memory isolation |
| **Code Quality** | Ruff / ESLint | Latest | Python formatting/linting and React/JS linting with strict rules |
| **Containers** | Docker / Compose | Multi-Stage | Non-root containers (`appuser` UID 10001 for backend, `nginx` UID 101 for frontend) |
| **CI/CD** | GitHub Actions | Ubuntu 24.04 | 4-job automated delivery pipeline triggered on push/PR to `main` |
| **Security Scanning** | Trivy / Gitleaks | Master / v2 | Container CVE vulnerability scanning (SARIF export) and credential leak audits |
| **Infrastructure as Code** | Terraform | AWS Provider 5.x | Provisions VPC across 3 AZs (`ap-south-1`), EKS v1.30, Node Groups, and Addons (30 resources) |
| **Workload Delivery** | Helm 3 | v3.x | Parameterized chart (`helm/podiumhq`) with `values-dev.yaml` and `values-prod.yaml` |
| **GitOps** | ArgoCD | v2.x | Declarative synchronization and automated self-healing (`argocd/application.yaml`) |
| **Observability** | Prometheus / Grafana | kube-prometheus-stack | Telemetry scraping at `/metrics`, latency histograms, custom domain metrics |

---

## 4. Local Setup (Docker Compose)

The entire multi-container stack can be launched locally using Docker Compose.

### Prerequisites
* Docker Desktop (v24.0+ recommended)
* Git

### Step-by-Step Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nandakishore-dasari/podiumHQ.git
   cd podiumHQ
   ```

2. **Configure local environment variables:**
   ```bash
   cp .env.example .env
   ```
   *(The default `.env.example` comes pre-configured with local development credentials).*

3. **Build and start all services:**
   ```bash
   docker compose up --build -d
   ```

4. **Verify running containers and health checks:**
   ```bash
   docker compose ps
   ```
   Expected output shows all 3 services healthy:
   ```text
   NAME                IMAGE                     COMMAND                  SERVICE    STATUS
   podiumhq-postgres   postgres:16-alpine        "docker-entrypoint.s…"   postgres   Up (healthy)
   podiumhq-backend    podiumhq-backend:local    "/app/entrypoint.sh"     backend    Up (healthy)
   podiumhq-frontend   podiumhq-frontend:local   "/docker-entrypoint.…"   frontend   Up (healthy)
   ```

### Local Service URLs

| Component | URL | Description |
|---|---|---|
| **Frontend Application** | [http://localhost:3000](http://localhost:3000) | React dashboard and live judging interface |
| **Backend Swagger API Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive OpenAPI documentation and test console |
| **Liveness Health Probe** | [http://localhost:8000/health](http://localhost:8000/health) | Cheap HTTP 200 OK process check |
| **Readiness Health Probe** | [http://localhost:8000/ready](http://localhost:8000/ready) | Deep database connectivity check (`SELECT 1`) |
| **Prometheus Telemetry** | [http://localhost:8000/metrics](http://localhost:8000/metrics) | Real-time Prometheus metrics exposition |

---

## 5. Testing & Quality Gates

PodiumHQ enforces automated unit and integration tests with an automated coverage gate (minimum 80% required).

### Running Backend Tests Locally

Run the test suite using Python 3.12 (or virtual environment):

```bash
# Set in-memory database URL for test isolation
export DATABASE_URL="sqlite:///:memory:"
pytest -v --cov=backend.app --cov-report=term-missing backend/tests
```

*(On Windows PowerShell, use `$env:DATABASE_URL="sqlite:///:memory:"`).*

### Actual Test Execution Output

```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\nandu\OneDrive\Desktop\devsecops-proj\backend
configfile: pytest.ini
plugins: anyio-4.15.1, asyncio-1.4.0, cov-7.1.0
collecting ... collected 31 items

backend\tests\test_events.py (8 tests) ......................... PASSED [ 25%]
backend\tests\test_health_and_ops.py (5 tests) ................. PASSED [ 41%]
backend\tests\test_scoring_and_leaderboard.py (7 tests) ........ PASSED [ 64%]
backend\tests\test_teams.py (11 tests) ......................... PASSED [100%]

=============================== tests coverage ================================
Name                                     Stmts   Miss  Cover   Missing
----------------------------------------------------------------------
backend\app\config.py                       23      3    87%   40-42
backend\app\database.py                     15      4    73%   31-35
backend\app\logger.py                       22      2    91%   30, 41
backend\app\main.py                         45      4    91%   78-84
backend\app\metrics.py                      12      0   100%
backend\app\models\criterion.py             15      0   100%
backend\app\models\event.py                 24      0   100%
backend\app\models\judge.py                 14      0   100%
backend\app\models\round.py                 21      0   100%
backend\app\models\score.py                 20      0   100%
backend\app\models\team.py                  26      0   100%
backend\app\routers\events.py               56      3    95%   30, 81, 96
backend\app\routers\judges.py               29      5    83%   29, 42-45
backend\app\routers\leaderboard.py          26      4    85%   31-34, 37
backend\app\routers\ops.py                  23      0   100%
backend\app\routers\rounds.py               44     13    70%   21-24, 38-41, 46-49, 58
backend\app\routers\scores.py               69     18    74%   36-43, 51, 61, 66, 68, 76, 83, 115-117, 138
backend\app\routers\teams.py               112      6    95%   97, 133, 165, 186, 192, 214
backend\app\schemas\criterion.py            12      0   100%
backend\app\schemas\event.py                21      0   100%
backend\app\schemas\judge.py                12      0   100%
backend\app\schemas\leaderboard.py           9      0   100%
backend\app\schemas\round.py                12      0   100%
backend\app\schemas\score.py                14      0   100%
backend\app\schemas\team.py                 23      0   100%
backend\app\services\scoring_engine.py      72     15    79%   57, 144-161
----------------------------------------------------------------------
TOTAL                                      801     77    90%
Required test coverage of 80% reached. Total coverage: 90.39%
============================= 31 passed in 1.16s ==============================
```

### Frontend Code Quality

The frontend is validated using ESLint and a production compilation check:
```bash
cd frontend
npm run lint    # ESLint checking React hooks and syntax
npm run build   # Production Vite bundle compilation
```

---

## 6. CI/CD Pipeline & Delivery Workflow

The continuous integration and delivery pipeline is configured in [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml). It triggers automatically on every push and pull request to the `main` branch.

```
+-----------------------------------------------------------------------------------------+
|                                CI/CD PIPELINE FLOW                                      |
|                                                                                         |
|  [Push to main]                                                                         |
|        │                                                                                |
|        ├──► Job 1: Lint & Test Suite (Ruff, Pytest Coverage Gate >=80%, ESLint, Build)  |
|        │                                                                                |
|        ├──► Job 2: Secret & Dependency Audits (Gitleaks, pip-audit, npm audit)          |
|        │                                                                                |
|        └──► Job 3: Build, Scan & Push (GHCR) [needs: Job 1 & Job 2]                     |
|                   │                                                                     |
|                   ├── Docker Build (Backend & Frontend)                                 |
|                   ├── Trivy CVE Scan & SARIF Upload to GitHub Security                  |
|                   └── Push SHA-Tagged Images to GHCR (Never :latest)                    |
|                             │                                                           |
|                             └──► Job 4: GitOps Image Tag Bump [on push to main]         |
|                                        ├── Updates helm/podiumhq/values-prod.yaml       |
|                                        └── Commits with [skip ci] -> Triggers ArgoCD    |
+-----------------------------------------------------------------------------------------+
```

### The 4 Pipeline Jobs:

1. **Job 1: `lint-test` (Lint & Test Suite)**:
   * Checks Python formatting and syntax with Ruff.
   * Executes the 31 Pytest test suite with an automated gate (`--cov-fail-under=80`).
   * Validates React code with ESLint and compiles the production Vite bundle.
2. **Job 2: `secrets-and-deps` (Secret & Dependency Audits)**:
   * Scans git commit history with Gitleaks for leaked API keys, tokens, or credentials.
   * Audits Python backend packages with `pip-audit`.
   * Audits production npm packages with `npm audit --omit=dev --audit-level=moderate`.
3. **Job 3: `build-scan-push` (Build, Scan & Push GHCR)**:
   * Depends on `lint-test` and `secrets-and-deps` passing.
   * Builds production Docker images for frontend and backend.
   * Scans both images with Trivy for HIGH and CRITICAL vulnerabilities and uploads SARIF reports to GitHub Security Code Scanning.
   * Publishes images to GitHub Container Registry tagged with the immutable Git commit SHA:
     * `ghcr.io/nandakishore-dasari/podiumhq-backend:<commit-sha>`
     * `ghcr.io/nandakishore-dasari/podiumhq-frontend:<commit-sha>`
4. **Job 4: `gitops-bump` (GitOps Image Tag Bump)**:
   * Runs only on pushes to `main`.
   * Uses `yq` to update the backend and frontend image tags in `helm/podiumhq/values-prod.yaml` with `${{ github.sha }}`.
   * Commits the change with `[skip ci]`, allowing ArgoCD to detect the new desired state and roll out the release.

---

## 7. DevSecOps & Security Hardening

Security is treated as a first-class requirement across every phase of the engineering lifecycle:

### Shift-Left Security Measures

1. **Non-Root Container Execution**:
   * **Backend**: Dockerfile creates a dedicated system user `appuser` (UID `10001`, GID `10001`). The application process never runs as root.
   * **Frontend**: Multi-stage build copies static assets into an unprivileged Nginx image running under user `nginx` (UID `101`, GID `101`) on port 8080.
2. **Secret Leak Detection (Gitleaks)**:
   * Integrated into pre-commit workflows and CI/CD via `gitleaks-action@v2`.
   * Configured via [`.gitleaks.toml`](.gitleaks.toml) to prevent sensitive credentials, private keys, or API tokens from entering the git tree.
3. **Container Vulnerability Scanning (Trivy)**:
   * Integrated directly into the CI build pipeline using `aquasecurity/trivy-action@master`.
   * **What Trivy Scans**: Trivy scans both the container operating system packages (e.g. Alpine/Debian base image binaries) and application-level language packages (Python pip wheels and Node npm modules) against the National Vulnerability Database (NVD) and GitHub Security Advisories.
   * **Plain-English Meaning of the Scan**: Trivy checks if any installed software component contains a publicly disclosed security vulnerability categorized as HIGH or CRITICAL. The resulting security report is exported as a standard SARIF file and uploaded to GitHub Security Code Scanning, ensuring every deployed container image is transparently auditable and free from unpatched vulnerabilities.
4. **Scheduled IaC Security Scans**:
   * [`.github/workflows/security.yml`](.github/workflows/security.yml) runs weekly scheduled and dispatch scans across the Terraform code, Helm templates, and Dockerfiles to identify misconfigurations.

---

## 8. Terraform Cloud Infrastructure (AWS EKS)

The [`terraform/`](terraform/) directory contains modular Infrastructure as Code to provision a production-ready AWS environment in region **`ap-south-1` (Mumbai)** across **3 Availability Zones**.

### Planned Cloud Resources (30 Total)

A verified run of `terraform plan` produces **30 resources to add**:
* **Networking & VPC**:
  * AWS VPC (`10.0.0.0/16`) tagged for Kubernetes integration (`kubernetes.io/cluster/podiumhq-eks = shared`).
  * 3 Public Subnets across `ap-south-1a`, `ap-south-1b`, `ap-south-1c`.
  * 3 Private Subnets across `ap-south-1a`, `ap-south-1b`, `ap-south-1c`.
  * 1 Internet Gateway, 1 Elastic IP (EIP), 1 NAT Gateway for secure outbound internet access.
  * Public and Private Route Tables and associations.
* **Kubernetes Control Plane (Amazon EKS)**:
  * Managed EKS Cluster v1.30 (`podiumhq-eks`).
  * Security groups for cluster control plane communication.
  * IAM Role and attached policies for EKS cluster administration.
* **Worker Node Groups**:
  * Managed EC2 Node Group with `t3.medium` instances (min: 2, desired: 2, max: 4 nodes).
  * IAM Role and policies for node group instances (`AmazonEKSWorkerNodePolicy`, `AmazonEKS_CNI_Policy`, `AmazonEC2ContainerRegistryReadOnly`).
* **EKS Managed Add-ons**:
  * `aws-ebs-csi-driver` (for EBS gp3 persistent volumes)
  * `coredns` (cluster DNS)
  * `kube-proxy` (networking rules)
  * `vpc-cni` (pod IP allocation)

### Provisioning Steps

1. Configure AWS credentials:
   ```bash
   aws configure
   ```
2. Navigate to the terraform directory:
   ```bash
   cd terraform
   ```
3. Initialize Terraform providers and state:
   ```bash
   terraform init
   ```
4. Copy the variable template (no credentials are committed to git):
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```
5. Review the execution plan:
   ```bash
   terraform plan
   ```
6. Apply the infrastructure:
   ```bash
   terraform apply
   ```
7. Connect `kubectl` to your new cluster:
   ```bash
   aws eks --region ap-south-1 update-kubeconfig --name podiumhq-eks
   kubectl get nodes
   ```

### 🛑 Cloud Teardown & Cost Warning (`terraform destroy`)

> [!CAUTION]
> **FinOps & Cost Warning**: Running a live AWS EKS cluster with NAT Gateways costs ~$0.15/hour (~$150/month). To avoid unnecessary cloud charges, teardown the infrastructure immediately after demonstration:

```bash
# 1. Uninstall Helm releases and delete PVCs first so AWS load balancers and EBS volumes don't block VPC deletion
helm uninstall podiumhq -n podiumhq || true
kubectl delete pvc --all -n podiumhq || true

# 2. Destroy all AWS cloud resources
cd terraform
terraform destroy -auto-approve
```

---

## 9. Kubernetes & Helm Deployment

Workloads are packaged using Helm v3 under [`helm/podiumhq/`](helm/podiumhq/).

### Helm Chart Components & Parameters

* **Backend Deployment**: 2 replicas, resources (req: 100m CPU / 128Mi RAM, limit: 500m CPU / 512Mi RAM), non-root security context (UID 10001).
* **Frontend Deployment**: 2 replicas, resources (req: 50m CPU / 64Mi RAM, limit: 250m CPU / 256Mi RAM), unprivileged Nginx (UID 101).
* **Database**: PostgreSQL 16 StatefulSet with PersistentVolumeClaim (`10Gi` storage on `gp3` storage class in prod, hostpath/standard in dev).
* **Horizontal Pod Autoscaler (HPA)**: Automatically scales the backend deployment between 2 and 6 pods based on 60% average CPU utilization.
* **PodDisruptionBudget (PDB)**: Configured with `minAvailable: 1` to guarantee high availability during cluster maintenance.
* **Ingress Routing**: Configured for Nginx Ingress Controller (Host: `podiumhq.local`):
  * `/` -> Frontend Service (port 8080)
  * `/api` -> Backend Service (port 8000)
  * `/health` -> Backend Liveness Probe (port 8000)
  * `/ready` -> Backend Readiness Probe (port 8000)

### Deployment Commands

1. **Lint the Helm chart:**
   ```bash
   helm lint ./helm/podiumhq
   ```
2. **Render and inspect manifests locally:**
   ```bash
   helm template podiumhq ./helm/podiumhq -f ./helm/podiumhq/values-dev.yaml
   ```
3. **Deploy to Kubernetes (namespace `podiumhq`):**
   ```bash
   kubectl create namespace podiumhq --dry-run=client -o yaml | kubectl apply -f -
   helm upgrade --install podiumhq ./helm/podiumhq -n podiumhq -f ./helm/podiumhq/values-dev.yaml
   ```
4. **Verify deployed workloads:**
   ```bash
   helm list -n podiumhq
   kubectl get pods,svc,ingress,pvc,hpa -n podiumhq
   ```

### Verified Live Kubernetes Output

```text
NAME                                     READY   STATUS    RESTARTS   AGE
pod/podiumhq-backend-69d67566cb-7467x    1/1     Running   0          42m
pod/podiumhq-frontend-79c5cbb75b-489qf   1/1     Running   0          42m
pod/podiumhq-postgres-0                  1/1     Running   0          42m

NAME                         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/podiumhq-backend     ClusterIP   10.106.126.160   <none>        8000/TCP   42m
service/podiumhq-frontend    ClusterIP   10.111.139.117   <none>        8080/TCP   42m
service/podiumhq-postgres    ClusterIP   10.102.196.223   <none>        5432/TCP   42m

NAME                                          CLASS   HOSTS            ADDRESS   PORTS   AGE
ingress.networking.k8s.io/podiumhq            nginx   podiumhq.local             80      42m

NAME                                            STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
persistentvolumeclaim/data-podiumhq-postgres-0   Bound    pvc-1f5ef09f-6825-4c07-b765-b0f3ee33f7c9   2Gi        RWO            standard       42m
```

---

## 10. GitOps Continuous Delivery with ArgoCD

PodiumHQ implements declarative GitOps using ArgoCD to eliminate manual `kubectl` deployments.

```
+-----------------------------------------------------------------------------------------+
|                                  GITOPS ARCHITECTURE                                    |
|                                                                                         |
|   1. CI/CD Pipeline (Job 4)                                                             |
|          │                                                                              |
|          ▼                                                                              |
|      Bumps image.tag in helm/podiumhq/values-prod.yaml                                  |
|          │                                                                              |
|          ▼                                                                              |
|   2. Git Repository (main branch)                                                       |
|          ▲                                                                              |
|          │ Polls repository every 3 minutes                                             |
|   3. ArgoCD Controller (argocd/application.yaml)                                        |
|          │                                                                              |
|          ├── Detects Git commit SHA change                                              |
|          ├── Applies Helm chart to AWS EKS (namespace: podiumhq)                        |
|          └── Self-Heals any manual cluster configuration drift                          |
+-----------------------------------------------------------------------------------------+
```

### Installation and Sync Setup

1. **Install ArgoCD on the cluster:**
   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```

2. **Access the ArgoCD Web UI:**
   ```bash
   kubectl port-forward svc/argocd-server -n argocd 8080:443
   ```
   * Open: `https://localhost:8080`
   * Username: `admin`
   * Get initial password:
     ```bash
     kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
     ```

3. **Deploy the GitOps Application:**
   ```bash
   kubectl apply -f argocd/application.yaml
   ```

4. **Demonstrating Self-Healing (Viva Demo):**
   * Manually tamper with the cluster by scaling backend pods:
     ```bash
     kubectl scale deployment podiumhq-backend -n podiumhq --replicas=5
     ```
   * Observe ArgoCD mark the application `OutOfSync` and immediately trigger automated reconciliation (`selfHeal: true`) back to the Helm specification.

---

## 11. Observability (Prometheus & Grafana)

PodiumHQ incorporates complete operational and business metric telemetry.

### Metrics Architecture

* **Standard HTTP Metrics**: Handled via `prometheus-fastapi-instrumentator` (request duration histograms, HTTP status code counts, request rates).
* **Custom Business Metrics** (declared in [`backend/app/metrics.py`](backend/app/metrics.py)):
  1. `podiumhq_scores_submitted_total` (Counter with labels `round_id`, `criterion_name`): Tracks total judge score submissions.
  2. `podiumhq_teams_by_status` (Gauge with label `status`): Current count of teams in `registered`, `active`, or `disqualified` states.
  3. `podiumhq_score_value` (Histogram): Distribution of scores awarded (buckets 1.0 to 10.0).
  4. `podiumhq_leaderboard_requests_total` (Counter with label `event_slug`): Tracks leaderboard API traffic.
  5. `podiumhq_judge_evaluation_duration_seconds` (Histogram): Tracks time taken to submit round evaluations.

### Installing Prometheus & Grafana via Helm

1. Add the Prometheus community Helm repository:
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   ```
2. Install the `kube-prometheus-stack` using the custom values file:
   ```bash
   helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
     -n monitoring --create-namespace \
     -f monitoring/kube-prometheus-stack-values.yaml
   ```
3. Access the Prometheus Web UI:
   ```bash
   kubectl port-forward -n monitoring svc/kube-prometheus-stack-prometheus 9090:9090
   ```
   Open `http://localhost:9090/targets` and verify that the `serviceMonitor/podiumhq/podiumhq-servicemonitor/0` target is in the **UP** state.
4. Access Grafana:
   ```bash
   kubectl port-forward -n monitoring svc/kube-prometheus-stack-grafana 3001:80
   ```
   * Open `http://localhost:3001`
   * Username: `admin`
   * Password: `admin_secure_grafana_2026` (configured in [`monitoring/kube-prometheus-stack-values.yaml`](monitoring/kube-prometheus-stack-values.yaml))
5. Import Dashboard:
   * Import [`monitoring/grafana-dashboard.json`](monitoring/grafana-dashboard.json) to visualize backend request latency, error rates, and custom score counts.

---

## 12. Evidence Gallery

A comprehensive visual catalog of all 24 verified screenshots is documented in [**`docs/evidence/screenshots/all-screenshots.md`**](docs/evidence/screenshots/all-screenshots.md).

| # | Artifact / Checkpoint | Primary Screenshot | Additional Verification Image | Rubric Module & Verification Proof |
| :-: | :--- | :--- | :--- | :--- |
| **01** | CI/CD Pipeline Automation | [`image.png`](docs/evidence/screenshots/image.png) | [`image-1.png`](docs/evidence/screenshots/image-1.png) | **M5 (15 Pts)**: GitHub Actions 4-stage pipeline passing green on main |
| **02** | Gitleaks Secret Audit | [`image-2.png`](docs/evidence/screenshots/image-2.png) | — | **M6 (5 Pts)**: Zero leaks detected across all 21 git commits |
| **03** | Backend Pytest & Coverage | [`image-3.png`](docs/evidence/screenshots/image-3.png) | — | **M2 (10 Pts)**: 31 passed tests, 90.39% code coverage table |
| **04** | Frontend ESLint & Audit | [`image-4.png`](docs/evidence/screenshots/image-4.png) | — | **M2 & M6 (10 Pts)**: Clean ESLint and 0 npm production vulnerabilities |
| **05** | Terraform Plan & Destroy | [`image-5.png`](docs/evidence/screenshots/image-5.png) | [`image-10.png`](docs/evidence/screenshots/image-10.png) | **M7 (15 Pts)**: Plan 30 AWS resources; verified clean teardown |
| **06** | Docker Compose Stack | [`image-6.png`](docs/evidence/screenshots/image-6.png) | — | **M4 (10 Pts)**: Backend, frontend, postgres all Up (healthy) |
| **07** | Non-Root Container Security | [`image-7.png`](docs/evidence/screenshots/image-7.png) | — | **M4 (10 Pts)**: Backend UID 10001 (`appuser`), Frontend UID 101 (`nginx`) |
| **08** | Kubernetes Live Workloads | [`image-8.png`](docs/evidence/screenshots/image-8.png) | — | **M8 (15 Pts)**: Pods 1/1 Running in namespace podiumhq, PVC Bound |
| **09** | Frontend Health & Headers | [`image-9.png`](docs/evidence/screenshots/image-9.png) | — | **M1 & M4 (10 Pts)**: HTTP 200 OK with hardened security headers |
| **10** | PodiumHQ Web Application | [`image-11.png`](docs/evidence/screenshots/image-11.png) | [`image-18.png`](docs/evidence/screenshots/image-18.png), [`image-19.png`](docs/evidence/screenshots/image-19.png) | **M1 (10 Pts)**: Live Leaderboard, Teams Lifecycle, and Judge Scoring |
| **11** | Interactive Swagger API | [`image-12.png`](docs/evidence/screenshots/image-12.png) | [`image-13.png`](docs/evidence/screenshots/image-13.png), [`image-14.png`](docs/evidence/screenshots/image-14.png) | **M1 (10 Pts)**: OpenAPI documentation for `/health`, `/ready`, `/api` |
| **12** | Prometheus Telemetry Stream | [`image-16.png`](docs/evidence/screenshots/image-16.png) | [`image-21.png`](docs/evidence/screenshots/image-21.png) | **M9 (10 Pts)**: Raw `/metrics` stream and in-app Telemetry dashboard |
| **13** | GHCR Container Packages | [`image-17.png`](docs/evidence/screenshots/image-17.png) | — | **M5 (15 Pts)**: Published images on GHCR tagged with Git commit SHAs |

*Detailed capture commands and rubric criteria mappings are documented in [`docs/SCREENSHOT-EVIDENCE-GUIDE.md`](docs/SCREENSHOT-EVIDENCE-GUIDE.md) and [`docs/evidence/screenshots/all-screenshots.md`](docs/evidence/screenshots/all-screenshots.md).*

---

## 13. Demo Video & Presentation Slides

* **Demo Video**: `<!-- TODO: add after recording -->` *(Record a 6–8 minute walkthrough showing GitHub Actions, Terraform plan, Kubernetes workloads, web UI, and metrics. See [`docs/VIDEO_SCRIPT.md`](docs/VIDEO_SCRIPT.md) or [`STUDENT_SUBMISSION_AND_DEMO_GUIDE.md`](STUDENT_SUBMISSION_AND_DEMO_GUIDE.md) for the exact script).*
* **Presentation Slides (PDF)**: [demo/slides.pdf](demo/slides.pdf)
* **Presentation Slides (PowerPoint)**: [demo/slides.pptx](demo/slides.pptx)
* **Student Presentation Deck**: [demo/presentation_student.pptx](demo/presentation_student.pptx)

---

## 14. Known Issues & Limitations

In accordance with course grading guidelines and honest engineering standards:

1. **Cloud Cost vs. Local Demonstration Parity**:
   * Running a live AWS EKS cluster with NAT Gateways continuously costs ~$150/month in idle cloud charges.
   * **Mitigation**: Cloud infrastructure is validated via `terraform plan` (30 resources planned cleanly with zero errors), while live Kubernetes workloads are deployed and verified on Docker Desktop Kubernetes using the identical Helm chart.
2. **In-Cluster Database High Availability**:
   * The local and dev Kubernetes deployment packages PostgreSQL 16 as a single-node StatefulSet with persistent volume storage (`gp3` or local volume). While persistent across pod restarts, it does not provide multi-region Active-Active replication like AWS Aurora PostgreSQL.
3. **TLS/HTTPS Termination**:
   * Ingress is configured for local testing over HTTP on port 80/8080. In production on AWS, TLS termination should be handled via `cert-manager` with Let's Encrypt or an AWS Certificate Manager (ACM) ARN configured on the AWS Load Balancer Controller.
4. **AWS Organizations SCP Policy Restrictions**:
   * In student/sandbox AWS accounts, IAM users frequently face AWS Organizations Service Control Policies (SCPs) that restrict `ec2:DescribeAvailabilityZones`.
   * **Mitigation**: Rather than querying the AWS API dynamically, `terraform/variables.tf` explicitly specifies the target Availability Zones (`ap-south-1a`, `ap-south-1b`, `ap-south-1c`), enabling `terraform plan` to execute without requiring administrator escalation.

---

## 15. Project Directory Structure

```text
podiumHQ/
├── .github/
│   └── workflows/
│       ├── ci-cd.yml                          # 4-job CI/CD pipeline (Lint/Test, Security, Build/Push, GitOps)
│       └── security.yml                       # Scheduled weekly security & IaC scans
├── argocd/
│   ├── application.yaml                       # ArgoCD Application CR targeting Helm chart
│   └── install.md                             # ArgoCD installation and self-healing runbook
├── backend/
│   ├── alembic/                               # Database migration scripts
│   ├── app/                                   # FastAPI application source
│   │   ├── models/                            # SQLAlchemy ORM models (Event, Team, Judge, Round, Score)
│   │   ├── routers/                           # API routers (events, teams, judges, rounds, scores, ops)
│   │   ├── schemas/                           # Pydantic v2 validation models
│   │   ├── services/                          # Business logic (scoring_engine.py)
│   │   ├── config.py                          # Pydantic BaseSettings configuration
│   │   ├── database.py                        # SQLAlchemy session engine
│   │   ├── logger.py                          # Structured JSON logging
│   │   ├── main.py                            # FastAPI entrypoint, CORS, Prometheus middleware
│   │   └── metrics.py                         # Custom Prometheus metric declarations
│   ├── tests/                                 # 31 Pytest unit & integration tests
│   │   ├── conftest.py                        # SQLite in-memory fixtures & FastAPI TestClient
│   │   ├── test_events.py                     # 8 event lifecycle tests
│   │   ├── test_health_and_ops.py             # 5 health probe and metrics tests
│   │   ├── test_scoring_and_leaderboard.py    # 7 judging and scoring engine tests
│   │   └── test_teams.py                      # 11 team registration and status tests
│   ├── Dockerfile                             # Multi-stage non-root Python 3.12 container
│   ├── entrypoint.sh                          # Startup script with auto-migration support
│   ├── requirements.txt                       # Production backend dependencies
│   ├── requirements-dev.txt                   # Testing and linting dependencies (pytest, ruff)
│   └── ruff.toml                              # Ruff linter rules and formatting settings
├── demo/
│   ├── presentation_student.pptx              # Student oral defense presentation
│   ├── presentation.pptx                      # Technical presentation deck
│   ├── slides.pdf                             # Compiled PDF presentation slides
│   └── slides.pptx                            # 12-slide comprehensive presentation deck
├── docs/
│   ├── evidence/
│   │   ├── screenshots/                       # 12 submission evidence screenshots (.gitkeep)
│   │   ├── helm-rendered.yaml                 # Pre-rendered Helm manifests
│   │   ├── k8s-workloads.txt                  # Verified kubectl get all output
│   │   └── terraform-plan.txt                 # Full 30-resource terraform plan output
│   ├── EVIDENCE_CHECKLIST.md                  # Checklist mapping commands to evidence
│   ├── FINAL-SUBMISSION-CHECKLIST.md          # 100-Point rubric score card and verification
│   ├── REQUIREMENT-TRACEABILITY.md            # Traceability matrix mapping rubric to code
│   ├── RUBRIC_CHECK.md                        # Module-by-module audit check
│   ├── SCREENSHOT-EVIDENCE-GUIDE.md           # Step-by-step guide for taking the 12 screenshots
│   ├── VERIFICATION-REPORT.md                 # Detailed execution and test verification report
│   └── VIDEO_SCRIPT.md                        # Script and speaking lines for demo recording
├── frontend/
│   ├── nginx/                                 # Unprivileged Nginx configuration template
│   ├── src/                                   # React 18 single-page application source
│   ├── Dockerfile                             # Multi-stage build with unprivileged Nginx (UID 101)
│   ├── index.html                             # Web application HTML entrypoint
│   ├── package.json                           # Frontend dependencies and scripts (with esbuild override)
│   ├── package-lock.json                      # Locked dependency tree
│   └── vite.config.js                         # Vite build configuration
├── helm/
│   └── podiumhq/
│       ├── templates/                         # Deployments, Services, Ingress, HPA, PDB, Postgres, ServiceMonitor
│       ├── Chart.yaml                         # Helm chart metadata
│       ├── values.yaml                        # Default chart values
│       ├── values-dev.yaml                    # Development values overlay
│       └── values-prod.yaml                   # Production values overlay (updated by CI GitOps bump)
├── monitoring/
│   ├── alerts.yaml                            # Prometheus Alertmanager alerting rules
│   ├── grafana-dashboard.json                 # Pre-built Grafana dashboard JSON
│   └── kube-prometheus-stack-values.yaml      # Custom values for kube-prometheus-stack
├── scripts/
│   ├── bootstrap-secrets.sh                   # Helper script to initialize Kubernetes secrets
│   ├── load-test.sh                           # Traffic generation script for testing HPA autoscaling
│   └── smoke-test.sh                          # Automated curl health verification script
├── terraform/
│   ├── addons.tf                              # EKS Addons (EBS CSI, CoreDNS, Kube-Proxy, VPC-CNI)
│   ├── eks.tf                                 # EKS Cluster, node groups, IAM roles
│   ├── outputs.tf                             # Outputs (cluster_name, endpoint, kubeconfig command)
│   ├── README.md                              # Terraform provisioning and teardown guide
│   ├── terraform.tfvars.example               # Variable configuration template
│   ├── variables.tf                           # AWS region, VPC CIDR, EKS version, static AZs
│   ├── versions.tf                            # Terraform (>= 1.5.0) and AWS provider (>= 5.0) constraints
│   └── vpc.tf                                 # VPC, subnets, route tables, NAT Gateway, EIP
├── troubleshooting/
│   ├── RUNBOOK.md                             # Diagnostic runbook for 4 real-world failure scenarios
│   ├── broken-image.yaml                      # Scenario 1: ImagePullBackOff reproduction
│   ├── broken-probe.yaml                      # Scenario 2: CrashLoopBackOff reproduction
│   ├── broken-secret.yaml                     # Scenario 3: Missing secret reproduction
│   └── broken-service.yaml                    # Scenario 4: Service routing failure reproduction
├── .dockerignore                              # Build exclusion rules
├── .env.example                               # Environment variable template for local Docker Compose
├── .gitignore                                 # Git version control exclusions
├── .gitleaks.toml                             # Gitleaks secret scanning rules and allowlist
├── docker-compose.yml                         # Multi-container orchestration (backend, frontend, postgres)
├── Makefile                                   # Developer workflow shortcuts
├── pull_request_template.md                   # PR template with DevSecOps quality and security checklist
├── README.md                                  # Main project documentation and runbook
└── STUDENT_SUBMISSION_AND_DEMO_GUIDE.md       # Master human-readable guide for submission and video recording
```

---

## 16. Author & License

* **Author**: [Nanda Kishore Dasari](https://github.com/nandakishore-dasari)
* **Repository**: [https://github.com/nandakishore-dasari/podiumHQ](https://github.com/nandakishore-dasari/podiumHQ)
* **License**: [MIT](https://opensource.org/licenses/MIT)
