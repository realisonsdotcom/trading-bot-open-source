---
domain: 7_standards
title: Retro-Contribution Tooling Guide
description: Guide for retro-contributing development and documentation tooling from trading-bot-open-source to other projects.
keywords: tooling, retro-contribution, documentation, automation, scripts, ci-cd
last_updated: 2026-01-07
related:
  - codex.md
  - project-evaluation.md
  - generate-index-v2-guide.md
---

# Retro-Contribution Tooling Guide

> **Audience**: Developers, DevOps Engineers, Documentation Maintainers  
> **Issue**: #55

## Purpose

This guide documents the process of retro-contributing development and documentation tooling from `trading-bot-open-source` to other projects. It covers identification, adaptation, and integration of useful tools and workflows.

## Overview

The `trading-bot-open-source` project has developed several tooling solutions that can benefit other projects:

1. **Documentation Automation Scripts** - Generate and validate documentation metadata
2. **CI/CD Workflows** - GitHub Actions for documentation validation
3. **Development Tooling** - Makefile commands and helper scripts
4. **Codex Automation Platform** - Advanced contribution lifecycle automation (optional)

## Available Tooling

### 1. Documentation Scripts

#### `scripts/generate_index_v2.py`

**Purpose**: Automatically generates `INDEX.md` files for documentation domains from YAML front matter metadata.

> **Note**: This v2 script supersedes the legacy `generate_index.py` and adds recursive indexing plus Jinja2 templates.

**Features**:
- Scans markdown files in domain directories
- Extracts YAML front matter metadata
- Generates structured index files with descriptions
- Supports custom domain ordering
- Dry-run mode for testing

**Location**: `trading-bot-open-source/scripts/generate_index_v2.py`

**Dependencies**: `pyyaml`, `jinja2`

**Adaptation for Target Project**:
- Update `DOMAIN_ORDER` to match the target project's domain structure:
  ```python
  DOMAIN_ORDER = [
      "frontend",
      "backend",
      "architecture",
      "devops",
      "standards",
  ]
  ```
- Adjust `docs/domains` path if the target project uses different structure
- Update domain header generation to match the target project's metadata format

#### `scripts/validate_docs_metadata.py`

**Purpose**: Validates YAML front matter in documentation files to ensure consistency and completeness.

**Features**:
- Validates required fields (domain, title, description, keywords, last_updated)
- Checks domain names against valid list
- Checks if domain field matches actual directory name
- Validates date format (YYYY-MM-DD)
- Validates status values
- Validates internal markdown links and 'related' links (with --strict flag)
- Reports all errors with file locations

**Location**: `trading-bot-open-source/scripts/validate_docs_metadata.py`

**Dependencies**: `pyyaml`

**Adaptation for Target Project**:
- Update `VALID_DOMAINS` to match the target project's domains:
  ```python
  VALID_DOMAINS = {
      "frontend",
      "backend",
      "architecture",
      "devops",
      "standards",
  }
  ```
- Adjust `REQUIRED_FIELDS` if the target project uses different metadata schema
- Update field aliases if the target project uses different field names (e.g., `last-updated` vs `last_updated`)

### 2. CI/CD Workflows

#### `.github/workflows/validate-docs.yml`

**Purpose**: GitHub Actions workflow that validates documentation on pull requests and pushes.

**Features**:
- Validates YAML front matter metadata
- Checks markdown link integrity
- Validates documentation structure (prevents orphaned files)
- Runs on PR and push to main branch
- Only triggers on documentation file changes

**Location**: `trading-bot-open-source/.github/workflows/validate-docs.yml`

**Adaptation for Target Project**:
- Update allowed root files list if the target project has different structure:
  ```yaml
  ALLOWED_FILES=("00-START-HERE.md" "DOCUMENTATION-GUIDE-FOR-AGENTS.md" "ROADMAP.md")
  ```
- Adjust Python version if needed (currently 3.11)
- Update script paths if the target project uses different script locations
- Configure markdown-link-check config file path

