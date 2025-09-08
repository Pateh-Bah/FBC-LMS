$ErrorActionPreference = "Stop"

# Create venv if missing
if (-not (Test-Path "$PSScriptRoot\venv\Scripts\Activate.ps1")) {
    Write-Host "Creating virtual environment..."
    python -m venv "$PSScriptRoot\venv"
}

# Activate venv
Write-Host "Activating virtual environment..."
. "$PSScriptRoot\venv\Scripts\Activate.ps1"

# Upgrade pip and install requirements
python -m pip install --upgrade pip
if (Test-Path "$PSScriptRoot\requirements.txt") {
    Write-Host "Installing dependencies from requirements.txt..."
    pip install -r "$PSScriptRoot\requirements.txt"
}

Write-Host "Environment ready. Use ./run.ps1 dev to start the server."