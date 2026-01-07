#!/usr/bin/env python3
"""Generate domain INDEX.md files from YAML metadata in docs/domains."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("Missing dependency: pyyaml. Install with `pip install pyyaml`.") from exc

DOMAIN_ORDER = [
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
]

YAML_START = "---\n"
YAML_END = "---\n"


def _extract_front_matter(path: Path) -> dict | None:
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


def _collect_docs(domain_dir: Path) -> list[tuple[Path, dict]]:
    docs: list[tuple[Path, dict]] = []
    for md_file in sorted(domain_dir.rglob("*.md")):
        if md_file.name == "INDEX.md":
            continue
        metadata = _extract_front_matter(md_file)
        if not metadata:
            continue
        docs.append((md_file, metadata))
    return docs


def _title_for_doc(metadata: dict, fallback: str) -> str:
    title = metadata.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()
    return fallback


def _description_for_doc(metadata: dict) -> str:
    description = metadata.get("description")
    if isinstance(description, str):
        return description.strip()
    return ""


def _domain_header(domain: str) -> str:
    label = domain.replace("_", " ").title()
    return (
        f"---\n"
        f"domain: {domain}\n"
        f"title: {label} Domain Index\n"
        f"description: Auto-generated index for {domain}.\n"
        f"keywords: {domain}\n"
        f"last_updated: AUTO\n"
        f"---\n\n"
        f"# {label} Domain Index\n\n"
        f"> Auto-generated. Do not edit manually.\n\n"
        f"## Documents\n\n"
    )


def _format_doc_entry(doc_path: Path, metadata: dict, domain_dir: Path) -> str:
    title = _title_for_doc(metadata, doc_path.stem.replace("-", " ").title())
    description = _description_for_doc(metadata)
    rel_path = doc_path.relative_to(domain_dir).as_posix()
    if description:
        return f"- [{title}]({rel_path}) - {description}\n"
    return f"- [{title}]({rel_path})\n"


def _write_index(domain_dir: Path, docs: list[tuple[Path, dict]], dry_run: bool) -> None:
    if not docs:
        return
    content = _domain_header(domain_dir.name)
    for doc_path, metadata in docs:
        content += _format_doc_entry(doc_path, metadata, domain_dir)
    index_path = domain_dir / "INDEX.md"
    if dry_run:
        print(f"Would write: {index_path}")
        return
    index_path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate domain INDEX.md files from metadata.")
    parser.add_argument("--root", default="docs/domains", help="Docs domains root directory")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"Directory not found: {root}")
        return 1

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
        docs = _collect_docs(domain_dir)
        _write_index(domain_dir, docs, args.dry_run)

    return 0


if __name__ == "__main__":
    sys.exit(main())
