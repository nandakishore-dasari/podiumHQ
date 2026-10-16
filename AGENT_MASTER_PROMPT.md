# MASTER PROMPT — DevSecOps Capstone Automation Agent

> Give this entire file to an autonomous coding agent (Claude Code, Cursor agent, Copilot agent, etc.).
> Fill in **Section 1** first. Everything else is the agent's brief.

---

## 1. PROJECT VARIABLES (human fills these in before running)

| Variable | Value | Notes |
|---|---|---|
| `PROJECT_NAME` | `PodiumHQ` | Short, unique, lowercase slug is derived from it (`podiumhq`) |
| `PROJECT_DOMAIN` | Hackathon & event judging platform: teams submit projects, judges score them across rounds against weighted criteria, and a live leaderboard ranks results | **Must be your own domain, NOT a task/project board.** See Rule R1 |
| `GITHUB_USER` | `<your-github-username>` | Used for GHCR image paths |
| `GITHUB_REPO` | `<your-repo-name>` | |
| `AWS_REGION` | `ap-south-1` | Reference project default |
| `K8S_NAMESPACE` | `podiumhq` | |
| `INGRESS_HOST` | `podiumhq.local` | Use nip.io / LB hostname for real AWS access |
| `AUTHOR_NAME` | `<your name>` | For README, slides, commits |

If any variable is left as a `<placeholder>`, use a sensible default, record it under "Assumptions" in the README, and keep going. Do not stop to ask unless a credential is required.

---

## 2. ROLE AND MISSION

You are a senior DevSecOps / platform engineer and full-stack developer. Build a **complete, original, production-style capstone project** that satisfies the course reference project and its 100-point grading rubric, and then go beyond the minimum so the result is clearly distinctive and impressive.

The project must show one real application travelling the whole path:

```
Developer → Git/GitHub → GitHub Actions (lint, test, build, scan, push to GHCR)
          → GitOps commit (image tag bump) → ArgoCD
          → Terraform-provisioned AWS VPC + EKS
          → Helm-packaged workloads (frontend, backend, PostgreSQL)
          → Ingress → HPA → Prometheus + Grafana → troubleshooting lab
```

You will work in phases, verify each phase before moving on, commit with meaningful messages, and finish with a rubric self-audit.

---

## 3. GROUND TRUTH — WHAT THE COURSE ASKS (already analysed, treat as requirements)

The reference project is **"Session 21 — DevOps Final Capstone: TaskBoard (Python)"**. Its README and `GRADING.md` define the requirements below.

### 3.1 Reference stack (must be matched in spirit; same architecture, your own domain)
React + Vite frontend · responsive CSS · FastAPI backend · PostgreSQL · SQLAlchemy ORM · Alembic migrations · REST APIs · Pytest · Docker (multi-stage frontend, non-root) · GitHub Actions · Trivy · GHCR · Terraform (AWS VPC + EKS, default region `ap-south-1`) · Kubernetes · Helm · Ingress · HPA · Prometheus + Grafana · `/health`, `/ready`, `/metrics` · troubleshooting exercises.

### 3.2 Reference backend surface (replicate the *pattern* for your domain)
`GET /`, `GET /health`, `GET /ready` (checks DB), `GET /metrics`, full CRUD under `/api/<resource>`, a `/api/<resource>/stats` endpoint, Swagger at `/docs`.

### 3.3 Grading rubric (100 points) — every item below must be demonstrably satisfied

| Module | Topic | Pts |
|---|---|---|
| M1 | Application (FE + BE + DB) | 10 |
| M2 | Testing (Pytest + code quality) | 10 |
| M3 | Git & GitHub | 5 |
| M4 | Docker (Dockerfiles + Compose) | 10 |
| M5 | CI/CD (GitHub Actions) | 15 |
| M6 | DevSecOps (Trivy) | 5 |
| M7 | Terraform (AWS IaC) | 15 |
| M8 | Kubernetes + Helm | 15 |
| M9 | Observability (Prometheus + Grafana) | 10 |
| M10 | Presentation + Documentation | 5 |

A skipped module scores **zero** for that module; partial credit exists only inside a module.

### 3.4 Gaps and traps found in the reference material (IMPORTANT — handle all of these)

