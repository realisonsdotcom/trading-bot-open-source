---
domain: 7_standards
title: Generate Index v2 Guide
description: Guide for generating documentation indexes with generate_index_v2.py.
keywords: documentation, index, tooling, generate-index, jinja2
last_updated: 2026-01-07
status: published
related:
  - INDEX.md
  - retro-contribution-rbok-tooling.md
---

# Generate Index Script (v2)

## Overview

The `generate_index_v2.py` script automatically generates `INDEX.md` files for documentation directories based on YAML front matter metadata. It supports recursive processing of subdirectories and uses Jinja2 templates for customizable output.

## Features

- ✅ **Recursive Index Generation**: Processes domains and all subdirectories
- ✅ **Metadata Extraction**: Reads `title`, `description`, `keywords` from YAML front matter
- ✅ **Jinja2 Templates**: Customizable output format via templates
- ✅ **Subdirectory Linking**: Auto-generates links to subdirectory indexes
- ✅ **Ordered Domains**: Respects domain ordering (1_trading, 2_architecture, etc.)
- ✅ **Dry-run Mode**: Preview changes without modifying files

## Installation

Install required dependencies:

```bash
pip install -r requirements/requirements-dev.txt
```

Or install individually:

```bash
pip install jinja2>=3.1.0 pyyaml>=6.0
```

## Usage

### Basic Usage

Generate indexes for all domains and subdirectories:

```bash
python3 scripts/generate_index_v2.py
```

### Dry-run Mode

Preview what would be generated without writing files:

```bash
python3 scripts/generate_index_v2.py --dry-run
```

### Custom Root Directory

Process a different documentation root:

```bash
python3 scripts/generate_index_v2.py --root docs/custom-path
```

### Custom Template

Use a custom Jinja2 template:

```bash
python3 scripts/generate_index_v2.py --template docs/templates/my-template.md.j2
```

### Limit Recursion Depth

Control how deep the script processes subdirectories:

```bash
python3 scripts/generate_index_v2.py --max-depth 2
```

## Command-line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--root` | `docs/domains` | Root directory to process |
| `--template` | Built-in template | Path to custom Jinja2 template |
| `--max-depth` | `10` | Maximum recursion depth |
| `--dry-run` | `false` | Preview changes without writing |

## How It Works

### 1. Document Discovery

The script scans each directory for markdown files (`.md`) with YAML front matter:

```markdown
---
title: My Document
description: A description of the document
keywords: keyword1, keyword2
---

# My Document

Content here...
```

### 2. Metadata Extraction

Front matter fields used:
- **`title`**: Document title (fallback: filename converted to title case)
- **`description`**: Brief description (optional)
- **`keywords`**: Comma-separated keywords (optional)

### 3. Subdirectory Processing

For each subdirectory:
- Checks for existing `INDEX.md` to extract metadata
- Uses directory name as fallback title
- Generates link to subdirectory's `INDEX.md`

### 4. Index Generation

Creates `INDEX.md` with:
- **Front matter**: Domain, title, description, keywords, last_updated
- **Documents section**: Links to all markdown files with descriptions
- **Subdirectories section**: Links to subdirectory indexes (if any)

### 5. Recursive Processing

Processes subdirectories recursively up to `--max-depth` levels.

## Template Format

### Default Template

The built-in template structure:

```jinja2
---
domain: {{ domain }}
title: {{ title }}
description: {{ description }}
keywords: {{ keywords }}
last_updated: {{ last_updated }}
---

# {{ title }}

> Auto-generated. Do not edit manually.

## Documents

{% for doc in documents %}
- [{{ doc.title }}]({{ doc.path }}){% if doc.description %} - {{ doc.description }}{% endif %}
{% endfor %}
{% if subdirectories %}

## Subdirectories

{% for subdir in subdirectories %}
- [{{ subdir.name }}]({{ subdir.path }}){% if subdir.description %} - {{ subdir.description }}{% endif %}
{% endfor %}
{% endif %}
```

### Template Variables

| Variable | Type | Description |
|----------|------|-------------|
| `domain` | `str` | Top-level domain name (e.g., `1_trading`) |
| `title` | `str` | Index title |
| `description` | `str` | Index description |
| `keywords` | `str` | Comma-separated keywords |
| `last_updated` | `str` | ISO date (YYYY-MM-DD) |
| `documents` | `list[dict]` | List of document metadata |
| `subdirectories` | `list[dict]` | List of subdirectory metadata |

