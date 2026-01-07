---
domain: 4_security
title: Auth0 Migration Status (2025-11)
description: Status report for the Auth0 migration effort.
keywords: auth0, migration, status, security, archived
last_updated: 2026-01-06
status: deprecated
archived_reason: "Migrated from root after documentation restructuring"
related:
  - ../AUTH0_SETUP.md
  - ../INDEX.md
---

# 🚀 Migration Auth0 - État d'Avancement

**Date**: 12 novembre 2025
**Objectif**: Remplacer le système d'authentification custom par Auth0 avec gestion fine des droits utilisateurs

---

## ✅ Phase 1: Architecture Backend (COMPLÉTÉ)

### 📦 Livrables créés

#### 1. **Service `auth_gateway_service`**
   - ✅ Structure complète du service FastAPI
   - ✅ Modèles de données (`Auth0User`, `UserSession`)
   - ✅ Client Auth0 avec validation JWT RS256
   - ✅ Service de synchronisation utilisateurs
   - ✅ Endpoints d'authentification complets
   - ✅ Migration Alembic pour les tables
   - ✅ Configuration Docker + docker compose
   - ✅ Documentation complète (README.md)

**Localisation**: `services/auth_gateway_service/`

#### 2. **Documentation Auth0**
   - ✅ Instructions de setup Auth0 complètes
   - ✅ Configuration des applications (SPA + API)
   - ✅ Configuration social login (Google, GitHub, LinkedIn)
   - ✅ Configuration des rôles et permissions
   - ✅ Custom claims pour les métadonnées

**Localisation**: `docs/domains/4_security/AUTH0_SETUP.md`

#### 3. **Configuration**
   - ✅ Variables d'environnement dans `config/.env.dev`
   - ✅ Configuration docker compose
   - ✅ Port exposé: 8012

### 🏗️ Architecture implémentée

```
┌─────────────────────────────────────────────────┐
│           Frontend (React)                       │
│  • Auth0 SDK (à implémenter)                    │
│  • Redirect vers Auth0 login                    │
└─────────────────────────────────────────────────┘
                    ↓ ↑
┌─────────────────────────────────────────────────┐
│         Auth0 (SaaS) - CONFIGURÉ                │
│  • Universal Login                               │
│  • Social providers (Google, GitHub, LinkedIn)  │
│  • MFA/TOTP support                             │
│  • JWT RS256 tokens                             │
└─────────────────────────────────────────────────┘
                    ↓ ↑
┌─────────────────────────────────────────────────┐
│    auth_gateway_service (NEW) ✅                │
│  • Callback Auth0                                │
│  • Validation tokens                            │
│  • Sync users Auth0 ↔ local                     │
│  • Session management                           │
│  • Entitlements enrichment                      │
└─────────────────────────────────────────────────┘
        ↓               ↓               ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ user_service │ │ entitlements │ │   billing    │
│  (existing)  │ │   (existing) │ │  (existing)  │
│              │ │              │ │              │
│ • Profiles   │ │ • Plans      │ │ • Stripe     │
│ • Prefs      │ │ • Features   │ │ • Subscript. │
│ • API keys   │ │ • Quotas     │ │              │
└──────────────┘ └──────────────┘ └──────────────┘
```

### 🗄️ Base de données

**Nouvelles tables créées**:

1. `auth0_users` - Mapping Auth0 ↔ User local
   - `auth0_sub` → identifiant Auth0 (e.g., "auth0|123456")
   - `local_user_id` → FK vers `users.id`
   - Email, name, picture, login tracking

2. `user_sessions` - Sessions actives
   - `session_id` → UUID de session
   - `local_user_id` → FK vers `users.id`
   - Expiration, révocation, tracking

**Tables conservées** (système entitlements):
- ✅ `plans` - Plans d'abonnement (free, pro, enterprise)
- ✅ `features` - Capabilities et quotas
- ✅ `plan_features` - Features par plan avec limites
- ✅ `subscriptions` - Abonnements actifs (Stripe)
- ✅ `entitlements_cache` - Cache des permissions