1. **ArgoCD is required but never taught in the README.** `GRADING.md` (M10 video requirements) demands showing "ArgoCD — the synced application and GitOps flow". Implement ArgoCD properly (Section 6, M8b).
2. **Plagiarism rule:** a clone of TaskBoard without meaningful changes gets **zero for all modules**. The domain, data model, API naming, UI design, metrics, dashboards, and docs must be original. Do not copy reference code, names, text, or layout.
3. **Workflow location:** the reference keeps `ci-cd.yml` at the repo root, but the rubric checks `.github/workflows/`. Put workflows in `.github/workflows/`.
4. **Reference compose hard-codes DB credentials.** Do better: `.env.example` + variable substitution; real `.env` is git-ignored.
5. **Video + slides are MANDATORY** (missing video = 0 for M10). An agent cannot record video; see Section 11 (human-only tasks). You must still prepare everything the human needs to record it in one take.
6. **Commit history:** the rubric expects ≥ 10 commits with meaningful messages (not "update", "fix", "test").
7. **Secrets:** any committed credential in history gets the submission rejected. Never commit secrets, state files, or kubeconfigs.
8. **Cost responsibility:** `terraform destroy` must work cleanly and be documented; provide a teardown runbook.
9. **Reference Dockerfile runs migrations on every container start.** With 2+ replicas this races. Use a Helm hook Job for migrations in Kubernetes (Section 6, M8).
10. **PVC on EKS needs the EBS CSI driver** and a default StorageClass, and **HPA needs Metrics Server**. Provision both via EKS add-ons in Terraform, or the in-cluster PostgreSQL and HPA will silently fail.

---

## 4. NON-NEGOTIABLE RULES

- **R1 — Originality.** Your own domain (default `PROJECT_DOMAIN`), ≥ 3 related tables, ≥ 8 REST endpoints, own UI design language, own metric names, own dashboard. Never mention or reuse "TaskBoard".
- **R2 — No secrets in Git.** Use `.env.example`, GitHub Actions secrets/`GITHUB_TOKEN`, Kubernetes Secrets created out-of-band by a bootstrap script, and `terraform.tfvars.example` only. Add a `gitleaks` check to CI.
- **R3 — Image tags are the Git commit SHA.** Never publish or deploy `:latest`.
- **R4 — Quality gates in order:** lint → tests → build → Trivy scan → push. A failed gate stops the pipeline; nothing broken is pushed.
- **R5 — Non-root everywhere.** Both Dockerfiles and all Kubernetes pods run as non-root.
- **R6 — Verify, don't assume.** Run every command you can. If you cannot run something (no Docker daemon, no AWS credentials), say so explicitly, validate statically (`terraform validate`, `helm lint`, `helm template | kubeconform`, `yamllint`, `docker build --check` if available), and list it under "Not executed" in the final report. **Never fabricate outputs, screenshots, or links.**
- **R7 — Pin versions.** Pin base images, Actions (by tag or SHA), Python/Node deps, Terraform providers/modules, Helm chart versions. Check the current stable version of each before pinning.
- **R8 — Meaningful commits.** Conventional-commit style, one logical change per commit, ≥ 12 commits total (Section 8).
- **R9 — Everything reproducible.** One command per stage: `docker compose up --build`, `make test`, `make scan`, `terraform apply`, `helm upgrade --install`. Provide a `Makefile` wrapping them.

---

## 5. TARGET REPOSITORY LAYOUT

