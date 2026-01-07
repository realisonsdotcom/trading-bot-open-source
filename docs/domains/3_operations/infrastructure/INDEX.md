---
domain: 3_operations
title: Infrastructure Domain Documentation
description: Infrastructure setup, Docker configuration, database migrations, and infrastructure as code.
keywords: infrastructure, docker, migrations, operations, index
last_updated: 2026-01-07
---

# Infrastructure Domain Documentation

> **Domain**: Infrastructure setup, Docker configuration, database migrations, and infrastructure as code

**Keywords**: infrastructure, docker, docker-compose, postgresql, timescaledb, redis, migrations, alembic, prometheus, grafana, monitoring

---

## Overview

The Infrastructure domain covers all aspects of the technical infrastructure that supports the trading bot platform. This includes Docker containerization, database setup and migrations, monitoring infrastructure, and infrastructure configuration files.

---

## Documentation Index

### Infrastructure Components

#### Docker & Containerization

**Configuration Files**:
- `infra/docker-compose.yml` - Main Docker Compose configuration
- `infra/docker-compose.codespaces.yml` - Codespaces-specific configuration
- `infra/docker-compose.override.yml` - Local override configuration
- `.dockerignore` - Docker ignore patterns
- `infra/docker/fastapi-service.Dockerfile` - Base Dockerfile for FastAPI services

**Services Defined**:
- PostgreSQL/TimescaleDB - Database service
- Redis - Caching and message broker
- Prometheus - Metrics collection
- Grafana - Metrics visualization
- All microservices (auth_service, user_service, billing_service, etc.)

**Related Documentation**:
- See [Operations Domain](../INDEX.md) for deployment guides
- See [README.md](../../../../README.md#-quick-start) for quick start instructions

---

#### Database Infrastructure

**Database**: PostgreSQL with TimescaleDB extension

**Configuration**:
- Database: `trading`
- User: `trading`
- Port: `5432`
- Image: `timescale/timescaledb:2.14.2-pg14`

**Migrations**:
- Location: `infra/migrations/`
- Tool: Alembic
- Config: `infra/migrations/alembic.ini`
- Migration files: `infra/migrations/versions/`

**Key Migration Files**:
- `0001_init.py` - Initial schema
- `0002_market_data.py` - Market data tables
- `0003_screener.py` - Screener tables
- `0004_auth_user_timestamps.py` - Auth timestamps
- `0005_user_profile_fields.py` - User profile fields
- Additional migrations for strategies, orders, reports, etc.

**Database Models**:
- `infra/audit_models.py` - Audit trail models
- `infra/entitlements_models.py` - Entitlements models
- `infra/marketplace_models.py` - Marketplace models
- `infra/screener_models.py` - Screener models
- `infra/social_models.py` - Social models
- `infra/strategy_models.py` - Strategy models
- `infra/trading_models.py` - Trading models

**Migration Commands**:
```bash
# Run migrations
make migrate-up

# Generate new migration
make migrate-generate REVISION=<revision_name>

# Rollback migration
make migrate-down DOWN_REVISION=-1
```

---

#### Redis Infrastructure

**Configuration**:
- Image: `redis:7`
- Port: `6379`
- Used for: Caching and message broker

**Health Check**: `redis-cli ping`

---

#### Monitoring Infrastructure

**Prometheus**:
- Configuration: `infra/prometheus/prometheus.yml`
- Alert Rules: `infra/prometheus/alert_rules.yml`
- Port: `9090` (default)

**Grafana**:
- Configuration: `infra/grafana/provisioning/`
- Dashboards: `infra/grafana/provisioning/dashboards/`
- Datasources: `infra/grafana/provisioning/datasources/`
- Pre-configured dashboards:
  - `trading-bot-overview.json` - Main platform overview

**Related Documentation**:
- See [Observability Domain](../observability/README.md) for monitoring setup
- See [Metrics Domain](../metrics/README.md) for custom metrics

---

## Infrastructure as Code

### Docker Compose Structure

The platform uses Docker Compose for orchestration:

```yaml
services:
  postgres:      # TimescaleDB database
  redis:         # Cache and message broker
  db_migrations: # Database migration runner
  prometheus:    # Metrics collection
  grafana:       # Metrics visualization
  # ... microservices
```

### Environment Configuration

**Development Environment**:
- `config/.env.dev` - Docker-based development variables
- `config/.env.native` - Host-based (localhost) development variables

**Key Variables**:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `ENVIRONMENT` - Environment type (`docker` or `native`)

---

## Development Workflows

### Docker-based Development

```bash
# Start infrastructure (postgres, redis)
make dev-up

# Start full demo stack
make demo-up

# Stop all services
make dev-down
```

### Native Development

```bash
# Use native host services
export $(cat config/.env.native | grep -v '^#' | xargs)
export ENVIRONMENT=native

# Run migrations
scripts/run_migrations.sh
```

---

## Infrastructure Files Reference

### Root Level
- `infra/docker-compose.yml` - Main compose file
- `Makefile` - Infrastructure automation commands
- `.dockerignore` - Docker build exclusions

### `infra/` Directory
- `infra/docker/` - Docker configuration files
- `infra/migrations/` - Database migrations (Alembic)
- `infra/prometheus/` - Prometheus configuration
- `infra/grafana/` - Grafana provisioning
- `infra/*_models.py` - SQLAlchemy models

---

## Related Domains

- **[3_operations](../INDEX.md)**: Deployment guides and operational procedures
- **[Platform](../../2_architecture/platform/INDEX.md)**: Platform services that use this infrastructure
- **[1_trading](../../1_trading/INDEX.md)**: Trading services infrastructure

---

## Quick Links

| Topic | Location |
|-------|----------|
| Docker Compose | `infra/docker-compose.yml` |
| Database Migrations | `infra/migrations/` |
| Prometheus Config | `infra/prometheus/prometheus.yml` |
| Grafana Dashboards | `infra/grafana/provisioning/dashboards/` |
| Database Models | `infra/*_models.py` |
| Makefile Commands | `Makefile` |
| Docs CI Workflow | `docs/domains/3_operations/cicd-pipeline.md` |

---

## Gaps & Future Work

**Missing Documentation**:
- Infrastructure architecture diagram
- Production deployment infrastructure guide
- Infrastructure scaling guidelines
- Infrastructure as Code (IaC) documentation (Terraform/Ansible)
- Disaster recovery procedures
- Infrastructure monitoring best practices

**Planned Improvements**:
- Infrastructure provisioning automation
- Multi-environment infrastructure (dev/staging/prod)
- Infrastructure cost optimization guide
- Infrastructure security hardening guide

---

**Last Updated**: 2026-01-06  
**Domain**: 3_operations  
**Maintained By**: Trading Bot Team
