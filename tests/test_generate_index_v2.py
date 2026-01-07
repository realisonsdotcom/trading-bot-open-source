"""Tests for scripts/generate_index_v2.py."""

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent

import pytest

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from generate_index_v2 import (
    _collect_docs,
    _collect_subdirectories,
    _extract_front_matter,
    _get_domain_name,
    _load_template,
    main,
)


@pytest.fixture
def temp_docs_dir(tmp_path: Path) -> Path:
    """Create temporary docs directory structure."""
    docs = tmp_path / "docs" / "domains"
    docs.mkdir(parents=True)
    return docs


@pytest.fixture
def sample_doc_with_metadata(tmp_path: Path) -> Path:
    """Create a sample markdown file with front matter."""
    doc = tmp_path / "sample.md"
    content = dedent("""
        ---
        title: Sample Document
        description: A sample document for testing
        keywords: test, sample
        ---
        
        # Sample Document
        
        This is a test.
    """).strip()
    doc.write_text(content, encoding="utf-8")
    return doc


@pytest.fixture
def sample_doc_without_metadata(tmp_path: Path) -> Path:
    """Create a markdown file without front matter."""
    doc = tmp_path / "no-metadata.md"
    doc.write_text("# No Metadata\n\nJust content.", encoding="utf-8")
    return doc


class TestExtractFrontMatter:
    """Tests for _extract_front_matter function."""

    def test_extract_valid_front_matter(self, sample_doc_with_metadata: Path) -> None:
        """Should extract valid YAML front matter."""
        metadata = _extract_front_matter(sample_doc_with_metadata)
        assert metadata is not None
        assert metadata["title"] == "Sample Document"
        assert metadata["description"] == "A sample document for testing"
        assert metadata["keywords"] == "test, sample"

    def test_extract_no_front_matter(self, sample_doc_without_metadata: Path) -> None:
        """Should return None when no front matter exists."""
        metadata = _extract_front_matter(sample_doc_without_metadata)
        assert metadata is None

    def test_extract_invalid_yaml(self, tmp_path: Path) -> None:
        """Should return None for invalid YAML."""
        doc = tmp_path / "bad.md"
        doc.write_text("---\ntitle: [unclosed\n---\nContent", encoding="utf-8")
        metadata = _extract_front_matter(doc)
        assert metadata is None

    def test_extract_non_dict_yaml(self, tmp_path: Path) -> None:
        """Should return None if YAML is not a dict."""
        doc = tmp_path / "list.md"
        doc.write_text("---\n- item1\n- item2\n---\nContent", encoding="utf-8")
        metadata = _extract_front_matter(doc)
        assert metadata is None


class TestCollectDocs:
    """Tests for _collect_docs function."""

    def test_collect_docs_with_metadata(self, tmp_path: Path) -> None:
        """Should collect documents with metadata."""
        directory = tmp_path / "test_dir"
        directory.mkdir()
        
        doc1 = directory / "doc1.md"
        doc1.write_text("---\ntitle: Doc 1\ndescription: First doc\n---\nContent", encoding="utf-8")
        
        doc2 = directory / "doc2.md"
        doc2.write_text("---\ntitle: Doc 2\n---\nContent", encoding="utf-8")
        
        docs = _collect_docs(directory)
        assert len(docs) == 2
        assert docs[0]["title"] == "Doc 1"
        assert docs[0]["description"] == "First doc"
        assert docs[1]["title"] == "Doc 2"
        assert docs[1]["description"] == ""

    def test_collect_docs_skip_index(self, tmp_path: Path) -> None:
        """Should skip INDEX.md files."""
        directory = tmp_path / "test_dir"
        directory.mkdir()
        
        index = directory / "INDEX.md"
        index.write_text("---\ntitle: Index\n---\nIndex content", encoding="utf-8")
        
        doc = directory / "doc.md"
        doc.write_text("---\ntitle: Doc\n---\nContent", encoding="utf-8")
        
        docs = _collect_docs(directory)
        assert len(docs) == 1
        assert docs[0]["title"] == "Doc"

    def test_collect_docs_no_metadata(self, tmp_path: Path) -> None:
        """Should skip documents without front matter."""
        directory = tmp_path / "test_dir"
        directory.mkdir()
        
        doc = directory / "no-meta.md"
        doc.write_text("# No Metadata\nContent", encoding="utf-8")
        
        docs = _collect_docs(directory)
        assert len(docs) == 0

    def test_collect_docs_fallback_title(self, tmp_path: Path) -> None:
        """Should use filename as fallback title."""
        directory = tmp_path / "test_dir"
        directory.mkdir()
        
        doc = directory / "my-great-doc.md"
        doc.write_text("---\ndescription: Test\n---\nContent", encoding="utf-8")
        
        docs = _collect_docs(directory)
        assert len(docs) == 1
        assert docs[0]["title"] == "My Great Doc"


