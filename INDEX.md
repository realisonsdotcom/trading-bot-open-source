# 📚 Trading Bot Documentation Index

> **Navigation Hub**: Central entry point for all project documentation

**Keywords**: documentation, index, navigation, architecture, services, guides, tutorials, AI-agent-friendly

---

## 🎯 Quick Navigation

| Role | Start Here |
|------|------------|
| **New User** | [Quick Start Guide](README.md#-quick-start) → [Demo Setup](docs/domains/3_operations/demo.md) |
| **Developer** | [Contributing Guide](CONTRIBUTING.md) → [Infrastructure Index](docs/domains/6_infrastructure/INDEX.md) |
| **DevOps** | [Operations](docs/domains/3_operations/INDEX.md) → [Observability](docs/domains/3_operations/observability/README.md) |
| **Trader** | [Trading Index](docs/domains/1_trading/INDEX.md) → [Screener](docs/domains/1_trading/screener.md) |
| **AI Agent** | [AI Navigation](#-ai-agent-navigation) below |

---

## 📋 Documentation Domains

### 🎯 Trading

**Description**: Strategy research, backtesting, and trading logic.

**Keywords**: trading, strategies, backtesting, algo-engine, screener, inplay, market-data

**Critical Documents**:
- [Algo Engine](docs/domains/1_trading/algo-engine.md) - Strategy execution engine
- [Algo-Order Contract](docs/domains/1_trading/algo-order-contract.md) - Strategy to execution payloads
- [Screener](docs/domains/1_trading/screener.md) - Market scanning workflows
- [InPlay](docs/domains/1_trading/inplay.md) - Live trading monitoring
- [Market Data](docs/domains/1_trading/market-data.md) - Data feeds and inputs
- [Strategies](docs/domains/1_trading/strategies/) - Strategy catalog & development notes

**Domain Index**: [docs/domains/1_trading/INDEX.md](docs/domains/1_trading/INDEX.md)

---

### ⚡ Execution

**Description**: Order routing, broker integration, and execution contracts.

**Keywords**: execution, order-router, brokers, risk-rules, algo-order, routing

**Critical Documents**:
- [Order Router](docs/domains/2_execution/order-router.md) - Order routing service
- [Algo-Order Contract](docs/domains/2_execution/algo-order-contract.md) - Execution contract spec

**Domain Index**: [docs/domains/2_execution/INDEX.md](docs/domains/2_execution/INDEX.md)

---

### 📈 Operations

**Description**: Deployment workflows, observability, metrics, and operational runbooks.

**Keywords**: operations, deployment, observability, metrics, alerting, demo, sandbox

**Critical Documents**:
- [Demo Setup](docs/domains/3_operations/demo.md) - End-to-end demo environment
- [MVP Sandbox Flow](docs/domains/3_operations/mvp-sandbox-flow.md) - Sandbox validation
- [Observability Stack](docs/domains/3_operations/observability/README.md) - Logs, traces, dashboards
- [Alerting Runbook](docs/domains/3_operations/operations/alerting.md) - Notifications & incident flow
- [Metrics Overview](docs/domains/3_operations/metrics/README.md) - KPI reporting

**Domain Index**: [docs/domains/3_operations/INDEX.md](docs/domains/3_operations/INDEX.md)

---

### 🏢 Platform

**Description**: Authentication, user management, billing, and shared platform services.

**Keywords**: platform, auth, users, billing, marketplace, notifications, streaming, social

**Critical Documents**:
- [Auth Service](docs/domains/4_platform/auth-service.md) - Authentication & sessions
- [User Service](docs/domains/4_platform/user-service.md) - Accounts & profiles
- [Billing](docs/domains/4_platform/billing.md) - Subscriptions & payments
- [Marketplace](docs/domains/4_platform/marketplace.md) - Strategy listings
- [Notification Service](docs/domains/4_platform/notification-service.md) - Alerts delivery
- [Streaming Service](docs/domains/4_platform/streaming.md) - Real-time updates
- [Social Features](docs/domains/4_platform/social.md) - Social & collaboration

**Domain Index**: [docs/domains/4_platform/INDEX.md](docs/domains/4_platform/INDEX.md)

---

### 🎨 WebApp

**Description**: Web dashboard UI, SPA architecture, and design system guidance.

**Keywords**: webapp, ui, dashboard, spa, design-system, frontend

**Critical Documents**:
- [UI Design System](docs/domains/5_webapp/ui/README.md) - Tokens & layout guidelines
- [Dashboard SPA Overview](docs/domains/5_webapp/ui/web-dashboard-spa-overview.md) - Shell architecture
- [Dashboard Data Contracts](docs/domains/5_webapp/ui/dashboard-data-contracts.md) - Frontend payloads
- [Dashboard Modernization](docs/domains/5_webapp/ui/dashboard-modernization.md) - Upgrade roadmap

**Domain Index**: [docs/domains/5_webapp/INDEX.md](docs/domains/5_webapp/INDEX.md)

---

### 🏗️ Infrastructure

**Description**: Docker, migrations, and infrastructure configuration.

**Keywords**: infrastructure, docker, migrations, timescaledb, redis, prometheus, grafana

**Critical Documents**:
- [Infrastructure Index](docs/domains/6_infrastructure/INDEX.md) - Full infra reference
- [Docker Compose](docker-compose.yml) - Core service orchestration
- [Migration Config](infra/migrations/alembic.ini) - Alembic setup
- [Migrations](infra/migrations/) - Database schema history
- [Prometheus Config](infra/prometheus/prometheus.yml) - Metrics scrape rules
- [Grafana Provisioning](infra/grafana/provisioning/) - Dashboards & datasources

**Domain Index**: [docs/domains/6_infrastructure/INDEX.md](docs/domains/6_infrastructure/INDEX.md)

---

### ✅ Standards & Quality

**Description**: Engineering standards, quality baselines, and backlog tracking.

**Keywords**: standards, quality, codex, evaluation, roadmap, backlog

**Critical Documents**:
- [Engineering Codex](docs/domains/7_standards/codex.md) - Standards & conventions
- [Project Evaluation](docs/domains/7_standards/project-evaluation.md) - Quality assessment
- [Standards Roadmap](docs/domains/7_standards/roadmap.md) - Standards planning
- [Standards Backlog](docs/domains/7_standards/tasks/2025-q4-backlog.md) - Open actions

**Domain Index**: [docs/domains/7_standards/](docs/domains/7_standards/)

---

### 🧭 Supporting Domains (indexes pending)

**Description**: Supporting topics awaiting dedicated indexes.

**Keywords**: architecture, security, community, quality

- [Architecture](docs/domains/2_architecture/)
- [Security](docs/domains/4_security/)
- [Community](docs/domains/5_community/)
- [Quality](docs/domains/6_quality/)

---

## 🤖 AI Agent Navigation

**Purpose**: This section helps AI coding assistants (GitHub Copilot, Cursor, Claude Code, etc.) quickly understand the codebase structure and locate relevant documentation.

### Quick Orientation

**Project Type**: Python/FastAPI microservices trading bot with Docker orchestration

**Tech Stack**:
- **Backend**: Python 3.12, FastAPI, SQLAlchemy, PostgreSQL, Redis, RabbitMQ
- **Infrastructure**: Docker, docker-compose, Makefile
- **Testing**: pytest, coverage, pre-commit hooks
- **CI/CD**: GitHub Actions
- **Frontend**: React (SPA) - see [WebApp docs](docs/domains/5_webapp/INDEX.md)

### Common AI Agent Tasks

| Task | Documentation Path | Keywords |
|------|-------------------|----------|
| **Add new service** | [Infrastructure Index](docs/domains/6_infrastructure/INDEX.md) | microservices, FastAPI, Docker |
| **Modify trading logic** | [Trading Index](docs/domains/1_trading/INDEX.md) | algo-engine, backtesting, orders |
| **Fix authentication** | [Auth Service](docs/domains/4_platform/auth-service.md) | auth, tokens, sessions |
| **Add monitoring** | [Observability Stack](docs/domains/3_operations/observability/README.md) | metrics, Prometheus, Grafana |
| **Deploy changes** | [Operations Index](docs/domains/3_operations/INDEX.md) | Docker, deployment, CI/CD |
| **Write tests** | [Engineering Codex](docs/domains/7_standards/codex.md) | pytest, coverage, QA |
| **Update UI** | [WebApp Index](docs/domains/5_webapp/INDEX.md) | React, dashboard, SPA |

### File Location Patterns

```
services/           # Each service is a FastAPI app (auth, algo_engine, etc.)
├── {service}/
│   ├── app/
│   │   ├── main.py         # FastAPI app entrypoint
│   │   ├── api/            # API routes
│   │   ├── models/         # SQLAlchemy models
│   │   ├── services/       # Business logic
│   │   └── tests/          # Service-specific tests
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Service container

infra/              # Database, migrations, shared infrastructure
libs/               # Shared Python libraries
scripts/            # Automation & deployment scripts
docs/               # Domain-specific documentation
tests/              # Integration & end-to-end tests
```

### Key Configuration Files

- **`.env.dev`**: Docker-based development environment variables
- **`.env.native`**: Host-based (localhost) development environment variables
- **`docker-compose.yml`**: Main service orchestration
- **`Makefile`**: Common development commands (`make dev-up`, `make test`, etc.)
- **`pyproject.toml`**: Python project metadata & dependencies
- **`.pre-commit-config.yaml`**: Code quality automation (black, mypy, bandit, etc.)

### When to Update Documentation

- **New service**: Update the relevant domain index under `docs/domains/*/INDEX.md`
- **New feature**: Update [Feature Overview](README.md#-feature-overview) and the matching domain index
- **Breaking change**: Update [Changelog](CHANGELOG.md) and affected service docs
- **API change**: Update service doc and [Dashboard Data Contracts](docs/domains/5_webapp/ui/dashboard-data-contracts.md) if applicable
- **Configuration change**: Update [Quick Start](README.md#-quick-start) or [Operations Index](docs/domains/3_operations/INDEX.md)

### Code Quality Standards

- **Python**: Black formatting (120 cols), mypy strict typing, pytest ≥80% coverage
- **Pre-commit**: Run `pre-commit install` before first commit
- **Testing**: Always write tests for new features (see [Testing](#-testing--quality))
- **Documentation**: Update relevant docs in same PR as code changes

---

## 📖 Additional Resources

- **Main README**: [README.md](README.md) - Project overview & quick start
- **French README**: [README.fr.md](README.fr.md) - Documentation en français
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- **License**: [LICENSE](LICENSE) - Project license
- **Changelog**: [CHANGELOG.md](CHANGELOG.md) - Version history

---

**Last Updated**: 2026-01-06  
**Maintained By**: Trading Bot Community  
**Questions?** Open an issue or check [FAQ](docs/help/faq/)