### 📋 Endpoints implémentés

| Endpoint | Méthode | Description | Status |
|----------|---------|-------------|--------|
| `/health` | GET | Health check | ✅ |
| `/auth/login` | GET | Redirect Auth0 login | ✅ |
| `/auth/callback` | GET/POST | Callback Auth0 | ✅ |
| `/auth/session` | GET | Session courante | ✅ |
| `/auth/logout` | POST | Déconnexion | ✅ |
| `/auth/validate` | POST | Validation token (S2S) | ✅ |
| `/auth/user` | GET | Info utilisateur | ✅ |

### 🔐 Sécurité

- ✅ Validation JWT avec RS256 (clés publiques Auth0)
- ✅ JWKS caching (1h TTL)
- ✅ Session httponly cookies
- ✅ CORS configuré
- ✅ Token expiration handling
- ✅ Session révocation support

---

## 🔄 Phase 2: Intégrations (EN COURS)

### A. Adapter le middleware d'entitlements ⏳

**Fichier**: `libs/entitlements/fastapi.py`

**Changements requis**:
1. Remplacer validation JWT custom par Auth0
2. Extraire `customer_id` depuis les custom claims Auth0
3. Appeler `auth_gateway_service` pour validation
4. Maintenir la logique d'entitlements existante

**Status**: 🔴 Pending

### B. Créer le portail de login séparé ⏳

**Requirements**:
- Page distincte de l'interface métier
- Embedded Auth0 login (ou Universal Login)
- Social login buttons (Google, GitHub, LinkedIn)
- Responsive design
- Redirect vers dashboard après login

**Technologies**:
- React + Auth0 React SDK
- Tailwind CSS (ou existant)

**Status**: 🔴 Pending

### C. Ajouter menu + logout dans l'interface métier ⏳

**Modifications**:
1. Header avec dropdown user menu
2. Avatar + nom utilisateur
3. Bouton "Logout"
4. Affichage du plan actuel (free, pro, enterprise)
5. Link vers profile/settings

**Fichier**: `services/web_dashboard/src/`

**Status**: 🔴 Pending

---

## 📦 Phase 3: Frontend (À FAIRE)

### A. Installer Auth0 React SDK

```bash
cd services/web_dashboard
npm install @auth0/auth0-react
```

### B. Wrapper App avec Auth0Provider

```jsx
import { Auth0Provider } from '@auth0/auth0-react';

<Auth0Provider
  domain={process.env.REACT_APP_AUTH0_DOMAIN}
  clientId={process.env.REACT_APP_AUTH0_CLIENT_ID}
  redirectUri={window.location.origin + "/auth/callback"}
  audience={process.env.REACT_APP_AUTH0_AUDIENCE}
>
  <App />
</Auth0Provider>
```

### C. Créer composant de callback

**Fichier**: `src/pages/AuthCallback.tsx`

```jsx
import { useAuth0 } from '@auth0/auth0-react';

export const AuthCallback = () => {
  const { error, isLoading } = useAuth0();

  if (isLoading) return <Loading />;
  if (error) return <Error message={error.message} />;

  // Redirect to dashboard
  window.location.href = '/dashboard';
};
```

### D. Remplacer AuthContext custom

**Supprimer**:
- `src/context/AuthContext.jsx`
- `src/pages/Account/AccountLoginPage.jsx`
- `src/pages/Account/AccountRegisterPage.jsx`

**Remplacer par**:
- Auth0 hooks (`useAuth0()`)

---

## 🧪 Phase 4: Tests (À FAIRE)

### Test Checklist

- [ ] **Auth0 Setup**
  - [ ] Tenant créé
  - [ ] Application SPA configurée
  - [ ] API créée avec audience
  - [ ] Social providers activés
  - [ ] Custom Action (claims) déployé

