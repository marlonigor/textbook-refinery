"""Ponto de entrada para iniciar a interface gráfica diretamente."""

from adaptbook.gui.application import run_desktop_application


def main() -> None:
    """Inicia a janela do Adaptbook.

    Exemplo: ``python -m adaptbook.gui``.
    """

    run_desktop_application()


if __name__ == "__main__":
    main()
