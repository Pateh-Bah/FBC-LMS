#!/usr/bin/env python
"""
Simple test to verify that the admin URL fix is working correctly.
"""
import os
import sys
import django

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.urls import reverse, NoReverseMatch
from django.contrib.auth import get_user_model

def test_admin_urls():
    print("Testing Django Admin URLs after fix...")
    print("=" * 50)
    
    # Get the custom user model
    User = get_user_model()
    print(f"Custom User Model: {User}")
    print(f"App Label: {User._meta.app_label}")
    print(f"Model Name: {User._meta.model_name}")
    
    # Test different URL patterns
    url_patterns = [
        'admin:index',
        f'admin:{User._meta.app_label}_{User._meta.model_name}_changelist',
        f'admin:{User._meta.app_label}_{User._meta.model_name}_add',
    ]
    
    for pattern in url_patterns:
        try:
            url = reverse(pattern)
            print(f"✓ {pattern} -> {url}")
        except NoReverseMatch as e:
            print(f"✗ {pattern} -> Error: {e}")
    
    # Test the problematic URL that should now be handled gracefully
    print("\nTesting problematic URLs:")
    try:
        url = reverse('admin:auth_user_changelist')
        print(f"✓ admin:auth_user_changelist -> {url}")
    except NoReverseMatch as e:
        print(f"✗ admin:auth_user_changelist -> Error: {e}")
        print("This should now be handled gracefully by the fix")

if __name__ == '__main__':
    test_admin_urls()
