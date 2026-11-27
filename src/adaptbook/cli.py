"""Comandos da linha de comando que compartilham a lógica da interface gráfica."""

from pathlib import Path
from typing import Annotated

import typer

from adaptbook.gui.application import run_desktop_application
from adaptbook.workspace import BookWorkspaceInitializer, WorkspaceValidationError

app = typer.Typer(help="Cria textbooks autossuficientes para estudo local.", no_args_is_help=True)


@app.command()
def init(source_pdf: Annotated[Path, typer.Argument(help="PDF do livro a preparar.")]) -> None:
    """Cria uma área de trabalho sem modificar o PDF de entrada.

    Exemplo: ``adaptbook init livro.pdf``.
    """

    try:
        workspace = BookWorkspaceInitializer().initialize(source_pdf)
    except WorkspaceValidationError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=2) from error
    typer.echo(f"Área de trabalho criada: {workspace.root}")


@app.command()
def gui() -> None:
    """Abre a aplicação gráfica local.

    Exemplo: ``adaptbook gui``.
    """

    run_desktop_application()
