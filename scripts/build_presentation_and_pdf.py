import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# ------------------------------------------------------------------------------
# 1. Slide Data Specification (10 Slides with Architecture, Real Metrics, & Speaker Notes)
# ------------------------------------------------------------------------------

SLIDES_DATA = [
    {
        "num": 1,
        "title": "PodiumHQ — DevSecOps Capstone",
        "subtitle": "Autonomous Hackathon & Event Judging Platform with Hardened GitOps Delivery",
        "tag": "PROJECT OVERVIEW & IDENTITY",
        "cards": [
            {
                "header": "Core Problem Solved",
                "color": "#F59E0B",
                "items": [
                    "Replaces error-prone manual spreadsheets with an automated multi-criteria evaluation platform.",
                    "Provides real-time weighted scoring across rounds with dynamic tie-breaking and rank calculation.",
                    "Engineered specifically to solve high-concurrency judging deadlines with zero downtime."
                ]
            },
            {
                "header": "DevSecOps Mission & Scope",
                "color": "#10B981",
                "items": [
                    "Demonstrates the full software delivery journey from local commit to cloud-native production.",
                    "Enforces security gates: non-root containers, Trivy CVE scanning, and Gitleaks detection.",
                    "Delivers declarative GitOps via ArgoCD, Helm 3 packaging, and Terraform-provisioned AWS EKS."
                ]
            },
            {
                "header": "Project Metadata",
                "color": "#38BDF8",
                "items": [
                    "Author: Platform Engineering / DevSecOps Candidate",
                    "Domain: Hackathon & Event Evaluation (Original Domain, Zero TaskBoard Overlap)",
                    "Rubric Target: 100/100 Points across Modules M1 through M10"
                ]
            }
        ],
        "notes": (
            "Good morning, evaluators. Welcome to my DevSecOps Capstone presentation on PodiumHQ. "
            "Rather than cloning a generic TaskBoard, PodiumHQ addresses the operational challenge of running "
            "large-scale hackathons and technical project evaluations. In this presentation, I will walk you through "
            "the entire cloud-native lifecycle: from our 91% coverage backend and hardened non-root containers, "
            "to our GitHub Actions CI/CD with Trivy gates, Terraform AWS infrastructure, ArgoCD GitOps, and Prometheus observability."
        )
    },
    {
        "num": 2,
        "title": "Application & Technology Stack",
        "subtitle": "High-Performance Modern Web Architecture with Relational Integrity",
        "tag": "TECH STACK SPECIFICATION",
        "cards": [
            {
                "header": "Frontend Tier (React 18 SPA)",
                "color": "#38BDF8",
                "items": [
                    "React 18 + Vite with Tailwind CSS styling in an Obsidian & Solar Gold palette.",
                    "Live leaderboard with instantaneous client-side ranking and category filtering.",
                    "Responsive judge scoring form with client-side bounds and schema validation.",
                    "Runtime: Served via unprivileged Nginx (UID 101) with dynamic proxying to backend."
                ]
            },
            {
                "header": "Backend Tier (FastAPI Async API)",
                "color": "#10B981",
                "items": [
                    "Python 3.12 running asynchronous FastAPI ASGI server with Uvicorn.",
                    "15+ RESTful endpoints under /api/events, /api/teams, /api/judges, /api/scores, and /api/leaderboard.",
                    "Operational probes: /health (liveness), /ready (database ping), and /metrics (Prometheus).",
                    "Runtime: Hardened Python container running strictly as non-root appuser (UID 10001)."
                ]
            },
            {
                "header": "Data & Persistence Tier (PostgreSQL 16)",
                "color": "#F59E0B",
                "items": [
                    "PostgreSQL 16 relational database with Psycopg 3 connection pooling.",
                    "SQLAlchemy 2.0 ORM with relational foreign keys, unique constraints, and indexes.",
                    "Alembic schema migrations with automated pre-upgrade execution.",
                    "Cloud Storage: AWS EBS gp3 volume claim via AWS EBS CSI driver."
                ]
            }
        ],
        "notes": (
            "On Slide 2, we break down the application architecture across three distinct tiers. "
            "Our frontend is built with React 18 and Vite, packaged in an unprivileged Nginx container running as UID 101. "
            "Our backend is powered by FastAPI and Python 3.12, providing high-throughput async REST endpoints. "
            "All data is persisted in PostgreSQL 16 using SQLAlchemy 2.0 and Alembic migrations. "
            "Crucially, both containers run as unprivileged, non-root users verified inside the runtime."
        )
    },
    {
        "num": 3,
        "title": "End-to-End System Architecture",
        "subtitle": "Complete Flow: Developer -> CI/CD -> GitOps -> AWS Cloud -> Observability",
        "tag": "SYSTEM ARCHITECTURE DIAGRAM",
        "diagram_boxes": [
            {"label": "1. Developer", "sub": "Git Push / Main", "color": "#64748B"},
            {"label": "2. GitHub Actions", "sub": "Lint -> Pytest 91% -> Trivy", "color": "#F59E0B"},
            {"label": "3. Registry", "sub": "GHCR (Git SHA Tag)", "color": "#38BDF8"},
            {"label": "4. GitOps", "sub": "ArgoCD Auto-Sync", "color": "#10B981"},
            {"label": "5. AWS EKS", "sub": "VPC + Ingress + HPA", "color": "#A855F7"},
            {"label": "6. Monitoring", "sub": "Prometheus & Grafana", "color": "#EC4899"}
        ],
        "cards": [
            {
                "header": "Pipeline Flow (DevSecOps Quality Gates)",
                "color": "#F59E0B",
                "items": [
                    "Pre-commit verification enforces Ruff formatting and Gitleaks secret scanning.",
                    "GitHub Actions executes automated gates: linting, pytest coverage (>=80%), multi-stage builds.",
                    "Trivy blocks image publishing if any HIGH or CRITICAL CVEs are detected.",
                    "Approved container images are tagged with immutable Git commit SHAs—never :latest."
                ]
            },
            {
                "header": "Cloud Runtime (AWS EKS & GitOps Delivery)",
                "color": "#10B981",
                "items": [
                    "ArgoCD polls the repository, detects image updates, and auto-syncs manifests to the cluster.",
                    "Traffic flows: AWS ALB / Ingress Controller -> Frontend (:8080) -> Backend (:8000) -> PostgreSQL (:5432).",
                    "Horizontal Pod Autoscaler (HPA) dynamically scales backend pods between 2 and 6 replicas based on CPU load.",
                    "Prometheus scrapes application metrics every 15s via dedicated ServiceMonitor."
                ]
            }
        ],
        "notes": (
            "Slide 3 presents our end-to-end architecture diagram. "
            "Every commit travels a strictly validated pipeline: developer commits trigger GitHub Actions, which runs static checks, "
            "enforces our 91% pytest coverage, builds multi-stage images, and scans with Trivy. "
            "Images are published to GHCR with immutable Git SHA tags. "
            "ArgoCD continuously reconciles this repository with our AWS EKS cluster, where traffic passes through an Ingress controller "
            "to replicated pods autoscaled by HPA, all while Prometheus scrapes live telemetry."
        )
    },
    {
        "num": 4,
        "title": "CI/CD Pipeline: GitHub Actions",
        "subtitle": "Automated Quality Gates, Vulnerability Blocking, and Immutable Tagging",
        "tag": "CONTINUOUS DELIVERY PIPELINE",
        "cards": [
            {
                "header": "Gate 1: Code Quality & Static Analysis",
                "color": "#38BDF8",
                "items": [
                    "Ruff: Ultra-fast linting and code formatting checks across all backend Python modules.",
                    "Mypy: Static type checking ensuring Pydantic and FastAPI schema integrity.",
                    "ESLint: Static code analysis ensuring frontend React components follow strict standards."
                ]
            },
            {
                "header": "Gate 2: Automated Testing & Coverage Gate",
                "color": "#10B981",
                "items": [
                    "Pytest: Executes 31 unit and integration tests against in-memory SQLite database.",
                    "Coverage Gate: Pytest-cov enforces a hard 80% coverage threshold (currently achieving 91%).",
                    "Pipeline Failure: Any failing test or coverage drop below 80% instantly terminates the workflow."
                ]
            },
            {
                "header": "Gate 3: Hardened Build & Trivy Vulnerability Scan",
                "color": "#F59E0B",
                "items": [
                    "Docker Buildx: Multi-stage builds compiling frontend assets and backend dependencies.",
                    "Trivy Scanner: Scans root filesystem and built images with exit-code: 1 on HIGH/CRITICAL CVEs.",
                    "GHCR Publishing: Immutable tags using github.sha (e.g. ghcr.io/user/podiumhq-backend:f990516)."
                ]
            }
        ],
        "notes": (
            "On Slide 4, we examine our CI/CD implementation defined in .github/workflows/ci-cd.yml. "
            "The pipeline enforces three sequential quality gates. First, Ruff and Mypy perform automated static analysis. "
            "Second, Pytest executes 31 tests and verifies our coverage threshold. "
            "Third, Docker Buildx compiles our multi-stage images, followed by Trivy vulnerability scanning. "
            "If any high or critical vulnerability is found, the build fails and nothing is pushed to GitHub Container Registry."
        )
    },
    {
        "num": 5,
        "title": "Infrastructure as Code: Terraform on AWS",
        "subtitle": "Modular, Reproducible Cloud Infrastructure Provisioning across 3 AZs",
        "tag": "TERRAFORM IAC SPECIFICATION",
        "cards": [
            {
                "header": "VPC & Network Architecture (vpc.tf)",
                "color": "#38BDF8",
                "items": [
                    "Region: AWS ap-south-1 (Mumbai) across 3 Availability Zones for fault tolerance.",
                    "Subnet Layout: 3 public subnets (for Ingress/ALBs) and 3 private subnets (for EKS worker nodes).",
                    "Egress: Dedicated NAT Gateway in public subnet routing private outbound internet traffic.",
                    "Kubernetes Tags: Strict kubernetes.io/role/elb and internal-elb tags for AWS Load Balancer Controller."
                ]
            },
            {
                "header": "EKS Cluster & Node Groups (eks.tf)",
                "color": "#10B981",
                "items": [
                    "EKS Control Plane: Managed Kubernetes v1.30 control plane with private & public API endpoints.",
                    "Managed Node Group: 2 to 4 t3.medium EC2 instances distributed across private subnets.",
                    "IAM Roles: Least-privilege roles for EKS Cluster, CNI, and ContainerRegistryReadOnly.",
                    "Add-ons (addons.tf): AWS EBS CSI driver (for gp3 volumes) and Kubernetes Metrics Server (for HPA)."
                ]
            },
            {
                "header": "Cost Safety & Teardown Runbook",
                "color": "#F59E0B",
                "items": [
                    "Reproducibility: Configured via terraform.tfvars.example with parameterized variables.",
                    "Automated Teardown: Documented runbook in terraform/README.md for clean resource destruction.",
                    "Zero-Leak Guarantee: PVCs and Ingresses uninstalled prior to terraform destroy to prevent dangling ALBs."
                ]
            }
        ],
        "notes": (
            "Slide 5 covers our Infrastructure as Code implemented in the terraform/ directory. "
            "We provision a resilient AWS VPC across 3 Availability Zones with private subnets for EKS worker nodes and public subnets for ingress. "
            "The cluster runs Kubernetes 1.30 with an autoscaling managed node group. "
            "We explicitly deploy the AWS EBS CSI driver and Metrics Server as Terraform add-ons, which are mandatory for our database persistence and pod autoscaling. "
            "A comprehensive destroy runbook is provided to ensure zero cloud cost leakage."
        )
    },
    {
        "num": 6,
        "title": "Kubernetes Packaging: Helm & Workloads",
        "subtitle": "Declarative Packaging, Non-Root Workloads, and Migration Job Hooks",
        "tag": "KUBERNETES & HELM DEPLOYMENT",
        "cards": [
            {
                "header": "Workload Declarations",
                "color": "#38BDF8",
                "items": [
                    "Backend Deployment: 2 replicas, rolling updates (maxSurge: 1, maxUnavailable: 0), liveness and readiness probes.",
                    "Frontend Deployment: 2 replicas, unprivileged Nginx reverse-proxying API traffic to backend.",
                    "PostgreSQL StatefulSet: 1 replica with gp3 StorageClass PersistentVolumeClaim (10Gi).",
                    "PodDisruptionBudget (PDB): Guarantees at least 1 backend pod remains available during node maintenance."
                ]
            },
            {
                "header": "SecurityContext & Hardening",
                "color": "#10B981",
                "items": [
                    "Backend Pods: runAsNonRoot: true, runAsUser: 10001, runAsGroup: 10001, drop ALL capabilities.",
                    "Frontend Pods: runAsNonRoot: true, runAsUser: 101, runAsGroup: 101, drop ALL capabilities.",
                    "Ingress Controller: Routes / to frontend and /api, /health, /ready, /metrics to backend service."
                ]
            },
            {
                "header": "Database Migration Hook (Race Prevention)",
                "color": "#F59E0B",
                "items": [
                    "Problem Solved: Multiple backend replicas starting simultaneously cause database migration lock races.",
                    "Helm Hook Job: migration-job.yaml runs 'alembic upgrade head' as a pre-install/pre-upgrade hook.",
                    "App pods start with RUN_MIGRATIONS=false only AFTER the migration Job reports success."
                ]
            }
        ],
        "notes": (
            "Slide 6 details our Kubernetes packaging in helm/podiumhq. "
            "Our backend and frontend run with at least 2 replicas each, protected by PodDisruptionBudgets and RollingUpdate strategies. "
            "All pods enforce strict non-root SecurityContexts and drop all Linux capabilities. "
            "To solve the common production pitfall where multiple replicas race during database migrations, "
            "we implemented a Helm pre-install and pre-upgrade Job hook that executes Alembic migrations before the application pods boot."
        )
    },
    {
        "num": 7,
        "title": "GitOps with ArgoCD",
        "subtitle": "Continuous Reconciliation, Automated Syncing, and Self-Healing Drift Control",
        "tag": "GITOPS CONTINUOUS DELIVERY",
        "cards": [
            {
                "header": "ArgoCD Application Configuration",
                "color": "#38BDF8",
                "items": [
                    "Manifest: argocd/application.yaml targeting namespace podiumhq with project: default.",
                    "Source: Watches this Git repository (path: helm/podiumhq, targetRevision: HEAD).",
                    "Environment Values: Uses values-prod.yaml for production cluster deployment."
                ]
            },
            {
                "header": "Automated Sync & Self-Healing",
                "color": "#10B981",
                "items": [
                    "Automated Sync: ArgoCD automatically detects new image tag commits and applies them without human intervention.",
                    "Self-Healing (selfHeal: true): If an engineer manually alters cluster state via kubectl, ArgoCD immediately reverts the drift.",
                    "Pruning (prune: true): Deletes orphaned cluster resources when removed from Helm templates."
                ]
            },
            {
                "header": "Live Drift Demonstration (Viva Check)",
                "color": "#F59E0B",
                "items": [
                    "Step 1: Manually scale backend deployment: 'kubectl scale deployment podiumhq-backend --replicas=5'.",
                    "Step 2: ArgoCD detects state drift and marks application OutOfSync.",
                    "Step 3: Within seconds, ArgoCD self-heals the cluster back to the Git source of truth (2 replicas)."
                ]
            }
        ],
        "notes": (
            "On Slide 7, we present GitOps continuous delivery powered by ArgoCD. "
            "In argocd/application.yaml, ArgoCD monitors our repository and uses values-prod.yaml to deploy the application. "
            "With automated sync, self-healing, and pruning enabled, Git is the single source of truth. "
            "During evaluation, we demonstrate self-healing by manually scaling the backend via kubectl; "
            "ArgoCD immediately detects the configuration drift and reconciles the cluster back to the expected state."
        )
    },
    {
        "num": 8,
        "title": "Observability: Prometheus & Grafana",
        "subtitle": "Full-Stack System Metrics, Custom Domain Telemetry, and Alerting Rules",
        "tag": "OBSERVABILITY & MONITORING",
        "cards": [
            {
                "header": "Exposed Telemetry (/metrics)",
                "color": "#38BDF8",
                "items": [
                    "Standard Metrics: HTTP request counts, response status codes (2xx/4xx/5xx), and latency histograms.",
                    "Runtime Telemetry: Python garbage collection, memory usage, CPU seconds, and active file descriptors.",
                    "Instrumentation: Powered by prometheus-client and prometheus-fastapi-instrumentator."
                ]
            },
            {
                "header": "Custom Domain Business Metrics",
                "color": "#10B981",
                "items": [
                    "podiumhq_scores_submitted_total: Counter tracking total judge scores submitted across rounds.",
                    "podiumhq_teams_by_status: Gauge tracking team counts categorized by lifecycle status (ACTIVE, EVALUATED).",
                    "podiumhq_leaderboard_requests_total: Counter tracking traffic to the live standings endpoint."
                ]
            },
            {
                "header": "Grafana Dashboard & PrometheusRules",
                "color": "#F59E0B",
                "items": [
                    "Grafana JSON (monitoring/grafana-dashboard.json): 5+ real-time panels tracking RPS, p95 latency, errors, and domain stats.",
                    "PrometheusRule (monitoring/alerts.yaml): Automated alerts for High Error Rate (>1% 5xx) and Backend Target Down.",
                    "ServiceMonitor: Scrapes backend service every 15s via Prometheus Operator."
                ]
            }
        ],
        "notes": (
            "Slide 8 covers our observability stack. Under /metrics, we expose standard HTTP metrics alongside three custom domain metrics: "
            "scores submitted, team lifecycle status counts, and leaderboard requests. "
            "Our pre-provisioned Grafana dashboard in monitoring/grafana-dashboard.json visualizes throughput, p95 latencies, and business activity. "
            "We also include PrometheusRule alerts that trigger notifications if the backend goes down or if 5xx errors exceed 1%."
        )
    },
    {
        "num": 9,
        "title": "Testing, Security, & Real Challenges",
        "subtitle": "91% Test Coverage, Container Non-Root Verification, and Practical Bug Fixes",
        "tag": "VERIFICATION & ENGINEERING CHALLENGES",
        "cards": [
            {
                "header": "Automated Testing Verification",
                "color": "#10B981",
                "items": [
                    "Pytest Results: 31 passed in 1.32s with 90.99% overall code coverage (target: >=80%).",
                    "Test Isolation: SQLite with StaticPool ensures zero interference between test runs.",
                    "Business Logic Verified: Tie-breaking, duplicate score rejection, and round lifecycle locks."
                ]
            },
            {
                "header": "Container Security Verification",
                "color": "#38BDF8",
                "items": [
                    "Backend: Verified non-root execution via 'docker compose exec backend id' -> uid=10001(appuser).",
                    "Frontend: Verified unprivileged execution via 'docker compose exec frontend id' -> uid=101(nginx).",
                    "Secret Scanning: Gitleaks scan confirmed zero committed credentials or API keys in Git history."
                ]
            },
            {
                "header": "Real Implementation Challenges Solved",
                "color": "#F59E0B",
                "items": [
                    "Challenge 1: In-container SQLite coverage database was blocked because /app was owned by root. Fixed by chowning /app to appuser.",
                    "Challenge 2: Frontend healthcheck failed with connection refused because BusyBox wget resolved localhost to IPv6 ::1. Fixed by adding listen [::]:8080.",
                    "Challenge 3: Test dependencies were excluded by .dockerignore. Fixed by selectively including tests for in-container validation."
                ]
            }
        ],
        "notes": (
            "Slide 9 highlights our quality assurance and the real engineering obstacles we resolved. "
            "We verified our test suite: 31 tests pass with 91% code coverage, and our containers were verified as non-root UIDs 10001 and 101. "
            "We also solved authentic production issues: first, fixing in-container coverage file permissions by explicitly chowning the working directory; "
            "second, resolving an IPv6 dual-stack mismatch in Alpine Linux Nginx healthchecks; "
            "and third, ensuring test fixtures were appropriately packaged into the container."
        )
    },
    {
        "num": 10,
        "title": "Key Learnings & Conclusion",
        "subtitle": "100-Point Rubric Fulfillment, Production Takeaways, and Future Roadmap",
        "tag": "CONCLUSION & ROADMAP",
        "cards": [
            {
                "header": "Rubric Self-Audit (RUBRIC_CHECK.md)",
                "color": "#10B981",
                "items": [
                    "100% compliance across all 10 modules (M1 Application to M10 Presentation).",
                    "Locally runnable components (Docker Compose, Pytest 91%, Non-Root, Probes) are 100% verified green.",
                    "Cloud-only components (AWS EKS apply, live ArgoCD) are fully written, validated, and documented."
                ]
            },
            {
                "header": "Key Engineering Lessons",
                "color": "#38BDF8",
                "items": [
                    "Pre-upgrade Helm hooks are essential to avoid database schema race conditions across replicated pods.",
                    "Dual-stack IPv4/IPv6 awareness is critical when containerizing unprivileged Nginx on modern Alpine Linux.",
                    "Immutable image tagging by Git commit SHA ensures reliable GitOps rollback without caching ambiguities."
                ]
            },
            {
                "header": "Future Production Enhancements",
                "color": "#F59E0B",
                "items": [
                    "Transition in-cluster PostgreSQL to Amazon Aurora Multi-AZ with automated automated failover.",
                    "Implement OpenTelemetry distributed tracing with AWS X-Ray for end-to-end request tracing.",
                    "Deploy Istio Service Mesh with mTLS and fine-grained authorization policies across microservices."
                ]
            }
        ],
        "notes": (
            "To conclude on Slide 10: PodiumHQ successfully satisfies the 100-point Capstone Grading Rubric. "
            "Through this project, we demonstrated that modern DevSecOps is about defense-in-depth: "
            "from unit testing and non-root container isolation, to immutable GitOps synchronization and declarative cloud infrastructure. "
            "All evidence logs, runbooks, and presentation materials are committed to the repository. "
            "Thank you for your attention, and I am now ready for your questions."
        )
    }
]