```
<GITHUB_REPO>/
├── .github/
│   ├── workflows/
│   │   ├── ci-cd.yml              # lint → test → build → scan → push → gitops bump
│   │   └── security.yml           # scheduled gitleaks / pip-audit / npm audit / Trivy fs+IaC
│   └── dependabot.yml
├── backend/
│   ├── app/                       # main.py, config.py, database.py, models/, schemas/, routers/, services/, metrics.py, logging.py
│   ├── alembic/ (+ alembic.ini)   # versions/ ≥ 2 migrations
│   ├── tests/                     # conftest.py, test_*.py
│   ├── pytest.ini
│   ├── requirements.txt           # + requirements-dev.txt
│   ├── Dockerfile
│   └── entrypoint.sh
├── frontend/
│   ├── src/                       # components/, pages/, api/, styles/
│   ├── nginx/default.conf.template
│   ├── package.json  vite.config.js
│   └── Dockerfile                 # multi-stage: node build → nginx-unprivileged runtime
├── docker-compose.yml
├── .env.example
├── terraform/
│   ├── versions.tf  providers.tf  variables.tf  main.tf  vpc.tf  eks.tf  addons.tf  outputs.tf
│   ├── terraform.tfvars.example
│   └── README.md                  # apply/destroy runbook + cost note
├── k8s/
│   ├── namespace.yaml
│   └── bootstrap/                 # StorageClass (gp3), optional NetworkPolicies
├── helm/<project_slug>/
│   ├── Chart.yaml  values.yaml  values-dev.yaml  values-prod.yaml
│   └── templates/                 # deployments, services, ingress, hpa, pdb, configmap, secret ref,
│                                  # postgres statefulset+pvc, migration-job (hook), servicemonitor, _helpers.tpl, NOTES.txt
├── argocd/
│   ├── install.md                 # how ArgoCD is installed on EKS
│   └── application.yaml           # Application CR: automated sync, prune, selfHeal
├── monitoring/
│   ├── kube-prometheus-stack-values.yaml
│   ├── grafana-dashboard-<slug>.json
│   ├── grafana-dashboard-configmap.yaml
│   └── alerts.yaml                # PrometheusRule (optional-but-do-it)
├── troubleshooting/
│   ├── broken-image.yaml  broken-service.yaml
│   ├── broken-probe.yaml  broken-secret.yaml     # extras
│   └── RUNBOOK.md                 # symptom → command → root cause → fix
├── scripts/
│   ├── load-test.sh (or .py)      # drives HPA
│   ├── bootstrap-secrets.sh
│   └── smoke-test.sh
├── docs/
│   ├── architecture.md  (+ Mermaid diagrams)
│   ├── adr/                       # short architecture decision records
│   ├── evidence/                  # screenshots go here (human-captured) + EVIDENCE_CHECKLIST.md
│   ├── SECURITY_SCAN_NOTES.md     # the 2–3 sentence Trivy explanation (M6)
│   ├── RUBRIC_CHECK.md            # self-audit traceability matrix
│   └── VIDEO_SCRIPT.md            # timestamped demo script
├── demo/
│   ├── slides.pptx (and slides.pdf)   # ≥ 8 slides; agent generates
│   └── README.md                      # "Place presentation.mp4 here" (human uploads)
├── Makefile
├── .gitignore  .dockerignore  .editorconfig
└── README.md
```

---

## 6. MODULE-BY-MODULE SPECIFICATION

### M1 — Application (10 pts)

**Backend (FastAPI, Python 3.12, SQLAlchemy 2.x, psycopg 3, pydantic-settings):**
- Model ≥ 3 related tables for `PROJECT_DOMAIN` (default PodiumHQ: `events`, `teams`, `judges`, `rounds`, `criteria` (with weights), and `scores` linking judge + team + round + criterion; team status lifecycle `registered → submitted → under_review → scored → disqualified`; unique constraint so a judge can score a team once per criterion per round). Use foreign keys, enums, timestamps, unique constraints, indexes.
- Endpoints (≥ 8, must include GET/POST/PUT/DELETE): full CRUD on the primary resource, list + read on the others, `GET /api/<primary>/stats`, plus pagination, filtering by status, and text search on list endpoints.
- Operational endpoints: `GET /` (service info + version), `GET /health` (cheap liveness), `GET /ready` (executes `SELECT 1`; returns 503 when DB is down), `GET /metrics` (Prometheus), Swagger at `/docs`.
- Proper validation (Pydantic v2), consistent error envelope, correct status codes (201, 204, 404, 409, 422), CORS config from env, structured JSON logging with request-ID middleware, graceful DB-down handling.
- All config via environment variables (`DATABASE_URL`, `LOG_LEVEL`, `CORS_ORIGINS`, `APP_VERSION`, `RUN_MIGRATIONS`).
- **Alembic:** ≥ 2 migration files in `alembic/versions/` (initial schema + one follow-up such as an index or new column), `env.py` reading `DATABASE_URL`.
- Seed script (idempotent, dev-only) so the UI isn't empty during demos.

**Frontend (React + Vite):**
- Original design language (own palette, typography, layout — **do not mimic a dark-sidebar task-board dashboard**). Required UI elements: navigation, summary KPI cards from `/stats`, data table with filters + search + pagination, create/edit modal, delete confirmation, status/priority badges, a live leaderboard view (auto-refreshing, with rank-change indicators) and a judge scoring form that fit the domain, loading skeletons, empty states, and clear backend-error states.
- Responsive (mobile, tablet, desktop). Accessible basics (labels, focus states, contrast, keyboard-closable modal).
- Calls only relative `/api/...` paths. No hardcoded hostnames.
- Environment-agnostic: the same built bundle must work in Compose and behind Kubernetes Ingress.

