"""
WSGI config for library_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings_vercel')

# Get base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Get WSGI application
application = get_wsgi_application()

# Add WhiteNoise for static files
application = WhiteNoise(application)
application.add_files(os.path.join(BASE_DIR, 'staticfiles'), prefix='static/')