- [ ] **Backend**
  - [ ] Service démarre sans erreur
  - [ ] Health check répond
  - [ ] Login redirect fonctionne
  - [ ] Callback crée un user local
  - [ ] Session persiste
  - [ ] Logout révoque session

- [ ] **Entitlements**
  - [ ] Plan par défaut assigné aux nouveaux users
  - [ ] Capabilities correctement résolues
  - [ ] Quotas appliqués
  - [ ] Upgrade de plan fonctionne

- [ ] **Frontend**
  - [ ] Login flow complet
  - [ ] User info affichée
  - [ ] Menu user accessible
  - [ ] Logout fonctionne
  - [ ] Refresh tokens gérés

- [ ] **Intégration**
  - [ ] Middleware entitlements adapté
  - [ ] Services validant tokens Auth0
  - [ ] CORS configuré partout
  - [ ] Error handling

---

## 📝 Configuration requise

### 1. Auth0 Tenant Setup

Suivre: `docs/domains/4_security/AUTH0_SETUP.md`

**Valeurs à configurer dans `config/.env.dev`**:
```bash
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_CLIENT_ID=<obtenir depuis Auth0 dashboard>
AUTH0_CLIENT_SECRET=<obtenir depuis Auth0 dashboard>
AUTH0_AUDIENCE=https://api.trading-bot.dev
AUTH0_MANAGEMENT_CLIENT_ID=<obtenir depuis Auth0>
AUTH0_MANAGEMENT_CLIENT_SECRET=<obtenir depuis Auth0>
```

### 2. Default Plan

Le plan par défaut pour les nouveaux utilisateurs:
```bash
DEFAULT_PLAN_CODE=free_trial
DEFAULT_PLAN_TRIAL_DAYS=14
```

Assurez-vous que ce plan existe dans la table `plans`:
```sql
INSERT INTO plans (code, name, stripe_price_id, description, trial_period_days, active)
VALUES ('free_trial', 'Free Trial', NULL, '14-day free trial with limited features', 14, true);
```

### 3. Entitlements pour free_trial

Définir les features du plan gratuit:
```sql
-- Capabilities
INSERT INTO features (code, name, kind) VALUES
  ('can.use_strategies', 'Use Strategies', 'capability'),
  ('can.use_alerts', 'Use Alerts', 'capability');

-- Quotas
INSERT INTO features (code, name, kind) VALUES
  ('quota.active_algos', 'Active Algorithms', 'quota'),
  ('quota.api_calls_per_minute', 'API Calls per Minute', 'quota');

-- Assign to free_trial plan
INSERT INTO plan_features (plan_id, feature_id, limit) VALUES
  ((SELECT id FROM plans WHERE code='free_trial'), (SELECT id FROM features WHERE code='can.use_strategies'), NULL),
  ((SELECT id FROM plans WHERE code='free_trial'), (SELECT id FROM features WHERE code='can.use_alerts'), NULL),
  ((SELECT id FROM plans WHERE code='free_trial'), (SELECT id FROM features WHERE code='quota.active_algos'), 3),
  ((SELECT id FROM plans WHERE code='free_trial'), (SELECT id FROM features WHERE code='quota.api_calls_per_minute'), 100);
```

---

## 🚀 Démarrage rapide

### 1. Prérequis

- Docker & Docker Compose
- Auth0 tenant configuré (suivre `docs/domains/4_security/AUTH0_SETUP.md`)
- Variables d'environnement dans `config/.env.dev`

### 2. Lancer les services backend

```bash
# Démarrer la base de données et dépendances
docker compose --project-directory . -f infra/docker-compose.yml up -d postgres redis

# Appliquer les migrations du auth_gateway_service
cd services/auth_gateway_service
alembic upgrade head
cd ../..

# Lancer tous les services
docker compose --project-directory . -f infra/docker-compose.yml up -d
```