**Acceptance:** app loads at `http://localhost:3000`, full create/read/update/delete from the UI works, `/docs` shows all routes.

### M2 — Testing and Code Quality (10 pts)

- `backend/pytest.ini` **and** `backend/tests/conftest.py` (both present and correct).
- Tests use an isolated database (SQLite in-memory with `StaticPool` via FastAPI dependency override, or Testcontainers). **Never** the real DB. Keep model types portable if using SQLite.
- **≥ 15 test cases** (rubric minimum is 5 across ≥ 3 endpoints): CRUD happy paths, validation errors (422), not-found (404), conflict (409), pagination/filter/search, `/stats`, `/health`, `/ready` (including DB-failure case via mock), `/metrics` content type and a known metric name.
- `pytest-cov` with a **≥ 80 %** coverage gate; `ruff` (lint + format check) and `mypy` (lenient config) configured and clean.
- Optional strong extra: a CI job that runs `alembic upgrade head` against a real Postgres service container to prove migrations work.
- Frontend: ESLint clean; add a few Vitest component tests if time allows.
- Save `pytest -v` output to `docs/evidence/pytest-output.txt` (real output only).

### M3 — Git and GitHub (5 pts)

- `.gitignore` must exclude at least: `.env`, `__pycache__/`, `node_modules/`, `.venv/`, `*.tfstate*`, `.terraform/`, `terraform.tfvars`, `*.pem`, `kubeconfig*`, `dist/`, coverage artefacts.
- Add `.env.example` and `terraform.tfvars.example` instead.
- Follow the commit plan in Section 8 (≥ 12 meaningful commits, `main` branch).
- Add PR template and `CODEOWNERS` (small, quick wins), plus Dependabot for pip, npm, docker, github-actions, terraform.

### M4 — Docker (10 pts)

**`backend/Dockerfile`:** multi-stage or slim, `python:3.12-slim` pinned, no build tools in runtime, `PYTHONDONTWRITEBYTECODE`, `PYTHONUNBUFFERED`, non-root user with fixed UID (e.g. 10001), `HEALTHCHECK`, `EXPOSE 8000`, entrypoint that conditionally runs `alembic upgrade head` (`RUN_MIGRATIONS=true`) then `exec uvicorn`.

**`frontend/Dockerfile`:** **multi-stage** — `node:22-alpine` build stage (`npm ci`, `npm run build`) → `nginxinc/nginx-unprivileged:<pinned>-alpine` runtime (non-root, listens on 8080). Nginx template proxies `/api` to a configurable upstream (via `envsubst` template) for Compose, serves SPA fallback, adds security headers, gzip, and long-cache for hashed assets.

**`docker-compose.yml`:** exactly three services — `postgres`, `backend`, `frontend` — with healthchecks, `depends_on: condition: service_healthy`, named volume, env from `.env`, frontend published as `3000:8080`, backend `8000:8000`. `docker compose up --build` must start everything with no manual steps.

**Also:** `.dockerignore` per image context, images < reasonable size, labels (`org.opencontainers.image.*`).

### M5 — CI/CD (15 pts) — `.github/workflows/ci-cd.yml`

Triggers: `push` to `main`, `pull_request` to `main`, `workflow_dispatch`. Use `concurrency` and least-privilege `permissions`.

Jobs in order:
1. **lint-test** — checkout, setup-python 3.12 (pip cache), install deps, `ruff`, `pytest --cov` (**fails the build on failure**), setup-node 22 (npm cache), `npm ci`, `npm run lint`, **`npm run build`** (frontend built in pipeline). Upload coverage artifact.
2. **secrets-and-deps** (parallel) — `gitleaks`, `pip-audit`, `npm audit --audit-level=high`.
3. **build-scan-push** (`needs: [lint-test, secrets-and-deps]`) — Buildx + layer cache; build **both** images tagged `ghcr.io/<owner>/<slug>-backend:${{ github.sha }}` and `...-frontend:${{ github.sha }}`; **Trivy scan both** (see M6); only on `main` push to GHCR using `GITHUB_TOKEN` (`packages: write`). **No `:latest` tag. SHA tags only.** (A short-SHA convenience tag is fine; `latest` is not.)
4. **gitops-bump** (only on `main`) — update `image.tag` in `helm/<slug>/values-prod.yaml` to the commit SHA using `yq`, commit back with `[skip ci]` and `contents: write` permission, guarding against loops. ArgoCD then syncs.