### 3. Development Tooling

#### `Makefile`

**Purpose**: Provides common development commands for testing, linting, migrations, and service management.

**Key Commands**:
- `make lint` - Run pre-commit hooks
- `make test` - Run pytest with coverage
- `make migrate-generate` - Generate Alembic migrations
- `make migrate-up` - Apply migrations
- `make demo-up` - Start demo environment

**Location**: `trading-bot-open-source/Makefile`

**Adaptation for Target Project**:
- Extract relevant commands for the target project's stack
- Adapt database migration commands if the target project uses different migration tool
- Update service names and Docker Compose service references
- Adjust Python version and dependency paths

### 4. Codex Automation Platform (Advanced)

**Purpose**: Automated contribution lifecycle management with GitHub/Stripe/TradingView integration.

**Components**:
- `services/codex_gateway/` - Webhook gateway service
- `services/codex_worker/` - Event processing worker
- `libs/codex/` - Shared library
- `.github/workflows/codex-run.yml` - Reusable workflow

**Status**: Optional - More complex integration requiring infrastructure setup

**See**: [Codex Documentation](codex.md) for full details

## Retro-Contribution Process

### Phase 1: Assessment

1. **Identify Target Project's Needs**
   - Review the target project's current documentation structure
   - Identify pain points in documentation maintenance
   - Assess current CI/CD capabilities
   - Review development workflow gaps

2. **Map Tooling to Needs**
   - Match available tooling to identified needs
   - Prioritize high-impact, low-effort tools first
   - Document dependencies and prerequisites

### Phase 2: Adaptation

1. **Copy Tooling Files**
   ```bash
   # From trading-bot-open-source
   cp scripts/generate_index_v2.py /path/to/target-project/scripts/
   cp scripts/validate_docs_metadata.py /path/to/target-project/scripts/
   cp .github/workflows/validate-docs.yml /path/to/target-project/.github/workflows/
   ```

2. **Adapt Configuration**
   - Update domain lists and paths
   - Adjust metadata schemas
   - Modify file structure validations
   - Update Python versions and dependencies

3. **Test Locally**
   ```bash
   # Test index generation
   python scripts/generate_index_v2.py --dry-run
   
   # Test metadata validation
   python scripts/validate_docs_metadata.py
   ```

### Phase 3: Integration

1. **Update Target Project Documentation**
   - Document new scripts in the target project's documentation guide
   - Add usage examples
   - Update contributor guidelines

2. **Configure CI/CD**
   - Add workflow to the target project's `.github/workflows/`
   - Configure required secrets (if any)
   - Test workflow on a test branch

3. **Add to Makefile (Optional)**
   ```makefile
docs-validate:
    python scripts/validate_docs_metadata.py

docs-index:
    python scripts/generate_index_v2.py
   ```

### Phase 4: Validation

1. **Run Validation Suite**
   - Execute all scripts locally
   - Verify CI/CD workflows trigger correctly
   - Test edge cases and error handling

2. **Documentation Update**
   - Update the target project's documentation guide if needed
   - Add references to new tooling
   - Document any project-specific adaptations

## Step-by-Step: Documentation Scripts

### Step 1: Copy Scripts

```bash
cd /path/to/target-project
mkdir -p scripts
cp /path/to/trading-bot-open-source/scripts/generate_index_v2.py scripts/
cp /path/to/trading-bot-open-source/scripts/validate_docs_metadata.py scripts/
chmod +x scripts/*.py
```

### Step 2: Install Dependencies

```bash
# Add to target project's requirements or install directly
pip install pyyaml
```

### Step 3: Adapt Domain Configuration

Edit `scripts/generate_index_v2.py`:

```python
DOMAIN_ORDER = [
    "frontend",
    "backend",
    "architecture",
    "devops",
    "standards",
]
```

Edit `scripts/validate_docs_metadata.py`:

