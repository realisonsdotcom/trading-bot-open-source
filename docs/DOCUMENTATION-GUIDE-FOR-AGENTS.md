# Documentation Guide for AI Agents

> **Purpose**: This guide helps AI coding agents (GitHub Copilot, Cursor, Claude, etc.) create, update, and maintain documentation in this repository following our standards and conventions.

**Last Updated**: 2026-01-06  
**Target Audience**: CLI AI agents, automated documentation tools

---

## 📋 Table of Contents

1. [Documentation Structure](#-documentation-structure)
2. [Mandatory Rules](#-mandatory-rules)
3. [Workflow Steps](#-workflow-steps)
4. [YAML Front Matter](#-yaml-front-matter)
5. [Domain Organization](#-domain-organization)
6. [Common Errors](#-common-errors)
7. [Examples](#-examples)
8. [Validation Checklist](#-validation-checklist)

---

## 🏗️ Documentation Structure

### Repository Documentation Layout

```
trading-bot-open-source/
├── INDEX.md                          # Main documentation entry point
├── README.md                         # Project overview & quick start
├── CONTRIBUTING.md                   # Contribution guidelines
├── CHANGELOG.md                      # Version history
├── CODE_OF_CONDUCT.md               # Community standards
│
└── docs/
    ├── DOCUMENTATION-GUIDE-FOR-AGENTS.md  # This file
    ├── migration-map.md                   # Domain migration mapping
    │
    └── domains/                      # Domain-based organization
        ├── 1_trading/                # Trading & strategies domain
        │   ├── INDEX.md              # Domain index
        │   ├── assets/               # Domain-specific assets
        │   ├── algo-engine.md
        │   ├── market-data.md
        │   └── strategies/
        │
        ├── 2_architecture/           # Architecture & services domain
        │   ├── INDEX.md
        │   ├── assets/
        │   └── ...
        │
        ├── 3_operations/             # Operations & deployment domain
        │   ├── INDEX.md
        │   ├── assets/
        │   └── ...
        │
        ├── 4_security/               # Security & compliance domain
        │   ├── INDEX.md
        │   ├── assets/
        │   └── ...
        │
        ├── 5_community/              # Community & governance domain
        │   ├── INDEX.md
        │   ├── assets/
        │   └── ...
        │
        ├── 6_quality/                # Quality & tutorials domain
        │   ├── INDEX.md
        │   ├── assets/
        │   └── ...
        │
        └── 7_standards/              # Standards & project management
            ├── INDEX.md
            ├── assets/
            └── ...
```

### Domain Definitions

| Domain | Purpose | Common Content |
|--------|---------|----------------|
| **1_trading** | Trading strategies, algo engine, market data | Strategy docs, API specs, data feeds |
| **2_architecture** | System design, microservices, core services | Service docs, architecture diagrams, API contracts |
| **3_operations** | Deployment, infrastructure, CI/CD | Deployment guides, monitoring setup, runbooks |
| **4_security** | Authentication, authorization, security practices | Security guides, compliance docs, audit procedures |
| **5_community** | Community resources, governance, communication | Contribution guides, release notes, community updates |
| **6_quality** | Testing, QA, tutorials, help guides | Testing guides, tutorials, FAQ, learning resources |
| **7_standards** | Coding standards, project management, task tracking | Standards docs, roadmaps, project evaluation |

---

## ⚠️ Mandatory Rules

### Rule 1: YAML Front Matter is REQUIRED

**Every documentation file** (except INDEX.md at repo root) **MUST** include YAML front matter at the top.

✅ **Correct**:
```markdown
---
domain: 1_trading
title: Algo Engine Service
description: Strategy execution engine with plugin-based registry
keywords: algo-engine, strategies, plugins, backtesting
last_updated: 2026-01-06
related:
  - market-data.md
  - ../2_architecture/order-router.md
---

# Algo Engine Service

Content here...
```

❌ **Incorrect** (missing front matter):
```markdown
# Algo Engine Service

Content here...
```

### Rule 2: Domain Placement is STRICT

**All documentation** (except root-level project files) **MUST** live in a domain directory:

✅ **Correct**: `docs/domains/1_trading/algo-engine.md`  
❌ **Incorrect**: `docs/algo-engine.md`

### Rule 3: Use `git mv` for Migrations

When moving existing files to domains, **ALWAYS** use `git mv` to preserve history:

✅ **Correct**:
```bash
git mv docs/algo-engine.md docs/domains/1_trading/
```

❌ **Incorrect**:
```bash
mv docs/algo-engine.md docs/domains/1_trading/
git add docs/domains/1_trading/algo-engine.md
```

### Rule 4: Domain INDEX.md is REQUIRED

Every domain directory **MUST** have an `INDEX.md` file that serves as the domain's table of contents and navigation hub.

### Rule 5: Update Last Modified Date

When editing a document, **ALWAYS** update the `last_updated` field in the YAML front matter to the current date (YYYY-MM-DD).

### Rule 6: Maintain Cross-References

When adding related documents, update the `related` field in both documents' YAML front matter to ensure bidirectional linking.

---

## 🔄 Workflow Steps

### Creating New Documentation

1. **Identify the correct domain** (1_trading through 7_standards)
2. **Create the file** in `docs/domains/{domain}/`
3. **Add YAML front matter** (see template below)
4. **Write the content** using Markdown
5. **Update domain INDEX.md** to link to the new document
6. **Test all links** to ensure they work
7. **Commit with descriptive message**

### Updating Existing Documentation

1. **Locate the file** in its domain directory
2. **Update `last_updated`** in YAML front matter to today's date
3. **Make your changes** to the content
4. **Update `related` field** if referencing new documents
5. **Test all links** to ensure they still work
6. **Commit with descriptive message**

### Migrating Existing Documentation

1. **Check migration-map.md** for the file's target domain
2. **Use `git mv`** to move the file (preserves history)
   ```bash
   git mv docs/old-file.md docs/domains/{domain}/
   ```
3. **Add YAML front matter** to the migrated file
4. **Update internal links** in the content if needed
5. **Update domain INDEX.md** to include the migrated document
6. **Update related documents** that link to the moved file
7. **Test all links** to ensure they work
8. **Commit with migration message**

---

## 📝 YAML Front Matter

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `domain` | string | Domain identifier (1_trading, 2_architecture, etc.) | `1_trading` |
| `title` | string | Human-readable document title | `Algo Engine Service` |
| `description` | string | Brief one-line description | `Strategy execution engine with plugins` |
| `keywords` | string | Comma-separated keywords for search | `algo-engine, strategies, plugins` |
| `last_updated` | date | Last modification date (YYYY-MM-DD) | `2026-01-06` |

### Optional Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `related` | array | List of related documents (relative paths) | `- market-data.md`<br>`- ../2_architecture/order-router.md` |
| `status` | string | Document status (draft, review, published, deprecated) | `published` |
| `authors` | array | Document authors/contributors | `- Trading Team` |
| `version` | string | Document version | `1.0.0` |

### Template

```yaml
---
domain: {domain_number}_{domain_name}
title: {Document Title}
description: {One-line description of the document}
keywords: {keyword1}, {keyword2}, {keyword3}
last_updated: {YYYY-MM-DD}
related:
  - {relative-path-to-related-doc-1.md}
  - {relative-path-to-related-doc-2.md}
status: {draft|review|published|deprecated}
---
```

### Templates Directory

Reusable templates are available in `docs/templates/`:

- `docs/templates/service-doc-template.md`
- `docs/templates/guide-template.md`

### Minimal Valid Example

```yaml
---
domain: 1_trading
title: My New Document
description: A brief description of this document
keywords: trading, example, documentation
last_updated: 2026-01-06
---
```

---

## 🗂️ Domain Organization

### Choosing the Right Domain

Ask yourself these questions:

1. **Is it about trading/strategies/market data?** → `1_trading`
2. **Is it about system architecture/services?** → `2_architecture`
3. **Is it about deployment/infrastructure/operations?** → `3_operations`
4. **Is it about security/compliance/authentication?** → `4_security`
5. **Is it about community/governance/releases?** → `5_community`
6. **Is it about testing/tutorials/learning?** → `6_quality`
7. **Is it about standards/project management?** → `7_standards`

### Domain Overlap Handling

If a document could fit in multiple domains, use this priority order:

1. **Primary purpose** (what is the main topic?)
2. **Target audience** (who will use this most?)
3. **Cross-reference** (link from other relevant domains)

**Example**: A document about testing trading strategies
- **Primary domain**: `6_quality` (testing is the main topic)
- **Cross-reference from**: `1_trading/INDEX.md` (link to the testing guide)

### Subdirectories Within Domains

You can create subdirectories within domains for better organization:

```
docs/domains/1_trading/
├── INDEX.md
├── algo-engine.md
├── market-data.md
├── strategies/              # Subdirectory for strategy docs
│   ├── README.md
│   ├── orb-strategy.md
│   └── gap-fill-strategy.md
└── assets/                  # Subdirectory for images/diagrams
    ├── algo-engine-diagram.png
    └── market-data-flow.svg
```

### Assets Organization

- Place images, diagrams, and other assets in the `assets/` subdirectory of the domain
- Reference assets using relative paths: `![Diagram](assets/diagram.png)`
- Use descriptive filenames: `algo-engine-architecture.svg` instead of `image1.svg`

---

## ❌ Common Errors

### Error 1: Missing YAML Front Matter

**Problem**:
```markdown
# My Document

Content here...
```

**Solution**: Add YAML front matter at the very top:
```markdown
---
domain: 1_trading
title: My Document
description: Document description
keywords: keyword1, keyword2
last_updated: 2026-01-06
---

# My Document

Content here...
```

### Error 2: Incorrect Domain Path

**Problem**: File created at `docs/my-document.md`

**Solution**: Move to correct domain:
```bash
git mv docs/my-document.md docs/domains/1_trading/
```

### Error 3: Using `mv` Instead of `git mv`

**Problem**:
```bash
mv docs/old.md docs/domains/1_trading/
git add docs/domains/1_trading/old.md
```

**Result**: Git history is lost

**Solution**: Use `git mv`:
```bash
git mv docs/old.md docs/domains/1_trading/
```

### Error 4: Broken Relative Links

**Problem**: After moving a file, links like `[See this](../other-doc.md)` break

**Solution**: Update relative paths based on new location:
```markdown
# Before move (docs/my-doc.md)
[See this](other-doc.md)

# After move (docs/domains/1_trading/my-doc.md)
[See this](../2_architecture/other-doc.md)
```

### Error 5: Forgetting to Update Domain INDEX

**Problem**: Created new doc but didn't add it to domain INDEX.md

**Solution**: Always update `docs/domains/{domain}/INDEX.md` to link to new documents:
```markdown
## Core Documentation

- **[My New Document](my-new-doc.md)** - Brief description
```

### Error 6: Incorrect Date Format

**Problem**:
```yaml
last_updated: 06/01/2026  # Wrong format
```

**Solution**: Use ISO 8601 format (YYYY-MM-DD):
```yaml
last_updated: 2026-01-06  # Correct
```

---

## 📚 Examples

### Example 1: Creating a New Trading Strategy Guide

**File**: `docs/domains/1_trading/strategies/momentum-strategy.md`

```markdown
---
domain: 1_trading
title: Momentum Strategy Implementation
description: Guide for implementing momentum-based trading strategies
keywords: momentum, strategy, trading, technical-analysis
last_updated: 2026-01-06
related:
  - ../algo-engine.md
  - ../market-data.md
status: published
---

# Momentum Strategy Implementation

This guide explains how to implement momentum-based trading strategies...

## Overview

Momentum strategies capitalize on the continuation of existing trends...

## Implementation Steps

1. Define momentum indicators
2. Set entry/exit criteria
3. Configure risk parameters
4. Backtest the strategy

...
```

**Update Domain INDEX**:

Edit `docs/domains/1_trading/INDEX.md`:
```markdown
### Strategy Guides

- **[Momentum Strategy](strategies/momentum-strategy.md)**
  - Guide for implementing momentum-based trading strategies
  - Keywords: `momentum`, `strategy`, `technical-analysis`
```

### Example 2: Migrating an Existing Service Doc

**Original**: `docs/billing.md`  
**Target**: `docs/domains/2_architecture/billing.md`

**Step 1**: Move with git mv
```bash
git mv docs/billing.md docs/domains/2_architecture/
```

**Step 2**: Add YAML front matter

Edit `docs/domains/2_architecture/billing.md`:
```markdown
---
domain: 2_architecture
title: Billing Service
description: Subscription and payment processing service
keywords: billing, subscriptions, payments, stripe
last_updated: 2026-01-06
related:
  - user-service.md
  - ../5_community/governance/pricing-policy.md
---

# Billing Service

(Original content continues here...)
```

**Step 3**: Update domain INDEX

Edit `docs/domains/2_architecture/INDEX.md`:
```markdown
### Core Services

- **[Billing Service](billing.md)** ⭐
  - Subscription and payment processing
  - Stripe integration
  - Keywords: `billing`, `subscriptions`, `payments`
```

### Example 3: Creating a Domain INDEX

**File**: `docs/domains/3_operations/INDEX.md`

```markdown
---
domain: 3_operations
title: Operations & Deployment Domain Index
description: Deployment guides, infrastructure setup, CI/CD, and operational procedures
keywords: operations, deployment, infrastructure, CI/CD, monitoring
last_updated: 2026-01-06
---

# 🚀 Operations & Deployment Domain

> **Domain**: Deployment guides, infrastructure setup, and operational procedures

---

## 📑 Domain Overview

This domain covers:
- Deployment procedures and automation
- Infrastructure setup and configuration
- CI/CD pipelines
- Monitoring and observability
- Operational runbooks

---

## 📚 Core Documentation

### Deployment

- **[Demo Environment](demo.md)** ⭐
  - Complete demo environment setup guide
  - Keywords: `demo`, `docker`, `setup`

- **[Production Deployment](production-deployment.md)** ⭐
  - Production environment deployment procedures
  - Keywords: `production`, `deployment`, `scaling`

### Monitoring

- **[Observability Overview](observability/README.md)** ⭐
  - Monitoring stack setup (Prometheus, Grafana)
  - Keywords: `monitoring`, `observability`, `metrics`

---

## 🔗 Related Domains

- **[2_architecture](../2_architecture/INDEX.md)** - Service architecture details
- **[4_security](../4_security/INDEX.md)** - Security configuration

---

[← Back to Main Index](../../../INDEX.md)
```

---

## ✅ Validation Checklist

Before committing documentation changes, verify:

### File Structure
- [ ] File is in correct domain directory (`docs/domains/{domain}/`)
- [ ] Domain has an `INDEX.md` file
- [ ] Assets (if any) are in domain `assets/` subdirectory

### YAML Front Matter
- [ ] YAML front matter exists at top of file
- [ ] All required fields present: `domain`, `title`, `description`, `keywords`, `last_updated`
- [ ] `domain` matches directory name
- [ ] `last_updated` uses ISO format (YYYY-MM-DD)
- [ ] `related` paths are relative and correct

### Content
- [ ] Markdown formatting is correct
- [ ] Code blocks have language specified
- [ ] Images/diagrams have alt text
- [ ] Links are relative (not absolute GitHub URLs)
- [ ] Internal links work (test by clicking)

### Domain INDEX
- [ ] Domain INDEX.md is updated with new/changed documents
- [ ] Document is listed with brief description
- [ ] Keywords are included in INDEX entry

### Git
- [ ] Used `git mv` for migrations (not `mv`)
- [ ] Commit message is descriptive
- [ ] No unrelated changes included

### Cross-References
- [ ] Related documents updated (bidirectional linking)
- [ ] Root INDEX.md updated if needed (for major additions)
- [ ] Migration map updated if moving files

---

## 🤖 Agent-Specific Tips

### For GitHub Copilot CLI

When asked to create/update documentation:
1. Always check if file exists first: `ls docs/domains/{domain}/`
2. Use `git mv` for moves: `git mv source target`
3. Validate YAML syntax before committing
4. Update INDEX.md in same commit

### For Automated Tools

- Parse existing YAML front matter before editing
- Preserve formatting when updating `last_updated`
- Batch update related documents in single commit
- Use migration-map.md as authoritative source for file locations

### Common Commands

```bash
# Check file location
find docs -name "algo-engine.md"

# Move file preserving history
git mv docs/old.md docs/domains/1_trading/new.md

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('file.md').read().split('---')[1])"

# List files in domain
ls -la docs/domains/1_trading/

# Search for keyword in docs
grep -r "keyword" docs/domains/
```

---

## 📖 Additional Resources

- **[Main Documentation Index](../../INDEX.md)** - Repository documentation hub
- **[Migration Map](migration-map.md)** - Domain migration mapping
- **[Contributing Guide](../../CONTRIBUTING.md)** - Contribution guidelines
- **[README](../../README.md)** - Project overview

---

**Maintained By**: Documentation Team  
**Last Updated**: 2026-01-06  
**Questions?** Open an issue or check [Contributing Guide](../../CONTRIBUTING.md)