Add a status badge to the README, and a job summary (`$GITHUB_STEP_SUMMARY`) showing image names, tags, and scan results.

### M6 — DevSecOps / Trivy (5 pts)

- Trivy scan step for **both** backend and frontend images, `severity: HIGH,CRITICAL`, `exit-code: '1'`, `ignore-unfixed: true`, pinned `aquasecurity/trivy-action` version.
- Scan happens **before push** (build → scan → push).
- Upload SARIF to GitHub Security tab (`github/codeql-action/upload-sarif`) and keep a table-format scan in the log for screenshots.
- Additionally: Trivy `fs` scan (deps + secrets), Trivy `config` scan on Terraform/Helm/Dockerfiles.
- If findings appear: fix by upgrading base images/dependencies first. Use `.trivyignore` only with a written justification and expiry comment.
- Write `docs/SECURITY_SCAN_NOTES.md` — 2–3 sentences explaining what Trivy scanned and what the result means, plus one concrete CVE (or a clear explanation of a clean result) so the student can answer the oral question.
- Document the layers: SAST (ruff/bandit/CodeQL), dependency scanning, secret scanning, container scanning, IaC scanning, runtime hardening.

### M7 — Terraform (15 pts)

- Terraform ≥ 1.6; AWS provider pinned; prefer the community modules `terraform-aws-modules/vpc/aws` and `terraform-aws-modules/eks/aws` (pin versions after checking current major versions).
- **VPC:** CIDR variable, ≥ 2 AZs, **≥ 2 public subnets** and private subnets, single NAT gateway (cost-aware), correct EKS subnet tags (`kubernetes.io/role/elb`, `kubernetes.io/role/internal-elb`, cluster tag).
- **EKS:** pinned supported Kubernetes version (verify the current supported version), **≥ 1 managed node group** (e.g. 2× `t3.medium`, min 2 / max 4), private nodes, public endpoint restricted by a CIDR variable if possible, cluster logging minimal, IRSA/OIDC enabled.
- **EKS add-ons (required for the app to work):** `aws-ebs-csi-driver` (with IAM role), `vpc-cni`, `coredns`, `kube-proxy`, **`metrics-server`** (for HPA).
- **Ingress controller:** verify which controller is currently maintained before choosing (the community `ingress-nginx` project was announced for retirement in 2026 — confirm status). Prefer the **AWS Load Balancer Controller** (IAM via IRSA, installed via Terraform `helm_release`) and `ingressClassName: alb`; document the choice in `docs/adr/`.
- Variables with sensible defaults and descriptions; `outputs.tf` includes cluster name, endpoint, region, and the exact `aws eks update-kubeconfig ...` command.
- `terraform.tfvars.example` present; real `terraform.tfvars` ignored. Local state by default (ignored), S3 backend block provided but commented with instructions.
- `terraform fmt -check` and `terraform validate` must pass. Run `terraform init -backend=false` and `validate` locally; run `plan` if credentials exist.
- **Destroy runbook** in `terraform/README.md`: uninstall ArgoCD apps and Ingress/ALB first, delete PVCs/LoadBalancer Services, **then** `terraform destroy` (otherwise orphaned ENIs/ALBs block VPC deletion). Include a cost estimate note (EKS control plane + NAT + nodes) and "destroy right after the demo".

### M8 — Kubernetes + Helm (15 pts) and ArgoCD (M8b)

