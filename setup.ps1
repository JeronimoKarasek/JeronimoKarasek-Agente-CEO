param(
    [switch]$RecreateVenv
)

$ErrorActionPreference = 'Stop'

if ($RecreateVenv -and (Test-Path .\.venv)) { Remove-Item -Recurse -Force .\.venv }

if (-not (Test-Path .\.venv)) {
    python -m venv .venv
}

. .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install

Write-Host "Environment ready. Start with:`nuvicorn app.main:app --reload --port 8080" -ForegroundColor Green
