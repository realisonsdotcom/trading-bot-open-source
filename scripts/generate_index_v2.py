#!/usr/bin/env python3
"""Generate INDEX.md files recursively from YAML metadata in docs/domains.

Version 2: Supports subdirectories and Jinja2 templates.
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("Missing dependency: pyyaml. Install with `pip install pyyaml`.") from exc

try:
    from jinja2 import Environment, FileSystemLoader, Template
except ImportError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("Missing dependency: jinja2. Install with `pip install jinja2`.") from exc

DOMAIN_ORDER = [
    "1_trading",
    "2_architecture",
    "3_operations",
    "4_security",
    "5_community",
    "6_quality",
    "7_standards",
]

YAML_START = "---\n"
YAML_END = "---\n"

DEFAULT_TEMPLATE = """---
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
"""


def _extract_front_matter(path: Path) -> dict[str, Any] | None:
    """Extract YAML front matter from markdown file."""
    content = path.read_text(encoding="utf-8")
    if not content.startswith(YAML_START):
        return None
    try:
        _, rest = content.split(YAML_START, 1)
        yaml_block, _ = rest.split(YAML_END, 1)
    except ValueError:
        return None
    try:
        data = yaml.safe_load(yaml_block)
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    return data


def _collect_docs(directory: Path) -> list[dict[str, str]]:
    """Collect all markdown documents in the directory (non-recursive)."""
    docs: list[dict[str, str]] = []
    for md_file in sorted(directory.glob("*.md")):
        if md_file.name == "INDEX.md":
            continue
        metadata = _extract_front_matter(md_file)
        if not metadata:
            continue
        
        title = metadata.get("title", "").strip() or md_file.stem.replace("-", " ").title()
        description = metadata.get("description", "").strip()
        rel_path = md_file.name
        
        docs.append({
            "title": title,
            "description": description,
            "path": rel_path,
        })
    return docs


def _collect_subdirectories(directory: Path) -> list[dict[str, str]]:
    """Collect subdirectories with their INDEX.md metadata."""
    subdirs: list[dict[str, str]] = []
    for subdir in sorted(directory.iterdir()):
        if not subdir.is_dir():
            continue
        if subdir.name in ("assets", "__pycache__", ".git"):
            continue
        
        index_path = subdir / "INDEX.md"
        name = subdir.name.replace("_", " ").title()
        description = ""
        
        if index_path.exists():
            metadata = _extract_front_matter(index_path)
            if metadata:
                name = metadata.get("title", "").strip() or name
                description = metadata.get("description", "").strip()
        
        subdirs.append({
            "name": name,
            "description": description,
            "path": f"{subdir.name}/INDEX.md",
        })
    return subdirs


def _get_domain_name(directory: Path, root: Path) -> str:
    """Extract domain name from directory path."""
    try:
        rel_path = directory.relative_to(root)
        parts = rel_path.parts
        if parts:
            return parts[0]
    except ValueError:
        pass
    return directory.name


def _render_index(
    directory: Path,
    root: Path,
    template: Template,
    dry_run: bool,
) -> None:
    """Generate INDEX.md for a directory using Jinja2 template."""
    docs = _collect_docs(directory)
    subdirs = _collect_subdirectories(directory)
    
    # Skip if no content
    if not docs and not subdirs:
        return
    
    domain_name = _get_domain_name(directory, root)
    dir_name = directory.name.replace("_", " ").title()
    
    # Check if there's existing INDEX.md with metadata
    index_path = directory / "INDEX.md"
    existing_title = f"{dir_name} Index"
    existing_description = f"Auto-generated index for {directory.name}."
    existing_keywords = f"{directory.name}, index"
    
    if index_path.exists():
        metadata = _extract_front_matter(index_path)
        if metadata:
            existing_title = metadata.get("title", existing_title)
            existing_description = metadata.get("description", existing_description)
            existing_keywords = metadata.get("keywords", existing_keywords)
    
    context = {
        "domain": domain_name,
        "title": existing_title,
        "description": existing_description,
        "keywords": existing_keywords,
        "last_updated": date.today().isoformat(),
        "documents": docs,
        "subdirectories": subdirs,
    }
    
    content = template.render(**context)
    
    if dry_run:
        print(f"Would write: {index_path}")
        return
    
    index_path.write_text(content, encoding="utf-8")
    print(f"Generated: {index_path}")


def _process_directory_recursive(
    directory: Path,
    root: Path,
    template: Template,
    dry_run: bool,
    max_depth: int,
    current_depth: int = 0,
) -> None:
    """Recursively process directory and subdirectories."""
    if current_depth > max_depth:
        return
    
    # Generate index for current directory
    _render_index(directory, root, template, dry_run)
    
    # Process subdirectories
    for subdir in sorted(directory.iterdir()):
        if not subdir.is_dir():
            continue
        if subdir.name in ("assets", "__pycache__", ".git"):
            continue
        _process_directory_recursive(
            subdir,
            root,
            template,
            dry_run,
            max_depth,
            current_depth + 1,
        )


def _load_template(template_path: Path | None) -> Template:
    """Load Jinja2 template from file or use default."""
    if template_path and template_path.exists():
        env = Environment(loader=FileSystemLoader(template_path.parent))
        return env.get_template(template_path.name)
    return Template(DEFAULT_TEMPLATE)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate INDEX.md files recursively from metadata."
    )
    parser.add_argument(
        "--root",
        default="docs/domains",
        help="Docs domains root directory (default: docs/domains)",
    )
    parser.add_argument(
        "--template",
        type=Path,
        help="Path to Jinja2 template (default: built-in template)",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=10,
        help="Maximum recursion depth (default: 10)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without writing",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"Directory not found: {root}")
        return 1

    template = _load_template(args.template)

    # Process domains in order
    domains = [p for p in root.iterdir() if p.is_dir()]
    domains_sorted: list[Path] = []
    for name in DOMAIN_ORDER:
        candidate = root / name
        if candidate in domains:
            domains_sorted.append(candidate)
    for domain_dir in sorted(domains):
        if domain_dir not in domains_sorted:
            domains_sorted.append(domain_dir)

    for domain_dir in domains_sorted:
        _process_directory_recursive(
            domain_dir,
            root,
            template,
            args.dry_run,
            args.max_depth,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
