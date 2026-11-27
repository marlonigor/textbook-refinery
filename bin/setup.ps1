$ErrorActionPreference = "Stop"
$projectPath = Split-Path -Parent $PSScriptRoot
$environmentPath = Join-Path $projectPath ".venv"

if (-not (Test-Path -LiteralPath $environmentPath)) {
    py -3.13 -m venv $environmentPath
}

$pythonPath = Join-Path $environmentPath "Scripts\python.exe"
& $pythonPath -m pip install --require-virtualenv -e "${projectPath}[dev]"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
