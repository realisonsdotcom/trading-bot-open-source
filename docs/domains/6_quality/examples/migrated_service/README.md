---
domain: 6_quality
title: Migrated Service Example
description: Example service showing an Auth0 migration with entitlements integration.
keywords: example, auth0, entitlements, migration, service
last_updated: 2026-01-07
status: published
---

# Example Migrated Service

Cet exemple montre comment migrer un service du système JWT custom vers Auth0.

## Structure

```
docs/domains/6_quality/examples/migrated_service/
├── app/
│   └── main.py        # Service example avec Auth0 + Entitlements
└── README.md          # Ce fichier
```

## Points clés démontrés

### 1. Installation des middlewares

```python
from libs.entitlements.auth0_integration import install_auth0_with_entitlements

install_auth0_with_entitlements(
    app,
    required_capabilities=["can.use_strategies"],
    required_quotas={"quota.active_algos": 1},
    skip_paths=["/public"],
)
```

### 2. Endpoints publics (no auth)

```python
@app.get("/health")
async def health():
    return {"status": "ok"}
```

### 3. Endpoints protégés (auth required)

```python
@app.get("/api/profile")
async def get_profile(request: Request):
    # User info automatically available
    customer_id = request.state.customer_id
    email = request.state.user_email
    return {"customer_id": customer_id, "email": email}
```

### 4. Vérification manuelle de rôles

```python
@app.get("/api/admin/users")
async def list_users(request: Request):
    roles = request.state.user_roles
    if "admin" not in roles:
        raise HTTPException(403, "Admin role required")
    # ...
```

### 5. Vérification de quotas

```python
@app.post("/api/strategies")
async def create_strategy(request: Request):
    entitlements = request.state.entitlements
    max_algos = entitlements.quotas.get("quota.active_algos", 0)
    current_count = get_current_count()  # From DB

    if current_count >= max_algos:
        raise HTTPException(403, "Quota exceeded")
    # ...
```

## Lancer l'exemple

### Prérequis

- Auth0 configuré (voir `docs/domains/4_security/AUTH0_SETUP.md`)
- auth_gateway_service running
- entitlements_service running

### Développement (avec bypass)

```bash
# Activer bypass mode
export AUTH0_BYPASS=1
export ENTITLEMENTS_BYPASS=1
export AUTH_GATEWAY_URL=http://localhost:8012

# Lancer le service
cd docs/domains/6_quality/examples/migrated_service
python -m app.main
```

Service accessible sur http://localhost:8000

### Test avec bypass

```bash
# Health check (public)
curl http://localhost:8000/health

# Endpoint public
curl http://localhost:8000/public

# Profile (avec bypass)
curl -H "x-customer-id: 1" http://localhost:8000/api/profile

# Strategies
curl -H "x-customer-id: 1" http://localhost:8000/api/strategies
```

### Test avec Auth0 (production)

```bash
# Désactiver bypass
export AUTH0_BYPASS=0
export ENTITLEMENTS_BYPASS=0

# Get Auth0 token (via frontend ou auth flow)
TOKEN="your_auth0_access_token_here"

# Call protected endpoint
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/profile
```

## Endpoints disponibles

| Endpoint | Auth | Capabilities | Quotas | Description |
|----------|------|-------------|--------|-------------|
| `GET /health` | ❌ | - | - | Health check |
| `GET /public` | ❌ | - | - | Public endpoint |
| `GET /api/profile` | ✅ | can.use_strategies | - | User profile |
| `GET /api/strategies` | ✅ | can.use_strategies | - | List strategies |
| `POST /api/strategies` | ✅ | can.use_strategies | quota.active_algos | Create strategy |
| `GET /api/quotas` | ✅ | can.use_strategies | - | Quota usage |
| `GET /api/admin/users` | ✅ | - | - | Admin only |
| `GET /api/check-auth` | ✅ | can.use_strategies | - | Auth status |

## Documentation interactive

Une fois le service lancé:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Comparaison Avant/Après

### Avant (Custom JWT)

```python
from fastapi import Depends, HTTPException
from jose import jwt

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET)
        return payload.get("user_id")
    except:
        raise HTTPException(401)

@app.get("/api/data")
async def get_data(user_id: int = Depends(get_current_user)):
    return {"user_id": user_id}
```

### Après (Auth0)

```python
from fastapi import Request

install_auth0_with_entitlements(app, ...)

@app.get("/api/data")
async def get_data(request: Request):
    customer_id = request.state.customer_id
    return {"customer_id": customer_id}
```

## Request State

Informations disponibles dans `request.state`:

```python
request.state.customer_id       # Local user ID (string)
request.state.auth0_sub         # Auth0 user ID (e.g., "auth0|123")
request.state.user_email        # Email address
request.state.user_roles        # List of roles
request.state.user_plan         # Plan code (e.g., "pro")
request.state.authenticated     # Boolean
request.state.entitlements      # Entitlements object
    .features                   # Dict[str, bool] - capabilities
    .quotas                     # Dict[str, int] - quota limits
```

## Tests

Créer des tests avec bypass mode:

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_public_endpoint():
    response = client.get("/public")
    assert response.status_code == 200

def test_protected_endpoint_with_bypass(monkeypatch):
    monkeypatch.setenv("AUTH0_BYPASS", "1")
    monkeypatch.setenv("ENTITLEMENTS_BYPASS", "1")

    response = client.get(
        "/api/profile",
        headers={"x-customer-id": "1"}
    )
    assert response.status_code == 200
    assert "customer_id" in response.json()
```

## Migration depuis un service existant

1. **Copier ce fichier** comme point de départ
2. **Adapter les capabilities**: Remplacer `can.use_strategies` par les vôtres
3. **Adapter les quotas**: Ajouter/retirer selon votre service
4. **Migrer les endpoints**: Remplacer `Depends(get_current_user)` par `Request`
5. **Tester**: Avec bypass mode puis avec Auth0 tokens
6. **Déployer**: Désactiver bypass en production

## Troubleshooting

### Service démarre mais endpoints 401

Vérifier:
```bash
# auth_gateway_service est up?
curl http://localhost:8012/health

# Bypass activé?
echo $AUTH0_BYPASS

# Token valide?
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8012/auth/validate
```

### "Missing x-customer-id header"

Cause: Auth0Middleware pas installé ou pas en premier

Solution: Vérifier l'ordre des middlewares:
```python
# Auth0 DOIT être installé AVANT entitlements
install_auth0_middleware(app, ...)       # 1st
install_entitlements_middleware(app, ...)  # 2nd
```

### Quotas pas appliqués

Vérifier:
```bash
# ENTITLEMENTS_BYPASS activé?
echo $ENTITLEMENTS_BYPASS

# Plan a des quotas?
curl http://entitlements_service:8000/entitlements/1
```

## Voir aussi

- Guide de migration: `libs/entitlements/MIGRATION_GUIDE.md`
- Auth0 Middleware docs: `libs/entitlements/README_AUTH0.md`
- Auth Gateway docs: `services/auth_gateway_service/README.md`
