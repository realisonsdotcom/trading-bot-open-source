---
domain: 7_standards
title: Trading Bot MVP - Next Steps
description: Post-MVP priorities and follow-up tasks.
keywords: mvp, next-steps, planning, standards, archived
last_updated: 2026-01-06
status: deprecated
archived_reason: "Migrated from root after documentation restructuring"
---

# Trading Bot MVP - Next Steps

## Current Status

### ✅ Completed Setup

#### Infrastructure
- **PostgreSQL** (TimescaleDB): Running on port 5432
- **Redis**: Running on port 6379
- **Database Migrations**: 18 migrations successfully applied
- **Docker Environment**: WSL2 integration enabled

#### Services Running
- **auth_service**: Port 8011 (Healthy)
  - Swagger UI: http://localhost:8011/docs
  - Endpoints: /auth/register, /auth/login, /auth/refresh, /auth/me, /auth/totp/*

- **user_service**: Port 8001 (Healthy)
  - Health check working
  - Requires authentication headers for non-health endpoints

#### Database Schema
20 tables created:
- Authentication: `users`, `roles`, `user_roles`, `mfa_totp`
- User Management: `user_preferences`, `user_broker_credentials`
- Trading: `trading_orders`, `trading_executions`
- Market Data: `market_data_ohlcv`, `market_data_ticks`
- Strategies: `strategies`, `strategy_versions`, `strategy_executions`, `strategy_backtests`
- Screening: `screener_presets`, `screener_results`, `screener_snapshots`
- Reports: `report_jobs`, `report_backtests`

---

## Next Steps to Complete MVP

### Phase 1: Fix Migration Configuration Issues

#### Issue #1: RUN_MIGRATIONS Flag
**Problem**: Services skip migrations via `RUN_MIGRATIONS=0` environment variable

**Files Modified**:
- `infra/docker-compose.yml:78` - auth_service
- `infra/docker-compose.yml:105` - user_service

**Resolution Options**:
1. **Keep as-is** (Recommended for MVP): Run migrations separately before starting services
2. **Remove flag**: Allow services to run migrations on startup (requires fixing Docker path issues)

#### Issue #2: TimescaleDB Dependencies Removed
**Files Modified**:
- `infra/migrations/versions/0002_market_data.py:17-18,36-39`
- `infra/migrations/versions/a1b8c9d0e1f2_market_data_composite_pk.py:70-79`

**Impact**: TimescaleDB hypertables not created (acceptable for MVP, may affect performance at scale)

**Future Enhancement**:
```bash
# To enable TimescaleDB in production:
docker exec trading-bot-open-source-postgres-1 psql -U trading -d trading -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
# Then uncomment TimescaleDB sections in migration files
```

#### Issue #3: Migration Branch Conflict Resolution
**File Modified**: `infra/migrations/versions/8f7b4a1e5b6c_add_report_jobs_table.py:10-24`

**Fix Applied**: Added enum existence check to prevent duplicate creation errors

---

### Phase 2: Start Additional MVP Services

#### Services to Start

```bash
# Start core trading services
docker compose --project-directory . -f infra/docker-compose.yml up -d billing_service algo_engine order_router

# Start market data service
docker compose --project-directory . -f infra/docker-compose.yml up -d market_data

# Start streaming services
docker compose --project-directory . -f infra/docker-compose.yml up -d streaming streaming_gateway

# Optional: Start web dashboard
docker compose --project-directory . -f infra/docker-compose.yml up -d web_dashboard
```

#### Expected Service Ports
| Service | Port | Purpose |
|---------|------|---------|
| billing_service | 8013 | Subscription & billing management |
| algo_engine | 8014 | Trading algorithm execution |
| order_router | 8015 | Order routing & execution |
| market_data | 8016 | Market data ingestion |
| streaming | 8017 | Real-time data streaming |
| streaming_gateway | 8018 | WebSocket gateway |
| web_dashboard | 8022 | Frontend UI |

#### Dependency Requirements

Each service may require additional Python dependencies. Check:
```bash
# Review service-specific requirements
cat services/billing_service/requirements.txt
cat services/algo_engine/requirements.txt
cat services/order_router/requirements.txt
cat services/market_data/requirements.txt
```

#### Common Issues to Watch For

1. **Missing Python Dependencies**:
   - `httpx` (added to auth_service and user_service)
   - `email-validator` (added via pydantic[email])
   - May need to add similar dependencies to other services

2. **Docker Build Context**:
   - Services need `services/__init__.py` and `services/_bootstrap.py`
   - Already fixed for auth_service and user_service
   - May need similar fixes for other services

3. **Database Connection**:
   - Ensure services use `postgres` hostname (not `localhost`) in containers
   - Connection string: `postgresql+psycopg2://trading:trading@postgres:5432/trading`

---

### Phase 3: Service Configuration & Dependencies

#### Common Dockerfile Pattern

Services should include:
```dockerfile
COPY services/__init__.py ./services/__init__.py
COPY services/_bootstrap.py ./services/_bootstrap.py
COPY httpx  # If using libs/entitlements
```

#### Environment Variables

Review and set in `config/.env.dev`:
```bash
# Core Settings
ENVIRONMENT=dev
DATABASE_URL=postgresql+psycopg2://trading:trading@postgres:5432/trading
REDIS_URL=redis://redis:6379/0

# Service URLs (for inter-service communication)
AUTH_SERVICE_URL=http://auth_service:8000
USER_SERVICE_URL=http://user_service:8000
BILLING_SERVICE_URL=http://billing_service:8000
ALGO_ENGINE_URL=http://algo_engine:8000
ORDER_ROUTER_URL=http://order_router:8000
MARKET_DATA_URL=http://market_data:8000

# External Services (if needed)
# EXCHANGE_API_KEY=your_key_here
# EXCHANGE_API_SECRET=your_secret_here
```

---

### Phase 4: Testing & Validation

#### 1. Service Health Checks

```bash
# Check all services are healthy
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Test individual health endpoints
curl http://localhost:8011/health  # auth_service
curl http://localhost:8001/health  # user_service
curl http://localhost:8013/health  # billing_service
curl http://localhost:8014/health  # algo_engine
curl http://localhost:8015/health  # order_router
```

#### 2. Authentication Flow Test

```bash
# 1. Register a user
curl -X POST http://localhost:8011/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "trader@example.com",
    "password": "SecurePass123!",
    "full_name": "Test Trader"
  }'

# 2. Login
curl -X POST http://localhost:8011/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "trader@example.com",
    "password": "SecurePass123!"
  }' | jq .

# Save the access_token from response for authenticated requests
```

#### 3. Run Bootstrap Demo Script

Once more services are running:
```bash
# Bootstrap demo data
python3 scripts/dev/bootstrap_demo.py BTCUSDT 0.25 --order-type market

# This should:
# - Create a demo user
# - Set up sample trading orders
# - Initialize market data
# - Create test strategies
```

#### 4. Database Verification

```bash
# Check data was created
PGPASSWORD=trading psql -h localhost -U trading -d trading

# In psql:
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM trading_orders;
SELECT COUNT(*) FROM strategies;
```

---

### Phase 5: Common Issues & Troubleshooting

#### Issue: Service Won't Start

**Check Logs**:
```bash
docker logs <service-container-name> --tail 50
```

**Common Causes**:
1. Missing Python dependency → Add to requirements.txt, rebuild
2. Database connection failure → Check DATABASE_URL environment variable
3. Port conflict → Check if port is already in use: `netstat -tlnp | grep <port>`

#### Issue: Authentication Fails

**Verify**:
1. auth_service is running and healthy
2. User exists in database: `SELECT * FROM users WHERE email='trader@example.com';`
3. Token is valid and not expired

#### Issue: Inter-Service Communication Fails

**Check**:
1. Services using correct hostnames (`auth_service`, not `localhost`)
2. Services are on same Docker network: `docker network inspect trading-bot-open-source_default`
3. Firewall/security groups not blocking internal traffic

#### Issue: Migration Failures

**Reset Database** (if needed):
```bash
# Drop and recreate
PGPASSWORD=trading psql -h localhost -U trading -d postgres -c "DROP DATABASE IF EXISTS trading;"
PGPASSWORD=trading psql -h localhost -U trading -d postgres -c "CREATE DATABASE trading;"

# Re-run migrations
ALEMBIC_DATABASE_URL=postgresql+psycopg2://trading:trading@localhost:5432/trading \
  python3 -m alembic -c infra/migrations/alembic.ini upgrade head
```

---

### Phase 6: MVP Feature Validation

#### Core Features to Test

1. **User Management**
   - [ ] User registration
   - [ ] User login/logout
   - [ ] Password management
   - [ ] MFA/TOTP setup

2. **Trading Operations**
   - [ ] Create market order
   - [ ] Create limit order
   - [ ] View order status
   - [ ] View execution history

3. **Market Data**
   - [ ] Fetch OHLCV data
   - [ ] Real-time tick data
   - [ ] Symbol lookup

4. **Strategy Management**
   - [ ] Create strategy
   - [ ] Backtest strategy
   - [ ] Deploy strategy
   - [ ] View strategy performance

5. **Screening & Alerts**
   - [ ] Create screener preset
   - [ ] Run screener
   - [ ] Set up alerts
   - [ ] Receive notifications

6. **Reports**
   - [ ] Generate trade report
   - [ ] Generate backtest report
   - [ ] Export reports

---

### Phase 7: Performance & Optimization

#### Database Optimization

```sql
-- Add missing indexes if needed
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_trading_orders_user_id
  ON trading_orders(user_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_trading_orders_status
  ON trading_orders(status);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_market_data_ohlcv_symbol_timestamp
  ON market_data_ohlcv(symbol, timestamp DESC);
```

#### Docker Optimization

```yaml
# Add resource limits in infra/docker-compose.yml
services:
  postgres:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

---

## MVP Completion Checklist

### Infrastructure
- [x] PostgreSQL running
- [x] Redis running
- [x] Docker network configured
- [x] Database migrations applied

### Core Services
- [x] auth_service running
- [x] user_service running
- [ ] billing_service running
- [ ] algo_engine running
- [ ] order_router running
- [ ] market_data running
- [ ] streaming services running
- [ ] web_dashboard running

### Configuration
- [x] Database schema created
- [x] Environment variables configured
- [ ] Service discovery working
- [ ] Inter-service authentication

### Testing
- [ ] Health checks passing for all services
- [ ] Authentication flow working
- [ ] Sample orders can be created
- [ ] Market data ingestion working
- [ ] Strategy execution working
- [ ] Web dashboard accessible

### Documentation
- [x] Setup documentation
- [ ] API documentation review
- [ ] User guide for testing
- [ ] Known issues documented

---

## Quick Commands Reference

### Start All MVP Services
```bash
docker compose --project-directory . -f infra/docker-compose.yml up -d postgres redis
docker compose --project-directory . -f infra/docker-compose.yml up -d auth_service user_service billing_service
docker compose --project-directory . -f infra/docker-compose.yml up -d algo_engine order_router market_data
docker compose --project-directory . -f infra/docker-compose.yml up -d streaming streaming_gateway
docker compose --project-directory . -f infra/docker-compose.yml up -d web_dashboard
```

### View All Logs
```bash
docker compose --project-directory . -f infra/docker-compose.yml logs -f --tail=100
```

### Restart a Service
```bash
docker compose --project-directory . -f infra/docker-compose.yml restart <service_name>
```

### Rebuild a Service
```bash
docker compose --project-directory . -f infra/docker-compose.yml up -d --build <service_name>
```

### Check Service Health
```bash
# All services
for port in 8011 8012 8013 8014 8015 8016 8017 8018; do
  echo "Port $port: $(curl -s http://localhost:$port/health || echo 'FAILED')"
done
```

### Access Database
```bash
PGPASSWORD=trading psql -h localhost -U trading -d trading
```

### Access Redis
```bash
docker exec -it trading-bot-open-source-redis-1 redis-cli
```

---

## Support & Resources

### Project Structure
```
trading-bot-open-source/
├── services/           # Microservices (22 services)
├── libs/              # Shared libraries
├── infra/             # Infrastructure (migrations, docker)
├── scripts/           # Development scripts
├── libs/schemas/      # Shared data schemas
└── docs/              # Documentation
```

### Key Files
- `infra/docker-compose.yml` - Service orchestration
- `config/.env.dev` - Development environment config
- `Makefile` - Build & deployment commands
- `infra/migrations/` - Database schema versions

### Getting Help
- Check service logs: `docker compose --project-directory . -f infra/docker-compose.yml logs <service>`
- Review API docs: `http://localhost:<port>/docs`
- Inspect database: `psql -h localhost -U trading -d trading`

---

**Last Updated**: 2025-11-11
**MVP Status**: Core services running, additional services pending startup
**Next Action**: Start remaining services and run integration tests
