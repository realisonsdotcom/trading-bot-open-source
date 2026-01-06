# Platform Domain Documentation

> **Domain**: Core platform services - authentication, user management, billing, notifications, streaming, marketplace, and social features

**Keywords**: platform, services, auth, user-management, billing, notifications, streaming, marketplace, social, entitlements, Stripe, WebSocket

---

## Overview

The Platform domain encompasses all core platform services that provide foundational capabilities for the trading bot platform. This includes user authentication and management, billing and entitlements, multi-channel notifications, real-time streaming, strategy marketplace, and social features.

---

## Documentation Index

### Core Platform Services

#### [Auth Service](auth-service.md)

The **auth-service** issues JWTs, manages user credentials, and enforces entitlements on every request.

**Key Features**:
- JWT token generation and validation
- User credential management
- Entitlements enforcement
- CORS configuration for web frontends

**Configuration**:
- `AUTH_SERVICE_ALLOWED_ORIGINS` - CORS origins
- `AUTH_SERVICE_ALLOWED_METHODS` - HTTP methods
- `AUTH_SERVICE_ALLOWED_HEADERS` - Request headers
- `AUTH_SERVICE_ALLOW_CREDENTIALS` - Credentials policy

**Related Code**: `services/auth_service/`

---

#### [User Service](user-service.md)

The **User Service** centralizes application profiles and exposes a JWT-secured REST API with shared entitlements middleware.

**Key Features**:
- User registration and activation
- Profile management
- User preferences
- Entitlements integration

**API Endpoints**:
- `POST /users/register` - Register new user
- `POST /users/{user_id}/activate` - Activate account
- `PATCH /users/{user_id}` - Update profile
- `PUT /users/me/preferences` - Update preferences
- `GET /users/{user_id}` - Get user profile
- `GET /users` - List users (requires `can.manage_users`)

**Related Code**: `services/user_service/`

---

#### [Billing & Entitlements](billing.md)

The **billing-service** synchronizes Stripe Billing objects with the internal entitlements database and exposes a query API.

**Key Features**:
- Stripe integration
- Subscription management
- Entitlements synchronization
- FastAPI middleware for capability validation

**Configuration**:
- `STRIPE_API_KEY` - Stripe API key
- `STRIPE_WEBHOOK_SECRET` - Webhook signing secret

**Database Schema**: `infra/entitlements_models.py`

**Related Code**: `services/billing_service/`, `libs/entitlements/`

---

#### [Notification Service](notification-service.md)

The **Notification Service** supports multiple delivery channels (webhook, Slack, email, Telegram, SMS).

**Status**: Beta - All channels run in dry-run mode by default

**Supported Channels**:
- Webhook
- Slack
- Email (SMTP)
- Telegram
- SMS (Twilio)

**Configuration Variables**:
- `NOTIFICATION_SERVICE_HTTP_TIMEOUT` - HTTP request timeout
- `NOTIFICATION_SERVICE_SLACK_DEFAULT_WEBHOOK` - Slack webhook URL
- `NOTIFICATION_SERVICE_SMTP_HOST` - SMTP server
- `NOTIFICATION_SERVICE_TELEGRAM_BOT_TOKEN` - Telegram bot token
- `NOTIFICATION_SERVICE_TWILIO_ACCOUNT_SID` - Twilio account
- `NOTIFICATION_SERVICE_DRY_RUN` - Dry-run mode (default: `True`)

**Related Code**: `services/notification_service/`

---

#### [Streaming Service](streaming.md)

The **Streaming Module** provides real-time streaming for dashboards and business indicators.

**Status**: Streaming dashboards delivered, OBS/overlay automation in beta

**Key Components**:
- `streaming_gateway` - WebSocket gateway
- `overlay_renderer` - Overlay rendering
- `obs_controller` - OBS automation
- `streaming_bus` - Event bus

**Features**:
- WebSocket rooms (`/ws/rooms/{roomId}`)
- REST API for session management
- Real-time moderation
- Ingestion pipeline for reports and inplay
- OAuth and TradingView integrations

