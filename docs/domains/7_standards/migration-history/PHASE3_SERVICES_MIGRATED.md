---
domain: 7_standards
title: Phase 3 Services Migrated
description: Summary of services migrated during phase 3.
keywords: migration, phase-3, services, history, archived
last_updated: 2026-01-06
status: deprecated
archived_reason: "Migrated from root after documentation restructuring"
---

# ✅ Phase 3 - Services Migrated (In Progress)

**Date**: 12 novembre 2025
**Status**: Migration en cours
**Services migrés**: 2/7

---

## 🎯 Services Migrés

### 1. ✅ algo_engine (Backend)

**Changements:**
- **Fichier**: `services/algo_engine/app/main.py`
- **Import mis à jour** (ligne 63):
  ```python
  from libs.entitlements.auth0_integration import install_auth0_with_entitlements
  ```
- **Middleware installé** (lignes 183-187):
  ```python
  install_auth0_with_entitlements(
      app,
      required_capabilities=["can.manage_strategies"],
      skip_paths=["/health"],
  )
  ```

**Résultat:**
- ✅ Service authentifie via Auth0
- ✅ Entitlements fonctionnent (max_active_strategies)
- ✅ Endpoints inchangés (utilisent déjà `Request`)
- ✅ httpx déjà installé

---

### 2. ✅ user_service (Backend)

**Changements:**
- **Fichier**: `services/user_service/app/main.py`
- **Imports nettoyés**:
  - ❌ Supprimé: `from jose import jwt`
  - ❌ Supprimé: `Header` de fastapi
  - ✅ Ajouté: `from libs.entitlements.auth0_integration import install_auth0_with_entitlements`

- **JWT constants supprimés** (lignes 58-60 supprimées):
  ```python
  # Supprimé:
  # _default_jwt_secret = os.getenv("JWT_SECRET", "dev-secret-change-me")
  # JWT_SECRET = get_secret("JWT_SECRET", default=_default_jwt_secret) or _default_jwt_secret
  # JWT_ALG = "HS256"
  ```

- **Middleware installé** (lignes 145-150):
  ```python
  install_auth0_with_entitlements(
      app,
      required_capabilities=["can.use_users"],
      required_quotas={},
      skip_paths=["/health", "/users/register"],
  )
  ```

- **Fonctions d'auth remplacées**:

  **`require_auth()`** (ligne 451-458):
  ```python
  # Avant: Décodage JWT manuel avec jose
  # Après:
  def require_auth(request: Request) -> dict:
      """Extract user info from Auth0 middleware state."""
      customer_id = getattr(request.state, "customer_id", None)
      if not customer_id:
          raise HTTPException(status_code=401, detail="Not authenticated")
      return {"sub": customer_id}
  ```

  **`get_authenticated_actor()`** (ligne 480-490):
  ```python
  # Avant: Validation JWT + vérification x-customer-id header
  # Après:
  def get_authenticated_actor(request: Request) -> int:
      """Extract the authenticated user ID from Auth0 middleware state."""
      customer_id = getattr(request.state, "customer_id", None)
      if not customer_id:
          raise HTTPException(status_code=401, detail="Not authenticated")
      try:
          user_id = int(customer_id)
      except (TypeError, ValueError):
          raise HTTPException(status_code=401, detail="Invalid customer ID")
      return user_id
  ```

**Résultat:**
- ✅ JWT custom supprimé (jose non utilisé)
- ✅ Auth0 middleware gère l'authentification
- ✅ Endpoints inchangés (même signature `Depends(get_authenticated_actor)`)
- ✅ httpx déjà installé
- ✅ Backward compatible avec code existant

---

## 🔄 Services à Migrer

### 3. ⏳ web_dashboard (Frontend)

**Type**: React 18 + Vite + Tailwind

**État actuel:**
- Custom AuthContext (`src/context/AuthContext.jsx`)
- Custom login/logout API calls
- User displayed in header (email)
- Simple logout button

**Changements requis:**
1. Installer `@auth0/auth0-react`
2. Créer UserMenu component
3. Remplacer AuthProvider par Auth0Provider dans `main.jsx`
4. Mettre à jour DashboardLayout pour utiliser UserMenu
5. Créer `config/.env.example` avec config Auth0

