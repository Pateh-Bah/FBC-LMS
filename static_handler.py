"""
Static files handler for Vercel deployment
"""
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.utils.six import BytesIO
from django.views.static import serve

def static_handler(request, path):
    """
    Handle static files for Vercel deployment
    """
    # Check if file exists in staticfiles directory
    static_path = os.path.join(settings.STATIC_ROOT, path)
    
    if os.path.exists(static_path):
        return serve(request, path, document_root=settings.STATIC_ROOT)
    else:
        # Try staticfiles directory in project root
        project_static_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'staticfiles', path)
        if os.path.exists(project_static_path):
            return serve(request, path, document_root=os.path.join(os.path.dirname(settings.BASE_DIR), 'staticfiles'))
    
    raise Http404("Static file not found")
