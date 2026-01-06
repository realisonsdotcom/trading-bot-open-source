"""Configuration for Auth Gateway Service."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env.dev",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Service
    service_name: str = "auth_gateway_service"
    debug: bool = False

    # Database
    database_url: str = "postgresql://postgres:postgres@postgres:5432/trading_bot"

    # Auth0 Configuration
    auth0_domain: str
    auth0_client_id: str
    auth0_client_secret: str
    auth0_audience: str
    auth0_callback_url: str = "http://localhost:3000/auth/callback"
    auth0_logout_url: str = "http://localhost:3000"

    # Auth0 Management API (for user creation/sync)
    auth0_management_client_id: str
    auth0_management_client_secret: str
    auth0_management_audience: str | None = None

    # Default Plan
    default_plan_code: str = "free_trial"
    default_plan_trial_days: int = 14

    # CORS
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5173"
    ]

    # Session
    session_secret: str = "change-me-in-production"
    session_cookie_name: str = "session"
    session_cookie_secure: bool = False
    session_cookie_httponly: bool = True
    session_cookie_samesite: str = "lax"
    session_max_age: int = 86400  # 24 hours

    # User Service
    user_service_url: str = "http://user_service:8000"

    # Entitlements Service
    entitlements_service_url: str = "http://entitlements_service:8000"

    # Billing Service
    billing_service_url: str = "http://billing_service:8000"

    @property
    def auth0_issuer(self) -> str:
        """Get Auth0 issuer URL."""
        return f"https://{self.auth0_domain}/"

    @property
    def auth0_jwks_url(self) -> str:
        """Get Auth0 JWKS URL for token validation."""
        return f"https://{self.auth0_domain}/.well-known/jwks.json"

    @property
    def auth0_management_api_url(self) -> str:
        """Get Auth0 Management API URL."""
        return f"https://{self.auth0_domain}/api/v2"


settings = Settings()