- `k8s/namespace.yaml` applies cleanly (with Pod Security labels, e.g. `restricted` or `baseline`).
- Helm chart `helm/<slug>/`: `Chart.yaml`, `values.yaml`, `values-dev.yaml`, `values-prod.yaml`, `templates/`. Must pass `helm lint --strict` and `helm template | kubeconform`.
- **Workloads:** backend and frontend Deployments with **≥ 2 replicas each**, rolling update strategy, resource requests/limits, liveness (`/health`) and readiness (`/ready`) probes, `startupProbe` for backend, `securityContext` (runAsNonRoot, readOnlyRootFilesystem where feasible, drop ALL capabilities, seccomp `RuntimeDefault`), topology spread or anti-affinity, `PodDisruptionBudget`.
- **Services:** `ClusterIP` for backend and frontend.
- **PostgreSQL:** StatefulSet + PVC (gp3 StorageClass) in-cluster for the demo, credentials from a pre-created Secret (`existingSecret`), plus an ADR comparing in-cluster Postgres vs Amazon RDS (document the trade-off; RDS is the production recommendation).
- **Migrations:** Helm `pre-install,pre-upgrade` hook **Job** running `alembic upgrade head`; app pods run with `RUN_MIGRATIONS=false`.
- **Ingress:** one resource routing `/` → frontend and `/api` → backend (also exposes `/docs` and `/metrics` only as appropriate). Provide `values-dev.yaml` for local (kind/minikube + host `INGRESS_HOST`) and `values-prod.yaml` for EKS.
- **HPA:** backend (and optionally frontend) CPU-based, min 2 / max 6, target ~60 %; requests set so HPA works. `scripts/load-test.sh` generates controlled load and the README shows `kubectl get hpa -w`.
- **ServiceMonitor** for the backend `/metrics`.
- **NetworkPolicies (bonus):** default-deny + allow frontend→backend, backend→postgres, ingress→frontend/backend, Prometheus→backend.
- `NOTES.txt` prints how to reach the app.
- **Secrets:** `scripts/bootstrap-secrets.sh` creates the DB Secret in-cluster (never in Git).
- **ArgoCD (M8b):** install via Helm/manifests on EKS (documented in `argocd/install.md`), `argocd/application.yaml` with `automated: {prune: true, selfHeal: true}`, `CreateNamespace=true`, source = this repo's `helm/<slug>` path with `values-prod.yaml`. Demonstrate the GitOps loop: CI bumps the image tag → ArgoCD shows OutOfSync → auto-syncs → Healthy. Document how to reach the ArgoCD UI (port-forward) and `argocd app list`.

### M9 — Observability (10 pts)

- `/metrics` exposes request count, latency histogram, in-progress requests (via `prometheus-fastapi-instrumentator`) **plus ≥ 3 custom domain metrics** (e.g. `podiumhq_scores_submitted_total`, `podiumhq_teams_by_status` (gauge), `podiumhq_score_value` (histogram), `podiumhq_leaderboard_requests_total`).
- `monitoring/kube-prometheus-stack-values.yaml` (Prometheus + Alertmanager + Grafana; sensible retention, resources, `serviceMonitorSelectorNilUsesHelmValues: false`, Grafana sidecar to auto-load dashboards).
- Custom **Grafana dashboard JSON** (provisioned via ConfigMap), ≥ 6 panels: request rate, p50/p95 latency, 5xx error rate, requests by endpoint, pod CPU/replica count (HPA), and ≥ 1 domain metric. Dashboard must show **live data** after running the load script.
- `monitoring/alerts.yaml` `PrometheusRule`: high error rate, high latency, pod crash-looping, target down.
- Document access: `kubectl port-forward` for Prometheus (Targets page must show the backend **UP**) and Grafana.

### M10 — Documentation and Presentation (5 pts)

**`README.md`** (project root) must contain: project description and purpose · architecture diagram (Mermaid + ASCII fallback) · tech stack table · local setup (`docker compose up --build`) · running tests · CI/CD pipeline description (with diagram) · security scanning description · Terraform infrastructure summary · Kubernetes/Helm deployment steps · **ArgoCD GitOps flow** · Ingress/HPA · observability setup · troubleshooting lab summary · teardown/cost · project structure · **known issues and limitations** · assumptions · author. Add badges (CI, license).

**`demo/slides.pptx` + `demo/slides.pdf`** — generate with the PPTX skill/tool if available (otherwise `python-pptx`), **≥ 10 slides**: title, project overview/problem, tech stack, architecture diagram, application walkthrough, CI/CD flow, DevSecOps/security, Terraform/AWS infrastructure, Kubernetes + Helm + ArgoCD, observability, troubleshooting, key learnings + future work. Clean, consistent design; diagrams drawn as shapes or embedded PNG rendered from Mermaid.

**`docs/VIDEO_SCRIPT.md`** — timestamped, minute-by-minute script and command list covering exactly what the rubric requires the video to show: PPT first; push triggering GitHub Actions to completion; codebase tour with design decisions; Terraform plan/apply + AWS Console proof of VPC + EKS; **ArgoCD synced app**; `kubectl get pods/svc/ingress`; Prometheus Targets UP; Grafana live panel; a live troubleshooting break/fix. Include pre-flight checklist and fallback plans.

