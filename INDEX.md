# 📚 Trading Bot Documentation Index

> **Navigation Hub**: Central entry point for all project documentation

**Keywords**: documentation, index, navigation, architecture, services, guides, tutorials, AI-agent-friendly

---

## 🎯 Quick Navigation

| Role | Start Here |
|------|------------|
| **New User** | [Quick Start Guide](README.md#-quick-start) → [Demo Setup](docs/DEMO.md) |
| **Developer** | [Contributing Guide](CONTRIBUTING.md) → [Architecture](#-architecture--services) |
| **DevOps** | [Operations](#-operations--deployment) → [Observability](#-observability--monitoring) |
| **Trader** | [Strategies](#-strategies--trading) → [Risk Management](#-risk--compliance) |
| **AI Agent** | [AI Navigation](#-ai-agent-navigation) below |

---

## 📋 Documentation Domains

### 🏗️ Architecture & Services

**Description**: System design, microservices architecture, and core service documentation.

**Keywords**: architecture, microservices, services, backend, API, FastAPI, Docker, PostgreSQL, Redis

**Critical Documents**:
- [Project Structure](README.md#project-structure) - Overview of repository layout
- [Auth Service](docs/auth-service.md) - Authentication & authorization (Auth0)
- [User Service](docs/user-service.md) - User management & profiles
- [Algo Engine](docs/algo-engine.md) - Strategy execution engine
- [Order Router](docs/order-router.md) - Order management & routing
- [Market Data](docs/market-data.md) - Real-time & historical data feeds
- [Billing Service](docs/billing.md) - Subscription & payment processing
- [Notification Service](docs/notification-service.md) - Multi-channel alerts
- [Streaming Service](docs/streaming.md) - WebSocket & real-time data

**Domain Index**: [docs/architecture/INDEX.md](docs/architecture/INDEX.md) _(placeholder)_

---

### 📊 Strategies & Trading

**Description**: Trading strategy development, backtesting, research tools, and execution.

**Keywords**: strategies, trading, backtesting, algo, automation, visual-designer, AI-assistant, market-connectors

**Critical Documents**:
- [Feature Overview](README.md#-feature-overview) - Strategies & research domain status
- [Algo Engine](docs/algo-engine.md) - Strategy execution & management
- [Algo-Order Contract](docs/algo-order-contract.md) - Strategy-order integration spec
- [Screener](docs/screener.md) - Market scanning & opportunity detection
- [InPlay Service](docs/inplay.md) - Live trading monitoring

**Domain Index**: [docs/strategies/INDEX.md](docs/strategies/INDEX.md) _(placeholder)_

---

### 🔐 Security & Compliance

**Description**: Authentication, authorization, security best practices, and compliance documentation.

**Keywords**: security, auth, Auth0, compliance, secrets, encryption, RBAC, audit

**Critical Documents**:
- [Auth0 Setup](docs/AUTH0_SETUP.md) - Authentication configuration
- [Auth Service](docs/auth-service.md) - Security architecture
- [Secrets Management](.secrets.baseline) - Baseline secrets detection
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community standards

**Domain Index**: [docs/security/INDEX.md](docs/security/INDEX.md) _(placeholder)_

---

### 📈 Observability & Monitoring

**Description**: Logging, metrics, tracing, dashboards, and system health monitoring.

**Keywords**: observability, monitoring, metrics, logs, traces, Prometheus, Grafana, alerts, SRE

**Critical Documents**:
- [Observability Overview](docs/observability/README.md) - Monitoring stack setup
- [Dashboards](docs/observability/dashboards/) - Grafana dashboard configs
- [Metrics](docs/metrics/) - Custom metrics & KPIs

**Domain Index**: [docs/observability/INDEX.md](docs/observability/INDEX.md) _(placeholder)_

---

### 🚀 Operations & Deployment

**Description**: Deployment guides, infrastructure setup, CI/CD, and operational procedures.

**Keywords**: deployment, DevOps, CI/CD, Docker, docker-compose, infrastructure, operations, maintenance

**Critical Documents**:
- [Quick Start](README.md#-quick-start) - Development environment setup
- [Demo Guide](docs/DEMO.md) - Complete demo environment
- [Native Development](README.md#native-host-development) - Host-based setup
- [Operations Docs](docs/operations/) - Operational procedures
- [Makefile](Makefile) - Common development & deployment tasks

**Domain Index**: [docs/operations/INDEX.md](docs/operations/INDEX.md) _(placeholder)_

---

### 🎓 Tutorials & Guides

**Description**: Step-by-step tutorials, how-to guides, and learning resources.

**Keywords**: tutorials, guides, learning, examples, how-to, getting-started, onboarding

**Critical Documents**:
- [Getting Started Guide](docs/help/guides/getting-started.md) - First steps
- [Tutorials](docs/tutorials/) - Step-by-step walkthroughs
- [FAQ](docs/help/faq/) - Frequently asked questions
- [Webinars](docs/help/webinars/) - Video tutorials & recordings
- [Notebooks](docs/help/notebooks/) - Jupyter notebook examples

**Domain Index**: [docs/tutorials/INDEX.md](docs/tutorials/INDEX.md) _(placeholder)_

---

### 🛡️ Risk & Compliance

**Description**: Risk management, position sizing, drawdown controls, and regulatory compliance.

**Keywords**: risk, compliance, position-sizing, drawdown, limits, controls, regulation

**Critical Documents**:
- [Risk Checklist](docs/help/notebooks/risk-checklist.md) - Risk management guidelines
- [Risk Docs](docs/risk/) - Risk management documentation
- [Billing](docs/billing.md) - Financial compliance & billing

**Domain Index**: [docs/risk/INDEX.md](docs/risk/INDEX.md) _(placeholder)_

---

### 💬 Community & Governance

**Description**: Community resources, contribution guidelines, governance, and communication.

**Keywords**: community, governance, contributions, pull-requests, issues, releases, communications

**Critical Documents**:
- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community standards
- [Changelog](CHANGELOG.md) - Release history
- [Roadmap](docs/ROADMAP.md) - Future plans
- [Release Highlights](docs/release-highlights/) - Feature announcements
- [Communications](docs/communications/) - Project updates
- [Community Docs](docs/community/) - Community resources
- [AMA Notes](docs/community/ama-notes/) - Ask-me-anything sessions
- [Governance](docs/governance/) - Project governance

**Domain Index**: [docs/community/INDEX.md](docs/community/INDEX.md) _(placeholder)_

---

### 🎨 User Interface

**Description**: Frontend documentation, UI/UX guidelines, and dashboard specifications.

**Keywords**: UI, frontend, dashboard, SPA, web, React, components, design-system

**Critical Documents**:
- [UI Overview](docs/ui/README.md) - Frontend architecture
- [Dashboard Overview](docs/ui/web-dashboard-spa-overview.md) - Web dashboard specs
- [Dashboard Data Contracts](docs/ui/dashboard-data-contracts.md) - API contracts
- [Dashboard Modernization](docs/ui/dashboard-modernization.md) - UI upgrade plan

**Domain Index**: [docs/ui/INDEX.md](docs/ui/INDEX.md) _(placeholder)_

---

### 🏪 Marketplace & Social

**Description**: Marketplace features, social trading, copy-trading, and strategy sharing.

**Keywords**: marketplace, social-trading, copy-trading, subscriptions, listings, Stripe, monetization

**Critical Documents**:
- [Marketplace](docs/marketplace.md) - Strategy marketplace & listings
- [Social Features](docs/social.md) - Social trading & collaboration
- [Billing](docs/billing.md) - Subscription & payment processing

**Domain Index**: [docs/marketplace/INDEX.md](docs/marketplace/INDEX.md) _(placeholder)_

---

### 📋 Project Management

**Description**: Project planning, task tracking, sprint reports, and project status.

**Keywords**: project-management, tasks, sprints, milestones, planning, tracking, status

**Critical Documents**:
- [MVP Checklist](MVP_CHECKLIST.md) - MVP completion status
- [MVP Next Steps](MVP_NEXT_STEPS.md) - Post-MVP roadmap
- [Release Highlights 2025-12](docs/release-highlights/2025-12.md) - December 2025 milestones
- [Tasks](docs/tasks/) - Task tracking & planning
- [Project Evaluation](docs/project-evaluation.md) - Project assessment

**Domain Index**: [docs/tasks/INDEX.md](docs/tasks/INDEX.md) _(placeholder)_

---

### 🧪 Testing & Quality

**Description**: Testing strategies, quality assurance, test automation, and coverage reports.

**Keywords**: testing, QA, pytest, coverage, CI, quality, test-automation, unit-tests, integration-tests

**Critical Documents**:
- [Test Local Guide](GUIDE_TEST_LOCAL.md) - Local testing setup
- [Pre-commit Config](.pre-commit-config.yaml) - Code quality hooks
- [Coverage Config](.coveragerc) - Test coverage settings
- [AGENTS.md](AGENTS.md) - AI agent testing guidelines

**Domain Index**: [docs/testing/INDEX.md](docs/testing/INDEX.md) _(placeholder)_

---

### 📄 Reports & Analytics

**Description**: Reporting APIs, analytics dashboards, performance metrics, and data exports.

**Keywords**: reports, analytics, metrics, KPIs, performance, data-exports, PDF, dashboards

**Critical Documents**:
- [Reports](docs/reports/) - Report generation & exports
- [Metrics](docs/metrics/) - Analytics & KPIs
- [Observability Dashboards](docs/observability/dashboards/) - Visual analytics

**Domain Index**: [docs/reports/INDEX.md](docs/reports/INDEX.md) _(placeholder)_

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
- **Frontend**: React (SPA) - see [UI docs](docs/ui/)

### Common AI Agent Tasks

| Task | Documentation Path | Keywords |
|------|-------------------|----------|
| **Add new service** | [Architecture](#-architecture--services) | microservices, FastAPI, Docker |
| **Modify trading logic** | [Strategies](#-strategies--trading) | algo-engine, backtesting, orders |
| **Fix authentication** | [Security](#-security--compliance) | Auth0, auth-service, tokens |
| **Add monitoring** | [Observability](#-observability--monitoring) | metrics, Prometheus, Grafana |
| **Deploy changes** | [Operations](#-operations--deployment) | Docker, deployment, CI/CD |
| **Write tests** | [Testing](#-testing--quality) | pytest, coverage, fixtures |
| **Update UI** | [User Interface](#-user-interface) | React, dashboard, SPA |

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

- **New service**: Update [Architecture](#-architecture--services) and create service doc in `docs/`
- **New feature**: Update [Feature Overview](README.md#-feature-overview) and relevant domain index
- **Breaking change**: Update [Changelog](CHANGELOG.md) and affected service docs
- **API change**: Update service doc and [Dashboard Data Contracts](docs/ui/dashboard-data-contracts.md) if applicable
- **Configuration change**: Update [Quick Start](README.md#-quick-start) or [Operations](#-operations--deployment)

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
