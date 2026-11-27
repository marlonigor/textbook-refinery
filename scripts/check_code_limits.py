"""Verifica limites locais de tamanho para manter módulos e funções focados."""

import ast
from pathlib import Path

MAX_FILE_LINES = 500
MAX_FUNCTION_LINES = 20


def _python_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.py") if "__pycache__" not in path.parts)


def _file_violations(path: Path) -> list[str]:
    line_count = len(path.read_text(encoding="utf-8").splitlines())
    return [] if line_count <= MAX_FILE_LINES else [f"{path}: {line_count} linhas"]


def _function_violations(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    functions = (
        node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
    )
    return [message for node in functions if (message := _function_message(path, node)) is not None]


def _function_message(path: Path, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str | None:
    end_line = node.end_lineno or node.lineno
    line_count = end_line - node.lineno + 1
    if line_count <= MAX_FUNCTION_LINES:
        return None
    return f"{path}:{node.lineno} {node.name} tem {line_count} linhas"


def main() -> int:
    """Retorna falha quando algum limite automático é ultrapassado.

    Exemplo: ``python scripts/check_code_limits.py``.
    """

    files = _python_files(Path("src"))
    violations = [
        message for path in files for message in _file_violations(path) + _function_violations(path)
    ]
    if not violations:
        return 0
    print("\n".join(violations))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
