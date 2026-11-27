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

Invoke-PythonCheck @("-m", "coverage", "erase")
Invoke-PythonCheck @("-m", "coverage", "run", "-m", "pytest")
Invoke-PythonCheck @("-m", "coverage", "report", "--fail-under=80")
