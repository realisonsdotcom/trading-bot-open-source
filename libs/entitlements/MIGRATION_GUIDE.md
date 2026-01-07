# Migration Guide: Custom JWT → Auth0

Guide pas-à-pas pour migrer vos services du système JWT custom vers Auth0.

## Vue d'ensemble

| Aspect | Avant (Custom JWT) | Après (Auth0) |
|--------|-------------------|---------------|
| **Authentification** | JWT HS256 custom | Auth0 RS256 + OIDC |
| **Validation** | Locale (JWT_SECRET) | Via auth_gateway_service |
| **User ID** | `payload["user_id"]` | `request.state.customer_id` |
| **Headers** | `x-customer-id` manual | `Authorization: Bearer <token>` |
| **Middleware** | Custom JWT validation | Auth0Middleware + EntitlementsMiddleware |

---

## Étape 1: Mettre à jour les dépendances

### Dans votre `requirements.txt`:

**Ajouter**:
```
httpx>=0.28.0  # Pour les appels HTTP async
```

**Optionnel (si vous supprimez le code JWT custom)**:
```
# Vous pouvez retirer python-jose si vous ne l'utilisez plus
# python-jose[cryptography]
```

### Installer:
```bash
pip install httpx
```

---

## Étape 2: Remplacer le middleware

### Option A: Utiliser le helper combiné (recommandé)

**Avant** (`services/your_service/app/main.py`):
```python
from fastapi import FastAPI, Depends
from jose import jwt, JWTError

app = FastAPI()

# Custom JWT validation
def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload.get("user_id")
    except JWTError:
        raise HTTPException(401, "Invalid token")

@app.get("/data")
async def get_data(user_id: int = Depends(get_current_user)):
    return {"user_id": user_id}
```

**Après**:
```python
from fastapi import FastAPI, Request
from libs.entitlements.auth0_integration import install_auth0_with_entitlements

app = FastAPI()

# Install Auth0 + Entitlements middleware
install_auth0_with_entitlements(
    app,
    required_capabilities=["can.use_your_service"],
    skip_paths=["/health", "/docs"],
)

@app.get("/data")
async def get_data(request: Request):
    # User info automatically available in request.state
    customer_id = request.state.customer_id
    email = request.state.user_email
    return {"customer_id": customer_id, "email": email}
```

### Option B: Installation manuelle

Si vous avez besoin de plus de contrôle:

```python
from libs.entitlements.auth0_middleware import install_auth0_middleware
from libs.entitlements.fastapi import install_entitlements_middleware

# IMPORTANT: Auth0 middleware MUST be installed FIRST
install_auth0_middleware(
    app,
    skip_paths=["/health", "/docs"],
    require_auth=True,
)

install_entitlements_middleware(
    app,
    required_capabilities=["can.use_strategies"],
    required_quotas={"quota.active_algos": 1},
    skip_paths=["/health", "/docs"],
)
```

---

## Étape 3: Mettre à jour les endpoints

### Accéder aux informations utilisateur

**Avant**:
```python
from fastapi import Depends

@app.get("/profile")
async def get_profile(user_id: int = Depends(get_current_user)):
    user = get_user_from_db(user_id)
    return user
```

**Après**:
```python
from fastapi import Request

@app.get("/profile")
async def get_profile(request: Request):
    # User info from Auth0Middleware
    customer_id = request.state.customer_id
    email = request.state.user_email
    auth0_sub = request.state.auth0_sub

    # Entitlements from EntitlementsMiddleware
    entitlements = request.state.entitlements

    user = get_user_from_db(customer_id)
    return {
        "user": user,
        "email": email,
        "capabilities": entitlements.features,
        "quotas": entitlements.quotas,
    }
```

### Vérifier l'authentification

**Avant**:
```python
@app.get("/protected")
async def protected(user_id: int = Depends(get_current_user)):
    # user_id will be None if not authenticated
    if not user_id:
        raise HTTPException(401)
    return {"message": "OK"}
```

**Après**:
```python
@app.get("/protected")
async def protected(request: Request):
    # Auth0Middleware already enforced authentication
    # If we reach here, user is authenticated
    return {"message": "OK", "user": request.state.user_email}
```

### Vérifier les permissions (capabilities)

**Avant** (manuelle):
```python
@app.post("/strategies")
async def create_strategy(user_id: int = Depends(get_current_user)):
    # Manually check permissions
    user_plan = get_user_plan(user_id)
    if not user_plan.can_create_strategies:
        raise HTTPException(403, "Plan does not allow strategy creation")
    # Create strategy...
```

**Après** (automatique):
```python
# Add required_capabilities at middleware level
install_auth0_with_entitlements(
    app,
    required_capabilities=["can.use_strategies"],
)

@app.post("/strategies")
async def create_strategy(request: Request):
    # EntitlementsMiddleware already verified capability
    # If we reach here, user has permission
    customer_id = request.state.customer_id
    # Create strategy...
```

### Vérifier les quotas

**Avant** (manuelle):
```python
@app.post("/algorithms")
async def create_algo(user_id: int = Depends(get_current_user)):
    active_count = count_active_algos(user_id)
    max_algos = get_user_plan(user_id).max_algos
    if active_count >= max_algos:
        raise HTTPException(403, f"Quota exceeded: {active_count}/{max_algos}")
    # Create algo...
```

**Après** (automatique):
```python
install_auth0_with_entitlements(
    app,
    required_quotas={"quota.active_algos": 1},
)

@app.post("/algorithms")
async def create_algo(request: Request):
    # EntitlementsMiddleware already verified quota
    customer_id = request.state.customer_id
    entitlements = request.state.entitlements
    max_algos = entitlements.quotas.get("quota.active_algos", 0)
    # Create algo...
```