**`docs/EVIDENCE_CHECKLIST.md`** — every screenshot the rubric asks for, the exact command to produce it, and the target filename in `docs/evidence/`.

---

## 7. DIFFERENTIATORS (do these after all rubric items pass — they make the project "unique and satisfying")

1. **Domain-driven depth:** realistic business rules (weighted score aggregation, ranking with tie-break rules, status transitions validated server-side, a judge cannot double-score, scoring locked once a round is closed, judge-agreement/variance indicator in `/stats`).
2. **Domain metrics + dashboard** tied to real business events, not just HTTP counters.
3. **Security depth:** gitleaks, pip-audit, npm audit, Trivy image/fs/config, SARIF upload, Dependabot, non-root + read-only FS + dropped capabilities, NetworkPolicies, Pod Security Admission labels.
4. **GitOps:** ArgoCD with automated sync/self-heal, and a documented drift-correction demo (manually scale a deployment → ArgoCD reverts it).
5. **Troubleshooting lab** with 4 broken scenarios (bad image, selector mismatch, failing readiness probe, missing Secret) and a symptom→diagnosis→fix `RUNBOOK.md`.
6. **Developer experience:** `Makefile` (`make up`, `test`, `lint`, `scan`, `tf-plan`, `helm-lint`, `load-test`), pre-commit config (ruff, gitleaks, terraform fmt), `.editorconfig`.
7. **Docs quality:** ADRs (why FastAPI, why ALB controller, in-cluster Postgres vs RDS, why ArgoCD), Mermaid architecture + CI/CD sequence diagram, cost note.
8. **Resilience demo:** kill a backend pod during load and show zero-downtime via readiness + PDB.

---

## 8. EXECUTION PLAN, VERIFICATION GATES, AND COMMIT PLAN

Work in this order. Do **not** proceed to the next phase until the current phase's gate passes.

| Phase | Work | Gate (must pass) | Commit message (example) |
|---|---|---|---|
| 0 | Repo scaffold, `.gitignore`, `.editorconfig`, `.env.example`, Makefile skeleton | `git status` clean of secrets | `chore: scaffold repository with gitignore and env template` |
| 1 | Backend models, schemas, routers, Alembic migrations | `alembic upgrade head` works on local Postgres; `/docs` loads | `feat(backend): add domain models, REST API and alembic migrations` |
| 2 | Observability endpoints (`/health`, `/ready`, `/metrics`) + custom metrics + logging | `curl` all three | `feat(backend): add health, readiness and prometheus metrics` |
| 3 | Tests, pytest config, ruff, mypy, coverage gate | `pytest -v` green, coverage ≥ 80 % | `test(backend): add pytest suite with isolated test database` |
| 4 | Frontend app | `npm run build` + `npm run lint` pass; manual UI check | `feat(frontend): build responsive React UI with filters and modals` |
| 5 | Dockerfiles, compose | `docker compose up --build` → UI at :3000 works end to end; containers run as non-root (`docker exec ... id`) | `build(docker): add hardened multi-stage images and compose stack` |
| 6 | CI workflow (lint/test/build/scan/push/gitops) | `actionlint` clean; (if repo access) green run on GitHub | `ci: add github actions pipeline with trivy scan and ghcr push` |
| 7 | Security workflow, Dependabot, pre-commit | YAML valid | `ci(security): add gitleaks, dependency audit and scheduled scans` |
| 8 | Terraform VPC + EKS + add-ons | `terraform fmt -check`, `init`, `validate` pass (`plan` if creds) | `feat(terraform): provision VPC and EKS with managed node group` |
| 9 | Helm chart + namespace + bootstrap | `helm lint --strict`, `helm template` → `kubeconform` pass; test on kind if possible | `feat(helm): package application with ingress, hpa and migration job` |
| 10 | ArgoCD Application + GitOps bump | manifest validates | `feat(gitops): add argocd application and image tag bump` |
| 11 | Monitoring values, dashboard, alerts, load script | `helm template`/JSON valid; dashboard JSON loads | `feat(monitoring): add prometheus stack values, dashboard and alerts` |
| 12 | Troubleshooting lab + RUNBOOK | each broken manifest applies and fails in the documented way (if cluster available) | `docs(troubleshooting): add broken scenarios and runbook` |
| 13 | README, architecture docs, ADRs | all rubric README sections present | `docs: write full technical documentation and architecture` |
| 14 | Slides (pptx + pdf), video script, evidence checklist | slides ≥ 10, open without error | `docs(demo): add presentation deck, video script and evidence checklist` |
| 15 | Self-audit `docs/RUBRIC_CHECK.md`, fix gaps | every rubric line marked ✅ / ⚠️ with file path | `docs: add rubric self-audit and final fixes` |