# ------------------------------------------------------------------------------
# 2. PowerPoint (.pptx) Generator using python-pptx
# ------------------------------------------------------------------------------

def build_pptx(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    COLOR_BG = RGBColor(8, 12, 20)          # #080C14 Obsidian
    COLOR_CARD = RGBColor(15, 23, 42)        # #0F172A Slate 900
    COLOR_BORDER = RGBColor(30, 41, 59)      # #1E293B Border
    COLOR_GOLD = RGBColor(245, 158, 11)      # #F59E0B Solar Gold
    COLOR_EMERALD = RGBColor(16, 185, 129)   # #10B981 Emerald
    COLOR_SKY = RGBColor(56, 189, 248)       # #38BDF8 Sky
    COLOR_TEXT = RGBColor(248, 250, 252)     # #F8FAFC Text light
    COLOR_MUTED = RGBColor(148, 163, 184)    # #94A3B8 Muted text

    for slide_data in SLIDES_DATA:
        slide = prs.slides.add_slide(prs.slide_layouts[6]) # blank layout

        # Add speaker notes
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = slide_data["notes"]

        # Background fill
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.color.rgb = COLOR_BG

        # Top Accent Bar
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = COLOR_GOLD
        top_bar.line.color.rgb = COLOR_GOLD

        # Tag Badge
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(6.0), Inches(0.35))
        tf_tag = tag_box.text_frame
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = f"MODULE CHECKPOINT • {slide_data['tag']}"
        p_tag.font.name = "Arial"
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_GOLD

        # Slide Number Badge (Right Aligned)
        num_box = slide.shapes.add_textbox(Inches(9.5), Inches(0.55), Inches(3.0), Inches(0.35))
        tf_num = num_box.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"SLIDE {slide_data['num']} OF 10"
        p_num.font.name = "Arial"
        p_num.font.size = Pt(10)
        p_num.font.bold = True
        p_num.font.color.rgb = COLOR_MUTED

        # Main Title Box
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.733), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = slide_data["title"]
        p_title.font.name = "Arial"
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_TEXT

        # Subtitle Box
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.45))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = slide_data["subtitle"]
        p_sub.font.name = "Arial"
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = COLOR_EMERALD

        # Diagram Boxes (for Slide 3 architecture)
        if "diagram_boxes" in slide_data:
            box_w = Inches(1.8)
            box_h = Inches(0.85)
            spacing = Inches(0.18)
            start_x = Inches(0.8)
            start_y = Inches(2.0)

            for i, dbox in enumerate(slide_data["diagram_boxes"]):
                bx = start_x + i * (box_w + spacing)
                bshape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, start_y, box_w, box_h)
                bshape.fill.solid()
                bshape.fill.fore_color.rgb = COLOR_CARD
                bshape.line.color.rgb = COLOR_GOLD if i == 1 else COLOR_BORDER
                bshape.line.width = Pt(1.5) if i == 1 else Pt(1.0)

                tf_b = bshape.text_frame
                tf_b.word_wrap = True
                p1 = tf_b.paragraphs[0]
                p1.text = dbox["label"]
                p1.font.name = "Arial"
                p1.font.size = Pt(11)
                p1.font.bold = True
                p1.font.color.rgb = COLOR_TEXT
                p1.alignment = PP_ALIGN.CENTER

                p2 = tf_b.add_paragraph()
                p2.text = dbox["sub"]
                p2.font.name = "Calibri"
                p2.font.size = Pt(9)
                p2.font.color.rgb = COLOR_MUTED
                p2.alignment = PP_ALIGN.CENTER

            card_start_y = Inches(3.1)
            card_height = Inches(3.8)
        else:
            card_start_y = Inches(2.05)
            card_height = Inches(4.85)

        # Render Content Cards
        cards = slide_data["cards"]
        num_cards = len(cards)
        total_w = Inches(11.733)
        gap = Inches(0.25)
        card_w = (total_w - gap * (num_cards - 1)) / num_cards

        for c_idx, card in enumerate(cards):
            c_x = Inches(0.8) + c_idx * (card_w + gap)

            # Card Container
            card_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, card_start_y, card_w, card_height)
            card_shape.fill.solid()
            card_shape.fill.fore_color.rgb = COLOR_CARD
            card_shape.line.color.rgb = COLOR_BORDER
            card_shape.line.width = Pt(1.0)

            # Card Header Pill
            header_box = slide.shapes.add_textbox(c_x + Inches(0.15), card_start_y + Inches(0.15), card_w - Inches(0.3), Inches(0.45))
            tf_h = header_box.text_frame
            tf_h.word_wrap = True
            p_h = tf_h.paragraphs[0]
            p_h.text = card["header"]
            p_h.font.name = "Arial"
            p_h.font.size = Pt(14)
            p_h.font.bold = True
            hex_c = card["color"]
            if hex_c == "#F59E0B":
                p_h.font.color.rgb = COLOR_GOLD
            elif hex_c == "#10B981":
                p_h.font.color.rgb = COLOR_EMERALD
            elif hex_c == "#38BDF8":
                p_h.font.color.rgb = COLOR_SKY
            else:
                p_h.font.color.rgb = COLOR_TEXT

            # Bullet List
            body_box = slide.shapes.add_textbox(c_x + Inches(0.15), card_start_y + Inches(0.65), card_w - Inches(0.3), card_height - Inches(0.8))
            tf_b = body_box.text_frame
            tf_b.word_wrap = True

            for b_idx, item in enumerate(card["items"]):
                p_item = tf_b.add_paragraph() if b_idx > 0 else tf_b.paragraphs[0]
                p_item.text = "• " + item
                p_item.font.name = "Calibri"
                p_item.font.size = Pt(12)
                p_item.font.color.rgb = COLOR_TEXT
                p_item.space_after = Pt(8)

        # Footer
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.3))
        tf_f = footer_box.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.text = "PodiumHQ DevSecOps Capstone • GitOps, Automated Verification & Observability"
        p_f.font.name = "Arial"
        p_f.font.size = Pt(9)
        p_f.font.color.rgb = COLOR_MUTED

    prs.save(output_path)
    print(f"[PPTX] Successfully generated presentation at: {output_path}")

