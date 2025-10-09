"""
Health check endpoint for Vercel deployment
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

def handler(request):
    """
    Simple health check handler
    """
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
        'body': '{"status": "ok", "message": "Django FBC-LMS is running", "timestamp": "' + str(os.environ.get("VERCEL_REGION", "unknown")) + '"}'
    }