**Configuration**:
- `STREAMING_PIPELINE_BACKEND` - Backend (`memory`, `redis`, `nats`)
- `STREAMING_SERVICE_TOKEN_REPORTS` - Service token for reports
- `STREAMING_SERVICE_TOKEN_INPLAY` - Service token for inplay

**Related Code**: `services/streaming/`

---

#### [Marketplace Service](marketplace.md)

The **Marketplace Service** exposes APIs to publish algorithmic strategies and manage copy-trading subscriptions.

**Feature Status**:
- Listings publication & versioning: ✅ Beta (private)
- Copy-trading subscriptions: ✅ Beta
- Moderation & analytics: 🔜 Planned (Q1 2026)

**Key Features**:
- Strategy publication
- Version management
- Copy-trading subscriptions
- Stripe Connect integration for revenue sharing
- Audit trail

**Database Tables**:
- `marketplace_listings` - Published strategies
- `marketplace_versions` - Immutable payloads
- `marketplace_subscriptions` - Copy-trading subscriptions
- `audit_logs` - Event audit trail

**Entitlements**:
- `can.publish_strategy` - Required to publish listings
- `can.copy_trade` - Required to subscribe

**Related Code**: `services/marketplace_service/`

---

#### [Social Service](social.md)

The **Social Service** powers public profiles, follow relationships, activity feeds, and performance leaderboards.

**Key Features**:
- Public user profiles
- Follow/unfollow relationships
- Activity feeds
- Performance leaderboards
- Entitlements-based access control

**Database Tables**:
- `social_profiles` - Public profiles
- `social_follows` - Follow relationships
- `social_activities` - Activity feed entries
- `social_leaderboards` - Leaderboard snapshots
- `audit_logs` - Central audit trail

**Entitlements**:
- `can.publish_strategy` - Required for profile management and activities
- `can.copy_trade` - Required to follow profiles

**API Prefix**: `/social`

**Related Code**: `services/social_service/`

---

## Service Dependencies

```
auth-service
  └──> user-service (user registration)
  └──> entitlements (capability validation)

user-service
  └──> auth-service (JWT validation)
  └──> entitlements (middleware)

billing-service
  └──> Stripe API
  └──> entitlements (database)

notification-service
  └──> Slack/Email/Telegram/SMS APIs

streaming-service
  └──> reports-service (ingestion)
  └──> inplay-service (ingestion)
  └──> entitlements (can.stream_public)

marketplace-service
  └──> Stripe Connect
  └──> entitlements (can.publish_strategy, can.copy_trade)

social-service
  └──> entitlements (can.publish_strategy, can.copy_trade)
```

---

## Related Domains

- **[2_execution](../2_execution/INDEX.md)**: Order routing and execution
- **[1_trading](../1_trading/INDEX.md)**: Strategy execution and algo engine
- **[3_operations](../3_operations/INDEX.md)**: Deployment and operations

---

## Quick Links

| Document | Description |
|----------|-------------|
| [Auth Service](auth-service.md) | Authentication and JWT management |
| [User Service](user-service.md) | User profiles and management |
| [Billing & Entitlements](billing.md) | Stripe integration and entitlements |
| [Notification Service](notification-service.md) | Multi-channel notifications |
| [Streaming Service](streaming.md) | Real-time streaming and WebSocket |
| [Marketplace Service](marketplace.md) | Strategy marketplace and copy-trading |
| [Social Service](social.md) | Social features and leaderboards |

---

## Code References

- **Auth Service**: `services/auth_service/`
- **User Service**: `services/user_service/`
- **Billing Service**: `services/billing_service/`
- **Notification Service**: `services/notification_service/`
- **Streaming Service**: `services/streaming/`
- **Marketplace Service**: `services/marketplace_service/`
- **Social Service**: `services/social_service/`
- **Entitlements Library**: `libs/entitlements/`
- **Entitlements Models**: `infra/entitlements_models.py`

---

**Last Updated**: 2026-01-06  
**Domain**: 4_platform  
**Maintained By**: Trading Bot Team