---

## Étape 4: Mettre à jour les variables d'environnement

### Ajouter dans `config/.env.dev`:

```bash
# Auth Gateway Service (new)
AUTH_GATEWAY_URL=http://auth_gateway_service:8000

# Bypass Auth0 (development only)
AUTH0_BYPASS=1

# Existing entitlements config
ENTITLEMENTS_SERVICE_URL=http://entitlements_service:8000
ENTITLEMENTS_BYPASS=1
```

### Retirer (optionnel):

```bash
# Custom JWT config (no longer needed)
# JWT_SECRET=...
# JWT_ALGO=HS256
```

---

## Étape 5: Mettre à jour infra/docker-compose.yml

### Ajouter dépendance à auth_gateway_service:

**Dans `infra/docker-compose.yml`**:
```yaml
your_service:
  # ... existing config ...
  environment:
    AUTH_GATEWAY_URL: http://auth_gateway_service:8000
  depends_on:
    auth_gateway_service:
      condition: service_healthy
```

---

## Étape 6: Tester la migration

### Test 1: Health check (sans auth)

```bash
curl http://localhost:8000/health
# Should return 200 OK without authentication
```

### Test 2: Endpoint protégé (avec Auth0 token)

```bash
# 1. Get Auth0 token (via frontend or auth flow)
TOKEN="your_auth0_token_here"

# 2. Call protected endpoint
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/data

# Should return 200 with user data
```

### Test 3: Bypass mode (dev only)

```bash
# With AUTH0_BYPASS=1
curl -H "x-customer-id: 1" \
     http://localhost:8000/api/data

# Should work without Authorization header
```

---

## Étape 7: Mode de compatibilité (optionnel)

Si vous voulez supporter les deux systèmes temporairement:

```python
from fastapi import Request, Header, HTTPException
from typing import Optional

async def get_user_id(
    request: Request,
    authorization: Optional[str] = Header(None),
    x_customer_id: Optional[str] = Header(None),
):
    """Support both Auth0 and legacy auth."""

    # Try Auth0 first (if middleware installed)
    if hasattr(request.state, "customer_id"):
        return request.state.customer_id

    # Fallback to x-customer-id header (legacy)
    if x_customer_id:
        return x_customer_id

    # Fallback to custom JWT (legacy)
    if authorization:
        # ... custom JWT validation ...
        pass

    raise HTTPException(401, "Not authenticated")

@app.get("/data")
async def get_data(user_id: str = Depends(get_user_id)):
    return {"user_id": user_id}
```

---

## Checklist de migration

### Par service:

- [ ] Installer httpx dependency
- [ ] Remplacer custom JWT validation par Auth0Middleware
- [ ] Installer EntitlementsMiddleware si nécessaire
- [ ] Mettre à jour endpoints pour utiliser `request.state`
- [ ] Remplacer `Depends(get_current_user)` par `Request` param
- [ ] Ajouter `AUTH_GATEWAY_URL` dans `infra/docker-compose.yml`
- [ ] Tester health check (skip_paths)
- [ ] Tester avec Auth0 token
- [ ] Tester avec AUTH0_BYPASS=1
- [ ] Vérifier entitlements enforcement
- [ ] Retirer code JWT custom (optionnel)

### Global:

- [ ] Tous les services migrés
- [ ] Frontend utilise Auth0 SDK
- [ ] Tests end-to-end passent
- [ ] Documentation mise à jour
- [ ] Variables d'environnement vérifiées
- [ ] Retirer `auth_service` (ancien)

---

## Services à migrer

Liste des services du projet utilisant l'authentification:

| Service | Port | Status | Notes |
|---------|------|--------|-------|
| `algo_engine` | 8001 | 🔴 À migrer | Nécessite `can.use_strategies` |
| `user_service` | 8002 | 🔴 À migrer | Profile management |
| `reports` | 8003 | 🔴 À migrer | Nécessite `can.view_reports` |
| `notification_service` | 8004 | 🔴 À migrer | Internal notifications |
| `streaming_gateway` | 9000 | 🔴 À migrer | WebSocket auth |
| `marketplace` | 8005 | 🔴 À migrer | Nécessite `can.browse_marketplace` |
| `web_dashboard` | 8022 | 🔴 À migrer | Frontend React |

---

## Problèmes courants

### Erreur: "Missing Authorization header"

**Cause**: Frontend n'envoie pas le token Auth0

**Solution**:
```javascript
// Frontend
const { getAccessTokenSilently } = useAuth0();
const token = await getAccessTokenSilently();

fetch('/api/data', {
  headers: {
    'Authorization': `Bearer ${token}`,
  },
});
```

### Erreur: "Auth gateway unavailable"

**Cause**: auth_gateway_service n'est pas démarré

**Solution**:
```bash
docker compose --project-directory . -f infra/docker-compose.yml up -d auth_gateway_service
docker compose --project-directory . -f infra/docker-compose.yml logs auth_gateway_service
```

### Erreur: "Missing x-customer-id header"

**Cause**: Auth0Middleware pas installé avant EntitlementsMiddleware

**Solution**: Vérifier l'ordre des middlewares (Auth0 MUST be first)

### Tests échouent après migration

**Cause**: Tests utilisent l'ancien système JWT

**Solution**:
- Activer `AUTH0_BYPASS=1` pour les tests
- Ou mocker le token Auth0
- Ou utiliser `x-customer-id` header en bypass mode

---

## Exemple complet

Voir `docs/domains/6_quality/examples/migrated_service/` pour un exemple complet de service migré.

---

## Support

- Auth0 Middleware: `libs/entitlements/README_AUTH0.md`
- Auth Gateway Service: `services/auth_gateway_service/README.md`
- Questions: Créer une issue sur GitHub
