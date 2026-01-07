# Auth0 Integration for Entitlements Middleware

## Overview

This document explains how to use Auth0 authentication with the existing entitlements system.

## Architecture

```
Request with Auth0 token
    ↓
Auth0Middleware (new)
    ├─ Validate token via auth_gateway_service
    ├─ Extract customer_id from token
    └─ Inject x-customer-id header
    ↓
EntitlementsMiddleware (existing)
    ├─ Read x-customer-id header
    ├─ Fetch entitlements from service
    └─ Enforce capabilities/quotas
    ↓
Your endpoint handler
```

## Installation

### Method 1: Combined installation (recommended)

Use the new helper that installs both middlewares in the correct order:

```python
from fastapi import FastAPI
from libs.entitlements.auth0_integration import install_auth0_with_entitlements

app = FastAPI()

install_auth0_with_entitlements(
    app,
    required_capabilities=["can.use_strategies"],
    required_quotas={"quota.active_algos": 1},
    skip_paths=["/public"],  # Additional paths to skip
)
```

### Method 2: Manual installation

Install middlewares separately (Auth0 MUST be first):

```python
from fastapi import FastAPI
from libs.entitlements.auth0_middleware import install_auth0_middleware
from libs.entitlements.fastapi import install_entitlements_middleware

app = FastAPI()

# 1. Install Auth0 middleware FIRST
install_auth0_middleware(
    app,
    skip_paths=["/health", "/docs"],
)

# 2. Then install entitlements middleware
install_entitlements_middleware(
    app,
    required_capabilities=["can.use_strategies"],
    required_quotas={"quota.active_algos": 1},
    skip_paths=["/health", "/docs"],
)
```

## Environment Variables

```bash
# Auth Gateway Service
AUTH_GATEWAY_URL=http://auth_gateway_service:8000

# Bypass Auth0 (development only)
AUTH0_BYPASS=1  # Set to "1" to skip Auth0 validation

# Entitlements Service (existing)
ENTITLEMENTS_SERVICE_URL=http://entitlements_service:8000
ENTITLEMENTS_BYPASS=1  # Set to "1" to skip entitlements checks
```

## Usage in Endpoints

### Access user information

```python
from fastapi import Request

@app.get("/api/profile")
async def get_profile(request: Request):
    # User info from Auth0Middleware
    customer_id = request.state.customer_id
    email = request.state.user_email
    auth0_sub = request.state.auth0_sub
    roles = request.state.user_roles
    plan = request.state.user_plan

    # Entitlements from EntitlementsMiddleware
    entitlements = request.state.entitlements
    can_use_strategies = entitlements.features.get("can.use_strategies", False)
    max_algos = entitlements.quotas.get("quota.active_algos", 0)

    return {
        "customer_id": customer_id,
        "email": email,
        "plan": plan,
        "can_use_strategies": can_use_strategies,
        "max_algos": max_algos,
    }
```

### Check authentication

```python
@app.get("/api/protected")
async def protected_route(request: Request):
    if not request.state.authenticated:
        raise HTTPException(401, "Not authenticated")

    # User is authenticated
    return {"message": f"Hello {request.state.user_email}"}
```

## Frontend Integration

### Sending Auth0 token

```javascript
// Get Auth0 token
const { getAccessTokenSilently } = useAuth0();
const token = await getAccessTokenSilently();

// Make API request
const response = await fetch('http://api.example.com/api/profile', {
  headers: {
    'Authorization': `Bearer ${token}`,
  },
});
```

### Example with React + Auth0

```jsx
import { useAuth0 } from '@auth0/auth0-react';
import { useEffect, useState } from 'react';

function Profile() {
  const { getAccessTokenSilently } = useAuth0();
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = await getAccessTokenSilently();
        const response = await fetch('/api/profile', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        const data = await response.json();
        setProfile(data);
      } catch (error) {
        console.error('Failed to fetch profile:', error);
      }
    };

    fetchProfile();
  }, [getAccessTokenSilently]);

  if (!profile) return <div>Loading...</div>;

  return (
    <div>
      <h1>Profile</h1>
      <p>Email: {profile.email}</p>
      <p>Plan: {profile.plan}</p>
      <p>Max Algorithms: {profile.max_algos}</p>
    </div>
  );
}
```

## Migration Guide

### Existing services using custom JWT

If your service currently validates custom JWT tokens:

**Before (custom JWT):**
```python
from fastapi import Depends, HTTPException
from jose import jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("user_id")
        return user_id
    except JWTError:
        raise HTTPException(401, "Invalid token")

@app.get("/api/data")
async def get_data(user_id: int = Depends(get_current_user)):
    # Use user_id
    pass
```

**After (Auth0):**
```python
from fastapi import Request

# No need for get_current_user dependency
# Auth0Middleware handles it

@app.get("/api/data")
async def get_data(request: Request):
    # User info already in request.state
    user_id = request.state.customer_id
    email = request.state.user_email
    # Use user_id
    pass
```

### Testing

During development, you can bypass Auth0 validation:

```bash
# In config/.env.dev
AUTH0_BYPASS=1
ENTITLEMENTS_BYPASS=1
```

This allows testing without Auth0 configured.

## Troubleshooting

### Error: "Missing Authorization header"

**Cause**: Frontend not sending Auth0 token

**Solution**: Ensure frontend includes Authorization header:
```javascript
headers: {
  'Authorization': `Bearer ${token}`,
}
```

### Error: "Token validation failed"

**Cause**: Invalid or expired Auth0 token

**Solution**:
- Frontend: Use `getAccessTokenSilently()` to get fresh tokens
- Backend: Check `AUTH_GATEWAY_URL` is correct

### Error: "Auth gateway unavailable"

**Cause**: auth_gateway_service not running or unreachable

**Solution**:
```bash
# Check service status
docker compose --project-directory . -f infra/docker-compose.yml ps auth_gateway_service

# Check logs
docker compose --project-directory . -f infra/docker-compose.yml logs auth_gateway_service

# Verify URL
curl http://auth_gateway_service:8000/health
```

### Middleware order is important

Auth0Middleware MUST be installed BEFORE EntitlementsMiddleware:

```python
# ✅ Correct order
install_auth0_middleware(app, ...)
install_entitlements_middleware(app, ...)

# ❌ Wrong order (will not work)
install_entitlements_middleware(app, ...)
install_auth0_middleware(app, ...)
```

## Performance Considerations

- **Token validation**: Cached by auth_gateway_service (JWKS cache: 1h TTL)
- **Entitlements**: Cached by entitlements_service (5 min TTL)
- **Network calls**: 2 per request (auth validation + entitlements fetch)

For high-traffic services, consider:
- Using Redis for distributed caching
- Implementing request-level caching
- Connection pooling for httpx client

## Security Notes

- ✅ Tokens validated against Auth0 public keys (RS256)
- ✅ Customer_id extracted from validated tokens (cannot be spoofed)
- ✅ Entitlements enforced server-side
- ⚠️ Never use `AUTH0_BYPASS=1` in production
- ⚠️ Always use HTTPS in production for token transmission

## Examples

See example services:
- `services/algo_engine/` - Algorithm execution with quotas
- `services/user_service/` - User profile management
- `services/reports/` - Report generation with capabilities

## Support

- Auth0 Middleware docs: This file
- Entitlements docs: `libs/entitlements/README.md`
- Auth Gateway docs: `services/auth_gateway_service/README.md`
- Auth0 Setup: `docs/domains/4_security/AUTH0_SETUP.md`