class TestCollectSubdirectories:
    """Tests for _collect_subdirectories function."""

    def test_collect_subdirectories_with_index(self, tmp_path: Path) -> None:
        """Should collect subdirectories with INDEX.md metadata."""
        directory = tmp_path / "test_dir"
        directory.mkdir()
        
        subdir = directory / "subdir1"
        subdir.mkdir()
        index = subdir / "INDEX.md"
        index.write_text("---\ntitle: Subdir 1\ndescription: First subdir\n---\nContent", encoding="utf-8")
        
        subdirs = _collect_subdirectories(directory)
        assert len(subdirs) == 1
        assert subdirs[0]["name"] == "Subdir 1"
        assert subdirs[0]["description"] == "First subdir"
        assert subdirs[0]["path"] == "subdir1/INDEX.md"

    def test_collect_subdirectories_no_index(self, tmp_path: Path) -> None:
        """Should use directory name as fallback."""
        directory = tmp_path / "test_dir"
        directory.mkdir()
        
        subdir = directory / "my_subdir"
        subdir.mkdir()
        
        subdirs = _collect_subdirectories(directory)
        assert len(subdirs) == 1
        assert subdirs[0]["name"] == "My Subdir"
        assert subdirs[0]["description"] == ""

    def test_collect_subdirectories_skip_assets(self, tmp_path: Path) -> None:
        """Should skip assets and special directories."""
        directory = tmp_path / "test_dir"
        directory.mkdir()
        
        (directory / "assets").mkdir()
        (directory / "__pycache__").mkdir()
        (directory / ".git").mkdir()
        
        subdir = directory / "valid"
        subdir.mkdir()
        
        subdirs = _collect_subdirectories(directory)
        assert len(subdirs) == 1
        assert subdirs[0]["name"] == "Valid"


class TestGetDomainName:
    """Tests for _get_domain_name function."""

    def test_get_domain_name_top_level(self, tmp_path: Path) -> None:
        """Should extract top-level domain name."""
        root = tmp_path / "domains"
        root.mkdir()
        domain = root / "1_trading"
        domain.mkdir()
        
        result = _get_domain_name(domain, root)
        assert result == "1_trading"

    def test_get_domain_name_nested(self, tmp_path: Path) -> None:
        """Should extract domain from nested directory."""
        root = tmp_path / "domains"
        root.mkdir()
        domain = root / "2_architecture"
        domain.mkdir()
        subdir = domain / "execution"
        subdir.mkdir()
        
        result = _get_domain_name(subdir, root)
        assert result == "2_architecture"

    def test_get_domain_name_fallback(self, tmp_path: Path) -> None:
        """Should use directory name as fallback."""
        directory = tmp_path / "standalone"
        directory.mkdir()
        
        result = _get_domain_name(directory, tmp_path)
        assert result == "standalone"


class TestLoadTemplate:
    """Tests for _load_template function."""

    def test_load_template_from_file(self, tmp_path: Path) -> None:
        """Should load template from file."""
        template_file = tmp_path / "custom.j2"
        template_file.write_text("# {{ title }}", encoding="utf-8")
        
        template = _load_template(template_file)
        result = template.render(title="Test")
        assert result == "# Test"

    def test_load_template_default(self) -> None:
        """Should use default template when file doesn't exist."""
        template = _load_template(None)
        result = template.render(
            domain="test",
            title="Test",
            description="Test desc",
            keywords="test",
            last_updated="2026-01-07",
            documents=[],
            subdirectories=[],
        )
        assert "# Test" in result
        assert "Auto-generated" in result


