---
domain: 2_architecture
title: User Menu Component
description: Composant UserMenu Auth0 pour le dashboard web (avatar, plan, logout).
keywords: webapp, ui, auth0, user-menu, dashboard
last_updated: 2026-01-07
---

# Auth Components

Composants React réutilisables pour l'authentification Auth0.

## Composants disponibles

### UserMenu

Menu dropdown utilisateur avec avatar, nom, plan, et logout.

**Features:**
- ✅ Avatar utilisateur
- ✅ Nom et email
- ✅ Badge du plan (free, pro, enterprise)
- ✅ Links vers Profile, Settings, Billing
- ✅ Bouton Logout
- ✅ Click outside pour fermer
- ✅ Responsive (masque info sur mobile)
- ✅ Loading state
- ✅ Not authenticated state

## Installation

### 1. Utiliser le composant existant

Le composant est déjà disponible ici :

```
services/web_dashboard/src/components/auth/UserMenu.jsx
```

Si vous souhaitez le réutiliser dans un autre frontend, copiez depuis cette source :

```bash
cp services/web_dashboard/src/components/auth/UserMenu.jsx ./src/components/auth/
```

### 2. Installer Auth0 SDK

```bash
cd services/web_dashboard
npm install @auth0/auth0-react
```

### 3. Wrapper votre app avec Auth0Provider

**Dans `src/main.jsx` ou `src/index.jsx`:**

```jsx
import { Auth0Provider } from '@auth0/auth0-react'

const domain = import.meta.env.VITE_AUTH0_DOMAIN
const clientId = import.meta.env.VITE_AUTH0_CLIENT_ID
const audience = import.meta.env.VITE_AUTH0_AUDIENCE

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Auth0Provider
      domain={domain}
      clientId={clientId}
      authorizationParams={{
        redirect_uri: window.location.origin + '/callback',
        audience: audience,
        scope: 'openid profile email',
      }}
      useRefreshTokens={true}
      cacheLocation="localstorage"
    >
      <App />
    </Auth0Provider>
  </React.StrictMode>,
)
```

## Usage

### Dans votre Header/Navbar

```jsx
import { UserMenu } from "../components/auth/UserMenu.jsx"

export function Header() {
  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo */}
          <div className="flex-shrink-0">
            <h1 className="text-2xl font-bold">Trading Bot</h1>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex space-x-8">
            <a href="/dashboard">Dashboard</a>
            <a href="/strategies">Strategies</a>
            <a href="/reports">Reports</a>
          </nav>

          {/* User Menu */}
          <UserMenu />
        </div>
      </div>
    </header>
  )
}
```

### Exemple complet avec Layout

```jsx
import { UserMenu } from "../components/auth/UserMenu.jsx"
import { useAuth0 } from '@auth0/auth0-react'

export function DashboardLayout({ children }) {
  const { isLoading, isAuthenticated } = useAuth0()

  if (isLoading) {
    return <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>
  }

  if (!isAuthenticated) {
    window.location.href = 'http://localhost:3000'  // Redirect to auth portal
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <h1 className="text-2xl font-bold">Trading Bot</h1>
            <UserMenu />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  )
}
```

## Customization

### Changer l'API endpoint

Par défaut, le composant appelle `http://localhost:8012/auth/user`. Pour changer:

```jsx
const AUTH_GATEWAY_URL = import.meta.env.VITE_AUTH_GATEWAY_URL || 'http://localhost:8012'

const response = await fetch(`${AUTH_GATEWAY_URL}/auth/user`, {
  headers: { 'Authorization': `Bearer ${token}` },
})
```

### Changer les menu items

Modifier la section "Menu Items" dans `UserMenu.jsx`:

```jsx
<a
  href="/your-custom-page"
  className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
>
  <svg className="w-5 h-5 mr-3 text-gray-400">
    {/* Your icon */}
  </svg>
  Your Custom Page
</a>
```

### Personnaliser le style

Le composant utilise Tailwind CSS. Changez les classes:

```jsx
// Avatar size
className="w-10 h-10"  // Change to w-12 h-12 for larger

// Dropdown width
className="w-72"  // Change to w-80 for wider

// Plan badge colors
const planColors = {
  free: 'bg-gray-100 text-gray-800',
  pro: 'bg-purple-100 text-purple-800',  // Customize
  enterprise: 'bg-yellow-100 text-yellow-800',
}
```

## Props (optionnel)

Pour rendre le composant plus flexible:

```jsx
export function UserMenu({
  authGatewayUrl = 'http://localhost:8012',
  authPortalUrl = 'http://localhost:3000',
  onLogout,
}) {
  // Use props for configuration
}
```

## Variables d'environnement

Ajouter dans `.env`:

```bash
# Auth0 Configuration
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your_client_id
VITE_AUTH0_AUDIENCE=https://api.trading-bot.dev

# Service URLs
VITE_AUTH_GATEWAY_URL=http://localhost:8012
VITE_AUTH_PORTAL_URL=http://localhost:3000
```

## Exemples

Voir:
- `examples/dashboard-with-auth/` - Dashboard complet avec UserMenu
- `services/auth_portal/` - Portail de login standalone

## Troubleshooting

### UserMenu ne s'affiche pas

**Cause**: Auth0Provider manquant

**Solution**: Wrapper l'app avec Auth0Provider (voir installation)

### Avatar par défaut montré

**Cause**: `user.picture` non disponible

**Solution**: Le composant utilise automatiquement ui-avatars.com en fallback

### Menu ne ferme pas au click outside

**Cause**: Ref not set

**Solution**: Vérifier que `menuRef` est bien assigné au div parent

### Erreur "Failed to fetch user profile"

**Cause**: auth_gateway_service non accessible

**Solution**:
```bash
curl http://localhost:8012/health
docker compose --project-directory . -f infra/docker-compose.yml logs auth_gateway_service
```

## Testing

### Test avec des données mockées

```jsx
import { render } from '@testing-library/react'
import { Auth0Provider } from '@auth0/auth0-react'
import { UserMenu } from './UserMenu'

const mockUser = {
  name: 'John Doe',
  email: 'john@example.com',
  picture: 'https://example.com/avatar.jpg',
}

test('renders user menu', () => {
  render(
    <Auth0Provider
      domain="test.auth0.com"
      clientId="test"
      authorizationParams={{ redirect_uri: window.location.origin }}
    >
      <UserMenu />
    </Auth0Provider>
  )
  // Add assertions
})
```

## Accessibilité

Le composant suit les best practices d'accessibilité:

- ✅ `aria-label` sur le bouton
- ✅ `aria-expanded` pour indiquer l'état du menu
- ✅ Keyboard navigation (Tab, Enter, Esc)
- ✅ Focus management
- ✅ Semantic HTML

## Browser Support

- ✅ Chrome/Edge (dernières versions)
- ✅ Firefox (dernières versions)
- ✅ Safari (dernières versions)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- Lazy load du profil utilisateur
- Memoization des callbacks
- Click outside listener ajouté/retiré dynamiquement
- Avatar optimisé (service externe pour fallback)

## License

MIT - Free to use dans votre projet Trading Bot
