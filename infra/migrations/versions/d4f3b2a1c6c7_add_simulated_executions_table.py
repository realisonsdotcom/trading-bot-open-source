"""Create table for simulated executions used in dry-run mode."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "d4f3b2a1c6c7"
down_revision = "c3a2b1d4e5f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "simulated_executions",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("simulation_id", sa.String(length=128), nullable=False),
        sa.Column("correlation_id", sa.String(length=128), nullable=True),
        sa.Column("account_id", sa.String(length=64), nullable=False),
        sa.Column("broker", sa.String(length=32), nullable=False),
        sa.Column("venue", sa.String(length=64), nullable=False),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("side", sa.String(length=8), nullable=False),
        sa.Column("quantity", sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column("filled_quantity", sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column("price", sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column(
            "status",
            sa.String(length=16),
            nullable=False,
            server_default=sa.text("'filled'"),
        ),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.UniqueConstraint("simulation_id"),
    )
    op.create_index(
        "ix_simulated_executions_account_submitted",
        "simulated_executions",
        ["account_id", "submitted_at"],
        unique=False,
    )
    op.create_index(
        "ix_simulated_executions_symbol_submitted",
        "simulated_executions",
        ["symbol", "submitted_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_simulated_executions_account_id"),
        "simulated_executions",
        ["account_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_simulated_executions_symbol"),
        "simulated_executions",
        ["symbol"],
        unique=False,
    )
    op.create_index(
        op.f("ix_simulated_executions_correlation_id"),
        "simulated_executions",
        ["correlation_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_simulated_executions_correlation_id"),
        table_name="simulated_executions",
    )
    op.drop_index(
        op.f("ix_simulated_executions_symbol"),
        table_name="simulated_executions",
    )
    op.drop_index(
        op.f("ix_simulated_executions_account_id"),
        table_name="simulated_executions",
    )
    op.drop_index(
        "ix_simulated_executions_symbol_submitted",
        table_name="simulated_executions",
    )
    op.drop_index(
        "ix_simulated_executions_account_submitted",
        table_name="simulated_executions",
    )
    op.drop_table("simulated_executions")
