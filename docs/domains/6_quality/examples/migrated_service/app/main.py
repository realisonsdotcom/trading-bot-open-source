"""
Example service showing Auth0 + Entitlements integration.

This example demonstrates how to migrate from custom JWT to Auth0.
"""

from fastapi import FastAPI, Request, HTTPException
from libs.entitlements.auth0_integration import install_auth0_with_entitlements

# Create FastAPI app
app = FastAPI(
    title="Example Migrated Service",
    description="Demonstrates Auth0 + Entitlements integration",
    version="1.0.0",
)

# Install Auth0 + Entitlements middleware
install_auth0_with_entitlements(
    app,
    required_capabilities=["can.use_strategies"],  # All endpoints require this capability
    required_quotas={"quota.active_algos": 1},     # Must have at least 1 algo quota
    skip_paths=["/public"],                         # Public endpoints
)


# ===== Public endpoints (no auth required) =====

@app.get("/health", tags=["Public"])
async def health():
    """Health check - no authentication required."""
    return {"status": "ok"}


@app.get("/public", tags=["Public"])
async def public_endpoint():
    """Public endpoint - accessible without authentication."""
    return {"message": "This is public"}


# ===== Protected endpoints (auth required) =====

@app.get("/api/profile", tags=["User"])
async def get_profile(request: Request):
    """Get current user profile - requires authentication."""

    # User info from Auth0Middleware
    customer_id = request.state.customer_id
    email = request.state.user_email
    auth0_sub = request.state.auth0_sub
    roles = request.state.user_roles
    plan = request.state.user_plan

    # Entitlements from EntitlementsMiddleware
    entitlements = request.state.entitlements

    return {
        "customer_id": customer_id,
        "email": email,
        "auth0_sub": auth0_sub,
        "roles": roles,
        "plan": plan,
        "capabilities": entitlements.features,
        "quotas": entitlements.quotas,
    }


@app.get("/api/strategies", tags=["Strategies"])
async def list_strategies(request: Request):
    """
    List user strategies.

    Requires:
    - Authentication (Auth0 token)
    - Capability: can.use_strategies (enforced by middleware)
    """
    customer_id = request.state.customer_id

    # Fetch strategies from database (mock)
    strategies = [
        {"id": 1, "name": "Momentum Strategy", "user_id": customer_id},
        {"id": 2, "name": "Mean Reversion", "user_id": customer_id},
    ]

    return {
        "customer_id": customer_id,
        "strategies": strategies,
        "count": len(strategies),
    }


@app.post("/api/strategies", tags=["Strategies"])
async def create_strategy(request: Request, name: str):
    """
    Create a new strategy.

    Requires:
    - Authentication
    - Capability: can.use_strategies
    - Quota: quota.active_algos >= 1
    """
    customer_id = request.state.customer_id
    entitlements = request.state.entitlements

    # Check current usage vs quota
    max_algos = entitlements.quotas.get("quota.active_algos", 0)
    current_count = 2  # Mock - would query DB

    if current_count >= max_algos:
        raise HTTPException(
            status_code=403,
            detail=f"Quota exceeded: {current_count}/{max_algos} algorithms active"
        )

    # Create strategy (mock)
    new_strategy = {
        "id": 3,
        "name": name,
        "user_id": customer_id,
        "created_at": "2025-11-12T10:00:00Z",
    }

    return {
        "message": "Strategy created",
        "strategy": new_strategy,
        "quota_used": f"{current_count + 1}/{max_algos}",
    }


@app.get("/api/quotas", tags=["User"])
async def get_quotas(request: Request):
    """Get current quota usage for user."""
    entitlements = request.state.entitlements

    # Mock current usage
    usage = {
        "active_algos": {
            "current": 2,
            "max": entitlements.quotas.get("quota.active_algos", 0),
        },
        "api_calls_per_minute": {
            "current": 45,
            "max": entitlements.quotas.get("quota.api_calls_per_minute", 0),
        },
    }

    return {
        "quotas": usage,
        "capabilities": entitlements.features,
    }


@app.get("/api/admin/users", tags=["Admin"])
async def list_users(request: Request):
    """
    Admin endpoint - list all users.

    Requires admin role (checked manually).
    """
    roles = request.state.user_roles

    if "admin" not in roles:
        raise HTTPException(
            status_code=403,
            detail="Admin role required"
        )

    # List users (mock)
    users = [
        {"id": 1, "email": "user1@example.com"},
        {"id": 2, "email": "user2@example.com"},
    ]

    return {"users": users}


# ===== Optional: Check authentication status =====

@app.get("/api/check-auth", tags=["User"])
async def check_auth(request: Request):
    """Check if user is authenticated."""
    is_authenticated = getattr(request.state, "authenticated", False)

    if not is_authenticated:
        raise HTTPException(401, "Not authenticated")

    return {
        "authenticated": True,
        "email": request.state.user_email,
        "customer_id": request.state.customer_id,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
