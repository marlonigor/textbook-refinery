"""Testes do comando de inicialização compartilhado com a interface gráfica."""

from pathlib import Path

from typer.testing import CliRunner

from adaptbook.cli import app


def test_initializes_workspace_from_cli(tmp_path: Path) -> None:
    source_pdf = tmp_path / "livro.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")

    result = CliRunner().invoke(app, ["init", str(source_pdf)])

    assert result.exit_code == 0
    assert "Área de trabalho criada" in result.stdout


def test_reports_invalid_input_from_cli(tmp_path: Path) -> None:
    source_file = tmp_path / "livro.txt"
    source_file.write_text("conteúdo", encoding="utf-8")

    result = CliRunner().invoke(app, ["init", str(source_file)])

    assert result.exit_code == 2
    assert "esperado um PDF" in result.stderr
