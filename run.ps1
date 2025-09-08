$ErrorActionPreference = "Stop"
$env:DJANGO_SETTINGS_MODULE = "library_system.settings"

# Auto-activate local venv if present
$venvActivate = Join-Path $PSScriptRoot "venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Activating virtual environment..."
    . $venvActivate
}

if ($args[0] -eq "dev") {
    Write-Host "Starting development server..."
    python manage.py runserver
}
else {
    Write-Host "Starting production server with Gunicorn..."
    gunicorn library_system.wsgi:application -c gunicorn.conf.py
}
