# Auth Portal - Standalone Login Portal

Portail d'authentification standalone pour le Trading Bot, utilisant Auth0.

## 🎯 Objectif

Fournir une page de login **séparée** de l'interface métier principale, avec:
- Design moderne et professionnel
- Social login (Google, GitHub, LinkedIn)
- Inscription et connexion
- Redirect automatique vers le dashboard après auth

## 🏗️ Architecture

```
User accesses login page
    ↓
Auth Portal (React + Auth0 SDK)
    ↓
Auth0 Universal Login / Embedded
    ↓
Auth Gateway Service (sync user)
    ↓
Redirect to Dashboard
```

## 📦 Technologies

- **React 18** - UI framework
- **Vite** - Build tool
- **Auth0 React SDK** - Authentication
- **Tailwind CSS** - Styling
- **React Router** - Routing

## 🚀 Installation

### 1. Installer les dépendances

```bash
cd services/auth_portal
npm install
```

### 2. Configuration

Créer un fichier `.env.local`:

```bash
cp .env.example .env.local
```

Editer `.env.local`:

```bash
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your_spa_client_id
VITE_AUTH0_AUDIENCE=https://api.trading-bot.dev
VITE_AUTH0_CALLBACK_URL=http://localhost:3000/callback
VITE_DASHBOARD_URL=http://localhost:8022
VITE_AUTH_GATEWAY_URL=http://localhost:8012
```

### 3. Démarrer en développement

```bash
npm run dev
```

Le portail sera accessible sur http://localhost:3000

### 4. Build pour production

```bash
npm run build
npm run preview
```

## 📁 Structure

```
services/auth_portal/
├── src/
│   ├── pages/
│   │   ├── LoginPage.jsx       # Page de login principale
│   │   └── CallbackPage.jsx    # Callback après Auth0
│   ├── App.jsx                 # App root avec routing
│   ├── main.jsx                # Entry point + Auth0Provider
│   └── index.css               # Styles Tailwind
├── public/                     # Assets statiques
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## 🎨 Design Features

### Page de Login

- **Logo et titre** avec animation
- **Bouton Sign In** principal
- **Bouton Create Account** avec style outline
- **Stats** en bas (Uptime, Support, Users)
- **Responsive** design
- **Loading states** pendant l'authentification

### Page de Callback

- **Loading spinner** animé
- **Status messages** en temps réel
- **Progress steps** (Auth → Sync → Redirect)
- **Error handling** avec option de retry

## 🔄 Flow d'authentification

### 1. User clique "Sign In"

```javascript
const { loginWithRedirect } = useAuth0();
loginWithRedirect();  // Redirect to Auth0
```

### 2. Auth0 authentication

User se connecte avec:
- Email/password
- Google account
- GitHub account
- LinkedIn account

### 3. Callback

Auth0 redirige vers `/callback` avec code

```javascript
// CallbackPage.jsx
const token = await getAccessTokenSilently();

// Sync with backend
const authGatewayUrl = import.meta.env.VITE_AUTH_GATEWAY_URL || 'http://localhost:8012';
await fetch(`${authGatewayUrl}/auth/callback`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  credentials: 'include',
});
```

### 4. Redirect to Dashboard

```javascript
window.location.href = dashboardUrl;
```

## 🔧 Customization

### Changer les couleurs

Editer `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        500: '#your-color',
        600: '#your-color',
        700: '#your-color',
      },
    },
  },
}
```

### Changer le logo

Remplacer le SVG dans `LoginPage.jsx`:

```jsx
<svg className="w-16 h-16 text-primary-600">
  {/* Your logo SVG */}
</svg>
```

### Ajouter des features

Modifier les stats dans `LoginPage.jsx`:

```jsx
<div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
  <div className="text-2xl font-bold text-white">Your Stat</div>
  <div className="text-sm text-primary-100">Label</div>
</div>
```

## 🔐 Sécurité

- ✅ Tokens stockés en `localstorage` (secure avec Auth0 SDK)
- ✅ Refresh tokens enabled (automatic token renewal)
- ✅ HTTPS required in production
- ✅ CORS configured in Auth0 dashboard
- ✅ No password handling (Auth0 managed)

## 🌐 Déploiement

### Build

```bash
npm run build
```

Les fichiers seront dans `dist/`

### Servir les fichiers statiques

**Option 1: NGINX**

```nginx
server {
    listen 80;
    server_name login.yourdomain.com;
    root /path/to/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

**Option 2: Docker**

Créer `Dockerfile`:

```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Variables d'environnement en production

```bash
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your_prod_client_id
VITE_AUTH0_AUDIENCE=https://api.yourdomain.com
VITE_AUTH0_CALLBACK_URL=https://login.yourdomain.com/callback
VITE_DASHBOARD_URL=https://app.yourdomain.com
VITE_AUTH_GATEWAY_URL=https://auth.yourdomain.com
```

## 🐛 Troubleshooting

### Erreur: "domain is required"

**Cause**: Variables d'environnement manquantes

**Solution**:
```bash
# Vérifier que .env.local existe
ls -la .env.local

# Vérifier les variables
cat .env.local

# Redémarrer dev server
npm run dev
```

### Login redirect ne fonctionne pas

**Cause**: Callback URL mal configurée dans Auth0

**Solution**:
1. Auth0 Dashboard → Applications → Your App
2. **Allowed Callback URLs**: `http://localhost:3000/callback`
3. Save changes
4. Clear browser cache

### Callback page affiche une erreur

**Cause**: auth_gateway_service non accessible

**Solution**:
```bash
# Vérifier que le service tourne
curl http://localhost:8012/health

# Vérifier les logs
docker-compose logs auth_gateway_service

# Démarrer si nécessaire
docker-compose up -d auth_gateway_service
```

### CORS errors

**Cause**: Origin non autorisé dans Auth0

**Solution**:
1. Auth0 Dashboard → Applications → Your App
2. **Allowed Web Origins**: `http://localhost:3000`
3. **Allowed Origins (CORS)**: `http://localhost:3000`
4. Save changes

## 📱 Responsive Design

Le portail est entièrement responsive:

- **Mobile**: Design vertical, touch-friendly
- **Tablet**: Layout adapté
- **Desktop**: Full design avec stats

Testez avec:
```bash
# Chrome DevTools
Cmd+Option+I → Toggle device toolbar
```

## 🧪 Tests

### Test manuel

1. Ouvrir http://localhost:3000
2. Cliquer "Sign In"
3. Se connecter sur Auth0
4. Vérifier redirect vers callback
5. Vérifier redirect vers dashboard

### Test avec différents providers

- Email/password
- Google
- GitHub
- LinkedIn

### Test en mode incognito

Pour tester sans cache:
```
Cmd+Shift+N (Chrome)
Cmd+Shift+P (Firefox)
```

## 🎯 Next Steps

Après avoir testé le portail:

1. Intégrer avec le dashboard principal
2. Ajouter UserMenu component
3. Configurer logout
4. Tests end-to-end
5. Déploiement en production

## 📚 Resources

- [Auth0 React Quickstart](https://auth0.com/docs/quickstart/spa/react)
- [Auth0 SDK API](https://auth0.github.io/auth0-react/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)

## 🆘 Support

- Auth Portal issues: Check console errors
- Auth0 issues: Check Auth0 Dashboard logs
- Backend issues: Check auth_gateway_service logs

```bash
# Browser console
F12 → Console

# Backend logs
docker-compose logs -f auth_gateway_service
```
