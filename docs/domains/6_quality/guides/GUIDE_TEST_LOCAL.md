---
domain: 6_quality
title: Local Auth0 Test Guide
description: Steps to test the Auth0 flow locally end to end.
keywords: tests, local, auth0, guide, archived
last_updated: 2026-01-06
status: deprecated
archived_reason: "Migrated from root after documentation restructuring"
---

# 🧪 Guide de Test Local - Auth0 Flow Complet

**Date**: 12 novembre 2025
**Objectif**: Tester le flow d'authentification Auth0 de bout en bout

---

## 📋 Prérequis

### 1. Configuration Auth0 (Mode Développement)

Pour tester rapidement sans configurer Auth0, utilisez le **bypass mode**:

```bash
# Dans TOUS les terminaux de services backend:
export AUTH0_BYPASS=1
export ENTITLEMENTS_BYPASS=1
```

> ⚠️ **Note**: Le bypass mode permet de tester sans Auth0 configuré. Pour un test complet avec Auth0, suivez `docs/domains/4_security/AUTH0_SETUP.md`.

### 2. Base de Données

```bash
# Vérifier PostgreSQL
docker ps | grep postgres

# Si pas démarré:
docker compose --project-directory . -f infra/docker-compose.yml up -d postgres
```

---

## 🚀 Démarrage des Services

### Terminal 1: auth_gateway_service (Port 8012)

```bash
cd /home/decarvalhoe/projects/trading-bot-open-source/services/auth_gateway_service

# Installer dependencies (si pas fait)
pip install -r requirements.txt

# Variables d'environnement
export AUTH0_BYPASS=1
export ENTITLEMENTS_BYPASS=1
export DATABASE_URL="postgresql://user:password@localhost:5432/trading_bot"

# Démarrer le service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8012 --reload

# Vérifier:
# ✅ Service running on http://0.0.0.0:8012
```

**Test rapide:**
```bash
curl http://localhost:8012/health
# Attendu: {"status":"ok"}
```

---

### Terminal 2: algo_engine (Port 8000)

```bash
cd /home/decarvalhoe/projects/trading-bot-open-source/services/algo_engine

# Variables d'environnement
export AUTH0_BYPASS=1
export ENTITLEMENTS_BYPASS=1
export DATABASE_URL="postgresql://user:password@localhost:5432/trading_bot"

# Démarrer
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Vérifier:
# ✅ Service running on http://0.0.0.0:8000
```

**Test rapide:**
```bash
curl http://localhost:8000/health
# Attendu: {"status":"ok"}

# Test avec customer_id
curl -H "x-customer-id: 1" http://localhost:8000/strategies
# Attendu: JSON avec liste de stratégies
```

---

### Terminal 3: user_service (Port 8001)

```bash
cd /home/decarvalhoe/projects/trading-bot-open-source/services/user_service

# Variables d'environnement
export AUTH0_BYPASS=1
export ENTITLEMENTS_BYPASS=1
export DATABASE_URL="postgresql://user:password@localhost:5432/trading_bot"

# Démarrer
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Test rapide:**
```bash
curl http://localhost:8001/health
# Attendu: {"status":"ok"}

curl -H "x-customer-id: 1" http://localhost:8001/users/me
# Attendu: JSON avec profil utilisateur
```

---

### Terminal 4: auth_portal (Port 3000)

```bash
cd /home/decarvalhoe/projects/trading-bot-open-source/services/auth_portal

# Installer dependencies (si pas fait)
npm install

# Créer .env.local
cat > .env.local << 'EOF'
VITE_AUTH0_DOMAIN=dev-example.auth0.com
VITE_AUTH0_CLIENT_ID=test_client_id
VITE_AUTH0_AUDIENCE=https://api.trading-bot.dev
VITE_AUTH0_CALLBACK_URL=http://localhost:3000/callback
VITE_DASHBOARD_URL=http://localhost:8022
EOF

# Démarrer (mode dev)
npm run dev

