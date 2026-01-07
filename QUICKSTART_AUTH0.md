# 🚀 Auth0 Integration - Quick Start Guide

Guide rapide pour démarrer avec la nouvelle intégration Auth0.

## ⏱️ Temps estimé: 30 minutes

---

## Étape 1: Configurer Auth0 (15 min)

### 1.1 Créer un compte Auth0

1. Aller sur https://auth0.com/signup
2. Créer un compte gratuit (7,000 utilisateurs actifs inclus)
3. Choisir un nom de tenant: `trading-bot-dev`
4. Région: EU ou US (selon votre localisation)

### 1.2 Créer l'application SPA

1. Dans Auth0 Dashboard: **Applications** → **Create Application**
2. Nom: `Trading Bot Web App`
3. Type: **Single Page Application**
4. **Settings**:
   - **Allowed Callback URLs**: `http://localhost:3000/auth/callback`
   - **Allowed Logout URLs**: `http://localhost:3000`
   - **Allowed Web Origins**: `http://localhost:3000`
   - **Allowed Origins (CORS)**: `http://localhost:3000`
5. **Save Changes**

📝 Noter: `Client ID` et `Client Secret`

### 1.3 Créer l'API

1. **Applications** → **APIs** → **Create API**
2. Nom: `Trading Bot API`
3. Identifier: `https://api.trading-bot.dev`
4. Signing Algorithm: **RS256**

### 1.4 Activer Social Login (optionnel)

1. **Authentication** → **Social**
2. Activer **Google** (utiliser Dev Keys)
3. Activer **GitHub** (utiliser Dev Keys)

### 1.5 Configurer Custom Claims

1. **Actions** → **Flows** → **Login**
2. **Create Action**: "Enrich Token"
3. Code:

```javascript
exports.onExecutePostLogin = async (event, api) => {
  const namespace = 'https://api.trading-bot.dev';

  if (event.user.app_metadata) {
    if (event.user.app_metadata.customer_id) {
      api.accessToken.setCustomClaim(`${namespace}/customer_id`, event.user.app_metadata.customer_id);
    }
    if (event.user.app_metadata.plan_code) {
      api.accessToken.setCustomClaim(`${namespace}/plan_code`, event.user.app_metadata.plan_code);
    }
  }
};
```

4. **Deploy** → **Add to Flow**

---

## Étape 2: Configurer l'environnement (5 min)

### 2.1 Mettre à jour `.env.dev`

```bash
cd ~/projects/trading-bot-open-source

# Remplacer les valeurs Auth0
nano .env.dev
```

Modifier:
```bash
AUTH0_DOMAIN=your-tenant.auth0.com  # Remplacer
AUTH0_CLIENT_ID=your_client_id_here  # Depuis Auth0 dashboard
AUTH0_CLIENT_SECRET=your_secret_here  # Depuis Auth0 dashboard
AUTH0_AUDIENCE=https://api.trading-bot.dev
AUTH0_CALLBACK_URL=http://localhost:3000/auth/callback
AUTH0_LOGOUT_URL=http://localhost:3000
```

### 2.2 Management API credentials

1. Dans Auth0: **Applications** → **APIs** → **Auth0 Management API**
2. **Machine to Machine Applications**
3. Autoriser **Trading Bot Web App** avec scopes:
   - `read:users`
   - `update:users`
   - `create:users`
4. Noter Client ID et Secret

Ajouter dans `.env.dev`:
```bash
AUTH0_MANAGEMENT_CLIENT_ID=mgmt_client_id_here
AUTH0_MANAGEMENT_CLIENT_SECRET=mgmt_secret_here
```

---

## Étape 3: Créer le plan par défaut (5 min)

### 3.1 Démarrer la base de données

```bash
docker-compose up -d postgres
```

### 3.2 Créer le plan free_trial

```bash
docker-compose exec postgres psql -U trading -d trading << 'EOF'
-- Créer le plan
INSERT INTO plans (code, name, stripe_price_id, description, trial_period_days, active)
VALUES ('free_trial', 'Free Trial', NULL, '14-day free trial', 14, true)
ON CONFLICT (code) DO NOTHING;

-- Créer les features
INSERT INTO features (code, name, kind, description) VALUES
  ('can.use_strategies', 'Use Strategies', 'capability', 'Access to trading strategies'),
  ('can.use_alerts', 'Use Alerts', 'capability', 'Create and manage alerts'),
  ('quota.active_algos', 'Active Algorithms', 'quota', 'Max concurrent algorithms'),
  ('quota.api_calls_per_minute', 'API Rate Limit', 'quota', 'API calls per minute')
ON CONFLICT (code) DO NOTHING;

-- Assigner les features au plan
INSERT INTO plan_features (plan_id, feature_id, limit)
SELECT p.id, f.id,
  CASE
    WHEN f.code = 'quota.active_algos' THEN 3
    WHEN f.code = 'quota.api_calls_per_minute' THEN 100
    ELSE NULL
  END
FROM plans p, features f
WHERE p.code = 'free_trial'
  AND f.code IN ('can.use_strategies', 'can.use_alerts', 'quota.active_algos', 'quota.api_calls_per_minute')
ON CONFLICT DO NOTHING;
EOF
```

