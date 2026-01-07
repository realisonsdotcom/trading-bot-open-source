# 📚 Trading Bot Documentation Index

> **Navigation Hub**: Central entry point for all project documentation

**Keywords**: documentation, index, navigation, architecture, services, guides, tutorials, AI-agent-friendly

---

## 🎯 Quick Navigation

| Role | Start Here |
|------|------------|
| **New User** | [Quick Start Guide](README.md#-quick-start) → [Demo Setup](docs/domains/3_operations/demo.md) |
| **Developer** | [Contributing Guide](CONTRIBUTING.md) → [Architecture Index](docs/domains/2_architecture/INDEX.md) |
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

### 🏗️ Architecture & Services

**Description**: System architecture and service documentation for execution, platform, and web dashboard.

**Keywords**: architecture, services, execution, platform, webapp, routing, auth

**Critical Documents**:
- [Execution Index](docs/domains/2_architecture/execution/INDEX.md) - Order routing & broker integration
- [Order Router](docs/domains/2_architecture/execution/order-router.md) - Execution service details
- [Platform Index](docs/domains/2_architecture/platform/INDEX.md) - Auth, users, billing, streaming
- [Auth Service](docs/domains/2_architecture/platform/auth-service.md) - Authentication & sessions
- [WebApp Index](docs/domains/2_architecture/webapp/INDEX.md) - Dashboard UI & SPA shell
- [UI Design System](docs/domains/2_architecture/webapp/ui/README.md) - UI tokens & patterns

**Domain Index**: [docs/domains/2_architecture/INDEX.md](docs/domains/2_architecture/INDEX.md)

---

### 📈 Operations

**Description**: Deployment workflows, observability, infrastructure, and operational runbooks.

**Keywords**: operations, deployment, observability, metrics, alerting, infrastructure, demo

**Critical Documents**:
- [Operations Index](docs/domains/3_operations/INDEX.md) - Runbooks and deployment guidance
- [Demo Setup](docs/domains/3_operations/demo.md) - End-to-end demo environment
- [Observability Stack](docs/domains/3_operations/observability/README.md) - Logs, traces, dashboards
- [Alerting Runbook](docs/domains/3_operations/operations/alerting.md) - Notifications & incident flow
- [Infrastructure Index](docs/domains/3_operations/infrastructure/INDEX.md) - Docker and migrations

**Domain Index**: [docs/domains/3_operations/INDEX.md](docs/domains/3_operations/INDEX.md)

---

### 🔐 Security

**Description**: Authentication security, credential handling, and compliance guidance.

**Keywords**: security, auth0, credentials, encryption, rotation, compliance

**Critical Documents**:
- [Auth0 Setup](docs/domains/4_security/AUTH0_SETUP.md) - Identity configuration
- [Broker Credential Encryption](docs/domains/4_security/broker-credentials-encryption.md) - Secret handling
- [JWT/TOTP Rotation](docs/domains/4_security/jwt-totp-key-rotation.md) - Key rotation policy

**Domain Index**: [docs/domains/4_security/INDEX.md](docs/domains/4_security/INDEX.md)

---

### 💬 Community

**Description**: Community updates, governance notes, and release highlights.

**Keywords**: community, communications, governance, release-highlights, collaboration

**Critical Documents**:
- [Community Guide](docs/domains/5_community/community/README.md) - Community norms
- [Communications](docs/domains/5_community/communications/) - Internal updates
- [Governance](docs/domains/5_community/governance/) - KPI reviews & approvals
- [Release Highlights](docs/domains/5_community/release-highlights/) - Milestone summaries

**Domain Index**: [docs/domains/5_community/INDEX.md](docs/domains/5_community/INDEX.md)

---

### 🧪 Quality & Enablement

**Description**: Help center content, tutorials, reports, and risk checklists.

**Keywords**: quality, help, tutorials, reports, risk, onboarding

**Critical Documents**:
- [Help Center](docs/domains/6_quality/help/) - FAQs and onboarding guides
- [Tutorials](docs/domains/6_quality/tutorials/README.md) - Walkthroughs and notebooks
- [Reports](docs/domains/6_quality/reports/) - Code reviews and analyses
- [Risk Checklist](docs/domains/6_quality/risk/README.md) - Risk management notes

**Domain Index**: [docs/domains/6_quality/INDEX.md](docs/domains/6_quality/INDEX.md)

---

### 📋 Standards

**Description**: Engineering standards, quality baselines, and planning artifacts.

**Keywords**: standards, codex, evaluation, planning, backlog

**Critical Documents**:
- [Engineering Codex](docs/domains/7_standards/codex.md) - Standards & conventions
- [Project Evaluation](docs/domains/7_standards/project-evaluation.md) - Quality assessment
- [Roadmap](docs/ROADMAP.md) - Program milestones
- [Migration Map](docs/domains/7_standards/migration-map.md) - Documentation migration

**Domain Index**: [docs/domains/7_standards/INDEX.md](docs/domains/7_standards/INDEX.md)

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
- **Frontend**: React (SPA) - see [WebApp docs](docs/domains/2_architecture/webapp/INDEX.md)

### Common AI Agent Tasks

| Task | Documentation Path | Keywords |
|------|-------------------|----------|
| **Add new service** | [Infrastructure Index](docs/domains/3_operations/infrastructure/INDEX.md) | microservices, FastAPI, Docker |
| **Modify trading logic** | [Trading Index](docs/domains/1_trading/INDEX.md) | algo-engine, backtesting, orders |
| **Fix authentication** | [Auth Service](docs/domains/2_architecture/platform/auth-service.md) | auth, tokens, sessions |
| **Add monitoring** | [Observability Stack](docs/domains/3_operations/observability/README.md) | metrics, Prometheus, Grafana |
| **Deploy changes** | [Operations Index](docs/domains/3_operations/INDEX.md) | Docker, deployment, CI/CD |
| **Write tests** | [Engineering Codex](docs/domains/7_standards/codex.md) | pytest, coverage, QA |
| **Update UI** | [WebApp Index](docs/domains/2_architecture/webapp/INDEX.md) | React, dashboard, SPA |

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
config/             # Local environment configuration (dev/native)
libs/               # Shared Python libraries
scripts/            # Automation & deployment scripts
docs/               # Domain-specific documentation
tests/              # Integration & end-to-end tests
```

### Key Configuration Files

- **`config/.env.dev`**: Docker-based development environment variables
- **`config/.env.native`**: Host-based (localhost) development environment variables
- **`docker-compose.yml`**: Main service orchestration
- **`Makefile`**: Common development commands (`make dev-up`, `make test`, etc.)
- **`pyproject.toml`**: Python project metadata & dependencies
- **`.pre-commit-config.yaml`**: Code quality automation (black, mypy, bandit, etc.)

### When to Update Documentation

- **New service**: Update the relevant domain index under `docs/domains/*/INDEX.md`
- **New feature**: Update [Feature Overview](README.md#-feature-overview) and the matching domain index
- **Breaking change**: Update [Changelog](CHANGELOG.md) and affected service docs
- **API change**: Update service doc and [Dashboard Data Contracts](docs/domains/2_architecture/webapp/ui/dashboard-data-contracts.md) if applicable
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
**Questions?** Open an issue or check [FAQ](docs/domains/6_quality/help/faq/)
