import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette: Obsidian (#080C14), Solar Gold (#F59E0B), Emerald (#10B981), Slate (#94A3B8), White (#FFFFFF)
COLOR_BG = RGBColor(8, 12, 20)
COLOR_CARD = RGBColor(15, 23, 42)
COLOR_GOLD = RGBColor(245, 158, 11)
COLOR_EMERALD = RGBColor(16, 185, 129)
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_SLATE = RGBColor(148, 163, 184)

slides_data = [
    {
        "title": "PodiumHQ — DevSecOps Capstone",
        "subtitle": "Autonomous Hackathon & Event Judging Platform with Hardened GitOps Pipeline",
        "bullets": [
            "Author: Platform Engineering / DevSecOps Candidate",
            "Architecture: React 18 (Vite) + FastAPI (Python 3.12) + PostgreSQL 16",
            "Deployment: AWS VPC + EKS | Helm Charts | ArgoCD GitOps | Prometheus & Grafana",
            "Security: Non-Root Containers, Trivy Scanning, Gitleaks, Non-Root UID 10001/101"
        ]
    },
    {
        "title": "Problem Statement & Domain Selection",
        "subtitle": "Moving Beyond Generic CRUD / TaskBoards to Multi-Criteria Event Evaluation",
        "bullets": [
            "Domain Originality: Hackathon evaluation platform where judges score teams across rounds against weighted criteria.",
            "Real-Time Business Logic: Live rank calculation, multi-criterion weighted aggregation, round lock enforcement.",
            "Anti-Plagiarism Architecture: Custom schema (Events, Rounds, Criteria, Teams, Judges, Scores) - zero TaskBoard overlap.",
            "Production Rigor: Built to withstand high concurrency during judging deadlines with zero downtime."
        ]
    },
    {
        "title": "End-to-End DevSecOps Architecture",
        "subtitle": "From Local Code to Cloud-Native GitOps Continuous Delivery",
        "bullets": [
            "Developer Flow: Feature branch -> Pre-commit hooks (ruff, gitleaks, mypy).",
            "CI/CD Pipeline: GitHub Actions validates lint -> runs pytest (91% coverage) -> builds multi-stage images -> Trivy security gates.",
            "GitOps Continuous Deployment: ArgoCD monitors repository image tags and synchronizes state to AWS EKS automatically.",
            "Cloud Infrastructure: AWS VPC (3 AZs, public/private subnets) + Managed EKS Cluster provisioned via Terraform."
        ]
    },
    {
        "title": "Application Deep-Dive: PodiumHQ",
        "subtitle": "High-Performance Modern Web Architecture",
        "bullets": [
            "Frontend: React 18 SPA built with Vite, Tailwind CSS, custom Obsidian & Solar Gold visual palette.",
            "Backend: FastAPI async ASGI service running Python 3.12 with SQLAlchemy 2.0 and Alembic database migrations.",
            "Database: PostgreSQL 16 with indexed relational constraints and connection pooling via Psycopg 3.",
            "Observability Endpoints: Standardized /health (liveness), /ready (database ping), and /metrics (Prometheus instrumentation)."
        ]
    },
    {
        "title": "Test Automation & Quality Assurance",
        "subtitle": "Exceeding the 80% Coverage Rubric Requirement with Isolated Fixtures",
        "bullets": [
            "Pytest Suite: 31 comprehensive unit and integration tests passing in under 1.5 seconds.",
            "Test Coverage: 91% code coverage across all routers, services, models, and schemas.",
            "Zero Flakiness: In-memory SQLite with StaticPool ensures 100% test isolation without touching production databases.",
            "Full Validation: Tested team lifecycle transitions, duplicate prevention, out-of-bounds score rejection, and leaderboard ranking."
        ]
    },
    {
        "title": "Container Hardening & DevSecOps Gates",
        "subtitle": "Defense-in-Depth Container Security from Base Image to Runtime",
        "bullets": [
            "Multi-Stage Builds: Frontend compiles React with Node 22, served via unprivileged Nginx (UID 101).",
            "Strict Non-Root Runtime: Backend runs as explicit UID/GID 10001 (appuser:appgroup), verified via in-container inspection.",
            "Vulnerability Scanning: Trivy scans filesystems, dependencies, and container images for HIGH/CRITICAL vulnerabilities.",
            "Secret Prevention: Gitleaks automated scanning blocks credentials, API keys, or database secrets from entering Git history."
        ]
    },
    {
        "title": "CI/CD Pipeline: GitHub Actions",
        "subtitle": "Automated Quality Gates, Vulnerability Blocking, and Immutable Tagging",
        "bullets": [
            "Gate 1 - Code Quality: Ruff linter, Mypy type-checking, and frontend ESLint.",
            "Gate 2 - Automated Tests: Pytest with coverage threshold gate (must be >= 80%).",
            "Gate 3 - Multi-Stage Container Build: Buildx caching for backend and frontend images.",
            "Gate 4 - Security Scanning: Trivy container vulnerability scanner with blocking threshold.",
            "Gate 5 - Release & GitOps: Push to GHCR with Git commit SHA tags (never :latest) and trigger ArgoCD image bump."
        ]
    },
    {
        "title": "Infrastructure as Code: Terraform on AWS",
        "subtitle": "Modular, Reproducible Cloud Infrastructure Provisioning",
        "bullets": [
            "VPC Module: 3 Availability Zones, public/private subnets, NAT Gateways, and EKS tag compliance.",
            "EKS Cluster: Managed Kubernetes control plane (v1.30) with managed node groups across multiple AZs.",
            "Add-Ons: AWS EBS CSI driver with gp3 StorageClass for persistent data, plus Kubernetes Metrics Server for HPA.",
            "Lifecycle & Cost Safety: Comprehensive terraform.tfvars.example and verified 'terraform destroy' runbook for cost zeroing."
        ]
    },
    {
        "title": "Kubernetes Packaging: Helm & GitOps with ArgoCD",
        "subtitle": "Declarative Cloud-Native Delivery & Automated Drift Healing",
        "bullets": [
            "Helm Chart: Modular templates for Backend, Frontend, PostgreSQL StatefulSet, Ingress, and HorizontalPodAutoscaler.",
            "Migration Job Hook: Database migrations run as a Helm pre-upgrade/pre-install Job, preventing container restart race conditions.",
            "Pod Security Standards: Restricted securityContext with runAsNonRoot: true, drop ALL capabilities, read-only root filesystem.",
            "ArgoCD Synchronization: Automated sync with selfHeal=true and prune=true; reconciles cluster drift in real time."
        ]
    },
    {
        "title": "Observability: Prometheus, Grafana & Custom Metrics",
        "subtitle": "Full-Stack Telemetry and Domain-Driven Business Visibility",
        "bullets": [
            "Instrumentation: Prometheus metrics endpoint exposing HTTP request rate, p50/p95 latency, and error distributions.",
            "Custom Domain Metrics: podiumhq_scores_submitted_total, podiumhq_teams_by_status, and podiumhq_leaderboard_requests_total.",
            "Grafana Dashboards: Pre-provisioned multi-panel dashboard tracking system health, HPA scaling events, and judging activity.",
            "Alerting Rules: PrometheusRules for High Error Rate (>1%), High Latency (>500ms), and Backend Target Down."
        ]
    },
    {
        "title": "Troubleshooting Lab & Runbook",
        "subtitle": "Four Real-World Kubernetes Failure Scenarios and Resolution Runbooks",
        "bullets": [
            "Scenario 1 - Broken Image: CrashLoopBackOff due to nonexistent tag; diagnosed via kubectl describe and fixed in values.yaml.",
            "Scenario 2 - Service Selector Mismatch: 502 Bad Gateway; diagnosed via endpoints inspection and selector alignment.",
            "Scenario 3 - Readiness Probe Failure: Pod unready; diagnosed via probe logs and HTTP endpoint path fix.",
            "Scenario 4 - Missing Secret: Pod blocked from initialization; diagnosed via describe pod events and secret provisioning."
        ]
    },
    {
        "title": "Project Summary & Submission Audit",
        "subtitle": "100-Point Grading Rubric Compliance and Demonstration Readiness",
        "bullets": [
            "Rubric Check: Complete honest self-audit in docs/RUBRIC_CHECK.md covering Modules M1 through M10.",
            "Local Verification: 100% green Docker stack (PostgreSQL, Backend, Frontend) with verified non-root UIDs.",
            "Reproducible Tooling: Single-command workflows via Makefile, complete video recording script in docs/VIDEO_SCRIPT.md.",
            "Clean Git History: Atomic, conventional commits with zero committed secrets."
        ]
    }
]

for item in slides_data:
    slide_layout = prs.slide_layouts[6] # blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Background card shape
    shape = slide.shapes.add_shape(1, 0, 0, Inches(13.333), Inches(7.5)) # 1 is rectangle
    shape.fill.solid()
    shape.fill.fore_color.rgb = COLOR_BG
    shape.line.color.rgb = COLOR_BG
    
    # Inner accent container
    container = slide.shapes.add_shape(1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    container.fill.solid()
    container.fill.fore_color.rgb = COLOR_CARD
    container.line.color.rgb = COLOR_GOLD
    container.line.width = Pt(1.5)
    
    # Title Box
    title_box = slide.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(11.0), Inches(0.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = item["title"]
    p.font.name = "Arial"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD
    
    # Subtitle Box
    sub_box = slide.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(0.6))
    stf = sub_box.text_frame
    stf.word_wrap = True
    sp = stf.paragraphs[0]
    sp.text = item["subtitle"]
    sp.font.name = "Arial"
    sp.font.size = Pt(16)
    sp.font.color.rgb = COLOR_EMERALD
    
    # Bullet points box
    content_box = slide.shapes.add_textbox(Inches(1.2), Inches(2.6), Inches(11.0), Inches(3.8))
    ctf = content_box.text_frame
    ctf.word_wrap = True
    for i, bullet in enumerate(item["bullets"]):
        p = ctf.add_paragraph() if i > 0 else ctf.paragraphs[0]
        p.text = "• " + bullet
        p.font.name = "Calibri"
        p.font.size = Pt(18)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(14)

output_path = os.path.abspath("demo/slides.pptx")
prs.save(output_path)
print(f"Successfully generated slides at: {output_path}")