### Document Object

```python
{
    "title": "Document Title",
    "description": "Document description",
    "path": "relative/path/to/doc.md"
}
```

### Subdirectory Object

```python
{
    "name": "Subdirectory Name",
    "description": "Subdirectory description",
    "path": "subdirectory/INDEX.md"
}
```

## Custom Template Example

Create a minimal template (`docs/templates/minimal.md.j2`):

```jinja2
# {{ title }}

{% for doc in documents %}
- [{{ doc.title }}]({{ doc.path }})
{% endfor %}
```

Use it:

```bash
python3 scripts/generate_index_v2.py --template docs/templates/minimal.md.j2
```

## Examples

### Generate All Indexes

```bash
cd /path/to/trading-bot-open-source
python3 scripts/generate_index_v2.py
```

Output:
```
Generated: docs/domains/1_trading/INDEX.md
Generated: docs/domains/1_trading/strategies/INDEX.md
Generated: docs/domains/2_architecture/INDEX.md
Generated: docs/domains/2_architecture/execution/INDEX.md
...
```

### Preview Changes

```bash
python3 scripts/generate_index_v2.py --dry-run
```

Output:
```
Would write: docs/domains/1_trading/INDEX.md
Would write: docs/domains/1_trading/strategies/INDEX.md
...
```

### Process Specific Subdomain

```bash
python3 scripts/generate_index_v2.py --root docs/domains/2_architecture/webapp
```

Processes only the `webapp` subdomain and its children.

### Shallow Processing

```bash
python3 scripts/generate_index_v2.py --max-depth 1
```

Processes only domain-level and first-level subdirectories.

## Excluded Directories

The script automatically skips:
- `assets/` - Asset directories
- `__pycache__/` - Python cache
- `.git/` - Git directory
- `INDEX.md` - Existing index files (to avoid infinite loops)

## Integration with CI/CD

### Pre-commit Hook

Add to `config/pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: generate-index
      name: Generate documentation indexes
      entry: python3 scripts/generate_index_v2.py
      language: system
      pass_filenames: false
      files: ^docs/domains/.*\.md$
```

### GitHub Actions

Add to `.github/workflows/docs.yml`:

```yaml
name: Documentation

on:
  pull_request:
    paths:
      - 'docs/domains/**/*.md'

jobs:
  generate-indexes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements/requirements-dev.txt
      - run: python3 scripts/generate_index_v2.py --dry-run
```

## Troubleshooting

### Missing Dependencies

**Error**: `Missing dependency: jinja2`

**Solution**:
```bash
pip install jinja2 pyyaml
```

### Invalid Front Matter

**Symptom**: Documents not appearing in index

**Solution**: Ensure front matter is valid YAML:
```markdown
---
title: Valid Title
description: Valid description
---
```

### Empty Indexes

**Symptom**: INDEX.md files are not generated

**Cause**: No markdown files with front matter found

**Solution**: Add front matter to at least one `.md` file in the directory

### Template Errors

**Error**: `TemplateNotFound` or `TemplateSyntaxError`

**Solution**: Verify template path and Jinja2 syntax:
```bash
python3 scripts/generate_index_v2.py --template docs/templates/index-template.md.j2
```

## Comparison with v1

| Feature | v1 (generate_index.py) | v2 (generate_index_v2.py) |
|---------|------------------------|---------------------------|
| Domain-level indexes | ✅ | ✅ |
| Subdirectory indexes | ❌ | ✅ |
| Jinja2 templates | ❌ | ✅ |
| Custom templates | ❌ | ✅ |
| Subdirectory linking | ❌ | ✅ |
| Recursion depth control | ❌ | ✅ |
| Dry-run mode | ✅ | ✅ |

## Related Documentation

- [DOCUMENTATION-GUIDE-FOR-AGENTS.md](../../DOCUMENTATION-GUIDE-FOR-AGENTS.md) - Documentation standards
- [docs/templates/](../../templates/) - Template examples
- [CONTRIBUTING.md](../../../CONTRIBUTING.md) - Contribution guidelines

## Maintainers

- **Script**: `scripts/generate_index_v2.py`
- **Tests**: `tests/test_generate_index_v2.py`
- **Template**: `docs/templates/index-template.md.j2`
- **Issue**: [#52](https://github.com/realisonsdotcom/trading-bot-open-source/issues/52)

---

**Last Updated**: 2026-01-07  
**Version**: 2.0.0  
**License**: Same as project license
