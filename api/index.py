"""
Vercel serverless function handler for Django
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings_vercel')

# Import Django
import django
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse

# Configure Django
django.setup()

# Get WSGI application
application = get_wsgi_application()

def handler(request):
    """
    Vercel serverless function handler
    """
    try:
        # Basic request diagnostics to help debug routing issues on Vercel
        method = request.get('method', 'GET')
        path = request.get('path', '/')
        print(f"[vercel-serverless] Received request method={method} path={path}")

        # Simple health-check endpoint to confirm the serverless function is reachable
        if path in ['/__health', '/__alive']:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': '{"ok": true, "path": "%s", "method": "%s"}' % (path, method)
            }

        # Import necessary Django components
        from django.test import Client
        from django.conf import settings

        # Create Django test client
        client = Client()
        
        # Handle different HTTP methods
        if method == 'GET':
            response = client.get(path)
        elif method == 'POST':
            data = request.get('body', {})
            response = client.post(path, data=data)
        elif method == 'PUT':
            data = request.get('body', {})
            response = client.put(path, data=data, content_type='application/json')
        elif method == 'DELETE':
            response = client.delete(path)
        else:
            response = HttpResponse('Method not allowed', status=405)
        
        # Convert Django response to Vercel response format
        return {
            'statusCode': response.status_code,
            'headers': dict(response.items()),
            'body': response.content.decode('utf-8')
        }
        
    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'Internal Server Error: {str(e)}'
        }
