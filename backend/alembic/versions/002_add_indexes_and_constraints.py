"""002_add_indexes_and_constraints

Revision ID: 002_add_indexes_and_constraints
Revises: 001_initial_schema
Create Date: 2026-10-16 12:30:00.000000

"""

from typing import Sequence, Union

from alembic import op

revision: str = "002_add_indexes_and_constraints"
down_revision: Union[str, None] = "001_initial_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Performance composite indexes and constraints using batch_alter_table for SQLite + Postgres compatibility
    with op.batch_alter_table("scores") as batch_op:
        batch_op.create_index("ix_scores_team_round", ["team_id", "round_id"], unique=False)
        batch_op.create_unique_constraint(
            "uq_judge_team_round_criterion", ["judge_id", "team_id", "round_id", "criterion_id"]
        )

    with op.batch_alter_table("teams") as batch_op:
        batch_op.create_index("ix_teams_status", ["status"], unique=False)
        batch_op.create_index("ix_teams_event_status", ["event_id", "status"], unique=False)


def downgrade() -> None:
    with op.batch_alter_table("teams") as batch_op:
        batch_op.drop_index("ix_teams_event_status")
        batch_op.drop_index("ix_teams_status")

    with op.batch_alter_table("scores") as batch_op:
        batch_op.drop_constraint("uq_judge_team_round_criterion", type_="unique")
        batch_op.drop_index("ix_scores_team_round")
