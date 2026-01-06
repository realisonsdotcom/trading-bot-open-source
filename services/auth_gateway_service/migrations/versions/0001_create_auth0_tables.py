"""Create Auth0 user mapping and session tables

Revision ID: 0001_create_auth0_tables
Revises:
Create Date: 2025-11-12 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_create_auth0_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create auth0_users table
    op.create_table(
        'auth0_users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('auth0_sub', sa.String(length=255), nullable=False),
        sa.Column('local_user_id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('email_verified', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('picture', sa.String(length=500), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('nickname', sa.String(length=255), nullable=True),
        sa.Column('auth0_created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('login_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('auth0_sub'),
        sa.ForeignKeyConstraint(['local_user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_auth0_users_auth0_sub', 'auth0_users', ['auth0_sub'])
    op.create_index('ix_auth0_users_local_user_id', 'auth0_users', ['local_user_id'])
    op.create_index('ix_auth0_users_email', 'auth0_users', ['email'])

    # Create user_sessions table
    op.create_table(
        'user_sessions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('session_id', sa.String(length=255), nullable=False),
        sa.Column('local_user_id', sa.Integer(), nullable=False),
        sa.Column('auth0_sub', sa.String(length=255), nullable=False),
        sa.Column('access_token_jti', sa.String(length=255), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('last_activity', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_id'),
        sa.ForeignKeyConstraint(['local_user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_user_sessions_session_id', 'user_sessions', ['session_id'])
    op.create_index('ix_user_sessions_local_user_id', 'user_sessions', ['local_user_id'])
    op.create_index('ix_user_sessions_expires_at', 'user_sessions', ['expires_at'])


def downgrade() -> None:
    op.drop_index('ix_user_sessions_expires_at', table_name='user_sessions')
    op.drop_index('ix_user_sessions_local_user_id', table_name='user_sessions')
    op.drop_index('ix_user_sessions_session_id', table_name='user_sessions')
    op.drop_table('user_sessions')

    op.drop_index('ix_auth0_users_email', table_name='auth0_users')
    op.drop_index('ix_auth0_users_local_user_id', table_name='auth0_users')
    op.drop_index('ix_auth0_users_auth0_sub', table_name='auth0_users')
    op.drop_table('auth0_users')
