---
domain: 4_security
title: Auth0 Setup Instructions - Trading Bot
description: Step-by-step Auth0 configuration and local quick start.
keywords: auth0, setup, security, identity, quick-start
last_updated: 2026-01-06
---

# Auth0 Setup Instructions - Trading Bot

## Quick Start (30 minutes)

1. Create the Auth0 tenant, SPA application, and API (sections 1-3).
2. Configure environment variables (section 9 + summary below).
3. Seed the default plan (section 11).
4. Run the auth gateway service locally (section 12).
5. Validate the login flow (section 13).

## 1. Create Auth0 Tenant

1. Go to https://auth0.com/signup
2. Create a FREE account (up to 7,000 active users)
3. Choose tenant name: `trading-bot-dev` (or your preference)
4. Region: Choose closest to your users (e.g., EU/US)

## 2. Create Application

1. Navigate to **Applications** → **Applications**
2. Click **Create Application**
3. Name: `Trading Bot Web App`
4. Type: **Single Page Application** (for embedded login)
5. Click **Create**

### Application Settings

Once created, go to **Settings** tab:

**Allowed Callback URLs:**
```
http://localhost:3000/auth/callback
http://localhost:8000/auth/callback
```

**Allowed Logout URLs:**
```
http://localhost:3000
http://localhost:8000
```

**Allowed Web Origins:**
```
http://localhost:3000
http://localhost:8000
```

**Allowed Origins (CORS):**
```
http://localhost:3000
http://localhost:8000
```

Save changes.

## 3. Configure API

1. Navigate to **Applications** → **APIs**
2. Click **Create API**
3. Name: `Trading Bot API`
4. Identifier: `https://api.trading-bot.dev` (this is your audience)
5. Signing Algorithm: **RS256**
6. Click **Create**

### API Settings

**Token Expiration:**
- Access Token: 86400 seconds (24 hours)
- Refresh Token: 2592000 seconds (30 days)

**RBAC Settings:**
- Enable RBAC: ✅ ON
- Add Permissions in Access Token: ✅ ON

### API Permissions (Scopes)

Add these permissions:
- `read:profile` - Read user profile
- `write:profile` - Update user profile
- `read:strategies` - View strategies
- `write:strategies` - Create/modify strategies
- `read:alerts` - View alerts
- `write:alerts` - Create alerts
- `manage:users` - Admin user management

## 4. Enable Social Connections

### Google

1. Navigate to **Authentication** → **Social**
2. Click **Google**
3. Toggle **Enable**
4. Use Auth0 Dev Keys (for testing) OR add your own:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create OAuth 2.0 Client ID
   - Authorized redirect URI: `https://YOUR_TENANT.auth0.com/login/callback`
5. Save

### GitHub

1. In **Social** connections, click **GitHub**
2. Toggle **Enable**
3. For production, create GitHub OAuth App:
   - Go to GitHub Settings → Developer settings → OAuth Apps
   - Authorization callback URL: `https://YOUR_TENANT.auth0.com/login/callback`
4. Save

### LinkedIn