# Vérifier:
# ✅ VITE ready in XXX ms
# ✅ ➜  Local:   http://localhost:3000/
```

**Test rapide:**
Ouvrir http://localhost:3000 dans le navigateur
- ✅ Page de login s'affiche
- ✅ Boutons "Sign In" et "Create Account" visibles

---

### Terminal 5: web_dashboard (Port 8022)

```bash
cd /home/decarvalhoe/projects/trading-bot-open-source/services/web_dashboard

# Installer dependencies (si pas fait)
npm install

# Créer .env.local
cat > .env.local << 'EOF'
VITE_AUTH0_DOMAIN=dev-example.auth0.com
VITE_AUTH0_CLIENT_ID=test_client_id
VITE_AUTH0_AUDIENCE=https://api.trading-bot.dev
VITE_AUTH_GATEWAY_URL=http://localhost:8012
VITE_AUTH_PORTAL_URL=http://localhost:3000
EOF

# Démarrer
npm run dev -- --port 8022

# Vérifier:
# ✅ VITE ready in XXX ms
# ✅ ➜  Local:   http://localhost:8022/
```

**Test rapide:**
Ouvrir http://localhost:8022 dans le navigateur
- ✅ Dashboard s'affiche
- ✅ Sidebar avec navigation visible

---

## 🧪 Tests du Flow Complet

### Test 1: Health Checks (Tous les services)

```bash
# Script de vérification
echo "=== Testing Health Endpoints ==="

echo "\n1. auth_gateway_service (8012):"
curl -s http://localhost:8012/health | jq .

echo "\n2. algo_engine (8000):"
curl -s http://localhost:8000/health | jq .

echo "\n3. user_service (8001):"
curl -s http://localhost:8001/health | jq .

echo "\n4. auth_portal (3000):"
curl -s http://localhost:3000/ -I | head -1

echo "\n5. web_dashboard (8022):"
curl -s http://localhost:8022/ -I | head -1

echo "\n✅ All services are UP!"
```

**Résultat attendu:**
```
=== Testing Health Endpoints ===

1. auth_gateway_service (8012):
{ "status": "ok" }

2. algo_engine (8000):
{ "status": "ok" }

3. user_service (8001):
{ "status": "ok" }

4. auth_portal (3000):
HTTP/1.1 200 OK

5. web_dashboard (8022):
HTTP/1.1 200 OK

✅ All services are UP!
```

---

### Test 2: Bypass Mode (Sans Auth0)

```bash
# Test algo_engine avec bypass
echo "=== Testing algo_engine with bypass mode ==="
curl -H "x-customer-id: 1" http://localhost:8000/strategies | jq .

# Test user_service avec bypass
echo "\n=== Testing user_service with bypass mode ==="
curl -H "x-customer-id: 1" http://localhost:8001/users/me | jq .

# Attendu: 200 OK avec données JSON
```

---

### Test 3: Frontend Navigation (Manuel)

**Étapes:**

1. **Ouvrir auth_portal**: http://localhost:3000
   - ✅ Page de login s'affiche
   - ✅ Design moderne avec gradient
   - ✅ Boutons "Sign In" et "Create Account"
   - ✅ Stats affichées (99.9% Uptime, etc.)

2. **Ouvrir web_dashboard**: http://localhost:8022
   - ✅ Dashboard s'affiche
   - ✅ Sidebar avec navigation
   - ✅ UserMenu visible en haut à droite
   - ✅ Si non authentifié: bouton "Sign In"

3. **Tester navigation**:
   - Cliquer sur "Stratégies" dans sidebar
   - Cliquer sur "Ordres"
   - Cliquer sur "Tableau de bord"
   - ✅ Toutes les pages se chargent

---

### Test 4: Auth0 Flow (Si Auth0 configuré)

**Prérequis**: Avoir configuré Auth0 selon `docs/domains/4_security/AUTH0_SETUP.md`

#### Étape 1: Supprimer bypass mode

```bash
# Dans TOUS les terminaux:
unset AUTH0_BYPASS
unset ENTITLEMENTS_BYPASS

# Redémarrer les services
```

#### Étape 2: Configurer .env avec vrais credentials

```bash
# Dans auth_portal/.env.local
VITE_AUTH0_DOMAIN=your-real-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your_real_client_id
VITE_AUTH0_AUDIENCE=https://api.trading-bot.dev

