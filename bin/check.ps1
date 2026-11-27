$ErrorActionPreference = "Stop"
$projectPath = Split-Path -Parent $PSScriptRoot
$pythonPath = Join-Path $projectPath ".venv\Scripts\python.exe"

function Invoke-PythonCheck {
    param([string[]]$Arguments)

    & $pythonPath @Arguments
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

Invoke-PythonCheck @("-m", "ruff", "format", "--check", $projectPath)
Invoke-PythonCheck @("-m", "ruff", "check", $projectPath)
Invoke-PythonCheck @("-m", "mypy")
Invoke-PythonCheck @("$projectPath\scripts\check_code_limits.py")
& "$PSScriptRoot\test.ps1"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
Invoke-PythonCheck @("-m", "pip", "wheel", ".", "--no-deps", "--wheel-dir", "build")