1. In **Social** connections, click **LinkedIn**
2. Toggle **Enable**
3. For production, create LinkedIn App:
   - Go to [LinkedIn Developers](https://www.linkedin.com/developers)
   - Redirect URLs: `https://YOUR_TENANT.auth0.com/login/callback`
4. Save

## 5. Configure User Metadata

Navigate to **Actions** → **Flows** → **Login**

Create a new Action: **Enrich Token with Custom Claims**

```javascript
exports.onExecutePostLogin = async (event, api) => {
  const namespace = 'https://api.trading-bot.dev';

  // Add custom claims to access token
  if (event.user.app_metadata) {
    if (event.user.app_metadata.customer_id) {
      api.accessToken.setCustomClaim(`${namespace}/customer_id`, event.user.app_metadata.customer_id);
    }
    if (event.user.app_metadata.plan_code) {
      api.accessToken.setCustomClaim(`${namespace}/plan_code`, event.user.app_metadata.plan_code);
    }
  }

  // Add user roles
  if (event.authorization && event.authorization.roles) {
    api.accessToken.setCustomClaim(`${namespace}/roles`, event.authorization.roles);
  }
};
```

**Deploy** the Action and **Add to Flow** (drag to the flow diagram).

## 6. Create Roles

Navigate to **User Management** → **Roles**

Create these roles:
1. **Admin** - Full access
2. **User** - Standard user access
3. **Free User** - Limited access (free tier)
4. **Pro User** - Pro tier access
5. **Enterprise User** - Enterprise tier access

For each role, assign appropriate API permissions from step 3.

## 7. Configure Default User Settings

Navigate to **User Management** → **Users** → **Default Directory**

Set default role: **Free User**

## 8. Customize Universal Login (Optional)

Navigate to **Branding** → **Universal Login**

- **Logo**: Upload your trading bot logo
- **Primary Color**: Choose brand color
- **Background Color**: Choose background
- **Save Changes**

## 9. Get Credentials

Navigate to **Applications** → **Applications** → **Trading Bot Web App** → **Settings**

Copy these values for your `.env` file:

```bash
# Auth0 Configuration
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_CLIENT_ID=your_client_id_here
AUTH0_CLIENT_SECRET=your_client_secret_here
AUTH0_AUDIENCE=https://api.trading-bot.dev
AUTH0_CALLBACK_URL=http://localhost:3000/auth/callback
AUTH0_LOGOUT_URL=http://localhost:3000

# Management API (for user creation/sync)
AUTH0_MANAGEMENT_CLIENT_ID=your_mgmt_client_id
AUTH0_MANAGEMENT_CLIENT_SECRET=your_mgmt_client_secret
```

## 10. Get Management API Credentials

For backend services to create/update users:

1. Navigate to **Applications** → **Applications**
2. Find **Auth0 Management API** (auto-created)
3. Go to **Machine to Machine Applications** tab
4. Authorize **Trading Bot Web App** with these scopes:
   - `read:users`
   - `update:users`
   - `create:users`
   - `read:roles`
   - `update:roles`
   - `read:user_idp_tokens`
5. Copy **Client ID** and **Client Secret**

## 11. Seed Default Plan (Optional)

Create the default `free_trial` plan in the database if it does not exist yet:

```bash
docker-compose up -d postgres

docker-compose exec postgres psql -U trading -d trading << 'EOF'
INSERT INTO plans (code, name, stripe_price_id, description, trial_period_days, active)
VALUES ('free_trial', 'Free Trial', NULL, '14-day free trial', 14, true)
ON CONFLICT (code) DO NOTHING;

INSERT INTO features (code, name, kind, description) VALUES
  ('can.use_strategies', 'Use Strategies', 'capability', 'Access to trading strategies'),
  ('can.use_alerts', 'Use Alerts', 'capability', 'Create and manage alerts'),
  ('quota.active_algos', 'Active Algorithms', 'quota', 'Max concurrent algorithms'),
  ('quota.api_calls_per_minute', 'API Rate Limit', 'quota', 'API calls per minute')
ON CONFLICT (code) DO NOTHING;

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

## 12. Run auth_gateway_service (Local)

```bash
docker-compose up -d postgres redis user_service
docker-compose build auth_gateway_service
docker-compose run --rm auth_gateway_service alembic upgrade head
docker-compose up -d auth_gateway_service
```

## 13. Validate Configuration

Use Auth0's **Try It** button in your application settings to test login flow.

### Health check

```bash
curl http://localhost:8012/health
```

### Session test (browser + curl)

```bash
# 1. Get login URL
curl -I http://localhost:8012/auth/login

# 2. Complete login in the browser and capture the session cookie

# 3. Verify session (replace SESSION_ID)
curl -b "trading_bot_session=SESSION_ID" \
  http://localhost:8012/auth/session

# 4. Fetch user info
curl -b "trading_bot_session=SESSION_ID" \
  http://localhost:8012/auth/user
```

## Validation Checklist

- [ ] Auth0 tenant created
- [ ] SPA application configured
- [ ] API created with correct audience
- [ ] Custom action deployed
- [ ] `config/.env.dev` updated
- [ ] Default plan created (optional)
- [ ] Service starts without errors
- [ ] Health check responds (http://localhost:8012/health)
- [ ] Login redirect works
- [ ] Session persists and validates
- [ ] User info returns correctly

---

## Environment Variables Summary

Add to `config/.env.dev`:

```bash
# ===== Auth0 Configuration =====
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_CLIENT_ID=abc123...
AUTH0_CLIENT_SECRET=xyz789...
AUTH0_AUDIENCE=https://api.trading-bot.dev
AUTH0_CALLBACK_URL=http://localhost:3000/auth/callback
AUTH0_LOGOUT_URL=http://localhost:3000
AUTH0_MANAGEMENT_CLIENT_ID=mgmt_client_id
AUTH0_MANAGEMENT_CLIENT_SECRET=mgmt_secret

# ===== Default Plan =====
DEFAULT_PLAN_CODE=free_trial
DEFAULT_PLAN_TRIAL_DAYS=14
```

---

## Next Steps

Once Auth0 is configured:
1. ✅ Run backend services with new Auth0 configuration
2. ✅ Test login flow through auth gateway service
3. ✅ Verify token validation and entitlements
4. ✅ Test social login providers
5. ✅ Create test users and assign roles

## Historical References

- `docs/domains/4_security/history/AUTH0_MIGRATION_STATUS.md`
- `docs/domains/4_security/history/PROJET_AUTH0_ETAT_COMPLET.md`

---

## Troubleshooting

### CORS Errors
- Ensure your URLs are added to **Allowed Origins (CORS)** in application settings
- Check that callback URLs match exactly (no trailing slashes)

### Token Validation Fails
- Verify `AUTH0_AUDIENCE` matches API identifier exactly
- Check `AUTH0_DOMAIN` format (should be `tenant.region.auth0.com`)

### Social Login Not Working
- Verify social connection is enabled
- Check callback URLs in social provider settings
- For dev: Use Auth0 Dev Keys first

### User Creation Fails
- Verify Management API credentials
- Check scopes are granted in Machine to Machine settings
- Ensure `email_verified` is set to true for programmatic user creation
