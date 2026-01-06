"""Helper to install Auth0 + Entitlements middlewares together.

This module provides a convenient way to install both Auth0 authentication
and entitlements enforcement in the correct order.
"""

from __future__ import annotations

from typing import Dict, Iterable, Optional

from .auth0_middleware import install_auth0_middleware
from .fastapi import install_entitlements_middleware


def install_auth0_with_entitlements(
    app,
    *,
    required_capabilities: Optional[Iterable[str]] = None,
    required_quotas: Optional[Dict[str, int]] = None,
    skip_paths: Optional[Iterable[str]] = None,
    require_auth: bool = True,
) -> None:
    """
    Install Auth0 authentication + entitlements enforcement middlewares.

    This is a convenience function that installs both middlewares in the correct order:
    1. Auth0Middleware (validates token, extracts customer_id)
    2. EntitlementsMiddleware (enforces capabilities/quotas)

    Args:
        app: FastAPI application
        required_capabilities: List of required capability codes (e.g., ["can.use_strategies"])
        required_quotas: Dict of required quotas with minimum values (e.g., {"quota.active_algos": 1})
        skip_paths: Additional paths to skip authentication and entitlements
        require_auth: If True, require authentication for all non-skipped paths

    Environment Variables:
        AUTH_GATEWAY_URL: URL of auth_gateway_service (default: http://auth_gateway_service:8000)
        AUTH0_BYPASS: Set to "1" to bypass Auth0 validation (development only)
        ENTITLEMENTS_SERVICE_URL: URL of entitlements service
        ENTITLEMENTS_BYPASS: Set to "1" to bypass entitlements checks (development only)

    Example:
        from fastapi import FastAPI
        from libs.entitlements.auth0_integration import install_auth0_with_entitlements

        app = FastAPI()

        install_auth0_with_entitlements(
            app,
            required_capabilities=["can.use_strategies", "can.use_alerts"],
            required_quotas={"quota.active_algos": 1},
            skip_paths=["/public", "/webhooks"],
        )

        @app.get("/api/data")
        async def get_data(request: Request):
            # User is authenticated and has required entitlements
            customer_id = request.state.customer_id
            entitlements = request.state.entitlements
            return {"customer_id": customer_id}
    """
    # 1. Install Auth0 middleware FIRST (validates token, injects customer_id)
    install_auth0_middleware(
        app,
        skip_paths=skip_paths,
        require_auth=require_auth,
    )

    # 2. Install entitlements middleware SECOND (enforces permissions)
    install_entitlements_middleware(
        app,
        required_capabilities=required_capabilities,
        required_quotas=required_quotas,
        skip_paths=skip_paths,
    )


__all__ = ["install_auth0_with_entitlements"]
