from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0002_ingestion_runs"
down_revision = "0001_init"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "ingestion_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("run_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("ingestion_runs")
