# Set environment variables
$env:DJANGO_SETTINGS_MODULE = "library_system.settings"

# Install required packages if not already installed
python -m pip install waitress

Write-Host "Starting WSGI server..."
# Run the WSGI server using waitress
python -m waitress-serve --host=127.0.0.1 --port=8000 library_system.wsgi:application
