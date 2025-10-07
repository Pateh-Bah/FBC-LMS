#!/bin/bash
set -e

echo "Checking for Vercel-specific requirements file..."
if [ -f requirements-vercel.txt ]; then
	echo "Installing requirements-vercel.txt"
	python -m pip install -r requirements-vercel.txt
else
	echo "Installing requirements.txt"
	python -m pip install -r requirements.txt
fi

# Ensure a SECRET_KEY exists during build (temporary value for collectstatic)
if [ -z "${SECRET_KEY}" ]; then
	echo "No SECRET_KEY set - generating temporary key for build"
	export SECRET_KEY=$(python - <<'PY'
import secrets
print(secrets.token_urlsafe(50))
PY
)
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build script finished successfully"