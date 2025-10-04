web: gunicorn library_system.wsgi:application --workers 3 --threads 2 --worker-class=gthread --bind 0.0.0.0:$PORT --log-file=- --access-logfile=- --error-logfile=- --capture-output
