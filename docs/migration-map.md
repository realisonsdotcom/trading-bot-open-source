# Documentation Migration Map

> **Purpose**: Map existing documentation files to the new domain-based structure (`docs/domains/1_trading` through `docs/domains/7_standards`).

**Status**: Phase 2.2 - Mapping only. No files moved in this phase.

**Last Updated**: 2026-01-06

---

## Domain Mapping

### 1_trading - Trading & Strategies

**Domain**: Trading strategies, algo engine, market data, screening, and live trading.

**Files to migrate**:

| Current Path | Target Path | Notes |
|--------------|-------------|-------|
| `docs/algo-engine.md` | `docs/domains/1_trading/algo-engine.md` | Core strategy execution engine |
| `docs/algo-order-contract.md` | `docs/domains/1_trading/algo-order-contract.md` | Strategy-order integration spec |
| `docs/market-data.md` | `docs/domains/1_trading/market-data.md` | Market data service & adapters |
| `docs/screener.md` | `docs/domains/1_trading/screener.md` | Market scanning & opportunity detection |
| `docs/inplay.md` | `docs/domains/1_trading/inplay.md` | Live trading monitoring service |
| `docs/strategies/` | `docs/domains/1_trading/strategies/` | Strategy documentation (already in subfolder) |

**Gaps identified**:
- Strategy backtesting guide (referenced in tutorials but no dedicated doc)
- Market connector comparison matrix
- Strategy performance metrics documentation

---

### 2_architecture - Architecture & Services

**Domain**: System design, microservices architecture, and core service documentation.

**Files to migrate**:

| Current Path | Target Path | Notes |
|--------------|-------------|-------|
| `docs/auth-service.md` | `docs/domains/2_architecture/auth-service.md` | Authentication & authorization service |
| `docs/user-service.md` | `docs/domains/2_architecture/user-service.md` | User management & profiles |
| `docs/billing.md` | `docs/domains/2_architecture/billing.md` | Subscription & payment processing |
| `docs/notification-service.md` | `docs/domains/2_architecture/notification-service.md` | Multi-channel alerts service |
| `docs/order-router.md` | `docs/domains/2_architecture/order-router.md` | Order management & routing |
| `docs/streaming.md` | `docs/domains/2_architecture/streaming.md` | WebSocket & real-time data service |
| `docs/marketplace.md` | `docs/domains/2_architecture/marketplace.md` | Strategy marketplace & listings |
| `docs/social.md` | `docs/domains/2_architecture/social.md` | Social trading & collaboration features |

**Gaps identified**:
- Overall architecture diagram/documentation
- Service communication patterns (API contracts)
- Database schema documentation
- Event-driven architecture patterns

---

### 3_operations - Operations & Deployment

**Domain**: Deployment guides, infrastructure setup, CI/CD, and operational procedures.

**Files to migrate**:

| Current Path | Target Path | Notes |
|--------------|-------------|-------|
| `docs/DEMO.md` | `docs/domains/3_operations/demo.md` | Complete demo environment guide |
| `docs/mvp-sandbox-flow.md` | `docs/domains/3_operations/mvp-sandbox-flow.md` | MVP sandbox workflow |
| `docs/operations/` | `docs/domains/3_operations/operations/` | Operational procedures (already in subfolder) |
| `docs/observability/` | `docs/domains/3_operations/observability/` | Monitoring stack (already in subfolder) |
| `docs/metrics/` | `docs/domains/3_operations/metrics/` | Custom metrics & KPIs (already in subfolder) |

**Gaps identified**:
- Production deployment guide
- Disaster recovery procedures
- Scaling guidelines
- Infrastructure as Code (IaC) documentation
- CI/CD pipeline documentation

---

### 4_security - Security & Compliance

**Domain**: Authentication, authorization, security best practices, and compliance documentation.

**Files to migrate**:

| Current Path | Target Path | Notes |
|--------------|-------------|-------|
| `docs/AUTH0_SETUP.md` | `docs/domains/4_security/auth0-setup.md` | Auth0 authentication configuration |
| `docs/security/` | `docs/domains/4_security/security/` | Security documentation (already in subfolder) |

**Gaps identified**:
- Security audit checklist
- Secrets management guide (beyond baseline)
- Compliance requirements documentation
- Security incident response procedures
- API security best practices

---

### 5_community - Community & Governance

**Domain**: Community resources, contribution guidelines, governance, and communication.

**Files to migrate**:

| Current Path | Target Path | Notes |
|--------------|-------------|-------|
| `docs/community/` | `docs/domains/5_community/community/` | Community resources (already in subfolder) |
| `docs/governance/` | `docs/domains/5_community/governance/` | Project governance (already in subfolder) |
| `docs/communications/` | `docs/domains/5_community/communications/` | Project updates (already in subfolder) |
| `docs/release-highlights/` | `docs/domains/5_community/release-highlights/` | Feature announcements (already in subfolder) |

**Gaps identified**:
- Contributor onboarding guide
- Code review guidelines
- Release process documentation
- Community moderation guidelines

---

### 6_quality - Quality & Tutorials

**Domain**: Testing strategies, quality assurance, tutorials, help guides, and learning resources.

**Files to migrate**:

| Current Path | Target Path | Notes |
|--------------|-------------|-------|
| `docs/tutorials/` | `docs/domains/6_quality/tutorials/` | Step-by-step walkthroughs (already in subfolder) |
| `docs/help/` | `docs/domains/6_quality/help/` | Help guides, FAQ, notebooks (already in subfolder) |
| `docs/risk/` | `docs/domains/6_quality/risk/` | Risk management documentation (already in subfolder) |

**Gaps identified**:
- Testing best practices guide
- Code quality standards documentation
- Performance testing guide
- Load testing procedures

---

### 7_standards - Standards & Project Management

**Domain**: Project planning, task tracking, standards, and project status.

**Files to migrate**:

| Current Path | Target Path | Notes |
|--------------|-------------|-------|
| `docs/codex.md` | `docs/domains/7_standards/codex.md` | Codex automation platform |
| `docs/project-evaluation.md` | `docs/domains/7_standards/project-evaluation.md` | Project assessment |
| `docs/tasks/` | `docs/domains/7_standards/tasks/` | Task tracking & planning (already in subfolder) |
| `docs/ROADMAP.md` | `docs/domains/7_standards/roadmap.md` | Future plans & milestones |

**Gaps identified**:
- Coding standards document
- API design standards
- Documentation standards
- Git workflow standards

---

## Root-Level Documentation Files

**Files that remain at `docs/` root**:

| File | Reason |
|------|--------|
| `INDEX.md` | Main documentation entry point (created in Phase 1) |
| `reports/` | Reports directory - may stay at root or move to `docs/domains/5_community/reports/` (TBD) |

**Note**: The `reports/` directory contains analysis reports (`2025-09-phase4-analysis.md`, `2025-11-code-review.md`) which could logically belong to either:
- `docs/domains/5_community/reports/` (as community/governance artifacts)
- `docs/domains/7_standards/reports/` (as project management artifacts)
- Remain at root as standalone analysis documents

**Recommendation**: Move `reports/` to `docs/domains/5_community/reports/` as these are governance/analysis artifacts.

---

## Missing Documentation Gaps

### High Priority

1. **Architecture Overview Document** (`docs/domains/2_architecture/overview.md`)
   - System architecture diagram
   - Service interaction patterns
   - Technology stack overview

2. **Production Deployment Guide** (`docs/domains/3_operations/production-deployment.md`)
   - Production environment setup
   - Scaling guidelines
   - High availability configuration

3. **Security Best Practices** (`docs/domains/4_security/best-practices.md`)
   - API security guidelines
   - Secrets management procedures
   - Security audit checklist

4. **Contributor Guide** (`docs/domains/5_community/contributing.md`)
   - Onboarding process
   - Code review guidelines
   - Development workflow

### Medium Priority

5. **Testing Guide** (`docs/domains/6_quality/testing-guide.md`)
   - Testing strategies
   - Test coverage requirements
   - Performance testing

6. **Coding Standards** (`docs/domains/7_standards/coding-standards.md`)
   - Code style guidelines
   - API design standards
   - Documentation standards

7. **Database Schema Documentation** (`docs/domains/2_architecture/database-schema.md`)
   - Entity relationship diagrams
   - Migration guide
   - Data model documentation

### Low Priority

8. **Market Connector Comparison** (`docs/domains/1_trading/market-connectors.md`)
   - Exchange comparison matrix
   - Connector capabilities
   - Integration guide

9. **Disaster Recovery** (`docs/domains/3_operations/disaster-recovery.md`)
   - Backup procedures
   - Recovery scenarios
   - Business continuity

10. **Performance Optimization** (`docs/domains/6_quality/performance.md`)
    - Performance tuning guide
    - Load testing results
    - Optimization best practices

---

## Migration Checklist

### Phase 2.2 (Current Phase)
- [x] Create migration map document
- [x] Map all existing docs to domains
- [x] Identify root-level files
- [x] Identify documentation gaps

### Phase 2.3 (Next Phase - File Migration)
- [ ] Migrate `1_trading` domain files
- [ ] Migrate `2_architecture` domain files
- [ ] Migrate `3_operations` domain files
- [ ] Migrate `4_security` domain files
- [ ] Migrate `5_community` domain files
- [ ] Migrate `6_quality` domain files
- [ ] Migrate `7_standards` domain files
- [ ] Update all internal links
- [ ] Update INDEX.md with new paths
- [ ] Verify all links work

### Phase 2.4 (Future Phase - Gap Filling)
- [ ] Create high-priority missing docs
- [ ] Create medium-priority missing docs
- [ ] Review and update existing docs
- [ ] Final documentation audit

---

## Notes

- **Subdirectories**: Many files are already organized in subdirectories (`strategies/`, `security/`, `tutorials/`, etc.). These subdirectories will be moved as-is to their respective domain directories.

- **Link Updates**: After migration, all internal documentation links will need to be updated to reflect the new structure. This includes:
  - Links in README.md
  - Links in INDEX.md
  - Cross-references between documents
  - Links in code comments

- **Naming Conventions**: Some files use uppercase names (`AUTH0_SETUP.md`, `DEMO.md`). Consider standardizing to lowercase with hyphens (`auth0-setup.md`, `demo.md`) during migration for consistency.

- **Reports Directory**: The `reports/` directory placement is TBD. Recommendation is to move it to `docs/domains/5_community/reports/` as governance artifacts.

---

**Created**: 2026-01-06  
**Author**: Documentation Migration Team  
**Related Issue**: #7
