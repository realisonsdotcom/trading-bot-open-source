#!/usr/bin/env python3
"""Validate YAML front matter metadata in docs/domains markdown files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("Missing dependency: pyyaml. Install with `pip install pyyaml`.") from exc

REQUIRED_FIELDS = {
    "domain",
    "title",
    "description",
    "keywords",
    "last_updated",
}

FIELD_ALIASES = {
    "last_updated": ["last_updated", "last-updated"],
}

VALID_DOMAINS = {
    "1_trading",
    "2_architecture",
    "3_operations",
    "4_security",
    "5_community",
    "6_quality",
    "7_standards",
}

VALID_STATUSES = {"draft", "review", "published", "deprecated"}

YAML_PATTERN = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
LINK_PATTERN = re.compile(r"!?\[[^\]]+\]\(([^)]+)\)")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:")


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
    if domain is not None:
        if domain not in VALID_DOMAINS:
            errors.append(f"Invalid domain: {domain}")
        else:
            # Check if domain matches directory
            parts = path.parts
            if "domains" in parts:
                idx = parts.index("domains")
                if len(parts) > idx + 1:
                    expected_domain = parts[idx + 1]
                    if domain != expected_domain:
                        errors.append(f"Domain mismatch: '{domain}' field does not match directory '{expected_domain}'")

    status = _get_field(metadata, "status")
    if status is not None and status not in VALID_STATUSES:
        errors.append(f"Invalid status: {status}")

    keywords = _get_field(metadata, "keywords")
    if keywords is not None and not isinstance(keywords, str):
        errors.append("'keywords' must be a comma-separated string")

    last_updated = _get_field(metadata, "last_updated")
    if last_updated is not None:
        value = str(last_updated)
        if not DATE_PATTERN.match(value):
            errors.append("'last_updated' must be in YYYY-MM-DD format")

    return errors


def _strip_link_target(target: str) -> str:
    target = target.split("#", 1)[0]
    target = target.split("?", 1)[0]
    return target.strip()


def _is_external_target(target: str) -> bool:
    return target.startswith(EXTERNAL_PREFIXES) or "://" in target


def _validate_related_links(path: Path, metadata: dict) -> list[str]:
    errors: list[str] = []
    related = metadata.get("related")
    if related is None:
        return errors
    if not isinstance(related, list):
        return ["'related' must be a list of relative paths"]
    for rel in related:
        if not isinstance(rel, str):
            errors.append("Related entry must be a string path")
            continue
        rel_target = _strip_link_target(rel)
        if not rel_target or rel_target.startswith("#") or _is_external_target(rel_target):
            continue
        rel_path = (path.parent / rel_target).resolve()
        if not rel_path.exists():
            errors.append(f"Broken related link: {rel}")
    return errors


def _validate_markdown_links(path: Path, content: str) -> list[str]:
    errors: list[str] = []
    for match in LINK_PATTERN.finditer(content):
        target = match.group(1).strip()
        if not target or target.startswith("#") or _is_external_target(target):
            continue
        target = _strip_link_target(target)
        if not target:
            continue
        target_path = (path.parent / target).resolve()
        if not target_path.exists():
            errors.append(f"Broken markdown link: {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate YAML metadata and optionally validate doc links.",
    )
    parser.add_argument("--root", default="docs/domains", help="Docs domains root directory")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Validate related and markdown links (fails on broken links).",
    )
    args = parser.parse_args()

    docs_dir = Path(args.root)
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
        if args.strict:
            errors.extend(_validate_related_links(md_file, metadata))
            content = md_file.read_text(encoding="utf-8")
            errors.extend(_validate_markdown_links(md_file, content))
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
