"""
Vercel serverless function handler for Django
"""
import os
import sys
import traceback
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Set environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings_vercel')
os.environ.setdefault('VERCEL_DEPLOYMENT', 'true')

# Import Django and configure
import django
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, JsonResponse

# Configure Django
django.setup()

# Get WSGI application
application = get_wsgi_application()

# Debug flag
DEBUG = os.getenv('DEBUG', 'False') == 'True'

def handler(request):
    """
    Vercel serverless function handler
    """
    try:
        # Extract request details
        method = request.get('method', 'GET')
        path = request.get('path', '/')
        query = request.get('query', {})
        cookies = request.get('cookies', {})
        body = request.get('body', '')
        headers = request.get('headers', {})

        # Debug logging
        print(f"[vercel-serverless] Request: method={method} path={path}")
        if DEBUG:
            print(f"[vercel-serverless] Headers: {headers}")
            print(f"[vercel-serverless] Query: {query}")
            print(f"[vercel-serverless] Cookies: {cookies}")

        # Health check endpoints
        if path in ['/__health', '/__alive', '/api/health']:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': '{"status": "ok", "path": "%s", "method": "%s"}' % (path, method)
            }

        # Static files handling
        if path.startswith('/static/'):
            try:
                static_file = project_root / 'staticfiles' / path[8:]
                if static_file.exists() and static_file.is_file():
                    with open(static_file, 'rb') as f:
                        content = f.read()
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/octet-stream'},
                        'body': content,
                        'isBase64Encoded': True
                    }
            except Exception as e:
                print(f"[vercel-serverless] Static file error: {e}")

        # Import necessary Django components
        from django.test import Client
        from django.conf import settings

        # Create Django test client
        client = Client()
        
        # Set cookies from request
        for key, value in cookies.items():
            client.cookies[key] = value

        # Handle different HTTP methods
        if method == 'GET':
            response = client.get(path, query)
        elif method == 'POST':
            content_type = headers.get('content-type', 'application/x-www-form-urlencoded')
            response = client.post(path, body, content_type=content_type)
        elif method == 'PUT':
            response = client.put(path, body, content_type='application/json')
        elif method == 'DELETE':
            response = client.delete(path)
        else:
            response = HttpResponse('Method not allowed', status=405)
        
        # Convert Django response to Vercel response format
        response_headers = dict(response.items())
        response_headers['X-Powered-By'] = 'Vercel'
        
        return {
            'statusCode': response.status_code,
            'headers': response_headers,
            'body': response.content.decode('utf-8')
        }
        
    except Exception as e:
        # Detailed error response in debug mode
        error_details = {
            'error': str(e),
            'traceback': traceback.format_exc() if DEBUG else None,
            'path': path if 'path' in locals() else 'unknown',
            'method': method if 'method' in locals() else 'unknown'
        }
        
        print(f"[vercel-serverless] Error: {error_details}")
        
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': JsonResponse(error_details, safe=False).content.decode('utf-8') if DEBUG else '{"error": "Internal Server Error"}'
        }
