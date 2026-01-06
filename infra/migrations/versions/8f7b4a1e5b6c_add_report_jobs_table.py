"""Add report jobs table"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import ENUM

revision = "8f7b4a1e5b6c"
down_revision = "6efde1f16e9f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enum only if it doesn't exist (handle migration tree branching)
    conn = op.get_bind()
    result = conn.execute(sa.text(
        "SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'reportjobstatus')"
    ))
    if not result.scalar():
        conn.execute(sa.text(
            "CREATE TYPE reportjobstatus AS ENUM ('pending', 'running', 'success', 'failure')"
        ))

    # Create table using existing enum
    op.create_table(
        "report_jobs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("symbol", sa.String(length=64), nullable=True),
        sa.Column("parameters", sa.JSON(), nullable=True),
        sa.Column("status", ENUM('pending', 'running', 'success', 'failure', name='reportjobstatus', create_type=False), nullable=False, server_default="pending"),
        sa.Column("file_path", sa.String(length=512), nullable=True),
    )
    op.create_index(op.f("ix_report_jobs_symbol"), "report_jobs", ["symbol"])
    op.alter_column("report_jobs", "status", server_default=None)


def downgrade() -> None:
    op.drop_index(op.f("ix_report_jobs_symbol"), table_name="report_jobs")
    op.drop_table("report_jobs")
    status_enum.drop(op.get_bind(), checkfirst=True)
