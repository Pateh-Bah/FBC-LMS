#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')

# Setup Django
django.setup()

from django.template.loader import render_to_string
from fbc_users.system_settings import SystemSettings

def test_system_settings_template():
    """Test the system settings template rendering"""
    print("Testing system settings template...")
    
    try:
        # Get or create system settings
        settings_obj, created = SystemSettings.objects.get_or_create(id=1)
        print(f"SystemSettings object: {settings_obj}")
        print(f"System name: {settings_obj.system_name}")
        print(f"Primary color: {settings_obj.primary_color}")
        
        # Test template rendering
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Get a test user (admin user)
        try:
            test_user = User.objects.filter(is_superuser=True).first()
            if not test_user:
                test_user = User.objects.first()
        except:
            test_user = None
            
        context = {
            'settings': settings_obj,
            'error': None,
            'message': None,
            'user': test_user,
            'system_name': settings_obj.system_name if settings_obj else 'FBC Library System',
        }
        
        html = render_to_string('dashboard/system_settings.html', context)
        print(f"Template rendered successfully! Length: {len(html)} characters")
        
        # Check if the template contains key elements
        if 'System Settings' in html:
            print("✓ Title found in template")
        else:
            print("✗ Title not found in template")
            
        if settings_obj.system_name in html:
            print(f"✓ System name '{settings_obj.system_name}' found in template")
        else:
            print(f"✗ System name '{settings_obj.system_name}' not found in template")
            
        if settings_obj.primary_color in html:
            print(f"✓ Primary color '{settings_obj.primary_color}' found in template")
        else:
            print(f"✗ Primary color '{settings_obj.primary_color}' not found in template")
            
        print("Template test completed successfully!")
        
    except Exception as e:
        print(f"Error testing template: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_system_settings_template()
