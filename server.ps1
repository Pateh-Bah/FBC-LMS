# Set environment variables and activate venv if present
$ErrorActionPreference = "Stop"
$env:DJANGO_SETTINGS_MODULE = "library_system.settings"

$venvActivate = Join-Path $PSScriptRoot "venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Activating virtual environment..."
    . $venvActivate
}

function Start-Development {
    Write-Host "Starting development server..."
    python manage.py runserver 127.0.0.1:8000
}

function Start-Production {
    Write-Host "Starting production server..."
    # Collect static files
    python manage.py collectstatic --noinput
    # Start Waitress server
    python production.py
}

# Get command line argument
$environment = $args[0]

if ($environment -eq "dev") {
    Start-Development
}
elseif ($environment -eq "prod") {
    Start-Production
}
else {
    Write-Host "Please specify 'dev' or 'prod' as an argument"
    Write-Host "Example: .\server.ps1 prod"
}
