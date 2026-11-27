"""Criação segura e reproduzível da pasta de trabalho de um livro."""

import json
import re
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import yaml

from adaptbook.configuration import AdaptbookConfiguration, create_initial_configuration

Clock = Callable[[], datetime]


class WorkspaceValidationError(ValueError):
    """Indica que uma área de trabalho não pode ser criada com segurança.

    Exemplo: ``raise WorkspaceValidationError("arquivo inválido")``.
    """


@dataclass(frozen=True, slots=True)
class BookWorkspace:
    """Expõe os caminhos estáveis de uma execução de livro.

    Exemplo: ``workspace.configuration_path``.
    """

    root: Path
    configuration_path: Path
    manifest_path: Path


class BookWorkspaceInitializer:
    """Cria uma área isolada sem alterar o PDF de entrada.

    Exemplo: ``BookWorkspaceInitializer().initialize(Path("livro.pdf"))``.
    """

    def __init__(self, clock: Clock | None = None) -> None:
        self._clock = clock or _current_time

    def initialize(self, source_pdf: Path) -> BookWorkspace:
        """Valida o PDF e cria arquivos iniciais de forma atômica.

        Exemplo: ``initializer.initialize(Path("livro.pdf"))``.
        """

        normalized_source = _validate_source_pdf(source_pdf)
        workspace_root = _workspace_root(normalized_source)
        _assert_workspace_is_new(workspace_root)
        _create_workspace_directories(workspace_root)
        workspace = _workspace_paths(workspace_root)
        _write_configuration(workspace.configuration_path, normalized_source)
        _write_manifest(workspace.manifest_path, normalized_source, self._clock())
        return workspace


def _current_time() -> datetime:
    return datetime.now(UTC)


def _validate_source_pdf(source_pdf: Path) -> Path:
    normalized_source = source_pdf.expanduser().resolve()
    if normalized_source.suffix.casefold() != ".pdf":
        raise WorkspaceValidationError(f"Arquivo inválido: recebido {source_pdf}; esperado um PDF.")
    if not normalized_source.is_file():
        raise WorkspaceValidationError(
            f"Arquivo inválido: recebido {source_pdf}; esperado um PDF existente."
        )
    return normalized_source


def _workspace_root(source_pdf: Path) -> Path:
    return source_pdf.parent / "trabalho" / _workspace_name(source_pdf.stem)


def _workspace_name(book_stem: str) -> str:
    normalized_name = unicodedata.normalize("NFKD", book_stem)
    ascii_name = normalized_name.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", ascii_name.casefold()).strip("-") or "livro"


def _assert_workspace_is_new(workspace_root: Path) -> None:
    if workspace_root.exists():
        expected_state = "um destino ainda não utilizado"
        message = f"Área de trabalho já existe: {workspace_root}; esperado {expected_state}."
        raise WorkspaceValidationError(message)


def _create_workspace_directories(workspace_root: Path) -> None:
    for relative_path in _workspace_directories():
        (workspace_root / relative_path).mkdir(parents=True, exist_ok=False)


def _workspace_directories() -> tuple[Path, ...]:
    return (Path("."), *(Path(name) for name in ("01_ingestao", "02_mapa", "logs")))


def _workspace_paths(workspace_root: Path) -> BookWorkspace:
    return BookWorkspace(
        root=workspace_root,
        configuration_path=workspace_root / "config.yaml",
        manifest_path=workspace_root / "manifesto.json",
    )


def _write_configuration(configuration_path: Path, source_pdf: Path) -> None:
    configuration = create_initial_configuration(source_pdf)
    _write_yaml_atomically(configuration_path, configuration)


def _write_yaml_atomically(path: Path, configuration: AdaptbookConfiguration) -> None:
    contents = yaml.safe_dump(
        configuration.model_dump(by_alias=True), allow_unicode=True, sort_keys=False
    )
    _write_text_atomically(path, contents)


def _write_manifest(path: Path, source_pdf: Path, created_at: datetime) -> None:
    manifest = _manifest_contents(source_pdf, created_at)
    _write_text_atomically(path, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


def _manifest_contents(source_pdf: Path, created_at: datetime) -> dict[str, str | int]:
    return {
        "versao_esquema": 1,
        "arquivo_origem": str(source_pdf),
        "criado_em": created_at.isoformat(),
        "status_execucao": "inicializado",
    }


def _write_text_atomically(path: Path, contents: str) -> None:
    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    temporary_path.write_text(contents, encoding="utf-8")
    temporary_path.replace(path)