If a local Kubernetes tool (kind/minikube) is available, deploy the chart locally and test Ingress, HPA, and ServiceMonitor behaviour as far as possible.

---

## 9. RUBRIC SELF-AUDIT (final deliverable `docs/RUBRIC_CHECK.md`)

Create a table with **every** rubric criterion from the course (M1–M10, ~70 lines), and for each: status (✅ done and verified · 🟡 done but not executed in this environment · ❌ missing), the file path or command that proves it, and notes. Include the "Submission Checklist" from `GRADING.md` verbatim as checkboxes. Do not mark ✅ unless you actually ran/verified it.

---

## 10. QUALITY BAR

- Clean, idiomatic, typed, commented where non-obvious; no dead code, no TODO placeholders left in shipped files.
- Every config file has a short header comment explaining its purpose.
- No hardcoded environment-specific values; everything flows from variables/values files.
- Every runbook command is copy-paste correct and tested where possible.
- Consistent naming (`<slug>-backend`, `<slug>-frontend`, `<slug>-postgres`).
- The README alone should let a stranger run the stack locally in under 5 minutes and deploy to AWS in under an hour.

---

## 11. HUMAN-ONLY TASKS (the agent must list these clearly at the end; it cannot do them)

1. Create the GitHub repo, push, and grant Actions `packages: write` / enable GHCR visibility if needed; copy the green run URL.
2. Provide AWS credentials locally (never in Git) and run `terraform apply`; take AWS Console screenshots (VPC + EKS); run `terraform destroy` afterwards and screenshot it.
3. Install the ingress controller/ArgoCD/monitoring on the cluster per the runbooks, and capture the screenshots listed in `docs/EVIDENCE_CHECKLIST.md`.
4. **Record the demo video** following `docs/VIDEO_SCRIPT.md`; upload `demo/presentation.mp4` (or attach as a release asset and link it in the README). **No video = 0 for M10.**
5. Be able to explain one Trivy finding (or the clean result) and each architectural choice in the viva.
6. Verify the commit history shows ≥ 10 meaningful commits and no secrets (`gitleaks detect`).

---

## 12. FINAL REPORT FORMAT (print this when done)

1. **Summary** of what was built (domain, stack, highlights).
2. **Repo tree** (top 3 levels).
3. **Verification results** — each gate: command run → pass/fail (real output excerpts).
4. **Not executed** — everything that needs Docker/AWS/GitHub access you didn't have, and how to run it.
5. **Rubric self-score** (estimated per module, with honest caveats).
6. **Human-only checklist** (Section 11) with exact commands.
7. **Assumptions and known limitations.**

---

## 13. DEFINITION OF DONE

- [ ] `docker compose up --build` runs the full stack; UI works at `localhost:3000`
- [ ] `pytest` green, ≥ 15 tests, ≥ 80 % coverage, isolated DB, `pytest.ini` + `conftest.py`
- [ ] Both images non-root; frontend multi-stage; Trivy gates HIGH/CRITICAL
- [ ] CI: lint → test → frontend build → build both images → Trivy → push to GHCR with **SHA tags** → GitOps bump
- [ ] Terraform: valid HCL, VPC with ≥ 2 public subnets, EKS + node group + EBS CSI + metrics-server, tfvars example, clean destroy runbook
- [ ] Helm chart lints; ≥ 2 replicas; ClusterIP services; Ingress `/` + `/api`; HPA; PVC Postgres; migration hook Job
- [ ] ArgoCD Application with auto-sync/self-heal documented
- [ ] Prometheus scraping backend (ServiceMonitor), Grafana dashboard with live panels, alert rules
- [ ] Troubleshooting lab with runbook
- [ ] README complete; slides (pptx + pdf) generated; video script and evidence checklist ready
- [ ] `docs/RUBRIC_CHECK.md` honest and complete
- [ ] No secrets in repo or history; project is clearly original, not a TaskBoard clone

**Begin now. Start with Phase 0. After every phase, state what you verified and what you could not.**
