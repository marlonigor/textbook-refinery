"""Testes da primeira experiência visual da aplicação."""

import tkinter as tk
from collections.abc import Generator
from datetime import UTC, datetime
from pathlib import Path

import pytest

from adaptbook.gui.application import AdaptbookDesktopApplication
from adaptbook.workspace import BookWorkspaceInitializer


class FakePdfPathSelector:
    """Fornece um caminho conhecido sem abrir um diálogo nativo."""

    def __init__(self, source_pdf: Path | None) -> None:
        self._source_pdf = source_pdf

    def select_pdf(self) -> Path | None:
        """Retorna o valor preparado pelo teste."""

        return self._source_pdf


class FakeUserNotifier:
    """Registra mensagens de erro sem depender de uma caixa de diálogo."""

    def __init__(self) -> None:
        self.messages: list[tuple[str, str]] = []

    def show_error(self, title: str, message: str) -> None:
        """Guarda a mensagem exibida pela aplicação."""

        self.messages.append((title, message))


class FakeWorkspaceOpener:
    """Registra a abertura de pastas sem iniciar o Explorador do Windows."""

    def __init__(self) -> None:
        self.opened_paths: list[Path] = []

    def open_workspace(self, workspace_path: Path) -> None:
        """Guarda o caminho solicitado pela interface."""

        self.opened_paths.append(workspace_path)


@pytest.fixture(scope="module")
def root() -> Generator[tk.Tk]:
    """Fornece uma janela oculta para testar widgets nativos."""

    window = tk.Tk()
    window.withdraw()
    yield window
    window.destroy()


def test_shows_created_workspace_after_pdf_selection(root: tk.Tk, tmp_path: Path) -> None:
    source_pdf = tmp_path / "livro.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")
    opener = FakeWorkspaceOpener()
    application = _application(root, source_pdf, opener=opener)

    application.select_pdf()
    application.open_workspace()

    assert "Área de trabalho criada" in application.status_message
    assert application.step_message == "Etapa 1 de 5 concluída: Livro."
    assert application.workspace_message.endswith("trabalho\\livro")
    assert opener.opened_paths[0].name == "livro"


def test_shows_error_for_invalid_selection(root: tk.Tk, tmp_path: Path) -> None:
    invalid_file = tmp_path / "livro.txt"
    invalid_file.write_text("não é PDF", encoding="utf-8")
    notifier = FakeUserNotifier()
    application = _application(root, invalid_file, notifier)

    application.select_pdf()

    assert application.status_message == "Não foi possível criar a área de trabalho."
    assert notifier.messages[0][0] == "Adaptbook"


def test_enters_and_exits_event_loop(root: tk.Tk, tmp_path: Path) -> None:
    application = _application(root, tmp_path / "livro.pdf")
    root.after(0, root.quit)

    application.run()

    assert application.status_message == "Selecione um PDF para começar."


def _application(
    root: tk.Tk,
    source_pdf: Path | None,
    notifier: FakeUserNotifier | None = None,
    opener: FakeWorkspaceOpener | None = None,
) -> AdaptbookDesktopApplication:
    return AdaptbookDesktopApplication(
        root,
        BookWorkspaceInitializer(clock=_fixed_clock),
        FakePdfPathSelector(source_pdf),
        notifier or FakeUserNotifier(),
        opener or FakeWorkspaceOpener(),
    )


def _fixed_clock() -> datetime:
    return datetime(2026, 11, 26, 12, 0, tzinfo=UTC)
