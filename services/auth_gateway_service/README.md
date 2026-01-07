# Auth Gateway Service

Service passerelle d'authentification intégrant Auth0 avec l'architecture du Trading Bot.

## 🎯 Objectif

Remplacer le système d'authentification custom (JWT maison) par Auth0 tout en conservant:
- ✅ Le système d'entitlements existant (plans, features, quotas)
- ✅ La gestion fine des permissions par plan d'abonnement
- ✅ L'intégration avec Stripe pour la facturation
- ✅ Les données utilisateurs locales (profils, préférences, API keys)

## 🏗️ Architecture

```
Auth0 (SaaS)
    ↓ (Authentication)
Auth Gateway Service
    ↓ (User Sync + Session)
User Service (profiles) + Entitlements Service (permissions)
```

### Flow d'authentification

1. **Login**: L'utilisateur clique sur "Login"
2. **Redirect**: Redirect vers Auth0 Universal Login
3. **Auth0**: L'utilisateur s'authentifie (email/password, social login, MFA)
4. **Callback**: Auth0 redirige vers `/auth/callback` avec un code
5. **Exchange**: Le service échange le code contre des tokens Auth0
6. **Sync**: Synchronisation avec la base locale:
   - Création/mise à jour du user dans `user_service`
   - Création du mapping Auth0 ↔ user local dans `auth0_users`
   - Attribution du plan par défaut (free_trial) si nouveau user
7. **Session**: Création d'une session locale avec cookie httponly
8. **Entitlements**: Récupération des permissions basées sur le plan
9. **Response**: Retour des infos utilisateur + entitlements

## 📁 Structure

```
services/auth_gateway_service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app + endpoints
│   ├── config.py            # Configuration (Auth0, DB, etc.)
│   ├── models.py            # SQLAlchemy models (Auth0User, UserSession)
│   ├── schemas.py           # Pydantic schemas (requests/responses)
│   ├── database.py          # Database connection
│   ├── auth0_client.py      # Client Auth0 (validation tokens, Management API)
│   └── user_sync.py         # Synchronisation users Auth0 ↔ local
├── migrations/              # Alembic migrations
│   └── versions/
│       └── 0001_create_auth0_tables.py
├── requirements.txt         # Dependencies Python
├── Dockerfile              # Image Docker
└── README.md               # Ce fichier
```

## 🗄️ Modèles de données

### Table `auth0_users`

Mapping entre utilisateurs Auth0 et utilisateurs locaux.

```sql
CREATE TABLE auth0_users (
    id SERIAL PRIMARY KEY,
    auth0_sub VARCHAR(255) UNIQUE NOT NULL,  -- Auth0 user ID (e.g., "auth0|123456")
    local_user_id INT NOT NULL REFERENCES users(id),
    email VARCHAR(255) NOT NULL,
    email_verified BOOLEAN DEFAULT false,
    picture VARCHAR(500),
    name VARCHAR(255),
    nickname VARCHAR(255),
    auth0_created_at TIMESTAMPTZ,
    last_login TIMESTAMPTZ,
    login_count INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Table `user_sessions`

Sessions utilisateurs actives.

```sql
CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    local_user_id INT NOT NULL REFERENCES users(id),
    auth0_sub VARCHAR(255) NOT NULL,
    access_token_jti VARCHAR(255),
    expires_at TIMESTAMPTZ NOT NULL,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_activity TIMESTAMPTZ DEFAULT NOW(),
    revoked_at TIMESTAMPTZ
);
```

## 🔌 Endpoints

### GET `/health`
Health check du service.

### GET `/auth/login`
Redirect vers Auth0 login.

**Response**: 302 Redirect vers Auth0

### POST/GET `/auth/callback`
Callback Auth0 après authentification.

**Query params**:
- `code`: Authorization code from Auth0
- `state`: State parameter (optional)

**Headers (SPA flow)**:
- `Authorization: Bearer <access_token>`: Utiliser directement un access token Auth0 (pas de `code` requis)

**Response**: `UserSessionResponse`
```json
{
  "session_id": "...",
  "user_id": 123,
  "email": "user@example.com",
  "name": "John Doe",
  "picture": "https://...",
  "plan_code": "free_trial",
  "roles": ["user"],
  "expires_at": "2025-11-13T10:00:00Z",
  "capabilities": {
    "can.use_strategies": true,
    "can.use_alerts": true
  },
  "quotas": {
    "quota.active_algos": 5
  }
}
```

### GET `/auth/session`
Récupère la session courante.

**Headers/Cookies**: `trading_bot_session` cookie

**Response**: `UserSessionResponse`

### POST `/auth/logout`
Déconnexion (révoque la session + logout Auth0).

**Response**:
```json
{
  "message": "Logged out successfully",
  "logout_url": "https://your-tenant.auth0.com/v2/logout?..."
}
```

### POST `/auth/validate`
Valide un token Auth0 (service-to-service).

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "valid": true,
  "auth0_sub": "auth0|123456",
  "local_user_id": 123,
  "email": "user@example.com",
  "roles": ["user"],
  "plan_code": "pro"
}
```

### GET `/auth/user`
Infos sur l'utilisateur courant.

**Response**:
```json
{
  "id": 123,
  "email": "user@example.com",
  "name": "John Doe",
  "picture": "https://...",
  "email_verified": true,
  "last_login": "2025-11-12T10:00:00Z",
  "login_count": 42
}
```