```python
VALID_DOMAINS = {
    "frontend",
    "backend",
    "architecture",
    "devops",
    "standards",
}
```

### Step 4: Test Scripts

```bash
# Test index generation (dry-run)
python scripts/generate_index_v2.py --root docs/domains --dry-run

# Test metadata validation
python scripts/validate_docs_metadata.py
```

### Step 5: Generate Indexes

```bash
# Generate all domain indexes
python scripts/generate_index_v2.py --root docs/domains
```

## Step-by-Step: CI/CD Workflow

### Step 1: Copy Workflow

```bash
mkdir -p .github/workflows
cp /path/to/trading-bot-open-source/.github/workflows/validate-docs.yml \
   .github/workflows/validate-docs.yml
```

### Step 2: Adapt Workflow

Edit `.github/workflows/validate-docs.yml`:

```yaml
# Update allowed files if target project has different root docs
ALLOWED_FILES=("00-START-HERE.md" "DOCUMENTATION-GUIDE-FOR-AGENTS.md" "ROADMAP.md")

# Update script paths if different
run: python3 scripts/validate_docs_metadata.py
```

### Step 3: Configure Markdown Link Check (Optional)

Create `.github/markdown-link-check-config.json`:

```json
{
  "ignorePatterns": [
    {
      "pattern": "^http://localhost"
    },
    {
      "pattern": "^https://localhost"
    }
  ]
}
```

### Step 4: Test Workflow

1. Create a test branch
2. Make a documentation change
3. Open a pull request
4. Verify workflow runs successfully

## Benefits

### Documentation Scripts

- **Consistency**: Ensures all documentation follows metadata standards
- **Automation**: Reduces manual index maintenance
- **Validation**: Catches errors before merge
- **Scalability**: Handles growing documentation easily

### CI/CD Workflows

- **Quality Gate**: Prevents broken documentation from merging
- **Early Detection**: Catches issues in PRs, not production
- **Automation**: No manual validation needed
- **Standards Enforcement**: Ensures documentation structure compliance

## Considerations

### Differences Between Projects

1. **Domain Structure**: Target projects may use different domain names than trading-bot-open-source
2. **Metadata Schema**: May need to adapt field names and requirements
3. **File Organization**: Target projects may have different allowed root files
4. **Dependencies**: Python version and package requirements may differ

### Maintenance

- **Updates**: Tooling may need updates as projects evolve
- **Synchronization**: Consider if tooling should stay in sync or diverge
- **Documentation**: Keep project-specific adaptations documented

### Testing

- Always test adapted tooling in a test branch first
- Verify edge cases work correctly
- Ensure error messages are helpful for the target project's context

## Troubleshooting

### Issue: Script fails with "Invalid domain"

**Resolution**: Update `VALID_DOMAINS` in `validate_docs_metadata.py` to include all target project domains.

### Issue: Index generation creates wrong structure

**Resolution**: Check `DOMAIN_ORDER` matches the target project's domain organization and update accordingly.

### Issue: CI workflow fails on allowed files check

**Resolution**: Update `ALLOWED_FILES` array in workflow to match the target project's root documentation files.

### Issue: Metadata validation fails on required fields

**Resolution**: Review the target project's metadata schema and update `REQUIRED_FIELDS` in validation script.

## Next Steps

1. **Evaluate**: Review the target project's current tooling needs
2. **Prioritize**: Start with high-impact, low-effort tools
3. **Adapt**: Copy and adapt selected tooling
4. **Test**: Validate adapted tooling thoroughly
5. **Integrate**: Add to CI/CD and documentation
6. **Document**: Update the target project's documentation guides

## Related Documentation

- [Codex Automation Platform](codex.md) - Advanced automation platform details
- [Project Evaluation](project-evaluation.md) - Project assessment framework
- [Standards Domain Index](INDEX.md) - Standards domain overview

## References

- **Source Repository**: `trading-bot-open-source`
- **Issue**: #55 - Retro-contribution tooling guide