**Estimation:** 30 min

---

### 4. ⏳ streaming_gateway (Backend)

**Type**: WebSocket service (FastAPI)

**État actuel:** À analyser

**Changements requis:**
1. Installer httpx (si manquant)
2. Installer Auth0 middleware
3. Gérer authentification WebSocket

**Estimation:** 1-2h (WebSocket = plus complexe)

---

### 5. ⏳ reports (Backend)

**Type**: FastAPI service

**État actuel:** À analyser

**Changements requis:**
1. Vérifier httpx
2. Installer Auth0 middleware
3. Mettre à jour endpoints

**Estimation:** 30 min

---

### 6. ⏳ marketplace (Backend)

**Type**: FastAPI service

**État actuel:** À analyser

**Changements requis:**
1. Vérifier httpx
2. Installer Auth0 middleware
3. Mettre à jour endpoints

**Estimation:** 30 min

---

### 7. ⏳ notification_service (Backend)

**Type**: FastAPI service

**État actuel:** À analyser

**Changements requis:**
1. Vérifier httpx
2. Installer Auth0 middleware
3. Mettre à jour endpoints

**Estimation:** 30 min

---

## 📊 Progression

| Service | Type | Status | Temps estimé | Temps réel |
|---------|------|--------|--------------|------------|
| algo_engine | Backend | ✅ Complété | 30 min | 15 min |
| user_service | Backend | ✅ Complété | 1h | 30 min |
| web_dashboard | Frontend | 🔄 En cours | 30 min | - |
| streaming_gateway | Backend | ⏳ À faire | 1-2h | - |
| reports | Backend | ⏳ À faire | 30 min | - |
| marketplace | Backend | ⏳ À faire | 30 min | - |
| notification_service | Backend | ⏳ À faire | 30 min | - |

**Total**: 2/7 services migrés (29%)

**Temps total estimé restant**: 3-4h

---

## 🎯 Patterns de Migration

### Backend Services (FastAPI)

**Pattern standard:**
```python
# 1. Import
from libs.entitlements.auth0_integration import install_auth0_with_entitlements

# 2. Middleware
install_auth0_with_entitlements(
    app,
    required_capabilities=["can.use_service"],
    skip_paths=["/health"],
)

# 3. Endpoints utilisent Request
@app.get("/api/data")
async def get_data(request: Request):
    customer_id = request.state.customer_id
    email = request.state.user_email
    entitlements = request.state.entitlements
    return {"customer_id": customer_id}
```

**Suppression du code custom JWT:**
- ❌ `from jose import jwt`
- ❌ `JWT_SECRET`, `JWT_ALG` constants
- ❌ Functions `decode_token()`, `require_auth()` avec décodage JWT
- ✅ Garder les fonctions helpers si elles lisent `request.state`

---

### Frontend (React)

**Pattern standard:**
```javascript
// 1. Install
// npm install @auth0/auth0-react

// 2. main.jsx
import { Auth0Provider } from '@auth0/auth0-react'

<Auth0Provider
  domain={domain}
  clientId={clientId}
  authorizationParams={{
    redirect_uri: window.location.origin + '/callback',
    audience: audience,
  }}
>
  <App />
</Auth0Provider>

// 3. Components
import { useAuth0 } from '@auth0/auth0-react'

const { user, isAuthenticated, logout } = useAuth0()
```

---

## ✅ Checklist Migration Service

Pour chaque service:

- [ ] Vérifier que httpx est installé (backend uniquement)
- [ ] Remplacer import entitlements
- [ ] Installer Auth0 middleware
- [ ] Ajouter `/health` dans skip_paths
- [ ] Supprimer code JWT custom (si présent)
- [ ] Tester avec bypass mode
- [ ] Vérifier que les endpoints fonctionnent
- [ ] Committer les changements

---

## 🐛 Problèmes Rencontrés

Aucun pour le moment! 🎉

---

## 🚀 Prochaines Étapes

1. ✅ Terminer web_dashboard (30 min)
2. ✅ Migrer streaming_gateway (1-2h)
3. ✅ Migrer reports, marketplace, notification_service (1.5h)
4. ✅ Tests end-to-end
5. ✅ Documentation finale

**ETA Phase 3 complète**: ~4h
