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

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from fbc_users.views import system_settings_view

def test_system_settings_page():
    """Test the system settings view and template rendering with proper request context"""
    print("Testing system settings page with request context...")
    
    try:
        # Create a test request
        factory = RequestFactory()
        request = factory.get('/users/system-settings/')
        
        # Get a superuser for testing
        User = get_user_model()
        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                print("No superuser found, creating test admin...")
                admin_user = User.objects.create_superuser(
                    username='testadmin',
                    email='admin@test.com',
                    password='testpass123',
                    first_name='Test',
                    last_name='Admin'
                )
        except Exception as e:
            print(f"Error getting admin user: {e}")
            return
        
        request.user = admin_user
        
        # Call the view
        response = system_settings_view(request)
        
        print(f"Response status code: {response.status_code}")
        print(f"Response content length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Check if the template contains key elements
            if 'System Settings' in content:
                print("✓ Title found in rendered page")
            else:
                print("✗ Title not found in rendered page")
                
            if 'FBC Library System' in content:
                print("✓ System name found in rendered page")
            else:
                print("✗ System name not found in rendered page")
                
            if 'primary_color' in content:
                print("✓ Primary color field found in rendered page")
            else:
                print("✗ Primary color field not found in rendered page")
                
            if len(content) > 1000:
                print("✓ Page content is substantial (not blank)")
            else:
                print("✗ Page content is too short (possibly blank)")
                print(f"Content preview: {content[:500]}...")
        else:
            print(f"✗ View returned error status: {response.status_code}")
            
        print("System settings page test completed!")
        
    except Exception as e:
        print(f"Error testing system settings page: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_system_settings_page()
