"""Janela inicial para criar áreas de trabalho de textbooks."""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Protocol

from adaptbook.workspace import BookWorkspace, BookWorkspaceInitializer, WorkspaceValidationError


class PdfPathSelector(Protocol):
    """Define a seleção de PDF para tornar a interface testável.

    Exemplo: ``selector.select_pdf()``.
    """

    def select_pdf(self) -> Path | None:
        """Retorna o PDF escolhido ou ``None`` em caso de cancelamento.

        Exemplo: ``Path("livro.pdf")``.
        """


class UserNotifier(Protocol):
    """Define a notificação de erros mostrada à pessoa usuária.

    Exemplo: ``notifier.show_error("Adaptbook", "erro")``.
    """

    def show_error(self, title: str, message: str) -> None:
        """Exibe um erro sem acoplar a regra de negócio ao Tkinter.

        Exemplo: ``notifier.show_error("Adaptbook", "PDF inválido")``.
        """


class TkPdfPathSelector:
    """Abre o seletor nativo de arquivos do Windows.

    Exemplo: ``TkPdfPathSelector().select_pdf()``.
    """

    def select_pdf(self) -> Path | None:
        """Converte a escolha nativa em caminho tipado.

        Exemplo: ``Path("C:/livro.pdf")``.
        """

        selected_file = filedialog.askopenfilename(
            filetypes=(("PDF", "*.pdf"), ("Todos os arquivos", "*.*"))
        )
        return Path(selected_file) if selected_file else None


class TkUserNotifier:
    """Mostra erros da aplicação em caixas nativas.

    Exemplo: ``TkUserNotifier(root).show_error("Adaptbook", "erro")``.
    """

    def __init__(self, root: tk.Tk) -> None:
        self._root = root

    def show_error(self, title: str, message: str) -> None:
        """Abre uma caixa de erro vinculada à janela principal.

        Exemplo: ``notifier.show_error("Adaptbook", "PDF inválido")``.
        """

        messagebox.showerror(title, message, parent=self._root)


class AdaptbookDesktopApplication:
    """Coordena a primeira tela gráfica do Adaptbook.

    Exemplo: ``AdaptbookDesktopApplication(root, initializer)``.
    """

    def __init__(
        self,
        root: tk.Tk,
        initializer: BookWorkspaceInitializer,
        selector: PdfPathSelector,
        notifier: UserNotifier,
    ) -> None:
        self._root = root
        self._initializer = initializer
        self._selector = selector
        self._notifier = notifier
        self._status = tk.StringVar(value="Selecione um PDF para começar.")
        self._workspace = tk.StringVar(value="Nenhuma área de trabalho criada.")
        self._configure_window()
        self._build_layout()

    def run(self) -> None:
        """Exibe a janela até que a pessoa a feche.

        Exemplo: ``application.run()``.
        """

        self._root.mainloop()

    @property
    def status_message(self) -> str:
        """Expõe a última mensagem de progresso para testes e acessibilidade.

        Exemplo: ``application.status_message``.
        """

        return self._status.get()

    @property
    def workspace_message(self) -> str:
        """Expõe o caminho informado pela interface após a inicialização.

        Exemplo: ``application.workspace_message``.
        """

        return self._workspace.get()

    def _configure_window(self) -> None:
        self._root.title("Adaptbook")
        self._root.configure(background="#F4F1EA")
        self._root.minsize(880, 560)
        self._configure_style()

    def _configure_style(self) -> None:
        style = ttk.Style(self._root)
        style.theme_use("clam")
        style.configure("Surface.TFrame", background="#FFFDF8")
        style.configure("Body.TFrame", background="#F4F1EA")
        self._configure_label_styles(style)
        self._configure_primary_button_style(style)

    def _configure_label_styles(self, style: ttk.Style) -> None:
        style.configure(
            "Title.TLabel",
            background="#FFFDF8",
            foreground="#18212B",
            font=("Segoe UI", 24, "bold"),
        )
        style.configure(
            "Body.TLabel", background="#FFFDF8", foreground="#18212B", font=("Segoe UI", 11)
        )
        style.configure(
            "Muted.TLabel", background="#FFFDF8", foreground="#52606D", font=("Segoe UI", 10)
        )

    def _configure_primary_button_style(self, style: ttk.Style) -> None:
        style.configure(
            "Primary.TButton",
            background="#176B87",
            foreground="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            padding=(20, 12),
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#12566E"), ("disabled", "#A6BFC9")],
            foreground=[("disabled", "#F4F1EA")],
        )

    def _build_layout(self) -> None:
        body = ttk.Frame(self._root, style="Body.TFrame", padding=32)
        body.grid(sticky="nsew")
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        self._build_steps(body)
        self._build_workspace_panel(body)

    def _build_steps(self, parent: ttk.Frame) -> None:
        steps = ttk.Frame(parent, style="Surface.TFrame", padding=24)
        steps.grid(row=0, column=0, sticky="nsw", padx=(0, 24))
        ttk.Label(steps, text="Etapas", style="Title.TLabel").grid(sticky="w")
        for index, label in enumerate(
            ("1. Livro", "2. Mapa", "3. Auditoria", "4. Adaptações", "5. PDF final")
        ):
            ttk.Label(steps, text=label, style="Body.TLabel").grid(
                row=index + 1, sticky="w", pady=(20, 0)
            )

    def _build_workspace_panel(self, parent: ttk.Frame) -> None:
        panel = ttk.Frame(parent, style="Surface.TFrame", padding=40)
        panel.grid(row=0, column=1, sticky="nsew")
        ttk.Label(panel, text="Comece pelo seu livro", style="Title.TLabel").grid(sticky="w")
        ttk.Label(panel, text="O PDF original não será alterado.", style="Body.TLabel").grid(
            sticky="w", pady=(12, 28)
        )
        button = ttk.Button(
            panel, text="Selecionar PDF do livro", style="Primary.TButton", command=self.select_pdf
        )
        button.grid(sticky="w")
        ttk.Label(panel, textvariable=self._status, style="Body.TLabel", wraplength=500).grid(
            sticky="w", pady=(28, 8)
        )
        ttk.Label(panel, textvariable=self._workspace, style="Muted.TLabel", wraplength=500).grid(
            sticky="w"
        )

    def select_pdf(self) -> None:
        """Cria a área de trabalho para o PDF escolhido na janela.

        Exemplo: ``application.select_pdf()``.
        """

        source_pdf = self._selector.select_pdf()
        if source_pdf is None:
            return
        self._initialize_workspace(source_pdf)

    def _initialize_workspace(self, source_pdf: Path) -> None:
        try:
            workspace = self._initializer.initialize(source_pdf)
        except WorkspaceValidationError as error:
            self._show_workspace_error(error)
            return
        self._show_workspace_success(workspace)

    def _show_workspace_error(self, error: WorkspaceValidationError) -> None:
        self._status.set("Não foi possível criar a área de trabalho.")
        self._notifier.show_error("Adaptbook", str(error))

    def _show_workspace_success(self, workspace: BookWorkspace) -> None:
        self._status.set(
            "Área de trabalho criada. A próxima etapa será mapear as páginas do livro."
        )
        self._workspace.set(str(workspace.root))


def run_desktop_application() -> None:
    """Abre a interface gráfica com as dependências reais de produção.

    Exemplo: ``run_desktop_application()``.
    """

    root = tk.Tk()
    application = AdaptbookDesktopApplication(
        root,
        BookWorkspaceInitializer(),
        TkPdfPathSelector(),
        TkUserNotifier(root),
    )
    application.run()