# Dans web_dashboard/.env.local
VITE_AUTH0_DOMAIN=your-real-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your_real_client_id
VITE_AUTH0_AUDIENCE=https://api.trading-bot.dev

# Redémarrer les frontends
```

#### Étape 3: Test du flow complet

1. **Login**:
   - Aller sur http://localhost:3000
   - Cliquer "Sign In"
   - ✅ Redirect vers Auth0 Universal Login

2. **Authentification**:
   - Se connecter avec email/password OU
   - Se connecter avec Google/GitHub/LinkedIn
   - ✅ Authentification réussie

3. **Callback**:
   - Auth0 redirige vers http://localhost:3000/callback
   - ✅ Page callback affiche "Processing authentication..."
   - ✅ Spinner animé visible
   - ✅ Steps progression: Auth → Sync → Redirect

4. **Sync**:
   - auth_gateway_service reçoit le callback
   - ✅ User sync dans la DB
   - ✅ Session créée

5. **Dashboard**:
   - Redirect automatique vers http://localhost:8022
   - ✅ Dashboard s'affiche avec user connecté
   - ✅ UserMenu affiche avatar et nom
   - ✅ Badge du plan visible (FREE/PRO/etc.)

6. **API Calls**:
   - Dashboard appelle les APIs backend
   - ✅ Token Auth0 envoyé dans headers
   - ✅ Middleware valide le token
   - ✅ Données retournées

7. **Logout**:
   - Cliquer sur UserMenu → "Sign Out"
   - ✅ Logout Auth0
   - ✅ Redirect vers auth_portal
   - ✅ User déconnecté

---

## 🐛 Troubleshooting

### Problème: Service ne démarre pas

**Symptôme**: `ModuleNotFoundError: No module named 'app'`

**Solution**:
```bash
# Vérifier qu'on est dans le bon dossier
pwd
# Doit être: /path/to/services/SERVICE_NAME

# Installer requirements
pip install -r requirements.txt

# Ou utiliser absolute path:
cd /home/decarvalhoe/projects/trading-bot-open-source
python -m services.algo_engine.app.main
```

---

### Problème: Port déjà utilisé

**Symptôme**: `[Errno 48] Address already in use`

**Solution**:
```bash
# Trouver le process sur le port
lsof -i :8000

# Tuer le process
kill -9 <PID>

# Ou utiliser un autre port
uvicorn app.main:app --port 8001
```

---

### Problème: Database connection error

**Symptôme**: `could not connect to server: Connection refused`

**Solution**:
```bash
# Vérifier PostgreSQL
docker ps | grep postgres

# Démarrer si besoin
docker compose --project-directory . -f infra/docker-compose.yml up -d postgres

# Tester connection
psql -h localhost -U user -d trading_bot

# Mettre à jour DATABASE_URL
export DATABASE_URL="postgresql://user:password@localhost:5432/trading_bot"
```

---

### Problème: Frontend - Module not found

**Symptôme**: `Error: Cannot find module '@auth0/auth0-react'`

**Solution**:
```bash
# Réinstaller dependencies
cd services/web_dashboard
rm -rf node_modules package-lock.json
npm install

# Vérifier que @auth0/auth0-react est installé
npm list @auth0/auth0-react
```

---

### Problème: CORS errors

**Symptôme**: `Access to fetch blocked by CORS policy`

**Solution**:
```bash
# Vérifier que les services backend ont CORS configuré
# Les middlewares Auth0 doivent être AVANT CORS

# Dans le code backend:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8022"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## ✅ Checklist de Validation

### Backend Services

- [ ] **auth_gateway_service** démarre sur port 8012
- [ ] **algo_engine** démarre sur port 8000
- [ ] **user_service** démarre sur port 8001
- [ ] Health checks retournent `{"status":"ok"}`
- [ ] Endpoints avec `x-customer-id` fonctionnent (bypass mode)

### Frontend

- [ ] **auth_portal** démarre sur port 3000
- [ ] **web_dashboard** démarre sur port 8022
- [ ] Pages se chargent sans erreur
- [ ] Navigation fonctionne
- [ ] UserMenu s'affiche

### Auth0 Flow (Si configuré)

