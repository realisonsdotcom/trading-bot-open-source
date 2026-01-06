"""Database models for Auth Gateway Service."""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Auth0User(Base):
    """Mapping between Auth0 users and local users."""

    __tablename__ = "auth0_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    auth0_sub = Column(String(255), unique=True, nullable=False, index=True)
    local_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    email_verified = Column(Boolean, default=False)
    picture = Column(String(500), nullable=True)
    name = Column(String(255), nullable=True)
    nickname = Column(String(255), nullable=True)

    # Auth0 metadata
    auth0_created_at = Column(DateTime(timezone=True), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    login_count = Column(Integer, default=0)

    # Tracking
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("ix_auth0_users_auth0_sub", "auth0_sub"),
        Index("ix_auth0_users_local_user_id", "local_user_id"),
        Index("ix_auth0_users_email", "email"),
    )


class UserSession(Base):
    """User session tracking."""

    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    local_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    auth0_sub = Column(String(255), nullable=False, index=True)

    # Token info
    access_token_jti = Column(String(255), nullable=True)  # JWT ID from Auth0
    expires_at = Column(DateTime(timezone=True), nullable=False)

    # Session metadata
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)

    # Tracking
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_activity = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    revoked_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_user_sessions_session_id", "session_id"),
        Index("ix_user_sessions_local_user_id", "local_user_id"),
        Index("ix_user_sessions_expires_at", "expires_at"),
    )


# Note: The User table is defined in user_service, we don't redefine it here.
# We reference it via ForeignKey for the mapping.
