"""Add strategy lineage columns for cloned strategies."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "c3a2b1d4e5f6"
down_revision = "a2cba7eee9aa"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # strategies.derived_from references strategies.id, nullable for root records
    op.add_column("strategies", sa.Column("derived_from", sa.String(length=36), nullable=True))
    op.create_foreign_key(
        "fk_strategies_derived_from",
        source_table="strategies",
        referent_table="strategies",
        local_cols=["derived_from"],
        remote_cols=["id"],
        ondelete="SET NULL",
    )
    op.create_index(
        "ix_strategies_derived_from",
        "strategies",
        ["derived_from"],
        unique=False,
    )

    # strategy_versions keeps lineage metadata for each snapshot
    op.add_column(
        "strategy_versions",
        sa.Column("derived_from", sa.String(length=36), nullable=True),
    )
    op.create_index(
        "ix_strategy_versions_derived_from",
        "strategy_versions",
        ["derived_from"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_strategy_versions_derived_from", table_name="strategy_versions")
    op.drop_column("strategy_versions", "derived_from")

    op.drop_constraint(
        "fk_strategies_derived_from",
        table_name="strategies",
        type_="foreignkey",
    )
    op.drop_index("ix_strategies_derived_from", table_name="strategies")
    op.drop_column("strategies", "derived_from")
