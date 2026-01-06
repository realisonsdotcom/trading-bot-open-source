# AGENTS.md - Trading Bot Development Contract

**Version:** 1.0
**Date:** 2026-01-04
**Purpose:** Quick reference for CLI agents (code quality, standards, workflow)

## Quick Navigation for Agents

**READ FIRST:**
- docs/DOCUMENTATION-GUIDE-FOR-AGENTS.md
- INDEX.md
- docs/00-START-HERE.md

## Agent Roles and Responsibilities

| Agent | Primary Task | Branch Pattern | Domain |
| --- | --- | --- | --- |
| TradingAgent | Strategies and Analysis | feat/agent-trading-* | Trading |
| ExecutionAgent | Order Execution and Market Data | feat/agent-exec-* | Execution |
| MonitoringAgent | Reports and Alerts | feat/agent-monitor-* | Monitoring |
| PlatformAgent | Platform Services | feat/agent-platform-* | Platform |
| WebAppAgent | Web Dashboard | feat/agent-webapp-* | WebApp |
| InfraAgent | Infrastructure and CI/CD | chore/agent-infra-* | Infrastructure |
| QualityAgent | Standards and Testing | test/agent-quality-* | Standards |

## Essential Code Standards

### Backend (Python/FastAPI)

```
services/
├── [service_name]/
│   ├── app/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── api/
│   │   └── services/
│   ├── tests/
│   └── requirements.txt
```

Naming:
- Classes: PascalCase (UserModel)
- Functions: snake_case (get_user_by_id)
- Constants: UPPER_SNAKE_CASE (API_VERSION)

Tools:
- Formatter: black
- Linter: flake8, isort, mypy (strict)
- Tests: pytest

### Frontend (TypeScript/React)

```
services/web_dashboard/
├── src/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── utils/
│   └── types/
```

Naming:
- Components: PascalCase (Button, UserCard)
- Functions: camelCase (getUserData)
- Types: PascalCase (UserProps)
- Constants: UPPER_SNAKE_CASE (API_BASE_URL)

Notes:
- TypeScript: no any types

## Git Workflow

```
# 1. Create feature branch
git checkout -b feat/agent-trading-new-strategy

# 2. Make changes and commit
git add .
git commit -m "feat(trading): add momentum strategy"

# 3. Push and create PR
git push origin feat/agent-trading-new-strategy
gh pr create --title "Title" --body "Description"
```

Conventional Commits:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- refactor: Code restructuring
- test: Tests
- chore: Dependencies, config

## Before Committing

- Code follows naming conventions
- Tests written and passing
- Docstrings/comments added
- No hardcoded secrets
- Linting passes (black, flake8, mypy)
- TypeScript: no any types
- Documentation updated
- PR description clear

## Documentation by Domain

- Trading: docs/domains/1_trading/INDEX.md
- Execution: docs/domains/2_execution/INDEX.md
- Monitoring: docs/domains/3_monitoring/INDEX.md
- Platform: docs/domains/4_platform/INDEX.md
- WebApp: docs/domains/5_webapp/INDEX.md
- Infrastructure: docs/domains/6_infrastructure/INDEX.md
- Standards: docs/domains/7_standards/INDEX.md

## CI/CD and Testing

- GitHub Actions runs on every PR
- Tests: pytest plus E2E
- Deployment: Docker-based
- Release: semantic versioning

## Help and Escalation

- Documentation question: docs/DOCUMENTATION-GUIDE-FOR-AGENTS.md
- Code style question: standards section above
- Architecture question: docs/domains/6_infrastructure/
- Blocked: escalate to maintainers

Last Updated: 2026-01-04
Version: 1.0