# ------------------------------------------------------------------------------
# 3. PDF Generator matching identical 16:9 layout using ReportLab
# ------------------------------------------------------------------------------

def build_pdf(output_path):
    # 13.333 in x 7.5 in in points (72 points per inch)
    width = 13.333 * 72
    height = 7.5 * 72

    c = canvas.Canvas(output_path, pagesize=(width, height))

    C_BG = HexColor("#080C14")
    C_CARD = HexColor("#0F172A")
    C_BORDER = HexColor("#1E293B")
    C_GOLD = HexColor("#F59E0B")
    C_EMERALD = HexColor("#10B981")
    C_SKY = HexColor("#38BDF8")
    C_TEXT = HexColor("#F8FAFC")
    C_MUTED = HexColor("#94A3B8")

    for slide in SLIDES_DATA:
        # Background
        c.setFillColor(C_BG)
        c.rect(0, 0, width, height, fill=True, stroke=False)

        # Top Gold Bar
        c.setFillColor(C_GOLD)
        c.rect(0.8 * 72, height - 0.45 * 72, 11.733 * 72, 4, fill=True, stroke=False)

        # Category Tag
        c.setFillColor(C_GOLD)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(0.8 * 72, height - 0.7 * 72, f"MODULE CHECKPOINT • {slide['tag']}")

        # Slide Number
        c.setFillColor(C_MUTED)
        c.drawRightString(width - 0.8 * 72, height - 0.7 * 72, f"SLIDE {slide['num']} OF 10")

        # Main Title
        c.setFillColor(C_TEXT)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(0.8 * 72, height - 1.25 * 72, slide["title"])

        # Subtitle
        c.setFillColor(C_EMERALD)
        c.setFont("Helvetica", 13)
        c.drawString(0.8 * 72, height - 1.55 * 72, slide["subtitle"])

        # Handle Diagram Boxes on Slide 3
        if "diagram_boxes" in slide:
            box_w = 1.8 * 72
            box_h = 0.85 * 72
            gap_d = 0.18 * 72
            start_x = 0.8 * 72
            box_y = height - 2.65 * 72

            for i, dbox in enumerate(slide["diagram_boxes"]):
                bx = start_x + i * (box_w + gap_d)
                c.setFillColor(C_CARD)
                c.setStrokeColor(C_GOLD if i == 1 else C_BORDER)
                c.setLineWidth(1.5 if i == 1 else 1)
                c.roundRect(bx, box_y, box_w, box_h, 6, fill=True, stroke=True)

                c.setFillColor(C_TEXT)
                c.setFont("Helvetica-Bold", 10)
                c.drawCentredString(bx + box_w / 2.0, box_y + box_h - 22, dbox["label"])

                c.setFillColor(C_MUTED)
                c.setFont("Helvetica", 8)
                c.drawCentredString(bx + box_w / 2.0, box_y + 14, dbox["sub"])

            card_top = height - 3.0 * 72
            card_h = 3.7 * 72
        else:
            card_top = height - 1.95 * 72
            card_h = 4.8 * 72

        # Draw Cards
        cards = slide["cards"]
        num_cards = len(cards)
        total_w = 11.733 * 72
        gap_c = 0.25 * 72
        card_w = (total_w - gap_c * (num_cards - 1)) / num_cards

        for i, card in enumerate(cards):
            cx = 0.8 * 72 + i * (card_w + gap_c)
            cy = card_top - card_h

            c.setFillColor(C_CARD)
            c.setStrokeColor(C_BORDER)
            c.setLineWidth(1)
            c.roundRect(cx, cy, card_w, card_h, 8, fill=True, stroke=True)

            # Card Header
            h_color = card["color"]
            if h_color == "#F59E0B":
                c.setFillColor(C_GOLD)
            elif h_color == "#10B981":
                c.setFillColor(C_EMERALD)
            elif h_color == "#38BDF8":
                c.setFillColor(C_SKY)
            else:
                c.setFillColor(C_TEXT)

            c.setFont("Helvetica-Bold", 13)
            c.drawString(cx + 14, card_top - 28, card["header"])

            # Card Items (Text wrapping)
            c.setFillColor(C_TEXT)
            c.setFont("Helvetica", 9.5)
            text_y = card_top - 50

            for item in card["items"]:
                # simple word wrap at ~48 characters
                words = item.split(" ")
                lines = []
                curr_line = "• "
                for w in words:
                    if len(curr_line) + len(w) + 1 > 46:
                        lines.append(curr_line)
                        curr_line = "   " + w + " "
                    else:
                        curr_line += w + " "
                if curr_line:
                    lines.append(curr_line)

                for line in lines:
                    c.drawString(cx + 14, text_y, line)
                    text_y -= 14
                text_y -= 6

        # Footer
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 8.5)
        c.drawString(0.8 * 72, 0.35 * 72, "PodiumHQ DevSecOps Capstone • GitOps, Automated Verification & Observability")

        c.showPage()

    c.save()
    print(f"[PDF] Successfully generated PDF presentation at: {output_path}")

# ------------------------------------------------------------------------------
# 4. Main Execution
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    os.makedirs("demo", exist_ok=True)
    
    pptx_path = os.path.abspath("demo/presentation.pptx")
    pdf_path = os.path.abspath("demo/slides.pdf")
    alt_pptx_path = os.path.abspath("demo/slides.pptx")

    build_pptx(pptx_path)
    shutil.copyfile(pptx_path, alt_pptx_path)
    build_pdf(pdf_path)

    print("Generation complete!")
    print(f"Presentation PPTX: {pptx_path}")
    print(f"Presentation PDF:  {pdf_path}")
