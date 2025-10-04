#!/usr/bin/env python
"""
Test script to verify X-Frame-Options header is correctly set
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.conf import settings
from django.test import Client
from django.urls import reverse

def test_x_frame_options():
    """Test that X-Frame-Options header is correctly set"""
    print("=== X-Frame-Options Header Test ===\n")
    
    # Check Django settings
    print("Django Settings:")
    print(f"  X_FRAME_OPTIONS: {getattr(settings, 'X_FRAME_OPTIONS', 'Not set')}")
    print(f"  SECURE_BROWSER_XSS_FILTER: {getattr(settings, 'SECURE_BROWSER_XSS_FILTER', 'Not set')}")
    print()
    
    # Test with Django test client
    client = Client()
    
    try:
        # Test the preview page
        response = client.get('/books/12/preview/')
        print("Preview page response:")
        print(f"  Status: {response.status_code}")
        
        # Check X-Frame-Options header
        x_frame_header = response.get('X-Frame-Options', 'Not found')
        print(f"  X-Frame-Options: {x_frame_header}")
        
        if x_frame_header == 'SAMEORIGIN':
            print("  ✅ X-Frame-Options is correctly set to SAMEORIGIN")
        elif x_frame_header == 'DENY':
            print("  ❌ X-Frame-Options is still set to DENY - SecurityMiddleware override not fixed")
        else:
            print(f"  ⚠️  X-Frame-Options is set to: {x_frame_header}")
        
        print()
        
        # Test the reader page
        response = client.get('/books/12/read/')
        print("Reader page response:")
        print(f"  Status: {response.status_code}")
        
        x_frame_header = response.get('X-Frame-Options', 'Not found')
        print(f"  X-Frame-Options: {x_frame_header}")
        
        if x_frame_header == 'SAMEORIGIN':
            print("  ✅ X-Frame-Options is correctly set to SAMEORIGIN")
        elif x_frame_header == 'DENY':
            print("  ❌ X-Frame-Options is still set to DENY - SecurityMiddleware override not fixed")
        else:
            print(f"  ⚠️  X-Frame-Options is set to: {x_frame_header}")
            
    except Exception as e:
        print(f"Error testing pages: {e}")
        print("Make sure the Django development server is running")
    
    print("\n=== Test Complete ===")
    print("\nIf X-Frame-Options is still DENY:")
    print("1. Restart Django development server")
    print("2. Clear browser cache")
    print("3. Try accessing pages again")

if __name__ == '__main__':
    test_x_frame_options()