- [ ] Login redirect vers Auth0
- [ ] Authentification réussie
- [ ] Callback traité correctement
- [ ] User sync dans DB
- [ ] Dashboard affiche user connecté
- [ ] API calls avec token fonctionnent
- [ ] Logout fonctionne

### Intégration

- [ ] Pas d'erreurs dans les consoles
- [ ] Pas d'erreurs dans les logs backend
- [ ] Tokens validés correctement
- [ ] Entitlements appliqués
- [ ] Session persiste après refresh

---

## 📊 Résultats Attendus

### Bypass Mode (Sans Auth0)

```bash
# Test réussi:
✅ Tous les health checks OK
✅ Endpoints avec x-customer-id: 200 OK
✅ Frontend charge sans erreur
✅ Navigation fonctionne

# Limites:
⚠️ Pas de vraie authentification
⚠️ x-customer-id manuel
⚠️ Pas de social login
```

### Avec Auth0 Configuré

```bash
# Test réussi:
✅ Login flow complet OK
✅ Social login fonctionne
✅ Token validation OK
✅ User sync DB OK
✅ Session persiste
✅ Logout OK

# Avantages:
🔒 Authentification sécurisée
👥 Social login (Google, GitHub, etc.)
🔄 Token refresh automatique
📱 MFA disponible
```

---

## 🎯 Scénarios de Test

### Scénario 1: Premier Login

1. User va sur auth_portal
2. Clique "Sign In"
3. Première fois → Redirect vers signup Auth0
4. Remplit formulaire (ou social login)
5. Auth0 crée le compte
6. Callback vers auth_portal
7. auth_gateway_service sync le user (création DB)
8. Redirect vers dashboard
9. Dashboard affiche le profil
10. Plan = "free" par défaut

**Attendu**: ✅ User créé, connecté, plan free

---

### Scénario 2: Login Existing User

1. User va sur auth_portal
2. Clique "Sign In"
3. Entre credentials
4. Auth0 authentifie
5. Callback vers auth_portal
6. auth_gateway_service trouve le user existant
7. Redirect vers dashboard
8. Dashboard affiche le profil avec plan actuel

**Attendu**: ✅ User connecté, plan existant conservé

---

### Scénario 3: API Call avec Token

1. User connecté sur dashboard
2. Dashboard appelle GET /api/strategies
3. Auth0 SDK ajoute token dans header
4. Backend reçoit: `Authorization: Bearer <token>`
5. Auth0Middleware valide le token
6. Extrait customer_id
7. EntitlementsMiddleware fetch entitlements
8. Endpoint retourne les stratégies filtrées par permissions

**Attendu**: ✅ Données filtrées par plan

---

### Scénario 4: Quota Exceeded

1. User avec plan FREE (max_active_strategies=2)
2. A déjà 2 stratégies actives
3. Essaye de créer une 3ème
4. EntitlementsMiddleware bloque
5. Retourne: `403 Forbidden - Active strategy limit reached`

**Attendu**: ✅ Quota respecté, erreur explicite

---

## 📝 Logs à Vérifier

### Backend Logs

```bash
# auth_gateway_service
INFO:     Token validated for customer_id: 1
INFO:     User synced: user@example.com
INFO:     Session created: session_abc123

# algo_engine
INFO:     Auth0 middleware: customer_id=1 extracted
INFO:     Entitlements loaded: plan=free, capabilities=[can.manage_strategies]
INFO:     Request authorized: GET /strategies
```

### Frontend Console

```javascript
// Auth0 SDK
Auth0 Provider initialized
Getting access token silently...
Token obtained: eyJ...
Calling API: http://localhost:8000/api/strategies
API response: 200 OK

// UserMenu
Fetching user profile...
Profile loaded: { name: "John", plan: "free" }
```

---

## 🚀 Commandes Rapides

### Démarrer tous les services (Bypass Mode)

```bash
chmod +x scripts/dev/start-all-services.sh
scripts/dev/start-all-services.sh
```

### Stopper tous les services

```bash
chmod +x scripts/dev/stop-all-services.sh
scripts/dev/stop-all-services.sh
```

---

**Guide de test créé avec succès!** 🎉

**Prochaine action**: Exécuter les tests ci-dessus pour valider la migration.