## 🔐 Configuration Auth0

Voir [docs/domains/4_security/AUTH0_SETUP.md](../../docs/domains/4_security/AUTH0_SETUP.md) pour les instructions complètes.

### Variables d'environnement requises

```bash
# Auth0 Application (SPA)
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_CLIENT_ID=your_client_id
AUTH0_CLIENT_SECRET=your_client_secret
AUTH0_AUDIENCE=https://api.trading-bot.dev
AUTH0_CALLBACK_URL=http://localhost:3000/auth/callback
AUTH0_LOGOUT_URL=http://localhost:3000

# Auth0 Management API
AUTH0_MANAGEMENT_CLIENT_ID=your_mgmt_client_id
AUTH0_MANAGEMENT_CLIENT_SECRET=your_mgmt_secret

# Default Plan
DEFAULT_PLAN_CODE=free_trial
DEFAULT_PLAN_TRIAL_DAYS=14

# Database
DATABASE_URL=postgresql+psycopg2://trading:trading@postgres:5432/trading

# Services URLs
USER_SERVICE_URL=http://user_service:8000
ENTITLEMENTS_SERVICE_URL=http://entitlements_service:8000
BILLING_SERVICE_URL=http://billing_service:8000
```

## 🚀 Démarrage

### Développement local

1. **Configurer Auth0** (voir [AUTH0_SETUP.md](../../docs/domains/4_security/AUTH0_SETUP.md))

2. **Mettre à jour `config/.env.dev`** avec vos credentials Auth0

3. **Lancer les services**:
```bash
docker-compose up -d postgres redis user_service entitlements_service billing_service
```

4. **Appliquer les migrations**:
```bash
cd services/auth_gateway_service
alembic upgrade head
```

5. **Lancer le service**:
```bash
cd services/auth_gateway_service
uvicorn app.main:app --reload --port 8012
```

Le service sera accessible sur http://localhost:8012

### Avec Docker Compose

```bash
docker-compose up auth_gateway_service
```

## 🧪 Tests

### Test manuel du flow

1. Ouvrir http://localhost:8012/auth/login
2. Se connecter sur Auth0
3. Vérifier le callback et la création de session
4. Tester http://localhost:8012/auth/session
5. Tester http://localhost:8012/auth/user
6. Logout: http://localhost:8012/auth/logout

### Test avec curl

```bash
# Health check
curl http://localhost:8012/health

# Obtenir l'URL de login
curl -I http://localhost:8012/auth/login

# Vérifier session (avec cookie)
curl -b "trading_bot_session=..." http://localhost:8012/auth/session

# Valider un token Auth0
curl -H "Authorization: Bearer <auth0_token>" \
     http://localhost:8012/auth/validate
```

## 🔄 Intégration avec les autres services

### Middleware d'entitlements

Les services existants doivent être adaptés pour valider les tokens Auth0 au lieu des JWT custom.

**Avant** (`libs/entitlements/fastapi.py`):
```python
# Validation JWT custom
token = extract_jwt_from_header()
payload = validate_jwt(token)
customer_id = payload.get("user_id")
```

**Après** (à implémenter):
```python
# Validation token Auth0 via auth_gateway_service
token = extract_jwt_from_header()
response = await auth_gateway_validate(token)
customer_id = response["local_user_id"]
```

### Frontend

Le frontend doit utiliser l'Auth0 SDK au lieu du système custom.

**React** (`services/web_dashboard`):
```javascript
import { Auth0Provider, useAuth0 } from '@auth0/auth0-react';

// Dans le root component
<Auth0Provider
  domain="your-tenant.auth0.com"
  clientId="your_client_id"
  redirectUri={window.location.origin + "/auth/callback"}
  audience="https://api.trading-bot.dev"
>
  <App />
</Auth0Provider>

// Dans les composants
const { loginWithRedirect, logout, user, isAuthenticated } = useAuth0();
```

## 📋 TODO / Prochaines étapes

- [ ] Adapter le middleware d'entitlements pour Auth0
- [ ] Créer le portail de login séparé (React)
- [ ] Mettre à jour le frontend du dashboard
- [ ] Ajouter menu + logout dans l'interface métier
- [ ] Migrer les utilisateurs existants (si applicable)
- [ ] Tests end-to-end complets
- [ ] Documentation API complète
- [ ] Monitoring et logs

## 🐛 Troubleshooting

### Erreur "Invalid token"
- Vérifier que `AUTH0_AUDIENCE` correspond à l'API identifier dans Auth0
- Vérifier que `AUTH0_DOMAIN` est correct
- S'assurer que le token n'est pas expiré

### Erreur "User not found locally"
- Le mapping Auth0 ↔ user local n'existe pas
- Vérifier que le callback a bien été appelé
- Checker les logs du user_sync_service

### Session invalide/expirée
- Vérifier que le cookie `trading_bot_session` existe
- Vérifier `SESSION_MAX_AGE` dans la config
- Checker la table `user_sessions` en DB

### CORS errors
- Ajouter l'origin à `ALLOWED_ORIGINS` dans `config/.env.dev`
- Vérifier les settings CORS dans Auth0

## 📚 Ressources

- [Auth0 Documentation](https://auth0.com/docs)
- [Auth0 Python SDK](https://github.com/auth0/auth0-python)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Project docs/domains/4_security/AUTH0_SETUP.md](../../docs/domains/4_security/AUTH0_SETUP.md)
