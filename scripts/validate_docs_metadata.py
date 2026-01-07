#!/usr/bin/env python3
"""Validate YAML front matter metadata in docs/domains markdown files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("Missing dependency: pyyaml. Install with `pip install pyyaml`.") from exc

REQUIRED_FIELDS = {
    "domain",
    "responsible",
    "status",
    "last_updated",
}

FIELD_ALIASES = {
    "last_updated": ["last_updated", "last-updated"],
    "keywords": ["keywords", "tags"],
}

VALID_DOMAINS = {
    "1_trading",
    "2_execution",
    "3_operations",
    "4_platform",
    "5_webapp",
    "6_infrastructure",
    "7_standards",
    "2_architecture",
    "4_security",
    "5_community",
    "6_quality",
    "meta",
}

VALID_STATUSES = {"draft", "active", "deprecated", "archived"}

VALID_AGENTS = {
    "TradingAgent",
    "ExecutionAgent",
    "MonitoringAgent",
    "PlatformAgent",
    "WebAppAgent",
    "InfraAgent",
    "QualityAgent",
}

YAML_PATTERN = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _extract_front_matter(path: Path) -> dict | None:
    content = path.read_text(encoding="utf-8")
    match = YAML_PATTERN.match(content)
    if not match:
        return None
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    return data


def _get_field(metadata: dict, field: str) -> object | None:
    aliases = FIELD_ALIASES.get(field, [field])
    for key in aliases:
        if key in metadata:
            return metadata[key]
    return None


def _validate_metadata(path: Path, metadata: dict) -> list[str]:
    errors: list[str] = []

    for field in REQUIRED_FIELDS:
        if _get_field(metadata, field) is None:
            errors.append(f"Missing required field: {field}")

    domain = _get_field(metadata, "domain")
    if domain is not None and domain not in VALID_DOMAINS:
        errors.append(f"Invalid domain: {domain}")

    status = _get_field(metadata, "status")
    if status is not None and status not in VALID_STATUSES:
        errors.append(f"Invalid status: {status}")

    responsible = _get_field(metadata, "responsible")
    if responsible is not None:
        if not isinstance(responsible, list):
            errors.append("'responsible' must be a list")
        else:
            for agent in responsible:
                if agent not in VALID_AGENTS:
                    errors.append(f"Invalid agent: {agent}")

    keywords = _get_field(metadata, "keywords")
    if keywords is not None and not isinstance(keywords, list):
        errors.append("'keywords' must be a list")

    last_updated = _get_field(metadata, "last_updated")
    if last_updated is not None:
        value = str(last_updated)
        if not DATE_PATTERN.match(value):
            errors.append("'last_updated' must be in YYYY-MM-DD format")

    return errors


def main() -> int:
    docs_dir = Path("docs/domains")
    if not docs_dir.exists():
        print(f"Directory not found: {docs_dir}")
        return 1

    total_files = 0
    files_with_errors = 0

    for md_file in sorted(docs_dir.rglob("*.md")):
        total_files += 1
        print(f"{md_file}")
        metadata = _extract_front_matter(md_file)
        if metadata is None:
            print("  ERROR: Missing or invalid YAML front matter")
            files_with_errors += 1
            continue

        errors = _validate_metadata(md_file, metadata)
        if errors:
            files_with_errors += 1
            for error in errors:
                print(f"  ERROR: {error}")
        else:
            print("  OK")

    print("\nSummary:")
    print(f"  Total files: {total_files}")
    print(f"  Files with errors: {files_with_errors}")

    return 1 if files_with_errors else 0


if __name__ == "__main__":
    sys.exit(main())
