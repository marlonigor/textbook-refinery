"""Modelos da configuração local de cada livro."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class BookSettings(BaseModel):
    """Representa os dados editáveis do livro selecionado.

    Exemplo: ``BookSettings(file_name="espanhol.pdf", target_language="es", level="A2")``.
    """

    model_config = ConfigDict(populate_by_name=True)

    file_name: str = Field(serialization_alias="arquivo")
    target_language: str = Field(default="es", serialization_alias="idioma_alvo")
    level: str = Field(default="A2", serialization_alias="nivel")
    instruction_language: str = Field(
        default="igual_ao_livro", serialization_alias="idioma_instrucoes"
    )
    extra_transcripts: list[str] = Field(
        default_factory=list, serialization_alias="transcricoes_extra"
    )
    answer_key_pages: list[int] = Field(
        default_factory=list, serialization_alias="paginas_gabarito"
    )


class ModelSettings(BaseModel):
    """Mantém valores seguros antes de um provedor de modelo ser escolhido.

    Exemplo: ``ModelSettings()``.
    """

    model_config = ConfigDict(populate_by_name=True)

    provider: str = Field(default="pendente", serialization_alias="provedor")
    detection_temperature: float = Field(default=0.0, serialization_alias="temperatura_deteccao")
    generation_temperature: float = Field(default=0.7, serialization_alias="temperatura_geracao")
    simultaneous_requests: int = Field(default=4, serialization_alias="simultaneas")


class AdaptbookConfiguration(BaseModel):
    """Agrupa a configuração que será gravada como YAML em uma área de trabalho.

    Exemplo: ``AdaptbookConfiguration(book=BookSettings(file_name="livro.pdf"))``.
    """

    model_config = ConfigDict(populate_by_name=True)

    book: BookSettings = Field(serialization_alias="livro")
    model: ModelSettings = Field(default_factory=ModelSettings, serialization_alias="modelo")


def create_initial_configuration(source_pdf: Path) -> AdaptbookConfiguration:
    """Cria a configuração inicial sem registrar nenhum dado sensível.

    Exemplo: ``create_initial_configuration(Path("livro.pdf"))``.
    """

    return AdaptbookConfiguration(book=BookSettings(file_name=source_pdf.name))
