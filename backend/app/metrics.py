"""
PodiumHQ Prometheus Metrics Module
Defines custom domain metrics and instrumentation hooks.
"""

from prometheus_client import Counter, Gauge, Histogram

# Custom Domain Metrics
SCORES_SUBMITTED_TOTAL = Counter(
    "podiumhq_scores_submitted_total",
    "Total number of judge scores submitted across all rounds and criteria",
    ["round_id", "criterion_name"],
)

TEAMS_BY_STATUS = Gauge(
    "podiumhq_teams_by_status",
    "Current count of hackathon teams categorized by evaluation lifecycle status",
    ["status"],
)

SCORE_VALUE_HISTOGRAM = Histogram(
    "podiumhq_score_value",
    "Distribution of individual score values awarded by judges",
    buckets=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
)

LEADERBOARD_REQUESTS_TOTAL = Counter(
    "podiumhq_leaderboard_requests_total",
    "Total number of times the live leaderboard has been requested or streamed",
    ["event_slug"],
)

JUDGE_EVALUATION_DURATION_SECONDS = Histogram(
    "podiumhq_judge_evaluation_duration_seconds",
    "Time taken by judges to submit round evaluations",
    buckets=[1, 5, 10, 30, 60, 120, 300],
)


def record_score_submission(round_id: int, criterion_name: str, score_value: float) -> None:
    """Helper to record metrics whenever a score is submitted."""
    SCORES_SUBMITTED_TOTAL.labels(round_id=str(round_id), criterion_name=criterion_name).inc()
    SCORE_VALUE_HISTOGRAM.observe(score_value)


def update_team_status_gauge(status_counts: dict) -> None:
    """Updates team status gauges based on database aggregate counts."""
    for status, count in status_counts.items():
        TEAMS_BY_STATUS.labels(status=str(status)).set(count)
