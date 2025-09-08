#!/usr/bin/env python
"""
Test script to check Django admin URLs for custom user model
"""
import os
import sys
import django

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

def test_admin_urls():
    print("Testing Django Admin URLs for Custom User Model")
    print("=" * 50)
    
    # Get the custom user model
    User = get_user_model()
    print(f"Custom User Model: {User}")
    print(f"App Label: {User._meta.app_label}")
    print(f"Model Name: {User._meta.model_name}")
    
    # Try to get the content type
    try:
        content_type = ContentType.objects.get_for_model(User)
        print(f"Content Type: {content_type}")
    except Exception as e:
        print(f"Error getting content type: {e}")
    
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
        except Exception as e:
            print(f"✗ {pattern} -> Error: {e}")
    
    # Test the problematic URL
    try:
        url = reverse('admin:auth_user_changelist')
        print(f"✓ admin:auth_user_changelist -> {url}")
    except Exception as e:
        print(f"✗ admin:auth_user_changelist -> Error: {e}")
        print("This is expected for custom user models")

if __name__ == '__main__':
    test_admin_urls()
