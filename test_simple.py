import sys
import os
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Django project directory: {os.path.exists('manage.py')}")

try:
    import django
    print(f"Django version: {django.VERSION}")
    print(f"Django installed: True")
except ImportError:
    print("Django not installed")

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
    django.setup()
    print("Django setup successful")
    
    from django.urls import reverse
    print("Django URLs imported successfully")
    
    # Test a simple URL
    try:
        url = reverse('admin:index')
        print(f"Admin URL: {url}")
    except Exception as e:
        print(f"Admin URL error: {e}")
        
except Exception as e:
    print(f"Django setup error: {e}")
    import traceback
    traceback.print_exc()
