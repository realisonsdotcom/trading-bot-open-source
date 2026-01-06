"""Auth0 authentication middleware for FastAPI services.

This middleware validates Auth0 JWT tokens and extracts the customer_id
to be used by the EntitlementsMiddleware.
"""

from __future__ import annotations

import os
from typing import Optional
import httpx

from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED


class Auth0Middleware(BaseHTTPMiddleware):
    """
    Middleware to validate Auth0 tokens and inject customer_id.

    This middleware should be installed BEFORE EntitlementsMiddleware.
    It validates the Auth0 JWT token and injects x-customer-id header
    for downstream middleware to use.

    Flow:
    1. Extract Authorization header (Bearer token)
    2. Validate token via auth_gateway_service
    3. Inject x-customer-id header with local_user_id
    4. Continue to next middleware (EntitlementsMiddleware)
    """

    def __init__(
        self,
        app,
        *,
        auth_gateway_url: str,
        skip_paths: Optional[set[str]] = None,
        require_auth: bool = True,
    ) -> None:
        super().__init__(app)
        self._auth_gateway_url = auth_gateway_url.rstrip("/")
        self._skip_paths = skip_paths or set()
        self._require_auth = require_auth
        self._bypass = os.getenv("AUTH0_BYPASS", "0") == "1"

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Skip auth for specific paths
        if path in self._skip_paths:
            return await call_next(request)

        # Bypass mode (development only)
        if self._bypass:
            # In bypass mode, use x-customer-id if provided, or default to test user
            customer_id = request.headers.get("x-customer-id", "1")
            request.state.customer_id = customer_id
            request.state.auth0_sub = "bypass|test"
            request.state.user_email = "test@example.com"
            request.state.authenticated = True
            # Inject header for downstream middleware
            request.scope["headers"].append((b"x-customer-id", customer_id.encode()))
            return await call_next(request)

        # Extract Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            if self._require_auth:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Missing Authorization header",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            # If auth not required, continue without user context
            request.state.authenticated = False
            return await call_next(request)

        # Validate Bearer token format
        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid Authorization header format. Expected: Bearer <token>",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header[7:]  # Remove "Bearer " prefix

        # Validate token via auth_gateway_service
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._auth_gateway_url}/auth/validate",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=5.0,
                )

                if response.status_code == 401:
                    raise HTTPException(
                        status_code=HTTP_401_UNAUTHORIZED,
                        detail="Invalid or expired token",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

                response.raise_for_status()
                user_data = response.json()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Token validation failed",
                    headers={"WWW-Authenticate": "Bearer"},
                ) from e
            raise HTTPException(
                status_code=500,
                detail=f"Auth gateway error: {str(e)}",
            ) from e
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Auth gateway unavailable: {str(e)}",
            ) from e

        # Extract user info
        customer_id = str(user_data.get("local_user_id"))
        auth0_sub = user_data.get("auth0_sub")
        email = user_data.get("email")
        roles = user_data.get("roles", [])
        plan_code = user_data.get("plan_code")

        # Store in request state
        request.state.customer_id = customer_id
        request.state.auth0_sub = auth0_sub
        request.state.user_email = email
        request.state.user_roles = roles
        request.state.user_plan = plan_code
        request.state.authenticated = True

        # Inject x-customer-id header for downstream middleware
        # This allows EntitlementsMiddleware to work without changes
        request.scope["headers"].append((b"x-customer-id", customer_id.encode()))

        # Continue to next middleware
        response = await call_next(request)
        return response


def install_auth0_middleware(
    app,
    *,
    skip_paths: Optional[list[str]] = None,
    require_auth: bool = True,
) -> None:
    """
    Install Auth0 authentication middleware.

    Args:
        app: FastAPI application
        skip_paths: List of paths to skip authentication (e.g., /health, /docs)
        require_auth: If True, require authentication for all non-skipped paths

    Environment Variables:
        AUTH_GATEWAY_URL: URL of auth_gateway_service (default: http://auth_gateway_service:8000)
        AUTH0_BYPASS: Set to "1" to bypass Auth0 validation (development only)

    Example:
        from libs.entitlements.auth0_middleware import install_auth0_middleware

        app = FastAPI()

        # Install Auth0 middleware BEFORE entitlements middleware
        install_auth0_middleware(
            app,
            skip_paths=["/health", "/metrics", "/docs", "/openapi.json"],
        )

        # Then install entitlements middleware
        install_entitlements_middleware(app, ...)
    """
    default_skip_paths = {"/health", "/metrics", "/docs", "/openapi.json", "/redoc"}
    if skip_paths:
        default_skip_paths.update(skip_paths)

    auth_gateway_url = os.getenv(
        "AUTH_GATEWAY_URL",
        os.getenv("AUTH_GATEWAY_SERVICE_URL", "http://auth_gateway_service:8000"),
    )

    app.add_middleware(
        Auth0Middleware,
        auth_gateway_url=auth_gateway_url,
        skip_paths=default_skip_paths,
        require_auth=require_auth,
    )


__all__ = ["Auth0Middleware", "install_auth0_middleware"]
