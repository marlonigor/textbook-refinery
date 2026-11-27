$ErrorActionPreference = "Stop"
$projectPath = Split-Path -Parent $PSScriptRoot
$pythonPath = Join-Path $projectPath ".venv\Scripts\python.exe"

& "$PSScriptRoot\check.ps1"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
& $pythonPath -m pip wheel . --no-deps --wheel-dir dist
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