---

## Étape 4: Lancer le service (5 min)

### 4.1 Build et démarrage

```bash
# Lancer tous les services requis
docker-compose up -d postgres redis user_service

# Build auth_gateway_service
docker-compose build auth_gateway_service

# Appliquer les migrations
docker-compose run --rm auth_gateway_service alembic upgrade head

# Lancer le service
docker-compose up -d auth_gateway_service
```

### 4.2 Vérifier que ça marche

```bash
# Health check
curl http://localhost:8012/health

# Devrait retourner:
# {"status":"ok","service":"auth_gateway_service","timestamp":"..."}
```

### 4.3 Voir les logs

```bash
docker-compose logs -f auth_gateway_service
```

---

## Étape 5: Tester le flow Auth0

### 5.1 Test avec navigateur

1. Ouvrir: http://localhost:8012/auth/login
2. Vous serez redirigé vers Auth0
3. Créer un compte ou se connecter
4. Callback vers http://localhost:8012/auth/callback
5. Vérifier la réponse JSON avec session

### 5.2 Test avec curl

```bash
# 1. Get login URL
curl -I http://localhost:8012/auth/login

# 2. Suivre le redirect dans navigateur et récupérer le code

# 3. Vérifier la session (remplacer SESSION_ID)
curl -b "trading_bot_session=SESSION_ID" \
     http://localhost:8012/auth/session

# 4. Tester user info
curl -b "trading_bot_session=SESSION_ID" \
     http://localhost:8012/auth/user
```

---

## ✅ Checklist de validation

- [ ] Auth0 tenant créé
- [ ] Application SPA configurée
- [ ] API créée avec audience
- [ ] Custom Action déployée
- [ ] `.env.dev` mis à jour
- [ ] Plan `free_trial` créé en DB
- [ ] Service démarre sans erreur
- [ ] Health check répond (http://localhost:8012/health)
- [ ] Login redirect fonctionne
- [ ] Callback crée un user local
- [ ] Session persiste et est validée
- [ ] User info retournée correctement

---

## 🐛 Problèmes courants

### Erreur: "Invalid token"

**Solution**: Vérifier que `AUTH0_AUDIENCE` correspond exactement à l'API identifier dans Auth0.

```bash
# Dans .env.dev
AUTH0_AUDIENCE=https://api.trading-bot.dev

# Doit matcher exactement l'identifier de l'API dans Auth0
```

### Erreur: "CORS policy"

**Solution**: Ajouter l'origin dans Auth0 settings:

1. Auth0 Dashboard → Applications → Votre App
2. **Allowed Web Origins**: `http://localhost:3000`
3. **Allowed Origins (CORS)**: `http://localhost:3000`

### Service ne démarre pas

**Solution**: Vérifier les logs et dépendances

```bash
# Logs détaillés
docker-compose logs auth_gateway_service

# Vérifier que postgres est up
docker-compose ps postgres

# Vérifier user_service
docker-compose ps user_service
```

### User n'est pas créé localement

**Solution**: Vérifier les logs du service de sync

```bash
docker-compose logs auth_gateway_service | grep "sync"
```

Vérifier que user_service est accessible:
```bash
docker-compose exec auth_gateway_service curl http://user_service:8000/health
```

---

## 📚 Prochaines étapes

Une fois le backend fonctionnel:

1. **Frontend**: Intégrer Auth0 React SDK
   - Voir `services/web_dashboard`
   - Installer `@auth0/auth0-react`
   - Remplacer AuthContext custom

2. **Portail de login**: Créer page séparée
   - Page standalone avec Auth0 login
   - Social buttons
   - Redirection vers dashboard

3. **Menu utilisateur**: Ajouter dans dashboard
   - Header avec avatar
   - Dropdown avec logout
   - Affichage du plan

4. **Middleware**: Adapter entitlements
   - Modifier `libs/entitlements/fastapi.py`
   - Valider tokens Auth0
   - Extraire customer_id des claims

---

## 🆘 Besoin d'aide?

**Documentation**:
- `docs/domains/4_security/AUTH0_SETUP.md` - Setup détaillé
- `services/auth_gateway_service/README.md` - Doc du service
- `AUTH0_MIGRATION_STATUS.md` - État de la migration

**Logs**:
```bash
# Tous les services
docker-compose logs -f

# Service spécifique
docker-compose logs -f auth_gateway_service
```

**Database**:
```bash
# Se connecter à PostgreSQL
docker-compose exec postgres psql -U trading -d trading

# Vérifier les tables
\dt

# Voir les users Auth0
SELECT * FROM auth0_users;

# Voir les sessions
SELECT * FROM user_sessions;
```

---

**Bon démarrage! 🚀**
