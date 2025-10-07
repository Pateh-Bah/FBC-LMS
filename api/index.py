# api/index.py
# This file acts as the entry point for the Vercel serverless function.

# The `application` object is the standard WSGI entry point.
# Vercel's Python runtime knows how to handle it automatically.
from library_system.wsgi import application

# Vercel will look for a WSGI app named 'app' or 'application'.
# By importing it here, we expose it to the Vercel runtime.
app = application