### 3. Vérifier que auth_gateway_service fonctionne

```bash
curl http://localhost:8012/health

# Devrait retourner:
# {"status":"ok","service":"auth_gateway_service","timestamp":"..."}
```

### 4. Tester le login flow

```bash
# 1. Ouvrir dans navigateur
open http://localhost:8012/auth/login

# 2. Se connecter sur Auth0
# 3. Devrait redirect vers callback avec code
# 4. Vérifier session créée
curl -i http://localhost:8012/auth/session
```

---

## 📊 Progression globale

| Phase | Description | Status | Progression |
|-------|-------------|--------|-------------|
| 1 | Architecture Backend | ✅ Complété | 100% |
| 2 | Intégrations Backend | ⏳ En cours | 0% |
| 3 | Frontend Auth0 | 🔴 Pending | 0% |
| 4 | Tests & QA | 🔴 Pending | 0% |
| 5 | Documentation | ⏳ En cours | 60% |
| 6 | Déploiement | 🔴 Pending | 0% |

**Progression totale**: ~27% (1.6/6 phases)

---

## 🎯 Prochaines étapes prioritaires

1. **⚠️ URGENT**: Configurer Auth0 tenant
   - Créer application SPA
   - Créer API avec audience
   - Activer social providers
   - Déployer Custom Action pour claims

2. **Backend**: Adapter middleware entitlements
   - Modifier `libs/entitlements/fastapi.py`
   - Valider tokens Auth0
   - Tester avec services existants

3. **Frontend**: Créer portail de login
   - Page séparée avec Auth0 SDK
   - Social login buttons
   - Redirect vers dashboard

4. **Frontend**: Ajouter menu user
   - Header avec dropdown
   - Avatar + nom
   - Bouton logout
   - Affichage plan

5. **Tests**: Flow end-to-end
   - Login → Callback → Dashboard
   - Permissions par plan
   - Logout

---

## 🐛 Points d'attention

### ⚠️ Breaking Changes

**L'ancien système d'authentification sera REMPLACÉ**:
- ❌ `POST /auth/login` (JWT custom) → ✅ Auth0 login
- ❌ `POST /auth/register` → ✅ Auth0 signup
- ❌ Tokens JWT HS256 → ✅ Tokens Auth0 RS256
- ❌ Password reset custom → ✅ Auth0 password reset
- ❌ MFA TOTP custom → ✅ Auth0 MFA

### 🔄 Coexistence temporaire

Pendant la migration, les deux systèmes peuvent coexister:
- `auth_service` (port 8011) - ancien système
- `auth_gateway_service` (port 8012) - nouveau système

**Frontend peut basculer progressivement**:
```javascript
const USE_AUTH0 = process.env.REACT_APP_USE_AUTH0 === 'true';
```

### 🗑️ À supprimer après migration

Une fois la migration complète:
- Supprimer `services/auth_service`
- Supprimer tables: `users.password_hash`, `mfa_totp`, `user_roles`, `roles`
- Supprimer endpoints `/account/login`, `/account/register` du web_dashboard
- Supprimer `AuthContext.jsx` custom

---

## 📞 Support

**Documentation**:
- `docs/domains/4_security/AUTH0_SETUP.md` - Setup Auth0
- `services/auth_gateway_service/README.md` - Service documentation

**Troubleshooting**:
- Vérifier logs: `docker compose --project-directory . -f infra/docker-compose.yml logs auth_gateway_service`
- Health check: `curl http://localhost:8012/health`
- Database: `docker compose --project-directory . -f infra/docker-compose.yml exec postgres psql -U trading -d trading`

**Resources**:
- [Auth0 Documentation](https://auth0.com/docs)
- [Auth0 React Quickstart](https://auth0.com/docs/quickstart/spa/react)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Dernière mise à jour**: 12 novembre 2025
**Auteur**: Claude Code
**Status**: Phase 1 complétée ✅
