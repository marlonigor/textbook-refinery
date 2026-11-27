"""Testes do início seguro de uma área de trabalho de livro."""

from datetime import UTC, datetime
from pathlib import Path

import pytest

from adaptbook.workspace import BookWorkspaceInitializer, WorkspaceValidationError


def test_creates_workspace_without_modifying_source_pdf(tmp_path: Path) -> None:
    source_pdf = tmp_path / "Espanhol A2.pdf"
    source_bytes = b"%PDF-1.4\ntexto de teste"
    source_pdf.write_bytes(source_bytes)

    workspace = BookWorkspaceInitializer(clock=_fixed_clock).initialize(source_pdf)

    assert source_pdf.read_bytes() == source_bytes
    assert workspace.configuration_path.exists()
    assert workspace.manifest_path.exists()
    assert workspace.root == tmp_path / "trabalho" / "espanhol-a2"


def test_rejects_file_without_pdf_extension(tmp_path: Path) -> None:
    source_file = tmp_path / "livro.txt"
    source_file.write_text("conteúdo", encoding="utf-8")

    with pytest.raises(WorkspaceValidationError, match="PDF"):
        BookWorkspaceInitializer(clock=_fixed_clock).initialize(source_file)


def test_rejects_existing_workspace_without_overwriting_files(tmp_path: Path) -> None:
    source_pdf = tmp_path / "livro.pdf"
    workspace_root = tmp_path / "trabalho" / "livro"
    source_pdf.write_bytes(b"%PDF-1.4")
    workspace_root.mkdir(parents=True)
    marker = workspace_root / "preservar.txt"
    marker.write_text("não sobrescrever", encoding="utf-8")

    with pytest.raises(WorkspaceValidationError, match="já existe"):
        BookWorkspaceInitializer(clock=_fixed_clock).initialize(source_pdf)

    assert marker.read_text(encoding="utf-8") == "não sobrescrever"


def _fixed_clock() -> datetime:
    return datetime(2026, 11, 26, 12, 0, tzinfo=UTC)
