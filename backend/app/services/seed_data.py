"""
PodiumHQ Dev Database Seed Script
Idempotently populates the database with realistic hackathon events, rounds,
criteria, judges, teams, and scores for demo and development.
"""

import sys
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal, engine, Base
from backend.app.models.event import Event, EventStatus
from backend.app.models.team import Team, TeamStatus
from backend.app.models.judge import Judge
from backend.app.models.round import Round, RoundStatus
from backend.app.models.criterion import Criterion
from backend.app.models.score import Score
from backend.app.metrics import record_score_submission, update_team_status_gauge


def seed_database(db: Session) -> None:
    """Populates realistic seed data idempotently."""
    print("Checking if seed data already exists...")
    existing_event = db.query(Event).filter(Event.slug == "podiumhq-global-2026").first()
    if existing_event:
        print("Seed data already present. Skipping initialization.")
        return

    print("Creating initial event...")
    now = datetime.now(timezone.utc)
    event = Event(
        name="PodiumHQ Global DevSecOps & AI Hackathon",
        slug="podiumhq-global-2026",
        description="The premier global competition evaluating production-grade DevSecOps, Kubernetes resilience, GitOps automation, and full-stack excellence.",
        location="AWS ap-south-1 Virtual Cloud Arena",
        status=EventStatus.ACTIVE,
        max_teams=50,
        start_time=now - timedelta(days=2),
        end_time=now + timedelta(days=5),
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    print("Creating judging rounds...")
    round1 = Round(
        event_id=event.id,
        round_number=1,
        name="Round 1: Architecture & Hardened CI/CD",
        status=RoundStatus.OPEN,
        weight=1.0,
    )
    round2 = Round(
        event_id=event.id,
        round_number=2,
        name="Round 2: Production EKS, GitOps & Observability",
        status=RoundStatus.OPEN,
        weight=1.2,
    )
    db.add_all([round1, round2])
    db.commit()
    db.refresh(round1)
    db.refresh(round2)

    print("Creating weighted evaluation criteria...")
    criteria_r1 = [
        Criterion(
            round_id=round1.id,
            name="Security Hardening & Non-Root SecurityContext",
            description="Trivy scans zero-criticals, read-only root filesystems, dropped Linux capabilities, network isolation.",
            max_score=10.0,
            weight=0.35,
        ),
        Criterion(
            round_id=round1.id,
            name="CI/CD Pipeline Quality & SHA Immutability",
            description="Strict quality gates in order: lint, test, build, Trivy scan, GHCR push with commit SHA tags, no :latest.",
            max_score=10.0,
            weight=0.30,
        ),
        Criterion(
            round_id=round1.id,
            name="IaC & Kubernetes Multi-Replica Architecture",
            description="Terraform EKS + VPC modularity, Helm packaging, HPA horizontal scaling, migration Job hooks.",
            max_score=10.0,
            weight=0.20,
        ),
        Criterion(
            round_id=round1.id,
            name="Originality & Architecture Documentation",
            description="Distinctive non-generic domain, comprehensive Mermaid diagrams, ADRs, clean runbooks.",
            max_score=10.0,
            weight=0.15,
        ),
    ]

    criteria_r2 = [
        Criterion(
            round_id=round2.id,
            name="Prometheus Observability & Custom Metrics",
            description="ServiceMonitor integration, custom domain metrics, Grafana executive dashboards with live HPA panels.",
            max_score=10.0,
            weight=0.40,
        ),
        Criterion(
            round_id=round2.id,
            name="UI Aesthetics & Interactive Leaderboard UX",
            description="Bespoke Obsidian/Solar color palette, real-time rank delta indicators, responsive glassmorphism UI.",
            max_score=10.0,
            weight=0.35,
        ),
        Criterion(
            round_id=round2.id,
            name="Resilience & Troubleshooting Runbooks",
            description="Self-healing ArgoCD GitOps, zero-downtime rolling upgrades, documented failure recovery labs.",
            max_score=10.0,
            weight=0.25,
        ),
    ]

    db.add_all(criteria_r1 + criteria_r2)
    db.commit()

    print("Creating technical judges...")
    judges = [
        Judge(
            name="Dr. Aris Thorne",
            email="aris.thorne@clouddefense.io",
            organization="CloudDefense Labs",
            title="Principal Platform Architect",
        ),
        Judge(
            name="Maya Lin",
            email="maya.lin@kubernetes-wg.org",
            organization="Kubernetes SIG-Security",
            title="Senior Security Evaluator",
        ),
        Judge(
            name="Vikram Patel",
            email="vikram.patel@devsecops-summit.com",
            organization="Apex Cloud Systems",
            title="VP of Infrastructure & SRE",
        ),
        Judge(
            name="Elena Rostova",
            email="elena.rostova@gitops-alliance.net",
            organization="GitOps Standards Consortium",
            title="Distinguished Fellow",
        ),
    ]
    db.add_all(judges)
    db.commit()

    print("Creating hackathon teams...")
    teams = [
        Team(
            event_id=event.id,
            name="ZeroTrust Guard",
            project_title="eBPF-Powered Kubernetes Microsegmentation & Policy Shield",
            project_repo_url="https://github.com/nandukrishnak/zerotrust-guard",
            demo_url="https://zerotrust.podiumhq.local",
            track="DevSecOps & Platform Defense",
            status=TeamStatus.SCORED,
            submitted_at=now - timedelta(hours=28),
        ),
        Team(
            event_id=event.id,
            name="NeuroMesh Orchestrator",
            project_title="Autonomous Self-Healing Microservices with ArgoCD & eBPF",
            project_repo_url="https://github.com/nandukrishnak/neuromesh-k8s",
            demo_url="https://neuromesh.podiumhq.local",
            track="Cloud Native AI & Autonomous SRE",
            status=TeamStatus.SCORED,
            submitted_at=now - timedelta(hours=26),
        ),
        Team(
            event_id=event.id,
            name="VaultKube Sentinel",
            project_title="Hardware-Enclave Secrets Operator for EKS & KMS IRSA",
            project_repo_url="https://github.com/nandukrishnak/vaultkube-sentinel",
            demo_url="https://vaultkube.podiumhq.local",
            track="Zero-Trust Infrastructure",
            status=TeamStatus.SCORED,
            submitted_at=now - timedelta(hours=24),
        ),
        Team(
            event_id=event.id,
            name="PulseMetrics AI",
            project_title="Real-Time Metric Anomaly Detection with Prometheus Agent",
            project_repo_url="https://github.com/nandukrishnak/pulse-metrics",
            demo_url="https://pulse.podiumhq.local",
            track="Observability & Telemetry",
            status=TeamStatus.UNDER_REVIEW,
            submitted_at=now - timedelta(hours=18),
        ),
        Team(
            event_id=event.id,
            name="HyperScale Grid",
            project_title="Dynamic KEDA Event-Driven Workload Autoscaler on Spot EC2",
            project_repo_url="https://github.com/nandukrishnak/hyperscale-grid",
            demo_url="https://hyperscale.podiumhq.local",
            track="Infrastructure Optimization",
            status=TeamStatus.SUBMITTED,
            submitted_at=now - timedelta(hours=12),
        ),
        Team(
            event_id=event.id,
            name="CyberLedger X",
            project_title="Immutable Container Provenance & SBOM Cosign Verification",
            project_repo_url="https://github.com/nandukrishnak/cyberledger-x",
            demo_url="https://cyberledger.podiumhq.local",
            track="DevSecOps & Supply Chain",
            status=TeamStatus.REGISTERED,
            submitted_at=None,
        ),
        Team(
            event_id=event.id,
            name="DarkVector Exploiters",
            project_title="Bypassed Policy Engine PoC",
            project_repo_url="https://github.com/nandukrishnak/darkvector",
            demo_url="https://darkvector.podiumhq.local",
            track="Offensive Security",
            status=TeamStatus.DISQUALIFIED,
            submitted_at=now - timedelta(hours=35),
        ),
    ]
    db.add_all(teams)
    db.commit()

    print("Generating authentic judge scores across criteria...")
    # Seed scores for top teams
    score_matrix = [
        # ZeroTrust Guard (Leading podium contender)
        (judges[0].id, teams[0].id, round1.id, criteria_r1[0].id, 9.8, "Flawless non-root container profile and read-only FS."),
        (judges[0].id, teams[0].id, round1.id, criteria_r1[1].id, 9.6, "Clean GitHub Actions workflow using pinned commit SHAs."),
        (judges[0].id, teams[0].id, round1.id, criteria_r1[2].id, 9.5, "Terraform VPC + EKS modularity is production-grade."),
        (judges[0].id, teams[0].id, round1.id, criteria_r1[3].id, 9.7, "Extensive Mermaid architecture diagrams and ADRs."),
        (judges[1].id, teams[0].id, round1.id, criteria_r1[0].id, 9.9, "Zero Trivy CVEs, excellent dropped capabilities."),
        (judges[1].id, teams[0].id, round1.id, criteria_r1[1].id, 9.4, "Quality gates in correct sequential order."),
        (judges[1].id, teams[0].id, round1.id, criteria_r1[2].id, 9.6, "HPA and PDB configured with precision."),
        (judges[1].id, teams[0].id, round1.id, criteria_r1[3].id, 9.8, "Superb documentation clarity."),
        
        # NeuroMesh Orchestrator (Silver rank)
        (judges[0].id, teams[1].id, round1.id, criteria_r1[0].id, 9.2, "Solid security posture, minor memory limit tuning needed."),
        (judges[0].id, teams[1].id, round1.id, criteria_r1[1].id, 9.4, "Automated GitOps tag bumping works seamlessly."),
        (judges[0].id, teams[1].id, round1.id, criteria_r1[2].id, 9.3, "EKS add-ons like EBS CSI properly installed."),
        (judges[0].id, teams[1].id, round1.id, criteria_r1[3].id, 9.1, "Clear runbook for ArgoCD self-heal."),
        (judges[2].id, teams[1].id, round1.id, criteria_r1[0].id, 9.3, "Strong non-root configuration."),
        (judges[2].id, teams[1].id, round1.id, criteria_r1[1].id, 9.5, "Pipeline coverage gate passes cleanly."),
        (judges[2].id, teams[1].id, round1.id, criteria_r1[2].id, 9.2, "Multi-replica rolling updates verified."),
        (judges[2].id, teams[1].id, round1.id, criteria_r1[3].id, 9.0, "Great architectural rationale."),

        # VaultKube Sentinel (Bronze rank)
        (judges[1].id, teams[2].id, round1.id, criteria_r1[0].id, 8.8, "High security focus, good KMS IRSA binding."),
        (judges[1].id, teams[2].id, round1.id, criteria_r1[1].id, 8.9, "Clean CI triggers and caching."),
        (judges[1].id, teams[2].id, round1.id, criteria_r1[2].id, 8.7, "StatefulSet PVC setup functional."),
        (judges[1].id, teams[2].id, round1.id, criteria_r1[3].id, 8.9, "Solid decision records."),
        (judges[3].id, teams[2].id, round1.id, criteria_r1[0].id, 9.0, "Very secure container footprint."),
        (judges[3].id, teams[2].id, round1.id, criteria_r1[1].id, 8.8, "Well-structured unit and integration tests."),
        (judges[3].id, teams[2].id, round1.id, criteria_r1[2].id, 8.9, "Good Helm template rendering."),
        (judges[3].id, teams[2].id, round1.id, criteria_r1[3].id, 8.6, "Good troubleshooting lab."),

        # PulseMetrics AI (Under Review)
        (judges[2].id, teams[3].id, round1.id, criteria_r1[0].id, 8.2, "Decent security, need slightly stricter PDB."),
        (judges[2].id, teams[3].id, round1.id, criteria_r1[1].id, 8.4, "Fast builds with Docker Buildx."),
        (judges[2].id, teams[3].id, round1.id, criteria_r1[2].id, 8.0, "Good Prometheus metrics integration."),
        (judges[2].id, teams[3].id, round1.id, criteria_r1[3].id, 8.3, "Nice overview in README."),
    ]

    for j_id, t_id, r_id, c_id, raw, feedback in score_matrix:
        score_entry = Score(
            judge_id=j_id,
            team_id=t_id,
            round_id=r_id,
            criterion_id=c_id,
            raw_score=raw,
            feedback=feedback,
        )
        db.add(score_entry)
        record_score_submission(r_id, "Criteria Evaluation", raw)

    db.commit()

    # Update metric gauges
    counts = {
        TeamStatus.SCORED.value: 3,
        TeamStatus.UNDER_REVIEW.value: 1,
        TeamStatus.SUBMITTED.value: 1,
        TeamStatus.REGISTERED.value: 1,
        TeamStatus.DISQUALIFIED.value: 1,
    }
    update_team_status_gauge(counts)

    print("Database seeding completed successfully with 1 Event, 2 Rounds, 7 Criteria, 4 Judges, 7 Teams, and 28 Scores.")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        seed_database(session)
    finally:
        session.close()
