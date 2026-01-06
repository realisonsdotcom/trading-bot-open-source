"""Pydantic schemas for Auth Gateway Service."""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class Auth0TokenPayload(BaseModel):
    """Auth0 JWT token payload."""

    sub: str  # Auth0 user ID (e.g., "auth0|123456")
    iss: str  # Issuer
    aud: str | list[str]  # Audience
    iat: int  # Issued at
    exp: int  # Expiration
    azp: str | None = None  # Authorized party
    scope: str | None = None  # Scopes

    # Custom claims (namespace: https://api.trading-bot.dev)
    customer_id: int | None = Field(None, alias="https://api.trading-bot.dev/customer_id")
    plan_code: str | None = Field(None, alias="https://api.trading-bot.dev/plan_code")
    roles: list[str] | None = Field(None, alias="https://api.trading-bot.dev/roles")

    class Config:
        populate_by_name = True


class Auth0UserInfo(BaseModel):
    """Auth0 user information."""

    sub: str
    email: EmailStr
    email_verified: bool = False
    name: str | None = None
    nickname: str | None = None
    picture: str | None = None
    updated_at: str | None = None
    created_at: str | None = None


class UserSessionResponse(BaseModel):
    """User session response."""

    session_id: str
    user_id: int
    email: str
    name: str | None = None
    picture: str | None = None
    plan_code: str | None = None
    roles: list[str] = []
    expires_at: datetime

    # Entitlements
    capabilities: dict[str, bool] = {}
    quotas: dict[str, int] = {}


class LoginCallbackRequest(BaseModel):
    """Login callback request from Auth0."""

    code: str
    state: str | None = None


class LogoutRequest(BaseModel):
    """Logout request."""

    session_id: str | None = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "ok"
    service: str = "auth_gateway_service"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Error response."""

    error: str
    detail: str | None = None
    code: str | None = None