class TestMainFunction:
    """Tests for main function."""

    def test_main_dry_run(self, temp_docs_dir: Path, capsys, monkeypatch) -> None:
        """Should run in dry-run mode without writing files."""
        domain = temp_docs_dir / "1_trading"
        domain.mkdir()
        
        doc = domain / "test.md"
        doc.write_text("---\ntitle: Test\n---\nContent", encoding="utf-8")
        
        monkeypatch.setattr(sys, "argv", [
            "generate_index_v2.py",
            "--root", str(temp_docs_dir),
            "--dry-run",
        ])
        
        exit_code = main()
        assert exit_code == 0
        
        captured = capsys.readouterr()
        assert "Would write" in captured.out
        assert not (domain / "INDEX.md").exists()

    def test_main_generate_index(self, temp_docs_dir: Path, monkeypatch) -> None:
        """Should generate INDEX.md files."""
        domain = temp_docs_dir / "1_trading"
        domain.mkdir()
        
        doc = domain / "test.md"
        doc.write_text("---\ntitle: Test Doc\ndescription: Testing\n---\nContent", encoding="utf-8")
        
        monkeypatch.setattr(sys, "argv", [
            "generate_index_v2.py",
            "--root", str(temp_docs_dir),
        ])
        
        exit_code = main()
        assert exit_code == 0
        
        index = domain / "INDEX.md"
        assert index.exists()
        
        content = index.read_text(encoding="utf-8")
        assert "Test Doc" in content
        assert "Testing" in content

    def test_main_recursive(self, temp_docs_dir: Path, monkeypatch) -> None:
        """Should recursively generate indexes for subdirectories."""
        domain = temp_docs_dir / "2_architecture"
        domain.mkdir()
        
        subdir = domain / "execution"
        subdir.mkdir()
        
        doc = subdir / "router.md"
        doc.write_text("---\ntitle: Router\n---\nContent", encoding="utf-8")
        
        monkeypatch.setattr(sys, "argv", [
            "generate_index_v2.py",
            "--root", str(temp_docs_dir),
        ])
        
        exit_code = main()
        assert exit_code == 0
        
        assert (domain / "INDEX.md").exists()
        assert (subdir / "INDEX.md").exists()

    def test_main_custom_template(self, temp_docs_dir: Path, tmp_path: Path, monkeypatch) -> None:
        """Should use custom template."""
        domain = temp_docs_dir / "1_trading"
        domain.mkdir()
        
        doc = domain / "test.md"
        doc.write_text("---\ntitle: Test\n---\nContent", encoding="utf-8")
        
        template_file = tmp_path / "custom.j2"
        template_file.write_text("CUSTOM: {{ title }}", encoding="utf-8")
        
        monkeypatch.setattr(sys, "argv", [
            "generate_index_v2.py",
            "--root", str(temp_docs_dir),
            "--template", str(template_file),
        ])
        
        exit_code = main()
        assert exit_code == 0
        
        index = domain / "INDEX.md"
        content = index.read_text(encoding="utf-8")
        assert "CUSTOM:" in content

    def test_main_missing_root(self, tmp_path: Path, monkeypatch, capsys) -> None:
        """Should handle missing root directory."""
        monkeypatch.setattr(sys, "argv", [
            "generate_index_v2.py",
            "--root", str(tmp_path / "nonexistent"),
        ])
        
        exit_code = main()
        assert exit_code == 1
        
        captured = capsys.readouterr()
        assert "Directory not found" in captured.out

    def test_main_max_depth(self, temp_docs_dir: Path, monkeypatch) -> None:
        """Should respect max-depth parameter."""
        domain = temp_docs_dir / "1_trading"
        domain.mkdir()
        
        level1 = domain / "level1"
        level1.mkdir()
        
        level2 = level1 / "level2"
        level2.mkdir()
        
        doc = level2 / "test.md"
        doc.write_text("---\ntitle: Test\n---\nContent", encoding="utf-8")
        
        monkeypatch.setattr(sys, "argv", [
            "generate_index_v2.py",
            "--root", str(temp_docs_dir),
            "--max-depth", "1",
        ])
        
        exit_code = main()
        assert exit_code == 0
        
        assert (domain / "INDEX.md").exists()
        assert (level1 / "INDEX.md").exists()
        assert not (level2 / "INDEX.md").exists()  # Beyond max depth
